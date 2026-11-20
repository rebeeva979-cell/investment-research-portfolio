# Investment Research Portfolio — Casebook

**Версия:** 20 ноября 2026
**Позиционирование:** Junior Investment Research / Crypto & Digital Assets Analyst
**Важно:** это учебно-практическое портфолио и decision-support research, а не управление чужими деньгами и не персональная рекомендация.

## Как читать портфолио

Каждый кейс отвечает не на вопрос «какую монету купить», а на вопрос:

> какое действие допустимо при текущих данных и заданном risk budget?

В каждом кейсе есть пять слоёв:

1. Investment question — какой вопрос проверяем.
2. Evidence — какие данные и источники нужны.
3. Model — как считаем экономику, valuation и риск.
4. Decision Card — действие, уверенность, лимит и отмена тезиса.
5. Reproducibility — dashboard, SQL/Python, source register и дата обновления.

## Сводная карта кейсов

| Кейс | Что демонстрирует | Главный артефакт | Текущий статус | Временный max |
|---|---|---|---|---:|
| [LTC — Network & Market Research](../01_LTC/LTC_RESEARCH_MEMO.md) | on-chain activity, PoW security, supply, mining economics, drawdown и peer analysis | [LTC Dashboard](../01_LTC/LTC_Dashboard.html) + workbook | `wait` | 3% |
| [ETHFI — Protocol Economics & On-chain Verification](../04_ETHFI/ETHFI_ONCHAIN_VERIFICATION_2026-11-20.md) | buyback ≠ burn ≠ dividend; treasury/vesting/CEX labeling; supply reconciliation; DEX depth | verification report + 4-page bilingual case + CSVs/SVG | `wait` | 2% |
| [LYFT — Marketplace Unit Economics](../05_OTHER_ASSETS/LYFT_RESEARCH_BRIEF.md) | rides, active riders, take rate, adjusted EBITDA и нормализация FCF | SEC/IR brief + valuation seed | `wait` | 3% |
| [ZNTL — Clinical Risk & Runway](../05_OTHER_ASSETS/ZNTL_RESEARCH_BRIEF.md) | binary clinical risk, cash runway, burn, dilution и scenario valuation | clinical investment brief | `wait` | 0.5% |
| [GPRO — Special Situation](../05_OTHER_ASSETS/GPRO_RESEARCH_BRIEF.md) | deal probability, debt/covenants, residual ownership и downside | merger/deal-risk brief | `wait` | 1% |
| [ANT — AI IPO Valuation](../05_OTHER_ASSETS/ANTHROPIC_RESEARCH_BRIEF.md) | revenue run-rate vs TTM, dilution, compute commitments и IPO microstructure | [ANT calculator](../05_OTHER_ASSETS/ANT_Anthropic_Calculator.html) + IPO brief | `wait` | 0.5% |
| [SNX — SIP-423 Supply Overhang](../02_SNX/SNX_SIP423_RESEARCH_REPORT_2026-11-19.md) | real mint, Safe custody, lock enforceability, unlock scenarios и market-cap methodology | [SNX report](../02_SNX/SNX_SIP423_RESEARCH_REPORT_2026-11-19.md) + data pack | `defensive / research` | 0% now |

Общий слой: [Macro & ETF Flows](../05_OTHER_ASSETS/COMBINED_DASHBOARD_BUILD_GUIDE.md) — SPY, DXY, USDT, BTC/ETH ETF flows и weekly change.

---

## Case 1 — LTC: Network & Market Research

### Investment question

Сохраняется ли тезис Litecoin как платёжной Proof-of-Work сети, если рыночная оценка, адресная активность, комиссии, эмиссия и доходность майнеров рассматриваются вместе?

### Что исследовано

- daily market data, MA, returns, volatility и drawdowns;
- active addresses и transactions как proxy adoption;
- blocks, difficulty, block interval и hashrate;
- supply, issuance, halving context и remaining supply;
- gross transfer value и output metrics с оговоркой о change/self-transfers;
- fees, subsidy revenue, gross miner revenue и fee share;
- MVRV/realized-cap proxy и peers BTC/BCH/DOGE/DASH.

