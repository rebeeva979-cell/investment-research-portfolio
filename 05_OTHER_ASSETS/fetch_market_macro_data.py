#!/usr/bin/env python3
"""Build Looker-ready market, macro and ETF-flow tables.

Automatic sources:
  * Yahoo Finance chart endpoint for SPY, DXY, GPRO and LYFT.
  * CoinGecko public API for USDT.

Farside ETF pages use Cloudflare in many environments. Therefore ETF flows are
accepted from a saved HTML file with --farside-html and are never silently
treated as zero when the latest row is not reported.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import re
from pathlib import Path

import requests


BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw_market_macro"
MARKET_OUTPUT = BASE_DIR / "MARKET_MACRO_DAILY.csv"
KPI_OUTPUT = BASE_DIR / "MARKET_MACRO_KPI_LATEST.csv"
ETF_OUTPUT = BASE_DIR / "ETF_FLOWS_DAILY.csv"
SOURCE_OUTPUT = BASE_DIR / "MACRO_SOURCE_REGISTER.csv"

YAHOO_SYMBOLS = {
    "SPY": "SPY",
    "DXY": "DX-Y.NYB",
    "GPRO": "GPRO",
    "LYFT": "LYFT",
}


def get_json(url: str) -> dict:
    response = requests.get(url, headers={"User-Agent": "InvestmentResearch/1.0"}, timeout=60)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {url}")
    return payload


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def yahoo_history(symbol: str, range_value: str) -> list[dict]:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={range_value}&interval=1d&events=history"
    payload = get_json(url)
    result = payload["chart"]["result"][0]
    timestamps = result.get("timestamp") or []
    quote = result["indicators"]["quote"][0]
    rows = []
    previous_close = None
    for index, timestamp in enumerate(timestamps):
        close = quote.get("close", [])[index]
        if close is None:
            continue
        date = dt.datetime.fromtimestamp(timestamp, tz=dt.timezone.utc).date().isoformat()
        return_1d = None if previous_close in (None, 0) else close / previous_close - 1
        rows.append(
            {
                "date": date,
                "asset_id": symbol,
                "ticker": symbol,
                "close_usd": close,
                "return_1d": return_1d,
                "volume": (quote.get("volume", [None])[index]),
                "source_url": url,
                "quality_status": "market-data API; close is unadjusted chart close",
            }
        )
        previous_close = close
    return rows


def coingecko_usdt() -> list[dict]:
    url = "https://api.coingecko.com/api/v3/coins/tether?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
    payload = get_json(url)
    market = payload.get("market_data", {})
    date = dt.datetime.now(dt.timezone.utc).date().isoformat()
    return [
        {
            "date": date,
            "asset_id": "USDT",
            "ticker": "USDT",
            "close_usd": market.get("current_price", {}).get("usd"),
            "return_1d": None,
            "volume": market.get("total_volume", {}).get("usd"),
            "market_cap_usd": market.get("market_cap", {}).get("usd"),
            "source_url": url,
            "quality_status": "CoinGecko snapshot; intraday peg deviations require exchange-level data",
        }
    ]


def clean_cell(value: str) -> str:
    value = html.unescape(re.sub(r"<[^>]+>", "", value)).strip()
    return re.sub(r"\s+", " ", value)


def parse_amount(value: str) -> float | None:
    value = value.strip().replace(",", "")
    if value in {"", "-", "—"}:
        return None
    negative = value.startswith("(") and value.endswith(")")
    value = value.strip("()")
    try:
        result = float(value)
    except ValueError:
        return None
    return -result if negative else result


def parse_farside_html(path: Path, product: str, source_url: str) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    header: list[str] | None = None
    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", text, flags=re.I | re.S):
        cells = [clean_cell(cell) for cell in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, flags=re.I | re.S)]
        if not cells:
            continue
        if cells[0].lower() == "date" and len(cells) > 2:
            header = cells[1:]
            continue
        if header is None or not re.match(r"^\d{1,2} [A-Z][a-z]{2} \d{4}$", cells[0]):
            continue
        try:
            date = dt.datetime.strptime(cells[0], "%d %b %Y").date().isoformat()
        except ValueError:
            continue
        for fund, value in zip(header, cells[1:]):
            if fund in {"", "-"}:
                continue
            rows.append(
                {
                    "date": date,
                    "product": product,
                    "fund": fund,
                    "net_flow_usd_m": parse_amount(value),
                    "source_url": source_url,
                    "extraction_method": "saved Farside HTML",
                    "quality_status": "reported row; Farside notes data may contain errors",
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--range", default="5y", help="Yahoo range, e.g. 1y, 5y, max")
    parser.add_argument("--bitcoin-farside-html", type=Path)
    parser.add_argument("--ethereum-farside-html", type=Path)
    args = parser.parse_args()
    RAW_DIR.mkdir(exist_ok=True)

    market_rows: list[dict] = []
    for asset_id, symbol in YAHOO_SYMBOLS.items():
        rows = yahoo_history(symbol, args.range)
        market_rows.extend([{**row, "asset_id": asset_id} for row in rows])
        (RAW_DIR / f"yahoo_{asset_id}.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    market_rows.extend(coingecko_usdt())
    write_csv(
        MARKET_OUTPUT,
        market_rows,
        ["date", "asset_id", "ticker", "close_usd", "return_1d", "volume", "market_cap_usd", "source_url", "quality_status"],
    )

    latest_rows = []
    by_asset: dict[str, list[dict]] = {}
    for row in market_rows:
        by_asset.setdefault(row["asset_id"], []).append(row)
    for asset_id, rows in sorted(by_asset.items()):
        latest = max(rows, key=lambda row: row["date"])
        latest_rows.append(
            {
                "asset_id": asset_id,
                "as_of_date": latest["date"],
                "close_usd": latest.get("close_usd"),
                "return_1d": latest.get("return_1d"),
                "volume": latest.get("volume"),
                "market_cap_usd": latest.get("market_cap_usd"),
                "source_url": latest["source_url"],
                "quality_status": latest["quality_status"],
            }
        )
    write_csv(KPI_OUTPUT, latest_rows, list(latest_rows[0].keys()))

    etf_rows: list[dict] = []
    if args.bitcoin_farside_html:
        etf_rows.extend(parse_farside_html(args.bitcoin_farside_html, "Bitcoin", "https://farside.co.uk/bitcoin-etf-flow-all-data/"))
    if args.ethereum_farside_html:
        etf_rows.extend(parse_farside_html(args.ethereum_farside_html, "Ethereum", "https://farside.co.uk/ethereum-etf-flow-all-data/"))
    etf_fields = ["date", "product", "fund", "net_flow_usd_m", "source_url", "extraction_method", "quality_status"]
    if etf_rows:
        write_csv(ETF_OUTPUT, etf_rows, etf_fields)
    elif not ETF_OUTPUT.exists():
        write_csv(ETF_OUTPUT, [], etf_fields)
    else:
        # Preserve manually refreshed Farside rows when Cloudflare blocks the fetch.
        etf_rows = list(csv.DictReader(ETF_OUTPUT.open(newline="", encoding="utf-8")))

    source_rows = [
        {"source_id": "SRC-MACRO-001", "provider": "Yahoo Finance chart", "dataset": "SPY, DXY, GPRO, LYFT daily history", "url": "https://query1.finance.yahoo.com/v8/finance/chart/", "update_frequency": "daily", "quality_status": "public market-data endpoint", "limitations": "unadjusted chart close; verify corporate actions and licensing"},
        {"source_id": "SRC-MACRO-002", "provider": "CoinGecko", "dataset": "USDT spot and market cap", "url": "https://api.coingecko.com/api/v3/coins/tether", "update_frequency": "daily", "quality_status": "market-data aggregator", "limitations": "peg deviation requires exchange-level and reserve context"},
        {"source_id": "SRC-MACRO-003", "provider": "Farside Investors", "dataset": "Bitcoin/Ethereum ETF flows", "url": "https://farside.co.uk/bitcoin-etf-flow-all-data/; https://farside.co.uk/ethereum-etf-flow-all-data/", "update_frequency": "daily", "quality_status": "manual HTML refresh in this environment", "limitations": "Cloudflare may block automated requests; dash means not reported, not zero"},
    ]
    write_csv(SOURCE_OUTPUT, source_rows, list(source_rows[0].keys()))
    print(f"market_rows={len(market_rows)} latest_assets={len(latest_rows)} etf_rows={len(etf_rows)}")


if __name__ == "__main__":
    main()
