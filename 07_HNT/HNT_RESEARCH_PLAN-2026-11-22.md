# HNT — план инвестиционного исследования

Дата старта: 22 ноября 2026 года
Статус: `research / first snapshot / decision = wait`

## Инвестиционный вопрос

Растёт ли Helium как платная carrier-offload сеть быстрее, чем HNT размывается эмиссиями и вознаграждениями? И может ли burn Data Credits компенсировать текущий и одобренный будущий выпуск HNT?

## Что уже проверено

1. **Продукт.** Helium Mobile/Carrier использует распределённые Wi‑Fi-точки для offload трафика; IoT остаётся отдельным поднаправлением.
2. **Токен.** HNT — базовый токен; Data Credits (DC) создаются только через сжигание HNT и имеют фиксированную стоимость $0.00001 за DC.
3. **Сеть.** Официальный snapshot сообщает 1M+ daily users, 49 TB+ daily data transferred и 40k+ active access points. Это заявленные командой показатели, не независимая сверка.
4. **Эмиссия.** Документация описывает халвинг и net emissions. HIP‑149 имеет статус `Approved` и предусматривает отдельный operations & growth supplement около 141M HNT за 36 месяцев; фактическое включение программы и даты mint нужно подтвердить on-chain.
5. **Market snapshot.** Цена из CoinGecko около $0.2217, market cap около $45.15M; публичный Solana RPC показывает total token supply 203,625,648.88 HNT на slot 472,646,415.

## Данные, которые нужно добрать

- ежедневный HNT burn из DC за 30/90/365 дней;
- отдельно Mobile и IoT: bytes, DCs, payer и rewardable bytes;
- HNT minted по reward buckets, net emissions и service-provider rewards;
- HIP‑149 deployment status, supplement vault address, фактические inflows/outflows;
- active access points, unique users и traffic на одном и том же окне;
- carrier concentration и доля трафика крупнейшего плательщика;
- полный supply bridge: current supply → base emissions → net emissions → supplement → burns;
- данные о governance/veHNT concentration и multisig controls.

## Источники и методика

- первичная методика токена: Helium Docs HNT/DC;
- usage: официальный snapshot и открытый Iceberg catalog Helium Mobile;
- supply: Solana `getTokenSupply` для mint HNT;
- market: CoinGecko snapshot с timestamp в JSON;
- governance/emissions: исходный текст HIP‑149.

Нельзя считать daily users, access points или TB выручкой. Для экономики используем только подтверждённый DC burn/paid traffic, а не маркетинговые counters. Volatility для крипторасчётов годится с 365 периодами.

## Правило решения

До сверки burn против mint и проверки HIP‑149 deployment решение не переводить в `buy/add`.
Следующее обновление: после получения 30-дневного ряда burn/mint или через 7 дней, если ряд ещё не доступен.