### Что демонстрирует работодателю

Умение не подменять пользователей адресами, выручку gross transfer value, а валовую выручку майнеров — прибылью. Также показывает полный цикл: data extraction → data quality → dashboard → investment memo → decision gates.

### Decision Card

| Поле | Текущее решение |
|---|---|
| Статус | `wait` |
| Уверенность | `medium` |
| Временный max | 3% ликвидного портфеля |
| Главный риск | сеть может оставаться безопасной, но реальный платёжный спрос и fee economics — слабыми |
| Отмена тезиса | ухудшение security/activity при отсутствии подтверждённого спроса |
| Следующий катализатор | новый on-chain snapshot и peer comparison |

### Артефакты

- [LTC research memo](../01_LTC/LTC_RESEARCH_MEMO.md)
- [LTC Looker build guide](../01_LTC/LOOKER_STUDIO_BUILD_GUIDE.md)
- [LTC standalone dashboard](../01_LTC/LTC_Dashboard.html)
- [LTC dataset](../01_LTC/LTC_LOOKER_DATASET.xlsx)

---

## Case 2 — ETHFI: Protocol Economics & On-chain Value Accrual

### Investment question

Растёт ли ether.fi как бизнес достаточно качественно, чтобы рост протокола отражался в стоимости ETHFI, и доходит ли документированный buyback до держателя — или остаётся внутри структур протокола?

### Что проверено on-chain

- **Buyback исполняется:** 566 сделок CoW, 2,542,499 ETHFI за $1,645,541, средняя $0.6472, период 17.09–20.11.2026; 30 дней — 1,155,696 ETHFI / $663,000.
- **Маршрут:** Funding Safe `0xf40bcc…f7021` → Buyback Safe `0x43f4ca…6408c` → CoW `0x9008D1…0ab41`; 2,054,374 ETHFI ушло на EOA `0x9eaC71…843f`, 893,950 — в LZMultiCall `0xAcdDAC…c05f1` (LayerZero/Optimism).
- **До держателя не дошло:** ни один ETHFI с buyback Safe не ушёл в sETHFI; holder revenue = $0 с 1 апреля 2026; распределение cashback на Optimism не подтверждено до адресов получателей.
- **Политика vs поток:** buyback/revenue = 17.3% за 30 дней против 30% на buyback (60% с cashback, который не подтверждён); annualised $7.96M = 1.71% market cap; 1.16M ETHFI/мес покрывает ~26% разлоков.
- **Supply:** on-chain 998,535,999; burn 1,464,001 через `burn()`; CoinGecko считает total как circulating; DefiLlama — 983,600,557 + 16,399,443 locked = 1B. Расхождение ~1.5% float.
- **Концентрация:** top-10 62.19%, top-5 45.84%; treasury Safe 15.34%, sETHFI 10.92%, CEX 13.94%; EOA float 47.5%, top-1 EOA 21.4% float; Gini 0.805, HHI 761, Nakamoto 5.
- **Ликвидность:** $1.23M видимой DEX-глубины (0.26% mcap); $250k продажа — −38.8% по QuoterV2.
- **Экономика:** TVL $3.73B, −70.9% от пика; mcap/revenue 10.73×, mcap/TVL 0.125×; сценарии Bear/Base/Bull $0.228 / $0.435 / $0.730.

### Что демонстрирует работодателю

Полный цикл on-chain forensic research: от адреса и транзакции до policy-vs-flow вывода, supply reconciliation, концентрации, микроструктуры и Decision Card. Ключевой навык — не принимать «buyback» за «holder yield» и показывать, где заканчиваются данные и начинается интерпретация.

### Decision Card

