# Gate Futures Take Profit / Stop Loss — Scenarios & Reference

This reference covers creating and managing TP/SL orders on existing futures positions using `cex_fx_create_fx_price_triggered_order`.

---

## Concept

A TP/SL order is a **price-triggered order** attached to an existing position. It fires a close (or reduce) order when the market price crosses the trigger level.

| Order type | Position side | Trigger rule | When it fires |
|------------|--------------|--------------|---------------|
| Take Profit | Long | `>=` | Price rises to TP level → close long |
| Stop Loss | Long | `<=` | Price falls to SL level → close long |
| Take Profit | Short | `<=` | Price falls to TP level → close short |
| Stop Loss | Short | `>=` | Price rises to SL level → close short |

---

## Workflow

### 1. Identify position

Call `cex_fx_get_fx_accounts(settle)` to determine account mode, then call position query:

- **Single mode** (`position_mode === "single"`): call `cex_fx_get_fx_position(settle, contract)`
- **Dual mode** (`position_mode === "dual"` or `in_dual_mode === true`): call `cex_fx_list_fx_positions(settle, holding=true)` or `cex_fx_get_fx_dual_position(settle, contract)`

Key data to extract:
- `position_mode` — from account query (`single` or `dual`)
- `size` — current position size (positive = long, negative = short)
- Side: positive `size` → long; negative `size` → short

If no position exists, tell the user and abort.

### 2. Determine trigger rule

Call `cex_fx_get_fx_order_book(settle, contract, limit=1)` to get current best bid/ask for validation.

| Position side | TP trigger | SL trigger |
|--------------|-----------|-----------|
| **Long** (size > 0) | `>=` (price rises to TP) | `<=` (price falls to SL) |
| **Short** (size < 0) | `<=` (price falls to TP) | `>=` (price rises to SL) |

**Validation**: warn if trigger price is already past current market price (i.e., order would fire immediately):
- Long TP with trigger ≤ current price → warn: "BTC is already at [price], TP would trigger immediately."
- Long SL with trigger ≥ current price → warn: "BTC is already at [price], SL would trigger immediately."
- Short TP with trigger ≥ current price → same warning pattern.
- Short SL with trigger ≤ current price → same warning pattern.

Key data to extract:
- `trigger_rule` — `>=` or `<=` based on position side and order type
- `best_bid` / `best_ask` — for immediate-trigger validation

### 3. Determine size, close, auto_size, and order_type

Call `cex_fx_get_fx_contract(settle, contract)` to get size constraints. The `close`, `auto_size`, and `order_type` fields depend on **position mode** (from step 1), **position side**, and **close scope** (full vs partial).

#### `order_type` field rules

For TP/SL orders, `order_type` must be set to indicate the close direction and scope:

| Position side | Close scope | `order_type` |
|---------------|-------------|-------------|
| **Long** | Full close | `close-long-position` |
| **Long** | Partial close | `plan-close-long-position` |
| **Short** | Full close | `close-short-position` |
| **Short** | Partial close | `plan-close-short-position` |

> **Note**: `close-long-order` and `close-short-order` are read-only types returned by the API; they **cannot** be passed in create requests.

#### `close` field rules

| Position mode | Close scope | `close` |
|---------------|-------------|---------|
| **Single** | Full close | `true` (required to execute close) |
| **Single** | Partial close | `false` (or omit) |
| **Dual** | Full close | `false` (or omit) |
| **Dual** | Partial close | `false` (or omit) |

#### `auto_size` field rules

| Position mode | Close scope | `auto_size` |
|---------------|-------------|-------------|
| **Single** | Any | Do **not** set |
| **Dual** | Full close (`size = 0`) | **Required**: `close_long` (close long position) or `close_short` (close short position) |
| **Dual** | Partial close (`size ≠ 0`) | Do **not** set |

#### Combined parameter table

