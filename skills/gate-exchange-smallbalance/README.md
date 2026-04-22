# Gate Exchange Small Balance Skill

## Overview

Gate Exchange Small Balance Skill exposes **dust / small-balance** workflows for Gate: list spot holdings eligible under the platform threshold, **convert** selected or all eligible balances to **GT**, and query **conversion history**. It is intended for `gate-cli`-backed agents with user authentication.

### Core Capabilities

| Capability | Description | `gate-cli` commands |
|------------|-------------|-----------|
| List eligible dust | Show currencies that qualify for small-balance conversion and estimated GT | `gate-cli cex wallet balance small` |
| Convert to GT | Convert explicit tickers or all eligible small balances (irreversible) | `gate-cli cex wallet balance convert-small` |
| History | Paginated log of past small-balance conversions | `gate-cli cex wallet balance small-history` |

## Architecture

This Skill uses **Standard Architecture** with a single `SKILL.md` and shared scenarios.

```
skills/gate-exchange-smallbalance/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

**Typical flow**:
1. Classify intent (list / convert / history / out-of-scope).
2. For **list**: `gate-cli cex wallet balance small`; if empty, explain clearly.
3. For **convert**: confirm tickers or **all eligible**, warn irreversibility, then `gate-cli cex wallet balance convert-small`.
4. For **history**: `gate-cli cex wallet balance small-history` with optional filters.

## Usage

Example triggers:
- "What small balances can I convert to GT?"
- "Convert my dust FLOKI and MBLK to GT"
- "Convert all eligible small coins to GT"
- "Show my small balance conversion history"

## Dependencies

- **`gate-cli`**: Gate CEX wallet tools (`cex_wallet_*` small-balance family).
- **Authentication**: **Required** for list, convert, and history.
- **API Key permissions**: Wallet / account access consistent with Gate API management for the authenticated user. **Write** permission is required for `gate-cli cex wallet balance convert-small`; read operations need matching read access.

## Tool routing (primary)

| Flow | `gate-cli` command |
|------|----------|
| List eligible dust | `gate-cli cex wallet balance small` |
| Convert | `gate-cli cex wallet balance convert-small` |
| History | `gate-cli cex wallet balance small-history` |

**Convert**: subset = non-empty `currencies` + `is_all: false`; all eligible = `is_all: true`. List/history rows may be nested — see `SKILL.md` **Payload note**.

Underlying HTTP (reference only): `GET/POST /wallet/small_balance`, `GET /wallet/small_balance_history`. Rate limits follow Gate API docs for wallet routes.
