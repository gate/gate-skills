---
name: gate-exchange-futurestrade
version: "2026.3.5-1"
updated: "2026-03-05"
description: "The USDT perpetual futures trading function of Gate Exchange: open position, close position, cancel order, amend order. Trigger phrases: open position, close position, cancel order, amend order, reverse, close all."
---

# Gate Futures Trading Suite

This skill is the single entry for Gate USDT perpetual futures. It supports **four operations only**: open position, close position, cancel order, amend order. User intent is routed to the matching workflow.

## Module overview

| Module | Description | Trigger keywords |
|--------|-------------|------------------|
| **Open** | Limit/market open long or short, cross/isolated mode | `long`, `short`, `buy`, `sell`, `open` |
| **Close** | Full close, partial close, reverse position | `close`, `close all`, `reverse` |
| **Cancel** | Cancel one or many orders | `cancel`, `revoke` |
| **Amend** | Change order price or size | `amend`, `modify` |

## Routing rules

| Intent | Example phrases | Route to |
|--------|-----------------|----------|
| **Open position** | "BTC long 1 contract", "market short ETH", "10x leverage long" | Read `references/open-position.md` |
| **Close position** | "close all BTC", "close half", "reverse to short", "close everything" | Read `references/close-position.md` |
| **Cancel orders** | "cancel that buy order", "cancel all orders", "list my orders" | Read `references/cancel-order.md` |
| **Amend order** | "change price to 60000", "change order size" | Read `references/amend-order.md` |
| **Unclear** | "help with futures", "show my position" | **Clarify**: query position/orders, then guide user |

## Execution workflow

### 1. Intent and parameters

- Determine module (Open/Close/Cancel/Amend).
- Extract: `contract`, `side`, `size`, `price`, `leverage`.
- **Missing**: if required params missing (e.g. size), ask user (clarify mode).

### 2. Pre-flight checks

- **Contract**: call `get_futures_contract` to ensure contract exists and is tradeable.
- **Account**: check balance and conflicting positions (e.g. when switching margin mode).
- **Risk**: limit orders must be within `order_price_deviate`; warn on large size.
- **Margin mode vs position mode** (only when user **explicitly** requested a margin mode and it differs from current): call **`get_futures_accounts(settle)`** to get **position mode**. From response **`position_mode`**: `single` = single position mode, `dual` = dual (hedge) position mode. Margin mode from position: `get_futures_position` → `pos_margin_mode` (cross/isolated). **If user did not specify margin mode, do not switch; place order in current mode.**
  - **Single position** (`position_mode === "single"`): do **not** interrupt. Prompt user: *"You already have a {currency} position; switching margin mode will apply to this position too. Continue?"* (e.g. currency from contract: BTC_USDT → BTC). Wait for user confirmation, then continue.
  - **Dual position** (`position_mode === "dual"`): **interrupt** flow. Tell user: *"Please close the position first, then open a new one."*

### 3. Module logic

#### Module A: Open position

1. **Unit conversion**: if user does not specify size in **contracts**, get `mark_price`, `quanto_multiplier` from `get_futures_contract`, then convert:
   - **U (USDT notional)**: contracts = u ÷ mark_price ÷ quanto_multiplier (no leverage); **with leverage**: contracts = u × leverage ÷ mark_price ÷ quanto_multiplier
   - **Base (e.g. BTC, ETH)**: contracts = base_amount ÷ quanto_multiplier
   - Round/truncate to `order_size_min` and size precision.
2. **Mode**: **Switch margin mode only when the user explicitly requests it**: switch to isolated only when user explicitly asks for isolated (e.g. "isolated", "逐仓"); switch to cross only when user explicitly asks for cross (e.g. "cross", "全仓"). **If the user does not specify margin mode, do not switch — place the order in the current margin mode** (from position `pos_margin_mode`). If user explicitly wants isolated, check leverage.
3. **Mode switch**: only when user **explicitly** requested a margin mode and it **differs from current** (current from position: `pos_margin_mode`), then **before** calling `update_futures_dual_comp_position_cross_mode`: get **position mode** via `get_futures_accounts(settle)` → **`position_mode`** (single/dual); if `position_mode === "single"`, show prompt *"You already have a {currency} position; switching margin mode will apply to this position too. Continue?"* and continue only after user confirms; if `position_mode === "dual"`, **do not** switch—interrupt and tell user *"Please close the position first, then open a new one."*
4. **Mode switch (no conflict)**: only when user **explicitly** requested cross or isolated and that target differs from current: if no position, or single position and user confirmed, call `update_futures_dual_comp_position_cross_mode(settle, contract, mode)` with **`mode`** `"CROSS"` or `"ISOLATED"`. **Do not switch if the user did not explicitly request a margin mode.**
5. **Leverage**: if user specified leverage and it **differs from current** (from `get_position`), call MCP **`update_futures_position_leverage`** (params: `settle`, `contract`, `leverage`) **first**, then proceed; in isolated mode always set via `update_futures_position_leverage` when switching.
6. **Pre-order confirmation**: call `get_position(settle, contract)` for **contract + side** to get current leverage (from position or default), and show it. Show **final order summary** (contract, side, size, price or market, mode, **leverage**, estimated margin/liq price). Ask user to confirm (e.g. "Reply 'confirm' to place the order."). **Only after user confirms**, place order.
7. **Place order**: call `create_futures_order` (market: `tif=ioc`, `price=0`).
8. **Verify**: call `get_futures_position` to confirm position.

#### Module B: Close position

1. **Position**: call `get_futures_position` for current `size` and side.
2. **Branch**: full close (query then close with reduce_only); partial (compute size, `create_futures_order` reduce_only); reverse (close then open opposite in two steps).
3. **Verify**: confirm remaining position.

#### Module C: Cancel order

1. **Locate**: by order_id, or `list_futures_orders` and let user choose.
2. **Cancel**: single `cancel_futures_order`; batch `cancel_futures_batch_orders` or `cancel_all_futures_orders` (by contract if needed).
3. **Verify**: `finish_as` == `cancelled`.

#### Module D: Amend order

1. **Check**: order status must be `open`.
2. **Precision**: validate new price/size against contract.
3. **Amend**: call `amend_futures_order` to update price or size.

## Report template

After each operation, output a short standardized result.

## Safety rules

### Confirmation

- **Open**: show final order summary (contract, side, size, price/market, mode, leverage, estimated liq/margin), then ask for confirmation before `create_futures_order`. Do **not** add text about mark price vs limit price, order_price_deviate, or suggesting to adjust price. Example: *"Reply 'confirm' to place the order."*
- **Close all, reverse, batch cancel**: show scope and ask for confirmation. Example: *"Close all positions? Reply to confirm."* / *"Cancel all orders for this contract. Continue?"*

### Errors

| Code | Action |
|------|--------|
| `BALANCE_NOT_ENOUGH` | Suggest deposit or lower leverage/size. |
| `PRICE_TOO_DEVIATED` | Show valid price range and suggest adjustment. |
| `POSITION_NOT_EMPTY` (mode switch) | Ask user to close position first. |
