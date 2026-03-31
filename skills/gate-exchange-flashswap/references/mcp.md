---
name: gate-exchange-flashswap-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for Flash Swap: pair capability query, quote preview, one-to-one and multi-currency order placement, and order tracking."
---

# Gate FlashSwap MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Supported pair query
- Swap preview/quote query
- Flash swap order placement (single and multi-currency forms)
- Order/history/detail query

Out of scope:
- Spot orderbook trading
- DEX on-chain swaps

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate MCP exposes `cex_fc_preview_fc_order_v1` and `cex_fc_create_fc_order_v1`.
2. Probe with pair list endpoint.

Fallback:
- If write endpoints unavailable, downgrade to query/preview only.
- If MCP/auth fails, return setup/auth guidance.

## 3. Authentication

- API key required for user order operations.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

### 5.1 Read tools

- `cex_fc_list_fc_currency_pairs`
- `cex_fc_preview_fc_order_v1`
- `cex_fc_preview_fc_multi_currency_one_to_many_order`
- `cex_fc_preview_fc_multi_currency_many_to_one_order`
- `cex_fc_list_fc_orders`
- `cex_fc_get_fc_order`

### 5.2 Write tools

- `cex_fc_create_fc_order_v1`
- `cex_fc_create_fc_multi_currency_one_to_many_order`
- `cex_fc_create_fc_multi_currency_many_to_one_order`

## 6. Execution SOP (Non-Skippable)

1. Confirm swap intent and form (1:1 / 1:many / many:1).
2. Validate pair support and amount bounds.
3. Call corresponding preview endpoint first.
4. Present **Swap Draft** with expected exchange amounts and limits.
5. Require explicit confirmation before create endpoint.
6. Execute order and verify status with order query tool.

## 7. Output Templates

```markdown
## FlashSwap Draft
- Mode: {one_to_one_or_multi}
- Sell: {asset_and_amount}
- Buy: {asset_and_amount}
- Quote Summary: {preview_result}
- Risk: quote may change before execution.
Reply "Confirm swap" to execute.
```

```markdown
## FlashSwap Result
- Status: {success_or_failed}
- Order ID: {order_id}
- Filled: {filled_summary}
- Notes: {error_or_followup}
```

## 8. Safety and Degradation Rules

1. Always preview before create.
2. Never execute create endpoints without explicit immediate confirmation.
3. If preview/create mismatch occurs, re-preview and re-confirm.
4. Keep unsupported pairs and limit violations explicit.
5. Preserve API failures and avoid fabricated execution outcomes.
