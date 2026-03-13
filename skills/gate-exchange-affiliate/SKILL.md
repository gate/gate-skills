---
name: gate-exchange-affiliate
version: "2026.3.13"
updated: "2026-03-13"
description: "Gate Exchange affiliate program data query and management skill. Use this skill when users ask about their affiliate/partner commission, trading volume, net fees, customer count, trading users, or want to apply for the affiliate program. Supports queries for up to 180 days (API limited to 30 days per request, agent should split longer queries). IMPORTANT: user_id parameter in APIs refers to 'trader' not 'commission receiver' - avoid using unless explicitly specified. Aggregated data from API lists should be calculated using custom scripts, not simple summation. CRITICAL TIME CONSTRAINT: All query times are calculated based on user's system current date in UTC+8 timezone. For relative time descriptions (e.g., 'last 7 days', 'last 30 days', 'this week', 'last month'), calculate start date by subtracting days from current date, then convert both start and end dates to UTC+8 00:00:00 and 23:59:59 respectively, then convert to Unix timestamps. NEVER use future timestamps as query conditions. When timestamps are needed, obtain them via system functions, never generate manually. The 'to' parameter must always be less than or equal to the current Unix timestamp. Trigger phrases include 'my affiliate data', 'commission this week', 'partner earnings', 'team performance', 'customer trading volume', 'rebate income', 'apply for affiliate'."
---

# Gate Exchange Affiliate Program Assistant

Query and manage Gate Exchange affiliate/partner program data, including commission tracking, team performance analysis, and application guidance.

## General Rules

Read and follow the shared runtime rules before proceeding:
→ [exchange-runtime-rules.md](../exchange-runtime-rules.md)

## Important Notice

- **Role**: This skill uses Partner APIs only. The term "affiliate" in user queries refers to Partner role.
- **Time Limit**: API supports maximum 30 days per request. For queries >30 days (up to 180 days), agent must split into multiple 30-day segments.
- **Authentication**: Requires `X-Gate-User-Id` header with partner privileges.
- **CRITICAL - user_id Parameter**: In both `commission_history` and `transaction_history` APIs, the `user_id` parameter filters by "trader/trading user" NOT "commission receiver". Only use this parameter when explicitly querying a specific trader's contribution. For general commission queries, DO NOT use user_id parameter.
- **Data Aggregation**: When calculating totals from API response lists, use custom aggregation logic based on business rules. DO NOT simply sum all values as this may lead to incorrect results due to data structure and business logic considerations.
- **⚠️ CRITICAL - Time Constraint**: All query times are calculated based on the user's system current date in UTC+8 timezone. For relative time descriptions like "last 7 days", "last 30 days", "this week", "last month", etc., calculate the start date by subtracting the requested days from the current date, then convert both start and end dates to UTC+8 00:00:00 and 23:59:59 respectively, then convert these times to Unix timestamps. **NEVER use future timestamps as query conditions**. The `to` parameter must always be ≤ current timestamp. If user specifies a future date, reject the query and explain that only historical data is available.

## Available APIs (Partner Only)

| API Endpoint | Description | Time Limit |
|--------------|-------------|------------|
| `GET /rebate/partner/transaction_history` | Get referred users' trading records | ≤30 days per request |
| `GET /rebate/partner/commission_history` | Get referred users' commission records | ≤30 days per request |
| `GET /rebate/partner/sub_list` | Get subordinate list (for customer count) | No time parameter |

**Note**: Agency APIs (`/rebate/agency/*`) are deprecated and not used in this skill.

## ⚠️ CRITICAL API USAGE WARNINGS

### user_id Parameter Clarification
- **NEVER use `user_id` parameter for general commission queries**
- The `user_id` parameter in both `commission_history` and `transaction_history` APIs filters by **TRADER/TRADING USER**, not commission receiver
- Only use `user_id` when explicitly querying a specific trader's contribution (e.g., "UID 123456's trading volume")
- For queries like "my commission", "my earnings", "my rebate" - **DO NOT use user_id parameter**

### Data Aggregation Rules
- **DO NOT simply sum all values from API response lists**
- Use custom aggregation logic that considers:
  - Business rules and data relationships
  - Asset type grouping
  - Proper filtering and deduplication
  - Time period boundaries
- Raw summation may lead to incorrect results due to data structure complexities

## Core Metrics

1. **Commission Amount**: Total rebate earnings from `commission_history`
2. **Trading Volume**: Total trading amount from `transaction_history`
3. **Net Fees**: Total fees collected from `transaction_history`
4. **Customer Count**: Total subordinates from `sub_list`
5. **Trading Users**: Unique user count from `transaction_history`

