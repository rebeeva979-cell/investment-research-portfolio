# LTC data-source licence review

**Дата проверки:** 21 ноября 2026
**Назначение:** публикация портфолио, Substack, GitHub Pages и возможный оплачиваемый research pilot

## Вывод

Текущий LTC workbook можно использовать как учебный и внутренний research artefact с атрибуцией. Для коммерческого распространения сырых или производных рядов нужно сначала получить отдельное разрешение/лицензию.

### Coin Metrics Community

Официальная документация указывает, что Community Data распространяется под Creative Commons; в репозитории архивов Coin Metrics указан **CC BY-NC 4.0**. `NC` означает non-commercial: бесплатный Community API не следует использовать как источник для продажи датасета, платного dashboard или оплачиваемого research-пакета без дополнительного разрешения.

Практическое решение:

- в публичном портфолио оставить ссылки, атрибуцию, дату извлечения, методику и ограниченные иллюстративные значения;
- не выкладывать полный raw export Coin Metrics и не обещать клиенту обновляемый commercial data feed;
- для платного пилота получить письменное разрешение или перейти на источник с коммерческой лицензией;
- сохранить доказательство проверки в source register.

### Blockchair

В открытых найденных материалах Blockchair подтверждается наличие REST API и продуктов для компаний, но ясная лицензия на повторное коммерческое распространение агрегированных данных в используемом наборе не подтверждена. Поэтому статус — **`permission_required / not verified`**.

Практическое решение:

- ссылаться на Blockchair как на extraction provider;
- не перепродавать raw Blockchair response;
- запросить у Blockchair условия API/data use для GitHub Pages, Substack и paid research;
- до ответа считать коммерческое использование незакрытым.

## Source register

| Источник | URL | Наблюдение | Статус |
|---|---|---|---|
| Coin Metrics Community docs | https://github.com/coinmetrics/product-docs/blob/master/docs/packages/coin-metrics-community-data.md | Community Data, rate limits и описание бесплатного community access | прочитано |
| Coin Metrics data archive | https://github.com/coinmetrics/data/blob/master/LICENSE | CC BY-NC 4.0 | commercial reuse не подтверждён |
| CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ | non-commercial licence terms | учитывать до публикации |
| Blockchair API/about | https://blockchair.com/about | REST API и business use cases | licence для redistribution не подтверждена |
| Blockchair FAQ | https://blockchair.com/faq | публичные объяснения сервиса | не является data licence |

## Что меняется в решении

Проблема лицензии не меняет числовой вывод LTC, но меняет публикационный gate:

- **internal / educational:** `pass with attribution`;
- **public portfolio with small cited examples:** `conditional`, после проверки конкретного объёма цитирования;
- **paid recurring research/data feed:** `wait` до разрешения Coin Metrics и Blockchair либо замены источников.
