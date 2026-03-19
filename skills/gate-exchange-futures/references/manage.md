# Gate Futures Price-Triggered Orders — Manage (List / Cancel / Amend)

This reference covers querying, cancelling, and amending existing futures price-triggered orders.

---

## Available operations

| Operation | API tool | When to use |
|-----------|----------|-------------|
| List open orders | `cex_fx_list_fx_price_triggered_orders` | "Show my TP/SL orders", "List conditional orders" |
| Get order detail | `cex_fx_get_fx_price_triggered_order` | "Show details of order #123" |
| Cancel single | `cex_fx_cancel_fx_price_triggered_order` | "Cancel that stop loss", "Cancel order #456" |
| Cancel all | `cex_fx_cancel_fx_price_triggered_order_list` | "Cancel all TP/SL for BTC", "Cancel all triggered orders" |
| Amend order | `cex_fx_update_fx_price_triggered_order` | "Change TP to 73000", "Update trigger price", "Amend size" |

---

## Workflow

### 1. Identify operation

Parse user intent to determine which operation to perform (list / get detail / cancel single / cancel all / amend).

Key data to extract:
- `operation` — one of: list, detail, cancel_single, cancel_all, amend
- `contract` (optional) — filter by contract (e.g. BTC_USDT)
- `order_id` (optional) — specific order to act on

### 2. Execute operation

Route to the matching operation below.

Key data to extract (varies by operation):
- **List**: `status` (`"open"` or `"finished"`), `contract`, `limit`, `offset`
- **Detail**: `order_id`
- **Cancel single**: `order_id`
- **Cancel all**: `contract` (optional; omit to cancel all contracts)
- **Amend**: `order_id`, changed fields (`trigger_price`, `price`, `size`, `price_type`, `close`)

### 3. Confirm before destructive actions

For cancel and amend operations, show summary and ask user to confirm before calling the API.

### 4. Verify

After cancel or amend, call `cex_fx_get_fx_price_triggered_order` or `cex_fx_list_fx_price_triggered_orders` to confirm the result.

Key data to extract:
- `status` — should be `cancelled` (after cancel) or `open` (after amend)

---

## List price-triggered orders

### Parameters

```
cex_fx_list_fx_price_triggered_orders(
  settle   = "usdt",
  status   = "open",       # "open" for active; "finished" for history
  contract = "BTC_USDT",   # optional: filter by contract
  limit    = 20,           # optional: default 20, max 100
  offset   = 0             # optional: pagination offset
)
```

### Display format

Show a table of results:

```
Open Price-Triggered Orders (BTC_USDT)
─────────────────────────────────────────────────────────────────
ID      Contract   Trigger             Execute    Size      Type
123     BTC_USDT   >= 72000            Market     close all TP (Long)
124     BTC_USDT   <= 58000            Limit 57800 close all SL (Long)
125     ETH_USDT   <= 3000             Market     -5        Conditional Short
```

**Determining type for display**:
- `order_close = true` or `order_reduce_only = true` → TP or SL (check trigger_rule vs position side)
- Neither flag → Conditional open (check size sign: positive = long open, negative = short open)

### Workflow

1. Call `cex_fx_list_fx_price_triggered_orders(settle="usdt", status="open")`.
2. If no orders, say "No open price-triggered orders found."
3. If orders found, display the table above.
4. Offer to show details, cancel, or amend.

---

## Get order detail

```
cex_fx_get_fx_price_triggered_order(
  settle   = "usdt",
  order_id = "123"
)
```

Display all fields: contract, trigger price, trigger rule, execution price, size, reduce_only, close, status, creation time.

---

## Cancel a single order

### Workflow

