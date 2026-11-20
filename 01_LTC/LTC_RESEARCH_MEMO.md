# Litecoin (LTC) — Investment Research Memo

**Статус:** Market-data POC / не инвестиционная рекомендация  
**Дата расчёта:** 16 ноября 2026  
**Последняя дата рыночного ряда:** 14 ноября 2026  
**Источник:** `litecoin(1).xlsx`, провайдер в исходном файле не указан

## Executive summary

Загруженный ряд описывает слабый рыночный профиль LTC на последней доступной дате: цена закрытия составляет **$44,39**, она находится ниже рассчитанной MA200 (**$51,87**) и примерно на **88,5% ниже максимума дневного close в датасете** (**$386,45**, 9 мая 2021 года).

Последние наблюдаемые результаты:

| Метрика | Значение |
|---|---:|
| 1D return | -10,01% |
| 7D return | -14,82% |
| 30D return | -27,13% |
| 90D return | +0,61% |
| 365D return | -54,48% |
| YTD return | -44,41% |
| 30-observation annualized volatility | 62,45% |
| Historical VaR 95%, 30D | -8,34% |
| Historical VaR 99%, 30D | -10,01% |
| Downside deviation, annualized | 59,17% |
| Rolling Sharpe / Sortino, 30D, MAR 0 | -5,82 / -6,14 |
| 52-week high / low close | $101,77 / $40,85 |

Эти цифры поддерживают вывод о высокой волатильности и значительной просадке. Дополненный on-chain срез позволяет проверить активность и безопасность, но всё ещё не отвечает на вопрос о денежном объёме переводов: в текущем покрытии нет transfer value в USD.

## On-chain и mining snapshot

На общей для market и on-chain данных дате **14 ноября 2026**:

| Метрика | Значение |
|---|---:|
| Market cap | $3,43 млрд |
| Visible supply | 77,83 млн LTC |
| Active addresses | 239 083 |
| Transactions | 162 313 |
| Hashrate | 2 797,15 в единицах Coin Metrics |
| Blocks | 594 |
| Block height range | 3 212 647 — 3 213 240 |
| Average difficulty | 94 729 203 |
| Estimated block interval | 145,45 сек. |
| Issuance / subsidy | 3 712,54 LTC |
| Fees | 6,62 LTC |
| Gross miner revenue | $163,8 тыс. |
| Fee share of gross miner revenue | 0,18% |
| Supply inflation, trailing 365D | 1,71% |
| Gross transfer/output value, non-coinbase | 41,94 млн LTC / $1,85 млрд |
| Transfer transactions | 162 473 |
| Outputs / inputs | 372 619 / 357 222 |
| MVRV | 0,592 |
| Derived realized cap | $5,79 млрд |
| Remaining supply to 84m hard cap | 6,17 млн LTC, 92,66% mined |

Изменения за 30 дней: active addresses **−5,87%**, transactions **−0,77%**, hashrate **+22,70%**, market cap **−23,66%**. Безопасность по хешрейту не ухудшилась, но рыночная капитализация и часть activity-метрик слабее. Низкая fee share показывает, что валовая экономика майнеров почти полностью зависит от block subsidy. Это не оценка чистой прибыли майнеров.

## Расширенный слой: blocks, transfers, mining, supply и valuation

### `ltc_blocks`

В `LTC_BLOCKS_DAILY.csv` и листе `LTC_BLOCKS` добавлены дневные агрегаты Blockchair:

- `block_height_min`, `block_height_max`, `block_count`;
- `difficulty` как средняя сложность блоков за UTC-день;
- `block_interval_sec_est = 86400 / block_count`;
- `block_timestamp_utc` как якорь даты `00:00:00 UTC`.

Последнее поле помечено как `daily_utc_anchor_not_exact_block_time`: агрегированный endpoint не выдаёт один точный timestamp блока для каждой строки. Поэтому в отчёте нельзя называть его временем конкретного блока.

### Transfer value и outputs

В `LTC_TRANSFER_DAILY.csv` и листе `TRANSFER_DAILY` добавлены агрегаты всех non-coinbase transactions:

- `transfer_value_ltc` и `transfer_value_usd` — gross output value;
- input value и fee revenue;
- `output_count`, `input_count`, `outputs_per_transfer_tx`;
- `transfer_tx_count`.

Это полезнее, чем один `tx_count`, но это не adjusted transfer value: в gross output остаются change outputs, self-transfers, биржевые внутренние перемещения и batching. Поля `adjusted_transfer_value_ltc/usd` оставлены `NULL` со статусом `NOT_AVAILABLE`, чтобы не выдавать gross volume за экономический платёжный оборот.

### `ltc_mining_daily`

Лист `MINING_DAILY` объединяет difficulty, subsidy revenue, fee revenue, gross miner revenue, fee share и `miner_cost_usd`.

`miner_cost_usd` остаётся `N/A`: по публичным агрегатам нельзя надёжно восстановить электричество, capex, pool fees, энергомикс, эффективность оборудования и хеджирование. Поэтому `miner_revenue_usd` — валовая выручка, а не прибыль.

### `ltc_supply_daily`

