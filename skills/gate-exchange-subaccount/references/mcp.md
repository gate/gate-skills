---
name: gate-exchange-subaccount-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for Gate sub-account operations: list/query/create/lock/unlock with main-account authorization safeguards."
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

## 2. MCP Detection and Fallback

Detection:
1. Verify Gate main MCP exposes `cex_sa_list_sas` and `cex_sa_create_sa`.
2. Probe with read endpoint (`cex_sa_list_sas`).

Fallback:
- MCP/auth unavailable: return setup/auth guidance and stop writes.

## 3. Authentication

- API key required.
- Requires main-account privileges for sub-account management.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

| Tool | Purpose | Common errors |
|---|---|---|
| `cex_sa_list_sas` | list sub-accounts | permission denied |
| `cex_sa_get_sa` | fetch one sub-account detail | user_id invalid |
| `cex_sa_create_sa` | create sub-account | duplicate login_name |
| `cex_sa_lock_sa` | lock sub-account | already locked |
| `cex_sa_unlock_sa` | unlock sub-account | already unlocked |

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
