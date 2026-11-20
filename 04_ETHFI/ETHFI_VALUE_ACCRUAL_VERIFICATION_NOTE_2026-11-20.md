# ETHFI — Value accrual verification note

**Дата проверки:** 20 ноября 2026  
**Цель:** отделить buyback policy от фактического потока ETHFI и понять, получает ли держатель ETHFI экономическую ценность.

## Короткий вывод

В текущем кейсе нельзя писать просто «ETHFI получает buybacks». Нужно разделять как минимум три режима:

1. **Политика:** официальная документация описывает еженедельные buybacks из eETH withdrawal fees и ежемесячные buybacks из части protocol revenue; купленный ETHFI должен перераспределяться sETHFI holders.
2. **Методика агрегатора:** DefiLlama определяет `holders revenue` как token buybacks. В текущем 30-дневном API-срезе `holders revenue = $0`, хотя исторический cumulative holders revenue на странице протокола не равен нулю.
3. **Фактический поток новой программы:** независимый BlockPinned-исследовательский срез утверждает, что с 8 сентября 2026 новый buyback-маршрут через CoW направляет ETHFI на Optimism для cashback пользователям, а не напрямую в sETHFI и не на burn. Это пока **вторичный verification lead**, а не окончательно проверенный нами факт.

Инвестиционный смысл: даже если buyback исполнен, нужно определить, является ли он возвратом стоимости токенодержателю, customer-acquisition subsidy или смешанным механизмом. До прямой on-chain сверки `value_accrual` остаётся `conditional / unresolved`, а ETHFI — `wait`.

## Что говорит первичный источник

Официальная страница [ETHFI Buyback Program](https://etherfi.gitbook.io/gov/ethfi-buyback-program) утверждает:

- 100% дохода от eETH withdrawal fees направляется на еженедельные ETHFI buybacks;
- часть более широкого protocol revenue направляется на ежемесячные buybacks;
- купленный ETHFI передаётся sETHFI holders;
- Foundation wallet: `0x2f5301a3D59388c509C65f8698f521377D41Fd0F`.

Это подтверждает существование заявленной политики, но само по себе не подтверждает каждый фактический buyback, путь токена и текущую реализацию после изменения Cash-программы.

## Что показывает методика DefiLlama

На [странице ether.fi в DefiLlama](https://defillama.com/protocol/ether.fi?denomination=ETH&fdv=false&fees=false) отдельно показаны:

- Fees;
- Revenue;
- Holders Revenue;
- Incentives;
- Earnings.

В методике страницы `Holders Revenue` описан как token buybacks, а `Earnings` — как revenue минус incentives. Это полезнее, чем приравнивать `protocol_revenue` к чистой прибыли, но всё равно остаётся adapter methodology, а не audited treasury P&L.

Текущий локальный API-срез на 20.11.2026 показывает:

- gross fees 30d: `$13.924m`;
- protocol revenue 30d: `$3.892m`;
- holders revenue 30d: `$0`.

Нельзя трактовать `$0` как «buyback никогда не было»: это значение конкретного 30-дневного окна и выбранной методики.

## Вторичный on-chain lead, который нужно воспроизвести

На [BlockPinned ETHFI research page](https://terminal.blockpinned.com/en/ethfi/) опубликованы следующие наблюдения, датированные 19.11.2026:

- с 8.09.2026 новая программа покупает ETHFI за USDC через CoW;
- купленный ETHFI направляется на Optimism и используется для cashback пользователей;
- в 30 дней до 18.11 было около `1.12m ETHFI` из CoW в buyback Safe и около `$1.25m USDC` депозитов;
- исследователь не обнаружил прямого перемещения новой покупки в sETHFI и burn в проверенном окне;
- cashback может частично продаваться, использоваться как collateral или стейкаться; доли на странице помечены как верхние границы/инференс.

Это не заменяет самостоятельную проверку. Но это существенный конфликт с простой формулировкой «все buybacks получают sETHFI holders» и должен быть отдельным risk flag.

Для независимого повторения использовать [Dune query: ETHFI buybacks vs cashback distributions](https://dune.com/queries/9059186) и [Dune funding-by-source query](https://dune.com/queries/9059194). Dune — secondary structured source: сохранить SQL, дату выгрузки и список адресов.

### Адреса для повторной проверки

Это рабочие адреса из публичного BlockPinned source map; перед использованием в модели каждый нужно открыть в explorer и подтвердить chain/bytecode:

- Ethereum ETHFI: `0xfe0c30065b384f05761f15d0cc899d4f9f9cc0eb`;
- Ethereum sETHFI: `0x86b5780b606940eb59a062aa85a07959518c0161`;
- buyback Safe cited by the research: `0x43f4ca92f7f378bcdcf1508b866b5b6c47d6408c`;
- Optimism ETHFI token: `0xe0080d2F853ecDdbd81A643dC10DA075Df26fD3f` (сверить checksum и chain в explorer перед SQL/RPC);
- official Foundation wallet from Ether.fi docs: `0x2f5301a3D59388c509C65f8698f521377D41Fd0F`.

Адрес Optimism отмечен как требующий ручной сверки chain/checksum перед SQL/RPC. Попытка получить metadata через Blockscout API в текущем окружении получила HTTP 403, поэтому эти адреса пока остаются leads, а не independently verified contract metadata.

## Revised value-accrual model

Вместо одной строки `token_value_accrual = Buybacks` использовать waterfall:

```text
protocol fees
  → protocol retained revenue
  → buyback funding
  → ETHFI acquired
  → destination:
       sETHFI holders / treasury / cashback users / burn / unknown
  → secondary behaviour:
       hold / sell / collateral / stake
```

Каждое звено получает `verified`, `secondary`, `inferred` или `unverified`.

## Что нужно проверить on-chain

1. Foundation wallet и buyback Safe: incoming USDC, outgoing USDC, CoW orders.
2. ETHFI output from CoW: destination Safe, chain bridge and Optimism distributor.
3. Cashback distributor events: amount, recipient class, timestamp and token contract.
4. sETHFI vault: ETHFI balance before/after each buyback period и backing per share.
5. Burn address / `Transfer(..., 0x0)`: был ли burn именно в новом периоде.
6. Reconcile Dune/BlockPinned totals with raw Ethereum and Optimism logs.
7. Разделить старую программу (до лета 2026) и новую программу (с сентября 2026), не смешивать их в одном cumulative KPI.

## Влияние на инвестиционный тезис

**Положительное, если подтвердится:** protocol revenue действительно финансирует регулярный open-market demand, а часть приобретённого ETHFI остаётся у sETHFI holders или создаёт measurable backing.

**Нейтральное/смешанное:** buyback существует, но большая часть токена выдаётся пользователям как cashback. Это может поддерживать adoption и спрос, но не является прямым распределением дохода держателю ETHFI.

**Негативное:** gross fees и protocol revenue выглядят крупными, но фактический token-holder cash flow отсутствует, а buyback является расходом на customer incentives. Тогда valuation должен опираться на бизнес-экономику протокола, а не на обещание dividend-like value accrual.

## Обновлённая формулировка для отчёта

> «У ETHFI есть документированная buyback policy, но policy не равна фактическому распределению. Для новой Cash-программы нужно проверить, куда приходит купленный ETHFI: sETHFI holders, cashback users, treasury, burn или комбинация. До этой сверки я считаю value accrual условным и оставляю статус `wait`».

