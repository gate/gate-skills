---
name: gate-exchange-tradfi-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for TradFi module: symbols, market data, assets, order/position query and order/position mutations."
---

# Gate TradFi MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- TradFi symbols and market data query
- TradFi order/position/assets query
- TradFi order/place/update/cancel and position close/update operations

Out of scope:
- CEX spot/futures/DEX operations

## 2. MCP Detection and Fallback

Detection:
1. Verify `cex_tradfi_*` tools are available.
2. Probe with `cex_tradfi_query_symbols` or `cex_tradfi_query_user_assets`.

Fallback:
- If write operations unavailable, switch to read-only TradFi mode.

## 3. Authentication

- API key required.
- Mutation calls require strict auth and explicit confirmation.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

Namespace note:
- `cex_tradfi` is the base namespace prefix used by this module.
- `cex_tradfi_*` endpoints belong to the TradFi module namespace.

### Read tools
- `cex_tradfi_query_categories`
- `cex_tradfi_query_mt5_account_info`
- `cex_tradfi_query_symbols`
- `cex_tradfi_query_symbol_detail`
- `cex_tradfi_query_symbol_ticker`
- `cex_tradfi_query_symbol_kline`
- `cex_tradfi_query_order_list`
- `cex_tradfi_query_order_history_list`
- `cex_tradfi_query_position_list`
- `cex_tradfi_query_position_history_list`
- `cex_tradfi_query_user_assets`

### Write tools
- `cex_tradfi_create_tradfi_order`
- `cex_tradfi_update_order`
- `cex_tradfi_delete_order`
- `cex_tradfi_update_position`
- `cex_tradfi_close_position`

## 6. Execution SOP (Non-Skippable)

1. Classify intent (query vs mutation).
2. For mutations, build action draft including symbol/side/volume/price and risk notes.
3. Require explicit confirmation.
4. Execute mutation call.
5. Verify via order/position query endpoints.

## 7. Output Templates

```markdown
## TradFi Action Draft
- Action: {place_or_update_or_cancel_or_close}
- Symbol: {symbol}
- Parameters: {key_params}
- Risk: market volatility and execution slippage.
Reply "Confirm action" to proceed.
```

```markdown
## TradFi Result
- Status: {success_or_failed}
- Object: {order_or_position_id}
- Updated State: {state_summary}
```

## 8. Safety and Degradation Rules

1. Never execute TradFi mutation calls without explicit immediate confirmation.
2. Keep symbol and volume precision as API expects.
3. If market data is stale/unavailable, warn before mutation.
4. Preserve backend error codes/messages.
5. Degrade to query-only mode when write permissions are missing.
