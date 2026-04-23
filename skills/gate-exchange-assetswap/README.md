# Gate Exchange Asset Allocation Optimization Skill

## Overview

This skill covers **Asset Allocation Optimization** on Gate Exchange (internal product identifier may appear in APIs as `asset-swap` or similar): restructuring multiple **spot** holdings into a strategy-driven target using the published **allocation optimization** `gate-cli` commands under `gate-cli cex assetswap` (see the table below). It is **not** the same as **spot grid trading** (bots), **manual single spot orders** (use the spot trading skill), or **instant pair conversion** products outside this allocation flow (route to the flash-swap or spot skill when appropriate).

### Core Capabilities

| Capability | Description | `gate-cli` commands |
|------------|-------------|-----------|
| Eligible assets | List spot balances and data available for portfolio optimization | `gate-cli cex assetswap assets` |
| Configuration | Strategy enums, targets, limits, precision | `gate-cli cex assetswap config` |
| Evaluation | Optional pre-preview estimate for a candidate set and strategy | `gate-cli cex assetswap evaluate` |
| Preview | Trade-scoped preview of an optimization (slippage, risk hints) | `gate-cli cex assetswap order preview` |
| Place order | Create optimization order after confirmed preview | `gate-cli cex assetswap order create` |
| Order list | Paginated history of allocation optimization orders | `gate-cli cex assetswap order list` |
| Order detail | Single order with child order states | `gate-cli cex assetswap order get` |

## Architecture

Standard layout: runtime instructions in `SKILL.md`, human-oriented summary here, scenarios in `references/scenarios.md`.

```
skills/gate-exchange-assetswap/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── scenarios.md
```

**Workflow (order placement)**:

1. List eligible assets (Case 1)
2. Load config (Case 2)
3. Optionally evaluate (Case 3a), then preview (Case 3b)
4. Create order only after user confirms preview (Case 4)

**Query-only paths**: Cases 5 and 6 can run without placing an order.

## Usage

Example trigger phrases:

- "List spot assets I can use for asset allocation optimization"
- "Show allocation optimization configuration and supported strategies"
- "Preview rebalancing these alts to USDT using conservative strategy"
- "Place the allocation optimization order after I confirm the preview"
- "Show my allocation optimization orders from last month"
- "Status of allocation optimization order {id}"

## gate-cli command index

| Tool | Type | Auth | Description |
|------|------|------|-------------|
| `gate-cli cex assetswap assets` | Query | Yes | Eligible assets for optimization |
| `gate-cli cex assetswap config` | Query | Yes | Strategy and parameter configuration |
| `gate-cli cex assetswap evaluate` | Query | Yes | Optional valuation / estimate |
| `gate-cli cex assetswap order preview` | Preview | Yes (trade) | Preview optimization before create |
| `gate-cli cex assetswap order create` | Create | Yes (trade) | Submit optimization order |
| `gate-cli cex assetswap order list` | Query | Yes | Order history |
| `gate-cli cex assetswap order get` | Query | Yes | Single order detail |

## Safety and Compliance

- Preview before create is the default safe path; obtain explicit confirmation on preview outputs.
- Trade-scoped tools require API key permissions that allow trading.
- Relay API errors honestly; never invent order or quote identifiers.
- Compliance, KYC, and region rules are enforced by the platform.

## Authentication

Credentials are handled by the Gate MCP / **gate-cli** stack. Configure the Gate main MCP server (or `gate-cli` per your environment) and an API key with **profile** read access for queries and **trade** permission for preview and create. Setup references: Gate MCP and gate-cli repository documentation on GitHub.

## Source

- **Repository**: https://github.com/gate/gate-skills
- **Publisher**: https://www.gate.com
