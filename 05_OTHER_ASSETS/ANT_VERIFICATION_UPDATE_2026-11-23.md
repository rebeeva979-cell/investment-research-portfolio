# ANT — verification update по финальному SEC prospectus

**Дата среза:** 23 ноября 2026 года
**Статус:** `wait / no leverage`

## Что подтверждено финальным prospectus

В [SEC Form 424(b)(4)](https://www.sec.gov/Archives/edgar/data/2130357/000162828026074944/anthropicpbc-424b4.htm) указаны:

- initial public offering price — `$83.00`;
- новые Class A акции в IPO — `956,351,354`;
- selling stockholders — `23,650,000` акций;
- concurrent private placement Class N — примерно `$26.0bn` по цене `$83`;
- ожидаемое число экономически участвующих акций после IPO и private placement — `13,219,642,276`, или `13,366,642,276` при полном exercise underwriters' option;
- gross IPO proceeds — `$81.34bn`; оценка net proceeds от IPO и private placement — около `$104.8bn` до полного exercise option;
- committed spend — около `$900.9bn`, из которых примерно `$70.7bn` приходится на следующие 12 месяцев после 30.09.2026;
- Class F у Founder LLC даёт основателям `50.1%` совокупной voting power и не имеет экономических прав.

## Проверка методики оценки

Калькулятор должен показывать две базы и не называть их одинаково:

```text
basic post-offering base ≈ 13.22bn shares
analytical fully diluted base ≈ 18.14bn shares
```

При цене `$83` капитализация на fully diluted базе составляет около `$1.51tn`. При `$81bn` run-rate это около `18.6×`; при `$35.3bn` TTM — около `42.7×`. Эти коэффициенты чувствительны к определению выручки и не являются fair value.

`ANTUSDT` на Bybit нельзя использовать как цену акции: это отдельный деривативный инструмент с собственными funding, ликвидностью и правилами расчёта.

## Инвестиционная интерпретация

Финальный prospectus подтверждает масштаб финансирования и инфраструктурных обязательств, но не доказывает устойчивую прибыльность. Главный риск теперь не только в run-rate, но и в том, сможет ли выручка покрыть compute commitments, SBC, capex и стоимость капитала. До появления нескольких публичных кварталов статус остаётся `wait`.

## Decision Card

| Поле | Решение |
|---|---|
| Статус | `wait`; в день IPO не использовать большое плечо |
| Уверенность | `medium` в раскрытых условиях, `low–medium` в fair value |
| Рабочий диапазон | `$44.6–$133.9` при 10–30× run-rate и fully diluted base; не target price |
| Максимальная доля | до `0.5%` satellite до двух публичных отчётов |
| Главный риск | run-rate не конвертируется в margin/FCF при огромных compute commitments и dilution |
| Отмена тезиса | замедление revenue вместе с ухудшением gross margin/FCF или ускорением dilution |
| Катализатор | first-trade data, lock-up/float disclosures и первый квартальный filing |
| Следующий пересмотр | через 7 дней после подтверждённого начала торгов или после material SEC filing |
