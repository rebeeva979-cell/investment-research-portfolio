#!/usr/bin/env python3
"""Fetch LTC network data for the investment-research dashboard.

Sources: Coin Metrics Community API v4 plus Blockchair Litecoin aggregated API.
The script discovers metric coverage first, then downloads daily observations
for LTC and a small PoW peer set, plus daily block and non-coinbase transfer
aggregates. It never fabricates missing economic metrics.

Usage:
    python3 fetch_ltc_research_data.py
    python3 fetch_ltc_research_data.py --start 2018-08-22 --end 2026-11-16

Review Coin Metrics Community Data and Blockchair API terms before using the
output in a commercial production report. The output is suitable for a
research POC and keeps source, coverage and metric availability in
LTC_CATALOG.csv.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
API_BASE = "https://community-api.coinmetrics.io/v4"
BLOCKCHAIR_BASE = "https://api.blockchair.com"
ASSETS = {"ltc": "Litecoin", "btc": "Bitcoin", "bch": "Bitcoin Cash", "doge": "Dogecoin", "dash": "Dash"}
CANDIDATE_METRICS = [
    "PriceUSD",
    "CapMrktCurUSD",
    "CapMVRVCur",
    "SplyCur",
    "AdrActCnt",
    "TxCnt",
    "TxTfrCnt",
    "HashRate",
    "BlkCnt",
    "FeeTotNtv",
    "IssTotNtv",
]
LTC_OUTPUT = BASE_DIR / "LTC_ONCHAIN_DAILY.csv"
PEER_OUTPUT = BASE_DIR / "LTC_PEER_DAILY.csv"
CATALOG_OUTPUT = BASE_DIR / "LTC_CATALOG.csv"
KPI_OUTPUT = BASE_DIR / "LTC_ONCHAIN_KPI_LATEST.csv"
BLOCKS_OUTPUT = BASE_DIR / "LTC_BLOCKS_DAILY.csv"
TRANSFERS_OUTPUT = BASE_DIR / "LTC_TRANSFER_DAILY.csv"


def api_get(path: str, params: dict[str, str]) -> dict:
    query = urllib.parse.urlencode(params)
    url = f"{API_BASE}{path}?{query}"
    last_error: Exception | None = None
    for attempt in range(6):
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "LTC-Investment-Research/1.0", "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            last_error = error
            if error.code not in {403, 429, 500, 502, 503, 504}:
                raise
            time.sleep(1.5 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = error
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Coin Metrics request failed after retries: {url}: {last_error}")


def blockchair_get(path: str, params: dict[str, str]) -> dict:
    """Fetch an aggregated Blockchair response.

    Blockchair documents aggregated infinitable queries for Litecoin blocks and
    transactions. The optional API key is read from BLOCKCHAIR_API_KEY when the
    user has one; the POC also works with the public try-out limits.
    """
    query_params = dict(params)
    api_key = os.environ.get("BLOCKCHAIR_API_KEY")
    if api_key:
        query_params["key"] = api_key
    query = urllib.parse.urlencode(query_params)
    url = f"{BLOCKCHAIR_BASE}/{path}?{query}"
    last_error: Exception | None = None
    for attempt in range(5):
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "LTC-Investment-Research/1.0", "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                payload = json.load(response)
            if payload.get("context", {}).get("code") not in (None, 200):
                raise RuntimeError(f"Blockchair API returned context code {payload['context']['code']}: {payload}")
            return payload
        except urllib.error.HTTPError as error:
            last_error = error
            if error.code not in {403, 429, 500, 502, 503, 504}:
                raise
            time.sleep(2.0 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, RuntimeError) as error:
            last_error = error
            time.sleep(2.0 * (attempt + 1))
    raise RuntimeError(f"Blockchair request failed after retries: {url}: {last_error}")


def fetch_blockchair_daily(start: str, end: str) -> tuple[list[dict], list[dict]]:
    """Fetch daily block and non-coinbase transaction aggregates for Litecoin."""
    time_filter = f"time({start}..{end})"
    block_payload = blockchair_get(
        "litecoin/blocks",
        {
            "a": "date,min(id),max(id),count(),avg(difficulty),sum(transaction_count),sum(fee_total),sum(generation),sum(reward)",
            "q": time_filter,
            "limit": "10000",
        },
    )
    transfer_payload = blockchair_get(
        "litecoin/transactions",
        {
            "a": "date,count(),sum(output_total),sum(input_total),sum(fee),sum(output_count),sum(input_count)",
            "q": f"{time_filter},is_coinbase(false)",
            "limit": "10000",
        },
    )

    def value(row: dict, key: str) -> float | None:
        raw = row.get(key)
        try:
            return float(raw) if raw not in (None, "") else None
        except (TypeError, ValueError):
            return None

    blocks: list[dict] = []
    for raw in block_payload.get("data", []):
        date = raw.get("date")
        if not date:
            continue
        block_count = value(raw, "count()")
        height_min = value(raw, "min(id)")
        height_max = value(raw, "max(id)")
        blocks.append(
            {
                "date": date,
                "height_min": height_min,
                "height_max": height_max,
                "height": height_max,
                "timestamp_utc": f"{date}T00:00:00Z",
                "timestamp_type": "daily_utc_anchor_not_exact_block_time",
                "block_count": block_count,
                "difficulty": value(raw, "avg(difficulty)"),
                "transaction_count": value(raw, "sum(transaction_count)"),
                "fee_total_litoshi": value(raw, "sum(fee_total)"),
                "subsidy_total_litoshi": value(raw, "sum(generation)"),
                "reward_total_litoshi": value(raw, "sum(reward)"),
                "block_interval_sec_est": 86400.0 / block_count if block_count else None,
                "source": "Blockchair Litecoin API v2 aggregated blocks",
            }
        )

    transfers: list[dict] = []
    for raw in transfer_payload.get("data", []):
        date = raw.get("date")
        if not date:
            continue
        transfers.append(
            {
                "date": date,
                "transfer_tx_count": value(raw, "count()"),
                "transfer_output_litoshi": value(raw, "sum(output_total)"),
                "transfer_input_litoshi": value(raw, "sum(input_total)"),
                "transfer_fee_litoshi": value(raw, "sum(fee)"),
                "output_count": value(raw, "sum(output_count)"),
                "input_count": value(raw, "sum(input_count)"),
                "source": "Blockchair Litecoin API v2 aggregated transactions",
            }
        )
    write_csv(BLOCKS_OUTPUT, blocks)
    write_csv(TRANSFERS_OUTPUT, transfers)
    return blocks, transfers


def discover_catalog(assets: list[str]) -> list[dict]:
    payload = api_get(
        "/catalog-v2/asset-metrics",
        {"assets": ",".join(assets), "metrics": ",".join(CANDIDATE_METRICS)},
    )
    rows: list[dict] = []
    for asset_record in payload.get("data", []):
        asset = asset_record["asset"]
        for metric_record in asset_record.get("metrics", []):
            for frequency in metric_record.get("frequencies", []):
                rows.append(
                    {
                        "asset": asset,
                        "asset_name": ASSETS.get(asset, asset),
                        "metric": metric_record["metric"],
                        "frequency": frequency.get("frequency"),
                        "min_time": frequency.get("min_time"),
                        "max_time": frequency.get("max_time"),
                        "community": frequency.get("community"),
                    }
                )
    return rows


def available_metrics(catalog: list[dict], asset: str) -> list[str]:
    return sorted(
        {
            row["metric"]
            for row in catalog
            if row["asset"] == asset and row["frequency"] == "1d" and row["community"]
        }
    )


def fetch_asset(asset: str, metrics: list[str], start: str, end: str) -> list[dict]:
    if not metrics:
        return []
    payload = api_get(
        "/timeseries/asset-metrics",
        {
            "assets": asset,
            "metrics": ",".join(metrics),
            "frequency": "1d",
            "start_time": start,
            "end_time": end,
            "page_size": "10000",
        },
    )
    rows: list[dict] = []
    for raw in payload.get("data", []):
        row = {"asset": raw.get("asset"), "date": raw["time"][:10]}
        for metric in metrics:
            value = raw.get(metric)
            try:
                row[metric] = float(value) if value not in (None, "") else None
            except (TypeError, ValueError):
                row[metric] = None
        rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def add_derived_ltc_fields(rows: list[dict]) -> list[dict]:
    rows = sorted(rows, key=lambda row: row["date"])
    by_date = {row["date"]: row for row in rows}
    output: list[dict] = []
    for row in rows:
        price = row.get("PriceUSD")
        fees = row.get("FeeTotNtv")
        issuance = row.get("IssTotNtv")
        supply = row.get("SplyCur")
        miner_revenue = (fees or 0.0) + (issuance or 0.0) if fees is not None or issuance is not None else None
        item = {
            "date": row["date"],
            "asset": "LTC",
            "cm_price_usd": price,
            "market_cap_usd": row.get("CapMrktCurUSD"),
            "supply_ltc": supply,
            "active_addresses": row.get("AdrActCnt"),
            "tx_count": row.get("TxCnt"),
            "transfer_count": row.get("TxTfrCnt"),
            "hashrate": row.get("HashRate"),
            "block_count": row.get("BlkCnt"),
            "fees_ltc": fees,
            "issuance_ltc": issuance,
            "miner_revenue_ltc": miner_revenue,
            "fees_usd": fees * price if fees is not None and price is not None else None,
            "issuance_usd": issuance * price if issuance is not None and price is not None else None,
            "miner_revenue_usd": miner_revenue * price if miner_revenue is not None and price is not None else None,
            "fee_share_of_miner_revenue_pct": fees / miner_revenue * 100.0 if fees is not None and miner_revenue else None,
            "active_addresses_per_tx": row["AdrActCnt"] / row["TxCnt"] if row.get("AdrActCnt") and row.get("TxCnt") else None,
            "supply_change_1d_ltc": None,
            "supply_inflation_365d_pct": None,
            "active_addresses_30d_change_pct": None,
            "tx_count_30d_change_pct": None,
            "hashrate_30d_change_pct": None,
            "market_cap_30d_change_pct": None,
            "fee_to_issuance_ratio": fees / issuance if fees is not None and issuance else None,
            "fees_usd_30d_sum": None,
            "issuance_usd_30d_sum": None,
            "fee_to_issuance_30d_ratio": None,
            "annualized_issuance_to_market_cap_pct": issuance * price * 365.0 / row["CapMrktCurUSD"] * 100.0 if issuance is not None and price is not None and row.get("CapMrktCurUSD") else None,
            "mvrv": row.get("CapMVRVCur"),
            "realized_cap_usd": row.get("CapMrktCurUSD") / row["CapMVRVCur"] if row.get("CapMrktCurUSD") and row.get("CapMVRVCur") else None,
            "source": "Coin Metrics Community API v4",
        }
        previous = by_date.get((dt.date.fromisoformat(row["date"]) - dt.timedelta(days=1)).isoformat())
        year_ago = by_date.get((dt.date.fromisoformat(row["date"]) - dt.timedelta(days=365)).isoformat())
        month_ago = by_date.get((dt.date.fromisoformat(row["date"]) - dt.timedelta(days=30)).isoformat())
        if previous and supply is not None and previous.get("SplyCur") is not None:
            item["supply_change_1d_ltc"] = supply - previous["SplyCur"]
        if year_ago and supply is not None and year_ago.get("SplyCur"):
            item["supply_inflation_365d_pct"] = (supply / year_ago["SplyCur"] - 1.0) * 100.0
        if month_ago:
            for source, target in (
                ("AdrActCnt", "active_addresses_30d_change_pct"),
                ("TxCnt", "tx_count_30d_change_pct"),
                ("HashRate", "hashrate_30d_change_pct"),
                ("CapMrktCurUSD", "market_cap_30d_change_pct"),
            ):
                if row.get(source) is not None and month_ago.get(source):
                    item[target] = (row[source] / month_ago[source] - 1.0) * 100.0
        position = len(output)
        trailing = rows[max(0, position - 29) : position + 1]
        item["fees_usd_30d_sum"] = sum((x.get("FeeTotNtv") or 0.0) * (x.get("PriceUSD") or 0.0) for x in trailing)
        item["issuance_usd_30d_sum"] = sum((x.get("IssTotNtv") or 0.0) * (x.get("PriceUSD") or 0.0) for x in trailing)
        if item["issuance_usd_30d_sum"]:
            item["fee_to_issuance_30d_ratio"] = item["fees_usd_30d_sum"] / item["issuance_usd_30d_sum"]
        output.append(item)
    return output


def merge_blockchain_daily(rows: list[dict], blocks: list[dict], transfers: list[dict]) -> list[dict]:
    """Join Blockchair daily aggregates and calculate the investment fields.

    Native amounts from Blockchair are litoshi and are divided by 1e8. USD
    values are calculated with Coin Metrics PriceUSD rather than trusting the
    vendor's historical USD columns, which are incomplete for early LTC dates.
    """
    blocks_by_date = {row["date"]: row for row in blocks}
    transfers_by_date = {row["date"]: row for row in transfers}
    max_supply = 84_000_000.0
    for row in rows:
        date = row["date"]
        date_key = date.isoformat() if hasattr(date, "isoformat") else str(date)[:10]
        block = blocks_by_date.get(date_key, {})
        transfer = transfers_by_date.get(date_key, {})
        price = row.get("cm_price_usd")
        row["block_height_min"] = block.get("height_min")
        row["block_height_max"] = block.get("height_max")
        row["block_timestamp_utc"] = block.get("timestamp_utc")
        row["block_timestamp_type"] = block.get("timestamp_type")
        row["difficulty"] = block.get("difficulty")
        row["block_interval_sec_est"] = block.get("block_interval_sec_est")
        row["blockchair_block_count"] = block.get("block_count")
        row["blockchair_transaction_count"] = block.get("transaction_count")
        row["blockchair_fee_litoshi"] = block.get("fee_total_litoshi")
        row["blockchair_subsidy_litoshi"] = block.get("subsidy_total_litoshi")
        row["blockchair_reward_litoshi"] = block.get("reward_total_litoshi")

        row["transfer_tx_count"] = transfer.get("transfer_tx_count")
        row["transfer_value_ltc"] = transfer.get("transfer_output_litoshi") / 100_000_000.0 if transfer.get("transfer_output_litoshi") is not None else None
        row["input_value_ltc"] = transfer.get("transfer_input_litoshi") / 100_000_000.0 if transfer.get("transfer_input_litoshi") is not None else None
        row["fee_revenue_ltc"] = transfer.get("transfer_fee_litoshi") / 100_000_000.0 if transfer.get("transfer_fee_litoshi") is not None else None
        row["output_count"] = transfer.get("output_count")
        row["input_count"] = transfer.get("input_count")
        row["transfer_value_usd"] = row["transfer_value_ltc"] * price if row.get("transfer_value_ltc") is not None and price is not None else None
        row["input_value_usd"] = row["input_value_ltc"] * price if row.get("input_value_ltc") is not None and price is not None else None
        row["fee_revenue_usd"] = row["fee_revenue_ltc"] * price if row.get("fee_revenue_ltc") is not None and price is not None else None
        row["output_value_ltc"] = row.get("transfer_value_ltc")
        row["output_value_usd"] = row.get("transfer_value_usd")
        row["adjusted_transfer_value_ltc"] = None
        row["adjusted_transfer_value_usd"] = None
        row["adjusted_transfer_value_status"] = "NOT_AVAILABLE"
        row["transfer_value_method"] = "Gross non-coinbase output value; includes change/self transfers"
        row["outputs_per_transfer_tx"] = row["output_count"] / row["transfer_tx_count"] if row.get("output_count") and row.get("transfer_tx_count") else None

        row["subsidy_revenue_ltc"] = block.get("subsidy_total_litoshi") / 100_000_000.0 if block.get("subsidy_total_litoshi") is not None else None
        row["subsidy_revenue_usd"] = row["subsidy_revenue_ltc"] * price if row.get("subsidy_revenue_ltc") is not None and price is not None else None
        row["miner_revenue_ltc_blockchair"] = block.get("reward_total_litoshi") / 100_000_000.0 if block.get("reward_total_litoshi") is not None else None
        row["miner_revenue_usd_blockchair"] = row["miner_revenue_ltc_blockchair"] * price if row.get("miner_revenue_ltc_blockchair") is not None and price is not None else None
        row["fee_share_of_miner_revenue_blockchair_pct"] = (
            row["fee_revenue_ltc"] / row["miner_revenue_ltc_blockchair"] * 100.0
            if row.get("fee_revenue_ltc") is not None and row.get("miner_revenue_ltc_blockchair")
            else None
        )
        row["miner_cost_usd"] = None
        row["miner_cost_status"] = "NOT_OBSERVED"

        supply = row.get("supply_ltc")
        row["max_supply_ltc"] = max_supply
        row["remaining_supply_ltc"] = max_supply - supply if supply is not None else None
        row["supply_mined_pct"] = supply / max_supply * 100.0 if supply is not None else None
        row["annualized_issuance_ltc"] = row.get("issuance_ltc") * 365.0 if row.get("issuance_ltc") is not None else None
        row["estimated_years_to_max_at_current_issuance"] = (
            row["remaining_supply_ltc"] / row["annualized_issuance_ltc"]
            if row.get("remaining_supply_ltc") is not None and row.get("annualized_issuance_ltc")
            else None
        )
        height = row.get("block_height_max")
        if height is not None:
            halving_index = min(int(height) // 840_000, 10)
            row["model_block_reward_ltc"] = 50.0 / (2 ** halving_index)
            next_halving = (halving_index + 1) * 840_000
            row["next_halving_block"] = next_halving
            row["blocks_to_next_halving"] = max(next_halving - int(height), 0)
        else:
            row["model_block_reward_ltc"] = None
            row["next_halving_block"] = None
            row["blocks_to_next_halving"] = None
    return rows


def latest_kpi(rows: list[dict], catalog: list[dict], start: str, end: str) -> dict:
    latest = rows[-1] if rows else {"date": None}
    result = {"asset": "LTC", "as_of_date": latest.get("date"), "coverage_start_requested": start, "coverage_end_requested": end}
    for key, value in latest.items():
        if key not in {"asset", "date", "source"}:
            result[key] = value
    result["coverage_start_actual"] = rows[0]["date"] if rows else None
    result["coverage_end_actual"] = rows[-1]["date"] if rows else None
    result["observations"] = len(rows)
    result["catalog_metrics_available"] = ",".join(available_metrics(catalog, "ltc"))
    result["data_note"] = "Coin Metrics Community API v4; verify license/terms before commercial use."
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2018-08-22")
    parser.add_argument("--end", default=dt.datetime.now(dt.timezone.utc).date().isoformat())
    args = parser.parse_args()

    catalog = discover_catalog(list(ASSETS))
    write_csv(CATALOG_OUTPUT, catalog)

    all_rows: list[dict] = []
    for index, asset in enumerate(ASSETS):
        metrics = available_metrics(catalog, asset)
        print(f"{asset}: {', '.join(metrics)}")
        rows = fetch_asset(asset, metrics, args.start, args.end)
        all_rows.extend(rows)
        if index < len(ASSETS) - 1:
            time.sleep(0.8)

    ltc_raw = [row for row in all_rows if row["asset"] == "ltc"]
    ltc_rows = add_derived_ltc_fields(ltc_raw)
    print("Fetching Blockchair daily block and transfer aggregates...")
    blocks, transfers = fetch_blockchair_daily(args.start, args.end)
    ltc_rows = merge_blockchain_daily(ltc_rows, blocks, transfers)
    write_csv(LTC_OUTPUT, ltc_rows)

    peers: list[dict] = []
    for row in all_rows:
        if row["asset"] == "ltc":
            continue
        peers.append(
            {
                "date": row["date"],
                "asset": row["asset"].upper(),
                "asset_name": ASSETS.get(row["asset"], row["asset"]),
                "cm_price_usd": row.get("PriceUSD"),
                "market_cap_usd": row.get("CapMrktCurUSD"),
                "supply_native": row.get("SplyCur"),
                "active_addresses": row.get("AdrActCnt"),
                "tx_count": row.get("TxCnt"),
                "hashrate": row.get("HashRate"),
                "block_count": row.get("BlkCnt"),
                "source": "Coin Metrics Community API v4",
            }
        )
    write_csv(PEER_OUTPUT, sorted(peers, key=lambda row: (row["date"], row["asset"])))
    write_csv(KPI_OUTPUT, [latest_kpi(ltc_rows, catalog, args.start, args.end)])
    print(f"LTC rows={len(ltc_rows)} peers rows={len(peers)}")
    print(f"Wrote {LTC_OUTPUT}")
    print(f"Wrote {PEER_OUTPUT}")
    print(f"Wrote {CATALOG_OUTPUT}")
    print(f"Wrote {KPI_OUTPUT}")
    print(f"Wrote {BLOCKS_OUTPUT}")
    print(f"Wrote {TRANSFERS_OUTPUT}")


if __name__ == "__main__":
    main()
