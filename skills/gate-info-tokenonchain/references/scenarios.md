# gate-info-tokenonchain — Scenarios & Prompt Examples

## Scenario 1: Holder distribution

**Context**: User asks about concentration or top holders for a token.

**Prompt Examples**:
- "ETH holder distribution"
- "Who holds most BTC on-chain?"

**Expected Behavior**:
1. Set `scope` to include `holders`; pass `symbol`, optional `chain`, `time_range` per `SKILL.md`.
2. Parallel: `info_onchain_get_token_onchain`, `info_coin_get_coin_info` (`scope="basic"`).
3. Fill holder section of **Report Template**; shorten addresses for privacy.

## Scenario 2: Full on-chain overview (multi-scope)

**Context**: User wants an overall on-chain picture for one token.

**Prompt Examples**:
- "Full on-chain analysis for SOL"
- "ETH on-chain activity and large transfers"

**Expected Behavior**:
1. Use `scope` combining `holders`, `activity`, and `transfers` as appropriate.
2. Parallel on-chain + coin info calls per **Execution Workflow**.
3. Include health-score style synthesis only from returned data; no price targets.

## Scenario 3: Smart Money not available

**Context**: User asks for smart-money or unavailable scope.

**Prompt Examples**:
- "Smart money flows for ETH"
- "Track smart money on this token"

**Expected Behavior**:
1. State clearly that **Smart Money** is not available in this skill version (`SKILL.md` **Known Limitations**).
2. Offer `holders`, `activity`, or `transfers` only; do not approximate smart-money data.
3. If user agrees, run allowed scopes only.

## Scenario 4: Route to address tracker

**Context**: User gives a specific wallet address to track.

**Prompt Examples**:
- "Track this address 0x1234..."
- "What is this wallet doing?"

**Expected Behavior**:
1. Route to `gate-info-addresstracker` per **Routing Rules**; do not use `info_onchain_get_token_onchain` as a substitute for address-level tracking unless `SKILL.md` explicitly allows that tool for the same intent (it does not for single-address follow).
