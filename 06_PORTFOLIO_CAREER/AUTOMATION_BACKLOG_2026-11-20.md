# Automation Backlog — Investment Research Portfolio

**Дата:** 20 ноября 2026  
**Цель:** превратить портфолио из набора сильных разовых отчётов в воспроизводимый research-процесс, который можно показать работодателю и поддерживать без ручной сборки.

## Главный вывод

Аналитическая часть уже сильная: ETHFI-кейс доведён до транзакций, supply reconciliation, holder classification, liquidity и Decision Card. Но процесс пока **не доказан как процесс**:

- сайт собран, но не опубликован;
- ETHFI on-chain пайплайн перенесён в `04_ETHFI/onchain/` 20.11.2026;
- числа в HTML и CSV не связаны автоматической проверкой;
- обновление данных и weekly update делаются вручную;
- нет CI, тестов, алертов и единой базы.

Для найма важны не ещё три графика, а ответ на вопрос: **может ли этот человек обновлять исследование каждую неделю и не терять качество данных?**

## Текущий уровень зрелости

| Слой | Что уже есть | Оценка |
|---|---|---|
| Research | ETHFI deep dive, LTC dashboard/memo, SNX report, casebook | 7/10 |
| Reproducibility | `04_ETHFI/onchain/`: fetch → raw → build → manifest → check; 9 unit tests | 8/10 |
| Data engineering | CSV + ad-hoc merge; нет БД, схемы и версий | 3/10 |
| Quality control | `make check`: manifest, tests, links/tables/numbers/CSV drift; stale-контроль ещё вручную | 7/10 |
| Monitoring | Weekly register вручную; алертов нет | 2/10 |
| Publishing | `docs/` готов, локально; публичного URL нет | 5/10 |
| Distribution | Нет Substack, LinkedIn Featured, внешних ссылок | 1/10 |
| Commercial | План есть; пилотов и отзывов нет | 2/10 |

## Целевая архитектура

```text
scheduler (GitHub Actions / cron / DSH)
  → fetch: DefiLlama, CoinGecko, Blockscout, RPC, CoW, SEC
  → raw/YYYY-MM-DD/*.json + manifest.json (URL, fetched_at, sha256, rows)
  → normalize: DuckDB / SQL views
  → checks: freshness, duplicates, units, supply, links
  → build: site data + PDF + charts
  → deploy: GitHub Pages
  → digest + alerts: Telegram / email
```

Принцип: **raw → проверяемая база → шаблон → публикация**. Числа не вводятся в HTML вручную.

### Где сейчас лежит рабочий код ETHFI

Пайплайн on-chain проверки (Blockscout holders, treasury transfers, CoW orders, RPC supply, SVG/CSV) находится вне проекта:

```text
/home/nikolay/Documents/deepseek-harness/default-workspace/ethfi_onchain/
  fetch_lib.py
  build_outputs.py
  raw/*.json
  assets/*.svg
  data/*.csv
```

A02 закрыт 20.11.2026: пайплайн, raw-снимки и проверки лежат в `04_ETHFI/onchain/`.

## Backlog

### P0 — до отправки резюме

| ID | Задача | Зачем | Результат / критерий готовности | Оценка | Зависит |
|---|---|---|---|---|---|
| A01 | Опубликовать `docs/` на GitHub Pages | Без URL портфолио не существует для рекрутера | Репозиторий public, Pages `main /docs`, URL открывает все страницы, PDF и CSV | 2–3 ч | GitHub account |
| A02 | Перенести ETHFI on-chain пайплайн в проект | Отчёт ссылается на `fetch_lib.py` / `build_outputs.py`, которых нет в репозитории | `04_ETHFI/onchain/` с кодом, README и выборочным raw; `python run.py` воспроизводит `ethfi_metrics.csv`, `ethfi_holders_top.csv`, `ethfi_buybacks_daily.csv` | 4–6 ч | — |
| A03 | Единый manifest и source register | Сейчас нельзя доказать, когда и откуда взято каждое число | Каждый fetch пишет `manifest.json`; `ETHFI_SOURCE_REGISTER.csv` генерируется; у каждой метрики есть URL, `as_of`, метод | 3–4 ч | A02 |
| A04 | Consistency gate | Числа в HTML, CSV и отчёте могут разойтись после ручной правки | `make check`: пересчёт ключевых коэффициентов, проверка ссылок/ассетов, stale-дат, арифметики supply; 0 ошибок | 4 ч | A02 |
| A05 | CI/CD на GitHub Actions | Ручная сборка и деплой не масштабируются | На push: pytest, link check, сборка PDF, deploy Pages; зелёный workflow | 3–4 ч | A01, A04 |
| A06 | Weekly refresh + digest (digest/timer ready; Telegram needs env) | Работодателю нужен cadence, а не один замороженный кейс | Понедельник 08:00: ETHFI + macro + LTC, сравнение с порогами, `weekly/YYYY-MM-DD.md`, Telegram-дайджест | 6–8 ч | A03 |

### P1 — следующий уровень

