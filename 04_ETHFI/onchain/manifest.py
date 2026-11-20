#!/usr/bin/env python3
"""Write or verify ``MANIFEST.csv`` for the committed ETHFI snapshots.

The manifest is the bridge between a number on the site and the exact bytes it
came from. It records size, SHA-256 and the canonical source for every input.

    python3 manifest.py            # rewrite MANIFEST.csv
    python3 manifest.py --check    # fail if a file changed or is missing
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
OUT = HERE / "MANIFEST.csv"

TOKEN = "0xFe0c30065B384F05761f15d0CC899D4F9F9Cc0eB"
BUYBACK = "0x43f4ca92f7f378bcdcf1508b866b5b6c47d6408c"
TREASURY = "0x7A6A41F353B3002751d94118aA7f4935dA39bB53"
FUNDING = "0xf40bcc0845528873784F36e5C105E62a93ff7021"
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

SOURCES = {
    "ll_fees.json": "https://api.llama.fi/summary/fees/ether.fi?dataType=dailyFees",
    "ll_revenue.json": "https://api.llama.fi/summary/fees/ether.fi?dataType=dailyRevenue",
    "ll_holders_rev.json": "https://api.llama.fi/summary/fees/ether.fi?dataType=dailyHoldersRevenue",
    "ll_protocol.json": "https://api.llama.fi/protocol/ether.fi",
    "holders_top.json": f"https://eth.blockscout.com/api/v2/tokens/{TOKEN}/holders",
    "buyback_ethfi_all.json": f"https://eth.blockscout.com/api/v2/addresses/{BUYBACK}/token-transfers?token={TOKEN}",
    "buyback_usdc_all.json": f"https://eth.blockscout.com/api/v2/addresses/{BUYBACK}/token-transfers?token={USDC}",
    "safe_token_transfers.json": f"https://eth.blockscout.com/api/v2/addresses/{TREASURY}/token-transfers?token={TOKEN}",
    "funding_usdc_all.json": f"https://eth.blockscout.com/api/v2/addresses/{FUNDING}/token-transfers?token={USDC}",
    "dex_token.json": f"https://api.dexscreener.com/latest/dex/tokens/{TOKEN}",
    "cg_coin.json": "https://api.coingecko.com/api/v3/coins/ether-fi?market_data=true",
    "cg_eth_price.json": "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd",
    "dex_quotes.json": "Uniswap V3 QuoterV2 eth_call; see SOURCES.md (point-in-time fixture)",
    "rpc_supply.json": "Ethereum JSON-RPC eth_call totalSupply() + eth_blockNumber",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def records(path: Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return 0
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        if isinstance(data.get("items"), list):
            return len(data["items"])
        if isinstance(data.get("pairs"), list):
            return len(data["pairs"])
        return 1
    return 0


def build() -> list[dict]:
    rows = []
    for path in sorted(RAW.glob("*.json")):
        rows.append({
            "file": path.name,
            "bytes": path.stat().st_size,
            "sha256": digest(path),
            "records": records(path),
            "modified_utc": dt.datetime.fromtimestamp(
                path.stat().st_mtime, dt.timezone.utc
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source": SOURCES.get(path.name, "see SOURCES.md"),
        })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    rows = build()
    if args.check:
        if not OUT.exists():
            print(f"missing {OUT}")
            return 1
        with OUT.open(encoding="utf-8", newline="") as fh:
            old = {r["file"]: r for r in csv.DictReader(fh)}
        errors = []
        for row in rows:
            prev = old.get(row["file"])
            if not prev:
                errors.append(f"new file not in manifest: {row['file']}")
            elif prev["sha256"] != row["sha256"] or prev["bytes"] != str(row["bytes"]):
                errors.append(f"changed: {row['file']}")
        for name in old.keys() - {r["file"] for r in rows}:
            errors.append(f"manifest lists missing file: {name}")
        if errors:
            print("MANIFEST CHECK FAILED")
            for e in errors:
                print(" -", e)
            return 1
        print(f"OK: {len(rows)} snapshots match MANIFEST.csv")
        return 0

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {OUT} ({len(rows)} snapshots)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
