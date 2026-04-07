---
name: gate-exchange-welfare
version: "2026.4.3-1"
updated: "2026-04-03"
description: "Gate welfare center and new-user task skill. Use when the user asks about welfare rewards, tasks, or how to claim benefits. Triggers on 'welfare center', 'new user tasks', 'claim reward'. Must use real MCP data only."
required_credentials:
  - gate_api_key
  - gate_api_secret
required_env_vars:
  - GATE_API_KEY
  - GATE_API_SECRET
required_permissions:
  - Welfare:Read
metadata:
  openclaw:
    requires:
      env:
        - GATE_API_KEY
        - GATE_API_SECRET
    primaryEnv: GATE_API_KEY
    homepage: https://github.com/gate/gate-skills
---

# Gate Exchange Welfare Center

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read `./references/gate-runtime-rules.md`
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

- cex_welfare_get_beginner_task_list
- cex_welfare_get_user_identity

### Authentication
- Credentials Source: Local Gate MCP deployment (`GATE_API_KEY`, `GATE_API_SECRET`)
- API Key Required: Yes
- Permissions: Welfare:Read
- Never ask the user to paste secrets into chat; rely on the configured MCP session only.
- API Key Provisioning Reference: https://www.gate.com/myaccount/profile/api-key/manage (create or rotate keys outside the chat when the local MCP setup requires them).

### Installation Check
- Required: Gate (main)
- Install: Use the local Gate MCP installation flow for the current host IDE before continuing.
- Continue only after the Gate MCP session is configured with the credentials listed above; do not switch to browser auth or ask the user to paste secrets into chat.

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this skill's welfare workflow.

- `SKILL.md` keeps user-type routing, task-display semantics, and policy constraints.
- `references/mcp.md` is the authoritative MCP execution layer for identity gate, task query sequence, and fallback handling.

## Overview

> Welfare center new user task entry Skill (version 2026.3.18-6, with MCP tools integration). When users ask about benefits/rewards/tasks, first determine if they are new users. Show all new user onboarding task details for new users, guide existing users to official website or App.

**Trigger Scenarios**: Execute this Skill when users mention welfare benefits, new user rewards, task claiming, reward claiming and other related keywords.

---

## Domain Knowledge

### New User Definition
- **New User (code=0)**: Newly registered users who have not completed any trading activities, deposits, or other engagement tasks
- **Existing User (code=1001)**: Users with trading history, completed tasks, or established account activity

### User Status Categories
- **Normal Users**: Can participate in all new user activities and claim rewards
- **Risk Control Users (code=1002)**: Temporarily restricted from participating in activities due to security concerns
- **Sub-accounts (code=1003)**: Cannot participate; must use main account
- **Agent Users (code=1004)**: Excluded from new user welfare programs
- **Market Makers (code=1005)**: Professional traders excluded from new user benefits
- **Enterprise Users (code=1006)**: Corporate accounts excluded from individual user benefits
- **Not Logged In (code=1008)**: Must authenticate before accessing welfare information

### Task Types
- **Registration Tasks (type=10)**: Basic onboarding activities like app download, account setup
- **Guidance Tasks (type=11)**: Progressive engagement tasks like KYC verification, first deposit, first trade

### Reward Mechanisms
- **USDT Trial Vouchers**: Practice trading credits for new users
- **Bonus USDT**: Real trading capital rewards
- **Points**: Loyalty program credits for redemption
- **Task Completion**: Sequential unlock of advanced features and higher rewards

### Welfare Ecosystem
- **Centralized Hub**: All welfare activities accessible via https://www.gate.com/rewards_hub
- **Mobile Integration**: Full feature parity in Gate mobile app
- **Cross-platform Sync**: Task progress and rewards synchronized across web and mobile

---

## Routing Rules

| User Intent | Keywords / Patterns | Routing |
|-------------|-------------------|---------|
| Query welfare / rewards / tasks (general) | "what welfare", "how to claim rewards", "what tasks can I do", "welfare", "rewards" | Execute this Skill → Determine user type first |
| Query new user benefits / rewards | "new user benefits", "how to claim new user rewards", "new user tasks", "new user benefits", "newbie rewards" | Execute this Skill → Determine user type first |
| Spot trading | "buy BTC", "sell ETH" | Route to `gate-exchange-spot` |
| Asset query | "how much USDT do I have", "check balance" | Route to `gate-exchange-assets` |
| Deposit | "how to deposit", "how to fund account" | Route to deposit related Skill |

---

## Execution Workflow

### Step 1: Determine User Identity

Call MCP tool to query whether the current user is a new user.

| Step | MCP Tool | Parameters | Data Retrieved |
|------|----------|------------|----------------|
| 1 | `cex_welfare_get_user_identity` (User identity determination interface) | Automatically get current user identity | Returns code=0 (qualifies as new user) or error codes (1001=existing user, 1002=risk control, 1003=sub-account, 1004=agent, 1005=market maker, 1006=enterprise, 1008=not logged in) |

