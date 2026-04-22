# Gate VIP & Fee Query Skill

## Overview

`gate-exchange-vipfee` is a read-only query Skill that helps users quickly check their Gate VIP tier and trading fee rates (spot and futures). It leverages gate-cli tools to retrieve account profile and fee rate data, presenting results in a clean, structured format.

### Core Capabilities

| Capability | Description | `gate-cli` command |
|------------|-------------|----------|
| VIP Tier Query | Query the user's current VIP level | `gate-cli cex account detail` |
| Trading Fee Query | Query spot and futures maker/taker fee rates | `gate-cli cex wallet market trade-fee` |
| Combined Query | Return both VIP tier and fee rates in one response | Both tools |

## Architecture

This Skill uses the **Standard Architecture** (single-function, all logic in one SKILL.md).

```
gate-exchange-vipfee/
├── SKILL.md                    # AI Agent runtime instructions
├── README.md                   # Human-readable documentation
├── CHANGELOG.md                # Version changelog
└── references/
    └── scenarios.md            # Usage scenarios and prompt examples
```

### Workflow Summary

```
User Request
    ↓
Step 1: Identify query type (VIP / Fee / Combined)
    ↓
Step 2: Query VIP tier via `gate-cli cex account detail`
    ↓
Step 3: Query fee rates via `gate-cli cex wallet market trade-fee`
    ↓
Step 4: Format and return result
```

## Usage

Trigger this Skill with prompts such as:

- "What is my VIP level?"
- "Check my trading fees"
- "Show me the spot and futures fees"
- "What is my VIP level and fee rate?"

## gate-cli command index

| Tool | Purpose | Auth Required |
|------|---------|---------------|
| `gate-cli cex account detail` | Get account profile including VIP tier | Yes |
| `gate-cli cex wallet market trade-fee` | Get spot and futures trading fee rates | Yes |

## Authentication

This skill does **not** read secrets from chat. Configure **`gate-cli`** on the agent host with **`gate-cli config init`** or **`GATE_API_KEY`** / **`GATE_API_SECRET`**, with account/fee read permissions. See [gate-cli](https://github.com/gate/gate-cli) and run `sh ./setup.sh` from this skill directory for installation.

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
