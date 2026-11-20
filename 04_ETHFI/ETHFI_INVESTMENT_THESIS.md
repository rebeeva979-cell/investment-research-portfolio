# Ether.fi (ETHFI) — Investment Thesis

**Статус:** Baseline assembled / final rating pending. Срез данных: 16 ноября 2026 UTC.

## Executive question

Растёт ли бизнес Ether.fi достаточно качественно, чтобы его экономический рост отражался в стоимости ETHFI, или протокол растёт в основном за счёт субсидий, эмиссии и привлечения капитала, не создавая value accrual для токена?

## Короткий вывод, который должен появиться в финальной версии

Финальный отчёт должен закончиться одним из трёх состояний:

- `Bull`: adoption и retained revenue растут, dilution контролируема, механизм value accrual подтверждён;
- `Base`: продукт используется, но рост стоимости токена зависит от внешнего рынка ETH, incentives или будущего governance;
- `Bear`: fees не превращаются в устойчивую protocol revenue, unlocks создают sell pressure, а риски restaking/liquidity недооценены.

## Наблюдаемый baseline на 16.11.2026

По независимому API-срезу DefiLlama и рыночному срезу CoinGecko:

- цена ETHFI — около `$0.479`, market cap и FDV — около `$478m`;
- parent TVL Ether.fi — около `$3.85bn`; TVL снизился примерно на `13.3%` за 7 дней и на `23.5%` за 30 дней;
- gross fees за 30 дней — около `$14.1m`, protocol revenue — около `$3.88m`;
- наблюдаемая конверсия gross fees в protocol revenue — около `27.6%`;
- holders revenue в последнем 30-дневном окне в срезе DefiLlama равен `0`, поэтому protocol revenue нельзя называть денежным потоком держателя ETHFI;
- отношение market cap к annualised protocol revenue — около `10.3x`, но это screening multiple: в знаменателе нет проверенных расходов, incentives и treasury reconciliation.

Есть существенный источникный конфликт по circulating supply: CoinGecko показывает около `998.5m`, а страница unlocks DefiLlama — около `983.0m` и примерно `1.7%` ещё locked. До reconciliation supply-based valuation нельзя считать точной.

**Промежуточный статус:** `Base / Watchlist`, не рекомендация к покупке. Adoption и экономика требуют объяснения снижения TVL; value accrual ETHFI подтверждён политикой buyback и staking utility на уровне документации, но фактический объём исполненных buybacks и holder distributions ещё не reconciled on-chain.

## Инвестиционная гипотеза

### Потенциальная bull-гипотеза

Ether.fi может быть интересен, если одновременно выполняются четыре условия:

1. eETH / weETH и связанные продукты привлекают капитал не только через incentives;
2. протокол получает устойчивые fees от staking, restaking, lending или других сервисов;
3. после выплат операторам, валидаторам и incentives остаётся измеримая retained revenue;
4. ETHFI получает подтверждённый механизм value accrual: fee distribution, buyback, staking utility, governance rights with economic power или иной enforceable mechanism.

### Что может разрушить гипотезу

- TVL держится только на баллах и токенных наградах;
- gross fees ошибочно принимаются за protocol revenue;
- доходы растут, но treasury не удерживает денежный поток;
- ETHFI имеет высокий FDV и большой future unlock overhang;
- держатель токена не получает экономической связи с ростом протокола;
- restaking, oracle, operator concentration или liquidity risk приводит к потере доверия.

## Evidence map

| Вопрос | Нужная метрика | Источник первого выбора | Состояние |
|---|---|---|---|
| Растёт ли adoption? | TVL, deposits, withdrawals, active wallets, eETH/weETH supply | Official contracts, DefiLlama, Dune | TVL baseline loaded; wallets/flows pending |
| Какие продукты работают? | eETH, weETH, staking, restaking, lending, vault usage | Ether.fi docs and contracts | To verify |
| Сколько платят пользователи? | Gross fees by product | Protocol docs, contract events, Dune | 30d gross fees loaded; product split pending |
| Сколько остаётся протоколу? | Protocol revenue after operator/validator/partner share | Treasury disclosures and contracts | 30d revenue loaded; cost waterfall pending |
| Есть ли net economics? | Revenue minus incentives and operating/security costs | Treasury, governance, emissions | To verify |
| Получает ли ETHFI value? | Distribution, buyback, staking utility, governance rights | Token docs, contracts, governance | Policy documented; execution reconciliation pending |
| Не переоценён ли токен? | Market cap, FDV, unlock-adjusted supply, fees/revenue multiples | CoinGecko/CMC plus token docs | Multiples loaded; supply conflict unresolved |
| Что может сломать кейс? | Slashing, liquidity, concentration, unlocks, governance | Audits, contracts, governance, holder data | To verify |

## Bull / Base / Bear framework

| Сценарий | Adoption | Economics | Token value accrual | Главный риск |
|---|---|---|---|---|
| Bull | TVL и product usage растут без ускорения incentives | Retained revenue растёт быстрее расходов | Есть юридически и технически подтверждённый механизм | Конкуренция и smart-contract risk |
| Base | TVL стабильна или растёт умеренно | Gross fees есть, net revenue неочевидна | ETHFI в основном governance / utility token | Dilution и зависимость от ETH рынка |
| Bear | TVL падает после снижения incentives | Revenue сжимается, расходы фиксированы | Value accrual отсутствует | Slashing, liquidity event или unlock sell pressure |

## Decision gates

До формулировки инвестиционного вывода нужно пройти gates:

1. **Product gate:** понятно, за какой сервис платит пользователь.
2. **Adoption gate:** есть рост капитала и использования, а не только token emissions.
3. **Revenue gate:** gross fees reconciled to protocol revenue.
4. **Profitability gate:** incentives and costs separated from revenue.
5. **Token gate:** circulating supply, unlocks and value accrual verified.
6. **Risk gate:** smart-contract, slashing, liquidity and governance risks mapped to triggers.
7. **Valuation gate:** at least one defensible multiple or scenario valuation.

Если не пройден Revenue gate или Token gate, итоговый рейтинг не может быть выше `Watchlist`.

## Финальный формат

1. One-page executive summary.
2. Product and competitive map.
3. Adoption and TVL analysis.
4. Financial and tokenomics model.
5. Valuation scenarios.
6. Risk assessment.
7. Weekly change note.
8. Appendix: source register, SQL, contract addresses and dashboard screenshots.

## Decision Card — 16 ноября 2026

| Поле | Решение |
|---|---|
| `decision_status` | `wait` |
| `confidence` | `medium` |
| `valuation_range` | `N/A`: около `10.3x` annualised protocol revenue — только screening multiple; expenses, treasury flow и supply conflict не reconciled |
| `max_position_pct` | до `2%` как high-risk token satellite |
| `main_risk` | TVL снизился примерно на `23.5%` за 30 дней, а holders revenue в последнем 30-дневном окне равен `0` |
| `thesis_invalidation` | продолжение падения TVL вместе с ухудшением revenue capture и отсутствие подтверждённого on-chain исполнения buybacks/distributions |
| `next_catalyst` | treasury/buyback reconciliation, supply reconciliation и новый weekly KPI snapshot |
| `next_review_date` | `2026-11-23` |

До прохождения revenue, cost и token gates допустимо только наблюдение или небольшая заранее ограниченная позиция.
