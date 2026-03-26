# Gate Futures Conditional Open Order — Scenarios & Reference

This reference covers creating a conditional open order (触价开仓) that places a new futures position when the market price reaches a specified level.

---

## Concept

A **conditional open order** is a price-triggered order that **opens a new position** (not reduce/close) when the trigger condition is met. Use this when the user wants to:

- Buy the dip: "Open long if BTC drops to 60000"
- Breakout buy: "Open long if BTC breaks above 68000"
- Breakout short: "Open short if ETH breaks below 3000"

---

## Trigger rule logic

| User intent | Example | Trigger rule |
|-------------|---------|-------------|
| Open long when price **drops** to level (buy dip) | "Long BTC if it falls to 60000" | `<=` |
| Open long when price **rises** to level (breakout long) | "Long BTC when it breaks 68000" | `>=` |
| Open short when price **rises** to level (breakout short) | "Short ETH if it breaks above 3000" | `>=` |
| Open short when price **falls** to level | "Short ETH when it drops to 2800" | `<=` |

**Rule**: the trigger rule describes the **price condition that must be true** for the order to fire.

---

## Workflow

### 1. Extract parameters

Parse user intent to extract:

Key data to extract:
- `contract` — e.g. BTC_USDT
- `trigger_price` — the price level that activates the order
- `trigger_rule` — `>=` or `<=` (see trigger rule logic table above)
- `side` — long (positive size) or short (negative size)
- `size` — in contracts, USDT cost, USDT value, or base amount
- `order_price` (optional) — execution price; omit or `"0"` for market
- `order_tif` (optional) — `"gtc"` for limit, `"ioc"` for market
- `trigger_expiration` (optional) — expiry in seconds (omit for no expiry)

### 2. Size conversion

When user does not specify size in **contracts**, convert using the same rules as the main futures open-position skill.

Call `cex_fx_get_fx_contract(settle, contract)` and `cex_fx_get_fx_order_book(settle, contract, limit=1)` for conversion data.

Key data to extract:
- `quanto_multiplier` — from contract, for unit conversion
- `order_size_min` — from contract, for validation
- `best_ask` / `best_bid` — from order book, for price reference
- For current leverage (if relevant): position query (see main skill)

**USDT Cost → contracts (margin-based)**:

| Direction | Formula | `order_price` used |
|-----------|---------|-------------------|
| Open long | `contracts = cost / (0.0015 + 1/leverage) / quanto_multiplier / order_price` | Limit: specified; Market: best ask |
| Open short | `contracts = cost / (0.0015 + 1.00075/leverage) / quanto_multiplier / max(order_price, best_bid)` | Limit: specified; Market: best bid |

For conditional orders, use `trigger_price` as the reference `order_price` when computing cost-based contracts (since that is the expected execution price). If the user also specified an execution limit price, use that instead.

**USDT Value → contracts (notional-based)**:

| Direction | Formula |
|-----------|---------|
| Long | `contracts = usdt_value / price / quanto_multiplier` (price = trigger_price or order_price) |
| Short | `contracts = usdt_value / max(best_bid, order_price) / quanto_multiplier` |

**Base amount → contracts**: `contracts = base_amount / quanto_multiplier`

**Precision**: floor to integer; must satisfy `order_size_min`.

### 3. Order size sign

Key data to extract:
- `order_size` — **positive** for open long, **negative** for open short

### 4. Execution price (when triggered)

| User preference | `order_price` | `order_tif` |
|-----------------|--------------|-------------|
| Market (default) | `"0"` | `"ioc"` |
| Limit at specific price | `"<price>"` | `"gtc"` |

If user says "at market" or doesn't specify execution price, use market (`"0"`, `"ioc"`).
If user says "limit at X" or "execute at X", use limit.

Key data to extract:
- `order_price` — `"0"` for market, or user-specified limit price as string
- `order_tif` — `"ioc"` for market, `"gtc"` for limit

### 5. Pre-order confirmation

Show summary and ask for confirmation:

