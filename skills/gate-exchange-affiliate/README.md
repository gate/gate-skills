# Gate Exchange Affiliate Program Skill

## Overview

`gate-exchange-affiliate` helps partners query and interpret Gate Exchange affiliate (Partner) program data: commission history, referred users’ trading activity, subordinate lists, eligibility to apply, and recent application status. It uses **Partner APIs only** (Agency APIs are out of scope). Queries can cover up to **180 days** by splitting requests into **30-day segments** per API limits.

## Core Capabilities

| Capability | Description |
|------------|-------------|
| Commission & trading history | Referred users’ trading records and commission records (time-bounded queries) |
| Team / subordinates | Subordinate list and customer counts |
| Partner onboarding | Eligibility check and recent application status (last 30 days for application API) |

### MCP Tools (when Gate MCP is configured)

| MCP tool | Purpose |
|----------|---------|
| `cex_rebate_partner_transaction_history` | Referred users’ trading records |
| `cex_rebate_partner_commissions_history` | Commission records |
| `cex_rebate_partner_sub_list` | Subordinate list |
| `cex_rebate_get_partner_eligibility` | Whether the user may apply for partner |
| `cex_rebate_get_partner_application_recent` | Recent partner application record |

When MCP is not available, the skill documents equivalent REST paths under `GET /rebate/partner/*` in `SKILL.md`.

## Architecture

```
gate-exchange-affiliate/
├── SKILL.md                 # Agent runtime instructions, workflows, API reference
├── README.md                # This file
├── CHANGELOG.md             # Version history
└── references/
    ├── scenarios.md         # Scenario-based examples
    └── quick-start.md       # Quick start notes
```

**Pattern**: Standard architecture — routing, judgment logic, and report templates live in `SKILL.md`.

## Usage examples

- "What is my affiliate commission this week?"
- "Show my partner team performance"
- "Am I eligible to apply for the affiliate program?"
- "What is the status of my partner application?"

## Authentication

The skill does not embed credentials. The Gate MCP layer injects the user context (e.g. `X-Gate-User-Id`) when calling Partner APIs or MCP tools. Configure the Gate MCP server per your client (see [Gate MCP](https://github.com/gateio/gate-mcp) for setup).

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
