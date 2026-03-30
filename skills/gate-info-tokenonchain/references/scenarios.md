# gate-info-tokenonchain — Scenarios & Prompt Examples

## Scenario 1: Full token on-chain overview

**Context**: User asks for general on-chain picture of a token.

**Prompt Examples**:
- "ETH on-chain analysis"
- "SOL on-chain data"

**Expected Behavior**:
1. Set `scope` to include `holders`, `activity`, and `transfers` as appropriate; call in parallel `info_onchain_get_token_onchain` and `info_coin_get_coin_info`.
2. Output SKILL.md report with all requested sections; state **Smart Money not available** if user asks.

## Scenario 2: Holders or concentration only

**Context**: User focuses on distribution.

**Prompt Examples**:
- "Top ETH holders"
- "Is BTC supply concentrated"

**Expected Behavior**:
1. `scope=holders` (plus `info_coin_get_coin_info` in parallel).
2. Apply **Decision Logic** for concentration thresholds; no price predictions.

## Scenario 3: Large transfers / whale flow

**Context**: User asks about big moves.

**Prompt Examples**:
- "Large SOL transfers today"
- "Unusual whale movements for BTC"

**Expected Behavior**:
1. `scope=transfers` with sensible `time_range`; parallel coin info.
2. Label exchange addresses as best-effort per **Safety Rules**.

## Scenario 4: Smart Money requested (unsupported)

**Context**: User asks for smart money or `scope=smart_money`.

**Prompt Examples**:
- "What is smart money buying on ETH"

**Expected Behavior**:
1. Inform user that Smart Money is **not** in this skill version; offer holders / activity / transfers only. Do not invent smart-money data.

## Scenario 5: Address vs token — route away

**Context**: User pastes an address.

**Prompt Examples**:
- "Track 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

**Expected Behavior**:
1. Route to **`gate-info-addresstracker`**; do not use `info_onchain_get_token_onchain` as a substitute for address tracking.
