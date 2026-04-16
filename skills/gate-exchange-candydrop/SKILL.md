---
name: gate-exchange-candydrop
version: "2026.4.14-1"
updated: "2026-04-14"
description: "Gate CandyDrop activity operations guide. Use this skill whenever users want to browse CandyDrop activities, view activity rules, register for activities, check task completion progress, or query participation and airdrop records. Trigger phrases include: candydrop, candydrop activities, activity list, register for candydrop, task progress, participation records, airdrop records."
---

# Gate Exchange CandyDrop

**Authoring language:** This skill’s **instructions and reference prose** are written in **English** (Gate skill standard). **End-user replies** still follow **Language adaptation** (match the user’s locale).

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

---

## MCP Dependencies

### Required MCP Servers

| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ Required (public endpoints) |
| Gate (trading) | ✅ Required (authenticated endpoints) |

### MCP Tools Used

**Query Operations (Read-only, Public)**

- cex_launch_get_candy_drop_activity_list_v4
- cex_launch_get_candy_drop_activity_rules_v4

**Query Operations (Read-only, Auth Required)**

- cex_launch_get_candy_drop_task_progress_v4
- cex_launch_get_candy_drop_participation_records_v4
- cex_launch_get_candy_drop_airdrop_records_v4

**Execution Operations (Write)**

- cex_launch_register_candy_drop_v4

### Authentication

- API Key Required: Yes (see skill doc/runtime MCP deployment)
- Permissions: Launch:Write
- Get API Key: https://www.gate.io/myaccount/profile/api-key/manage

### Installation Check

- Required: Gate (main), Gate (trading)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this skill's CandyDrop workflow.

- `SKILL.md` keeps routing and product semantics.
- `references/mcp.md` is the authoritative MCP execution layer for activity/rule queries, registration confirmation gates, progress/record queries, and result verification.

## Module overview

| Module | Description | Trigger keywords |
|--------|-------------|------------------|
| **Activity List** | Browse CandyDrop activities, filter by status/coin/task type | `candydrop`, `candydrop activities`, `activity list`, `ongoing candydrop`, `USDT candydrop` |
| **Activity Rules** | View activity rules, prize pools, and tasks | `activity rules`, `task rules`, `prize pool`, `reward rules`, `candydrop rules` |
| **Register** | Register for a CandyDrop activity | `register`, `join activity`, `candydrop register`, `participate candydrop` |
| **Task Progress** | Query task completion progress for enrolled activities | `task progress`, `completion progress`, `progress query`, `task progress` |
| **Participation Records** | Query registration/participation history | `participation records`, `registration records`, `history records`, `participation records` |
| **Airdrop Records** | Query airdrop/reward distribution records | `airdrop records`, `reward records`, `received records`, `airdrop records` |

## Domain Knowledge

### CandyDrop concepts

| Concept | Description |
|---------|-------------|
| CandyDrop | A Gate activity platform where users complete tasks (trading, depositing, etc.) to earn airdrop rewards from prize pools. |
| Activity (`currency` / `activity_id`) | A CandyDrop campaign for a specific token. Identified by `currency` (token symbol) or `activity_id` (numeric ID). |
| Activity Status | Lifecycle: `upcoming` (upcoming) → `ongoing` (ongoing) → `ended` (ended). |
| Registration Status | `registered` (already registered) or `unregistered` (not yet registered). |
| Record Status | For participation records: `ongoing` (in progress), `awaiting_draw` (awaiting draw), `won` (won), `not_win` (not won). |
| Prize Pool | Each activity has one or more prize pools, each with a total prize amount (`prize_all`), per-user cap (`prize_limit`), and a list of tasks. |
| Task | Individual challenges within a prize pool (e.g. spot trading, futures trading, deposit, invite). Each has a name (`task_name`), description (`task_desc`), and exclusive label (`exclusive_label`). |
| Task Progress | The user's current completion value for a task (e.g. trading volume, deposit amount). Only shown for registered tasks (`task_status > 0`). |

### Timestamp formatting

