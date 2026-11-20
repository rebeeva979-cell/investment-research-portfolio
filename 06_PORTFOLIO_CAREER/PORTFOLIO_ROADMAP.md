# Portfolio Roadmap — Investment Research / Digital Assets

## Позиционирование
Junior Investment Research / Crypto Research Analyst с сильным предпринимательским, продуктовым и партнёрским бэкграундом и примерно 5 годами самостоятельной практики управления личным инвестиционным портфелем. Личную практику не представлять как управление клиентскими средствами или работу в инвестиционном фонде.

План коммерциализации и workflow: [RESEARCH_SERVICE_AND_MONETIZATION_PLAN.md](RESEARCH_SERVICE_AND_MONETIZATION_PLAN.md).
Финансово-консультационный workflow: [FINANCIAL_CONSULTANT_WORKFLOW.md](../05_OTHER_ASSETS/FINANCIAL_CONSULTANT_WORKFLOW.md).

## Принцип портфолио
Лучше меньше, но глубже: воспроизводимые исследования с источниками, методологией, расчётами, dashboard, выводами, рисками и сценариями. Незавершённые кейсы маркировать `In Progress` / `Research Design`.

## Стандарт каждого кейса
Подробный стандарт: [INVESTMENT_RESEARCH_STANDARD.md](INVESTMENT_RESEARCH_STANDARD.md).

1. Investment Thesis.
2. Financial & Tokenomics Model.
3. Risk Assessment.
4. Research Questions и Data Sources.
5. Methodology и Data Model / SQL.
6. Dashboard как приложение.
7. Findings, scenarios и weekly update.
8. README, source register и воспроизводимость.
9. IPS / suitability gate / position sizing / review date до любого клиентского вывода.

## Список проектов
### Blockchain / Network
- LTC — adoption, supply, network activity, payments, mining economics.
- EGLD — MultiversX network, staking, tokenomics, ecosystem.
- ROSE — Oasis Network, demand, staking, tokenomics, privacy infrastructure.
- LRC — Loopring, L2 adoption, DEX activity, token economics.
- AVAIL — network / wallet / staking / token-flow intelligence dashboard.

### DeFi Protocols
- ZRX — 0x Protocol, governance, token utility/value capture.
- COMP — Compound, lending economics, TVL, fees/revenue, governance.
- UNI — Uniswap, volumes, fees, governance and value accrual.
- ETHFI — staking/restaking, protocol economics, unlocks and value accrual.
- SNX — SIP-423 supply overhang and actual mint analysis.

### Equity Research
- ZNTL — Zentalis Therapeutics: financials, cash runway, burn rate, pipeline, clinical and regulatory risk.
- GPRO — GoPro / Starman: merger probability, debt waivers, residual ownership and special-situation valuation.
- LYFT — Lyft: rides, active riders, marketplace take rate, adjusted EBITDA, FCF and institutional ownership.

## Приоритеты
1. Собрать IPS-профиль: `$300/мес` во вклад/консервативную корзину и `$1,000/мес` в инвестиционный поток; отдельно зафиксировать цель, горизонт, ликвидность, capacity/willingness to risk и максимальную просадку.
2. Применить единый suitability/risk-budget шаблон к LTC, ETHFI, LYFT, ZNTL и GPRO; до заполнения критических полей действие по новым покупкам — `wait`.
3. Довести LTC Market Overview в Looker Studio, затем расширить сетевыми данными.
4. Довести ETHFI blueprint до трёх полноценных инвестиционных документов и собрать подтверждённую data model.
5. Закончить briefs по LYFT и GPRO; ZNTL вести как clinical/special-situation кейс с отдельным лимитом.
6. Подключить Macro & ETF Flows и обновлять decision cards еженедельно.
7. Проверить и оформить SNX dashboard, затем выбрать UNI или COMP для следующего завершённого кейса по revenue/value accrual.

## Новый общий слой crypto + equity research

Файлы в `05_OTHER_ASSETS` задают единый dashboard-модель: `asset_master`, `market_daily`, `operating_daily`, `tokenomics_daily`, `ownership_snapshot`, `financials_annual`, `valuation_snapshot` и `risk_catalyst_log`. Это позволяет сравнивать не сами бизнесы напрямую, а качество тезиса, источник данных, мультипликатор и риск-бюджет.

## Карьерные направления
- Junior Crypto Research Analyst.
- Crypto / DeFi Analyst.
- On-chain Analyst.
- Investment Research Analyst.
- Research Assistant.
- Investment Operations / Portfolio Analyst.
- Market Intelligence Analyst.
- Junior Wealth / Financial Research Analyst.
- Investment Advisory / Portfolio Support Analyst.

## Принципы честного позиционирования
- Личный портфель — personal investment experience, не client asset management.
- Не завышать SQL / Dune / Power BI / Looker Studio до уровня, который не подтверждается практическими проектами.
- Отдельно обозначать спецификации, POC и завершённые исследования.
