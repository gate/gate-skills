# gate-info-coincompare — Scenarios & Prompt Examples

## Scenario 1: Compare three coins (English) — spec path

**Context**: User wants to compare BTC, ETH, and SOL.

**Prompt Examples**:
- "Compare BTC, ETH, SOL"
- "Which of these coins is stronger: BTC, ETH, SOL"

**Expected Behavior**:
1. Parse coin list: BTC, ETH, SOL. **Spec path**: call `info_marketsnapshot_batch_market_snapshot`(symbols=[BTC,ETH,SOL], timeframe=1d, source=spot) and `info_coin_search_coins` (query or symbol list). **Fallback**: if batch/search not available, for each coin call `info_coin_get_coin_info` + `info_marketsnapshot_get_market_snapshot` (same timeframe/source).
2. Output **5-section report**: (1) Key Metrics Comparison, (2) Fundamentals Comparison, (3) Technical Comparison (if requested), (4) Comparative Summary, (5) Dimension-by-Dimension Winners; plus Risk Warnings. Use "Data unavailable" if a tool fails.

## Scenario 2: Compare two coins (Chinese)

**Context**: User wants to compare SOL and AVAX.

**Prompt Examples**:
- "Compare SOL and AVAX"
- "Which is stronger among SOL, AVAX"

**Expected Behavior**:
1. Parse coins: SOL, AVAX. Same tool strategy as Scenario 1 (spec then fallback); same timeframe/source for both.
2. Return 5-section comparison + Risk Warnings; read-only.

## Scenario 3: Implicit comparison

**Context**: User asks which coin is stronger among several.

**Prompt Examples**:
- "SOL vs ETH, which is better right now?"

**Expected Behavior**:
1. Extract SOL, ETH; use same timeframe (e.g. 1d) and source (spot). Call `info_marketsnapshot_batch_market_snapshot` + `info_coin_search_coins`, or per-coin `info_coin_get_coin_info` + `info_marketsnapshot_get_market_snapshot`.
2. Output 5-section report (Key Metrics, Fundamentals, Comparative Summary, Dimension-by-Dimension Winners, Risk Warnings) with relative strength and key differences.

## Scenario 4: Only one coin (route or ask)

**Context**: User gives only one coin — do not run full comparison.

**Prompt Examples**:
- "Compare SOL"
- "Compare BTC"

**Expected Behavior**:
1. Ask user for at least one more coin to compare, or route to **gate-info-coinanalysis** for single-coin analysis.
2. Do not produce a comparison report with a single coin.