| Position mode | Position side | User intent | `order_type` | `order_size` | `close` | `auto_size` | `order_reduce_only` |
|---------------|--------------|-------------|-------------|-------------|---------|-------------|---------------------|
| **Single** | Long | Close all | `close-long-position` | `0` | `true` | — | `true` |
| **Single** | Long | Partial close | `plan-close-long-position` | negative size | `false` | — | `true` |
| **Single** | Short | Close all | `close-short-position` | `0` | `true` | — | `true` |
| **Single** | Short | Partial close | `plan-close-short-position` | positive size | `false` | — | `true` |
| **Dual** | Long | Close all | `close-long-position` | `0` | `false` | `close_long` | `true` |
| **Dual** | Long | Partial close | `plan-close-long-position` | negative size | `false` | — | `true` |
| **Dual** | Short | Close all | `close-short-position` | `0` | `false` | `close_short` | `true` |
| **Dual** | Short | Partial close | `plan-close-short-position` | positive size | `false` | — | `true` |

**Size sign for partial close**:
- Closing a long position → `order_size` = **negative** (sell to close long)
- Closing a short position → `order_size` = **positive** (buy to close short)

Key data to extract:
- `position_mode` — from account query (`single` or `dual`), determines `close` and `auto_size` usage
- `order_type` — based on position side and close scope (see `order_type` table above)
- `order_close` — `true` only for single-mode full close; `false` otherwise
- `auto_size` — only for dual-mode full close (`close_long` or `close_short`)
- `order_reduce_only` — always `true`
- `order_size` — signed size (or 0 for full close)
- `order_size_min` — from contract, for validation

### 4. Execution price (when triggered)

| User preference | `order_price` | `order_tif` |
|-----------------|--------------|-------------|
| Market (default if not specified) | `"0"` | `"ioc"` |
| Limit at specific price | `"<price>"` | `"gtc"` |

Key data to extract:
- `order_price` — `"0"` for market, or user-specified limit price as string
- `order_tif` — `"ioc"` for market, `"gtc"` for limit

### 5. Pre-order confirmation

Show this summary and ask the user to confirm:

```
Take Profit / Stop Loss Order Summary
─────────────────────────────────────
Contract:      BTC_USDT
Position:      Long × 5 contracts
Order type:    [Take Profit / Stop Loss]
Trigger:       price >= 72000  (TP)  /  price <= 58000  (SL)
Execute:       Market (IOC)  /  Limit 71500 (GTC)
Close:         All  /  2 contracts (reduce-only)
Expiration:    [never / X hours]

Reply 'confirm' to place this order.
```

**Only after user confirms**, call `cex_fx_create_fx_price_triggered_order`.

### 6. Place order

Call `cex_fx_create_fx_price_triggered_order`. The `close`, `auto_size`, and `order_type` fields differ by position mode and close scope:

**Single mode — full close (close long TP)**:
```
cex_fx_create_fx_price_triggered_order(
  settle          = "usdt",
  contract        = "BTC_USDT",
  order_type      = "close-long-position",  # full close long
  trigger_price   = "72000",
  trigger_rule    = ">=",
  order_price     = "0",          # market
  order_tif       = "ioc",
  order_size      = 0,
  order_close     = true,         # single mode: must be true for full close
                                  # auto_size: do NOT set in single mode
  order_reduce_only = true,
  trigger_expiration = <seconds>  # optional; omit for no expiry
)
```

**Dual mode — full close (close long TP)**:
```
cex_fx_create_fx_price_triggered_order(
  settle          = "usdt",
  contract        = "BTC_USDT",
  order_type      = "close-long-position",  # full close long
  trigger_price   = "72000",
  trigger_rule    = ">=",
  order_price     = "0",          # market
  order_tif       = "ioc",
  order_size      = 0,
  order_close     = false,        # dual mode: must be false (or omit)
  auto_size       = "close_long", # dual mode full close: required (close_long / close_short)
  order_reduce_only = true,
  trigger_expiration = <seconds>  # optional; omit for no expiry
)
```

