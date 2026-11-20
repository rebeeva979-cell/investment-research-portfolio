# ETHFI — Weekly Investment Case Update

**Дата среза:** 20 ноября 2026 UTC  
**Предыдущий срез:** 16 ноября 2026 UTC  
**Статус:** baseline refreshed; revenue/cost/value-accrual reconciliation remains open

## Decision

- **Статус:** `wait / watchlist`
- **Уверенность:** `medium`
- **Оценка:** не финализировать; `10.3x` annualised protocol revenue из старого среза был screening multiple, а не fair value
- **Максимальная доля:** до 2% только как high-risk satellite при отдельном подтверждении suitability
- **Главный риск:** TVL продолжает снижаться, а `holders revenue` в последнем 30-дневном окне равен нулю
- **Отмена тезиса:** продолжение снижения TVL вместе с падением revenue capture и отсутствием подтверждённого исполнения buybacks/distributions
- **Ближайший катализатор:** treasury/cost reconciliation, supply reconciliation и on-chain проверка buyback/cashback
- **Следующий пересмотр:** 27 ноября 2026 или раньше при governance/treasury событии

## Что изменилось

| Метрика | 16.11 | 20.11 | Изменение | Интерпретация |
|---|---:|---:|---:|---|
| ETHFI price | $0.478619 | $0.473372 | −1.10% | Небольшое рыночное снижение |
| Market cap | $477.9m | $472.7m | −1.10% | Движение следует цене при стабильной supply базе |
| Parent TVL | $3.848bn | $3.725bn | −3.19% | Краткосрочно отрицательный сигнал; 7d change −12.39% |
| TVL change, 30d | −23.50% | −26.66% | ухудшение | Сокращение капитала ускорилось |
| Gross fees, 30d | $14.083m | $13.924m | −1.12% | Платежная активность слегка снизилась |
| Protocol revenue, 30d | $3.882m | $3.892m | +0.25% | Retained-revenue proxy почти стабильна |
| Revenue capture ratio | 27.57% | 27.95% | +0.38 п.п. | Небольшое улучшение, но методика DefiLlama не заменяет P&L |
| Holders revenue, 30d | $0 | $0 | без изменений | Распределение держателям в источнике не наблюдается |
| Unlock-page locked | 16.98m | 16.40m | −0.58m | Непогашенная доля уменьшается; continuous release продолжается |

## Как это влияет на тезис

**Ослабляет:** TVL за четыре дня снизился примерно на `$123m`, а 30-дневное изменение ухудшилось до `−26.66%`. Это требует объяснения: withdrawals, смена состава TVL, цена ETH или incentive-driven capital.

**Стабилизирует:** protocol revenue за 30 дней не упала вместе с TVL и остаётся около `$3.9m`. Это может означать устойчивость fee-generating части, но пока неизвестно, сколько из неё остаётся после operator/partner share, incentives, operating и security costs.

**Не решает проблему токена:** holders revenue остаётся `$0` в срезе DefiLlama. Официальная политика buyback/cashback описывает механизм, но policy не доказывает фактический объём и дату on-chain исполнения.

## Evidence quality

- TVL, fees, protocol revenue и holders revenue: DefiLlama API; independent aggregator, methodology review required.
- Цена, market cap и supply: CoinGecko API; provider-defined supply methodology.
- Allocation, vesting и value-accrual policy: official Ether.fi governance materials and DefiLlama rights registry.
- Source register обновлён до 20.11.2026 в `ETHFI_SOURCE_REGISTER.csv`.

## Что пока нельзя утверждать

1. Нельзя называть `$3.89m` чистой прибылью: расходы и treasury inflows не reconciled.
2. Нельзя называть buyback policy денежным потоком держателя ETHFI без on-chain transaction trail.
3. Нельзя считать снижение TVL чистым оттоком пользователей без product/chain decomposition.
4. Нельзя строить точный FDV-мультипликатор при конфликте circulating supply между CoinGecko и unlock page.

## Следующие проверки

1. Разложить protocol revenue по operator, partner, incentives и treasury components.
2. Проверить official governance/treasury wallet flows и фактические buyback/cashback transactions.
3. Сверить continuous unlock с wallet-level distribution и effective float.
4. Добавить users, deposits, withdrawals, eETH/weETH supply и product mix.
5. После reconciliation обновить bull/base/bear valuation и Decision Card.

