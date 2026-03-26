# Coupon Detail

Handles Case 3, Case 4, and Case 5.

---

## Shared Execution Steps

Before executing any scenario below:

1. Extract `coupon_type` from the user's message using Coupon Types Reference in SKILL.md. If unclear, ask: "Which coupon are you referring to?"
2. Call `cex_coupon_list_user_coupons` with `expired=0`, `coupon_type={matched_type}`, `limit=20`
3. If no coupon found of this type → "You currently have no {coupon_name} coupons. You can earn coupons by completing tasks, participating in activities, or inviting friends."
4. If multiple coupons of the same type exist, present a numbered list and ask user to select:
   ```
   You have {N} {coupon_name}(s). Which one would you like to check?
   1. {amount} {currency} — expires {date}
   2. ...
   ```
5. Call `cex_coupon_get_user_coupon_detail` with:
   - `coupon_type`: matched type
   - `detail_id`: `details_id` for regular coupons (`is_task_coupon=0`); `id` for task coupons (`is_task_coupon=1`)
   - `is_task_coupon`: `0` or `1`

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

### Formatting Rules for `extra` item types

- `timestamp` → `YYYY-MM-DD HH:mm` in **UTC**. The value is a Unix timestamp (seconds since epoch). Use a programming tool to convert it (e.g. `python3 -c "from datetime import *; print(datetime.fromtimestamp({value}, timezone.utc).strftime('%Y-%m-%d %H:%M'))"`). Append ` (UTC)` suffix to the result.
- `day` → `{N} day(s)`
- `hour` → `{N} hour(s)`
- `status` → human-readable text from Status Text Mapping above (no emoji prefix)
- `string` → display as-is
- `btn` → display the value as plain text (button label); do not render as a link or interactive element

### Core Attributes vs Time Info grouping

The `extra` array has up to 3 blocks by index:

- `extra[0]` → Name / Source / Status header (rendered separately, not in Core Attributes or Time Info)
- `extra[1]` → **Core Attributes**
- `extra[2]` → **Time Info**

Use the block index directly — do NOT classify by key text content. If a block is absent or empty, omit that section entirely.

### Task Coupon Extra Time Fields

For task coupons (`is_task_coupon=1`), additionally append the following top-level fields to the **Time Info** section if their value is non-zero:

| Field | Display Label | Format |
|-------|--------------|--------|
| `task_start_at` | Task Start Time | `YYYY-MM-DD HH:mm (UTC)` |
| `task_expire_at` | Task Expires At | `YYYY-MM-DD HH:mm (UTC)` |
| `task_completed_at` | Task Completed At | `YYYY-MM-DD HH:mm (UTC)` |

All three are Unix timestamps (seconds, UTC+0). Skip any field whose value is `0`. Convert using a programming tool, same as other timestamp fields.

---

## Scenario 1: Query Coupon Details

**Context**: User asks about a specific field or the full details of a coupon. Triggered by coupon name combined with any field keyword.

**Trigger Field Keywords**: expiry, market, leverage, amount, cashback ratio, remaining balance, used balance, applicable market, usage records, acquired time, activation validity, usage duration, activation time, max leverage, trading pairs, position duration, capital amount, VIP level, benefit duration, min copy amount, available traders, rate boost cap, rate boost ratio, rate boost days, applicable earn types, available currencies, available products, min purchase amount, applicable robots, stop-loss amount, runtime, deduction cap, deduction ratio, usage conditions, applicable fiat, max discount, rate reduction ratio, loan amount limit, reduction duration, reduction start/expiry time

**Prompt Examples**:
- "When does my futures bonus expire?"
- "What market can I use my position voucher on?"
- "Tell me everything about my commission rebate voucher"
- "What's the leverage for my position voucher?"

**Expected Behavior**:
1. Follow Shared Execution Steps above
2. Parse all `extra` blocks from the detail response
3. Output using the structured card format below

Source extraction: `extra[0]` always contains a name item (`type: "string"`) and a status item (`type: "status"`). A source item (`type: "string"`) may exist between them. If `extra[0]` has 3 items, the 2nd item is the source; if only 2 items, the source is absent. When absent or value is `""`, display `"Platform reward"`.

**Response Template**:

- The heading and **Type** field both use the **Display Name** from Coupon Types Reference in SKILL.md, mapped from `coupon_type`. Use exactly as written — do NOT translate or abbreviate.

