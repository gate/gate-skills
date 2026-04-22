---
name: gate-exchange-launchpool-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for LaunchPool: project discovery, pledge/reward records, stake and redeem operations."
---

# Gate LaunchPool MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- LaunchPool project listing/discovery
- Pledge and reward records query
- Stake and redeem operations

Out of scope:
- Non-LaunchPool earn modules

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify LaunchPool endpoints are available.
2. Probe with project listing endpoint.

Fallback:
- If write endpoints unavailable, keep read-only project/record mode.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required.
- Stake/redeem are write operations requiring explicit confirmation.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

- `gate-cli cex launch projects`
- `gate-cli cex launch pledge-records`
- `gate-cli cex launch reward-records`
- `gate-cli cex launch pledge`
- `gate-cli cex launch redeem`

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
