# Subscription & Order Placement — Cases 7, 8, 9, 10, 15, 17

Sell-high / buy-low order placement, amount validation, and compliance handling.

## Available Tools

| Tool | Auth | Description |
|------|------|-------------|
| `cex_earn_list_dual_investment_plans` | Yes | List dual investment plans (optional param: plan_id) |
| `cex_earn_place_dual_order` | Yes | Place a dual investment order. Params: `plan_id` (required, string), `amount` (required, string), `text` (optional comment). |

### Parameters: `cex_earn_place_dual_order`

| Param | Required | Type | Description |
|-------|----------|------|-------------|
| `plan_id` | **Yes** | string | Plan ID from `cex_earn_list_dual_investment_plans` |
| `amount` | **Yes** | string | Investment amount |
| `text` | No | string | Custom order ID. Must start with `t-`; excluding the `t-` prefix, max 28 bytes; only digits, letters, underscore (`_`), hyphen (`-`), or dot (`.`) allowed. Example: `t-my_order.001` |

---

## Workflow: Case 7 — Sell-High Order (Invest Crypto)

User wants to sell-high with a crypto asset (e.g. "Sell high 0.1 BTC, target price 65000, 7-day term").

### Step 1: Parse user intent

Extract from the user's message:
- **Coin**: The crypto to invest (e.g. BTC, ETH)
- **Amount**: How much to invest (e.g. 0.1)
- **Target price**: Desired exercise price (e.g. 65000)

If any required parameter is missing, ask the user to provide it.

### Step 2: Find matching plan

Call `cex_earn_list_dual_investment_plans` to get all plans.

Filter locally:
- `type` = `call` (Sell High)
- `exercise_currency` matches the user's coin (e.g. BTC)
- `exercise_price` matches or is closest to the user's target price

If no matching plan found, list available sell-high plans for that coin and ask the user to choose.

### Step 3: Transform APY and confirm with user (MANDATORY)

**First**: compute display APY = `apy_display × 100` + `%`. E.g. raw `2.7814` → display `278.14%`.

Before placing the order, present the full order details and **require explicit confirmation**:

```
Order Confirmation:
- Type: Sell High (Call)
- Invest: {amount} {coin}
- Target Price: {exercise_price} USDT
- APY: {apy_display × 100}%

Settlement scenarios:
  • Settlement price ≥ {exercise_price} → Receive {amount × exercise_price × (1 + apy/365 × days)} USDT
  • Settlement price ＜ {exercise_price} → Receive {amount × (1 + apy/365 × days)} {coin}

⚠️ Dual investment is NOT principal-protected. Settlement currency depends on market price at delivery.
Do you confirm this order? (Yes/No)
```

> **Critical**: NEVER call `cex_earn_place_dual_order` without explicit user confirmation.

### Step 4: Place order

If user confirms, call `cex_earn_place_dual_order` with:
- `plan_id`: the matched plan's ID (as string)
- `amount`: the user's investment amount (as string)

### Step 5: Handle response

- **Success** (⚠️ `apy_display` is a raw value like `2.7814` which means **278.14%**. You MUST compute `apy_display × 100` for display):

```
Order submitted.

Your subscribed dual investment product: {coin} Sell High, target price {exercise_price} USDT, APY {apy_display × 100}%.
At delivery: if settlement price ≥ {exercise_price}, you will receive USDT; if settlement price < {exercise_price}, you will receive {coin}. Both scenarios include principal and corresponding yield.
```

- **Failure**: Display the error. If compliance-related, route to Cases 15–17.

---

## Workflow: Case 8 — Buy-Low Order (Invest Stablecoin)

User wants to buy-low with stablecoins (e.g. "Buy low BTC with 1000 USDT, target price 58000, 7-day term").

### Step 1: Parse user intent

Extract:
- **Coin**: The crypto to buy (e.g. BTC, ETH)
- **Amount**: USDT amount to invest (e.g. 1000)
- **Target price**: Desired exercise price (e.g. 58000)

If any required parameter is missing, ask the user to provide it.

### Step 2: Find matching plan

Call `cex_earn_list_dual_investment_plans` to get all plans.

Filter locally:
- `type` = `put` (Buy Low)
- `exercise_currency` matches the user's target coin (e.g. BTC)
- `exercise_price` matches or is closest to the user's target price

If no matching plan found, list available buy-low plans for that coin and ask the user to choose.

### Step 3: Transform APY and confirm with user (MANDATORY)

**First**: compute display APY = `apy_display × 100` + `%`. E.g. raw `2.7814` → display `278.14%`.

```
Order Confirmation:
- Type: Buy Low (Put)
- Invest: {amount} USDT
- Target Coin: {coin}
- Target Price: {exercise_price} USDT
- APY: {apy_display × 100}%

Settlement scenarios:
  • Settlement price ≤ {exercise_price} → Receive {amount / exercise_price × (1 + apy/365 × days)} {coin}
  • Settlement price ＞ {exercise_price} → Receive {amount × (1 + apy/365 × days)} USDT

⚠️ Dual investment is NOT principal-protected. Settlement currency depends on market price at delivery.
Do you confirm this order? (Yes/No)
```

