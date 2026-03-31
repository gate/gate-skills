---
name: gate-exchange-welfare-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for welfare identity check and beginner task list retrieval."
---

# Gate Welfare MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Identify user welfare eligibility
- Fetch beginner task list for eligible new users
- Return guidance for non-eligible users

Out of scope:
- Reward claiming/distribution writes
- Unrelated trading/account operations

Misroute examples:
- If user asks to trade or transfer assets, route to corresponding exchange skills.

## 2. MCP Detection and Fallback

Detection:
1. Verify welfare endpoints are available.
2. Probe with identity endpoint first.

Fallback:
- If welfare APIs unavailable, provide official rewards hub fallback guidance.

## 3. Authentication

- Authenticated context/API key required for user-specific identity and tasks.
- If not logged in or auth invalid, return login guidance and stop.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

Read tools:
- `cex_welfare_get_user_identity`
- `cex_welfare_get_beginner_task_list`

Required sequence:
1. Call identity endpoint first.
2. Only if user is eligible new user, call beginner task list endpoint.

Common error handling:
- code 1001 existing user -> rewards hub guidance
- code 1002/1003/1004/1005/1006/1008 -> return mapped restriction guidance

## 6. Execution SOP (Non-Skippable)

1. Receive welfare/reward/task intent.
2. Call `cex_welfare_get_user_identity`.
3. Branch by returned code:
   - eligible new user -> fetch and render task list
   - otherwise -> render mapped restriction/guidance
4. Render only real API-returned tasks and reward fields.

## 7. Output Templates

```markdown
## Welfare Result
- Identity Status: {new_user_or_restriction_code}
- Next Step: {task_list_or_rewards_hub_or_login_or_support}
```

```markdown
## Beginner Task List
- Task: {task_name}
- Description: {task_desc}
- Reward: {reward_num} {reward_unit}
- Status: {pending_or_completed}
```

## 8. Safety and Degradation Rules

1. Never fabricate task names, reward amounts, or statuses.
2. Never show new-user task details before identity gate passes.
3. Keep this skill read-only.
4. If APIs fail, return explicit fallback to official rewards hub.
5. Preserve restriction-code semantics in user-facing guidance.
