---
name: gate-exchange-staking-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for staking/earn staking flows: staking assets, rewards, orders, and stake/redeem actions."
---

# Gate Staking MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Staking asset/reward/order queries
- Staking coin discovery
- Stake/redeem execution

Out of scope:
- Non-staking trading actions

## 2. `gate-cli` detection and Fallback

Detection:
1. Verify staking-related `cex_earn_*` tools.
2. Probe with `gate-cli cex earn staking assets`.

Fallback:
- If write endpoint unavailable, provide read-only staking status.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

- `gate-cli cex earn staking assets`
- `gate-cli cex earn staking awards`
- `gate-cli cex earn staking find`
- `gate-cli cex earn staking orders`
- `gate-cli cex earn staking swap`

## 6. Execution SOP (Non-Skippable)

1. Resolve user intent: query vs stake/redeem.
2. For stake/redeem, pre-check coin and amount validity.
3. Show stake/redeem draft with operation side and amount.
4. Require explicit confirmation.
5. Execute and verify through order/asset query.

## 7. Output Templates

```markdown
## Staking Action Draft
- Action: {stake_or_redeem}
- Coin: {coin}
- Amount: {amount}
- Notes: {protocol_or_limit}
Reply "Confirm action" to proceed.
```

```markdown
## Staking Result
- Status: {success_or_failed}
- Coin/Amount: {coin} {amount}
- Updated Position: {position_summary}
```

## 8. Safety and Degradation Rules

1. Never execute stake/redeem without explicit immediate confirmation.
2. Preserve operation side (`stake` vs `redeem`) exactly.
3. If amount/coin invalid, block and explain constraints.
4. Keep read-only fallback when write path is unavailable.
5. Do not fabricate reward projections.
