# On-chain + Investment Research Playbook

**Статус:** подключённый рабочий процесс для LTC, ETHFI, SNX, UNI и новых токенов/протоколов.

## Что именно мы делаем

Отчёт должен отвечать на шесть вопросов:

1. Есть ли реальный продукт и пользователи?
2. Растёт ли экономическая активность, а не только цена/TVL?
3. Сколько денег получает протокол и сколько тратит?
4. Как supply, unlocks и holders влияют на цену токена?
5. Не переоценён ли актив относительно экономики и peer group?
6. Какое действие допустимо при текущем риск-бюджете?

7. Соответствует ли это действие целям, горизонту, ликвидности и психологической переносимости инвестора?

## Пайплайн анализа

### 1. Product and network map

Используем `digital-assets`: chain security, consensus, smart-contract dependencies, oracle/bridge assumptions, product surface, competitors and value-accrual mechanism.

### 2. Adoption and activity

Собираем:

- active addresses и новые адреса;
- retained / returning addresses;
- transactions, transfer value и adjusted transfer value;
- protocol users, deposits, withdrawals и utilization;
- DEX volume, stablecoin supply и bridge flows;
- TVL с разбиением на chain, asset и protocol.

Источники: `defillama-api`, `coingecko-api`, chain RPC, `helius-api`, `birdeye-api`.

### 3. Protocol economics

Храним отдельные строки:

`gross fees → protocol revenue → token-holder revenue → operating costs/incentives → net protocol economics`.

Нельзя называть TVL выручкой, volume доходом или nominal APR реальной доходностью. Для LP добавляем impermanent loss, slippage, pool concentration и MEV.

### 4. Tokenomics and holder quality

`token-economics` считает circulating/max supply, FDV, emissions, burns, vesting, unlock calendar и sell-pressure. `token-holder-analysis` считает top-1/5/10/20, Gini, HHI и Nakamoto. `wallet-profiling`, `whale-tracking` и `sybil-detection` проверяют, являются ли крупные держатели инвесторами, ботами, пулами, bridge escrow или связанными кошельками.

### 5. Valuation

Минимальный набор:

- market cap / FDV;
- FDV / protocol revenue;
- FDV / fees;
- market cap / TVL;
- revenue growth и retention;
- NVT/MVRV только при проверенном source и понятной методике;
- peers на одинаковом определении revenue, fees и circulating supply.

Каждая оценка имеет bull/base/bear сценарий. Один агрегатор не является достаточным доказательством.

### 6. Risk and sizing

`historical-risk` показывает фактический volatility/drawdown. `forward-risk` строит стресс: -30/-50/-70% token price, TVL outflow, stablecoin depeg, oracle failure, bridge exploit, unlock shock и liquidity haircut. `asset-allocation`, `diversification` и `bet-sizing` переводят стресс в максимальную долю позиции.

### 7. Investment case

Финальный документ включает:

- Investment Thesis;
- Financial & Tokenomics Model;
- Risk Assessment;
- comparables и valuation range;
- catalyst calendar;
- Decision Card.

### 8. Финансово-консультационный слой

Перед рекомендацией `investment-policy` фиксирует IPS: цель, горизонт, обязательные расходы, risk capacity, risk willingness, ликвидность и запреты. `investment-suitability` проверяет актив и серию сделок на уровне всего портфеля. `proposal-generation` переводит результат в сравнение current vs proposed. `client-review-prep` готовит ежеквартальный пересмотр, `liquidity-management` отделяет резерв от инвестиций, `rebalancing` задаёт drift bands, а `finance-psychology` добавляет cooling-off и анти-herding правила.

Для текущего плана $1,000 в месяц базовая запись должна разделять **$300 ликвидного резерва** и **$700 инвестиционного потока**. Это временная рабочая гипотеза до заполнения фактических обязательных расходов и размера уже накопленной подушки; резерв не считается доходным активом или частью risk budget.

## Decision Card — обязательный финал

| Поле | Что фиксируем |
|---|---|
| Status | `buy/add`, `hold`, `trim`, `avoid`, `wait` |
| Confidence | high / medium / low с объяснением data gaps |
| Valuation range | bull / base / bear, дата и метод |
| Max position | доля капитала и отдельный risk budget |
| Main risk | один риск, который может уничтожить тезис |
| Thesis invalidation | наблюдаемое условие отмены |
| Next catalyst | событие и ожидаемый срок |
| Next review | дата следующей проверки |

## Quality gate перед публикацией

- source URL и дата обновления есть у каждой метрики;
- primary sources отделены от aggregators;
- contracts, wallets и pools проверены на правильной chain/network;
- raw и adjusted transfer value не смешаны;
- пользователи не равны числу адресов без retention/sybil check;
- fees, revenue, costs и token-holder value accrual reconciled;
- supply and unlock data cross-checked against contracts/docs;
- all charts have units, period, timezone and denominator;
- missing data marked `N/A`, never filled with invented values;
- report ends with Decision Card and explicit next review date.

## Подключённые skills

**On-chain core:** `digital-assets`, `defillama-api`, `coingecko-api`, `token-economics`, `token-holder-analysis`, `wallet-profiling`.

**Available on-chain extensions (подключаются под конкретный кейс):** `whale-tracking`, `sybil-detection`, `helius-api`, `birdeye-api`, `dexscreener-api`, `liquidity-analysis`, `mev-analysis`, `yield-analysis`, `impermanent-loss`.

**Investment core:** `ic-memo`, `thesis-tracker`, `historical-risk`, `forward-risk`, `performance-metrics`, `factor-investing`, `asset-allocation`, `diversification`, `bet-sizing`.

**Financial-advisor core:** `investment-policy`, `investment-suitability`, `proposal-generation`, `client-review-prep`, `liquidity-management`, `rebalancing`, `finance-psychology`.

Этот playbook описывает методику исследования, а не обещание доходности или персональную инвестиционную рекомендацию.
