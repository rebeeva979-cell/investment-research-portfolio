# Ether.fi (ETHFI) — Risk Assessment

**Статус:** Risk framework / requires live evidence before rating.

## Risk register

| Риск | Механизм | Что проверяем | Trigger | Влияние на thesis |
|---|---|---|---|---|
| Smart-contract | Ошибка в staking, vault или withdrawal logic | Audits, deployed bytecode, incidents, admin rights | exploit, pause, abnormal withdrawals | Critical |
| Slashing / validator | Потеря ETH или доходности из-за действий операторов | Operator set, insurance, restaking dependencies | slashing event, penalty, operator concentration | High |
| Liquidity | eETH/weETH торгуется с дисконтом к underlying | DEX depth, redemption queue, peg history | persistent discount, redemption delay | High |
| Oracle / pricing | Неверная цена collateral или share token | Oracle sources, update frequency, fallback | stale or divergent price | High |
| Concentration | TVL или rewards зависят от нескольких wallets/operators | Top holders, operator share, treasury | one entity controls material share | High |
| Incentive dependency | TVL уходит после снижения points/emissions | Net flows, rewards, TVL without incentives | TVL falls as rewards decline | High |
| Revenue quality | Gross fees не превращаются в retained revenue | Fee waterfall, treasury inflow, partner shares | revenue margin compresses | High |
| Token dilution | Unlocks и emissions создают supply overhang | Allocation, vesting, unlock calendar, transfers | large unlock + weak liquidity | High |
| Value accrual | Рост протокола не связан с ETHFI | Contracts, governance, buybacks, distributions | no enforceable holder benefit | Critical |
| Governance | Multisig or governance can change risk parameters | Signers, quorum, timelock, proposals | unilateral parameter change | High |
| Competition | Liquid staking/restaking alternatives capture flows | Competitor TVL, fees, liquidity, integrations | share loss or price war | Medium/High |
| Regulatory / custody | Access, listing or custody constraints | Official risk disclosures and market access | delisting, restriction, legal event | High |
| Data quality | Inconsistent definitions produce false thesis | Source register, reconciliations, missing periods | unexplained divergence | High |

## Risk scoring

Использовать score 1–5:

- 1: low, evidence stable;
- 2: manageable;
- 3: material uncertainty;
- 4: high probability or high impact;
- 5: thesis-breaking until resolved.

Итоговый risk score не должен быть средним арифметическим без комментария: один critical risk может быть достаточным для остановки инвестиционного вывода.

## Falsifiers

Инвестиционная гипотеза ETHFI должна считаться ослабленной, если выполняется хотя бы одно из условий:

1. TVL падает при сохранении или росте incentives.
2. Gross fees растут, но protocol revenue не растёт.
3. Net economics остаётся отрицательной после incentives и operator share.
4. Unlock-adjusted supply растёт быстрее adoption.
5. Не найден подтверждённый механизм ETHFI value accrual.
6. Возникает material slashing, liquidity или smart-contract event.
7. Ключевые цифры не удаётся reconciliate между protocol, chain и independent sources.

## Required evidence before final rating

- verified contract addresses;
- protocol fee and revenue definitions;
- treasury inflow/outflow data;
- current and future token unlock schedule;
- holder and operator concentration;
- withdrawal and liquidity stress test;
- incident and audit review;
- weekly change log.
