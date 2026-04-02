# Gate Auto-Invest — Scenario Index

This document lists all auto-invest scenarios in validator-friendly form (`## Scenario N:`). Detailed steps and response templates live in `autoinvest-plans.md`, `autoinvest-compliance.md`, or `SKILL.md` as noted under each scenario.

## Scenario 1: Single-target recurring buy (create)

**Context**: User specifies invest currency, amount, cadence, single target (e.g. BTC).

**Prompt Examples**:
- "Invest 100 USDT weekly into BTC—create a plan."
- "DCA 50 USDT every day into ETH."

**Expected Behavior**:
1. Validate amount range via `cex_earn_get_auto_invest_min_amount` and `cex_earn_list_auto_invest_config`
2. Check spot balance via `cex_spot_get_spot_accounts`
3. Set defaults if not provided (execution time, fund source, fund flow)
4. Show **Action Draft** and obtain explicit user confirmation before any write (`SKILL.md` → **Execution**, **Safety Rules**)
5. Call `cex_earn_create_auto_invest_plan` with parsed params
6. On success, restate plan summary; full workflow and response templates in `autoinvest-plans.md` → Scenario 1

---

## Scenario 2: Multi-target create

**Context**: User splits one periodic amount across multiple targets.

**Prompt Examples**:
- "500 USDT monthly into BTC and ETH."

**Expected Behavior**:
1. Validate amount range for all target coins
2. Verify total invest currency balance
3. Set defaults for optional parameters
4. Show **Action Draft** and obtain explicit user confirmation before any write (`SKILL.md` → **Safety Rules**)
5. Call `cex_earn_create_auto_invest_plan` with multiple targets; details in `autoinvest-plans.md` → Scenario 2

---

## Scenario 3: Check balance then create

**Context**: User asks to verify funds before creating.

**Prompt Examples**:
- "Check if I have enough USDT for 200 biweekly into ETH, then create if ok."

**Expected Behavior**:
1. Check balance via `cex_spot_get_spot_accounts`
2. If insufficient → do not create; explain shortfall
3. If sufficient → confirm once, then create (see `autoinvest-plans.md` → Scenario 3)

---

## Scenario 4: Create with auto Simple Earn after buy

**Context**: User wants purchased assets moved to Simple Earn when product supports it.

**Prompt Examples**:
- "Weekly 50 USDT into BTC, auto-send BTC to Simple Earn."

**Expected Behavior**:
1. Pass product flags via create tool when MCP exposes them
2. If unclear whether feature exists, say so and offer standard create; full steps in `autoinvest-plans.md` → Scenario 4

---

## Scenario 5: Named plan + frequency

**Context**: User gives a display name and schedule.

**Prompt Examples**:
- "Name it 'BTC dip', 20 USDT daily into BTC."

**Expected Behavior**:
1. Include plan name + daily cadence + amount in create payload per MCP schema (`autoinvest-plans.md` → Scenario 5)

---

## Scenario 6: Vague intent (no write yet)

**Context**: User only says "auto-invest" or similar vague terms.

**Prompt Examples**:
- "I want DCA."
- "Auto-invest wealth management."

**Expected Behavior**:
1. No write call
2. Suggest defaults (USDT → BTC), ask for amount, targets, cadence (`autoinvest-plans.md` → Scenario 6)

---

## Scenario 7: Partial parameters

**Context**: User gives amount only or target only.

**Prompt Examples**:
- "DCA 100 USDT."
- "DCA BTC."

**Expected Behavior**:
1. Ask one concise clarifying question for missing target, invest currency, or cadence (`autoinvest-plans.md` → Scenario 7)

---

## Scenario 8: Plan detail (single plan)

**Context**: User asks for one plan's metadata.

**Prompt Examples**:
- "Show my ETH DCA plan details."

**Expected Behavior**:
1. Call `cex_earn_list_auto_invest_plans` if needed to resolve plan id
2. Call `cex_earn_get_auto_invest_plan_detail`
3. Present invest currency, targets, amount, cadence, flags, execution counts (`autoinvest-plans.md` → Scenario 8)

---

## Scenario 9: Stop plan

**Context**: User terminates a plan.

