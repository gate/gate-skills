# Gate Exchange Affiliate Program Skill

## Overview

A read-oriented skill for Gate Exchange **Partner (affiliate)** data: commission history, referred users’ trading activity, subordinate lists, eligibility to apply, and recent application status. It uses Partner APIs only (not deprecated Agency APIs). Queries can span up to **180 days** by splitting into **30-day** API windows.

### Core Capabilities

- Commission and rebate history for the authenticated partner
- Trading volume and net fees from referred users’ transaction history
- Subordinate (referred user) list and customer counts
- Partner program eligibility check and recent application status (last 30 days)
- Time-range queries with UTC+8 boundaries and **no future timestamps**
- Safe aggregation guidance (avoid blind summation of list fields; respect `user_id` semantics)

## Execution Guardrail (Mandatory)

- **Authentication**: Requires a valid Gate identity with **partner** privileges (e.g. via configured MCP / `X-Gate-User-Id` as documented in `SKILL.md`).
- **`user_id` filter**: In `commission_history` and `transaction_history`, `user_id` filters by **trader**, not commission receiver. Do **not** use it for generic “my commission” queries—only when the user explicitly asks about a **specific trader UID**.
- **Time rules**: Compute ranges from the user’s current date in **UTC+8**; `to` must be ≤ current Unix time. Reject future-dated ranges.
- **Data scope**: Only query data for the authenticated partner; do not infer or access other partners’ data.

## Architecture

```
gate-exchange-affiliate/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    ├── scenarios.md
    └── quick-start.md
```

## Usage Examples

```
"Show my affiliate commission for the last 7 days."
"How much trading volume did my referrals generate this month?"
"Am I eligible to apply for the partner program?"
"What’s the status of my recent partner application?"
"List my subordinates and how many are direct vs indirect."
```

## Trigger Phrases

- my affiliate data / partner earnings / commission this week
- team performance / referral volume / net fees from referrals
- apply for affiliate / am I eligible / application status
- subordinate list / customer count / referred users

## Related Documentation

- Runtime rules shared with other exchange skills: follow the instruction in `SKILL.md` to read `exchange-runtime-rules.md` from the repository (see GitHub Gate Skills tree for the canonical copy).
- Detailed workflow, API tables, and report templates: `SKILL.md`
- Scenarios: `references/scenarios.md`
- Quick start: `references/quick-start.md`
