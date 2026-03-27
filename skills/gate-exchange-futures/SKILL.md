---
name: gate-exchange-futures
version: "2026.3.23-1"
updated: "2026-03-23"
description: "Gate Exchange USDT perpetual futures: open/close position, cancel/amend order, take profit, stop loss, conditional open. Use this skill whenever the user wants to trade USDT perpetual futures on Gate. Trigger phrases include open, close, cancel, amend, take profit, stop loss, TP/SL, conditional order, price trigger, when price reaches."
---

# Gate Futures Trading Suite

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.


---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- cex_fx_get_fx_accounts
- cex_fx_get_fx_contract
- cex_fx_get_fx_dual_position
- cex_fx_get_fx_order
- cex_fx_get_fx_order_book
- cex_fx_get_fx_position
- cex_fx_get_fx_price_triggered_order
- cex_fx_get_fx_tickers
- cex_fx_list_fx_orders
- cex_fx_list_fx_positions
- cex_fx_list_fx_price_triggered_orders

**Execution Operations (Write)**

- cex_fx_amend_fx_order
- cex_fx_cancel_all_fx_orders
- cex_fx_cancel_fx_order
- cex_fx_cancel_fx_price_triggered_order
- cex_fx_cancel_fx_price_triggered_order_list
- cex_fx_create_fx_order
- cex_fx_create_fx_price_triggered_order
- cex_fx_update_fx_dual_position_cross_mode
- cex_fx_update_fx_dual_position_leverage
- cex_fx_update_fx_position_cross_mode
- cex_fx_update_fx_position_leverage
- cex_fx_update_fx_price_triggered_order

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)
- Permissions: Fx:Write
- Get API Key: https://www.gate.io/myaccount/profile/api-key/manage

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Module overview

| Module | Description | Trigger keywords |
|--------|-------------|------------------|
| **Open** | Limit/market open long or short, cross/isolated mode, top gainer/loser order | `long`, `short`, `buy`, `sell`, `open`, `top gainer`, `top loser` |
| **Close** | Full close, partial close, reverse position | `close`, `close all`, `reverse` |
| **Cancel** | Cancel one or many orders | `cancel`, `revoke` |
| **Amend** | Change order price or size | `amend`, `modify` |
| **TP/SL** | Attach take-profit or stop-loss to an existing position; fires a close/reduce order when price is reached | `take profit`, `stop loss`, `TP`, `SL`, `止盈`, `止损` |
| **Conditional Open** | Place a pending open order that triggers when price hits a level | `conditional order`, `when price reaches`, `breakout buy`, `dip buy`, `条件单`, `触价开仓` |
| **Manage Triggers** | List, cancel, or amend open price-triggered orders | `list triggers`, `cancel TP`, `cancel SL`, `amend trigger`, `查询条件单`, `取消止盈止损` |

## Routing rules

| Intent | Example phrases | Route to |
|--------|-----------------|----------|
| **Open position** | "BTC long 1 contract", "market short ETH", "10x leverage long", "top gainer long 10U" | Read `references/open-position.md` |
| **Close position** | "close all BTC", "close half", "reverse to short", "close everything" | Read `references/close-position.md` |
| **Cancel orders** | "cancel that buy order", "cancel all orders", "list my orders" | Read `references/cancel-order.md` |
| **Amend order** | "change price to 60000", "change order size" | Read `references/amend-order.md` |
| **Set TP/SL** | "Set BTC TP at 70000", "SL at 58000 for my long", "止损60000" | Read `references/tp-sl.md` |
| **Conditional open** | "Buy BTC when it drops to 60000", "Open short if price breaks above 68000", "条件单做多" | Read `references/conditional.md` |
| **Manage triggered orders** | "List my TP/SL orders", "Cancel that stop loss", "Amend trigger price", "查询条件单" | Read `references/manage.md` |
| **Unclear** | "help with futures", "show my position" | **Clarify**: query position/orders, then guide user |

## MCP tools

