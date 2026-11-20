-- Macro and ETF-flow SQL for Looker / DuckDB.

-- Daily macro dashboard: risk-on, dollar and stablecoin context.
WITH latest AS (
    SELECT asset_id, MAX(date) AS as_of_date
    FROM market_macro_daily
    GROUP BY asset_id
)
SELECT
    m.asset_id,
    m.date,
    m.close_usd,
    m.return_1d,
    m.volume,
    m.market_cap_usd,
    CASE
        WHEN m.asset_id = 'USDT' THEN m.close_usd - 1.0
    END AS usdt_peg_deviation,
    CASE
        WHEN m.asset_id IN ('SPY', 'GPRO', 'LYFT') THEN 'equity'
        WHEN m.asset_id = 'DXY' THEN 'macro'
        WHEN m.asset_id = 'USDT' THEN 'stablecoin'
    END AS macro_bucket
FROM market_macro_daily m
JOIN latest l ON l.asset_id = m.asset_id AND l.as_of_date = m.date
ORDER BY macro_bucket, m.asset_id;

-- ETF flows by product and day. Empty net_flow means not reported, not zero.
SELECT
    date,
    product,
    SUM(CASE WHEN fund <> 'Total' THEN COALESCE(net_flow_usd_m, 0) END) AS sum_reported_funds_usd_m,
    MAX(CASE WHEN fund = 'Total' THEN net_flow_usd_m END) AS published_total_usd_m,
    COUNT(*) FILTER (WHERE net_flow_usd_m IS NOT NULL) AS reported_rows,
    COUNT(*) FILTER (WHERE net_flow_usd_m IS NULL) AS not_reported_rows,
    CASE
        WHEN COUNT(*) FILTER (WHERE net_flow_usd_m IS NULL) > 0 THEN 'partial_or_not_reported'
        ELSE 'reported'
    END AS flow_status
FROM etf_flows_daily
GROUP BY date, product
ORDER BY date, product;

-- Seven-day ETF-flow momentum excluding days not yet reported.
SELECT
    product,
    SUM(net_flow_usd_m) AS net_flow_7d_usd_m,
    AVG(net_flow_usd_m) AS average_daily_flow_usd_m,
    COUNT(*) AS reported_days
FROM etf_flows_daily
WHERE fund = 'Total'
  AND net_flow_usd_m IS NOT NULL
  AND date > (SELECT MAX(date) FROM etf_flows_daily WHERE net_flow_usd_m IS NOT NULL) - INTERVAL '7 days'
GROUP BY product;

-- Cross-asset signal table. This is descriptive, not a trading signal.
WITH latest AS (
    SELECT asset_id, close_usd, return_1d
    FROM market_macro_kpi_latest
)
SELECT
    MAX(CASE WHEN asset_id = 'SPY' THEN return_1d END) AS spy_return_1d,
    MAX(CASE WHEN asset_id = 'DXY' THEN return_1d END) AS dxy_return_1d,
    MAX(CASE WHEN asset_id = 'GPRO' THEN return_1d END) AS gpro_return_1d,
    MAX(CASE WHEN asset_id = 'LYFT' THEN return_1d END) AS lyft_return_1d,
    MAX(CASE WHEN asset_id = 'USDT' THEN close_usd END) - 1.0 AS usdt_peg_deviation
FROM latest;
