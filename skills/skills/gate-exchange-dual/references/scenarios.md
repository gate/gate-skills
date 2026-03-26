# Gate Exchange Dual Investment — Scenarios & Prompt Examples (15 Cases)

## Scenario 1: Browse Dual Product List

**Context**: User wants to explore available dual investment products.

**Prompt Examples**:
- "What dual investment plans does Gate offer?"
- "What sell-high and buy-low products are available?"
- "Show me all dual currency products"
- "What dual investment options do you have?"

**Expected Behavior**:
1. Call `cex_earn_list_dual_investment_plans()` to get the list
2. Group results by type: Call (Sell High) and Put (Buy Low)
3. Display as comparison table. APY display as `apy_display × 100`%
4. Append risk disclaimer

---

## Scenario 3: Product Details

**Context**: User wants to know the terms and details for a specific coin's dual product.

**Prompt Examples**:
- "I want to sell-high BTC, what's the minimum?"
- "What's the minimum for ETH sell-high dual?"
- "What are the terms and target prices for BTC sell-high?"

**Expected Behavior**:
1. Call `cex_earn_list_dual_investment_plans()` to get all plans, then filter locally by currency (e.g. `BTC`)
2. Filter for matching type: sell-high → `call`, buy-low → `put`
3. Display: target prices available, APY (`apy_display × 100`%)
4. Do NOT display timestamp fields to the user
5. If sell-high: note user needs to invest the crypto itself (e.g. BTC)
6. If buy-low: note user needs to invest stablecoins (e.g. USDT)
7. If user asks about minimum investment amount: do NOT return min amount data. Still present the matching plan details (target prices, APY, delivery date, etc.) from the query results, and note: "Minimum investment amount is not available via API. Please check the Gate App or website for details."

---

## Scenario 4: Settlement Simulation

**Context**: User wants to understand what happens at delivery under different price scenarios.

**Prompt Examples**:
- "BTC is at 60000, I pick sell-high target 62000, what if it goes to 65000?"
- "If I buy low ETH at target 3000 and it drops to 2800, what do I get?"
- "Calculate the settlement return for this dual plan"
- "Simulate the settlement for this dual plan"

**Expected Behavior**:
1. Call `cex_earn_list_dual_investment_plans()` to get plan details (`apy_display`, target price)
2. Display APY as `apy_display × 100`%. **NEVER** display the raw value directly as a percentage. Use raw `apy_display` value in formulas
3. Calculate settlement scenarios:
   - **Sell High**: settlement price ≥ target → USDT payout = principal × target price × (1 + apy_display/365 × days); settlement price < target → crypto + interest
   - **Buy Low**: settlement price ≤ target → crypto payout = USDT amount / target price × (1 + apy_display/365 × days); settlement price > target → USDT + interest
4. Present both scenarios clearly with calculated amounts
5. Append risk disclaimer

---

## Scenario 5: Position Summary (Ongoing)

**Context**: User wants to see a summary of their ongoing (not yet delivered) dual investments.

**Prompt Examples**:
- "How much do I have locked in dual investment? Which ones haven't matured?"
- "Show my ongoing dual investments"
- "Dual position summary"
- "What dual orders are still active?"

**Expected Behavior**:
1. Call `cex_earn_list_dual_orders(page=1, limit=100)` to get active orders. **Must complete ALL pagination** (loop: increment `page` until returned rows < `limit`) before proceeding — do NOT answer based on partial data
2. Call `cex_earn_list_dual_balance()` to get total asset overview
3. Derive type from `invest_currency`: crypto (BTC, ETH, etc.) → Sell High; stablecoin (USDT) → Buy Low
4. Show: `invest_currency`/`exercise_currency` (coin pair), type, `invest_amount`, `exercise_price` (target price), APY (`apy_display × 100`%)
5. Show total locked amount from balance
6. Do NOT display `settlement_price` for ongoing orders. Do NOT display timestamp fields

---

## Scenario 6: Settlement Records

**Context**: User wants to check the settlement result of a completed dual investment order within a specific time range.

**Prompt Examples**:
- "My BTC dual order from last month — did I get crypto or USDT?"
- "Show my settled dual orders"
- "Dual settlement records"
- "What happened with my ETH dual that expired last week?"

