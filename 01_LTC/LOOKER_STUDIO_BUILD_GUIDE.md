# Litecoin Investment Research в Looker Studio

Этот файл описывает сборку рабочего investment-research дашборда по LTC из `LTC_LOOKER_DATASET.xlsx`.
Дашборд предназначен для дисциплинированной проверки тезиса и риска. Он не превращает on-chain метрики в автоматическую рекомендацию купить или продать.

## 0. Что использовать

- `LTC_LOOKER_STARTER.xlsx` — компактная версия на 11 листов для быстрой сборки в Looker Studio.
- `LTC_LOOKER_DATASET.xlsx` — полная research-база на 20 листов, когда понадобятся blocks, transfers, mining, supply и valuation.
- `LOOKER_STUDIO_STARTER_CHECKLIST.md` — короткий чеклист на 3 первые страницы.
- `LTC_Dashboard.html` — локальный интерактивный дашборд без Google-аккаунта. Это не Looker Studio, но готовый portfolio-артефакт.
- `LTC_RESEARCH_MEMO.md` — текстовый investment memo с выводами и ограничениями.

Для первого прохода используй `LTC_LOOKER_STARTER.xlsx`: он быстрее загружается и не перегружает интерфейс. Полный workbook подключай по мере необходимости.

## 1. Подготовка источника

1. Загрузить `LTC_LOOKER_STARTER.xlsx` (или полный `LTC_LOOKER_DATASET.xlsx`) в Google Drive.
2. Открыть файл через Google Sheets и сохранить как Google-таблицу.
3. В Looker Studio создать отчёт → **Add data** → **Google Sheets**.
4. Выбрать лист `MARKET_DAILY`, включить `Use first row as headers` и отключить агрегацию даты.
5. Добавить отдельные источники для `KPI_LATEST`, `ONCHAIN_DAILY`, `PEER_LATEST`, `DECISION_RULES`, `YEARLY_SUMMARY`, `MONTHLY_RETURNS`, `DATA_QUALITY` и `SOURCES`. В полном workbook дополнительно доступны `LTC_BLOCKS`, `TRANSFER_DAILY`, `MINING_DAILY`, `SUPPLY_DAILY`, `VALUATION_DAILY` и `PEER_DAILY`.
6. В настройках полей проверить типы:
   - `date` → Date;
   - `price_*_usd`, `ma_*_usd`, `high_water_mark_usd` → Currency / USD;
   - поля без суффикса `_pct` (`return_1d`, `drawdown_from_ath`, `year_return` и т. п.) → Percent;
   - поля с суффиксом `_pct` оставить как Number. Они хранят процентные пункты, например `4.2` означает `4.2%`;
   - `market_cap_usd`, `fees_usd`, `issuance_usd`, `miner_revenue_usd` → Currency / USD;
   - `transfer_value_usd`, `realized_cap_usd`, `subsidy_revenue_usd`, `fee_revenue_usd`, `miner_revenue_usd_blockchair` → Currency / USD;
   - `supply_ltc`, `fees_ltc`, `issuance_ltc`, `miner_revenue_ltc`, `transfer_value_ltc`, `remaining_supply_ltc` → Number;
   - `active_addresses`, `tx_count`, `transfer_tx_count`, `block_count`, `output_count`, `input_count` → Number;
   - `mvrv`, `difficulty`, `block_interval_sec_est`, `estimated_years_to_max_at_current_issuance` → Number.

## 2. Страницы отчёта

### Page 1 — Market Overview

- Scorecards: `price_close_usd`, `return_1d`, `return_30d`, `ytd_return`, `drawdown_from_ath`, `volatility_30d_annualized`.
- Time series: dimension `date`, metrics `price_close_usd`, `ma_30_usd`, `ma_200_usd`.
- Column chart: `date` → `volume`. Заголовок должен содержать `raw volume, unit unconfirmed`.
- Area chart: `date` → `drawdown_from_ath`.
- Date range control: по умолчанию последние 365 дней.

### Page 2 — Cycles & Drawdowns

