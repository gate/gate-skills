# gate-exchange-welfare — Scenarios & Prompt Examples

## Scenario 1: Existing user queries welfare

**Context**: The user is an existing account holder asking about welfare access or newcomer rewards.

**Prompt Examples**:
- "What welfare do I have?"
- "How do I claim newcomer rewards?"

**Expected Behavior**:
1. Call `gate-cli cex welfare identity`.
2. If `code=1001`, do not call other welfare tools.
3. Return rewards-hub guidance.

---

## Scenario 2: Newcomer queries welfare task list (Base flow)

**Context**: The user is eligible for newcomer welfare and wants to see the current task list.

**Prompt Examples**:
- "What new user benefits are available?"
- "Show my new user tasks"

**Expected Behavior**:
1. Call `gate-cli cex welfare identity` and get `code=0`.
2. Call `gate-cli cex welfare beginner-tasks`.
3. Render all real tasks with reward, cleaned description, and mapped status.

---

## Scenario 3: Newcomer queries general tasks without saying "new user"

**Context**: The user asks for available tasks in a generic way and identity resolution is required.

**Prompt Examples**:
- "What tasks can I do?"
- "Task list"

**Expected Behavior**:
1. Call `gate-cli cex welfare identity`.
2. If `code=0`, enter the same flow as Scenario 2.

---

## Scenario 4: Claim a single task successfully (Case 1)

**Context**: A newcomer wants to claim one currently claimable welfare task, typically the download task.

**Prompt Examples**:
- "Claim task"
- "Claim the download task"

**Expected Behavior**:
1. Call `gate-cli cex welfare identity`.
2. Call `gate-cli cex welfare beginner-tasks`.
3. Find one task with `status=0`.
4. Call `cex_welfare_claim_task` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) with its `welfare_task_id`.
5. Reply that the task was claimed successfully and remind the user to complete it before claiming the reward.

---

## Scenario 5: Claim task but no claimable task is available

**Context**: The user wants to claim a task, but the current newcomer list has no `status=0` task.

**Prompt Examples**:
- "Claim task"

**Expected Behavior**:
1. Call identity and task list.
2. If no task with `status=0` exists, do not call `cex_welfare_claim_task` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二).
3. Tell the user there is no currently claimable newcomer task.

---

## Scenario 6: Complete identity verification task (Case 2)

**Context**: The user wants to finish the newcomer KYC task and needs guidance instead of a welfare write action.

**Prompt Examples**:
- "I want to complete the identity verification task"
- "How do I finish the KYC task?"

**Expected Behavior**:
1. Do not call a welfare write tool.
2. Return generic KYC guidance.

---

## Scenario 7: Complete first deposit task (Case 3)

**Context**: The user wants to finish the newcomer first-deposit task and needs deposit guidance.

**Prompt Examples**:
- "I want to complete the first deposit task"
- "How do I finish the deposit task?"

**Expected Behavior**:
1. Do not call a welfare write tool.
2. Return generic deposit guidance without inventing deposit thresholds.

---

## Scenario 8: Complete first trade task (Case 4)

**Context**: The user wants to finish the newcomer first-trade task and should be handed off to the trading skill.

**Prompt Examples**:
- "I want to complete the first trade task"
- "Help me do my first trade"

**Expected Behavior**:
1. Resolve this as a trade-completion flow.
2. Hand off to `gate-exchange-trading`.

---

## Scenario 9: Complete task with ambiguous intent (Case 5)

**Context**: The user says only "complete task" and the agent must resolve which actionable newcomer task is meant.

**Prompt Examples**:
- "I want to complete a task"
- "Help me finish my welfare task"

**Expected Behavior**:
1. Call identity and task list.
2. Collect actionable tasks from `status=0` and `status=1`.
3. If more than one actionable task exists, ask the user which task to complete.
4. If exactly one exists, dispatch to claim/KYC/deposit/trade guidance based on the task.

---

## Scenario 10: Claim all available rewards (Case 6)

