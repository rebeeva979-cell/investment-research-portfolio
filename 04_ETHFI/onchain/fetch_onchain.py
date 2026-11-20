#!/usr/bin/env python3
"""Refresh the ETHFI on-chain / market snapshots used by the case.

By default this script does **not** touch the network: the committed files in
``raw/`` are the point-in-time evidence. Pass ``--refresh`` to fetch a new
snapshot, then rebuild and review the diff before committing.

Examples:
    python3 fetch_onchain.py --refresh
    python3 fetch_onchain.py --refresh --only supply,holders
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import urllib.parse
from pathlib import Path

from fetch_lib import blockscout, get_json, save_json

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
RAW.mkdir(exist_ok=True)

TOKEN = "0xFe0c30065B384F05761f15d0CC899D4F9F9Cc0eB"
TOKEN_L = TOKEN.lower()
BUYBACK_SAFE = "0x43f4ca92f7f378bcdcf1508b866b5b6c47d6408c"
TREASURY_SAFE = "0x7A6A41F353B3002751d94118aA7f4935dA39bB53"
FUNDING_SAFE = "0xf40bcc0845528873784F36e5C105E62a93ff7021"
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
RPC = "https://ethereum-rpc.publicnode.com"

CG_URL = (
    "https://api.coingecko.com/api/v3/coins/ether-fi?localization=false&tickers=false&"
    "market_data=true&community_data=false&developer_data=false&sparkline=false"
)


def _save(name: str, data) -> None:
    save_json(name, data)
    print(f"  wrote raw/{name} ({len(data) if hasattr(data, '__len__') else '?'} records)")


def paginate(path: str, params: dict | None = None, max_pages: int = 12, refresh: bool = True) -> list:
    items: list = []
    params = dict(params or {})
    for _ in range(max_pages):
        query = urllib.parse.urlencode(params)
        url = f"https://eth.blockscout.com/api/v2{path}" + (f"?{query}" if query else "")
        data = get_json(url, refresh=refresh)
        items.extend(data.get("items", []))
        nxt = data.get("next_page_params")
        if not nxt:
            break
        params.update(nxt)
    return items


def rpc(method: str, params: list):
    import urllib.request

    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    req = urllib.request.Request(
        RPC, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)
    if "error" in body:
        raise RuntimeError(body["error"])
    return body["result"]


def fetch_supply() -> None:
    raw = rpc("eth_call", [{"to": TOKEN, "data": "0x18160ddd"}, "latest"])
    total = int(raw, 16) / 1e18
    block = int(rpc("eth_blockNumber", []), 16)
    _save("rpc_supply.json", {
        "as_of": dt.datetime.now(dt.timezone.utc).date().isoformat(),
        "block": block,
        "total_supply_ethfi": total,
        "raw": raw,
    })

def fetch_holders() -> None:
    _save("holders_top.json", paginate(f"/tokens/{TOKEN}/holders", max_pages=5))


def fetch_transfers(address: str, token: str, name: str, max_pages: int = 12) -> None:
    _save(name, paginate(f"/addresses/{address}/token-transfers",
                         {"token": token}, max_pages=max_pages))


def fetch_market() -> None:
    _save("cg_coin.json", get_json(CG_URL, refresh=True))
    _save("cg_eth_price.json", get_json(
        "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd",
        refresh=True,
    ))
    _save("dex_token.json", get_json(
        f"https://api.dexscreener.com/latest/dex/tokens/{TOKEN}", refresh=True
    ))


def fetch_defillama() -> None:
    base = "https://api.llama.fi"
    for name, url in {
        "ll_fees.json": f"{base}/summary/fees/ether.fi?dataType=dailyFees",
        "ll_revenue.json": f"{base}/summary/fees/ether.fi?dataType=dailyRevenue",
        "ll_holders_rev.json": f"{base}/summary/fees/ether.fi?dataType=dailyHoldersRevenue",
        "ll_protocol.json": f"{base}/protocol/ether.fi",
    }.items():
        _save(name, get_json(url, refresh=True))


GROUPS = {
    "supply": fetch_supply,
    "holders": fetch_holders,
    "transfers": lambda: (
        fetch_transfers(BUYBACK_SAFE, TOKEN, "buyback_ethfi_all.json"),
        fetch_transfers(BUYBACK_SAFE, USDC, "buyback_usdc_all.json"),
        fetch_transfers(TREASURY_SAFE, TOKEN, "safe_token_transfers.json"),
        fetch_transfers(FUNDING_SAFE, USDC, "funding_usdc_all.json"),
    ),
    "market": fetch_market,
    "defillama": fetch_defillama,
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="hit the network (otherwise no-op)")
    ap.add_argument("--only", default=",".join(GROUPS), help="comma-separated groups")
    args = ap.parse_args()
    if not args.refresh:
        print("No network calls. Pass --refresh to update the snapshots.")
        return 0
    groups = [g.strip() for g in args.only.split(",") if g.strip()]
    unknown = [g for g in groups if g not in GROUPS]
    if unknown:
        ap.error(f"unknown groups: {unknown}; choose from {sorted(GROUPS)}")
    for group in groups:
        print(f"[{group}]")
        GROUPS[group]()
    print("done; now run: python3 build_outputs.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