- API returns time fields (e.g. `start_time`, `end_time`, `register_time`, `airdrop_time`) as **pre-formatted UTC strings** in the format `YYYY-MM-DD HH:MM:SS(UTC)`.
- **Tables / lists**: Put `(UTC)` in the **column header** when the time is UTC. If the header already says `(UTC)` (ASCII or full-width punctuation variants), **do not** repeat it on every cell: strip a trailing `(UTC)` from the API value and show **`YYYY-MM-DD HH:MM:SS`** only (example: `2026-04-13 04:04:10`, not `2026-04-13 04:04:10(UTC)`). If the header does **not** mark UTC, keep the API string as-is so the zone is not lost.
- **Other surfaces** (e.g. inline sentences without a UTC-labeled header): you may keep the API form or use header + stripped cell style consistently within one reply.
- Query parameters `start_time` / `end_time` for records are **integer unix timestamps (seconds)**. See **Timestamp strategy** in `references/records.md` for correct computation.

### Number formatting

| Category | Precision | Examples |
|----------|-----------|----------|
| Amounts (rewards, progress values) | 8 decimals, trailing zeros removed | `1.23` not `1.23000000` |
| Airdrop `rewards` (display) | Same numeric formatting, **then** append ` ` + row `currency` | `4.02032 ETH` not `4.02032` |
| Percentage-like fields | 2 decimals, trailing zeros retained | `5.20%` not `5.2%` |

### Dual-parameter resolution

Activity query interfaces support locating an activity by **either** `activity_id` or `currency`:

- `currency` (e.g. "USDT"): API auto-matches the nearest active activity for that token.
- `activity_id`: Precise numeric ID lookup.
- **Priority**: `currency` is preferred. If user provides both, use both. If only `activity_id` is given, use it directly. If neither is provided for rules/progress, ask the user for `currency`.

## Routing rules

| Intent | Example phrases | Route to |
|--------|-----------------|----------|
| **Browse activities** | "Show CandyDrop activities", "ongoing candydrop events", "USDT candydrop" | Read `references/activities.md` |
| **Activity rules** | "Show CandyDrop rules", "what tasks are in this candydrop", "prize pool details" | Read `references/activities.md` |
| **Register** | "Register for CandyDrop USDT", "join this candydrop activity" | Read `references/register.md` |
| **Task progress** | "My CandyDrop task progress", "check my candydrop task progress" | Read `references/progress.md` |
| **Participation records** | "My CandyDrop participation history", "registration records" | Read `references/records.md` |
| **Airdrop records** | "My CandyDrop airdrop rewards", "view airdrop records" | Read `references/records.md` |
| **Unclear** | "CandyDrop" | **Clarify**: browse / rules / register / progress / records, then route. If defaulting to **browse/list**, reply with **minimal activity list** only (see `references/activities.md` → *Activity list — answer directly*). |

## Execution

### 1. Intent and parameters

- Determine module (Activity List / Activity Rules / Register / Task Progress / Participation Records / Airdrop Records).
- **Register intent**: Route to `references/register.md`. Requires `currency` (required) and optionally `activity_id`. Must follow Preview-Confirm flow.
- **Records intent**: Route to `references/records.md`. Extract `currency`, `status`, `start_time`, `end_time`, `page`, `limit`.
- Extract parameters: `currency`, `activity_id`, `status`, `rule_name`, `register_status`, `limit`, `offset`, `page`, `start_time`, `end_time`.
- **Missing**: If user says "CandyDrop" without specifying intent, ask which operation or show activities by default — if showing the list, use **concise output** (title + table, no glossary; see `references/activities.md`).

### 2. Tool selection

| Module | MCP tool | Required params | Optional params |
|--------|----------|-----------------|-----------------|
| Activity List | `cex_launch_get_candy_drop_activity_list_v4` | — | `currency`, `status`, `rule_name`, `register_status`, `limit`, `offset` |
| Activity Rules | `cex_launch_get_candy_drop_activity_rules_v4` | `currency` **or** `activity_id` (at least one) | — |
| Register | `cex_launch_register_candy_drop_v4` | `currency` | `activity_id` |
| Task Progress | `cex_launch_get_candy_drop_task_progress_v4` | `currency` **or** `activity_id` (at least one) | — |
| Participation Records | `cex_launch_get_candy_drop_participation_records_v4` | — | `currency`, `status`, `start_time`, `end_time`, `page`, `limit` |
| Airdrop Records | `cex_launch_get_candy_drop_airdrop_records_v4` | — | `currency`, `start_time`, `end_time`, `page`, `limit` |

- **Register**: Show registration preview, wait for confirmation, then call `cex_launch_register_candy_drop_v4`.
- **Records**: Follow the **Timestamp strategy** in `references/records.md` for time parameter computation.