Enter corresponding branch based on returned result:
- **code=0 (new user)** → Execute [Case 2: New User Task List](#case-2-new-user-task-list)
- **code=1001 (existing user)** → Execute [Case 1: Existing User Guidance](#case-1-existing-user-guidance)
- **Other error codes** → Execute corresponding handling logic according to [Exception Handling](#exception-handling) section

---

### Case 1: Existing User Guidance

**Trigger Condition**: Step 1 determines user as existing user (`cex_welfare_get_user_identity` returns code=1001).

**No additional MCP tool calls needed**, directly output guidance text.

**Output Template**:

```
Please visit Gate web at https://www.gate.com/rewards_hub or open Gate App to view welfare tasks and rewards.
```

---

### Case 2: New User Task List

**Trigger Condition**: Step 1 determines user as new user (`cex_welfare_get_user_identity` returns code=0).

#### Step 2: Get All New User Onboarding Tasks

| Step | MCP Tool | Parameters | Data Retrieved |
|------|----------|------------|----------------|
| 2 | `cex_welfare_get_beginner_task_list` (Query beginner guidance task list) | Automatically get current user tasks | Get beginner guidance task list, including registration tasks (type=10) and guidance tasks (type=11), each task contains reward information, completion status and task description |

#### Step 3: Generate Task List Response

**Important Note**: Must use real task data obtained from MCP interface in Step 2, absolutely cannot fabricate or use template example data!

Based on the real task data returned from Step 2, output to users in the following format:

1. **Iterate through all tasks**: For each task in the `data.tasks` array returned by `cex_welfare_get_beginner_task_list`
2. **Extract real fields**: Use the task's real fields such as `task_name`, `task_desc`, `reward_num`, `reward_unit`, `status`
3. **Status display**: `status=1` shows "Pending", `status=2` shows "Completed"
4. **Format output**: Strictly follow template format, but content must be real MCP data

**Data mapping rules**:
- Task title: Use `task_name` field
- Task description: Use `task_desc` field  
- Reward amount: Use `reward_num` field
- Reward unit: Use `reward_unit` field
- Completion status: Use `status` field (1=Pending, 2=Completed)

---

## Response Templates

### Case 1 — Existing User Guidance

```
Please visit Gate web at https://www.gate.com/rewards_hub or open Gate App to view welfare tasks and rewards.
```

---

### Case 2 — New User Task List

```
🎁 Your exclusive new user tasks are as follows. Complete tasks to claim corresponding rewards:

{for each task in task_list:}

📌 {task_name}
   {task_desc}
   💰 Reward: {reward_num} {reward_unit}
   Status: {Display based on status field: 1=Pending, 2=Completed}

---

⚠️ Non-agent, non-institutional users and users with normal account status can complete tasks and claim rewards. Specific tasks and rewards are subject to final display on Gate official website/App.
```

**Example Output**:

```
🎁 Your exclusive new user tasks are as follows. Complete tasks to claim corresponding rewards:

{Generate dynamically based on actual task data returned from MCP interface, format:}

📌 {task_name}
   {task_desc}
   💰 Reward: {reward_num} {reward_unit}
   Status: {Display based on status field: 1=Pending, 2=Completed}

{Repeat above format until all tasks are displayed}

---

⚠️ Non-agent, non-institutional users and users with normal account status can complete tasks and claim rewards. Specific tasks and rewards are subject to final display on Gate official website/App.
```

---

## Exception Handling

| Exception Type | Handling Method |
|----------------|-----------------|
| Existing user (code=1001) | Execute existing user guidance: Prompt to visit https://www.gate.com/rewards_hub |
| Risk control user (code=1002) | Prompt: "Your account is temporarily unable to participate in new user activities, please contact customer service for details" |
| Sub-account (code=1003) | Prompt: "Sub-accounts cannot participate in new user activities, please log in with main account" |
| Agent user (code=1004) | Prompt: "Agent users cannot participate in new user activities" |
| Market maker (code=1005) | Prompt: "Market maker users cannot participate in new user activities" |
| Enterprise user (code=1006) | Prompt: "Enterprise users cannot participate in new user activities" |
| Not logged in (code=1008) | Prompt: "Please log in to your Gate account first before querying welfare tasks" |
| Unable to determine user type (interface timeout/exception) | Prompt: "Welfare information is temporarily unavailable, please try again later, or visit https://www.gate.com/rewards_hub directly" |
| New user task list is empty | Prompt: "No new user tasks available at the moment, please check later, or visit https://www.gate.com/rewards_hub for more benefits" |
| Interface returns other errors | Generic fallback: "Service is temporarily unavailable, please try again later" |

---

## Cross-Skill Integration

| User Follow-up Intent | Routing Target |
|-----------------------|----------------|
| User wants to complete "First Deposit" task | Route to deposit / funding Skill |
| User wants to complete "First Trade" task | Route to `gate-exchange-spot` |
| User wants to complete "Identity Verification" task | Show guidance text: Go to Gate web or open Gate App to complete KYC |
| User asks about asset balance | Route to `gate-exchange-assets` |

---

## Safety Rules

1. **Read-only queries**: This Skill only queries task information, does not execute task claiming, reward distribution or other write operations.
2. **Identity verification prerequisite**: Must complete user type determination first, must not show new user task list to existing users.
3. **Real data only**: **Strictly prohibit fabricating task information!** Must use real data returned by MCP interface, must not use fake reward information from example templates (such as "10 points", "5 USDT trial voucher", etc.).
4. **Data integrity**: All displayed task names, descriptions, reward amounts, reward units must come from real return values of `cex_welfare_get_beginner_task_list` interface.
5. **Disclaimer**: Task information is subject to final display on Gate official website, data returned by this Skill is for reference only.
6. **Required prompt text**: When displaying task rewards, must include the required prompt text as specified: "Non-agent, non-institutional users and users with normal account status can complete tasks and claim rewards. Specific tasks and rewards are subject to final display on Gate official website/App", must not be omitted.