| # | Tool | Purpose |
|---|------|---------|
| 1 | `cex_fx_get_fx_tickers` | Get all futures tickers (for top gainer/loser sorting) |
| 2 | `cex_fx_get_fx_contract` | Get single contract info (precision, multiplier, etc.) |
| 3 | `cex_fx_get_fx_order_book` | Get contract order book (best bid/ask) |
| 4 | `cex_fx_get_fx_accounts` | Get futures account (position mode: single/dual) |
| 5 | `cex_fx_list_fx_positions` | List positions (dual mode) |
| 6 | `cex_fx_get_fx_dual_position` | Get dual-mode position for a contract |
| 7 | `cex_fx_get_fx_position` | Get single-mode position for a contract |
| 8 | `cex_fx_update_fx_dual_position_cross_mode` | Switch margin mode (cross/isolated) |
| 9 | `cex_fx_update_fx_position_cross_mode` | Switch margin mode in single mode (do NOT use in dual) |
| 10 | `cex_fx_update_fx_dual_position_leverage` | Set leverage (dual mode) |
| 11 | `cex_fx_update_fx_position_leverage` | Set leverage (single mode, do NOT use in dual) |
| 12 | `cex_fx_create_fx_order` | Place order (open/close/reverse) |
| 13 | `cex_fx_list_fx_orders` | List orders |
| 14 | `cex_fx_get_fx_order` | Get single order detail |
| 15 | `cex_fx_cancel_fx_order` | Cancel single order |
| 16 | `cex_fx_cancel_all_fx_orders` | Cancel all orders for a contract |
| 17 | `cex_fx_amend_fx_order` | Amend order (price/size) |

## Execution workflow

### 1. Intent and parameters

- Determine module (Open/Close/Cancel/Amend/TP-SL/Conditional/Manage).
- Extract: `contract`, `side`, `size`, `price`, `leverage` (for Open/Close); `trigger_price`, `trigger_rule`, `order_size`, `order_price`, `order_tif` (for TP/SL/Conditional).
- **Top gainer/loser**: if user requests "top gainer" / "top loser" (or equivalent) instead of a specific contract, call `cex_fx_get_fx_tickers(settle="usdt")`, sort by `changePercentage` (descending for gainer, ascending for loser), pick the top contract. Then continue the open flow with that contract.
- **Missing**: if required params missing (e.g. size), ask user (clarify mode).

### 2. Pre-flight checks

- **Contract**: call `cex_fx_get_fx_contract` to ensure contract exists and is tradeable.
- **Account**: check balance and conflicting positions (e.g. when switching margin mode).
- **Risk**: do **not** pre-calculate valid limit price from `order_price_deviate` (actual deviation limit depends on risk_limit_tier). On `PRICE_TOO_DEVIATED`, show the valid range from the error message.
- **Settle currency**: always `usdt` unless user explicitly specifies BTC-settled contract.
- **Margin mode vs position mode** (only when user **explicitly** requested a margin mode and it differs from current): call **`cex_fx_get_fx_accounts(settle)`** to get **position mode**. From response **`position_mode`**: `single` = single position mode, `dual` = dual (hedge) position mode. Margin mode from position: use **position query** per dual/single above → `pos_margin_mode` (cross/isolated). **If user did not specify margin mode, do not switch; place order in current mode.**
  - **Single position** (`position_mode === "single"`): do **not** interrupt. Prompt user: *"You already have a {currency} position; switching margin mode will apply to this position too. Continue?"* (e.g. currency from contract: BTC_USDT → BTC). Wait for user confirmation, then continue.
  - **Dual position** (`position_mode === "dual"`): **interrupt** flow. Tell user: *"Please close the position first, then open a new one."*

- **Dual mode vs single mode (API choice)**: call **`cex_fx_get_fx_accounts(settle)`** first. If **`position_mode === "dual"`** (or **`in_dual_mode === true`**):
  - **Position / leverage query**: use **`cex_fx_list_fx_positions(settle, holding=true)`** or **`cex_fx_get_fx_dual_position(settle, contract)`**. Do **not** use `cex_fx_get_fx_position` in dual mode (API returns an array and causes parse error).
  - **Margin mode switch**: use **`cex_fx_update_fx_dual_position_cross_mode(settle, contract, mode)`** (do not use `cex_fx_update_fx_position_cross_mode` in dual mode).
  - **Leverage**: use **`cex_fx_update_fx_dual_position_leverage(settle, contract, leverage)`** (do not use `cex_fx_update_fx_position_leverage` in dual mode; it returns array and causes parse error).
  If **single** mode: use **`cex_fx_get_fx_position(settle, contract)`** for position; **`cex_fx_update_fx_position_cross_mode`** for mode switch; **`cex_fx_update_fx_position_leverage`** for leverage.

