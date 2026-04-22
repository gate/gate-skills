# Gate CandyDrop Activities — Browse & Rules

Browse available CandyDrop activities and view activity rules including prize pools and tasks.

**Note:** Reference prose is **English**. Non-English strings in the **task-type mapping** table are **example user-facing labels** for Chinese users (`Language adaptation` in `SKILL.md`), not alternate skill text.

## MCP tools and parameters

| Tool | Purpose | Required | Optional |
|------|---------|----------|----------|
| **cex_launch_get_candy_drop_activity_list_v4** | Query activity list | — | `currency`, `status`, `rule_name`, `register_status`, `limit`, `offset` |
| **cex_launch_get_candy_drop_activity_rules_v4** | Query activity rules & prize pools | `currency` **or** `activity_id` (at least one) | — |

- **cex_launch_get_candy_drop_activity_list_v4**: No authentication required (public endpoint).
  - `status`: `ongoing` (ongoing), `upcoming` (upcoming), `ended` (ended). Omit for all.
  - `rule_name`: Task type filter: `spot`, `futures`, `deposit`, `invite`, `trading_bot`, `simple_earn`, `first_deposit`, `alpha`, `flash_swap`, `tradfi`, `etf`.
  - `register_status`: `registered` (already registered), `unregistered` (not yet registered). Omit for all.
  - `limit`: Max rows to return, default 10, max 30.
  - `offset`: Offset for pagination, default 0.
  - `currency`: Filter by token name (e.g. "USDT").

- **cex_launch_get_candy_drop_activity_rules_v4**: No authentication required (public endpoint).
  - Must provide at least one of `currency` or `activity_id`.
  - If `currency` is provided without `activity_id`, API auto-matches the nearest valid activity.

**API response — Activity List item (`CandyDropV4Activity`):**

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Activity ID |
| currency | string | Token/project name (e.g. "USDT") |
| total_rewards | string | Total prize pool amount |
| start_time | string | Activity start time (pre-formatted UTC string) |
| end_time | string | Activity end time (pre-formatted UTC string) |
| rule_name | array of string | List of task types included (often English product words; **localize for display** — see below) |
| participants | integer | Number of registered participants |
| user_max_rewards | string | Maximum reward per user |

**`rule_name` — task types: localize for display (mandatory in user language)**

Each string is a **task category label**, not a currency ticker. When the user writes in **Chinese** (or any non-English language), **do not** paste raw API English into the table; map each value using the table below (match **case-insensitively**; treat `_` and spaces as equivalent). If the API returns a synonym (e.g. `Convert` for flash convert), map it to the **same localized label as `flash_swap`** (use the zh-CN column when the user is writing in Chinese).

| Filter / key (API) | Typical English in payload | zh-CN user-facing label (when user writes in Chinese) |
|--------------------|----------------------------|--------------------------------------------------------|
| spot | Spot | 现货 |
| futures | Futures | 合约 |
| deposit | Deposit | 充值 |
| invite | Invite | 邀请 |
| trading_bot | Trading Bot | 交易机器人 |
| simple_earn | Simple Earn | 余币宝 |
| first_deposit | First Deposit | 首次充值 |
| alpha | Alpha | Alpha |
| flash_swap | Flash Swap, Convert | 闪兑 |
| tradfi | TradFi | TradFi |
| etf | ETF | ETF |

- **List separator**: Use a locale-appropriate separator between types — e.g. ideographic comma **`、`** for zh-CN (example: `ETF、TradFi`), **`, `** for English.
- **Tool calls**: When passing **`rule_name`** as a query parameter to `cex_launch_get_candy_drop_activity_list_v4` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二), keep using the API filter token (e.g. `futures`, `simple_earn`) — only **end-user visible** text is translated.

**Activity list — answer directly, no filler (mandatory)**

Applies when the user only wants a **catalogue** of activities (e.g. “what CandyDrop activities are there”, “list ongoing CandyDrop”, or the same intent in any language) — and is **not** asking for concepts, field definitions, or “how the skill works”.

- **Do**: Call the list tool, then output **immediately** a **short title line** (optional, e.g. status + total count in the user’s language) + **one compact table** (or the Response Template fields) with data. Apply `rule_name` localization **inside cells** using the table above — **do not** paste the mapping table into the reply.
- **Do not**: Long introductions (“according to the docs…”, “first let me explain what an activity is…”); explaining `currency` / `activity_id` / statuses unless asked; reproducing this whole skill section; naming MCP tools or parameters unless the user needs them for debugging.

If the user **explicitly** asks for explanations or mappings, keep answers **short** and on-topic — still avoid repeating the full list tool output as a second wall of text.

