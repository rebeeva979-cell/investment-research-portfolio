# LTC — Data refresh note, 20 ноября 2026

## Что обновлено

Сборщик `fetch_ltc_research_data.py` успешно обновил публичные on-chain и mining ряды до **20.11.2026**:

- `LTC_ONCHAIN_DAILY.csv` — Coin Metrics Community API, включая price, market cap, supply, active addresses, transactions, hashrate, fees, issuance и MVRV/realized cap, где покрытие доступно;
- `LTC_BLOCKS_DAILY.csv` — Blockchair daily block aggregates, difficulty, reward, fees и оценочный block interval;
- `LTC_TRANSFER_DAILY.csv` — non-coinbase transfer/output aggregates, inputs/outputs и explicit adjusted-value gap;
- `LTC_PEER_DAILY.csv` — peer panel;
- `LTC_CATALOG.csv` и `LTC_ONCHAIN_KPI_LATEST.csv` — coverage/source metadata.

После этого пересобраны `LTC_LOOKER_DATASET.xlsx`, `LTC_MARKET_DAILY_ENRICHED.csv` и `LTC_Dashboard.html`.

## Обнаруженное ограничение

Загруженный market source `litecoin(1).xlsx` и `LTC_MARKET_DAILY.csv` заканчивались **14.11.2026**. После сверки добавлен Yahoo continuation patch **15–19.11.2026**, и итоговый Looker dataset/dashboard теперь синхронизированы на **19.11.2026**, когда присутствует соответствующий Coin Metrics on-chain snapshot. Строка рынка 20.11 остаётся отдельным patch-наблюдением, потому что Coin Metrics on-chain ряд на эту дату ещё не опубликован.

Это не ошибка расчёта, а рассинхрон покрытия двух источников. Нельзя говорить, что dashboard показывает актуальную цену на 20 ноября, пока не добавлен проверенный OHLC/volume source для 15–20 ноября.

## Что означает последний on-chain срез

На 20.11 в Blockchair-агрегате наблюдается 246 блоков, оценочный интервал около 351 секунд, difficulty около `91.3m`; это point-in-time/daily aggregate и не заменяет абсолютную оценку стоимости атаки. Transfer value остаётся gross non-coinbase output value и включает change/self transfers.

## Кандидатный market patch

Проверен отдельный Yahoo Finance `LTC-USD` ряд для **15–20.11.2026** и сохранён в `LTC_MARKET_PATCH_2026-11-15_TO_2026-11-20.csv`. В основной dataset влиты только даты **15–19.11**; 20.11 оставлена отдельно для синхронизации с on-chain. Volume остаётся provider-defined, а provenance continuation source явно указан.

## Следующий шаг

1. Получить Coin Metrics on-chain snapshot за 20.11 или оставить dashboard as-of 19.11.
2. Зафиксировать source URL, license/terms и единицы volume для Yahoo continuation.
3. Контролировать отсутствующие даты и `return_1d` при каждом обновлении.
4. Сравнивать пять контрольных KPI после пересборки workbook/dashboard.
5. Не повышать decision gate только из-за market patch; оценивать все четыре gate вместе.

## Рабочий вывод

On-chain обновление выполнено, но свежесть инвестиционного dashboard ограничена market layer. Это хороший пример корректной аналитической оговорки: новые данные не должны автоматически считаться доказательством изменения тезиса, если ключевой price/volume ряд имеет другой `as_of`.

