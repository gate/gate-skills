---
name: gate-exchange-options
description: "Use this skill whenever you want to trade Gate options: place order (market/limit), close or reduce a position, cancel open orders, or amend open orders. Trigger phrases include: options, call, put, strike, expiration, mark IV, close option, cancel option order, amend option order."
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


Read and follow [exchange-runtime-rules.md](../exchange-runtime-rules.md) first.

# Gate Options Trading

This skill is the single entry for Gate options. It supports **five operation types**: place order (market/limit), place order (mark IV), close/reduce position, cancel open orders, amend open orders. User intent is routed to the matching workflow.

## Case coverage (5 cases)

| Case | Description | Example triggers (EN) | Example output (EN) |
|------|-------------|------------------------|----------------------|
| **Case 1** | Market/limit place order | "Market buy 1 BTC call, strike at current price, expire in one week" / "Sell 1000U weekly BTC call at 70k strike" / "Open long 1 SOL weekly option at market" / "Use half of account to buy BTC call expiring in 3 days" | "Order submitted! You have placed a {buy/sell} order on {underlying} at {market/limit price}, strike {xxx}, expiration {xxx}, option type {call/put}, size {xxx} contracts." |
| **Case 2** | Mark IV place order | "Mark IV order: buy 1 BTC call, one week expiry" / "Sell 1000U weekly BTC call at 70k strike, mark IV" / "Open long 1 SOL weekly option, mark IV" | Same as Case 1, but price is derived from mark IV or IV-to-price backend. |
| **Case 3** | Market/limit close or reduce position | "Market close my BTC call, expiry 03/18, strike 70000" / "Close half of my ETH put at market" / "Close all profitable option positions" / "Market close all options with loss over 50%" | "Close order submitted! As requested, you have closed {size} of your {long/short} position on {underlying} at {market/limit price}." |
| **Case 4** | Cancel open orders | "Cancel the BTC call order at 70k strike, expiry 03/18" / "Cancel all SOL call buy orders" / "Cancel all open orders" / "One-click cancel" | "Cancel successful! Your {specified/all} open order(s) have been cancelled. A total of {N} order(s) were cancelled, releasing {xxx} USDT margin." |
| **Case 5** | Amend open orders | "Change my BTC call order at 70k strike, expiry 03/18, price to 0.05" / "Halve the size of my SOL put at strike 70, expiry 03/20" | "Amend confirmed! Your open order on {underlying} has been updated: price is now {new price}, size is now {new size}. Waiting for fill." |

## Module overview

| Module | Description | Trigger keywords |
|--------|-------------|------------------|
| **Place order (market/limit)** | Buy or sell options at market or limit price | market buy, limit sell, open long, buy call, sell put, spend X on option |
| **Place order (mark IV)** | Place order by implied volatility (mark IV) | mark IV, IV order |
| **Close/reduce position** | Market/limit close or partial close | close position, flat, reduce half, close all profitable, close losing |
| **Cancel orders** | Cancel one or all open option orders | cancel order, revoke, cancel all, one-click cancel |
| **Amend orders** | Change price or size of open order | amend, modify price, change size |

## Routing rules

| Intent | Example phrases | Route to |
|--------|-----------------|---------|
| **Place order (market/limit)** | "Market buy 1 BTC call, strike at current price, expire in one week" / "Sell 1000U of weekly BTC call at 70k strike" / "Open long 1 SOL weekly option at market" / "Use half of account to buy BTC call expiring in 3 days" | Read `references/place-order.md` |
| **Place order (mark IV)** | "Mark IV order: buy 1 BTC call, one week expiry" / "Sell 1000U weekly BTC call at 70k strike, mark IV" / "Open long 1 SOL weekly option, mark IV" | Read `references/place-order.md` |
| **Close/reduce position** | "Market close my BTC call, expiry MM/DD, strike XXXX" / "Close half of ETH put at market" / "Close all BTC call long when price hits 60000" / "Market close all profitable option positions" | Read `references/close-position.md` |
| **Cancel orders** | "Cancel the BTC call order at 70k strike, expiry MM/DD" / "Cancel all SOL call buy orders" / "Cancel all open orders" | Read `references/cancel-order.md` |
| **Amend orders** | "Change my BTC call order at 70k strike, expiry MM/DD, price to XXXX" / "Halve the size of my SOL put at strike 70, expiry MM/DD" | Read `references/amend-order.md` |
| **Unclear** | "Help with options", "Show my option positions" | **Clarify**: query positions/orders, then guide user |

## Tool mapping

