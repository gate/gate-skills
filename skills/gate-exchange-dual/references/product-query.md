# Product Query — Cases 1, 3, 4, 5, 6

Product listing, eligibility check, settlement simulation, position summary, and settlement records.

## Available Tools

| Tool | Auth | Description |
|------|------|-------------|
| `cex_earn_list_dual_investment_plans` | Yes | List dual investment plans (optional param: plan_id) |
| `cex_earn_list_dual_orders` | Yes | List dual investment orders (see parameters below) |
| `cex_earn_list_dual_balance` | Yes | Get dual investment balance & interest stats |

### Parameters: `cex_earn_list_dual_orders`

| Param | Required | Type | Description |
|-------|----------|------|-------------|
| `page` | **Yes** | integer | Page number, **always start from 1** |
| `limit` | **Yes** | integer | Rows per page, **always pass 100** |
| `from` | No | integer | Start time (Unix timestamp in seconds) |
| `to` | No | integer | End time (Unix timestamp in seconds) |

> **Critical**: `page` and `limit` are **required** parameters. Always pass `page=1, limit=100` on the first call, then increment `page` until all data is fetched.

### Response Fields: `cex_earn_list_dual_orders`

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Order ID |
| `plan_id` | integer | Plan ID |
| `copies` | string | Number of copies |
| `invest_amount` | string | Investment amount |
| `settlement_amount` | string | Settlement amount |
| `create_time` | integer | Order creation time (Unix timestamp) |
| `complete_time` | integer | Order completion time (Unix timestamp) |
| `status` | string | Order status (see mapping below) |
| `invest_currency` | string | Investment currency (e.g. BTC, USDT) |
| `exercise_currency` | string | Exercise currency |
| `exercise_price` | string | Target price (exercise price) |
| `settlement_price` | string | Settlement price at delivery |
| `settlement_currency` | string | Currency received at settlement |
| `apy_display` | string | APY (decimal, multiply × 100 for %) |
| `apy_settlement` | string | Realized APY at settlement (decimal) |
| `delivery_time` | integer | **Delivery / Expiry date** (Unix timestamp) |

> **Important**: There is NO `type` field in order response. Derive sell-high / buy-low from `invest_currency`:
> - `invest_currency` is crypto (e.g. BTC, ETH) → **Sell High (Call)**
> - `invest_currency` is stablecoin (e.g. USDT) → **Buy Low (Put)**
>
> There is NO `instrument_name` field. To filter by coin (e.g. "BTC"), check if `invest_currency` or `exercise_currency` matches.

### Pagination Rule

To fetch all orders, loop with incrementing `page`:
1. Set `limit=100`, `page=1`
2. Call `cex_earn_list_dual_orders`
3. If returned rows < `limit` → all data fetched, stop
4. If returned rows == `limit` → increment `page`, repeat from step 2

---

### Global Data Formatting Rules (apply to ALL dual tools: orders, plans, balance, etc.)

| Field category | Rule |
|---------------|------|
| **Any APY/rate field** (`apy`, `apy_display`, `apy_settlement`, or any other rate field from any dual tool) | Raw decimal (e.g. `0.85`). **MUST multiply by 100** then append `%` for display (e.g. `85%`). Use raw decimal only in formulas. This applies to `cex_earn_list_dual_investment_plans`, `cex_earn_list_dual_orders`, `cex_earn_list_dual_balance`, and any other dual tool. |
| `invest_days` | Integer (days). Always display as a whole number — **no decimals**. Do NOT calculate from `invest_hours`. |
| All timestamps (`delivery_time`, `create_time`, `complete_time` for orders; `delivery_timest` for plans) | Unix timestamps. Format as **`yyyy-MM-dd`** in UTC+0. Label table header with "(UTC)" or append "UTC" inline. |
| `status` | Map API status values to user-friendly labels (see table below). |

### Timestamp Field Semantics for Orders (do NOT confuse)

| Field | Meaning | Use for |
|-------|---------|---------|
| `delivery_time` | **Delivery / Expiry date** — when the product matures | "Delivery date", "Expiry date" — **always use this field** |
| `create_time` | Order creation time | "Created at" |
| `complete_time` | Order completion time | "Completed at" |

> **Critical**: When displaying "delivery date" / "expiry date", always use **`delivery_time`**. The order response has only these 3 timestamp fields.

### Order Status Display Mapping

| API `status` value | Display label |
|-------------------|---------------|
| `INIT` | Pending |
| `SETTLEMENT_SUCCESS` | Settled |
| `SETTLEMENT_PROCESSING` | Settling |
| `CANCELED` | Canceled |
| `FAILED` | Failed |
| `REFUND_SUCCESS` | Early Redemption (Completed) |
| `REFUND_PROCESSING` | Early Redemption (Processing) |
| `REFUND_FAILED` | Early Redemption (Failed) |

