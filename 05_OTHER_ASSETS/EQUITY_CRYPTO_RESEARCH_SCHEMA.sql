-- DuckDB/PostgreSQL-compatible schema for the combined dashboard.

CREATE TABLE IF NOT EXISTS asset_master (
    asset_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    ticker VARCHAR,
    asset_class VARCHAR NOT NULL, -- token, network, equity
    sector VARCHAR,
    status VARCHAR,
    case_type VARCHAR,
    source_url VARCHAR,
    as_of_date DATE
);

CREATE TABLE IF NOT EXISTS market_daily (
    asset_id VARCHAR,
    date DATE,
    price_usd DOUBLE,
    market_cap_usd DOUBLE,
    enterprise_value_usd DOUBLE,
    volume_usd DOUBLE,
    shares_outstanding DOUBLE,
    circulating_supply DOUBLE,
    max_supply DOUBLE,
    PRIMARY KEY (asset_id, date)
);

CREATE TABLE IF NOT EXISTS operating_daily (
    asset_id VARCHAR,
    date DATE,
    tvl_usd DOUBLE,
    gross_fees_usd DOUBLE,
    protocol_revenue_usd DOUBLE,
    holder_revenue_usd DOUBLE,
    revenue_usd DOUBLE,
    gross_bookings_usd DOUBLE,
    rides DOUBLE,
    active_riders DOUBLE,
    cameras_shipped DOUBLE,
    subscribers DOUBLE,
    free_cash_flow_usd DOUBLE,
    adjusted_ebitda_usd DOUBLE,
    quality_status VARCHAR,
    source_id VARCHAR,
    PRIMARY KEY (asset_id, date)
);

CREATE TABLE IF NOT EXISTS tokenomics_daily (
    asset_id VARCHAR,
    date DATE,
    circulating_supply DOUBLE,
    max_supply DOUBLE,
    unlocked_supply DOUBLE,
    next_30d_unlock DOUBLE,
    next_12m_unlock DOUBLE,
    insider_allocation_pct DOUBLE,
    treasury_allocation_pct DOUBLE,
    holder_value_accrual VARCHAR,
    source_id VARCHAR
);

CREATE TABLE IF NOT EXISTS ownership_snapshot (
    asset_id VARCHAR,
    as_of_date DATE,
    holder_name VARCHAR,
    holder_type VARCHAR, -- insider, founder, institution, fund, strategic
    shares_or_tokens DOUBLE,
    ownership_pct DOUBLE,
    voting_pct DOUBLE,
    filing_type VARCHAR,
    source_url VARCHAR,
    quality_status VARCHAR
);

CREATE TABLE IF NOT EXISTS financials_annual (
    asset_id VARCHAR,
    fiscal_year INTEGER,
    revenue_usd DOUBLE,
    gross_profit_usd DOUBLE,
    operating_income_usd DOUBLE,
    net_income_usd DOUBLE,
    adjusted_ebitda_usd DOUBLE,
    free_cash_flow_usd DOUBLE,
    cash_usd DOUBLE,
    debt_usd DOUBLE,
    shares_diluted DOUBLE,
    source_url VARCHAR,
    quality_status VARCHAR
);

CREATE TABLE IF NOT EXISTS valuation_snapshot (
    asset_id VARCHAR,
    as_of_date DATE,
    market_cap_usd DOUBLE,
    enterprise_value_usd DOUBLE,
    annual_revenue_usd DOUBLE,
    annual_protocol_revenue_usd DOUBLE,
    annual_fees_usd DOUBLE,
    annual_fcf_usd DOUBLE,
    ev_sales DOUBLE,
    ev_revenue DOUBLE,
    ev_ebitda DOUBLE,
    price_to_fcf DOUBLE,
    market_cap_to_tvl DOUBLE,
    fdv_to_protocol_revenue DOUBLE,
    valuation_note VARCHAR
);

CREATE TABLE IF NOT EXISTS risk_catalyst_log (
    asset_id VARCHAR,
    event_date DATE,
    event_type VARCHAR, -- catalyst, risk, thesis_update, filing
    description VARCHAR,
    thesis_impact VARCHAR, -- strengthen, weaken, neutral
    trigger_or_falsifier VARCHAR,
    source_url VARCHAR
);

-- Dashboard calculations.
SELECT
    a.name,
    a.ticker,
    v.as_of_date,
    v.ev_sales,
    v.ev_ebitda,
    v.price_to_fcf,
    v.market_cap_to_tvl,
    v.fdv_to_protocol_revenue,
    CASE
        WHEN a.asset_class = 'equity' THEN COALESCE(v.ev_revenue, v.ev_sales)
        WHEN a.asset_class = 'token' THEN v.fdv_to_protocol_revenue
    END AS primary_multiple,
    a.status
FROM asset_master a
JOIN valuation_snapshot v USING (asset_id)
ORDER BY primary_multiple;

-- Weekly change table.
WITH current_week AS (
    SELECT asset_id, MAX(date) AS as_of_date
    FROM operating_daily
    GROUP BY asset_id
)
SELECT
    o.asset_id,
    c.as_of_date,
    o.tvl_usd,
    o.protocol_revenue_usd,
    o.revenue_usd,
    o.active_riders,
    o.subscribers,
    o.cameras_shipped
FROM operating_daily o
JOIN current_week c USING (asset_id)
WHERE o.date >= c.as_of_date - INTERVAL '7 days';