### 3. Module logic

#### Module A: Open position

1. **Unit conversion**: if user does not specify size in **contracts**, distinguish between **USDT cost** ("spend 100U") and **USDT value** ("100U worth"), get `quanto_multiplier` from `cex_fx_get_fx_contract` and best bid/ask from `cex_fx_get_fx_order_book(settle, contract, limit=1)`:
   - **USDT cost (margin-based)**: open long: `contracts = cost / (0.0015 + 1/leverage) / quanto_multiplier / order_price`; open short: `contracts = cost / (0.0015 + 1.00075/leverage) / quanto_multiplier / max(order_price, best_bid)`. `order_price`: limit → specified price; market → best ask (long) or best bid (short). **`leverage` must come from the current position query (step 5); do not assume a default.**
   - **USDT value (notional-based)**: buy/open long: `contracts = usdt_value / price / quanto_multiplier`; sell/open short: `contracts = usdt_value / max(best_bid, order_price) / quanto_multiplier`. `price`: limit → specified price; market → best ask (buy) or best bid (sell).
   - **Base (e.g. BTC, ETH)**: contracts = base_amount ÷ quanto_multiplier
   - Floor to integer; must satisfy `order_size_min`.
2. **Mode**: **Switch margin mode only when the user explicitly requests it**: switch to isolated only when user explicitly asks for isolated (e.g. "isolated"); switch to cross only when user explicitly asks for cross (e.g. "cross"). **If the user does not specify margin mode, do not switch — place the order in the current margin mode** (from position `pos_margin_mode`). If user explicitly wants isolated, check leverage.
3. **Mode switch**: only when user **explicitly** requested a margin mode and it **differs from current** (current from position: `pos_margin_mode`), then **before** calling `cex_fx_update_fx_dual_position_cross_mode`/`cex_fx_update_fx_position_cross_mode`: get **position mode** via `cex_fx_get_fx_accounts(settle)` → **`position_mode`** (single/dual); if `position_mode === "single"`, show prompt *"You already have a {currency} position; switching margin mode will apply to this position too. Continue?"* and continue only after user confirms; if `position_mode === "dual"`, **do not** switch—interrupt and tell user *"Please close the position first, then open a new one."*
4. **Mode switch (no conflict)**: only when user **explicitly** requested cross or isolated and that target differs from current: if no position, or single position and user confirmed, call `cex_fx_update_fx_dual_position_cross_mode` (dual) or `cex_fx_update_fx_position_cross_mode` (single) with **`mode`** `"cross"` or `"isolated"`. **Do not switch if the user did not explicitly request a margin mode.**
5. **Leverage**: if user specified leverage and it **differs from current** (from position query per dual/single above), call **`cex_fx_update_fx_dual_position_leverage`** in dual mode or **`cex_fx_update_fx_position_leverage`** in single mode **first**, then proceed. **If user did not specify leverage, do not change it — use the current leverage from the position query for all calculations (e.g. USDT cost formula). Do not default to any value (e.g. 10x or 20x).**
6. **Pre-order confirmation**: get current leverage from **position query** (dual: `cex_fx_list_fx_positions` or `cex_fx_get_fx_dual_position`; single: `cex_fx_get_fx_position`) for contract + side. Show **final order summary** (contract, side, size, price or market, mode, **leverage**, estimated margin/liq price). Ask user to confirm (e.g. "Reply 'confirm' to place the order."). **Only after user confirms**, place order.
7. **Place order**: call `cex_fx_create_fx_order` (market: `tif=ioc`, `price=0`).
8. **Verify**: confirm position via **position query** (dual: `cex_fx_list_fx_positions(holding=true)` or `cex_fx_get_fx_dual_position`; single: `cex_fx_get_fx_position`).

#### Module B: Close position

1. **Position**: get current `size` and side via **position query** (dual: `cex_fx_list_fx_positions(settle, holding=true)` or `cex_fx_get_fx_dual_position(settle, contract)`; single: `cex_fx_get_fx_position(settle, contract)`).
2. **Branch**: full close (query then close with reduce_only); partial (compute size, `cex_fx_create_fx_order` reduce_only); reverse (close then open opposite in two steps).
3. **Verify**: confirm remaining position via same position query as step 1.

#### Module C: Cancel order

