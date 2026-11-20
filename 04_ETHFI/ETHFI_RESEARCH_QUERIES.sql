-- Ether.fi investment-research SQL layer
-- Dialect: DuckDB / PostgreSQL-compatible. Replace :as_of_date and table names
-- with the names used in the warehouse or Looker Studio extract.
--
-- Required tables:
--   ethfi_daily(date, tvl_parent_usd, tvl_stake_usd, tvl_liquid_usd,
--               fees_gross_usd, protocol_revenue_usd, holders_revenue_usd,
--               revenue_capture_ratio)
--   ethfi_kpi_latest(as_of_date, price_usd, market_cap_usd, fdv_usd,
--                    circulating_supply, max_supply, tvl_parent_usd,
--                    fees_30d_usd, revenue_30d_usd, holders_revenue_30d_usd,
--                    revenue_capture_ratio_30d, tvl_change_7d, tvl_change_30d)
--   ethfi_source_register(source_id, provider, dataset, url, as_of,
--                         quality_status, limitations)

-- 1. Daily operating and economic baseline.
WITH ordered AS (
    SELECT
        date,
        tvl_parent_usd,
        tvl_stake_usd,
        tvl_liquid_usd,
        fees_gross_usd,
        protocol_revenue_usd,
        holders_revenue_usd,
        CASE
            WHEN fees_gross_usd > 0 THEN protocol_revenue_usd / fees_gross_usd
        END AS revenue_capture_ratio,
        LAG(tvl_parent_usd, 7) OVER (ORDER BY date) AS tvl_7d_ago,
        LAG(tvl_parent_usd, 30) OVER (ORDER BY date) AS tvl_30d_ago
    FROM ethfi_daily
)
SELECT
    date,
    tvl_parent_usd,
    fees_gross_usd,
    protocol_revenue_usd,
    holders_revenue_usd,
    revenue_capture_ratio,
    CASE WHEN tvl_7d_ago > 0 THEN tvl_parent_usd / tvl_7d_ago - 1 END AS tvl_change_7d,
    CASE WHEN tvl_30d_ago > 0 THEN tvl_parent_usd / tvl_30d_ago - 1 END AS tvl_change_30d
FROM ordered
ORDER BY date;

-- 2. Rolling 30-day economics: gross fees, protocol revenue and holder revenue.
SELECT
    MAX(date) AS as_of_date,
    SUM(COALESCE(fees_gross_usd, 0)) AS fees_30d_usd,
    SUM(COALESCE(protocol_revenue_usd, 0)) AS protocol_revenue_30d_usd,
    SUM(COALESCE(holders_revenue_usd, 0)) AS holders_revenue_30d_usd,
    CASE
        WHEN SUM(COALESCE(fees_gross_usd, 0)) > 0
        THEN SUM(COALESCE(protocol_revenue_usd, 0)) / SUM(COALESCE(fees_gross_usd, 0))
    END AS revenue_capture_ratio_30d
FROM ethfi_daily
WHERE date > (SELECT MAX(date) FROM ethfi_daily) - INTERVAL '30 days';

-- 3. Simple valuation bridge. This is a screening multiple, not a DCF.
SELECT
    k.as_of_date,
    k.market_cap_usd,
    k.fdv_usd,
    k.fees_30d_usd * 12 AS annualised_gross_fees_usd,
    k.revenue_30d_usd * 12 AS annualised_protocol_revenue_usd,
    CASE WHEN k.revenue_30d_usd > 0
         THEN k.market_cap_usd / (k.revenue_30d_usd * 12)
    END AS market_cap_to_annualised_revenue,
    CASE WHEN k.fees_30d_usd > 0
         THEN k.market_cap_usd / (k.fees_30d_usd * 12)
    END AS market_cap_to_annualised_gross_fees
FROM ethfi_kpi_latest k;

-- 4. Token supply and dilution check.
SELECT
    as_of_date,
    price_usd,
    circulating_supply,
    max_supply,
    max_supply - circulating_supply AS not_yet_circulating,
    CASE WHEN max_supply > 0 THEN circulating_supply / max_supply END AS float_ratio,
    CASE WHEN circulating_supply > 0 THEN market_cap_usd / circulating_supply END AS spot_price_check,
    fdv_usd / NULLIF(market_cap_usd, 0) - 1 AS fdv_premium_to_market_cap
FROM ethfi_kpi_latest;

-- 5. Weekly investment-case change report.
WITH current AS (
    SELECT * FROM ethfi_kpi_latest
), prior AS (
    SELECT *
    FROM ethfi_daily
    WHERE date <= (SELECT as_of_date FROM current) - INTERVAL '7 days'
    ORDER BY date DESC
    LIMIT 1
)
SELECT
    current.as_of_date,
    current.tvl_change_7d,
    current.tvl_change_30d,
    current.revenue_capture_ratio_30d,
    current.revenue_30d_usd,
    current.holders_revenue_30d_usd,
    current.tvl_parent_usd - prior.tvl_parent_usd AS tvl_delta_vs_7d_ago,
    CASE WHEN prior.tvl_parent_usd > 0
         THEN current.tvl_parent_usd / prior.tvl_parent_usd - 1
    END AS tvl_change_recomputed_7d,
    CASE
        WHEN current.tvl_change_7d > 0 AND current.revenue_30d_usd > 0 THEN 'improving'
        WHEN current.tvl_change_7d < 0 AND current.revenue_30d_usd <= 0 THEN 'deteriorating'
        ELSE 'mixed'
    END AS weekly_case_signal
FROM current
CROSS JOIN prior;

-- 6. Source-quality gate: do not publish a metric without a source and date.
SELECT
    source_id,
    provider,
    dataset,
    url,
    as_of,
    quality_status,
    limitations
FROM ethfi_source_register
WHERE url IS NULL
   OR as_of IS NULL
   OR quality_status IS NULL
ORDER BY source_id;

-- Interpretation guardrails:
-- * TVL is adoption/capital-at-risk context, not revenue.
-- * Gross fees are not protocol revenue.
-- * Protocol revenue is not automatically token-holder cash flow.
-- * Buyback policy must be reconciled to executed on-chain transactions.
-- * Any valuation multiple should show both market cap and FDV, with the
--   relevant supply date and source.
