---
name: gate-exchange-futures-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for Gate USDT perpetual futures: open/close, cancel/amend, TP/SL, conditional orders, trigger management, and risk-safe confirmations."
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

## 2. MCP Detection and Fallback

Detection:
1. Confirm MCP server exposes `cex_fx_get_fx_accounts` and `cex_fx_create_fx_order`.
2. Verify with a read call (`cex_fx_get_fx_tickers` or contract query).

Fallback:
- Missing server: show installer flow and stop.
- Auth/permission failure: stop writes, return corrective guidance.
- Mode-specific endpoint mismatch: re-check `position_mode` and re-route to dual/single tool variant.

## 3. Authentication

- API key required with `Fx:Write`.
- On auth errors, do not continue write operations.
- Never mask API/tool error root causes in user-facing status.

## 4. MCP Resources

No mandatory MCP Resource in futures skill.

## 5. Tool Calling Specification

### 5.1 Read Tools

| Tool | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `cex_fx_get_fx_accounts` | `settle` | account balance, `position_mode` | settle invalid |
| `cex_fx_get_fx_contract` | `settle`, `contract` | multiplier, min size, precision | contract not found |
| `cex_fx_get_fx_order_book` | `settle`, `contract` | best bid/ask, depth | market unavailable |
| `cex_fx_get_fx_tickers` | `settle` | mark/last price, change stats | unavailable |
| `cex_fx_list_fx_positions` | `settle`, optional holding | positions list | mode/empty |
| `cex_fx_get_fx_position` | `settle`, `contract` | single-mode position detail | invalid in dual mode |
| `cex_fx_get_fx_dual_position` | `settle`, `contract` | dual-side position detail | invalid in single mode |
| `cex_fx_list_fx_orders` | `settle`, filters | open/finished orders | filter mismatch |
| `cex_fx_get_fx_order` | `settle`, `order_id` | order detail/state | id not found |
| `cex_fx_list_price_triggered_orders` | `settle`, status | trigger order list | none found |
| `cex_fx_get_fx_price_triggered_order` | `settle`, `order_id` | trigger order detail | id invalid |

### 5.2 Write Tools

| Tool | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `cex_fx_create_fx_order` | settle, contract, size, price/tif | order id, status | size/price invalid |
| `cex_fx_cancel_fx_order` | settle, order_id | cancel status | already closed |
| `cex_fx_cancel_all_fx_orders` | settle, contract | cancel summary | none open |
| `cex_fx_amend_fx_order` | settle, order_id, price/size | amended order | not open |
| `cex_fx_create_fx_price_triggered_order` | settle + trigger payload | trigger order id | payload mismatch |
| `cex_fx_cancel_fx_price_triggered_order` | settle, order_id | cancel status | already done |
| `cex_fx_cancel_fx_price_triggered_order_list` | settle, optional contract | batch cancel summary | none open |
| `cex_fx_update_fx_price_triggered_order` | settle, order_id, update payload | updated trigger order | invalid transition |
| `cex_fx_update_fx_dual_position_cross_mode` | settle, contract, mode | mode updated | has conflicting position |
| `cex_fx_update_fx_position_cross_mode` | settle, contract, mode | mode updated | invalid in dual mode |
| `cex_fx_update_fx_dual_position_leverage` | settle, contract, leverage | leverage updated | invalid leverage |
| `cex_fx_update_fx_position_leverage` | settle, contract, leverage | leverage updated | invalid in dual mode |

## 6. Execution SOP (Non-Skippable)

### 6.1 Mode-first SOP
1. Always read `position_mode` from `cex_fx_get_fx_accounts` first.
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