**Dual mode — partial close (SL 3 contracts of a long)**:
```
cex_fx_create_fx_price_triggered_order(
  settle          = "usdt",
  contract        = "BTC_USDT",
  order_type      = "plan-close-long-position",  # partial close long
  trigger_price   = "58000",
  trigger_rule    = "<=",
  order_price     = "0",          # market
  order_tif       = "ioc",
  order_size      = -3,           # negative = sell to close long
  order_close     = false,        # partial: always false
                                  # auto_size: do NOT set for partial close
  order_reduce_only = true,
)
```

### 7. Verify

Call `cex_fx_get_fx_price_triggered_order(settle, order_id)` to confirm status is `open`.

Key data to extract:
- `id` — order ID (pass as string)
- `status` — should be `open`

---

## Scenarios

### Scenario 1: Set TP for a long position (market close)

**Context**: User holds a BTC_USDT long position (5 contracts), current price ~68000. Wants to set a take-profit trigger at 72000.

**Prompt Examples**:
- "Set take profit at 72000 for my BTC long"
- "BTC 止盈 72000"

**Expected Behavior**:
1. Query position via `cex_fx_get_fx_position` / `cex_fx_get_fx_dual_position` → long 5 contracts.
2. Validate trigger: current price ~68000, TP 72000 > current → valid.
3. Determine trigger rule: long TP → `>=`.
4. No size specified → full close, `order_type = "close-long-position"`, `order_reduce_only = true`.
   - Single mode: `order_close = true`, no `auto_size`.
   - Dual mode: `order_close = false`, `auto_size = "close_long"`.
5. No execution price specified → market (`order_price = "0"`, `order_tif = "ioc"`).
6. Show summary, ask user to confirm, then call `cex_fx_create_fx_price_triggered_order`.

**Response Template**:
```
✓ Take Profit BTC_USDT
  Trigger: >= 72000
  Execute: Market (IOC) × close all (reduce-only)
  Order ID: [id]
```

---

### Scenario 2: Set SL for a long position (limit close)

**Context**: User holds a BTC_USDT long position (5 contracts), current price ~68000. Wants a stop-loss at 58000 with limit execution at 57800.

**Prompt Examples**:
- "SL at 58000 for my BTC long, execute at 57800"
- "BTC 止损 58000，限价 57800 平仓"

**Expected Behavior**:
1. Query position via `cex_fx_get_fx_position` / `cex_fx_get_fx_dual_position` → long 5 contracts.
2. Validate trigger: current price ~68000, SL 58000 < current → valid.
3. Determine trigger rule: long SL → `<=`.
4. No size specified → full close, `order_type = "close-long-position"`, `order_reduce_only = true`.
   - Single mode: `order_close = true`, no `auto_size`.
   - Dual mode: `order_close = false`, `auto_size = "close_long"`.
5. User specified execution price 57800 → limit (`order_price = "57800"`, `order_tif = "gtc"`).
6. Show summary, confirm, then call `cex_fx_create_fx_price_triggered_order`.

**Response Template**:
```
✓ Stop Loss BTC_USDT
  Trigger: <= 58000
  Execute: Limit 57800 (GTC) × close all (reduce-only)
  Order ID: [id]
```

---

### Scenario 3: Partial SL for a long position

**Context**: User holds a BTC_USDT long position (5 contracts), current price ~68000. Wants to stop-loss only 3 contracts at 58000.

**Prompt Examples**:
- "Stop loss 3 contracts at 58000"
- "BTC 止损 58000，平 3 张"

**Expected Behavior**:
1. Query position → long 5 contracts.
2. Determine trigger rule: long SL → `<=`.
3. Partial close: 3 contracts; closing long → `order_type = "plan-close-long-position"`, `order_size = -3` (negative = sell to close long), `order_reduce_only = true`.
   - Both single and dual mode: `order_close = false`, no `auto_size` (partial close never uses `auto_size`).
