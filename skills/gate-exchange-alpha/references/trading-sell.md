# Trading (Sell)

This module handles Alpha token sell operations including full position sell, partial sell, and sell with order tracking.

## Workflow

### Step 1: Identify Query Type

Classify the request into one of four cases:
1. Sell entire position of a **specific token** (full available balance)
2. Sell a partial amount (half, specific quantity, etc.)
3. Sell and track order result
4. **Batch sell all holdings** (sell everything in the account)

### Step 2: Resolve Currency Symbol

Before checking holdings, resolve the user's input to an exact currency symbol:

1. **Check holdings first**: Call `cex_alpha_list_alpha_accounts` to get all user holdings.
2. **Match against holdings**: Search for tokens in holdings whose `currency` contains the user's keyword (case-insensitive).
3. **Handle results**:
   - **Single match in holdings**: Proceed with that currency symbol.
   - **Multiple matches in holdings**: Present a numbered list of candidates and ask the user to choose:
     ```
     Found multiple tokens matching "trump" in your holdings:
     1. memeboxtrump - Available: 1000.5
     2. trumpwif - Available: 500.0
     Which one do you want to sell? (Enter number)
     ```
   - **No match in holdings**: Inform the user they don't hold any token matching that name.

### Step 3: Check Holdings, Quote, and Execute

All sell flows follow the same core pipeline:

1. **Check holdings**: Call `cex_alpha_list_alpha_accounts` to get the `available` balance for the target currency. Verify `available >= sell_amount`.
2. **Quote**: Call `cex_alpha_quote_alpha_order` with `currency`, `side="sell"`, `amount` (token quantity), `gas_mode="speed"` (default). Use `gas_mode="custom"` with `slippage` only if user specifies custom slippage.
3. **Confirm**: Present the quote details to the user and wait for explicit confirmation before proceeding.
4. **Execute**: Call `cex_alpha_place_alpha_order` with `currency`, `side="sell"`, `amount`, `quote_id`, and optional `gas_mode`/`slippage`.
5. **Track** (Case 13 only): Poll `cex_alpha_get_alpha_order` until a terminal status is reached.

Key parameters:
- `amount`: **Token quantity** when selling (NOT USDT). For full sell, use the entire `available` balance.
- `gas_mode`: `"speed"` (default) or `"custom"` (user-specified slippage). Note: API returns `gasMode` as `"1"` for speed mode, `"2"` for custom mode.
- `slippage`: percentage string, only used when `gas_mode="custom"`
- `quote_id`: obtained from the quote step, valid for **1 minute only**

### Step 3: Return Formatted Result

Present the order result using the appropriate template.

## Report Template

For quote confirmation (before placing order):

```markdown
## Sell Quote Confirmation

| Item | Value |
|------|-------|
| Currency | {currency} |
| Side | Sell |
| Quantity | {amount} {currency} |
| Available Balance | {available} {currency} |
| Gas Mode | {gas_mode} |
| Quote ID | {quote_id} |

Proceed with this order? (Yes/No)
```

For order result:

```markdown
## Sell Order Result

| Item | Value |
|------|-------|
| Order ID | {order_id} |
| Currency | {currency} |
| Side | Sell |
| Quantity | {amount} {currency} |
| USDT Received | {usdt_amount} USDT |
| Status | {status_text} |
| Tx Hash | {tx_hash} |
```

## Safety Rules

- **Mandatory confirmation**: NEVER place a sell order without explicit user confirmation after showing the quote.
- **Balance check**: Always verify `available >= sell_amount` before quoting. If insufficient, inform the user of their actual available balance.
- **Quote expiry**: `quote_id` is valid for 1 minute. Re-quote if confirmation is delayed.
- **Rate limits**: Quote endpoint is limited to 10 requests/second; order endpoint is limited to 5 requests/second.

---

## Scenario 11: Full Position Sell

**Context**: User wants to sell their entire holding of a specific token.

**Prompt Examples**:
- "把我的 ELON 全部卖掉"
- "Sell all my trump"
- "清仓 memeboxtrump"

**Expected Behavior**:
1. Call `cex_alpha_list_alpha_accounts` to get the user's holdings.
2. **Resolve currency symbol**:
   - Search holdings for tokens whose `currency` contains the user's keyword.
   - If multiple matches found, list candidates with their available balances and ask user to select.
   - If no match found, inform user they don't hold any matching token.
3. Find the target currency and extract the `available` balance. If `available` is 0, inform the user they have no holdings to sell.
4. Call `cex_alpha_quote_alpha_order` with `currency={resolved_symbol}`, `side="sell"`, `amount="{available}"`, `gas_mode="speed"`.
5. Present the quote details (including the full sell quantity and available balance) to the user and ask for confirmation.
6. Upon confirmation, call `cex_alpha_place_alpha_order` with `currency={resolved_symbol}`, `side="sell"`, `amount="{available}"`, `quote_id="{quote_id}"`, `gas_mode="speed"`.
7. Return the order result including order ID, status, and USDT received.

