# Order Management

This module handles Alpha order queries including single order status lookup, historical order filtering by currency/side/status, and time-range order searches.

## Workflow

### Step 1: Identify Query Type

Classify the request into one of four cases:
1. Check a specific order's status by order ID
2. View historical buy orders (filtered by currency and/or status)
3. View historical sell orders (filtered by currency and/or status)
4. Search orders within a time range

### Step 2: Call Tools and Extract Data

Use the minimal tool set required:
- Single order detail: `cex_alpha_get_alpha_order` with `order_id`
- Order list with filters: `cex_alpha_list_alpha_orders` with optional `currency`, `side`, `status`, `from`, `to`, `page`, `limit`

Order status enumeration:
- `0` = All (used as filter to return all statuses)
- `1` = Processing
- `2` = Success
- `3` = Failed
- `4` = Cancelled
- `5` = Transferring
- `6` = Cancelling transfer

Terminal statuses: 2 (Success), 3 (Failed), 4 (Cancelled).
Non-terminal statuses: 1 (Processing), 5 (Transferring), 6 (Cancelling transfer).

Key data to extract from each order:
- `order_id`: unique order identifier
- `currency`: token symbol
- `side`: buy or sell
- `currency_amount`: token quantity
- `status`: order status code
- `usdt_amount`: USDT value involved
- `tx_hash`: on-chain transaction hash
- `gas_fee`: gas fee (USDT)
- `transaction_fee`: transaction fee (USDT)
- `create_time`: order creation timestamp
- `failed_reason`: reason for failure (if applicable)

### Step 3: Return Formatted Result

Present order data in a clear format.

## Report Template

For single order detail:

```markdown
## Order Detail

| Item | Value |
|------|-------|
| Order ID | {order_id} |
| Currency | {currency} |
| Side | {side} |
| Token Amount | {currency_amount} |
| USDT Amount | {usdt_amount} |
| Status | {status_text} |
| Tx Hash | {tx_hash} |
| Gas Fee | {gas_fee} |
| Transaction Fee | {transaction_fee} |
| Created | {create_time} |
| Failed Reason | {failed_reason} |
```

For order list:

```markdown
## Alpha Order History

| Order ID | Currency | Side | Token Amount | USDT | Status | Time |
|----------|----------|------|--------|------|--------|------|
| {order_id} | {currency} | {side} | {currency_amount} | {usdt_amount} | {status_text} | {create_time} |

| **Filter** | {filter_description} |
| **Records Found** | {count} |
```

---

## Scenario 18: Check Order Status

**Context**: User wants to check the status of a specific order, typically one that was recently placed.

**Prompt Examples**:
- "我刚才那笔买单成功了吗？"
- "Check order status for order 12345"
- "那笔订单怎么样了？"

**Expected Behavior**:
1. Obtain the `order_id` from the user. If the order was placed in the current conversation, use the order ID from the previous order response. If the user doesn't provide an order ID, ask for it.
2. Call `cex_alpha_get_alpha_order` with `order_id={order_id}`.
3. Present the full order detail including status, amounts, transaction hash, fees, and timestamps.
4. Interpret the status for the user (e.g., "Your order was successful" for status 2, "Your order failed because..." for status 3).

## Scenario 19: View Historical Buy Orders

**Context**: User wants to see their buy order history, optionally filtered by currency and/or status.

**Prompt Examples**:
- "看看我买 ELON 的所有成功订单"
- "Show me my buy orders for trump"
- "我的买单记录"

**Expected Behavior**:
1. Extract filter criteria from the user request: currency symbol, status (if specified).
2. Call `cex_alpha_list_alpha_orders` with `side="buy"` and any additional filters:
   - `currency={symbol}` if a specific token is mentioned
   - `status={status_code}` if a specific status is mentioned (e.g., "成功" → `status=2`)
   - Default `status=0` (all) if not specified
3. Present the order list in a table with order ID, currency, amount, USDT amount, status, and creation time.
4. If there are more pages, inform the user and offer to show the next page.

## Scenario 20: View Historical Sell Orders

**Context**: User wants to see their sell order history, optionally filtered by currency and/or status.

**Prompt Examples**:
- "我卖 trump 的记录"
- "Show me my sell history for ELON"
- "看看我的卖单"

**Expected Behavior**:
1. Extract filter criteria from the user request: currency symbol, status (if specified).
2. Call `cex_alpha_list_alpha_orders` with `side="sell"` and any additional filters:
   - `currency={symbol}` if a specific token is mentioned
   - `status={status_code}` if a specific status is mentioned
   - Default `status=0` (all) if not specified
3. Present the order list in a table with order ID, currency, amount, USDT received, status, and creation time.
4. If there are more pages, inform the user and offer to show the next page.

## Scenario 21: Search Orders by Time Range

**Context**: User wants to see orders within a specific time period.

**Prompt Examples**:
- "最近 24 小时的买单"
- "Show me orders from this week"
- "昨天的所有订单"

**Expected Behavior**:
1. Parse the user's time range and convert to Unix timestamps for `from` and optionally `to`.
2. Extract any additional filters: `side` (buy/sell) and `currency` if mentioned.
3. Call `cex_alpha_list_alpha_orders` with `from={start_timestamp}`, `to={end_timestamp}` (if specified), and any additional filters. Use `status=0` to include all statuses unless the user specifies otherwise.
4. Present the order list in a table sorted by creation time.
5. If there are more pages, inform the user and offer to show the next page.