| Поле | Текущее решение |
|---|---|
| Статус | `wait` |
| Уверенность | `high` в исполнении buyback; `low` в распределении держателям |
| Временный max | 0–2% ликвидного портфеля |
| Горизонт | 3–6 месяцев |
| Главный риск | buyback — customer-acquisition расход, а не yield; TVL и revenue продолжают сжиматься; 156M ETHFI у allocation/vesting EOA |
| Апгрейд | buyback уходит в sETHFI/holders или burn с проверяемыми tx; TVL >$4.5B 30 дней с ростом revenue; подтверждённый cashback >$1M с адресами |
| Отмена | treasury/allocation EOA отправляют >5% float на CEX; buyback останавливается >30 дней; TVL <$3B или revenue <$2.5M/30 дней |
| Почему не short | реальный механический bid, тонкий float, стоимость заимствования и squeeze-риск не измерены |

### Артефакты

- [On-chain verification report](../04_ETHFI/ETHFI_ONCHAIN_VERIFICATION_2026-11-20.md)
- [Interactive bilingual case](../docs/ethfi.html)
- [Methodology](../docs/method.html)
- [Investment thesis](../04_ETHFI/ETHFI_INVESTMENT_THESIS.md)
- [Financial & Tokenomics Model](../04_ETHFI/ETHFI_FINANCIAL_TOKENOMICS_MODEL.md)
- [Risk Assessment](../04_ETHFI/ETHFI_RISK_ASSESSMENT.md)
- [Metrics CSV](../docs/data/ethfi_metrics.csv) · [Holders CSV](../docs/data/ethfi_holders_top.csv) · [Buybacks CSV](../docs/data/ethfi_buybacks_daily.csv) · [Scenarios CSV](../docs/data/ethfi_valuation_scenarios.csv)

---

## Case 3 — LYFT: Marketplace Unit Economics

### Investment question

Превращается ли рост rides и active riders в устойчивый FCF на акцию после insurance, incentives, stock-based compensation и разовых изменений оборотного капитала?

### Что исследовано

- active riders, rides, gross bookings и revenue;
- take rate, contribution economics и adjusted EBITDA;
- operating cash flow и FCF bridge;
- SBC, insurance reserves, incentives и legal/tax one-offs;
- cash, debt, ownership и valuation multiples;
- bull/base/bear сценарии и operating invalidation triggers.

### Что демонстрирует работодателю

Способность не принимать adjusted EBITDA или headline FCF за чистую экономику бизнеса. Кейс связывает операционные KPI с денежным потоком и valuation.

### Decision Card

| Поле | Текущее решение |
|---|---|
| Статус | `wait`; starter до 1% только после normalised FCF gate |
| Уверенность | `medium` |
| Временный max | 3% после operating и valuation gates |
| Главный риск | рост rides не превращается в FCF из-за insurance, incentives, SBC и конкуренции |
| Отмена тезиса | замедление riders вместе со сжатием take rate/contribution margin и FCF |
| Следующий катализатор | следующий квартальный отчёт и обновление unit economics |

### Артефакты

- [LYFT research brief](../05_OTHER_ASSETS/LYFT_RESEARCH_BRIEF.md)
- [combined dashboard specification](../05_OTHER_ASSETS/COMBINED_DASHBOARD_BUILD_GUIDE.md)
- [ownership and valuation seed](../05_OTHER_ASSETS/OWNERSHIP_AND_VALUATION_SEED.csv)

---

## Case 4 — ZNTL: Clinical Risk, Runway & Dilution

### Investment question

Создаёт ли cash runway и клинический pipeline достаточно привлекательную асимметрию, чтобы оправдать binary clinical/regulatory risk и вероятность будущего dilution?

### Что исследовано

- cash, marketable securities, liabilities и operating burn;
- runway до ключевого readout;
- clinical program, endpoints, biomarker и regulatory path;
- share count и влияние follow-on offering;
- bear/base/bull сценарии вместо P/E или обычного DCF;
- catalyst calendar и условия отмены тезиса.

### Что демонстрирует работодателю

