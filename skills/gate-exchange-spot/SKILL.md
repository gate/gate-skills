---
name: gate-exchange-spot
version: "2026.3.10-1"
updated: "2026-03-10"
description: "Gate spot trading and account operations skill. Use this skill whenever the user asks to buy/sell crypto, check account value, cancel/amend spot orders, place conditional buy/sell plans, verify fills, or perform coin-to-coin swaps in Gate spot trading. Trigger phrases include 'buy coin', 'sell coin', 'monitor market', 'cancel order', 'amend order', 'break-even price', 'rebalance', 'spot trading', 'buy/sell', or any request that combines spot order execution with account checks."
---

# Gate Spot Trading Assistant

Execute integrated operations for Gate spot workflows, including:
- Buy and account queries (balance checks, asset valuation, minimum order checks)
- Smart monitoring and trading (automatic price-condition limit orders, no take-profit/stop-loss support)
- Order management and amendment (price updates, cancellations, fill verification, cost-basis checks, swaps)
- Advanced execution utilities (batch cancel, batch amend, batch order placement, slippage simulation, fee comparison, account-book checks)

## Domain Knowledge

### Tool Mapping by Domain

| Group | Tool Calls (`jsonrpc: call.method`) |
|------|------|
| Account and balances | `cex_spot_get_spot_accounts`, `cex_spot_list_spot_account_book` |
| Place/cancel/amend orders | `cex_spot_create_spot_order`, `cex_spot_create_spot_batch_orders`, `cex_spot_cancel_all_spot_orders`, `cex_spot_cancel_spot_order`, `cex_spot_cancel_spot_batch_orders`, `cex_spot_amend_spot_order`, `cex_spot_amend_spot_batch_orders` |
| Open orders and fills | `cex_spot_list_spot_orders`, `cex_spot_list_spot_my_trades` |
| Market data | `cex_spot_get_spot_tickers`, `cex_spot_get_spot_order_book`, `cex_spot_get_spot_candlesticks` |
| Trading rules | `cex_spot_get_currency`, `cex_spot_get_currency_pair` |
| Fees | `cex_wallet_get_wallet_fee`, `cex_spot_get_spot_batch_fee` |

### Key Trading Rules

- Use `BASE_QUOTE` format for trading pairs, for example `BTC_USDT`.
- Check quote-currency balance first before buy orders (for example USDT).
- Amount-based buys must satisfy `min_quote_amount` (commonly 10U).
- Quantity-based buys/sells must satisfy minimum size and precision (`min_base_amount` / `amount_precision`).
- Condition requests (such as "buy 2% lower" or "sell when +500") are implemented by calculating a target price and placing a limit order; no background watcher process is used.
- Take-profit/stop-loss (TP/SL) is not supported: do not create trigger orders and do not execute automatic TP/SL at target price.

### Market Order Parameter Extraction Rules (Mandatory)

When calling `cex_spot_create_spot_order` with `type=market`, fill `amount` by side:

| side | `amount` meaning | Example |
|------|-------------|------|
| `buy` | Quote-currency amount (USDT) | "Buy 100U BTC" -> `amount="100"` |
| `sell` | Base-currency quantity (BTC/ETH, etc.) | "Sell 0.01 BTC" -> `amount="0.01"` |

Pre-check before execution:
- `buy` market order: verify quote-currency balance can cover `amount` (USDT).
- `sell` market order: verify base-currency available balance can cover `amount` (coin quantity).

## Workflow

When the user asks for any spot trading operation, follow this sequence.

### Step 1: Identify Task Type

Classify the request into one of these six categories:
1. Buy (market/limit/full-balance buy)
2. Sell (full-position sell/conditional sell)
3. Account query (total assets, balance checks, tradability checks)
4. Order management (list open orders, amend, cancel)
5. Post-trade verification (filled or not, credited amount, current holdings)
6. Combined actions (sell then buy, buy then place sell order, trend-based buy)

### Step 2: Extract Parameters and Run Pre-checks

Extract key fields:
- `currency` / `currency_pair`
- `side` (`buy`/`sell`)
- `amount` (coin quantity) or `quote_amount` (USDT amount)
- `price` or price condition (for example "2% below current")
- trigger condition (execute only when condition is met)

When `type=market`, normalize parameters as:
- `side=buy`: `amount = quote_amount` (USDT amount)
- `side=sell`: `amount = base_amount` (base-coin quantity)

Pre-check order:
1. Trading pair/currency tradability status
2. Minimum order amount/size and precision
3. Available balance sufficiency
4. User condition satisfaction (for example "buy only below 60000")

### Step 3: Final User Confirmation Before Any Order Placement (Mandatory)

