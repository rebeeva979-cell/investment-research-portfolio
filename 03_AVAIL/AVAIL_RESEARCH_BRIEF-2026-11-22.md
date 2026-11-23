# AVAIL — research brief (starter)

**Состояние:** `research / no decision`
**Дата:** 22 ноября 2026
**Источник текущей версии:** официальная страница AVAIL, официальный circulating-supply API, официальный docs и read-only RPC; market snapshot — CoinGecko. Полный 30-дневный usage-ряды ещё не собраны.

## Первый проверенный snapshot — 22 ноября 2026

| Показатель | Значение | Статус |
|---|---:|---|
| Chain | `Avail DA Mainnet` | RPC read |
| Latest header | `3 759 520` | RPC read |
| RPC peers | `30` | RPC read |
| `isSyncing` | `false` | RPC read |
| Official circulating supply | `4 114 494 609 AVAIL` | официальный API |
| Official total supply | `10 000 000 000 AVAIL` | официальная token page |
| Circulating / official total | `41.14%` | расчёт |
| Price | `$0.00143054` | CoinGecko snapshot, 17:28 UTC |
| Market cap | `$5.88M` | CoinGecko snapshot |
| FDV at 10B supply | `$14.31M` | расчёт |
| FDV / reported market cap | `2.43x` | расчёт, не fully diluted valuation model |

RPC snapshot подтверждает доступность mainnet на момент чтения, но не доказывает платный спрос на DA.

## Что заявлено официально, но ещё требует on-chain сверки

Официальная token page сообщает около **3.2M финализированных блоков, 4.5B AVAIL в staking, 80 активных валидаторов и 10+ подключённых сетей**. Это useful context, но в первом read эти counters не были получены из отдельного исторического API и пока считаются `reported`, а не полностью reconciled.

Проект описывает AVAIL как токен для staking, governance и оплаты network services. В token model указано, что использование сети оплачивается AVAIL либо через конвертацию/байбек; блог проекта также описывает buyback из Nexus revenue. Это **policy/product claim**, который нужно подтвердить транзакциями, fee events и treasury wallets.

## Риск сети, уже подтверждённый первичным источником

В официальном incident report зафиксировано, что 31 августа 2026 года mainnet остановил block production примерно на 4 часа, а finality задержалась ещё примерно на 12 часов после faulty emergency runtime upgrade. Во время восстановления были проблемы с validator set и bridge; инцидент был mitigated 1 сентября 2026 года.

Это не означает, что сеть сейчас неработоспособна. Но в risk model нужно отдельно учитывать:

- emergency upgrade process;
- validator coordination и slashing cascade;
- finality/bridge downtime;
- зависимость безопасности от фактического stake и внешних операторов.

## Исследовательский вопрос

Есть ли у Avail измеримый платный спрос на data availability и такой механизм value accrual, который оправдывает текущую оценку AVAIL после учёта эмиссии, unlocks, bridge-рискa и конкуренции?

## Предварительная гипотеза

AVAIL может быть интересен как инфраструктурный актив, если рост rollup/appchain usage приводит к росту bytes/blobs и комиссий, а токен нужен для staking, security или оплаты данных. Первый snapshot показывает низкую reported market cap, но это **не доказательство дешёвой оценки**: при 41.14% circulating будущая эмиссия остаётся главным фактором риска. Гипотеза не подтверждена, пока не разделены:

- narrative и реально оплаченные DA-операции;
- native AVAIL и bridged/EVM representations;
- staking APR и доходность после inflation;
- total supply, circulating supply и будущие unlocks;
- network fees и доход держателя токена.

## Что нужно получить до valuation

| Блок | Минимальный результат |
|---|---|
| Usage | ежедневные blobs/bytes, namespaces, активные отправители, paid operations |
| Network | validators, stake, finality, uptime, sampling/security indicators |
| Fees | native fees, USD conversion, recipients и burn/treasury rule |
| Supply | total/circulating/locked, allocation и unlock calendar |
| Flows | bridge/CEX/treasury transfers и top-holder concentration |
| Market | mcap/FDV на одной supply-базе, DEX depth и slippage |
| Peers | Celestia, EigenDA, NEAR DA: usage, fees, token mechanics |

## Что будет считаться сильным подтверждением

1. Bytes и платные операции растут 30/90 дней без пропорционального роста incentives.
2. Fees можно воспроизвести по событиям и понять, кому они достаются.
3. Supply/unlocks сверены по официальной tokenomics и on-chain балансу.
4. Staking demand и security не зависят от одного крупного оператора.
5. Valuation не держится только на FDV и narrative «modular blockchain».

## Главные риски

- слабый реальный спрос при большой будущей эмиссии;
- концентрация валидаторов или treasury;
- двойной счёт native и bridged supply;
- конкуренция DA-провайдеров и падение unit price за bytes;
- bridge, RPC и smart-contract риски;
- высокая волатильность и недостаточная глубина рынка.

## Начальная Decision Card

| Поле | Значение |
|---|---|
| Status | `research` |
| Confidence | `low` |
| Valuation range | `N/A` |
| Max position | не устанавливается до live verification |
| Main risk | unlock/supply pressure при неподтверждённом платном спросе |
| Invalidation | будет определена после baseline, сейчас не применяется |
| Next catalyst | первый полный native-chain и tokenomics snapshot |
| Next review | после сборки data pack |

## Следующий технический шаг

Проверить RPC/эксплорер и собрать минимальный 30-дневный ряд: дата, block height, blobs/bytes, paid operations, fees, validators, stake, native supply и market price. Затем обновить brief фактическими числами и только после этого строить valuation-сценарии.
