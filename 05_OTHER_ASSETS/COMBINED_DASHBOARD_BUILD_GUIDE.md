# Combined Investment Research Dashboard

## Страницы

1. **Decision overview** — статус, conviction, основной тезис, текущая оценка, следующий катализатор.
2. **Market & valuation** — price, market cap/EV, EV/Sales, EV/EBITDA, FCF yield, FDV/revenue, market cap/TVL.
3. **Operating economics** — revenue bridge, gross fees/protocol revenue, TVL, riders, rides, cameras, subscribers, FCF.
4. **Ownership & tokenomics** — insiders, institutions, voting power, allocation, unlocks, circulating/max supply.
5. **Risk & catalysts** — risk score, falsifiers, events, source links.
6. **Weekly change** — что изменилось за 7 дней и усилило или ослабило тезис.

7. **Macro & flows** — SPY, DXY, USDT peg/market cap и BTC/ETH ETF net flows.

## Looker-ready seed tables

- `ASSET_MASTER.csv` — список активов, статус и лимит позиции;
- `VALUATION_SNAPSHOT.csv` — каркас мультипликаторов и дата проверки;
- `OWNERSHIP_AND_VALUATION_SEED.csv` — первичные investor/financial rows для GPRO и LYFT;
- `RISK_CATALYST_LOG.csv` — катализаторы, риски и falsifiers.
- `MARKET_MACRO_DAILY.csv` и `MARKET_MACRO_KPI_LATEST.csv` — SPY, DXY, GPRO, LYFT, USDT;
- `ETF_FLOWS_DAILY.csv` — BTC/ETH ETF flows в `$m`.
- `ANTHROPIC_RESEARCH_BRIEF.md` и `ANT_Anthropic_Calculator.html` — IPO valuation ladder, run-rate/TTM revenue sensitivity, dilution и compute-risk gates.

Подключай каждый CSV отдельным источником, а затем объединяй через `asset_id`. Пустые valuation-поля не заполнять оценками «на глаз» — сначала загрузить market cap/EV и дату.

## Минимальные карточки по активам

### GoPro (GPRO)

- `case_type = special_situation`, а не обычный growth/value stock;
- отдельно показать merger consideration `$1.14/share`, вероятность закрытия и residual 10% ownership;
- выручка, camera units, subscription revenue, cash, debt и covenant/default risk;
- не строить P/E на убыточной отчётности; использовать probability-weighted deal value и downside-to-liquidation.

### Lyft (LYFT)

- rides, active riders, gross bookings, revenue, adjusted EBITDA, FCF;
- take rate и contribution margin, чтобы не путать рост rides с ростом прибыли;
- institutional ownership и voting structure из SEC proxy/13G;
- EV/Sales, EV/Adjusted EBITDA и FCF yield; P/E только после нормализации разовых налоговых эффектов.

### Anthropic (ANT)

- revenue run-rate отдельно от фактической TTM revenue;
- basic / option-adjusted / fully diluted share count;
- IPO price, derivative mark и sensitivity по revenue multiple;
- compute commitments, governance control, dilution и first-quarter gates;
- `ANTUSDT` на Bybit показывать как derivative, не как Nasdaq equity quote.

### Криптопроекты

- TVL отдельно от fees/revenue;
- supply/unlocks и holder value accrual на отдельной странице;
- market cap и FDV всегда показывать рядом;
- без подтверждения on-chain исполнения buybacks/distributions — `value_accrual_status = policy_only`.

## Типы полей

- `date` — Date;
- `_usd` — Currency USD;
- `_pct` — Number в процентных пунктах;
- `return`, `drawdown`, `yield` — Percent;
- `shares`, `tokens`, `rides`, `active_riders`, `subscribers`, `cameras_shipped` — Number;
- `quality_status`, `source_url`, `source_id` — Text.

## Правило решения

Dashboard не выдаёт «купить» автоматически. Он выдаёт `watchlist`, `research_candidate`, `special_situation`, `avoid` или `position_review`, а окончательное решение опирается на тезис, сценарии, рисковый бюджет и дату последней проверки.

## Как читать macro & flows

- DXY и SPY — контекст ликвидности и risk appetite, не самостоятельный сигнал по токену.
- USDT около `$1` — не равно подтверждению резервов; отслеживать peg deviation, market cap и mint/burn отдельно.
- ETF flow `Total` — дневной net flow в `$m`; пустое значение означает «данные ещё не опубликованы», а не нулевой поток.
- Farside используется как независимый потоковый источник; дату и метод extraction сохранять в source register.
