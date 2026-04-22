---
name: gate-exchange-welfare
description: "Gate Exchange welfare center phase-2 skill with MCP integration. Use this skill whenever the user asks about welfare benefits, newcomer rewards, available newcomer tasks, claiming a task, completing a welfare task, or claiming newcomer rewards. Trigger phrases include \"welfare center\", \"new user tasks\", \"claim task\", \"claim download task\", \"complete KYC task\", \"complete first deposit task\", \"complete first trade task\", \"claim reward\", and \"claim all rewards\". Use only real MCP data and current business codes; never fabricate task or reward details."
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "💱"
    os:
      - darwin
      - linux
    primaryEnv: GATE_API_KEY
    requires:
      bins:
        - gate-cli
      env:
        - GATE_API_KEY
        - GATE_API_SECRET

    install:
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux x64)"
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux arm64)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Intel)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Apple Silicon)"
---

### Resolving `gate-cli` (binary path)

Resolve **`gate-cli`** in order: **(1)** **`command -v gate-cli`** and **`gate-cli --version`** succeeds; **(2)** **`${HOME}/.local/bin/gate-cli`** if executable; **(3)** **`${HOME}/.openclaw/skills/bin/gate-cli`** if executable. Canonical rules: [`exchange-runtime-rules.md`](../exchange-runtime-rules.md) §4 (or [`gate-runtime-rules.md`](../gate-runtime-rules.md) §4).


# Gate Exchange Welfare Center

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read `./references/gate-runtime-rules.md`
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

## Skill Dependencies


### gate-cli commands used

**Query Operations**

- `gate-cli cex welfare identity`
- `gate-cli cex welfare beginner-tasks`

**Execution Operations**

- `cex_welfare_claim_task` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)
- `cex_welfare_claim_reward` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)

### Authentication
- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- API Key Required: Yes
- **Permissions:** Welfare query and claim access in the current Gate MCP deployment
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- **Required:** `gate-cli` (run `sh ./setup.sh` from this skill directory if missing; optional `GATE_CLI_SETUP_MODE=release`).
- Add `$HOME/.openclaw/skills/bin` to **`PATH`** if you invoke `gate-cli` by name (or the directory where [`setup.sh`](./setup.sh) installs it).
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`** — that is equivalent valid config for `gate-cli`. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Do not proceed with authenticated calls until the CLI behaves as expected (e.g. **`gate-cli --version`** or a read-only **`gate-cli cex ...`** command from this skill); confirm credentials resolve before mutating operations.


## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute this skill's welfare workflow.

- `SKILL.md` keeps routing, business intent mapping, and safety rules.
- `references/gate-cli.md` is the authoritative `gate-cli` execution contract for identity gating, task lookup, task claim, reward claim, and degraded handling.

## Overview

> Welfare center newcomer skill, phase 2. When users ask about welfare, newcomer rewards, task claiming, task completion, or reward claiming, first determine user eligibility. Then either guide restricted/existing users, show real newcomer tasks, claim a single task, guide task completion, or claim all currently claimable newcomer rewards.

**Trigger Scenarios**: Execute this skill when users mention welfare benefits, newcomer rewards, task lists, claiming a task, completing a welfare task, or claiming newcomer rewards.

---

## Domain Knowledge

### Eligibility codes
- **`code=0`**: Eligible newcomer
- **`code=1001`**: Existing user
- **`code=1002`**: Risk-control user
- **`code=1003`**: Sub-account
- **`code=1004`**: Agent user
- **`code=1005`**: Market maker
- **`code=1006`**: Enterprise user
- **`code=1008`**: Not logged in

### Beginner task list semantics
- The newcomer list is fetched from `gate-cli cex welfare beginner-tasks`.
- Registration tasks are returned before guidance tasks.
- When the user has not yet received a download task and the system determines the app is not downloaded, the list may include a **download task** with **`task_type=23`** and **`status=0`**.
- `task_desc` may contain simple HTML such as `<span>`; present the text content only, not raw tags.

### Task type notes
- **`task_type=10`**: Registration task
- **`task_type=23`**: Download task
- Guidance tasks may surface task-scene codes such as:
 - **`1`**: KYC / identity verification
 - **`2`**: Spot trading
 - **`3`**: Futures trading
 - **`8`**: First deposit
- Some live payloads may use other supported task-scene values. Follow the real MCP payload instead of hardcoding assumptions beyond the documented mappings above.

### Status mapping

| Status | Meaning | Handling |
|--------|---------|----------|
| `0` | Unclaimed / task can be claimed | Candidate for `cex_welfare_claim_task` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) |
| `1` | Claimed / in progress | User should complete the task action |
| `2` | Completed, reward claimable | Candidate for `cex_welfare_claim_reward` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) |
| `3` | Reward distributing | Inform user reward is being processed |
| `4` | Completed / settled | Inform user task is already finished |
| `5` | Expired | Inform user task has expired |

### Rewards hub
- Official hub: `https://www.gate.com/zh/rewards_hub`
- Use the official web/App welfare center as the fallback whenever the APIs cannot return a reliable action result.

