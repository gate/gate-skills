# Gate LaunchPool Records — Pledge History & Reward History

Query LaunchPool staking/redemption participation records and airdrop reward distribution records.

## MCP tools and parameters

| Tool | Purpose | Required | Optional |
|------|---------|----------|----------|
| **cex_launch_list_launch_pool_pledge_records** | Query pledge/redeem records | — | `coin`, `type`, `start_time`, `end_time`, `page`, `page_size` |
| **cex_launch_list_launch_pool_reward_records** | Query airdrop reward records | `page`, `page_size` | `coin`, `start_time`, `end_time` |

**IMPORTANT — Time parameter format difference:**
- **Pledge records**: `start_time` / `end_time` are **strings** in format `YYYY-MM-DD HH:MM:SS` (e.g. `"2026-03-17 00:00:00"`)
- **Reward records**: `start_time` / `end_time` are **integers** (unix timestamp in seconds, e.g. `1772323200` = 2026-03-01). See **Timestamp strategy** below for how to compute correctly.

**IMPORTANT — `coin` parameter meaning difference:**
- **Pledge records**: `coin` filters by **staking coin** (e.g. "USDT", "GT" — the coin the user staked)
- **Reward records**: `coin` filters by **reward coin** (e.g. "DOGE", "PUMP" — the airdrop token received)

Both endpoints require authentication.

**API response — `LaunchPoolV4PledgeRecord` fields:**

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Record ID |
| create_timest | string | Record creation date (e.g. "2026-03-16 09:32:22") — display as-is; put `(UTC)` in the table header, not in each row |
| reward_coin | string | Reward coin of the project (e.g. "PUMP", "DOGE") |
| coin | string | Staking coin (e.g. "USDT", "GT") |
| type | integer | Operation type: 1=Stake, 2=Redeem |
| amount | string | Staking/redeem amount |

Note: The API does **not** return project name or pid. Use `reward_coin` to identify which project the record belongs to.

**API response — `LaunchPoolV4RewardRecord` fields:**

| Field | Type | Description |
|-------|------|-------------|
| reward_timest | string | Reward distribution date — display as-is; put `(UTC)` in the table header, not in each row |
| coin | string | Reward coin (the airdrop token, e.g. "DOGE") |
| valid_mortgage_amount | string | Effective staked amount counted for this reward |
| amount_base | string | Base airdrop amount |
| amount_ext | string | Extra/bonus airdrop amount |

Note: The API does **not** return project name, pid, or staking coin. Use `coin` (reward coin) to identify the project.

---

# Part 1: Pledge Records

## Workflow

1. **Parse parameters**: Extract `coin` (staking coin), `type` (1=stake, 2=redeem), `start_time`, `end_time`, `page` from user query.
2. **Call tool**: Call `cex_launch_list_launch_pool_pledge_records` with optional filters. Time parameters must be strings in `YYYY-MM-DD HH:MM:SS` format.
3. **Key data to extract**: From each record: `id`, `create_timest`, `reward_coin`, `coin`, `type`, `amount`.
4. **Format response**: Map `type`: 1="Stake", 2="Redeem". Show as table with all fields. Use pagination info when relevant.

## Report Template

Use the **Response Template** block from the matching scenario. Show `create_timest`, `reward_coin`, `coin`, `amount`, `type` (mapped to Stake/Redeem).

**Number formatting**: For amounts use 8 decimal places precision with trailing zeros removed.

---

## Scenario 1: Query pledge records by time range

**Context**: User wants to see their LaunchPool participation history within a specific time period.

**Prompt Examples**:
- "Show my LaunchPool participation last month"
- "What LaunchPool projects did I join in the past week?"
- "My LaunchPool staking records this year"

**Expected Behavior**:
1. Parse time range from user query (e.g. "last month" → calculate start_time and end_time)
2. Call `cex_launch_list_launch_pool_pledge_records` with `start_time="{YYYY-MM-DD HH:MM:SS}"`, `end_time="{YYYY-MM-DD HH:MM:SS}"`, `page=1`
3. For each record use: `create_timest`, `reward_coin`, `coin`, `amount`, `type`
4. Map `type`: 1="Stake", 2="Redeem"

**Response Template**:
```
LaunchPool Participation Records ({time_period})

| Date (UTC) | Reward Coin | Amount | Type |
|------------|-------------|--------|------|
| {create_timest} | {reward_coin} | {amount} {coin} | Stake/Redeem |
| ... | ... | ... | ... |

Total: {total} records.
```

---

## Scenario 2: Query pledge records by staking coin

