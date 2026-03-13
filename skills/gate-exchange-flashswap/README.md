# Gate Flash Swap Query Skill

## Overview

Gate Flash Swap Query Skill provides comprehensive query capabilities for the Gate Flash Swap service. It supports querying supported currency pair lists, validating currency support with min/max swap limits, reviewing historical order records, and tracking specific order details.

### Core Capabilities

| Capability | Description | MCP Tool |
|------------|-------------|----------|
| Currency Pair List Query | Query all supported flash swap currency pairs | `cex_fc_list_fc_currency_pairs` |
| Currency Limit Validation | Check if a specific currency supports flash swap and its min/max swap amounts | `cex_fc_list_fc_currency_pairs` |
| Order History Query | Query flash swap order history with status, currency, and pagination filters | `cex_fc_list_fc_orders` |
| Order Detail Tracking | Query complete details of a single flash swap order by order ID | `cex_fc_get_fc_order` |

## Architecture

This Skill uses **Standard Architecture**, with all query logic centralized in `SKILL.md`.

```
skills/gate-exchange-flashswap/
├── SKILL.md                    # AI Agent runtime instructions
├── README.md                   # Human-readable documentation
├── CHANGELOG.md                # Version change log
└── references/
    └── scenarios.md            # Scenario examples and prompt samples
```

**Workflow**:

1. Identify user intent (pair listing / limit check / order history / order tracking)
2. Call the corresponding MCP tool to fetch data
3. Format and present the query results

## Usage

Trigger phrase examples:
- "Show me flash swap supported pairs"
- "Can I swap BTC for USDT? What are the limits?"
- "Query my flash swap orders"
- "Check flash swap order 120841 details"
- "What is the minimum amount to flash swap ETH?"

## Dependencies

- MCP Service: `user-gate`
- Authentication: Order queries require user to have Gate API authentication configured
