#!/usr/bin/env python3
"""Build the weekly ETHFI digest from the latest verified snapshot.

Default: read the committed metrics, compare with reports/latest.json, write a
Markdown digest and a small JSON state file. No network.

--refresh: fetch a new on-chain snapshot first, rebuild metrics, then digest.
--telegram: also send the digest if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
are set (otherwise the digest is still written and the reason is printed).

The digest is deliberately a checklist, not a new thesis: it shows whether the
published upgrade / invalidation triggers moved.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = HERE / "data" / "ethfi_metrics.csv"
REPORTS = HERE / "reports"
STATE = REPORTS / "latest.json"

TRIGGERS = [
    ("holders_revenue_30d", ">", 0.0, "Holder revenue resumed"),
    ("buyback_30d_pct_revenue", ">=", 30.0, "Buyback at the 30% policy allocation"),
    ("tvl", ">=", 4_500_000_000.0, "TVL above $4.5B (spot; sustained check is manual)"),
    ("revenue_30d", ">=", 2_500_000.0, "Revenue above $2.5M / 30d"),
]


def read_metrics() -> tuple[dict[str, float], str]:
    if not METRICS.exists():
        raise SystemExit(f"missing {METRICS}; run `make build` first")
    values: dict[str, float] = {}
    as_of = date.today().isoformat()
    with METRICS.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            try:
                values[row["metric"]] = float(row["value"])
            except (TypeError, ValueError):
                continue
            as_of = row.get("as_of") or as_of
    return values, as_of


def previous() -> dict[str, float]:
    if not STATE.exists():
        return {}
    try:
        return json.loads(STATE.read_text(encoding="utf-8")).get("metrics", {})
    except json.JSONDecodeError:
        return {}


def fmt(key: str, value: float | None) -> str:
    if value is None:
        return "—"
    if key == "price":
        return f"${value:,.4f}"
    if key == "buyback_30d_ethfi":
        return f"{value / 1_000_000:,.2f}M ETHFI"
    if key in PCT_KEYS:
        return f"{value:.2f}%"
    if key in MONEY_KEYS:
        if abs(value) >= 1_000_000_000:
            return f"${value / 1_000_000_000:,.2f}B"
        if abs(value) >= 1_000_000:
            return f"${value / 1_000_000:,.2f}M"
        return f"${value:,.0f}"
    return f"{value:,.2f}"


MONEY_KEYS = {
    "price",
    "market_cap",
    "fdv",
    "tvl",
    "tvl_peak",
    "fees_30d",
    "revenue_30d",
    "holders_revenue_30d",
    "fees_365d",
    "revenue_365d",
    "holders_revenue_365d",
    "cumulative_revenue",
    "cumulative_holders_revenue",
    "buyback_usdc",
    "buyback_30d_usdc",
    "dex_liquidity",
}

PCT_KEYS = {
    "tvl_drawdown_from_peak",
    "buyback_30d_pct_revenue",
    "buyback_mark_vs_spot_pct",
    "holders_revenue_share_cumulative",
    "top1_holder_share",
    "top5_holder_share",
    "top10_holder_share",
    "top20_holder_share",
    "eoa_float_share",
    "eoa_top1_share_of_float",
    "eoa_top5_share_of_float",
    "buyback_annualized_pct_mcap",
    "dex_liquidity_pct_mcap",
}


def delta(key: str, now: float, old: float | None) -> str:
    if old is None or old == 0:
        return "—"
    if key in PCT_KEYS:
        return f"{now - old:+.1f} п.п."
    pct = (now / old - 1) * 100
    return f"{pct:+.1f}%"


def threshold(key: str, value: float) -> str:
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:,.1f}M"
    return fmt(key, value)


def trigger_lines(values: dict[str, float]) -> list[str]:
    lines = []
    for key, op, limit, label in TRIGGERS:
        value = values.get(key)
        if value is None:
            lines.append(f"- [ ] {label} — нет данных")
            continue
        ok = value > limit if op == ">" else value >= limit
        mark = "x" if ok else " "
        lines.append(f"- [{mark}] {label}: {fmt(key, value)} (порог {op} {threshold(key, limit)})")
    return lines


def build_digest(values: dict[str, float], as_of: str) -> str:
    old = previous()
    rows = [
        ("price", "Цена"),
        ("market_cap", "Market cap"),
        ("tvl", "TVL"),
        ("tvl_drawdown_from_peak", "Просадка от пика"),
        ("fees_30d", "Fees 30d"),
        ("revenue_30d", "Revenue 30d"),
        ("holders_revenue_30d", "Holder revenue 30d"),
        ("buyback_30d_ethfi", "Buyback 30d, ETHFI"),
        ("buyback_30d_pct_revenue", "Buyback / revenue 30d"),
        ("top10_holder_share", "Top-10 доля"),
        ("dex_liquidity", "DEX-ликвидность"),
    ]
    table = ["| Метрика | Сейчас | Неделя назад | Δ |", "|---|---:|---:|---:|"]
    for key, label in rows:
        now = values.get(key)
        if now is None:
            continue
        table.append(f"| {label} | {fmt(key, now)} | {fmt(key, old.get(key))} | {delta(key, now, old.get(key))} |")

    changed = []
    for key, label in rows:
        now = values.get(key)
        prev = old.get(key)
        if now is None or prev is None or prev == 0:
            continue
        pct = (now / prev - 1) * 100
        if abs(pct) >= 2:
            changed.append(f"{label}: {pct:+.1f}%")

    return "\n".join(
        [
            f"# ETHFI weekly — {as_of}",
            "",
            "**Decision: WAIT, 0–2%.** Это недельный контроль триггеров, не пересмотр тезиса.",
            "",
            "## Метрики",
            "",
            *table,
            "",
            "## Триггеры",
            "",
            *trigger_lines(values),
            "",
            "## Что изменилось",
            "",
            *([f"- {x}" for x in changed] if changed else ["- Изменений ≥2% к прошлому снимку нет."]),
            "",
            "## Проверить вручную",
            "",
            "- [ ] Buyback → sETHFI / burn / подтверждённая выплата (главный upgrade-триггер).",
            "- [ ] Переводы treasury/allocation-EOA на CEX (invalidation).",
            "- [ ] Optimism cashback: адреса получателей и суммы.",
            "- [ ] Непрерывность buyback: не остановился ли более чем на 30 дней.",
            "",
            f"_Источник: `04_ETHFI/onchain/data/ethfi_metrics.csv`, as of {as_of}. "
            "Пороговые значения — из Decision Card, не прогноз._",
            "",
        ]
    )


def send_telegram(text: str) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        print("Telegram skipped: TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set", file=sys.stderr)
        return False
    data = urllib.parse.urlencode(
        {"chat_id": chat, "text": text, "disable_web_page_preview": "true"}
    ).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=data)
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = json.load(resp)
    if not body.get("ok"):
        print(f"Telegram error: {body}", file=sys.stderr)
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--refresh", action="store_true", help="fetch a new snapshot and rebuild")
    ap.add_argument("--telegram", action="store_true", help="send the digest if env vars are set")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if args.refresh:
        subprocess.run([sys.executable, str(HERE / "fetch_onchain.py"), "--refresh"], check=True)
        subprocess.run([sys.executable, str(HERE / "build_outputs.py")], check=True)

    values, as_of = read_metrics()
    REPORTS.mkdir(exist_ok=True)
    digest = build_digest(values, as_of)
    out = REPORTS / f"weekly_{as_of}.md"
    out.write_text(digest, encoding="utf-8")
    STATE.write_text(
        json.dumps({"as_of": as_of, "metrics": values}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(digest)
    print(f"\nwritten: {out}")
    if args.telegram and not send_telegram(digest):
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