Before every `cex_spot_create_spot_order` or `cex_spot_create_spot_batch_orders`, always provide an **Order Draft** first, then wait for explicit confirmation.

Required execution flow:
1. Send order draft (no trading call yet)
2. Wait for explicit user approval
3. Only after approval, submit the real order
4. Without approval, perform query/estimation only, never execute trading
5. Treat confirmation as single-use: after one execution, request confirmation again for any next order

Required confirmation fields:
- trading pair (`currency_pair`)
- side and order type (`buy/sell`, `market/limit`)
- `amount` meaning and value
- limit price (if applicable) or pricing basis
- estimated fill / estimated cost or proceeds
- main risk note (for example slippage)

Recommended draft wording:
- `Order Draft: BTC_USDT, buy, market, amount=100 USDT, estimated fill around current ask, risk: slippage in fast markets. Reply "Confirm order" to place it.`

Allowed confirmation responses (examples):
- `Confirm order`, `Confirm`, `Proceed`, `Yes, place it`

Hard blocking rules (non-bypassable):
- NEVER call `cex_spot_create_spot_order` unless the user explicitly confirms in the immediately previous turn.
- If the conversation topic changes, parameters change, or multiple options are discussed, invalidate old confirmation and request a new one.
- For multi-leg execution (for example case 15/22), require confirmation for each leg separately before each `cex_spot_create_spot_order`.

If user confirmation is missing, ambiguous, or negative:
- do not place the order
- return a pending status and ask for explicit confirmation
- continue with read-only actions only (balance checks, market quotes, fee estimation)

### Step 4: Call Tools by Scenario

Use only the minimal tool set required for the task:
- Balance and available funds: `cex_spot_get_spot_accounts`
- Rule validation: `cex_spot_get_currency_pair`
- Live price and moves: `cex_spot_get_spot_tickers`
- Order placement: `cex_spot_create_spot_order` / `cex_spot_create_spot_batch_orders`
- Cancel/amend: `cex_spot_cancel_all_spot_orders` / `cex_spot_cancel_spot_order` / `cex_spot_cancel_spot_batch_orders` / `cex_spot_amend_spot_order` / `cex_spot_amend_spot_batch_orders`
- Open order query: `cex_spot_list_spot_orders` (use `status=open`)
- Fill verification: `cex_spot_list_spot_my_trades`
- Account change history: `cex_spot_list_spot_account_book`
- Batch fee query: `cex_spot_get_spot_batch_fee`

### Step 5: Return Actionable Result and Status

The response must include:
- Whether execution succeeded (or why it did not execute)
- Core numbers (price, quantity, amount, balance change)
- If condition not met, clearly explain why no order is placed now

## Case Routing Map (1-31)

### A. Buy and Account Queries (1-8)

| Case | User Intent | Core Decision | Tool Sequence |
|------|----------|----------|----------|
| 1 | Market buy | Place market buy if USDT is sufficient | `cex_spot_get_spot_accounts` → `cex_spot_create_spot_order` |
| 2 | Buy at target price | Create a `limit buy` order | `cex_spot_get_spot_accounts` → `cex_spot_create_spot_order` |
| 3 | Buy with all balance | Use all available USDT balance to buy | `cex_spot_get_spot_accounts` → `cex_spot_create_spot_order` |
| 4 | Buy readiness check | Currency status + min size + current unit price | `cex_spot_get_currency` → `cex_spot_get_currency_pair` → `cex_spot_get_spot_tickers` |
| 5 | Asset summary | Convert all holdings to USDT value | `cex_spot_get_spot_accounts` → `cex_spot_get_spot_tickers` |
| 6 | Cancel all then check balance | Cancel all open orders and return balances | `cex_spot_cancel_all_spot_orders` → `cex_spot_get_spot_accounts` |
| 7 | Sell dust | Sell only if minimum size is met | `cex_spot_get_spot_accounts` → `cex_spot_get_currency_pair` → `cex_spot_create_spot_order` |
| 8 | Balance + minimum buy check | Place order only if account balance and `min_quote_amount` are both satisfied | `cex_spot_get_spot_accounts` → `cex_spot_get_currency_pair` → `cex_spot_create_spot_order` |

### B. Smart Monitoring and Trading (9-16)

