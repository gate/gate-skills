---
name: gate-exchange-launchpool
version: "2026.3.23-1"
updated: "2026-03-23"
description: "The LaunchPool staking and airdrop function of Gate Exchange. Use this skill whenever you need to browse LaunchPool projects, stake tokens, redeem staked assets, query pledge records, or check airdrop reward history. Trigger phrases include: LaunchPool, launch pool, staking event, airdrop, pledge, redeem, LaunchPool rewards, LaunchPool projects."
---

# Gate LaunchPool Suite

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

- cex_launch_list_launch_pool_pledge_records
- cex_launch_list_launch_pool_projects
- cex_launch_list_launch_pool_reward_records

**Execution Operations (Write)**

- cex_launch_create_launch_pool_order
- cex_launch_redeem_launch_pool

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)
- Permissions: Launch:Write
- Get API Key: https://www.gate.io/myaccount/profile/api-key/manage

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Module overview

| Module | Description | Trigger keywords |
|--------|-------------|------------------|
| **Projects** | Browse LaunchPool project list, filter by status/APR/coin/pool type | `projects`, `activities`, `events`, `ongoing`, `ended`, `warming up`, `APY`, `APR`, `which LaunchPool` |
| **Stake** | Stake tokens to a LaunchPool project | `stake`, `participate`, `join`, `pledge`, `contribute`, `put in` |
| **Redeem** | Early redeem staked assets from a project | `redeem`, `withdraw`, `unstake`, `take out`, `exit`, `pull out` |
| **Pledge Records** | Query staking/redemption participation history | `pledge records`, `participation history`, `staking records`, `my LaunchPool history` |
| **Reward Records** | Query airdrop reward distribution history | `airdrop`, `rewards`, `earnings`, `reward records`, `airdrop history`, `LaunchPool income` |

## Domain Knowledge

### LaunchPool concepts

| Concept | Description |
|---------|-------------|
| LaunchPool | A platform feature where users stake existing tokens to earn new token airdrops. Projects have a fixed staking period. |
| Project (pid) | A LaunchPool campaign for a specific new token. Has start/end time, total reward pool, and staking rules. |
| Reward Pool (rid) | Within a project, different reward pools exist for different staking coins (e.g. USDT pool, BTC pool). Each has its own estimated APR. |
| Staking Period | The duration during which users can stake and earn rewards. After the period ends, rewards are distributed. |
| Estimated APR | `rate_year` — the estimated Annual Percentage Rate (simple, no compounding) for a reward pool. Users may say "APY" colloquially; always display as "Estimated APR" in output. |
| Newbie Pool | Special pool with lower entry requirements or bonus rewards for new users (`limit_rule=1`). |
| Normal Pool | Standard staking pool open to all users (`limit_rule=0`). |
| Status (`project_state`) | Project lifecycle: Warming up (2) → In progress (1) → Ended (3). The request param `status` also supports 0 (All) and 4 (In progress + Warming up). |
| Personal Limit | Maximum/minimum staking amount per user per reward pool (`personal_max_amount` / `personal_min_amount`). |
| Transaction Config | Tiered participation conditions based on the user's **60-day total trading volume (in USD)**. Each tier defines a `transaction_amount` threshold and a corresponding `mortgage_limit` (personal staking cap, unit follows the reward pool's staking `coin`). If the user's trading volume is below the lowest tier, the staking limit is **0** (not eligible to participate). The `transaction_config` array is optional — only some reward pools have it. |

### Timestamp formatting

The `create_timest` and `reward_timest` fields in pledge/reward records are pre-formatted strings from the API (e.g. "2026-03-16 09:32:22"). Display them as-is in the data row and put `(UTC)` in the table header instead of appending to each value.

Project time fields (`start_timest`, `end_timest`) are internal data — do NOT display them to the user.

**Reward records time params**: The reward records API requires `start_time`/`end_time` as **integer unix timestamps**, which are error-prone to calculate. Follow the **Timestamp strategy** in `references/records.md` (Strategy 1: skip time params for recent queries; Strategy 2: use anchor table for historical ranges). Do NOT attempt to mentally compute unix timestamps without the anchor table.

### Number formatting

| Category | Precision | Examples |
|----------|-----------|----------|
| Amounts (staking, redeem, rewards) | 8 decimals, trailing zeros removed | `1.23` not `1.23000000` |
| Rate fields (Estimated APR) | 2 decimals, trailing zeros retained | `5.20%` not `5.2%` |

## Routing rules

| Intent | Example phrases | Route to |
|--------|-----------------|----------|
| **Browse projects** | "Show LaunchPool projects", "What LaunchPool events are ongoing?", "Highest APR LaunchPool", "Any USDT LaunchPool?", "Newbie pool projects" | Read `references/launch-projects.md` |
| **Stake** | "Stake 500 USDT to LaunchPool BTC project", "I want to participate in LaunchPool", "Put 1000 USDT into LaunchPool" | Read `references/stake-redeem.md` (Stake section) |
| **Redeem** | "Redeem my LaunchPool BTC stake", "Withdraw from LaunchPool", "Unstake my USDT from LaunchPool" | Read `references/stake-redeem.md` (Redeem section) |
| **Pledge records** | "My LaunchPool participation last month", "Show my LaunchPool staking records", "Check my BTC LaunchPool pledge history" | Read `references/records.md` (Part 1: Pledge Records) |
| **Reward records** | "My LaunchPool airdrop rewards", "Check LaunchPool earnings this month", "Show my BTC LaunchPool airdrop" | Read `references/records.md` (Part 2: Reward Records) |
| **Unclear** | "LaunchPool", "launch pool" | **Clarify**: projects / stake / redeem / pledge records / reward records, then route |