> **Important**: `REFUND_*` statuses represent **early redemption** (user cancelled before delivery), NOT a refund. Always display as "Early Redemption", never as "Refund". Early-redeemed orders have zero yield.

---

## Workflow: Case 1 — Browse Dual Product List

### Step 1: Fetch plans

Call `cex_earn_list_dual_investment_plans` to get available plans.

### Step 2: Group and present

Group results by `type`:
- **Call (Sell High)**: user invests crypto, target price above current price
- **Put (Buy Low)**: user invests stablecoins, target price below current price

## Workflow: Case 3 — Product Details

### Step 1: Fetch plans by currency

Call `cex_earn_list_dual_investment_plans` to get all plans, then filter results locally by currency (e.g. `BTC`).

### Step 2: Filter by type

- "sell high" → filter `type=call` (user invests the crypto itself)
- "buy low" → filter `type=put` (user invests stablecoins)

### Step 3: Present product details

Display:
- Lock period (`invest_days`, integer — display as whole number, no decimals) / delivery date **(UTC)** — `delivery_timest` is a Unix timestamp, format as `yyyy-MM-dd` in UTC+0
- Available target prices and corresponding APYs (`apy_display × 100`%)

> **Note**: If user asks about minimum investment amount, do NOT return min amount data. Instead, present the matching plan details (target prices, APY, delivery date, etc.) from the query results, and note: "Minimum investment amount is not available via API. Please check the Gate App or website for details."

## Workflow: Case 4 — Settlement Simulation

### Step 1: Fetch plan details

Call `cex_earn_list_dual_investment_plans` to get `apy_display`, `exercise_price`, `invest_days`.

> **Note**: `apy_display` is returned as a decimal (e.g. `0.85` means 85%). Display as `apy_display × 100` + `%`. Use the raw decimal in formulas.

### Step 2: Calculate settlement scenarios

**Sell High (Call)**:
- Settlement price ≥ target price → USDT payout = principal × target_price × (1 + apy_display/365 × days)
- Settlement price < target price → Crypto payout = principal × (1 + apy_display/365 × days)

**Buy Low (Put)**:
- Settlement price ≤ target price → Crypto payout = USDT_amount / target_price × (1 + apy_display/365 × days)
- Settlement price > target price → USDT payout = USDT_amount × (1 + apy_display/365 × days)

### Step 3: Present both scenarios

Show calculated amounts for the user's specific scenario, clearly labeled.

## Workflow: Case 5 — Position Summary (Ongoing)

### Step 1: Fetch ongoing orders

Call `cex_earn_list_dual_orders` with `page=1`, `limit=100` to get active (not yet delivered) orders.

> **Critical**: You MUST complete ALL pagination (loop: increment `page` until returned rows < `limit`) before presenting results. Do NOT answer based on partial data.

### Step 2: Fetch balance overview

Call `cex_earn_list_dual_balance` to get total dual investment asset summary.

### Step 3: Present combined summary

Derive type from `invest_currency`: crypto (BTC, ETH, etc.) → Sell High; stablecoin (USDT) → Buy Low.

Display:
- `invest_currency`/`exercise_currency` (coin pair), type, `invest_amount`, `exercise_price` (target price), `apy_display × 100`%, `delivery_time` → delivery date (UTC)
- Total locked amount from balance

> **Note**: `delivery_time` is a Unix timestamp (seconds). Format as **`yyyy-MM-dd`** in UTC+0 for display. Do NOT display `settlement_price` for ongoing orders — it is only meaningful for settled orders.

## Workflow: Case 6 — Settlement Records

### Step 1: Parse time range from user query

Extract the time reference from the user's message and convert to `from`/`to` **Unix timestamps in seconds** (UTC+0).

> **Critical**: You MUST calculate the correct `from` and `to` timestamps before calling the API. Do NOT ignore the time range and return the most recent order instead.

**Calculation examples** (assuming today is 2026-03-11):

| User says | from (Unix seconds) | to (Unix seconds) |
|-----------|--------------------|--------------------|
| "last month" | `2026-02-01 00:00:00 UTC` → 1738368000 | `2026-02-28 23:59:59 UTC` → 1741046399 |
| "last week" | Monday 00:00:00 UTC of last week | Sunday 23:59:59 UTC of last week |
| "yesterday" | yesterday 00:00:00 UTC | yesterday 23:59:59 UTC |
| "recent" / no time specified | omit `from`/`to` (return recent orders) |

**Key rules**:
- `from` = start of the period, `to` = end of the period, both as **integer seconds since epoch**
- Always use **UTC+0** for calculation
- Double-check month boundaries (e.g. Feb has 28/29 days)

### Step 2: Fetch ALL matching orders (with pagination)

Call `cex_earn_list_dual_orders` with `from`, `to`, `page=1`, `limit=100`.

