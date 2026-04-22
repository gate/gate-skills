---
name: gate-exchange-welfare-gate-cli
version: "2026.4.10-1"
updated: "2026-04-10"
description: "gate-cli execution specification for welfare eligibility, newcomer task list query, task claim, completion guidance, and newcomer reward claim."
---

# Gate Welfare (`gate-cli`) specification

## 1. Scope and Trigger Boundaries

In scope:
- Determine newcomer welfare eligibility
- Fetch the newcomer beginner-task list
- Claim a single newcomer task
- Guide completion of KYC / first deposit / first trade newcomer tasks
- Claim all currently claimable newcomer rewards

Out of scope:
- Deposit execution
- Trading execution
- Non-welfare wallet/account operations
- Guessing thresholds, coupon titles, or activity rules not returned by MCP

Misroute examples:
- If the user wants to actually trade, hand off to `gate-exchange-trading`.
- If the user wants to check balances, route to `gate-exchange-assets`.

## 1.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex welfare beginner-tasks --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields:** obtain values (ask the user only for non-secret business inputs; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs).

**Cross-skill example (spot):** `gate-cli cex spot account get` → first `gate-cli cex spot account get --help`; if `--currency` is mandatory, then `gate-cli cex spot account get --currency BTC`; if nothing is required beyond auth, run `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 2. Authentication and Response Model

- Authenticated context/API key is required.
- Unauthenticated calls may return business `code=1008`.
- Welfare APIs use **business `code` in the response body** as the primary success signal, even when HTTP status is `200`.
- Gateway validation, rate-limit, or upstream failures may still return standard HTTP `4xx` with `label` + `message`.
- Always inspect the response `code` field before continuing a welfare flow.

## 3. Tool Allowlist

Read tools:
- `gate-cli cex welfare identity`
- `gate-cli cex welfare beginner-tasks`

Write tools:
- `cex_welfare_claim_task` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)
- `cex_welfare_claim_reward` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)

## 4. Task Status Semantics

| Status | Meaning | Agent Handling |
|--------|---------|----------------|
| `0` | Unclaimed | Can be claimed via `cex_welfare_claim_task` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) |
| `1` | Claimed / in progress | Guide completion only |
| `2` | Completed, reward claimable | Can be claimed via `cex_welfare_claim_reward` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) |
| `3` | Reward distributing | Inform user to wait |
| `4` | Completed / settled | Inform user already finished |
| `5` | Expired | Inform user expired |

Other task semantics:
- `task_desc` may contain HTML tags; remove tags before presenting the text.
- A download task may be returned with `task_type=23` and `status=0`.

## Workflow

### Query / list newcomer tasks

Required order:
1. `gate-cli cex welfare identity`
2. If `code=0`, `gate-cli cex welfare beginner-tasks`
3. Render real tasks only

Branching:
- `code=1001` -> existing-user rewards-hub guidance
- `code=1002/1003/1004/1005/1006/1008` -> mapped restriction guidance
- list `code=1007` or empty list -> no-task fallback

### Claim a single task

Required order:
1. `gate-cli cex welfare identity`
2. `gate-cli cex welfare beginner-tasks`
3. Select exactly one task with `status=0`
4. `cex_welfare_claim_task` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)

Rules:
- Prefer an explicit task named by the user.
- If exactly one claimable task exists, use it directly.
- If multiple claimable tasks exist, ask the user which one to claim.
- Never call `cex_welfare_claim_task` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) for tasks that are already `1/2/3/4/5`.

### Complete-task guidance

Required order:
1. `gate-cli cex welfare identity`
2. `gate-cli cex welfare beginner-tasks`
3. Resolve the target task from list state and user wording

Dispatch:
- KYC / identity verification -> generic KYC guidance
- First deposit -> generic deposit guidance
- First trade -> hand off to `gate-exchange-trading`
  - Reference: [gate-exchange-trading/references/execution-and-guardrails.md](https://github.com/gate/gate-skills/blob/master/skills/gate-exchange-trading/references/execution-and-guardrails.md)
- Ambiguous "complete task" -> ask which actionable task if multiple

### Claim newcomer rewards

Required order:
1. `gate-cli cex welfare identity`
2. `gate-cli cex welfare beginner-tasks`
3. Filter tasks with `status=2`
4. Call `cex_welfare_claim_reward` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二) sequentially for each selected task

Rules:
- General "claim reward" intent should claim **all** currently claimable newcomer rewards.
- If `coupon_full_name` is non-empty, use it in the success summary.
- If `coupon_full_name` is empty, fall back to the task list's `reward_num` + `reward_unit`.
- If `has_m_n_task=true`, do not describe the reward as claimed; redirect the user to the official rewards hub/App for that task.

## Error Handling

Eligibility / list errors:
- `1001` -> existing user
- `1002` -> risk-control user
- `1003` -> sub-account
- `1004` -> agent
- `1005` -> market maker
- `1006` -> enterprise
- `1007` -> no active newcomer task data
- `1008` -> not logged in

Task-claim errors:
- `51501009` -> invalid activity / task config unavailable
- `51501010` -> already claimed or conditions not met
- `51501026` -> risk reject

Reward-claim errors:
- `51501004` -> record does not exist
- `51501026` -> risk reject
- `51501027` -> refresh and retry
- `51501034` -> task expired

Gateway / transport errors:
- HTTP `4xx` with `label` + `message` -> stop and surface a brief fallback

## Report Template

```markdown
## Welfare Task List
- Task: {task_name}
- Description: {task_desc_without_html}
- Reward: {reward_num} {reward_unit}
- Status: {mapped_status}
- Next Step: {claim task / complete / claim reward / wait / completed / expired}
```

```markdown
## Task Claim Result
- Task: {task_name}
- Result: Claimed successfully
- Reward After Completion: {reward_num} {reward_unit}
```

```markdown
## Reward Claim Result
- Claimed Rewards:
- {task_name}: {coupon_full_name_or_reward_num_reward_unit}
- {task_name}: {coupon_full_name_or_reward_num_reward_unit}
```

## 8. Safety and Degradation Rules

1. Identity gate is mandatory before any newcomer task detail, task claim, or reward claim.
2. Use only the four tools in this spec.
3. Strip HTML tags from `task_desc` before presenting text.
4. Never fabricate task names, reward numbers, reward units, coupon names, or thresholds.
5. Treat response `code` as the source of truth.
6. Do not claim rewards for tasks not currently shown as `status=2`.
7. Do not claim tasks not currently shown as `status=0`.
8. For `has_m_n_task=true`, redirect to Gate web/App instead of marking the reward as claimed.
9. If APIs fail or data is inconsistent, fall back to `https://www.gate.com/zh/rewards_hub`.
