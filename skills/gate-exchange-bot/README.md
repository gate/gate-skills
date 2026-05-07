# Gate Exchange Bot

## Overview

`gate-exchange-bot` is a `gate-cli`-style Gate Exchange skill for AIHub bot workflows. It covers strategy recommendation, manual bot creation, and basic running-strategy management.

This skill is intended for users aged 18 or above with full civil capacity. Availability may vary by product, account state, and local legal or regulatory restrictions.

## Core Capabilities

| Module | Description | Example |
|--------|-------------|---------|
| **Discover** | Recommend strategies by market, strategy type, filter, or refresh context | "Recommend a BTC strategy" |
| **Grid Create** | Manually create spot, margin, infinite, or futures grid bots | "Create a BTC spot grid from 60000 to 72000 with 50 grids and 1000 USDT" |
| **Martingale Create** | Manually create spot or contract martingale bots | "Create an ETH contract martingale with 5x leverage and 2% deviation" |
| **Portfolio Running** | List running strategies | "What bots do I have running?" |
| **Portfolio Detail** | Query one strategy detail | "Show detailed performance for that bot" |
| **Portfolio Stop** | Stop one concrete strategy after confirmation | "Stop that BTC grid bot" |

## Architecture

The skill uses a routing architecture:

- `SKILL.md` provides the top-level routing, safety rules, credential expectations, and product boundaries.
- `references/gate-cli.md` is the authoritative execution contract for `gate-cli cex bot ...` commands.
- `references/scenarios.md` provides scenario-style examples for validation and review.
- The remaining files in `references/` define per-product behavior for discover, grid creation, martingale creation, running-list queries, detail queries, and stop flows.

## Runtime and Installation Requirements

- `gate-cli` must be installed and available to the host runtime.
- `setup.sh` depends on `curl`, `tar`, and either `shasum` or `sha256sum`.
- `setup.sh` first attempts user-local installation into `$HOME/.openclaw/skills/bin`; if that fails, it may fall back to `sudo install` into `/usr/local/bin`.
- API credentials are expected through `gate-cli config init` or secure host-side environment configuration such as `GATE_API_KEY` and `GATE_API_SECRET`.

## Safety and Confirmation

- Recommendation and read-only portfolio queries do not mutate account state.
- Every create or stop action must present an Action Draft or equivalent confirmation summary first.
- No create or stop command should run without explicit user confirmation in the immediately following turn.
- Success must be judged from response `code` and `message`, not HTTP status alone.

## Data and Privacy

- User requests, bot parameters, and final payloads are passed through the host runtime, `gate-cli`, and the Gate APIs required for the requested operation.
- This skill does not define any extra telemetry, analytics sink, or custom persistence layer.
- Operators should assume the host environment may still keep shell history, terminal logs, or platform audit logs.
- Users should never paste API secrets into chat.

## Compliance

- Use of this skill must comply with local laws, platform rules, and product eligibility requirements.
- Some products may be unavailable due to account status, KYC state, geography, or risk controls.

## File Structure

```text
gate-exchange-bot/
├── README.md
├── SKILL.md
├── CHANGELOG.md
├── setup.sh
└── references/
    ├── gate-cli.md
    ├── scenarios.md
    ├── strategy-recommend.md
    ├── create-spot-grid.md
    ├── create-margin-grid.md
    ├── create-infinite-grid.md
    ├── create-futures-grid.md
    ├── create-spot-martingale.md
    ├── create-contract-martingale.md
    ├── list-running.md
    ├── get-detail.md
    └── stop-strategy.md
```

## Support

- For maintenance or review feedback, open an issue in this repository or contact the repository maintainers through the normal project support channel.
