# Gate Exchange Coupon

## Overview

An AI skill for querying and inspecting coupon/voucher accounts on Gate Exchange. Users can list all available coupons, search by type, view full details, check usage rules, and trace the acquisition source of any coupon — all through natural language.

### Core Capabilities

| Module | Description | Example Prompt |
|--------|-------------|----------------|
| **List Coupons** | Retrieve all available (or expired) coupons with summary info | "What coupons do I have?" |
| **Search by Type** | Filter coupons by specific type | "Do I have a futures bonus?" |
| **Coupon Details** | View full details of a specific coupon including all attributes | "Show me the details of my commission rebate voucher" |
| **Usage Rules** | Read the usage rules and terms for a coupon | "What are the rules for my VIP trial card?" |
| **Coupon Source** | Find out how a coupon was acquired | "How did I get this coupon?" |

## Architecture

Routing architecture: `SKILL.md` handles intent classification and routing; sub-module documents handle detailed workflows.

```
gate-exchange-coupon/
├── SKILL.md                        # Routing rules + domain knowledge
├── README.md                       # This file
├── CHANGELOG.md                    # Version history
└── references/
    ├── list-coupons.md             # Case 1 & 2: list + type-filter workflows
    └── coupon-detail.md            # Case 3, 4 & 5: details + rules + source workflows
```

## Prerequisites

- Gate MCP installed and configured with valid API Key
- User must be logged in (API Key with read permissions)

## Example Prompts

```
# List coupons
"What coupons do I have right now?"
"Show all my available vouchers"
"Do I have any usable coupons in my account?"

# Search by type
"Do I have a commission rebate voucher?"
"Check if I have any futures bonuses"
"Show my VIP trial cards"

# Coupon details
"Show the full details of my 100 USDT commission rebate coupon"
"How much is left on my rebate voucher?"
"When does my futures bonus expire?"

# Usage rules
"What are the usage rules for my futures bonus?"
"How do I use this commission rebate voucher?"

# Coupon source
"How did I get this coupon?"
"What activity gave me this voucher?"
```

## Security

- Read-only skill: no funds movement or order placement
- Uses Gate MCP tools only
- No credential handling or storage in this skill

## License

MIT

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
