---
name: gate-exchange-affiliate
version: "2026.3.30-1"
updated: "2026-03-30"
description: "Use this skill whenever users ask about partner affiliate data, commissions, applications, or aggregated summaries. `transaction_history` and `commission_history` enforce a hard 30-day maximum per request (segment longer ranges up to 180 days); `cex_rebate_get_partner_agent_data_aggregated` supports up to 180 days in one request (do not split when ≤180 days). Trigger phrases include 'my affiliate data', 'my rebate', 'query my rebate', 'commission records', 'rebate history', 'commission', 'partner earnings', 'apply for affiliate', 'am I eligible', 'my application status', 'aggregated data', 'total summary', 'overall statistics'."
---

# Gate Exchange Affiliate Program Assistant

Query and manage Gate Exchange affiliate/partner program data, including commission tracking, team performance analysis, and application guidance.

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
| Gate (main) | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- cex_rebate_get_partner_application_recent
- cex_rebate_get_partner_eligibility
- cex_rebate_partner_commissions_history
- cex_rebate_partner_sub_list
- cex_rebate_partner_transaction_history
- cex_rebate_get_partner_agent_data_aggregated

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)
- Permissions: Rebate:Read
- Get API Key: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Important Notice

- **Role**: This skill uses Partner APIs only. The term "affiliate" in user queries refers to Partner role.
- **Time limit (list APIs) — mandatory**: `transaction_history` and `commission_history` each accept **at most 30 days of data per request** (`from`/`to` Unix window). **Never** send a single list API call spanning **more than 30 days**. For user windows **>30 days and ≤180 days**, issue **multiple** list calls with **non-overlapping 30-day segments** (or shorter last segment), then merge. This **30-day cap is unchanged** by the aggregated endpoint; it applies only to these two list endpoints.
- **Time limit (aggregated summary)**: `cex_rebate_get_partner_agent_data_aggregated` / `GET /rebate/partner/data/aggregated` supports **up to 180 days in one request** (set `start_date` / `end_date` in UTC+8). If the user’s range is **≤180 days**, use **a single aggregated call** — **do not** split into multiple aggregated queries.
- **Authentication**: Requires `X-Gate-User-Id` header with partner privileges.
- **CRITICAL - user_id Parameter**: In both `commission_history` and `transaction_history` APIs, the `user_id` parameter filters by "trader/trading user" NOT "commission receiver". Only use this parameter when explicitly querying a specific trader's contribution. For general commission queries, DO NOT use user_id parameter.
- **Data Aggregation**: When calculating totals from API response lists, use custom aggregation logic based on business rules. DO NOT simply sum all values as this may lead to incorrect results due to data structure and business logic considerations. For **rebate/commission summary** questions, prefer the **aggregated** endpoint (`rebate_amount`) instead of summing `commission_history` rows unless the user explicitly needs record-level data.

### Query time and timezone (UTC+8)

All query windows use the user's **current calendar date** in **UTC+8**. For relative phrases ("last 7 days", "last 30 days", "this week", "last month"): compute the start date by subtracting the requested span from today, convert start and end to UTC+8 00:00:00 and 23:59:59 respectively, then to Unix timestamps. **NEVER** use future timestamps as query bounds. The `to` parameter must always be ≤ current Unix time. If the user specifies a future date, reject the query and explain that only historical data is available.

## Available APIs (Partner Only)

| API Endpoint | Description | Time Limit |
|--------------|-------------|------------|
| `GET /rebate/partner/transaction_history` | Get referred users' trading records | **Hard max 30 days** per `from`/`to`; never widen a single call beyond 30 days |
| `GET /rebate/partner/commission_history` | Get referred users' commission records | **Hard max 30 days** per `from`/`to`; never widen a single call beyond 30 days |
| `GET /rebate/partner/sub_list` | Get subordinate list (for customer count) | No time parameter |
| `GET /rebate/partner/eligibility` | Check if user is eligible to apply for partner | No time parameter |
| `GET /rebate/partner/applications/recent` | Get user's recent partner application record (last 30 days) | No time parameter |
| `GET /rebate/partner/data/aggregated` | Get aggregated partner data summary | Optional `start_date`/`end_date` (UTC+8); default last 7 days if omitted; **≤180 days per single request — never split** multiple aggregated calls for one query when the window is ≤180 days |

**Note**: Agency APIs (`/rebate/agency/*`) are deprecated and not used in this skill.

### Rebate / commission intent routing (aggregated vs `commission_history`)

Use this routing whenever the user mentions rebate or commission in Chinese or English:

| User intent (examples) | Preferred API | MCP tool (when configured) |
|------------------------|---------------|----------------------------|
| **Summary or total** — how much rebate/commission overall, "my rebate", "query my rebate", "how much did I earn", rebate for a period without asking for line items | `GET /rebate/partner/data/aggregated` | `cex_rebate_get_partner_agent_data_aggregated` |
| **Records or history** — commission/rebate **records**, **history**, **list**, **ledger**, line-by-line entries, per-trade commission detail, export-style detail | `GET /rebate/partner/commission_history` | `cex_rebate_partner_commissions_history` |

**Rules**:
1. If the user asks for **totals or a dashboard-style answer** for their own rebate/commission, classify as **`aggregated_summary`** and call the aggregated endpoint **once** with `start_date`/`end_date` in UTC+8 for the full window (**up to 180 days** — **no** multi-call splitting when ≤180 days; otherwise use API default last 7 days). **Do not** use `user_id` unless they explicitly name a **trader** UID.
2. If the user asks for **records**, **history**, **list**, or **each** commission/rebate entry, classify as **`commission_records`** (or `metric_specific` with metric `commission` + list intent) and call **`commission_history`** with Unix `from`/`to`, pagination as needed. **Do not** use `user_id` for "my commission records"—only when filtering by a specific **trader**.
3. If both are asked (e.g. "total and the list"), return aggregated totals first, then offer or fetch `commission_history` for detail.

## ⚠️ CRITICAL API USAGE WARNINGS

### 30-day maximum per request (`transaction_history` / `commission_history` only)

- Each **`cex_rebate_partner_transaction_history`** / **`GET /rebate/partner/transaction_history`** call and each **`cex_rebate_partner_commissions_history`** / **`GET /rebate/partner/commission_history`** call **must** use a `from`–`to` range covering **≤30 days** of history. **Violating this is invalid** regardless of aggregated API behavior.
- For ranges longer than 30 days (up to 180 days total for partner history), **keep** segmenting into **30-day (or shorter) chunks** per call. Do **not** replace this with one 60- or 90-day list call.
- The **180-day single-call** rule applies **only** to **`cex_rebate_get_partner_agent_data_aggregated`** / **`GET /rebate/partner/data/aggregated`**, not to list APIs.

### user_id Parameter Clarification
- **NEVER use `user_id` parameter for general commission queries**
- The `user_id` parameter in both `commission_history` and `transaction_history` APIs filters by **TRADER/TRADING USER**, not commission receiver
- Only use `user_id` when explicitly querying a specific trader's contribution (e.g., "UID 123456's trading volume")
- For queries like "my commission", "my earnings", "my rebate" (summary intent) — **DO NOT use user_id**; prefer **`aggregated_summary`** for totals. For **record-list** intent, call **`commission_history`** without `user_id` unless a trader UID is given

### Data Aggregation Rules
- **DO NOT simply sum all values from API response lists**
- Use custom aggregation logic that considers:
  - Business rules and data relationships
  - Asset type grouping
  - Proper filtering and deduplication
  - Time period boundaries
- Raw summation may lead to incorrect results due to data structure complexities

## Safety Rules

- **List APIs (`transaction_history`, `commission_history`)**: **Always** enforce the **30-day maximum per request**. Never stretch one list call past 30 days; use segmented calls for longer windows (see **30-day maximum per request** above).
- **Query times (UTC+8)**: Follow **Important Notice → Query time and timezone (UTC+8)** for relative ranges, day boundaries, and Unix conversion. Never use future timestamps; `to` must be ≤ current Unix time; reject user-specified future dates.
- **user_id usage**: Use the `user_id` parameter only when the user explicitly asks about a specific trader's contribution (e.g. "UID 123456's volume"). Do not use `user_id` for "my commission" or "my earnings"—those are the partner's own totals across all referred users.
- **Data scope**: Query only data for the authenticated partner. Do not attempt to access other partners' data or to infer data outside the API responses.
- **Aggregation**: Do not sum list fields blindly. Use documented aggregation rules and respect asset types, deduplication, and period boundaries to avoid incorrect totals.
- **Sub-accounts**: If the API indicates the account is a sub-account or returns a sub_account eligibility block, direct the user to use the main account for partner data or application.

## Core Metrics

1. **Commission / rebate amount (summary)**: Prefer **`rebate_amount`** from `GET /rebate/partner/data/aggregated` when the user wants totals ("my rebate", "how much commission"). Use **`commission_history`** only when they need line-item records or when aggregated is unsuitable.
2. **Trading Volume**: Total trading amount from `transaction_history` or `trade_volume` from aggregated when using the summary endpoint
3. **Net Fees**: From `transaction_history` or `net_fee` from aggregated when using the summary endpoint
4. **Customer Count**: From `sub_list` or `customer_count` from aggregated when using the summary endpoint
5. **Trading Users**: Unique user count from `transaction_history`, or `trading_user_count` from aggregated when `business_type=0`

