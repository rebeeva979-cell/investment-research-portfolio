# LYFT — проверка квартального ряда и качества cash flow

**Дата среза:** 23 ноября 2026 года
**Статус:** `wait`
**Период:** Q1 2024 — Q3 2026

## Что проверено

Из SEC Company Facts для CIK `0001759509` собран квартальный ряд выручки, operating income, net income, operating cash flow, SBC и diluted shares. Первичный источник — [SEC Company Facts](https://data.sec.gov/api/xbrl/companyfacts/CIK0001759509.json); последний filing в срезе — [Lyft 10-Q за Q3 2026](https://www.sec.gov/Archives/edgar/data/1759509/000162828026071225/lyft-20260930.htm). Ряд сохранён в [LYFT_QUARTERLY_OPERATING_SERIES_2026-11-23.csv](LYFT_QUARTERLY_OPERATING_SERIES_2026-11-23.csv).

`Operating cash flow` и `SBC` за Q2/Q3 рассчитаны как разница между накопленным YTD и предыдущим кварталом. Поэтому это не «прямое» раскрытие за квартал, а воспроизводимая производная. `OCF less SBC` — диагностический proxy качества cash conversion, не GAAP FCF: в нём ещё остаются оборотный капитал, страховые резервы, capex и другие статьи.

## Изменение картины

- Выручка выросла с `$1.28bn` в Q1 2024 до `$1.82bn` в Q3 2026; Q3 2026 к Q3 2025 — около `+8%`.
- Operating income остаётся нестабильным: Q2 2026 был `+$47.6m`, но Q3 2026 снова `-$19.4m`.
- OCF в Q3 2026 составил около `$328.4m`, а после вычитания SBC — около `$274.5m`. Это поддерживает тезис о денежной генерации, но не доказывает устойчивый FCF на акцию.
- Diluted shares снизились с `424.0m` в Q1 2025 до `378.5m` в Q3 2026. Снижение поддерживает per-share кейс, но нужно отдельно проверить механизм buyback, timing и влияние SBC.
- В Q4 2025 reported net income резко вырос из-за крупного налогового эффекта в 10-K; этот квартал нельзя использовать как нормализованный earnings run-rate.

## Инвестиционная интерпретация

Операционный тезис остаётся положительным: revenue и активность растут, а diluted share count снижается. Финансовый тезис не закрыт: operating income проваливается в отрицательную зону в Q3 2026, а OCF less SBC ещё не является нормализованным FCF. Поэтому статус не меняется: `wait`, starter возможен только после проверки нормализованного FCF и оценки против Uber.

## Decision Card

| Поле | Решение |
|---|---|
| Статус | `wait` |
| Уверенность | `medium` |
| Рабочий диапазон | `$14–18` bear / `$18–23` base / `$23–30` bull; не target price |
| Максимальная доля | до `3%` только после normalized-FCF gate |
| Главный риск | рост bookings не превращается в устойчивую прибыль на акцию после SBC, incentives и страховых резервов |
| Условие отмены тезиса | два последовательных квартала замедления riders/booking вместе со снижением take rate и OCF less SBC |
| Ближайший катализатор | следующий filing: riders, gross bookings, operating income, OCF, SBC, diluted shares |
| Следующий пересмотр | после следующего квартального filing или не позднее 15.02.2027 |

## Что ещё нужно

1. Получить capex и полный FCF bridge из 10-Q/10-K, а не подменять FCF proxy.
2. Разложить снижение diluted shares на buyback, option exercises и SBC.
3. Сверить одинаковые определения LYFT/Uber: gross bookings, revenue, take rate, contribution margin.
4. Обновить valuation snapshot через EV/revenue и normalized FCF yield.
