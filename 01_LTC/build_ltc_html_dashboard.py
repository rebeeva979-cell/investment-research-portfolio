#!/usr/bin/env python3
"""Build a self-contained interactive LTC research dashboard.

Input:
    01_LTC/LTC_LOOKER_DATASET.xlsx
    01_LTC/vendor/echarts.min.js

Output:
    01_LTC/LTC_Dashboard.html

The output is a single HTML file with embedded data and ECharts. It works
offline and can be opened in any modern browser.

Run:
    python3 01_LTC/build_ltc_html_dashboard.py
"""

from __future__ import annotations

import datetime as dt
import json
import math
from pathlib import Path

import openpyxl

BASE_DIR = Path(__file__).resolve().parent
INPUT_XLSX = BASE_DIR / "LTC_LOOKER_DATASET.xlsx"
ECHARTS_JS = BASE_DIR / "vendor" / "echarts.min.js"
OUTPUT_HTML = BASE_DIR / "LTC_Dashboard.html"


def clean(value):
    if value is None:
        return None
    if isinstance(value, dt.datetime):
        return value.date().isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
        return value
    return str(value)


def sheet_rows(wb, name: str):
    ws = wb[name]
    rows = ws.iter_rows(values_only=True)
    header = list(next(rows))
    for row in rows:
        yield dict(zip(header, row))


def num(value):
    if value in (None, ""):
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(result) or math.isinf(result):
        return None
    return result


def build_data() -> dict:
    wb = openpyxl.load_workbook(INPUT_XLSX, read_only=True, data_only=True)

    kpi_raw = next(sheet_rows(wb, "KPI_LATEST"))
    kpi = {
        "price": num(kpi_raw.get("price_close_usd")),
        "r1": num(kpi_raw.get("return_1d")),
        "r7": num(kpi_raw.get("return_7d")),
        "r30": num(kpi_raw.get("return_30d")),
        "r90": num(kpi_raw.get("return_90d")),
        "r365": num(kpi_raw.get("return_365d")),
        "ytd": num(kpi_raw.get("ytd_return")),
        "vol": num(kpi_raw.get("volatility_30d_annualized")),
        "ath": num(kpi_raw.get("ath_close_usd_in_dataset")),
        "ath_date": clean(kpi_raw.get("ath_close_date_in_dataset")),
        "dd": num(kpi_raw.get("drawdown_from_ath")),
        "hi52": num(kpi_raw.get("high_52w_close_usd")),
        "lo52": num(kpi_raw.get("low_52w_close_usd")),
        "ma200": num(kpi_raw.get("ma_200_usd")),
        "vs_ma200": num(kpi_raw.get("price_vs_ma_200")),
        "mcap": num(kpi_raw.get("market_cap_usd")),
        "supply": num(kpi_raw.get("supply_ltc")),
        "remaining": num(kpi_raw.get("remaining_supply_ltc")),
        "mined": num(kpi_raw.get("supply_mined")),
        "max_supply": num(kpi_raw.get("max_supply_ltc")),
        "aa": num(kpi_raw.get("active_addresses")),
        "tx": num(kpi_raw.get("tx_count")),
        "hr": num(kpi_raw.get("hashrate")),
        "mvrv": num(kpi_raw.get("mvrv")),
        "rcap": num(kpi_raw.get("realized_cap_usd")),
        "fees30": num(kpi_raw.get("fees_usd_30d_sum")),
        "iss30": num(kpi_raw.get("issuance_usd_30d_sum")),
        "fee_iss_ratio": num(kpi_raw.get("fee_to_issuance_30d_ratio")),
        "inflation": num(kpi_raw.get("supply_inflation_365d")),
        "aa30": num(kpi_raw.get("active_addresses_30d_change")),
        "tx30": num(kpi_raw.get("tx_count_30d_change")),
        "hr30": num(kpi_raw.get("hashrate_30d_change")),
        "mc30": num(kpi_raw.get("market_cap_30d_change")),
        "var95": num(kpi_raw.get("var_95_30d")),
        "var99": num(kpi_raw.get("var_99_30d")),
        "sharpe": num(kpi_raw.get("sharpe_30d")),
        "sortino": num(kpi_raw.get("sortino_30d")),
        "coverage_start": clean(kpi_raw.get("coverage_start")),
        "coverage_end": clean(kpi_raw.get("coverage_end")),
        "obs": num(kpi_raw.get("observations")),
        "gaps": num(kpi_raw.get("date_gaps")),
        "calc_at": clean(kpi_raw.get("calculated_at_utc")),
    }

    market = []
    for row in sheet_rows(wb, "MARKET_DAILY"):
        market.append({
            "d": clean(row.get("date")),
            "c": num(row.get("price_close_usd")),
            "v": num(row.get("volume")),
            "r1": num(row.get("return_1d")),
            "r30": num(row.get("return_30d")),
            "ytd": num(row.get("ytd_return")),
            "ma30": num(row.get("ma_30_usd")),
            "ma200": num(row.get("ma_200_usd")),
            "dd": num(row.get("drawdown_from_ath")),
            "vol": num(row.get("volatility_30d_annualized")),
            "mc": num(row.get("market_cap_usd")),
            "aa": num(row.get("active_addresses")),
            "tx": num(row.get("tx_count")),
            "hr": num(row.get("hashrate")),
            "fees": num(row.get("fees_usd")),
            "iss": num(row.get("issuance_usd")),
            "sup": num(row.get("supply_ltc")),
            "mvrv": num(row.get("mvrv")),
            "rcap": num(row.get("realized_cap_usd")),
            "diff": num(row.get("difficulty")),
            "blocks": num(row.get("block_count")),
            "fee_share": num(row.get("fee_share_of_miner_revenue")),
            "aa30": num(row.get("active_addresses_30d_change")),
            "tx30": num(row.get("tx_count_30d_change")),
            "hr30": num(row.get("hashrate_30d_change")),
            "mc30": num(row.get("market_cap_30d_change")),
            "mined": num(row.get("supply_mined")),
            "remaining": num(row.get("remaining_supply_ltc")),
        })

    yearly = []
    for row in sheet_rows(wb, "YEARLY_SUMMARY"):
        yearly.append({
            "year": int(num(row.get("year")) or 0),
            "ret": num(row.get("year_return")),
            "vol": num(row.get("realized_vol_annualized")),
            "dd": num(row.get("year_max_drawdown")),
            "first": num(row.get("first_close_usd")),
            "last": num(row.get("last_close_usd")),
            "min": num(row.get("min_close_usd")),
            "max": num(row.get("max_close_usd")),
            "obs": num(row.get("observations")),
            "partial": bool(row.get("is_partial_year")),
        })

    monthly = []
    for row in sheet_rows(wb, "MONTHLY_RETURNS"):
        monthly.append({
            "year": int(num(row.get("year")) or 0),
            "month": int(num(row.get("month")) or 0),
            "ret": num(row.get("monthly_return")),
            "dd": num(row.get("month_max_drawdown")),
            "partial": bool(row.get("is_partial_month")),
        })

    decisions = []
    for row in sheet_rows(wb, "DECISION_RULES"):
        decisions.append({
            "gate": clean(row.get("gate")),
            "metric": clean(row.get("metric")),
            "current": clean(row.get("current_value")),
            "rule": clean(row.get("rule")),
            "status": clean(row.get("status")),
            "note": clean(row.get("interpretation")),
        })

    quality = []
    for row in sheet_rows(wb, "DATA_QUALITY"):
        quality.append({
            "check": clean(row.get("check")),
            "result": clean(row.get("result")),
            "detail": clean(row.get("detail")),
        })

    sources = []
    for row in sheet_rows(wb, "SOURCES"):
        sources.append({
            "id": clean(row.get("source_id")),
            "provider": clean(row.get("provider")),
            "dataset": clean(row.get("dataset_or_endpoint")),
            "metrics": clean(row.get("metric_covered")),
            "coverage": f"{clean(row.get('coverage_start')) or '—'} — {clean(row.get('coverage_end')) or '—'}",
            "license": clean(row.get("license_or_terms")),
            "limitations": clean(row.get("known_limitations")),
            "url": clean(row.get("url")),
            "checked": clean(row.get("last_checked")),
        })

    # Peer table: latest common date across the four Coin Metrics peers, plus LTC.
    peer_rows = list(sheet_rows(wb, "PEER_DAILY"))
    by_asset_dates: dict[str, set] = {}
    for row in peer_rows:
        day = clean(row.get("date"))
        by_asset_dates.setdefault(row.get("asset"), set()).add(day)
    common = set.intersection(*by_asset_dates.values())
    latest_common = max(common)

    peers = [{
        "asset": "LTC",
        "name": "Litecoin",
        "price": kpi["price"],
        "mcap": kpi["mcap"],
        "supply": kpi["supply"],
        "aa": kpi["aa"],
        "tx": kpi["tx"],
        "hr": kpi["hr"],
        "blocks": 594,
        "source": "Base LTC dataset + Coin Metrics",
    }]
    order = ["BTC", "BCH", "DOGE", "DASH"]
    for asset in order:
        for row in peer_rows:
            if row.get("asset") == asset and clean(row.get("date")) == latest_common:
                peers.append({
                    "asset": asset,
                    "name": clean(row.get("asset_name")),
                    "price": num(row.get("cm_price_usd")),
                    "mcap": num(row.get("market_cap_usd")),
                    "supply": num(row.get("supply_native")),
                    "aa": num(row.get("active_addresses")),
                    "tx": num(row.get("tx_count")),
                    "hr": num(row.get("hashrate")),
                    "blocks": num(row.get("block_count")),
                    "source": clean(row.get("source")),
                })
                break

    wb.close()

    return {
        "meta": {
            "asset": "LTC",
            "name": "Litecoin",
            "as_of": kpi["coverage_end"],
            "coverage_start": kpi["coverage_start"],
            "coverage_end": kpi["coverage_end"],
            "observations": kpi["obs"],
            "date_gaps": kpi["gaps"],
            "calculated_at": kpi["calc_at"],
            "peer_date": latest_common,
            "source": "Uploaded LTC market file + Coin Metrics Community API v4 + Blockchair",
        },
        "kpi": kpi,
        "market": market,
        "yearly": yearly,
        "monthly": monthly,
        "peers": peers,
        "decisions": decisions,
        "quality": quality,
        "sources": sources,
    }


