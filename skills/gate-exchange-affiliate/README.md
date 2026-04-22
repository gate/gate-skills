# Gate Exchange Affiliate Program Skill

## Overview

`gate-exchange-affiliate` helps partners query and interpret Gate Exchange affiliate (Partner) program data: commission history, referred users’ trading activity, subordinate lists, eligibility to apply, and recent application status. It uses **Partner APIs only** (Agency APIs are out of scope). Queries can cover up to **180 days** by splitting requests into **30-day segments** per API limits.

## Core Capabilities

| Capability | Description |
|------------|-------------|
| Commission & trading history | Referred users’ trading records and commission records (time-bounded queries) |
| Team / subordinates | Subordinate list and customer counts |
| Partner onboarding | Eligibility check and recent application status (last 30 days for application API) |

### gate-cli command index (when gate-cli is configured)

| `gate-cli` command | Purpose |
|----------|---------|
| `gate-cli cex rebate partner transactions` | Referred users’ trading records |
| `gate-cli cex rebate partner commissions` | Commission records |
| `gate-cli cex rebate partner sub-list` | Subordinate list |
| `gate-cli cex rebate partner eligibility` | Whether the user may apply for partner |
| `gate-cli cex rebate partner application` | Recent partner application record |

When `gate-cli` is not available, the skill documents equivalent REST paths under `GET /rebate/partner/*` in `SKILL.md`.

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

The skill does not embed credentials. The gate-cli layer injects the user context (e.g. `X-Gate-User-Id`) when calling Partner APIs or `gate-cli` commands. Configure the gate-cli per your client (see [gate-cli](https://github.com/gate/gate-cli) for setup).

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