**Context**: User wants to see their participation details for a specific staking coin or project.

**Prompt Examples**:
- "Show my USDT LaunchPool staking records"
- "What's my GT participation in LaunchPool?"
- "Query my LaunchPool USDT pledge records"

**Expected Behavior**:
1. Extract staking coin from user query (e.g. "USDT"). Note: if user mentions a reward coin like "DOGE project", explain that the filter works on staking coin and suggest the correct coin.
2. Call `cex_launch_list_launch_pool_pledge_records` with `coin={staking_coin}`, `page=1`
3. For each record display: `create_timest`, `reward_coin`, `coin`, `amount`, `type`

**Response Template**:
```
LaunchPool Pledge Records (Staking Coin: {coin})

| Date (UTC) | Reward Coin | Amount | Type |
|------------|-------------|--------|------|
| {create_timest} | {reward_coin} | {amount} {coin} | Stake/Redeem |
| ... | ... | ... | ... |

Total: {total} records for {coin}.
```

---

## Scenario 3: Empty pledge records

**Context**: User queries pledge records but has no LaunchPool participation history.

**Prompt Examples**:
- "Show my LaunchPool history" (when user has none)

**Expected Behavior**:
1. Call `cex_launch_list_launch_pool_pledge_records`
2. Receive empty array with `total=0`
3. Suggest browsing active projects

**Response Template**:
```
You have no LaunchPool participation records.

To get started:
- Browse active projects with "Show LaunchPool projects"
- Find high APR options with "Highest APR LaunchPool"
```

---

# Part 2: Reward Records

## Timestamp strategy

The reward records API requires `start_time`/`end_time` as **integer unix timestamps (seconds)**, which LLMs often miscalculate. Use the following two strategies to avoid errors.

### Strategy 1 — Relative time including present → skip time params, single-page display

**When to use**: The user's time range **ends at or near now** — e.g. "recent", "latest", "last week", "last N days", "last month", "last 3 months".

**How** (strictly one page at a time — NEVER auto-fetch multiple pages):
1. Do **NOT** pass `start_time`/`end_time`. Call with `page=1` only (do not pass `page_size`, let the API use its default).
2. The API returns records in reverse chronological order (newest first).
3. From the returned records, discard any whose `reward_timest` is outside the user's intended range. **Immediately display** the remaining records to the user.
4. **Check if more pages may exist**: if the number of returned records >= 10 (API default page size) and all are within range, append a prompt: "There may be more records. Reply 'next page' to continue." Then **STOP and wait for the user's reply**. Do NOT fetch page 2 on your own.
5. If returned records < 10, or the last record is older than the range start, all data has been shown — do NOT prompt for next page.

### Strategy 2 — Historical / absolute date range → use anchor table

**When to use**: The time range **does not include the present** — e.g. "last month" (meaning the previous calendar month, not the last 30 days), "February 2026", "last year", "2025-01 to 2025-06".

**How**: Look up the anchor table below and compute `start_time`/`end_time` by simple addition. Each day = `+86400`.

```
2026 monthly anchors (1st day 00:00:00 UTC):
Jan 1 = 1767225600    Jul 1 = 1782864000
Feb 1 = 1769904000    Aug 1 = 1785542400
Mar 1 = 1772323200    Sep 1 = 1788220800
Apr 1 = 1775001600    Oct 1 = 1790812800
May 1 = 1777593600    Nov 1 = 1793491200
Jun 1 = 1780272000    Dec 1 = 1796083200

2025 reference: Jan 1 = 1735689600  (subtract 31536000 from 2026 anchors for non-leap year)
```

Example: "February 2026" → `start_time=1769904000`, `end_time=1772323200` (Mar 1, exclusive).

### Decision guide

| User expression | Ends at now? | Strategy | Pass time params? |
|-----------------|-------------|----------|-------------------|
| "recent" / "latest" / "最近的" | Yes | 1 | No |
| "last week" / "last 30 days" / "最近一个月" | Yes | 1 | No |
| "last month" (= previous calendar month) / "上个月" | No | 2 | Yes (anchor table) |
| "February 2026" / "2026年2月" | No | 2 | Yes (anchor table) |
| "last year" / "去年" | No | 2 | Yes (anchor table) |
| "2026-02-01 to 2026-03-15" | No | 2 | Yes (anchor table) |

## Workflow

