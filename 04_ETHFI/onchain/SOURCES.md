# ETHFI on-chain source register

Point-in-time snapshot: **2026-11-20**. Everything in `data/` is derived from
the files in `raw/`; `MANIFEST.csv` pins each file by SHA-256. If a number on
the site changes, this directory and the manifest must change with it.

## Primary / on-chain

| Question | Source | Snapshot | Notes |
|---|---|---|---|
| Token float | Ethereum JSON-RPC `eth_call` `totalSupply()` on `0xFe0c30065B384F05761f15d0CC899D4F9F9Cc0eB` | `raw/rpc_supply.json` | 998,535,999 ETHFI at block 26,457,647; `balanceOf(0x0)=0`, burn used `burn()` |
| Holders | Blockscout v2 `GET /api/v2/tokens/{token}/holders` | `raw/holders_top.json` | 5 pages × 50 = top 250; full holder count 93,377 from token endpoint |
| Treasury flows | Blockscout v2 `GET /api/v2/addresses/{safe}/token-transfers?token=ETHFI` | `raw/safe_token_transfers.json` | Safe `0x7A6A…bB53`, tagged ether.fi; 169 transfers |
| Buyback purchases | Blockscout v2 token transfers, buyback Safe `0x43f4…d6408c`, counterparty CoW Settlement `0x9008…0ab41` | `raw/buyback_ethfi_all.json`, `raw/buyback_usdc_all.json` | 600-transfer API cap; program starts 2026-09-17, 566 matched orders |
| Funding | Blockscout v2 USDC transfers for `0xf40b…f7021` | `raw/funding_usdc_all.json` | 300 records; funding source, not proof of revenue |
| DEX depth | DexScreener `GET /latest/dex/tokens/{token}` | `raw/dex_token.json` | 9 Ethereum pairs; `liquidity.usd` summed |
| Slippage | Uniswap V3 QuoterV2 `quoteExactInputSingle` | `raw/dex_quotes.json` | $10k/−1.03%, $50k/−3.95%, $250k/−38.78% at WETH $1,744.44 |

## Aggregators (convenience, not primary)

| Series | Endpoint | Snapshot |
|---|---|---|
| Gross fees | `https://api.llama.fi/summary/fees/ether.fi?dataType=dailyFees` | `raw/ll_fees.json` |
| Protocol revenue | same, `dataType=dailyRevenue` | `raw/ll_revenue.json` |
| Holders revenue | same, `dataType=dailyHoldersRevenue` | `raw/ll_holders_rev.json` |
| TVL | `https://api.llama.fi/protocol/ether.fi` | `raw/ll_protocol.json` |
| Price / supply / mcap | CoinGecko `/coins/ether-fi` | `raw/cg_coin.json` |
| ETH price for quote USD | CoinGecko simple price | `raw/cg_eth_price.json` |

## Labels and confidence

- **Verified**: token supply, holder balances, transfers, CoW fills, DEX pool
  liquidity, QuoterV2 output.
- **Inferred**: the buyback Safe address came from a secondary BlockPinned
  lead; behaviour (CoW fills, funding, outflows) is consistent, but no signed
  statement from ether.fi confirms it. The Optimism cashback leg is inferred
  from `LZMultiCall`; recipient-level payment is **not** verified.
- **Lead**: `0x4ECF…D643` ($3.728M from the funding Safe) has no confirmed
  purpose; could be operations or a partner settlement.

## Refresh

```bash
python3 fetch_onchain.py --refresh
python3 build_outputs.py
python3 manifest.py
python3 check_site.py
```

`fetch_onchain.py` writes canonical filenames only. The Blockscout pagination
caps are deliberate (5 pages for holders, 12 for transfers); raise them only
with a note in the manifest. `dex_quotes.json` is a point-in-time fixture and
is not refreshed automatically because it requires constructing QuoterV2 calls
and an ETH/USD reference.
