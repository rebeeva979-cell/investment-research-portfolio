# LTC — Looker Studio Starter Checklist

Компактный чеклист для сборки первого investment-research дашборда по Litecoin.
Полная версия логики и всех страниц — в `LOOKER_STUDIO_BUILD_GUIDE.md`.

## Что использовать

- `LTC_LOOKER_STARTER.xlsx` — 11 листов, ~2.3 MB. Быстрее загружается и проще подключается, чем полный workbook.
- `LTC_LOOKER_DATASET.xlsx` — полная research-база (20 листов). Нужна, когда понадобятся blocks, transfers, mining, supply и valuation.
- `KPI_LATEST` — одна строка для scorecards.
- `MARKET_DAILY` — цена, MA, доходности, волатильность, drawdown.
- `ONCHAIN_DAILY` — active addresses, transactions, hashrate, fees, issuance, supply, MVRV.
- `PEER_DAILY` — дневная панель BTC, BCH, DOGE, DASH.
- `PEER_LATEST` — пять активов на последнюю общую дату; LTC добавлен из базового ряда.
- `DECISION_RULES` — 6 gate-проверок и итоговый research state.

## 1. Импорт

1. Загрузи `LTC_LOOKER_STARTER.xlsx` в Google Drive.
2. Открой файл → **File → Open with → Google Sheets** → **Save as Google Sheets**.
3. В Looker Studio: **Create → Report**.
4. **Add data → Google Sheets →** выбери файл.
5. Подключи листы по одному. Каждый лист — отдельный источник.
6. В настройках источника включи **Use first row as headers**.

## 2. Типы полей

| Поле | Тип в Looker Studio |
|---|---|
| `date`, `as_of_date`, `first_date`, `last_date` | Date |
| `price_close_usd`, `ma_30_usd`, `ma_200_usd`, `ath_close_usd_in_dataset`, `high_52w_close_usd`, `low_52w_close_usd` | Currency / USD |
| `market_cap_usd`, `realized_cap_usd`, `fees_usd`, `issuance_usd`, `miner_revenue_usd` | Currency / USD |
| `return_1d`, `return_7d`, `return_30d`, `return_90d`, `return_365d`, `ytd_return`, `drawdown_from_ath`, `volatility_30d_annualized`, `year_return`, `monthly_return` | Percent |
| Поля с суффиксом `_pct` (например, `return_30d_pct`) | Number (процентные пункты) |
| `active_addresses`, `tx_count`, `transfer_count`, `block_count`, `supply_ltc`, `observations` | Number |
| `hashrate`, `mvrv`, `fee_to_issuance_30d_ratio`, `sharpe_30d`, `sortino_30d` | Number |
| `year`, `month`, `halving_epoch` | Number |
| `status` | Text |

Важно: поля без `_pct` хранят доли. `0.042` = `4.2%`. Если поставить им Number, получится `0.04`, а не `4.2%`.

## 3. Минимальные 3 страницы

### Page 1 — Market Overview

1. **Scorecards** из `KPI_LATEST`:
   - `price_close_usd`
   - `return_1d`
   - `return_30d`
   - `ytd_return`
   - `drawdown_from_ath`
   - `volatility_30d_annualized`
2. **Time series** из `MARKET_DAILY`:
   - Dimension: `date`
   - Metrics: `price_close_usd`, `ma_30_usd`, `ma_200_usd`
   - Sort: `date` ascending.
3. **Column chart**:
   - Dimension: `date`
   - Metric: `volume`
   - Title: `Volume (raw, unit unconfirmed)`.
4. **Area chart**:
   - Dimension: `date`
   - Metric: `drawdown_from_ath`
   - Format: Percent.
5. **Date range control**:
   - Default: last 365 days.
   - Apply to the charts on this page.

### Page 2 — On-chain

1. **Time series** из `ONCHAIN_DAILY`:
   - Dimension: `date`
   - Metrics: `active_addresses`, `tx_count`
   - Dual axis or two separate charts.
2. **Time series**:
   - Dimension: `date`
   - Metric: `hashrate`.
3. **Time series**:
   - Dimension: `date`
   - Metrics: `fees_usd`, `issuance_usd`.
4. **Scorecards** из `KPI_LATEST`:
   - `market_cap_usd`
   - `mvrv`
   - `active_addresses_30d_change`
   - `tx_count_30d_change`
   - `hashrate_30d_change`
5. Подпись: addresses ≠ users; hashrate = security proxy, not full attack-cost model.

### Page 3 — Decision Gates

1. **Table** из `DECISION_RULES`:
   - Dimensions: `gate`, `metric`, `status`
   - Metrics: `current_value`
   - Sort: `gate` ascending.
2. **Scorecard**:
   - `Overall research state` = `DEFENSIVE` (или актуальный статус).
3. Цвета:
   - `PASS` — зелёный;
   - `MIXED` — жёлтый;
   - `FAIL` — красный;
   - `DEFENSIVE` — оранжевый.

## 4. Добавить позже

- **Mining & Tokenomics** — `MINING_DAILY`, `SUPPLY_DAILY`, `LTC_BLOCKS` из полного workbook.
- **Valuation & Peers** — `PEER_DAILY`, `VALUATION_DAILY`, `market_cap_usd`, `mvrv`, `realized_cap_usd`.
- **Risk & Returns** — `volatility_30d_annualized`, `var_95_30d`, `var_99_30d`, `sharpe_30d`, `sortino_30d`.
- **Data & Sources** — `DATA_QUALITY`, `SOURCES`, `KPI_LATEST` coverage fields.
- **Monthly heatmap** — `MONTHLY_RETURNS`: rows `year`, columns `month`, metric `monthly_return`.

## 5. Частые ошибки

| Проблема | Решение |
|---|---|
| Looker Studio не видит XLSX | Сначала открой файл как Google Sheets; Looker Studio подключает Google Sheets, а не локальный XLSX. |
| Дата стала текстом | В источнике данных измени тип `date` на Date; проверь формат `YYYY-MM-DD`. |
| Доходность 0.04 вместо 4.2% | Поставь тип Percent для поля без `_pct`. |
| Scorecard показывает сумму | Для `KPI_LATEST` используй одну строку; для `MARKET_DAILY` поставь aggregation = Average или Max, либо используй `KPI_LATEST`. |
| Date range control не фильтрует часть графиков | Все графики страницы должны использовать один источник или быть сгруппированы. Для смешанных источников добавь отдельные controls. |
| Слишком много данных | Начни с `LTC_LOOKER_STARTER.xlsx`, а полный workbook подключай по мере необходимости. |

## 6. Обновление

```bash
python3 01_LTC/fetch_ltc_research_data.py
python3 01_LTC/build_ltc_looker_dataset.py
python3 01_LTC/build_ltc_looker_starter.py
```

Затем замени файл в Google Drive или обнови листы в Google Sheets. Проверь `calculated_at_utc` и `coverage_end` в `KPI_LATEST`.

## 7. Ограничения

- ATH — максимум дневного close в датасете, не внутридневной all-time high.
- Volume — raw field без подтверждённой единицы.
- Active addresses — не уникальные пользователи.
- Miner revenue — валовая выручка, не прибыль.
- Adjusted transfer value и miner costs — `N/A`; не подставлять gross values.
- MVRV — provider metric; низкое значение не является самостоятельным сигналом покупки.
- Это research decision-support, не инвестиционная рекомендация.
