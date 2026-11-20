# ETHFI — on-chain value-accrual verification

**Snapshot:** 20 November 2026  
**Asset:** ether.fi (ETHFI), Ethereum `0xFe0c30065B384F05761f15d0CC899D4F9F9Cc0eB`  
**Decision:** `WAIT`, maximum 0–2% of a liquid portfolio, 3–6 month review  
**Site case:** [`docs/ethfi.html`](../docs/ethfi.html) · **Data:** [`docs/data/`](../docs/data/) · **Charts:** [`docs/assets/`](../docs/assets/)

## 1. The question

Does ETHFI's documented buyback actually return value to ETHFI holders?

That question is not the same as "does the protocol buy tokens". Three mechanisms are routinely conflated:

| Mechanism | What it is | What the holder receives |
|---|---|---|
| Buyback | The protocol buys ETHFI on the market | Price support while funded; no cash flow |
| Burn | ETHFI is destroyed, supply falls | A smaller float; no cash flow |
| Dividend | Revenue is distributed to holders | Cash or tokens |

ether.fi's stated policy is a 40/30/30 split of protocol revenue: 40% to Labs expenses, 30% to buybacks held in the Foundation treasury, 30% to user cashback. The fee switch is on. The policy does **not** say that every bought token is delivered to sETHFI holders, and it is not a legal claim on revenue.

## 2. What the protocol does

ether.fi is liquid restaking and ETH staking. The depositor receives eETH/weETH; the protocol earns a fee on staking and restaking rewards.

TVL on 20 November 2026 was **$3.728B**: $3.344B staking, $284M liquid, and the remainder on other chains and products.

The economics chain is:

```text
gross fees
  → protocol revenue (after validator/partner/expense costs)
  → buyback funding
  → ETHFI acquired
  → destination: sETHFI / treasury / cashback users / burn / unknown
```

| Metric | 30 days | 365 days |
|---|---:|---:|
| Gross fees | $13,621,953 | $178,083,989 |
| Protocol revenue | $3,824,601 | $43,391,303 |
| Holders revenue | $0 | $6,549,981 |
| Cumulative revenue | $110,191,116 | — |
| Cumulative holders revenue | $16,591,119 | — |

Source: DefiLlama `dailyFees`, `dailyRevenue`, `dailyHoldersRevenue`, snapshot 20 November 2026. Revenue capture is 28.1% of gross fees. Holders revenue is zero over 30 and 90 days; the last non-zero observation is **1 April 2026**.

The key distinction: **$13.6M fees is commission turnover. $3.8M revenue is what the protocol kept. $0 holders revenue is what reached the holder.** For token valuation, only the third line is a direct cash-flow claim.

## 3. Supply: three numbers and one conflict

| Source | Circulating | Locked | Total | Status |
|---|---:|---:|---:|---|
| On-chain `totalSupply()` | 998,535,999 | — | 998,535,999 | RPC, verified |
| CoinGecko | 998,535,999 | 0 | 998,535,999 | treats total as circulating |
| DefiLlama unlocks | 983,600,557 | 16,399,443 | 1,000,000,000 | different base |
| Docs / max supply | — | — | 1,000,000,000 | hard cap |

The token was minted at 1B. On-chain supply is **998,535,999**: **1,464,001 ETHFI was burned** through `burn()`. The zero address balance is 0; the dead address holds 0.6696 ETHFI. This is a reduction of `totalSupply`, not a transfer to a burn address.

The three-way conflict is material: if DefiLlama is right, CoinGecko overstates float by ~14.9M ETHFI (1.5% of supply) and market cap by roughly **$7M**. For a position, that is not decisive. For overhang and dilution math, it is.

The practical float is thinner than the headline: the top 10 wallets hold **62.19%** of supply. Treasury, sETHFI, CEX and two unlabelled allocation EOAs account for most of it. This is why a $1.65M buyback can be visible in the price.

## 4. Who holds the float

Blockscout returns 93,377 holders. We classified the top 250 and separated contracts, CEX, treasury and EOAs.