## Execution

### 1. Intent and parameters

- Determine module (Projects / Stake / Redeem / Pledge Records / Reward Records).
- **Stake intent**: If the user wants to stake tokens, route to `references/stake-redeem.md` Stake section. Requires project identification + amount + user confirmation.
- **Redeem intent**: If the user wants to redeem, route to `references/stake-redeem.md` Redeem section. Requires project identification + amount + user confirmation.
- Extract parameters: `coin`, `pid`, `rid`, `amount`, `status`, `sort_type`, `limit_rule`, `page`, `start_time`, `end_time`.
- **Missing**: if user says "LaunchPool" without specifying intent, ask which operation or show projects by default.

### 2. Tool selection

| Module | MCP tool | Required params | Optional params |
|--------|----------|-----------------|-----------------|
| Projects | `cex_launch_list_launch_pool_projects` | `page`, `page_size` | `status`, `sort_type`, `mortgage_coin`, `search_coin`, `limit_rule` |
| Stake | `cex_launch_create_launch_pool_order` | `body` (JSON: pid, rid, amount) | — |
| Redeem | `cex_launch_redeem_launch_pool` | `body` (JSON: pid, rid, amount) | — |
| Pledge Records | `cex_launch_list_launch_pool_pledge_records` | — | `coin`, `type`, `start_time`, `end_time`, `page`, `page_size` |
| Reward Records | `cex_launch_list_launch_pool_reward_records` | `page`, `page_size` | `coin`, `status`, `start_time`, `end_time` |

- **Stake**: First call `cex_launch_list_launch_pool_projects` to identify the target project pid and reward pool rid, then show preview, wait for confirmation, then call `cex_launch_create_launch_pool_order`.
- **Redeem**: Show preview of the redemption, wait for confirmation, then call `cex_launch_redeem_launch_pool`.

### 3. Format response

- Use the **Response Template** and field names from the reference file for the chosen module.
- Projects: show `name`, `project_state`, `total_amount`, `days`, and per reward pool: `coin`, `rate_year`, `already_buy_total_amount`, `personal_max_amount`/`personal_min_amount`, `transaction_config`. Do NOT display `start_timest`/`end_timest`, `pid`, or `rid`.
- Stake/Redeem: show order preview first, then confirmation result. Stake returns `flow_id`; Redeem returns `success` boolean.
- Pledge Records: show `create_timest`, `reward_coin`, `coin`, `amount`, `type` (1=Stake, 2=Redeem). Note: API does **not** return project name.
- Reward Records: show `reward_timest`, `coin` (reward coin), `valid_mortgage_amount`, `amount_base`, `amount_ext`. Note: API does **not** return project name.

## Report template

After each operation, output a short standardized result consistent with the reference (e.g. project list table, stake confirmation, redeem confirmation, pledge record list, reward record list). Use the exact response fields from the API (see references) so the user sees correct field names and values.

**Language adaptation**: Always respond in the same language as the user's input. The Response Templates in reference files define the **structure and fields** to display, not the literal output language. Translate all display labels to match the user's language.

**Do NOT translate** (keep as-is regardless of language):
- Product name: `LaunchPool`
- Currency symbols from API: USDT, GT, BTC, DOGE, etc.
- Project names from API `name` field (e.g. "DOGE", "USDT-rudy")
- Technical IDs and their values: pid, rid, flow_id (internal use only, do NOT display to user)
- Timestamp format including the `(UTC)` suffix
- API error labels: INVALID_PARAM_VALUE, INSUFFICIENT_BALANCE, INVALID_CREDENTIALS, PROJECT_NOT_FOUND
- Numeric values, percentages, and the unit `USD` in trading volume thresholds

All other display labels should be translated to match the user's language.

## Error Handling

### API error labels

The API returns structured errors with a `label` field. Map them as follows:

| API label | User-facing message |
|-----------|---------------------|
| `INVALID_PARAM_VALUE` | "Invalid request parameters. Please check your input and try again." |
| `INVALID_CREDENTIALS` | "Please log in to access LaunchPool features." |
| `INSUFFICIENT_BALANCE` | "Insufficient balance. Please top up first." |
| `PROJECT_NOT_FOUND` | "The specified LaunchPool project was not found." |

### Empty result handling

| Scenario | Action |
|----------|--------|
| Empty project list | "No LaunchPool projects match your criteria. Try different filters or check back later." |
| Empty pledge records | "You have no LaunchPool participation records. Browse active projects to get started." |
| Empty reward records | "No airdrop rewards found. Rewards are typically distributed after the staking period ends." |
| Compliance restriction | "Due to compliance restrictions, LaunchPool is not available in your region." |
| Stake limit exceeded | "This project has a personal staking limit. Please reduce your amount." |
| API error / 401 | "Unable to fetch LaunchPool data. Please try again later." or "Please log in to access LaunchPool features." |

## Safety rules

### Confirmation required

- **Stake and Redeem are write operations.** Before calling `cex_launch_create_launch_pool_order` or `cex_launch_redeem_launch_pool`, MUST show an order preview and wait for explicit user confirmation.
- Preview format: project name, staking coin, amount, estimated APR (for stake), staking period.
- Ask user to reply "confirm" to proceed or "cancel" to abort.
- Only call the API after receiving explicit confirmation.

### Compliance

- When the API returns a compliance or region restriction error, display a friendly message: "Due to compliance restrictions, LaunchPool is not available in your region." Do NOT retry.
