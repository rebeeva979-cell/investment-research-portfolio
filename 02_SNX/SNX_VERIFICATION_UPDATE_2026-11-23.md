# SNX SIP-423 — verification update

**Дата проверки:** 23 ноября 2026
**Статус:** `defensive / research`
**Назначение:** уточнить timeline и отделить официальные условия SIP от фактического движения токенов

## 0. Результат нового Safe-прохода

Проверены Ethereum RPC и официальный Safe Transaction Service для Safe `0x3265fF13F29Fe2DD7501C608b914bfA5E1fFcf6d`.

- **owners:** 5 адресов;
- **threshold:** 3 из 5;
- **version:** Safe 1.4.1;
- **modules:** пустой список;
- **guard:** zero address;
- **module guard:** zero address;
- **creation:** 6 июля 2026, block/tx зафиксированы Safe API;
- **Safe executions:** 2 операции всего на момент запроса;
- **SNX outflow:** не найден.

Safe API показывает две операции: вход **236,464,356 SNX** от `0xc1C332...` 6 июля 2026 (block 25,473,284, tx `0xda4c600d...`) и отдельный вход 1 CAT-токена 18 июля 2026. Последняя операция не относится к SNX и не меняет supply analysis.

Источники снимка: [Safe API](https://safe-transaction-mainnet.safe.global/api/v1/safes/0x3265fF13F29Fe2DD7501C608b914bfA5E1fFcf6d/), [Safe creation](https://safe-transaction-mainnet.safe.global/api/v1/safes/0x3265fF13F29Fe2DD7501C608b914bfA5E1fFcf6d/creation/), [Safe all-transactions](https://safe-transaction-mainnet.safe.global/api/v1/safes/0x3265fF13F29Fe2DD7501C608b914bfA5E1fFcf6d/all-transactions/?limit=20), Ethereum RPC `eth_call` на latest block.

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
| Safe owners/threshold | 5 owners, threshold 3 | `verified` через Safe API + RPC |
| Modules/guards | modules `[]`, guard и module guard — zero address | `verified` через Safe API |
| Unclaimed expiry | SIP одновременно указывает 6 месяцев и `TBD` treatment | `open / conflicting` |

## 3. Почему Safe governance остаётся риском

Safe — multisig-контракт, а не trustless vesting contract. Теперь конфигурация известна: 3-of-5, без modules и guard. Это снижает неопределённость операционного контроля, но не превращает Safe в vesting contract: три владельца всё ещё могут подписать исходящую операцию до окончания policy lock.

Проверяемая модель риска:

```text
effective lock = Safe owner policy + threshold + modules/guards + governance process
```

Owners/threshold теперь подтверждены через RPC и официальный Safe Transaction Service, но lock всё равно остаётся policy commitment, а не криптографической гарантией vesting.

## 4. Влияние на Decision Card

- **Статус:** `defensive / research`
- **Уверенность:** высокая в факте mint, Safe config и официальном timeline; средняя в enforceability custody, поскольку Safe не является vesting contract
- **Максимальная доля:** 0% сейчас; до 0.5% только после закрытия Safe verification и подтверждения unlock mechanics
- **Главный риск:** 40.67% post-mint supply сосредоточено в Safe, который не является vesting contract
- **Условие отмены:** receipt contract не появляется, expiry остаётся неопределённым, либо Safe config позволяет недостаточно контролируемый outflow
- **Ближайший катализатор:** deployment/seeding receipt contract и публикация Safe configuration
- **Следующий пересмотр:** при появлении receipt contract или не позднее 28.11.2026

## 5. Что осталось сделать

1. Проверить receipt contract deployment по адресу из официального Synthetix announcement/SIP update, а не по сторонним публикациям.
2. Поставить мониторинг Safe owners/threshold и любых исходящих SNX-трансферов.
3. Обновить timeline в HTML/PDF/data pack, разделив snapshot, mint transfer и lock start.
