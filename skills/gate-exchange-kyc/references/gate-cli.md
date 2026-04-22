---
name: gate-exchange-kyc-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for KYC portal guidance and runtime fallback behavior."
---

# Gate KYC MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- KYC portal entry guidance
- KYC process routing and non-execution explanation

Out of scope:
- In-chat document submission
- KYC status mutation or approval actions

Misroute examples:
- If user asks to trade, transfer, or withdraw operations, route to corresponding exchange skills.

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify Gate MCP runtime availability at session start.
2. If runtime is unavailable, continue with portal-only guidance.

Fallback:
- This skill can complete with static portal guidance even without callable `gate-cli` commands.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key is not required for returning the KYC portal link itself.
- If runtime policy requires authenticated context for user-specific guidance, request login first.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

No direct `gate-cli` commands invocation is required in this skill.

## 6. Execution SOP (Non-Skippable)

1. Confirm user intent is KYC or verification access.
2. Provide official portal URL: `https://www.gate.com/myaccount/profile/kyc_home`.
3. State that verification must be completed on the portal.
4. If user asks for status/doc upload in chat, redirect to portal or support.

## 7. Output Templates

```markdown
## KYC Guidance
- Portal: https://www.gate.com/myaccount/profile/kyc_home
- Steps: Log in, open portal, follow on-screen verification flow.
- Note: Verification is completed only on the official portal.
```

## 8. Safety and Degradation Rules

1. Never claim KYC is completed from chat-side actions.
2. Never request users to send sensitive identity documents in chat.
3. Use only official Gate portal/support endpoints.
4. If runtime unavailable, provide the same safe portal guidance without fabrication.
