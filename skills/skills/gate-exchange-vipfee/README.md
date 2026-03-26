# Gate VIP & Fee Query Skill

## Overview

`gate-exchange-vipfee` is a read-only query Skill that helps users quickly check their Gate VIP tier and trading fee rates (spot and futures). It leverages Gate MCP tools to retrieve account profile and fee rate data, presenting results in a clean, structured format.

### Core Capabilities

| Capability | Description | MCP Tool |
|------------|-------------|----------|
| VIP Tier Query | Query the user's current VIP level | `cex_account_get_account_detail` |
| Trading Fee Query | Query spot and futures maker/taker fee rates | `cex_wallet_get_wallet_fee` |
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
Step 2: Query VIP tier via cex_account_get_account_detail (if needed)
    ↓
Step 3: Query fee rates via cex_wallet_get_wallet_fee (if needed)
    ↓
Step 4: Format and return result
```

## Usage

Trigger this Skill with prompts such as:

- "What is my VIP level?"
- "Check my trading fees"
- "Show me the spot and futures fees"
- "What is my VIP level and fee rate?"

## MCP Tools

| Tool | Purpose | Auth Required |
|------|---------|---------------|
| `cex_account_get_account_detail` | Get account profile including VIP tier | Yes |
| `cex_wallet_get_wallet_fee` | Get spot and futures trading fee rates | Yes |

## Authentication

This skill does **not** handle credentials directly. Authentication is managed by the Gate MCP platform layer — the MCP server holds the user's API key and injects it into API calls automatically. No environment variables or secrets are required by the skill itself. Users should configure their Gate API key in the MCP server settings (see [Gate MCP](https://github.com/gateio/gate-mcp) for setup instructions).

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