1. **Locate**: by order_id, or `cex_fx_list_fx_orders` and let user choose.
2. **Cancel**: single `cex_fx_cancel_fx_order` only (no batch cancel).
3. **Verify**: `finish_as` == `cancelled`.

#### Module D: Amend order

1. **Check**: order status must be `open`.
2. **Precision**: validate new price/size against contract.
3. **Amend**: call `cex_fx_amend_fx_order` to update price or size.

#### Module E: Take Profit / Stop Loss

Read `references/tp-sl.md` for full logic. Key points:

1. **Position check**: get current position to confirm side and size (dual/single mode rules from pre-flight checks apply).
2. **Trigger rule auto-selection**:
   - **Long TP**: `trigger_rule = ">="` (price rises to TP level)
   - **Long SL**: `trigger_rule = "<="` (price falls to SL level)
   - **Short TP**: `trigger_rule = "<="` (price falls to TP level)
   - **Short SL**: `trigger_rule = ">="` (price rises to SL level)
3. **Close flags** (`close`, `auto_size`, and `order_type` depend on position mode and side):
   - **Single mode, full close long**: `order_type = "close-long-position"`, `close = true`, no `auto_size`, `order_reduce_only = true`.
   - **Single mode, full close short**: `order_type = "close-short-position"`, `close = true`, no `auto_size`, `order_reduce_only = true`.
   - **Single mode, partial close long**: `order_type = "plan-close-long-position"`, `close = false`, no `auto_size`, `order_reduce_only = true`.
   - **Single mode, partial close short**: `order_type = "plan-close-short-position"`, `close = false`, no `auto_size`, `order_reduce_only = true`.
   - **Dual mode, full close long**: `order_type = "close-long-position"`, `close = false`, `auto_size = "close_long"`, `order_reduce_only = true`.
   - **Dual mode, full close short**: `order_type = "close-short-position"`, `close = false`, `auto_size = "close_short"`, `order_reduce_only = true`.
   - **Dual mode, partial close long**: `order_type = "plan-close-long-position"`, `close = false`, no `auto_size`, `order_reduce_only = true`.
   - **Dual mode, partial close short**: `order_type = "plan-close-short-position"`, `close = false`, no `auto_size`, `order_reduce_only = true`.
4. **Size**: if user says "close all" or does not specify size, use full close (size = 0) with mode-appropriate flags above; if partial, compute size and set `order_reduce_only = true`.
5. **Market vs limit**: if user does not specify execution price, use market (`order_price = "0"`, `order_tif = "ioc"`); otherwise limit (`order_tif = "gtc"`).
6. **Confirmation**: show summary (contract, side, trigger price, trigger rule, execution type, size or "close all") and ask user to confirm before calling `cex_fx_create_fx_price_triggered_order`.

#### Module F: Conditional Open

Read `references/conditional.md` for full logic. Key points:

1. **No position required**: this opens a new position when triggered.
2. **Trigger rule**: user specifies direction — "buy when drops to X" → `trigger_rule = "<="`, "buy when breaks above X" → `trigger_rule = ">="`.
3. **Size conversion**: same unit conversion rules as Module A (contracts, USDT cost, USDT value, base amount). Use `cex_fx_get_fx_contract` for `quanto_multiplier` and `cex_fx_get_fx_order_book` for best bid/ask. For cost-based conversion, use `trigger_price` as reference `order_price` when user has not specified an execution limit price.
4. **Order size sign**: positive = long, negative = short.
5. **Confirmation**: show full summary before placing.

#### Module G: Manage Triggered Orders

Read `references/manage.md` for full logic. Supports:
- **List**: `cex_fx_list_fx_price_triggered_orders`
- **Get detail**: `cex_fx_get_fx_price_triggered_order`
- **Cancel single**: `cex_fx_cancel_fx_price_triggered_order`
- **Cancel all**: `cex_fx_cancel_fx_price_triggered_order_list`
- **Amend**: `cex_fx_update_fx_price_triggered_order`

**Amend limitation**: only **TP/SL orders** (order_type contains `plan-close-*` or has `reduce_only`/`close` flag) support direct amendment via `cex_fx_update_fx_price_triggered_order`. **Conditional open orders created via API** return `APIOrderNotSupportUpdateTouchOrder` and **cannot** be amended — must cancel and re-create instead.

## Report template

After each operation, output a short standardized result.

