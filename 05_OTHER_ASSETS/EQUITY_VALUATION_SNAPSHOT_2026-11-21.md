# Public-equity valuation snapshot — 21 November 2026

**Назначение:** единая screening-таблица для ZNTL, LYFT и GPRO. Это не fair-value model и не торговая рекомендация.

## Сводка

| Актив | Подходящая база | Текущий reference | Рабочий диапазон | Статус |
|---|---|---:|---:|---|
| ZNTL | cash / net cash + clinical scenarios | $1.36/share | $0.40–$6.00+ | `wait`, binary biotech |
| LYFT | EV/Sales + normalized FCF | $17.60/share | $14–$30 | `wait`, operating gate |
| GPRO | probability-weighted merger / break value | $0.581/share | $0.05–$1.20+ | `wait`, financing gate |

## ZNTL — cash is a floor reference, not liquidation value

Последний 10-Q: cash, equivalents и marketable securities $228.9m, reported liabilities $65.3m, shares 98.265863m. Простые ориентиры:

```text
cash/share = 228.9m / 98.265863m ≈ $2.33
cash minus liabilities per share = (228.9m - 65.3m) / 98.265863m ≈ $1.67
```

При цене $1.36 эти показатели выглядят низкими относительно баланса, но cash будет расходоваться на DENALI, ASPENOVA и operating costs. Поэтому нельзя превращать $2.33 в target price. Корректная модель — clinical probability × commercial value − future burn − dilution.

## LYFT — multiple требует FCF bridge

Reference market cap около $6.65bn и EV около $6.14bn. При annualized/TTM revenue около $6.91bn:

```text
EV / Sales ≈ 0.89×
```

Headline TTM FCF около $1.129bn даёт screening price/FCF около 5.9×. Но Q3-2026 FCF включает working-capital and reserve effects, а 9M 2026 SBC составил $217.3m. Поэтому 5.9× нельзя считать устойчивой доходностью без нормализации SBC, insurance, incentives и legal/tax adjustments.

## GPRO — headline spread не равен expected return

Reference market cap около $125.7m, debt около $92.2m, cash около $33.5m; грубый EV — около $184.4m. При revenue около $501.9m:

```text
EV / Sales ≈ 0.37×
```

Этот multiple не является аргументом покупки, потому что equity value зависит от закрытия Starman merger, financing commitment, covenant waivers, $10m termination fee и post-merger 10% residual stake. До подтверждения commitment letter и pro forma cap table probability-weighted value не присваивается.

## Decision Card для valuation-layer

| Актив | Статус | Max | Главный valuation-риск | Следующий gate |
|---|---|---:|---|---|
| ZNTL | `wait` | 0.5% | clinical outcome и будущая dilution съедят cash/share | DENALI Part 2c/topline |
| LYFT | `wait` | 3% после gate | headline FCF не нормализован | quarterly FCF/SBC/insurance bridge |
| GPRO | `wait` | 1% special situation | merger/financing failure и residual dilution | commitment letter 25.11 |

## Ограничения

- Market cap и цены — secondary market snapshots на 18–19 ноября 2026.
- EV использует упрощённую формулу и не заменяет полный debt/cash reconciliation.
- Сценарные диапазоны не являются статистическими доверительными интервалами.
- Для ZNTL нет зрелого revenue multiple; для GPRO нельзя использовать обычный P/E до закрытия сделки.
- Для LYFT reported FCF и normalized FCF должны показываться раздельно.