Умение анализировать pre-revenue biotech через cash-per-share, runway, clinical probability и dilution, а не через неподходящие мультипликаторы.

### Decision Card

| Поле | Текущее решение |
|---|---|
| Статус | `wait` |
| Уверенность | `medium` в оценке риска; `low` в upside |
| Временный max | 0.5%; до 1% только отдельная clinical sleeve |
| Главный риск | неубедительный clinical readout и последующее dilution |
| Отмена тезиса | отсутствие clinically meaningful benefit, остановка программы или дорогая эмиссия |
| Следующий катализатор | DENALI readout и новые financing disclosures |

### Артефакты

- [ZNTL research brief](../05_OTHER_ASSETS/ZNTL_RESEARCH_BRIEF.md)
- [ZNTL / LYFT / GPRO cases](../05_OTHER_ASSETS/ZNTL_LYFT_GPRO_INVESTMENT_CASES.md)
- [risk and catalyst log](../05_OTHER_ASSETS/RISK_CATALYST_LOG.csv)

---

## Case 5 — GPRO: Merger Special Situation

### Investment question

Какова вероятность закрытия сделки и сколько реально стоит заявленная cash consideration плюс residual ownership после учёта debt, covenants, financing conditions и dilution?

### Что исследовано

- merger consideration и spread к рыночной цене;
- conditions precedent, closing deadline и commitment letter;
- cash, debt, covenant waivers и going-concern disclosures;
- hardware revenue, camera units и subscription revenue;
- residual ownership и post-merger cap table;
- probability-weighted downside вместо headline spread.

### Что демонстрирует работодателю

Умение разбирать special situation как событие и структуру капитала, а не как обычную growth-акцию. Центральный объект анализа — вероятность сделки и остаточная стоимость, а не P/E.

### Decision Card

| Поле | Текущее решение |
|---|---|
| Статус | `wait / watchlist only` |
| Уверенность | `medium` |
| Временный max | 1% special-situation budget |
| Главный риск | срыв/перенос сделки, covenant/default pressure и размывание residual stake |
| Отмена тезиса | отсутствие closing на согласованных условиях или резкое ухудшение cash/debt |
| Следующий катализатор | новый 8-K, waiver/commitment-letter update и pro forma cap table |

### Артефакты

- [GPRO research brief](../05_OTHER_ASSETS/GPRO_RESEARCH_BRIEF.md)
- [combined dashboard specification](../05_OTHER_ASSETS/COMBINED_DASHBOARD_BUILD_GUIDE.md)
- [risk and catalyst log](../05_OTHER_ASSETS/RISK_CATALYST_LOG.csv)

---

## Case 6 — ANT: AI IPO Valuation & Revenue-Multiple Calculator

### Investment question

Какую цену можно обосновать при разных определениях выручки и share count, и когда рост Anthropic превращается из run-rate story в доказанную публичную экономику?

### Что исследовано

- `$81bn` run-rate против `$35.3bn` TTM;
- basic, option-adjusted и fully diluted share bases;
- IPO price `$83` против Bybit ANTUSDT derivative mark;
- sensitivity 10–30× revenue run-rate;
- dilution, Class F control, compute commitments и IPO volatility.

### Что демонстрирует работодателю

Способность превратить сложный IPO narrative в прозрачный калькулятор, явно разделить фактическую выручку и run-rate, а также показать, почему headline valuation нельзя принимать без dilution и unit-economics gates.

### Decision Card

| Поле | Текущее решение |
|---|---|
| Статус | `wait`; в день IPO не использовать большое плечо |
| Уверенность | `medium` в рисках; `low–medium` в оценке |
| Временный max | 0.5% satellite до первых двух публичных отчётов |
| Главный риск | рынок капитализирует run-rate, а маржа, FCF и compute economics не доказаны |
| Отмена тезиса | замедление revenue вместе с ухудшением margin/FCF и ускорением dilution |
| Следующий катализатор | first trade, price discovery и первый квартальный отчёт |

