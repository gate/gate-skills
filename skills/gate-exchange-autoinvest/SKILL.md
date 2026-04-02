---
name: gate-exchange-autoinvest
version: "2026.4.2-3"
updated: "2026-04-02"
description: The fast auto-invest function of Gate Exchange Earn. Use this skill whenever you need to create, update, stop, or top up invest plans and to query supported coins, minimum amounts, records, orders, and plan detail. Trigger phrases include "auto-invest", "DCA", "dollar cost averaging", "invest plan", or equivalent.
---

# gate-exchange-autoinvest

The fast auto-invest (DCA) function of Gate Exchange Earn, supporting create, update, stop plans, and query related information.

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [`exchange-runtime-rules.md`](../exchange-runtime-rules.md) first (mirror: [`exchange-runtime-rules.md` on GitHub](https://github.com/gate/gate-skills/blob/master/skills/exchange-runtime-rules.md)).
- **Only call MCP tools explicitly listed in this skill** (see **MCP tools** below: Auto-Invest Related Tools and Supporting Tools). Tools not documented here must NOT be called, even if they exist in the MCP server.

## Risk Disclaimer

**Digital Asset Trading Risk Statement**:
Digital asset trading carries significant risks. Prices are subject to high volatility and market manipulation. Past performance is not indicative of future results. This skill provides informational tools only and does not constitute investment advice. Users are solely responsible for their investment decisions. Only invest what you can afford to lose. For full risk disclosure, please visit Gate's official website.

## AI Interaction Data Flow

**Data Handling Notice**:
When you use this skill, your queries and account data are processed through AI systems to provide trading assistance. This includes:
- Your trading instructions and preferences
- Account balance and position information (read-only access)
- Historical trading records for context

**Important**:
- All data transmission is encrypted and follows Gate's privacy policy
- AI processes data in real-time; no long-term storage of your trading data by the AI
- You retain full control; AI only executes trades after your explicit confirmation
- For privacy details, see Gate's Privacy Policy

## Feature Modules

| Module | Description | Trigger Keywords |
|--------|-------------|------------------|
| **Plan Management** | Create, update, stop, and add position to auto-invest plans | `create DCA`, `auto-invest`, `stop plan`, `add to my DCA`, `dollar cost averaging` |
| **Information Query** | Query supported coins, minimum amounts, execution records, order details, and plan details | `min amount`, `execution history`, `records`, `plan detail` |

## Business Rules

### Investment Currency Restrictions

- **Only USDT or BTC supported** as investment currency (the currency deducted each period)
- Target coins can be other assets

### Create Plan Constraints

**Required Parameters**:
- Target coins to invest (asset list)
- Investment amount per period

**Optional Parameters** (with defaults):
- Investment time: Defaults to daily at 10:00 (can be customized)
- Fund source: Defaults to `spot` (spot account)
- Fund flow: Defaults to `auto_invest` (purchased assets remain in Spot account)

**Execution Time Restriction**:
- **Auto-invest only supports execution on the hour** (0-23 o'clock)
- `plan_period_hour` must be an integer from 0 to 23
- Minutes and seconds are not supported; all executions occur at :00
- ⚠️ **CRITICAL - Time Zone**: `plan_period_hour` uses **UTC time zone**
  - When user specifies local time (e.g., "10:00 AM Beijing time"), **convert to UTC** before passing to API
  - Example: Beijing 10:00 (UTC+8) → UTC 02:00 → set `plan_period_hour: 2`
  - **Fallback**: If system time zone cannot be detected, use user's specified hour directly
  - Always show both UTC and local time in confirmation (or note if time zone detection failed)
  - See `references/autoinvest-plans.md` → Time Zone Handling section for detailed conversion rules

**`plan_period_day` (create plans only)**:
- Required on create; value **must not be `0`**. Full workflow: `references/autoinvest-plans.md` → Workflow step 6.
- By **`plan_period_type`**:
  - **`monthly`**: Day of month **1–30**
  - **`weekly`** or **`biweekly`**: Weekday **1–7** (**1 = Monday**, **7 = Sunday**)
  - **`daily`**, **`hourly`**, or **`4-hourly`**: Use **`1`**

**Investment Amount Limits**:
- **Minimum amount**: Must be ≥ the value returned by `cex_earn_get_auto_invest_min_amount`
- **Maximum amount**: Must be ≤ the value returned by `cex_earn_list_auto_invest_config`
- Before creating a plan:
  1. Call `cex_earn_get_auto_invest_min_amount` to query the minimum amount
  2. Call `cex_earn_list_auto_invest_config` to query the maximum amount
  3. Validate that the user's input amount is within the valid range

**Target Coins Constraints** (for multi-target plans):
- **Maximum target coins**: A plan can have at most **10 target coins**
- **Minimum allocation per coin**: Each target coin must have at least **10% allocation** (ratio ≥ 10)
- Before creating a multi-target plan:
  1. Check that the number of target coins ≤ 10
  2. Check that each coin's ratio ≥ 10
  3. If validation fails, reject immediately with clear explanation

**Fund Flow (where purchased assets go)**:
After creating a plan, purchased assets will flow to one of two destinations based on the `fund_flow` parameter (API field: **post-purchase destination**):

| API `fund_flow` | Meaning (EN) | Typical Gate app label (localized; may vary) |
|-----------------|--------------|---------------------------------------------|
| `earn` | Simple Earn / flexible earn | Often labeled Simple Earn / flexible earn in English locales |
| `auto_invest` | Spot account (default) | Spot account |

- **`fund_flow: "earn"`** → Assets automatically transfer to **Simple Earn** to earn interest
- **`fund_flow: "auto_invest"`** → Assets remain in **Spot account** for manual management (default)

**Important**: 
- User should choose fund flow based on their investment strategy
- `earn` is recommended for passive income on accumulated assets
- `auto_invest` is recommended if user plans to trade or withdraw assets frequently
- When users refer to Simple Earn (flexible earn) or spot account in any language, map to `earn` or `auto_invest` respectively when calling MCP create/update
- Do not use angle brackets (`<` or `>`) in user-facing replies.

### After Stopping a Plan

- After stopping a plan, automatic deductions will cease
- Purchased assets typically remain in the spot account

### Next Purchase Time

- This function does not provide specific query for the next automatic purchase time
- For this information, please visit Gate App or website

## MCP tools

### Auto-Invest Related Tools (11 tools)

| # | Tool Name | Type | Function |
|---|-----------|------|----------|
| 1 | `cex_earn_create_auto_invest_plan` | Write | Create a new auto-invest plan **(See Create Plan Constraints)** |
| 2 | `cex_earn_update_auto_invest_plan` | Write | Update an existing plan |
| 3 | `cex_earn_stop_auto_invest_plan` | Write | Stop a plan **(explicit user confirmation before call — same as other writes)** |
| 4 | `cex_earn_add_position_auto_invest_plan` | Write ⚠️ | Add position immediately **(Call only once after confirmation, strictly no repeated calls)** |
| 5 | `cex_earn_list_auto_invest_plans` | Query | List user's auto-invest plans |
| 6 | `cex_earn_get_auto_invest_plan_detail` | Query | View single plan details |
| 7 | `cex_earn_list_auto_invest_coins` | Query | Query supported target coins |
| 8 | `cex_earn_get_auto_invest_min_amount` | Query | Query minimum investment amount |
| 9 | `cex_earn_list_auto_invest_plan_records` | Query | Query plan execution records |
| 10 | `cex_earn_list_auto_invest_orders` | Query | Query order details |
| 11 | `cex_earn_list_auto_invest_config` | Query | Query auto-invest configuration options |

### Supporting Tools

| Tool Name | Function |
|-----------|----------|
| `cex_spot_get_spot_accounts` | Query spot account balance |
| `cex_earn_list_user_uni_lends` | Optional read-only context for Simple Earn / Uni balances when fund source or debits involve earn (see **Execution** → balance check) |

## Query Function Usage

### Tool Mapping

| User Request | Tool to Use |
|--------------|-------------|
| List my auto-invest plans | `cex_earn_list_auto_invest_plans` |
| View single plan details | `cex_earn_get_auto_invest_plan_detail` |
| Query supported coins | `cex_earn_list_auto_invest_coins` |
| Query minimum investment amount | `cex_earn_get_auto_invest_min_amount` |
| View plan execution records | `cex_earn_list_auto_invest_plan_records` |
| View order details | `cex_earn_list_auto_invest_orders` |
| Query auto-invest config | `cex_earn_list_auto_invest_config` |

### Common Query Scenarios

#### Scenario 1: Query Supported Coins

**Example Questions**:
- "Which coins can I auto-invest in?"
- "What target coins does auto-invest support?"

**Operation**: Use the `cex_earn_list_auto_invest_coins` tool to query, which will return a list of all coins that support auto-invest.

---

#### Scenario 2: Query Minimum Investment Amount

**Example Questions**:
- "What's the minimum amount per period for USDT auto-invest?"
- "What's the minimum amount when BTC is the investment currency?"

**Operation**: Use the `cex_earn_get_auto_invest_min_amount` tool, need to specify the investment currency (USDT or BTC) and target coins.

---

#### Scenario 3: View Execution History

**Example Questions**:
- "How many times has my BTC auto-invest been executed recently?"
- "View the recent execution status of this plan"

**Operation**: Use `cex_earn_list_auto_invest_plan_records` to view execution records, use `cex_earn_list_auto_invest_orders` to view specific order details.

**Return Information Example**:
```
📋 Auto-Invest Execution Records

- Plan: {Plan name or ID}
- Execution count: {count}
- Latest execution: {amount} {currency} → {target coin}
```

---

#### Scenario 4: Plan Not Found

**Situation**: No matching auto-invest plan found during query.

**Prompt**: No matching auto-invest plan found. You can create a new auto-invest plan.

---

### Other Query Functions

- **List all plans**: Use `cex_earn_list_auto_invest_plans` to view all your auto-invest plans
- **Query configuration**: Use `cex_earn_list_auto_invest_config` to view available auto-invest settings and preset options

## Sub-Modules

| Module | Document | Purpose |
|--------|----------|---------|
| **Plan Management** | `references/autoinvest-plans.md` | Create, update, stop, and top-up (add position) workflows with detailed scenarios |
| **Compliance & Rules** | `references/autoinvest-compliance.md` | Investment currency restrictions, region compliance, and funding source rules |

## Routing Rules

| User Intent | Route to | Key Decision |
|-------------|----------|--------------|
| Create plan | `references/autoinvest-plans.md` → Scenario 1/2 | Single or multi-target |
| Update plan | `references/autoinvest-plans.md` | Modify existing plan parameters |
| Stop plan | `references/autoinvest-plans.md` → Scenario 9 | Terminate automatic deductions |
| Top-up / Add position | `references/autoinvest-plans.md` → Scenario 10 | One-off extra purchase |
| Query plans | SKILL.md → Tool Mapping | `cex_earn_list_auto_invest_plans` |
| Query plan detail | SKILL.md → Tool Mapping | `cex_earn_get_auto_invest_plan_detail` |
| Query supported coins | SKILL.md → Scenario 1 | `cex_earn_list_auto_invest_coins` |
| Query minimum amount | SKILL.md → Scenario 2 | `cex_earn_get_auto_invest_min_amount` |
| Query execution records | SKILL.md → Scenario 3 | `cex_earn_list_auto_invest_plan_records` |
| Query orders | SKILL.md → Tool Mapping | `cex_earn_list_auto_invest_orders` |
| Ask about restrictions | `references/autoinvest-compliance.md` | Investment currency, region, funding |

## Execution

1. **Intent Detection**: Analyze user request to determine operation type (create/update/stop/top-up/query/compliance)
2. **Route Selection**: 
   - **Plan lifecycle operations** (create/update/stop/top-up) → Load `references/autoinvest-plans.md` and follow workflows
   - **Query operations** → Use Tool Mapping table and call corresponding MCP tools directly
   - **Compliance questions** → Load `references/autoinvest-compliance.md` for rules and restrictions
3. **Parameter Validation**:
   - For write operations: Validate investment currency (USDT/BTC only), amount range, execution time, and for **creates** `plan_period_day` per **Create Plan Constraints**
   - For queries: Extract required parameters from user request
4. **Balance Check** (for write operations):
   - Call `cex_spot_get_spot_accounts` to verify sufficient funds
   - For Simple Earn fund source: Call `cex_earn_list_user_uni_lends` if applicable
5. **Confirmation** (for write operations):
   - Display operation summary (Action Draft)
   - Wait for explicit user confirmation
   - **Stop plan** (`cex_earn_stop_auto_invest_plan`): Show **Action Draft** and **stop** — do **not** call the tool in that same assistant turn. Call stop only after the user's **next message** contains explicit confirmation (`references/autoinvest-plans.md` → Scenario 9).
6. **MCP Tool Call**:
   - Execute the corresponding tool from the **MCP tools** section (Auto-Invest Related Tools or Supporting Tools tables) only
   - Pass validated parameters
7. **Response Formatting**:
   - Use Response Template from sub-module documents
   - Include key information: plan ID, amount, currency, targets, cadence

## Domain Knowledge

### What is Auto-Invest (DCA)?

**Dollar-Cost Averaging (DCA)** is an investment strategy where you invest a fixed amount at regular intervals, regardless of market conditions. This approach:
- Reduces timing risk by spreading purchases over time
- Averages out entry prices across market volatility
- Removes emotional decision-making from investing
- Suitable for long-term accumulation strategies

### Auto-Invest vs Manual Trading

| Aspect | Auto-Invest (DCA) | Manual Trading |
|--------|-------------------|----------------|
| **Execution** | Automatic, scheduled | Manual, on-demand |
| **Discipline** | High (no emotion) | Varies (emotion-driven) |
| **Timing** | Spread over time | Single point |
| **Use case** | Long-term accumulation | Active trading |
| **Skill required** | Low | High |

### Investment Currency

- **Investment currency**: The currency deducted from your account each period (USDT or BTC only)
- **Target coins**: The cryptocurrencies you want to buy (can be any supported coin)
- **Example**: Invest 100 USDT (investment currency) → Buy BTC (target coin)

### Cadence Options

| Period Type | Description | Min Interval |
|-------------|-------------|--------------|
| **Hourly** | Every N hours | 1 hour |
| **Daily** | Every day at specified hour | 1 day |
| **Weekly** | Every week on specified day | 7 days |
| **Biweekly** | Every 2 weeks | 14 days |
| **Monthly** | Every month on specified day | ~30 days |

### Fund Flow Options

**After creating a plan, purchased assets flow to one of two destinations**:

| Option | Field Value | Destination | Chinese UI (typical) | Description | Use Case |
|--------|-------------|-------------|----------------------|-------------|----------|
| **Simple Earn** | `fund_flow: "earn"` | Simple Earn | Localized app label | Assets automatically transfer to Simple Earn to earn interest | **Recommended for**: Passive income seekers, long-term holders who want to maximize returns |
| **Spot Account** | `fund_flow: "auto_invest"` | Spot Account | Localized app label | Assets remain in Spot account for manual management (default) | **Recommended for**: Active traders, users who plan to withdraw or transfer assets frequently |

**Important Notes**:
- This setting determines where purchased coins go **after each auto-invest execution** (post-purchase destination)
- **`earn`** maps to Simple Earn; **`auto_invest`** maps to spot account. API values align with localized app strings; if docs and the app disagree, follow the in-app wording.
- `earn` option provides additional passive income on accumulated assets
- `auto_invest` option gives you full control to trade, withdraw, or transfer at any time
- Default is `auto_invest` if not specified

## Safety Rules

### Default: no write without confirmation

Until the user has given **explicit confirmation** for the **current** Action Draft, **do not** call any write tool (`cex_earn_create_auto_invest_plan`, `cex_earn_update_auto_invest_plan`, `cex_earn_stop_auto_invest_plan`, `cex_earn_add_position_auto_invest_plan`). **Only** read/query operations are allowed—for example: list/detail plans, supported coins, min/max config, execution records and orders, and supporting balance reads (`cex_spot_get_spot_accounts`, `cex_earn_list_user_uni_lends`).

### Mandatory Confirmation for Write Operations

All write operations (create, update, stop, add position) **MUST** follow this confirmation workflow:

1. **Display Action Draft**: Show complete operation details before execution
2. **Wait for Confirmation**: Explicitly ask user "Please confirm to proceed"
3. **Execute Only After Confirmation**: Do not proceed without user's explicit agreement

**Stop plan** (`cex_earn_stop_auto_invest_plan`): Show Action Draft (plan ID, name, effect: future deductions stop) and **end the turn** asking for confirmation. Call MCP **only** after the user's **following message** explicitly confirms — never call stop in the same assistant response as the first draft, even if the user already named a plan ID.

### Stale confirmation

If the user changes any material detail after seeing an Action Draft (amount, targets, cadence, plan ID, fund flow, `plan_period_hour`, `plan_period_day`, etc.), treat earlier confirmation as **void**. Show an **updated** Action Draft and obtain a **fresh** explicit confirmation before any write tool call.

### Add Position Safety (Critical)

⚠️ **The `cex_earn_add_position_auto_invest_plan` tool is extremely sensitive**:

- **Call EXACTLY ONCE** per user confirmation
- **NEVER call multiple times** for the same request (causes duplicate deductions)
- **Always confirm amount** with user before calling
- **Check balance** before calling

**Bad practice** ❌:
```
User: "Add more to my plan"
Assistant: [Calls add_position multiple times to show different amounts]
```

**Good practice** ✅:
```
User: "Add more to my plan"
Assistant: "How much would you like to add? Your current plan is 100 USDT per period."
User: "Add 50 USDT"
Assistant: [Shows draft] "Confirm to add 50 USDT?"
User: "Yes"
Assistant: [Calls add_position ONCE]
```

### Parameter Validation

Before calling any write tool:

| Validation | Rule | Action if Failed |
|------------|------|------------------|
| Investment currency | Must be USDT or BTC | Reject and explain restriction |
| Amount | Must be within [min, max] range | Query min/max, then reject with valid range |
| Execution time | Must be integer 0-23 (on the hour) | Reject and explain hourly restriction |
| `plan_period_day` (create) | Must not be `0`; ranges per `plan_period_type` (see **Create Plan Constraints**) | Reject with allowed ranges; see `references/autoinvest-plans.md` Workflow step 6 |
| Balance | Must be sufficient for first period | Show shortfall, suggest top-up or lower amount |

### No Speculation on Next Purchase Time

- Do **not** calculate or display the next automatic purchase time
- If user asks, direct them to Gate App or website for real-time schedule
- The system does not provide this information via API

## Error Handling

| Error Condition | Detection | Response |
|-----------------|-----------|----------|
| **Too many target coins** | User specifies > 10 target coins | Reject immediately: "A plan can have at most 10 target coins. You specified {N} coins. Please reduce the number of targets." |
| **Coin allocation too small** | Any target coin has ratio < 10 | Reject immediately: "Each target coin must have at least 10% allocation. Coin {X} has only {Y}%. Please adjust the ratios to ensure each coin has at least 10%." |
| **Insufficient balance** | `cex_spot_get_spot_accounts` shows balance < amount | Do not proceed. Inform user of shortfall: "Your current balance is {X} {currency}, but {Y} {currency} is required. Please deposit more funds or reduce the investment amount." |
| **Invalid investment currency** | User specifies currency other than USDT/BTC | Reject immediately: "Only USDT or BTC are supported as investment currency. Please choose USDT or BTC." |
| **Amount below minimum** | User amount < `cex_earn_get_auto_invest_min_amount` | Call min amount tool, then inform: "Minimum amount is {min} {currency}. Please increase your investment amount." |
| **Amount above maximum** | User amount > `cex_earn_list_auto_invest_config` max | Call config tool, then inform: "Maximum amount is {max} {currency}. Please reduce your investment amount." |
| **Invalid execution time** | User specifies minutes/seconds or hour outside 0-23 | Reject: "Auto-invest only supports execution on the hour (0-23). Please choose an hour between 0 and 23." |
| **Invalid `plan_period_day`** | `0` or out of range for `plan_period_type` on create | Do not call create; state valid ranges: monthly **1–30**; weekly/biweekly **1–7** (1 = Monday); daily/hourly/4-hourly use **`1`** (`references/autoinvest-plans.md` Workflow step 6) |
| **Plan not found** | Query returns no matching plan | Inform: "No matching auto-invest plan found. You can create a new plan." (See Scenario 4) |
| **MCP tool missing** | Required tool not available in MCP service | Explain: "Auto-invest feature requires updated MCP service. Please ensure gate-mcp is properly configured." |
| **API error (401/403)** | Authentication failure | Guide: "Authentication error. Please check your API key permissions include Earn (auto-invest) access." See [`exchange-runtime-rules.md`](../exchange-runtime-rules.md) for auth handling. |
| **API error (4xx/5xx)** | Other API errors | Report error message and suggest retry or contact support |
| **Missing required parameter** | Tool schema requires param with no default | **Do not guess**. Ask user: "Please specify {parameter_name} (e.g., {example})." |

### Parameter Hygiene

- If a tool parameter is **required** and the schema provides **no default**, **prompt the user** for the value
- **Never** guess or invent parameter values
- **Always** validate parameters against Business Rules before calling tools

## Judgment Logic Summary

| Condition | Action | Tool(s) to Use |
|-----------|--------|----------------|
| User wants to create plan | Route to `references/autoinvest-plans.md` Scenario 1/2 | Validate (incl. `plan_period_day`) → `cex_spot_get_spot_accounts` (and `cex_earn_list_user_uni_lends` if earn fund source) → `cex_earn_get_auto_invest_min_amount` → `cex_earn_list_auto_invest_config` → Confirm → `cex_earn_create_auto_invest_plan` |
| User wants to update plan | Route to `references/autoinvest-plans.md` | `cex_earn_list_auto_invest_plans` (if no ID) → Confirm → `cex_earn_update_auto_invest_plan` |
| User wants to stop plan | Route to `references/autoinvest-plans.md` Scenario 9 | `cex_earn_list_auto_invest_plans` (if no ID) → Action Draft (end turn) → user's **next** message confirms → `cex_earn_stop_auto_invest_plan` |
| User wants to top-up (add position) | Route to `references/autoinvest-plans.md` Scenario 10 | `cex_earn_list_auto_invest_plans` (if no ID) → `cex_earn_get_auto_invest_plan_detail` (if no amount) → `cex_spot_get_spot_accounts` → Confirm → `cex_earn_add_position_auto_invest_plan` (ONCE ONLY) |
| User wants to list plans | Direct query | `cex_earn_list_auto_invest_plans` |
| User wants plan detail | Direct query | `cex_earn_get_auto_invest_plan_detail` |
| User asks "which coins?" | Scenario 1 | `cex_earn_list_auto_invest_coins` |
| User asks "minimum amount?" | Scenario 2 | `cex_earn_get_auto_invest_min_amount` |
| User asks "execution history?" | Scenario 3 | `cex_earn_list_auto_invest_plan_records` |
| User asks "order details?" | Direct query | `cex_earn_list_auto_invest_orders` |
| User asks about investment currency restrictions | Route to `references/autoinvest-compliance.md` | Explain USDT/BTC only rule |
| User asks about fund source | Route to `references/autoinvest-compliance.md` | Explain spot vs earn options |
| Plan not found in query | Scenario 4 | Inform user, offer to create new plan |
| Insufficient balance | Error Handling | Show shortfall, do not proceed |
| Invalid parameters | Error Handling | Validate against Business Rules, reject with explanation |

## Report Template

### Plan Creation Success

```markdown
✅ Auto-invest plan created

- Invest currency: {USDT|BTC}
- Amount per period: {amount}
- Cadence: {cadence description}
- Target(s): {target coin(s) with ratios if multi-target}
- Fund source: {spot|earn}
- Fund flow: {auto_invest|earn} (spot account|Simple Earn)
```

### Plan Update Success

```markdown
✅ Auto-invest plan updated

- Plan: {id or name}
- Updated: {changed fields and new values}
```

### Plan Stop Success

```markdown
✅ Auto-invest plan stopped

- Plan: {id or name}
- Status: Automatic deductions ceased
- Note: Purchased assets remain in {account type}
```

### Top-up Success

```markdown
✅ Top-up executed

- Plan: {id or name}
- Amount: {amount} {invest_currency}
- Target allocation: {per Business Rules}
```

### Query Response (Plans List)

```markdown
📋 Your Auto-Invest Plans

{For each plan:}
**Plan {N}: {plan_name}**
- Investment: {amount} {currency} per {cadence}
- Target(s): {coin(s)}
- Execution count: {period} times
- Status: Active

{If no plans:}
You have no active auto-invest plans. Create one to start DCA investing.
```

### Query Response (Supported Coins)

```markdown
📋 Supported Auto-Invest Coins

{List coins returned by cex_earn_list_auto_invest_coins}

You can use any of these coins as targets in your auto-invest plan.
```

### Query Response (Minimum Amount)

```markdown
📋 Minimum Investment Amount

- Investment currency: {USDT|BTC}
- Target(s): {coin(s)}
- Minimum per period: {min_amount} {currency}
```

### Error Response

```markdown
❌ {Error type}

{Explanation of what went wrong}

{Actionable suggestion to resolve}
```

## Reference Documentation

| Document | Content |
|----------|---------|
| `references/scenarios.md` | Comprehensive scenario index covering all 16 scenarios (plan lifecycle, queries, compliance) |
| `references/autoinvest-plans.md` | Plan lifecycle operations and scenarios (create, update, stop, top-up) |
| `references/autoinvest-compliance.md` | Compliance rules and restrictions (investment currency, region, funding) |
