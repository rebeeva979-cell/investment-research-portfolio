# AVAIL — план полноценного investment research

**Статус:** `research / first snapshot complete / no decision`
**Дата старта:** 22 ноября 2026
**Почему берём:** AVAIL уже есть в портфеле и имеет готовую спецификацию dashboard, но пока нет подтверждённой live-базы, supply reconciliation и investment memo.

Первый read 22.11.2026 уже подтверждает mainnet RPC, official circulating supply и market snapshot. Следующий пробел — исторический 30-дневный DA usage/fees/staking ряд и on-chain сверка unlock/treasury flows.

## 1. Инвестиционный вопрос

Создаёт ли Avail устойчивый спрос на data availability, который превращается в fees, staking demand и ценность AVAIL, или токен в основном оценивается по narrative, грантам и будущей эмиссии?

## 2. Что нужно доказать

### Product / adoption

- сколько rollups/appchains публикуют данные через Avail;
- сколько data blobs/bytes posted по дням;
- число namespaces, пользователей и активных отправителей;
- растут ли объём и платные операции без incentives;
- кто конкурирует: Celestia, EigenDA, Near DA и другие DA-решения.

### Network health

- число валидаторов и номинальный/активный stake;
- концентрация stake у крупнейших операторов;
- uptime, block production, finality и ошибки RPC;
- участие в data availability sampling и параметры безопасности;
- доля bridged/EVM activity против native chain activity.

### Economics

- fees в AVAIL и USD;
- формула комиссии за bytes/blob/namespace;
- кто получает fees: validators, treasury, burns или другой участник;
- staking rewards, inflation и real staking yield;
- расходы/субсидии, если они публично раскрываются.

### Tokenomics

- on-chain `total_supply` и отдельно подтверждённый `circulating_supply`;
- initial allocation: investors, team, ecosystem, community, foundation;
- vesting и unlocks по датам и кошелькам;
- эмиссия staking rewards и изменение supply;
- bridge-монеты и EVM representations без двойного счёта.

### Market / flows

- market cap и FDV на одинаковой supply-базе;
- ликвидность AVAIL/USDT, AVAIL/USDC и AVAIL/ETH;
- CEX/DEX depth и slippage для $10k/$50k/$250k;
- притоки на биржи из treasury/vesting-кошельков;
- концентрация top-10/top-50 holders и доля контрактов/бриджей.

## 3. Методология и почему именно так

1. **Native chain отдельно от EVM.** Иначе bridged AVAIL можно посчитать дважды.
2. **NULL не считать нулём.** Отсутствие данных о fees или holders — это `N/A`, а не доказательство отсутствия активности.
3. **Supply сверять через несколько источников.** Aggregator circulating supply может включать locked или bridged токены.
4. **Fees отделять от revenue.** Комиссия сети не равна доходу держателя AVAIL.
5. **Staking APR корректировать на inflation.** Номинальная награда не равна реальной доходности токена.
6. **Потоки читать вместе с unlocks.** Перевод токенов на CEX может быть treasury operation, а не немедленной продажей.
7. **DA usage измерять bytes и платными событиями.** Число транзакций без размера данных плохо описывает спрос на data availability.

## 4. План данных

| Слой | Поля | Предпочтительный источник | Статус |
|---|---|---|---|
| Market | price, volume, mcap, FDV | CoinGecko/CMC + DEX Screener | `pending` |
| Native chain | blocks, extrinsics, blobs, bytes, fees | Avail RPC / Subscan | `pending` |
| Validators | validator set, stake, rewards, commission | Avail staking endpoints / explorer | `pending` |
| Holders | top holders, transfers, exchange labels | explorer + token contract data | `pending` |
| Tokenomics | allocations, unlocks, emission | official docs/tokenomics + dated schedule | `pending` |
| Liquidity | pools, depth, slippage | DEX Screener + pool RPC/quoter | `pending` |
| Macro | BTC/ETH, DXY, ETF flows, USDT supply | separate Macro & ETF dashboard | `pending` |

## 5. Dashboard pages

1. **Market Overview** — price, returns, volatility, drawdown, mcap/FDV and peer set.
2. **Network Health** — blocks, finality, validators, stake, uptime and sampling indicators.
3. **DA Usage** — blobs, bytes, namespaces, active senders, paid operations and 7/30-day changes.
4. **Wallets & Whales** — holders, concentration, exchange/treasury/bridge labels and large transfers.
5. **Staking** — staked share, nominal rewards, inflation-adjusted yield and validator concentration.
6. **Token Flows** — unlock wallets, bridge flows, CEX deposits/withdrawals and net pressure.
7. **Tokenomics & Unlocks** — supply bridge, vesting calendar, future emissions and float scenarios.
8. **Valuation & Decision** — fees/usage multiples, peer comparison, scenarios, risk triggers and Decision Card.

## 6. Initial Decision Card

До сбора и сверки данных нельзя ставить `buy`, `hold` или `avoid`.

| Поле | Начальное значение |
|---|---|
| Status | `research` |
| Confidence | `low` — live data not verified |
| Valuation range | `N/A` |
| Max position | не устанавливать по этому исследованию |
| Main risk | unlock/supply pressure при недостаточном платном DA demand |
| Thesis invalidation | не применять до появления baseline |
| Next catalyst | первый полный native-chain snapshot и проверка tokenomics |
| Next review date | после первого data pack, затем еженедельно |

## 7. Рабочий порядок

### Этап 1 — 1 день

- подтвердить chain ID, RPC и историческую глубину;
- получить один live block и один historical block;
- найти определения blob/namespace/fee events;
- проверить pagination и rate limits;
- зафиксировать адреса native token, bridge и staking pallets.

### Этап 2 — 2–3 дня

- собрать native-chain daily table;
- отдельно собрать market и supply snapshots;
- загрузить официальную tokenomics/unlock schedule;
- составить source register и verification log;
- проверить, что bridged supply не удваивается.

### Этап 3 — 4–7 дней

- построить dashboard v0;
- посчитать fees/usage/staking/unlock metrics;
- сравнить с Celestia/EigenDA/NEAR DA;
- подготовить bear/base/bull сценарии;
- написать investment memo и Decision Card.

## 8. Критерии перехода к инвестиционному выводу

AVAIL может перейти из `research` в `watchlist`, только если:

- supply и unlocks сверены минимум по двум источникам;
- есть исторический ряд платного DA usage;
- понятно, кому достаются fees;
- staking rewards и inflation reconciled;
- wallet/bridge/CEX flows имеют проверяемую атрибуцию;
- ликвидность и максимальная доля позиции рассчитаны.

Переход в `buy/add` возможен только после доказательства роста usage и value accrual, а не только после снижения цены или приближения unlock.

## 9. Ожидаемые результаты

- `AVAIL_DAILY.csv`;
- `AVAIL_TOKENOMICS.csv`;
- `AVAIL_UNLOCKS.csv`;
- `AVAIL_HOLDERS.csv`;
- `AVAIL_SOURCE_REGISTER.csv`;
- SQL/Python pipeline;
- dashboard HTML/Looker starter;
- `AVAIL_INVESTMENT_THESIS.md`;
- `AVAIL_RISK_ASSESSMENT.md`;
- weekly update и Decision Card.