---

## Routing Rules

| User Intent | Keywords / Patterns | Routing |
|-------------|---------------------|---------|
| Query welfare / rewards / task list | "what welfare", "what tasks can I do", "new user tasks", "welfare rewards" | Execute this skill → identity gate first |
| Claim a task | "claim task", "claim download task", "receive task" | Execute this skill → identity → list tasks → claim one status=`0` task |
| Complete KYC task | "complete identity verification task", "complete KYC task" | Execute this skill → respond with generic KYC guidance |
| Complete first deposit task | "complete first deposit task", "how do I finish deposit task" | Execute this skill → respond with generic deposit guidance |
| Complete first trade task | "complete first trade task", "I want to do my first trade" | Execute this skill → hand off to `gate-exchange-trading` |
| Complete task (ambiguous) | "complete task", "finish my welfare task" | Execute this skill → identity → list actionable tasks → resolve task |
| Claim reward / claim all rewards | "claim reward", "claim all rewards", "receive newcomer rewards" | Execute this skill → identity → list tasks → claim all status=`2` tasks |
| Asset query | "check my balance", "how much USDT do I have" | Route to `gate-exchange-assets` |

---

## Execution

### Step 1: Determine user identity

Call `gate-cli cex welfare identity` first for every welfare intent.

Branch by `code`:
- **`0`** → newcomer flow
- **`1001`** → existing-user guidance
- **`1002/1003/1004/1005/1006/1008`** → mapped restriction guidance
- **other failure / timeout / HTTP 4xx** → degraded fallback

### Base Flow: Query or list newcomer tasks

**Trigger**: The user asks what newcomer welfare/tasks/rewards are available.

Required flow:
1. Call `gate-cli cex welfare identity`.
2. If `code=0`, call `gate-cli cex welfare beginner-tasks`.
3. If list result is `code=1007` or the task list is empty, return the no-task fallback.
4. Render every real task using:
 - `task_name`
 - `task_desc` with HTML tags removed
 - `reward_num`
 - `reward_unit`
 - `status`
5. Map each task's next step from `status`:
 - `0`: can be claimed
 - `1`: complete the task action
 - `2`: reward can be claimed
 - `3`: reward is distributing
 - `4`: already completed
 - `5`: expired

### Case 1: Claim a single task

**Trigger**: The user asks to claim a task, usually a download task.

Required flow:
1. Call `gate-cli cex welfare identity`.
2. Call `gate-cli cex welfare beginner-tasks`.
3. Find claimable tasks with `status=0`.
4. Resolve the target task:
 - If the user names a task, match by `task_name`.
 - If exactly one claimable task exists, use it.
 - If multiple claimable tasks exist and intent is ambiguous, ask which task to claim.
5. Call `cex_welfare_claim_task` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with the selected `welfare_task_id`.
6. On success, confirm the claimed task name and remind the user to complete it before claiming the reward.

Do not call `cex_welfare_claim_task` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) for tasks whose status is not `0`.

### Case 2: Complete identity verification task

**Trigger**: The user asks to complete a KYC / identity verification newcomer task.

Required behavior:
- Do **not** call a welfare write tool.
- Return generic KYC guidance, for example:

```text
Please complete identity verification in Gate web or the Gate App first. After the verification is approved and the newcomer task becomes claimable, come back to the welfare center to claim the reward.
```

### Case 3: Complete first deposit task

**Trigger**: The user asks to complete a first-deposit newcomer task.

Required behavior:
- Do **not** call a welfare write tool.
- Return generic deposit guidance without inventing thresholds:

```text
Please complete your first deposit in Gate web or the Gate App using the deposit flow shown there. Deposit requirements, supported assets, and any threshold conditions follow the Rewards Hub display. After the deposit is credited and the task becomes claimable, come back to claim the reward.
```

### Case 4: Complete first trade task

**Trigger**: The user asks to complete a first-trade newcomer task.

→ Read [gate-exchange-trading/references/execution-and-guardrails.md](https://github.com/gate/gate-skills/blob/master/skills/gate-exchange-trading/references/execution-and-guardrails.md)

Required behavior:
- Hand off to `gate-exchange-trading`.
- If the user has not yet specified what to trade, let the trading skill collect symbol / side / size and follow its own Action Draft plus confirmation rules.

### Case 5: Complete task with ambiguous intent

**Trigger**: The user only says "complete task" or equivalent.

Required flow:
1. Call `gate-cli cex welfare identity`.
2. Call `gate-cli cex welfare beginner-tasks`.
3. Build an actionable task set from statuses `0` and `1`.
4. If multiple actionable tasks exist, ask the user which task they want to complete.
5. If exactly one actionable task exists:
 - `status=0` → use **Case 1**
 - task wording or `task_type` indicates KYC → use **Case 2**
 - task wording or `task_type` indicates first deposit → use **Case 3**
 - task wording or `task_type` indicates trading → use **Case 4**
 - otherwise, provide general completion guidance and rewards-hub fallback

### Case 6: Claim reward(s)

**Trigger**: The user asks to claim reward / claim all rewards.

Required flow:
1. Call `gate-cli cex welfare identity`.
2. Call `gate-cli cex welfare beginner-tasks`.
3. Filter tasks with `status=2`.
4. If none exist, tell the user there are no currently claimable newcomer rewards.
5. For general "claim reward" intent, iterate through all status=`2` tasks and call `cex_welfare_claim_reward` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) one by one.
6. For each successful claim:
 - Prefer `coupon_full_name` from the claim response.
 - If `coupon_full_name` is empty, fall back to the task's `reward_num` + `reward_unit`.