All options tools use the `cex_options_` prefix. See [gate-mcp tools](https://github.com/gate/gate-mcp/blob/main/gate-exchange/gate-local-mcp-tools.md).

| Group | MCP tools |
|-------|-----------|
| Underlying & contracts | `gate-cli cex options market underlyings`, `gate-cli cex options market expirations`, `gate-cli cex options market contracts`, `gate-cli cex options market contract` |
| Market data | `gate-cli cex options market order-book`, `gate-cli cex options market tickers` |
| Account & positions | `gate-cli cex options account get`, `gate-cli cex options position list` |
| Orders | `gate-cli cex options order list`, `gate-cli cex options order create`, `gate-cli cex options order cancel`, `gate-cli cex options order cancel-all` |
| Amend | `gate-cli cex options order amend` |
| Trades | `gate-cli cex options position my-trades` |

### Authentication
- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- **Permissions:** Options:Write (and reads as required for quotes/positions); use least privilege consistent with this skill.
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- **Required:** `gate-cli` (install from [gate-cli releases](https://github.com/gate/gate-cli/releases) or via a Gate MCP / skills installer for your environment).
- Add the directory containing **`gate-cli`** to **`PATH`** when invoking by name.
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`**. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Do not proceed with authenticated or mutating calls until the CLI works as expected (e.g. **`gate-cli cex options market tickers`** or **`gate-cli --version`**); confirm credentials resolve before orders.

## Execution workflow

### 1. Intent and parameters

- Determine module (Place / Close / Cancel / Amend).
- Extract: underlying, expiration, strike, call/put → resolve to exact **contract** name. Contract format is `{underlying}-{expiration}-{strike}-{C|P}` (e.g. `BTC_USDT-20210916-50000-C`). Use `list_options_contracts` or `get_options_contract`.
- **Missing**: if required params missing (e.g. strike or expiration), ask user (clarify mode).

### 2. Unit conversion (place order only)

When the user does not specify size in **contracts**, convert to **contracts** before placing the order.

| User phrase | Intent | How to get size (contracts) |
|-------------|--------|----------------------------|
| **Contracts** | Explicit contract count | "1 contract", "buy 3 contracts" → size = 1, 3 |
| **Base notional** | Notional in underlying | "0.1 BTC call", "1 BTC put" → contracts = **base_amount / multiplier** (from `get_options_contract`) |
| **Quote (USDT)** | Premium / cost in USDT | "1000U", "spend 500 USDT", "half of account" → contracts = **usdt_amount / price_per_contract** (from order book/ticker) |

- **Base notional → contracts**: `contracts = base_amount / multiplier`. Multiplier = face value of one contract in underlying units (from `get_options_contract`).
- **Quote (USDT) → contracts**: `contracts = usdt_amount / price_per_contract`. For "half of account", use `list_options_account` then half of available balance.
- **Default**: When user says "X BTC" or "X ETH" without "contract(s)", treat as **base notional** and convert. Use explicit "X contracts" for contract count.
- **Precision**: Floor to integer; must satisfy `order_size_min` from `get_options_contract`. If result &lt; order_size_min, inform user.

### 3. Pre-flight checks

- **Contract**: call `get_options_contract` (or resolve via `list_options_contracts`) to ensure contract exists.
- **Account**: for buy, check balance (and for quote-based size, check price_per_contract from order book/ticker).
- **Close/reduce**: verify position exists and close size does not exceed position. Full close: `close: true`, `size: 0`; partial: `reduce_only: true` and size (negative for long, positive for short).
- **Disambiguation**: If "one week" or "3 days" matches multiple expirations, pick nearest or list and ask. If "strike at current price", use underlying index price and pick nearest strike.

### 4. Confirmation

- **Place order**: show final order summary (contract, side, size in contracts, price or market, strike, expiration, call/put). Optionally show equivalent base notional or USDT when size was converted. *"Reply 'confirm' to place the order."* Only after user confirms, call `create_options_order`.
- **Close / cancel / amend**: show scope and ask for confirmation before executing.

### 5. Call tools and output

- Call tools in the order specified in the reference.
- Output using the response template for that case.

## Report template

After each operation, output a short standardized result (see Response templates below).

## Response templates

Use the English templates below for standardized output.

### Place order (Case 1 & 2)

```
Order submitted! You have placed a {buy/sell} order on {underlying} at {market/limit price / mark IV}, strike {xxx}, expiration {xxx}, option type {call/put}, size {xxx} contracts.
```
When size was converted from base notional or USDT, optionally add e.g. " (equiv. 1 BTC notional)" or " (equiv. xxx USDT)".

### Close/reduce position (Case 3)

```
Close order submitted! As requested, you have closed {size} of your {long/short} position on {underlying} at {market/limit price}.
```

### Cancel orders (Case 4)

**Tools**:
- **Cancel all open option orders (one-click / all underlyings)**: `gate-cli cex options order cancel-all` with **no params**.
- **Cancel a single order**: `gate-cli cex options order cancel`.
- **List open orders (to find order_id / confirm scope)**: `gate-cli cex options order list`.

```
Cancel successful! Your {specified/all} open order(s) have been cancelled. A total of {N} order(s) were cancelled, releasing {xxx} USDT margin.
```

### Amend order (Case 5)

```
Amend confirmed! Your open order on {underlying} has been updated: price is now {new price}, size is now {new size}. Waiting for fill.
```

## Safety rules

### Confirmation

- **Place order**: show final order summary (contract, side, size in contracts, price/market, strike, expiration, call/put), then ask for confirmation before `create_options_order`. Example: *"Reply 'confirm' to place the order."*
- **Close / cancel / amend (including single-order cancel)**: show exact scope (contract/order_id, side, size/price where applicable) and ask for confirmation before executing any action that creates/amends/cancels orders.

### Errors

| Code / situation | Action |
|------------------|--------|
| Insufficient balance | Suggest depositing or reducing size. |
| Size below `order_size_min` | Inform user; do not submit. |
| Contract not found | Confirm underlying, expiration, strike, call/put; suggest listing contracts. |
| Order not found | Order may be filled, cancelled, or wrong id; suggest checking order history. |

### Other

- Resolve **underlying, expiration, strike, call/put** to a single contract before create/cancel/amend.
- **Mark IV** orders: use backend IV-to-price conversion when available; otherwise clarify with user.
- **Precision**: Respect `order_size_min` and `order_price_round` from `get_options_contract`; round price to `order_price_round`.