1. **Locate order**: if user provides an order ID, use it directly. If not, call `cex_fx_list_fx_price_triggered_orders` to show open orders and let user identify the one to cancel.
2. **Confirm**: ask *"Cancel price-triggered order #[id] for [contract] (trigger [rule] [price])? Reply to confirm."*
3. **Cancel**: call `cex_fx_cancel_fx_price_triggered_order(settle, order_id)`.
4. **Verify**: call `cex_fx_get_fx_price_triggered_order(settle, order_id)` → confirm status is `cancelled`.

```
cex_fx_cancel_fx_price_triggered_order(
  settle   = "usdt",
  order_id = "123"
)
```

---

## Cancel all orders

### Workflow

1. **Clarify scope**: does user want to cancel all orders for a specific contract, or all contracts?
2. **Confirm**: show scope and ask *"Cancel all price-triggered orders for [BTC_USDT / all contracts]? Reply to confirm."*
3. **Cancel all**: call `cex_fx_cancel_fx_price_triggered_order_list`.
4. **Verify**: call `cex_fx_list_fx_price_triggered_orders(settle, status="open")` → confirm list is empty (or reduced).

```
cex_fx_cancel_fx_price_triggered_order_list(
  settle   = "usdt",
  contract = "BTC_USDT"   # optional: omit to cancel all contracts
)
```

---

## Amend an order

Supports updating: trigger price, execution price, order size, price type, auto_size, close flag.

**Important limitation**: only **TP/SL orders** (order_type contains `plan-close-*`, or has `reduce_only`/`close` flag) can be amended via API. **Conditional open orders created via API** return `APIOrderNotSupportUpdateTouchOrder` and **cannot** be amended — cancel and re-create instead. See `references/conditional.md` for the cancel-and-recreate workflow.

### Workflow

1. **Locate order**: by order ID or via list → user selects.
2. **Get current values**: call `cex_fx_get_fx_price_triggered_order` to show what will change.
3. **Determine position mode**: call `cex_fx_get_fx_accounts(settle)` to get `position_mode` (single/dual). This determines the correct `close` and `auto_size` values to include in the amend request.
4. **Collect new values**: ask user which fields to change.
5. **Determine `close` and `auto_size`**: even when only changing `trigger_price` or `price`, the amend request must include correct `close` and `auto_size` values based on position mode and close scope:

   #### `close` and `auto_size` rules for amend

   | Position mode | Close scope | `close` | `auto_size` |
   |---------------|-------------|---------|-------------|
   | **Single** | Full close (`size = 0`) | `true` | Do **not** set |
   | **Single** | Partial close (`size ≠ 0`) | `false` (or omit) | Do **not** set |
   | **Dual** | Full close (`size = 0`) | `false` (or omit) | **Required**: `close_long` or `close_short` |
   | **Dual** | Partial close (`size ≠ 0`) | `false` (or omit) | Do **not** set |

6. **Confirm**: show old → new comparison and ask *"Reply 'confirm' to update this order."*
7. **Amend**: call `cex_fx_update_fx_price_triggered_order` with changed fields **plus** the correct `close`/`auto_size` for the current mode.
8. **Verify**: call `cex_fx_get_fx_price_triggered_order` to confirm new values.

**Single mode — amend trigger price (full close)**:
```
cex_fx_update_fx_price_triggered_order(
  settle        = "usdt",
  order_id      = "123",
  trigger_price = "73000",
  price         = "0",        # must include execution price
  close         = true        # single mode full close: must be true
                              # auto_size: do NOT set in single mode
)
```

**Dual mode — amend trigger price (full close long)**:
```
cex_fx_update_fx_price_triggered_order(
  settle        = "usdt",
  order_id      = "123",
  trigger_price = "73000",
  price         = "0",        # must include execution price
  auto_size     = "close_long" # dual mode full close: required (close_long / close_short)
                               # close: do NOT set to true in dual mode
)
```

**Dual mode — amend trigger price (partial close)**:
```
cex_fx_update_fx_price_triggered_order(
  settle        = "usdt",
  order_id      = "123",
  trigger_price = "58000",
  price         = "0",        # must include execution price
  size          = -3           # partial close: set size
                               # auto_size: do NOT set for partial close
                               # close: do NOT set (or false)
)
```