**Expected Behavior**:
1. Parse time reference from user query (e.g. "last month" → calculate exact `from`/`to` Unix timestamps in seconds for that calendar month in UTC+0). **Must** pass correct `from`/`to` to the API — do NOT ignore the time range or return the most recent order instead
2. Call `cex_earn_list_dual_orders(from, to, page=1, limit=100)`. **Must complete ALL pagination** (loop until returned rows < limit) before proceeding — do NOT answer based on partial data
3. After all pages are collected, if user mentions a coin (e.g. "BTC"), filter the **complete** result set locally — check if `invest_currency` or `exercise_currency` matches
4. If multiple matching orders found: list all in a table, present all results to the user
5. If no matching orders found: respond "No settled dual investment orders found in this time range."
6. Derive type from `invest_currency`: crypto → Sell High; stablecoin → Buy Low. For each settled order, explain the outcome:
   - Sell-high (invest_currency is crypto): settlement_price ≥ exercise_price → "Successfully sold, received USDT"; < exercise_price → "Got back crypto + interest"
   - Buy-low (invest_currency is stablecoin): settlement_price ≤ exercise_price → "Successfully bought crypto"; > exercise_price → "Got back USDT + interest"
7. Display: `settlement_currency`, `settlement_amount`, `settlement_price`, Realized APY (`apy_settlement × 100`%). Do NOT display timestamp fields
8. `apy_display`, `apy_settlement` are raw values (NOT percentages) — multiply by 100 before appending `%`. E.g. `2.7814` → `278.14%`

---

## Scenario 7: Sell-High Order (Invest Crypto)

**Context**: User wants to place a sell-high (call) dual investment order.

**Prompt Examples**:
- "Sell high 0.1 BTC, target price 65000, 7-day term"
- "Sell high 0.1 BTC, target price 65000, 7-day term"
- "Sell high 0.5 ETH with target price 4000"
- "Place a sell-high dual with BTC"

**Expected Behavior**:
1. Parse user intent: extract coin (BTC), amount (0.1), target price (65000). Ask for missing params.
2. Call `cex_earn_list_dual_investment_plans()` to find matching sell-high (type=call) plan for BTC with target price ~65000.
3. If matching plan found, present order confirmation with full details: type, amount, target price, APY (`apy_display × 100`%), and both settlement scenarios with calculated amounts.
4. **Wait for explicit user confirmation before proceeding.**
5. On confirmation, call `cex_earn_place_dual_order(plan_id, amount)`.
6. Success: "Order submitted! Your subscribed dual investment product: BTC (target price 65000, APY X%)."
7. Failure: display error. If compliance error, route to Cases 15–17.

---

## Scenario 8: Buy-Low Order (Invest Stablecoin)

**Context**: User wants to place a buy-low (put) dual investment order.

**Prompt Examples**:
- "Buy low BTC with 1000 USDT, target price 58000, 7-day term"
- "Buy low BTC with 1000 USDT, target price 58000, 7-day term"
- "Buy low ETH with 500 USDT, target 3000"
- "Place a buy-low dual on BTC with USDT"

**Expected Behavior**:
1. Parse user intent: extract coin (BTC), USDT amount (1000), target price (58000). Ask for missing params.
2. Call `cex_earn_list_dual_investment_plans()` to find matching buy-low (type=put) plan for BTC with target price ~58000.
3. If matching plan found, present order confirmation with full details and both settlement scenarios.
4. **Wait for explicit user confirmation before proceeding.**
5. On confirmation, call `cex_earn_place_dual_order(plan_id, amount)`.
6. Success: "Order submitted! Your subscribed dual investment product: BTC (target price 58000, APY X%)."
7. Failure: display error. If compliance error, route to Cases 15–17.

---

## Scenario 9: Amount Eligibility for Order

**Context**: User asks if their amount is enough to place a dual investment order.

**Prompt Examples**:
- "I want to buy-low 5000U of ETH, can I?"
- "I want to buy-low 5000U of ETH, can I?"
- "Can I invest 0.001 BTC in dual?"
- "Is 5000U enough to buy dual?"

**Expected Behavior**:
1. Call `cex_earn_list_dual_investment_plans()` to get plans for the target coin and type
2. Compare user's amount against plan's `min_amount`
3. If amount meets minimum: inform the user and offer to proceed with order placement (Case 7 or 8 workflow)
4. If amount < `min_amount`: "Insufficient balance. The minimum subscription amount is {min_amount} {currency}."
5. If no matching plans: "No dual investment plans available for this coin at the moment."

---

## Scenario 10: Minimum Purchase Check for Order

**Context**: User asks about the minimum amount needed to place a dual investment order.

**Prompt Examples**:
- "I only have 50U, can I buy dual?"
- "I only have 50U, can I buy dual?"
- "What's the minimum to buy dual investment?"
- "Is 50U enough for dual?"

**Expected Behavior**:
1. Call `cex_earn_list_dual_investment_plans()` to get available plans
2. List minimum investment amounts for available plans
3. If user's amount < all minimums: "The minimum subscription amount for current dual investment products is {min_amount} {currency}. Your amount is below the minimum."
4. If user's amount meets some plans: list those eligible plans and offer to proceed

