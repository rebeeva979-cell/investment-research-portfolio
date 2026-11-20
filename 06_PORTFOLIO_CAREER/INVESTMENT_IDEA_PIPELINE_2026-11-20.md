# Investment Idea Pipeline — ончейн и публичные активы

**Назначение:** превращать сообщения из Telegram, YouTube, X, новостей, SEC/IR и on-chain наблюдений в проверяемые исследовательские кейсы, а не в список случайных покупок.

## 1. Главное правило

Идея — это не актив и не прогноз. Идея должна быть записана как проверяемое утверждение:

```text
Источник → конкретный claim → какие данные его подтверждают или опровергают
```

Пример плохой записи: «ETHFI может вырасти».  
Пример хорошей записи: «Buyback ETHFI создаёт прямой value accrual держателю, если приобретённый токен действительно поступает в sETHFI или сжигается; проверить маршрут ETHFI по Ethereum/Optimism logs».

## 2. Приём новой идеи

Для каждого источника фиксируем:

| Поле | Что записывать |
|---|---|
| `idea_id` | Уникальный ID |
| `captured_at` | Дата и часовой пояс |
| `asset` / `ticker` | Актив, сеть или компания |
| `source_url` | Прямая ссылка |
| `source_type` | video, Telegram, X, filing, docs, RPC, dashboard |
| `claim` | Одно проверяемое утверждение без усиления риторики |
| `source_tier` | 1 primary, 2 structured, 3 secondary/lead |
| `as_of` | Дата данных из источника |
| `status` | `lead`, `research`, `watchlist`, `wait`, `rejected`, `case-ready` |
| `falsifier` | Что докажет, что идея неверна |
| `next_check` | Конкретное следующее действие |

Если видео или пост ещё не расшифрован, `claim` оставляем `unknown until transcript`, а не угадываем содержание.

## 3. Быстрый triage до полноценного отчёта

Каждая идея получает 0–2 балла по семи критериям:

| Критерий | 0 | 1 | 2 |
|---|---|---|---|
| Источник | слух/скриншот | вторичный разбор | первичный документ или воспроизводимый on-chain факт |
| Demand/adoption | нет метрики | proxy | подтверждённая динамика пользователей/капитала/выручки |
| Экономика | нет денежных потоков | gross fees/выручка без waterfall | retained revenue и расходы reconciled |
| Tokenomics/capital structure | supply неизвестен | есть агрегатор | allocations, unlocks и actual flows проверены |
| Valuation | только target price | один multiple | диапазон и sensitivity по сценариям |
| Catalyst | дата неизвестна | событие без критерия | событие и измеримый trigger |
| Risk/falsifier | риски не названы | список рисков | наблюдаемые условия отмены тезиса |

Максимум — 14 баллов:

- `0–5`: `rejected` или информационный фон;
- `6–8`: `lead`, нужен первичный источник;
- `9–11`: `research`, собираем data pack;
- `12–14`: `watchlist/case-ready`, можно готовить Decision Card.

Нельзя переводить идею в `buy/add`, если source quality = 0, supply/dilution неизвестны или отсутствует falsifier.

## 4. Слои проверки для crypto/on-chain

### Market

Цена, ликвидность, market cap, FDV, volume, volatility, drawdown. Проверяем дату, валюту и provider.

### Network/protocol usage

Active/new/returning addresses, transactions, transfer value, TVL, deposits, withdrawals, product mix. Адреса не равны пользователям; gross transfer value не равен платежному обороту.

### Economics

```text
gross fees
- operator/validator/partner share
- incentives and rebates
- operating/security costs
= net protocol economics
```

Нельзя называть gross fees protocol revenue, а protocol revenue — доходом токенодержателя.

### Tokenomics

```text
max supply → minted supply → circulating supply → unlocks/emissions
→ treasury/insider flows → effective float → sell-pressure scenarios
```

Buyback policy считается value accrual только после проверки фактического маршрута токена: holder distribution, burn, treasury, cashback или неизвестный адрес.

### Security and custody

Проверяем upgradeability, admin keys, multisig threshold, oracle/bridge risk, holder concentration, liquidity depth и incidents.

## 5. Слои проверки для акций

- SEC/IR: revenue, margins, cash, debt, shares diluted, SBC, FCF;
- operating metrics: users, rides, bookings, shipments, subscriptions;
- capital structure: merger terms, preferred/residual claims, dilution;
- catalyst calendar: filing, clinical readout, first trade, earnings;
- valuation: EV/Sales, EV/EBITDA, FCF or scenario DCF;
- falsifier: cash runway failure, margin compression, dilution, failed trial, changed deal terms.

## 6. Минимальный research pack

Идея становится полноценным кейсом, если есть:

1. `Investment Thesis` — что должно быть правдой для роста;
2. `Financial & Tokenomics Model` — как создаётся и распределяется ценность;
3. `Risk Assessment` — что разрушает гипотезу;
4. `Source Register` — URL, дата, метод, качество, ограничение;
5. dashboard/data appendix;
6. Decision Card: статус, уверенность, диапазон, max position, risk, invalidation, catalyst, review date.

## 7. Режимы обновления

**Ежедневно:** новые filings, governance, unlocks, hacks, unusual flows.  
**Еженедельно:** TVL, fees/revenue, ETF/macro context, price/valuation, thesis change.  
**Ежемесячно:** token supply bridge, treasury flows, holders, peer multiples.  
**Event-driven:** clinical readout, merger, IPO/first trade, exploit, major governance vote.

Каждое обновление отвечает на пять вопросов: что изменилось, каким источником подтверждено, усилился ли тезис, какое действие допустимо, когда следующий пересмотр.

## 8. Зарегистрированный lead от 20.11.2026

| ID | Источник | Claim | Статус | Следующий check |
|---|---|---|---|---|
| VIDEO-2026-11-20-001 | https://youtu.be/rmVTEdI6Xrc | `unknown until transcript` | `lead` | получить субтитры/транскрипт, выделить не более 3 проверяемых тезисов, затем проверить primary sources |

До расшифровки этот URL не влияет на портфель, watchlist или Decision Card.

## 9. Карта навыков в проекте

- `digital-assets`: network, DeFi, staking, stablecoins, valuation и риски;
- `token-economics`: supply, unlocks, dilution, buyback/burn и сценарии sell pressure;
- `defillama-api` / `coingecko-api`: TVL, fees, revenue, market data и supply snapshots;
- `token-holder-analysis`: концентрация, insiders и distribution;
- `whale-tracking` / `wallet-profiling`: поведение крупных адресов, только для публичных адресов;
- `thesis-tracker`: weekly thesis changes и falsifiers;
- `investment-suitability` / `bet-sizing`: перевод research-вывода в допустимый размер позиции;
- `research-tools`: живой поиск первичных страниц, конкурентов и источников.

Навыки не заменяют проверку источника: они задают метод, но каждая цифра всё равно получает URL, дату, формулу и ограничение.

