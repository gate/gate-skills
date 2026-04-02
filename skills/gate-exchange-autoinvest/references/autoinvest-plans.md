# Gate Auto-Invest — Plan lifecycle (create, update, stop, top-up)

Create, update, stop, and add-position workflows for fast auto-invest. Use the **write** tools in `SKILL.md` → **MCP tools**: `cex_earn_create_auto_invest_plan`, `cex_earn_update_auto_invest_plan`, `cex_earn_stop_auto_invest_plan`, `cex_earn_add_position_auto_invest_plan`.

## ⚠️ Time Zone Handling (CRITICAL)

**All execution times use UTC time zone**:
- The `plan_period_hour` parameter (0-23) represents **UTC hours**, NOT local time
- When users specify times in their local time zone, **you MUST convert to UTC** before calling the API
- **Always show both UTC and local time** in confirmation messages to avoid confusion

**Conversion Process**:
1. **Try to detect user's system time zone** (e.g., via `date +"%Z %z"` command)
2. **If time zone detected successfully**:
   - When user says "every day at 10:00", determine if they mean:
     - Local time (most common) → convert to UTC
     - UTC time (explicitly stated) → use directly
   - Formula: `UTC hour = local hour - timezone offset`
     - Example: Beijing time 10:00 (UTC+8) → 10 - 8 = 02:00 UTC → `plan_period_hour: 2`
     - Example: New York time 14:00 (UTC-5) → 14 - (-5) = 19:00 UTC → `plan_period_hour: 19`
3. **If time zone detection fails** (fallback):
   - Use the hour number directly as specified by user
   - Assume user provided the hour in their intended execution time
   - Example: User says "10:00" → set `plan_period_hour: 10` directly
   - In confirmation, note that time zone could not be detected

**Confirmation Templates**:

When time zone is detected:
```
Execution time: 02:00 UTC (10:00 Beijing time / UTC+8)
```

When time zone detection fails:
```
Execution time: 10:00 (time zone could not be detected, using your specified hour directly)
```

## MCP alignment

Map user intent to the **MCP tools** table in `SKILL.md`, then call the matching tool. Supporting calls:

| Step | Tool |
|------|------|
| Check spot balance | `cex_spot_get_spot_accounts` |
| Check Uni balance context | `cex_earn_list_user_uni_lends` (when relevant) |

---

## Workflow

Write operations (create, update, stop, top-up). Steps:

1. **Schema check**: For the chosen write tool, confirm every **required** argument is available or has a documented default in the MCP schema; if not, **ask the user** to provide the missing value(s) (`SKILL.md` → **Error Handling** → **Parameter Hygiene**).
2. **Parse**: invest currency (USDT/BTC only), targets, amount, cadence, optional plan name, optional fund flow.
3. **Validate targets**:
   - **Supported target coins** (creates, and updates that set or add targets): Call `cex_earn_list_auto_invest_coins` and verify every user-specified target symbol appears in the response. If any coin is missing from that list, **do not** proceed with the write; inform the user: "{SYMBOL} is not supported for auto-invest. Please remove it or choose a supported coin."
   - **Multi-target plans only** — **Maximum targets**: A plan can have at most **10 target coins**
   - **Multi-target plans only** — **Minimum ratio per coin**: Each target coin must have at least **10% allocation**
   - If multi-target validation fails, reject and inform the user of these constraints
4. **Validate amount** (for creates):
   - Call `cex_earn_get_auto_invest_min_amount` to get minimum amount
   - Call `cex_earn_list_auto_invest_config` to get maximum amount
   - Verify user's amount is within [min, max] range; if not, reject and inform user
5. **Validate execution time**: Ensure `plan_period_hour` is an integer 0-23 (only on-the-hour execution supported)
   - ⚠️ **IMPORTANT**: `plan_period_hour` uses **UTC time zone**. When user specifies a local time (e.g., "10:00 AM Beijing time"), you MUST convert it to UTC before passing to the API.
   - **Conversion example**: Beijing time 10:00 (UTC+8) → UTC 02:00 → pass `plan_period_hour: 2`
   - **Fallback**: If system time zone cannot be detected, use user's specified hour directly (e.g., user says "10:00" → use `plan_period_hour: 10`)
   - **Always clarify with user** in confirmation: show both local time and UTC time (if time zone detected), or note that time zone detection failed