**Prompt Examples**:
- "Stop my ETH auto-invest."

**Expected Behavior**:
1. If no plan ID provided, call `cex_earn_list_auto_invest_plans` to query all plans
2. Match by plan name or ask user to specify; disambiguate duplicate names by plan `id`
3. Show **Action Draft** and end the turn; **do not** call `cex_earn_stop_auto_invest_plan` in that same assistant turn (`SKILL.md` → **Mandatory Confirmation for Write Operations**)
4. After the user's **next message** with explicit confirmation, call `cex_earn_stop_auto_invest_plan` (`autoinvest-plans.md` → Scenario 9)
5. Explain holdings remain in spot unless product states otherwise

---

## Scenario 10: Top-up (add position)

**Context**: One-off extra purchase on existing plan.

**Prompt Examples**:
- "Add another 100 USDT buy to my BTC DCA."
- "Add one more to my ETH-GT-GRIN auto-invest"
- "Add another buy to my DCA"

**Expected Behavior**:
1. If no plan ID provided, query all plans and match by name
2. Determine add position amount (use plan's periodic amount if not specified)
3. Check balance via `cex_spot_get_spot_accounts`
4. Confirm with user
5. Call `cex_earn_add_position_auto_invest_plan` EXACTLY ONCE (`autoinvest-plans.md` → Scenario 10)

---

## Scenario 11: Query Supported Coins

**Context**: User asks which coins support auto-invest.

**Prompt Examples**:
- "Which coins can I auto-invest in?"
- "What target coins does auto-invest support?"

**Expected Behavior**:
1. Call `cex_earn_list_auto_invest_coins`
2. Return list of all coins that support auto-invest (`SKILL.md` → Query Function Usage → Scenario 1)

---

## Scenario 12: Query Minimum Investment Amount

**Context**: User asks about minimum investment amount.

**Prompt Examples**:
- "What's the minimum amount per period for USDT auto-invest?"
- "What's the minimum amount when BTC is the investment currency?"

**Expected Behavior**:
1. Call `cex_earn_get_auto_invest_min_amount`
2. Specify investment currency (USDT or BTC) and target coins
3. Return minimum amount (`SKILL.md` → Query Function Usage → Scenario 2)

---

## Scenario 13: View Execution History

**Context**: User asks about plan execution records.

**Prompt Examples**:
- "How many times has my BTC auto-invest been executed recently?"
- "View the recent execution status of this plan"

**Expected Behavior**:
1. Call `cex_earn_list_auto_invest_plan_records` to view execution records
2. Call `cex_earn_list_auto_invest_orders` to view specific order details
3. Present execution count and latest execution info (`SKILL.md` → Query Function Usage → Scenario 3)

---

## Scenario 14: Plan Not Found

**Context**: No matching auto-invest plan found during query.

**Prompt Examples**:
- "Show my non-existent plan"

**Expected Behavior**:
1. Inform: "No matching auto-invest plan found. You can create a new auto-invest plan." (`SKILL.md` → Query Function Usage → Scenario 4)

---

## Scenario 15: Investment Currency Question

**Context**: User asks about which currencies can be used as investment currency.

**Prompt Examples**:
- "Can I use ETH as the investment currency?"
- "What currencies are supported for auto-invest?"

**Expected Behavior**:
1. Explain: "Only USDT or BTC are supported as investment currency (the currency deducted each period). Target coins can be other assets." (policy in `autoinvest-compliance.md`)

---

## Scenario 16: Fund Source Question

**Context**: User asks about fund sources.

**Prompt Examples**:
- "Does it take from Simple Earn?"
- "Where does the money come from?"

**Expected Behavior**:
1. Explain fund source options: `spot` (spot account, default) or `earn` (Simple Earn)
2. Explain fund flow options: `auto_invest` → spot account; `earn` → Simple Earn (`autoinvest-compliance.md`, `SKILL.md` → **Fund Flow**)

---

## Scenario Statistics

| Category | Scenario Count | Document |
|----------|----------------|----------|
| Plan Lifecycle | 10 | `autoinvest-plans.md` |
| Query | 4 | `SKILL.md` |
| Compliance | 2 | `autoinvest-compliance.md` |
| **Total** | **16** | - |