- Time series с ценой LTC и вертикальными reference lines на `2019-08-05` и `2023-08-02`.
- Отдельно подписать `2027-08-02` как estimate, а не как гарантированную дату.
- Bar chart: `YEARLY_SUMMARY`, dimension `year`, metric `year_return`.
- Pivot / heatmap: `MONTHLY_RETURNS`, dimensions `year` и `month`, metric `monthly_return`.
- Таблица халвингов: `halving_date`, `price_on_or_after_date_usd`, `return_30d`, `return_90d`, `return_180d`, `return_365d`.

### Page 3 — Network Activity

- Active addresses: `date` → `active_addresses`.
- Transactions: `date` → `tx_count`.
- Activity change scorecards: `active_addresses_30d`, `tx_count_30d`.
- Activity efficiency: `date` → `active_addresses_per_tx`.
- Gross transfer demand: source `TRANSFER_DAILY`, `date` → `transfer_value_usd` and `transfer_tx_count`.
- Output structure: `date` → `output_count`, `input_count`, `outputs_per_transfer_tx`.
- Подпись на странице: «адреса не равны пользователям; биржи могут агрегировать множество пользователей».

### Page 4 — Mining & Tokenomics

- Hashrate: `date` → `hashrate`.
- Difficulty and interval: source `LTC_BLOCKS`, `date` → `difficulty`, `block_interval_sec_est`, `block_count`.
- Blocks and issuance: `date` → `block_count`, `issuance_ltc`, `subsidy_revenue_ltc`.
- Miner revenue: source `MINING_DAILY`, `date` → `miner_revenue_usd_blockchair`, `subsidy_revenue_usd`, `fee_revenue_usd`.
- Fee share: `date` → `fee_share_of_miner_revenue_blockchair`.
- Supply: source `SUPPLY_DAILY`, `date` → `supply_ltc`, `remaining_supply_ltc`, `supply_mined`, `supply_inflation_365d`, `estimated_years_to_max_at_current_issuance`.
- В тексте рядом с графиком указать, что miner revenue — валовая выручка до затрат, а `miner_cost_usd` намеренно `N/A`.

### Page 5 — Valuation & Peers

- Market cap: `date` → `market_cap_usd`.
- MVRV / realized cap: source `VALUATION_DAILY`, `date` → `mvrv`, `realized_cap_usd`, `market_cap_usd`.
- Таблица последней общей даты: `PEER_LATEST` — BTC, BCH, DOGE, DASH и LTC. LTC добавлен из базового ряда, остальные — из Coin Metrics; это явно указано в поле `source`.
- Сравнивать одновременно market cap, active addresses, transactions и hashrate. Не строить рейтинг по одной метрике.
- Gross transfer value теперь есть в `TRANSFER_DAILY`, но он включает change/self-transfers и поэтому не является adjusted transfer value. NVT можно строить только с явной подписью gross output proxy.

### Page 6 — Risk & Returns

- Rolling volatility: `date` → `volatility_30d_annualized`.
- Tail-risk scorecards: `var_95_30d`, `var_99_30d`, `downside_deviation_30d_annualized`.
- Risk-adjusted scorecards: `sharpe_30d`, `sortino_30d`, both with MAR = 0.
- Price vs MA200: `date` → `price_vs_ma_200`.
- Таблица по годам: `year`, `year_return`, `realized_vol_annualized`, `year_max_drawdown`.
- Scorecards: `high_52w_close_usd`, `low_52w_close_usd`, `ma_200_usd`.

### Page 7 — Network Economics

Эта страница отвечает на вопросы, которые обычно задают по DeFi-протоколу, но переводит их на уровень Litecoin-сети. Источник: `ECONOMICS_FRAMEWORK`.

- Пользователи: `active_addresses`, `tx_count`, их 30-дневная динамика.
- TVL: пометить как `N/A` для базового L1. Вместо TVL показывать `market_cap_usd` и `supply_ltc`; wrappers/bridges потребуют отдельного датасета.
- Комиссии: `fees_usd_30d_sum`, `fee_to_issuance_30d_ratio`, `fee_share_of_miner_revenue`.
- Расходы/бюджет безопасности: `issuance_usd_30d_sum`, `miner_revenue_usd_blockchair`, `miner_cost_usd`, `hashrate`.
- Transfer demand: `transfer_value_usd`, `output_count`, `outputs_per_transfer_tx`.
- Реальная экономика: `fee_to_issuance_30d_ratio`, `supply_inflation_365d`, `mvrv`, adoption gates.
- Ценность для держателя: `price_close_usd`, `market_cap_usd`, supply inflation и отсутствие прямого fee distribution.

