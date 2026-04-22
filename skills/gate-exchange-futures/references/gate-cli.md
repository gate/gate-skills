---
name: gate-exchange-futures-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for Gate USDT perpetual futures: open/close, cancel/amend, TP/SL, conditional orders, trigger management, and risk-safe confirmations."
---

# Gate Futures MCP Specification

> Authoritative MCP execution document for `gate-exchange-futures`.

## 1. Scope and Trigger Boundaries

In scope:
- Open/close futures positions
- Cancel/amend normal orders
- Create/manage price-triggered orders (TP/SL, conditional open)
- Position/account verification in single vs dual mode

Out of scope:
- Spot trading -> `gate-exchange-spot`
- DEX swap -> `gate-dex-trade`
- Pure market commentary without trading action -> `gate-exchange-marketanalysis`

## 2. `gate-cli` detection and Fallback

Detection:
1. Confirm `gate-cli` exposes `gate-cli cex futures account get` and `gate-cli cex futures order add; gate-cli cex futures order close; gate-cli cex futures order long; gate-cli cex futures order remove; gate-cli cex futures order short`.
2. Verify with a read call (`gate-cli cex futures market tickers` or contract query).

Fallback:
- Missing server: show installer flow and stop.
- Auth/permission failure: stop writes, return corrective guidance.
- Mode-specific endpoint mismatch: re-check `position_mode` and re-route to dual/single tool variant.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required with `Fx:Write`.
- On auth errors, do not continue write operations.
- Never mask API/tool error root causes in user-facing status.

## 4. Optional resources

No mandatory MCP Resource in futures skill.

## 5. `gate-cli` command specification

### 5.1 Read Tools

| Command | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `gate-cli cex futures account get` | `settle` | account balance, `position_mode` | settle invalid |
| `gate-cli cex futures market contract` | `settle`, `contract` | multiplier, min size, precision | contract not found |
| `gate-cli cex futures market orderbook` | `settle`, `contract` | best bid/ask, depth | market unavailable |
| `gate-cli cex futures market tickers` | `settle` | mark/last price, change stats | unavailable |
| `gate-cli cex futures position list` | `settle`, optional holding | positions list | mode/empty |
| `gate-cli cex futures position get` | `settle`, `contract` | single-mode position detail | invalid in dual mode |
| `gate-cli cex futures position get-dual` | `settle`, `contract` | dual-side position detail | invalid in single mode |
| `gate-cli cex futures order list` | `settle`, filters | open/finished orders | filter mismatch |
| `gate-cli cex futures order get` | `settle`, `order_id` | order detail/state | id not found |
| `gate-cli cex futures price-trigger list` | `settle`, status | trigger order list | none found |
| `gate-cli cex futures price-trigger get` | `settle`, `order_id` | trigger order detail | id invalid |

### 5.2 Write Tools

| Command | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `gate-cli cex futures order add; gate-cli cex futures order close; gate-cli cex futures order long; gate-cli cex futures order remove; gate-cli cex futures order short` | settle, contract, size, price/tif | order id, status | size/price invalid |
| `gate-cli cex futures order cancel` | settle, order_id | cancel status | already closed |
| `gate-cli cex futures order cancel` | settle, contract | cancel summary | none open |
| `gate-cli cex futures order amend` | settle, order_id, price/size | amended order | not open |
| `gate-cli cex futures price-trigger create` | settle + trigger payload | trigger order id | payload mismatch |
| `gate-cli cex futures price-trigger cancel` | settle, order_id | cancel status | already done |
| `gate-cli cex futures price-trigger cancel-all` | settle, optional contract | batch cancel summary | none open |
| `gate-cli cex futures price-trigger update` | settle, order_id, update payload | updated trigger order | invalid transition |
| `gate-cli cex futures position update-dual-cross-mode` | settle, contract, mode | mode updated (dual/hedge mode) | has conflicting position |
| `gate-cli cex futures position update-cross-mode` | settle, contract, mode | mode updated (single/one-way mode) | invalid in dual mode |
| `gate-cli cex futures position update-dual-leverage` | settle, contract, leverage | leverage updated (dual/hedge mode) | invalid leverage |
| `gate-cli cex futures position update-leverage` | settle, contract, leverage | leverage updated (single/one-way mode) | invalid in dual mode |

## 6. Execution SOP (Non-Skippable)

### 6.1 Mode-first SOP
1. Always read `position_mode` from `gate-cli cex futures account get` first.
2. Select dual/single tool variants accordingly.
3. If user requests margin-mode switch, apply strict conflict checks before writes.

### 6.2 Open/Close SOP
1. Validate contract + precision/multiplier.
2. Normalize size units (contracts vs USDT value/cost inputs).
3. Resolve leverage/margin mode changes only when explicitly requested.
4. **Mandatory confirmation gate**: contract, side, size, leverage, margin mode, order price/type, major risk.
5. Execute order and verify position/order state.

### 6.3 Trigger-order SOP (TP/SL + conditional)
1. Determine trigger rule based on user intent and side.
2. Determine full-close vs partial-close flags by position mode.
3. Draft trigger order details for confirmation.
4. Execute create/update/cancel only after confirmation.

### 6.4 Cancel/Amend SOP
1. Confirm target order is open.
2. For batch/all cancels, summarize scope and require confirmation.
3. Execute and return post-state.

## 7. Output Templates

```markdown
## Futures Order Draft
- Contract: {contract}
- Action: {open_or_close} {long_or_short}
- Size: {size_contracts}
- Type/Price: {order_type} {price_or_market}
- Leverage/Mode: {leverage}x, {cross_or_isolated}, {single_or_dual}
- Risk: {key_risk_note}
Reply "confirm" to place.
```

```markdown
## Trigger Draft
- Contract: {contract}
- Trigger: {rule} {trigger_price}
- Execution: {market_or_limit} {execution_price}
- Scope: {close_all_or_partial}
Reply "confirm" to place trigger order.
```

```markdown
## Futures Execution Result
- Status: {success_or_failed}
- Order ID: {order_id}
- Position Snapshot: {position_summary}
- Note: {error_or_next_step}
```

## 8. Safety and Degradation Rules

1. Every write action requires immediate explicit confirmation.
2. Do not mix dual-mode and single-mode endpoints.
3. Preserve order IDs as strings to avoid precision loss.
4. If `PRICE_TOO_DEVIATED` or similar risk errors occur, return server-provided valid range and stop auto-retry.
5. On any uncertain state transition, degrade to read-only verification before the next write.
