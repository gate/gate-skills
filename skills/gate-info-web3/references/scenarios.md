# gate-info-web3 — Scenarios & Prompt Examples

> Maps concrete prompts to a playbook id. **Web3** is the umbrella — do not default every row to “DeFi”.

## Scenario 1 — Address tracking (English)

**Playbook**: `address_tracking`

**Prompts**:
- "Track 0xabc... on eth"
- "What is this wallet doing"

**Expected behavior**:
1. Extract `address` + `chain`.
2. Run `get-address-info` (scope `full`) + optional `get-address-transactions`.
3. Six-section report; emphasize **identity clues + recent behavior**, not a safety verdict (that is `gate-info-risk`).

## Scenario 2 — Token on-chain / smart money

**Playbook**: `token_onchain`

**Prompts**:
- "ETH on-chain distribution analysis"
- "Smart money flows on ARB"

**Expected behavior**:
1. Extract `token` + `chain`.
2. Run `get-token-onchain` scope `full`.
3. Section 3 cites holder / smart-money fields from JSON; no fabricated levels.

## Scenario 3 — Entity / desk (no `get-entity-profile` in v0.5.2)

**Playbook**: `entity_intel`

**Prompts**:
- "What is Jump Trading doing recently"

**Expected behavior**:
1. Extract `entity_query`.
2. Run `news feed web-search` with a precise query string.
3. Label output as **media / open-web synthesis**, not on-chain ground truth. If the user also names a ticker, optionally add `search-news` for that coin (manual optional — verify flags).

## Scenario 4 — Protocol TVL / yield

**Playbook**: `protocol_platform`

**Prompts**:
- "How much is Uniswap TVL"
- "What is the USDC deposit APY on AAVE"

**Expected behavior**:
1. Extract `platform`; optional `asset` for yield pools.
2. Run `get-defi-overview` + `get-platform-info` / `get-platform-history` as needed; `get-yield-pools` when APY/TVL of a specific asset is asked.
3. Answer **scale + change**, not investment advice.

## Scenario 5 — Exchange reserves

**Playbook**: `exchange_reserves`

**Prompts**:
- "Binance BTC reserves"

**Expected behavior**:
1. Extract `exchange` + `asset`.
2. Run `get-exchange-reserves`.

## Scenario 6 — Liquidation heatmap

**Playbook**: `liquidation_heatmap`

**Prompts**:
- "At what price level is BTC liquidation density highest"

**Expected behavior**:
1. Extract `symbol` (e.g. BTC).
2. Run `get-liquidation-heatmap` with flags from `--help` if defaults are insufficient.

## Scenario 7 — Stablecoin + bridge (market structure)

**Playbook**: `stablecoin_bridge`

**Prompts**:
- "Stablecoin market share"
- "Which cross-chain bridge is the largest right now"

**Expected behavior**:
1. Run `get-stablecoin-info` + `get-bridge-metrics` in parallel.
2. Frame as **market-structure / infra**, not a single DEX protocol report.

## Scenario 8 — On-chain + sentiment

**Playbook**: `token_onchain_social`

**Prompts**:
- "Analyze SOL on-chain and check community sentiment"

**Expected behavior**:
1. Same as `token_onchain` plus `news` feed commands in the YAML extension.
2. Strictly separate **on-chain** vs **community** paragraphs.

## Anti-scenario — Risk-first

**Prompts**: "Will this address be blacklisted", "honeypot?"

**Route**: ``gate-info-risk`` — do **not** use `address_tracking` as a substitute for a verdict.
