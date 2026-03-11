---
name: gate-exchange-futures
version: "2026.3.5-1"
updated: "2026-03-05"
description: "The USDT perpetual futures trading function of Gate Exchange: open position, close position, cancel order, amend order. Trigger phrases: open position, close position, cancel order, amend order, reverse, close all."
---

# Gate Futures Trading Suite

This skill is the single entry for Gate USDT perpetual futures. It supports **four operations only**: open position, close position, cancel order, amend order. User intent is routed to the matching workflow.

## Module overview

| Module | Description | Trigger keywords |
|--------|-------------|------------------|
| **Open** | Limit/market open long or short, cross/isolated mode, top gainer/loser order | `long`, `short`, `buy`, `sell`, `open`, `top gainer`, `top loser` |
| **Close** | Full close, partial close, reverse position | `close`, `close all`, `reverse` |
| **Cancel** | Cancel one or many orders | `cancel`, `revoke` |
| **Amend** | Change order price or size | `amend`, `modify` |

## Routing rules

| Intent | Example phrases | Route to |
|--------|-----------------|----------|
| **Open position** | "BTC long 1 contract", "market short ETH", "10x leverage long", "top gainer long 10U" | Read `references/open-position.md` |
| **Close position** | "close all BTC", "close half", "reverse to short", "close everything" | Read `references/close-position.md` |
| **Cancel orders** | "cancel that buy order", "cancel all orders", "list my orders" | Read `references/cancel-order.md` |
| **Amend order** | "change price to 60000", "change order size" | Read `references/amend-order.md` |
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

- Determine module (Open/Close/Cancel/Amend).
- Extract: `contract`, `side`, `size`, `price`, `leverage`.
- **Top gainer/loser**: if user requests "top gainer" / "top loser" (or equivalent) instead of a specific contract, call `cex_fx_get_fx_tickers(settle="usdt")`, sort by `changePercentage` (descending for gainer, ascending for loser), pick the top contract. Then continue the open flow with that contract.
- **Missing**: if required params missing (e.g. size), ask user (clarify mode).

### 2. Pre-flight checks

- **Contract**: call `cex_fx_get_fx_contract` to ensure contract exists and is tradeable.
- **Account**: check balance and conflicting positions (e.g. when switching margin mode).
- **Risk**: do **not** pre-calculate valid limit price from `order_price_deviate` (actual deviation limit depends on risk_limit_tier). On `PRICE_TOO_DEVIATED`, show the valid range from the error message.
- **Margin mode vs position mode** (only when user **explicitly** requested a margin mode and it differs from current): call **`cex_fx_get_fx_accounts(settle)`** to get **position mode**. From response **`position_mode`**: `single` = single position mode, `dual` = dual (hedge) position mode. Margin mode from position: use **position query** per dual/single above → `pos_margin_mode` (cross/isolated). **If user did not specify margin mode, do not switch; place order in current mode.**
  - **Single position** (`position_mode === "single"`): do **not** interrupt. Prompt user: *"You already have a {currency} position; switching margin mode will apply to this position too. Continue?"* (e.g. currency from contract: BTC_USDT → BTC). Wait for user confirmation, then continue.
  - **Dual position** (`position_mode === "dual"`): **interrupt** flow. Tell user: *"Please close the position first, then open a new one."*

- **Dual mode vs single mode (API choice)**: call **`cex_fx_get_fx_accounts(settle)`** first. If **`position_mode === "dual"`** (or **`in_dual_mode === true`**):
  - **Position / leverage query**: use **`cex_fx_list_fx_positions(settle, holding=true)`** or **`cex_fx_get_fx_dual_position(settle, contract)`**. Do **not** use `cex_fx_get_fx_position` in dual mode (API returns an array and causes parse error).
  - **Margin mode switch**: use **`cex_fx_update_fx_dual_position_cross_mode(settle, contract, mode)`** (do not use `cex_fx_update_fx_position_cross_mode` in dual mode).
  - **Leverage**: use **`cex_fx_update_fx_dual_position_leverage(settle, contract, leverage)`** (do not use `cex_fx_update_fx_position_leverage` in dual mode; it returns array and causes parse error).
  If **single** mode: use **`cex_fx_get_fx_position(settle, contract)`** for position; **`cex_fx_update_fx_dual_position_cross_mode`** for mode switch; **`cex_fx_update_fx_position_leverage`** for leverage.

### 3. Module logic

#### Module A: Open position

