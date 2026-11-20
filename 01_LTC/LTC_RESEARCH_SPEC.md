# Litecoin (LTC) — Research & Looker Studio Project

## Цель
Подготовить воспроизводимый исследовательский кейс о долгосрочной экономической полезности Litecoin как платёжной Proof-of-Work сети и о соответствии сетевой безопасности, денежной модели и рыночной оценки.

## Выбранный охват
- Исторический горизонт: full history, с 2011 года до последней доступной даты.
- Аналитический акцент: balanced.
- Результат: research report + dashboard.
- Конкуренты: BTC, BCH, DOGE, DASH.

## Основные исследовательские блоки
1. Network fundamentals.
2. Adoption & payments.
3. Tokenomics.
4. Mining & security.
5. On-chain behaviour.
6. Market & valuation.
7. Competitive position.
8. Risks & scenarios.

## Планируемые метрики
- Supply, issuance, inflation, remaining supply, stock-to-flow.
- Transactions, active addresses, transfer count, gross output volume, inputs/outputs, fees, transactions per block.
- Miner revenue = block subsidy + transaction fees; fee share; hashrate; difficulty; block interval.
- Realized cap / MVRV.
- Price return, volatility, market cap, volume / market cap, maximum drawdown.
- Сравнительные метрики с BTC, BCH, DOGE и DASH.

## Структура данных
`raw → staging → core → marts`

Предлагаемые таблицы:
- `ltc_blocks`
- `ltc_transactions`
- `ltc_inputs`
- `ltc_outputs`
- `ltc_market_daily`
- `ltc_supply_daily`
- `ltc_mining_daily`
- `ltc_network_daily`
- `ltc_competitors_daily`
- `ltc_research_metrics`

## Источники и ограничения
- Litecoin Core RPC — первичный источник блокчейн-данных; для полного исторического извлечения нужна не-pruned нода. В текущем POC для daily block/transfer aggregates используется Blockchair.
- Bitquery — есть 4 sample Parquet-файла; полный исторический экспорт ранее указывался как платный продукт. Покупку для POC не планировали.
- Coin Metrics Community API v4 — POC-источник для market cap, MVRV, supply, active addresses, transactions, transfer count, hashrate, blocks, issuance и fees в native units. Перед коммерческим использованием проверить license/terms.
- Blockchair Litecoin API — агрегированные blocks и non-coinbase transactions по UTC-дням. Transfer USD считается через Coin Metrics PriceUSD, поскольку historical vendor USD columns не используются.
- CoinGecko / другие market-data providers — рыночные ряды; историческая глубина зависит от тарифа и API.
- MWEB confidential transfers не полностью наблюдаемы.
- Адреса не равны пользователям; gross output value не равен платёжному обороту; hashrate не является абсолютной мерой безопасности.

## Текущие загруженные рыночные данные
Файл `litecoin(1).xlsx` обработан в `LTC_Market_Data_Cleaned.xlsx` и `LTC_MARKET_DAILY.csv`.
- 2 989 дневных записей.
- Период dashboard: 22.08.2018–19.11.2026; отдельный Yahoo market patch содержит наблюдение 20.11.2026.
- 5 разрывов в последовательности дат; отсутствующие даты не интерполированы.
- Есть OHLC и исходное поле volume.
- Единица `volume` не подтверждена; не подписывать его как USD без проверки.
- Market cap и supply добавлены отдельным on-chain source; в исходном загруженном файле их по-прежнему нет.
- `LTC_ONCHAIN_DAILY.csv` содержит derived miner revenue, fee share, supply inflation, MVRV/realized cap, blocks, gross transfer value, mining and supply fields.
- `LTC_BLOCKS_DAILY.csv` содержит daily block height range, difficulty, reward, fee totals and estimated interval.
- `LTC_TRANSFER_DAILY.csv` содержит gross non-coinbase output value, input/output metrics and explicit adjusted-value gap.
- `LTC_PEER_DAILY.csv` содержит выровненный peer panel для BTC, BCH, DOGE и DASH.
- `LTC_CATALOG.csv` фиксирует доступные метрики и окна покрытия.
- `LTC_MARKET_PATCH_2026-11-15_TO_2026-11-20.csv` хранит continuation source; 20.11 не включён в dashboard до появления соответствующего on-chain snapshot.

## Looker Studio: страницы
1. Market Overview.
2. Cycles & Drawdowns.
3. Network Activity.
4. Mining & Tokenomics.
5. Valuation & Peers.
6. Risk & Returns.
7. Network Economics.
8. Decision Gates.
9. Data & Sources.

## Текущий decision-support слой

`DECISION_RULES` содержит четыре проверяемых gate: market trend, momentum, adoption и security. Они формируют состояния `CONFIRMATION`, `CAUTION` или `DEFENSIVE`, но не являются автономным торговым сигналом. В текущем срезе LTC state = `DEFENSIVE`: тренд и adoption не подтверждены, security gate проходит.

## Обновление

```bash
python3 fetch_ltc_research_data.py --start 2018-08-22 --end 2026-11-16
python3 build_ltc_looker_dataset.py
```
