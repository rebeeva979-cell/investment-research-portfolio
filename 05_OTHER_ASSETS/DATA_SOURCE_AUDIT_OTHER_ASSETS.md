# Data Source Audit — Other Research Assets

Это рабочий аудит источников и методик; перед публикацией требуется актуальная проверка API, покрытий, лицензий и контрактов.

## EGLD — MultiversX
- Официальные MultiversX REST API / Explorer / Elastic Indexer.
- Проверить глубину истории, пагинацию, rate limits, события staking, token supply и экосистемные данные.
- Фокус: сеть, staking, tokenomics, ecosystem.

## ZNTL — Zentalis Therapeutics
- SEC EDGAR / XBRL, company IR, clinical trial registries, FDA.
- Это equity research, не on-chain analytics.
- Анализировать cash runway, burn rate, pipeline, clinical/regulatory risk, dilution и финансовую отчётность.
- Финансовые цифры из старых заметок не переносить без обновления по последнему filing.

## GPRO — GoPro
- SEC EDGAR 10-Q/10-K/8-K и merger exhibit — revenue, camera units, subscriptions, cash, debt, waivers, merger consideration и post-merger ownership.
- Основной риск источника: transaction headline может не совпасть с closing price из-за условий, net working capital и financing/covenant waivers.
- Для ownership использовать SEC 13D/13G/13F; агрегаторы — только как вспомогательный экран.

## LYFT — Lyft
- Investor Relations / SEC 10-K, 10-Q, 8-K, proxy и Schedule 13G/A — rides, active riders, gross bookings, revenue, adjusted EBITDA, FCF, SBC, shares и holders.
- EV/Sales, EV/Adjusted EBITDA и FCF yield считать на одной дате; GAAP net income отдельно от non-GAAP adjusted EBITDA.
- Не использовать P/E без проверки разовых налоговых эффектов и reconciliation.

## ZRX — 0x Protocol
- Ethereum contract logs, официальные 0x API / docs, governance sources.
- Проверить актуальную utility токена и исторические/текущие staking механизмы по контрактам и governance.

## COMP — Compound
- Compound v2/v3 contract events, официальная документация, DefiLlama.
- Разделять TVL, fees, protocol revenue, supplier/borrower economics и governance.
- Не считать TVL или LP/supplier flows выручкой протокола.

## UNI — Uniswap
- Subgraphs / contract events, официальные docs, DefiLlama.
- Разделять v2/v3/v4; LP fees не равны protocol revenue.
- Fee switch / burn / value-accrual mechanisms проверять по версиям пулов и governance решениям.

## ROSE — Oasis Network
- Oasis Nexus / Explorer / официальные API.
- Разделять consensus layer и ParaTimes; отдельно учитывать bridged representations.
- Фокус: staking, network activity, tokenomics, privacy infrastructure.

## LRC — Loopring
- Loopring API / Explorer и Ethereum contracts.
- Разделять L1 и L2 активность; проверить историческое покрытие API и определения метрик.

## SNX — Synthetix
- SIP-423 / SIP-424, Ethereum и Optimism events.
- Различать максимальный разрешённый mint и фактический mint; проверять recipient behaviour, lock и vesting.

## Общие требования к источникам
Для каждой метрики фиксировать endpoint / contract, coverage start/end, update frequency, timezone, unit, licensing terms, limitations и retrieval timestamp.
