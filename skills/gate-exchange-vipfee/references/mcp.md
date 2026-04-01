---
name: gate-exchange-vipfee-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for VIP tier and trading fee queries on Gate Exchange."
---

# Gate VIP Fee MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Query user VIP level/account detail
- Query spot/futures fee rates

Out of scope:
- Any order placement or account mutation

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate MCP exposes `cex_account_get_account_detail` and `cex_wallet_get_wallet_fee`.
2. Probe with account detail query.

Fallback:
- If MCP unavailable/auth invalid, return setup/auth guidance.

## 3. Authentication

- API key required for user-specific fee data.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

| Tool | Purpose | Common errors |
|---|---|---|
| `cex_account_get_account_detail` | fetch VIP/account profile context | auth denied |
| `cex_wallet_get_wallet_fee` | fetch spot/futures fee rates | market/pair filter mismatch |

## 6. Execution SOP (Non-Skippable)

1. Determine query type (VIP level, fee rates, combined).
2. Call minimal required read tools.
3. Normalize fee rendering (maker/taker, spot/futures context).
4. Return structured summary.

## 7. Output Templates

```markdown
## VIP & Fee Summary
- VIP Level: {vip_level}
- Spot Fee: maker {spot_maker}, taker {spot_taker}
- Futures Fee: maker {fx_maker}, taker {fx_taker}
- Notes: {conditions_or_scope}
```

## 8. Safety and Degradation Rules

1. Keep values as returned by API; no fabricated discounts.
2. Distinguish spot and futures fee contexts clearly.
3. If unavailable for a market/pair, mark as unavailable instead of defaulting.
4. This skill is read-only.
5. Preserve timestamp/context when fee values are queried for specific pairs.
