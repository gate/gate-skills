# gate-info-web3 — Troubleshooting

## `get-address-info --scope with-defi` in the PRD

v0.5.2 exposes `scope` as **`basic` / `full`** for this tool. Use **`full`** for the richest address context (closest to “with DeFi / full portrait”).

## `trace-fund-flow` / `get-entity-profile` missing

- **Fund flow**: use `get-address-info` + `get-address-transactions` (and optional `get-transaction` per hash).
- **Entity**: use `news feed web-search` until `get-entity-profile` ships; label results as **open-web / media**, not raw chain state.

## User pastes a transaction hash

If the question is **about one tx**, run:

`gate-cli info onchain get-transaction --format json` (add flags per `--help`).

This is an optional branch **outside** default playbooks — only when a hash is present.

## `search-platforms` / `get-liquidation-heatmap` flag errors

Always read `gate-cli info platformmetrics <cmd> --help` before adding flags. Different CLI builds may require extra parameters (e.g. contract type, interval).

## News commands expect a ticker

`search-news` uses `--coin` with a **symbol** (e.g. `SOL`). If the user only gives a contract address, resolve chain + symbol first or ask.

## Cross-skill confusion

- **Risk verdict** (safe or not) → `gate-info-risk`.
- **Investment-style research** without on-chain focus → `gate-info-research`.
- This skill: **behavior, structure, flows, infra** — neutral Web3 framing, not DeFi-only.
