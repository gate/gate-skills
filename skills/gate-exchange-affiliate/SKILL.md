---
name: gate-exchange-affiliate
version: "2026.3.25-1"
updated: "2026-03-25"
description: "Retrieves partner commission reports, displays referral trading volume and fee metrics, checks affiliate program eligibility, and returns application status for Gate Exchange partners. Use when the user asks about partner commissions, referral volume, team performance, or applying for the affiliate program. Triggers on 'my affiliate data', 'partner earnings', 'apply for affiliate', 'commission', 'referral stats', 'team report'."
---

# Gate Exchange Affiliate Program Assistant

Query and manage Gate Exchange affiliate/partner program data, including commission tracking, team performance analysis, and application guidance.

## General Rules

STOP — Read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)

Only call MCP tools explicitly listed in this skill. Tools not documented here must NOT be called, even if they exist in the MCP server.

---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate (main) | Required |

### MCP Tools Used (Read-only)

- `cex_rebate_get_partner_application_recent`
- `cex_rebate_get_partner_eligibility`
- `cex_rebate_partner_commissions_history`
- `cex_rebate_partner_sub_list`
- `cex_rebate_partner_transaction_history`

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)
- Permissions: Rebate:Read
- Get API Key: https://www.gate.io/myaccount/profile/api-key/manage

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this skill's affiliate workflow.

- `SKILL.md` keeps routing and reporting policy.
- `references/mcp.md` is the authoritative MCP execution layer for eligibility/application/commission query flow and degraded handling.

## Critical Rules (Single Source of Truth)

These rules apply throughout the entire workflow. Do not duplicate — reference this section.

### user_id parameter

The `user_id` parameter in `commission_history` and `transaction_history` filters by **trader (the referred user who traded)**, NOT the commission receiver (the partner). Only pass `user_id` when the user explicitly asks about a specific trader's contribution (e.g. "UID 123456's volume"). For "my commission", "my earnings", or any general query, **omit user_id entirely**.

### Time handling (UTC+8)

All query windows use the user's **current calendar date in UTC+8**. For relative phrases ("last 7 days", "this week", "last month"):
1. Compute start date by subtracting the requested span from today in UTC+8.
2. Convert start to `00:00:00 UTC+8` and end to `23:59:59 UTC+8`, then to Unix seconds.
3. The `to` parameter must be less than or equal to the current Unix time. Reject future dates.
4. Maximum 30 days per API request. For ranges up to 180 days, split into 30-day segments and merge results. Reject ranges exceeding 180 days.

### Data aggregation

Do NOT naively sum all values from API response lists. Instead:
1. **Group by asset**: Aggregate `commission_amount` per `commission_asset`, and `amount`/`fee` per `amount_asset`/`fee_asset`.
2. **Deduplicate**: Ensure no duplicate records across paginated or split-segment responses (match on transaction/commission time + user_id + amount).
3. **Respect period boundaries**: Only include records whose timestamps fall within the requested range.
4. **Count unique users**: Use a set of `user_id` values from `transaction_history` for trading user counts.

See [`references/api-integration.md`](./references/api-integration.md) for concrete aggregation code examples.

### Safety

- Query only data for the authenticated partner. Do not access other partners' data.
- If the API returns a sub-account indicator, direct the user to their main account.
- Show metrics as 0 (not an error) when the API returns empty data for a valid range.
- Display amounts with appropriate precision (USDT: 2 decimals, BTC: 8 decimals) and thousand separators.

## Available APIs (Partner Only)

| API Endpoint | Description | Time Limit |
|--------------|-------------|------------|
| `GET /rebate/partner/transaction_history` | Referred users' trading records | ≤30 days/request |
| `GET /rebate/partner/commission_history` | Referred users' commission records | ≤30 days/request |
| `GET /rebate/partner/sub_list` | Subordinate list (customer count) | None |
| `GET /rebate/partner/eligibility` | Check partner program eligibility | None |
| `GET /rebate/partner/applications/recent` | Recent application record (last 30 days) | None |

Agency APIs (`/rebate/agency/*`) are deprecated and not used in this skill.

For full parameter schemas, response shapes, and code examples, see [`references/api-integration.md`](./references/api-integration.md).