## Domain Knowledge

- **Partner (affiliate)**: In this skill, "affiliate" and "partner" refer to the same role: a user who refers others to trade on Gate Exchange and earns rebate (commission) from referred users' trading activity. Only Partner APIs are used; Agency APIs are deprecated.
- **Commission (rebate)**: Commission is the rebate paid to the partner from trading fees generated by referred users. **Summary totals** are served by the aggregated endpoint (`rebate_amount`). **Per-entry detail** comes from `commission_history`. See **Rebate / commission intent routing** to choose the correct API.
- **Trading volume and net fees**: These come from referred users' trading activity (spot, futures, etc.). Transaction history returns per-trade records; volume and fees must be aggregated with proper logic—do not naively sum list fields.
- **Subordinates**: Users referred by the partner. The subordinate list returns them with types: Sub-agent (1), Indirect customer (2), Direct customer (3). Customer count is the total number of subordinates; trading users is the count of unique users with trading activity in the requested period.
- **Eligibility**: Whether the current user can apply for the partner program. Checked via the eligibility API; the response includes `eligible` and, when not eligible, `block_reasons` and `block_reason_codes` (e.g. sub_account, already_agent, kyc_incomplete).
- **Application status**: The user's recent partner application (if any) within the last 30 days, including audit status (pending / approved / rejected), returned by the applications/recent API.

## Workflow
### Step 1: Parse User Query

Call `N/A` (local parsing; no MCP) with:
- Latest user message and any clarified entities (time phrases, trader UID, metric intent)

Key data to extract:
- `query_type`: overview | time_specific | metric_specific | user_specific | team_report | application | application_eligibility | application_status | aggregated_summary | commission_records
- `rebate_routing`: `aggregated_summary` | `commission_records` | unset — set from **Rebate / commission intent routing** when the user mentions rebate or commission
- `time_range`: default 7 days or user-specified period
- `metric`: commission | volume | fees | customers | trading_users (if metric-specific); for commission, distinguish **summary** (→ aggregated) vs **records** (→ commission_history)
- `user_id`: specific user ID (if user-specific query)
- `business_type`: business type filter for aggregated queries (0=all, 1=spot, 2=futures, etc.)

### Step 2: Validate Time Range

Call `N/A` (local validation; no MCP) with:
- `query_type`, `time_range`, and planned endpoints from Step 1

Key data to extract:
- `needs_splitting`: boolean — **true** only when the plan uses **`transaction_history`** and/or **`commission_history`** (e.g. overview, team report, `commission_records`) and the window is **>30 days** and **≤180 days**. **false** for **`aggregated_summary`** when the window is **≤180 days** (one aggregated call covers the full range).
- `segments`: array of time segments — **only** for list APIs when `needs_splitting` is true; **not** used for a single aggregated request ≤180 days.
- `error`: string if time range **>180 days** (applies to partner data queries overall)

### Step 3: Call Partner APIs

Call `cex_rebate_partner_transaction_history` with:
- `from`, `to` (Unix seconds, **≤30 days** per request), optional `currency_pair`, optional `user_id` (trader only when user-specific). Omit when `query_type` does not need trading list data.

Call `cex_rebate_partner_commissions_history` with:
- `from`, `to` (Unix seconds, **≤30 days** per request), optional `currency`, optional `user_id` (trader only). Omit when `query_type` does not need commission list data.

Call `cex_rebate_partner_sub_list` with:
- Optional `user_id` filter, `limit`, `offset`. Omit when subordinate list is not needed.

Call `cex_rebate_get_partner_eligibility` with:
- No parameters (authenticated context). Use for `application_eligibility` or optional pre-application checks.

Call `cex_rebate_get_partner_application_recent` with:
- No parameters (authenticated context). Use for `application_status`.

Call `cex_rebate_get_partner_agent_data_aggregated` with:
- Optional `start_date`, `end_date` (UTC+8 `yyyy-mm-dd hh:ii:ss`, **up to 180 days** in **one** call when range ≤180 days), optional `business_type`. Use for `aggregated_summary` / rebate-commission **summary** intent; **do not** split multiple aggregated calls for the same request when ≤180 days.

When MCP is unavailable, use the equivalent `GET /rebate/partner/*` paths from **API Parameter Reference**.

**CRITICAL REMINDER**: 
- DO NOT use `user_id` parameter unless explicitly querying a specific trader's contribution
- The `user_id` in API responses represents the TRADER, not the commission receiver
- For "my commission" queries, omit the user_id parameter entirely

