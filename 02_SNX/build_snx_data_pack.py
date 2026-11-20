#!/usr/bin/env python3
"""Build the SNX SIP-423 research data pack for Looker Studio.

All values are point-in-time snapshots. The pack separates:
  * on-chain facts verified through JSON-RPC and Blockscout;
  * SIP-423 primary-source terms;
  * market, fee and TVL data from CoinGecko and DefiLlama;
  * derived scenarios and calculations.

Output:
    02_SNX/SNX_SIP423_DATA_PACK.xlsx

Run:
    python3 02_SNX/build_snx_data_pack.py
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

BASE_DIR = Path(__file__).resolve().parent
OUTPUT = BASE_DIR / "SNX_SIP423_DATA_PACK.xlsx"

AS_OF = dt.date(2026, 11, 19)
CALC_AT = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None, microsecond=0)

# Verified on-chain facts
TOTAL_SUPPLY = 581_404_223.5556632
PRE_MINT_SUPPLY = 344_939_867.55566317
MINT_AMOUNT = 236_464_356.0
SAFE_BALANCE = 236_464_356.0
SUSD_ENTITLEMENT = 59_116_089.0

# Market data (CoinGecko, 2026-11-19T17:03:57Z)
PRICE = 0.164855
MARKET_CAP = 95_831_317.0
FDV = 95_901_194.0
CIRCULATING = 580_980_590.4572881
VOLUME_24H = 6_330_298.0

# DefiLlama, 2026-11-19
FEES_24H = 54.0
FEES_30D = 3_678.0
FEES_1Y = 32_242.0
TVL = 856_123.0
TVL_1Y_AGO = 88_428_843.0
TVL_PEAK = 2_966_823_065.0

# Derived values
SAFE_SHARE = SAFE_BALANCE / TOTAL_SUPPLY
MINT_TO_PRE = MINT_AMOUNT / PRE_MINT_SUPPLY
MINT_TO_TOTAL = MINT_AMOUNT / TOTAL_SUPPLY
SAFE_VALUE = SAFE_BALANCE * PRICE
CLAIM_VALUE_MARKET = MINT_AMOUNT * PRICE
CLAIM_VALUE_PAR = MINT_AMOUNT * 0.25
DISCOUNT_TO_PAR = PRICE / 0.25 - 1
IMPLIED_PRE_MINT_MCAP = PRE_MINT_SUPPLY * PRICE
MCAP_RATIO = MARKET_CAP / IMPLIED_PRE_MINT_MCAP
FEES_ANNUALIZED_30D = FEES_30D * 365 / 30
TVL_CHANGE_1Y = TVL / TVL_1Y_AGO - 1
MCAP_TO_FEES30 = MARKET_CAP / FEES_30D
MCAP_TO_FEES1Y = MARKET_CAP / FEES_1Y
MCAP_TO_TVL = MARKET_CAP / TVL
FDV_TO_TVL = FDV / TVL
REVENUE_HURDLE_MULTIPLE = 10_000_000 / FEES_1Y
MONTHLY_UNLOCK = MINT_AMOUNT / 12
MONTHLY_UNLOCK_USD = MONTHLY_UNLOCK * PRICE
MONTHLY_VOLUME = VOLUME_24H * 30
MONTHLY_UNLOCK_VS_VOLUME = MONTHLY_UNLOCK_USD / MONTHLY_VOLUME
CLAIM_WINDOW_OPEN = dt.date(2027, 7, 6)
VEST_END = dt.date(2028, 7, 6)
UNCLAIMED_EXPIRY = dt.date(2028, 1, 6)

# Styling
HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=10)
TITLE_FONT = Font(bold=True, size=15, color="1F3864")
SECTION_FONT = Font(bold=True, size=11, color="1F3864")
NOTE_FONT = Font(italic=True, size=9, color="595959")
THIN_BORDER = Border(bottom=Side(style="thin", color="D9E2F3"))
DATE_FMT = "yyyy-mm-dd"
DATETIME_FMT = "yyyy-mm-dd hh:mm"
USD_FMT = "$#,##0"
USD2_FMT = "$#,##0.00"
PCT_FMT = "0.00%"
NUM_FMT = "#,##0"
FLOAT_FMT = "#,##0.00"
RATIO_FMT = "#,##0.000"


def style_header(ws) -> None:
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
    ws.row_dimensions[1].height = 34


def autosize(ws, max_width: int = 60) -> None:
    for column in ws.columns:
        letter = get_column_letter(column[0].column)
        length = 0
        for cell in column:
            value = "" if cell.value is None else str(cell.value)
            length = max(length, len(value))
        ws.column_dimensions[letter].width = min(max(12, length + 2), max_width)


def write_table(ws, headers: list[str], rows: list[list], formats: dict[str, str] | None = None) -> None:
    ws.append(headers)
    for row in rows:
        ws.append(row)
    style_header(ws)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    formats = formats or {}
    header_map = {cell.value: cell.column for cell in ws[1]}
    for name, fmt in formats.items():
        column = header_map.get(name)
        if not column:
            continue
        for cell in ws.iter_rows(min_row=2, min_col=column, max_col=column):
            cell[0].number_format = fmt
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=False)
    autosize(ws)


def add_readme(ws) -> None:
    ws["A1"] = "SNX SIP-423 — RESEARCH DATA PACK"
    ws["A1"].font = TITLE_FONT
    ws.merge_cells("A1:C1")
    ws["A3"] = "As of"
    ws["B3"] = AS_OF
    ws["A4"] = "Purpose"
    ws["B4"] = (
        "Воспроизводимый датапак по supply overhang Synthetix SIP-423: ончейн-факты, "
        "SIP-термы, рыночный контекст, сценарии и карта дашборда."
    )
    ws["A5"] = "Source hierarchy"
    ws["B5"] = (
        "1) Ethereum JSON-RPC и Blockscout для on-chain; 2) GitHub SIP-423 для правил; "
        "3) CoinGecko для market data; 4) DefiLlama для fees/TVL; 5) расчёты в этом файле."
    )
    ws["A7"] = "Как использовать в Looker Studio"
    ws["B7"] = (
        "Загрузить XLSX в Google Drive → открыть как Google Sheets → подключить каждый лист "
        "отдельным источником. KPI — scorecards; SUPPLY_BRIDGE — waterfall/bar; "
        "TOKEN_PATH — таблица; TIMELINE — таймлайн; MARKET_CONTEXT — cards; "
        "SCENARIOS — таблица; DECISION_RULES — gate cards; VERIFICATION_LOG и SOURCES — data page."
    )
    ws["A8"] = "Типы полей"
    ws["B8"] = (
        "Даты — Date; поля *_usd — Currency USD; поля *_share, *_to_*, *_change, *_discount, "
        "*_vs_volume — доли (формат Percent); поля *_x и *_multiple — Number (ratios); "
        "supply, snx, balances — Number."
    )
    ws["A9"] = "Ключевая оговорка"
    ws["B9"] = (
        "Safe — это мультиподпись, а не on-chain vesting-контракт. Lock/vest — обязательство "
        "по SIP и операционное состояние Safe, а не гарантия, зашитая в контракт. "
        "Нет исходящих переводов на 2026-11-19 — это point-in-time observation, не permanent guarantee."
    )
    ws["A10"] = "Вторая оговорка"
    ws["B10"] = (
        "CoinGecko включает заблокированные 236.46M SNX в circulating supply (580.98M из 581.40M). "
        "Поэтому reported market cap и pre-mint market cap расходятся в 1.685x. "
        "Для comparability показывать обе базы."
    )
    ws["A11"] = "Третья оговорка"
    ws["B11"] = (
        "SIP-423 содержит и «unclaimed receipts after 6 months expire worthless», и строку "
        "«Unclaimed sUSD entitlement treatment = TBD». Дата 2028-01-06 — условная, не финальная."
    )
    ws["A13"] = "Листы"
    ws["A13"].font = SECTION_FONT
    sheets = [
        ("KPI", "Одна строка для scorecards: цена, market cap, supply bridge, fees, TVL, scenarios."),
        ("SUPPLY_BRIDGE", "Pre-mint → mint → post-mint → Safe → circulating."),
        ("TOKEN_PATH", "Четыре перевода 2026-07-06 с tx hash и block number."),
        ("TIMELINE", "SIP, snapshot, mint, Safe transfer, claim window, vest, expiry."),
        ("MARKET_CONTEXT", "Price, market cap, FDV, volume, fees, TVL и valuation multiples."),
        ("SCENARIOS", "Sell pressure при разных ценах и долях продаж."),
        ("CALCULATIONS", "Формулы, входные значения и результаты."),
        ("DECISION_RULES", "Шесть gate-проверок и итоговый research state."),
        ("VERIFICATION_LOG", "Что проверено, каким методом и с каким статусом."),
        ("SOURCES", "Источники, ссылки, as-of и ограничения."),
        ("DASHBOARD_LAYOUT", "Карта страниц и чартов для Looker Studio."),
    ]
    for offset, (name, description) in enumerate(sheets, start=14):
        ws.cell(row=offset, column=1, value=name).font = Font(bold=True)
        ws.cell(row=offset, column=2, value=description)
    ws["A26"] = "Disclaimer"
    ws["A26"].font = Font(bold=True, color="C00000")
    ws["B26"] = "Research artifact, not investment advice. Не является персональной рекомендацией."
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 120
    for row in ws.iter_rows(min_row=3, max_row=26, min_col=1, max_col=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")


def add_kpi(wb: Workbook) -> None:
    ws = wb.create_sheet("KPI")
    headers = [
        "as_of_date", "price_usd", "market_cap_usd", "fdv_usd", "circulating_supply",
        "total_supply", "pre_mint_supply", "mint_amount_snx", "safe_balance_snx",
        "safe_share", "safe_value_usd", "mint_to_pre", "mint_to_total",
        "claim_value_at_market_usd", "claim_value_at_par_usd", "discount_to_par",
        "implied_pre_mint_mcap_usd", "mcap_ratio_vs_pre_mint", "fees_24h_usd",
        "fees_30d_usd", "fees_1y_usd", "fees_annualized_30d_usd", "tvl_usd",
        "tvl_1y_ago_usd", "tvl_change_1y", "tvl_peak_usd", "mcap_to_fees30_x",
        "mcap_to_fees1y_x", "mcap_to_tvl_x", "revenue_hurdle_multiple",
        "monthly_unlock_snx", "monthly_unlock_usd", "monthly_volume_usd",
        "monthly_unlock_vs_volume", "claim_window_open_est", "vest_end_est", "calc_at_utc",
    ]
    values = [
        AS_OF, PRICE, MARKET_CAP, FDV, CIRCULATING, TOTAL_SUPPLY, PRE_MINT_SUPPLY,
        MINT_AMOUNT, SAFE_BALANCE, SAFE_SHARE, SAFE_VALUE, MINT_TO_PRE, MINT_TO_TOTAL,
        CLAIM_VALUE_MARKET, CLAIM_VALUE_PAR, DISCOUNT_TO_PAR, IMPLIED_PRE_MINT_MCAP,
        MCAP_RATIO, FEES_24H, FEES_30D, FEES_1Y, FEES_ANNUALIZED_30D, TVL, TVL_1Y_AGO,
        TVL_CHANGE_1Y, TVL_PEAK, MCAP_TO_FEES30, MCAP_TO_FEES1Y, MCAP_TO_TVL,
        REVENUE_HURDLE_MULTIPLE, MONTHLY_UNLOCK, MONTHLY_UNLOCK_USD, MONTHLY_VOLUME,
        MONTHLY_UNLOCK_VS_VOLUME, CLAIM_WINDOW_OPEN, VEST_END, CALC_AT,
    ]
    ws.append(headers)
    ws.append(values)
    style_header(ws)
    ws.row_dimensions[1].height = 48
    formats = {
        "as_of_date": DATE_FMT, "claim_window_open_est": DATE_FMT, "vest_end_est": DATE_FMT,
        "calc_at_utc": DATETIME_FMT, "price_usd": USD2_FMT, "market_cap_usd": USD_FMT,
        "fdv_usd": USD_FMT, "circulating_supply": NUM_FMT, "total_supply": NUM_FMT,
        "pre_mint_supply": NUM_FMT, "mint_amount_snx": NUM_FMT, "safe_balance_snx": NUM_FMT,
        "safe_share": PCT_FMT, "safe_value_usd": USD_FMT, "mint_to_pre": PCT_FMT,
        "mint_to_total": PCT_FMT, "claim_value_at_market_usd": USD_FMT,
        "claim_value_at_par_usd": USD_FMT, "discount_to_par": PCT_FMT,
        "implied_pre_mint_mcap_usd": USD_FMT, "mcap_ratio_vs_pre_mint": RATIO_FMT,
        "fees_24h_usd": USD_FMT, "fees_30d_usd": USD_FMT, "fees_1y_usd": USD_FMT,
        "fees_annualized_30d_usd": USD_FMT, "tvl_usd": USD_FMT, "tvl_1y_ago_usd": USD_FMT,
        "tvl_change_1y": PCT_FMT, "tvl_peak_usd": USD_FMT, "mcap_to_fees30_x": NUM_FMT,
        "mcap_to_fees1y_x": NUM_FMT, "mcap_to_tvl_x": FLOAT_FMT,
        "revenue_hurdle_multiple": FLOAT_FMT, "monthly_unlock_snx": NUM_FMT,
        "monthly_unlock_usd": USD_FMT, "monthly_volume_usd": USD_FMT,
        "monthly_unlock_vs_volume": PCT_FMT,
    }
    header_map = {cell.value: cell.column for cell in ws[1]}
    for name, fmt in formats.items():
        column = header_map[name]
        ws.cell(row=2, column=column).number_format = fmt
    for column in ws.columns:
        letter = get_column_letter(column[0].column)
        ws.column_dimensions[letter].width = max(13, min(30, len(str(column[0].value)) + 2))
    ws.freeze_panes = "B2"


def add_supply_bridge(wb: Workbook) -> None:
    ws = wb.create_sheet("SUPPLY_BRIDGE")
    headers = ["step", "supply_snx", "change_snx", "share_of_total", "as_of", "source", "notes"]
    rows = [
        ["Pre-mint supply at snapshot block", PRE_MINT_SUPPLY, None, PRE_MINT_SUPPLY / TOTAL_SUPPLY, AS_OF,
         "JSON-RPC eth_call totalSupply at block 25473065", "Ethereum snapshot block timestamp 2026-07-06 11:02:35 UTC"],
        ["Mint under SIP-423", PRE_MINT_SUPPLY + MINT_AMOUNT, MINT_AMOUNT, (PRE_MINT_SUPPLY + MINT_AMOUNT) / TOTAL_SUPPLY, AS_OF,
         "Transfer log in tx 0x0bb737…bc0b9", "Maximum mint equals actual mint: 236,464,356 SNX"],
        ["Post-mint total supply", TOTAL_SUPPLY, MINT_AMOUNT, 1.0, AS_OF,
         "JSON-RPC eth_call totalSupply (latest)", "Matches pre-mint + mint to the token"],
        ["Safe balance", SAFE_BALANCE, None, SAFE_BALANCE / TOTAL_SUPPLY, AS_OF,
         "JSON-RPC balanceOf Safe 0x3265ff13…cf6d", "No outgoing SNX transfers found as of 2026-11-19"],
        ["CoinGecko circulating supply", CIRCULATING, None, CIRCULATING / TOTAL_SUPPLY, AS_OF,
         "CoinGecko /coins/havven market_data", "Includes locked Safe tokens; 99.93% of total supply"],
        ["Pre-mint circulating basis", PRE_MINT_SUPPLY, None, PRE_MINT_SUPPLY / TOTAL_SUPPLY, AS_OF,
         "Derived: post-mint total − mint", "Used for the pre-mint market cap comparison"],
    ]
    write_table(ws, headers, rows, {
        "supply_snx": NUM_FMT, "change_snx": NUM_FMT, "share_of_total": PCT_FMT,
        "as_of": DATE_FMT,
    })
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def add_token_path(wb: Workbook) -> None:
    ws = wb.create_sheet("TOKEN_PATH")
    headers = ["step", "timestamp_utc", "from_address", "to_address", "amount_snx", "tx_hash", "block_number", "verified_by", "notes"]
    rows = [
        [1, dt.datetime(2026, 7, 6, 11, 43, 59), "0x0000000000000000000000000000000000000000",
         "0xc5f0b4194455e0c175ab68c501400e46c7203504", MINT_AMOUNT,
         "0x0bb737a85b740a2e9557859c587cf6ba3c89ad531b960483cdfc89e42e5bc0b9", 25473272,
         "eth_getTransactionReceipt logs", "Mint event; same transaction as steps 2–3"],
        [2, dt.datetime(2026, 7, 6, 11, 43, 59), "0xc5f0b4194455e0c175ab68c501400e46c7203504",
         "0x94433f0da8b5bfb473ea8cd7ad10d9c8aef4ab7b", MINT_AMOUNT,
         "0x0bb737a85b740a2e9557859c587cf6ba3c89ad531b960483cdfc89e42e5bc0b9", 25473272,
         "eth_getTransactionReceipt logs", "Pass-through address"],
        [3, dt.datetime(2026, 7, 6, 11, 43, 59), "0x94433f0da8b5bfb473ea8cd7ad10d9c8aef4ab7b",
         "0xc1c33291f26aa83ba174e3b12da523183ba9f54a", MINT_AMOUNT,
         "0x0bb737a85b740a2e9557859c587cf6ba3c89ad531b960483cdfc89e42e5bc0b9", 25473272,
         "eth_getTransactionReceipt logs", "Intermediate EOA"],
        [4, dt.datetime(2026, 7, 6, 11, 46, 23), "0xc1c33291f26aa83ba174e3b12da523183ba9f54a",
         "0x3265ff13f29fe2dd7501c608b914bfa5e1ffcf6d", MINT_AMOUNT,
         "0xda4c600d3e85437e73f5f4128948877500158e881a32c83b4694c38699d3644c", 25473284,
         "Blockscout token transfers + tx receipt", "Separate tx ~2m24s after mint; no outgoing transfers since"],
    ]
    write_table(ws, headers, rows, {
        "timestamp_utc": DATETIME_FMT, "amount_snx": NUM_FMT, "block_number": NUM_FMT,
    })
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def add_timeline(wb: Workbook) -> None:
    ws = wb.create_sheet("TIMELINE")
    headers = ["event", "date_utc", "offset", "status", "source", "notes"]
    rows = [
        ["SIP-423 created", dt.date(2026, 6, 12), "T0", "Completed", "SIP-423 frontmatter", "Authors: Kain Warwick, Benjamin Celermajer"],
        ["SIP-423 marked Implemented", dt.date(2026, 7, 1), "T0+19d", "Completed", "SIPs commit 180c54b", "Governance status"],
        ["Ethereum snapshot block 25,473,065", dt.datetime(2026, 7, 6, 11, 2, 35), "T0", "Completed", "Ethereum RPC", "Timestamp 2026-07-06 11:02:35 UTC"],
        ["Optimism snapshot block 153,868,527", dt.datetime(2026, 7, 6, 11, 3, 51), "T0", "Completed", "Optimism RPC", "Timestamp 2026-07-06 11:03:51 UTC"],
        ["Mint 236,464,356 SNX", dt.datetime(2026, 7, 6, 11, 43, 59), "T0+41m", "Completed", "Ethereum tx 0x0bb737…bc0b9", "Block 25,473,272"],
        ["Transfer to Safe", dt.datetime(2026, 7, 6, 11, 46, 23), "T0+44m", "Completed", "Ethereum tx 0xda4c60…d3644c", "Block 25,473,284"],
        ["SIP update records mint and snapshots", dt.date(2026, 8, 16), "T0+41d", "Completed", "SIPs commit 6fffb2c", "Adds exact 236,464,356 and block numbers"],
        ["Claim window opens (estimate)", CLAIM_WINDOW_OPEN, "T0+365d", "Scheduled", "SIP-423 timeline", "365 days after snapshot/freeze; deployment date may shift"],
        ["6-month unclaimed expiry (if applied)", UNCLAIMED_EXPIRY, "T0+549d", "TBD", "SIP-423 text", "Conflicts with the TBD row in configurable values"],
        ["One-year vest ends (estimate)", VEST_END, "T0+730d", "Scheduled", "SIP-423 text", "Linear vest after 1-year lock"],
    ]
    write_table(ws, headers, rows, {"date_utc": DATETIME_FMT})
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def add_market_context(wb: Workbook) -> None:
    ws = wb.create_sheet("MARKET_CONTEXT")
    headers = ["metric", "value", "unit", "as_of", "source", "notes"]
    rows = [
        ["Price", PRICE, "USD", AS_OF, "CoinGecko /coins/havven", "Last updated 2026-11-19T17:03:57Z"],
        ["Market cap", MARKET_CAP, "USD", AS_OF, "CoinGecko", "Uses circulating supply 580.98M"],
        ["Fully diluted valuation", FDV, "USD", AS_OF, "CoinGecko", "Uses total supply 581.40M"],
        ["Circulating supply", CIRCULATING, "SNX", AS_OF, "CoinGecko", "99.93% of total; includes locked tokens"],
        ["Total supply", TOTAL_SUPPLY, "SNX", AS_OF, "Ethereum RPC totalSupply", "Exact value"],
        ["24h volume", VOLUME_24H, "USD", AS_OF, "CoinGecko", "Used as a liquidity proxy only"],
        ["Fees 24h", FEES_24H, "USD", AS_OF, "DefiLlama dailyFees", "Very low absolute level"],
        ["Fees 30d", FEES_30D, "USD", AS_OF, "DefiLlama dailyFees", "Trailing 30 days"],
        ["Fees 1y", FEES_1Y, "USD", AS_OF, "DefiLlama dailyFees", "Trailing 12 months"],
        ["Fees annualized from 30d", FEES_ANNUALIZED_30D, "USD", AS_OF, "Derived: 30d × 365/30", "Short-window annualization"],
        ["TVL", TVL, "USD", AS_OF, "DefiLlama protocol", "Ethereum only; other chains zero"],
        ["TVL 1y ago", TVL_1Y_AGO, "USD", dt.date(2025, 11, 19), "DefiLlama protocol", "For 1-year change"],
        ["TVL peak", TVL_PEAK, "USD", dt.date(2021, 2, 10), "DefiLlama protocol", "All-time peak"],
        ["TVL change 1y", TVL_CHANGE_1Y, "%", AS_OF, "Derived", "Fraction; format as Percent"],
        ["Market cap / 30d fees", MCAP_TO_FEES30, "x", AS_OF, "Derived", "Diagnostic, not fair value"],
        ["Market cap / 1y fees", MCAP_TO_FEES1Y, "x", AS_OF, "Derived", "Diagnostic, not fair value"],
        ["Market cap / TVL", MCAP_TO_TVL, "x", AS_OF, "Derived", "Reported market cap basis"],
        ["FDV / TVL", FDV_TO_TVL, "x", AS_OF, "Derived", "Fully diluted basis"],
        ["Revenue hurdle", 10_000_000, "USD", AS_OF, "SIP-423", "Within 2-year lock-up; configurable via SCCP"],
        ["Revenue hurdle / 1y fees", REVENUE_HURDLE_MULTIPLE, "x", AS_OF, "Derived", "How far current fees are from the hurdle"],
        ["Monthly unlock", MONTHLY_UNLOCK, "SNX", AS_OF, "Derived: mint / 12", "Linear vest assumption"],
        ["Monthly unlock value", MONTHLY_UNLOCK_USD, "USD", AS_OF, "Derived", "At current price"],
        ["Monthly volume proxy", MONTHLY_VOLUME, "USD", AS_OF, "Derived: 24h volume × 30", "Liquidity proxy, not a forecast"],
        ["Monthly unlock / monthly volume", MONTHLY_UNLOCK_VS_VOLUME, "%", AS_OF, "Derived", "At current price"],
    ]
    write_table(ws, headers, rows, {
        "value": NUM_FMT, "as_of": DATE_FMT,
    })
    # Specific formats by row
    fmt_by_metric = {
        "Price": USD2_FMT, "Market cap": USD_FMT, "Fully diluted valuation": USD_FMT,
        "24h volume": USD_FMT, "Fees 24h": USD_FMT, "Fees 30d": USD_FMT, "Fees 1y": USD_FMT,
        "Fees annualized from 30d": USD_FMT, "TVL": USD_FMT, "TVL 1y ago": USD_FMT,
        "TVL peak": USD_FMT, "TVL change 1y": PCT_FMT, "Market cap / 30d fees": NUM_FMT,
        "Market cap / 1y fees": NUM_FMT, "Market cap / TVL": FLOAT_FMT, "FDV / TVL": FLOAT_FMT,
        "Revenue hurdle": USD_FMT, "Revenue hurdle / 1y fees": FLOAT_FMT,
        "Monthly unlock": NUM_FMT, "Monthly unlock value": USD_FMT,
        "Monthly volume proxy": USD_FMT, "Monthly unlock / monthly volume": PCT_FMT,
    }
    for row in range(2, ws.max_row + 1):
        metric = ws.cell(row=row, column=1).value
        if metric in fmt_by_metric:
            ws.cell(row=row, column=2).number_format = fmt_by_metric[metric]
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def add_scenarios(wb: Workbook) -> None:
    ws = wb.create_sheet("SCENARIOS")
    headers = [
        "scenario", "price_usd", "price_vs_par", "total_claim_value_usd", "monthly_unlock_usd",
        "annual_unlock_usd", "monthly_sell_25pct_usd", "monthly_sell_50pct_usd",
        "monthly_sell_100pct_usd", "monthly_unlock_vs_volume", "notes",
    ]
    prices = [0.10, 0.15, PRICE, 0.25, 0.50, 1.00]
    rows = []
    for price in prices:
        if price < 0.25:
            note = "Below $0.25 reference: claim is at a mark-to-market discount; selling incentive is lower."
        elif abs(price - 0.25) < 1e-9:
            note = "At the $0.25 reference: claim equals sUSD par value."
        else:
            note = "Above $0.25: recipients have a gain versus the reference; selling incentive rises."
        monthly = MONTHLY_UNLOCK * price
        rows.append([
            f"Price ${price:.4f}" if price not in (0.10, 0.25, 0.50, 1.00) else f"Price ${price:.2f}",
            price, price / 0.25 - 1, MINT_AMOUNT * price, monthly, MINT_AMOUNT * price,
            monthly * 0.25, monthly * 0.50, monthly,
            monthly / MONTHLY_VOLUME, note,
        ])
    write_table(ws, headers, rows, {
        "price_usd": USD2_FMT, "price_vs_par": PCT_FMT, "total_claim_value_usd": USD_FMT,
        "monthly_unlock_usd": USD_FMT, "annual_unlock_usd": USD_FMT,
        "monthly_sell_25pct_usd": USD_FMT, "monthly_sell_50pct_usd": USD_FMT,
        "monthly_sell_100pct_usd": USD_FMT, "monthly_unlock_vs_volume": PCT_FMT,
    })
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def add_calculations(wb: Workbook) -> None:
    ws = wb.create_sheet("CALCULATIONS")
    headers = ["metric", "formula", "inputs", "result", "notes"]
    rows = [
        ["mint_to_pre", "mint / pre-mint supply", "236,464,356 / 344,939,867.56", MINT_TO_PRE, "Supply increase vs pre-mint"],
        ["mint_to_total", "mint / post-mint supply", "236,464,356 / 581,404,223.56", MINT_TO_TOTAL, "Share of post-mint supply"],
        ["safe_share", "Safe balance / total supply", "236,464,356 / 581,404,223.56", SAFE_SHARE, "Same as mint_to_total while Safe holds all minted tokens"],
        ["safe_value_usd", "Safe balance × price", "236,464,356 × 0.164855", SAFE_VALUE, "Mark-to-market value of the Safe balance"],
        ["claim_value_at_market", "mint × price", "236,464,356 × 0.164855", CLAIM_VALUE_MARKET, "Value of the SNX claim at market price"],
        ["claim_value_at_par", "mint × 0.25", "236,464,356 × 0.25", CLAIM_VALUE_PAR, "Equals 59,116,089 sUSD at 4:1"],
        ["discount_to_par", "price / 0.25 − 1", "0.164855 / 0.25 − 1", DISCOUNT_TO_PAR, "Negative = claim below sUSD par"],
        ["implied_pre_mint_mcap", "pre-mint supply × price", "344,939,867.56 × 0.164855", IMPLIED_PRE_MINT_MCAP, "Comparable market cap on pre-mint basis"],
        ["mcap_ratio_vs_pre_mint", "reported market cap / pre-mint market cap", "95,831,317 / 56,865,061.87", MCAP_RATIO, "Aggregator methodology effect"],
        ["monthly_unlock", "mint / 12", "236,464,356 / 12", MONTHLY_UNLOCK, "Linear vest assumption"],
        ["monthly_unlock_usd", "monthly unlock × price", "19,705,363 × 0.164855", MONTHLY_UNLOCK_USD, "At current price"],
        ["mcap_to_fees30", "market cap / 30d fees", "95,831,317 / 3,678", MCAP_TO_FEES30, "Diagnostic only"],
        ["mcap_to_fees1y", "market cap / 1y fees", "95,831,317 / 32,242", MCAP_TO_FEES1Y, "Diagnostic only"],
        ["mcap_to_tvl", "market cap / TVL", "95,831,317 / 856,123", MCAP_TO_TVL, "Reported market cap basis"],
        ["revenue_hurdle_multiple", "$10M / 1y fees", "10,000,000 / 32,242", REVENUE_HURDLE_MULTIPLE, "How many years of current fees equal the hurdle"],
        ["tvl_change_1y", "current TVL / TVL 1y ago − 1", "856,123 / 88,428,843 − 1", TVL_CHANGE_1Y, "TVL collapse"],
        ["monthly_unlock_vs_volume", "monthly unlock USD / monthly volume proxy", "3,248,527.62 / 189,908,940", MONTHLY_UNLOCK_VS_VOLUME, "Liquidity absorption proxy"],
    ]
    write_table(ws, headers, rows, {"result": FLOAT_FMT})
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def add_decision_rules(wb: Workbook) -> None:
    ws = wb.create_sheet("DECISION_RULES")
    headers = ["gate", "metric", "current_value", "rule", "status", "interpretation"]
    rows = [
        ["Supply overhang", "Safe balance / total supply", f"{SAFE_BALANCE:,.0f} SNX ({SAFE_SHARE:.2%})",
         "FAIL if one address holds >20% of total supply", "FAIL", "Large single-entity overhang; monitor outflows"],
        ["Lock enforceability", "Safe vs vesting contract", "Safe multisig; no on-chain vesting contract",
         "PASS only if lock is enforced by a contract or verified escrow", "CAUTION",
         "Policy commitment, not trustless code"],
        ["Revenue support", "1y fees vs $10M hurdle", f"${FEES_1Y:,.0f} vs $10,000,000",
         "PASS only if revenue approaches the hurdle", "FAIL", "Current fees are ~310x below the hurdle"],
        ["TVL trend", "TVL 1y change", f"{TVL_CHANGE_1Y:.2%}",
         "PASS only if TVL is stable or growing", "FAIL", "TVL down ~99% YoY"],
        ["Market cap methodology", "Reported vs pre-mint market cap", f"{MCAP_RATIO:.3f}x",
         "CAUTION if aggregator treatment changes the base by >20%", "CAUTION",
         "CoinGecko includes locked tokens; report both bases"],
        ["Claim timing", "Claim window and vest", "2027-07-06 → 2028-07-06 (est.)",
         "Track deployment and SIP amendments", "NEUTRAL", "Timing is known but not yet executed"],
        ["Overall research state", "Six-gate summary", "3 FAIL, 2 CAUTION, 1 NEUTRAL",
         "DEFENSIVE if >=2 hard FAILs", "DEFENSIVE", "Research state only; not a recommendation"],
    ]
    write_table(ws, headers, rows)
    status_column = 5
    for row in range(2, ws.max_row + 1):
        cell = ws.cell(row=row, column=status_column)
        value = str(cell.value or "").upper()
        if value == "PASS":
            cell.fill = PatternFill("solid", fgColor="D9EAD3")
        elif value == "FAIL":
            cell.fill = PatternFill("solid", fgColor="F4CCCC")
        elif value == "CAUTION":
            cell.fill = PatternFill("solid", fgColor="FFF2CC")
        elif value == "DEFENSIVE":
            cell.fill = PatternFill("solid", fgColor="FCE5CD")
            cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center", vertical="center")


def add_verification_log(wb: Workbook) -> None:
    ws = wb.create_sheet("VERIFICATION_LOG")
    headers = ["check", "result", "method", "source", "checked_at", "status", "notes"]
    rows = [
        ["Current totalSupply", f"{TOTAL_SUPPLY:,.6f} SNX", "eth_call 0x18160ddd", "Ethereum RPC", CALC_AT, "VERIFIED", "Decimals = 18"],
        ["Pre-mint totalSupply at block 25,473,065", f"{PRE_MINT_SUPPLY:,.6f} SNX", "eth_call at historical block", "Archive RPC", CALC_AT, "VERIFIED", "Snapshot block timestamp 2026-07-06 11:02:35 UTC"],
        ["Safe balanceOf", f"{SAFE_BALANCE:,.6f} SNX", "eth_call 0x70a08231", "Ethereum RPC", CALC_AT, "VERIFIED", "Address 0x3265ff13…cf6d"],
        ["Mint transaction status", "success", "eth_getTransactionReceipt", "Ethereum RPC", CALC_AT, "VERIFIED", "Block 25,473,272"],
        ["Mint transfer logs", "3 × 236,464,356 SNX in one tx", "Receipt log decoding", "Ethereum RPC", CALC_AT, "VERIFIED", "Mint, pass-through, intermediate EOA"],
        ["Transfer to Safe", "236,464,356 SNX at 11:46:23 UTC", "Tx + Blockscout token transfers", "Blockscout", CALC_AT, "VERIFIED", "Tx 0xda4c60…d3644c"],
        ["Safe outgoing SNX transfers", "0 (as of 2026-11-19)", "Blockscout token-transfer query", "Blockscout", CALC_AT, "VERIFIED", "Point-in-time; not a permanent guarantee"],
        ["Snapshot block timestamps", "ETH 11:02:35; OP 11:03:51 UTC", "eth_getBlockByNumber", "Ethereum + Optimism RPC", CALC_AT, "VERIFIED", "2026-07-06"],
        ["SIP-423 max mint", "236,464,356 SNX", "Primary text", "GitHub SIPs", CALC_AT, "VERIFIED", "Commit 6fffb2c records the number"],
        ["SIP-423 sUSD entitlement", "59,116,089 sUSD", "Primary text", "GitHub SIPs", CALC_AT, "VERIFIED", "4:1 ratio check: 59,116,089 × 4 = 236,464,356"],
        ["CoinGecko circulating supply", f"{CIRCULATING:,.6f} SNX", "API", "CoinGecko", CALC_AT, "VERIFIED", "99.93% of total"],
        ["CoinGecko market cap / FDV", f"${MARKET_CAP:,.0f} / ${FDV:,.0f}", "API", "CoinGecko", CALC_AT, "VERIFIED", "Same API snapshot"],
        ["DefiLlama fees", f"${FEES_30D:,.0f} 30d; ${FEES_1Y:,.0f} 1y", "API", "DefiLlama", CALC_AT, "VERIFIED", "Daily fees; no protocol revenue breakdown"],
        ["DefiLlama TVL", f"${TVL:,.0f}", "API", "DefiLlama", CALC_AT, "VERIFIED", "Ethereum only in currentChainTvls"],
        ["Coinbase / CoinCodex circulating supply", "not independently verified in this pass", "API/page access failed", "Coinbase / CoinCodex", CALC_AT, "UNVERIFIED", "Do not assert their methodology without a dated snapshot"],
        ["Receipt contract deployment", "not observed", "SIP status and on-chain search", "SIP-423", CALC_AT, "OPEN", "Claim contract deployment date remains TBC"],
        ["Unclaimed entitlement treatment", "TBD / conflicting text", "SIP-423 configurable values", "GitHub SIPs", CALC_AT, "OPEN", "Do not present 2028-01-06 as final"],
    ]
    write_table(ws, headers, rows, {"checked_at": DATETIME_FMT})
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def add_sources(wb: Workbook) -> None:
    ws = wb.create_sheet("SOURCES")
    headers = ["source_id", "provider", "dataset_or_endpoint", "metric_covered", "url", "as_of", "limitations"]
    rows = [
        ["SRC-001", "Ethereum JSON-RPC (publicnode / archive RPC)", "eth_call, eth_getTransactionReceipt, eth_getBlockByNumber",
         "totalSupply, balanceOf, tx logs, block timestamps", "https://ethereum-rpc.publicnode.com", AS_OF,
         "Public endpoint; archive calls may be rate-limited; verify with a second provider before publication"],
        ["SRC-002", "Blockscout", "Address token transfers", "Incoming/outgoing SNX transfers for the Safe",
         "https://eth.blockscout.com/address/0x3265ff13f29fe2dd7501c608b914bfa5e1ffcf6d?tab=token_transfers", AS_OF,
         "Point-in-time; pagination and indexing can lag"],
        ["SRC-003", "Synthetix SIPs (GitHub)", "content/sips/sip-423.md", "SIP terms, max mint, snapshot blocks, vesting, revenue hurdle",
         "https://github.com/Synthetixio/SIPs/blob/master/content/sips/sip-423.md", AS_OF,
         "Governance text; implementation details may change via SCCP"],
        ["SRC-004", "CoinGecko", "/coins/havven", "Price, market cap, FDV, circulating supply, volume",
         "https://www.coingecko.com/en/coins/havven", AS_OF,
         "Aggregator methodology; includes locked tokens in circulating supply"],
        ["SRC-005", "DefiLlama", "/summary/fees/synthetix?dataType=dailyFees", "Fees 24h / 30d / 1y",
         "https://defillama.com/protocol/synthetix", AS_OF,
         "Fees are not protocol revenue or profit; methodology can change"],
        ["SRC-006", "DefiLlama", "/protocol/synthetix", "TVL history and current TVL",
         "https://defillama.com/protocol/synthetix", AS_OF,
         "TVL is chain/protocol coverage dependent; currentChainTvls shows Ethereum only"],
        ["SRC-007", "Etherscan", "Token, address, tx pages", "Human-readable verification links",
         "https://etherscan.io/token/0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F", AS_OF,
         "Explorer UI; use RPC/Blockscout for programmatic checks"],
        ["SRC-008", "Internal calculations", "build_snx_data_pack.py", "Derived ratios, scenarios, valuation diagnostics",
         "", AS_OF, "Inherit all source limitations; not investment advice"],
    ]
    write_table(ws, headers, rows, {"as_of": DATE_FMT})
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def add_dashboard_layout(wb: Workbook) -> None:
    ws = wb.create_sheet("DASHBOARD_LAYOUT")
    headers = ["page", "section", "chart_type", "dimension", "metric", "notes"]
    rows = [
        ["1. Executive", "KPI row", "Scorecards", "", "price_usd; market_cap_usd; fdv_usd; safe_share; claim_value_at_market_usd; discount_to_par",
         "Source KPI; 6 cards"],
        ["1. Executive", "Research state", "Scorecard", "status", "Overall research state", "DEFENSIVE; explain it is not a recommendation"],
        ["2. Supply bridge", "Supply bridge", "Waterfall / bar", "step", "supply_snx", "Source SUPPLY_BRIDGE; annotate pre-mint, mint, post-mint, Safe, circulating"],
        ["2. Supply bridge", "Safe share", "Scorecard", "", "safe_share; safe_value_usd", "40.67% of total supply; mark-to-market value"],
        ["3. Token path", "Transfer table", "Table", "step", "timestamp_utc; from_address; to_address; amount_snx; tx_hash", "Source TOKEN_PATH; link tx hashes"],
        ["3. Token path", "Safe balance", "Time series / scorecard", "as_of", "safe_balance_snx", "Point-in-time; add outflow alert threshold >1%"],
        ["4. Timeline", "Unlock timeline", "Table / timeline", "date_utc", "event; status", "Source TIMELINE; mark estimates"],
        ["4. Timeline", "Monthly unlock", "Bar / scorecard", "", "monthly_unlock_snx; monthly_unlock_usd", "Linear vest assumption; label it"],
        ["5. Valuation", "Market cap vs fees", "Bar / scatter", "metric", "market_cap_usd; fees_1y_usd", "Show both reported and pre-mint market cap"],
        ["5. Valuation", "Revenue hurdle", "Scorecard / bar", "", "revenue_hurdle_multiple", "10M / 1y fees; 310x"],
        ["5. Valuation", "TVL", "Time series", "as_of", "tvl_usd", "Source MARKET_CONTEXT; show 1y ago and peak"],
        ["6. Scenarios", "Sell pressure", "Table / bar", "price_usd", "monthly_sell_25pct_usd; monthly_sell_50pct_usd; monthly_sell_100pct_usd", "Source SCENARIOS; label assumptions"],
        ["7. Risk & monitoring", "Decision gates", "Gate cards", "gate", "status; current_value", "Source DECISION_RULES"],
        ["7. Risk & monitoring", "Verification log", "Table", "check", "result; status", "Source VERIFICATION_LOG"],
        ["7. Risk & monitoring", "Sources", "Table", "source_id", "provider; metric_covered; limitations", "Source SOURCES"],
    ]
    write_table(ws, headers, rows)
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)


def main() -> None:
    wb = Workbook()
    wb.remove(wb.active)
    readme = wb.create_sheet("README")
    add_readme(readme)
    add_kpi(wb)
    add_supply_bridge(wb)
    add_token_path(wb)
    add_timeline(wb)
    add_market_context(wb)
    add_scenarios(wb)
    add_calculations(wb)
    add_decision_rules(wb)
    add_verification_log(wb)
    add_sources(wb)
    add_dashboard_layout(wb)
    wb.save(OUTPUT)
    print(f"OK: {OUTPUT}")
    print(f"sheets={len(wb.sheetnames)} size={OUTPUT.stat().st_size/1024/1024:.2f} MB")


if __name__ == "__main__":
    main()