6. **`plan_period_day` (create plans only — required; must not be `0`)**: When calling `cex_earn_create_auto_invest_plan`, always pass **`plan_period_day`**. The value **must not be `0`**.
   - Meaning depends on **`plan_period_type`**:
     - **`monthly`**: Calendar day of the month, **1–30** (inclusive).
     - **`weekly`** or **`biweekly`**: Day of the week, **1–7**, where **1 = Monday** and **7 = Sunday**.
     - **`daily`**, **`hourly`**, or **`4-hourly`**: Set **`plan_period_day` to `1`** (fixed convention; the field is still required and must be non-zero).
   - If the user’s chosen day or weekday is outside the valid range for the selected `plan_period_type`, reject and state the allowed range before calling the create tool.
7. **Determine fund flow** (for creates):
   - If user specifies fund flow preference, use their choice
   - If not specified, default to `auto_invest` (assets remain in spot account)
   - **Options** (`fund_flow` = post-purchase destination):
     - `fund_flow: "earn"` → Simple Earn
     - `fund_flow: "auto_invest"` → Spot account (default)
8. **Balance**: For creates/top-ups, verify spot (and if applicable Uni) per product rules using supporting tools.
9. **Confirm**: Show an **Action Draft** (operation, amounts, targets, cadence, fund flow); wait for explicit confirmation (stop plan: **one follow-up user message** after the draft — see Scenario 9).
10. **Execute**: Call the matching **write** tool (see `SKILL.md` → **MCP tools**); map errors to compliance messages when needed.
11. **Format**: Use Response Template style below; English user-facing text.

---

## Scenario 1: Single-target recurring buy (create)

**Context**: User specifies invest currency, amount, cadence, single target (e.g. BTC).

**Prompt Examples**:
- "Invest 100 USDT weekly into BTC—create a plan."
- "DCA 50 USDT every day into ETH."

**Expected Behavior**:
1. Validate amount range:
   - Call `cex_earn_get_auto_invest_min_amount` with target coins
   - Call `cex_earn_list_auto_invest_config` to get max amount
   - If user's amount is outside [min, max], reject and inform user of valid range
2. `cex_spot_get_spot_accounts` (filter by invest currency) to check sufficiency for at least the first period.
3. Set defaults if not provided:
   - `plan_period_hour`: default 10 (10:00 UTC, **NOT local time**)
   - `plan_period_day`: follow Workflow step 6 — use **`1`** for `daily` / `hourly` / `4-hourly`; for `monthly` use **1–30** from user intent; for `weekly` / `biweekly` use **1–7** (1 = Monday) from user intent (**never `0`**)
   - `fund_source`: default `spot`
   - `fund_flow`: default `auto_invest` (assets remain in Spot account)
4. **Time zone handling**: 
   - Try to detect user's system time zone via `date +"%Z %z"` command
   - **If detected**: Convert user's local time to UTC before setting `plan_period_hour`
   - **If detection fails**: Use user's specified hour directly (fallback mode)
5. Explain fund flow if user asks or if relevant:
   - `fund_flow: "auto_invest"` → Spot account (default)
   - `fund_flow: "earn"` → Simple Earn
6. **Confirm**: Show an **Action Draft** (operation, amounts, targets, cadence, fund flow, UTC/local execution time); wait for explicit user confirmation per `SKILL.md` → **Safety Rules** and **Workflow** step 9 before calling the create tool.
7. Call `cex_earn_create_auto_invest_plan` with parsed params.
8. On success, restate plan summary including fund flow destination (do **not** surface scheduled timing for the next automatic purchase).

**Response Template**:
```
✅ Auto-invest plan created

- Invest currency: {USDT|BTC}
- Amount per period: {amount}
- Cadence: {cadence}
- Execution time: 
  - If time zone detected: {HH:00 UTC} (local time: {HH:00 in user's timezone})
  - If time zone not detected: {HH:00} (time zone could not be detected, using your specified hour)
- Target(s): {targets}
- Fund flow: {auto_invest → spot account | earn → Simple Earn} (API: {auto_invest|earn})
```

---

## Scenario 2: Multi-target create

**Context**: User splits one periodic amount across multiple targets.

**Prompt Examples**:
- "500 USDT monthly into BTC and ETH."
- "Create a plan with 100 USDT daily across BTC, ETH, and SOL."

**Target Constraints**:
- ⚠️ **Maximum 10 target coins** per plan
- ⚠️ **Each coin must have at least 10% allocation** (ratio ≥ 10)
- If user specifies more than 10 coins → reject with error
- If any coin has less than 10% allocation → reject with error

**Expected Behavior**:
1. **Validate target constraints**:
   - Check that the number of target coins ≤ 10
   - Check that each coin's ratio ≥ 10 (10%)
   - If validation fails, reject immediately with clear explanation
