---
name: gate-exchange-futures
description: "Gate Exchange USDT perpetual futures trading skill. Use when the user wants to trade contracts, open/close perpetual positions, or manage futures leverage. Triggers on 'open long', 'close short', 'USDT perpetual', 'futures TP/SL'."
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "💱"
    os:
      - darwin
      - linux
    primaryEnv: GATE_API_KEY
    requires:
      bins:
        - gate-cli
      env:
        - GATE_API_KEY
        - GATE_API_SECRET

    install:
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux x64)"
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux arm64)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Intel)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Apple Silicon)"
---

### Resolving `gate-cli` (binary path)

Resolve **`gate-cli`** in order: **(1)** **`command -v gate-cli`** and **`gate-cli --version`** succeeds; **(2)** **`${HOME}/.local/bin/gate-cli`** if executable; **(3)** **`${HOME}/.openclaw/skills/bin/gate-cli`** if executable. Canonical rules: [`exchange-runtime-rules.md`](../exchange-runtime-rules.md) §4 (or [`gate-runtime-rules.md`](../gate-runtime-rules.md) §4).


# Gate Futures Trading Suite

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

## Skill Dependencies


### gate-cli commands used

**Query Operations (Read-only)**

- `gate-cli cex futures account get`
- `gate-cli cex futures market contract`
- `gate-cli cex futures position get`
- `gate-cli cex futures order get`
- `gate-cli cex futures market orderbook`
- `gate-cli cex futures position get`
- `gate-cli cex futures price-trigger get`
- `gate-cli cex futures market tickers`
- `gate-cli cex futures order list`
- `gate-cli cex futures position list`
- `gate-cli cex futures price-trigger list`

**Execution Operations (Write)**

- `gate-cli cex futures order amend`
- `gate-cli cex futures order cancel`
- `gate-cli cex futures order cancel`
- `gate-cli cex futures price-trigger cancel`
- `gate-cli cex futures price-trigger cancel-all`
- `gate-cli cex futures order add; gate-cli cex futures order close; gate-cli cex futures order long; gate-cli cex futures order remove; gate-cli cex futures order short`
- `gate-cli cex futures price-trigger create`
- `gate-cli cex futures position update-cross-mode`
- `gate-cli cex futures position update-leverage`
- `gate-cli cex futures position update-cross-mode`
- `gate-cli cex futures position update-leverage`
- `gate-cli cex futures price-trigger update`

