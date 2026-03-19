# Gate LaunchPool Stake & Redeem — Participate and Withdraw

Stake tokens to LaunchPool projects and redeem staked assets.

## MCP tools and parameters

| Tool | Purpose | Required | Optional |
|------|---------|----------|----------|
| **cex_launch_list_launch_pool_projects** | Find project pid and reward pool rid | `page`, `page_size` | `status`, `mortgage_coin`, `search_coin` |
| **cex_launch_create_launch_pool_order** | Create staking order | `body` (JSON) | — |
| **cex_launch_redeem_launch_pool** | Redeem staked assets | `body` (JSON) | — |

- **cex_launch_create_launch_pool_order**: `body` is a JSON string: `{"pid": int, "rid": int, "amount": "string"}`. Returns `{"flow_id": integer}` on success.
- **cex_launch_redeem_launch_pool**: `body` is a JSON string: `{"pid": int, "rid": int, "amount": "string"}`. Returns `{"success": boolean}` on success.
- Both require API Key authentication.

**API request — `CreateOrderV4` / `RedeemV4` fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| pid | integer | Yes | Project ID (from `LaunchPoolV4Project.pid`) |
| rid | integer | Yes | Reward pool ID (from `LaunchPoolV4RewardPool.rid`) |
| amount | string | Yes | Staking/redeem amount (string format for precision) |

**API response — Create order:**

| Field | Type | Description |
|-------|------|-------------|
| flow_id | integer | Order ID for the created staking order |

**API response — Redeem:**

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether the redemption was successful |

**API error labels:**

| label | Description |
|-------|-------------|
| INVALID_PARAM_VALUE | Invalid request parameters (wrong pid/rid/amount) |
| INVALID_CREDENTIALS | User not authenticated |
| INSUFFICIENT_BALANCE | User balance not enough to stake |
| PROJECT_NOT_FOUND | Project does not exist or has ended |

---

# Part 1: Stake

## Workflow

1. **Parse parameters**: Extract project name/coin, staking coin, and amount from user query.
2. **Find project**: Call `cex_launch_list_launch_pool_projects` with `page=1`, `page_size=10`, and optional `search_coin` or `mortgage_coin` to identify the target project.
3. **Key data to extract**: From the project list, find the matching project's `pid` and the appropriate reward pool's `rid` based on the staking coin.
4. **Show preview**: Display order preview with project name, staking coin, amount, estimated APR (`rate_year`), staking period. Ask user to confirm.
5. **Wait for confirmation**: User must reply "confirm" to proceed or "cancel" to abort.
6. **Execute stake**: Call `cex_launch_create_launch_pool_order` with `body` containing `pid`, `rid`, and `amount`.
7. **Format response**: Show success or failure message.

## Report Template

Show a preview first, then the confirmation result. Include project name, staking coin, amount, estimated APR, and any relevant warnings.

---

## Scenario 1: Normal stake with confirmation

**Context**: User wants to stake tokens to a specific LaunchPool project. The full Preview → Confirm flow is required.

**Prompt Examples**:
- "Stake 500 USDT to the BTC LaunchPool project"
- "I want to put all my BNB into LaunchPool"
- "Help me participate in the USDT LaunchPool with 1000 USDT"

**Expected Behavior**:
1. Extract: target project (e.g. "BTC"), staking coin (e.g. "USDT"), amount (e.g. "500")
2. Call `cex_launch_list_launch_pool_projects` with `search_coin` or `mortgage_coin` to find the project
3. Identify `pid` and `rid` from the matching project and reward pool
4. Display order preview and ask for confirmation (show `name`, `coin`, `amount`, `rate_year` as percentage)
5. On "confirm": call `cex_launch_create_launch_pool_order` with body `{"pid": {pid}, "rid": {rid}, "amount": "{amount}"}`
6. Display success with `flow_id`, or error with API error label

**Response Template**:
```
LaunchPool Stake Preview

Project: {name} (pid: {pid})
Staking Coin: {coin} (rid: {rid})
Amount: {amount} {coin}
Reward Pool Estimated APR: {rate_year}%

Please reply "confirm" to proceed or "cancel" to abort.

---
(After confirmation)
Stake order submitted! Flow ID: {flow_id}. You have successfully staked {amount} {coin} to the {name} LaunchPool project.
```