2. Validate amount range:
   - Call `cex_earn_get_auto_invest_min_amount` with all target coins and their ratios
   - Call `cex_earn_list_auto_invest_config` to get max amount
   - If amount is outside [min, max], reject with error message
3. Verify total invest currency balance ≥ periodic total (per product rules).
4. Set defaults for optional parameters (execution time, fund source, fund flow, **`plan_period_day`** per Workflow step 6 — never `0`).
   - **Note**: If user specifies execution time, remember to convert local time to UTC (see Time Zone Handling section)
5. **Confirm**: Show an **Action Draft**; wait for explicit user confirmation per `SKILL.md` → **Safety Rules** before any create call.
6. Call `cex_earn_create_auto_invest_plan` with multiple targets if product allows (e.g. max targets per MCP schema).

**Response Template**:
```
✅ Multi-target plan created

- Invest currency: {currency}
- Total per period: {amount}
- Targets: {list with weights if applicable}
```

**Error Examples**:
- Too many targets: "❌ A plan can have at most 10 target coins. You specified {N} coins. Please reduce the number of targets."
- Ratio too small: "❌ Each target coin must have at least 10% allocation. Coin {X} has only {Y}%. Please adjust the ratios."

---

## Scenario 3: Check balance then create

**Context**: User asks to verify funds before creating.

**Prompt Examples**:
- "Check if I have enough USDT for 200 biweekly into ETH, then create if ok."

**Expected Behavior**:
1. `cex_spot_get_spot_accounts` for USDT.
2. If insufficient → **do not** create; explain shortfall.
3. If sufficient → confirm once, then create.

---

## Scenario 4: Create with auto Simple Earn after buy

**Context**: User wants purchased assets moved to Simple Earn when product supports it.

**Prompt Examples**:
- "Weekly 50 USDT into BTC, auto-send BTC to Simple Earn."
- "Create a daily 100 USDT plan for ETH, transfer to Simple Earn automatically."

**Expected Behavior**:
1. Recognize user intent to auto-transfer to Simple Earn
2. Set `fund_flow: "earn"` in the create plan parameters
3. Validate amount and balance (same as Scenario 1)
4. Confirm with user, explicitly mentioning that purchased assets will auto-transfer to Simple Earn
5. Call `cex_earn_create_auto_invest_plan` with `fund_flow: "earn"`
6. On success, restate plan summary and confirm fund flow destination

**Response Template**:
```
✅ Auto-invest plan created

- Invest currency: {USDT|BTC}
- Amount per period: {amount}
- Cadence: {cadence}
- Target(s): {targets}
- Fund flow: **Simple Earn** ✨ (Assets will earn interest automatically)
```

**Note**: If MCP schema doesn't support fund flow, explain that feature may not be available and offer standard create with manual transfer instructions.

---

## Scenario 5: Named plan + frequency

**Context**: User gives a display name and schedule.

**Prompt Examples**:
- "Name it ‘BTC dip’, 20 USDT daily into BTC."

**Expected Behavior**:
1. Include plan name + daily cadence + amount in create payload per MCP schema.

---

## Scenario 6: Vague intent (no write yet)

**Context**: User only says "auto-invest" or similar vague terms.

**Prompt Examples**:
- "I want DCA."
- "Auto-invest wealth management."

**Expected Behavior**:
1. **No** write call.
2. Suggest defaults (USDT → BTC), ask for amount, targets, cadence.

---

## Scenario 7: Partial parameters

**Context**: User gives amount only or target only.

**Prompt Examples**:
- "DCA 100 USDT."
- "DCA BTC."

**Expected Behavior**:
1. Ask one concise clarifying question for missing target, invest currency, or cadence.

---

## Scenario 8: Plan detail (single plan)

**Context**: User asks for one plan’s metadata.

**Prompt Examples**:
- "Show my ETH DCA plan details."

**Expected Behavior**:
1. Call `cex_earn_list_auto_invest_plans` if needed to resolve plan id; then `cex_earn_get_auto_invest_plan_detail`.
2. Present invest currency, targets, amount, cadence, flags, execution counts (omit any field that only conveys **when the next automatic purchase will run**).

---

## Scenario 9: Stop plan

**Context**: User terminates a plan.

**Prompt Examples**:
- "Stop my ETH auto-invest."

