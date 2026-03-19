# List Coupons

Handles Case 1 and Case 2.

---

## Workflow

Both scenarios call `cex_coupon_list_user_coupons`. Key parameters:
- `expired=0` — valid coupons only
- `coupon_type` — omit for all types (Scenario 1); set to matched enum value (Scenario 2)
- `is_task_coupon` — omit for all; `0` = regular only; `1` = task only
- `limit=20` — max per page
- `last_id` + `expire_time` — cursor pagination when `next_page=true`

Key data to extract:
- `id`, `details_id`, `is_task_coupon` — used for detail lookup and category display
- `name`, `amount`, `currency`, `status` — display fields
- `expire_time_order_by` — pagination cursor
- `next_page` — whether more results exist
- `task_title`, `task_desc`, `task_start_at`, `task_expire_at`, `task_completed_at` — task coupon fields (only when `is_task_coupon=1`)

### Status Text Mapping

Map status codes to human-readable text (no emoji):

| Status | Display Text |
|--------|--------------|
| `ACTIVATED` | Activated |
| `TO_BE_USED` | To Be Used |
| `TASK_RECEIVE_SUCCESS` | Reward Received |
| `NOT_ACTIVE` | Pending Activation |
| `TASK_START` | Task Not Started |
| `TASK_WAIT` | Task In Progress |
| `TASK_DONE` | Task Done |
| `EXPIRED` | Expired |
| `RECYCLED` | Recycled |
| `INVALID` | Invalid |
| `TASK_EXPIRED` | Task Expired |
| `TASK_NOT_STARTED_EXPIRED` | Task Not Started (Expired) |
| `USED` | Used |
| `TASK_RECEIVE_FAIL` | Reward Claim Failed |
| `UNKNOWN` | Unknown |

---

## Scenario 1: List All Available Coupons

**Context**: User wants to see all coupons currently available in their account, without specifying a type.

**Prompt Examples**:
- "What coupons do I have right now?"
- "Show my available coupons"
- "Do I have any coupons in my account?"
- "I want to check my coupons"

**Expected Behavior**:
1. Call `cex_coupon_list_user_coupons` with `expired=0`, `limit=20`
2. Split results into two groups by `is_task_coupon`: task coupons (`is_task_coupon=1`) and regular coupons (`is_task_coupon=0` or field absent)
3. Output two sections in order: **Task Coupons** first, then **Regular Coupons**. Each section uses a single merged markdown table. If a section is empty, show "(None)" under the header.
4. Use a single merged table per section — do NOT create one table per coupon.
5. No emoji anywhere — not in headers, not in status.
6. If `next_page=true`, append: *Reply "load more" to see more.*

**Column rules (apply to both task and regular coupon tables)**:

- `Type`: map `coupon_type` to the **Display Name** from the Coupon Types Reference in SKILL.md. You may translate the Display Name to match the response language, but the mapping must be exact — never swap or conflate two different coupon types. Do NOT use the `name` field from the API response as the type label.
- `Expires (Remaining)`: format as `YYYY-MM-DD (UTC) ({X} days)`. Use `< 1 day` when less than 24 hours remain. Use `Expired` if already past. The `expire_time_order_by` value is a Unix timestamp (seconds since epoch) — use a programming tool to convert it to UTC date (e.g. `python3 -c "from datetime import *; print(datetime.fromtimestamp({value}, timezone.utc).strftime('%Y-%m-%d'))"`). Batch all timestamps into a single tool call to avoid repeated invocations.

**Table columns**: `#`, `Name`, `ID`, `Type`, `Amount`, `Expires (Remaining)`, `Status`

**Empty State**: "You currently have no available coupons. You can earn coupons by completing tasks, participating in activities, or inviting friends."

**Pagination** — when user replies "load more":
1. Record `id` and `expire_time_order_by` of the last item in current list as `last_id` and `expire_time`
2. Call `cex_coupon_list_user_coupons` again with same params + `last_id` and `expire_time`
3. Append new results into the same two-section layout; repeat footer until `next_page=false`, then show: "All {N} coupon(s) loaded."