```markdown
### {amount} {currency} {Display Name}

| Field | Value |
|-------|-------|
| **Name** | {name from extra[0] first item} |
| **Type** | {Display Name from Coupon Types Reference in SKILL.md} |
| **Source** | {source value, default "Platform reward" if absent or empty} |
| **Status** | {status display text} |

#### Core Attributes

| Field | Value |
|-------|-------|
| **{key}** | {formatted value} |
| ... | ... |

#### Time Info

| Field | Value |
|-------|-------|
| **{key}** | {formatted value} |
| ... | ... |
```

**Example**:

```markdown
### 7 USDT Commission Rebate Voucher

| Field | Value |
|-------|-------|
| **Name** | 100% Spot Trading Fee Rebate Voucher |
| **Type** | Commission Rebate Voucher |
| **Source** | test_english |
| **Status** | Activated |

#### Core Attributes

| Field | Value |
|-------|-------|
| **Voucher Amount** | 7 USDT |
| **Rebate Percentage** | 100% |
| **Balance** | 7 USDT |
| **Used Amount** | 0 USDT |
| **Applicable Market** | Spot |

#### Time Info

| Field | Value |
|-------|-------|
| **Obtained At** | 2026-03-18 02:04 (UTC) |
| **Usage Duration** | 3 day(s) |
| **Activation Time** | 2026-03-18 02:04 (UTC) |
```

**Unexpected Behavior**:
- Using emoji anywhere in the output
- Showing raw type codes from `extra` instead of formatted values
- Omitting fields from any of the `extra` blocks
- Displaying raw Unix timestamps instead of formatted UTC datetime strings

---

## Scenario 2: Query Usage Rules

**Context**: User asks about the rules or conditions for using a coupon.

**Prompt Examples**:
- "What are the usage rules for my futures bonus?"
- "How do I use my commission rebate voucher?"
- "What conditions must I meet to use my position voucher?"

**Expected Behavior**:
1. Follow Shared Execution Steps above
2. Output using a callout-style blockquote:

**Response Template**:

```markdown
### Usage Rules — {amount} {currency} {coupon_name}

> {rule_new content, each ###### heading rendered as a numbered item}
```

If `rule_new` is empty, extract and display relevant restriction fields from `extra` blocks as a table:

```markdown
### Usage Rules — {amount} {currency} {coupon_name}

| Restriction | Value |
|-------------|-------|
| **{key}** | {value} |
| ... | ... |
```

If still nothing: "No usage rules are available for this coupon at this time."

**Example**:

```markdown
### Usage Rules — 7 USDT Commission Rebate Voucher

1. Users can enjoy a partial trading fee rebate on applicable markets, during the validity period of Trading Fee Rebate Voucher.
2. Trade first, rebate later. The trading fee rebate will be credited to your account within 24 hours after the trade is completed.
3. Rebate Amount = Net Trading Fee Incurred Daily × Rebate Percentage. Net trading fees exclude commissions.
4. Trading Fee Rebate Voucher can be used multiple times.
5. If multiple vouchers applicable to the same market are activated at the same time, they will be applied in order.
6. Bots, Copy, and trades using Futures Bonus or Futures Voucher cannot enjoy rebates.
```

**Unexpected Behavior**:
- Returning empty or "no rules" without first checking `extra` blocks for restriction fields

---

## Scenario 3: Query Coupon Source

**Context**: User wants to know how they acquired a specific coupon.

**Prompt Examples**:
- "How did I get my futures bonus?"
- "Where did my commission rebate voucher come from?"
- "What activity gave me this coupon?"

**Expected Behavior**:
1. Follow Shared Execution Steps above
2. In `extra[0]`: if it has 3 items, the 2nd item is the coupon source; if only 2 items, the source is absent. When absent or value is `""`, default to `"Platform reward"`.
3. Output:

**Response Template**:

```markdown
Your **{amount} {currency} {coupon_name}** was acquired through: **{source}**.
```

Fallback (if the source is absent or its value is empty):

```markdown
Your **{amount} {currency} {coupon_name}** was acquired through: **Platform reward**.
```

If `from_task=true`, append on the next line:
```markdown
> This coupon was earned by completing a task.
```

**Unexpected Behavior**:
- Using emoji anywhere in the output
- Returning "Platform reward" without first checking the source item in `extra[0]`
