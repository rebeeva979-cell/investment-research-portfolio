# Investment Research Standard — Crypto / DeFi кейсы

## Зачем нужен этот документ

Публичных дашбордов много. Инвестфонду не нужен ещё один график цены ETH или TVL Uniswap. Нужен вывод, который помогает принять решение:

1. стоит ли инвестировать в актив;
2. за счёт чего он может вырасти;
3. какую реальную выручку генерирует протокол или сеть;
4. не переоценён ли токен;
5. какие риски рынок может недооценивать;
6. что изменилось в инвестиционном кейсе за последнюю неделю.

Дашборд является приложением к исследованию. Он показывает доказательства и динамику, но не заменяет тезис, модель и риск-анализ.

## Стандарт результата

Каждый приоритетный кейс должен состоять из трёх основных документов и одного приложения:

1. `Investment Thesis` — почему актив может быть интересен и какие условия необходимы для роста.
2. `Financial & Tokenomics Model` — как устроена экономика протокола, токена и денежных потоков.
3. `Risk Assessment` — что может разрушить инвестиционную гипотезу.
4. `Dashboard + Data Appendix` — интерактивные графики, SQL, источники и проверка качества данных.

Рекомендуемый объём финального research report: 10–20 страниц без приложения с сырыми данными.

## Обязательная Decision Card

Каждый отчёт заканчивается не вопросом «купить ли актив вообще», а формулировкой: **какое действие допустимо при текущих данных и заданном риск-бюджете**.

| Поле | Обязательное содержание |
|---|---|
| `decision_status` | `buy/add`, `hold`, `trim`, `avoid` или `wait` |
| `confidence` | `low`, `medium` или `high` |
| `valuation_range` | диапазон оценки, метод и ключевые предпосылки; `N/A`, если оценка незащищаема |
| `max_position_pct` | максимальная доля позиции в рамках риск-бюджета |
| `main_risk` | риск с наибольшим влиянием на тезис |
| `thesis_invalidation` | наблюдаемое условие отмены тезиса |
| `next_catalyst` | ближайшее событие и критерий подтверждения |
| `next_review_date` | дата следующего пересмотра |

`buy/add` не означает гарантированную доходность, а `wait` не означает обязательную продажу. Если качество данных недостаточно, корректное действие — `wait` и указание недостающих подтверждений.

## Вопросы, на которые должен отвечать analyst

### Инвестиционная привлекательность

- Какую проблему решает продукт?
- Кто платит за решение и почему?
- Есть ли сетевой эффект, switching cost или иной защитный механизм?
- Какие показатели подтверждают adoption?
- Какой catalyst может изменить спрос в ближайшие 6–18 месяцев?
- Что должно быть правдой, чтобы актив вырос?

### Экономика

- Сколько пользователей и капитала приходит в продукт?
- Как растёт TVL или другой релевантный запас капитала?
- Какой gross fee volume генерируется?
- Какая часть fees остаётся протоколу как protocol revenue?
- Какие incentives, grants, операционные и security costs несёт протокол?
- Есть ли net revenue или экономика держится на субсидиях?
- Получает ли токен прямой value accrual?

### Оценка

- Какова market cap и FDV?
- Какой circulating supply и какой будущий unlock overhang?
- Какие multiples уместны: fees/FDV, revenue/market cap, TVL/market cap, P/E-like net earnings?
- Что уже заложено в цене?
- Что произойдёт при сжатии multiples или падении TVL?

### Изменение кейса

- Что изменилось за последнюю неделю?
- Изменились ли пользователи, TVL, fees, revenue, supply, unlocks или risk events?
- Изменился ли базовый сценарий, или произошло только движение цены?

## Контроль качества источников

### Иерархия

**Tier 1, первичные источники:**

- protocol docs, GitHub и governance proposals;
- verified smart contracts и события в блокчейне;
- официальные API протокола, chain explorers и subgraphs;
- официальные token distribution, unlock и treasury disclosures.

**Tier 2, структурированные независимые источники:**

- Coin Metrics, DefiLlama, Dune queries с открытым SQL;
- Token Terminal, Artemis и аналогичные поставщики, если методика и лицензия понятны;
- независимые dashboards, если можно проверить raw query и период.

**Tier 3, источники для поиска, но не для ключевого вывода:**

- Telegram, X, YouTube, рекламные посты, агрегаторы без методологии;
- скриншоты без URL, даты и определения метрики.

Tier 3 может подсказать гипотезу, но не подтверждает revenue, TVL, unlock или valuation.

### Реестр каждой метрики

Для каждой цифры в модели нужно сохранять:

| Поле | Что записываем |
|---|---|
| metric | Каноническое имя метрики |
| value | Значение и единица |
| as_of | Дата и часовой пояс |
| source | Провайдер и прямой URL |
| method | API, SQL, contract event или ручная сверка |
| formula | Формула производной метрики |
| coverage | Период и пропуски |
| quality | verified, cross-checked, proxy или unavailable |
| limitation | Что метрика не измеряет |