**Routing (which calls apply)**:
- **Overview / time-specific (list path)**: `transaction_history` + `commission_history` per segment (≤30 days each) + `sub_list` as needed.
- **Aggregated summary** (including **my rebate / commission total**): `cex_rebate_get_partner_agent_data_aggregated` **once** for full window ≤180 days; no list merge for that endpoint.
- **Commission records**: `cex_rebate_partner_commissions_history` only, **≤30 days** per call, segment longer ranges; paginate when `total > limit`.
- **Metric-specific**: Only the tool(s) required; commission **summary** → aggregated tool; commission **records** → `commission_history` only.
- **User-specific**: Same list tools with `user_id` = **trader**.
- **Application**: `cex_rebate_get_partner_eligibility` and/or `cex_rebate_get_partner_application_recent` per Judgment Logic.

Key data to extract:
- `transactions`: array of trading records
- `commissions`: array of commission records
- `subordinates`: array of team members
- `aggregated_data`: pre-calculated summary data from aggregated API
- `total_count`: total records for pagination
- `eligibility`: { eligible, block_reasons, block_reason_codes } (for application_eligibility)
- `application_recent`: application record or empty (for application_status)

### Step 4: Handle Pagination

Call `cex_rebate_partner_transaction_history` with:
- Same `from`/`to` as the current segment (still **≤30 days**), increasing `offset` in steps of `limit` until all rows are retrieved when `total > limit`.

Call `cex_rebate_partner_commissions_history` with:
- Same `from`/`to` as the current segment (still **≤30 days**), increasing `offset` in steps of `limit` until all rows are retrieved when `total > limit`.

If aggregated-only or list `total <= limit` on the first page, call `N/A` (skip extra list fetches).

Key data to extract:
- `all_data`: complete dataset after pagination
- `pages_fetched`: number of API calls made

### Step 5: Aggregate Data

Call `N/A` (local computation; no MCP) with:
- Raw responses from Step 3–4; `query_type`; whether the primary source was **`cex_rebate_get_partner_agent_data_aggregated`**

**IMPORTANT**: If the answer came from **`cex_rebate_get_partner_agent_data_aggregated`**, use the API’s numeric/string fields (`rebate_amount`, `trade_volume`, etc.) directly — **do not** re-split the date range or merge multiple aggregated responses when the user window is ≤180 days.

**IMPORTANT**: Use custom aggregation logic based on business rules. DO NOT simply sum all values.
- Consider data relationships and business logic
- Handle different asset types appropriately
- Apply proper grouping and filtering rules

Key data to extract:
- `commission_amount`: aggregated commission amount with proper business logic
- `trading_volume`: aggregated trading amount with proper calculations
- `net_fees`: aggregated fees with appropriate rules
- `customer_count`: total from sub_list
- `trading_users`: count of unique user_ids

### Step 6: Format Response

Call `N/A` (local formatting; no MCP) with:
- Final metrics and metadata from Step 5; **Report Template** and **Usage Scenarios** for the active `query_type`

Key data to extract:
- `final_reply_markdown`: user-facing answer
- `citations_or_links`: dashboard / portal URLs if applicable

## Judgment Logic Summary

| Condition | Status | Action |
|-----------|--------|--------|
| Query type = overview | ✅ | Use default 7 days, call all 3 APIs |
| Query type = time_specific | ✅ | Parse time range, check if splitting needed |
| Query type = metric_specific | ✅ | Call only required API(s) for the metric |
| Query type = user_specific | ✅ | Add user_id filter to API calls (NOTE: user_id = trader, not receiver) |
| Query type = team_report | ✅ | Call all APIs, generate comprehensive report |
| Query type = aggregated_summary | ✅ | **Single** call to `cex_rebate_get_partner_agent_data_aggregated` / GET aggregated; full window up to **180 days** in UTC+8; **no splitting** if ≤180 days |
| Aggregated window >180 days | ❌ | Return error — aggregated supports at most 180 days per request |
| Query type = commission_records | ✅ | Call `commission_history` only; **≤30 days per call**; segment if needed; paginate; NO user_id unless trader-specific |
| User wants **my rebate / commission total** (summary, no line items) | ✅ | `aggregated_summary` — `cex_rebate_get_partner_agent_data_aggregated` / GET aggregated |
| User wants **commission or rebate records / history / list** | ✅ | `commission_records` — `cex_rebate_partner_commissions_history` / GET commission_history (**30-day max per call**) |
| Query type = application | ✅ | Return application guidance; optionally call eligibility or applications/recent when user asks "can I apply?" or "my application status?" |
| Query type = application_eligibility | ✅ | Call GET /rebate/partner/eligibility, return eligible status and block_reasons |
| Query type = application_status | ✅ | Call GET /rebate/partner/applications/recent, return recent application record and audit_status |
| List APIs (`transaction_history` / `commission_history`) — range ≤30 days | ✅ | Single API call per list endpoint |
| List APIs — range >30 days and ≤180 days | ✅ | Split into **30-day segments** per list endpoint |
| List APIs or aggregated — range >180 days | ❌ | Return error "Only supports queries within last 180 days" |
| Relative time description (e.g., "last 7 days") | ✅ | Calculate from current UTC+8 date, convert to 00:00:00-23:59:59 UTC+8, then to Unix timestamps |
| User specifies future date | ❌ | Reject query - only historical data available |
| `to` parameter > current timestamp | ❌ | Reject query - adjust to current time or earlier |
| API returns 403 | ❌ | Return "No affiliate privileges" error |
| API returns empty data | ⚠️ | Show metrics as 0, not error |
| Total > limit in response | ✅ | Implement pagination |
| User_id not in sub_list | ❌ | Return "User not in referral network" |
| Invalid UID format | ❌ | Return format error message |
| User asks for "my commission" (summary) | ✅ | Prefer aggregated API; DO NOT use user_id |
| User asks for "my commission" **records** / history / list | ✅ | commission_history; DO NOT use user_id unless trader UID given |
| User specifies trader UID | ✅ | Use user_id parameter to filter by that trader |
| User asks for "aggregated data" or "total summary" | ✅ | Use aggregated API for faster response |