### Authentication
- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- **Permissions:** Fx:Write
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- **Required:** `gate-cli` (run `sh ./setup.sh` from this skill directory if missing; optional `GATE_CLI_SETUP_MODE=release`).
- Add `$HOME/.openclaw/skills/bin` to **`PATH`** if you invoke `gate-cli` by name (or the directory where [`setup.sh`](./setup.sh) installs it).
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`** — that is equivalent valid config for `gate-cli`. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Do not proceed with authenticated calls until the CLI behaves as expected (e.g. **`gate-cli --version`** or a read-only **`gate-cli cex ...`** command from this skill); confirm credentials resolve before mutating operations.

## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute module-specific routes in this `SKILL.md`.

- `SKILL.md` keeps routing logic (Open/Close/Cancel/Amend/TP-SL/Conditional/Manage).
- `references/gate-cli.md` is the authoritative `gate-cli` execution contract for tool contracts, mode switching safeguards, confirmation gates, and degraded handling.

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

## gate-cli command index

| # | Tool | Purpose |
|---|------|---------|
| 1 | `gate-cli cex futures market tickers` | Get all futures tickers (for top gainer/loser sorting) |
| 2 | `gate-cli cex futures market contract` | Get single contract info (precision, multiplier, etc.) |
| 3 | `gate-cli cex futures market orderbook` | Get contract order book (best bid/ask) |
| 4 | `gate-cli cex futures account get` | Get futures account (position mode: single/dual) |
| 5 | `gate-cli cex futures position list` | List positions (dual mode) |
| 6 | `gate-cli cex futures position get` | Get dual-mode position for a contract |
| 7 | `gate-cli cex futures position get` | Get single-mode position for a contract |
| 8 | `gate-cli cex futures position update-cross-mode` | Switch margin mode (cross/isolated) |
| 9 | `gate-cli cex futures position update-cross-mode` | Switch margin mode in single mode (do NOT use in dual) |
| 10 | `gate-cli cex futures position update-leverage` | Set leverage (dual mode) |
| 11 | `gate-cli cex futures position update-leverage` | Set leverage (single mode, do NOT use in dual) |
| 12 | `gate-cli cex futures order add; gate-cli cex futures order close; gate-cli cex futures order long; gate-cli cex futures order remove; gate-cli cex futures order short` | Place order (open/close/reverse) |
| 13 | `gate-cli cex futures order list` | List orders |
| 14 | `gate-cli cex futures order get` | Get single order detail |
| 15 | `gate-cli cex futures order cancel` | Cancel single order |
| 16 | `gate-cli cex futures order cancel` | Cancel all orders for a contract |
| 17 | `gate-cli cex futures order amend` | Amend order (price/size) |

## Execution workflow

### 1. Intent and parameters

- Determine module (Open/Close/Cancel/Amend/TP-SL/Conditional/Manage).
- Extract: `contract`, `side`, `size`, `price`, `leverage` (for Open/Close); `trigger_price`, `trigger_rule`, `order_size`, `order_price`, `order_tif` (for TP/SL/Conditional).
- **Top gainer/loser**: if user requests "top gainer" / "top loser" (or equivalent) instead of a specific contract, call `gate-cli cex futures market tickers`, sort by `changePercentage` (descending for gainer, ascending for loser), pick the top contract. Then continue the open flow with that contract.
- **Missing**: if required params missing (e.g. size), ask user (clarify mode).
### 2. Pre-flight checks

- **Contract**: call `gate-cli cex futures market contract` to ensure contract exists and is tradeable.
- **Account**: check balance and conflicting positions (e.g. when switching margin mode).
- **Risk**: do **not** pre-calculate valid limit price from `order_price_deviate` (actual deviation limit depends on risk_limit_tier). On `PRICE_TOO_DEVIATED`, show the valid range from the error message.
- **Settle currency**: always `usdt` unless user explicitly specifies BTC-settled contract.
- **Margin mode vs position mode** (only when user **explicitly** requested a margin mode and it differs from current): call **`gate-cli cex futures account get`** to get **position mode**. From response **`position_mode`**: `single` = single position mode, `dual` = dual (hedge) position mode. Margin mode from position: use **position query** per dual/single above → `pos_margin_mode` (cross/isolated). **If user did not specify margin mode, do not switch; place order in current mode.**
 - **Single position** (`position_mode === "single"`): do **not** interrupt. Prompt user: *"You already have a {currency} position; switching margin mode will apply to this position too. Continue?"* (e.g. currency from contract: BTC_USDT → BTC). Wait for user confirmation, then continue.
 - **Dual position** (`position_mode === "dual"`): **interrupt** flow. Tell user: *"Please close the position first, then open a new one."*

- **Dual mode vs single mode (API choice)**: call **`gate-cli cex futures account get`** first. If **`position_mode === "dual"`** (or **`in_dual_mode === true`**):
 - **Position / leverage query**: use **`gate-cli cex futures position list`** or **`gate-cli cex futures position get`**. Do **not** use `gate-cli cex futures position get` in dual mode (API returns an array and causes parse error).
 - **Margin mode switch**: use **`gate-cli cex futures position update-cross-mode`** (do not use `gate-cli cex futures position update-cross-mode` in dual mode).
 - **Leverage**: use **`gate-cli cex futures position update-leverage`** (do not use `gate-cli cex futures position update-leverage` in dual mode; it returns array and causes parse error).
 If **single** mode: use **`gate-cli cex futures position get`** for position; **`gate-cli cex futures position update-cross-mode`** for mode switch; **`gate-cli cex futures position update-leverage`** for leverage.

### 3. Module logic

#### Module A: Open position

1. **Unit conversion**: if user does not specify size in **contracts**, distinguish between **USDT cost** ("spend 100U") and **USDT value** ("100U worth"), get `quanto_multiplier` from `gate-cli cex futures market contract` and best bid/ask from `gate-cli cex futures market orderbook`:
 - **USDT cost (margin-based)**: open long: `contracts = cost / (0.0015 + 1/leverage) / quanto_multiplier / order_price`; open short: `contracts = cost / (0.0015 + 1.00075/leverage) / quanto_multiplier / max(order_price, best_bid)`. `order_price`: limit → specified price; market → best ask (long) or best bid (short). **`leverage` must come from the current position query (step 5); do not assume a default.**
 - **USDT value (notional-based)**: buy/open long: `contracts = usdt_value / price / quanto_multiplier`; sell/open short: `contracts = usdt_value / max(best_bid, order_price) / quanto_multiplier`. `price`: limit → specified price; market → best ask (buy) or best bid (sell).
 - **Base (e.g. BTC, ETH)**: contracts = base_amount ÷ quanto_multiplier
 - Floor to integer; must satisfy `order_size_min`.
2. **Mode**: **Switch margin mode only when the user explicitly requests it**: switch to isolated only when user explicitly asks for isolated (e.g. "isolated"); switch to cross only when user explicitly asks for cross (e.g. "cross"). **If the user does not specify margin mode, do not switch — place the order in the current margin mode** (from position `pos_margin_mode`). If user explicitly wants isolated, check leverage.
3. **Mode switch**: only when user **explicitly** requested a margin mode and it **differs from current** (current from position: `pos_margin_mode`), then **before** calling `gate-cli cex futures position update-cross-mode`/`gate-cli cex futures position update-cross-mode`: get **position mode** via `gate-cli cex futures account get` → **`position_mode`** (single/dual); if `position_mode === "single"`, show prompt *"You already have a {currency} position; switching margin mode will apply to this position too. Continue?"* and continue only after user confirms; if `position_mode === "dual"`, **do not** switch—interrupt and tell user *"Please close the position first, then open a new one."*
4. **Mode switch (no conflict)**: only when user **explicitly** requested cross or isolated and that target differs from current: if no position, or single position and user confirmed, call `gate-cli cex futures position update-cross-mode` (dual) or `gate-cli cex futures position update-cross-mode` (single) with **`mode`** `"cross"` or `"isolated"`. **Do not switch if the user did not explicitly request a margin mode.**
5. **Leverage**: if user specified leverage and it **differs from current** (from position query per dual/single above), call **`gate-cli cex futures position update-leverage`** in dual mode or **`gate-cli cex futures position update-leverage`** in single mode **first**, then proceed. **If user did not specify leverage, do not change it — use the current leverage from the position query for all calculations (e.g. USDT cost formula). Do not default to any value (e.g. 10x or 20x).**
6. **Pre-order confirmation**: get current leverage from **position query** (dual: `gate-cli cex futures position list` or `gate-cli cex futures position get`; single: `gate-cli cex futures position get`) for contract + side. Show **final order summary** (contract, side, size, price or market, mode, **leverage**, estimated margin/liq price). Ask user to confirm (e.g. "Reply 'confirm' to place the order."). **Only after user confirms**, place order.
7. **Place order**: call `gate-cli cex futures order add; gate-cli cex futures order close; gate-cli cex futures order long; gate-cli cex futures order remove; gate-cli cex futures order short` (market: `tif=ioc`, `price=0`).
8. **Verify**: confirm position via **position query** (dual: `gate-cli cex futures position list` or `gate-cli cex futures position get`; single: `gate-cli cex futures position get`).
#### Module B: Close position

1. **Position**: get current `size` and side via **position query** (dual: `gate-cli cex futures position list` or `gate-cli cex futures position get`; single: `gate-cli cex futures position get`).
2. **Branch**: full close (query then close with reduce_only); partial (compute size, `gate-cli cex futures order add; gate-cli cex futures order close; gate-cli cex futures order long; gate-cli cex futures order remove; gate-cli cex futures order short` reduce_only); reverse (close then open opposite in two steps).
3. **Verify**: confirm remaining position via same position query as step 1.

#### Module C: Cancel order

1. **Locate**: by order_id, or `gate-cli cex futures order list` and let user choose.
2. **Cancel**: single `gate-cli cex futures order cancel` only (no batch cancel).
3. **Verify**: `finish_as` == `cancelled`.

#### Module D: Amend order

1. **Check**: order status must be `open`.
2. **Precision**: validate new price/size against contract.
3. **Amend**: call `gate-cli cex futures order amend` to update price or size.

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
6. **Confirmation**: show summary (contract, side, trigger price, trigger rule, execution type, size or "close all") and ask user to confirm before calling `gate-cli cex futures price-trigger create`.

#### Module F: Conditional Open

Read `references/conditional.md` for full logic. Key points:

1. **No position required**: this opens a new position when triggered.
2. **Trigger rule**: user specifies direction — "buy when drops to X" → `trigger_rule = "<="`, "buy when breaks above X" → `trigger_rule = ">="`.
3. **Size conversion**: same unit conversion rules as Module A (contracts, USDT cost, USDT value, base amount). Use `gate-cli cex futures market contract` for `quanto_multiplier` and `gate-cli cex futures market orderbook` for best bid/ask. For cost-based conversion, use `trigger_price` as reference `order_price` when user has not specified an execution limit price.
4. **Order size sign**: positive = long, negative = short.
5. **Confirmation**: show full summary before placing.

#### Module G: Manage Triggered Orders

Read `references/manage.md` for full logic. Supports:
- **List**: `gate-cli cex futures price-trigger list`
- **Get detail**: `gate-cli cex futures price-trigger get`
- **Cancel single**: `gate-cli cex futures price-trigger cancel`
- **Cancel all**: `gate-cli cex futures price-trigger cancel-all`
- **Amend**: `gate-cli cex futures price-trigger update`

**Amend limitation**: only **TP/SL orders** (order_type contains `plan-close-*` or has `reduce_only`/`close` flag) support direct amendment via `gate-cli cex futures price-trigger update`. **Conditional open orders created via API** return `APIOrderNotSupportUpdateTouchOrder` and **cannot** be amended — must cancel and re-create instead.

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

- **Open**: show final order summary (contract, side, size, price/market, mode, leverage, estimated liq/margin), then ask for confirmation before `gate-cli cex futures order add; gate-cli cex futures order close; gate-cli cex futures order long; gate-cli cex futures order remove; gate-cli cex futures order short`. Do **not** add text about mark price vs limit price, order_price_deviate, or suggesting to adjust price. Example: *"Reply 'confirm' to place the order."*
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
| `INVALID_PARAM_VALUE` | Often in dual mode when wrong API or params used (e.g. `gate-cli cex futures position update-cross-mode` or `gate-cli cex futures position update-leverage` in dual). Use dual-mode APIs: `gate-cli cex futures position update-cross-mode`, `gate-cli cex futures position update-leverage`; for position use `gate-cli cex futures position list` or `gate-cli cex futures position get`. For price-triggered orders: check `trigger_rule`, `order_size` sign, `order_price` format. |