7. If a task returns `has_m_n_task=true`, **do not** complete reward distribution for that task. Instead guide the user to Gate web/App rewards hub for manual claiming.

---

## Response Templates

### Existing user guidance

```text
Please visit Gate web at https://www.gate.com/zh/rewards_hub or open the Gate App to view welfare activities, exclusive benefits, and reward redemption items.
```

### Newcomer task list

```text
Your newcomer welfare tasks:

- {task_name}
 Description: {task_desc_without_html}
 Reward: {reward_num} {reward_unit}
 Status: {mapped_status}
 Next step: {claim task / complete task / claim reward / distributing / completed / expired}
```

### Task claim success

```text
Successfully claimed {task_name}. Complete the task first, then you can claim {reward_num} {reward_unit}.
```

### Reward claim success

```text
You have claimed these newcomer rewards:

- {task_name}: {coupon_full_name_or_reward_num_reward_unit}
- {task_name}: {coupon_full_name_or_reward_num_reward_unit}
```

### M-select-N reward fallback

```text
This reward must be claimed from Gate web at https://www.gate.com/zh/rewards_hub or from the Gate App welfare center.
```

---

## Error Handling

| Exception Type | Handling Method |
|----------------|-----------------|
| Existing user (`code=1001`) | Show rewards-hub guidance |
| Risk-control user (`code=1002`) | "Your account is temporarily unable to participate in welfare activities. Please contact customer service for details." |
| Sub-account (`code=1003`) | "Sub-accounts cannot participate in this welfare activity. Please log in with your main account." |
| Agent user (`code=1004`) | "Agent users cannot participate in this welfare activity." |
| Market maker (`code=1005`) | "Market maker users cannot participate in this welfare activity." |
| Enterprise user (`code=1006`) | "Enterprise users cannot participate in this welfare activity." |
| No task data (`code=1007`) | "There are currently no active newcomer welfare tasks. Please check the Rewards Hub for more activities." |
| Not logged in (`code=1008`) | "Please log in to your Gate account first." |
| Identity/list timeout or MCP unavailable | "Welfare information is temporarily unavailable. Please try again later or visit https://www.gate.com/zh/rewards_hub directly." |
| Claim task: invalid activity (`51501009`) | Tell the user the task is no longer valid or available |
| Claim task: already claimed / condition not met (`51501010`) | Tell the user the task cannot be claimed again or conditions are not met yet |
| Claim task or reward: risk rejected (`51501026`) | Tell the user the account is temporarily not eligible for the welfare center |
| Claim reward: refresh again (`51501027`) | Ask the user to refresh/recheck the task list, then retry |
| Claim reward: task expired (`51501034`) | Tell the user the reward claim window has expired |
| Claim reward: record not exist (`51501004`) | Tell the user the reward record is no longer available and suggest refreshing the task list |
| HTTP `4xx` with standard `label` + `message` | Surface the gateway error briefly and stop; do not treat HTTP `200` alone as success |

---

## Cross-Skill Integration

| User Follow-up Intent | Routing Target |
|-----------------------|----------------|
| User wants to perform the first trade | `gate-exchange-trading` |
| User narrows to a spot-only trading action | `gate-exchange-spot` |
| User asks about general asset balances | `gate-exchange-assets` |
| User asks general KYC status/details outside welfare completion guidance | `gate-exchange-kyc` |

---

## Safety Rules

1. **Identity gate first**: Always call `gate-cli cex welfare identity` before showing newcomer task details, claiming a task, or claiming a reward.
2. **Allowed tools only**: Use only the four MCP tools documented in this skill.
3. **Business code is authoritative**: Success/failure is determined by response `code`, not by HTTP `200` alone.
4. **Real data only**: Never fabricate task names, descriptions, reward numbers, reward units, or reward titles.
5. **Clean task descriptions**: Remove raw HTML tags from `task_desc` before presenting the text to the user.
6. **Claim-task precondition**: Only call `cex_welfare_claim_task` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) for a task selected from the current task list with `status=0`.
7. **Claim-reward precondition**: Only call `cex_welfare_claim_reward` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) for tasks currently shown as `status=2`.
8. **M-select-N handling**: If `has_m_n_task=true`, do not report the reward as claimed. Redirect the user to the official rewards hub/App.
9. **No unrelated trading writes here**: Deposit execution and trading execution are outside this skill. Route them to the proper product skills.
10. **Fallback safely**: If the MCP data is unavailable or inconsistent, guide the user to `https://www.gate.com/zh/rewards_hub` instead of guessing.