1. **Unit conversion**: if user does not specify size in **contracts**, distinguish between **USDT cost** ("spend 100U") and **USDT value** ("100U worth"), get `quanto_multiplier` from `cex_fx_get_fx_contract` and best bid/ask from `cex_fx_get_fx_order_book(settle, contract, limit=1)`:
   - **USDT cost (margin-based)**: open long: `contracts = cost / (0.0015 + 1/leverage) / quanto_multiplier / order_price`; open short: `contracts = cost / (0.0015 + 1.00075/leverage) / quanto_multiplier / max(order_price, best_bid)`. `order_price`: limit → specified price; market → best ask (long) or best bid (short). **`leverage` must come from the current position query (step 5); do not assume a default.**
   - **USDT value (notional-based)**: buy/open long: `contracts = usdt_value / price / quanto_multiplier`; sell/open short: `contracts = usdt_value / max(best_bid, order_price) / quanto_multiplier`. `price`: limit → specified price; market → best ask (buy) or best bid (sell).
   - **Base (e.g. BTC, ETH)**: contracts = base_amount ÷ quanto_multiplier
   - Floor to integer; must satisfy `order_size_min`.
2. **Mode**: **Switch margin mode only when the user explicitly requests it**: switch to isolated only when user explicitly asks for isolated (e.g. "isolated"); switch to cross only when user explicitly asks for cross (e.g. "cross"). **If the user does not specify margin mode, do not switch — place the order in the current margin mode** (from position `pos_margin_mode`). If user explicitly wants isolated, check leverage.
3. **Mode switch**: only when user **explicitly** requested a margin mode and it **differs from current** (current from position: `pos_margin_mode`), then **before** calling `cex_fx_update_fx_dual_position_cross_mode`: get **position mode** via `cex_fx_get_fx_accounts(settle)` → **`position_mode`** (single/dual); if `position_mode === "single"`, show prompt *"You already have a {currency} position; switching margin mode will apply to this position too. Continue?"* and continue only after user confirms; if `position_mode === "dual"`, **do not** switch—interrupt and tell user *"Please close the position first, then open a new one."*
4. **Mode switch (no conflict)**: only when user **explicitly** requested cross or isolated and that target differs from current: if no position, or single position and user confirmed, call `cex_fx_update_fx_dual_position_cross_mode(settle, contract, mode)` with **`mode`** `"CROSS"` or `"ISOLATED"`. **Do not switch if the user did not explicitly request a margin mode.**
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

## Report template

After each operation, output a short standardized result.

## Safety rules

### Confirmation

- **Open**: show final order summary (contract, side, size, price/market, mode, leverage, estimated liq/margin), then ask for confirmation before `cex_fx_create_fx_order`. Do **not** add text about mark price vs limit price, order_price_deviate, or suggesting to adjust price. Example: *"Reply 'confirm' to place the order."*
- **Close all, reverse, batch cancel**: show scope and ask for confirmation. Example: *"Close all positions? Reply to confirm."* / *"Cancel all orders for this contract. Continue?"*

### Errors

| Code | Action |
|------|--------|
| `BALANCE_NOT_ENOUGH` | Suggest deposit or lower leverage/size. |
| `PRICE_TOO_DEVIATED` | Extract **actual valid price range from the error message** and show to user (do not rely on contract `order_price_deviate`; actual limit depends on risk_limit_tier). |
| `POSITION_HOLDING` (mode switch) | API returns this (not `POSITION_NOT_EMPTY`). Ask user to close position first. |
| `CONTRACT_NOT_FOUND` | Contract invalid or not tradeable. Confirm contract name (e.g. BTC_USDT) and settle; suggest listing contracts. |
| `ORDER_NOT_FOUND` | Order already filled, cancelled, or wrong order_id. Suggest checking order history. |
| `SIZE_TOO_LARGE` | Order size exceeds limit. Suggest reducing size or check contract `order_size_max`. |
| `ORDER_FOK` | FOK order could not be filled entirely. Suggest different price/size or use GTC/IOC. |
| `ORDER_POC` | POC order would have taken liquidity; exchange rejected. Suggest different price for maker-only. |
| `INVALID_PARAM_VALUE` | Often in dual mode when wrong API or params used (e.g. `cex_fx_update_fx_position_cross_mode` or `cex_fx_update_fx_position_leverage` in dual). Use dual-mode APIs: `cex_fx_update_fx_dual_position_cross_mode`, `cex_fx_update_fx_dual_position_leverage`; for position use `cex_fx_list_fx_positions` or `cex_fx_get_fx_dual_position`. |
