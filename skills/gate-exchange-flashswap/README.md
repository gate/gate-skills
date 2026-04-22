# Gate Flash Swap Skill

## Overview

Gate Flash Swap Skill provides comprehensive flash swap capabilities for the Gate Exchange. It supports three swap modes — one-to-one, one-to-many, and many-to-one — covering the full lifecycle of previewing quotes, executing swaps, querying supported pairs, and tracking order history.

### Core Capabilities

| Capability | Description | `gate-cli` commands |
|------------|-------------|-----------|
| One-to-One Swap | Preview and execute a single currency swap (e.g. BTC → USDT) | `gate-cli cex flash-swap preview-v1`, `gate-cli cex flash-swap create-v1` |
| One-to-Many Swap | Swap one currency into multiple targets (e.g. USDT → BTC + ETH + SOL) | `gate-cli cex flash-swap preview-one-to-many`, `gate-cli cex flash-swap create-one-to-many` |
| Many-to-One Swap | Swap multiple currencies into one target (e.g. BTC + ETH + SOL → USDT) | `gate-cli cex flash-swap preview-many-to-one`, `gate-cli cex flash-swap create-many-to-one` |
| Pair Query | Query supported flash swap currency pairs and limits | `gate-cli cex flash-swap pairs` |
| Order History | Query flash swap order list with filters | `gate-cli cex flash-swap orders` |
| Order Detail | Query a single flash swap order by ID | `gate-cli cex flash-swap order` |

## Architecture

This Skill uses **Standard Architecture**, with all logic centralized in `SKILL.md`.

```
skills/gate-exchange-flashswap/
├── SKILL.md                    # AI Agent runtime instructions
├── README.md                   # Human-readable documentation
├── CHANGELOG.md                # Version change log
└── references/
    └── scenarios.md            # Scenario examples and prompt samples
```

**Workflow**:

1. Identify user intent (swap mode or query type)
2. For swaps: Pre-validate amount → Preview quote → Show to user → Confirm → Create order
3. For queries: Call the corresponding query tool and format results

## Usage

Trigger phrase examples:
- "Sell 1 BTC for USDT"
- "Buy 1u BTC, 2u ETH, 3u SOL"
- "Sell 1 BTC, 2 ETH, 3 SOL for USDT"
- "Show me flash swap supported pairs"
- "Query my flash swap orders"
- "Check flash swap order 122136 details"

## gate-cli command index

| Tool | Type | Auth Required | Description |
|------|------|---------------|-------------|
| `gate-cli cex flash-swap preview-v1` | Preview | Yes | One-to-one swap quote preview |
| `gate-cli cex flash-swap create-v1` | Create | Yes | One-to-one swap order creation (requires `quote_id`) |
| `gate-cli cex flash-swap preview-one-to-many` | Preview | Yes | One-to-many swap quote preview |
| `gate-cli cex flash-swap create-one-to-many` | Create | Yes | One-to-many swap order creation |
| `gate-cli cex flash-swap preview-many-to-one` | Preview | Yes | Many-to-one swap quote preview |
| `gate-cli cex flash-swap create-many-to-one` | Create | Yes | Many-to-one swap order creation |
| `gate-cli cex flash-swap pairs` | Query | No | List supported flash swap pairs and limits |
| `gate-cli cex flash-swap orders` | Query | Yes | Query flash swap order history |
| `gate-cli cex flash-swap order` | Query | Yes | Query single flash swap order by ID |

## Safety & Compliance

- **Preview before execution**: Every swap goes through a preview step first; the user must confirm the quote before order creation
- **One-click mode**: Users can explicitly request "direct" or "one-click" swap, which counts as pre-authorized confirmation
- **No fabricated results**: If any API call returns an error, the skill reports the actual error and never fabricates success responses, order IDs, or quote IDs
- **Amount validation**: Swap amounts are validated against pair min/max limits before previewing
- **Sensitive data**: API keys and authentication tokens are never exposed in responses
- **Amounts displayed as-is**: No rounding or modification of amounts from API responses

## Authentication

This skill does **not** read secrets from chat. Configure **`gate-cli`** on the agent host with **`gate-cli config init`** or **`GATE_API_KEY`** / **`GATE_API_SECRET`**, with Flash Swap permissions. See [gate-cli](https://github.com/gate/gate-cli) and run `sh ./setup.sh` from this skill directory for installation.

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