| Case | User Intent | Core Decision | Tool Sequence |
|------|----------|----------|----------|
| 9 | Buy 2% lower | Place limit buy at current price -2% | `cex_spot_get_spot_tickers` → `cex_spot_create_spot_order` |
| 10 | Sell at +500 | Place limit sell at current price +500 | `cex_spot_get_spot_tickers` → `cex_spot_create_spot_order` |
| 11 | Buy near today's low | Buy only if current price is near 24h low | `cex_spot_get_spot_tickers` → `cex_spot_create_spot_order` |
| 12 | Sell on 5% drop request | Calculate target drop price and place sell limit order | `cex_spot_get_spot_tickers` → `cex_spot_create_spot_order` |
| 13 | Buy top gainer | Auto-pick highest 24h gainer and buy | `cex_spot_get_spot_tickers` → `cex_spot_create_spot_order` |
| 14 | Buy larger loser | Compare BTC/ETH daily drop and buy the bigger loser | `cex_spot_get_spot_tickers` → `cex_spot_create_spot_order` |
| 15 | Buy then place sell | Market buy, then place sell at +2% reference price | `cex_spot_create_spot_order` → `cex_spot_create_spot_order` |
| 16 | Fee estimate | Estimate total cost from fee rate and live price | `cex_wallet_get_wallet_fee` → `cex_spot_get_spot_tickers` |

### C. Order Management and Amendment (17-25)

| Case | User Intent | Core Decision | Tool Sequence |
|------|----------|----------|----------|
| 17 | Raise price for unfilled order | Confirm how much to raise (or target price), locate unfilled buy orders, confirm which order to amend if multiple, then amend limit price | `cex_spot_list_spot_orders`(status=open) → `cex_spot_amend_spot_order` |
| 18 | Verify fill and holdings | Last buy fill quantity + current total holdings | `cex_spot_list_spot_my_trades` → `cex_spot_get_spot_accounts` |
| 19 | Cancel if not filled | If still open, cancel and then recheck balance | `cex_spot_list_spot_orders`(status=open) → `cex_spot_cancel_spot_order` → `cex_spot_get_spot_accounts` |
| 20 | Rebuy at last price | Use last fill price, check balance, then place limit buy | `cex_spot_list_spot_my_trades` → `cex_spot_get_spot_accounts` → `cex_spot_create_spot_order` |
| 21 | Sell at break-even or better | Sell only if current price is above cost basis | `cex_spot_list_spot_my_trades` → `cex_spot_get_spot_tickers` → `cex_spot_create_spot_order` |
| 22 | Asset swap | Estimate value, if >=10U then sell then buy | `cex_spot_get_spot_accounts` → `cex_spot_get_spot_tickers` → `cex_spot_create_spot_order`(sell) → `cex_spot_create_spot_order`(buy) |
| 23 | Buy if price condition met | Buy only when `current < 60000`, then report balance | `cex_spot_get_spot_tickers` → `cex_spot_create_spot_order` → `cex_spot_get_spot_accounts` |
| 24 | Buy on trend condition | Buy only if 3 of last 4 hourly candles are bullish | `cex_spot_get_spot_candlesticks` → `cex_spot_create_spot_order` |
| 25 | Fast-fill limit buy | Use best opposite-book price for fast execution | `cex_spot_get_spot_order_book` → `cex_spot_create_spot_order` |

### D. Advanced Spot Utilities (26-31)

| Case | User Intent | Core Decision | Tool Sequence |
|------|----------|----------|----------|
| 26 | Filter and batch-cancel selected open orders | Verify target order ids exist in open orders, show candidate list, cancel only after user verification | `cex_spot_list_spot_orders`(status=open) → `cex_spot_cancel_spot_batch_orders` |
| 27 | Market slippage simulation | Simulate average fill from order-book asks for a notional buy, compare to last price | `cex_spot_get_spot_order_book` → `cex_spot_get_spot_tickers` |
| 28 | Batch buy placement | Check total required quote amount vs available balance, then place multi-order basket | `cex_spot_get_spot_accounts` → `cex_spot_create_spot_batch_orders` |
| 29 | Fee-rate comparison across pairs | Compare fee tiers and translate fee impact into estimated cost | `cex_spot_get_spot_batch_fee` → `cex_spot_get_spot_tickers` |
| 30 | Account-book audit + current balance | Show recent ledger changes for a coin and current remaining balance | `cex_spot_list_spot_account_book` → `cex_spot_get_spot_accounts` |
| 31 | Batch amend open buy orders by +1% | Filter open orders by pair, select up to 5 target buy orders, reprice and batch amend after user verification | `cex_spot_list_spot_orders`(status=open) → `cex_spot_amend_spot_batch_orders` |

## Judgment Logic Summary

