# SNX SIP-423 — verification update

**Дата проверки:** 21 ноября 2026
**Статус:** `defensive / research`
**Назначение:** уточнить timeline и отделить официальные условия SIP от фактического движения токенов

## 1. Новое подтверждение из официальных материалов

Официальный SIP-423 по-прежнему помечает receipt-contract как **`CONTRACT BUILD DEFERRED`**, а `Claims contract deployment` — как **TBC**. В SIP указаны snapshot blocks 25,473,065 на Ethereum и 153,868,527 на Optimism, conversion ratio 4 SNX за 1 sUSD entitlement и maximum mint 236,464,356 SNX.

Официальный [Synthetix sUSD Retirement Dashboard](https://susd.synthetix.io/) показывает timeline:

- snapshot / freeze: **26 июня 2026**;
- lock ends: **26 июня 2027**;
- vesting ends: **26 июня 2028**;
- текущий прогресс vesting в dashboard: **0%**.

Это важное уточнение к предыдущему отчёту: **6 июля 2026** — дата фактического mint/перевода SNX в Safe, а не обязательно дата snapshot или начала lock. В будущих материалах эти события нужно показывать раздельно.

## 2. Что подтверждено, а что нет

| Вопрос | Результат | Статус |
|---|---|---|
| Maximum mint | 236,464,356 SNX | `verified` через SIP-423 |
| Receipt contract | в официальном SIP — `CONTRACT BUILD DEFERRED`; deployment TBC | `open / not observed` |
| Snapshot blocks | 25,473,065 Ethereum; 153,868,527 Optimism | `verified` через SIP-423 |
| Lock/vest timeline | 26.06.2026 → 26.06.2027 → 26.06.2028 | `verified` через official dashboard |
| Safe balance/outflows | 236.46M SNX и 0 исходящих на срез 19.11 | `point-in-time verified` в текущем пакете |
| Safe owners/threshold | не подтверждены в этом проходе | `open` |
| Modules/guards | не подтверждены в этом проходе | `open` |
| Unclaimed expiry | SIP одновременно указывает 6 месяцев и `TBD` treatment | `open / conflicting` |

## 3. Почему Safe governance остаётся риском

Safe — multisig-контракт, а не trustless vesting contract. Для оценки custody нужно знать текущих owners, threshold и modules/guards. Даже если исходящих переводов нет, отсутствие outflow на дату не доказывает невозможность будущего перевода.

Проверяемая модель риска:

```text
effective lock = Safe owner policy + threshold + modules/guards + governance process
```

Пока owners/threshold не подтверждены через RPC или официальный Safe Transaction Service, lock остаётся policy commitment, а не криптографической гарантией vesting.

## 4. Влияние на Decision Card

- **Статус:** `defensive / research`
- **Уверенность:** высокая в факте mint и официальном timeline; низкая в enforceability custody до проверки Safe config
- **Максимальная доля:** 0% сейчас; до 0.5% только после закрытия Safe verification и подтверждения unlock mechanics
- **Главный риск:** 40.67% post-mint supply сосредоточено в Safe, который не является vesting contract
- **Условие отмены:** receipt contract не появляется, expiry остаётся неопределённым, либо Safe config позволяет недостаточно контролируемый outflow
- **Ближайший катализатор:** deployment/seeding receipt contract и публикация Safe configuration
- **Следующий пересмотр:** после подтверждения owners/threshold или не позднее 28.11.2026

## 5. Что осталось сделать

1. Получить `getOwners()`, `getThreshold()`, modules и guards Safe `0x3265ff13f29fe2dd7501c608b914bfa5e1ffcf6d` через проверяемый Ethereum RPC/explorer.
2. Проверить официальный Safe Transaction Service на configuration changes и queued/executed transactions.
3. Проверить receipt contract deployment по адресу из официального Synthetix announcement/SIP update, а не по сторонним публикациям.
4. Обновить timeline в HTML/PDF/data pack, разделив snapshot, mint transfer и lock start.
