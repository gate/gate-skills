# New Coin Due Diligence and Event Radar

## Overview

**`gate-exchange-newcoin`** (product codename **New Coin Radar**) is an L2 **`gate-cli`** skill for **new listings**, **pre-listing research**, **LaunchPool-style calendars**, **risk screening**, **event and sentiment context**, **spot microstructure snapshots**, and **optional first spot or Alpha orders** gated by **Action Draft** plus explicit **Y/N** confirmation.

Execution uses **`gate-cli`** namespaces **`info`**, **`news`**, and **`cex`** only. Reads cover **10** deduplicated leaf commands; writes cover **2** (`cex spot order`, `cex alpha order place`). Install [`gate-cli`](https://github.com/gate/gate-cli) via [`setup.sh`](./setup.sh) when absent.

### Core capabilities

| Area | Capability |
|------|------------|
| Listings | Exchange announcements, launch project enumeration |
| Fundamentals | Coin info, news search |
| Risk | Token security screening; optional address info when user gives address + chain |
| Heat | Latest events, social sentiment, ticker, orderbook depth |
| Execution | First spot / Alpha orders **after** Action Draft **and** user **Y** |

### Naming note

Skill id **`gate-exchange-newcoin`** follows **`gate-{category}-{title}`** (`exchange` = CEX listings and related flows). Legacy aliases: **`gate-newcoin`** (early short id), **`gate-info-newcoin`** (previous package name).

## Execution guardrail (mandatory)

Before **`gate-cli cex spot order buy|sell`** or **`gate-cli cex alpha order place`**:

1. Deliver **Action Draft** (pair, side, type, amount meaning, estimates, fees, liquidity warning).
2. Wait for explicit confirmation (**Y** / **N**).
3. Execute only on **Y** for **that** draft.

Without confirmation, stay read-only.

## Architecture

```
gate-exchange-newcoin/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── setup.sh                    # installs gate-cli (same pattern as gate-exchange-spot)
└── references/
    ├── gate-cli.md             # gate-cli execution contract (12-leaf minimal loop)
    ├── gate-runtime-rules.md   # bundled runtime rules for auditors
    └── scenarios.md            # Scenario 1–7 templates
```

## Prerequisites

- **`gate-cli`** on PATH or under `~/.openclaw/skills/bin/gate-cli` after [`setup.sh`](./setup.sh).
- **`GATE_API_KEY`** / **`GATE_API_SECRET`** (or `gate-cli config init`) **for writes** only.

## Usage examples

```
"What listed on Gate recently that looks safer and talked about?"
"Due diligence only on XYZ before listing."
"This new coin pumped — rug check and whether I should chase a tiny spot buy."
"This week's LaunchPool calendar with rough risk labels."
```

## Trigger phrases

- new listing / listing announcement / launchpool / launch calendar
- due diligence / fundamentals / tokenomics (new coin context)
- rug / honeypot / scam check (new listing context)
- first buy / small chase / limit first order (with confirmation)

## Support

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills) (when published from upstream)
- **Issues**: use your package publisher's issue tracker or Gate skills hub support channel.
