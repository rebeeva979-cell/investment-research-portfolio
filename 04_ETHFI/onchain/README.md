# ETHFI on-chain pipeline

Reproducible evidence for the ether.fi (ETHFI) case in `docs/ethfi.html` and
`04_ETHFI/ETHFI_ONCHAIN_VERIFICATION_2026-11-20.md`.

The pipeline has three stages and no third-party runtime dependencies:

```
fetch_onchain.py  ->  raw/*.json  ->  build_outputs.py  ->  data/*.csv + assets/*.svg
                          |
                     manifest.py  (SHA-256 of every input)
                          |
                     check_site.py (links / tables / numbers / CSV drift)
```

`raw/` is the point-in-time evidence (2026-11-20). `data/` and `assets/` are
generated and copied into `docs/` for the site. Do not edit them by hand.

## Run

```bash
cd 04_ETHFI/onchain

# offline: rebuild from committed snapshots
python3 build_outputs.py

# refresh snapshots from public APIs, then rebuild
python3 fetch_onchain.py --refresh
python3 build_outputs.py
python3 manifest.py

# consistency gate (run from repository root or here)
python3 check_site.py
```

From the repository root:

```bash
make build      # rebuild metrics + charts
make check      # manifest + unit tests + site consistency
make test       # unit tests only
```

## What each file is

| File | Purpose |
|---|---|
| `fetch_lib.py` | cached stdlib HTTP helper; raw bodies are the cache |
| `fetch_onchain.py` | refresh RPC supply, Blockscout holders/transfers, DexScreener, DefiLlama, CoinGecko |
| `build_outputs.py` | metrics, CSVs, five hand-written SVG charts |
| `manifest.py` | write/verify `MANIFEST.csv` |
| `check_site.py` | fail if links, tables, quoted numbers or site CSVs drift |
| `SOURCES.md` | source register, confidence levels, refresh caveats |
| `raw/` | committed public-API snapshots (13 files, ~9 MB) |
| `data/` | generated CSVs served by the site |
| `assets/` | generated SVGs used by the site |

## Inputs that are intentionally point-in-time

- `rpc_supply.json` — block 26,457,647.
- `holders_top.json` — top 250 only; the token has 93,377 holders.
- `buyback_*_all.json` — Blockscout pagination cap (600 records). The observed
  program starts 2026-09-17, so the cap does not truncate the event window.
- `dex_quotes.json` — QuoterV2 fixture; not auto-refreshed.

See `SOURCES.md` for the verified / inferred / lead split.