| Rank | Wallet | Type | ETHFI | % supply |
|---:|---|---|---:|---:|
| 1 | `0x7A6A…bB53` | ether.fi Safe (treasury) | 153,200,600 | 15.34% |
| 2 | `0x86B5…0161` | sETHFI staking contract | 108,994,970 | 10.92% |
| 3 | `0x95Bf…995e` | unlabelled EOA | 101,547,168 | 10.17% |
| 4 | `0xf108…41aC` | unlabelled EOA | 54,533,029 | 5.46% |
| 5 | `0x5a52…Efcb` | Binance hot wallet | 39,447,593 | 3.95% |
| 6 | `0xF977…aceC` | Binance cold wallet | 37,000,000 | 3.71% |
| 7 | `0xe008…fD3f` | ether.fi OFT adapter | 35,992,714 | 3.60% |
| 8 | `0xF619…e39f` | unlabelled EOA | 35,877,782 | 3.59% |
| 9 | `0x7a93…b3fb` | unlabelled EOA | 27,633,150 | 2.77% |
| 10 | `0x6630…0739` | unlabelled EOA | 26,713,477 | 2.68% |

Concentration: top-1 15.34%, top-5 **45.84%**, top-10 **62.19%**, top-20 **73.96%**.

After excluding contracts, CEX and bridges, the EOA float is **473,955,369 ETHFI (47.5%)**. Within that float:

- top-1 EOA = **21.4%** of float; top-5 EOAs = **52.0%**;
- Gini **0.805**; HHI **761**; Nakamoto at 50% = **5 wallets**;
- two unlabelled EOAs received **156M ETHFI** from Safes: 101.5M in one transaction in February 2025, 54.5M in tranches in December 2025 and April 2026.

This is not proof that insiders are selling. It is an **overhang**: allocation/vesting-type recipients can exit, and their 156M balance is more than 100× the monthly buyback. Until they send tokens to a CEX, the sell pressure is unrealised; this is a point-in-time observation, not a guarantee.

## 5. The buyback: following the money

This is the core of the verification. The public policy says 30% of revenue goes to buybacks. The question is whether the policy is executed and where the purchased token goes.

### Value chain

```text
Funding Safe 0xf40bcc…f7021
  │  $7.90M in / $7.60M out (300 USDC transfers, 9 Sep–19 Nov 2026)
  ├─ $2.2M → Buyback Safe 0x43f4ca…6408c
  │            └─ CoW Settlement 0x9008D1…0ab41
  │                  └─ 2,779,410 ETHFI received (581 transfers)
  │                        └─ 2,054,374 → ops EOA 0x9eaC71…843f
  │                        └─ 893,950 → LZMultiCall 0xAcdDAC…c05f1 (LayerZero)
  │                              └─ cashback on Optimism (inferred)
  └─ $3.728M → 0x4ECF…D643 (purpose unconfirmed)
```

### What is verified

- The Funding Safe received **$7.90M** and sent **$2.2M** to the buyback Safe; another **$3.728M** went to `0x4ECF024b92f36C27F487dcb88cF109A6704ED643` (purpose not confirmed).
- The buyback Safe received **581 ETHFI transfers totalling 2,779,410**; **2,603,293** came directly from CoW.
- **566 matched CoW orders** bought **2,542,499 ETHFI for $1,645,541**, average **$0.6472**, range **$0.4643–$0.7898**.
- The last 30 days account for **1,155,696 ETHFI / $663,000**.
- The program is observed **17 September–20 November 2026**, 58 active days, average **47,921 ETHFI/day**.
- **No ETHFI left the buyback Safe for sETHFI.** sETHFI flows are user `deposit` / `boringRedeemSolve`, not buybacks.
- The buyback Safe sent **2,948,324 ETHFI** out: **2,054,374** to ops EOA `0x9eaC7114D1a1EaBc4732A886795cFD9E6E35843f` and **893,950** to LZMultiCall `0xAcdDAC6C77318B615f7F6fB9bb67c6833e9c05f1`. The EOA forwards to LZMultiCall with method `0x571d3dc7`.

### What is not verified

- The final cashback payout to users on Optimism. The path to LZMultiCall is visible; the distribution is inferred from the bridge and secondary research, not traced to recipient addresses.
- Who stands behind the Funding Safe and `0x4ECF…D643`. They may be an operating reserve or a partner settlement.
- That the buyback will continue. The observed period is only September–November 2026.

### Policy versus flow

| Measure | Value | Interpretation |
|---|---:|---|
| Buyback / revenue, last 30d | **17.3%** | Policy allocates 30% to buyback + 30% to cashback; the buyback line is 17.3% vs 30% |
| Annualised buyback | **$7.96M** | 1.71% of $465.7M market cap |
| Monthly buyback | **1.156M ETHFI** | ~26% of scheduled unlocks (~4.43M/month) |
| Average purchase price | **$0.647** | Spot $0.466 → position marked **−28%** |

