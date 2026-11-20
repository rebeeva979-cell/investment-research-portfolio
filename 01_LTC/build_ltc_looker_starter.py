#!/usr/bin/env python3
"""Create a compact, Google Sheets-friendly Looker Studio starter workbook.

The full research workbook (LTC_LOOKER_DATASET.xlsx) has 20 sheets and 130+
columns. That is good as a research database, but slow to connect in Looker
Studio. This script keeps the minimum needed for the first 9 dashboard pages.

Input:
    01_LTC/LTC_LOOKER_DATASET.xlsx

Output:
    01_LTC/LTC_LOOKER_STARTER.xlsx

Run:
    python3 01_LTC/build_ltc_looker_starter.py
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

BASE_DIR = Path(__file__).resolve().parent
INPUT_XLSX = BASE_DIR / "LTC_LOOKER_DATASET.xlsx"
OUTPUT_XLSX = BASE_DIR / "LTC_LOOKER_STARTER.xlsx"

HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=10)
TITLE_FONT = Font(bold=True, size=15, color="1F3864")
SECTION_FONT = Font(bold=True, size=11, color="1F3864")
NOTE_FONT = Font(italic=True, size=9, color="595959")
THIN_BORDER = Border(bottom=Side(style="thin", color="D9E2F3"))

DATE_FMT = "yyyy-mm-dd"
PRICE_FMT = "$#,##0.00"
USD_FMT = "$#,##0"
PCT_FMT = "0.00%"
PCT_POINT_FMT = "0.00"
NUM_FMT = "#,##0"
FLOAT_FMT = "#,##0.00"
RATIO_FMT = "0.000"

# sheet -> (columns, date columns, price columns, usd columns, pct fraction columns,
#           pct point columns, number columns, float columns)
SHEETS: dict[str, dict] = {
    "MARKET_DAILY": {
        "columns": [
            "date", "asset", "price_close_usd", "volume",
            "return_1d", "return_7d", "return_30d", "return_90d", "return_365d", "ytd_return",
            "ma_30_usd", "ma_200_usd", "price_vs_ma_200", "volatility_30d_annualized",
            "drawdown_from_ath", "high_water_mark_usd", "year", "month", "halving_epoch",
        ],
        "date": {"date"},
        "price": {"price_close_usd", "ma_30_usd", "ma_200_usd", "high_water_mark_usd"},
        "usd": set(),
        "pct": {
            "return_1d", "return_7d", "return_30d", "return_90d", "return_365d",
            "ytd_return", "price_vs_ma_200", "volatility_30d_annualized", "drawdown_from_ath",
        },
        "pct_point": set(),
        "number": {"volume", "year", "month", "halving_epoch"},
        "float": set(),
    },
    "KPI_LATEST": {
        "columns": [
            "asset", "as_of_date", "price_close_usd",
            "return_1d", "return_7d", "return_30d", "return_90d", "return_365d", "ytd_return",
            "volatility_30d_annualized", "ath_close_usd_in_dataset", "ath_close_date_in_dataset",
            "drawdown_from_ath", "high_52w_close_usd", "low_52w_close_usd",
            "ma_200_usd", "price_vs_ma_200", "market_cap_usd", "supply_ltc",
            "active_addresses", "tx_count", "hashrate", "mvrv", "realized_cap_usd",
            "fees_usd_30d_sum", "issuance_usd_30d_sum", "fee_to_issuance_30d_ratio",
            "supply_inflation_365d", "active_addresses_30d_change",
            "tx_count_30d_change", "hashrate_30d_change", "market_cap_30d_change",
            "var_95_30d", "var_99_30d", "sharpe_30d", "sortino_30d",
            "coverage_start", "coverage_end", "observations", "date_gaps", "calculated_at_utc",
        ],
        "date": {"as_of_date", "ath_close_date_in_dataset", "coverage_start", "coverage_end"},
        "price": {"price_close_usd", "ath_close_usd_in_dataset", "high_52w_close_usd", "low_52w_close_usd", "ma_200_usd"},
        "usd": {"market_cap_usd", "realized_cap_usd", "fees_usd_30d_sum", "issuance_usd_30d_sum"},
        "pct": {
            "return_1d", "return_7d", "return_30d", "return_90d", "return_365d", "ytd_return",
            "volatility_30d_annualized", "drawdown_from_ath", "price_vs_ma_200",
            "supply_inflation_365d", "active_addresses_30d_change", "tx_count_30d_change",
            "hashrate_30d_change", "market_cap_30d_change", "var_95_30d", "var_99_30d",
        },
        "pct_point": set(),
        "number": {"supply_ltc", "active_addresses", "tx_count", "observations", "date_gaps"},
        "float": {"hashrate", "mvrv", "fee_to_issuance_30d_ratio", "sharpe_30d", "sortino_30d"},
    },
    "ONCHAIN_DAILY": {
        "columns": [
            "date", "asset", "market_cap_usd", "supply_ltc", "active_addresses", "tx_count",
            "transfer_count", "hashrate", "block_count", "fees_usd", "issuance_usd",
            "miner_revenue_usd", "fee_share_of_miner_revenue", "active_addresses_per_tx",
            "active_addresses_30d_change", "tx_count_30d_change", "hashrate_30d_change",
            "market_cap_30d_change", "mvrv", "realized_cap_usd",
        ],
        "date": {"date"},
        "price": set(),
        "usd": {"market_cap_usd", "fees_usd", "issuance_usd", "miner_revenue_usd", "realized_cap_usd"},
        "pct": {
            "fee_share_of_miner_revenue", "active_addresses_30d_change",
            "tx_count_30d_change", "hashrate_30d_change", "market_cap_30d_change",
        },
        "pct_point": set(),
        "number": {"supply_ltc", "active_addresses", "tx_count", "transfer_count", "block_count"},
        "float": {"hashrate", "active_addresses_per_tx", "mvrv"},
    },
    "PEER_DAILY": {
        "columns": [
            "date", "asset", "asset_name", "cm_price_usd", "market_cap_usd",
            "supply_native", "active_addresses", "tx_count", "hashrate", "block_count", "source",
        ],
        "date": {"date"},
        "price": {"cm_price_usd"},
        "usd": {"market_cap_usd"},
        "pct": set(),
        "pct_point": set(),
        "number": {"supply_native", "active_addresses", "tx_count", "block_count"},
        "float": {"hashrate"},
    },
    "YEARLY_SUMMARY": {
        "columns": [
            "year", "first_date", "last_date", "first_close_usd", "last_close_usd",
            "year_return", "min_close_usd", "max_close_usd", "avg_close_usd",
            "realized_vol_annualized", "year_max_drawdown", "observations", "is_partial_year",
        ],
        "date": {"first_date", "last_date"},
        "price": {"first_close_usd", "last_close_usd", "min_close_usd", "max_close_usd", "avg_close_usd"},
        "usd": set(),
        "pct": {"year_return", "realized_vol_annualized", "year_max_drawdown"},
        "pct_point": set(),
        "number": {"year", "observations"},
        "float": set(),
    },
    "MONTHLY_RETURNS": {
        "columns": [
            "year", "month", "month_label", "monthly_return",
            "month_max_drawdown", "observations", "is_partial_month",
        ],
        "date": set(),
        "price": set(),
        "usd": set(),
        "pct": {"monthly_return", "month_max_drawdown"},
        "pct_point": set(),
        "number": {"year", "month", "observations"},
        "float": set(),
    },
    "DECISION_RULES": {
        "columns": [
            "as_of_date", "gate", "metric", "current_value", "rule", "status", "interpretation",
        ],
        "date": {"as_of_date"},
        "price": set(),
        "usd": set(),
        "pct": set(),
        "pct_point": set(),
        "number": set(),
        "float": set(),
    },
    "DATA_QUALITY": {
        "columns": ["check", "result", "detail"],
        "date": set(),
        "price": set(),
        "usd": set(),
        "pct": set(),
        "pct_point": set(),
        "number": set(),
        "float": set(),
    },
    "SOURCES": {
        "columns": [
            "source_id", "provider", "dataset_or_endpoint", "metric_covered",
            "coverage_start", "coverage_end", "update_frequency", "license_or_terms",
            "known_limitations", "url", "last_checked",
        ],
        "date": set(),
        "price": set(),
        "usd": set(),
        "pct": set(),
        "pct_point": set(),
        "number": set(),
        "float": set(),
    },
    "PEER_LATEST": {
        "columns": [
            "as_of_date", "asset", "asset_name", "price_usd", "market_cap_usd",
            "supply_native", "active_addresses", "tx_count", "hashrate", "block_count", "source",
        ],
        "date": {"as_of_date"},
        "price": {"price_usd"},
        "usd": {"market_cap_usd"},
        "pct": set(),
        "pct_point": set(),
        "number": {"supply_native", "active_addresses", "tx_count", "block_count"},
        "float": {"hashrate"},
    },
}


def read_sheet(wb: openpyxl.Workbook, name: str, columns: list[str]) -> tuple[list[str], list[list]]:
    ws = wb[name]
    rows = ws.iter_rows(values_only=True)
    header = list(next(rows))
    index = {value: position for position, value in enumerate(header)}
    missing = [column for column in columns if column not in index]
    if missing:
        raise ValueError(f"{name}: missing columns {missing}")
    selected = []
    for row in rows:
        selected.append([row[index[column]] for column in columns])
    return columns, selected


def add_peer_latest(source, target) -> None:
    """Build a 5-asset latest-date peer table, adding LTC from the base dataset.

    PEER_DAILY contains BTC, BCH, DOGE and DASH from Coin Metrics, but not LTC.
    LTC is added from KPI_LATEST so the comparison is complete and explicitly
    labelled as a mixed-source row.
    """
    config = SHEETS["PEER_LATEST"]
    peer_ws = source["PEER_DAILY"]
    peer_rows = list(peer_ws.iter_rows(values_only=True))
    peer_header = list(peer_rows[0])
    peer_index = {value: position for position, value in enumerate(peer_header)}

    dates_by_asset: dict[str, set] = {}
    for row in peer_rows[1:]:
        value = row[peer_index["date"]]
        day = value.date() if isinstance(value, dt.datetime) else value
        dates_by_asset.setdefault(row[peer_index["asset"]], set()).add(day)
    common_dates = set.intersection(*dates_by_asset.values())
    latest_common = max(common_dates)

    peer_source_rows = {}
    for row in peer_rows[1:]:
        value = row[peer_index["date"]]
        day = value.date() if isinstance(value, dt.datetime) else value
        if day == latest_common:
            peer_source_rows[row[peer_index["asset"]]] = row

    kpi_ws = source["KPI_LATEST"]
    kpi_rows = list(kpi_ws.iter_rows(values_only=True))
    kpi_header = list(kpi_rows[0])
    kpi = dict(zip(kpi_header, kpi_rows[1]))

    rows = []
    ltc_row = [
        kpi["as_of_date"], "LTC", "Litecoin", kpi["price_close_usd"], kpi["market_cap_usd"],
        kpi["supply_ltc"], kpi["active_addresses"], kpi["tx_count"], kpi["hashrate"],
        kpi["block_count"], "Base LTC dataset + Coin Metrics Community API v4",
    ]
    rows.append(ltc_row)

    order = ["BTC", "BCH", "DOGE", "DASH"]
    for asset in order:
        row = peer_source_rows.get(asset)
        if not row:
            continue
        rows.append([
            latest_common, asset, row[peer_index["asset_name"]], row[peer_index["cm_price_usd"]],
            row[peer_index["market_cap_usd"]], row[peer_index["supply_native"]],
            row[peer_index["active_addresses"]], row[peer_index["tx_count"]],
            row[peer_index["hashrate"]], row[peer_index["block_count"]], row[peer_index["source"]],
        ])

    ws = target.create_sheet("PEER_LATEST")
    ws.append(config["columns"])
    for row in rows:
        ws.append(row)
    style_header(ws)
    format_sheet(ws, config)


def style_header(ws) -> None:
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
    ws.row_dimensions[1].height = 32


def format_sheet(ws, config: dict) -> None:
    headers = {cell.value: cell.column for cell in ws[1]}
    for name, column in headers.items():
        letter = get_column_letter(column)
        for cell in ws.iter_rows(min_row=2, min_col=column, max_col=column):
            target = cell[0]
            if name in config["date"]:
                target.number_format = DATE_FMT
            elif name in config["price"]:
                target.number_format = PRICE_FMT
            elif name in config["usd"]:
                target.number_format = USD_FMT
            elif name in config["pct"]:
                target.number_format = PCT_FMT
            elif name in config["pct_point"]:
                target.number_format = PCT_POINT_FMT
            elif name in config["number"]:
                target.number_format = NUM_FMT
            elif name in config["float"]:
                target.number_format = FLOAT_FMT
            if name in {"status", "is_partial_year", "is_partial_month"}:
                target.alignment = Alignment(horizontal="center", vertical="top")
        # Width: header + a sample of values, capped.
        longest = len(str(name))
        for cell in ws.iter_rows(min_row=2, max_row=min(ws.max_row, 250), min_col=column, max_col=column):
            value = cell[0].value
            if value is not None:
                longest = max(longest, min(len(str(value)), 55))
        ws.column_dimensions[letter].width = min(max(12, longest + 2), 48)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    # Status colours for DECISION_RULES.
    if ws.title == "DECISION_RULES":
        status_column = headers.get("status")
        if status_column:
            for row in range(2, ws.max_row + 1):
                cell = ws.cell(row=row, column=status_column)
                value = str(cell.value or "").upper()
                if value == "PASS":
                    cell.fill = PatternFill("solid", fgColor="D9EAD3")
                elif value == "FAIL":
                    cell.fill = PatternFill("solid", fgColor="F4CCCC")
                elif value == "MIXED":
                    cell.fill = PatternFill("solid", fgColor="FFF2CC")
                elif value in {"DEFENSIVE", "CAUTION"}:
                    cell.fill = PatternFill("solid", fgColor="FCE5CD")
                    cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal="center", vertical="center")


def add_readme(ws) -> None:
    ws["A1"] = "LTC — LOOKER STUDIO STARTER"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:C1")
    ws["A3"] = "Зачем этот файл"
    ws["B3"] = (
        "Компактная версия полного research workbook. В ней только листы и поля, "
        "нужные для первых 9 страниц Looker Studio."
    )
    ws["A4"] = "Полная версия"
    ws["B4"] = "LTC_LOOKER_DATASET.xlsx — 20 листов, все исследования и audit-поля."
    ws["A5"] = "Гайд"
    ws["B5"] = "LOOKER_STUDIO_BUILD_GUIDE.md / .pdf / .html"
    ws["A7"] = "1. Загрузи"
    ws["B7"] = "Загрузи LTC_LOOKER_STARTER.xlsx в Google Drive."
    ws["A8"] = "2. Открой"
    ws["B8"] = "Открой файл через Google Sheets: File → Open with → Google Sheets. Сохрани как Google-таблицу."
    ws["A9"] = "3. Создай отчёт"
    ws["B9"] = "В Looker Studio: Create → Report → Add data → Google Sheets → выбери этот файл."
    ws["A10"] = "4. Подключи листы"
    ws["B10"] = "Каждый лист — отдельный источник. Начни с MARKET_DAILY, KPI_LATEST, ONCHAIN_DAILY."
    ws["A11"] = "5. Проверь типы"
    ws["B11"] = "date → Date; *_usd → Currency USD; поля без _pct → Percent; *_pct → Number; counts → Number."
    ws["A12"] = "6. Собери страницы"
    ws["B12"] = "Market Overview → On-chain → Mining/Tokenomics → Valuation & Peers → Risk → Decision Gates → Data & Sources."
    ws["A14"] = "Листы"
    ws["A14"].font = SECTION_FONT
    rows = [
        ("MARKET_DAILY", "Цена, MA30/MA200, доходности, волатильность, drawdown, volume."),
        ("KPI_LATEST", "Одна строка для scorecards: цена, доходности, market cap, MVRV, activity, risk."),
        ("ONCHAIN_DAILY", "Active addresses, transactions, hashrate, fees, issuance, supply, MVRV."),
        ("PEER_DAILY", "BTC, BCH, DOGE, DASH — дневная панель Coin Metrics."),
        ("PEER_LATEST", "Пять активов на последнюю общую дату; LTC добавлен из базового ряда."),
        ("YEARLY_SUMMARY", "Годовая доходность, волатильность и max drawdown."),
        ("MONTHLY_RETURNS", "Месячная доходность для heatmap year × month."),
        ("DECISION_RULES", "Шесть gate-проверок и итоговый research state."),
        ("DATA_QUALITY", "Проверки качества и известные ограничения."),
        ("SOURCES", "Источники, покрытие и условия использования."),
    ]
    for offset, (name, description) in enumerate(rows, start=15):
        ws.cell(row=offset, column=1, value=name).font = Font(bold=True)
        ws.cell(row=offset, column=2, value=description)
    ws["A26"] = "Важно"
    ws["A26"].font = Font(bold=True, color="C00000")
    ws["B26"] = (
        "Volume — raw field без подтверждённой единицы. ATH — максимум дневного close в датасете, "
        "не внутридневной all-time high. On-chain addresses — не уникальные пользователи. "
        "Miner revenue — валовая выручка, не прибыль."
    )
    ws["B26"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 118
    for row in ws.iter_rows(min_row=3, max_row=27, min_col=1, max_col=2):
        if row[0].row != 14:
            row[0].font = Font(bold=True)
        row[1].alignment = Alignment(wrap_text=True, vertical="top")


def main() -> None:
    if not INPUT_XLSX.exists():
        raise FileNotFoundError(INPUT_XLSX)

    source = openpyxl.load_workbook(INPUT_XLSX, read_only=True, data_only=True)
    target = openpyxl.Workbook()
    target.remove(target.active)

    readme = target.create_sheet("README")
    add_readme(readme)

    total_rows = 0
    for sheet_name, config in SHEETS.items():
        if sheet_name == "PEER_LATEST":
            continue
        columns, rows = read_sheet(source, sheet_name, config["columns"])
        ws = target.create_sheet(sheet_name)
        ws.append(columns)
        for row in rows:
            ws.append(row)
        style_header(ws)
        format_sheet(ws, config)
        total_rows += len(rows)
        print(f"{sheet_name}: {len(rows)} rows x {len(columns)} cols")

    add_peer_latest(source, target)
    print("PEER_LATEST: 5 rows x 11 cols")

    source.close()
    target.save(OUTPUT_XLSX)
    print(f"OK: {OUTPUT_XLSX}")
    print(f"sheets={len(target.sheetnames)} data_rows={total_rows} size={OUTPUT_XLSX.stat().st_size/1024/1024:.1f} MB")


if __name__ == "__main__":
    main()
