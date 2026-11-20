# Crypto & Investment Research Portfolio

Сводная папка рабочих материалов для портфолио Investment Research / Crypto Research / Digital Assets.

## Структура

- `01_LTC` — Litecoin: market + on-chain + peer датасеты, Network Economics framework, Looker-ready workbook, decision gates, research memo и инструкция сборки отчёта.
- `02_SNX` — исследование Synthetix SIP-423: supply overhang, методика и статус проверки.
- `03_AVAIL` — спецификация Avail On-chain Intelligence Dashboard.
- `04_ETHFI` — исследовательский blueprint Ether.fi.
- `05_OTHER_ASSETS` — аудит источников для EGLD, ZNTL, ZRX, COMP, UNI, ROSE, LRC и сопутствующих активов.
- `05_OTHER_ASSETS` также содержит единый research stack для crypto + equities, watchlist и briefs по GoPro и Lyft.
- `05_OTHER_ASSETS/fetch_market_macro_data.py` обновляет SPY, DXY, GPRO, LYFT и USDT; ETF-потоки BTC/ETH сохраняются отдельной таблицей с явным статусом `not reported` для ещё не опубликованных дней.
- `06_PORTFOLIO_CAREER` — общий план портфолио, стандарты кейсов и карьерное позиционирование.

План работы, клиентов и монетизации: [`06_PORTFOLIO_CAREER/RESEARCH_SERVICE_AND_MONETIZATION_PLAN.md`](../06_PORTFOLIO_CAREER/RESEARCH_SERVICE_AND_MONETIZATION_PLAN.md).

Главный стандарт инвестиционного кейса: [`06_PORTFOLIO_CAREER/INVESTMENT_RESEARCH_STANDARD.md`](../06_PORTFOLIO_CAREER/INVESTMENT_RESEARCH_STANDARD.md). Он задаёт обязательные документы Investment Thesis, Financial & Tokenomics Model, Risk Assessment и Dashboard/Data Appendix.

## Важное разграничение статусов

Не все материалы являются завершёнными инвестиционными исследованиями. В документах отдельно отмечены:
- готовые файлы и подготовленные структуры;
- данные, которые реально загружены и обработаны;
- проекты, находящиеся на стадии blueprint / specification;
- метрики и выводы, которые требуют повторной проверки по первоисточникам.

## Текущий статус LTC

Пользователь загрузила `litecoin(1).xlsx`. На его основе подготовлены:
- `LTC_original_uploaded_data.xlsx` — оригинал;
- `LTC_Market_Data_Cleaned.xlsx` — очищенная таблица и лист-инструкция;
- `LTC_MARKET_DAILY.csv` — CSV для импорта;
- `LTC_Looker_Studio_Starter.xlsx` — первоначальная структура листов для исследования;
- `LTC_LOOKER_DATASET.xlsx` — обогащённый workbook с листами для Looker Studio;
- `LTC_LOOKER_STARTER.xlsx` — компактная версия на 11 листов для быстрой сборки в Looker Studio;
- `LTC_Dashboard.html` — self-contained интерактивный дашборд на 7 разделов;
- `LTC_START_HERE.html` — единая стартовая страница со ссылками на все артефакты;
- `LTC_RESEARCH_MEMO.md` — краткий investment research memo с выводами и ограничениями;
- `LOOKER_STUDIO_BUILD_GUIDE.md` — пошаговая карта сборки отчёта;
- `LOOKER_STUDIO_STARTER_CHECKLIST.md` — короткий чеклист на первые 3 страницы;
- `build_ltc_looker_starter.py`, `build_ltc_html_dashboard.py` — воспроизводимая сборка starter и HTML-дашборда;
- `LTC_Research_Package.zip` — переносимый пакет с дашбордом, workbook, PDF и стартовой страницей;
- `fetch_ltc_research_data.py` — обновление on-chain, peer, block и transfer данных из Coin Metrics Community API и Blockchair;
- `LTC_ONCHAIN_DAILY.csv`, `LTC_BLOCKS_DAILY.csv`, `LTC_TRANSFER_DAILY.csv`, `LTC_PEER_DAILY.csv`, `LTC_CATALOG.csv` — сетевой ряд, блоки, gross transfer/output metrics, peer-панель и каталог покрытия.

Для ETHFI подготовлены рабочие документы:

- `ETHFI_INVESTMENT_THESIS.md` — центральная гипотеза и decision gates;
- `ETHFI_FINANCIAL_TOKENOMICS_MODEL.md` — protocol P&L bridge, supply bridge и valuation framework;
- `ETHFI_RISK_ASSESSMENT.md` — risk register и falsifiers;
- `ETHFI_WEEKLY_UPDATE_TEMPLATE.md` — шаблон изменения инвестиционного кейса за неделю.

Для объединённого research dashboard подготовлены:

- `05_OTHER_ASSETS/RESEARCH_SKILLS_AND_DATA_MODEL.md` — карта навыков и единая методология;
- `05_OTHER_ASSETS/EQUITY_CRYPTO_WATCHLIST.csv` — watchlist LTC, ETHFI, SNX, UNI, GPRO и LYFT;
- `05_OTHER_ASSETS/EQUITY_CRYPTO_RESEARCH_SCHEMA.sql` — схема данных, ownership, financials, tokenomics и valuation;
- `05_OTHER_ASSETS/COMBINED_DASHBOARD_BUILD_GUIDE.md` — страницы и правила Looker Studio;
- `05_OTHER_ASSETS/GPRO_RESEARCH_BRIEF.md` и `LYFT_RESEARCH_BRIEF.md` — первые investment briefs.

В очищенном файле 2 984 дневные записи, период 22.08.2018–14.11.2026. Временной ряд содержит 5 разрывов дат. Объём `Volume` оставлен без присвоения единицы измерения, поскольку она не подтверждена исходным файлом. On-chain и peer-панели обновляются отдельным fetch-скриптом.

В `LTC_LOOKER_DATASET.xlsx` поля без суффикса `_pct` хранят процентные значения как доли, совместимые с типом Percent в Looker Studio. Поля с `_pct` сохранены как audit-поля в процентных пунктах.

## Как продолжать

1. Открыть `01_LTC/LTC_START_HERE.html` — это единая точка входа во все артефакты.
2. При обновлении выполнить `python3 01_LTC/fetch_ltc_research_data.py`, затем `python3 01_LTC/build_ltc_looker_dataset.py`, `python3 01_LTC/build_ltc_looker_starter.py` и `python3 01_LTC/build_ltc_html_dashboard.py`.
3. Для быстрого Looker Studio использовать `01_LTC/LTC_LOOKER_STARTER.xlsx` и `01_LTC/LOOKER_STUDIO_STARTER_CHECKLIST.md`.
4. Для полного кейса загрузить `01_LTC/LTC_LOOKER_DATASET.xlsx` в Google Drive и использовать `01_LTC/LOOKER_STUDIO_BUILD_GUIDE.md` как карту страниц, типов полей и ограничений.
5. Перед коммерческим использованием проверить условия Coin Metrics Community API и Blockchair API/rate limits.
6. По остальным проектам использовать документы как рабочие спецификации, а не выдавать их за завершённые исследования.
