# AVAIL — On-chain Intelligence Dashboard Specification

## Проект
`AVAIL On-chain Intelligence Dashboard`
Статус: спецификация / проектирование; наличие работающего live dashboard не подтверждено.

## 8 модулей
1. Market Overview.
2. Network Health.
3. Wallet Analytics.
4. Whale Tracking.
5. Staking Analytics.
6. Token Flows.
7. Tokenomics & Unlocks.
8. DEX & Investment Signals.

## Предлагаемая архитектура
Avail RPC / Node, Subscan, EVM explorers, market data, DEX
→ API / Python / Cloud Run / Cloud Scheduler
→ BigQuery raw / staging / core / marts
→ Looker Studio.

## Принципы качества данных
- Полная историческая загрузка native chain, если источник позволяет.
- Ежедневное обновление.
- Сравнения 24h / 7d / 30d.
- Разделять native AVAIL и EVM representations.
- Не удваивать bridged supply.
- NULL не приравнивать к нулю.
- Для каждой метрики хранить источник, timestamp и метод расчёта.

## Возможные страницы
Network health, wallets, whales, staking, token flows, tokenomics/unlocks, DEX, market overview.

## Следующие проверки
Подтвердить API coverage, pagination, historical depth, rate limits, chain identifiers, event definitions и доступность данных для воспроизводимых расчётов.