### Amendable fields

| Field | Description |
|-------|-------------|
| `trigger_price` | New price level that activates the order |
| `price` | New execution price (`"0"` for market). **Required** in amend requests even if unchanged |
| `size` | New order size (positive = buy to close short, negative = sell to close long; `0` = full close) |
| `price_type` | Trigger price type: `0` = last price, `1` = mark price, `2` = index price |
| `auto_size` | **Dual mode full close only**: `close_long` (close long) or `close_short` (close short). Do **not** set in single mode or for partial close |
| `close` | **Single mode full close only**: must be `true`. In dual mode or partial close: `false` or omit |

**Note**: `trigger_rule` (`>=` / `<=`) **cannot** be changed via amend. To change the rule, cancel and re-create the order.

---

## Scenarios

### Scenario 1: List all TP/SL orders

**Context**: User wants to see all open price-triggered orders for BTC_USDT.

**Prompt Examples**:
- "Show my TP/SL orders for BTC"
- "查看我的 BTC 条件单"

**Expected Behavior**:
1. Call `cex_fx_list_fx_price_triggered_orders(settle="usdt", status="open", contract="BTC_USDT")`.
2. Display table with all open orders (ID, contract, trigger, execute, size, type).
3. Offer to show details, cancel, or amend.

**Response Template**:
```
Open Price-Triggered Orders (BTC_USDT)
─────────────────────────────────────────────────────────────────
ID      Contract   Trigger             Execute    Size      Type
123     BTC_USDT   >= 72000            Market     close all TP (Long)
124     BTC_USDT   <= 58000            Limit 57800 close all SL (Long)
```

---

### Scenario 2: Cancel a stop loss

**Context**: User wants to cancel their BTC stop-loss order. They don't provide an order ID, so the agent needs to list and identify.

**Prompt Examples**:
- "Cancel my BTC stop loss"
- "取消我的 BTC 止损"

**Expected Behavior**:
1. Call `cex_fx_list_fx_price_triggered_orders(settle="usdt", status="open", contract="BTC_USDT")`.
2. Filter/identify SL orders (trigger `<=` for long position or `>=` for short).
3. If ambiguous (multiple SL), show list and ask user to pick.
4. Confirm: "Cancel order #[id] (SL <= 58000)? Reply to confirm."
5. Call `cex_fx_cancel_fx_price_triggered_order(settle, order_id)`.
6. Verify via `cex_fx_get_fx_price_triggered_order` → status `cancelled`.

**Response Template**:
```
✓ Cancelled price-triggered order #[id]
  Contract: BTC_USDT
  Was: Stop Loss <= 58000
```

---

### Scenario 3: Move TP higher

**Context**: User wants to amend an existing take-profit order, raising the trigger from 72000 to 75000.

**Prompt Examples**:
- "Move my BTC take profit from 72000 to 75000"
- "把 BTC 止盈改到 75000"

**Expected Behavior**:
1. Call `cex_fx_list_fx_price_triggered_orders(settle="usdt", status="open", contract="BTC_USDT")` to find the TP order (trigger `>=` for long TP).
2. Get position mode via `cex_fx_get_fx_accounts(settle)` to determine `close`/`auto_size` for amend.
3. Show comparison: current trigger 72000 → new trigger 75000.
4. Confirm: "Update TP trigger from 72000 to 75000? Reply to confirm."
5. Call `cex_fx_update_fx_price_triggered_order` with `trigger_price="75000"`, `price` (current execution price), and mode-appropriate flags:
   - Single mode full close: `close = true`, no `auto_size`.
   - Dual mode full close: `auto_size = "close_long"`, no `close = true`.
6. Verify via `cex_fx_get_fx_price_triggered_order` → confirm new trigger price.

**Response Template**:
```
✓ Amended price-triggered order #[id]
  Contract: BTC_USDT
  Trigger: >= 72000 → >= 75000
```