> **Critical**: You MUST complete ALL pagination before drawing any conclusions. Do NOT answer the user based on partial data.

Pagination loop:
1. Set `page=1`, `limit=100`
2. Call `cex_earn_list_dual_orders(from, to, page, limit)`
3. Collect all returned rows into a result set
4. If returned rows == `limit` (100) → increment `page`, go to step 2
5. If returned rows < `limit` → all data fetched, proceed to Step 3

### Step 3: Filter by coin (if specified)

After ALL pages are fetched, if the user mentions a specific coin (e.g. "BTC"), filter the **complete** result set locally — check if `invest_currency` or `exercise_currency` matches the coin.

### Step 4: Handle result count

- **0 results**: "No settled dual investment orders found in this time range."
- **1 result**: Directly present the settlement outcome.
- **Multiple results**: List all matching orders in a summary table: "Found {N} settled orders matching your criteria. Here are the details:" and present all of them.

### Step 5: Interpret settlement outcomes

Derive type from `invest_currency`: crypto → Sell High; stablecoin → Buy Low.

**Sell-High (Call)** (invest_currency is crypto):
- `settlement_price` ≥ `exercise_price` → "Successfully sold at target price, received {settlement_amount} {settlement_currency} (USDT)"
- `settlement_price` < `exercise_price` → "Target price not reached, got back {settlement_amount} {settlement_currency} (crypto) + interest"

**Buy-Low (Put)** (invest_currency is stablecoin):
- `settlement_price` ≤ `exercise_price` → "Successfully bought at target price, received {settlement_amount} {settlement_currency} (crypto)"
- `settlement_price` > `exercise_price` → "Target price not reached, got back {settlement_amount} {settlement_currency} (USDT) + interest"

### Step 6: Present all data

Return all queried data including `settlement_currency`, `settlement_amount`, `settlement_price`, `apy_settlement`. `delivery_time` formatted as `yyyy-MM-dd` in UTC+0.

## Report Template

### Product Listing (Cases 1, 3)

```
Dual Investment Plans on Gate {for {coin}}

Call (Sell High) Plans:
| # | Instrument | Target Price | Period | APY | Delivery (UTC) |
|---|-----------|--------------|--------|-----|----------------|
| 1 | {instrument_name} | {exercise_price} USDT | {invest_days} days | {apy_display × 100}% | {delivery_timest → yyyy-MM-dd} |

Put (Buy Low) Plans:
| # | Instrument | Target Price | Period | APY | Delivery (UTC) |
|---|-----------|--------------|--------|-----|----------------|
| 1 | {instrument_name} | {exercise_price} USDT | {invest_days} days | {apy_display × 100}% | {delivery_timest → yyyy-MM-dd} |

This information is for reference only and does not constitute investment advice.
Dual investment is interest-guaranteed but not principal-protected.
```

### Settlement Simulation (Case 4)

```
Settlement Simulation for {instrument_name} ({type})

Investment: {amount} {invest_currency}
Target Price: {exercise_price} USDT
Period: {invest_days} days
APY: {apy_display × 100}%

Scenario A — {condition_A}:
  → Receive: {payout_A} {currency_A}

Scenario B — {condition_B}:
  → Receive: {payout_B} {currency_B}

Dual investment is not principal-protected. Settlement currency depends on market price at delivery.
```

### Ongoing Positions (Case 5)

```
Your Ongoing Dual Investments

| # | Coin Pair | Type | Invested | Target Price | APY | Delivery (UTC) |
|---|-----------|------|----------|--------------|-----|----------------|
| 1 | {invest_currency}/{exercise_currency} | {Sell-High/Buy-Low} | {invest_amount} {invest_currency} | {exercise_price} | {apy_display × 100}% | {delivery_time → yyyy-MM-dd} |

Total Locked: {balance summary from cex_earn_list_dual_balance}

Dual investment is not principal-protected. Orders cannot be cancelled once placed.
```

### Settlement Records (Case 6)

```
Your Settled Dual Orders

| # | Coin Pair | Type | Invested | Target Price | Settlement Price | Delivery (UTC) | Result | Received | Realized APY |
|---|-----------|------|----------|--------------|------------------|----------------|--------|----------|--------------|
| 1 | {invest_currency}/{exercise_currency} | {Sell-High/Buy-Low} | {invest_amount} {invest_currency} | {exercise_price} | {settlement_price} | {delivery_time → yyyy-MM-dd} | {Hit/Miss} | {settlement_amount} {settlement_currency} | {apy_settlement × 100}% |

Note: apy_display / apy_settlement are decimals — multiply by 100 before appending %.
All timestamp fields (delivery_time, create_time, complete_time) must be formatted as `yyyy-MM-dd` in UTC+0.
Settlement rule: Principal + interest are always received; settlement currency depends on whether the target price was reached.
```