**Response Template**:

```markdown
You currently have **{N}** available coupon(s):

### Task Coupons ({M})

| # | Name | ID | Type | Amount | Expires (Remaining) | Status |
|---|------|----|------|--------|---------------------|--------|
| 1 | 10% TradFi Trading Fee Rebate Voucher | 4313033 | Commission Rebate Voucher | 2 USDT | 2026-03-17 (UTC) (< 1 day) | Task Not Started |
| 2 | TradFi Position Voucher | 4313032 | TradFi Position Voucher | 1,000 USDx | 2026-03-18 (UTC) (< 1 day) | Task Not Started |
| 3 | Position Voucher | 4313031 | Position Trial Voucher | 20 USDT | 2026-03-18 (UTC) (< 1 day) | Task In Progress |

### Regular Coupons ({K})

| # | Name | ID | Type | Amount | Expires (Remaining) | Status |
|---|------|----|------|--------|---------------------|--------|
| 1 | 1 USDT Margin Interest Voucher | 4729 | Margin Interest Discount Voucher | 10% | 2026-04-15 (UTC) (28 days) | To Be Used |
| 2 | 1 USDT Crypto Loan Interest Voucher | 1526 | Crypto Loan Interest Discount Voucher | 10% | 2026-04-20 (UTC) (33 days) | To Be Used |
| 3 | Rate Boost Voucher | 196207 | Rate Boost Voucher | 1% APR | 2026-03-19 (UTC) (1 day) | To Be Used |
```

**Important**: Use a single merged table per section. Do NOT split into one table per coupon. No emoji anywhere. Do NOT add a Notes column.

*(If empty)*: "You currently have no available coupons. You can earn coupons by completing tasks, participating in activities, or inviting friends."

**Unexpected Behavior**:
- Using one separate table per coupon row
- Using emoji in section headers, status text, or anywhere in the output
- Adding a Notes column to the list table
- Using internal `coupon_type` values instead of human-readable names
- Calling the detail API for every coupon in the list

---

## Scenario 2: Query Specific Coupon Type

**Context**: User asks whether they have a particular type of coupon.

**Prompt Examples**:
- "Do I have a futures bonus?"
- "Do I have any commission rebate vouchers?"
- "Check if I have a VIP trial card"
- "I think I have a position voucher — can you check?"

**Expected Behavior**:
1. Map user's natural language to the correct `coupon_type` enum value using Coupon Types Reference in SKILL.md
2. Call `cex_coupon_list_user_coupons` with `expired=0`, `coupon_type={matched_type}`, `limit=20`
3. Split results into two groups by `is_task_coupon`: task coupons (`is_task_coupon=1`) and regular coupons (`is_task_coupon=0` or field absent)
4. Use the same single merged table layout as Scenario 1 (same columns, same column rules). No emoji. Do NOT add a Notes column.

**Response Template**:

```markdown
You have **{N}** {coupon_name}(s):

### Task Coupons ({M})

| # | Name | ID | Type | Amount | Expires (Remaining) | Status |
|---|------|----|------|--------|---------------------|--------|
| 1 | {name} | {id} | {Display Name} | {amount} {currency} | {YYYY-MM-DD (UTC)} ({X} days) | {status text} |

### Regular Coupons ({K})

| # | Name | ID | Type | Amount | Expires (Remaining) | Status |
|---|------|----|------|--------|---------------------|--------|
| 1 | {name} | {details_id} | {Display Name} | {amount} {currency} | {YYYY-MM-DD (UTC)} ({X} days) | {status text} |
```

**Empty State**: "You currently have no {coupon_name} coupons. You can earn coupons by completing tasks, participating in activities, or inviting friends."

**Unexpected Behavior**:
- Using one separate table per coupon row
- Using emoji anywhere in the output
- Adding a Notes column to the list table
- Showing only a count without listing each coupon's fields
- Calling the detail API for every coupon in the list
