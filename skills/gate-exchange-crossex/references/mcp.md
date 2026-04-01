---
name: gate-exchange-crossex-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for CrossEx operations across exchanges: account/position/order/history query, transfer, convert, order and leverage management."
---

# Gate CrossEx MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Cross-exchange account/order/position/history queries
- CrossEx order create/cancel/update
- Leverage and mode updates
- CrossEx transfer/convert operations

Out of scope:
- Non-CrossEx spot/futures workflows

## 2. MCP Detection and Fallback

Detection:
1. Verify `cex_crx_*` toolset is available.
2. Probe with account endpoint (`cex_crx_get_crx_account`).

Fallback:
- If read probe endpoints are unavailable (for example 404/permission/route errors), treat CrossEx as unavailable in this runtime, stop CrossEx execution, and route user to an alternative supported skill path.
- If read endpoints are available but write endpoints are unavailable, stay in query-only CrossEx mode.

## 3. Authentication

- API key required.
- Mutation actions require explicit confirmation.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

Namespace note:
- `cex_crx` is the base namespace prefix used by CrossEx module tools.

### Read tools
- `cex_crx_get_crx_account`
- `cex_crx_get_crx_fee`
- `cex_crx_get_crx_interest_rate`
- `cex_crx_get_crx_margin_positions_leverage`
- `cex_crx_get_crx_positions_leverage`
- `cex_crx_get_crx_order`
- `cex_crx_list_crx_open_orders`
- `cex_crx_list_crx_positions`
- `cex_crx_list_crx_margin_positions`
- `cex_crx_list_crx_history_orders`
- `cex_crx_list_crx_history_positions`
- `cex_crx_list_crx_history_trades`
- `cex_crx_list_crx_history_margin_positions`
- `cex_crx_list_crx_history_margin_interests`
- `cex_crx_list_crx_account_book`
- `cex_crx_list_crx_adl_rank`
- `cex_crx_list_crx_coin_discount_rate`
- `cex_crx_list_crx_rule_symbols`
- `cex_crx_list_crx_rule_risk_limits`
- `cex_crx_list_crx_transfer_coins`
- `cex_crx_list_crx_transfers`

### Write tools
- `cex_crx_create_crx_order`
- `cex_crx_cancel_crx_order`
- `cex_crx_update_crx_order`
- `cex_crx_close_crx_position`
- `cex_crx_create_crx_transfer`
- `cex_crx_create_crx_convert_quote`
- `cex_crx_create_crx_convert_order`
- `cex_crx_update_crx_account`
- `cex_crx_update_crx_margin_positions_leverage`
- `cex_crx_update_crx_positions_leverage`

## 6. Execution SOP (Non-Skippable)

1. Resolve target domain inside CrossEx (spot/margin/futures/transfer/convert/query).
2. Run read probe first (`cex_crx_get_crx_account` or equivalent). If probe fails, stop and degrade as module-unavailable.
3. Pre-check account and product rules (`rule_symbols`, leverage/risk limits as needed).
4. For every mutation, build action draft and require explicit confirmation.
5. Execute write call.
6. Verify resulting state with corresponding read endpoint.

## 7. Output Templates

```markdown
## CrossEx Action Draft
- Action: {order_or_transfer_or_convert_or_update}
- Target: {symbol_or_account}
- Parameters: {key_params}
- Risk: cross-exchange execution and margin/liquidation risk.
Reply "Confirm action" to proceed.
```

```markdown
## CrossEx Result
- Status: {success_or_failed}
- Object ID: {order_or_transfer_id}
- Post-State: {verification_summary}
```

## 8. Safety and Degradation Rules

1. Never execute CrossEx mutations without explicit immediate confirmation.
2. Validate exchange/symbol compatibility before write calls.
3. Surface leverage/risk-limit implications before changing leverage/mode.
4. Preserve backend error details and do not mask risk failures.
5. Degrade to query-only mode when write permissions are unavailable.
