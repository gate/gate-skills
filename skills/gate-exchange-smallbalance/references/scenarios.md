# Small Balance Scenarios

## Scenario 1: List Eligible Dust and Estimated GT

**Context**: The user wants to see which spot holdings qualify as small balances and how much GT they might receive, without converting yet.

**Prompt Examples**:
- "What small balances can I convert to GT?"
- "Do I have any dust to clean up?"
- "How much GT would I get from my dust?"
- "My wallet is messy — what can I convert?"

**Expected Behavior**:
1. Set intent to `list`
2. Call `cex_wallet_list_small_balance` with no required parameters
3. If the tool returns a nested array, use the **inner** list of rows (see SKILL.md **Payload note**)
4. If that list is empty or missing, tell the user no eligible small-balance assets were found
5. If non-empty, show a table using `currency`, `available_balance`, `estimated_as_btc`, `convertible_to_gt`
6. Offer optional next step: convert selected or all (without calling convert until the user confirms)

## Scenario 2: Convert Selected Currencies to GT

**Context**: The user names specific tickers to convert into GT using the small-balance product.

**Prompt Examples**:
- "Convert FLOKI and MBLK dust to GT"
- "Please convert my small SHIB balance to GT"
- "Turn these dust coins into GT: PEPE, FLOKI"

**Expected Behavior**:
1. Set intent to `convert_selected` and extract `currencies`
2. Optionally call `cex_wallet_list_small_balance` to verify those tickers appear eligible (unwrap nested list per SKILL **Payload note**)
3. Confirm with the user the exact currency list and that conversion is irreversible
4. Call `cex_wallet_convert_small_balance` with non-empty `currencies` and `is_all: false`
5. Report real API success or error; never fabricate GT amounts

## Scenario 3: Convert All Eligible Small Balances

**Context**: The user wants a one-shot cleanup of every eligible dust balance.

**Prompt Examples**:
- "Convert all my small balances to GT"
- "One-click convert all dust"
- "Clean up all eligible dust into GT"

**Expected Behavior**:
1. Set intent to `convert_all`
2. Recommend listing first with `cex_wallet_list_small_balance` so the user sees scope
3. Obtain explicit confirmation to convert **all** eligible assets and warn irreversibility
4. Call `cex_wallet_convert_small_balance` with `is_all: true`
5. Summarize the API outcome honestly

## Scenario 4: Small Balance Conversion History

**Context**: The user wants past records of dust-to-GT conversions.

**Prompt Examples**:
- "Show my small balance conversion history"
- "How much GT did I get from dust last time?"
- "List recent dust conversions for FLOKI"

**Expected Behavior**:
1. Set intent to `history` and extract optional `currency`, `page`, `limit`
2. Call `cex_wallet_list_small_balance_history` with those optional filters
3. Parse the **nested** response: rows are in the **inner** array (`id`, `create_time`, `currency`, `amount`, `gt_amount`)
4. Present a table; convert `create_time` from Unix seconds to a readable time for the user
5. If the inner list is empty or missing, state that clearly

## Scenario 5: Out of Scope — Normal Spot Sell

**Context**: The user intends to sell a large spot position at market or limit, not dust consolidation.

**Prompt Examples**:
- "Sell 1 BTC for USDT"
- "Place a limit order to sell my ETH"

**Expected Behavior**:
1. Classify as `exclude` for this Skill
2. Do not call `cex_wallet_convert_small_balance` for that goal
3. Direct the user to the appropriate **spot trading** flow or Skill