Ключевые цифры нельзя брать из одного источника без cross-check. Для revenue, TVL, supply и unlocks нужно сверять минимум два независимых представления, если они доступны.

### Правила дат и единиц

- Не смешивать дневной TVL с месячной выручкой без явной агрегации.
- Не смешивать market cap и FDV.
- Не называть gross fees protocol revenue.
- Не называть protocol revenue доходом токенхолдера без механизма распределения.
- Хранить исходную единицу и отдельно производный USD-ряд.
- Отмечать daily anchor, если timestamp не является точным временем события.
- `N/A` лучше неподтверждённой цифры.

## Структура Investment Thesis

1. Executive summary: вывод, рейтинг уверенности, текущий сценарий.
2. Product and market: продукт, клиент, проблема, конкуренты.
3. Adoption evidence: users, TVL, volumes, retention proxies.
4. Economic engine: fees, revenue, costs, incentives, net economics.
5. Token value accrual: utility, governance, staking, buyback, distribution, dilution.
6. Valuation: market cap, FDV, relevant multiples, scenario table.
7. Catalysts: measurable events with dates and confirmation criteria.
8. Falsifiers: data points that would invalidate the thesis.
9. Conclusion: Bull / Base / Bear, position suitability and open questions.

## Структура Financial & Tokenomics Model

### Protocol P&L bridge

```text
Gross fees
- rebates / LP or validator share
- incentives and token subsidies
- operating / security costs
= protocol revenue or net protocol earnings
```

Затем отдельно показать:

```text
Net protocol earnings
- treasury spend
- grants / buybacks / distributions
= cash-flow available for token holders (если механизм существует)
```

Если какой-либо элемент неизвестен, он отмечается как unavailable, а не приравнивается к нулю.

### Token bridge

```text
Max supply
→ allocated supply
→ unlocked supply
→ circulating supply
→ future unlocks / emissions
→ effective sell pressure scenarios
```

Нужно отделять:

- nominal APR от real yield;
- TVL от revenue;
- gross fees от protocol revenue;
- revenue от token-holder value accrual;
- market cap от FDV;
- announced allocation от actual on-chain distribution.

## Структура Risk Assessment

Для каждого риска нужны четыре поля:

1. механизм риска;
2. текущая экспозиция;
3. наблюдаемый trigger;
4. потенциальный ущерб для тезиса и токена.

Минимальный набор для DeFi:

- smart-contract exploit;
- oracle and pricing risk;
- slashing / validator risk;
- liquidity and redemption risk;
- leverage and liquidation risk;
- concentration of TVL, operators or holders;
- governance and multisig risk;
- unlocks, emissions and dilution;
- competitor substitution;
- regulatory and custody risk;
- source and measurement risk.

## Weekly Investment Case Update

Каждую неделю должен появляться короткий change log:

| Блок | Было | Стало | Влияние на тезис | Источник |
|---|---|---|---|---|
| Adoption |  |  | positive / neutral / negative |  |
| TVL / capital |  |  |  |  |
| Fees / revenue |  |  |  |  |
| Token supply |  |  |  |  |
| Valuation |  |  |  |  |
| Risk events |  |  |  |  |

Формат заключения: `Thesis strengthened`, `Thesis unchanged` или `Thesis weakened`, с двумя-тремя доказательствами.

## Приоритет проектов

| Проект | Что демонстрируем | Финальный артефакт |
|---|---|---|
| LTC | Анализ сети, денежной модели и конкурентного положения | Network & Market Research |
| SNX | Умение обнаруживать supply overhang и проверять actual mint | Tokenomics & Supply Analysis |
| ETHFI | Анализ экономики DeFi-протокола и value accrual токена | Protocol Economics |
| UNI | Анализ volumes, fees, revenue и механизмов создания стоимости | Revenue & Value Accrual |

Работы не должны быть равнозначными по глубине. Два-три законченных кейса лучше десяти незавершённых dashboards.

## Definition of done

Кейс считается готовым для портфолио, если:

- есть три документа: thesis, model, risk;
- каждая ключевая цифра имеет source URL, as-of date и definition;
- есть raw/staging/core/mart или эквивалентная прозрачная data flow;
- SQL или код воспроизводит основные расчёты;
- дашборд связан с конкретными вопросами исследования;
- есть Bull / Base / Bear или другой сценарный вывод;
- указан список неизвестных и рисков измерения;
- weekly update показывает, что изменилось после публикации.
- в конце отчёта заполнена Decision Card со статусом, уверенностью, valuation range, лимитом позиции, риском, invalidation, катализатором и датой пересмотра.

## 90-дневный план исполнения

1. Довести LTC и ETHFI до полноценных кейсов.
2. Подключить Macro & ETF Flows.
3. Закончить briefs по Lyft и GoPro.
4. Выпустить несколько публичных примеров.
5. Провести пять интервью с потенциальными пользователями.
6. Продать один небольшой оплачиваемый research-пилот.

Не продавать обещания `4–6x` и торговые сигналы. Продавать прозрачную методику, экономию времени и дисциплину принятия решений.
