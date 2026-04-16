# Gate CandyDrop Task Progress — Completion Tracking

Query task completion progress for enrolled CandyDrop activities.

## MCP tool and parameters

| Tool | Purpose | Required | Optional |
|------|---------|----------|----------|
| **cex_launch_get_candy_drop_task_progress_v4** | Query task progress for enrolled user | `currency` **or** `activity_id` (at least one) | — |

- **cex_launch_get_candy_drop_task_progress_v4**: Requires API Key authentication.
- Must provide at least one of `currency` or `activity_id`.
- If `currency` is provided without `activity_id`, API auto-matches the nearest valid activity.
- Only shows progress for tasks the user has already registered for (`task_status > 0`).

**API response — Task Progress (`CandyDropV4TaskProgress`):**

| Field | Type | Description |
|-------|------|-------------|
| currency | string | Token/project name |
| total_rewards | string | Total prize pool amount |
| start_time | string | Activity start time (pre-formatted UTC string) |
| end_time | string | Activity end time (pre-formatted UTC string) |
| tasks | array | List of registered task progress items (see below) |

**API response — Task Progress Item (`CandyDropV4TaskProgressItem`):**

| Field | Type | Description |
|-------|------|-------------|
| task_name | string | Task main title |
| task_desc | string | Task subtitle |
| value | string | Current progress value (e.g. trading volume, deposit amount) |

---

## Workflow

1. **Parse parameters**: Extract `currency` or `activity_id` from user query. If neither, ask the user for `currency`.
2. **Call tool**: Call `cex_launch_get_candy_drop_task_progress_v4` with the provided parameter(s).
3. **Key data to extract**: `currency`, `total_rewards`, `start_time`, `end_time`, and per task: `task_name`, `task_desc`, `value`.
4. **Format response**: Show activity overview followed by task progress list. Use the Response Template from the matching scenario.

## Report Template

Show activity overview first, then task progress items.

---

## Scenario 1: Query task progress by token

**Context**: User wants to see their task completion progress for a CandyDrop activity by token name.

**Prompt Examples**:
- "Show my USDT CandyDrop task progress"
- "Check my USDT CandyDrop task progress"
- "What's my progress on the BTC CandyDrop tasks?"

**Expected Behavior**:
1. Extract `currency` from user query (e.g. "USDT").
2. Call `cex_launch_get_candy_drop_task_progress_v4` with `currency={value}`.
3. For each registered task display: `task_name`, `task_desc`, `value`.
4. Show activity period info.

**Response Template**:
```
CandyDrop Task Progress — {currency}

Total Rewards: {total_rewards}
Period: {start_time} ~ {end_time}

Task Progress:
{For each task:}
  - {task_name}
    Description: {task_desc}
    Current Progress: {value}

Total: {count} tasks in progress.
```

---

## Scenario 2: Query task progress by activity ID

**Context**: User wants to see their task completion progress for a specific activity by ID.

**Prompt Examples**:
- "Show my task progress for CandyDrop activity 12345"
- "Query task progress for CandyDrop activity ID 12345"

**Expected Behavior**:
1. Extract `activity_id` from user query (e.g. 12345).
2. Call `cex_launch_get_candy_drop_task_progress_v4` with `activity_id={value}`.
3. For each registered task display: `task_name`, `task_desc`, `value`.

**Response Template**:
```
CandyDrop Task Progress — Activity {activity_id}

Token: {currency}
Total Rewards: {total_rewards}
Period: {start_time} ~ {end_time}

Task Progress:
{For each task:}
  - {task_name}
    Description: {task_desc}
    Current Progress: {value}

Total: {count} tasks in progress.
```
