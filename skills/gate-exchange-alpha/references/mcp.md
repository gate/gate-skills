---
name: gate-exchange-alpha-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for Gate Alpha: token discovery, market viewing, account/order queries, quote-based buy/sell execution and order tracking."
---

# Gate Alpha MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Discover Alpha tradable tokens
- View Alpha market prices/tickers
- Query Alpha holdings and account-book data
- Place Alpha buy/sell orders through quote -> place flow
- Query Alpha order status/history

Out of scope:
- Non-Alpha spot/futures trading
- DEX on-chain swap operations

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate main MCP exposes alpha query + place endpoints.
2. Probe with `cex_alpha_list_alpha_currencies` or ticker query.

Fallback:
- If trading endpoint unavailable, keep read-only Alpha mode.
- On auth failures, stop write flow and provide recovery guidance.

## 3. Authentication

- API key required for account/order/write operations.
- Read-only market endpoints may be public but still follow runtime checks.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

### 5.1 Read tools

- `cex_alpha_list_alpha_currencies`
- `cex_alpha_list_alpha_tokens`
- `cex_alpha_list_alpha_tickers`
- `cex_alpha_list_alpha_accounts`
- `cex_alpha_list_alpha_account_book`
- `cex_alpha_list_alpha_orders`
- `cex_alpha_get_alpha_order`
- `cex_alpha_quote_alpha_order`

### 5.2 Write tool

- `cex_alpha_place_alpha_order`

## 6. Execution SOP (Non-Skippable)

1. Route to module (discovery/market/account/order/trade).
2. For trade intent, normalize symbol/side/amount.
3. Always call `cex_alpha_quote_alpha_order` first.
4. Build trade draft from quote (expected receive/pay, slippage/gas fields if present).
5. Require explicit confirmation.
6. Execute `cex_alpha_place_alpha_order`.
7. Verify using `cex_alpha_get_alpha_order` or list orders.

## 7. Output Templates

```markdown
## Alpha Trade Draft
- Token: {currency}
- Side: {buy_or_sell}
- Amount: {amount}
- Quote ID: {quote_id}
- Estimated Result: {estimation}
- Risk: price changes quickly; confirm before execution.
Reply "Confirm" to place order.
```

```markdown
## Alpha Execution Result
- Status: {success_or_failed}
- Order ID: {order_id}
- Side/Amount: {side} {amount}
- Follow-up: {verification_hint}
```

## 8. Safety and Degradation Rules

1. Never place Alpha orders without a fresh quote.
2. Never place Alpha orders without explicit immediate confirmation.
3. Quote/order mismatches must trigger re-quote.
4. Preserve backend order status and failure reasons.
5. If only partial account data is available, mark sections as degraded.