**API response — Activity Rules (`CandyDropV4ActivityRules`):**

| Field | Type | Description |
|-------|------|-------------|
| currency | string | Token/project name |
| total_rewards | string | Total prize pool amount |
| start_time | string | Activity start time (pre-formatted UTC string) |
| end_time | string | Activity end time (pre-formatted UTC string) |
| prize_pools | array | List of prize pools (see below) |

**API response — Prize Pool (`CandyDropV4PrizePool`):**

| Field | Type | Description |
|-------|------|-------------|
| prize_pool_type | integer | Prize pool type: 1=By Candy count, 2=By amount, 3=Fixed reward. Display label in user language per SKILL.md "Language adaptation" rule. |
| prize_all | string | Total prize amount for this pool |
| prize_limit | string | Per-user reward cap for this pool |
| tasks | array | List of tasks in this pool (see below) |

**API response — Task (`CandyDropV4Task`):**

| Field | Type | Description |
|-------|------|-------------|
| task_name | string | Task main title |
| task_desc | string | Task subtitle (or "-" if none) |
| exclusive_label | string | Exclusive task label (or "-" if none) |

---

## Workflow

### Activity List

1. **Parse parameters**: Extract filters from user query — `status`, `currency`, `rule_name`, `register_status`, `limit`, `offset`.
2. **Call tool**: Call `cex_launch_get_candy_drop_activity_list_v4` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with optional filters. Use `limit=10`, `offset=0` by default.
3. **Key data to extract**: From each activity: `currency`, `total_rewards`, `start_time`, `end_time`, `rule_name`, `participants`, `user_max_rewards`.
4. **Format response**: Display activity list with all fields. Map `status` values to user-friendly labels if filtering. **Render `rule_name` in the user’s language** using the **Task types** table above (not raw English when the user is using Chinese, etc.). **Follow Activity list — answer directly** above: table first, no lecture. Use the Response Template from the matching scenario.

### Activity Rules

1. **Parse parameters**: Extract `currency` or `activity_id` from user query. If neither is provided, ask the user for `currency`.
2. **Call tool**: Call `cex_launch_get_candy_drop_activity_rules_v4` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with `currency` and/or `activity_id`.
3. **Key data to extract**: `currency`, `total_rewards`, `start_time`, `end_time`, and per prize pool: `prize_all`, `prize_limit`, `tasks` (task_name, task_desc, exclusive_label).
4. **Format response**: Show activity overview followed by prize pool details and task list. Use the Response Template from the matching scenario.

## Report Template

Use the **Response Template** block from the scenario that matches the user intent. Always include the fields specified in each template.

---

## Scenario 1: Query activities by status

**Context**: User wants to see CandyDrop activities filtered by status (all, ongoing, upcoming, or ended).

**Prompt Examples**:
- "Show all CandyDrop activities"
- "What ongoing CandyDrop activities are available?"
- "Any upcoming CandyDrop events?"
- "Show ended CandyDrop activities"

**Expected Behavior**:
1. Map user intent to status: all=omit, ongoing=`ongoing`, upcoming=`upcoming`, ended=`ended`.
2. Call `cex_launch_get_candy_drop_activity_list_v4` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with `status={value}`, `limit=10`, `offset=0` (use `limit=30` if the user clearly wants “all” and status is narrow, within API max).
3. For each activity display: `currency`, `total_rewards`, `start_time`, `end_time`, `rule_name`, `participants`, `user_max_rewards`.
4. Display formatted activity list **only** — **no** skill tutorial, **no** mapping tables; follow **Activity list — answer directly** above.

**Response Template**:
```
CandyDrop Activities ({status_label})

{For each activity:}
Token: {currency}
  Total Rewards: {total_rewards}
  Period: {start_time} ~ {end_time}
  Task Types: {rule_name localized per Task types table; locale-appropriate separator (e.g. "、" for zh-CN, ", " for English)}
  Participants: {participants}
  Max Reward Per User: {user_max_rewards}

Showing {count} activities total.
```

---

## Scenario 2: Query activities by token

**Context**: User wants to find CandyDrop activities for a specific token.

**Prompt Examples**:
- "Show CandyDrop activities for USDT"
- "What CandyDrop activities are available for USDT?"
- "Any CandyDrop events for BTC?"

**Expected Behavior**:
1. Extract the token name from user query (e.g. "USDT").
2. Call `cex_launch_get_candy_drop_activity_list_v4` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with `currency={token}`, `limit=10`, `offset=0`.
3. For each activity display all fields.
4. If no results, suggest trying other tokens.

