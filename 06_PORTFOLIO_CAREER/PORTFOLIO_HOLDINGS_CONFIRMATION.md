# Подтверждение текущих holdings

Источник baseline: `tezisy/portfolio_state.json`, срез 06.11.2026. Это не текущая котировка и не приказ на сделку.

Нужно подтвердить для каждой строки: `актуально / закрыто / изменилось`, текущую стоимость, биржу/кошелёк и количество.

| Тикер | Количество baseline | Средняя цена, USD | Bucket | Custody | Статус baseline |
|---|---:|---:|---|---|---|
| AVAIL | 678782.16 | 0.004391 | speculation | Bybit | broken |
| BABYDOGE | 200000000000.0 | 6e-10 | speculation | OKX|Bybit | ok |
| BTC | 0.0 |  | btc | OKX |  |
| COMP | 99.78 | 21.7 | quality | OKX|Bybit | ok |
| DOGE | 4157.0 | 0.1242 | speculation | OKX|Bybit | ok |
| DOT | 150.0 | 1.27 | speculation | OKX|Bybit | ok |
| EGLD | 1378.26 | 5.95 | speculation | OKX|Bybit | broken |
| ENJ | 7258.0 | 0.03044 | speculation | OKX|Bybit | ok |
| ETH | 0.0 |  | eth | OKX |  |
| ETHFI | 1598.0 | 0.5435 | quality | OKX|Bybit | ok |
| GRT | 13138.0 | 0.03684 | speculation | OKX|Bybit | ok |
| LINK | 23.7 | 12.23 | quality | OKX|Bybit | ok |
| LRC | 90121.66 | 0.01214 | speculation | OKX|Bybit | broken |
| LTC | 228.14 | 72.13 | ltc | OKX|Bybit | ok |
| MANA | 1099.0 | 0.1608 | speculation | OKX|Bybit | ok |
| MNT | 212.73 | 0.5782 | speculation | Bybit | broken |
| ROSE | 35911.87 | 0.029488857026938445 | speculation | Bybit | ok |
| SNX | 28021.73 | 0.2929 | speculation | OKX|Bybit | broken |
| TIA | 767.88 | 0.3412 | speculation | OKX|Bybit | ok |
| UNI | 244.0 | 3.73 | quality | OKX|Bybit | watch |
| USDT | 990.0 | 1.0 | reserve | dzengi.com |  |
| VIRTUAL | 612.47 | 0.594 | speculation | OKX|Bybit | unknown |
| ZNTL | 446.0 | 3.74 | stock | dzengi.com | watch |
| ZRX | 30737.0 | 0.1161 | speculation | OKX|Bybit | ok |

## Формат ответа

Можно прислать одним сообщением:

```text
Дата среза:
Актив — количество — текущая стоимость USD — где хранится — актуально/изменилось/закрыто
```

Если точные количества неизвестны, укажи хотя бы текущую стоимость и площадку. До подтверждения новые покупки по отдельным рискованным активам остаются `wait`.
