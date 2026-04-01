---
name: gate-exchange-transfer-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP execution specification for Gate internal transfer operations across spot, margin, futures, delivery and options accounts."
---

# Gate Exchange Transfer MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Internal transfer under same UID between account types
- Transfer pre-check and post-transfer ledger verification

Out of scope:
- On-chain transfer/withdraw -> DEX wallet skills
- Spot/futures order placement -> trading skills

## 2. MCP Detection and Fallback

Detection:
1. Validate Gate main MCP exposes `cex_wallet_create_transfer`.
2. Verify with one account-book read endpoint.

Fallback:
- Missing MCP -> show installer guidance.
- Auth failure -> stop write calls and return recovery steps.

## 3. Authentication

- API key required (wallet transfer permission).
- Never execute transfer if auth scope is insufficient.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

### 5.1 Read tools (verification)

| Tool | Purpose |
|---|---|
| `cex_spot_list_spot_account_book` | spot ledger verification |
| `cex_margin_list_margin_account_book` | margin ledger verification |
| `cex_fx_list_fx_account_book` | futures ledger verification |
| `cex_dc_list_dc_account_book` | delivery ledger verification |
| `cex_options_list_options_account_book` | options ledger verification |

### 5.2 Write tool

| Tool | Purpose | Required key fields |
|---|---|---|
| `cex_wallet_create_transfer` | execute account-to-account transfer | currency, amount, from, to |

## 6. Execution SOP (Non-Skippable)

1. Parse `from/to` account type, currency, amount.
2. Validate account type mapping and amount positivity.
3. Build **Transfer Draft** (from, to, amount, currency, risk note).
4. Require explicit confirmation.
5. Execute `cex_wallet_create_transfer`.
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
