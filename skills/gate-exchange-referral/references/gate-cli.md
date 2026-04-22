---
name: gate-exchange-referral-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for referral recommendation/rule interpretation skill. Current capability is primarily policy guidance with optional status checks when available."
---

# Gate Referral MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Invite-friends activity recommendation
- Rule interpretation for Earn Together / Help & Get Coupons / Super Commission
- Participation constraints and FAQ explanation

Out of scope:
- Executing referral actions on behalf of users
- Real-time reward progress APIs not exposed in this skill

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify Gate MCP availability for the skill runtime.
2. If no referral-specific tool is listed for this skill, run in policy-guidance mode.

Fallback:
- If no usable `gate-cli` commands is available, continue with deterministic rule-based guidance from skill knowledge.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key may be required by runtime policy, but this skill's primary flow is non-transactional guidance.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

This skill currently has **no explicitly listed `gate-cli` commands calls** in `SKILL.md` for runtime execution.
Execution is guidance-first and rule-interpretation-first.

## 6. Execution SOP (Non-Skippable)

1. Classify intent: recommendation / rule interpretation / FAQ / boundary query.
2. Apply decision table and activity constraints from `SKILL.md`.
3. Return structured recommendation/explanation with official referral URL.
4. For unsupported data-progress queries, transparently disclose boundary and redirect.

## 7. Output Templates

```markdown
## Referral Guidance
- Recommended Program: {program_name}
- Why: {fit_reason}
- Participation Steps: {short_steps}
- Key Notes: {constraints_and_timeline}
- Official Page: https://www.gate.com/referral
```

## 8. Safety and Degradation Rules

1. Do not fabricate live reward progress or unsupported account metrics.
2. Clearly separate platform rules from user-specific data.
3. Always include the official referral URL for final confirmation.
4. Keep timelines/constraints consistent with `SKILL.md` definitions.
5. If user asks unsupported operational actions, explain boundary and provide official path.