**Expected Behavior**:
1. **No stop MCP until a dedicated confirm reply**: **Do not** call `cex_earn_stop_auto_invest_plan` until the user has sent **one additional message after** the Action Draft (step 5), and that message is an unambiguous confirmation. Until then, you may use **read-only** MCP tools only (`cex_earn_list_auto_invest_plans`, `cex_earn_get_auto_invest_plan_detail`) to resolve the plan and build the draft.
2. **Same-turn ban**: In the assistant turn where you **first** present the Action Draft for this stop request, **do not** call `cex_earn_stop_auto_invest_plan` — end that turn by asking the user to confirm. Even if the user already supplied a plan ID or name (e.g. "stop plan 12345"), you still **must** wait for their **next** message before calling the stop tool.
3. If the user does not provide a plan ID, call `cex_earn_list_auto_invest_plans` to query all user plans.
4. Match by plan name:
   - If a match is found, use that plan's `id` for the stop call **only after** the confirming message (step 6).
   - If **multiple** plans share the same name, list the matching `id`s and ask the user to pick one before continuing.
   - If no name match is found, output all user plans and ask the user to specify which plan to stop.
5. **Action Draft (turn 1)**: Present an **Action Draft** — plan `id`, name, summary (invest currency, amount per period, cadence as useful), and that **future automatic deductions will cease**. Ask clearly for a **reply** to proceed (e.g. reply **yes** or **confirm** to stop this plan). **Valid confirmation** in the **next** user message includes **confirm**, **yes**, **I confirm**, or another unambiguous equivalent. Do **not** treat vague replies as confirmation.
6. **Only after** that **next** user message: If they explicitly confirm, call `cex_earn_stop_auto_invest_plan`. If they decline or are ambiguous, do **not** call the tool; clarify or re-show the draft as needed.
7. After success, explain holdings remain in spot unless product states otherwise.

---

## Scenario 10: Top-up (add position)

**Context**: One-off extra purchase on existing plan.

**Prompt Examples**:
- "Add another 100 USDT buy to my BTC DCA."
- "Add one more to my ETH-GT-GRIN auto-invest"
- "Add another buy to my DCA"

**Expected Behavior**:
1. If the user does not provide a plan ID, call `cex_earn_list_auto_invest_plans` to query all user plans.
2. Match by plan name:
   - If a match is found, use that plan's ID.
   - If no name match is found, output all user plans and ask the user to specify which plan to top up.
3. **Determine add position amount**:
   - If user specified an amount, use that amount.
   - If user did NOT specify an amount (e.g., "add one more", "top up again"), call `cex_earn_get_auto_invest_plan_detail` to get the plan's `amount` field, and use that as the default add position amount.
   - Show the determined amount to the user for confirmation.
4. `cex_spot_get_spot_accounts` to check balance sufficiency for the determined amount.
5. **Confirm with user**: Display add position details (plan name, amount, currency) and wait for explicit confirmation.
6. **Call once only**: After user confirms, call `cex_earn_add_position_auto_invest_plan` **exactly once** with the plan ID and amount.

**Response Template**:
```
✅ Top-up executed

- Plan: {id or label}
- Amount: {amount} {invest_currency}
- Result: {summary from tool response}
```

**Important**:
- ⚠️ **Never call `cex_earn_add_position_auto_invest_plan` multiple times** for the same request
- Always confirm with user before executing
- Default to plan's periodic amount when user doesn't specify

---

## Report Template

Use English for user-facing text. Per-scenario **Response Template** blocks appear under Scenario 1, 2, 4, and 10 above. Align success summaries with `SKILL.md` → **Report Template** (plan created, updated, stopped, top-up).

**Plan created (single-target, concise)**:

```
✅ Auto-invest plan created

- Invest currency: {USDT|BTC}
- Amount per period: {amount}
- Cadence: {cadence}
- Target(s): {targets}
- Fund flow: {auto_invest → spot account | earn → Simple Earn}
```

---

## Error handling (plans)

| Condition | Action |
|-----------|--------|
| Unsupported target coin (not in `cex_earn_list_auto_invest_coins`) | Do not call the write tool; reject: "{SYMBOL} is not supported for auto-invest. Please remove it or choose a supported coin." |
| Too many target coins (> 10) | Reject immediately: "A plan can have at most 10 target coins. You specified {N} coins. Please reduce the number of targets." |
| Coin ratio too small (< 10%) | Reject immediately: "Each target coin must have at least 10% allocation. Coin {X} has only {Y}%. Please adjust the ratios to ensure each coin has at least 10%." |
| `plan_period_day` is `0` or out of range for `plan_period_type` | Do not call create; explain valid ranges (Workflow step 6): monthly **1–30**; weekly/biweekly **1–7** (1 = Monday); daily/hourly/4-hourly use **`1`**. |
| Insufficient balance | Do not create/top-up; suggest top-up or lower amount |
| Autoinvest tools missing | Explain MCP update needed; no simulated execution |
| 401/403 | API key / permissions per [`exchange-runtime-rules.md`](../../exchange-runtime-rules.md) |
