---
name: gate-exchange-launchpool-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for LaunchPool: project discovery, pledge/reward records, stake and redeem operations."
---

# Gate LaunchPool MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- LaunchPool project listing/discovery
- Pledge and reward records query
- Stake and redeem operations

Out of scope:
- Non-LaunchPool earn modules

## 2. MCP Detection and Fallback

Detection:
1. Verify LaunchPool endpoints are available.
2. Probe with project listing endpoint.

Fallback:
- If write endpoints unavailable, keep read-only project/record mode.

## 3. Authentication

- API key required.
- Stake/redeem are write operations requiring explicit confirmation.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

- `cex_launch_list_launch_pool_projects`
- `cex_launch_list_launch_pool_pledge_records`
- `cex_launch_list_launch_pool_reward_records`
- `cex_launch_create_launch_pool_order`
- `cex_launch_redeem_launch_pool`

## 6. Execution SOP (Non-Skippable)

1. Resolve intent: query projects/records vs stake/redeem.
2. For stake/redeem, validate project (`pid`), reward pool (`rid`), and amount.
3. Present action draft with lock/reward notes.
4. Require explicit confirmation.
5. Execute write operation and verify via records.

## 7. Output Templates

```markdown
## LaunchPool Action Draft
- Action: {stake_or_redeem}
- Project/Pool: {pid}/{rid}
- Amount: {amount}
- Notes: {reward_and_lockup_summary}
Reply "Confirm action" to proceed.
```

```markdown
## LaunchPool Result
- Status: {success_or_failed}
- Project/Pool: {pid}/{rid}
- Amount: {amount}
- Follow-up: {record_check_hint}
```

## 8. Safety and Degradation Rules

1. Never execute stake/redeem without explicit immediate confirmation.
2. Preserve pid/rid and amount exactly as user-confirmed.
3. If project not active or parameters invalid, block and explain why.
4. Keep read-only fallback when write endpoints are unavailable.
5. Do not promise reward outcomes.
