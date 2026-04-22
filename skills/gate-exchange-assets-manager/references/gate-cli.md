---
name: gate-exchange-assets-manager-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for cross-account asset manager (L2): multi-account overview, risk checks, earn/alpha/rebate aggregation, and unified-account mutations."
---

# Gate Assets Manager MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Multi-account asset overview (spot/futures/margin/options/tradfi/unified/earn/alpha/rebate)
- Risk snapshots and account-health summary
- Unified-account write actions exposed in this skill

Out of scope:
- Direct spot/futures order execution
- On-chain DEX wallet operations

## 2. `gate-cli` detection and Fallback

Detection:
1. Confirm Gate MCP is available.
2. Probe with one baseline read (`gate-cli cex wallet balance total` or `gate-cli cex unified account get`).

Fallback:
- If partial modules fail, return partial report with degraded markers per module.
- If write module unavailable, keep skill in read-only mode and disclose limitation.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required for account data and mutations.
- For unified mutations, require proper permission and explicit confirmation.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

### 5.1 Portfolio aggregation (read)

- `gate-cli cex wallet balance total`
- `gate-cli cex spot account get`
- `gate-cli cex margin account list`
- `gate-cli cex futures account get`
- `gate-cli cex futures position list`
- `gate-cli cex options account get`
- `gate-cli cex tradfi account assets`
- `gate-cli cex unified account get`

### 5.2 Market/reference context (read)

- `gate-cli cex spot market tickers`
- `gate-cli cex spot market candlesticks`
- `gate-cli cex spot market orderbook`
- `gate-cli cex spot market trades`
- `gate-cli cex futures market tickers`
- `gate-cli cex futures market candlesticks`
- `gate-cli cex futures market orderbook`
- `gate-cli cex futures market trades`
- `gate-cli cex futures market contract`
- `gate-cli cex futures market funding-rate`
- `gate-cli cex futures market premium`

### 5.3 Earn/alpha/rebate modules (read)

- `gate-cli cex alpha account balances`
- `gate-cli cex alpha market tokens`
- `gate-cli cex alpha market tickers`
- `gate-cli cex alpha market currencies`
- `gate-cli cex earn staking assets`
- `gate-cli cex earn staking awards`
- `gate-cli cex earn staking find`
- `gate-cli cex earn uni currency`
- `gate-cli cex earn uni interest`
- `gate-cli cex earn uni rate`
- `gate-cli cex earn uni lends`
- `gate-cli cex earn dual balance`
- `gate-cli cex earn dual orders`
- `cex_earn_list_structured_orders` (no `gate-cli` mapping in `gate-cli/cmd/cex`; see `MCP_LEGACY_TOOL_RESOLUTION.md` §二)
- `gate-cli cex earn staking orders`
- `gate-cli cex earn uni currencies`
- `gate-cli cex rebate broker commissions`
- `gate-cli cex rebate broker transactions`
- `gate-cli cex rebate partner commissions`
- `gate-cli cex rebate partner transactions`
- `gate-cli cex rebate partner sub-list`
- `gate-cli cex rebate user-info`
- `gate-cli cex rebate sub-relation`

### 5.4 Ledger/risk helpers (read)

- `gate-cli cex spot account book`
- `gate-cli cex futures market liquidations`
- `gate-cli cex unified mode get`
- `gate-cli cex unified query borrowable`
- `gate-cli cex unified query transferable`
- `gate-cli cex unified query estimate-rate`
- `gate-cli cex unified config leverage-get`
- `gate-cli cex unified config discount-tiers`
- `gate-cli cex unified account currencies`
- `gate-cli cex unified loan records`
- `gate-cli cex unified loan interest`

### 5.5 Mutations (write)

- `gate-cli cex unified loan create`
- `gate-cli cex unified mode set`
- `gate-cli cex unified config collateral`
- `gate-cli cex unified config leverage-set`

## 6. Execution SOP (Non-Skippable)

1. Determine user target modules (portfolio only vs include risk vs include mutation).
2. Execute read modules in parallel where independent.
3. Merge data with explicit module tags and timestamps.
4. For any mutation, present action draft and require explicit confirmation.
5. Execute mutation only after confirmation; re-read relevant account state.

## 7. Output Templates

```markdown
## Assets Manager Snapshot
- Total Balance: {total_balance}
- Core Accounts: {spot/futures/margin/options/unified summary}
- Risk Flags: {imr_mmr_liquidation_signals}
- Earn/Alpha/Rebate: {module_highlights}
- Data Freshness: {timestamps}
```

```markdown
## Unified Mutation Draft
- Action: {borrow/repay/mode/collateral/leverage}
- Target: {currency_or_mode}
- Value: {amount_or_setting}
- Risk: {key_risk_note}
Reply "Confirm action" to execute.
```

## 8. Safety and Degradation Rules

1. Distinguish read aggregation from write execution clearly.
2. On partial module failure, keep successful modules and mark failed modules explicitly.
3. Never execute unified mutations without explicit immediate confirmation.
4. Keep numeric precision as returned by APIs (no silent rounding for risk fields).
5. For stale/empty modules, return "no data / unavailable" instead of inferred numbers.
