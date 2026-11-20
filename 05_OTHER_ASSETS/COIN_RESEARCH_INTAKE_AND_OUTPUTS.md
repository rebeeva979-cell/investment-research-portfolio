# Что нужно для самостоятельного отчёта и дашборда по монете

## Короткий ответ

Да, я могу самостоятельно собрать полный research-пакет: загрузить публичные данные, привести их к единой схеме, написать SQL/Python-пайплайн, построить dashboard, оформить investment thesis, tokenomics/financial model, risk assessment и Decision Card. От пользователя нужны только данные, которых нет в публичных источниках: фактические остатки портфеля, cost basis, адреса кошельков и ограничения IPS.

## Минимальный intake

| Блок | Что нужно |
|---|---|
| Идентичность | ticker, сеть, contract address, нужные торговые пары и биржа |
| Решение | горизонт, предполагаемый бюджет, уже открытая позиция, допустимая доля |
| Portfolio context | units, average cost, current value, custody, нереализованный P/L |
| Риск | допустимая просадка, что считать поломкой тезиса, необходимость ликвидности |
| Wallet data | публичные адреса или экспорт транзакций, если нужен wallet-level анализ |
| Обновления | разовый отчёт, недельный update или автоматический dashboard |

Если нужен только публичный network/protocol research, достаточно ticker/contract и горизонта. Приватные ключи, seed phrase и пароли никогда не нужны.

## Слои данных

1. **Market:** price, volume, market cap, FDV, circulating/max supply, volatility, liquidity and slippage.
2. **On-chain:** blocks, active/new/returning addresses, transactions, transfer value native/USD, fees, holders, flows, contract events.
3. **Protocol economics:** TVL, users, deposits/withdrawals, fees, revenue, expenses, incentives, retention and net revenue.
4. **Tokenomics:** allocation, unlocks, emissions, burns, treasury, insider/market-maker balances and dilution.
5. **Risk/security:** admin keys, upgradeability, oracle/bridge exposure, smart-contract incidents, concentration, sybil/wash signals.
6. **Investment:** peers, multiples, bear/base/bull scenarios, catalyst calendar, valuation range and position sizing.

Для LTC добавляются difficulty, subsidy/fee revenue, miner economics, supply schedule, block interval и проверенный realized-cap/MVRV источник, если он доступен. Для DeFi-протокола добавляются revenue-to-token value capture и устойчивость доходов.

## Источники и качество

Приоритет: primary filings/IR и официальная документация → блокчейн/RPC и verified contracts → DefiLlama/CoinGecko и другие агрегаторы → вторичные публикации. В source register для каждой метрики сохраняются URL, endpoint/query, дата обновления, период, единицы, преобразования и ограничения. Несогласованные источники не усредняются молча: расхождение отмечается как data-quality risk.

Базовый публичный pipeline можно запускать без API-ключей. Ключи требуются только для отдельных глубоких источников (например, Helius/Birdeye или платные провайдеры). Для wallet-level анализа нужен публичный адрес, но не доступ к аккаунту.

## Что я отдаю на выходе

- воспроизводимый CSV/SQL dataset и README;
- Looker Studio dashboard с вкладками `Overview`, `Usage`, `Economics`, `Tokenomics`, `Risk`, `Valuation`, `Decision Log`;
- исследовательский документ 10–20 страниц;
- таблицу источников и методику расчётов;
- Decision Card: `buy/add`, `hold`, `trim`, `avoid` или `wait`, уверенность, диапазон оценки, max position, риск, отмена тезиса, катализатор и дата пересмотра;
- недельный update: что изменилось, какие данные подтверждают/опровергают тезис и какое действие допустимо.

## Ограничения

Я не могу честно вывести фактическую доходность, долю или suitability без актуального экспорта портфеля. Не буду подменять отсутствие данных прогнозом и не буду считать слух об IPO, unlock или revenue подтверждённым фактом. При недостатке данных итоговый статус — `wait`.
