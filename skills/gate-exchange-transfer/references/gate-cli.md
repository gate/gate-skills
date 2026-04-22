---
name: gate-exchange-transfer-gate-cli
version: "2026.3.30-1"
updated: "2026-03-30"
description: "gate-cli execution specification for Gate internal transfer operations across spot, margin, futures, delivery and options accounts."
---

# Gate Exchange Transfer (`gate-cli`) Specification

## 1. Scope and Trigger Boundaries

In scope:
- Internal transfer under same UID between account types
- Transfer pre-check and post-transfer ledger verification

Out of scope:
- On-chain transfer/withdraw -> DEX wallet skills
- Spot/futures order placement -> trading skills

## 2. `gate-cli` detection and Fallback

Detection:
1. Validate host can run `gate-cli cex wallet transfer create`.
2. Verify with one account-book read endpoint.

Fallback:
- Missing `gate-cli` -> show installer guidance.
- Auth failure -> stop write calls and return recovery steps.

## 2.1 `gate-cli cex …` execution flow (MUST)

For every documented **`gate-cli cex …`** leaf command, **strictly** follow this order:

1. **Preflight with `--help`:** Run the same command with **`--help`** immediately after the full `cex …` subcommand path (before any other flags), e.g. `gate-cli cex spot account get --help`, to see whether the CLI marks any flags or arguments as **required**.
2. **If `--help` lists required fields** (e.g. `--currency`): obtain values (ask the user only for non-secret business inputs such as symbol or amount; never ask for API secrets in chat), then run the **real** invocation **without** `--help`, including every required flag, e.g. `gate-cli cex spot account get --currency BTC`.
3. **If `--help` shows no required fields** for that subcommand: you may run the bare **`gate-cli cex …`** (only add optional flags the task still needs for correct semantics).

**Example:** To run `gate-cli cex spot account get` — first run `gate-cli cex spot account get --help`. If help indicates `--currency` is mandatory, supply it (e.g. `--currency BTC`), then execute `gate-cli cex spot account get --currency BTC`. If nothing is required beyond auth, execute `gate-cli cex spot account get` as documented.

If `--help` is ambiguous, prefer a safe read-only probe or explicit user clarification—especially before writes.

## 3. Authentication

- API key required (wallet transfer permission).
- Never execute transfer if auth scope is insufficient.

## 4. Optional resources

No mandatory auxiliary resources.

## 5. `gate-cli` command specification

### 5.1 Read commands (verification)

| Command | Purpose |
|---|---|
| `gate-cli cex spot account book` | spot ledger verification |
| `gate-cli cex margin account book` | margin ledger verification |
| `gate-cli cex futures account book` | futures ledger verification |
| `gate-cli cex delivery account book` | delivery ledger verification |
| `gate-cli cex options account book` | options ledger verification |

### 5.2 Write commands

| Command | Purpose | Required key fields |
|---|---|---|
| `gate-cli cex wallet transfer create` | execute account-to-account transfer | currency, amount, from, to |

## 6. Execution SOP (Non-Skippable)

1. Parse `from/to` account type, currency, amount.
2. Validate account type mapping and amount positivity.
3. Build **Transfer Draft** (from, to, amount, currency, risk note).
4. Require explicit confirmation.
5. Execute `gate-cli cex wallet transfer create`.
6. Verify via relevant account-book endpoint(s).

## 7. Output Templates

```markdown
## Transfer Draft
- From: {from_account}
- To: {to_account}
- Currency: {currency}
- Amount: {amount}
- Risk: Internal transfer is usually irreversible.
Reply "Confirm transfer" to execute.
```

```markdown
## Transfer Result
- Status: {success_or_failed}
- Transfer ID: {tx_id}
- Currency/Amount: {currency} {amount}
- Verification: {ledger_check_summary}
```

## 8. Safety and Degradation Rules

1. Never execute transfers without explicit immediate confirmation.
2. Reject ambiguous source/target account names until clarified.
3. Preserve raw API error reasons for failed transfers.
4. If verification endpoints are degraded, mark result as "submitted, verification pending".
5. Do not infer cross-UID transfer; this skill is same-UID internal transfer only.
