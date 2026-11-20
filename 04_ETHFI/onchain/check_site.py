#!/usr/bin/env python3
"""Consistency gate for the public portfolio.

Checks the things that usually rot when a research page is edited by hand:

* local links and image sources exist;
* no duplicate HTML ids;
* every table row has the same number of cells as its header;
* the numbers quoted on the ETHFI page and in the report still match
  ``data/ethfi_metrics.csv`` (within the precision used on the page);
* the CSVs served by the site are identical to the build outputs.

Run from the repository root:

    python3 04_ETHFI/onchain/check_site.py
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
ONCHAIN = ROOT / "04_ETHFI" / "onchain"
REPORT = ROOT / "04_ETHFI" / "ETHFI_ONCHAIN_VERIFICATION_2026-11-20.md"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.tables: list[list[list[str]]] = []
        self._table: list[list[str]] | None = None
        self._row: list[str] | None = None
        self._cell: list[str] | None = None
        self._cell_tag: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"] or "")
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key] or "")
        if tag == "table":
            self._table = []
            self.tables.append(self._table)
        elif tag == "tr" and self._table is not None:
            self._row = []
            self._table.append(self._row)
        elif tag in ("td", "th") and self._row is not None:
            self._cell = []
            self._cell_tag = tag
            self._row.append("")

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in ("td", "th") and self._cell is not None:
            text = re.sub(r"\s+", " ", "".join(self._cell)).strip()
            if self._row is not None:
                self._row[-1] = text
            self._cell = None
            self._cell_tag = None
        elif tag == "tr":
            self._row = None
        elif tag == "table":
            self._table = None


def parse(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def local_target(page: Path, link: str) -> Path | None:
    parts = urlsplit(link)
    if parts.scheme or parts.netloc or link.startswith(("#", "mailto:", "tel:", "data:")):
        return None
    raw = unquote(parts.path)
    if not raw:
        return None
    if raw.startswith("/"):
        return DOCS / raw.lstrip("/")
    return (page.parent / raw).resolve()


def load_metrics() -> dict[str, float]:
    out: dict[str, float] = {}
    with (ONCHAIN / "data" / "ethfi_metrics.csv").open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            try:
                out[row["metric"]] = float(row["value"])
            except (TypeError, ValueError):
                pass
    return out


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    global DOCS, ONCHAIN
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default=str(DOCS))
    ap.add_argument("--onchain", default=str(ONCHAIN))
    args = ap.parse_args()
    DOCS = Path(args.docs).resolve()
    ONCHAIN = Path(args.onchain).resolve()

    errors: list[str] = []
    pages = sorted(DOCS.glob("*.html")) + sorted(ROOT.glob("*.html"))
    parsed: dict[Path, PageParser] = {}
    for page in pages:
        p = parse(page)
        parsed[page] = p
        if len(p.ids) != len(set(p.ids)):
            dupes = sorted({x for x in p.ids if p.ids.count(x) > 1})
            errors.append(f"{page.relative_to(ROOT)}: duplicate ids {dupes}")
        for link in p.links:
            target = local_target(page, link)
            if target is not None and not target.exists():
                errors.append(f"{page.relative_to(ROOT)}: missing local target {link}")
        for table in p.tables:
            widths = [len(row) for row in table if row]
            if len(set(widths)) > 1:
                errors.append(f"{page.relative_to(ROOT)}: table rows have widths {sorted(set(widths))}")

    metrics = load_metrics()
    required = {
        "price": (metrics.get("price", 0.0), "$0.466", "price"),
        "mcap": (metrics.get("market_cap", 0.0) / 1e6, "$465.7M", "market cap"),
        "tvl": (metrics.get("tvl", 0.0) / 1e9, "$3.73B", "TVL"),
        "drawdown": (abs(metrics.get("tvl_drawdown_from_peak", 0.0)), "70.9%", "drawdown"),
        "top10": (metrics.get("top10_holder_share", 0.0), "62.19%", "top-10 share"),
        "buyback": (metrics.get("buyback_ethfi", 0.0) / 1e6, "2.54M", "buyback"),
        "mcap_rev": (metrics.get("mcap_revenue", 0.0), "10.73×", "mcap/revenue"),
        "buyback_pct": (metrics.get("buyback_30d_pct_revenue", 0.0), "17.3%", "buyback/revenue"),
        "mark": (metrics.get("buyback_mark_vs_spot_pct", 0.0), "−28%", "mark vs spot"),
        "dex": (metrics.get("dex_liquidity", 0.0) / 1e6, "$1.23M", "DEX depth"),
        "burn": (metrics.get("burned_supply", 0.0), "1,464,001", "burned supply"),
    }
    for page, p in parsed.items():
        text = page.read_text(encoding="utf-8")
        if page.name == "ethfi.html":
            for name, (_, needle, label) in required.items():
                if needle not in text:
                    errors.append(f"{page.relative_to(ROOT)}: {label} {needle!r} not found")
    report_needles = {
        "tvl": "$3.728B",
        "buyback": "2,542,499",
        "dex": "$1.228M",
    }
    if REPORT.exists():
        report = REPORT.read_text(encoding="utf-8")
        for name, (_, needle, label) in required.items():
            if report_needles.get(name, needle) not in report:
                errors.append(f"report: {label} {needle!r} not found")

    for csv_name in ("ethfi_metrics.csv", "ethfi_holders_top.csv", "ethfi_buybacks_daily.csv",
                     "ethfi_fees_monthly.csv", "ethfi_tvl_weekly.csv", "ethfi_valuation_scenarios.csv"):
        src = ONCHAIN / "data" / csv_name
        dst = DOCS / "data" / csv_name
        if not src.exists():
            errors.append(f"missing build output {src.relative_to(ROOT)}")
        elif not dst.exists():
            errors.append(f"missing site copy {dst.relative_to(ROOT)}")
        elif sha256(src) != sha256(dst):
            errors.append(f"CSV drift: {csv_name} differs between build and docs")

    if errors:
        print("CHECK FAILED")
        for e in errors:
            print(" -", e)
        return 1
    print(f"OK: {len(pages)} pages, {len(metrics)} metrics, links/tables/numbers/CSVs consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
