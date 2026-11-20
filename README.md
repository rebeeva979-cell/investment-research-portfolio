# Crypto Investment Research Portfolio — Marina Rebeeva

**On-chain research analyst · DeFi & digital assets · Minsk / remote**

[RU] Портфолио воспроизводимых исследований цифровых активов: on-chain forensics, tokenomics, supply reconciliation, ликвидность и Decision Cards с условиями отмены.  
[EN] A portfolio of reproducible digital-asset research: on-chain forensics, tokenomics, supply reconciliation, liquidity and decision cards with invalidation triggers.

## Start here

- **Bilingual portfolio (RU/EN):** [`docs/index.html`](docs/index.html)
- **ETHFI case:** [`docs/ethfi.html`](docs/ethfi.html) · [verification report](04_ETHFI/ETHFI_ONCHAIN_VERIFICATION_2026-11-20.md)
- **Method:** [`docs/method.html`](docs/method.html)
- **CV:** [`docs/cv.html`](docs/cv.html) · [PDF](docs/assets/Marina_Rebeeva_CV.pdf)
- **Casebook:** [`06_PORTFOLIO_CAREER/PORTFOLIO_CASEBOOK.md`](06_PORTFOLIO_CAREER/PORTFOLIO_CASEBOOK.md)
- **Status:** [`00_README/PROJECT_STATUS.md`](00_README/PROJECT_STATUS.md)

The root `index.html` redirects to `docs/`.

## Lead case — ETHFI

Question: does the documented buyback actually return value to ETHFI holders?

What the on-chain work found:

- 566 CoW trades bought **2,542,499 ETHFI for $1,645,541** (average $0.6472) between 17 September and 20 November 2026.
- The flow runs from Funding Safe `0xf40bcc…f7021` → Buyback Safe `0x43f4ca…6408c` → CoW `0x9008D1…0ab41` → an ops EOA and LayerZero.
- **No ETHFI went from the buyback Safe to sETHFI.** Holder revenue is **$0** over the last 30 and 90 days; the last non-zero observation is 1 April 2026.
- Buyback / revenue is **17.3%** over 30 days versus a 30% buyback allocation (60% including cashback, unverified); annualised it is 1.71% of market cap and covers ~26% of scheduled unlocks.
- Supply has three conflicting bases: on-chain 998,535,999; CoinGecko 998,535,999 (treats total as circulating); DefiLlama 983,600,557 + 16,399,443 locked = 1B. On-chain burn is 1,464,001.
- Top-10 wallets hold **62.19%** of supply; EOA float is 47.5% with a top-1 EOA at 21.4% of float.
- DEX depth is **$1.23M** (0.26% of market cap); a $250k sale costs ~38.8% by Uniswap QuoterV2.
- Decision: **WAIT, 0–2%**, with explicit upgrade and invalidation triggers.

Full numbers, sources and limitations: [`04_ETHFI/ETHFI_ONCHAIN_VERIFICATION_2026-11-20.md`](04_ETHFI/ETHFI_ONCHAIN_VERIFICATION_2026-11-20.md).

## Other cases

| Case | Question | Status |
|---|---|---|
| [LTC](01_LTC/LTC_RESEARCH_MEMO.md) | Is Litecoin's security paid for by real demand or by emissions? | `wait`, max 3% |
| [SNX](02_SNX/SNX_SIP423_RESEARCH_REPORT_2026-11-19.md) | Does SIP-423 lock remove sell-side risk? | `defensive`, 0% now |
| [LYFT](05_OTHER_ASSETS/LYFT_RESEARCH_BRIEF.md) | Do rides convert into normalised FCF? | `wait`, max 3% |
| [GPRO](05_OTHER_ASSETS/GPRO_RESEARCH_BRIEF.md) | Merger probability vs residual downside | `wait`, max 1% |
| [ZNTL](05_OTHER_ASSETS/ZNTL_RESEARCH_BRIEF.md) | Cash runway, clinical risk and dilution | `wait`, max 0.5% |
| [ANT](05_OTHER_ASSETS/ANTHROPIC_RESEARCH_BRIEF.md) | IPO valuation, dilution and compute commitments | `wait`, max 0.5% |

## Structure

```text
docs/                       public bilingual site (GitHub Pages root)
   index.html               proof-first home
   ethfi.html               full ETHFI case
   method.html              evidence taxonomy, pipeline, checklists
   cv.html                  web CV + PDF
   assets/                  CSS, JS, SVG charts, CSV, PDFs
00_README/                  status register, legacy index
01_LTC/ … 05_OTHER_ASSETS/  research cases and data packs
04_ETHFI/                   ETHFI thesis, model, risk, on-chain report
   onchain/                  reproducible fetch → build → check pipeline
06_PORTFOLIO_CAREER/        casebook, IPS, work plan, CV/LinkedIn copy
07_PUBLICATION/             legacy publication builds
```

## Reproducibility

The ETHFI case is generated from committed public-API snapshots in [`04_ETHFI/onchain/`](04_ETHFI/onchain/):

```text
fetch_onchain.py → raw/*.json → build_outputs.py → data/*.csv + assets/*.svg → docs/
                         │
                    manifest.py (SHA-256)
                         │
                    check_site.py (links, tables, numbers, CSV drift)
```

```bash
make build      # rebuild metrics and charts from the committed snapshots
make check      # manifest + 9 unit tests + site consistency
make refresh    # fetch a new snapshot, then rebuild
```

Primary sources: Ethereum RPC, Blockscout, CoW Protocol API, Uniswap QuoterV2. Aggregators: DefiLlama, CoinGecko, DexScreener. No paid terminals or API keys are used. Every input is pinned by SHA-256 in `MANIFEST.csv`; see `04_ETHFI/onchain/SOURCES.md` for the verified / inferred / lead split.

## Publish

1. Create a GitHub repository and push this folder.
2. Settings → Pages → Source: `Deploy from a branch` → `main` / `/docs`.
3. Verify `/`, `/ethfi.html`, `/method.html`, `/cv.html`, the PDF and CSV in an incognito window.
4. Add the final URL to `docs/cv.html`, the CV PDF and LinkedIn (see [`06_PORTFOLIO_CAREER/CV_LINKEDIN_COPY_2026-11-20.md`](06_PORTFOLIO_CAREER/CV_LINKEDIN_COPY_2026-11-20.md)).

## Disclaimer

Personal research and a portfolio project, not client asset management or individual investment advice. All market and on-chain values are point-in-time and can change. Address labels are heuristics, not legal identity.
