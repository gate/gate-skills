---
name: gate-exchange-alpha-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for Gate Alpha: token discovery, market viewing, account/order queries, quote-based buy/sell execution and order tracking."
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

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify Gate main `gate-cli` supports alpha query + place endpoints.
2. Probe with `gate-cli cex alpha market currencies` or ticker query.

Fallback:
- If trading endpoint unavailable, keep read-only Alpha mode.
- On auth failures, stop write flow and provide recovery guidance.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required for account/order/write operations.
- Read-only market endpoints may be public but still follow runtime checks.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

### 5.1 Read commands

- `gate-cli cex alpha market currencies`
- `gate-cli cex alpha market tokens`
- `gate-cli cex alpha market tickers`
- `gate-cli cex alpha account balances`
- `gate-cli cex alpha account book`
- `gate-cli cex alpha order list`
- `gate-cli cex alpha order get`
- `gate-cli cex alpha order quote`

### 5.2 Write commands

- `gate-cli cex alpha order place`

## 6. Execution SOP (Non-Skippable)

1. Route to module (discovery/market/account/order/trade).
2. For trade intent, normalize symbol/side/amount.
3. Always call `gate-cli cex alpha order quote` first.
4. Build trade draft from quote (expected receive/pay, slippage/gas fields if present).
5. Require explicit confirmation.
6. Execute `gate-cli cex alpha order place`.
7. Verify using `gate-cli cex alpha order get` or list orders.

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