### Артефакты

- [ANTHROPIC research brief](../05_OTHER_ASSETS/ANTHROPIC_RESEARCH_BRIEF.md)
- [ANT calculator](../05_OTHER_ASSETS/ANT_Anthropic_Calculator.html)
- [SEC final prospectus](https://www.sec.gov/Archives/edgar/data/2130357/000162828026074944/anthropicpbc-424b4.htm)

---

## Case 7 — SNX: SIP-423 Supply Overhang & On-chain Verification

### Investment question

Является ли рост supply после SIP-423 реальной эмиссией и насколько надёжен lock, если новые токены лежат в Safe multisig, а protocol fees и TVL остаются низкими?

### Что исследовано

- `totalSupply()` до и после mint;
- 236.46 млн SNX, переведённые в один Safe;
- отсутствие исходящих SNX-переводов на дату среза;
- SIP terms: 1-year lock, 1-year vest, claim window и неопределённость unclaimed treatment;
- разницу между reported circulating market cap и pre-mint comparison basis;
- fees, TVL, revenue hurdle и дисконт claim value;
- сценарии unlock pressure и условия отмены тезиса.

### Что демонстрирует работодателю

Умение проверить токеномику не по агрегатору, а через RPC calls, Transfer logs, Safe custody и governance-документ. Кейс показывает разницу между «токены находятся в multisig» и trustless vesting-контрактом.

### Decision Card

| Поле | Текущее решение |
|---|---|
| Статус | `defensive / research`; не покупать сейчас |
| Уверенность | `high` в факте mint; `medium` в будущей реализации lock/claim |
| Временный max | 0%; до 0.5% только после отдельного gate |
| Главный риск | 40.67% post-mint supply сосредоточено в Safe, а revenue/TVL не дают достаточной поддержки |
| Отмена тезиса | receipt contract, lock mechanics и revenue hurdle не подтверждены или unlock выходит на рынок раньше спроса |
| Следующий катализатор | deployment receipt contract, governance updates и приближение claim window в 2027 |

### Артефакты

- [SNX research report](../02_SNX/SNX_SIP423_RESEARCH_REPORT_2026-11-19.md)
- [SNX HTML report](../02_SNX/SNX_SIP423_RESEARCH_REPORT_2026-11-19.html)
- [SNX data pack](../02_SNX/SNX_SIP423_DATA_PACK.xlsx)
- [SNX research brief](../02_SNX/SNX_SIP423_RESEARCH_BRIEF.md)

---

## Общий Macro & ETF Flows слой

Этот слой не является отдельным активом, а добавляет контекст к каждому кейсу:

- SPY — risk appetite и equity regime;
- DXY — долларовая ликвидность и давление на risk assets;
- USDT — peg deviation и market-cap trend, без вывода о резервах только по цене;
- BTC/ETH ETF flows — потоковый контекст, а не самостоятельный сигнал сделки.

Артефакты: [macro data](../05_OTHER_ASSETS/MARKET_MACRO_DAILY.csv), [ETF flows](../05_OTHER_ASSETS/ETF_FLOWS_DAILY.csv), [source register](../05_OTHER_ASSETS/MACRO_SOURCE_REGISTER.csv).

## Как презентовать кейсы работодателю

Для каждого кейса показать в таком порядке:

1. один investment question;
2. три ключевых графика;
3. один расчёт экономики/valuation;
4. главный риск и falsifier;
5. Decision Card с ограничением позиции;
6. ссылку на dataset, SQL и source register.

Не начинать презентацию с «актив может дать 4–6x». Начинать с качества данных, механизма создания стоимости и того, что должно быть правдой, чтобы тезис сработал.

## Что ещё добавить до публичной версии

- скриншот или публичную ссылку на каждый dashboard;
- короткий weekly update по каждому кейсу;
- один общий `README` с методикой и source policy;
- дату обновления и статус data quality на первой странице;
- disclosure: personal research, not client asset management or investment advice.
