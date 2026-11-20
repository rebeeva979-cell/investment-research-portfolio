# Research stack: crypto + public equities

Цель — не собирать «ещё один график цены», а выпускать воспроизводимый investment case: тезис, экономика, оценка, риски, катализаторы, weekly update и dashboard-приложение.

## Подключённый стек навыков

| Навык | Для каких задач | Выход в проекте |
|---|---|---|
| `digital-assets` | сеть, DeFi, TVL, fees, on-chain valuation | Network / protocol research |
| `token-economics` | supply, unlocks, vesting, FDV, value accrual | Tokenomics model |
| `factor-investing` | value, quality, momentum, size, factor exposure | Equity factor panel и peer screen |
| `performance-metrics` | CAGR, Sharpe/Sortino, drawdown, capture | Portfolio и stock performance |
| `historical-risk` | realized volatility, drawdown, downside risk | Risk page и position limits |
| `forward-risk` | scenarios, stress tests, VaR / expected shortfall | Bear/base/bull и stress dashboard |
| `diversification` | correlations, concentration, portfolio contribution | Portfolio construction |
| `asset-allocation` | crypto/equity/cash allocation | Policy portfolio, не сигнал «купить» |
| `bet-sizing` | sizing по риску и conviction | Max position, risk budget, DCA rules |
| `thesis-tracker` | thesis scorecard, catalysts, falsifiers | Weekly investment-case log |

### Слой финансового консультанта

| Навык | Для каких задач | Выход в проекте |
|---|---|---|
| `investment-policy` | цели, горизонт, риск capacity/willingness, ликвидность и ограничения | IPS / policy portfolio |
| `investment-suitability` | проверка «подходит ли актив этому инвестору», концентрация и размер серии сделок | suitability gate |
| `proposal-generation` | превращение анализа в клиентское предложение | current vs proposed portfolio, fees, scenarios |
| `client-review-prep` | подготовка регулярного пересмотра | agenda, drift table, talking points |
| `liquidity-management` | резерв, cash-flow forecast и liquidity tiers | emergency reserve / cash ladder |
| `rebalancing` | правила drift bands и пополнения без лишних сделок | rebalance plan |
| `finance-psychology` | loss aversion, overconfidence, herding, cooling-off rules | behavioral guardrails |

## Логика финансового консультанта

1. Сначала фиксируем цель, горизонт, обязательные расходы, ликвидность и допустимую просадку.
2. Разделяем **risk capacity** (можно ли финансово пережить убыток) и **risk willingness** (готов ли человек его психологически выдержать). При конфликте действует более низкий уровень.
3. Проверяем актив на разумность: продукт, источники дохода, ликвидность, контрагенты, dilution и сценарий потери капитала.
4. Проверяем suitability на уровне всего портфеля: концентрация, корреляции и суммарный risk budget, а не только отдельная сделка.
5. Определяем SAA/core и satellite-лимиты. On-chain идеи не должны незаметно превращать весь портфель в один фактор риска.
6. Фиксируем правила ребалансировки, дату пересмотра и условия отмены тезиса до сделки.
7. Только потом формируем предложение или список действий.

### On-chain слой: какие навыки использовать

| Слой | Навык | Вопрос, на который отвечает | Основной результат |
|---|---|---|---|
| Network / protocol | `digital-assets` | как работает сеть или протокол и где возникает ценность | фундаментальная карта актива |
| DeFi data | `defillama-api` | как меняются TVL, fees, revenue, DEX volume, stablecoins, bridges | reproducible time series |
| Market data | `coingecko-api` | цена, market cap, FDV, supply, исторические ряды и peers | market-data panel |
| Tokenomics | `token-economics` | supply, unlocks, vesting, emissions, burns, value accrual | dilution / supply model |
| Holders | `token-holder-analysis` | кто владеет токеном и насколько концентрирован supply | top-N, Gini, HHI, Nakamoto, insider flags |
| Wallet behavior | `wallet-profiling` | whale/smart-money wallet действительно зарабатывает или это один удачный трейд | win rate, profit factor, hold time, drawdown |
| Wallet flows | `whale-tracking` | накопление, распределение и крупные переводы | whale-flow log и alerts |
| Sybil / wash | `sybil-detection` | активность настоящая или скоординированная | cluster / fake-activity risk |
| DEX execution | `dexscreener-api`, `liquidity-analysis` | можно ли войти/выйти без чрезмерного price impact | liquidity, slippage, pool risk |
| Transaction detail | `helius-api`, `birdeye-api` | какие адреса, программы и сделки стоят за агрегированной метрикой | parsed transactions и wallet evidence |

### Investment-analysis слой: какие навыки использовать

