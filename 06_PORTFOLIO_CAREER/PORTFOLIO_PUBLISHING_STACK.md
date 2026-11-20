# Где вести Investment Research Portfolio

Дата решения: 19 ноября 2026.

## Рекомендация

Использовать не одну платформу, а три слоя:

```text
Substack = публичные исследования и аудитория
Static site / HTML = casebook, dashboards и навигация
Git repository / local archive = SQL, CSV, Python, source register и история изменений
```

Substack стоит использовать как «входную дверь» портфолио, но не как единственный источник данных. Сырые выгрузки, SQL и расчёты должны оставаться отдельно, чтобы работодатель мог проверить воспроизводимость.

## Что публиковать в Substack

### 1. Deep-dive research

Один большой материал раз в 2–4 недели:

- Investment question;
- краткий тезис;
- данные и качество источников;
- operating/tokenomics model;
- valuation scenarios;
- risk assessment;
- Decision Card;
- ссылка на dashboard и приложение с методикой.

Темы первого цикла:

1. Litecoin: network economics вместо обычного графика цены.
2. Ether.fi: почему TVL не равен value accrual ETHFI.
3. Lyft: rides и active riders против нормализованного FCF.
4. ZNTL: cash runway и binary clinical risk.
5. GPRO: merger probability и residual ownership.
6. Anthropic: run-rate, TTM revenue, dilution и IPO valuation.

### 2. Weekly change note

Короткий еженедельный пост:

- что изменилось за 7 дней;
- какие данные усилили или ослабили тезис;
- какой риск приблизился;
- какое действие допустимо сейчас;
- дата следующего пересмотра.

### 3. Macro & flows

Отдельная регулярная заметка по SPY, DXY, USDT и BTC/ETH ETF flows. Это контекст для кейсов, а не самостоятельный торговый сигнал.

## Что не публиковать в Substack

- seed phrase, приватные ключи и данные аккаунтов;
- полный экспорт личного портфеля с адресами и cost basis;
- неподтверждённые слухи как факты;
- обещания `4–6x`;
- торговые сигналы без risk budget и invalidation;
- сырые CSV без объяснения единиц, периода и качества данных.

## Роль каждой платформы

| Слой | Лучшее применение | Ограничение |
|---|---|---|
| Substack | статьи, email, подписчики, публичный архив, paid pilot | неудобен для SQL, больших CSV и интерактивной data model |
| Static HTML site | casebook, интерактивные dashboards, резюме и ссылки | нужно отдельно организовать рассылку и аудиторию |
| Looker Studio | интерактивные отчёты и клиентский просмотр | нужен Google-доступ и отдельная настройка источников |
| Git repository | версии кода, SQL, README, issue log, воспроизводимость | требует аккуратной публикации и базовых Git-навыков |
| Notion | внутренний индекс, CRM, pipeline контактов | не должен быть единственным хранилищем расчётов |

## Структура публичного портфолио

### Home

- короткое позиционирование;
- 6 карточек кейсов;
- ссылка на methodology;
- ссылка на dashboard;
- disclosure: personal research, not client asset management.

### Case page

Каждый кейс должен иметь один и тот же порядок:

1. вопрос исследования;
2. thesis;
3. data sources и source quality;
4. dashboard;
5. model / SQL;
6. risks and falsifiers;
7. Decision Card;
8. weekly update;
9. next review date.

## Почему Substack подходит

Substack позволяет публиковать посты в вебе и отправлять их подписчикам по email, а данные публикации и список подписчиков можно экспортировать. Для собственного домена нужен уже купленный домен; Substack указывает разовый сбор `$50` за подключение custom domain. Ссылки на актуальные условия нужно проверять перед оплатой.

Источники: [Substack — publishing](https://support.substack.com/hc/en-us/articles/29152946791188-How-can-I-publish-on-Substack), [Substack — export and features](https://substack.com/features), [Substack — custom domain](https://support.substack.com/hc/en-us/articles/360051222571-How-do-I-set-up-my-custom-domain-on-Substack).

## План запуска

### Этап 1 — portfolio hub

- [x] создать локальную deployment-ready стартовую страницу (`00_README/PORTFOLIO_INDEX.html` и корневой `index.html` для GitHub Pages/Netlify);
- [x] разместить casebook и связать его с индексом;
- [x] добавить LTC dashboard и первый Anthropic calculator в навигацию;
- [ ] добавить CV-style About и отдельную страницу methodology;

Получена версия `Investment_Research_Portfolio_RU_v2(1)` с единым тёмным дизайном. Она объединена с каноническими CSV/SQL/Python/PDF и сохранена в `07_PUBLICATION/Investment_Research_Portfolio_RU_v2/`. Локальные HTML-ссылки и изображения проверены: битых локальных ссылок не осталось.

Добавлен локальный CV PDF и блок About. Публичная ссылка GitHub Pages пока отсутствует: нужен GitHub username и созданный repository либо подключённый GitHub-коннектор.

Публичная публикация ещё не выполнена: для GitHub Pages/Netlify нужен выбранный канал и URL, а для Looker Studio — доступ к Google-аккаунту владельца.

### Этап 2 — три публичных материала

1. LTC: «Безопасность сети не равна экономической привлекательности монеты».
2. ETHFI: «TVL растёт, но получает ли держатель ETHFI ценность?».
3. Anthropic: «18.6× run-rate и 42.7× TTM — почему один revenue multiple вводит в заблуждение».

### Этап 3 — weekly cadence

- понедельник: macro/ETF flows;
- среда: один data point или SQL explanation;
- пятница: weekly change note по одному кейсу.

### Этап 4 — monetization

- бесплатные публичные кейсы как доказательство методики;
- платный research pilot для одного актива;
- индивидуальный dashboard audit;
- weekly decision-support update без обещаний доходности.

## Что нужно от владельца

1. название Substack и короткое описание;
2. авторское имя и bio;
3. решение: русский, английский или двуязычный формат;
4. публичный или закрытый старт;
5. домен, если нужен professional URL;
6. согласие на публикацию кейсов и screenshots.

Без доступа к Substack я могу подготовить Markdown/HTML drafts, обложки, структуру рубрик и ссылки, но не могу нажать Publish в аккаунте.
