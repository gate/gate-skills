# Account Book (Transaction History)

This module handles Alpha account transaction history queries, supporting recent and custom time-range lookups.

## Workflow

### Step 1: Identify Query Type

Classify the request into one of two cases:
1. View recent transaction history (e.g., last 7 days)
2. View transaction history for a specific time range

### Step 2: Call Tools and Extract Data

Use the minimal tool set required:
- Transaction history: `cex_alpha_list_alpha_account_book`

Key parameters:
- `from` (required): start time as Unix timestamp in seconds
- `to` (optional): end time as Unix timestamp in seconds; defaults to current time if omitted
- `page`: page number for pagination
- `limit`: max results per page

Time conversion guidelines:
- "最近一周" / "last 7 days" → `from` = current time - 7 * 86400
- "昨天" / "yesterday" → `from` = start of yesterday (00:00:00), `to` = end of yesterday (23:59:59)
- "最近 24 小时" / "last 24 hours" → `from` = current time - 86400
- "这个月" / "this month" → `from` = start of current month (1st day 00:00:00)

Key data to extract from each record:
- `time`: transaction timestamp
- `currency`: token symbol
- `change`: amount changed (positive = inflow, negative = outflow)
- `balance`: balance after this transaction

### Step 3: Return Formatted Result

Present transaction history in a clear, chronological format.

## Report Template

```markdown
## Alpha Transaction History

| Time | Currency | Change | Balance After |
|------|----------|--------|---------------|
| {time} | {currency} | {change} | {balance} |

| **Period** | {from_date} — {to_date} |
| **Records Found** | {count} |
```

---

## Scenario 16: View Recent Transaction History

**Context**: User wants to see recent asset changes in their Alpha account.

**Prompt Examples**:
- "最近一周的资产变动记录"
- "Show me recent Alpha transactions"
- "最近有什么资产变动？"

**Expected Behavior**:
1. Determine the time range from the user's request. If unspecified, default to the last 7 days.
2. Calculate the `from` Unix timestamp (e.g., current time - 7 * 86400 for 7 days).
3. Call `cex_alpha_list_alpha_account_book` with `from={timestamp}`.
4. Present the transaction history in a chronological table with time, currency, change amount, and post-transaction balance.
5. If there are more pages, inform the user and offer to show the next page.
6. If no records are found, inform the user that there are no transactions in the specified period.

## Scenario 17: View Transaction History for Specific Period

**Context**: User wants to see asset changes within a specific time window.

**Prompt Examples**:
- "看看昨天的资产变动"
- "Show me transactions from March 10 to March 15"
- "上周一到上周五的流水"

**Expected Behavior**:
1. Parse the user's time range description and convert to Unix timestamps for `from` and `to`.
2. Call `cex_alpha_list_alpha_account_book` with `from={start_timestamp}` and `to={end_timestamp}`.
3. Present the transaction history in a chronological table.
4. If there are more pages, inform the user and offer to show the next page.
5. If no records are found, inform the user that there are no transactions in the specified period.
