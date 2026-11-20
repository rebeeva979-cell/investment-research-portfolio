# Macro & ETF Flows — Decision Brief

**Дата среза:** YYYY-MM-DD HH:MM UTC  
**Universe:** SPY, DXY, USDT, BTC/ETH ETF flows, watchlist assets

## Что происходит сейчас

- Risk appetite: `risk-on / mixed / risk-off`
- Dollar/liquidity: `supportive / neutral / restrictive`
- ETF flows: `inflow / mixed / outflow / not reported`
- Stablecoin context: peg deviation, market cap change, exchange liquidity

## Данные

| Блок | Текущее | 1D | 7D | Источник | Quality |
|---|---:|---:|---:|---|---|
| SPY |  |  |  |  |  |
| DXY |  |  |  |  |  |
| USDT price |  |  |  |  |  |
| BTC ETF total |  |  |  |  |  |
| ETH ETF total |  |  |  |  |  |

## Decision Card

| Поле | Значение |
|---|---|
| `decision_status` | `buy/add`, `hold`, `trim`, `avoid` или `wait` |
| `confidence` | `low`, `medium` или `high` |
| `valuation_range` | если применимо; macro regime не заменяет valuation актива |
| `max_position_pct` | только для конкретной позиции, не для индекса рынка |
| `main_risk` |  |
| `thesis_invalidation` |  |
| `next_catalyst` |  |
| `next_review_date` |  |

## Правила интерпретации

- Не считать один день ETF outflow сигналом на полную продажу.
- Не считать пустой строку ETF flow нулевым потоком.
- DXY/SPY — контекст режима, а не готовая сделка.
- USDT около `$1` не доказывает качество резервов.
- Macro brief должен менять размер риска или статус наблюдения только при совпадении нескольких независимых сигналов.