## Workflow

### Step 1: Parse User Query

Identify the query type and extract parameters.

Key data to extract:
- `query_type`: overview | time_specific | metric_specific | user_specific | team_report | application
- `time_range`: default 7 days or user-specified period
- `metric`: commission | volume | fees | customers | trading_users (if metric-specific)
- `user_id`: specific user ID (if user-specific query)

### Step 2: Validate Time Range

Check if the requested time range is valid and determine if splitting is needed.

Key data to extract:
- `needs_splitting`: boolean (true if >30 days)
- `segments`: array of time segments if splitting needed
- `error`: string if time range >180 days

### Step 3: Call Partner APIs

Based on query type, call the appropriate Partner APIs.

**CRITICAL REMINDER**: 
- DO NOT use `user_id` parameter unless explicitly querying a specific trader's contribution
- The `user_id` in API responses represents the TRADER, not the commission receiver
- For "my commission" queries, omit the user_id parameter entirely

For overview or time-specific queries:
- Call `/rebate/partner/transaction_history` with time parameters (NO user_id)
- Call `/rebate/partner/commission_history` with time parameters (NO user_id)
- Call `/rebate/partner/sub_list` for customer count

For metric-specific queries:
- Call only the required API(s) based on the metric (NO user_id unless specified)

For user-specific queries:
- Call APIs with `user_id` parameter (this shows that specific trader's contribution)

Key data to extract:
- `transactions`: array of trading records
- `commissions`: array of commission records
- `subordinates`: array of team members
- `total_count`: total records for pagination

### Step 4: Handle Pagination

If `total > limit`, implement pagination to retrieve all data.

Key data to extract:
- `all_data`: complete dataset after pagination
- `pages_fetched`: number of API calls made

### Step 5: Aggregate Data

Calculate the requested metrics from the raw API responses.

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

Generate the appropriate response based on query type using the templates.

## Judgment Logic Summary

| Condition | Status | Action |
|-----------|--------|--------|
| Query type = overview | ✅ | Use default 7 days, call all 3 APIs |
| Query type = time_specific | ✅ | Parse time range, check if splitting needed |
| Query type = metric_specific | ✅ | Call only required API(s) for the metric |
| Query type = user_specific | ✅ | Add user_id filter to API calls (NOTE: user_id = trader, not receiver) |
| Query type = team_report | ✅ | Call all APIs, generate comprehensive report |
| Query type = application | ✅ | Return application guidance without API calls |
| Time range ≤30 days | ✅ | Single API call per endpoint |
| Time range >30 days and ≤180 days | ✅ | Split into multiple 30-day segments |
| Time range >180 days | ❌ | Return error "Only supports queries within last 180 days" |
| Relative time description (e.g., "last 7 days") | ✅ | Calculate from current UTC+8 date, convert to 00:00:00-23:59:59 UTC+8, then to Unix timestamps |
| User specifies future date | ❌ | Reject query - only historical data available |
| `to` parameter > current timestamp | ❌ | Reject query - adjust to current time or earlier |
| API returns 403 | ❌ | Return "No affiliate privileges" error |
| API returns empty data | ⚠️ | Show metrics as 0, not error |
| Total > limit in response | ✅ | Implement pagination |
| User_id not in sub_list | ❌ | Return "User not in referral network" |
| Invalid UID format | ❌ | Return format error message |
| User asks for "my commission" | ✅ | DO NOT use user_id parameter - query all commissions |
| User specifies trader UID | ✅ | Use user_id parameter to filter by that trader |

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
- Convert date ranges to UTC+8 00:00:00 (start) and 23:59:59 (end), then to Unix timestamps
- If ≤30 days: Single API call
- If >30 days and ≤180 days: Split into multiple 30-day segments
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
- Commission: "my rebate income", "commission earnings", "how much commission"
- Volume: "team trading volume", "total volume"
- Fees: "net fees collected", "fee contribution"
- Customers: "customer count", "team size", "how many referrals"
- Trading Users: "active traders", "how many users trading"

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

### Case 6: Affiliate Application Guidance

**Triggers**: "apply for affiliate", "become a partner", "join affiliate program"

**Output** (No API call needed):
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

- Maximum 30 days per API request, split if needed

## Amount Formatting

- Convert string amounts to numbers for calculation
- Display with appropriate precision (USDT: 2 decimals, BTC: 8 decimals)
- Add thousand separators for large numbers

## MCP Dependencies

This skill requires the following MCP tools to be installed:
- `gate-mcp` with rebate/partner endpoints enabled

If not installed, prompt user to install via:
```bash
npm install -g gate-mcp
```

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