```
Conditional Open Order Summary
────────────────────────────────
Contract:      BTC_USDT
Side:          Long
Trigger:       price <= 60000  (fires when BTC drops to 60000)
Execute:       Market (IOC)  /  Limit 59800 (GTC)
Size:          3 contracts  (~180 USDT margin at 10x)
Expiration:    [never / 24 hours]

Reply 'confirm' to place this order.
```

**Only after user confirms**, call `cex_fx_create_fx_price_triggered_order`.

### 6. Place order

Call `cex_fx_create_fx_price_triggered_order` with:

```
cex_fx_create_fx_price_triggered_order(
  settle           = "usdt",
  contract         = "BTC_USDT",
  trigger_price    = "60000",
  trigger_rule     = "<=",
  order_price      = "0",       # market
  order_tif        = "ioc",
  order_size       = 3,         # positive = long
  order_reduce_only = false,    # this is an open order
  order_close      = false
)
```

### 7. Verify

Call `cex_fx_get_fx_price_triggered_order(settle, order_id)` to confirm the order status is `open`.

Key data to extract:
- `id` — order ID (pass as string)
- `status` — should be `open`

---

## Scenarios

### Scenario 1: Buy the dip (long when price drops)

**Context**: User wants to open a long BTC_USDT position if price drops to 60000. Current price ~65000. Size specified in contracts.

**Prompt Examples**:
- "Open long 2 BTC_USDT contracts if BTC drops to 60000"
- "BTC 跌到 60000 做多 2 张"

**Expected Behavior**:
1. Determine side: long. Trigger: drops to 60000 → `trigger_rule = "<="`.
2. Size: 2 contracts → `order_size = 2` (positive = long).
3. No execution price → market (`order_price = "0"`, `order_tif = "ioc"`).
4. Show summary, confirm, then call `cex_fx_create_fx_price_triggered_order`.

**Response Template**:
```
✓ Conditional Open Long BTC_USDT
  Trigger: <= 60000
  Execute: Market (IOC) × 2 contracts
  Order ID: [id]
```

---

### Scenario 2: Breakout long

**Context**: User wants to open a long BTC_USDT position when price breaks above 68000. Size specified as USDT value (100U notional).

**Prompt Examples**:
- "Long 100U worth of BTC_USDT when it breaks above 68000"
- "BTC 突破 68000 做多 100U"

**Expected Behavior**:
1. Determine side: long. Trigger: breaks above 68000 → `trigger_rule = ">="`.
2. Call `cex_fx_get_fx_contract` for `quanto_multiplier`. Size: 100U value → `contracts = 100 / 68000 / quanto_multiplier` (floor, check `order_size_min`).
3. No execution price → market (`order_price = "0"`, `order_tif = "ioc"`).
4. Show summary, confirm, then call `cex_fx_create_fx_price_triggered_order`.

**Response Template**:
```
✓ Conditional Open Long BTC_USDT
  Trigger: >= 68000
  Execute: Market (IOC) × [N] contracts (~100 USDT)
  Order ID: [id]
```

---

### Scenario 3: Breakout short

**Context**: User wants to open a short ETH_USDT position when price breaks above 3200. Size specified as USDT cost (50U margin) with 10x leverage.

**Prompt Examples**:
- "Open short ETH_USDT if it breaks above 3200, 50U margin, 10x leverage"
- "ETH 突破 3200 做空，50U 保证金，10 倍杠杆"

**Expected Behavior**:
1. Determine side: short. Trigger: breaks above 3200 → `trigger_rule = ">="`.
2. Call `cex_fx_get_fx_contract` for `quanto_multiplier` and `cex_fx_get_fx_order_book` for best bid. Size: 50U cost, 10x leverage → `contracts = 50 / (0.0015 + 1.00075/10) / quanto_multiplier / max(3200, best_bid)` (floor, check `order_size_min`). `order_size` = negative (short).
3. No execution price → market (`order_price = "0"`, `order_tif = "ioc"`).
4. Show summary, confirm, then call `cex_fx_create_fx_price_triggered_order`.

