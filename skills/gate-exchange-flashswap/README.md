# Gate Flash Swap Skill

## Overview

Gate Flash Swap Skill provides comprehensive flash swap capabilities for the Gate Exchange. It supports three swap modes — one-to-one, one-to-many, and many-to-one — covering the full lifecycle of previewing quotes, executing swaps, querying supported pairs, and tracking order history.

### Core Capabilities

| Capability | Description | MCP Tools |
|------------|-------------|-----------|
| One-to-One Swap | Preview and execute a single currency swap (e.g. BTC → USDT) | `cex_fc_preview_fc_order_v1`, `cex_fc_create_fc_order_v1` |
| One-to-Many Swap | Swap one currency into multiple targets (e.g. USDT → BTC + ETH + SOL) | `cex_fc_preview_fc_multi_currency_one_to_many_order`, `cex_fc_create_fc_multi_currency_one_to_many_order` |
| Many-to-One Swap | Swap multiple currencies into one target (e.g. BTC + ETH + SOL → USDT) | `cex_fc_preview_fc_multi_currency_many_to_one_order`, `cex_fc_create_fc_multi_currency_many_to_one_order` |
| Pair Query | Query supported flash swap currency pairs and limits | `cex_fc_list_fc_currency_pairs` |
| Order History | Query flash swap order list with filters | `cex_fc_list_fc_orders` |
| Order Detail | Query a single flash swap order by ID | `cex_fc_get_fc_order` |

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
2. For swaps: Preview → Show quote to user → Confirm → Create order
3. For queries: Call the corresponding query tool and format results

## Usage

Trigger phrase examples:
- "Sell 1 BTC for USDT"
- "Buy 1u BTC, 2u ETH, 3u SOL"
- "Sell 1 BTC, 2 ETH, 3 SOL for USDT"
- "Show me flash swap supported pairs"
- "Query my flash swap orders"
- "Check flash swap order 122136 details"

## Dependencies

- MCP Service: `user-g-dev-ex`
- Authentication: All swap and order operations require Gate API authentication