def load_echarts() -> str:
    if not ECHARTS_JS.exists():
        raise FileNotFoundError(
            f"ECharts not found: {ECHARTS_JS}. Download it with:\n"
            "  curl -sSL https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js "
            "-o 01_LTC/vendor/echarts.min.js"
        )
    return ECHARTS_JS.read_text(encoding="utf-8")


def build_html(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/")
    echarts = load_echarts().replace("</script", "<\\/script")
    template = HTML_TEMPLATE
    return (
        template.replace("__TITLE__", "Litecoin (LTC) — Investment Research Dashboard")
        .replace("__DATA__", payload)
        .replace("__ECHARTS__", echarts)
    )


def main() -> None:
    data = build_data()
    html = build_html(data)
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    size_mb = OUTPUT_HTML.stat().st_size / 1024 / 1024
    print(f"OK: {OUTPUT_HTML} ({size_mb:.2f} MB)")
    print(
        f"market={len(data['market'])} monthly={len(data['monthly'])} "
        f"yearly={len(data['yearly'])} peers={len(data['peers'])}"
    )


HTML_TEMPLATE = r"""<!doctype html>
<html lang="ru" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{
  --bg:#f3f5f9; --panel:#ffffff; --panel-2:#f8fafc; --text:#152033; --muted:#667085;
  --border:#e3e8f0; --grid:#eef2f7; --axis:#cbd5e1;
  --accent:#2563eb; --accent-2:#0f766e; --amber:#d97706; --red:#dc2626;
  --green:#15803d; --violet:#7c3aed; --slate:#64748b;
  --sidebar:#0d1729; --sidebar-2:#111f38; --sidebar-text:#cbd5e1; --sidebar-muted:#7f8ea8;
  --shadow:0 8px 24px rgba(15,23,42,.06); --radius:16px;
}
html[data-theme="dark"]{
  --bg:#080e1a; --panel:#0f1a2d; --panel-2:#111f36; --text:#e6edf7; --muted:#93a4bd;
  --border:#22314b; --grid:#18253b; --axis:#334155;
  --accent:#60a5fa; --accent-2:#2dd4bf; --amber:#fbbf24; --red:#f87171;
  --green:#4ade80; --violet:#a78bfa; --slate:#94a3b8;
  --sidebar:#060c17; --sidebar-2:#0c1628; --sidebar-text:#dbe5f3; --sidebar-muted:#7f8ea8;
  --shadow:0 10px 30px rgba(0,0,0,.3);
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif}
body{font-size:14px;line-height:1.45}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.app{display:flex;min-height:100vh}
.sidebar{position:fixed;inset:0 auto 0 0;width:242px;background:linear-gradient(180deg,var(--sidebar),var(--sidebar-2));
  color:var(--sidebar-text);padding:24px 16px;display:flex;flex-direction:column;z-index:20}
.brand{display:flex;align-items:center;gap:12px;padding:0 8px 22px;border-bottom:1px solid rgba(255,255,255,.08)}
.brand-mark{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,#2563eb,#0f766e);
  display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;color:#fff;letter-spacing:.5px}
.brand-title{font-weight:700;font-size:15px;color:#fff;line-height:1.2}
.brand-sub{font-size:11px;color:var(--sidebar-muted);margin-top:3px;text-transform:uppercase;letter-spacing:.8px}
.nav{display:flex;flex-direction:column;gap:4px;margin-top:20px}
.nav-label{font-size:10px;text-transform:uppercase;letter-spacing:1.2px;color:var(--sidebar-muted);padding:14px 10px 6px}
.nav button{appearance:none;border:0;background:transparent;color:var(--sidebar-text);text-align:left;
  padding:10px 12px;border-radius:10px;font-size:13px;cursor:pointer;display:flex;align-items:center;gap:10px;
  transition:background .15s,color .15s}
.nav button:hover{background:rgba(255,255,255,.06);color:#fff}
.nav button.active{background:rgba(96,165,250,.14);color:#fff;box-shadow:inset 3px 0 0 #60a5fa}
.nav .dot{width:7px;height:7px;border-radius:50%;background:#4b5f7d;flex:0 0 auto}
.nav button.active .dot{background:#60a5fa}
.sidebar-footer{margin-top:auto;padding:16px 8px 0;border-top:1px solid rgba(255,255,255,.08);
  font-size:10.5px;color:var(--sidebar-muted);line-height:1.5}
.main{margin-left:242px;width:calc(100% - 242px);padding:26px 30px 60px}
.topbar{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;margin-bottom:22px;flex-wrap:wrap}
.title h1{margin:0;font-size:26px;letter-spacing:-.4px;line-height:1.15}
.title p{margin:5px 0 0;color:var(--muted);font-size:13px}
.badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.badge{display:inline-flex;align-items:center;gap:6px;padding:5px 9px;border-radius:999px;border:1px solid var(--border);
  background:var(--panel);font-size:11px;color:var(--muted);font-weight:600}
.badge strong{color:var(--text);font-weight:700}
.badge.live{border-color:rgba(37,99,235,.35);background:rgba(37,99,235,.08);color:var(--accent)}
.topbar-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.seg{display:inline-flex;background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:3px;gap:2px}
.seg button{appearance:none;border:0;background:transparent;color:var(--muted);font-weight:600;font-size:12px;
  padding:7px 10px;border-radius:8px;cursor:pointer}
.seg button.active{background:var(--accent);color:#fff}
.btn{appearance:none;border:1px solid var(--border);background:var(--panel);color:var(--text);border-radius:10px;
  padding:8px 11px;font-size:12px;font-weight:600;cursor:pointer;display:inline-flex;align-items:center;gap:7px}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.page{display:none}
.page.active{display:block;animation:fade .22s ease}
@keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
.kpi-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:16px}
.kpi{position:relative;background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:15px 16px 14px;
  box-shadow:var(--shadow);overflow:hidden}
.kpi::before{content:"";position:absolute;inset:0 auto 0 0;width:3px;background:var(--slate)}
.kpi.pos::before{background:var(--green)} .kpi.neg::before{background:var(--red)}
.kpi.accent::before{background:var(--accent)} .kpi.warn::before{background:var(--amber)}
.kpi-label{font-size:11px;text-transform:uppercase;letter-spacing:.7px;color:var(--muted);font-weight:700}
.kpi-value{font-size:23px;font-weight:750;letter-spacing:-.4px;margin-top:5px}
.kpi-sub{font-size:11.5px;color:var(--muted);margin-top:3px}
.pos-text{color:var(--green)} .neg-text{color:var(--red)}
.status-strip{display:flex;align-items:center;justify-content:space-between;gap:16px;background:linear-gradient(90deg,rgba(220,38,38,.10),rgba(220,38,38,.02));
  border:1px solid rgba(220,38,38,.25);border-radius:14px;padding:13px 16px;margin-bottom:16px;flex-wrap:wrap}
.status-strip.pass{background:linear-gradient(90deg,rgba(21,128,61,.10),rgba(21,128,61,.02));border-color:rgba(21,128,61,.25)}
.status-strip.caution{background:linear-gradient(90deg,rgba(217,119,6,.12),rgba(217,119,6,.02));border-color:rgba(217,119,6,.25)}
.status-badge{display:inline-flex;align-items:center;padding:5px 10px;border-radius:999px;font-size:11px;font-weight:800;
  letter-spacing:.6px;text-transform:uppercase;background:rgba(220,38,38,.14);color:var(--red);margin-right:8px}
.status-strip.pass .status-badge{background:rgba(21,128,61,.14);color:var(--green)}
.status-strip.caution .status-badge{background:rgba(217,119,6,.16);color:var(--amber)}
.status-meta{font-size:12px;color:var(--muted)}
.section-head{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;margin:22px 0 12px}
.section-head h2{margin:0;font-size:17px;letter-spacing:-.2px}
.section-head p{margin:4px 0 0;color:var(--muted);font-size:12px}
.card{background:var(--panel);border:1px solid var(--border);border-radius:var(--radius);padding:16px;box-shadow:var(--shadow)}
.card-title{font-size:13px;font-weight:700;margin:0 0 2px}
.card-sub{font-size:11.5px;color:var(--muted);margin:0 0 8px}
.chart-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.chart-grid.three{grid-template-columns:repeat(3,minmax(0,1fr))}
.span-2{grid-column:span 2}
.chart{width:100%;height:310px}
.chart.tall{height:390px}
.chart.short{height:250px}
.note{font-size:11.5px;color:var(--muted);border-top:1px dashed var(--border);padding-top:9px;margin-top:2px;line-height:1.5}
.table-wrap{overflow:auto;border:1px solid var(--border);border-radius:12px}
table{width:100%;border-collapse:collapse;font-size:12px;min-width:640px}
th,td{padding:9px 11px;text-align:left;border-bottom:1px solid var(--border);vertical-align:top}
th{position:sticky;top:0;background:var(--panel-2);color:var(--muted);font-size:10.5px;text-transform:uppercase;letter-spacing:.6px;z-index:1}
tr:last-child td{border-bottom:0}
tbody tr:hover{background:rgba(37,99,235,.04)}
.num{text-align:right;font-variant-numeric:tabular-nums}
.tag{display:inline-flex;align-items:center;padding:3px 8px;border-radius:999px;font-size:10.5px;font-weight:800;letter-spacing:.4px}
.tag.pass{background:rgba(21,128,61,.12);color:var(--green)}
.tag.fail{background:rgba(220,38,38,.12);color:var(--red)}
.tag.mixed{background:rgba(217,119,6,.14);color:var(--amber)}
.tag.defensive{background:rgba(194,65,12,.14);color:#c2410c}
html[data-theme="dark"] .tag.defensive{color:#fb923c}
.tag.neutral{background:rgba(100,116,139,.14);color:var(--slate)}
.gates{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.gate{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:14px;box-shadow:var(--shadow)}
.gate-top{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:10px}
.gate-name{font-weight:750;font-size:13px}
.gate-value{font-size:15px;font-weight:700;margin:8px 0 4px}
.gate-rule{font-size:11.5px;color:var(--muted);line-height:1.45}
.gate-note{font-size:11px;color:var(--muted);border-top:1px dashed var(--border);padding-top:8px;margin-top:10px}
.coverage-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:14px}
.footer{margin-top:28px;padding-top:14px;border-top:1px solid var(--border);color:var(--muted);font-size:11px;line-height:1.6}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:11px}
.small{font-size:11px;color:var(--muted)}
.right{text-align:right}
.nowrap{white-space:nowrap}
@media (max-width: 1180px){
  .kpi-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
  .chart-grid{grid-template-columns:1fr}
  .span-2{grid-column:auto}
  .gates{grid-template-columns:repeat(2,minmax(0,1fr))}
  .coverage-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width: 860px){
  .app{display:block}
  .sidebar{position:static;width:100%;height:auto;padding:16px}
  .brand{padding-bottom:14px}
  .nav{flex-direction:row;overflow-x:auto;gap:6px;margin-top:12px;padding-bottom:4px}
  .nav-label{display:none}
  .nav button{white-space:nowrap;padding:8px 10px}
  .sidebar-footer{display:none}
  .main{margin-left:0;width:100%;padding:18px 14px 40px}
  .kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .gates{grid-template-columns:1fr}
  .topbar-actions{width:100%}
  .title h1{font-size:21px}
}
@media (max-width: 520px){
  .kpi-grid{grid-template-columns:1fr 1fr}
  .kpi-value{font-size:19px}
  .chart{height:270px}
  .chart.tall{height:330px}
}
@media print{
  body{background:#fff}
  .sidebar,.topbar-actions,.nav{display:none!important}
  .main{margin:0;width:100%;padding:0}
  .card,.kpi,.gate{box-shadow:none;break-inside:avoid}
  .page{display:none!important}
  .page.active{display:block!important}
  .chart{height:300px}
}
</style>
</head>
<body>
<div class="app">
  <aside class="sidebar">
    <div class="brand">
      <div class="brand-mark">LTC</div>
      <div>
        <div class="brand-title">Litecoin Research</div>
        <div class="brand-sub">Investment dashboard</div>
      </div>
    </div>
    <nav class="nav" id="nav">
      <div class="nav-label">Research</div>
      <button data-page="overview" class="active"><span class="dot"></span>Overview</button>
      <button data-page="onchain"><span class="dot"></span>On-chain</button>
      <button data-page="mining"><span class="dot"></span>Mining &amp; Supply</button>
      <button data-page="valuation"><span class="dot"></span>Valuation &amp; Peers</button>
      <button data-page="risk"><span class="dot"></span>Risk &amp; Returns</button>
      <button data-page="decision"><span class="dot"></span>Decision Gates</button>
      <div class="nav-label">Data</div>
      <button data-page="data"><span class="dot"></span>Data &amp; Sources</button>
    </nav>
    <div class="sidebar-footer">
      <div><strong id="sb-asof">—</strong></div>
      <div>Research POC · not investment advice</div>
      <div style="margin-top:8px">ECharts 5.5.0 · Apache-2.0</div>
    </div>
  </aside>

  <main class="main">
    <header class="topbar">
      <div class="title">
        <h1>Litecoin <span style="color:var(--muted);font-weight:500">(LTC)</span></h1>
        <p>Цена, сеть, майнинг, оценка и дисциплина принятия решений</p>
        <div class="badges">
          <span class="badge live">Research POC</span>
          <span class="badge">As of <strong id="asof-badge">—</strong></span>
          <span class="badge">Coverage <strong id="coverage-badge">—</strong></span>
          <span class="badge">On-chain: Coin Metrics + Blockchair</span>
        </div>
      </div>
      <div class="topbar-actions">
        <div class="seg" id="range-seg">
          <button data-range="1Y">1Y</button>
          <button data-range="3Y" class="active">3Y</button>
          <button data-range="All">All</button>
        </div>
        <button class="btn" id="csv-btn" type="button">CSV</button>
        <button class="btn" id="theme-btn" type="button">Dark</button>
        <button class="btn" id="print-btn" type="button">Print</button>
      </div>
    </header>

    <!-- OVERVIEW -->
    <section class="page active" id="page-overview">
      <div class="kpi-grid" id="overview-kpis"></div>
      <div class="status-strip" id="overview-status">
        <div><span class="status-badge" id="overview-status-badge">—</span><strong>Overall research state</strong></div>
        <div class="status-meta" id="overview-status-meta">—</div>
      </div>
      <div class="chart-grid">
        <div class="card span-2">
          <p class="card-title">LTC price with moving averages</p>
          <p class="card-sub">Daily close, MA30 and MA200. Use the range control to change the window.</p>
          <div class="chart tall" id="chart-price"></div>
        </div>
        <div class="card">
          <p class="card-title">Drawdown from ATH close</p>
          <p class="card-sub">Maximum daily close in the dataset — not the intraday all-time high.</p>
          <div class="chart" id="chart-drawdown"></div>
        </div>
        <div class="card">
          <p class="card-title">Raw volume</p>
          <p class="card-sub">Volume is kept as a raw field; the unit is not confirmed by the source.</p>
          <div class="chart" id="chart-volume"></div>
        </div>
      </div>
      <div class="footer">
        <strong>Read:</strong> price is below MA200, drawdown from the 2021 close high remains extreme,
        and 30-observation annualized volatility is high. This is a research snapshot, not a trading signal.
      </div>
    </section>

    <!-- ONCHAIN -->
    <section class="page" id="page-onchain">
      <div class="kpi-grid" id="onchain-kpis"></div>
      <div class="chart-grid">
        <div class="card span-2">
          <p class="card-title">Network activity</p>
          <p class="card-sub">Active addresses and transactions. Addresses are a proxy, not unique users.</p>
          <div class="chart tall" id="chart-activity"></div>
        </div>
        <div class="card">
          <p class="card-title">Hashrate</p>
          <p class="card-sub">Coin Metrics units. Hashrate is a security proxy, not a full attack-cost model.</p>
          <div class="chart" id="chart-hashrate"></div>
        </div>
        <div class="card">
          <p class="card-title">Fees vs issuance</p>
          <p class="card-sub">USD values derived from native units × Coin Metrics PriceUSD.</p>
          <div class="chart" id="chart-fees"></div>
        </div>
        <div class="card">
          <p class="card-title">Supply</p>
          <p class="card-sub">Visible LTC supply. The hard cap is 84,000,000 LTC.</p>
          <div class="chart" id="chart-supply"></div>
        </div>
        <div class="card">
          <p class="card-title">MVRV</p>
          <p class="card-sub">Coin Metrics provider metric. A low value is not a standalone buy signal.</p>
          <div class="chart" id="chart-mvrv"></div>
        </div>
      </div>
      <div class="footer">
        <strong>Read:</strong> activity is mixed — active addresses and transactions are weaker over 30 days,
        while hashrate is higher. Fees remain small relative to issuance, so the security budget is still
        dominated by the block subsidy.
      </div>
    </section>

    <!-- MINING -->
    <section class="page" id="page-mining">
      <div class="kpi-grid" id="mining-kpis"></div>
      <div class="chart-grid">
        <div class="card">
          <p class="card-title">Hashrate and difficulty</p>
          <p class="card-sub">Hashrate uses Coin Metrics units; difficulty is the daily average from Blockchair.</p>
          <div class="chart" id="chart-mining-hashrate"></div>
        </div>
        <div class="card">
          <p class="card-title">Miner revenue composition</p>
          <p class="card-sub">Gross miner revenue = subsidy + fees. This is revenue, not profit.</p>
          <div class="chart" id="chart-miner-revenue"></div>
        </div>
        <div class="card">
          <p class="card-title">Fee share of miner revenue</p>
          <p class="card-sub">A low fee share means the security budget depends on issuance.</p>
          <div class="chart" id="chart-fee-share"></div>
        </div>
        <div class="card">
          <p class="card-title">Supply and remaining supply</p>
          <p class="card-sub">Remaining supply to the 84M cap. Estimates do not model future halving dates.</p>
          <div class="chart" id="chart-remaining"></div>
        </div>
      </div>
      <div class="footer">
        <strong>Read:</strong> miner revenue is gross revenue before electricity, capex, pool fees and hedging.
        Miner cost is not observable from the public data used here, so do not present this as miner profitability.
      </div>
    </section>

    <!-- VALUATION -->
    <section class="page" id="page-valuation">
      <div class="kpi-grid" id="valuation-kpis"></div>
      <div class="chart-grid">
        <div class="card">
          <p class="card-title">Market cap vs realized cap</p>
          <p class="card-sub">Realized cap is derived as market cap / MVRV.</p>
          <div class="chart" id="chart-caps"></div>
        </div>
        <div class="card">
          <p class="card-title">Peer market cap</p>
          <p class="card-sub">Latest common date: <span id="peer-date">—</span>. LTC is highlighted.</p>
          <div class="chart" id="chart-peers"></div>
        </div>
        <div class="card span-2">
          <p class="card-title">Peer comparison table</p>
          <p class="card-sub">Different assets, different units. Compare market cap, activity and hashrate together, not one metric alone.</p>
          <div class="table-wrap"><table id="peer-table"></table></div>
        </div>
      </div>
      <div class="footer">
        <strong>Read:</strong> LTC trades at a low MVRV relative to its own history, but MVRV is a provider metric
        and a low reading is not a standalone buy signal. Peer comparison is descriptive, not a ranking.
      </div>
    </section>

    <!-- RISK -->
    <section class="page" id="page-risk">
      <div class="kpi-grid" id="risk-kpis"></div>
      <div class="chart-grid">
        <div class="card span-2">
          <p class="card-title">Rolling 30-observation annualized volatility</p>
          <p class="card-sub">Stdev of daily returns × sqrt(365). Crypto uses 365 periods per year.</p>
          <div class="chart" id="chart-volatility"></div>
        </div>
        <div class="card">
          <p class="card-title">Yearly returns</p>
          <p class="card-sub">First close to last close within each calendar year.</p>
          <div class="chart" id="chart-yearly-returns"></div>
        </div>
        <div class="card">
          <p class="card-title">Monthly return heatmap</p>
          <p class="card-sub">Calendar-month return. Partial months are marked in the tooltip.</p>
          <div class="chart" id="chart-heatmap"></div>
        </div>
        <div class="card span-2">
          <p class="card-title">Yearly risk table</p>
          <p class="card-sub">Return, realized volatility and maximum drawdown within each year.</p>
          <div class="table-wrap"><table id="yearly-table"></table></div>
        </div>
      </div>
      <div class="footer">
        <strong>Read:</strong> the asset has a long history of large drawdowns and high volatility.
        VaR is historical and empirical, not a forecast of the maximum possible loss.
      </div>
    </section>

    <!-- DECISION -->
    <section class="page" id="page-decision">
      <div class="status-strip" id="decision-status">
        <div><span class="status-badge" id="decision-status-badge">—</span><strong>Overall research state</strong></div>
        <div class="status-meta" id="decision-status-meta">—</div>
      </div>
      <div class="gates" id="gates"></div>
      <div class="footer">
        <strong>Framework:</strong> CONFIRMATION requires at least 3 PASS gates and no hard FAIL.
        CAUTION is a mixed picture. DEFENSIVE is 2 or more hard FAILs. This is a pre-trade review framework,
        not a personalized recommendation or a substitute for position limits.
      </div>
    </section>

    <!-- DATA -->
    <section class="page" id="page-data">
      <div class="coverage-grid" id="coverage-cards"></div>
      <div class="chart-grid">
        <div class="card span-2">
          <p class="card-title">Data quality checks</p>
          <p class="card-sub">Known limitations are part of the research output, not an afterthought.</p>
          <div class="table-wrap"><table id="quality-table"></table></div>
        </div>
        <div class="card span-2">
          <p class="card-title">Sources</p>
          <p class="card-sub">Provider, coverage, terms and known limitations.</p>
          <div class="table-wrap"><table id="sources-table"></table></div>
        </div>
      </div>
      <div class="footer">
        <strong>Reproduce:</strong> market data from the uploaded LTC file; on-chain, supply and peer data from
        Coin Metrics Community API v4; block-level aggregates from Blockchair. Review provider terms before
        commercial use. The dashboard is a research snapshot, not investment advice.
      </div>
    </section>
  </main>
</div>

<script>
const DATA = __DATA__;
</script>
<script>
__ECHARTS__
</script>
<script>
"use strict";

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));
const nf = new Intl.NumberFormat("en-US");
const cf = new Intl.NumberFormat("en-US", { notation: "compact", maximumFractionDigits: 2 });
const df = new Intl.DateTimeFormat("en-US", { year: "numeric", month: "short", day: "numeric" });

const state = {
  page: "overview",
  range: "3Y",
  theme: localStorage.getItem("ltc-theme") || "light",
};

const COLORS = {
  light: {
    accent: "#2563eb", accent2: "#0f766e", amber: "#d97706", red: "#dc2626",
    green: "#15803d", violet: "#7c3aed", slate: "#64748b",
    text: "#152033", muted: "#667085", border: "#e3e8f0", grid: "#eef2f7",
    axis: "#cbd5e1", panel: "#ffffff", panel2: "#f8fafc",
  },
  dark: {
    accent: "#60a5fa", accent2: "#2dd4bf", amber: "#fbbf24", red: "#f87171",
    green: "#4ade80", violet: "#a78bfa", slate: "#94a3b8",
    text: "#e6edf7", muted: "#93a4bd", border: "#22314b", grid: "#18253b",
    axis: "#334155", panel: "#0f1a2d", panel2: "#111f36",
  },
};
const C = () => COLORS[state.theme] || COLORS.light;

function fmtUSD(value, digits = 2) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "—";
  const v = Number(value);
  const abs = Math.abs(v);
  if (abs >= 1e12) return "$" + (v / 1e12).toFixed(2) + "T";
  if (abs >= 1e9) return "$" + (v / 1e9).toFixed(2) + "B";
  if (abs >= 1e6) return "$" + (v / 1e6).toFixed(2) + "M";
  if (abs >= 1e3) return "$" + (v / 1e3).toFixed(1) + "K";
  return "$" + v.toFixed(digits);
}
function fmtPct(value, digits = 2) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "—";
  return (Number(value) * 100).toFixed(digits) + "%";
}
function fmtNum(value, digits = 0) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "—";
  return nf.format(Number(Number(value).toFixed(digits)));
}
function fmtCompact(value, digits = 2) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "—";
  return cf.format(Number(value));
}
function fmtDate(value) {
  if (!value) return "—";
  const d = new Date(value + "T00:00:00Z");
  return Number.isNaN(d.getTime()) ? value : df.format(d);
}
function toneClass(value) {
  if (value === null || value === undefined) return "";
  return Number(value) > 0 ? "pos-text" : Number(value) < 0 ? "neg-text" : "";
}
function toneCard(value) {
  if (value === null || value === undefined) return "accent";
  return Number(value) > 0 ? "pos" : Number(value) < 0 ? "neg" : "accent";
}
function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[ch]));
}
function statusClass(status) {
  const s = String(status || "").toUpperCase();
  if (s === "PASS") return "pass";
  if (s === "FAIL") return "fail";
  if (s === "MIXED") return "mixed";
  if (s === "DEFENSIVE" || s === "CAUTION") return "defensive";
  return "neutral";
}
function parseDate(value) { return new Date(value + "T00:00:00Z"); }

function latestMarketDate() {
  return DATA.market[DATA.market.length - 1].d;
}
function filteredMarket() {
  if (state.range === "All") return DATA.market;
  const latest = parseDate(latestMarketDate());
  const years = state.range === "1Y" ? 1 : 3;
  const start = new Date(latest);
  start.setUTCFullYear(start.getUTCFullYear() - years);
  return DATA.market.filter((row) => parseDate(row.d) >= start);
}

function getChart(id) {
  const el = document.getElementById(id);
  if (!el) return null;
  let chart = echarts.getInstanceByDom(el);
  if (!chart) {
    chart = echarts.init(el, null, { renderer: "canvas" });
  }
  return chart;
}

function baseTooltip() {
  return {
    trigger: "axis",
    backgroundColor: C().panel,
    borderColor: C().border,
    textStyle: { color: C().text, fontSize: 12 },
    axisPointer: { type: "cross", label: { backgroundColor: C().accent } },
    extraCssText: "box-shadow:0 8px 24px rgba(0,0,0,.16);border-radius:10px;",
  };
}
function baseLegend(names) {
  return {
    data: names,
    top: 0,
    textStyle: { color: C().muted, fontSize: 11 },
    itemWidth: 14,
    itemHeight: 8,
  };
}
function dateAxis(data) {
  return {
    type: "category",
    data: data.map((row) => row.d),
    boundaryGap: false,
    axisLine: { lineStyle: { color: C().axis } },
    axisTick: { show: false },
    axisLabel: { color: C().muted, fontSize: 10, formatter: (value) => value.slice(0, 7) },
  };
}
function valueAxis(formatter, opts = {}) {
  return Object.assign({
    type: "value",
    scale: true,
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: C().muted, fontSize: 10, formatter },
    splitLine: { lineStyle: { color: C().grid } },
  }, opts);
}
function zoom() {
  return [
    { type: "inside", throttle: 50 },
    { type: "slider", height: 16, bottom: 8, borderColor: C().border, fillerColor: "rgba(37,99,235,.12)",
      handleStyle: { color: C().accent }, textStyle: { color: C().muted, fontSize: 9 } },
  ];
}
function gradient(colorTop, colorBottom) {
  return new echarts.graphic.LinearGradient(0, 0, 0, 1, [
    { offset: 0, color: colorTop },
    { offset: 1, color: colorBottom },
  ]);
}

/* ---------- KPI cards ---------- */
function kpiCard(label, value, sub = "", tone = "accent") {
  return `<div class="kpi ${tone}">
    <div class="kpi-label">${escapeHtml(label)}</div>
    <div class="kpi-value">${value}</div>
    <div class="kpi-sub">${sub}</div>
  </div>`;
}

function renderOverviewKpis() {
  const k = DATA.kpi;
  const cards = [
    kpiCard("Price", fmtUSD(k.price), fmtDate(DATA.meta.as_of), "accent"),
    kpiCard("1D return", fmtPct(k.r1), "Daily close-to-close", toneCard(k.r1)),
    kpiCard("30D return", fmtPct(k.r30), "Calendar 30 days", toneCard(k.r30)),
    kpiCard("YTD return", fmtPct(k.ytd), "From first close of year", toneCard(k.ytd)),
    kpiCard("Drawdown from ATH close", fmtPct(k.dd), "ATH " + fmtUSD(k.ath), "neg"),
    kpiCard("30D volatility", fmtPct(k.vol), "Annualized, sqrt(365)", "warn"),
    kpiCard("Market cap", fmtUSD(k.mcap), "Coin Metrics market cap", "accent"),
    kpiCard("MVRV", fmtNum(k.mvrv, 3), "Provider metric, not a standalone signal", "accent"),
  ];
  $("#overview-kpis").innerHTML = cards.join("");
}

function renderOnchainKpis() {
  const k = DATA.kpi;
  $("#onchain-kpis").innerHTML = [
    kpiCard("Active addresses", fmtNum(k.aa), "Addresses, not users", "accent"),
    kpiCard("Transactions", fmtNum(k.tx), "Daily count", "accent"),
    kpiCard("Hashrate", fmtNum(k.hr, 0), "Coin Metrics units", "accent2"),
    kpiCard("Market cap", fmtUSD(k.mcap), "Current snapshot", "accent"),
    kpiCard("Active addresses 30D", fmtPct(k.aa30), "Change over 30 days", toneCard(k.aa30)),
    kpiCard("Transactions 30D", fmtPct(k.tx30), "Change over 30 days", toneCard(k.tx30)),
    kpiCard("Hashrate 30D", fmtPct(k.hr30), "Change over 30 days", toneCard(k.hr30)),
    kpiCard("Fees / issuance 30D", fmtPct(k.fee_iss_ratio), "Trailing 30 days", "warn"),
  ].join("");
}

function renderMiningKpis() {
  const k = DATA.kpi;
  $("#mining-kpis").innerHTML = [
    kpiCard("Hashrate", fmtNum(k.hr, 0), "Coin Metrics units", "accent2"),
    kpiCard("Hashrate 30D", fmtPct(k.hr30), "Change over 30 days", toneCard(k.hr30)),
    kpiCard("Gross miner revenue 30D", fmtUSD(k.iss30 + k.fees30), "Subsidy + fees", "accent"),
    kpiCard("Fees 30D", fmtUSD(k.fees30), "Trailing 30 days", "warn"),
    kpiCard("Issuance 30D", fmtUSD(k.iss30), "Trailing 30 days", "accent"),
    kpiCard("Fee share", fmtPct(k.fees30 / (k.iss30 + k.fees30)), "Share of gross miner revenue", "warn"),
    kpiCard("Supply inflation", fmtPct(k.inflation), "Trailing 365 days", "warn"),
    kpiCard("Remaining to 84M", fmtNum(k.remaining, 0), "LTC hard cap", "accent"),
  ].join("");
}

function renderValuationKpis() {
  const k = DATA.kpi;
  $("#valuation-kpis").innerHTML = [
    kpiCard("Market cap", fmtUSD(k.mcap), "Current snapshot", "accent"),
    kpiCard("Realized cap", fmtUSD(k.rcap), "Market cap / MVRV", "accent2"),
    kpiCard("MVRV", fmtNum(k.mvrv, 3), "Provider metric, not a standalone signal", "accent"),
    kpiCard("Price", fmtUSD(k.price), fmtDate(DATA.meta.as_of), "accent"),
    kpiCard("52W high close", fmtUSD(k.hi52), "Maximum daily close", "warn"),
    kpiCard("52W low close", fmtUSD(k.lo52), "Minimum daily close", "warn"),
    kpiCard("Price vs MA200", fmtPct(k.vs_ma200), "Close vs MA200", toneCard(k.vs_ma200)),
    kpiCard("Peer date", fmtDate(DATA.meta.peer_date), "Latest common date", "accent"),
  ].join("");
}

function renderRiskKpis() {
  const k = DATA.kpi;
  $("#risk-kpis").innerHTML = [
    kpiCard("30D volatility", fmtPct(k.vol), "Annualized", "warn"),
    kpiCard("VaR 95% (30D)", fmtPct(k.var95), "Historical empirical", "neg"),
    kpiCard("VaR 99% (30D)", fmtPct(k.var99), "Historical empirical", "neg"),
    kpiCard("Sharpe (30D)", fmtNum(k.sharpe, 2), "MAR = 0", toneCard(k.sharpe)),
    kpiCard("Sortino (30D)", fmtNum(k.sortino, 2), "MAR = 0", toneCard(k.sortino)),
    kpiCard("Max drawdown", fmtPct(k.dd), "From ATH close", "neg"),
    kpiCard("365D return", fmtPct(k.r365), "Calendar 365 days", toneCard(k.r365)),
    kpiCard("90D return", fmtPct(k.r90), "Calendar 90 days", toneCard(k.r90)),
  ].join("");
}

/* ---------- Charts ---------- */
function renderPriceChart() {
  const data = filteredMarket();
  const chart = getChart("chart-price");
  if (!chart) return;
  chart.setOption({
    animationDuration: 450,
    grid: { left: 60, right: 24, top: 34, bottom: 66, containLabel: true },
    tooltip: Object.assign(baseTooltip(), {
      formatter: (params) => {
        const idx = params[0].dataIndex;
        const row = data[idx];
        return `<strong>${row.d}</strong><br/>Close: ${fmtUSD(row.c)}<br/>MA30: ${fmtUSD(row.ma30)}<br/>MA200: ${fmtUSD(row.ma200)}`;
      },
    }),
    legend: baseLegend(["LTC close", "MA30", "MA200"]),
    xAxis: dateAxis(data),
    yAxis: valueAxis((value) => "$" + Number(value).toFixed(0)),
    dataZoom: zoom(),
    series: [
      { name: "LTC close", type: "line", data: data.map((row) => row.c), showSymbol: false, smooth: false,
        lineStyle: { width: 2, color: C().accent },
        areaStyle: { color: gradient("rgba(37,99,235,.26)", "rgba(37,99,235,0)") },
        emphasis: { focus: "series" } },
      { name: "MA30", type: "line", data: data.map((row) => row.ma30), showSymbol: false,
        lineStyle: { width: 1.4, color: C().amber }, emphasis: { focus: "series" } },
      { name: "MA200", type: "line", data: data.map((row) => row.ma200), showSymbol: false,
        lineStyle: { width: 1.4, color: C().violet }, emphasis: { focus: "series" } },
    ],
  }, true);
}

function renderDrawdownChart() {
  const data = filteredMarket();
  const chart = getChart("chart-drawdown");
  if (!chart) return;
  chart.setOption({
    grid: { left: 48, right: 18, top: 16, bottom: 36, containLabel: true },
    tooltip: Object.assign(baseTooltip(), { formatter: (params) => `${params[0].axisValue}<br/>Drawdown: ${fmtPct(params[0].value)}` }),
    xAxis: dateAxis(data),
    yAxis: valueAxis((value) => (Number(value) * 100).toFixed(0) + "%", { max: 0 }),
    series: [{
      name: "Drawdown", type: "line", data: data.map((row) => row.dd), showSymbol: false,
      lineStyle: { width: 1.5, color: C().red },
      areaStyle: { color: gradient("rgba(220,38,38,.30)", "rgba(220,38,38,.02)") },
    }],
  }, true);
}

function renderVolumeChart() {
  const data = filteredMarket();
  const chart = getChart("chart-volume");
  if (!chart) return;
  chart.setOption({
    grid: { left: 52, right: 18, top: 16, bottom: 36, containLabel: true },
    tooltip: Object.assign(baseTooltip(), { formatter: (params) => `${params[0].axisValue}<br/>Raw volume: ${fmtNum(params[0].value)}` }),
    xAxis: dateAxis(data),
    yAxis: valueAxis((value) => fmtCompact(value)),
    series: [{
      name: "Volume", type: "bar", data: data.map((row) => row.v),
      itemStyle: { color: "rgba(37,99,235,.55)", borderRadius: [2, 2, 0, 0] },
    }],
  }, true);
}

function renderActivityChart() {
  const data = filteredMarket();
  const chart = getChart("chart-activity");
  if (!chart) return;
  chart.setOption({
    grid: { left: 58, right: 62, top: 34, bottom: 66, containLabel: true },
    tooltip: Object.assign(baseTooltip(), {
      formatter: (params) => {
        const row = data[params[0].dataIndex];
        return `<strong>${row.d}</strong><br/>Active addresses: ${fmtNum(row.aa)}<br/>Transactions: ${fmtNum(row.tx)}`;
      },
    }),
    legend: baseLegend(["Active addresses", "Transactions"]),
    xAxis: dateAxis(data),
    yAxis: [
      valueAxis((value) => fmtCompact(value)),
      valueAxis((value) => fmtCompact(value), { splitLine: { show: false } }),
    ],
    dataZoom: zoom(),
    series: [
      { name: "Active addresses", type: "line", yAxisIndex: 0, data: data.map((row) => row.aa),
        showSymbol: false, lineStyle: { width: 1.8, color: C().accent },
        areaStyle: { color: gradient("rgba(37,99,235,.18)", "rgba(37,99,235,0)") } },
      { name: "Transactions", type: "line", yAxisIndex: 1, data: data.map((row) => row.tx),
        showSymbol: false, lineStyle: { width: 1.6, color: C().amber } },
    ],
  }, true);
}

function renderHashrateChart() {
  const data = filteredMarket();
  const chart = getChart("chart-hashrate");
  if (!chart) return;
  chart.setOption({
    grid: { left: 56, right: 18, top: 16, bottom: 36, containLabel: true },
    tooltip: Object.assign(baseTooltip(), { formatter: (params) => `${params[0].axisValue}<br/>Hashrate: ${fmtNum(params[0].value, 1)}` }),
    xAxis: dateAxis(data),
    yAxis: valueAxis((value) => fmtCompact(value)),
    series: [{
      name: "Hashrate", type: "line", data: data.map((row) => row.hr), showSymbol: false,
      lineStyle: { width: 1.7, color: C().accent2 },
      areaStyle: { color: gradient("rgba(15,118,110,.22)", "rgba(15,118,110,0)") },
    }],
  }, true);
}

function renderFeesChart() {
  const data = filteredMarket();
  const chart = getChart("chart-fees");
  if (!chart) return;
  chart.setOption({
    grid: { left: 62, right: 62, top: 34, bottom: 36, containLabel: true },
    tooltip: Object.assign(baseTooltip(), {
      formatter: (params) => {
        const row = data[params[0].dataIndex];
        return `<strong>${row.d}</strong><br/>Issuance: ${fmtUSD(row.iss)}<br/>Fees: ${fmtUSD(row.fees)}<br/>Fee share: ${fmtPct(row.fee_share)}`;
      },
    }),
    legend: baseLegend(["Issuance", "Fees"]),
    xAxis: dateAxis(data),
    yAxis: [
      valueAxis((value) => fmtUSD(value)),
      valueAxis((value) => fmtUSD(value), { splitLine: { show: false } }),
    ],
    series: [
      { name: "Issuance", type: "bar", yAxisIndex: 0, data: data.map((row) => row.iss),
        itemStyle: { color: "rgba(37,99,235,.55)", borderRadius: [2, 2, 0, 0] } },
      { name: "Fees", type: "line", yAxisIndex: 1, data: data.map((row) => row.fees),
        showSymbol: false, lineStyle: { width: 1.6, color: C().amber } },
    ],
  }, true);
}

function renderSupplyChart() {
  const data = filteredMarket();
  const chart = getChart("chart-supply");
  if (!chart) return;
  chart.setOption({
    grid: { left: 58, right: 18, top: 16, bottom: 36, containLabel: true },
    tooltip: Object.assign(baseTooltip(), {
      formatter: (params) => {
        const row = data[params[0].dataIndex];
        return `<strong>${row.d}</strong><br/>Supply: ${fmtNum(row.sup, 0)} LTC<br/>Mined: ${fmtPct(row.mined)}`;
      },
    }),
    xAxis: dateAxis(data),
    yAxis: valueAxis((value) => fmtCompact(value) + " LTC"),
    series: [{
      name: "Supply", type: "line", data: data.map((row) => row.sup), showSymbol: false,
      lineStyle: { width: 1.8, color: C().accent },
      areaStyle: { color: gradient("rgba(37,99,235,.20)", "rgba(37,99,235,0)") },
    }],
  }, true);
}

function renderMvrvChart() {
  const data = filteredMarket();
  const chart = getChart("chart-mvrv");
  if (!chart) return;
  chart.setOption({
    grid: { left: 48, right: 18, top: 16, bottom: 40, containLabel: true },
    tooltip: Object.assign(baseTooltip(), { formatter: (params) => `${params[0].axisValue}<br/>MVRV: ${fmtNum(params[0].value, 3)}` }),
    xAxis: dateAxis(data),
    yAxis: valueAxis((value) => Number(value).toFixed(1)),
    series: [{
      name: "MVRV", type: "line", data: data.map((row) => row.mvrv), showSymbol: false,
      lineStyle: { width: 1.7, color: C().violet },
      markLine: { silent: true, symbol: "none", lineStyle: { color: C().slate, type: "dashed" },
        label: { color: C().muted, formatter: "MVRV = 1" }, data: [{ yAxis: 1 }] },
    }],
  }, true);
}

function renderMiningHashrateChart() {
  const data = filteredMarket();
  const chart = getChart("chart-mining-hashrate");
  if (!chart) return;
  chart.setOption({
    grid: { left: 62, right: 62, top: 34, bottom: 36, containLabel: true },
    tooltip: Object.assign(baseTooltip(), {
      formatter: (params) => {
        const row = data[params[0].dataIndex];
        return `<strong>${row.d}</strong><br/>Hashrate: ${fmtNum(row.hr, 1)}<br/>Difficulty: ${fmtCompact(row.diff)}`;
      },
    }),
    legend: baseLegend(["Hashrate", "Difficulty"]),
    xAxis: dateAxis(data),
    yAxis: [
      valueAxis((value) => fmtCompact(value)),
      valueAxis((value) => fmtCompact(value), { splitLine: { show: false } }),
    ],
    series: [
      { name: "Hashrate", type: "line", yAxisIndex: 0, data: data.map((row) => row.hr),
        showSymbol: false, lineStyle: { width: 1.7, color: C().accent2 } },
      { name: "Difficulty", type: "line", yAxisIndex: 1, data: data.map((row) => row.diff),
        showSymbol: false, lineStyle: { width: 1.4, color: C().violet } },
    ],
  }, true);
}

function renderMinerRevenueChart() {
  const data = filteredMarket();
  const chart = getChart("chart-miner-revenue");
  if (!chart) return;
  chart.setOption({
    grid: { left: 62, right: 18, top: 34, bottom: 36, containLabel: true },
    tooltip: Object.assign(baseTooltip(), {
      formatter: (params) => {
        const row = data[params[0].dataIndex];
        return `<strong>${row.d}</strong><br/>Issuance: ${fmtUSD(row.iss)}<br/>Fees: ${fmtUSD(row.fees)}<br/>Gross: ${fmtUSD(row.iss + row.fees)}`;
      },
    }),
    legend: baseLegend(["Issuance", "Fees"]),
    xAxis: dateAxis(data),
    yAxis: valueAxis((value) => fmtUSD(value)),
    series: [
      { name: "Issuance", type: "bar", stack: "revenue", data: data.map((row) => row.iss),
        itemStyle: { color: "rgba(37,99,235,.60)" } },
      { name: "Fees", type: "bar", stack: "revenue", data: data.map((row) => row.fees),
        itemStyle: { color: "rgba(217,119,6,.75)" } },
    ],
  }, true);
}

function renderFeeShareChart() {
  const data = filteredMarket();
  const chart = getChart("chart-fee-share");
  if (!chart) return;
  chart.setOption({
    grid: { left: 48, right: 18, top: 16, bottom: 36, containLabel: true },
    tooltip: Object.assign(baseTooltip(), { formatter: (params) => `${params[0].axisValue}<br/>Fee share: ${fmtPct(params[0].value)}` }),
    xAxis: dateAxis(data),
    yAxis: valueAxis((value) => (Number(value) * 100).toFixed(1) + "%"),
    series: [{
      name: "Fee share", type: "line", data: data.map((row) => row.fee_share), showSymbol: false,
      lineStyle: { width: 1.6, color: C().amber },
      areaStyle: { color: gradient("rgba(217,119,6,.22)", "rgba(217,119,6,0)") },
    }],
  }, true);
}

function renderRemainingChart() {
  const data = filteredMarket();
  const chart = getChart("chart-remaining");
  if (!chart) return;
  chart.setOption({
    grid: { left: 58, right: 18, top: 16, bottom: 36, containLabel: true },
    tooltip: Object.assign(baseTooltip(), {
      formatter: (params) => {
        const row = data[params[0].dataIndex];
        return `<strong>${row.d}</strong><br/>Supply: ${fmtNum(row.sup, 0)} LTC<br/>Remaining: ${fmtNum(row.remaining, 0)} LTC`;
      },
    }),
    xAxis: dateAxis(data),
    yAxis: valueAxis((value) => fmtCompact(value) + " LTC"),
    series: [{
      name: "Remaining supply", type: "line", data: data.map((row) => row.remaining), showSymbol: false,
      lineStyle: { width: 1.7, color: C().amber },
      areaStyle: { color: gradient("rgba(217,119,6,.20)", "rgba(217,119,6,0)") },
    }],
  }, true);
}

function renderCapsChart() {
  const data = filteredMarket();
  const chart = getChart("chart-caps");
  if (!chart) return;
  chart.setOption({
    grid: { left: 62, right: 18, top: 34, bottom: 36, containLabel: true },
    tooltip: Object.assign(baseTooltip(), {
      formatter: (params) => {
        const row = data[params[0].dataIndex];
        return `<strong>${row.d}</strong><br/>Market cap: ${fmtUSD(row.mc)}<br/>Realized cap: ${fmtUSD(row.rcap)}<br/>MVRV: ${fmtNum(row.mvrv, 3)}`;
      },
    }),
    legend: baseLegend(["Market cap", "Realized cap"]),
    xAxis: dateAxis(data),
    yAxis: valueAxis((value) => fmtUSD(value)),
    series: [
      { name: "Market cap", type: "line", data: data.map((row) => row.mc), showSymbol: false,
        lineStyle: { width: 1.7, color: C().accent },
        areaStyle: { color: gradient("rgba(37,99,235,.18)", "rgba(37,99,235,0)") } },
      { name: "Realized cap", type: "line", data: data.map((row) => row.rcap), showSymbol: false,
        lineStyle: { width: 1.5, color: C().accent2 } },
    ],
  }, true);
}

function renderPeersChart() {
  const chart = getChart("chart-peers");
  if (!chart) return;
  const peers = DATA.peers.slice().sort((a, b) => (a.mcap || 0) - (b.mcap || 0));
  chart.setOption({
    grid: { left: 58, right: 70, top: 18, bottom: 24, containLabel: true },
    tooltip: Object.assign(baseTooltip(), {
      formatter: (params) => {
        const item = peers[params.dataIndex];
        return `<strong>${escapeHtml(item.name)} (${escapeHtml(item.asset)})</strong><br/>Market cap: ${fmtUSD(item.mcap)}`;
      },
    }),
    xAxis: { type: "log", axisLabel: { color: C().muted, fontSize: 10, formatter: (value) => fmtUSD(value) },
      splitLine: { lineStyle: { color: C().grid } } },
    yAxis: { type: "category", data: peers.map((item) => item.asset), axisLine: { show: false },
      axisTick: { show: false }, axisLabel: { color: C().text, fontWeight: 600 } },
    series: [{
      type: "bar", data: peers.map((item) => item.mcap), barWidth: "55%",
      itemStyle: { color: (params) => peers[params.dataIndex].asset === "LTC" ? C().accent : "rgba(100,116,139,.55)",
        borderRadius: [0, 6, 6, 0] },
      label: { show: true, position: "right", color: C().muted, fontSize: 10, formatter: (params) => fmtUSD(params.value) },
    }],
  }, true);
}

function renderVolatilityChart() {
  const data = filteredMarket();
  const chart = getChart("chart-volatility");
  if (!chart) return;
  chart.setOption({
    grid: { left: 48, right: 18, top: 16, bottom: 66, containLabel: true },
    tooltip: Object.assign(baseTooltip(), { formatter: (params) => `${params[0].axisValue}<br/>Volatility: ${fmtPct(params[0].value)}` }),
    xAxis: dateAxis(data),
    yAxis: valueAxis((value) => (Number(value) * 100).toFixed(0) + "%"),
    dataZoom: zoom(),
    series: [{
      name: "Volatility", type: "line", data: data.map((row) => row.vol), showSymbol: false,
      lineStyle: { width: 1.7, color: C().amber },
      areaStyle: { color: gradient("rgba(217,119,6,.22)", "rgba(217,119,6,0)") },
    }],
  }, true);
}

function renderYearlyReturnsChart() {
  const chart = getChart("chart-yearly-returns");
  if (!chart) return;
  const years = DATA.yearly.map((row) => String(row.year));
  const values = DATA.yearly.map((row) => row.ret);
  chart.setOption({
    grid: { left: 48, right: 18, top: 16, bottom: 32, containLabel: true },
    tooltip: Object.assign(baseTooltip(), { formatter: (params) => `${params[0].axisValue}<br/>Return: ${fmtPct(params[0].value)}` }),
    xAxis: { type: "category", data: years, axisLine: { lineStyle: { color: C().axis } },
      axisTick: { show: false }, axisLabel: { color: C().muted, fontSize: 10 } },
    yAxis: valueAxis((value) => (Number(value) * 100).toFixed(0) + "%"),
    series: [{
      type: "bar", data: values, barWidth: "58%",
      itemStyle: { color: (params) => params.value >= 0 ? C().green : C().red, borderRadius: [4, 4, 0, 0] },
      label: { show: true, position: "top", color: C().muted, fontSize: 9,
        formatter: (params) => (params.value * 100).toFixed(0) + "%" },
    }],
  }, true);
}

function renderHeatmap() {
  const chart = getChart("chart-heatmap");
  if (!chart) return;
  const years = Array.from(new Set(DATA.monthly.map((row) => row.year))).sort();
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const values = DATA.monthly.map((row) => [row.month - 1, years.indexOf(row.year), row.ret, row.partial]);
  chart.setOption({
    grid: { left: 48, right: 16, top: 16, bottom: 52, containLabel: true },
    tooltip: {
      backgroundColor: C().panel, borderColor: C().border, textStyle: { color: C().text, fontSize: 12 },
      formatter: (params) => {
        const [monthIndex, yearIndex, value, partial] = params.value;
        return `<strong>${years[yearIndex]}-${String(monthIndex + 1).padStart(2, "0")}</strong><br/>Return: ${fmtPct(value)}${partial ? " (partial)" : ""}`;
      },
    },
    xAxis: { type: "category", data: months, axisLine: { show: false }, axisTick: { show: false },
      axisLabel: { color: C().muted, fontSize: 9 }, splitArea: { show: false } },
    yAxis: { type: "category", data: years.map(String), axisLine: { show: false }, axisTick: { show: false },
      axisLabel: { color: C().muted, fontSize: 9 } },
    visualMap: {
      min: -0.6, max: 0.6, calculable: false, orient: "horizontal", left: "center", bottom: 0,
      itemWidth: 10, itemHeight: 90, textStyle: { color: C().muted, fontSize: 9 },
      inRange: { color: ["#b91c1c", "#fca5a5", "#f8fafc", "#86efac", "#15803d"] },
    },
    series: [{
      type: "heatmap", data: values,
      label: { show: true, color: C().text, fontSize: 8,
        formatter: (params) => Math.abs(params.value[2]) >= 0.15 ? (params.value[2] * 100).toFixed(0) : "" },
      itemStyle: { borderColor: C().panel, borderWidth: 2, borderRadius: 3 },
      emphasis: { itemStyle: { shadowBlur: 8, shadowColor: "rgba(0,0,0,.25)" } },
    }],
  }, true);
}

/* ---------- Tables ---------- */
function renderPeerTable() {
  const table = $("#peer-table");
  const peers = DATA.peers.slice().sort((a, b) => (b.mcap || 0) - (a.mcap || 0));
  const rows = peers.map((item) => `
    <tr>
      <td><strong>${escapeHtml(item.asset)}</strong> <span class="small">${escapeHtml(item.name)}</span></td>
      <td class="num">${fmtUSD(item.price)}</td>
      <td class="num">${fmtUSD(item.mcap)}</td>
      <td class="num">${fmtNum(item.aa)}</td>
      <td class="num">${fmtNum(item.tx)}</td>
      <td class="num">${fmtNum(item.hr, 0)}</td>
      <td class="num">${fmtNum(item.blocks)}</td>
      <td class="small">${escapeHtml(item.source)}</td>
    </tr>`).join("");
  table.innerHTML = `<thead><tr>
    <th>Asset</th><th class="num">Price</th><th class="num">Market cap</th>
    <th class="num">Active addresses</th><th class="num">Transactions</th>
    <th class="num">Hashrate</th><th class="num">Blocks</th><th>Source</th>
  </tr></thead><tbody>${rows}</tbody>`;
  $("#peer-date").textContent = fmtDate(DATA.meta.peer_date);
}

function renderYearlyTable() {
  const table = $("#yearly-table");
  const rows = DATA.yearly.map((row) => `
    <tr>
      <td><strong>${row.year}</strong>${row.partial ? ' <span class="tag neutral">partial</span>' : ""}</td>
      <td class="num ${toneClass(row.ret)}">${fmtPct(row.ret)}</td>
      <td class="num">${fmtPct(row.vol)}</td>
      <td class="num neg-text">${fmtPct(row.dd)}</td>
      <td class="num">${fmtUSD(row.first)}</td>
      <td class="num">${fmtUSD(row.last)}</td>
      <td class="num">${fmtUSD(row.min)}</td>
      <td class="num">${fmtUSD(row.max)}</td>
      <td class="num">${fmtNum(row.obs)}</td>
    </tr>`).join("");
  table.innerHTML = `<thead><tr>
    <th>Year</th><th class="num">Return</th><th class="num">Realized vol</th><th class="num">Max drawdown</th>
    <th class="num">First close</th><th class="num">Last close</th><th class="num">Min close</th><th class="num">Max close</th><th class="num">Days</th>
  </tr></thead><tbody>${rows}</tbody>`;
}

function renderGates() {
  const container = $("#gates");
  const overall = DATA.decisions.find((row) => row.gate === "Overall research state");
  const gates = DATA.decisions.filter((row) => row.gate !== "Overall research state");
  const k = DATA.kpi;
  const latest = DATA.market[DATA.market.length - 1];
  const displayByGate = {
    "Market trend": `${fmtPct(k.vs_ma200)} vs MA200`,
    "Momentum": `30D ${fmtPct(k.r30)} · 90D ${fmtPct(k.r90)}`,
    "Adoption": `Addresses ${fmtPct(k.aa30)} · TX ${fmtPct(k.tx30)} (30D)`,
    "Security": `Hashrate ${fmtPct(k.hr30)} · ${fmtNum(latest.blocks)} blocks`,
    "Data completeness": "Coin Metrics v4 refreshed",
  };
  container.innerHTML = gates.map((row) => `
    <div class="gate">
      <div class="gate-top">
        <div class="gate-name">${escapeHtml(row.gate)}</div>
        <span class="tag ${statusClass(row.status)}">${escapeHtml(row.status)}</span>
      </div>
      <div class="gate-value">${escapeHtml(displayByGate[row.gate] || row.current)}</div>
      <div class="gate-rule">${escapeHtml(row.rule)}</div>
      <div class="gate-note">${escapeHtml(row.note)}</div>
    </div>`).join("");
  if (overall) {
    const passes = DATA.decisions.filter((row) => row.status === "PASS").length;
    const fails = DATA.decisions.filter((row) => row.status === "FAIL").length;
    const mixed = DATA.decisions.filter((row) => row.status === "MIXED").length;
    $("#decision-status-badge").textContent = overall.status;
    $("#decision-status-meta").textContent = `${passes} PASS · ${fails} FAIL · ${mixed} MIXED · ${overall.note}`;
    $("#decision-status").className = "status-strip " + statusClass(overall.status);
  }
}

function renderOverviewStatus() {
  const overall = DATA.decisions.find((row) => row.gate === "Overall research state");
  const passes = DATA.decisions.filter((row) => row.status === "PASS").length;
  const fails = DATA.decisions.filter((row) => row.status === "FAIL").length;
  const mixed = DATA.decisions.filter((row) => row.status === "MIXED").length;
  const badge = $("#overview-status-badge");
  const meta = $("#overview-status-meta");
  const strip = $("#overview-status");
  if (overall) {
    badge.textContent = overall.status;
    meta.textContent = `${passes} PASS · ${fails} FAIL · ${mixed} MIXED · ${overall.note}`;
    strip.className = "status-strip " + statusClass(overall.status);
  }
}

function renderCoverage() {
  const k = DATA.kpi;
  $("#coverage-cards").innerHTML = [
    kpiCard("Coverage start", fmtDate(k.coverage_start), "First market observation", "accent"),
    kpiCard("Coverage end", fmtDate(k.coverage_end), "Last market observation", "accent"),
    kpiCard("Observations", fmtNum(k.obs), "Daily rows after sorting", "accent"),
    kpiCard("Date gaps", fmtNum(k.gaps), "Missing dates, not interpolated", "warn"),
  ].join("");
}

function renderQualityTable() {
  const table = $("#quality-table");
  const rows = DATA.quality.map((row) => `
    <tr><td><strong>${escapeHtml(row.check)}</strong></td>
    <td>${escapeHtml(row.result)}</td>
    <td class="small">${escapeHtml(row.detail)}</td></tr>`).join("");
  table.innerHTML = `<thead><tr><th>Check</th><th>Result</th><th>Detail</th></tr></thead><tbody>${rows}</tbody>`;
}

function renderSourcesTable() {
  const table = $("#sources-table");
  const rows = DATA.sources.map((row) => {
    const link = row.url ? `<a href="${escapeHtml(row.url)}" target="_blank" rel="noopener">${escapeHtml(row.dataset)}</a>` : escapeHtml(row.dataset);
    return `<tr>
      <td class="mono">${escapeHtml(row.id)}</td>
      <td><strong>${escapeHtml(row.provider)}</strong><div class="small">${link}</div></td>
      <td>${escapeHtml(row.metrics)}</td>
      <td class="small">${escapeHtml(row.coverage)}</td>
      <td class="small">${escapeHtml(row.limitations)}</td>
    </tr>`;
  }).join("");
  table.innerHTML = `<thead><tr><th>ID</th><th>Provider / dataset</th><th>Metrics</th><th>Coverage</th><th>Known limitations</th></tr></thead><tbody>${rows}</tbody>`;
}

/* ---------- Page renderer ---------- */
const renderers = {
  overview: () => { renderOverviewKpis(); renderOverviewStatus(); renderPriceChart(); renderDrawdownChart(); renderVolumeChart(); },
  onchain: () => { renderOnchainKpis(); renderActivityChart(); renderHashrateChart(); renderFeesChart(); renderSupplyChart(); renderMvrvChart(); },
  mining: () => { renderMiningKpis(); renderMiningHashrateChart(); renderMinerRevenueChart(); renderFeeShareChart(); renderRemainingChart(); },
  valuation: () => { renderValuationKpis(); renderCapsChart(); renderPeersChart(); renderPeerTable(); },
  risk: () => { renderRiskKpis(); renderVolatilityChart(); renderYearlyReturnsChart(); renderHeatmap(); renderYearlyTable(); },
  decision: () => { renderGates(); },
  data: () => { renderCoverage(); renderQualityTable(); renderSourcesTable(); },
};

function renderPage(page) {
  const fn = renderers[page];
  if (fn) fn();
  requestAnimationFrame(() => {
    $$(".page.active .chart").forEach((el) => {
      const chart = echarts.getInstanceByDom(el);
      if (chart) chart.resize();
    });
  });
}

function activatePage(page) {
  state.page = page;
  $$(".page").forEach((section) => section.classList.toggle("active", section.id === "page-" + page));
  $$("#nav button").forEach((button) => button.classList.toggle("active", button.dataset.page === page));
  if (location.hash.slice(1) !== page) history.replaceState(null, "", "#" + page);
  renderPage(page);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ---------- Actions ---------- */
function setRange(range) {
  state.range = range;
  $$("#range-seg button").forEach((button) => button.classList.toggle("active", button.dataset.range === range));
  renderPage(state.page);
}

function setTheme(theme) {
  state.theme = theme;
  document.documentElement.dataset.theme = theme;
  localStorage.setItem("ltc-theme", theme);
  $("#theme-btn").textContent = theme === "dark" ? "Light" : "Dark";
  renderPage(state.page);
}

function downloadCsv() {
  const data = filteredMarket();
  const header = ["date", "price_close_usd", "volume_raw", "return_1d", "return_30d", "ytd_return",
    "ma_30_usd", "ma_200_usd", "drawdown_from_ath", "volatility_30d_annualized",
    "market_cap_usd", "active_addresses", "tx_count", "hashrate", "supply_ltc", "mvrv"];
  const lines = [header.join(",")];
  for (const row of data) {
    lines.push([row.d, row.c, row.v, row.r1, row.r30, row.ytd, row.ma30, row.ma200,
      row.dd, row.vol, row.mc, row.aa, row.tx, row.hr, row.sup, row.mvrv]
      .map((value) => value === null || value === undefined ? "" : value).join(","));
  }
  const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "ltc_dashboard_data.csv";
  link.click();
  URL.revokeObjectURL(link.href);
}

/* ---------- Init ---------- */
document.addEventListener("DOMContentLoaded", () => {
  document.documentElement.dataset.theme = state.theme;
  $("#theme-btn").textContent = state.theme === "dark" ? "Light" : "Dark";
  $("#asof-badge").textContent = fmtDate(DATA.meta.as_of);
  $("#coverage-badge").textContent = `${DATA.meta.coverage_start} — ${DATA.meta.coverage_end}`;
  $("#sb-asof").textContent = "As of " + fmtDate(DATA.meta.as_of);

  $$("#nav button").forEach((button) => button.addEventListener("click", () => activatePage(button.dataset.page)));
  $$("#range-seg button").forEach((button) => button.addEventListener("click", () => setRange(button.dataset.range)));
  $("#theme-btn").addEventListener("click", () => setTheme(state.theme === "dark" ? "light" : "dark"));
  $("#print-btn").addEventListener("click", () => window.print());
  $("#csv-btn").addEventListener("click", downloadCsv);

  const initialPage = location.hash.replace("#", "");
  activatePage(renderers[initialPage] ? initialPage : "overview");
  window.addEventListener("hashchange", () => {
    const page = location.hash.replace("#", "");
    if (renderers[page] && page !== state.page) activatePage(page);
  });
  window.addEventListener("resize", () => {
    $$(".chart").forEach((el) => {
      const chart = echarts.getInstanceByDom(el);
      if (chart) chart.resize();
    });
  });
});
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
