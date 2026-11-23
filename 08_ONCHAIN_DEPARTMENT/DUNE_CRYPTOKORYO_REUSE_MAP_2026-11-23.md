# Dune / Cryptokoryo: карта повторного использования для Investment Research

**Дата аудита:** 23 ноября 2026 года
**Объект:** публичный профиль [@cryptokoryo на Dune](https://dune.com/cryptokoryo)
**Цель:** не копировать чужие выводы, а выбрать проверяемые паттерны метрик для собственных кейсов.

## Ограничение аудита

Dune-страницы в текущем окружении отдают каталог и названия публичных дашбордов, но не раскрывают JS-таблицы и SQL без запуска самого Dune. Поэтому ниже фиксируется **карта покрытия**, а не подтверждение текущих чисел. Любая цифра из Dune должна перед публикацией получить: URL конкретного query/dashboard, дату и время обновления, блок или период, экспорт результата и независимую проверку первоисточником.

Профиль показывает, среди прочего, `Narratives Tokens Breakdown`, `History of Airdrops`, `LRT Restaking`, `Wallet Profiler`, `Narratives Social Trends`, `Ethereum Staking`, `Uniswap v3 Pools`, `Pendle`, `Ecosystems` и `Best GMX Traders`. [Каталог профиля](https://dune.com/discover/content/relevant?q=author%3Acryptokoryo&resource-type=dashboards)

## Что берём в нашу систему

| Публичный паттерн | Наше применение | Метрики, которые добавляем | Приоритет |
|---|---|---|---|
| LRT Restaking | ETHFI: экономика Ether.fi и сравнение LRT | TVL по продукту, чистые депозиты/выводы, число депозиторов, доля крупных адресов, доходность базового ETH и протокольная комиссия | P0 |
| Ethereum Staking (LSD) | ETHFI: конкурентный benchmark | TVL/доля Lido, Coinbase, Kraken и Ether.fi; net flows; концентрация операторов; ликвидность LST/LRT | P0 |
| History of Airdrops | ETHFI и будущие листинги | eligible/claimed/unclaimed, claim velocity, sell-pressure window, адреса-аккумуляторы после claim | P0 |
| Wallet Profiler | Forensic слой для ETHFI, SNX, AVAIL, HNT | cohort PnL, realised/unrealised PnL, входы на CEX/DEX, treasury/market-maker labels, retention после события | P0 |
| Narratives Tokens Breakdown | Scout и weekly idea intake | распределение токенов по narrative, market-cap/volume breadth, лидерство и ротация секторов | P1 |
| Narratives Social Trends | Catalyst tracker | изменение mindshare, число уникальных авторов, скорость появления narrative; использовать только как lead | P1 |
| Uniswap v3 Pools | UNI/DEX и liquidity-risk модуль | volume, fees, TVL, fee/TVL, активные LP, глубина ±1%/±2%, price impact и концентрация liquidity | P1 |
| Ecosystems | макро-карта сетей | активные пользователи, fees, stablecoin supply, bridge netflow, DEX volume по chain | P1 |
| Best GMX Traders | только отдельный wallet-PnL эксперимент | доходность после комиссий, turnover, drawdown, survivorship bias; не использовать как готовый сигнал | P2 |

## Как это превращается в инвестиционное решение

1. **Scout:** narrative или social-trend создаёт lead, но не рекомендацию.
2. **Forensic:** адреса и потоки подтверждают, что рост не нарисован wash-trading, sybil-активностью или одним маркет-мейкером.
3. **Tokenomics:** claim/unlock/supply bridge переводит поток в будущую dilution и давление предложения.
4. **Economics:** TVL связывается с fees, revenue, expenses и value accrual токена.
5. **Liquidity:** рассчитывается допустимый размер позиции и стоимость выхода.
6. **Decision Card:** только после этого появляется `buy/add`, `hold`, `trim`, `avoid` или `wait` с размером, отменой тезиса и датой пересмотра.

## Что нельзя переносить автоматически

- число просмотров, место в каталоге или тег не являются доказательством качества идеи;
- social/mindshare не равен выручке и может быть легко инцентивирован;
- TVL без net flows, доходности и расходов не показывает экономику протокола;
- PnL отдельных кошельков содержит survivorship bias и не учитывает закрытые/неразмеченные адреса;
- airdrop claim не равен удержанию токена: нужен cohort-анализ через 7/30/90 дней;
- Dune-таблица не заменяет официальный контракт, отчёт эмитента, Safe API или SEC filing.

## Правило источника и воспроизводимости

Для каждого нового показателя в evidence ledger записываем:

```text
metric | query/dashboard URL | Dune query ID | extracted_at_utc | period/block
definition | SQL hash/commit | primary-source cross-check | status
```

Статусы: `verified` — совпадает с первичным источником; `inferred` — расчёт из опубликованных полей; `lead` — сигнал для дальнейшей проверки. В публичный отчёт попадают только `verified` и явно обозначенные `inferred`.

## Практический backlog

1. Собрать ETHFI LRT benchmark из собственных RPC/DefiLlama и сопоставить с Dune только на уровне агрегатов.
2. Добавить `wallet_cohort_pnl`, `claim_rate_7d/30d/90d` и `netflow_by_label` в on-chain schema.
3. Сделать для UNI отдельный liquidity worksheet: fee/TVL, active LP, depth и slippage.
4. Подключить narrative/social блок к Scout как источник лидов, без автоматической покупки.
5. Перед публикацией каждой метрики сохранять raw export и дату обновления; при отсутствии экспорта оставлять статус `lead`.

## Ссылки на публичные примеры

- [Narratives Tokens Breakdown](https://dune.com/cryptokoryo/btc-pairs)
- [History of Airdrops](https://dune.com/cryptokoryo/history-of-airdrops)
- [LRT Restaking](https://dune.com/cryptokoryo/lrt-restaking)
- [Wallet Profiler](https://dune.com/cryptokoryo/wallet-profiler)
- [Narratives Social Trends](https://dune.com/cryptokoryo/farcaster-trends)
- [Ethereum Staking](https://dune.com/cryptokoryo/ethstaking)
- [Uniswap v3 Pools](https://dune.com/cryptokoryo/uniswap)
