# gate-exchange-welfare — Scenarios & Prompt Examples

## Scenario 1: Existing User Queries Welfare (Case 1)

**Context**: User asks about welfare or rewards, but identity is existing user (has trading history).

**Prompt Examples**:
- "What welfare do I have"
- "How can I claim rewards"
- "What tasks can I do"
- "What welfare benefits do I have"
- "How can I claim rewards"

**Expected Behavior**:
1. Call `cex_welfare_get_user_identity` (user type determination interface), return result: code=1001 (existing user).
2. Do not call any additional MCP tools.
3. Directly output guidance text:

```
Please visit Gate web at https://www.gate.com/rewards_hub or open Gate App to view welfare tasks and rewards.
```

---

## Scenario 2: New User Queries New User Benefits (Case 2)

**Context**: User asks about new user benefits or new user tasks, identity is new user (newly registered, has not completed any trades).

**Prompt Examples**:
- "What new user benefits are available"
- "How to claim new user rewards"
- "What new user tasks can I do"
- "What new user benefits are available"
- "Show me my new user tasks"

**Expected Behavior**:
1. Call `cex_welfare_get_user_identity` (user type determination interface), return result: code=0 (new user).
2. Call `cex_welfare_get_beginner_task_list` (query beginner guidance task list), return task list.
3. Format and output all tasks according to template (title, subtitle, rewards, action buttons), append restriction condition prompt at the end:

```
🎁 Your exclusive new user tasks are as follows. Complete tasks to claim corresponding rewards:

{Generate dynamically based on actual task data returned from MCP interface, for example:}

📌 {Real task name obtained from MCP interface}
   {Real task description obtained from MCP interface}
   💰 Reward: {Real reward amount from MCP interface} {Real reward unit from MCP interface}
   Status: {Display based on status field returned by MCP interface}

{Continue displaying other real tasks...}

---

⚠️ Non-agent, non-institutional users and users with normal account status can complete tasks and claim rewards. Specific tasks and rewards are subject to final display on Gate official website/App.
```

---

## Scenario 3: New User Queries General Tasks (trigger words do not contain "new user")

**Context**: User says "what tasks", does not explicitly mention "new user", identity is new user.

**Prompt Examples**:
- "What tasks can I do"
- "What tasks are available"
- "Task list"

**Expected Behavior**:
1. Call `cex_welfare_get_user_identity` (user type determination interface), return result: code=0 (new user).
2. Enter Case 2 flow, same as Scenario 2, show new user task list.

---

## Scenario 4: Interface Timeout / User Type Determination Failed

**Context**: Calling user type determination interface times out or returns error.

**Prompt Examples**:
- "Check welfare status"
- "What welfare do I have"

**Expected Behavior**:
1. Do not enter Case 1 or Case 2 branch.
2. Output fallback text:

```
Welfare information is temporarily unavailable, please try again later, or visit https://www.gate.com/rewards_hub directly.
```

---

## Scenario 5: New User Task List is Empty

**Context**: User is new user, but task query interface returns empty list (activity not started or account exception).

**Prompt Examples**:
- "New user benefits"
- "What new user benefits are available"

**Expected Behavior**:
1. Step 1 determines user as new user.
2. Step 2 calls task interface, returns empty list.
3. Output fallback text:

```
No new user tasks available at the moment, please check later, or visit https://www.gate.com/rewards_hub for more benefits.
```

---

## Scenario 6: User Not Logged In

**Context**: User asks about welfare tasks while not logged in.

**Prompt Examples**:
- "What welfare benefits do I have"
- "What welfare do I have"

**Expected Behavior**:
1. Call `cex_welfare_get_user_identity` (user type determination interface), return result: code=1008 (not logged in).
2. Output prompt text:

```
Please log in to your Gate account first before querying welfare tasks.
```

---

## Scenario 7: New User Asks How to Complete "First Deposit" Task (Cross-Skill)

**Context**: New user sees task list and asks how to complete "First Deposit" task.

**Prompt Examples**:
- "How to deposit"
- "How to complete deposit task"
- "I want to deposit"

**Expected Behavior**:
1. Identify user intent as completing deposit task.
2. Route to deposit/funding Skill, do not handle deposit process within this Skill.

---

## Scenario 8: New User Asks How to Complete "First Trade" Task (Cross-Skill)

**Context**: New user sees task list and asks how to complete "First Trade" task.

**Prompt Examples**:
- "How to trade"
- "I want to buy coins"
- "How to complete trading task"

**Expected Behavior**:
1. Identify user intent as completing trading task.
2. Route to `gate-exchange-spot`, do not handle trading process within this Skill.

---

## Scenario 9: New User Asks How to Complete "Identity Verification" Task (Cross-Skill)

**Context**: New user sees task list and asks how to complete KYC verification task.

**Prompt Examples**:
- "How to complete identity verification"
- "How to do KYC"
- "Where is identity verification"

**Expected Behavior**:
1. Identify user intent as completing KYC task.
2. Output guidance text, do not route to other Skills:

```
Please visit Gate web or open Gate App, go to welfare center to complete identity verification task. Once verified, you can claim corresponding rewards.
```

---

## Scenario 10: Risk Control User Queries Welfare

**Context**: User asks about welfare, but account is in risk control status.

**Prompt Examples**:
- "My welfare benefits"
- "What welfare benefits can I get"

**Expected Behavior**:
1. Call `cex_welfare_get_user_identity` (user type determination interface), return result: code=1002 (risk control).
2. Output prompt text:

```
Your account is temporarily unable to participate in new user activities, please contact customer service for details.
```

---

## Scenario 11: Sub-account Queries Welfare

**Context**: User uses sub-account to ask about welfare.

**Prompt Examples**:
- "Sub-account welfare"
- "Sub-account welfare benefits"

**Expected Behavior**:
1. Call `cex_welfare_get_user_identity` (user type determination interface), return result: code=1003 (sub-account).
2. Output prompt text:

```
Sub-accounts cannot participate in new user activities, please log in with main account.
```

---

## Scenario 12: Agent User Queries Welfare

**Context**: Agent user asks about welfare.

**Prompt Examples**:
- "Agent welfare benefits"
- "Agent user benefits"

**Expected Behavior**:
1. Call `cex_welfare_get_user_identity` (user type determination interface), return result: code=1004 (agent).
2. Output prompt text:

```
Agent users cannot participate in new user activities.
```

---

## Scenario 13: Market Maker User Queries Welfare

**Context**: Market maker user asks about welfare.

**Prompt Examples**:
- "Market maker welfare"
- "Market maker benefits"

**Expected Behavior**:
1. Call `cex_welfare_get_user_identity` (user type determination interface), return result: code=1005 (market maker).
2. Output prompt text:

```
Market maker users cannot participate in new user activities.
```

---

## Scenario 14: Enterprise User Queries Welfare

**Context**: Enterprise user asks about welfare.

**Prompt Examples**:
- "Enterprise welfare benefits"
- "Enterprise user benefits"

**Expected Behavior**:
1. Call `cex_welfare_get_user_identity` (user type determination interface), return result: code=1006 (enterprise).
2. Output prompt text:

```
Enterprise users cannot participate in new user activities.
```