1. **Determine strategy**: Check whether the user's time range includes the present moment (→ Strategy 1) or is a historical/absolute range (→ Strategy 2). See decision guide above.
2. **Parse parameters**: Extract `coin` (reward coin), `page` from user query. For Strategy 2, compute `start_time`/`end_time` using the anchor table.
3. **Call tool**: Call `cex_launch_list_launch_pool_reward_records` with `page=1` and optional filters. Do not pass `page_size` (API defaults to 10). For Strategy 1, omit time params; for Strategy 2, include them. **Fetch only ONE page per turn.**
4. **Display current page immediately**: Show records to the user (Strategy 1: after discarding out-of-range records). If there may be more records (Strategy 1: returned count >= 10 and all within range; Strategy 2: `total` >= already shown count), append a pagination prompt and **STOP — wait for the user to confirm before fetching the next page**.
5. **Key data to extract**: From each record: `reward_timest`, `coin`, `valid_mortgage_amount`, `amount_base`, `amount_ext`.
6. **Format response**: Show as table with all fields. Append pagination prompt when applicable.

## Report Template

Use the **Response Template** block from the matching scenario. Show `reward_timest`, `coin` (reward coin), `valid_mortgage_amount`, `amount_base`, `amount_ext`.

---

## Scenario 4: Query reward records by time range

**Context**: User wants to see their LaunchPool airdrop rewards within a specific time period.

**Prompt Examples**:
- "Show my LaunchPool airdrop rewards this month"
- "What LaunchPool rewards did I receive last week?"
- "My LaunchPool earnings history"
- "Show my February 2026 LaunchPool rewards"

**Expected Behavior**:

*If Strategy 1 (range includes present):*
1. Call `cex_launch_list_launch_pool_reward_records` with `page=1` — do NOT pass `start_time`/`end_time` or `page_size`
2. Discard records whose `reward_timest` is outside the user's intended range
3. **Immediately display** the remaining records to the user
4. If returned count >= 10 and all are within range, append: "There may be more records. Reply 'next page' to continue." — then **STOP and wait**

*If Strategy 2 (historical / absolute range):*
1. Compute `start_time` and `end_time` as integers using the anchor table
2. Call `cex_launch_list_launch_pool_reward_records` with `start_time={timestamp}`, `end_time={timestamp}`, `page=1` — do NOT pass `page_size`
3. **Immediately display** returned records
4. If `total` >= already shown count, append: "There are more records ({total} total). Reply 'next page' to continue." — then **STOP and wait**

**Response Template**:
```
LaunchPool Airdrop Rewards ({time_period})

| Date (UTC) | Reward Coin | Effective Staked | Base Airdrop | Extra Airdrop |
|------------|-------------|-----------------|--------------|---------------|
| {reward_timest} | {coin} | {valid_mortgage_amount} | {amount_base} {coin} | {amount_ext} {coin} |
| ... | ... | ... | ... | ... |

Showing {current_count} records.
{If more records may exist:} There may be more records. Reply "next page" to continue.
```

---

## Scenario 5: Query reward records by reward coin

**Context**: User wants to see airdrop rewards for a specific reward coin.

**Prompt Examples**:
- "Show my DOGE LaunchPool airdrop details"
- "How much PUMP did I earn from LaunchPool?"
- "Check my LaunchPool BTC rewards"

**Expected Behavior**:
1. Extract reward coin from user query (e.g. "DOGE"). Note: the `coin` parameter here filters by **reward coin**, not staking coin.
2. Call `cex_launch_list_launch_pool_reward_records` with `coin={reward_coin}`, `page=1`
3. For each record display: `reward_timest`, `coin`, `valid_mortgage_amount`, `amount_base`, `amount_ext`

**Response Template**:
```
LaunchPool Airdrop Rewards (Reward Coin: {coin})

| Date (UTC) | Effective Staked | Base Airdrop | Extra Airdrop |
|------------|-----------------|--------------|---------------|
| {reward_timest} | {valid_mortgage_amount} | {amount_base} {coin} | {amount_ext} {coin} |
| ... | ... | ... | ... |

Showing {current_count} records for {coin}.
{If total >= current_count:} There are more records. Reply "next page" to continue.
```

---

## Scenario 6: Empty reward records

**Context**: User queries reward records but has no airdrop history.

**Prompt Examples**:
- "Show my LaunchPool rewards" (when user has none)

**Expected Behavior**:
1. Call `cex_launch_list_launch_pool_reward_records` with `page=1`
2. Receive empty array with `total=0`
3. Explain reward distribution timing and suggest participation

**Response Template**:
```
No airdrop rewards found.

Rewards are typically distributed after the staking period ends. If you have active stakes, please check back after the project concludes.

To start earning:
- Browse active projects with "Show LaunchPool projects"
- Check your current stakes with "My LaunchPool staking records"
```
