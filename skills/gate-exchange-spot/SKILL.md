---
name: gate-spot-trading-assistant
version: "2026.3.5-1"
updated: "2026-03-05"
description: "Gate.io spot trading and account operations skill. Use this skill whenever the user asks to buy/sell crypto, check account value, cancel/amend spot orders, place conditional buy/sell plans, verify fills, or perform coin-to-coin swaps in Gate spot trading. Trigger phrases include 'buy coin', 'sell coin', 'monitor market', 'cancel order', 'amend order', 'break-even price', 'rebalance', 'spot trading', 'buy/sell', or any request that combines spot order execution with account checks."
---

# Gate.io Spot Trading Assistant

Execute integrated operations for Gate.io spot workflows, including:
- Buy and account queries (balance checks, asset valuation, minimum order checks)
- Smart monitoring and trading (automatic price-condition limit orders, no take-profit/stop-loss support)
- Order management and amendment (price updates, cancellations, fill verification, cost-basis checks, swaps)

## Domain Knowledge

### Common API Groups

| Group | Endpoints |
|------|------|
| Account and balances | `GET /spot/accounts` |
| Place/cancel/amend orders | `POST /spot/orders`, `DELETE /spot/orders`, `PATCH /spot/orders` |
| Orders and fills | `GET /spot/open_orders`, `GET /spot/my_trades` |
| Market data | `GET /spot/tickers`, `GET /spot/order_book`, `GET /spot/candlesticks` |
| Trading rules | `GET /spot/currencies/{currency}`, `GET /spot/currency_pairs/{pair}` |
| Fees | `GET /wallet/fee` |

### Key Trading Rules

- Use `BASE_QUOTE` format for trading pairs, for example `BTC_USDT`.
- Check quote-currency balance first before buy orders (for example USDT).
- Amount-based buys must satisfy `min_quote_amount` (commonly 10U).
- Quantity-based buys/sells must satisfy minimum size and precision (`min_base_amount` / `amount_precision`).
- Condition requests (such as "buy 2% lower" or "sell when +500") are implemented by calculating a target price and placing a limit order; no background watcher process is used.
- Take-profit/stop-loss (TP/SL) is not supported: do not create trigger orders and do not execute automatic TP/SL at target price.

### Market Order Parameter Extraction Rules (Mandatory)

When calling `POST /spot/orders` with `type=market`, fill `amount` by side:

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

Before every `POST /spot/orders`, present an order summary and require explicit user confirmation.

Required confirmation fields:
- trading pair (`currency_pair`)
- side and order type (`buy/sell`, `market/limit`)
- `amount` meaning and value
- limit price (if applicable) or pricing basis
- estimated cost/proceeds and main risk note (for example slippage)

Allowed confirmation responses (examples):
- `Confirm`, `Proceed`, `Yes, place it`

If user confirmation is missing, ambiguous, or negative:
- do not place the order
- return a pending status and ask for explicit confirmation

### Step 4: Call APIs by Scenario

Use only the minimal API set required for the task:
- Balance and available funds: `GET /spot/accounts`
- Rule validation: `GET /spot/currency_pairs/{pair}`
- Live price and moves: `GET /spot/tickers`
- Order placement: `POST /spot/orders`
- Cancel/amend: `DELETE /spot/orders` / `PATCH /spot/orders`
- Fill verification: `GET /spot/my_trades`

### Step 5: Return Actionable Result and Status

The response must include:
- Whether execution succeeded (or why it did not execute)
- Core numbers (price, quantity, amount, balance change)
- If condition not met, clearly explain why no order is placed now

## Case Routing Map (1-25)

### A. Buy and Account Queries (1-8)

| Case | User Intent | Core Decision | API Sequence |
|------|----------|----------|----------|
| 1 | Market buy | Place market buy if USDT is sufficient | `GET /spot/accounts` → `POST /spot/orders` |
| 2 | Buy at target price | Create a `limit buy` order | `GET /spot/accounts` → `POST /spot/orders` |
| 3 | Buy with all balance | Use all available USDT balance to buy | `GET /spot/accounts` → `POST /spot/orders` |
| 4 | Buy readiness check | Currency status + min size + current unit price | `GET /spot/currencies/{currency}` → `GET /spot/currency_pairs/{pair}` → `GET /spot/tickers` |
| 5 | Asset summary | Convert all holdings to USDT value | `GET /spot/accounts` → `GET /spot/tickers` |
| 6 | Cancel all then check balance | Cancel all open orders and return balances | `DELETE /spot/orders` → `GET /spot/accounts` |
| 7 | Sell dust | Sell only if minimum size is met | `GET /spot/accounts` → `GET /spot/currency_pairs/{pair}` → `POST /spot/orders` |
| 8 | Minimum buy check | Warn if below `min_quote_amount` | `GET /spot/currency_pairs/{pair}` → `POST /spot/orders` |

### B. Smart Monitoring and Trading (9-16)

