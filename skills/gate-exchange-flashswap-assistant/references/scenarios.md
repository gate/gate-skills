# Scenarios

## Scenario 1: One-to-One Flash Swap With Confirmation

**Context**: The user wants to sell a known amount of one asset for another using flash swap, sees the quote, and confirms execution.

**Prompt Examples**:

- "Flash swap 1 BTC to USDT and execute after I confirm."
- "Preview selling 2 ETH for BTC via flash convert, then create if I say yes."

**Expected Behavior**:

1. Call `gate-cli cex flash-swap pairs` and `gate-cli cex spot account get` in parallel for the sell asset.
2. Verify amount is between `sell_min_amount` and `sell_max_amount`; if over max, plan S6 batches or explain the cap.
3. Call `gate-cli cex flash-swap preview-v1`, present Action Draft with `valid_timestamp`, wait for **Y**.
4. Call `gate-cli cex flash-swap create-v1` with the returned `quote_id` and matching amounts.
5. Report `status` and final amounts; on failure, suggest a fresh preview.

## Scenario 2: Many-to-One Consolidation With Skipped Legs

**Context**: The user names several alts to convert into USDT; some balances are below flash minimum or zero.

**Prompt Examples**:

- "Flash swap my SHIB, DOGE, and PEPE balances into USDT."
- "Convert FLOKI, BONK, and WIF to USDT; skip what cannot trade and tell me why."

**Expected Behavior**:

1. For each asset, parallel `gate-cli cex spot account get` and `gate-cli cex flash-swap pairs`.
2. Build **will execute** vs **skipped** tables with reasons (zero, below min, unsupported pair).
3. If the execute set is non-empty, call `gate-cli cex flash-swap preview-many-to-one`, highlight preview errors per leg.
4. Action Draft with both tables; after **Y**, call `gate-cli cex flash-swap create-many-to-one` excluding failed preview legs.
5. Verify each leg status separately.

## Scenario 3: Below-Minimum Balance Diagnosis (S5)

**Context**: The user suspects a balance is too small for flash swap.

**Prompt Examples**:

- "I only have a tiny PEPE balance; can I flash swap it to USDT?"
- "Is my FLOKI enough for flash swap? What is the minimum?"

**Expected Behavior**:

1. Call `gate-cli cex flash-swap pairs` and `gate-cli cex spot account get` for the asset.
2. If available < `sell_min_amount`, **do not** call fc preview; show balance vs minimum gap.
3. Optionally call `gate-cli cex wallet balance small`; if the asset appears, explain the separate **dust → GT** path and require S7 confirmation for convert.
4. If the user then increases balance or switches intent, continue with S1 only after gates pass.

## Scenario 4: Dust to GT (S7)

**Context**: The user wants to recycle small balances to GT, not USDT flash.

**Prompt Examples**:

- "List my convertible dust and convert DOGE and SHIB to GT."
- "Convert all eligible small balances to GT after you show the list."

**Expected Behavior**:

1. Call `gate-cli cex wallet balance small` and present the list.
2. Action Draft must state **GT** outcome and exact `currencies` or `is_all`; wait for **Y**.
3. Call `gate-cli cex wallet balance convert-small` only after confirmation.
4. Optionally call `gate-cli cex wallet balance small-history` to summarize recent conversions.

## Scenario 5: Route to Trading Copilot for Pure Spot Buy

**Context**: The user asks to buy multiple coins with USDT using spot-style language without flash/convert anchoring.

**Prompt Examples**:

- "Use 3000 USDT to buy BTC, ETH, and SOL with 1000 each."
- "Market buy a little BTC and ETH with my USDT."

**Expected Behavior**:

1. Detect dominant **buy / market buy** wording without flash swap or convert anchor.
2. Do **not** call `cex_fc_*` tools; instruct to use **`gate-exchange-trading`** (or equivalent spot trading skill) for spot orders.
3. If the user clarifies they want **flash convert** explicitly, switch to S2 and proceed with this skill.
