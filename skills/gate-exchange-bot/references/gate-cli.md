---
name: gate-exchange-bot-gate-cli
version: "2026.5.6-1"
updated: "2026-05-06"
description: "gate-cli execution specification for Gate bot workflows: strategy recommendation, manual grid or martingale creation, running strategy detail, and single-strategy stop."
---

# Gate Bot execution specification (`gate-cli`)

> Authoritative execution specification for `gate-cli cex bot`. `SKILL.md` handles intent routing; this file defines command probing, parameter passing, confirmation gates, and verification rules.

## 1. Scope and Trigger Boundaries

In scope:
- AIHub strategy recommendation
- Manual grid creation: spot, margin, infinite, futures
- Manual martingale creation: spot, contract
- Portfolio running list, single-strategy detail, and single-strategy stop

Out of scope / route elsewhere:
- Regular spot/futures order placement outside bot products
- Running-strategy advanced management not explicitly documented
- Batch stop or hidden bulk operations

## 2. `gate-cli` availability and fallback

Detection:
1. The **`gate-cli`** binary must be installed and runnable (see `SKILL.md` and `setup.sh`).
2. Confirm the host can run a read path such as `gate-cli cex bot strategy recommend --help`.
3. Before private bot calls, confirm credentials are configured and accepted by `gate-cli`.

Fallback:
- `gate-cli` missing: install per `SKILL.md` and retry read-only probe first.
- Auth failure: stop all writes and return credential recovery guidance.
- Endpoint degradation: keep the conversation in explanation or draft mode; do not fabricate execution success.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), for example `gate-cli cex bot portfolio detail --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields**: obtain values (ask the user only for non-secret business inputs such as symbol, amount, strategy id, or strategy type; never ask for API secrets in chat), then run the real invocation without `--help`, including every required flag.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** and add only the optional flags the task still needs for correct semantics.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- Configure credentials with **`gate-cli config init`** or supported env vars / flags (`GATE_API_KEY`, `GATE_API_SECRET`, `--api-key`, `--api-secret`) without pasting secrets into chat.
- API key required for bot recommendation, create, portfolio detail, running list, and stop.
- Minimal permissions: Bot:Read for recommendation/list/detail; Bot:Write for create/stop.
- On auth or permission errors, do not retry writes blindly.

## 4. Optional resources

No bundled auxiliary resources are required for this skill.

## 5. Command specification (`gate-cli`)

### 5.1 Read commands

| Command | Purpose | Input style | Key return fields | Common errors |
|---|---|---|---|---|
| `gate-cli cex bot strategy recommend` | discover recommendation | query-style flags | `code`, `message`, `data.recommendations` | invalid filter, unsupported strategy |
| `gate-cli cex bot portfolio running` | list running strategies | query-style flags | `code`, `data.items`, `data.total` | auth, invalid page |
| `gate-cli cex bot portfolio detail` | query single strategy detail | query-style flags | `code`, `data.strategy_id`, `data.metrics`, `data.position` | invalid strategy id/type |

### 5.2 Write commands

| Command | Purpose | Required payload pattern | Key return fields | Common errors |
|---|---|---|---|---|
| `gate-cli cex bot spot-grid create` | create manual spot grid | `body` JSON string | `code`, `message`, `data` | invalid range, insufficient balance |
| `gate-cli cex bot margin-grid create` | create manual margin grid | `body` JSON string | `code`, `message`, `data` | invalid leverage, unsupported pair |
| `gate-cli cex bot infinite-grid create` | create manual infinite grid | `body` JSON string | `code`, `message`, `data` | invalid floor/profit fields |
| `gate-cli cex bot futures-grid create` | create manual futures grid | `body` JSON string | `code`, `message`, `data` | invalid direction/leverage |
| `gate-cli cex bot spot-martingale create` | create manual spot martingale | `body` JSON string | `code`, `message`, `data` | invalid ratio, invalid stop-loss field |
| `gate-cli cex bot contract-martingale create` | create manual contract martingale | `body` JSON string | `code`, `message`, `data` | invalid direction/leverage |
| `gate-cli cex bot portfolio stop` | stop one strategy | `body` JSON string | `code`, `message`, `data.status` | invalid strategy id/type |

## 6. Execution SOP (Non-Skippable)

### 6.1 Universal pre-check
1. Identify whether the flow is read-only or mutating.
2. Normalize market / strategy type terminology before building flags or `body`.
3. For write flows, validate that all required business parameters are already collected.

### 6.2 Recommendation flow
1. Determine `scene`: `top1`, `bundle`, `filter`, or `refresh`.
2. Use query-style parameters only.
3. Return recommendations exactly from backend results; do not invent unsupported strategy types.

### 6.3 Mandatory confirmation gate for writes
Before any create or stop command:
- produce a draft / confirmation summary
- echo all critical parameters and normalized percentages
- wait for explicit user confirmation in the immediately following turn

### 6.4 Write execution flow
1. Pre-check parameters.
2. Build the final JSON business payload.
3. Pass that payload through **`body`** as a JSON string.
4. Execute the write command.
5. Verify result using returned `code`, `message`, and key `data` fields.

### 6.5 Portfolio stop flow
1. If target strategy is ambiguous, first call `gate-cli cex bot portfolio running`.
2. Let the user choose one exact strategy.
3. Present stop risk summary by strategy type.
4. Execute `gate-cli cex bot portfolio stop` only after explicit confirmation.

## Workflow

1. Probe the target `gate-cli cex bot ...` command with `--help`.
2. Resolve whether the flow is read-only or mutating.
3. Collect query flags or build the final `body` JSON string, depending on the command class.
4. For writes, present an Action Draft and require explicit confirmation.
5. Execute the command and evaluate response `code`, `message`, and `data`.

## 7. Output Templates

```markdown
## Bot Action Draft
- Action: {recommend | create | stop}
- Strategy Type: {strategy_type}
- Market: {market_or_n/a}
- Key Params: {normalized_summary}
- Risk: {risk_note}
Reply "Confirm action" to proceed.
```

```markdown
## Bot Execution Result
- Status: {success_or_failed}
- Code: {code}
- Message: {message}
- Strategy ID / Context: {id_or_refresh_context}
- Next Check: {follow_up_hint}
```

## Report Template

```markdown
## Bot Command Summary
- Command: {gate_cli_command}
- Flow Type: {read_or_write}
- Inputs: {key_inputs}
- Result Code: {code}
- Result Message: {message}
- Follow-up: {follow_up_hint}
```

## 8. Safety and Degradation Rules

1. Never execute create or stop without explicit final confirmation.
2. Never guess core strategy parameters that the user has not decided.
3. When ratio fields are required, always show both the user-facing percentage and the normalized decimal string before execution.
4. Preserve backend `message` on failures; do not invent thresholds, region lists, or hidden business rules.
5. Recommendation is read-only and must not be conflated with create.
6. Ambiguous stop requests must not be silently expanded into multiple stop calls.
