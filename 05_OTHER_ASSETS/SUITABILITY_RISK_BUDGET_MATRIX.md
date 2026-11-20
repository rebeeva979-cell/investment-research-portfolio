# Единый suitability / risk-budget шаблон

Дата рабочей версии: 19.11.2026. Статусы отражают качество тезиса и данных, а не сигнал к немедленной сделке.

| Актив | Роль | Основной риск | Временный max | Статус | Что нужно до `buy/add` | Отмена тезиса / trim | Следующий пересмотр |
|---|---|---|---:|---|---|---|---|
| LTC | network / payments | слабый рост реального спроса, майнинг и конкуренция | 3% | `wait` | blocks, fees, active addresses, transfer value, mining economics, peer comparison | usage не растёт при росте оценки; ухудшение security/ликвидности | 7 дней после обновления on-chain |
| ETHFI | DeFi protocol / token value accrual | unlocks, dilution, рестейкинг и отсутствие value capture для ETHFI | 2% | `wait` | TVL, users, fees, revenue, expenses/incentives, unlock schedule, holders, governance | revenue/retention падают, unlock опережает спрос, token utility не подтверждена | еженедельно |
| LYFT | public equity / operating turnaround | конкуренция, take rate, FCF quality, регуляторика | 3% | `wait` | latest 10-Q/10-K, active riders, rides, take rate, adjusted EBITDA→FCF bridge, cash/debt, valuation | нормализованный FCF не подтверждается или downside превышает budget | после следующего отчёта |
| ZNTL | clinical biotech / binary event | clinical/regulatory failure, cash runway, dilution | 0.5% | `wait` | актуальный filing, cash runway, pipeline milestones, trial design, catalyst calendar, scenario loss | отрицательные данные испытаний, runway < catalyst, новая эмиссия без финансирования | перед каждым clinical catalyst |
| GPRO | special situation equity | сделка/слияние, долг, waiver, residual ownership и ликвидность | 1% | `wait` | merger terms, debt waivers, cap table, residual value, downside case, event timing | сделка срывается и downside не покрывается cash/assets; ликвидность исчезает | после каждого filing/event |

## Decision Card — обязательные поля

Для любого `buy/add/hold/trim/avoid/wait` заполняются:

- действие и дата;
- уровень уверенности (`low / medium / high`);
- диапазон оценки или сценариев (`bear / base / bull`);
- максимальная доля и сумма риска;
- главный риск и что рынок может недооценивать;
- условие отмены тезиса;
- ближайший катализатор;
- источник и дата каждого ключевого показателя;
- дата следующего пересмотра.

Если цена или текущая доля неизвестны, карточка не может завершиться `buy/add`; корректный статус — `wait`.

## Как применять к портфелю

1. Сначала рассчитывается фактическая доля позиции от ликвидного капитала, а не от суммы внесённых денег.
2. Затем проверяется suitability: горизонт, ликвидность, capacity/willingness to risk и концентрация коррелированных активов.
3. Только после этого сравниваются valuation и upside.
4. Новый взнос направляется сначала в недостающий core, а не в актив с нарушенным лимитом.
5. Все исключения попадают в журнал отклонений IPS с причиной и датой пересмотра.