| Condition | Action |
|-----------|--------|
| User asks to check balance before buying | Must call `cex_spot_get_spot_accounts` first; place order only if sufficient |
| User specifies buy/sell at target price | Use `type=limit` at user-provided price |
| User asks for fastest fill at current market | Prefer `market`; if "fast limit" is requested, use best book price |
| Market buy (`buy`) | Fill `amount` with USDT quote amount, not base quantity |
| Market sell (`sell`) | Fill `amount` with base-coin quantity, not USDT amount |
| User requests take-profit/stop-loss | Clearly state TP/SL is not supported; provide manual limit alternative |
| Any order placement request | Require explicit final user confirmation before `cex_spot_create_spot_order` |
| User has not replied with clear confirmation | Keep order as draft; no trading execution |
| Confirmation is stale or not from the immediately previous turn | Invalidate it and require a fresh confirmation |
| Multi-leg trading flow | Require per-leg confirmation before each `cex_spot_create_spot_order` |
| User asks to amend an unfilled buy order | Confirm price increase amount or exact target price before `cex_spot_amend_spot_order` |
| Multiple open buy orders match amendment request | Ask user to choose which order to amend before executing |
| User requests selected-order batch cancellation | Verify each order id exists/open, present list, and run `cex_spot_cancel_spot_batch_orders` only after user verification |
| User requests batch amend for open orders | Filter target pair open buy orders (max 5), compute repriced levels, and run `cex_spot_amend_spot_batch_orders` only after user verification |
| User requests market slippage simulation | Use order-book depth simulation and compare weighted fill vs ticker last price |
| User requests multi-coin one-click buy | Validate summed quote requirement, then use `cex_spot_create_spot_batch_orders` |
| User requests fee comparison for multiple pairs | Use `cex_spot_get_spot_batch_fee` and convert to cost impact with latest prices |
| User requests account flow for a coin | Use `cex_spot_list_spot_account_book` and then reconcile with `cex_spot_get_spot_accounts` |
| User amount is too small | Check `min_quote_amount`; if not met, ask user to increase amount |
| User requests all-in buy/sell | Use available balance, then trim by minimum trade rules |
| Trigger condition not met | Do not place order; return current vs target price gap |

## Report Template

```markdown
## Execution Result

| Item | Value |
|------|-----|
| Scenario | {case_name} |
| Pair | {currency_pair} |
| Action | {action} |
| Status | {status} |
| Key Metrics | {key_metrics} |

{decision_text}
```

Example `decision_text`:
- `✅ Condition met. Your order has been placed.`
- `📝 Order draft ready. Reply "Confirm order" to execute.`
- `⏸️ No order placed yet: current price is 60200, above your target 60000.`
- `❌ Not executed: minimum order amount is 10U, your input is 5U.`

## Error Handling

| Error Type | Typical Cause | Handling Strategy |
|----------|----------|----------|
| Insufficient balance | Not enough available USDT/coins | Return shortfall and suggest reducing order size |
| Minimum trade constraint | Below minimum amount/size | Return threshold and suggest increasing order size |
| Unsupported capability | User asks for TP/SL | Clearly state unsupported, propose manual limit-order workflow |
| Missing final confirmation | User has not clearly approved final order summary | Keep order pending and request explicit confirmation |
| Stale confirmation | Confirmation does not match the current draft or is not in the previous turn | Reject execution and ask for reconfirmation |
| Draft-only mode | User has not confirmed yet | Only run query/estimation tools; do not call `cex_spot_create_spot_order` or `cex_spot_create_spot_batch_orders` |
| Ambiguous amendment target | Multiple candidate open buy orders | Keep pending and ask user to confirm order ID/row |
| Batch-cancel ambiguity | Some requested order ids are missing/not-open | Return matched vs unmatched ids and request reconfirmation |
| Batch-amend ambiguity | Candidate order set is unclear or exceeds max selection | Ask user to confirm exact order ids (up to 5) before execution |
| Order missing/already filled | Amendment/cancellation target is invalid | Ask user to refresh open orders and retry |
| Market condition not met | Trigger condition is not satisfied | Return current price, target price, and difference |
| Pair unavailable | Currency suspended or abnormal status | Clearly state pair is currently not tradable |

## Cross-Skill Workflows

### Workflow A: Buy Then Amend

1. Place order with `gate-exchange-spot` (Case 2/9/23)
2. If still unfilled, amend price (Case 17)

### Workflow B: Cancel Then Rebuy

1. Cancel all open orders to release funds (Case 6)
2. Re-enter with updated strategy (Case 1/2/9)

## Safety Rules

- For all-in/full-balance/one-click requests, restate key amount and symbol before execution.
- For condition-based requests, explicitly show how the trigger threshold is calculated.
- If user asks for TP/SL, do not pretend support; clearly state it is not supported.
- Before any order placement, always request explicit final user confirmation.
- Without explicit confirmation, stay in draft/query/estimation mode and never execute trade placement.
- Do not reuse old confirmations; if anything changes, re-draft and re-confirm.
- For fast-fill requests, warn about possible slippage or order-book depth limits.
- For chained actions (sell then buy), report step-by-step results clearly.
- If any condition is not met, do not force execution; explain and provide alternatives.
