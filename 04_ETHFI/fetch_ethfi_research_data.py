#!/usr/bin/env python3
"""Fetch a reproducible baseline for the Ether.fi investment-research case.

Sources:
  * DefiLlama public API for TVL, fees, protocol revenue and holders revenue.
  * CoinGecko public API for ETHFI price and supply snapshot.
  * DefiLlama token-rights registry and public unlock page for value-accrual
    and unlock context.

The script keeps gross fees, protocol revenue and holders revenue separate.
It does not infer protocol profitability or token-holder cash flow when a
source does not publish the required cost or distribution data.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
LLAMA_BASE = "https://api.llama.fi"
COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/coins/ether-fi?localization=false&tickers=false&"
    "market_data=true&community_data=false&developer_data=false&sparkline=false"
)
UNLOCK_PAGE = "https://defillama.com/unlocks/ether.fi"
TOKEN_RIGHTS_URL = "https://api.llama.fi/token-rights"

DAILY_OUTPUT = BASE_DIR / "ETHFI_DAILY.csv"
KPI_OUTPUT = BASE_DIR / "ETHFI_KPI_LATEST.csv"
TOKEN_OUTPUT = BASE_DIR / "ETHFI_TOKENOMICS.csv"
SOURCES_OUTPUT = BASE_DIR / "ETHFI_SOURCE_REGISTER.csv"
RAW_DIR = BASE_DIR / "raw"


def get_json(url: str, retries: int = 5) -> dict | list:
    last_error: Exception | None = None
    for attempt in range(retries):
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "ETHFI-Investment-Research/1.0", "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                return json.load(response)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
            last_error = error
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Request failed: {url}: {last_error}")


def get_text(url: str, retries: int = 5) -> str:
    last_error: Exception | None = None
    for attempt in range(retries):
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "ETHFI-Investment-Research/1.0", "Accept": "text/html"},
        )
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                return response.read().decode("utf-8", "ignore")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
            last_error = error
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Request failed: {url}: {last_error}")


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def daily_chart(chart: list[list[float | int]]) -> dict[str, float]:
    """Collapse timestamp/value pairs to the last observation per UTC date."""
    result: dict[str, float] = {}
    for item in chart or []:
        if len(item) < 2:
            continue
        timestamp, value = item[0], item[1]
        try:
            date = dt.datetime.fromtimestamp(float(timestamp), tz=dt.timezone.utc).date().isoformat()
            result[date] = float(value) if value is not None else None
        except (TypeError, ValueError, OSError):
            continue
    return result


def fetch_protocol(slug: str) -> dict:
    payload = get_json(f"{LLAMA_BASE}/protocol/{slug}")
    assert isinstance(payload, dict)
    write_json(RAW_DIR / f"defillama_protocol_{slug.replace('.', '_')}.json", payload)
    return payload


def fetch_fee_summary(data_type: str) -> dict:
    payload = get_json(f"{LLAMA_BASE}/summary/fees/ether.fi?dataType={data_type}")
    assert isinstance(payload, dict)
    write_json(RAW_DIR / f"defillama_{data_type}.json", payload)
    return payload


def parse_unlock_page(html: str) -> dict:
    def number(pattern: str) -> float | None:
        match = re.search(pattern, html)
        if not match:
            return None
        try:
            return float(match.group(1))
        except ValueError:
            return None

    meta = {
        "unlock_page_generated_at_utc": None,
        "unlock_page_circulating_supply": number(r'"meta":\{"gecko_id":"ether-fi","circSupply":([0-9.eE+-]+)'),
        "unlock_page_max_supply": number(r'"meta":\{"gecko_id":"ether-fi","circSupply":[0-9.eE+-]+,"maxSupply":([0-9.eE+-]+)'),
        "unlock_page_total_locked": number(r'"meta":\{"gecko_id":"ether-fi","circSupply":[0-9.eE+-]+,"maxSupply":[0-9.eE+-]+,"totalLocked":([0-9.eE+-]+)'),
        "unlock_page_mcap_usd": number(r'"meta":\{"gecko_id":"ether-fi","circSupply":[0-9.eE+-]+,"maxSupply":[0-9.eE+-]+,"totalLocked":[0-9.eE+-]+,"mcap":([0-9.eE+-]+)'),
    }
    generated = re.search(r'"generatedAtSec":([0-9]+)', html)
    if generated:
        meta["unlock_page_generated_at_utc"] = dt.datetime.fromtimestamp(int(generated.group(1)), tz=dt.timezone.utc).isoformat()
    sentence = re.search(r'"nextUnlockSentence":"([^"\\]*(?:\\.[^"\\]*)*)"', html)
    if sentence:
        meta["next_unlock_sentence"] = sentence.group(1).replace("\\u0026", "&").replace("\\\"", '"')
    return meta


def calculate_change(series: dict[str, float], latest_date: str, days: int) -> float | None:
    latest = series.get(latest_date)
    target_date = dt.date.fromisoformat(latest_date) - dt.timedelta(days=days)
    target = series.get(target_date.isoformat())
    if latest is None or target in (None, 0):
        return None
    return latest / target - 1.0


def main() -> None:
    RAW_DIR.mkdir(exist_ok=True)
    parent = fetch_protocol("ether.fi")
    stake = fetch_protocol("ether.fi-stake")
    liquid = fetch_protocol("ether.fi-liquid")
    fees = fetch_fee_summary("dailyFees")
    revenue = fetch_fee_summary("dailyRevenue")
    holders = fetch_fee_summary("dailyHoldersRevenue")
    coingecko = get_json(COINGECKO_URL)
    assert isinstance(coingecko, dict)
    write_json(RAW_DIR / "coingecko_ether-fi.json", coingecko)
    rights_payload = get_json(TOKEN_RIGHTS_URL)
    assert isinstance(rights_payload, list)
    rights = next(
        (row for row in rights_payload if row.get("Protocol Name", "").lower() in {"etherfi", "ether.fi"}),
        {},
    )
    write_json(RAW_DIR / "defillama_token_rights.json", rights)
    unlock_html = get_text(UNLOCK_PAGE)
    (RAW_DIR / "defillama_unlocks_ether_fi.html").write_text(unlock_html, encoding="utf-8")
    unlock = parse_unlock_page(unlock_html)

    tvl_parent = daily_chart([
        [row.get("date"), row.get("totalLiquidityUSD")]
        for row in parent.get("tvl", [])
    ])
    tvl_stake = daily_chart([
        [row.get("date"), row.get("totalLiquidityUSD")]
        for row in stake.get("tvl", [])
    ])
    tvl_liquid = daily_chart([
        [row.get("date"), row.get("totalLiquidityUSD")]
        for row in liquid.get("tvl", [])
    ])
    fee_daily = daily_chart(fees.get("totalDataChart", []))
    revenue_daily = daily_chart(revenue.get("totalDataChart", []))
    holders_daily = daily_chart(holders.get("totalDataChart", []))
    dates = sorted(set(tvl_parent) | set(fee_daily) | set(revenue_daily) | set(holders_daily))

    daily: list[dict] = []
    for date in dates:
        fee = fee_daily.get(date)
        protocol_revenue = revenue_daily.get(date)
        daily.append(
            {
                "date": date,
                "tvl_parent_usd": tvl_parent.get(date),
                "tvl_stake_usd": tvl_stake.get(date),
                "tvl_liquid_usd": tvl_liquid.get(date),
                "fees_gross_usd": fee,
                "protocol_revenue_usd": protocol_revenue,
                "holders_revenue_usd": holders_daily.get(date),
                "revenue_capture_ratio": protocol_revenue / fee if protocol_revenue is not None and fee else None,
                "source_tvl": "DefiLlama /protocol/ether.fi",
                "source_fees": "DefiLlama /summary/fees/ether.fi?dataType=dailyFees",
                "source_revenue": "DefiLlama /summary/fees/ether.fi?dataType=dailyRevenue",
                "quality_status": "independent_aggregator; methodology_review_required",
            }
        )

    latest_date = daily[-1]["date"]
    latest = daily[-1]
    latest["tvl_change_7d"] = calculate_change(tvl_parent, latest_date, 7)
    latest["tvl_change_30d"] = calculate_change(tvl_parent, latest_date, 30)
    for row in daily:
        row["tvl_change_7d"] = calculate_change(tvl_parent, row["date"], 7)
        row["tvl_change_30d"] = calculate_change(tvl_parent, row["date"], 30)

    market = coingecko.get("market_data", {})
    price = (market.get("current_price") or {}).get("usd")
    market_cap = (market.get("market_cap") or {}).get("usd")
    fully_diluted = (market.get("fully_diluted_valuation") or {}).get("usd")
    circulating = market.get("circulating_supply")
    total_supply = market.get("total_supply")
    max_supply = market.get("max_supply")
    tvl_current = latest.get("tvl_parent_usd")
    kpi = {
        "as_of_date": latest_date,
        "fetched_at_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "price_usd": price,
        "market_cap_usd": market_cap,
        "fdv_usd": fully_diluted,
        "circulating_supply": circulating,
        "total_supply": total_supply,
        "max_supply": max_supply,
        "tvl_parent_usd": tvl_current,
        "tvl_stake_usd": latest.get("tvl_stake_usd"),
        "tvl_liquid_usd": latest.get("tvl_liquid_usd"),
        "market_cap_to_tvl": market_cap / tvl_current if market_cap and tvl_current else None,
        "fees_24h_usd": fees.get("total24h"),
        "fees_7d_usd": fees.get("total7d"),
        "fees_30d_usd": fees.get("total30d"),
        "fees_1y_usd": fees.get("total1y"),
        "revenue_24h_usd": revenue.get("total24h"),
        "revenue_7d_usd": revenue.get("total7d"),
        "revenue_30d_usd": revenue.get("total30d"),
        "revenue_1y_usd": revenue.get("total1y"),
        "holders_revenue_30d_usd": holders.get("total30d"),
        "revenue_capture_ratio_30d": revenue.get("total30d") / fees.get("total30d") if fees.get("total30d") else None,
        "tvl_change_7d": latest.get("tvl_change_7d"),
        "tvl_change_30d": latest.get("tvl_change_30d"),
        "unlock_page_circulating_supply": unlock.get("unlock_page_circulating_supply"),
        "unlock_page_max_supply": unlock.get("unlock_page_max_supply"),
        "unlock_page_total_locked": unlock.get("unlock_page_total_locked"),
        "unlock_page_unlocked_pct": (
            1.0 - unlock["unlock_page_total_locked"] / unlock["unlock_page_max_supply"]
            if unlock.get("unlock_page_total_locked") is not None and unlock.get("unlock_page_max_supply")
            else None
        ),
        "next_unlock_sentence": unlock.get("next_unlock_sentence"),
        "token_rights_last_updated": rights.get("Last Updated"),
        "token_value_accrual": rights.get("Value Accrual"),
        "token_buyback_details": rights.get("Buyback Details"),
        "token_economic_rights": rights.get("Economic Rights (Summary)"),
        "token_fee_switch_status": rights.get("Fee Switch Status"),
        "token_equity_revenue_capture": rights.get("Equity Revenue Capture"),
        "quality_status": "baseline; key metrics cross-referenced across DefiLlama, CoinGecko and official Ether.fi materials",
    }

    token_rows = [
        {
            "category": "supply",
            "metric": "max_supply",
            "value": 1_000_000_000,
            "unit": "ETHFI",
            "as_of": latest_date,
            "source": "https://etherfi.gitbook.io/gov/ethfi-allocations",
            "quality_status": "official; last updated shown on source page",
            "note": "Official source says fully minted fixed supply; no further issuance.",
        },
        {
            "category": "allocation",
            "metric": "dao_treasury_pct",
            "value": 0.2162,
            "unit": "share of max supply",
            "as_of": latest_date,
            "source": "https://etherfi.gitbook.io/gov/ethfi-allocations",
            "quality_status": "official",
            "note": "Use latest dated allocation page; older beta page shows a different bucket split.",
        },
        {
            "category": "allocation",
            "metric": "user_airdrops_pct",
            "value": 0.1927,
            "unit": "share of max supply",
            "as_of": latest_date,
            "source": "https://etherfi.gitbook.io/gov/ethfi-allocations",
            "quality_status": "official",
            "note": "Older ETHFI page lists 17.57%; record source conflict rather than silently overwrite.",
        },
        {
            "category": "allocation",
            "metric": "partnerships_liquidity_pct",
            "value": 0.039,
            "unit": "share of max supply",
            "as_of": latest_date,
            "source": "https://etherfi.gitbook.io/gov/ethfi-allocations",
            "quality_status": "official",
            "note": "Includes Protocol Guild commitment according to source.",
        },
        {
            "category": "allocation",
            "metric": "core_contributors_pct",
            "value": 0.2147,
            "unit": "share of max supply",
            "as_of": latest_date,
            "source": "https://etherfi.gitbook.io/gov/ethfi-allocations",
            "quality_status": "official",
            "note": "Three-year vesting and one-year cliff stated on source page.",
        },
        {
            "category": "allocation",
            "metric": "investors_pct",
            "value": 0.3374,
            "unit": "share of max supply",
            "as_of": latest_date,
            "source": "https://etherfi.gitbook.io/gov/ethfi-allocations",
            "quality_status": "official",
            "note": "Two-year vesting and one-year cliff stated on source page.",
        },
        {
            "category": "value_accrual",
            "metric": "buyback_and_holder_distribution",
            "value": rights.get("Value Accrual"),
            "unit": "classification",
            "as_of": latest_date,
            "source": TOKEN_RIGHTS_URL,
            "quality_status": "independent registry; cross-check against governance and contracts",
            "note": rights.get("Economic Rights (Summary)"),
        },
    ]
    write_csv(DAILY_OUTPUT, daily)
    write_csv(KPI_OUTPUT, [kpi])
    write_csv(TOKEN_OUTPUT, token_rows)
    source_rows = [
        {
            "source_id": "SRC-ETHFI-001",
            "provider": "DefiLlama",
            "dataset": "protocol/ether.fi",
            "metrics": "parent TVL, chain and token breakdown",
            "url": "https://api.llama.fi/protocol/ether.fi",
            "as_of": latest_date,
            "method": "daily API snapshot; latest observation per UTC date",
            "quality_status": "independent aggregator",
            "limitations": "TVL methodology and token inclusion require review; not a protocol accounting statement",
        },
        {
            "source_id": "SRC-ETHFI-002",
            "provider": "DefiLlama",
            "dataset": "summary/fees/ether.fi",
            "metrics": "gross fees, protocol revenue, holders revenue",
            "url": "https://api.llama.fi/summary/fees/ether.fi",
            "as_of": latest_date,
            "method": "dailyFees, dailyRevenue, dailyHoldersRevenue",
            "quality_status": "independent aggregator; methodology review required",
            "limitations": "Revenue definition follows DefiLlama adapter; does not replace treasury reconciliation",
        },
        {
            "source_id": "SRC-ETHFI-003",
            "provider": "CoinGecko",
            "dataset": "coins/ether-fi",
            "metrics": "price, market cap, FDV, circulating/total/max supply",
            "url": COINGECKO_URL,
            "as_of": latest_date,
            "method": "public API snapshot",
            "quality_status": "market-data aggregator",
            "limitations": "Supply methodology and exchange coverage are provider-defined",
        },
        {
            "source_id": "SRC-ETHFI-004",
            "provider": "ether.fi governance",
            "dataset": "ETHFI allocations",
            "metrics": "allocation, vesting, fixed max supply",
            "url": "https://etherfi.gitbook.io/gov/ethfi-allocations",
            "as_of": latest_date,
            "method": "official page review",
            "quality_status": "primary source",
            "limitations": "Allocation page has a displayed last-updated date; actual wallet balances require on-chain reconciliation",
        },
        {
            "source_id": "SRC-ETHFI-005",
            "provider": "ether.fi governance",
            "dataset": "buyback program and proposals",
            "metrics": "buybacks, withdrawal fee allocation, sETHFI distributions",
            "url": "https://etherfi.gitbook.io/gov/ethfi-buyback-program",
            "as_of": latest_date,
            "method": "official docs and governance proposal review",
            "quality_status": "primary source",
            "limitations": "Approved mechanism does not prove every historical buyback or current execution volume",
        },
        {
            "source_id": "SRC-ETHFI-006",
            "provider": "DefiLlama",
            "dataset": "token-rights and unlock page",
            "metrics": "value accrual registry, unlock context",
            "url": "https://api.llama.fi/token-rights; https://defillama.com/unlocks/ether.fi",
            "as_of": latest_date,
            "method": "registry API and public page snapshot",
            "quality_status": "independent aggregator; cross-check required",
            "limitations": "Unlock API is not in the free public API; page snapshot and registry may lag governance changes",
        },
    ]
    write_csv(SOURCES_OUTPUT, source_rows)
    print(f"daily_rows={len(daily)} as_of={latest_date} tvl=${tvl_current:,.0f} fees30d=${fees.get('total30d', 0):,.0f} revenue30d=${revenue.get('total30d', 0):,.0f}")
    print(f"Wrote {DAILY_OUTPUT}")
    print(f"Wrote {KPI_OUTPUT}")
    print(f"Wrote {TOKEN_OUTPUT}")
    print(f"Wrote {SOURCES_OUTPUT}")


if __name__ == "__main__":
    main()