| Слой | Навык | Вопрос | Выход |
|---|---|---|---|
| Investment memo | `ic-memo` | можно ли защитить решение перед инвестиционным комитетом | IC-ready memo |
| Thesis | `thesis-tracker` | что должно быть правдой и что отменит тезис | scorecard, catalyst log, falsifier |
| Valuation / factors | `factor-investing` | доходность — это alpha или market/value/momentum/quality exposure | factor panel |
| Performance | `performance-metrics` | сколько доходности получено на единицу риска | Sharpe, Sortino, drawdown, capture |
| Historical risk | `historical-risk` | как актив реально падал и сколько времени восстанавливался | volatility, VaR, max drawdown |
| Forward risk | `forward-risk` | что произойдёт в stress-сценарии | scenario loss, ES/VaR, stress table |
| Portfolio | `asset-allocation`, `diversification` | сколько держать и что действительно диверсифицирует риск | SAA/TAA, correlations, risk contributions |
| Sizing | `bet-sizing` | какой размер позиции допустим при заданном риске | max position, tranche size, DCA rules |
| Policy / suitability | `investment-policy`, `investment-suitability` | соответствует ли актив целям, горизонту и ограничениям инвестора | IPS and suitability gate |
| Client output | `proposal-generation` | как превратить анализ в понятное предложение | client-ready proposal |

`yield-analysis`, `impermanent-loss`, `mev-analysis` и `liquidity-management` подключаются как специальные модули для DeFi-yield, LP и execution-кейсов; они не должны автоматически превращать nominal APR в инвестиционную рекомендацию.

## Как стек будет работать в одном исследовании

1. **Investment question:** формулируем решение: `buy/add`, `hold`, `trim`, `avoid` или `wait`, а не просто «покажи график».
2. **Protocol map:** `digital-assets` описывает продукт, chain, конкурентов, trust assumptions и механизм value accrual.
3. **Data pull:** `defillama-api` / `coingecko-api` дают временные ряды; `helius-api` / `birdeye-api` / RPC используются для проверки важных адресов и транзакций.
4. **On-chain quality:** `token-holder-analysis`, `wallet-profiling`, `whale-tracking` и `sybil-detection` проверяют концентрацию, инсайдеров, wash activity и качество роста.
5. **Economics:** считаем gross fees → protocol revenue → costs/incentives → net economics; TVL не смешиваем с revenue.
6. **Tokenomics:** строим circulating/max supply, unlock calendar, net inflation, sell-pressure и value-accrual model.
7. **Valuation:** применяем market cap/FDV-to-revenue/fees/TVL, NVT/MVRV при наличии проверенного source, peers и сценарии.
8. **Risk:** `historical-risk` + `forward-risk` дают drawdown и stress cases; `asset-allocation`/`bet-sizing` переводят это в лимит позиции.
9. **Decision card:** `thesis-tracker` и `ic-memo` фиксируют confidence, valuation range, max position, main risk, invalidation, catalyst и next review date.

## Единая модель оценки

### Для токена / протокола

1. Product and adoption: TVL, users, flows, retention, product mix.
2. Economics: gross fees → protocol revenue → costs/incentives → net economics.
3. Tokenomics: circulating/max supply, unlocks, insider share, treasury, value accrual.
4. Valuation: market cap/FDV to revenue, fees, TVL and comparable protocols.
5. Risks: smart contracts, oracle, liquidity, governance, concentration, dilution.
6. Decision: Bull / Base / Bear, invalidation trigger, max position.

### Для акции

1. Business quality: revenue growth, gross margin, operating leverage, cash conversion.
2. Unit economics: users/rides/cameras/subscribers, ARPU, retention, contribution margin.
3. Balance sheet: cash, debt, liquidity, burn/runway, covenants.
4. Ownership: founders, insiders, institutions, 13F/13G/13D, voting structure.
5. Valuation: EV/Sales, EV/EBITDA, P/E only when earnings are meaningful, FCF yield, net cash/debt.
6. Catalysts and failure modes: earnings, product, merger, regulation, financing, dilution.
7. Decision: research candidate / watchlist / avoid / special situation.

## Quality gates

- Каждый показатель имеет `source_url`, `as_of_date`, `definition`, `method`, `quality_status`.
- SEC/IR и официальные governance/contracts — первичные источники.
- Aggregator используется для screening, но не для окончательного вывода без cross-check.
- TVL не называется выручкой; gross fees не называются прибылью; market cap не смешивается с EV.
- Для equity-метрик GAAP и non-GAAP строки хранятся отдельно.
- Для on-chain-метрик отдельно хранятся `raw_value`, `adjusted_value`, chain, contract/address, block/time range и метод агрегации.
- Любая wallet-метрика обязана разделять EOA, smart-contract, bridge escrow, DEX pool и burn address; иначе concentration и users будут искажены.
- «Рост адресов» не считается ростом пользователей без проверки sybil, повторных адресов, retention и economic activity.
- APR/APY, TVL, volume и fees не называются доходом держателя токена без доказанного value-accrual механизма.
- Текущий срез не является персональной рекомендацией и не заменяет проверку ликвидности, брокера и лимитов риска.
