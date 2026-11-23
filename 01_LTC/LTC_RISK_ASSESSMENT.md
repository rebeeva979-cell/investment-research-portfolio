# Litecoin (LTC) — Risk Assessment

**Дата:** 21 ноября 2026
**Режим:** `DEFENSIVE`
**Объект:** сетевой asset, а не equity с отчётностью и дивидендами

## 1. Сводная карта рисков

| Риск | Вероятность | Влияние | Ранний индикатор | Митигирование |
|---|---|---|---|---|
| Слабый спрос на платежи | высокая | высокое | active addresses/tx снижаются 2–4 недели | не усреднять только по цене; ждать activity confirmation |
| Subsidy dependence | высокая | высокое | fee share остаётся около 0.20% при снижении reward | мониторить fee/issuance и miner revenue |
| Gross transfer misread | высокая | среднее | transfer value растёт без user/fee growth | не называть gross output платежным оборотом |
| Mining economics | высокая | высокое | hash rate/difficulty падают, shutdown price растёт | отдельная cost model и sensitivity по LTC price |
| Конкуренция | средняя | высокое | LTC теряет share activity/fees относительно BTC/BCH/DOGE | сопоставимый peer panel |
| MWEB/наблюдаемость | средняя | среднее | расхождение provider metrics и фактической activity | явно указывать coverage и не считать addresses users |
| Рыночная волатильность | высокая | высокое | 30D annualized vol ~60%, drawdown от ATH ~−89% | position cap, no leverage, staged entry |
| Ликвидность/custody | средняя | высокое | widening spreads, exchange/custodian incident | проверка venue, лимиты, cold custody |
| Регуляторный риск | средняя | среднее/высокое | изменение правил доступа/листинга | диверсификация юрисдикций и инструментов |
| Data/licence risk | средняя | среднее | API changes, terms/rate limits | source register, cached extracts, reproducible scripts |

## 2. Риск денежной модели

Главный фундаментальный риск не в том, что supply ограничен. Ограниченный supply помогает только при наличии устойчивого спроса. Сейчас 92.68% supply уже добыто, но fee share мала, а 30D activity снижается. Значит, в текущей модели безопасность оплачивается прежде всего новой эмиссией, а не пользовательскими fees.

Проверяемая формула риска:

```text
security budget stress = reward reduction + LTC price decline + fee stagnation
```

Если halving уменьшает subsidy, цена LTC не компенсирует снижение, а fees не растут, часть майнеров может уйти. Hashrate в текущем срезе проходит gate, но это snapshot, не доказательство долгосрочной устойчивости.

## 3. Риск данных и методологии

### Что нельзя утверждать

- active addresses ≠ количество пользователей;
- transactions ≠ количество платежей;
- gross transfer value ≠ economic payment volume;
- miner revenue ≠ miner profit;
- MVRV < 1 ≠ гарантированная недооценённость;
- halving ≠ гарантированный рост цены.

### Что сделано правильно

- adjusted transfer value оставлен `NOT_AVAILABLE`, а не оценён произвольно;
- `miner_cost_usd` оставлен `N/A`, потому что затратная база не наблюдается;
- block timestamp в daily aggregate помечен как UTC day anchor, а не timestamp отдельного блока;
- 20 ноября market row не смешана с 19 ноября on-chain snapshot;
- источник, дата и методика сохраняются в workbook/source register.

## 4. Риск портфеля и suitability

LTC не должен финансироваться из emergency reserve и не должен использовать кредитное плечо. При временном лимите **до 3% ликвидного портфеля** позиция остаётся satellite allocation. При drawdown tolerance портфеля −50% даже небольшая crypto-доля может дать заметную абсолютную просадку, поэтому размер позиции определяется не привлекательностью графика, а допустимым вкладом в total portfolio loss.

Практическое правило:

```text
max LTC loss contribution = portfolio risk budget × LTC max weight
```

До свежей сверки балансов, custody и валюты резерва численный target/min/max портфеля не финализируется. Это отдельный suitability gate, а не недостаток LTC-метрики.

## 5. Сценарии ущерба

### Bear

Activity и fees снижаются, market regime остаётся risk-off, halving приближает stress майнеров. Возможна цена ниже $35 и дополнительный drawdown. Действие: `avoid/add не делать`, пересмотр только после data confirmation.

### Base

Hashrate сохраняется, activity стабилизируется, но fee economics не улучшается. Цена колеблется в диапазоне $35–65. Действие: `wait` или малый hold в пределах лимита.

### Bull

Activity и fee share растут, цена возвращается выше MA200, peers не показывают структурного отставания. Возможен диапазон $65–110. Действие: `add` только после прохождения нескольких gates, не по одному ценовому импульсу.

## 6. Decision Card

| Поле | Решение |
|---|---|
| Статус | `wait` |
| Уверенность | `medium` в рисковой диагностике |
| Диапазон оценки | $25–35 bear / $35–65 base / $65–110 bull; сценарии, не target |
| Максимальная доля | 3% ликвидного портфеля; без leverage |
| Главный риск | спрос и fee economics могут не успеть компенсировать subsidy dependence |
| Условие отмены тезиса | ухудшение security + activity, потеря источников данных или невозможность подтвердить экономический спрос |
| Ближайший катализатор | on-chain snapshot 20.11 и обновлённый peer panel |
| Следующий пересмотр | через 7 дней или раньше при halving/security event |

## 7. Что нужно проверить до `hold/add`

1. Получить/подтвердить 20.11 on-chain snapshot, не смешивая его с market-only row.
2. Построить UTXO-adjusted transfer value с документированными правилами change/self-transfer.
3. Собрать miner cost sensitivity по ASIC efficiency, electricity price и LTC price.
4. Сравнить fee share, activity, inflation и valuation peers на одной дате.
5. Проверить custody/venue и персональный лимит позиции в IPS.