Лист `SUPPLY_DAILY` содержит текущий supply, `max_supply_ltc = 84,000,000`, remaining supply, процент добытого supply, дневную и годовую эмиссию, модельный block reward и следующий halving block.

`estimated_years_to_max_at_current_issuance` — статический сценарий текущего темпа. Он не учитывает будущие халвинги и не является прогнозом даты полного выпуска.

### Realized cap / MVRV

Для LTC в каталоге Coin Metrics доступен `CapMVRVCur`. В отчёте `mvrv` берётся напрямую из этого metric, а `realized_cap_usd` рассчитывается как `market_cap_usd / mvrv`. Лист `VALUATION_DAILY` предназначен для графика market cap, realized cap и MVRV.

MVRV является проверенным provider metric, но низкое значение не является самостоятельным сигналом покупки.

## Как перенести protocol research framework на Litecoin

Для DeFi-протокола обычно смотрят пользователей, TVL, fees, расходы, экономику и value accrual токена. Для LTC соответствие выглядит так:

| Вопрос | Что смотрим по LTC | Статус |
|---|---|---|
| Пользователи | Active addresses и transactions | Есть proxy, но адреса не равны пользователям |
| TVL | Для базового L1 не применим; вместо него market cap и supply | N/A |
| Комиссии | Fees в LTC/USD и fee share | Есть, комиссия мала относительно issuance |
| Расходы | Issuance и security budget proxy | Частично, затрат майнеров нет |
| Реальная экономика | Fee/issuance ratio, activity, supply inflation | Слабая комиссионная самодостаточность |
| Ценность держателя | Price, market cap, scarcity и network demand | Косвенная, fee distribution нет |

Главное отличие от ETHFI: LTC не даёт держателю автоматического права на комиссионный денежный поток протокола. Поэтому рост сети может поддерживать monetary demand, но не гарантирует value accrual для монеты.

## Research question

Проверить, сохраняется ли инвестиционная теза Litecoin как платёжной Proof-of-Work сети, сопоставив:

1. сетевую активность и платёжное использование;
2. денежную модель и выпуск;
3. экономику майнинга и безопасность;
4. рыночную оценку и поведение цены;
5. конкурентную позицию относительно BTC, BCH, DOGE и DASH.

На текущем этапе пункты 1–4 покрыты частично: gross transfer value и MVRV добавлены, но adjusted transfer value и полноценная конкурентная экономика ещё не собраны.

## Что реально измерено

- Дневные OHLC и исходное поле `volume`.
- Доходности на 1, 7, 30, 90 и 365 календарных дней, если точная дата сравнения присутствует.
- MA7, MA30, MA90 и MA200 по trailing observations.
- Реализованная 30-наблюдательная волатильность с annualization через `sqrt(365)`.
- Просадка от максимального дневного close внутри загруженного ряда.
- Годовые и месячные сводки.
- Контекст халвингов и доходность после дат, если рыночные наблюдения покрывают соответствующий горизонт.
- Market cap, MVRV, derived realized cap, supply, active addresses, transaction count, transfer count, hashrate, block count, issuance и fees в native units из Coin Metrics Community API.
- Daily block aggregates, difficulty, height range, reward and fee totals из Blockchair.
- Daily gross transfer/output value, inputs, outputs and non-coinbase transfer counts из Blockchair.
- Peer panel по BTC, BCH, DOGE и DASH на общей последней дате рынка.

## Халвинг-контекст

| Халвинг | Цена на дату / ближайшее наблюдение | +30D | +90D | +180D | +365D |
|---|---:|---:|---:|---:|---:|
| 2015-08-25 | н/д, ряд начинается в 2018 | н/д | н/д | н/д | н/д |
| 2019-08-05 | $96,83 | -30,51% | -39,46% | -26,87% | -40,59% |
| 2023-08-02 | $87,49 | -27,98% | -21,19% | -21,76% | -20,49% |
| 2027-08-02 (estimate) | н/д, дата в будущем | н/д | н/д | н/д | н/д |

Эта таблица не доказывает причинный эффект халвинга. Она показывает только поведение цены в двух покрытых исторических эпизодах. Выборка мала, рыночный режим менялся, а фактический момент исполнения халвинга зависит от высоты блока.

## Preliminary thesis

### Поддерживает тезу

- У сети есть понятная PoW-модель и предсказуемое снижение block subsidy.
- Датасет допускает воспроизводимый мониторинг цены, доходности, drawdown и volatility.
- Халвинг можно использовать как исследовательскую временную ось для дальнейшего сравнения с adoption и mining metrics.

### Ослабляет тезу

- Цена на последней дате ниже MA200 и значительно ниже максимума close в истории ряда.
- 365-дневная доходность отрицательная, а 30-дневная волатильность остаётся высокой.
- Два покрытых халвинга не дали положительной доходности на горизонтах 30–365 дней в этом конкретном ряду.
- Активные адреса и transactions теперь доступны, а gross transfer value добавлен, но он не заменяет adjusted transfer value и не доказывает платёжное использование.

После расширения данных формулировка точнее:

