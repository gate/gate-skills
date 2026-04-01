---
name: gate-exchange-spot-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for Gate spot trading: order placement, trigger orders, query, amend/cancel, verification, and safety gates."
---

# Gate Spot MCP Specification

> Authoritative execution specification for `gate-exchange-spot`. `SKILL.md` handles intent routing; this file defines MCP execution contracts.

## 1. Scope and Trigger Boundaries

In scope:
- Spot buy/sell (market/limit)
- Trigger/conditional spot orders
- Spot order query, amend, cancel
- Balance/fill verification and fee estimation

Out of scope / route elsewhere:
- Futures intent -> `gate-exchange-futures`
- DEX swap intent -> `gate-dex-trade`
- Pure market analysis without trading action -> `gate-exchange-marketanalysis` or info skills

## 2. MCP Detection and Fallback

Detection:
1. Find main Gate MCP exposing `cex_spot_get_spot_accounts` + `cex_spot_create_spot_order`.
2. Verify with a read call (`cex_spot_get_spot_tickers`).

Fallback:
- MCP missing: show installer guidance only.
- Auth failure: follow runtime auth recovery and stop writes.
- Tool degradation: downgrade to read-only draft/estimation mode.

## 3. Authentication

- API key required.
- Minimal permissions: Spot:Write, Wallet:Read.
- On auth errors (`401`, permission denied): do not retry writes blindly; switch to guidance mode.

## 4. MCP Resources

No mandatory MCP Resource in this skill.

## 5. Tool Calling Specification

### 5.1 Read Tools

| Tool | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `cex_spot_get_spot_accounts` | optional `currency` | available/locked balances | auth, currency invalid |
| `cex_spot_get_currency` | `currency` | chain/tradability metadata | currency not found |
| `cex_spot_get_currency_pair` | `currency_pair` | min size, precision, tradable status | pair invalid |
| `cex_spot_get_spot_tickers` | optional pair | last, ask, bid, 24h stats | market unavailable |
| `cex_spot_get_spot_order_book` | `currency_pair` | asks/bids depth | depth unavailable |
| `cex_spot_get_spot_candlesticks` | pair + interval | candles OHLCV | interval invalid |
| `cex_spot_list_spot_orders` | pair + status | open/finished orders | status filter mismatch |
| `cex_spot_get_spot_price_triggered_order` | `order_id` | trigger detail/status | id not found |
| `cex_spot_list_spot_price_triggered_orders` | status/filter | trigger order list | empty result |
| `cex_spot_list_spot_my_trades` | pair/time/order_id | fill list, fee, side | empty fills |
| `cex_spot_list_spot_account_book` | filters/time | account ledger | range too large |
| `cex_spot_get_spot_batch_fee` | `currency_pairs` | maker/taker fee rates | pair unsupported |
| `cex_wallet_get_wallet_fee` | optional pair | account fee config | auth |

### 5.2 Write Tools

| Tool | Required inputs | Key return fields | Common errors |
|---|---|---|---|
| `cex_spot_create_spot_order` | pair, side, amount, type | order id, status | min amount, precision, balance |
| `cex_spot_create_spot_batch_orders` | orders[] | per-order result | partial failures |
| `cex_spot_create_spot_price_triggered_order` | trigger+put+market | trigger order id | trigger schema mismatch |
| `cex_spot_cancel_spot_order` | pair, order_id | cancel status | already closed |
| `cex_spot_cancel_spot_batch_orders` | pair, order_ids | batch cancel result | id mismatch |
| `cex_spot_cancel_all_spot_orders` | pair/account | cancel summary | none open |
| `cex_spot_cancel_spot_price_triggered_order` | order_id | cancel status | already triggered |
| `cex_spot_cancel_spot_price_triggered_order_list` | status/market/account | cancel summary | none open |
| `cex_spot_amend_spot_order` | order_id + price/amount | amended order | non-open order |
| `cex_spot_amend_spot_batch_orders` | orders[] | batch amend result | invalid amend set |

## 6. Execution SOP (Non-Skippable)

### 6.1 Universal pre-check
1. Normalize pair format to `BASE_QUOTE`.
2. Validate tradability + min amount/precision.
3. Validate available balance (quote for market-buy, base for sell).

### 6.2 Mandatory confirmation gate for writes
Before any write tool call, show an order draft with:
- pair, side, type
- amount meaning
- price basis (limit/market/trigger)
- estimated fill/cost and major risk

Only execute after explicit user confirmation in immediate previous turn.

### 6.3 Place/amend/cancel flow
1. Pre-check + draft
2. Confirm
3. Execute write
4. Verify using read endpoint (`list_spot_orders` / `my_trades` / `get_trigger_order`)

### 6.4 Multi-leg flow
For chained actions (sell->buy, buy->place TP-like trigger), require confirmation per leg.

## 7. Output Templates

```markdown
## Spot Order Draft
- Pair: {currency_pair}
- Side/Type: {side} {type}
- Amount: {amount} ({amount_semantics})
- Price: {price_or_market_basis}
- Estimated: {est_cost_or_receive}
- Risk: {risk_note}
Reply "Confirm order" to execute.
```

```markdown
## Spot Execution Result
- Status: {success_or_failed}
- Order ID: {order_id}
- Filled: {filled_amount}
- Avg Price: {avg_price}
- Fee: {fee}
- Next Check: {verification_hint}
```

## 8. Safety and Degradation Rules

1. Never place spot write orders without explicit final confirmation.
2. If pre-check fails (min amount, precision, balance), return blocking reason and suggested corrected input.
3. For trigger orders, echo trigger rule and trigger price before execution.
4. On API/tool errors, preserve raw reason and do not fabricate success.
5. If auth is invalid, stop writes and route to MCP setup/auth recovery.
