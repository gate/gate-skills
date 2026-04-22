---
name: gate-exchange-subaccount-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for Gate sub-account operations: list/query/create/lock/unlock with main-account authorization safeguards."
---

# Gate Sub-Account MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- List sub-accounts
- Query sub-account detail
- Create sub-account
- Lock/unlock sub-account

Out of scope:
- Sub-account key management beyond this skill flow
- Non-subaccount trading/account operations

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify Gate main `gate-cli` supports `gate-cli cex sub-account list` and `gate-cli cex sub-account create`.
2. Probe with read endpoint (`gate-cli cex sub-account list`).

Fallback:
- MCP/auth unavailable: return setup/auth guidance and stop writes.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required.
- Requires main-account privileges for sub-account management.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

| Command | Purpose | Common errors |
|---|---|---|
| `gate-cli cex sub-account list` | list sub-accounts | permission denied |
| `gate-cli cex sub-account get` | fetch one sub-account detail | user_id invalid |
| `gate-cli cex sub-account create` | create sub-account | duplicate login_name |
| `gate-cli cex sub-account lock` | lock sub-account | already locked |
| `gate-cli cex sub-account unlock` | unlock sub-account | already unlocked |

## 6. Execution SOP (Non-Skippable)

1. Resolve intent (`list/query/create/lock/unlock`).
2. Validate required params (e.g., `user_id`, `login_name`).
3. For write actions (`create/lock/unlock`), show action draft and require explicit confirmation.
4. Execute tool call.
5. Re-query status where applicable to confirm final state.

## 7. Output Templates

```markdown
## Sub-Account Action Draft
- Action: {create_or_lock_or_unlock}
- Target: {user_id_or_login_name}
- Risk: Sub-account state change affects access and trading.
Reply "Confirm" to proceed.
```

```markdown
## Sub-Account Result
- Status: {success_or_failed}
- Target: {subaccount_identifier}
- Current State: {normal_or_locked}
- Notes: {error_or_next_step}
```

## 8. Safety and Degradation Rules

1. Never perform `create/lock/unlock` without explicit confirmation.
2. If target sub-account is ambiguous, stop and ask for exact UID/login name.
3. Preserve API errors verbatim for admin troubleshooting.
4. Do not assume cross-main-account permissions.
5. Keep read-only fallback available when write permission is missing.
