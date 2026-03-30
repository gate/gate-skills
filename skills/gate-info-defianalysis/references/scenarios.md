# gate-info-defianalysis — Scenarios & Prompt Examples

## Scenario 1: DeFi overview / TVL ranking

**Context**: User wants aggregate DeFi market view and top protocols.

**Prompt Examples**:
- "DeFi overview"
- "Top DeFi protocols by TVL"
- "What's total DeFi TVL"

**Expected Behavior**:
1. Route to **Sub-scenario A**: parallel `info_platformmetrics_get_defi_overview` (e.g. `category="all"`) and `info_platformmetrics_search_platforms` (e.g. `sort_by=tvl`, `limit=10`).
2. Output **Template A** per SKILL.md; note data gaps with "Data temporarily unavailable" if a tool fails.

## Scenario 2: Single protocol deep-dive

**Context**: User names one protocol (Uniswap, Aave, etc.).

**Prompt Examples**:
- "Uniswap TVL and volume"
- "Aave full metrics"

**Expected Behavior**:
1. **Sub-scenario B**: parallel `info_platformmetrics_get_platform_info`, `info_platformmetrics_get_platform_history`, and optionally `info_coin_get_coin_info` for the native token symbol.
2. Output **Template B**; competitive analysis from LLM only on MCP data.

## Scenario 3: Yield / stablecoins / bridges

**Context**: User asks for yield pools, stablecoin stats, or bridge volume.

**Prompt Examples**:
- "Best USDC lending APY"
- "Stablecoin market cap ranking"
- "Top bridges by volume"

**Expected Behavior**:
1. Map to **Sub-scenario C, D, or E**; call only the tools for that scenario. Use **progressive loading** for bridges/stablecoins: list first; user follow-up for chain-level detail.
2. Apply SKILL.md report guidance for templates C–E.

## Scenario 4: Exchange reserves / liquidation heatmap

**Context**: User asks for exchange on-chain reserves or liquidation density.

**Prompt Examples**:
- "Binance BTC reserves"
- "BTC liquidation heatmap"

**Expected Behavior**:
1. **Sub-scenario F or G** with extracted `exchange`, `asset`, or `symbol` per SKILL.md.
2. Reserve and liquidation disclaimers from **Safety Rules** must appear where relevant.

## Scenario 5: Route away — coin fundamentals only

**Context**: User wants a full coin thesis without DeFi/platform focus.

**Prompt Examples**:
- "Analyze SOL"
- "Is ETH worth buying"

**Expected Behavior**:
1. Route to **`gate-info-coinanalysis`** per Routing Rules; do not run DeFi platform tools for this intent.
