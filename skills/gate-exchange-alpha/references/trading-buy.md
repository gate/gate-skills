# Trading (Buy)

This module handles Alpha token buy operations including market buy, custom slippage buy, and buy with order tracking.

## Workflow

### Step 1: Identify Query Type

Classify the request into one of three cases:
1. Market buy with default settings
2. Buy with custom slippage
3. Buy and track order result

### Step 2: Resolve Currency Symbol

Before validating and quoting, resolve the user's input to an exact currency symbol:

1. **Try exact match first**: Call `cex_alpha_list_alpha_currencies` with `currency={user_input}`.
2. **If no exact match**: Call `cex_alpha_list_alpha_currencies` without currency filter, then search results for tokens whose `currency` or `name` contains the user's keyword (case-insensitive).
3. **Handle results**:
   - **Single match**: Proceed with that currency symbol.
   - **Multiple matches**: Present a numbered list of candidates and ask the user to choose:
     ```
     Found multiple tokens matching "trump":
     1. memeboxtrump (TRUMP) - SOL chain
     2. trumpwif (TRUMPWIF) - ETH chain
     Which one do you want to buy? (Enter number)
     ```
   - **No match**: Inform the user that no token was found and suggest checking the token name.

### Step 3: Validate, Quote, and Execute

All buy flows follow the same core pipeline:

1. **Validate**: Call `cex_alpha_list_alpha_currencies` with `currency={symbol}` to confirm the token exists and `status=1` (actively trading).
2. **Quote**: Call `cex_alpha_quote_alpha_order` with `currency`, `side="buy"`, `amount` (USDT quantity), `gas_mode="speed"` (default). Use `gas_mode="custom"` with `slippage` only if user specifies custom slippage.
3. **Confirm**: Present the quote details to the user and wait for explicit confirmation before proceeding.
4. **Execute**: Call `cex_alpha_place_alpha_order` with `currency`, `side="buy"`, `amount`, `quote_id`, and optional `gas_mode`/`slippage`.
5. **Track** (Case 10 only): Poll `cex_alpha_get_alpha_order` until a terminal status is reached.

Key parameters:
- `amount`: USDT quantity when buying (e.g., `"5"` means 5 USDT)
- `gas_mode`: `"speed"` (default, smart mode) or `"custom"` (user-specified slippage). Note: API returns `gasMode` as `"1"` for speed mode, `"2"` for custom mode.
- `slippage`: percentage string (e.g., `"10"` for 10%), only used when `gas_mode="custom"`
- `quote_id`: obtained from the quote step, valid for **1 minute only**

### Step 3: Return Formatted Result

Present the order result using the appropriate template.

## Report Template

For quote confirmation (before placing order):

```markdown
## Buy Quote Confirmation

| Item | Value |
|------|-------|
| Currency | {currency} |
| Side | Buy |
| Amount | {amount} USDT |
| Gas Mode | {gas_mode} |
| Slippage | {slippage}% |
| Quote ID | {quote_id} |

Proceed with this order? (Yes/No)
```

For order result:

```markdown
## Buy Order Result

| Item | Value |
|------|-------|
| Order ID | {order_id} |
| Currency | {currency} |
| Side | Buy |
| Amount | {amount} USDT |
| Status | {status_text} |
| Tx Hash | {tx_hash} |
```

## Safety Rules

- **Mandatory confirmation**: NEVER place an order without explicit user confirmation after showing the quote.
- **Quote expiry**: `quote_id` is valid for 1 minute. If the user takes longer to confirm, re-quote before placing the order.
- **Token validation**: Always verify `status=1` before quoting. If suspended (2) or delisted (3), inform the user and abort.
- **Rate limits**: Quote endpoint is limited to 10 requests/second; order endpoint is limited to 5 requests/second.

---

## Scenario 8: Market Buy

**Context**: User wants to buy a token with USDT using default settings (smart gas mode).

**Prompt Examples**:
- "帮我买 5u ELON"
- "Buy 10 USDT worth of trump"
- "I want to buy 50u of memeboxtrump"

**Expected Behavior**:
1. Extract the currency keyword and USDT amount from the user request.
2. **Resolve currency symbol**:
   - Call `cex_alpha_list_alpha_currencies` with `currency={keyword}` for exact match.
   - If no result, search all currencies for tokens containing the keyword in `currency` or `name`.
   - If multiple matches found, list candidates and ask user to select.
   - If no match found, inform user and abort.
3. Call `cex_alpha_list_alpha_currencies` with `currency={resolved_symbol}` to verify the token is actively trading (`status=1`).
4. Call `cex_alpha_quote_alpha_order` with `currency={resolved_symbol}`, `side="buy"`, `amount="{usdt_amount}"`, `gas_mode="speed"`.
5. Present the quote details to the user and ask for confirmation.
6. Upon confirmation, call `cex_alpha_place_alpha_order` with `currency={resolved_symbol}`, `side="buy"`, `amount="{usdt_amount}"`, `quote_id="{quote_id}"`, `gas_mode="speed"`.
7. Return the order result including order ID and status.

## Scenario 9: Custom Slippage Buy

**Context**: User wants to buy a token with a specific slippage tolerance.

**Prompt Examples**:
- "帮我买 100u ELON，滑点设 10%"
- "Buy 50u trump with 5% slippage"
- "买 200u memeboxtrump，滑点 15"

**Expected Behavior**:
1. Extract the currency keyword, USDT amount, and slippage percentage from the user request.
2. **Resolve currency symbol** (same as Scenario 8 step 2).
3. Call `cex_alpha_list_alpha_currencies` with `currency={resolved_symbol}` to verify the token is actively trading.
4. Call `cex_alpha_quote_alpha_order` with `currency={resolved_symbol}`, `side="buy"`, `amount="{usdt_amount}"`, `gas_mode="custom"`, `slippage="{slippage_pct}"`.
5. Present the quote details (including the custom slippage) to the user and ask for confirmation.
6. Upon confirmation, call `cex_alpha_place_alpha_order` with `currency={resolved_symbol}`, `side="buy"`, `amount="{usdt_amount}"`, `quote_id="{quote_id}"`, `gas_mode="custom"`, `slippage="{slippage_pct}"`.
7. Return the order result including order ID and status.

## Scenario 10: Buy and Track Result

**Context**: User wants to buy a token and receive a follow-up on whether the order succeeded.

**Prompt Examples**:
- "买 100u 的 ELON，买完告诉我结果"
- "Buy 50u trump and let me know when it's done"
- "帮我买 10u memeboxtrump，买完告诉我"

**Expected Behavior**:
1. Execute the full buy flow (same as Scenario 8 or 9 depending on whether slippage is specified).
2. After placing the order, poll `cex_alpha_get_alpha_order` with `order_id` at 3-5 second intervals.
3. Continue polling until a terminal status is reached:
   - `2` = Success — report the completed order details.
   - `3` = Failed — report the failure reason.
   - `4` = Cancelled — report the cancellation.
4. If polling exceeds 60 seconds without reaching a terminal status, inform the user that the order is still processing and provide the order ID for manual follow-up.
5. On success, present the final order details including any returned `usdt_amount` or token quantity received.