Ключевая оговорка: у LTC нет прямого аналога ETHFI value accrual. Держатель LTC получает потенциальную ценность через спрос на денежный актив, scarcity и сетевое использование, а не через распределение протокольных комиссий.

### Page 8 — Decision Gates

- Scorecard со статусом `DECISION_RULES[Overall research state]`.
- Таблица `gate`, `current_value`, `status`, `interpretation`.
- Четыре основные проверки:
  1. `Market trend`: close выше MA200;
  2. `Momentum`: 30D и 90D доходности положительны;
  3. `Adoption`: активные адреса и транзакции растут за 30 дней;
  4. `Security`: hashrate не снижается, блоки производятся.
- Логика использования: `CONFIRMATION` означает, что минимум три из четырёх gate проходят и нет hard fail; `CAUTION` означает смешанную картину; `DEFENSIVE` — два и более hard fail.
- Это framework для pre-trade review, а не персональная рекомендация и не замена лимитам позиции.

### Page 9 — Data & Sources

- Coverage scorecards из `KPI_LATEST`: `coverage_start`, `coverage_end`, `observations`, `date_gaps`.
- Таблица `DATA_QUALITY`.
- Таблица `SOURCES`.
- Текстовый блок с ограничениями исследования.

## 3. Правила интерпретации

- `ATH` в этом POC — максимум дневного close внутри загруженного ряда, не внутридневной максимум.
- `volume` оставлен как raw field: источник не подтвердил единицу измерения, поэтому нельзя подписывать его как USD.
- `return_*_pct` — audit fields в процентных пунктах. Для графиков и scorecards используйте нормализованные aliases без `_pct`.
- Calendar returns считаются только при наличии точной даты сравнения. Пропуски дат не интерполируются.
- Волатильность годовая считается через `sqrt(365)`, поскольку ряд относится к криптоактиву.
- VaR 95/99% — исторический empirical nearest-rank на последних 30 дневных доходностях, не прогноз максимального убытка.
- Sharpe и Sortino используют MAR = 0 и короткое 30-дневное окно, поэтому их нельзя трактовать как устойчивую долгосрочную оценку качества.
- On-chain источник — Coin Metrics Community API v4. Проверяйте условия Community Data перед коммерческим использованием.
- `active_addresses` — адресная активность, не число пользователей.
- `tx_count` — число транзакций, не экономический объём переводов.
- `transfer_value_usd` — gross non-coinbase output value; в нём остаются change и self-transfers. `adjusted_transfer_value_*` пока `N/A`.
- `hashrate` — proxy сетевой безопасности, не полная оценка стоимости атаки.
- `fees_usd`, `transfer_value_usd` и mining USD fields рассчитаны из native units и Coin Metrics PriceUSD. Это не vendor historical USD fields.
- `miner_cost_usd` остаётся N/A: нет проверенной модели электричества, capex, pool fee и структуры майнеров.
- `mvrv` берётся из Coin Metrics `CapMVRVCur`; `realized_cap_usd` рассчитывается как `market_cap_usd / mvrv`.
- `block_timestamp_utc` в `LTC_BLOCKS` — UTC day anchor агрегированного дня, не timestamp отдельного блока.
- Peer-сравнение использует последнюю общую дату рыночного ряда, чтобы не смешивать разные as-of dates.

## 4. Обновление

Для полного обновления:

```bash
python3 fetch_ltc_research_data.py --start 2018-08-22 --end 2026-11-16
python3 build_ltc_looker_dataset.py
```

Затем заменить листы в Google Sheets или обновить импортированный файл. Перед публикацией отчёта проверить `DATA_QUALITY`, `LTC_CATALOG.csv`, дату `calculated_at_utc` и общий as-of в `KPI_LATEST`.

## 5. Минимальный вывод для research-кейса

В отчёте отдельно показать:

1. Что измерено: цена, доходности, rolling volatility, drawdown, halving context, supply, activity, mining и peers.
2. Что не измерено: adjusted transfer value, фактические затраты майнеров, полная модель стоимости атаки и protocol-level fee distribution.
3. Какие выводы предварительные: это decision-support dashboard, а не автономный торговый бот и не fair-value модель.