| ID | Задача | Зачем | Результат / критерий готовности | Оценка | Зависит |
|---|---|---|---|---|---|
| A07 | DuckDB-слой и SQL-витрины | SQL в портфолио должен быть исполняемым, а не файлом `.sql` | `research.duckdb`: `market_daily`, `protocol_metrics`, `holders`, `buybacks`, `unlocks`; KPI считаются SQL-вью | 6–8 ч | A02 |
| A08 | Data-quality tests | Ошибки в supply, дублях и пропусках дат должны ломать сборку | Проверки freshness, duplicates, units, supply sum, holder sum, outlier; отчёт в CI | 4–6 ч | A07 |
| A09 | Wallet label registry | Сейчас адреса размечены вручную и могут устареть | `labels.csv` (address, entity, type, confidence, source, as_of); top-250 генерируется из реестра, unknown помечается | 4 ч | A02 |
| A10 | ETHFI trigger alerts | Decision Card должна срабатывать, а не перечитываться вручную | Алерты: buyback пауза >7 дней, treasury/insider → CEX >1%, TVL <$3B, revenue <$2.5M/30d, новый distribution | 4 ч | A06 |
| A11 | Шаблонизация сайта | Числа в HTML вбиты руками; обновление = риск ошибки | HTML генерируется из JSON/CSV; auto `as_of`; meta/OG, sitemap, robots, favicon | 6–8 ч | A07 |
| A12 | PDF-конвейер | CV, casebook и memo собираются вручную командами Chrome | `make pdf`: CV RU/EN, casebook, ETHFI one-pager; проверка страниц и ссылок | 3 ч | A04 |
| A13 | Публичная страница LTC | Один глубокий кейс — мало для найма | `docs/ltc.html` по тому же шаблону: вопрос, данные, модель, риски, Decision Card | 1–2 дня | A11 |
| A14 | SEC/equity pipeline | LYFT/GPRO/ZNTL пока briefs, не модели | EDGAR companyfacts/submissions → нормализованные financials; обновление по 10-Q/10-K | 1–2 дня | A07 |

### P2 — после первых откликов

| ID | Задача | Зачем | Результат |
|---|---|---|---|
| A15 | Portfolio tracker / IPS drift | Показать контроль риск-бюджета, а не только идеи | Holdings + prices → weights vs target/min/max, monthly review |
| A16 | Dune / Looker public dashboards | Работодатель хочет видеть инструмент вживую | 1–2 публичных дашборда со ссылкой из кейса |
| A17 | Substack + analytics | Дистрибуция и обратная связь | 2–3 drafts, публикация, privacy-friendly analytics |
| A18 | CRM платных пилотов | Переход от портфолио к доходу | 20 контактов, 5 интервью, 1 оплачиваемый pilot |

## Что не хватает для трудоустройства

| Пробел | Почему важен | Действие | Приоритет |
|---|---|---|---|
| Публичный URL и GitHub-история | Рекрутер не может проверить локальные файлы | A01, затем ссылка в CV/LinkedIn | Блокер |
| Воспроизводимый on-chain код | Отчёт выглядит убедительно, но код вне проекта | A02 + README с командами | Блокер |
| Второй глубокий публичный кейс | Один ETHFI — это один навык; нужен LTC/SNX | A13 | Высокий |
| English writing sample | CV на английском, но нет standalone memo | ETHFI one-pager EN (PDF) + 2 Substack drafts | Высокий |
| SQL/DB proof | SQL-файлы без исполняемой базы | A07 + 3 публичных запроса | Высокий |
| Cadence | Нет доказательства регулярного обновления | A06 + 4 weekly updates | Высокий |
| References / external validation | Всё self-attested | 2–3 рекомендателя, пилот, отзыв | Средний |
| Data tools | Только free API; нет Dune/Nansen/Arkham | Public Dune + free tiers, описать ограничения | Средний |
| Interview readiness | Нет отрепетированной защиты цифр | 10 вопросов, 90-day plan, mock interview | Средний |
| Availability | CV говорит part-time 15–20 ч; не все роли такие | Явно указывать в outreach; не подаваться на full-time без готовности | Средний |
| Domain / email | `gmail` и `github.io` выглядят менее профессионально | Домен + `hello@` после первых откликов | Низкий |
| Legal / invoicing | Нужно для платных пилотов, не для найма | Проверить статус ИП/самозанятости, договор, оплату | Низкий |

## Что не хватает для реальной работы

- **Источники и SLA.** Сейчас free API и публичные страницы; на работе нужны контракты, rate limits, fallback и понимание задержек.
- **База и версионность.** CSV-файлы с датами в имени не заменяют таблицы с `as_of`, `source_id`, `quality_status`.
- **Мониторинг.** Без алертов analyst узнаёт об изменении тезиса из чата, а не из системы.
- **Покрытие.** 3 кейса — портфолио; для роли нужен universe 15–30 активов и очередь deep dive.
- **Коммуникация.** Нужны короткие memo для неtechnical allocator, а не только длинные отчёты.
- **Compliance.** Дисклеймеры, запрет на обещания доходности, разделение personal research и client advice.
- **Скорость.** Цель: обновление кейса <30 минут, weekly note <2 часов, deep dive 2–3 дня.

## План на первые 7 дней

| День | Задача | Выход |
|---|---|---|
| 1 | A01: репозиторий, Pages, URL | Рабочая ссылка |
| 2 | A02: код ETHFI в проект | `04_ETHFI/onchain/` + README |
| 3 | A03: manifest и source register | `manifest.json`, обновлённый register |
| 4 | A04: consistency gate | `make check` без ошибок |
| 5 | A05: CI + deploy | Зелёный Actions, сайт обновляется push |
| 6 | A06: weekly digest | Первый автоматический дайджест |
| 7 | A13: LTC page | Вторая публичная страница |

## Метрики автоматизации

- время обновления кейса: **<30 минут**;
- доля метрик с source URL и `as_of`: **100%**;
- битые ссылки/ассеты: **0**;
- данные старше 7 дней: **0** в публичной витрине;
- воспроизведение ETHFI: **1 команда**;
- weekly digest: **каждый понедельник**;
- alert latency: **<24 часов**;
- CI: **зелёный** на каждом push.

## Следующий шаг

Начать с A02–A04: это можно сделать без GitHub-доступа и это сразу усиливает главный кейс. A01 требует только создания публичного репозитория владельцем аккаунта.
