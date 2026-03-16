# Gate Exchange Unified Account

## Overview

An integrated execution skill for Gate unified account operations, covering account overview, borrowable and transferable checks, borrowing and repayment, loan and interest history, account mode switching, leverage settings, and collateral management.

### Core Capabilities

- Account overview and mode checks (total equity, margin indicators, current unified mode)
- Borrow and repay workflows (limit checks, partial/full repayment handling)
- Loan and interest tracking (records, estimated rates, supported borrow currencies)
- Transferability checks (single and multi-currency aggregation via iterative queries)
- Risk configuration (per-currency leverage and collateral currency settings)

## Execution Guardrail (Mandatory)

Before any real mutation action (`cex_unified_create_unified_loan`, `cex_unified_set_unified_mode`, `cex_unified_set_user_leverage_currency_setting`, `cex_unified_set_unified_collateral`), the assistant must:

1. Send an **Action Draft** first (target, amount/config, pre-check result, risk note)
2. Wait for explicit user confirmation (for example: `Confirm action`, `Confirm`, `Proceed`)
3. Execute the mutation only after confirmation

If confirmation is missing or ambiguous, the assistant must stay in query mode and must not execute mutation calls.

Hard gate rules:
- NEVER call a mutation tool without explicit confirmation in the immediately previous user turn.
- Any parameter/topic change invalidates old confirmation and requires a new draft plus reconfirmation.
- For multi-step actions, require per-step confirmation before each mutation call.

## Output Quality Rules

- Keep numeric values consistent with API precision (no automatic rounding).
- Do not trim or shorten decimal values; display numeric strings exactly as returned by the API.
- For timestamps, return both raw timestamp and readable local time.
- Use fixed unified-mode labels:
  - `classic` -> `经典现货模式`
  - `single_currency` -> `单币种保证金模式`
  - `multi_currency` -> `跨币种保证金模式`
  - `portfolio` -> `组合保证金模式`
- In account-overview responses, include IMR/MMR explicitly:
  - IMR: `totalInitialMarginRate`
  - MMR: `totalMaintenanceMarginRate`
- When per-currency `balances` fields are shown, include `imr` and `mmr` for each reported currency when present.
- If unified account is not enabled/opened, place `⚠️ 当前账户未开通统一账户功能。` at the top.

## Architecture

```
gate-exchange-unified/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

## Usage Examples

```
"Query my unified account total equity and current mode."
"How much USDT can I borrow in unified account?"
"Borrow 200 USDT, but check max borrowable first."
"Repay all my BTC loan."
"Set my ETH leverage to 5x."
"Enable BTC and ETH as collateral and disable SOL."
```

## Trigger Phrases

- unified account / account mode / portfolio mode
- borrow limit / max borrowable / borrow now / repay loan
- loan records / interest records / borrow rate
- max transferable / transferable limit
- set leverage / leverage config / set collateral currencies