---

### Scenario 4: Cancel all triggered orders

**Context**: User wants to cancel all open price-triggered orders across all contracts.

**Prompt Examples**:
- "Cancel all my conditional orders"
- "取消所有条件单"

**Expected Behavior**:
1. Confirm: "Cancel all open price-triggered orders for all contracts? Reply to confirm."
2. Call `cex_fx_cancel_fx_price_triggered_order_list(settle="usdt")` (no contract filter).
3. Verify via `cex_fx_list_fx_price_triggered_orders(settle="usdt", status="open")` → confirm list is empty.

**Response Template**:
```
✓ Cancelled all open price-triggered orders
  Affected: [N] orders
```

---

### Scenario 5: Change execution to limit

**Context**: User wants to change the execution price of an existing SL order from market to limit at 57500. Note: `order_tif` is set at creation and cannot be amended.

**Prompt Examples**:
- "Change my BTC SL execution to limit at 57500"
- "把 BTC 止损执行价改成限价 57500"

**Expected Behavior**:
1. Call `cex_fx_list_fx_price_triggered_orders` to find the SL order.
2. Get position mode via `cex_fx_get_fx_accounts(settle)` to determine `close`/`auto_size` for amend.
3. Check original `order_tif`: if IOC (market), warn user: "The original order was IOC; amending price to a limit value applies, but tif cannot be changed. To switch to GTC, cancel and re-create."
4. Confirm: "Update SL execution price to 57500? Reply to confirm."
5. Call `cex_fx_update_fx_price_triggered_order` with `price="57500"`, `trigger_price` (current trigger), and mode-appropriate flags:
   - Single mode full close: `close = true`, no `auto_size`.
   - Dual mode full close: `auto_size = "close_short"`, no `close = true`.
6. Verify via `cex_fx_get_fx_price_triggered_order`.

**Response Template**:
```
✓ Amended price-triggered order #[id]
  Contract: BTC_USDT
  Execute: Market → Limit 57500
```

---

## Report Template

**List orders**:
```
Open Price-Triggered Orders ([Contract / All])
─────────────────────────────────────────────────────────────────
ID      Contract   Trigger             Execute      Size      Type
[id]    [contract] [rule] [price]      [mkt/limit]  [size]    [TP/SL/Conditional]
```

**Cancel single**:
```
✓ Cancelled price-triggered order #[id]
  Contract: [contract]
  Was: [TP/SL/Conditional] [rule] [trigger_price]
```

**Cancel all**:
```
✓ Cancelled all open price-triggered orders
  Scope: [contract / all contracts]
  Affected: [N] orders
```

**Amend**:
```
✓ Amended price-triggered order #[id]
  Contract: [contract]
  [changed_field]: [old_value] → [new_value]
```

---

## Error handling

| Situation | Action |
|-----------|--------|
| Order not found | Order may have triggered or been cancelled. Check `status="finished"` history. |
| Amending already-triggered order | Order status is `finished`; cannot amend. Show final status. |
| Cannot change trigger_rule | Cancel and re-create with new rule. |
| `APIOrderNotSupportUpdateTouchOrder` | API-created conditional open orders cannot be amended. Cancel and re-create instead. TP/SL orders (plan-close-*) are not affected and can be amended normally. |
| No open orders found | Confirm to user: "No open price-triggered orders found." |
| `AUTO_INVALID_PARAM_CLOSE` | In dual mode, `close` must be `false` when using `auto_size`. Remove `close = true` and use `auto_size` instead. |
| `AUTO_INVALID_PARAM_ORDER_TYPE` | Dual mode full close requires `auto_size` (`close_long` / `close_short`). Add the correct `auto_size` value. |
| `AUTO_INVALID_PARAM_PRICE` / `Invalid param:price` | Amend requests require `price` (execution price) even if unchanged. Include `price = "0"` for market. |
