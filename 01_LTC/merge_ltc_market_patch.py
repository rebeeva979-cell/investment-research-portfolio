#!/usr/bin/env python3
"""Merge the reviewed Yahoo LTC OHLCV continuation into the canonical market CSV.

The original market file is copied to a dated backup before replacement. The
patch carries only the canonical nine columns consumed by the LTC builder;
provider URL and quality notes remain in the versioned patch CSV and refresh
note.
"""

from __future__ import annotations

import csv
from pathlib import Path


base = Path(__file__).resolve().parent
main = base / "LTC_MARKET_DAILY.csv"
patch = base / "LTC_MARKET_PATCH_2026-11-15_TO_2026-11-20.csv"
backup = base / "LTC_MARKET_DAILY_PREPATCH_2026-11-20.csv"
fields = ["date", "asset", "price_open_usd", "price_high_usd", "price_low_usd", "price_close_usd", "volume", "return_1d_pct", "source_file"]

if not backup.exists():
    backup.write_bytes(main.read_bytes())

with (backup if backup.exists() else main).open(newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))
with patch.open(newline="", encoding="utf-8") as fh:
    patch_rows = [row for row in csv.DictReader(fh) if row["date"] <= "2026-11-19"]

patch_dates = {row["date"] for row in patch_rows}
rows = [row for row in rows if row["date"] not in patch_dates]
rows.extend({field: row[field] for field in fields} for row in patch_rows)
rows.sort(key=lambda row: row["date"])

with main.open("w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"merged_rows={len(rows)} patch_rows={len(patch_rows)} latest={rows[-1]['date']} backup={backup.name}")

