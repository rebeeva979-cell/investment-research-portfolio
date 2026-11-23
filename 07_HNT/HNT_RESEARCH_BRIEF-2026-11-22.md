# HNT (Helium) — инвестиционный brief

Дата среза: 22 ноября 2026 года
Статус исследования: `research / first snapshot`
Инвестиционный статус: **`wait`**
Уверенность: **средняя-низкая** — продуктовая активность выглядит реальной, но эмиссионный и governance-риск пока нельзя корректно смоделировать без on-chain ряда.

## 1. Что покупается

Helium — сеть carrier offload и IoT connectivity. Пользовательские платежи проходят через Data Credits: один DC привязан к $0.00001, DC создаются через burn HNT и не являются свободно торгуемым токеном. HNT одновременно используется как reward-токен для операторов, governance/veHNT и источник DC.

Это не акция телеком-компании: у держателя HNT нет права на денежный поток Nova Labs или на долю в выручке операторов. Связь с экономикой сети проходит через burn/mint, emissions и спрос на DC.

## 2. Первый снимок рынка и сети

| Метрика | Значение | Качество данных |
|---|---:|---|
| Цена HNT | ~$0.2217 | CoinGecko, динамический snapshot |
| Market cap | ~$45.15M | CoinGecko, динамический snapshot |
| Total supply on Solana | 203.626M HNT | Solana RPC, проверено на slot 472,646,415 |
| Официальный максимум по старой модели | ~223M HNT | Helium Docs; не использовать как единственный FDV |
| Эффективный потолок при полном HIP‑149 | ~347M HNT | текст одобренного HIP, deployment ещё нужно проверить |
| Официальный usage snapshot | 1M+ users/day; 49 TB+/day; 40k+ access points | заявленные Helium counters |
| Исторический ориентир usage | ~3.4M daily users и ~128 TB/day в Q1/May 2026 | официальная страница, даты показателей различаются |

Расчёты:

- FDV по старому потолку 223M: примерно **$49.4M**;
- supply при полном HIP‑149: примерно **$76.9M** по текущей цене;
- текущие 203.6M составляют около **58.7%** от потенциального потолка 347M;
- дополнительный supplement 141M равен примерно **69%** текущего on-chain supply.

Это не означает, что 347M уже выпущены: это сценарий, зависящий от фактического запуска HIP‑149.

## 3. Реальная экономика: что можно посчитать уже сейчас

Helium указывает цену Mobile data transfer $0.10 за GB. Если весь официальный snapshot 49 TB/day трактовать как billable traffic по этой ставке, получается грубая верхняя оценка:

- $4,900 paid usage в день;
- около $1.79M annualized gross network usage;
- около 8.07M HNT burn в год при цене HNT $0.2217.

Это **не выручка держателя HNT и не чистая прибыль протокола**. Это ориентир gross paid usage при сильном допущении, что весь опубликованный объём подтверждён и тарифицируется одинаково. При таком допущении annualized burn равен примерно 4.0% текущей market cap.

Ключевое сравнение: HIP‑149 предусматривает около 196k HNT/day supplement в первый год — примерно 71.5M HNT в год. При текущей цене это около $15.9M номинальной эмиссии в год, или почти в 9 раз больше грубого 49 TB/day burn в HNT-единицах. Поэтому рост трафика должен проверяться одновременно с burn и mint, а не отдельно.

## 4. Что является бычьим тезисом

1. Есть физическая услуга — carrier offload, а не только спекулятивный DeFi use case.
2. DC привязывают usage к доллару, поэтому клиенту не нужно принимать HNT-волатильность.
3. В официальном snapshot видны carrier-scale counters: десятки тысяч access points и десятки TB daily traffic.
4. Если paid traffic растёт быстрее выпуска, burn может поддерживать HNT через BME-механику.
5. Открытый Iceberg catalog позволяет воспроизводимо проверить sessions, burned sessions, rewardable bytes и rewards без приватного API-ключа.

## 5. Что ломает тезис

1. **HIP‑149 dilution.** Одобренный supplement на 141M HNT способен существенно превысить текущий burn, особенно в первые 12 месяцев.
2. **Маркетинговые counters ≠ cash flow.** Users и TB нужно сверить с billed/verified sessions и количеством DC, иначе нельзя оценивать unit economics.
3. **Carrier concentration.** Один-два крупных плательщика могут давать большую часть трафика; потеря контракта резко снизит burn.
4. **Governance/execution.** HIP‑149 объединяет изменение reward rules, retirement PoC, operations supplement и advisory council в один upgrade; задержка или неполное внедрение меняют модель.
5. **Модель rewards.** Вознаграждение операторам и service-provider allocation могут создавать постоянное давление продаж даже при росте usage.
6. **Нет equity claim.** Держатель HNT не получает право на выручку Nova Labs, carrier contracts или резервы компании.
7. **Технический/контрактный риск.** HNT после миграции живёт на Solana; нужно мониторить mint authority, reward programs, bridge/oracle и фактические vault outflows.

## 6. Сценарная оценка (рабочая, не price target)

| Сценарий | Условие | Рабочий диапазон HNT |
|---|---|---:|
| Bear | HIP‑149 supplement запускается, burn не растёт, carrier concentration высокая | $0.08–0.15 |
| Base | traffic/burn растут, но supplement реализуется и съедает большую часть network value | $0.18–0.35 |
| Bull | paid traffic растёт кратно, burn стабильно превышает net issuance, supplement ограничен/контролируем | $0.50–0.80 |

Диапазоны нужны для проверки чувствительности модели, а не для обещания доходности. Их надо заменить на supply-and-burn model после 30/90-дневного ряда.

## 7. Инвестиционное решение

- **Статус:** `wait`.
- **Уверенность:** средняя-низкая.
- **Рабочий диапазон:** $0.08–0.80 по сценариям; текущая цена около $0.2217 находится внутри диапазона и сама по себе ничего не решает.
- **Максимальная доля:** до 1% крипто-части только как венчурная позиция после проверки HIP‑149 и burn/mint; до этого — 0% новых покупок.
- **Главный риск:** одобренная эмиссия 141M HNT при недостаточном burn.
- **Отмена тезиса:** 30–90 дней показывают падение paid traffic/DC burn либо supplement mint идёт быстрее, чем рост подтверждённого burn.
- **Ближайший катализатор:** on-chain запуск или задержка HIP‑149, публикация vault address и первый полный burn/mint reconciliation.
- **Дата следующего пересмотра:** 29 ноября 2026 года или раньше при появлении данных о deployment.

## 8. Что добавить в дашборд

1. Daily paid GB, verified GB и DC burn отдельно по Mobile/IoT.
2. HNT burned, HNT minted, net issuance и burn/mint ratio.
3. Reward buckets: deployers, service provider, veHNT, operations supplement.
4. Active access points, unique users, carrier mix и retention — только с датой и источником.
5. HIP‑149 tracker: status, deployment slot, vault balance, daily inflow/outflow, cumulative supplement.
6. Supply bridge и sensitivity: usage growth × HNT price × reward/emission regime.

## Источники

- Helium Docs: HNT token economics и emission schedule.
- Helium Docs: Data Credits и Mobile pricing.
- Helium official network snapshot.
- Helium public Mobile Iceberg catalog and schema.
- Solana public RPC `getTokenSupply` for HNT mint.
- CoinGecko market snapshot.
- HIP‑149: Helium Utility and Emissions Realignment.
