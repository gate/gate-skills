# Scenarios

Behavior-oriented templates for `gate-exchange-earn`. All write paths require **Action Draft** and explicit **Y** before any `gate-cli` earn write command.

## Global execution gate (mandatory)

For any scenario that includes `gate-cli cex earn uni lend`, `gate-cli cex earn uni change`, `gate-cli cex earn fixed create`, `gate-cli cex earn dual place`, or `gate-cli cex earn staking swap`:

- Build and present an Action Draft first.
- Require **Y** or **N** from the immediately previous user turn for the exact drafted parameters.
- Treat confirmation as single-use; re-draft on any change.
- For multi-leg writes, confirm each leg separately.

## Scenario 1: Idle capital low-risk earn mix

**Context**: User wants recommendations for idle stablecoins or fiat-pegged funds across earn types without subscribing yet.

**Prompt Examples**:

- "I have 10,000 USDT idle and want low risk; what earn mix has the best indicative yield?"
- "Recommend conservative earn products for my spare USDT."

**Expected Behavior**:

1. Run parallel read commands such as `gate-cli cex earn fixed products`, `gate-cli cex earn fixed products-asset`, `gate-cli cex earn uni rate`, `gate-cli cex earn uni currency`, and `gate-cli cex earn dual plans` per `SKILL.md` Case 1.
2. Synthesize a ranked comparison with clear risk labels; do not promise returns.
3. Do not execute any write without a new user request and Action Draft + Y.

## Scenario 2: Compare dual vs staking for one coin

**Context**: User wants a read-only comparison of dual-currency and staking for the same asset (for example ETH).

**Prompt Examples**:

- "Compare ETH dual investment versus staking for expected yield and risk."
- "Which is safer for ETH, dual or staking?"

**Expected Behavior**:

1. Call `gate-cli cex earn dual plans` and `gate-cli cex earn staking find` with parameters per `--help`.
2. Optionally call `gate-cli info compliance check-token-security` for ETH; if empty, state that risk data is unavailable.
3. Output a structured comparison table; no `dual place` or `staking swap` unless the user later confirms a draft.

## Scenario 3: Subscribe flexible earn

**Context**: User asks to subscribe a stated amount to flexible (Simple Earn style) for a currency.

**Prompt Examples**:

- "Subscribe 2,000 USDT to flexible earn."
- "Lend 2,000 USDT to the flexible product."

**Expected Behavior**:

1. Preflight `--help` on `gate-cli cex earn uni lend` and related reads (`uni currency`, spot balance).
2. Present Action Draft with amount, indicative APR, and floating-yield disclaimer.
3. Only after **Y**, run `gate-cli cex earn uni lend` with the JSON body required by the CLI.
4. Verify with `gate-cli cex earn uni records` or equivalent read.

## Scenario 4: Redeem flexible partial amount

**Context**: User asks to redeem part of a flexible position.

**Prompt Examples**:

- "Redeem 500 USDT from flexible earn."
- "Withdraw 500 USDT from my flexible savings."

**Expected Behavior**:

1. Read position with `gate-cli cex earn uni records` (or as required by help) to confirm redeemable amount.
2. Action Draft with redeem amount and any window or timing notes from product rules.
3. Only after **Y**, run `gate-cli cex earn uni lend` with redeem semantics per CLI `--help`.
4. Do not auto-retry on failure.

## Scenario 5: Dual settled history by currency

**Context**: User wants read-only totals of recently settled dual orders broken down by currency.

**Prompt Examples**:

- "How much did my dual positions settle recently, per coin?"
- "Summarize my settled dual earn by settlement currency."

**Expected Behavior**:

1. Call `gate-cli cex earn dual orders` and `gate-cli cex earn dual balance` per Case 15.
2. Filter to settled success states as returned by the API; aggregate per user-requested dimensions.
3. Present APY or amounts consistently with CLI field semantics; no writes.

## Scenario 6: Write blocked without confirmation

**Context**: User states subscribe intent but does not reply Y after the draft.

**Prompt Examples**:

- "Yes sounds good" (ambiguous / not immediate Y after a new draft)
- User changes amount after saying yes once

**Expected Behavior**:

1. Do not call any earn write command.
2. If parameters changed after a prior Y, invalidate and issue a fresh Action Draft.
3. Remain in read-only or draft state until explicit **Y** matches the current draft.
