# Lyft (NASDAQ: LYFT) — research brief

**Дата среза:** 19 ноября 2026. **Статус:** `Research candidate / watchlist`. Цена закрытия 18 ноября: `$17.60`; market cap по secondary market data около `$6.65bn`.

## Операционный baseline

В 2025 Lyft показала выручку около `$6.316bn`, что на `9%` выше 2024; рост был связан прежде всего с увеличением rides на `14%` и active riders. Источник — официальный 10-K: <https://investor.lyft.com/financials/sec-filings/content/0001628280-26-006960/lyft-20251231.htm>.

В отчёте за III квартал 2026 раскрыты active riders `31.6m` (+10% г/г), rides `273.5m` (+10%), gross bookings `$5.6169bn` (+17%), revenue `$1.8218bn` (+8%), adjusted EBITDA `$203.9m` и margin `3.6%` от gross bookings. Q3 operating cash flow составил `$328.4m`, FCF `$294.7m`; Q4 guidance — gross bookings `$5.74–5.94bn`, adjusted EBITDA `$188–213m`. Источники: [IR Q3 2026](https://investor.lyft.com/news-events-presentations/press-releases/detail/210/lyft-reports-strong-q3-2026-results), [10-Q](https://investor.lyft.com/financials/sec-filings/content/0001628280-26-071225/lyft-20260930.htm).

Качество FCF требует нормализации: за 9M 2026 OCF составил `$986.0m`, но в нём были существенные изменения insurance reserves и accrued liabilities; SBC составил `$217.3m`. Incentive expense в sales & marketing вырос до `$599.4m` против `$312.1m` годом ранее. В Q3 revenue была снижена на `$69.1m` из-за legal/tax/regulatory reserve changes, а `$117.9m` таких изменений было исключено из adjusted EBITDA. Поэтому P/E и headline FCF yield нельзя использовать без bridge.

## Ownership / инвесторы

В proxy/SEC-материалах 2026 среди держателей свыше 5% указаны Ameriprise, Vanguard, Millennium, AQR и Fidelity; в таблице также раскрыты менеджмент и директорский пакет. Источник: <https://www.sec.gov/Archives/edgar/data/1759509/000162828026022374/lyft-20260331.htm>.

Для текущей картины инвесторов использовать свежие Schedule 13G/A из IR, а не старый ownership aggregator: <https://investor.lyft.com/financials/sec-filings>.

## Инвестиционная гипотеза

Lyft может быть интересна как marketplace с растущими rides/active riders и операционным рычагом, если take rate, contribution margin и FCF улучшаются без чрезмерного роста incentives и stock-based compensation.

### Bull

- active riders и rides растут быстрее расходов;
- adjusted EBITDA margin расширяется;
- FCF становится устойчивым и используется для buybacks/снижения dilution;
- международное расширение не ухудшает unit economics.

### Base

- выручка растёт, но маржа остаётся умеренной;
- конкуренция с Uber ограничивает pricing power;
- valuation зависит от нормализации FCF, а не от headline revenue growth.

### Bear

- ride growth замедляется;
- subsidies, insurance и regulatory costs сжимают contribution margin;
- stock-based compensation и buybacks не дают расти FCF на акцию.

## Мультипликаторы для dashboard

- `EV/Sales` — основной screening multiple;
- `EV/Adjusted EBITDA` — только с одинаковым определением EBITDA;
- `FCF yield` — после проверки, не содержит ли FCF разовых изменений оборотного капитала;
- `Revenue per active rider`, `gross bookings per ride`, `take rate`, `Adjusted EBITDA / gross bookings`;
- P/E не использовать без нормализации разовых налоговых эффектов и GAAP/non-GAAP reconciliation.

## Предварительное решение

`Research candidate`, но не автоматическая покупка. Следующий gate — собрать quarterly time series rides, active riders, gross bookings, revenue, take rate, insurance costs, SBC и diluted shares, затем сравнить Lyft с Uber по одинаковым определениям.

## Decision Card — 19 ноября 2026

| Поле | Решение |
|---|---|
| `decision_status` | `wait` (starter до 1% только после normalised FCF gate) |
| `confidence` | `medium` |
| `valuation_range` | рабочий сценарный диапазон `$14–$23/акцию`; не target price, пока не вычтены SBC/WC/legal one-offs |
| `max_position_pct` | до `3%` после прохождения operating/valuation gates |
| `main_risk` | рост rides может не превращаться в FCF из-за insurance, incentives, SBC и конкуренции |
| `thesis_invalidation` | замедление active riders при сжатии take rate/contribution margin и ухудшении FCF |
| `next_catalyst` | следующий квартальный отчёт и обновление rides, gross bookings, adjusted EBITDA и FCF |
| `next_review_date` | `2027-02-15` |
