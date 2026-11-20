# Ether.fi (ETHFI) — Financial & Tokenomics Model

**Статус:** Baseline loaded / cost and on-chain execution reconciliation pending. Срез: 16 ноября 2026 UTC.

## 1. Основное правило

Нельзя смешивать следующие понятия:

```text
TVL ≠ gross fees ≠ protocol revenue ≠ net earnings ≠ ETHFI holder cash flow
```

Каждый слой должен быть отдельным полем и отдельной строкой в модели.

## 2A. Observed baseline

| Метрика | Срез | Интерпретация |
|---|---:|---|
| Parent TVL | `$3.85bn` | Капитал в экосистеме; не выручка |
| TVL change, 7d / 30d | `-13.3% / -23.5%` | Негативный adoption-сигнал, требующий объяснения |
| Gross fees, 30d | `$14.1m` | Платежи/комиссии по методике DefiLlama |
| Protocol revenue, 30d | `$3.88m` | Агрегированная retained-revenue прокси, не audited P&L |
| Revenue capture ratio | `27.6%` | `protocol revenue / gross fees` |
| Holders revenue, 30d | `$0` | В этом окне распределение держателям не наблюдается в DefiLlama |
| Market cap / annualised protocol revenue | `10.3x` | Screening multiple без расходов и treasury reconciliation |

Следующий обязательный шаг — разложить `$3.88m` protocol revenue на operator/partner share, incentives, operating/security costs и фактические treasury inflows. Без этого `net_protocol_economics_usd` остаётся `N/A`.

## 2. Protocol operating model

### Adoption

| Блок | Метрики |
|---|---|
| Capital | TVL, eETH supply, weETH supply, deposits, withdrawals |
| Users | unique depositor wallets, active wallets, new wallets, returning wallets |
| Product mix | native staking, restaking, vaults, lending, liquidity venues |
| Retention | 7/30/90-day wallet retention, withdrawal rate, net flow |

Wallets являются proxy, а не гарантированным числом людей. Биржи, contracts и smart wallets нужно классифицировать отдельно.

### Revenue bridge

```text
Gross protocol fees
- validator / operator share
- restaking or partner share
- liquidity and referral rebates
= Protocol revenue retained
- token incentives
- grants and growth spend
- operating and security costs
= Net protocol economics
```

Для каждой строки нужно сохранять метод признания. Если источник публикует только gross fees, retained revenue нельзя выводить как равную gross fees.

### Минимальная таблица доходов

| Поле | Определение | Статус |
|---|---|---|
| `fees_gross_usd` | Все комиссии, оплаченные пользователями | Loaded: DefiLlama 30d `$14.1m` |
| `operator_share_usd` | Выплаты операторам / валидаторам | To source |
| `partner_share_usd` | Доля restaking / liquidity / partner layer | To source |
| `protocol_revenue_usd` | То, что остаётся treasury/protocol | Loaded: DefiLlama 30d `$3.88m`; reconcile required |
| `incentives_usd` | Token emissions и субсидии | To source |
| `operating_costs_usd` | Команда, инфраструктура, audits, service providers | To source |
| `net_protocol_economics_usd` | Revenue minus incentives and costs | `N/A` until cost inputs verified |

## 3. Tokenomics model

### Supply bridge

```text
Max supply
→ initial allocation
→ unlocked supply
→ circulating supply
→ scheduled unlocks
→ emissions / treasury transfers
→ effective liquid supply
```

Обязательные поля:

- `max_supply`;
- `circulating_supply`;
- `treasury_supply`;
- `team_and_investor_supply`;
- `user_allocation`;
- `unlocked_to_date`;
- `next_30d_unlock`;
- `next_12m_unlock`;
- `staking_or_governance_locked_supply`;
- `effective_float`.

### Value accrual checklist

Для ETHFI нужно отдельно проверить:

1. получает ли holder прямое распределение fees;
2. существуют ли buyback или burn и где это записано;
3. даёт ли staking токена право на доход или только governance utility;
4. имеет ли governance право менять комиссии, treasury или emissions;
5. есть ли обязательное, а не только возможное, использование ETHFI;
6. могут ли unlocks и treasury transfers создать sell pressure.

Если механизм не закреплён контрактом, официальным документом или governance decision, классифицировать его как `unconfirmed`.

## 4. Valuation framework

### Market metrics

- `market_cap = price × circulating_supply`;
- `FDV = price × max_supply`;
- `unlock_adjusted_FDV = price × effective_float_or_next_supply_scenario`.

### Multiples

```text
Market Cap / Gross Fees
Market Cap / Protocol Revenue
FDV / Protocol Revenue
Market Cap / Net Protocol Economics
TVL / Market Cap
```

Не использовать multiple, если numerator и denominator имеют разные даты или разные definitions.

### Scenario table

| Сценарий | TVL | Revenue margin | Annual protocol revenue | Token supply | Multiple | Implied value |
|---|---:|---:|---:|---:|---:|---:|
| Bear | input | input | formula | unlock-adjusted | input | formula |
| Base | input | input | formula | scheduled | input | formula |
| Bull | input | input | formula | controlled dilution | input | formula |

Сценарии не должны выдавать точную цену без диапазона, чувствительности и списка предпосылок.

## 5. Data model

```text
raw_protocol_events
raw_token_transfers
raw_tvl_fees
raw_market_data
raw_unlock_schedule
        ↓
staging_ethfi_daily
        ↓
ethfi_protocol_economics_daily
ethfi_supply_unlocks
ethfi_holder_distribution
ethfi_valuation_scenarios
```

Каждый mart должен иметь `as_of_date`, `source_id`, `method` и `quality_status`.

## 6. Minimum dashboard pages

1. Adoption: TVL, net flows, product mix, users.
2. Economics: gross fees, protocol revenue, incentives, net economics.
3. Tokenomics: supply, unlocks, effective float, holder concentration.
4. Valuation: market cap, FDV, multiples, scenario range.
5. Risks: incidents, concentration, liquidity, slashing, governance.
6. Weekly changes: what changed and whether thesis strengthened or weakened.