## Core Metrics

| Metric | Source | Calculation |
|--------|--------|-------------|
| Commission Amount | `commission_history` | Sum `commission_amount` grouped by `commission_asset` |
| Trading Volume | `transaction_history` | Sum `amount` grouped by `amount_asset` |
| Net Fees | `transaction_history` | Sum `fee` grouped by `fee_asset` |
| Customer Count | `sub_list` | `total` from response |
| Trading Users | `transaction_history` | Count of unique `user_id` values |

## Workflow

### Step 1: Parse User Query

Classify the query and extract parameters:
- **query_type**: `overview` | `time_specific` | `metric_specific` | `user_specific` | `team_report` | `application_eligibility` | `application_status` | `application` (generic guidance)
- **time_range**: Default 7 days unless user specifies otherwise
- **metric**: commission | volume | fees | customers | trading_users (for metric_specific)
- **user_id**: Specific trader UID (for user_specific only)

### Step 2: Validate and Prepare Time Range

Apply the rules from **Critical Rules > Time handling**. Determine whether splitting is needed (range >30 days). Reject ranges >180 days with an error message.

### Step 3: Call Partner APIs

Route to the correct MCP tools based on query type:

| Query Type | Tools to Call | user_id? |
|------------|--------------|----------|
| overview / time_specific | `transaction_history` + `commission_history` + `sub_list` | NO |
| metric_specific | Only the tool(s) for the requested metric | NO (unless user specifies a UID) |
| user_specific | `transaction_history` + `commission_history` with `user_id` | YES |
| team_report | All three data tools | NO |
| application_eligibility | `cex_rebate_get_partner_eligibility` | N/A |
| application_status | `cex_rebate_get_partner_application_recent` | N/A |
| application (generic) | Optionally `eligibility` first, then return guidance + portal link | N/A |

### Step 4: Paginate if Needed

When `total > limit` in the response, fetch subsequent pages (offset += 100) until all records are collected. See [`references/api-integration.md`](./references/api-integration.md) for pagination code.

### Step 5: Aggregate Data

Apply the aggregation rules from **Critical Rules > Data aggregation**. Produce the relevant core metrics.

### Step 6: Format Response

Use the report template and scenario-specific output formats documented in [`references/scenarios.md`](./references/scenarios.md) and [`references/example-queries.md`](./references/example-queries.md).

For application-related queries:
- **Eligibility**: Return `eligible` status; if blocked, show `block_reasons` and resolution guidance.
- **Application status**: Return `audit_status` (0=Pending, 1=Approved, 2=Rejected), `apply_msg`, and `jump_url`.
- **Generic guidance**: Provide application steps and portal link: `https://www.gate.com/referral/affiliate`

## Error Handling

| Condition | Response |
|-----------|----------|
| API returns 403 | "Your account does not have affiliate privileges. Apply at: https://www.gate.com/referral/affiliate" |
| Time range >180 days | "Query supports maximum 180 days of historical data. Please adjust your time range." |
| Empty data for valid range | Show metrics as 0 |
| UID not in sub_list | "UID {user_id} not found in your referral network. Please verify the user ID." |
| Invalid UID format | "Invalid UID format. UID should be a numeric value." |
| Sub-account detected | "Sub-accounts cannot query affiliate data. Please use your main account." |
| Future date requested | "Only historical data is available. Please use a past or current date." |

## Domain Knowledge

- **Partner = Affiliate**: Both terms refer to a user who refers others to Gate Exchange and earns rebate from their trading fees. Only Partner APIs are used; Agency APIs are deprecated.
- **Subordinate types**: Sub-agent (1), Indirect customer (2), Direct customer (3) — returned by `sub_list`.
- **Eligibility block reasons**: `sub_account`, `already_agent`, `kyc_incomplete`, `in_agent_tree`, `ch_code_conflict`, `user_not_exist`, `user_blacked`.
- **Application audit_status**: 0=Pending, 1=Approved, 2=Rejected.

For detailed scenarios, example queries with expected responses, and test cases, see:
- [`references/scenarios.md`](./references/scenarios.md)
- [`references/example-queries.md`](./references/example-queries.md)
- [`references/test-cases.md`](./references/test-cases.md)
