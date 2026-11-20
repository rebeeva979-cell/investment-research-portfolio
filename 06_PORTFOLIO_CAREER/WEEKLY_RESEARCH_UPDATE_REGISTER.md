# Weekly Research Update Register

Назначение: поддерживать кейсы живыми и показывать работодателю, как меняется инвестиционный тезис после появления новых данных.

## Правило weekly update

Каждый update должен занимать не больше одной страницы и отвечать на пять вопросов:

1. Что изменилось за 7 дней?
2. Какой источник это подтверждает?
3. Тезис усилился, ослаб или не изменился?
4. Какое действие допустимо при текущем risk budget?
5. Когда следующий пересмотр и какое событие его запускает?

`No material change` — допустимый результат. Нельзя создавать активность искусственно.

## Реестр кейсов

| Актив | Частота | Следующий обязательный data check | Текущий decision state | Артефакт |
|---|---|---|---|---|
| LTC | weekly on-chain / monthly deep dive | active addresses, tx, hashrate, fees, transfer value, mining/supply | `wait` | [LTC memo](../01_LTC/LTC_RESEARCH_MEMO.md) |
| ETHFI | weekly | TVL, fees, protocol revenue, holders revenue, unlocks, buyback execution | `wait` | [ETHFI thesis](../04_ETHFI/ETHFI_INVESTMENT_THESIS.md) · [20.11 update](../04_ETHFI/ETHFI_WEEKLY_UPDATE_2026-11-20.md) · [value-accrual note](../04_ETHFI/ETHFI_VALUE_ACCRUAL_VERIFICATION_NOTE_2026-11-20.md) |
| LYFT | after each filing / monthly market | riders, rides, bookings, take rate, SBC, insurance, FCF bridge | `wait` | [LYFT brief](../05_OTHER_ASSETS/LYFT_RESEARCH_BRIEF.md) |
| ZNTL | event-driven | DENALI readout, cash burn, runway, financing and share count | `wait` | [ZNTL brief](../05_OTHER_ASSETS/ZNTL_RESEARCH_BRIEF.md) |
| GPRO | event-driven | 8-K, waiver, closing conditions, debt and post-merger cap table | `wait` | [GPRO brief](../05_OTHER_ASSETS/GPRO_RESEARCH_BRIEF.md) |
| ANT | first-trade + quarterly | price discovery, diluted shares, revenue, gross margin, FCF, compute commitments | `wait` | [ANT brief](../05_OTHER_ASSETS/ANTHROPIC_RESEARCH_BRIEF.md) |
| SNX | weekly until claim mechanics clear | Safe balance/outflows, receipt contract, SIP changes, fees, TVL, supply | `defensive` | [SNX report](../02_SNX/SNX_SIP423_RESEARCH_REPORT_2026-11-19.md) |

## Update template

```markdown
# Weekly update — ASSET — YYYY-MM-DD

## Decision
- Status: buy/add | hold | trim | avoid | wait
- Confidence:
- Position limit:
- Next review:

## What changed
- Market:
- Operating/on-chain:
- Tokenomics/ownership:
- Macro/ETF context:

## Evidence
| Metric | Previous | Current | Change | Source | Quality |
|---|---:|---:|---:|---|---|

## Thesis impact
- Strengthened:
- Weakened:
- Unchanged:

## Risk and falsifier
- Main risk:
- Thesis invalidation condition:
- Next catalyst:

## Action
One sentence describing the permitted action under the IPS and risk budget.
```

## Publication rule

Публичный Substack update должен содержать только вывод и основные доказательства. Сырые SQL, wallet-level addresses и чувствительные данные портфеля остаются в private/local archive. Для каждого публичного графика указывать `as_of`, source URL и известное ограничение данных.
