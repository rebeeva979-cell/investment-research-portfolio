# Synthetix (SNX): SIP-423 и реальный масштаб supply overhang

**Ончейн-исследование · Марина Ребеева · 19 ноября 2026**

**Статус:** Research POC, не инвестиционная рекомендация  
**Дата среза:** 19 ноября 2026  
**Сеть:** Ethereum mainnet + Optimism (snapshot blocks)  
**Данные:** [`SNX_SIP423_DATA_PACK.xlsx`](SNX_SIP423_DATA_PACK.xlsx) · [`build_snx_data_pack.py`](build_snx_data_pack.py)  
**Первоисточники:** [SIP-423](https://github.com/Synthetixio/SIPs/blob/master/content/sips/sip-423.md) · [CoinGecko](https://www.coingecko.com/en/coins/havven) · [DefiLlama](https://defillama.com/protocol/synthetix)

---

## TL;DR

1. **Эмиссия реальна.** 6 июля 2026 года Synthetix выпустила **236 464 356 SNX** по SIP-423. Total supply вырос с **344 939 867.56** до **581 404 223.56 SNX**: **+68.55%** к pre-mint supply и **40.67%** от post-mint supply.
2. **Все новые токены лежат в одном Safe multisig** `0x3265ff13f29fe2dd7501c608b914bfa5e1ffcf6d`. Исходящих переводов SNX с этого адреса на 19.11.2026 не найдено.
3. **Это не on-chain vesting-контракт.** Safe — мультиподпись; lock/vest из SIP-423 является обязательством и операционным состоянием, а не кодом, который нельзя обойти. Receipt-контракт для claim ещё не развёрнут.
4. **Окно claim — ориентировочно 6 июля 2027 года**, затем линейный vest до 6 июля 2028 года. Текст SIP одновременно говорит про истечение невостребованных receipt через 6 месяцев и оставляет поле «Unclaimed sUSD entitlement treatment» как `TBD` — это надо трактовать как неопределённость, а не как точную дату.
5. **Рыночный контекст на 19.11.2026:** цена **$0.164855**, reported market cap **$95.83M**, FDV **$95.90M**, 30-дневные fees **$3 678**, TVL **$856 123**.
6. **При текущей цене claim стоит $38.98M против $59.12M sUSD par** — дисконт **−34.06%**. Ниже $0.25 у получателей меньше стимула продавать; выше $0.25 стимул резко растёт.
7. **Reported market cap завышен относительно pre-mint базы в 1.685x**, потому что CoinGecko считает заблокированные токены circulating. Для comparability нужно показывать обе базы: 581.40M и 344.94M.
8. **Вывод:** это реальный, но отложенный supply overhang. Главный риск — не завтрашний unlock, а период 2027–2028 годов и отсутствие revenue/TVL поддержки. Research state: **DEFENSIVE**.

---

## 1. Что изменилось по сравнению с предыдущей версией

| Утверждение в старой версии | Обновлённая проверка | Комментарий |
|---|---|---|
| Supply вырос с 344.5M до 581.4M (+69%) | 344 939 867.56 → 581 404 223.56 (+68.55%) | Точные значения; округление +69% корректно |
| 236.46M новых SNX ушли на Safe | 236 464 356.00 SNX; Safe balance подтверждён `balanceOf` | Совпадает до токена |
| С Safe не было исходящих переводов | 0 исходящих SNX-переводов на 2026-11-19 (Blockscout) | Point-in-time observation, не гарантия |
| Claim window откроется примерно с лета 2027 | T+365 дней от snapshot 2026-07-06 → 2027-07-06; vest до 2028-07-06 | Точная дата зависит от deployment receipt-контракта |
| Protocol revenue ~$9k/мес; TVL $0.9M, год назад $144M | 30d fees **$3 678**; 1y fees **$32 242**; TVL **$856 123**; год назад **$88 428 843** | Старые $9k/$144M не воспроизводятся по указанным источникам; заменены на датированный срез DefiLlama |
| Coinbase и CoinCodex не считают токены circulating; market cap отличается в 1.7x | CoinGecko включает 580.98M из 581.40M в circulating; Coinbase/CoinCodex в этом проходе не проверены независимо | Разница 1.685x подтверждена для CoinGecko vs pre-mint базы; методологию Coinbase/CoinCodex нельзя утверждать без dated snapshot |
| Для оценки надо использовать 581M, а не 344.5M | Для FDV — да, 581.40M; для circulating market cap — нужно показывать обе базы | Это не взаимоисключающие, а разные вопросы |
| Невостребованные токены сгорают через 6 месяцев | В SIP есть и «after 6 months expire worthless», и строка «Unclaimed sUSD entitlement treatment = TBD» | Не подавать 2028-01-06 как финальную дату |
| Safe = заблокированные токены | Safe — multisig, не vesting-контракт; signers/threshold не проверены | Ключевое ограничение силы lock |

---

## 2. Исследовательский вопрос

1. Рост supply на +68.55% — это реальная эмиссия или артефакт агрегатора?
2. Кто держит новые токены и когда они могут попасть на рынок?
3. Насколько силён lock: это контракт или обещание?
4. Что это значит для оценки SNX, market cap и FDV?
5. Какой сценарий unlock реалистичен при текущих revenue и TVL?

Почему это важно: **40.67% всего supply** сосредоточено в одном адресе. Даже если токены не продаются сегодня, рынок должен закладывать вероятность их выхода в 2027–2028 годах. При этом reported market cap и circulating supply у разных агрегаторов считаются по-разному, что меняет valuation в 1.685x.

---

## 3. Данные и методология

| Блок | Метод | Источник | Ограничение |
|---|---|---|---|
| Total supply | `eth_call` `totalSupply()` (0x18160ddd), decimals = 18 | Ethereum JSON-RPC | Public endpoint; повторить на втором провайдере |
| Pre-mint supply | `eth_call` `totalSupply()` на блоке 25 473 065 | Archive RPC | Нужен архивный узел |
| Safe balance | `eth_call` `balanceOf(address)` (0x70a08231) | Ethereum JSON-RPC | Point-in-time |
| Mint path | `eth_getTransactionReceipt`, decoding `Transfer` logs | Ethereum JSON-RPC | Логи проверены по tx hash |
| Safe inflows/outflows | Address token transfers | Blockscout API | Индексация может отставать |
| SIP terms | Первоисточник `sip-423.md` + commit history | GitHub Synthetixio/SIPs | Governance text, не код |
| Market data | `/coins/havven` | CoinGecko | Aggregator methodology |
| Fees | `/summary/fees/synthetix?dataType=dailyFees` | DefiLlama | Fees ≠ revenue ≠ profit |
| TVL | `/protocol/synthetix` | DefiLlama | Coverage dependent |

**Воспроизводимость:** все значения и формулы собраны в `SNX_SIP423_DATA_PACK.xlsx`; скрипт `build_snx_data_pack.py` пересобирает пакет. On-chain часть можно повторить через публичный RPC, Blockscout и Etherscan; ссылки — в разделе 13.

---

## 4. Supply bridge

| Шаг | SNX | Изменение | Доля от total |
|---|---:|---:|---:|
| Pre-mint supply на snapshot block 25 473 065 | 344 939 867.56 | — | 59.33% |
| Mint по SIP-423 | +236 464 356.00 | +236 464 356.00 | — |
| Post-mint total supply | 581 404 223.56 | +236 464 356.00 | 100.00% |
| Safe balance | 236 464 356.00 | — | 40.67% |
| CoinGecko circulating supply | 580 980 590.46 | — | 99.93% |
| Pre-mint circulating basis | 344 939 867.56 | — | 59.33% |

Ключевые отношения:

- `236 464 356 / 344 939 867.56 = 68.55%` — насколько вырос supply к pre-mint базе.
- `236 464 356 / 581 404 223.56 = 40.67%` — какая доля post-mint supply создана одним mint.
- `236 464 356 / 581 404 223.56 = 40.67%` — доля Safe, пока все токены лежат там.
- `580 980 590.46 / 581 404 223.56 = 99.93%` — какую часть total supply CoinGecko считает circulating.
- `59 116 089 × 4 = 236 464 356` — проверка 4:1.

Важно: total supply — дробное число (`581 404 223.5556632`), потому что pre-mint supply уже была дробной. Mint сам по себе — ровно `236 464 356.0`.

---

## 5. Путь токенов и custody

| Шаг | Время (UTC) | Откуда | Куда | SNX | Tx |
|---:|---|---|---|---:|---|
| 1 | 2026-07-06 11:43:59 | `0x0000…0000` (mint) | `0xc5f0b419…` | 236 464 356 | `0x0bb737a85b740a2e9557859c587cf6ba3c89ad531b960483cdfc89e42e5bc0b9` |
| 2 | 2026-07-06 11:43:59 | `0xc5f0b419…` | `0x94433f0d…` | 236 464 356 | та же tx |
| 3 | 2026-07-06 11:43:59 | `0x94433f0d…` | `0xc1c33291…` | 236 464 356 | та же tx |
| 4 | 2026-07-06 11:46:23 | `0xc1c33291…` | Safe `0x3265ff13…` | 236 464 356 | `0xda4c600d3e85437e73f5f4128948877500158e881a32c83b4694c38699d3644c` |

Проверки:

- Mint tx: block `25 473 272`, статус `success`, 3 основных `Transfer`-лога по 236 464 356 SNX.
- Перевод на Safe: отдельная tx, block `25 473 284`, timestamp `2026-07-06 11:46:23 UTC`.
- Safe balance: `236 464 356.0 SNX`.
- Исходящие SNX-переводы с Safe: **0** по состоянию на `2026-11-19`.
- Safe — контракт `SafeProxy`; это мультиподпись, а не биржа, не протокол и не vesting-контракт.

**Критическая оговорка.** «Токены в Safe» ≠ «токены в trustless vesting-контракте». SIP-423 описывает 1-year lock + 1-year vest и отдельный receipt-контракт, но на 19.11.2026 receipt-контракт не развёрнут и не наполнен. Пока токены лежат в multisig, сила lock зависит от signers, threshold и governance-процесса. Порог и состав signers в этом проходе не проверялись.

---

## 6. Условия SIP-423

| Параметр | Значение | Комментарий |
|---|---|---|
| Статус | Implemented | Commit `180c54b` от 2026-07-01 |
| Авторы | Kain Warwick, Benjamin Celermajer | Создан 2026-06-12 |
| Maximum Mint | 236 464 356 SNX | Совпадает с фактическим mint |
| sUSD entitlement | 59 116 089 sUSD | 4 SNX за 1 sUSD |
| Snapshot Ethereum | block 25 473 065 | 2026-07-06 11:02:35 UTC |
| Snapshot Optimism | block 153 868 527 | 2026-07-06 11:03:51 UTC |
| Lock | 1 год | «1 year lock + 1 year vest from the time of freeze» |
| Vest | 1 год, линейно | После lock |
| Claim window | T+365 дней | Ориентировочно 2027-07-06 |
| Unclaimed | «after 6 months expire worthless» + строка `TBD` | Неопределённость, не финальная дата |
| Revenue hurdle | $10M в течение 2-летнего lock-up | Configurable via SCCP |
| Revenue share | 25% | На redeem claims в USDT после hurdle |
| Receipt contract | `TBC` / `CONTRACT BUILD DEFERRED` | На 2026-11-19 не развёрнут |

### Таймлайн

| Дата | Событие | Статус |
|---|---|---|
| 2026-06-12 | SIP-423 создан | Completed |
| 2026-07-01 | SIP-423 помечен Implemented | Completed |
| 2026-07-06 11:02:35 UTC | Ethereum snapshot block 25 473 065 | Completed |
| 2026-07-06 11:03:51 UTC | Optimism snapshot block 153 868 527 | Completed |
| 2026-07-06 11:43:59 UTC | Mint 236 464 356 SNX | Completed |
| 2026-07-06 11:46:23 UTC | Перевод на Safe | Completed |
| 2026-08-16 | SIP update фиксирует mint amount и snapshot blocks | Completed |
| 2027-07-06 (оценка) | Claim window opens | Scheduled |
| 2028-01-06 (условно) | 6-month unclaimed expiry, если применимо | TBD |
| 2028-07-06 (оценка) | Конец 1-летнего vest | Scheduled |

**Неопределённость по expiry.** В SIP одновременно есть фраза «Any unclaimed receipts after 6 months will expire worthless» и строка «Unclaimed sUSD entitlement treatment | TBD». Это может означать 6 месяцев после открытия claim window, но финальное правило не зафиксировано. В отчёте и дашборде дата 2028-01-06 должна быть помечена как условная.

---

## 7. Рыночный контекст на 19.11.2026

| Метрика | Значение | Источник |
|---|---:|---|
| Цена | $0.164855 | CoinGecko, last_updated 2026-11-19T17:03:57Z |
| Reported market cap | $95 831 317 | CoinGecko |
| FDV | $95 901 194 | CoinGecko |
| Circulating supply | 580 980 590.46 SNX | CoinGecko |
| Total supply | 581 404 223.56 SNX | Ethereum RPC |
| 24h volume | $6 330 298 | CoinGecko |
| Fees 24h / 30d / 1y | $54 / $3 678 / $32 242 | DefiLlama |
| Fees annualized from 30d | $44 749 | Расчёт: 30d × 365/30 |
| TVL | $856 123 | DefiLlama |
| TVL 1 год назад | $88 428 843 | DefiLlama, 2025-11-19 |
| TVL peak | $2 966 823 065 | DefiLlama, 2021-02-10 |
| TVL change 1y | −99.03% | Расчёт |
| Market cap / 30d fees | 26 055x | Расчёт |
| Market cap / 1y fees | 2 972x | Расчёт |
| Market cap / TVL | 111.9x | Расчёт |
| FDV / TVL | 112.0x | Расчёт |
| Revenue hurdle / 1y fees | 310.2x | Расчёт |

Интерпретация:

- Абсолютные fees очень малы: **$3 678 за 30 дней** и **$32 242 за год**. Это не revenue и не прибыль, а fees по методологии DefiLlama.
- TVL упал на **99.03%** год к году и на **99.97%** от пика 2021 года. Экономический след протокола сейчас несопоставим с 2021 годом.
- Revenue hurdle $10M в 310 раз выше текущих годовых fees. Даже с учётом волатильности и возможного роста это не близкий триггер.
- SNX не является cash-flow claim на fees. 25% revenue redemption — условный механизм, который включается только после $10M и может быть изменён через SCCP. Поэтому multiples «market cap / fees» — диагностика, а не fair value.

---

## 8. Market cap discrepancy и оценка

| База | Supply | Цена | Market cap |
|---|---:|---:|---:|
| Reported CoinGecko circulating | 580 980 590.46 | $0.164855 | $95 831 317 |
| Pre-mint circulating basis | 344 939 867.56 | $0.164855 | $56 865 062 |
| FDV (total supply) | 581 404 223.56 | $0.164855 | $95 901 194 |

- Reported market cap / pre-mint implied market cap = **1.685x**.
- CoinGecko circulating / total supply = **99.93%**; market cap / FDV = **99.93%**.
- Pre-mint market cap / TVL = **66.4x**.
- Pre-mint market cap / annualized 30d fees = **1 271x**.
- Pre-mint market cap / 1y fees = **1 764x**.

Что это значит:

1. CoinGecko фактически считает заблокированные 236.46M SNX circulating. Это увеличивает reported market cap примерно на 40.7% относительно pre-mint базы.
2. Для **FDV** база 581.40M корректна: все токены существуют и могут когда-то выйти.
3. Для **сравнения с историей** и с агрегаторами, которые не считают locked tokens circulating, полезна pre-mint база 344.94M.
4. Нельзя одновременно говорить «market cap $95.8M» и «market cap $56.9M» без указания базы. В отчёте и дашборде нужно показывать обе.

---

## 9. Overhang и сценарии

### 9.1. Claim при разных ценах

При текущей цене $0.164855:

- Стоимость всех 236 464 356 SNX = **$38 982 331**.
- Номинал sUSD entitlement = **$59 116 089**.
- Дисконт к par = **−34.06%**.

То есть по текущей цене держатель sUSD получает примерно **66%** номинала в mark-to-market terms. Это важное уточнение к старой версии: пока цена ниже $0.25, экономический стимул продавать SNX ниже, чем при par. Но если рынок уходит выше $0.25, ситуация меняется.

### 9.2. Линейный unlock

Предположение: 236 464 356 SNX vest линейно за 12 месяцев после открытия claim window. Тогда в среднем **19 705 363 SNX/месяц**.

| Цена | Стоимость всего claim | Unlock/мес, $ | 25% продаж/мес | 50% продаж/мес | 100% продаж/мес | Unlock к monthly volume proxy |
|---:|---:|---:|---:|---:|---:|---:|
| $0.10 | $23.65M | $1.97M | $0.49M | $0.99M | $1.97M | 1.04% |
| $0.15 | $35.47M | $2.96M | $0.74M | $1.48M | $2.96M | 1.56% |
| $0.164855 | $38.98M | $3.25M | $0.81M | $1.62M | $3.25M | 1.71% |
| $0.25 | $59.12M | $4.93M | $1.23M | $2.46M | $4.93M | 2.59% |
| $0.50 | $118.23M | $9.85M | $2.46M | $4.93M | $9.85M | 5.19% |
| $1.00 | $236.46M | $19.71M | $4.93M | $9.85M | $19.71M | 10.38% |

Monthly volume proxy = $6 330 298 × 30 = **$189.9M**. Это грубый знаменатель ликвидности, а не гарантия, что рынок поглотит продажи.

### 9.3. Три режима

**Bear.** Цена ниже $0.15. Claim глубоко ниже par, часть получателей может не спешить с claim; overhang остаётся, но реализованное давление меньше. Revenue и TVL продолжают сжиматься. Reported market cap падает вместе с ценой, но multiple к fees остаётся высоким.

**Base.** Цена $0.15–0.25. Постепенный vest, продажи ограничены, пока цена не подходит к $0.25. Reported market cap примерно $87–145M на circulating базе; pre-mint market cap примерно $52–86M. Для роста нужны revenue/TVL, а не только сокращение overhang.

**Bull.** Цена выше $0.50. Получатели выходят в прибыль относительно $0.25 и продают в силу. 25% revenue buyback всё ещё далеко: hurdle $10M против $32k годовых fees. Для устойчивого роста нужен реальный возврат revenue/TVL и/или новый спрос на токен.

Это сценарии, а не прогнозы. Они показывают чувствительность, а не вероятность.

---

## 10. Что изменит взгляд

1. **Исходящий перевод с Safe больше 1% баланса** до открытия claim window — сигнал, что lock слабее, чем предполагалось.
2. **SIP-423 amendment** меняет vest/expiry, продлевает lock или отменяет 6-месячное истечение.
3. **Receipt-контракт развёрнут и наполнен** — lock становится on-chain, а не policy-based.
4. **Protocol revenue превышает $10M** и запускается 25% redemption mechanism.
5. **TVL и fees восстанавливаются** до уровней, при которых valuation multiples становятся осмысленными.
6. **CoinGecko меняет методологию** и исключает locked tokens из circulating supply — reported market cap падает примерно на 40%.
7. **Claim window сдвигается** или появляется новая дата deployment.
8. **Новый mint/burn вне SIP-423** меняет total supply.

---

## 11. Мониторинг

| Что | Где | Триггер |
|---|---|---|
| Safe balance и исходящие SNX | `0x3265ff13f29fe2dd7501c608b914bfa5e1ffcf6d` | Исходящий перевод >1% баланса |
| Receipt contract deployment | SIP-423 / Synthetix announcements | Появление контракта и seed |
| SIP-423 updates | GitHub `Synthetixio/SIPs` | Изменение vest/expiry/revenue hurdle |
| CoinGecko circulating supply | `/coins/havven` | Резкое изменение circulating без on-chain mint/burn |
| Coinbase / CoinCodex supply | Их страницы/API | Dated snapshot методологии |
| DefiLlama fees | `/summary/fees/synthetix` | Устойчивый рост >$10M run-rate |
| DefiLlama TVL | `/protocol/synthetix` | Восстановление TVL |
| Цена около $0.25 | Рынок | Переход claim из дисконта в par/прибыль |
| Governance SCCP | Snapshot Synthetix | Изменение revenue hurdle или 25% share |

---

## 12. Ограничения и data quality

1. **Safe — не vesting-контракт.** Signers, threshold и policy не проверены. «Нет исходящих переводов» — наблюдение на дату, не гарантия.
2. **Receipt-контракт не развёрнут.** Claim window и vest — оценки по SIP timeline, а не исполненные on-chain события.
3. **Unclaimed expiry противоречив.** В SIP есть 6-месячная фраза и строка `TBD`; 2028-01-06 — условная дата.
4. **CoinGecko methodology.** Reported market cap включает locked tokens. Coinbase/CoinCodex в этом проходе не проверены независимо; не утверждать их методологию без dated snapshot.
5. **DefiLlama fees/TVL.** Fees — не revenue и не profit. TVL зависит от покрытия и методологии; текущий `currentChainTvls` показывает только Ethereum.
6. **Public RPC.** Исторические `eth_call` могут требовать archive node и rate limits. Перед публикацией повторить на втором провайдере.
7. **Point-in-time.** Все рыночные значения — срез 2026-11-19; цена и TVL могут измениться.
8. **Rounding.** Total supply дробный; в отчёте округление до 2 знаков, в data pack — точные значения.
9. **Не инвестиционная рекомендация.** Это research artifact для проверки тезиса и риска.

---

## 13. Источники

| ID | Источник | Что покрывает | Ссылка |
|---|---|---|---|
| SRC-001 | Ethereum JSON-RPC | `totalSupply`, `balanceOf`, tx receipts, block timestamps | https://ethereum-rpc.publicnode.com |
| SRC-002 | Blockscout | Входящие/исходящие SNX-переводы Safe | https://eth.blockscout.com/address/0x3265ff13f29fe2dd7501c608b914bfa5e1ffcf6d?tab=token_transfers |
| SRC-003 | Synthetix SIPs | SIP-423 terms | https://github.com/Synthetixio/SIPs/blob/master/content/sips/sip-423.md |
| SRC-004 | SIP commit | Фиксация mint amount и snapshot blocks | https://github.com/Synthetixio/SIPs/commit/6fffb2ce2d540ace88cf1f77da9cece55c280b94 |
| SRC-005 | CoinGecko | Price, market cap, FDV, circulating, volume | https://www.coingecko.com/en/coins/havven |
| SRC-006 | DefiLlama fees | Fees 24h/30d/1y | https://defillama.com/protocol/synthetix |
| SRC-007 | DefiLlama TVL | TVL history и current | https://defillama.com/protocol/synthetix |
| SRC-008 | Etherscan | Human-readable tx/address links | https://etherscan.io/token/0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F |
| SRC-009 | Internal data pack | Расчёты, сценарии, verification log | `SNX_SIP423_DATA_PACK.xlsx` |

Ключевые ссылки:

- Mint tx: https://etherscan.io/tx/0x0bb737a85b740a2e9557859c587cf6ba3c89ad531b960483cdfc89e42e5bc0b9
- Safe transfer tx: https://etherscan.io/tx/0xda4c600d3e85437e73f5f4128948877500158e881a32c83b4694c38699d3644c
- Safe: https://etherscan.io/address/0x3265ff13f29fe2dd7501c608b914bfa5e1ffcf6d
- Ethereum snapshot block: https://etherscan.io/block/25473065
- Optimism snapshot block: https://optimistic.etherscan.io/block/153868527

---

## 14. Как повторить

### 14.1. Total supply

```bash
curl -s -X POST https://ethereum-rpc.publicnode.com \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F","data":"0x18160ddd"},"latest"],"id":1}'
```

Результат: `581404223555663177920417946` при decimals 18 → `581 404 223.5556632`.

### 14.2. Safe balance

```bash
curl -s -X POST https://ethereum-rpc.publicnode.com \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F","data":"0x70a082310000000000000000000000003265ff13f29fe2dd7501c608b914bfa5e1ffcf6d"},"latest"],"id":1}'
```

Результат: `236464356000000000000000000` → `236 464 356.0`.

### 14.3. Mint tx

```bash
curl -s -X POST https://ethereum-rpc.publicnode.com \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","method":"eth_getTransactionReceipt","params":["0x0bb737a85b740a2e9557859c587cf6ba3c89ad531b960483cdfc89e42e5bc0b9"],"id":1}'
```

Проверить `status = 0x1`, block `25 473 272`, три `Transfer`-лога по `236 464 356`.

### 14.4. Safe transfers

Открыть Blockscout token transfers для Safe и убедиться, что есть только входящий перевод `236 464 356` и нет исходящих.

### 14.5. Пересборка data pack

```bash
python3 02_SNX/build_snx_data_pack.py
```

---

## 15. English summary

**Synthetix (SNX) — SIP-423 supply overhang, updated 19 Nov 2026**

- On 6 July 2026 Synthetix minted **236,464,356 SNX** under SIP-423. Total supply rose from **344,939,867.56** to **581,404,223.56** (+68.55%; 40.67% of post-mint supply).
- The entire mint sits in one Safe multisig (`0x3265ff13…cf6d`); no outgoing SNX transfers were found as of 19 Nov 2026.
- The Safe is a multisig, not an on-chain vesting contract. The lock/vest is a policy commitment; the receipt contract is not deployed yet.
- Claim window is estimated at **6 July 2027**, followed by a one-year linear vest to **6 July 2028**. The unclaimed-entitlement treatment is contradictory in the SIP text (6 months vs `TBD`).
- Market snapshot: price **$0.164855**, reported market cap **$95.83M**, FDV **$95.90M**, 30-day fees **$3,678**, TVL **$856k** (down 99.03% YoY).
- At the current price the claim is worth **$38.98M** versus **$59.12M** sUSD par (−34.06%). Selling incentive is lower below $0.25 and rises above it.
- Reported market cap is **1.685x** the pre-mint implied market cap because CoinGecko counts locked tokens as circulating. Show both bases.
- **Conclusion:** real but deferred supply overhang. The key risk window is 2027–2028, and the protocol currently lacks the revenue/TVL base to absorb it. Research state: **DEFENSIVE**. Not investment advice.

---

*Не инвестиционная рекомендация. Все рыночные и on-chain значения — point-in-time snapshot; перед публикацией проверьте источники и условия использования провайдеров.*