> **Critical**: NEVER call `cex_earn_place_dual_order` without explicit user confirmation.

### Step 4: Place order

If user confirms, call `cex_earn_place_dual_order` with:
- `plan_id`: the matched plan's ID (as string)
- `amount`: the user's investment amount (as string)

### Step 5: Handle response

- **Success** (⚠️ `apy_display` is a raw value like `2.7814` which means **278.14%**. You MUST compute `apy_display × 100` for display):

```
Order submitted.

Your subscribed dual investment product: {coin} Buy Low, target price {exercise_price} USDT, APY {apy_display × 100}%.
At delivery: if settlement price ≤ {exercise_price}, you will receive {coin}; if settlement price > {exercise_price}, you will receive USDT. Both scenarios include principal and corresponding yield.
```

- **Failure**: Display the error. If compliance-related, route to Cases 15–17.

---

## Workflow: Case 9 — Amount Eligibility Check

User asks if their amount is enough (e.g. "I want to buy-low 5000U of ETH, can I?").

### Step 1: Fetch plans

Call `cex_earn_list_dual_investment_plans` to get available plans for the target coin and type.

### Step 2: Check eligibility

Compare the user's intended amount against the plan's `min_amount` and product availability.

- If matching plans exist and amount meets minimum: proceed to Case 7 or 8 workflow.
- If amount < `min_amount`: inform the user of the minimum required amount.
- If no matching plans: "No matching dual investment plans available for {coin} at the moment."

---

## Workflow: Case 10 — Minimum Purchase Check

User asks about the minimum amount (e.g. "I only have 50U, can I buy dual?").

### Step 1: Fetch plans

Call `cex_earn_list_dual_investment_plans` to get available plans.

### Step 2: Present minimum amounts

List minimum investment amounts for available plans. If the user's amount is below all minimums, inform them:

"The minimum subscription amount for current dual investment products is {min_amount} {currency}. Your amount does not meet the minimum requirement."

If the user's amount meets one or more plan's minimum, list those eligible plans.

---

## Compliance Handling — Cases 15, 17

These cases handle compliance errors returned by `cex_earn_place_dual_order`, or user questions about restrictions.

### Case 15: Restricted Region

**Trigger**: User asks about region restrictions, or `cex_earn_place_dual_order` returns a region restriction error.

**Response**: "Dual investment requires meeting the platform's compliance requirements. Your region is currently not supported for this product. If you have any questions, please contact Gate support."

### Case 17: General Compliance Failure

**Trigger**: `cex_earn_place_dual_order` returns a compliance error (OES, institutional/enterprise account, risk control blocklist, etc.).

**Response**: Based on the specific error code/message:
- OES / institutional / enterprise user: "Your account type does not currently support dual investment products."
- Risk control blocklist: "Your account is currently unable to operate this product. Please contact Gate support for details."
- Other compliance errors: Display the error description returned by the API.

---

## Report Template

### Order Confirmation — Sell High (Case 7)

```
Order Confirmation:
- Type: Sell High (Call)
- Invest: {amount} {coin}
- Target Price: {exercise_price} USDT
- APY: {apy_display × 100}%

Settlement scenarios:
  • Settlement price ≥ {exercise_price} → Receive {amount × exercise_price × (1 + apy/365 × days)} USDT
  • Settlement price ＜ {exercise_price} → Receive {amount × (1 + apy/365 × days)} {coin}

⚠️ Dual investment is NOT principal-protected. Settlement currency depends on market price at delivery.
Do you confirm this order? (Yes/No)
```

### Order Confirmation — Buy Low (Case 8)

```
Order Confirmation:
- Type: Buy Low (Put)
- Invest: {amount} USDT
- Target Coin: {coin}
- Target Price: {exercise_price} USDT
- APY: {apy_display × 100}%

Settlement scenarios:
  • Settlement price ≤ {exercise_price} → Receive {amount / exercise_price × (1 + apy/365 × days)} {coin}
  • Settlement price ＞ {exercise_price} → Receive {amount × (1 + apy/365 × days)} USDT

⚠️ Dual investment is NOT principal-protected. Settlement currency depends on market price at delivery.
Do you confirm this order? (Yes/No)
```

### Order Success

```
Order submitted.

Your subscribed dual investment product: {coin} {Sell High/Buy Low}, target price {exercise_price} USDT, APY {apy_display × 100}%.
At delivery: {settlement scenario A}; {settlement scenario B}. Both scenarios include principal and corresponding yield.
```

---

## Global Data Formatting Rules (apply to ALL dual tools)

| Field category | Rule |
|---------------|------|
| **Any APY/rate field** (`apy`, `apy_display`, `apyDisplay`, etc.) | Raw value — **NOT a percentage**. **MUST multiply by 100** then append `%`. Common mistake: `1.1343` → **113.43%** (NOT `1.13%`), `16.133` → **1613.3%** (NOT `16.13%`), `0.0619` → **6.19%**. **Sanity check**: if any displayed APY is a single or low-double digit percentage, you forgot ×100. |
| All timestamps (`delivery_timest` for plans) | Unix timestamps (seconds). Do NOT convert to dates or display to the user in any form. Do NOT use as section headers or grouping labels. Omit completely from user-facing output. |
