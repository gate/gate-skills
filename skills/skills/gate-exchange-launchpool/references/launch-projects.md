# Gate LaunchPool Projects — Browse & Filter

Browse available LaunchPool projects with filtering and sorting.

## MCP tools and parameters

| Tool | Purpose | Required | Optional |
|------|---------|----------|----------|
| **cex_launch_list_launch_pool_projects** | Query project list | `page`, `page_size` | `status`, `sort_type`, `mortgage_coin`, `search_coin`, `limit_rule` |

- Returns a paginated array of `LaunchPoolV4Project` objects
- No authentication required
- `status`: 0=All, 1=In progress, 2=Warming up, 3=Ended, 4=In progress + Warming up
- `sort_type`: 1=Max estimated APR descending, 2=Max estimated APR ascending
- `mortgage_coin`: Staking currency exact match (e.g. "USDT")
- `search_coin`: Reward currency & project name fuzzy match
- `limit_rule`: 0=Normal pool, 1=Newbie pool

**API response — `LaunchPoolV4Project` fields:**

| Field | Type | Description |
|-------|------|-------------|
| pid | integer | Project ID |
| name | string | Project name (also the reward coin symbol, e.g. "DOGE") |
| total_amount | string | Total reward amount for this project |
| start_timest | integer | Activity start timestamp (unix seconds) — internal only, do NOT display |
| end_timest | integer | Activity end timestamp (unix seconds) — internal only, do NOT display |
| days | integer | Staking period in days |
| project_state | integer | Project status: 1=In progress, 2=Warming up, 3=Ended |
| reward_pools | array | List of reward pools (see below) |

**API response — `LaunchPoolV4RewardPool` fields (nested in `reward_pools`):**

| Field | Type | Description |
|-------|------|-------------|
| rid | integer | Reward pool ID (needed for stake/redeem) |
| coin | string | Staking coin (e.g. "USDT", "GT", "BTC") |
| rate_year | string | Estimated APR — Annual Percentage Rate, no compounding (display as percentage with 2 decimal places, e.g. "767.06" → "Estimated APR 767.06%") |
| already_buy_total_amount | string | Total Staked — the circulating pledge total in this pool. Includes all pledged amounts (even if later redeemed). This is a running total, not net balance. E.g. if users pledge 100,000 and redeem 20,000, Total Staked remains 100,000. |
| personal_max_amount | string | Per-user maximum staking amount (-1 means unlimited) |
| personal_min_amount | string | Per-user minimum staking amount |
| transaction_config | array | Tiered participation conditions (optional, see below) |

**`TransactionConfig` fields (nested in `transaction_config`, optional per reward pool):**

This array defines tiered participation conditions based on the user's 60-day total trading volume. If the user's volume is below the lowest tier's `transaction_amount`, the personal staking limit is **0** (not eligible). The `mortgage_limit` unit follows the parent reward pool's `coin`.

