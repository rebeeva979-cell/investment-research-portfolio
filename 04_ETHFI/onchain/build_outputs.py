"""Build the ETHFI evidence pack: CSVs, metrics and hand-rolled SVG charts.

Inputs are the cached public-API responses in ./raw. No pandas/matplotlib:
the charts are plain SVG so they render in any browser and in headless Chrome.

Usage:
    python3 build_outputs.py
    ETHFI_AS_OF=2026-11-20 python3 build_outputs.py
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
from collections import defaultdict
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = HERE
DATA = os.path.join(OUT, "data")
ASSETS = os.path.join(OUT, "assets")
os.makedirs(DATA, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)

def _load_json(name):
    with open(os.path.join(RAW, name), encoding="utf-8") as fh:
        return json.load(fh)


CG = _load_json("cg_coin.json")
CG_MD = CG["market_data"]
AS_OF = os.environ.get("ETHFI_AS_OF") or CG_MD["last_updated"][:10]
# On-chain totalSupply is the primary float base; CoinGecko is the fallback.
RPC = _load_json("rpc_supply.json") if os.path.exists(os.path.join(RAW, "rpc_supply.json")) else {}
SUPPLY = float(RPC.get("total_supply_ethfi") or CG_MD["total_supply"])
INITIAL = 1_000_000_000.0
PRICE = float(CG_MD["current_price"]["usd"])
MCAP = float(CG_MD["market_cap"]["usd"])
WEEKLY_UNLOCKS = 1_020_000.0
COLORS = {
    "bg": "#0b1220",
    "text": "#eaf1fb",
    "muted": "#9fb0c6",
    "grid": "#243449",
    "accent": "#7dd3c0",
    "gold": "#f2c879",
    "red": "#ef8f8f",
    "blue": "#8ab4f8",
}


def load(name):
    with open(os.path.join(RAW, name), encoding="utf-8") as fh:
        return json.load(fh)


def day(ts):
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).date()


def series(name):
    d = load(f"{name}.json")
    return [(day(x[0]), float(x[1])) for x in d["totalDataChart"]]


def fmt_money(v, digits=0):
    if abs(v) >= 1e9:
        return f"${v/1e9:,.2f}B"
    if abs(v) >= 1e6:
        return f"${v/1e6:,.1f}M"
    if abs(v) >= 1e3:
        return f"${v/1e3:,.0f}k"
    return f"${v:,.{digits}f}"


# ---------------------------------------------------------------- data prep
fees = series("ll_fees")
rev = series("ll_revenue")
holders = series("ll_holders_rev")
tvl_raw = load("ll_protocol.json")["tvl"]
tvl = [(day(x["date"]), float(x["totalLiquidityUSD"])) for x in tvl_raw]
cur_tvl = tvl[-1][1]
peak_date, peak_tvl = max(tvl, key=lambda x: x[1])

top = load("holders_top.json")
cats = []
for h in top:
    a = h["address"]
    tags = " ".join(t.get("name", "") for t in (a.get("metadata") or {}).get("tags", []) or []).lower()
    name = (a.get("name") or "").lower()
    if "sethfi" in tags:
        c = "sETHFI staking contract"
    elif "oftadapter" in name:
        c = "Bridge adapter"
    elif "liquideth" in tags:
        c = "liquidETH vault"
    elif "symbiotic" in tags:
        c = "Symbiotic collateral"
    elif "protocol guild" in tags:
        c = "Protocol Guild"
    elif any(x in tags for x in ("binance", "bybit", "okx", "bithumb", "btcturk")):
        c = "CEX"
    elif "ether.fi" in tags:
        c = "ether.fi Safe"
    elif a["is_contract"]:
        c = "Other contract"
    else:
        c = "EOA"
    cats.append((a["hash"], int(h["value"]) / 1e18, c, a.get("name") or ""))

# top-10 labelled rows
labels = {
    "0x7a6a41f353b3002751d94118aa7f4935da39bb53": "ether.fi Safe (treasury)",
    "0x86b5780b606940eb59a062aa85a07959518c0161": "sETHFI staking contract",
    "0x95bf94e06d5be1000c23cd99968eff414aa4995e": "Unlabelled EOA #3",
    "0xf10873355b209b401262cadc753d654e2b7e41ac": "Unlabelled EOA #4",
    "0x5a52e96bacdabb82fd05763e25335261b270efcb": "Binance hot wallet",
    "0xf977814e90da44bfa03b6295a0616a897441acec": "Binance cold wallet",
    "0xe0080d2f853ecddbd81a643dc10da075df26fd3f": "Ether.fi OFT adapter",
    "0xf619ab1f33cdc8a0123e093de92ea4d7399de39f": "Unlabelled EOA #8",
    "0x7a93190d436436bbb79fa2c0d24ca93afb59b3fb": "Unlabelled EOA #9",
    "0x6630ff17cf5357c5f9c3d2a21ac98d2ff1070739": "Unlabelled EOA #10",
}
top10 = []
for h in top[:10]:
    a = h["address"]["hash"]
    v = int(h["value"]) / 1e18
    top10.append((labels.get(a.lower(), a[:10] + "…"), v, v / SUPPLY * 100, cats[[c[0] for c in cats].index(a)][2]))

# concentration
vals = [c[1] for c in cats]
top1, top5, top10p, top20 = (sum(vals[:n]) / SUPPLY * 100 for n in (1, 5, 10, 20))
eoa = [v for _, v, c, _ in cats if c == "EOA"]
eoa_share = sum(eoa) / SUPPLY * 100
eoa_top1 = eoa[0] / sum(eoa) * 100
eoa_top5 = sum(eoa[:5]) / sum(eoa) * 100
hhi = sum((v / sum(eoa)) ** 2 for v in eoa) * 10000
gini_x = sorted(eoa)
n = len(gini_x)
gini = sum((2 * i - n - 1) * x for i, x in enumerate(gini_x, 1)) / (n * sum(gini_x))
cum = 0
nak = 0
for v in sorted(eoa, reverse=True):
    cum += v
    nak += 1
    if cum >= sum(eoa) / 2:
        break

# buybacks
buy_eth = defaultdict(float)
buy_usdc = defaultdict(float)
buy_count = defaultdict(int)
buy_day_eth = defaultdict(float)
buy_day_usd = defaultdict(float)
buy_day_n = defaultdict(int)
for t in load("buyback_ethfi_all.json"):
    if t["to"]["hash"].lower() == "0x43f4ca92f7f378bcdcf1508b866b5b6c47d6408c" and t["from"]["hash"].lower() == "0x9008d19f58aabd9ed0d60971565aa8510560ab41":
        buy_eth[t["transaction_hash"]] += int(t["total"]["value"]) / 1e18
for t in load("buyback_usdc_all.json"):
    if t["from"]["hash"].lower() == "0x43f4ca92f7f378bcdcf1508b866b5b6c47d6408c" and t["to"]["hash"].lower() == "0x9008d19f58aabd9ed0d60971565aa8510560ab41":
        buy_usdc[t["transaction_hash"]] += int(t["total"]["value"]) / 10 ** int(t["total"].get("decimals", 6))
for h in buy_eth:
    if h not in buy_usdc:
        continue
    ts = next(t["timestamp"][:10] for t in load("buyback_ethfi_all.json") if t["transaction_hash"] == h)
    buy_day_eth[ts] += buy_eth[h]
    buy_day_usd[ts] += buy_usdc[h]
    buy_day_n[ts] += 1
bb_eth = sum(buy_eth[h] for h in buy_eth if h in buy_usdc)
bb_usd = sum(buy_usdc.values())
bb_n = sum(buy_day_n.values())
bb_px = bb_usd / bb_eth
last30_cut = (dt.date.fromisoformat(AS_OF) - dt.timedelta(days=30)).isoformat()
bb_30_eth = sum(v for d, v in buy_day_eth.items() if d >= last30_cut)
bb_30_usd = sum(v for d, v in buy_day_usd.items() if d >= last30_cut)
bb_30_n = sum(v for d, v in buy_day_n.items() if d >= last30_cut)
bb_days = len(buy_day_eth)

# fees aggregates
def tail_sum(s, days):
    return sum(v for _, v in s[-days:])


f30, f365 = tail_sum(fees, 30), tail_sum(fees, 365)
r30, r365 = tail_sum(rev, 30), tail_sum(rev, 365)
h30 = tail_sum(holders, 30)
h365 = tail_sum(holders, 365)
holders_last_nz = max((d for d, v in holders if v > 0), default=None)
h_all = sum(v for _, v in holders)
r_all = sum(v for _, v in rev)
f_all = sum(v for _, v in fees)

# monthly aggregation for the chart
monthly = defaultdict(lambda: [0.0, 0.0, 0.0])
for d, v in fees:
    monthly[d.strftime("%Y-%m")][0] += v
for d, v in rev:
    monthly[d.strftime("%Y-%m")][1] += v
for d, v in holders:
    monthly[d.strftime("%Y-%m")][2] += v
months = sorted(monthly)[-18:]

# liquidity quotes + pool depth from the same DexScreener snapshot
quotes = load("dex_quotes.json")
TOKEN = "0xfe0c30065b384f05761f15d0cc899d4f9f9cc0eb"
dex_pairs = [
    p for p in load("dex_token.json")["pairs"]
    if p.get("chainId") == "ethereum" and p["baseToken"]["address"].lower() == TOKEN
]
dex_total = sum(float((p.get("liquidity") or {}).get("usd") or 0) for p in dex_pairs)
top_pool = max(dex_pairs, key=lambda p: float((p.get("liquidity") or {}).get("usd") or 0))
TOP_POOL_LIQ = float((top_pool.get("liquidity") or {}).get("usd") or 0)

# scenario valuation
scen = []
for name, revenue, mult in [("Bear", r365 * 0.749, 7), ("Base", r365, 10), ("Bull", r365 * 1.20, 14)]:
    val = revenue * mult
    px = val / SUPPLY
    scen.append((name, revenue, mult, val, px, (px / PRICE - 1) * 100))

# ---------------------------------------------------------------- CSV
def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


write_csv(os.path.join(DATA, "ethfi_metrics.csv"),
          ["metric", "value", "unit", "as_of", "source"],
          [
              ("price", PRICE, "USD", AS_OF, "CoinGecko /coins/ether-fi"),
              ("market_cap", MCAP, "USD", AS_OF, "CoinGecko"),
              ("fdv", MCAP, "USD", AS_OF, "CoinGecko (circulating = total)"),
              ("circulating_supply", SUPPLY, "ETHFI", AS_OF, "on-chain totalSupply; CoinGecko"),
              ("max_supply", INITIAL, "ETHFI", AS_OF, "token docs"),
              ("burned_supply", INITIAL - SUPPLY, "ETHFI", AS_OF, "1B genesis - on-chain totalSupply"),
              ("defillama_locked", 16_399_443, "ETHFI", AS_OF, "DefiLlama unlocks page"),
              ("tvl", cur_tvl, "USD", AS_OF, "DefiLlama protocol"),
              ("tvl_peak", peak_tvl, "USD", str(peak_date), "DefiLlama protocol"),
              ("tvl_drawdown_from_peak", (cur_tvl / peak_tvl - 1) * 100, "%", AS_OF, "computed"),
              ("fees_30d", f30, "USD", AS_OF, "DefiLlama dailyFees"),
              ("revenue_30d", r30, "USD", AS_OF, "DefiLlama dailyRevenue"),
              ("holders_revenue_30d", h30, "USD", AS_OF, "DefiLlama dailyHoldersRevenue"),
              ("fees_365d", f365, "USD", AS_OF, "DefiLlama"),
              ("revenue_365d", r365, "USD", AS_OF, "DefiLlama"),
              ("holders_revenue_365d", h365, "USD", AS_OF, "DefiLlama"),
              ("holders_revenue_last_nonzero", str(holders_last_nz), "date", AS_OF, "DefiLlama daily series"),
              ("cumulative_revenue", r_all, "USD", AS_OF, "DefiLlama"),
              ("cumulative_holders_revenue", h_all, "USD", AS_OF, "DefiLlama"),
              ("holders_revenue_share_cumulative", h_all / r_all * 100, "%", AS_OF, "computed"),
              ("buyback_ethfi", bb_eth, "ETHFI", AS_OF, "CoW -> 0x43f4 Safe, on-chain"),
              ("buyback_usdc", bb_usd, "USD", AS_OF, "on-chain"),
              ("buyback_avg_price", bb_px, "USD", AS_OF, "computed"),
              ("buyback_txs", bb_n, "count", AS_OF, "on-chain"),
              ("buyback_30d_ethfi", bb_30_eth, "ETHFI", AS_OF, "on-chain"),
              ("buyback_30d_usdc", bb_30_usd, "USD", AS_OF, "on-chain"),
              ("buyback_annualized_pct_mcap", bb_30_usd * 12 / MCAP * 100, "%", AS_OF, "computed"),
              ("dex_liquidity", dex_total, "USD", AS_OF, "DexScreener"),
              ("dex_liquidity_pct_mcap", dex_total / MCAP * 100, "%", AS_OF, "computed"),
              ("top1_holder_share", top1, "%", AS_OF, "Blockscout holders"),
              ("top5_holder_share", top5, "%", AS_OF, "Blockscout holders"),
              ("top10_holder_share", top10p, "%", AS_OF, "Blockscout holders"),
              ("top20_holder_share", top20, "%", AS_OF, "Blockscout holders"),
              ("eoa_float_share", eoa_share, "%", AS_OF, "computed"),
              ("eoa_top1_share_of_float", eoa_top1, "%", AS_OF, "computed"),
              ("eoa_top5_share_of_float", eoa_top5, "%", AS_OF, "computed"),
              ("eoa_gini", gini, "index", AS_OF, "computed"),
              ("eoa_hhi", hhi, "index", AS_OF, "computed"),
              ("eoa_nakamoto_50", nak, "wallets", AS_OF, "computed"),
              ("mcap_revenue", MCAP / r365, "x", AS_OF, "computed"),
              ("mcap_fees", MCAP / f365, "x", AS_OF, "computed"),
              ("mcap_tvl", MCAP / cur_tvl, "x", AS_OF, "computed"),
              ("buyback_30d_pct_revenue", bb_30_usd / r30 * 100, "%", AS_OF, "computed: 30d buyback USD / 30d protocol revenue"),
              ("buyback_mark_vs_spot_pct", (PRICE / bb_px - 1) * 100, "%", AS_OF, "computed: spot / average buy price"),
              ("buyback_30d_vs_unlocks_30d", bb_30_eth / (WEEKLY_UNLOCKS * 30 / 7) * 100, "%", AS_OF, "computed vs DefiLlama unlock schedule"),
          ])

write_csv(os.path.join(DATA, "ethfi_holders_top.csv"),
          ["rank", "address", "label", "balance_ethfi", "share_pct", "category"],
          [(i, c[0], labels.get(c[0].lower(), c[3] or c[2]), round(c[1], 2), round(c[1] / SUPPLY * 100, 4), c[2])
           for i, c in enumerate(cats[:25], 1)])

write_csv(os.path.join(DATA, "ethfi_buybacks_daily.csv"),
          ["date", "ethfi_bought", "usdc_spent", "avg_price", "tx_count"],
          [(d, round(buy_day_eth[d], 4), round(buy_day_usd[d], 2),
            round(buy_day_usd[d] / buy_day_eth[d], 6) if buy_day_eth[d] else "", buy_day_n[d])
           for d in sorted(buy_day_eth)])

write_csv(os.path.join(DATA, "ethfi_fees_monthly.csv"),
          ["month", "fees_usd", "revenue_usd", "holders_revenue_usd"],
          [(m, round(monthly[m][0], 2), round(monthly[m][1], 2), round(monthly[m][2], 2)) for m in months])

write_csv(os.path.join(DATA, "ethfi_tvl_weekly.csv"),
          ["date", "tvl_usd"],
          [(str(d), round(v, 2)) for d, v in tvl[::7]])

write_csv(os.path.join(DATA, "ethfi_valuation_scenarios.csv"),
          ["scenario", "revenue_run_rate_usd", "multiple_x", "implied_mcap_usd", "implied_price_usd", "upside_pct"],
          [(a, b, c, round(d, 0), round(e, 4), round(f, 1)) for a, b, c, d, e, f in scen])

# ---------------------------------------------------------------- SVG helpers
def svg_open(w, h, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(title)}">'
            f'<style>text{{font-family:Inter,ui-sans-serif,system-ui,Arial,sans-serif}}'
            f'.t{{fill:{COLORS["text"]};font-size:14px;font-weight:600}}'
            f'.s{{fill:{COLORS["muted"]};font-size:11px}}'
            f'.a{{fill:{COLORS["muted"]};font-size:10px}}'
            f'</style>')


def axes(w, h, ml, mr, mt, mb, ymax, yfmt, xlabels, yticks=4):
    out = []
    for i in range(yticks + 1):
        y = mt + (h - mt - mb) * i / yticks
        val = ymax * (1 - i / yticks)
        out.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{w-mr}" y2="{y:.1f}" stroke="{COLORS["grid"]}" stroke-width="1"/>')
        out.append(f'<text x="{ml-9}" y="{y+4:.1f}" text-anchor="end" class="a">{escape(yfmt(val))}</text>')
    for x, lab in xlabels:
        out.append(f'<text x="{x:.1f}" y="{h-mb+18}" text-anchor="middle" class="a">{escape(lab)}</text>')
    return "".join(out)


def save(name, body):
    with open(os.path.join(ASSETS, name), "w", encoding="utf-8") as fh:
        fh.write(body)


# --- 1. TVL
W, H, ML, MR, MT, MB = 760, 330, 64, 18, 34, 44
pts = tvl[::7]
ymax = 13e9
sx = lambda i: ML + (W - ML - MR) * i / (len(pts) - 1)
sy = lambda v: MT + (H - MT - MB) * (1 - v / ymax)
path = " ".join(("M" if i == 0 else "L") + f"{sx(i):.1f},{sy(v):.1f}" for i, (_, v) in enumerate(pts))
area = path + f" L{sx(len(pts)-1):.1f},{H-MB} L{ML},{H-MB} Z"
pi = min(range(len(pts)), key=lambda i: abs((pts[i][0] - peak_date).days))
body = svg_open(W, H, "ether.fi TVL, 2024-2026")
body += f'<defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{COLORS["accent"]}" stop-opacity=".35"/><stop offset="1" stop-color="{COLORS["accent"]}" stop-opacity="0"/></linearGradient></defs>'
body += f'<text x="{ML}" y="20" class="t">TVL: {fmt_money(peak_tvl)} peak → {fmt_money(cur_tvl)} now</text>'
body += axes(W, H, ML, MR, MT, MB, ymax, lambda v: f"${v/1e9:.0f}B",
            [(sx(i), pts[i][0].strftime("%b %y")) for i in (0, len(pts)//3, 2*len(pts)//3, len(pts)-1)])
body += f'<path d="{area}" fill="url(#g1)"/><path d="{path}" fill="none" stroke="{COLORS["accent"]}" stroke-width="2.2"/>'
body += f'<line x1="{sx(pi)}" y1="{sy(peak_tvl)}" x2="{sx(pi)}" y2="{H-MB}" stroke="{COLORS["gold"]}" stroke-width="1" stroke-dasharray="3 3"/>'
body += f'<circle cx="{sx(pi)}" cy="{sy(peak_tvl)}" r="4" fill="{COLORS["gold"]}"/>'
body += f'<text x="{sx(pi)+8}" y="{sy(peak_tvl)-8}" class="s" fill="{COLORS["gold"]}">peak {fmt_money(peak_tvl)} · {peak_date}</text>'
body += f'<circle cx="{sx(len(pts)-1)}" cy="{sy(cur_tvl)}" r="4" fill="{COLORS["accent"]}"/>'
body += f'<text x="{sx(len(pts)-1)-2}" y="{sy(cur_tvl)+18}" text-anchor="end" class="s" fill="{COLORS["accent"]}">now {fmt_money(cur_tvl)}</text>'
body += "</svg>"
save("ethfi_tvl.svg", body)

# --- 2. fees, revenue, holders revenue
W, H, ML, MR, MT, MB = 760, 460, 64, 18, 34, 50
n = len(months)
bw = (W - ML - MR) / n
ymax = max(monthly[m][0] for m in months) * 1.12
body = svg_open(W, H, "ether.fi fees, revenue and holders revenue by month")
body += f'<text x="{ML}" y="20" class="t">Fees scale with TVL; holders revenue stopped in April 2026</text>'
body += axes(W, H, ML, MR, MT, 230, ymax, lambda v: f"${v/1e6:.0f}M",
            [(ML + bw * (i + .5), dt.date(int(m[:4]), int(m[5:]), 1).strftime("%b %y")) for i, m in enumerate(months) if i % 3 == 0])
for i, m in enumerate(months):
    x = ML + bw * i
    fh = (H - MT - 230) * monthly[m][0] / ymax
    rh = (H - MT - 230) * monthly[m][1] / ymax
    body += f'<rect x="{x+2:.1f}" y="{H-230-fh:.1f}" width="{bw*.42:.1f}" height="{fh:.1f}" fill="#33506b"/>'
    body += f'<rect x="{x+bw*.46:.1f}" y="{H-230-rh:.1f}" width="{bw*.42:.1f}" height="{rh:.1f}" fill="{COLORS["accent"]}"/>'
body += f'<rect x="{ML}" y="{H-206}" width="9" height="9" fill="#33506b"/><text x="{ML+14}" y="{H-198}" class="a">gross fees</text>'
body += f'<rect x="{ML+90}" y="{H-206}" width="9" height="9" fill="{COLORS["accent"]}"/><text x="{ML+104}" y="{H-198}" class="a">protocol revenue</text>'
# lower panel: holders revenue
H2 = 190
body += f'<text x="{ML}" y="{H-140}" class="s" fill="{COLORS["gold"]}">Holders revenue per month (buybacks recognised by DefiLlama)</text>'
hmax = max(monthly[m][2] for m in months) or 1
base = H - 18
for i, m in enumerate(months):
    x = ML + bw * i
    hh = (H2 - 70) * monthly[m][2] / hmax
    color = COLORS["gold"] if monthly[m][2] > 0 else "#334155"
    body += f'<rect x="{x+bw*.15:.1f}" y="{base-hh:.1f}" width="{bw*.7:.1f}" height="{max(hh,1):.1f}" fill="{color}"/>'
    if monthly[m][2] == 0 and m >= "2026-05":
        body += f'<text x="{x+bw*.5:.1f}" y="{base-5}" text-anchor="middle" class="a">0</text>'
body += f'<line x1="{ML}" y1="{base}" x2="{W-MR}" y2="{base}" stroke="{COLORS["grid"]}"/>'
body += f'<text x="{W-MR}" y="{H-145}" text-anchor="end" class="a">last non-zero: {holders_last_nz}</text>'
body += "</svg>"
save("ethfi_fees.svg", body)

# --- 3. buybacks
W, H, ML, MR, MT, MB = 760, 360, 64, 58, 34, 44
days = sorted(buy_day_eth)
ymax = max(buy_day_eth.values()) * 1.12
cum = []
c = 0
for d in days:
    c += buy_day_eth[d]
    cum.append(c)
cmax = bb_eth * 1.03
sx = lambda i: ML + (W - ML - MR) * i / (len(days) - 1)
sy = lambda v: MT + (H - MT - MB) * (1 - v / ymax)
sy2 = lambda v: MT + (H - MT - MB) * (1 - v / cmax)
body = svg_open(W, H, "ETHFI buybacks via CoW, September to November 2026")
body += f'<text x="{ML}" y="20" class="t">Buybacks are real: {bb_eth/1e6:.2f}M ETHFI bought via CoW since 17 Sep</text>'
body += axes(W, H, ML, MR, MT, MB, ymax, lambda v: f"{v/1e3:.0f}k",
            [(sx(i), days[i][5:]) for i in (0, len(days)//3, 2*len(days)//3, len(days)-1)])
bw = max(2.0, (W - ML - MR) / len(days) * .62)
for i, d in enumerate(days):
    hh = (H - MT - MB) * buy_day_eth[d] / ymax
    body += f'<rect x="{sx(i)-bw/2:.1f}" y="{H-MB-hh:.1f}" width="{bw:.1f}" height="{hh:.1f}" fill="{COLORS["blue"]}" opacity=".8"/>'
cpath = " ".join(("M" if i == 0 else "L") + f"{sx(i):.1f},{sy2(v):.1f}" for i, v in enumerate(cum))
body += f'<path d="{cpath}" fill="none" stroke="{COLORS["gold"]}" stroke-width="2"/>'
body += f'<text x="{W-MR+4}" y="{MT+8}" class="a" fill="{COLORS["gold"]}">{bb_eth/1e6:.2f}M</text>'


body += "</svg>"
save("ethfi_buyback.svg", body)

# --- 4. top holders
W, H, ML, MR, MT, MB = 760, 390, 190, 24, 34, 24
rows = top10[:10]
ymax = 16.5
bh = (H - MT - MB) / len(rows)
body = svg_open(W, H, "Top ETHFI holders")
body += f'<text x="18" y="20" class="t">Top 10 wallets hold {top10p:.1f}% of supply</text>'
for i, (lab, v, pct, cat) in enumerate(rows):
    y = MT + i * bh
    w = (W - ML - MR) * pct / ymax
    color = {"ether.fi Safe": COLORS["gold"], "sETHFI staking contract": "#64748b",
             "CEX": "#8ab4f8", "Bridge adapter": "#a78bfa"}.get(cat, COLORS["accent"])
    body += f'<text x="{ML-10}" y="{y+bh*.62:.1f}" text-anchor="end" class="a">{escape(lab)}</text>'
    body += f'<rect x="{ML}" y="{y+bh*.18:.1f}" width="{w:.1f}" height="{bh*.55:.1f}" rx="2" fill="{color}"/>'
    body += f'<text x="{ML+w+8:.1f}" y="{y+bh*.62:.1f}" class="a">{pct:.1f}%</text>'
body += f'<text x="18" y="{H-2}" class="a">Source: Blockscout holders API, {AS_OF}. Treasury = tagged ether.fi Safe; CEX = Binance/Bybit/OKX/Bithumb/BtcTurk.</text>'
body += "</svg>"
save("ethfi_holders.svg", body)

# --- 5. liquidity / impact
W, H, ML, MR, MT, MB = 760, 330, 64, 22, 34, 46
L = TOP_POOL_LIQ
def impact(usd):
    R = (L / 2) / PRICE
    q = usd / PRICE
    return q / (R + q) * 100
xs = [1000 * (10 ** (i / 20)) for i in range(0, 61)]  # 1k -> 1M
ys = [impact(x) for x in xs]
ymax = 100
sx = lambda v: ML + (W - ML - MR) * (math.log10(v) - 3) / 3
sy = lambda v: MT + (H - MT - MB) * (1 - v / ymax)
path = " ".join(("M" if i == 0 else "L") + f"{sx(x):.1f},{sy(y):.1f}" for i, (x, y) in enumerate(zip(xs, ys)))
body = svg_open(W, H, "ETHFI DEX price impact by order size")
body += f'<text x="{ML}" y="20" class="t">A $250k DEX sale costs ~{abs(quotes["250000"]["slippage_pct"]):.0f}%: depth is ${dex_total/1e6:.2f}M</text>'
body += axes(W, H, ML, MR, MT, MB, ymax, lambda v: f"{v:.0f}%",
            [(sx(10**e), ("$1k", "$10k", "$100k", "$1M")[e - 3]) for e in (3, 4, 5, 6)], yticks=4)
body += f'<path d="{path}" fill="none" stroke="{COLORS["red"]}" stroke-width="2" stroke-dasharray="5 4"/>'
for usd, lab in [(10_000, f"$10k: {quotes['10000']['slippage_pct']:+.1f}%"), (50_000, f"$50k: {quotes['50000']['slippage_pct']:+.1f}%"), (250_000, f"$250k: {quotes['250000']['slippage_pct']:+.1f}%")]:
    body += f'<circle cx="{sx(usd):.1f}" cy="{sy(impact(usd)):.1f}" r="4" fill="{COLORS["gold"]}"/>'
    body += f'<text x="{sx(usd)+8:.1f}" y="{sy(impact(usd))-8:.1f}" class="a" fill="{COLORS["gold"]}">{lab}</text>'
body += f'<text x="{ML}" y="{H-8}" class="a">Dashed = constant-product model (top pool, {fmt_money(TOP_POOL_LIQ)}); gold = Uniswap QuoterV2 quotes. Concentrated liquidity can reduce small-size impact and worsen it beyond range.</text>'
body += "</svg>"
save("ethfi_liquidity.svg", body)

# ---------------------------------------------------------------- print key numbers
print(json.dumps({
    "tvl": cur_tvl, "peak": peak_tvl, "peak_date": str(peak_date), "drawdown": (cur_tvl/peak_tvl-1)*100,
    "fees30": f30, "rev30": r30, "r365": r365, "h365": h365, "h_all": h_all, "ratio": h_all/r_all*100,
    "bb_eth": bb_eth, "bb_usd": bb_usd, "bb_px": bb_px, "bb_n": bb_n,
    "bb30_eth": bb_30_eth, "bb30_usd": bb_30_usd, "bb30_n": bb_30_n,
    "top1": top1, "top5": top5, "top10": top10p, "top20": top20,
    "eoa_share": eoa_share, "eoa_top1": eoa_top1, "eoa_top5": eoa_top5,
    "gini": gini, "hhi": hhi, "nak": nak,
    "mcap_rev": MCAP/r365, "mcap_fees": MCAP/f365, "mcap_tvl": MCAP/cur_tvl,
    "bb_ann_pct": bb_30_usd*12/MCAP*100,
    "bb_vs_unlock": bb_30_eth/(1_020_000*30/7)*100,
    "scen": scen,
}, indent=1))