---

## Scenario 2: Normal redeem with confirmation

**Context**: User wants to redeem (withdraw) staked assets from a LaunchPool project early.

**Prompt Examples**:
- "Redeem my USDT from the BTC LaunchPool"
- "I want to withdraw all my stake from LaunchPool"
- "Unstake 50% of my USDT from the BTC LaunchPool project"

**Expected Behavior**:
1. Extract: target project, staking coin, redeem amount (or "all")
2. Identify `pid` and `rid` for the project and reward pool
3. Display redemption preview and ask for confirmation
4. On "confirm": call `cex_launch_redeem_launch_pool` with body `{"pid": {pid}, "rid": {rid}, "amount": "{amount}"}`
5. Display success or error message

**Response Template**:
```
LaunchPool Redeem Preview

Project: {name} (pid: {pid})
Redeem Coin: {coin} (rid: {rid})
Redeem Amount: {amount} {coin}

Note: Early redemption may forfeit remaining airdrop rewards.
Please reply "confirm" to proceed or "cancel" to abort.

---
(After confirmation)
Redeem successful! You have redeemed {amount} {coin} from the {name} LaunchPool project.
```

---

# Part 2: Redeem

## Workflow

1. **Parse parameters**: Extract project name/coin, staking coin, and redeem amount from user query.
2. **Identify project**: Determine `pid` and `rid` from user context or by calling `cex_launch_list_launch_pool_projects`.
3. **Show preview**: Display redemption preview with project name, coin, amount, and early redemption warning.
4. **Wait for confirmation**: User must reply "confirm" to proceed.
5. **Execute redeem**: Call `cex_launch_redeem_launch_pool` with `body` containing `pid`, `rid`, and `amount`.
6. **Key data to extract**: Success/failure status, redeemed amount.
7. **Format response**: Show confirmation result.

## Report Template

Show redemption preview first, then the confirmation result. Always include the early redemption warning.

---

## Scenario 3: Missing parameters — clarification needed

**Context**: User expresses intent to stake or redeem but does not provide enough information (missing project, coin, or amount).

**Prompt Examples**:
- "I want to join LaunchPool"
- "Stake to LaunchPool"
- "Help me participate"

**Expected Behavior**:
1. Detect incomplete request (missing project, coin, or amount)
2. Ask clarifying questions to collect missing parameters
3. Once all parameters are collected, proceed with the normal stake/redeem flow

**Response Template**:
```
I'd like to help you participate in LaunchPool! I need a few more details:

1. Which LaunchPool project? (e.g. "BTC project")
2. Which coin would you like to stake? (e.g. "USDT")
3. How much would you like to stake?

You can also say "Show LaunchPool projects" to browse available options first.
```

---

## Scenario 4: Compliance error

**Context**: Stake or redeem fails due to regional compliance restrictions.

**Prompt Examples**:
- "Stake 500 USDT to LaunchPool" (from restricted region)
- "Why can't I participate in LaunchPool?"

**Expected Behavior**:
1. Attempt to execute the stake/redeem order
2. API returns compliance/region restriction error
3. Display friendly compliance message
4. Do NOT retry the operation

**Response Template**:
```
Due to compliance restrictions, LaunchPool is not available in your region.

For more information about regional availability, please visit the Gate website or contact support.
```

---

## Scenario 5: Insufficient balance or limit exceeded

**Context**: Stake fails because user balance is insufficient or the amount exceeds the personal staking limit.

**Prompt Examples**:
- "Stake 10000 USDT to LaunchPool" (exceeds limit or balance)

**Expected Behavior**:
1. Attempt to execute the stake order after user confirmation
2. API returns error with `label` field (e.g. `INSUFFICIENT_BALANCE` or `INVALID_PARAM_VALUE`)
3. Display the error label and message with helpful guidance
4. Suggest reducing amount or checking balance

**Response Template**:
```
Stake failed: [{label}] {message}

Suggestions:
- Check your available {coin} balance
- This project has a personal staking limit of {personal_min_amount} ~ {personal_max_amount} {coin}
- Try a smaller amount

You can say "Show LaunchPool projects" to see project details including limits.
```