The buyback is real. The holder yield is not. The tokens are used to buy customer cashback and to bridge to Optimism, not to pay ETHFI holders on Ethereum. That may be a rational growth strategy; it is not the dividend-like value accrual the policy language implies.

## 6. Economics compressing faster than price

| Metric | Value |
|---|---:|
| TVL | $3.728B |
| Peak TVL | $12.794B (14 Aug 2025) |
| Drawdown from peak | **−70.9%** |
| TVL 30d / 365d | −27.0% / −46.3% |
| Market cap / FDV | $465.7M |
| Price | $0.466 |
| Market cap / 365d revenue | **10.73×** |
| Market cap / 365d fees | **2.62×** |
| Market cap / TVL | **0.125×** |
| Price 365d | −42.6% |
| Annualised volatility | 94.3% |
| ATH | $8.53 |

Scenarios are sensitivity checks, not price targets. They flex revenue run-rate and the multiple:

| Scenario | Revenue run-rate | Multiple | Valuation | Price | vs spot |
|---|---:|---:|---:|---:|---:|
| Bear | $32.5M | 7× | $227.5M | $0.228 | −51.2% |
| Base | $43.39M | 10× | $433.9M | $0.435 | −6.8% |
| Bull | $52.07M | 14× | $729.0M | $0.730 | +56.5% |

Assumptions: Bear has revenue falling with TVL by another 25% and multiple compression; Base stabilises at the 365-day revenue level; Bull assumes TVL and revenue recovery. The point is the asymmetry, not the forecast.

## 7. Liquidity, unlocks and the cost of being wrong

Visible DEX liquidity is **$1.228M**, or **0.26% of market cap**. The top Uniswap ETHFI/ETH pool holds **$739,608**; the second, ETHFI/WETH, **$377,546**.

Uniswap QuoterV2 quotes for a sell:

| Order size | Price impact |
|---:|---:|
| $10,000 | −1.03% |
| $50,000 | −3.95% |
| $250,000 | **−38.78%** |

A constant-product single-pool model gives $10k 2.6%, $50k 11.9%, $250k 40.3%. The dashed line on the site chart is that model; the gold points are actual QuoterV2 results. Concentrated liquidity can reduce small-size impact, but $250k is already a double-digit cost.

Unlock overhang: Core Contributors receive **~1.02M ETHFI per week** (~$482k), continuously, with no dated "unlock day". The buyback covers about **26%** of that flow. If the buyback stops, the mechanical bid disappears.

## 8. Decision Card

| Field | Decision |
|---|---|
| Status | **WAIT** |
| Max position | **0–2%** of liquid portfolio |
| Horizon | 3–6 months |
| Why not buy | Buyback is a funded bid, not holder yield; TVL and revenue are still compressing; float is thin but overhung |
| Why not short | Real mechanical bid, thin float, borrow cost and squeeze risk not measured |
| Upgrade trigger | Buyback routed to sETHFI/holders or burn with verifiable transactions; TVL >$4.5B for 30 days with revenue rising; verified Optimism cashback >$1M with recipient addresses |
| Invalidation | Treasury/allocation EOAs send >5% of float to CEX; buyback stops for >30 days; TVL <$3B or revenue <$2.5M/30 days |

The honest position is observation: the buyback exists, but the distribution leg is not proven. A token with a working bid is not the same asset as a token with real yield.

## 9. Sources, reproducibility, limitations

Primary: Ethereum RPC (`totalSupply`, `balanceOf`), Blockscout API (holders, transfers, metadata), CoW Protocol API (orders, trades, execution prices), Uniswap QuoterV2.

Aggregators: DefiLlama (TVL, fees, revenue, holders revenue, unlocks), CoinGecko (price, supply), DexScreener (pools, liquidity).

Pipeline in this repository: `04_ETHFI/onchain/`.

```text
fetch_onchain.py → raw/*.json → build_outputs.py → data/*.csv + assets/*.svg
                         │
                    manifest.py (SHA-256)
                         │
                    check_site.py (links, tables, numbers, CSV drift)
```

Run `make build` to rebuild from the committed snapshots, `make check` to verify the manifest, unit tests and site consistency, and `make refresh` to fetch a new snapshot. The site charts and tables are generated from those files. Address labels are heuristics, not legal identity. The Optimism cashback leg is not verified. The supply conflict is not resolved; both bases are shown. The buyback is observed only from September 2026 and cannot be assumed permanent. No paid data terminals or API keys were used.

**Not investment advice.** This is a research process demonstration; the decision is an illustration of discipline, not a recommendation to buy or sell.