---

## Scenario 11: Settlement Result Query

**Context**: User wants to check the result of a recently delivered dual order.

**Prompt Examples**:
- "My ETH dual matured yesterday, did I get crypto or USDT?"
- "What did I receive from my expired BTC dual?"
- "Settlement result query"
- "My dual order matured, what's the outcome?"

**Expected Behavior**:
1. Call `cex_earn_list_dual_orders(from, to, page=1, limit=100)` to find settled orders. **Must complete ALL pagination** (loop until returned rows < limit) before proceeding
2. Derive type from `invest_currency`: crypto → Sell High; stablecoin → Buy Low. Explain settlement outcome:
   - Sell-high (invest_currency is crypto): settlement_price ≥ exercise_price → received USDT; < exercise_price → received crypto + interest
   - Buy-low (invest_currency is stablecoin): settlement_price ≤ exercise_price → received crypto; > exercise_price → received USDT + interest
3. Display: `settlement_currency`, `settlement_amount`, Realized APY (`apy_settlement × 100`%), and note that both scenarios include principal + interest
4. `apy_display`, `apy_settlement` are raw values (NOT percentages) — multiply by 100 before appending `%`. E.g. `2.7814` → `278.14%`
5. Do NOT display timestamp fields to the user
6. Append risk disclaimer

---

## Scenario 12: Dual Asset Briefing

**Context**: User wants to know their total dual investment locked amount.

**Prompt Examples**:
- "How much is locked in my dual investment?"
- "What's my dual investment balance?"
- "Total dual investment assets"
- "How much do I have in dual investments?"

**Expected Behavior**:
1. Call `cex_earn_list_dual_balance()` to get dual investment assets
2. Display total holdings in USDT and BTC, total interest earned
3. Append risk disclaimer

---

## Scenario 13: Currency Conversion Risk

**Context**: User asks about principal safety and risks of dual investment.

**Prompt Examples**:
- "Will I lose principal with dual investment?"
- "Is dual investment safe? Will I lose money?"
- "Is it principal-protected?"
- "What are the risks of dual investment?"

**Expected Behavior**:
1. No API call needed — answer from Domain Knowledge
2. Explain: Interest-guaranteed, not principal-protected. Principal + interest are always received, but settlement currency may change
3. Sell-high risk: may get back crypto instead of USDT if price doesn't reach target
4. Buy-low risk: may get back USDT instead of crypto if price stays above target
5. The closer the target price to current price, the higher the yield but also higher conversion probability

---

## Scenario 14: Missed Gains Explanation

**Context**: User placed a sell-high order and the price surged beyond the target price, feeling they "lost money".

**Prompt Examples**:
- "I sold high on BTC and the price surged a lot, did I lose money?"
- "I sold high and BTC mooned, did I lose?"
- "What about missed gains?"
- "My sell-high settled but the price went much higher"

**Expected Behavior**:
1. No API call needed — answer from Domain Knowledge
2. Explain: When settlement price ≥ target price, you successfully sold at target price and received USDT, but missed gains above the target
3. When settlement price < target price, you got back crypto + interest
4. This product suits sideways or mildly bullish markets; in strong bull markets you may "miss out" on excess gains
5. Emphasize this is not a loss of principal — you received the agreed payout at the target price

---

## Scenario 15: Restricted Region

**Context**: User asks about regional restrictions, or a `cex_earn_place_dual_order` call returns a region restriction error.

**Prompt Examples**:
- "I'm in [region], can I buy dual investment?"
- "I'm in [region], can I buy dual investment?"
- "Which regions support dual investment?"
- "Which regions support dual investment?"

**Expected Behavior**:
1. If triggered by user question (no order attempt): respond with compliance explanation.
2. If triggered by `cex_earn_place_dual_order` error response: explain the restriction.
3. Response: "Dual investment requires meeting the platform's compliance requirements. Your region is currently not supported for this product. If you have any questions, please contact Gate support."

---

## Scenario 17: General Compliance Failure

**Context**: User's order fails due to compliance checks (OES, institutional/enterprise account, risk control blocklist, etc.).

**Prompt Examples**:
- "I tried to subscribe dual but it failed with a compliance error."
- "I tried to subscribe dual but it failed with a compliance error."
- "Dual subscription failed, what happened?"

**Expected Behavior**:
1. Triggered by `cex_earn_place_dual_order` returning a compliance error.
2. Based on the specific error, respond accordingly:
   - OES / institutional / enterprise user: "Your account type does not currently support dual investment products."
   - Risk control blocklist: "Your account is currently unable to operate this product. Please contact Gate support for details."
   - Other compliance errors: display the error description returned by the API.
3. Do NOT retry the order — inform the user and suggest contacting Gate support if needed.