4. No execution price → market (`order_price = "0"`, `order_tif = "ioc"`).
5. Show summary, confirm, then call `cex_fx_create_fx_price_triggered_order`.

**Response Template**:
```
✓ Stop Loss BTC_USDT
  Trigger: <= 58000
  Execute: Market (IOC) × 3 contracts (reduce-only)
  Order ID: [id]
```

---

### Scenario 4: TP + SL together

**Context**: User holds a BTC_USDT long position, current price ~68000. Wants to set both take-profit at 72000 and stop-loss at 58000 simultaneously.

**Prompt Examples**:
- "Set BTC TP 72000 and SL 58000"
- "BTC 止盈 72000 止损 58000"

**Expected Behavior**:
1. Query position → confirm long position exists.
2. Create **two separate** price-triggered orders sequentially.
3. Order 1: TP (`>=` 72000, close all, market), `order_type = "close-long-position"`.
   - Single mode: `close = true`, no `auto_size`.
   - Dual mode: `close = false`, `auto_size = "close_long"`.
4. Order 2: SL (`<=` 58000, close all, market), `order_type = "close-long-position"`.
   - Same `close`/`auto_size` logic as Order 1.
5. Show combined summary for both, ask for single confirmation before placing both via `cex_fx_create_fx_price_triggered_order`.

**Response Template**:
```
✓ Take Profit BTC_USDT
  Trigger: >= 72000
  Execute: Market (IOC) × close all (reduce-only)
  Order ID: [id_1]

✓ Stop Loss BTC_USDT
  Trigger: <= 58000
  Execute: Market (IOC) × close all (reduce-only)
  Order ID: [id_2]
```

---

### Scenario 5: Set TP for a short position

**Context**: User holds an ETH_USDT short position (size < 0), current price ~65000. Wants to take profit at 62000.

**Prompt Examples**:
- "Take profit at 62000 for my ETH short"
- "ETH 空头止盈 62000"

**Expected Behavior**:
1. Query position → short (size < 0).
2. Validate trigger: current price ~65000, TP 62000 < current → valid (short profits when price falls).
3. Determine trigger rule: short TP → `<=`.
4. No size specified → full close, `order_type = "close-short-position"`, `order_reduce_only = true`.
   - Single mode: `order_close = true`, no `auto_size`.
   - Dual mode: `order_close = false`, `auto_size = "close_short"`.
5. No execution price → market (`order_price = "0"`, `order_tif = "ioc"`).
6. Show summary, confirm, then call `cex_fx_create_fx_price_triggered_order`.

**Response Template**:
```
✓ Take Profit ETH_USDT
  Trigger: <= 62000
  Execute: Market (IOC) × close all (reduce-only)
  Order ID: [id]
```

---

### Scenario 6: Set SL for a short position

**Context**: User holds an ETH_USDT short position (size < 0), current price ~65000. Wants to stop-loss at 68000.

**Prompt Examples**:
- "Stop loss at 68000 for my ETH short"
- "ETH 空头止损 68000"

**Expected Behavior**:
1. Query position → short (size < 0), current price ~65000.
2. Validate trigger: SL 68000 > current → valid (short loses when price rises).
3. Determine trigger rule: short SL → `>=`.
4. No size specified → full close, `order_type = "close-short-position"`, `order_reduce_only = true`.
   - Single mode: `order_close = true`, no `auto_size`.
   - Dual mode: `order_close = false`, `auto_size = "close_short"`.
5. No execution price → market (`order_price = "0"`, `order_tif = "ioc"`).
6. Show summary, confirm, then call `cex_fx_create_fx_price_triggered_order`.

**Response Template**:
```
✓ Stop Loss ETH_USDT
  Trigger: >= 68000
  Execute: Market (IOC) × close all (reduce-only)
  Order ID: [id]
```

