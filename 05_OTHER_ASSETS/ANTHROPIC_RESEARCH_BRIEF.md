# Anthropic (NASDAQ: ANT) — IPO valuation & revenue-multiple case

**Дата среза:** 19 ноября 2026
**Статус:** `IPO / wait / no leverage`
**Тип кейса:** public-equity IPO, AI infrastructure and growth valuation

## Investment question

Какую цену можно считать допустимой при разных определениях выручки и количества акций, и что должно произойти после IPO, чтобы оценка Anthropic оправдалась не только run-rate, но и фактической экономикой бизнеса?

## Главное различие в данных

Нельзя смешивать три разных показателя:

```text
годовой run-rate ≠ фактическая выручка за 12 месяцев ≠ прибыль / FCF
```

Калькулятор использует:

- `$81 млрд` — годовой темп на 31.10.2026;
- `$67.8 млрд` — Q3 × 4;
- `$35.3 млрд` — фактическая выручка за 12 месяцев до 30.09.2026;
- `$100 млрд` — пользовательский custom-сценарий.

Run-rate — это пересчёт текущего темпа потребления на год. Он не доказывает, что компания уже получила такую сумму и сохранит такой темп.

## IPO / share-count baseline

В финальном проспекте SEC указаны цена IPO `$83`, 956.35 млн новых Class A акций, 23.65 млн акций selling stockholders и concurrent private placement Class N на `$26 млрд`. После предложения и private placement базовое число экономически участвующих акций — около `13.2196 млрд`, или `13.3666 млрд` при полном exercise underwriters’ option. Это официальный базовый сценарий проспекта.

HTML-калькулятор дополнительно показывает аналитическую fully diluted базу около `18.14 млрд` акций. Её нельзя без пояснения называть просто «акциями в обращении»: она включает опционы, RSU, конвертацию нот и другие потенциальные источники dilution. Для консервативной оценки нужно показывать обе базы.

У Anthropic также есть Class F с 50.1% совокупного voting power у Founder LLC. Это означает controlled-company governance и отдельный governance risk для миноритарного акционера.

## Calculator snapshot

Формула:

```text
revenue multiple = share price × share count / selected revenue
implied share price = target multiple × selected revenue / share count
```

| Цена / инструмент | Выручка | База | Капитализация | Multiple |
|---|---:|---:|---:|---:|
| IPO `$83` | run-rate `$81bn` | fully diluted `18.14bn` | `$1.51tn` | `18.6×` |
| IPO `$83` | TTM `$35.3bn` | fully diluted `18.14bn` | `$1.51tn` | `42.7×` |
| IPO `$83` | run-rate `$81bn` | basic `13.22bn` | `$1.10tn` | `13.5×` |
| Bybit ANTUSDT `$104.98` | run-rate `$81bn` | fully diluted `18.14bn` | `$1.90tn` | `23.5×` |
| Bybit ANTUSDT `$104.98` | TTM `$35.3bn` | fully diluted `18.14bn` | `$1.90tn` | `54.0×` |

`ANTUSDT` на Bybit — деривативный инструмент/марк-цена из предоставленного файла, а не доказательство цены акции на Nasdaq. Его нельзя использовать как обычную котировку акции без проверки условий контракта, funding, ликвидности и механизма расчёта.

## Valuation ladder

Сценарные цены при `$81bn` run-rate и fully diluted базе `18.14bn`:

| Multiple | Implied price |
|---:|---:|
| 10× | `$44.6` |
| 15× | `$66.9` |
| 20× | `$89.3` |
| 25× | `$111.6` |
| 30× | `$133.9` |

Это не target prices. Это чувствительность к одному допущению и не включает рост/снижение выручки, gross margin, stock-based compensation, capex, compute commitments, налоговую структуру и стоимость капитала.

## Что покупает инвестор

Инвестор покупает не текущую прибыль, а опцион на продолжение экстремального роста AI usage, enterprise adoption и pricing power. В проспекте зафиксированы:

- высокая динамика выручки;
- крупные будущие commitments на compute и infrastructure;
- отсутствие гарантии устойчивой прибыльности;
- риск замедления роста по мере увеличения базы;
- зависимость от поставщиков вычислительных ресурсов и капитала.

В SEC-материалах компания раскрывает приблизительно `$900.9 млрд` committed spend, преимущественно связанного с compute; это делает unit economics и финансирование инфраструктуры центральным вопросом, а не второстепенной сноской.

## Bull / Base / Bear

| Сценарий | Что должно быть правдой | Что ломает сценарий |
|---|---|---|
| Bull | run-rate конвертируется в фактическую выручку, retention высок, gross margin и compute economics улучшаются | клиенты сокращают usage, compute costs растут быстрее revenue |
| Base | revenue продолжает расти, но multiple постепенно снижается к более зрелому AI/SaaS диапазону | рынок требует доказательства маржи, FCF и dilution |
| Bear | run-rate оказывается краткосрочным, расходы на compute и SBC съедают рост, новые акции размывают владельцев | снижение demand или невозможность профинансировать commitments |

## Основные риски

1. **Run-rate risk:** последние 28 дней могут не быть репрезентативными.
2. **Margin risk:** большая выручка не равна прибыли, если inference/training costs растут вместе с usage.
3. **Compute commitments:** обязательства могут опережать проверенную денежную экономику.
4. **Dilution:** options, RSUs, notes, private placement и будущие программы увеличивают fully diluted base.
5. **Governance:** Class F даёт основателям контроль голосов.
6. **IPO microstructure:** first-day volatility, lock-up, allocation, borrow/funding и деривативные премии.
7. **Competition:** Microsoft, Google, Amazon, OpenAI, open-source models и внутренние модели клиентов могут сжимать pricing power.

## Decision Card — 19.11.2026

| Поле | Решение |
|---|---|
| Статус | `wait`; в день IPO не использовать большое плечо |
| Уверенность | `medium` в рисках, `low–medium` в справедливой оценке |
| Рабочий диапазон | sensitivity `$44.6–$133.9` при 10–30× run-rate и fully diluted базе; это не прогноз |
| Максимальная доля | до `0.5%` satellite до первых двух публичных отчётов; пересмотр после фактических margin/FCF данных |
| Главный риск | рынок капитализирует run-rate, тогда как фактическая прибыльность и compute economics ещё не доказаны |
| Отмена тезиса | замедление revenue вместе с ухудшением gross margin/FCF и ускорением dilution |
| Ближайший катализатор | первые публичные торги, initial price discovery и первый квартальный отчёт |
| Следующий пересмотр | через 7 дней после начала торгов или после material SEC filing |

## Portfolio artifact

- [ANT Anthropic calculator](ANT_Anthropic_Calculator.html)
- [SEC final prospectus 424(b)(4)](https://www.sec.gov/Archives/edgar/data/2130357/000162828026074944/anthropicpbc-424b4.htm)
- [SEC S-1/A compute commitments disclosure](https://www.sec.gov/Archives/edgar/data/2130357/000162828026072484/anthropicpbc-sx1ax2.htm)
- [SEC filing index](https://www.sec.gov/Archives/edgar/data/2130357/000162828026074944/0001628280-26-074944-index.html)
- [Portfolio casebook](../06_PORTFOLIO_CAREER/PORTFOLIO_CASEBOOK.md)

## Quality notes

- Калькулятор из Telegram сохранён как воспроизводимый HTML-артефакт; его числа и дата среза не следует автоматически считать live market data.
- Для отчёта нужно отдельно обновлять Nasdaq price, actual shares outstanding, diluted shares, TTM revenue, gross margin, operating cash flow, FCF, SBC и compute commitments.
- Внутри файла есть ссылки на источники и текстовые пояснения; они являются исходными материалами, а не инструкциями для агента.