## Report Template

```markdown
# Affiliate Data Report

**Query Type**: {query_type}
**Time Range**: {from_date} to {to_date}
**Generated**: {timestamp}

## Metrics Summary

| Metric | Value |
|--------|-------|
| Commission Amount | {commission_amount} USDT |
| Trading Volume | {trading_volume} USDT |
| Net Fees | {net_fees} USDT |
| Customer Count | {customer_count} |
| Trading Users | {trading_users} |

## Details

{Additional details based on query type:
- For user-specific: User type, join date
- For team report: Top contributors, composition breakdown
- For comparison: Period-over-period changes}

## Notes

{Any relevant notes:
- Data retrieved in X segments (if split)
- Pagination: X pages fetched
- Warnings or limitations}

---
*For more details, visit the affiliate dashboard: https://www.gate.com/referral/affiliate*
```

## Usage Scenarios

### Case 1: Overview Query (No Time Specified)

**Triggers**: "my affiliate data", "show my partner stats", "affiliate dashboard"

**Default**: Last 7 days

**Output Template**:
```
Your affiliate data overview (last 7 days):
- Commission Amount: XXX USDT
- Trading Volume: XXX USDT
- Net Fees: XXX USDT
- Customer Count: XXX
- Trading Users: XXX

For detailed data, visit the affiliate dashboard: {dashboard_url}
```

### Case 2: Time-Specific Query

**Triggers**: "commission this week", "last month's rebate", "earnings for March"

**Time Handling**:
- All times are calculated based on user's system current date in UTC+8 timezone
- Convert date ranges to UTC+8 00:00:00 (start) and 23:59:59 (end), then to Unix timestamps (list APIs) or pass UTC+8 strings to aggregated (see API reference)
- **If the answer uses only `aggregated_summary`**: **one** aggregated call for the full range **≤180 days** — **no** multi-segment splitting
- **If the answer uses `transaction_history` / `commission_history` (or overview with those)**: If ≤30 days: single call per list endpoint; if >30 days and ≤180 days: split list calls into 30-day segments
- If >180 days: Return error "Only supports queries within last 180 days"

**Agent Splitting Logic** (for >30 days):
```
Example: User requests 60 days (2026-01-01 to 2026-03-01 in UTC+8)
Convert to UTC+8 00:00:00 and 23:59:59, then to Unix timestamps:
1. 2026-01-01 00:00:00 UTC+8 to 2026-01-31 23:59:59 UTC+8 (31 days -> adjust to 30)
2. 2026-01-31 00:00:00 UTC+8 to 2026-03-01 23:59:59 UTC+8 (29 days)
Call each segment separately with converted timestamps, then merge results.
```

**Output Template**:
```
Your affiliate data for {time_range}:
- Commission Amount: XXX USDT
- Trading Volume: XXX USDT
- Net Fees: XXX USDT
- Customer Count: XXX
- Trading Users: XXX
```

### Case 3: Metric-Specific Query

**Triggers**: 
- **Commission / rebate — summary (route to aggregated)**: "my rebate", "query my rebate", "how much rebate", "how much commission", "my rebate income", "commission earnings" when the user wants a **total or overview**, not a line-item list
- **Commission / rebate — records (route to commission_history)**: "commission records", "rebate records", "commission history", "rebate history", "list my commissions", "commission ledger", "line by line commission", "each commission entry"
- Volume: "team trading volume", "total volume" (or use aggregated `trade_volume` if already answering a summary query)
- Fees: "net fees collected", "fee contribution"
- Customers: "customer count", "team size", "how many referrals"
- Trading Users: "active traders", "how many users trading"

