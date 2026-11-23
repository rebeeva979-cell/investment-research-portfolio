# Litecoin (LTC) — Financial & Tokenomics Model

**Дата:** 21 ноября 2026
**As of:** 19 ноября 2026 (on-chain и dashboard), отдельный market patch 20 ноября хранится отдельно
**Назначение:** объяснить расчёты, а не выдать точную fair value

## 1. Как устроена экономика LTC

Litecoin — базовый PoW-asset. У сети нет treasury, которая собирает протокольную комиссию и распределяет её держателям. Экономическая цепочка выглядит так:

```text
пользовательский спрос → транзакции и fees → доход майнеров
                             + block subsidy → security budget
денежное предложение → выпуск LTC → dilution для держателей до полного выпуска
рыночный спрос → цена и market cap LTC
```

Отсюда важное отличие от DeFi: `transfer_value` и `miner_revenue` не являются revenue держателя LTC.

## 2. Supply bridge

| Показатель | Значение | Формула / смысл |
|---|---:|---|
| Maximum supply | 84,000,000 LTC | заданный hard cap |
| Current supply | 77,848,024 LTC | `SplyCur` Coin Metrics |
| Remaining supply | 6,151,976 LTC | `max_supply - current_supply` |
| Supply mined | 92.68% | `current_supply / max_supply` |
| Annualized issuance | 1,314,000 LTC | trailing/model annualized issuance |
| Current modeled reward | 6.25 LTC/block | reward after 2023 halving |
| Next halving block | 3,360,000 | model field |
| Blocks to next halving | 143,990 | `next_halving_block - current_height` |
| Static years to max | 4.68 | `remaining / annualized issuance`; не дата полного выпуска |

### Ограничение years-to-max

Эта оценка статична и не учитывает будущие халвинги. Она нужна как sanity check, а не как прогноз: фактический срок определяется block interval и последовательным снижением reward.

## 3. Miner revenue bridge

Базовая формула:

```text
gross miner revenue (LTC) = subsidy revenue + fee revenue
gross miner revenue (USD) = gross miner revenue (LTC) × PriceUSD
fee share = fee revenue / gross miner revenue
```

На 19 ноября 2026:

| Компонент | LTC | USD |
|---|---:|---:|
| Subsidy revenue | 3,600.00 | $151,910.70 |
| Fee revenue | 7.27 | $306.59 |
| Gross miner revenue | 3,607.27 | $152,217.29 |
| Fee share | 0.20% | — |

За 30 дней fee/issuance ratio — около **0.00198**. Это означает, что текущий security budget почти полностью subsidy-funded.

`miner_cost_usd` намеренно оставлен `N/A`: публичные daily fields не дают electricity price, ASIC efficiency, capex, pool fee, uptime, энергомикс и hedging. Поэтому нельзя писать «майнеры заработали $152k прибыли» — это только gross revenue proxy.

## 4. Network activity and transfer layer

На 19 ноября:

- active addresses: **243,069**;
- transactions: **148,691**;
- transfer count: **254,992**;
- gross non-coinbase transfer value: **35.10 млн LTC / $1.481 млрд**;
- outputs: **336,289**, inputs: **364,963**.

`transfer_value_usd` считается как gross non-coinbase output value × Coin Metrics `PriceUSD`. В нём остаются change outputs, self-transfers, exchange batching и прочие технические операции. Поля `adjusted_transfer_value_*` оставлены `NULL` со статусом `NOT_AVAILABLE`, потому что без UTXO-кластеризации нельзя честно заявить «платёжный оборот».

## 5. Valuation layer

### Market-cap and realized-cap proxy

```text
MVRV = market cap / realized cap
derived realized cap = market cap / MVRV
```

На 19 ноября:

- market cap: **$3.285 млрд**;
- MVRV: **0.5772**;
- derived realized cap: **$5.691 млрд**.

Это provider metric/derived field, а не DCF. Низкий MVRV может означать, что рыночная цена ниже агрегированной стоимости последнего перемещения монет, но не отвечает на вопрос, появится ли будущий спрос.

### Сценарная оценка

Для LTC лучше использовать сценарии market cap, а не «выручку протокола»:

| Сценарий | Условие | Ориентир цены | Действие |
|---|---|---:|---|
| Bear | activity и fees снижаются, цена ниже MA200 | $25–35 | avoid/add не делать |
| Base | безопасность сохраняется, activity стабилизируется | $35–65 | wait / small hold |
| Bull | activity, fees и market regime восстанавливаются | $65–110 | add только после gates |

Диапазоны не являются статистическим доверительным интервалом и не заменяют peer-adjusted valuation.

## 6. Что считать «реальной экономикой» LTC

| Вопрос | Ответ |
|---|---|
| Есть ли protocol revenue? | Нет treasury revenue в смысле DeFi; есть transaction fees, выплачиваемые майнерам. |
| Есть ли cash flow держателю? | Нет прямого распределения. Держатель зависит от monetary/network demand. |
| Что финансирует безопасность? | В основном subsidy, fees — около 0.20% gross miner revenue в текущем срезе. |
| Что измеряет TVL? | Для базового L1 метрика TVL неприменима; используем supply, market cap, activity и security. |
| Что нужно проверить дальше? | Adjusted transfer value, miner cost model, peer definitions, MWEB coverage. |

## 7. Source lineage

| Слой | Файл / источник | Дата |
|---|---|---|
| Market | `LTC_MARKET_DAILY.csv`, Yahoo continuation patch | 19.11.2026 dashboard; 20.11 отдельно |
| Network/supply/MVRV | `LTC_ONCHAIN_DAILY.csv`, Coin Metrics Community API v4 | 19.11.2026 |
| Blocks/transfers | `LTC_BLOCKS_DAILY.csv`, `LTC_TRANSFER_DAILY.csv`, Blockchair aggregates | 19.11.2026 |
| Catalog | `LTC_CATALOG.csv` | 19.11.2026 |
| Build | `fetch_ltc_research_data.py`, `build_ltc_looker_dataset.py` | reproducible |

Перед коммерческим распространением нужно отдельно проверить terms/license Coin Metrics Community и Blockchair, а также их rate limits.

## 8. Decision Card

| Поле | Решение |
|---|---|
| Статус | `wait` |
| Уверенность | `medium` в расчётах; `low` в выводе о будущей доходности |
| Диапазон оценки | $25–35 bear / $35–65 base / $65–110 bull; сценарный диапазон, не target price |
| Максимальная доля | до 3% ликвидного портфеля, без leverage |
| Главный риск | fee economics не покрывает зависимость security budget от subsidy |
| Условие отмены тезиса | activity и security ухудшаются, а adjusted transfer/fee demand не подтверждаются |
| Ближайший катализатор | новый on-chain snapshot и peer-normalized fee/security comparison |
| Дата следующего пересмотра | через 7 дней после очередного refresh |