---

### Scenario 7: Partial TP for a short position

**Context**: User holds an ETH_USDT short position (5 contracts, size = -5), current price ~65000. Wants to take profit on 2 contracts at 62000.

**Prompt Examples**:
- "Take profit 2 contracts at 62000 for my ETH short"
- "ETH 空头止盈 62000，平 2 张"

**Expected Behavior**:
1. Query position → short 5 contracts (size = -5).
2. Validate trigger: TP 62000 < current ~65000 → valid (short profits when price falls).
3. Determine trigger rule: short TP → `<=`.
4. Partial close: 2 contracts; closing short → `order_type = "plan-close-short-position"`, `order_size = 2` (positive = buy to close short), `order_reduce_only = true`.
   - Both single and dual mode: `order_close = false`, no `auto_size` (partial close never uses `auto_size`).
5. No execution price → market (`order_price = "0"`, `order_tif = "ioc"`).
6. Show summary, confirm, then call `cex_fx_create_fx_price_triggered_order`.

**Response Template**:
```
✓ Take Profit ETH_USDT
  Trigger: <= 62000
  Execute: Market (IOC) × 2 contracts (reduce-only)
  Order ID: [id]
```

---

## Report Template

```
✓ [Take Profit / Stop Loss] [Contract]
  Trigger: [rule] [trigger_price]
  Execute: [Market (IOC) / Limit price (GTC)] × [close all / N contracts] (reduce-only)
  Order ID: [id]
```

For TP + SL together (Scenario 4), output two reports sequentially:

```
✓ Take Profit [Contract]
  Trigger: [rule] [trigger_price]
  Execute: Market (IOC) × close all (reduce-only)
  Order ID: [id_1]

✓ Stop Loss [Contract]
  Trigger: [rule] [trigger_price]
  Execute: Market (IOC) × close all (reduce-only)
  Order ID: [id_2]
```

---

## Common mistakes

| Mistake | Correct behavior |
|---------|-----------------|
| Using `>=` for long SL | Long SL must use `<=` (fires when price **drops**) |
| Using `<=` for short SL | Short SL must use `>=` (fires when price **rises**) |
| Positive `order_size` for long close | Use **negative** size to close a long (sell direction) |
| Negative `order_size` for short close | Use **positive** size to close a short (buy direction) |
| Setting `order_close = true` without `order_reduce_only = true` | Always set `order_reduce_only = true`; additionally set `order_close = true` only in single mode for full close |
| Trigger price already past current market | Warn user before placing |
| Setting `auto_size` in single mode | Single mode does **not** use `auto_size`; only set `close = true` for full close |
| Setting `auto_size` for partial close in dual mode | `auto_size` is only for dual-mode **full close** (`size = 0`); partial close (`size ≠ 0`) must **not** set `auto_size` |
| Missing `auto_size` in dual-mode full close | Dual mode full close **requires** `auto_size` (`close_long` or `close_short`); omitting it causes `AUTO_INVALID_PARAM_ORDER_TYPE` |
| Setting `close = true` with `auto_size` in dual mode | When using `auto_size`, `close` must be `false`; setting both causes `AUTO_INVALID_PARAM_CLOSE` |
| Setting `close = true` in dual mode | In dual mode, `close` should always be `false` (or omitted); use `auto_size` instead for full close |
| Missing `order_type` for TP/SL | TP/SL orders **require** `order_type`; use `close-long-position` / `close-short-position` for full close, `plan-close-long-position` / `plan-close-short-position` for partial close |
| Using `close-long-order` / `close-short-order` as `order_type` | These are **read-only** types returned by the API; they **cannot** be passed in create requests |
| Wrong `order_type` direction (e.g. `close-short-position` for a long) | `order_type` must match position side: `*-long-*` for closing longs, `*-short-*` for closing shorts |
