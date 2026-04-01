# gate-info-defianalysis — Scenarios & Prompt Examples

## Scenario 1: DeFi overview and TVL ranking

**Context**: User wants a broad DeFi snapshot and top protocols by TVL.

**Prompt Examples**:
- "Give me a DeFi overview"
- "Top DeFi protocols by TVL this week"
- "DeFi TVL ranking"

**Expected Behavior**:
1. Execute Sub-scenario A: call `info_platformmetrics_get_defi_overview` with `category="all"` and `info_platformmetrics_search_platforms` with `sort_by="tvl", limit=10` in parallel.
2. Fill **Template A: DeFi Overview** in `SKILL.md` (market summary + platform table).
3. Call only MCP tools listed in `SKILL.md`.

## Scenario 2: Single platform deep-dive

**Context**: User asks for detailed metrics on a named protocol.

**Prompt Examples**:
- "What is Uniswap TVL and trading volume?"
- "Show me Aave full metrics and history"

**Expected Behavior**:
1. Execute Sub-scenario B: parallel `info_platformmetrics_get_platform_info` (`platform_name`, `scope="full"`), `info_platformmetrics_get_platform_history` (`metrics` include tvl/volume), and `info_coin_get_coin_info` for the native token symbol when applicable.
2. Produce the platform deep-dive sections per **Report Template** in `SKILL.md`.
3. If history is empty, note limitations; do not invent values.

## Scenario 3: Partial tool failure (degradation)

**Context**: One platform-metrics call fails while others succeed.

**Prompt Examples**:
- "Compound metrics" (assume `get_platform_history` errors)

**Expected Behavior**:
1. Per **Error Handling** in `SKILL.md`: skip the failed section; label "Data temporarily unavailable" for that dimension.
2. Continue with successful tool outputs (e.g. still show `get_platform_info` if it succeeded).
3. Do not fabricate historical series or TVL numbers.

## Scenario 4: Route to single-coin fundamentals

**Context**: User wants coin-only analysis without DeFi protocol focus.

**Prompt Examples**:
- "Analyze SOL fundamentals only"
- "Is ETH a good long-term hold?" (fundamentals-only framing)

**Expected Behavior**:
1. Route to `gate-info-coinanalysis` per **Routing Rules**; do not run DeFi sub-scenarios A–G.
2. Do not call `info_platformmetrics_*` for this intent unless the user explicitly asks DeFi/protocol questions in the same turn after clarification.
