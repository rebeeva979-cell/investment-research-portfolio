# Synthetix (SNX) — SIP-423 Supply Overhang Analysis

**Статус:** Verified research POC / updated 2026-11-19  
**Полный отчёт:** [`SNX_SIP423_RESEARCH_REPORT_2026-11-19.md`](SNX_SIP423_RESEARCH_REPORT_2026-11-19.md) · PDF/HTML рядом  
**Датапак:** [`SNX_SIP423_DATA_PACK.xlsx`](SNX_SIP423_DATA_PACK.xlsx) · скрипт [`build_snx_data_pack.py`](build_snx_data_pack.py)  
**Looker Studio dashboard:** https://datastudio.google.com/u/1/reporting/ce2f06e8-b3e4-49f9-be7a-f2547d8fac57/page/PxzBG

## Исследовательский фокус

Оценить дополнительное предложение SNX в связи с SIP-423: фактический mint, custody, lock/vest, рыночный контекст и потенциальное влияние на цену и оценку.

## Проверенные числа

| Метрика | Значение | Статус |
|---|---:|---|
| Maximum mint по SIP-423 | 236 464 356 SNX | Подтверждено первоисточником |
| Фактический mint | 236 464 356 SNX | Подтверждено tx `0x0bb737…bc0b9` |
| Pre-mint supply | 344 939 867.56 SNX | Подтверждено `totalSupply` на block 25 473 065 |
| Post-mint total supply | 581 404 223.56 SNX | Подтверждено текущим `totalSupply` |
| Рост к pre-mint | +68.55% | Расчёт |
| Доля от post-mint supply | 40.67% | Расчёт |
| Safe balance | 236 464 356.00 SNX | Подтверждено `balanceOf` |
| Исходящие переводы с Safe | 0 на 2026-11-19 | Blockscout, point-in-time |
| sUSD entitlement | 59 116 089 sUSD | Подтверждено SIP-423 |
| Конверсия | 4 SNX за 1 sUSD; reference $0.25 | Подтверждено SIP-423 |
| Snapshot blocks | Ethereum 25 473 065; Optimism 153 868 527 | Подтверждено RPC |
| Claim window | ~2027-07-06 | Оценка T+365 дней |
| Vest | до ~2028-07-06 | Оценка 1 год |
| Unclaimed expiry | 6 месяцев / TBD | Противоречие в SIP |
| Revenue hurdle | $10M в течение 2-летнего lock-up; 25% revenue | Подтверждено SIP |

## Рыночный срез на 2026-11-19

- Цена: **$0.164855**
- Reported market cap: **$95.83M**
- FDV: **$95.90M**
- Circulating supply (CoinGecko): **580.98M** (99.93% of total)
- Fees 30d / 1y: **$3 678 / $32 242**
- TVL: **$856 123**; год назад **$88.43M** (−99.03%)
- Claim value at market: **$38.98M** vs **$59.12M** sUSD par (−34.06%)
- Reported market cap / pre-mint implied market cap: **1.685x**

## Методологические предостережения

- Safe — мультиподпись, **не on-chain vesting-контракт**. Lock/vest — policy commitment; signers и threshold не проверены.
- «Нет исходящих переводов» — наблюдение на дату, не гарантия.
- CoinGecko включает заблокированные токены в circulating supply; Coinbase/CoinCodex в этом проходе не проверены независимо.
- Fees — не revenue и не profit; TVL зависит от покрытия и методологии.
- Unclaimed expiry противоречив: в SIP есть и 6-месячная фраза, и строка `TBD`.
- Не утверждать фактический sell pressure без анализа поведения получателей и ликвидности.
- Это research artifact, не инвестиционная рекомендация.

## Что дальше

1. Подключить `SNX_SIP423_DATA_PACK.xlsx` к Looker Studio и собрать страницы по `DASHBOARD_LAYOUT`.
2. Добавить алерт на исходящие переводы Safe >1% баланса.
3. Обновлять market/fees/TVL срез и фиксировать изменения в `VERIFICATION_LOG`.
4. Проверить Coinbase/CoinCodex circulating supply датированным snapshot.
5. Следить за deployment receipt-контракта и SIP-423 amendments.