| Field | Type | Description |
|-------|------|-------------|
| transaction_amount | number | 60-day total trading volume threshold in **USD** |
| mortgage_limit | number | Personal staking cap (in the reward pool's staking `coin`) unlocked when the trading volume threshold is met |

---

## Workflow

1. **Parse parameters**: Extract filters from user query — `status`, `sort_type`, `mortgage_coin`, `search_coin`, `limit_rule`.
2. **Call tool**: Call `cex_launch_list_launch_pool_projects` with `page=1`, `page_size=10`, and any optional filters.
3. **Key data to extract**: From each project: `pid`, `name`, `project_state`, `total_amount`, `days`. From each reward pool: `rid`, `coin`, `rate_year`, `already_buy_total_amount`, `personal_max_amount`, `personal_min_amount`, `transaction_config`. Note: `pid`, `rid`, `start_timest`, `end_timest` are internal — do NOT display them to the user.
4. **Format response**: Map `project_state` to label. Format `rate_year` as "Estimated APR {value}%" with 2 decimals. Do NOT display `start_timest`/`end_timest` to the user. If a reward pool has `transaction_config`, display it as a tiered list showing base tier (below lowest threshold → limit 0, not eligible) and each tier with trading volume threshold (USD) → staking limit ({coin}). **All projects must use the same tiered list format for `transaction_config`** — do NOT compress into a single line for any project. Use the Response Template from the matching scenario below.

## Report Template

Use the **Response Template** block from the scenario that matches the user intent. Always include: `name`, `project_state` (mapped to label), `total_amount`, `days`, and per reward pool: `coin`, `rate_year` as percentage, `already_buy_total_amount`, `personal_max_amount`/`personal_min_amount`. Do NOT display `start_timest`/`end_timest`.

---

## Scenario 1: Query projects by status

**Context**: User wants to see LaunchPool projects filtered by status (all, ongoing, ended, or warming up).

**Prompt Examples**:
- "Show all LaunchPool projects"
- "What LaunchPool events are currently ongoing?"
- "Any upcoming LaunchPool activities?"
- "Show ended LaunchPool projects"

**Expected Behavior**:
1. Map user intent to status: all=0, ongoing/in progress=1, warming up/upcoming=2, ended=3, ongoing+upcoming=4
2. Call `cex_launch_list_launch_pool_projects` with `page=1`, `page_size=10`, `status={mapped_value}`
3. For each project use: `name`, `project_state`, `total_amount`, `days`, and nested `reward_pools` (do NOT display `pid`, `rid`, `start_timest`, or `end_timest` to user)
4. Map `project_state` to status label (translate to user language): 1=in progress, 2=warming up, 3=ended
5. Display formatted project list

**Response Template**:
```
LaunchPool Projects ({status_label})

{For each project:}
Project: {name}
  Status: {project_state: 1=in progress, 2=warming up, 3=ended (translate to user language)}
  Total Rewards: {total_amount} {name}
  Staking Period: {days} days
  Reward Pools:
    - Stake {coin}: Estimated APR {rate_year}%, Circulating Pledge Total: {already_buy_total_amount}, Limit: {personal_min_amount} ~ {personal_max_amount}
      {If transaction_config exists for this pool:}
      Participation Conditions (60-day trading volume):
        Base: < {transaction_config[0].transaction_amount} USD → Staking Limit: 0 {coin} (not eligible)
        {For each item in transaction_config array, label as T1, T2, ... TN:}
        T{N}: ≥ {item.transaction_amount} USD → Staking Limit: {item.mortgage_limit} {coin}
    - ...

Showing {count} projects total.
```

---

## Scenario 2: Query projects sorted by estimated APR

**Context**: User wants to find the highest or lowest estimated APR LaunchPool projects.

**Prompt Examples**:
- "Find the highest APY LaunchPool projects"
- "Which LaunchPool has the best returns?"
- "Show LaunchPool sorted by lowest APY"

**Expected Behavior**:
1. Map user intent: highest/best=`sort_type=1` (descending), lowest=`sort_type=2` (ascending)
2. Call `cex_launch_list_launch_pool_projects` with `page=1`, `page_size=10`, `sort_type={value}`
3. For each project display: `name`, `project_state`, max `rate_year` across reward pools, `total_amount`
4. Highlight the top estimated APR in each project

**Response Template**:
```
LaunchPool Projects (Sorted by Estimated APR {Highest/Lowest} First)

{For each project:}
1. {name} — Max Estimated APR: {max rate_year}%
   Status: {project_state: 1=in progress, 2=warming up, 3=ended (translate)}
   Total Rewards: {total_amount} {name}
   Reward Pools:
     - Stake {coin}: Estimated APR {rate_year}%
     - ...

Showing {count} projects total.
```

---

## Scenario 3: Query projects by staking coin

**Context**: User wants to find LaunchPool projects that accept a specific staking coin.

**Prompt Examples**:
- "Which LaunchPool projects support USDT staking?"
- "I want to use BTC for LaunchPool, any options?"
- "Show me LaunchPool projects where I can stake ETH"

**Expected Behavior**:
1. Extract the staking coin from user query (e.g. "USDT")
2. Call `cex_launch_list_launch_pool_projects` with `page=1`, `page_size=10`, `mortgage_coin={coin}`
3. For each project, highlight the matching reward pool where `coin` equals the user's staking coin
4. Show `rid`, `rate_year`, `already_buy_total_amount`, `personal_max_amount`/`personal_min_amount` for the matching pool
5. If no results, suggest trying other coins

**Response Template**:
```
LaunchPool Projects (Staking with {coin})

{For each project:}
Project: {name}
  Status: {project_state: 1=in progress, 2=warming up, 3=ended (translate)}
  {coin} Pool:
    Estimated APR: {rate_year}%
    Circulating Pledge Total: {already_buy_total_amount} {coin}
    Limit: {personal_min_amount} ~ {personal_max_amount} {coin}
    {If transaction_config exists:}
    Participation Conditions (60-day trading volume):
      Base: < {transaction_config[0].transaction_amount} USD → Staking Limit: 0 {coin} (not eligible)
      {For each item in transaction_config array, label as T1, T2, ... TN:}
      T{N}: ≥ {item.transaction_amount} USD → Staking Limit: {item.mortgage_limit} {coin}
      ...
  Total Rewards: {total_amount} {name}

Found {count} projects supporting {coin} staking.
```

---

## Scenario 4: Query projects by pool type

**Context**: User wants to find LaunchPool projects with newbie pool or normal pool.

**Prompt Examples**:
- "Show LaunchPool projects with newbie pool"
- "Any LaunchPool for new users?"
- "Find normal pool LaunchPool projects"

**Expected Behavior**:
1. Map user intent: newbie/new users=`limit_rule=1`, normal/standard=`limit_rule=0`
2. Call `cex_launch_list_launch_pool_projects` with `page=1`, `page_size=10`, `limit_rule={value}`
3. Display matching projects with pool type highlighted
4. If no results, suggest trying without the pool type filter

**Response Template**:
```
LaunchPool Projects ({Newbie/Normal} Pool)

{For each project:}
Project: {name}
  Status: {project_state: 1=in progress, 2=warming up, 3=ended (translate)}
  Pool Type: {Newbie/Normal}
  Estimated APR: {rate_year}%
  Staking Coin: {coin}
  Total Rewards: {total_amount} {name}
  Limit: {personal_min_amount} ~ {personal_max_amount}

Found {count} projects with {pool_type} pool.
```

---

## Scenario 5: Empty project list

**Context**: User queries LaunchPool projects but no results match the filters.

**Prompt Examples**:
- "Show LaunchPool projects" (when none available)

**Expected Behavior**:
1. Call `cex_launch_list_launch_pool_projects` with user's filters
2. Receive empty array
3. Suggest alternative filters or checking back later

**Response Template**:
```
No LaunchPool projects match your criteria.

Suggestions:
- Try removing filters (status, coin, pool type)
- Check back later for new projects
- Browse all projects with "Show all LaunchPool projects"
```