- hashrate и block production выглядят устойчиво в последнем 30-дневном сравнении;
- activity не подтверждает ускорение adoption: active addresses снижаются, transactions почти не растут;
- fee share остаётся очень низкой, поэтому долгосрочная безопасность пока опирается на issuance, а не на комиссионный спрос;
- рыночный тренд и 30D momentum остаются слабыми.

## Decision gates

На дату 14 ноября 2026 research framework даёт состояние **DEFENSIVE**:

1. Market trend: `FAIL`, цена на 14,43% ниже MA200.
2. Momentum: `MIXED`, 30D доходность отрицательная, 90D около нуля.
3. Adoption: `FAIL`, active addresses и transactions не растут одновременно.
4. Security: `PASS`, hashrate за 30 дней вырос и блоки производятся.

Это означает «не увеличивать риск только на основании отскока», а не механический сигнал на полную продажу. Для смены состояния нужны подтверждения в нескольких независимых блоках.

## Что ещё остаётся до полноценного investment research

1. Adjusted transfer value в native/USD с явной UTXO-методологией, исключающей change и self-transfers.
2. Точные timestamps отдельных блоков, если нужен настоящий block-level, а не daily aggregate слой.
3. Полноценная модель затрат майнеров: electricity, capex, pool fees, энергомикс, эффективность ASIC и чувствительность к цене LTC.
4. Детальная модель эмиссии по будущим халвингам с блок-временной симуляцией, а не статическая years-to-max оценка.
5. Расширенный UTXO output layer для realized-cap audit и оценки long-term holder behaviour.
6. Полная конкурентная экономика с одинаковыми transfer, mining cost и valuation definitions для BTC, BCH, DOGE и DASH.
7. Источники, URL, методика извлечения и дата обновления уже записываются на листе `SOURCES`; перед коммерческим распространением нужно проверить API terms и rate limits.

## Ограничения и data quality

- Покрытие: 22 августа 2018 — 14 ноября 2026, 2 984 наблюдения.
- В ряду пять разрывов дат; пропуски не интерполировались.
- Единица измерения `volume` не подтверждена. Нельзя называть его USD-объёмом.
- `ATH` в этом memo — максимум дневного close, не внутридневной high.
- Адреса не равны пользователям, а gross output volume не равен платёжному обороту. Эти метрики потребуют отдельной методологии.
- MWEB и другие особенности приватности могут ограничивать полноту наблюдаемой активности.
- On-chain и mining-метрики добавлены из Coin Metrics Community API v4. Перед коммерческим использованием нужно отдельно проверить лицензию Community Data и условия распространения.
- Block и transfer агрегаты добавлены из Blockchair. `block_timestamp_utc` — UTC day anchor, а не timestamp отдельного блока; API terms и rate limits нужно проверить перед регулярным коммерческим использованием.
- `miner_revenue_usd` — proxy: `(issuance_ltc + fees_ltc) × PriceUSD`, без затрат майнеров и структуры пулов.
- `transfer_value_usd` — gross non-coinbase output value, рассчитанный из native units и Coin Metrics PriceUSD; это не adjusted value и не чистый платёжный оборот.
- `mvrv` — Coin Metrics `CapMVRVCur`; `realized_cap_usd` — derived field `market_cap_usd / mvrv`.
- `miner_cost_usd` — `N/A`, так как фактические затраты майнеров не наблюдаются в текущих источниках.

## Репродуцируемость

Пересборка:

```bash
python3 fetch_ltc_research_data.py --start 2018-08-22 --end 2026-11-16
python3 build_ltc_looker_dataset.py
```

`fetch_ltc_research_data.py` обновляет также `LTC_BLOCKS_DAILY.csv` и `LTC_TRANSFER_DAILY.csv`. Для повторяющихся коммерческих запусков проверьте лимиты Blockchair и при необходимости задайте `BLOCKCHAIR_API_KEY`.

Дашборд собирается по `LOOKER_STUDIO_BUILD_GUIDE.md`. Поле без суффикса `_pct` хранит процент как долю для корректного форматирования в Looker Studio; поле с `_pct` оставлено как audit value в процентных пунктах.

## Decision Card — 16 ноября 2026

| Поле | Решение |
|---|---|
| `decision_status` | `wait` |
| `confidence` | `medium` |
| `valuation_range` | `N/A`: market cap/realized cap и MVRV доступны, но диапазон справедливой стоимости без adjusted transfer value и полноценной mining-cost модели незащищаем |
| `max_position_pct` | до `3%` как watchlist-risk budget; не увеличивать на одном ценовом отскоке |
| `main_risk` | спрос и fee revenue недостаточны, а валовая безопасность сети в основном зависит от block subsidy |
| `thesis_invalidation` | устойчивое ухудшение activity/hashrate, проблемы с выпуском/консенсусом или невозможность подтвердить платёжное использование после расширения UTXO-аналитики |
| `next_catalyst` | обновление on-chain/mining ряда и проверка adjusted transfer value; ближайшая полноценная проверка — после следующего месячного среза |
| `next_review_date` | `2026-12-14` |

Допустимое действие — `wait`, а не автоматическая продажа и не усреднение только потому, что цена ниже исторического максимума.
