# GPRO — verification update по сделке Starman и covenant risk

**Дата среза:** 23 ноября 2026 года
**Статус:** `wait / special situation`

## Новые факты из SEC

Последний [Form 10-Q за Q3 2026](https://www.sec.gov/Archives/edgar/data/1500435/000150043526000076/gpro-20260930.htm) и [8-K от 6 ноября](https://www.sec.gov/Archives/edgar/data/1500435/000162828026073371/gpro-20261106.htm) меняют календарь сделки:

- «outside date» Merger Agreement продлён с 31 декабря 2026 года до `31 марта 2027 года`;
- текущим акционерам предусмотрены `$1.14 cash` и `0.1` акции surviving corporation на каждую eligible share;
- после закрытия сделки существующие держатели должны владеть примерно `10%` объединённой компании;
- cash consideration может быть уменьшена при отрицательном Net Working Capital ниже `$110m`;
- Parent должен попытаться продлить Commitment Letter до `31 марта 2027 года`, но на дату среза подтверждённого closing или окончательной пролонгации финансирования нет;
- Waiver and Amendment No. 4 от 15 ноября снял covenant non-compliance на 30.09.2026, но оставил условие: если продление Commitment Letter не получено к 25 ноября, minimum liquidity меняется с `$40m` monthly на `$25m` каждый business day, а доступность части revolver может быть исключена;
- на 30.09.2026 cash — `$33.530m`, debt и другие обязательства остаются существенными; 10-Q сохраняет substantial doubt о going concern, если merger не состоится.

## Что это значит для спреда

Разница между котировкой и `$1.14` — не гарантированная доходность. Нужно дисконтировать:

1. вероятность closing;
2. вероятность и размер NWC reduction;
3. срок ожидания до 31.03.2027;
4. стоимость/условия финансирования Parent;
5. стоимость и ликвидность residual 10% stake;
6. covenant/default risk до closing.

Простая модель должна выглядеть так:

```text
value/share = P(close) × (cash_after_NWC + 0.1 × residual_value_per_survivor_share)
              − expected_delay_cost − expected_failure_loss
```

До подтверждения financing extension не публикуем probability-weighted target и не превращаем headline `$1.14` в рекомендацию.

## Decision Card

| Поле | Решение |
|---|---|
| Статус | `wait` |
| Уверенность | `medium` в условиях договора; `low` в вероятности закрытия |
| Сценарный диапазон | `$0.05–1.20+`; probability-weighted value отложена до подтверждения financing и cap table |
| Максимальная доля | до `1%` отдельного special-situation budget |
| Главный риск | financing/closing failure и covenant pressure до закрытия |
| Отмена тезиса | новый waiver не продлён, default, существенное снижение cash consideration или residual ownership |
| Катализатор | подтверждение продления Commitment Letter к 25.11 и последующие 8-K о financing/closing |
| Следующий пересмотр | 27.11.2026 или сразу после material 8-K |