**Routing**: Apply **Rebate / commission intent routing** before choosing tools. Summary → `cex_rebate_get_partner_agent_data_aggregated`. Records → `cex_rebate_partner_commissions_history` with pagination.

**Output Template**:
```
Your {metric_name} for the last 7 days: XXX {unit}

For detailed data, visit the affiliate dashboard: {dashboard_url}
```

### Case 4: User-Specific Contribution

**Triggers**: "UID 123456 contribution", "user 123456 trading volume", "how much commission from 123456"

**IMPORTANT**: The user_id parameter filters by "trader" not "commission receiver". This shows the trading activity and commission generated BY that specific trader, not commissions received by them.

**Parameters**: 
- Required: `user_id` (the trader's UID whose contribution you want to check)
- Optional: time range (default last 7 days)

**Output Template**:
```
UID {user_id} contribution (last 7 days):
- Commission Amount: XXX USDT (commission generated from this trader's activity)
- Trading Volume: XXX USDT (this trader's trading volume)
- Fees: XXX USDT (fees from this trader's trades)
```

### Case 5: Team Performance Report

**Triggers**: "team performance", "affiliate report", "partner analytics"

**Process**:
1. Call `sub_list` to get team members
2. Call `transaction_history` for trading data
3. Call `commission_history` for commission data
4. Aggregate and analyze

**Output Template**:
```
=== Team Performance Report ({time_range}) ===

📊 Team Overview
- Total Members: XXX (Sub-agents: X, Direct: X, Indirect: X)
- Active Users: XXX (XX.X%)
- New Members: XXX

💰 Trading Data
- Total Volume: XXX,XXX.XX USDT
- Total Fees: X,XXX.XX USDT
- Average Volume per User: XX,XXX.XX USDT

🏆 Commission Data
- Total Commission: XXX.XX USDT
- Spot Commission: XXX.XX USDT (XX%)
- Futures Commission: XXX.XX USDT (XX%)

👑 Top 5 Contributors
1. UID XXXXX - Volume XXX,XXX USDT / Commission XX.X USDT
2. ...
```

### Case 6: Aggregated Data Summary

**Triggers**: "aggregated data", "total summary", "overall statistics", "summary report", "aggregate my data", "total earnings summary", "my rebate", "query my rebate", "how much is my rebate", "rebate overview", "commission total" (when **not** asking for record list)

**Process**:
1. Call `cex_rebate_get_partner_agent_data_aggregated` (or `GET /rebate/partner/data/aggregated`) **once** with:
   - `start_date` and `end_date`: Full window in UTC+8 (`"yyyy-mm-dd hh:ii:ss"`), **up to 180 days** — **do not** issue multiple aggregated calls for ranges ≤180 days
   - `business_type`: Filter by business type (0=all, 1=spot, 2=futures, etc.)
2. Get pre-calculated aggregated metrics without segment merging
3. Format response with business type and time range information

**Parameters**:
- Optional: `start_date`, `end_date` (defaults to last 7 days if not specified; max span **180 days** per request)
- Optional: `business_type` (defaults to 0=all)

**Output Template**:
```
=== Aggregated Partner Data Summary ===

📊 Business Type: {business_type_desc}
🕐 Time Range: {time_range_desc}

💰 Financial Summary
- Rebate Amount: {rebate_amount} USDT
- Trading Volume: {trade_volume} USDT
- Net Fees: {net_fee} USDT

👥 User Statistics
- Customer Count: {customer_count}
{trading_user_count ? `- Trading Users: ${trading_user_count}` : ''}

Note: Trading user count is only available when querying all business types.
```

### Case 7: Affiliate Application Guidance

**Triggers**: "apply for affiliate", "become a partner", "join affiliate program", "can I apply?", "am I eligible?", "my application status", "recent application", "application result"

**When to call APIs**:
- User asks "can I apply?" or "am I eligible?" → Call `GET /rebate/partner/eligibility`. If eligible, return application steps; if not, return block_reasons and guidance.
- User asks "my application status" or "recent application" → Call `GET /rebate/partner/applications/recent`. Return audit_status (0=pending, 1=approved, 2=rejected), apply_msg, and jump_url.
- User only asks "how to apply" → Optionally call eligibility first, then return steps and portal.

**Eligibility response template** (after calling eligibility API):
```
Eligibility check: {eligible ? "You are eligible to apply." : "You are not eligible at this time."}
{If not eligible:}
Block reasons: {block_reasons}
Please address the above before applying.

Application Portal: https://www.gate.com/referral/affiliate
```

**Application status template** (after calling applications/recent API):
```
Your recent partner application (last 30 days):
Status: {audit_status: 0=Pending, 1=Approved, 2=Rejected}
{apply_msg}
{jump_url if provided}
```

**Generic guidance** (no API or after API response):
```
You can apply to become a Gate Exchange affiliate and earn commission from referred users' trading.

Application Process:
1. Open the affiliate application page
2. Fill in application information
3. Submit application
4. Wait for platform review

Application Portal: https://www.gate.com/referral/affiliate

Benefits:
- Earn commission from referred users
- Access to marketing materials
- Dedicated support team
- Performance analytics dashboard
```

## Error Handling

### Not an Affiliate
```
Your account does not have affiliate privileges. 
To become an affiliate, please apply at: https://www.gate.com/referral/affiliate
```

### Time Range Exceeds 180 Days
```
Query supports maximum 180 days of historical data.
Please adjust your time range.
```

### No Data Available
```
No data found for the specified time range.
Please check if you have referred users with trading activity during this period.
```

### UID Not Found
```
UID {user_id} not found in your referral network.
Please verify the user ID.
```

### UID Not a Subordinate
```
UID {user_id} is not part of your referral network.
You can only query data for users you've referred.
```

### Sub-account Restriction
```
Sub-accounts cannot query affiliate data.
Please use your main account.
```

## API Parameter Reference

### transaction_history
```
Constraint: Each request **must** use a `from`/`to` window of **≤30 days** (API limit). Segment longer ranges into multiple calls.

Parameters:
- currency_pair: string (optional) - e.g., "BTC_USDT"
- user_id: integer (optional) - IMPORTANT: This is the TRADER's ID, not commission receiver
- from: integer (required) - start timestamp (unix seconds)
- to: integer (required) - end timestamp (unix seconds)
- limit: integer (default 100) - max records per page
- offset: integer (default 0) - pagination offset

Response: {
  total: number,
  list: [{
    transaction_time, user_id (trader), group_name, 
    fee, fee_asset, currency_pair, 
    amount, amount_asset, source
  }]
}
```

### commission_history
```
Constraint: Each request **must** use a `from`/`to` window of **≤30 days** (API limit). Segment longer ranges into multiple calls.

Parameters:
- currency: string (optional) - e.g., "USDT"
- user_id: integer (optional) - IMPORTANT: This is the TRADER's ID who generated the commission
- from: integer (required) - start timestamp
- to: integer (required) - end timestamp
- limit: integer (default 100)
- offset: integer (default 0)

Response: {
  total: number,
  list: [{
    commission_time, user_id (trader), group_name,
    commission_amount, commission_asset, source
  }]
}
```

### sub_list
```
Parameters:
- user_id: integer (optional) - filter by user ID
- limit: integer (default 100)
- offset: integer (default 0)

Response: {
  total: number,
  list: [{
    user_id, user_join_time, type
  }]
}
Type: 1=Sub-agent, 2=Indirect customer, 3=Direct customer
```

### eligibility
```
GET /rebate/partner/eligibility
Parameters: none (uses authenticated user)

Response: {
  data: {
    eligible: boolean,
    block_reasons: string[],
    block_reason_codes: string[]
  }
}
block_reason_codes may include: user_not_exist, user_blacked, sub_account, already_agent, kyc_incomplete, in_agent_tree, ch_code_conflict
```

### applications/recent
```
GET /rebate/partner/applications/recent
Parameters: none (returns current user's recent application in last 30 days)

Response: {
  data: {
    id, uid, audit_status, apply_msg, create_timest, update_timest,
    proof_url, jump_url, proof_images_url_list, ...
  } or empty
}
audit_status: 0=Pending, 1=Approved, 2=Rejected
```

### data/aggregated
```
GET /rebate/partner/data/aggregated
Time window: Up to **180 days** inclusive between `start_date` and `end_date` (UTC+8). Use **one request** for the entire window when ≤180 days — **do not** split into multiple aggregated calls.

Parameters:
- start_date: string (optional) - format: "yyyy-mm-dd hh:ii:ss" (UTC+8)
- end_date: string (optional) - format: "yyyy-mm-dd hh:ii:ss" (UTC+8)
- business_type: integer (optional, default 0) - business type filter
  0=All, 1=Spot, 2=Futures, 3=Alpha, 4=Web3, 5=Perps(DEX), 
  6=Exchange All, 7=Web3 All, 8=TradFi

Response: {
  code: 0,
  message: "success",
  data: {
    rebate_amount: string,      // Commission amount with up to 6 decimals
    trade_volume: string,       // Trading volume with up to 6 decimals
    net_fee: string,           // Net fees with up to 6 decimals
    customer_count: integer,    // Total customer count
    trading_user_count: integer|null,  // Only available when business_type=0
    time_range_desc: string,    // e.g., "2024-01-01 ~ 2024-01-07"
    business_type: integer,
    business_type_desc: string  // e.g., "All", "Spot", "Futures"
  }
}
```

## Pagination Strategy

For complete data retrieval when total > limit:
```python
offset = 0
all_data = []
while True:
    result = call_api(limit=100, offset=offset)
    all_data.extend(result['list'])
    if len(result['list']) < 100 or offset + 100 >= result['total']:
        break
    offset += 100

# IMPORTANT: Apply custom aggregation logic after collecting all data
# DO NOT simply sum values - consider business rules and data relationships
```

## Time Handling

- API accepts Unix timestamps in seconds (not milliseconds)
- **⚠️ CRITICAL TIME CALCULATION RULES**:
  - All query times are calculated based on the user's system current date (UTC+8 timezone)
  - For any relative time description ("last 7 days", "last 30 days", "this week", "last month", etc.):
    1. Get current system date in UTC+8 timezone
    2. Calculate the start date by subtracting the requested days from current date
    3. Convert both dates to UTC+8 00:00:00 (start of day) and 23:59:59 (end of day)
    4. Convert these UTC+8 times to Unix timestamps
    5. Use these timestamps for API calls
  - **NEVER use future timestamps as query conditions**
  - The `to` parameter must always be ≤ current Unix timestamp
  - If user specifies a future date, reject the query and explain only historical data is available

- **Time Conversion Examples** (assuming current date is 2026-03-13 in UTC+8):
  - "last 7 days" query:
    - Start date: 2026-03-07 (7 days ago)
    - from: 2026-03-07 00:00:00 UTC+8 → Unix timestamp
    - to: 2026-03-13 23:59:59 UTC+8 → Unix timestamp
  - "last 30 days" query:
    - Start date: 2026-02-12 (30 days ago)
    - from: 2026-02-12 00:00:00 UTC+8 → Unix timestamp
    - to: 2026-03-13 23:59:59 UTC+8 → Unix timestamp
  - "this week" query (assuming week starts Monday):
    - Start date: 2026-03-09 (Monday of current week)
    - from: 2026-03-09 00:00:00 UTC+8 → Unix timestamp
    - to: 2026-03-13 23:59:59 UTC+8 → Unix timestamp

- **List APIs** (`transaction_history`, `commission_history`): maximum **30 days** per request; split into segments if the window is longer (up to 180 days total).
- **Aggregated** (`cex_rebate_get_partner_agent_data_aggregated`): maximum **180 days** in **one** request; **no** splitting when the user range is ≤180 days.

## Amount Formatting

- Convert string amounts to numbers for calculation
- Display with appropriate precision (USDT: 2 decimals, BTC: 8 decimals)
- Add thousand separators for large numbers

## Validation Examples

### Golden Queries (Test Cases)

1. **Basic Overview**
   - Query: "Show my affiliate data"
   - Expected: Display last 7 days metrics

2. **Time Range**
   - Query: "Commission for last 60 days"
   - Expected: Split into 2x30-day requests, aggregate results

3. **Specific Metric**
   - Query: "How many customers do I have?"
   - Expected: Call sub_list, return total count

4. **User Contribution**
   - Query: "UID 12345 trading volume this month"
   - Expected: Call transaction_history with user_id filter

5. **Error Case**
   - Query: "Data for last 200 days"
   - Expected: Error message about 180-day limit

6. **Application**
   - Query: "How to become an affiliate?"
   - Expected: Application guidance without API calls

7. **Aggregated Summary**
   - Query: "Show me my aggregated data for last month"
   - Expected: **Single** call to `cex_rebate_get_partner_agent_data_aggregated` with full UTC+8 range (≤180 days); **no** multi-segment splitting

8. **Aggregated — long window (≤180 days)**
   - Query: "Aggregated partner summary for the last 90 days"
   - Expected: **One** aggregated call covering all 90 days; do not split into three 30-day aggregated requests

9. **My rebate / commission total (summary)**
   - Query: "Query my rebate" / "How much rebate did I get this week?"
   - Expected: Classify as `aggregated_summary`; call `cex_rebate_get_partner_agent_data_aggregated` (or GET aggregated); present `rebate_amount`; no `user_id`

10. **Commission / rebate records (line items)**
   - Query: "Show my commission records" / "Rebate history for last 7 days"
   - Expected: Classify as `commission_records`; call `cex_rebate_partner_commissions_history` with `from`/`to`; paginate; no `user_id` unless a trader UID is specified