| Case | User Intent | Core Decision | API Sequence |
|------|----------|----------|----------|
| 9 | Buy 2% lower | Place limit buy at current price -2% | `GET /spot/tickers` → `POST /spot/orders` |
| 10 | Sell at +500 | Place limit sell at current price +500 | `GET /spot/tickers` → `POST /spot/orders` |
| 11 | Buy near today's low | Buy only if current price is near 24h low | `GET /spot/tickers` → `POST /spot/orders` |
| 12 | Sell on 5% drop request | Calculate target drop price and place sell limit order | `GET /spot/tickers` → `POST /spot/orders` |
| 13 | Buy top gainer | Auto-pick highest 24h gainer and buy | `GET /spot/tickers` → `POST /spot/orders` |
| 14 | Buy larger loser | Compare BTC/ETH daily drop and buy the bigger loser | `GET /spot/tickers` → `POST /spot/orders` |
| 15 | Buy then place sell | Market buy, then place sell at +2% reference price | `POST /spot/orders` → `POST /spot/orders` |
| 16 | Fee estimate | Estimate total cost from fee rate and live price | `GET /wallet/fee` → `GET /spot/tickers` |

### C. Order Management and Amendment (17-25)

| Case | User Intent | Core Decision | API Sequence |
|------|----------|----------|----------|
| 17 | Raise price for unfilled order | Find open order, then amend price | `GET /spot/open_orders` → `PATCH /spot/orders` |
| 18 | Verify fill and holdings | Last buy fill quantity + current total holdings | `GET /spot/my_trades` → `GET /spot/accounts` |
| 19 | Cancel if not filled | If still open, cancel and then recheck balance | `GET /spot/open_orders` → `DELETE /spot/orders` → `GET /spot/accounts` |
| 20 | Rebuy at last price | Use last fill price, check balance, then place limit buy | `GET /spot/my_trades` → `GET /spot/accounts` → `POST /spot/orders` |
| 21 | Sell at break-even or better | Sell only if current price is above cost basis | `GET /spot/my_trades` → `GET /spot/tickers` → `POST /spot/orders` |
| 22 | Asset swap | Estimate value, if >=10U then sell then buy | `GET /spot/accounts` → `GET /spot/tickers` → `POST /spot/orders`(sell) → `POST /spot/orders`(buy) |
| 23 | Buy if price condition met | Buy only when `current < 60000`, then report balance | `GET /spot/tickers` → `POST /spot/orders` → `GET /spot/accounts` |
| 24 | Buy on trend condition | Buy only if 3 of last 4 hourly candles are bullish | `GET /spot/candlesticks` → `POST /spot/orders` |
| 25 | Fast-fill limit buy | Use best opposite-book price for fast execution | `GET /spot/order_book` → `POST /spot/orders` |

## Judgment Logic Summary

| Condition | Action |
|-----------|--------|
| User asks to check balance before buying | Must call `GET /spot/accounts` first; place order only if sufficient |
| User specifies buy/sell at target price | Use `type=limit` at user-provided price |
| User asks for fastest fill at current market | Prefer `market`; if "fast limit" is requested, use best book price |
| Market buy (`buy`) | Fill `amount` with USDT quote amount, not base quantity |
| Market sell (`sell`) | Fill `amount` with base-coin quantity, not USDT amount |
| User requests take-profit/stop-loss | Clearly state TP/SL is not supported; provide manual limit alternative |
| Any order placement request | Require explicit final user confirmation before `POST /spot/orders` |
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
- `⏸️ No order placed yet: current price is 60200, above your target 60000.`
- `❌ Not executed: minimum order amount is 10U, your input is 5U.`

## Error Handling

| Error Type | Typical Cause | Handling Strategy |
|----------|----------|----------|
| Insufficient balance | Not enough available USDT/coins | Return shortfall and suggest reducing order size |
| Minimum trade constraint | Below minimum amount/size | Return threshold and suggest increasing order size |
| Unsupported capability | User asks for TP/SL | Clearly state unsupported, propose manual limit-order workflow |
| Missing final confirmation | User has not clearly approved final order summary | Keep order pending and request explicit confirmation |
| Order missing/already filled | Amendment/cancellation target is invalid | Ask user to refresh open orders and retry |
| Market condition not met | Trigger condition is not satisfied | Return current price, target price, and difference |
| Pair unavailable | Currency suspended or abnormal status | Clearly state pair is currently not tradable |

## Cross-Skill Workflows

### Workflow A: Buy Then Amend

1. Place order with `gate-spot-trading-assistant` (Case 2/9/23)
2. If still unfilled, amend price (Case 17)

### Workflow B: Cancel Then Rebuy

1. Cancel all open orders to release funds (Case 6)
2. Re-enter with updated strategy (Case 1/2/9)

## Safety Rules

- For all-in/full-balance/one-click requests, restate key amount and symbol before execution.
- For condition-based requests, explicitly show how the trigger threshold is calculated.
- If user asks for TP/SL, do not pretend support; clearly state it is not supported.
- Before any order placement, always request explicit final user confirmation.
- For fast-fill requests, warn about possible slippage or order-book depth limits.
- For chained actions (sell then buy), report step-by-step results clearly.
- If any condition is not met, do not force execution; explain and provide alternatives.