### 3. Format response

- Use the **Response Template** and field names from the reference file for the chosen module.
- **Activity List**: Optional one-line title + **data table**; for browse / “what activities are there” intents, **no** tutorial, field glossary, or pasting the task-type map — localize `rule_name` **only inside cells**. Fields: `currency`, `total_rewards`, `start_time`, `end_time`, `rule_name`, `participants`, `user_max_rewards`.
- Activity Rules: show `currency`, `total_rewards`, `start_time`, `end_time`, and per prize pool: `prize_all`, `prize_limit`, `tasks`.
- Register: show confirmation result (`success`).
- Task Progress: show `currency`, `total_rewards`, `start_time`, `end_time`, and per task: `task_name`, `task_desc`, `value`.
- Participation Records: show `currency`, `status`, `register_time`, `id` (time cells: strip trailing `(UTC)` when the table header already marks UTC — see **Timestamp formatting** above).
- Airdrop Records: show `currency`, `airdrop_time`, **`rewards` with token unit** (`{rewards} {currency}`) only — do **not** show flash-convert / USDT (`convert_amount`) (see `references/records.md`).

## Report template

After each operation, output a short standardized result consistent with the reference (e.g. activity list, rules, registration confirmation, progress, records). **Activity list** answers stay **minimal** (see `references/activities.md`). Use the API field **names** and **semantic values**; where the reference requires localization (e.g. **`rule_name` task types**), render in the user’s language per `references/activities.md` **without** embedding the whole mapping as user-visible prose.

**Language adaptation**: Always respond in the same language as the user's input. The Response Templates in reference files define the **structure and fields** to display, not the literal output language. Translate all display labels to match the user's language.

**Must localize (not tickers / not “keep English”)**:
- **`rule_name`** entries in the activity list (and anywhere shown as “task type”): use the **Task types** mapping table in `references/activities.md` — these strings describe **product task categories** (e.g. Futures, Simple Earn), not token symbols.

**Do NOT translate** (keep as-is regardless of language):
- Product name: `CandyDrop`
- Currency symbols from API: USDT, GT, BTC, DOGE, etc.
- Technical IDs and their values: `id`, `activity_id` (internal use, do NOT display unless relevant)
- Timestamp layout `YYYY-MM-DD HH:MM:SS` and the literal `(UTC)` token when it must remain visible (e.g. no UTC in header); do not drop timezone information in those cases
- API error labels: `INVALID_PARAM_VALUE`, `SERVER_ERROR`
- Numeric values, percentages, and the unit `USD` in thresholds

All other display labels should be translated to match the user's language.

## Error Handling

### API error labels

The API returns structured errors with a `label` field. Map them as follows:

| API label | User-facing message |
|-----------|---------------------|
| `INVALID_PARAM_VALUE` | "Invalid request parameters. Please check your input and try again." |
| `SERVER_ERROR` | "System busy. Please try again later." |
| `Activity not found` | "Activity not found. Please check the currency or activity ID." |
| `currency is required` | "Please provide a currency name (e.g. USDT)." |
| `Device token is required` | "Registration requires a device token. Please try from the Gate app or website." |

### Empty result handling

| Scenario | Action |
|----------|--------|
| Empty activity list | "No CandyDrop activities match your criteria. Try different filters or check back later." |
| Empty participation records | "You have no CandyDrop participation records. Browse active activities to get started." |
| Empty airdrop records | "No airdrop rewards found. Rewards are typically distributed after the activity ends." |
| Compliance restriction | "Due to compliance restrictions, CandyDrop is not available in your region." |
| API error / 401 | "Unable to fetch CandyDrop data. Please log in and try again." |

## Safety rules

### Confirmation required

- **Register is a write operation.** Before calling `cex_launch_register_candy_drop_v4`, MUST show a registration preview and wait for explicit user confirmation.
- Preview format: activity currency, activity ID (if known).
- Ask user to reply "confirm" to proceed or "cancel" to abort.
- Only call the API after receiving explicit confirmation.

### Compliance

- When the API returns a compliance or region restriction error, display a friendly message: "Due to compliance restrictions, CandyDrop is not available in your region." Do NOT retry.

### Data integrity

- Preserve `currency` and `activity_id` exactly as the user provided.
- Do NOT fabricate activity data, reward amounts, or task progress.
- Only display data returned by actual API responses.
