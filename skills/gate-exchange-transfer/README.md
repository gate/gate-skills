# Gate Exchange Transfer

## Overview

A skill for Gate Exchange internal fund transfers. Covers transfers between account types (spot, margin, futures, delivery, options), main-sub-account transfers, and sub-account to sub-account transfers.

### Core Capabilities

- Transfer between main account types (spot ↔ margin ↔ futures ↔ delivery ↔ options)
- Transfer from main account to sub-account
- Transfer from sub-account to main account
- Transfer between two sub-accounts
- Query transfer status

### Execution Guardrail (Mandatory)

Before any transfer execution, the assistant must:

1. Verify source account balance (sufficient funds)
2. Present a **Transfer Draft** (currency, amount, from, to)
3. Wait for explicit user confirmation (e.g. `Confirm transfer`, `Confirm`, `Proceed`)
4. Execute only after confirmation

If confirmation is missing or ambiguous, do not execute the transfer.

## Architecture

```
gate-exchange-transfer/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

## Usage Examples

```
"Transfer 1000 USDT from spot to futures."
"Move 500 USDT from futures to spot."
"Transfer 200 USDT to my sub-account 12345."
"Transfer 100 USDT from sub-account A to sub-account B."
"Check my last transfer status."
```

## Trigger Phrases

- transfer / move funds
- spot to futures / futures to spot
- transfer to sub-account / sub-account transfer
- move USDT to margin

## Prerequisites

- Gate MCP configured and connected
- Authentication (OAuth) required
- Sufficient balance in source account