**Response Template**:
```
✓ Conditional Open Short ETH_USDT
  Trigger: >= 3200
  Execute: Market (IOC) × [N] contracts (~50 USDT margin)
  Order ID: [id]
```

---

### Scenario 4: Conditional limit order

**Context**: User wants to open a long BTC_USDT position when price drops to 61000, with limit execution at 60800. Size specified in contracts.

**Prompt Examples**:
- "When BTC drops to 61000, open long 1 contract with limit at 60800"
- "BTC 跌到 61000 做多 1 张，限价 60800"

**Expected Behavior**:
1. Determine side: long. Trigger: drops to 61000 → `trigger_rule = "<="`.
2. User specified execution price 60800 → limit (`order_price = "60800"`, `order_tif = "gtc"`).
3. Size: 1 contract → `order_size = 1` (positive = long).
4. Show summary, confirm, then call `cex_fx_create_fx_price_triggered_order`.

**Response Template**:
```
✓ Conditional Open Long BTC_USDT
  Trigger: <= 61000
  Execute: Limit 60800 (GTC) × 1 contract
  Order ID: [id]
```

---

### Scenario 5: With expiration

**Context**: User wants a conditional long order with a 24-hour expiration. If not triggered within 24 hours, the order auto-cancels.

**Prompt Examples**:
- "Long 2 BTC when it drops to 60000, expires in 24 hours"
- "BTC 跌到 60000 做多 2 张，24 小时后过期"

**Expected Behavior**:
1. Determine side: long. Trigger: drops to 60000 → `trigger_rule = "<="`.
2. Size: 2 contracts → `order_size = 2`.
3. No execution price → market.
4. User specified 24-hour expiry → `trigger_expiration = 86400` (24 × 3600 seconds).
5. Show summary (including expiration), confirm, then call `cex_fx_create_fx_price_triggered_order`.

**Response Template**:
```
✓ Conditional Open Long BTC_USDT
  Trigger: <= 60000
  Execute: Market (IOC) × 2 contracts
  Expiration: 24 hours
  Order ID: [id]
```

---

## Report Template

```
✓ Conditional Open [Long / Short] [Contract]
  Trigger: [rule] [trigger_price]
  Execute: [Market (IOC) / Limit price (GTC)] × [N] contracts
  Expiration: [never / N hours]
  Order ID: [id]
```

---

## Common mistakes

| Mistake | Correct behavior |
|---------|-----------------|
| Using `>=` for "buy when price drops" | Drops = `<=`. `>=` is for breakout above a level. |
| Positive size for open short | Use **negative** size for short. |
| Setting `order_reduce_only = true` on open orders | Only use `reduce_only` for close/TP/SL; leave `false` for open. |
| Using trigger_price as order_price without user specifying | Treat trigger and execution price separately; default execution = market. |
| Trying to amend a conditional open order via API | API-created conditional open orders **cannot** be amended (`APIOrderNotSupportUpdateTouchOrder`). Must cancel and re-create. See below. |

---

## Amending conditional open orders (cancel & re-create)

Gate does **not** support amending API-created conditional open orders via `cex_fx_update_fx_price_triggered_order`. The API returns `APIOrderNotSupportUpdateTouchOrder`. This limitation only applies to conditional open orders; TP/SL orders can be amended normally.

**Workaround**: cancel the existing order, then create a new one with the updated parameters.

### Workflow

1. **Cancel**: call `cex_fx_cancel_fx_price_triggered_order(settle, order_id)` to cancel the existing order.
2. **Verify cancel**: confirm status is `cancelled`.
3. **Re-create**: call `cex_fx_create_fx_price_triggered_order` with the updated parameters.
4. **Verify new order**: confirm new order status is `open`.

When user requests to amend a conditional open order (e.g. "change trigger price to X"), automatically perform the cancel-and-recreate flow without requiring separate confirmation for each step. Show one combined confirmation: *"Conditional open orders cannot be amended directly. I will cancel the old order and create a new one. Confirm?"*