## Scenario 12: Partial Sell

**Context**: User wants to sell a portion of their holdings (half, a specific quantity, etc.).

**Prompt Examples**:
- "卖掉一半的 trump"
- "Sell 1000 ELON"
- "卖掉 30% 的 memeboxtrump"

**Expected Behavior**:
1. Call `cex_alpha_list_alpha_accounts` to get the user's holdings.
2. **Resolve currency symbol** (same as Scenario 11 step 2).
3. Find the target currency and extract the `available` balance.
4. Calculate the sell quantity based on the user's instruction:
   - "一半" / "half" → `available / 2`
   - Specific quantity → use the stated amount
   - Percentage → `available * percentage / 100`
4. Verify the calculated quantity does not exceed `available`. If it does, inform the user and suggest the maximum sellable amount.
5. Call `cex_alpha_quote_alpha_order` with `currency={resolved_symbol}`, `side="sell"`, `amount="{calculated_quantity}"`, `gas_mode="speed"`.
6. Present the quote details to the user and ask for confirmation.
7. Upon confirmation, call `cex_alpha_place_alpha_order` with the quote details.
8. Return the order result.

## Scenario 13: Sell and Track Result

**Context**: User wants to sell tokens and receive a follow-up on the result, including profit information.

**Prompt Examples**:
- "把 ELON 全卖了，卖完告诉我赚了多少"
- "Sell all my trump and tell me the result"
- "清仓 memeboxtrump，完成后告诉我"

**Expected Behavior**:
1. Execute the full sell flow (same as Scenario 11 or 12 depending on the sell quantity).
2. After placing the order, poll `cex_alpha_get_alpha_order` with `order_id` at 3-5 second intervals.
3. Continue polling until a terminal status is reached:
   - `2` = Success — report the completed order details including `usdt_amount` received.
   - `3` = Failed — report the failure reason.
   - `4` = Cancelled — report the cancellation.
4. If polling exceeds 60 seconds without reaching a terminal status, inform the user that the order is still processing and provide the order ID for manual follow-up.
5. On success, present the final order details with the USDT amount received.

## Scenario 14: Batch Sell All Holdings

**Context**: User wants to sell ALL tokens in their Alpha account, not just one specific token.

**Prompt Examples**:
- "把我 Alpha 持仓全部卖出"
- "Sell everything in my Alpha account"
- "清仓所有 Alpha 币"
- "给我alpha 持仓能卖的全部卖出"

**Expected Behavior**:
1. Call `cex_alpha_list_alpha_accounts` to get all user holdings.
2. Filter holdings where `available > 0` to get the list of sellable tokens.
3. If no sellable holdings, inform the user their Alpha account is empty.
4. **Present summary for confirmation** (DO NOT call quote for all tokens at once):
   ```
   You have the following tokens available to sell:
   
   | # | Currency | Available Balance |
   |---|----------|-------------------|
   | 1 | memeboxtrump | 1000.5 |
   | 2 | memeboxELON | 500.0 |
   | 3 | memeboxpepe | 200.0 |
   
   Do you want to sell ALL of these? (Yes/No)
   Or specify which ones to sell (e.g., "1 and 3" or "just trump")
   ```
5. **Upon user confirmation**, process tokens **one by one sequentially**:
   - For each token:
     a. Call `cex_alpha_quote_alpha_order` with `currency={symbol}`, `side="sell"`, `amount="{available}"`, `gas_mode="speed"`.
     b. Show brief quote info and ask for confirmation for THIS token.
     c. Upon confirmation, call `cex_alpha_place_alpha_order`.
     d. Report the result before moving to the next token.
6. After all tokens are processed, present a summary:
   ```
   ## Batch Sell Summary
   
   | Currency | Quantity Sold | USDT Received | Status |
   |----------|---------------|---------------|--------|
   | memeboxtrump | 1000.5 | 150.25 | Success |
   | memeboxELON | 500.0 | 75.50 | Success |
   | memeboxpepe | 200.0 | - | Failed (insufficient liquidity) |
   
   **Total USDT Received**: 225.75 USDT
   ```

**Safety Rules for Batch Sell**:
- **NEVER** call quote for all tokens simultaneously — process one by one.
- **ALWAYS** confirm with user before starting the batch process.
- **ALWAYS** confirm each individual token sale before executing.
- If any token fails, continue with the remaining tokens and report failures at the end.
- Respect rate limits: wait at least 200ms between quote calls to avoid hitting 10r/s limit.