**Response Template**:
```
CandyDrop Activities (Token: {currency})

{For each activity:}
Activity: {currency}
  Total Rewards: {total_rewards}
  Period: {start_time} ~ {end_time}
  Task Types: {rule_name localized per Task types table; locale-appropriate separator (e.g. "、" for zh-CN, ", " for English)}
  Participants: {participants}
  Max Reward Per User: {user_max_rewards}

Found {count} activities for {currency}.
```

---

## Scenario 3: Query activities by task type

**Context**: User wants to find CandyDrop activities with a specific task type.

**Prompt Examples**:
- "Show CandyDrop activities with spot trading tasks"
- "What CandyDrop activities have spot trading tasks?"
- "Any CandyDrop with futures trading tasks?"

**Expected Behavior**:
1. Map user intent to `rule_name`: spot=`spot`, futures=`futures`, deposit=`deposit`, invite=`invite`, trading_bot=`trading_bot`, simple_earn=`simple_earn`, first_deposit=`first_deposit`, alpha=`alpha`, flash_swap=`flash_swap`, tradfi=`tradfi`, etf=`etf`.
2. Call `cex_launch_get_candy_drop_activity_list_v4` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with `rule_name={value}`, `limit=10`, `offset=0`.
3. For each activity display all fields.
4. If no results, suggest trying other task types.

**Response Template**:
```
CandyDrop Activities (Task Type: {task_type_label})

{For each activity:}
Token: {currency}
  Total Rewards: {total_rewards}
  Period: {start_time} ~ {end_time}
  Task Types: {rule_name localized per Task types table; locale-appropriate separator (e.g. "、" for zh-CN, ", " for English)}
  Participants: {participants}
  Max Reward Per User: {user_max_rewards}

Found {count} activities with {task_type_label} tasks.
```

---

## Scenario 4: Query activities by registration status

**Context**: User wants to see CandyDrop activities they have or have not registered for.

**Prompt Examples**:
- "Show CandyDrop activities I've registered for"
- "What CandyDrop activities have I registered for?"
- "Show CandyDrop activities I haven't joined yet"

**Expected Behavior**:
1. Map user intent to `register_status`: registered=`registered`, unregistered=`unregistered`.
2. Call `cex_launch_get_candy_drop_activity_list_v4` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with `register_status={value}`, `limit=10`, `offset=0`.
3. Note: This endpoint requires authentication for `register_status` filtering to work correctly.
4. Display formatted activity list.

**Response Template**:
```
CandyDrop Activities ({registered/unregistered})

{For each activity:}
Token: {currency}
  Total Rewards: {total_rewards}
  Period: {start_time} ~ {end_time}
  Task Types: {rule_name localized per Task types table; locale-appropriate separator (e.g. "、" for zh-CN, ", " for English)}
  Participants: {participants}
  Max Reward Per User: {user_max_rewards}

Showing {count} activities.
```

---

## Scenario 5: Query activity rules

**Context**: User wants to see the rules, prize pools, and tasks for a specific CandyDrop activity.

**Prompt Examples**:
- "Show rules for USDT CandyDrop"
- "What are the rules for the USDT CandyDrop activity?"
- "What are the prize pools for this CandyDrop?"
- "Show the task details for this CandyDrop activity"

**Expected Behavior**:
1. Extract `currency` or `activity_id` from user query. If neither, ask the user.
2. Call `cex_launch_get_candy_drop_activity_rules_v4` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with the provided parameter(s).
3. Display activity overview (currency, total rewards, period).
4. For each prize pool display: `prize_all`, `prize_limit`, and the task list.
5. For each task display: `task_name`, `task_desc`, `exclusive_label`.

**Response Template**:
```
CandyDrop Activity Rules — {currency}

Total Rewards: {total_rewards}
Period: {start_time} ~ {end_time}

Prize Pools:
{For each prize pool:}
  Prize Pool Type: {prize_pool_type mapped in user language: 1=By Candy count, 2=By amount, 3=Fixed reward}
  Total Prize: {prize_all}
  Per-User Cap: {prize_limit}
  Tasks:
{For each task:}
    - {task_name}
      Description: {task_desc}
      Exclusive Label: {exclusive_label}
```

---

## Scenario 6: Empty activity list

**Context**: User queries CandyDrop activities but no results match the filters.

**Prompt Examples**:
- "Show CandyDrop activities" (when none available)

**Expected Behavior**:
1. Call `cex_launch_get_candy_drop_activity_list_v4` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with user's filters.
2. Receive empty array.
3. Suggest alternative filters or checking back later.

**Response Template**:
```
No CandyDrop activities match your criteria.

Suggestions:
- Try removing filters (status, token, task type)
- Check back later for new activities
- Browse all activities with "Show all CandyDrop activities"
```