For price-triggered orders:

```
✓ [Operation] [Contract]
  Trigger: [rule] [trigger_price]
  Execute: [market/limit price] × [size or "close all"] [reduce_only/close]
  Order ID: [id]
```

## Domain Knowledge

- **USDT perpetual futures**: linear contracts settled in USDT. Position size is measured in contracts; each contract represents `quanto_multiplier` units of the base asset (e.g. 0.001 BTC).
- **Cross vs Isolated margin**: cross mode shares the entire account balance as margin; isolated mode limits margin to the amount allocated to this position.
- **Single vs Dual position mode**: single mode holds one net position per contract; dual mode (hedge) allows simultaneous long and short positions on the same contract. API endpoints differ between modes.
- **Price-triggered orders**: conditional orders that fire when market price crosses a trigger level. Used for TP/SL (close existing position) and conditional open (open new position). The trigger is server-side; no client needs to be online.
- **Reduce-only**: ensures the order only reduces an existing position and does not accidentally open a new one. Always set for TP/SL orders.
- **Order size sign**: for price-triggered close orders, negative size = sell (close long), positive size = buy (close short). For open orders, positive = long, negative = short.

## Safety rules

### Confirmation

- **Open**: show final order summary (contract, side, size, price/market, mode, leverage, estimated liq/margin), then ask for confirmation before `cex_fx_create_fx_order`. Do **not** add text about mark price vs limit price, order_price_deviate, or suggesting to adjust price. Example: *"Reply 'confirm' to place the order."*
- **Close all, reverse, batch cancel**: show scope and ask for confirmation. Example: *"Close all positions? Reply to confirm."* / *"Cancel all orders for this contract. Continue?"*
- **Create TP/SL / Conditional**: show full summary (contract, trigger rule + price, execution price/type, size), then ask *"Reply 'confirm' to place this order."*
- **Cancel all triggered orders**: show scope (contract or all) and ask *"Cancel all triggered orders for [contract]? Reply to confirm."*
- **Amend triggered order**: show old vs new values and ask for confirmation.

### Order ID precision

Gate order IDs are 64-bit integers that exceed `Number.MAX_SAFE_INTEGER` (2^53-1). Standard JSON parsers silently corrupt them.

- **Always pass `order_id` as a string** (e.g. `"728451920374819843"`, not `728451920374819843`).
- When reading an order ID from an API response, copy it as the raw string token, never as a parsed number.
- When displaying order IDs to the user, always render as a string with no formatting (no commas or scientific notation).

### Errors

| Code | Action |
|------|--------|
| `BALANCE_NOT_ENOUGH` | Suggest deposit or lower leverage/size. |
| `PRICE_TOO_DEVIATED` | Extract **actual valid price range from the error message** and show to user (do not rely on contract `order_price_deviate`; actual limit depends on risk_limit_tier). |
| `POSITION_HOLDING` (mode switch) | API returns this (not `POSITION_NOT_EMPTY`). Ask user to close position first. |
| `CONTRACT_NOT_FOUND` | Contract invalid or not tradeable. Confirm contract name (e.g. BTC_USDT) and settle; suggest listing contracts. |
| `ORDER_NOT_FOUND` | Order already filled, triggered, cancelled, or wrong order_id. Suggest checking order history or listing triggered orders. |
| `APIOrderNotSupportUpdateTouchOrder` | API-created conditional open orders cannot be amended. Cancel and re-create instead. TP/SL orders are not affected and can be amended normally. |
| `SIZE_TOO_LARGE` | Order size exceeds limit. Suggest reducing size or check contract `order_size_max`. |
| `ORDER_FOK` | FOK order could not be filled entirely. Suggest different price/size or use GTC/IOC. |
| `ORDER_POC` | POC order would have taken liquidity; exchange rejected. Suggest different price for maker-only. |
| `INVALID_PARAM_VALUE` | Often in dual mode when wrong API or params used (e.g. `cex_fx_update_fx_position_cross_mode` or `cex_fx_update_fx_position_leverage` in dual). Use dual-mode APIs: `cex_fx_update_fx_dual_position_cross_mode`, `cex_fx_update_fx_dual_position_leverage`; for position use `cex_fx_list_fx_positions` or `cex_fx_get_fx_dual_position`. For price-triggered orders: check `trigger_rule`, `order_size` sign, `order_price` format. |