**Context**: The user wants to claim all currently claimable newcomer rewards in one pass.

**Prompt Examples**:
- "Claim my rewards"
- "Claim all newcomer rewards"

**Expected Behavior**:
1. Call identity and task list.
2. Filter tasks with `status=2`.
3. Call `cex_welfare_claim_reward` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) for each status=`2` task.
4. Summarize all successfully claimed rewards using `coupon_full_name` when available.

---

## Scenario 11: Claim reward hits M-select-N pool

**Context**: A reward-claim attempt returns an M-select-N pool response and must be redirected to the rewards hub.

**Prompt Examples**:
- "Claim my reward"

**Expected Behavior**:
1. Call `cex_welfare_claim_reward` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二).
2. If `has_m_n_task=true`, do not describe the reward as claimed.
3. Tell the user to claim it from Gate web `https://www.gate.com/zh/rewards_hub` or the Gate App.

---

## Scenario 12: Claim reward but nothing is claimable

**Context**: The user asks to claim rewards, but the current newcomer list has no `status=2` task.

**Prompt Examples**:
- "Claim rewards"

**Expected Behavior**:
1. Call identity and task list.
2. If no task with `status=2` exists, do not call `cex_welfare_claim_reward` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二).
3. Tell the user there are no currently claimable newcomer rewards.

---

## Scenario 13: Identity lookup fails or times out

**Context**: The welfare identity gate fails, times out, or returns an unusable technical result.

**Prompt Examples**:
- "Check my welfare status"

**Expected Behavior**:
1. Do not enter claim/list flows.
2. Return the temporary-unavailable fallback and rewards-hub URL.

---

## Scenario 14: Task list returns no active tasks

**Context**: Identity succeeds for a newcomer, but the beginner-task list is empty or returns `code=1007`.

**Prompt Examples**:
- "What new user benefits are available?"

**Expected Behavior**:
1. Identity succeeds with `code=0`.
2. `gate-cli cex welfare beginner-tasks` returns `code=1007` or an empty list.
3. Tell the user there are currently no active newcomer tasks and suggest the rewards hub.

---

## Scenario 15: User is not logged in

**Context**: The user asks about welfare without an authenticated Gate session.

**Prompt Examples**:
- "What welfare benefits do I have?"

**Expected Behavior**:
1. `gate-cli cex welfare identity` returns `code=1008`.
2. Tell the user to log in first.

---

## Scenario 16: Risk-control user queries welfare

**Context**: The identity gate identifies the account as risk-controlled and ineligible for welfare participation.

**Prompt Examples**:
- "My welfare benefits"

**Expected Behavior**:
1. `gate-cli cex welfare identity` returns `code=1002`.
2. Return the risk-control guidance.

---

## Scenario 17: Sub-account queries welfare

**Context**: The welfare request comes from a sub-account that cannot participate in newcomer activities.

**Prompt Examples**:
- "Sub-account welfare"

**Expected Behavior**:
1. `gate-cli cex welfare identity` returns `code=1003`.
2. Tell the user to use the main account.

---

## Scenario 18: Agent user queries welfare

**Context**: The identity gate classifies the account as an agent account.

**Prompt Examples**:
- "Agent welfare benefits"

**Expected Behavior**:
1. `gate-cli cex welfare identity` returns `code=1004`.
2. Tell the user agent accounts cannot participate.

---

## Scenario 19: Market maker queries welfare

**Context**: The welfare request comes from a market-maker account that is excluded from newcomer benefits.

**Prompt Examples**:
- "Market maker welfare"

**Expected Behavior**:
1. `gate-cli cex welfare identity` returns `code=1005`.
2. Tell the user market maker accounts cannot participate.

---

## Scenario 20: Enterprise user queries welfare

**Context**: The identity gate classifies the account as an enterprise account.

**Prompt Examples**:
- "Enterprise welfare benefits"

**Expected Behavior**:
1. `gate-cli cex welfare identity` returns `code=1006`.
2. Tell the user enterprise accounts cannot participate.
