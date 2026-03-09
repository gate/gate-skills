# Gate DEX Transfer Skill

Transfer execution Skill providing Gas estimation, transaction preview, signing, and broadcast capabilities.

## Overview

`gate-dex-mcptransfer` is the transfer-domain Skill in the Gate DEX MCP Skill set. Based on 4 tools from Gate DEX MCP Server (+ 1 cross-Skill call), it provides full on-chain transfer capabilities for AI Agent.

**Key features:**

- All operations **require authentication** (need `mcp_token`)
- Involves on-chain write operations, with **mandatory balance verification** and **user confirmation gate**
- Supports EVM multi-chain (ETH, BSC, Polygon, Arbitrum, Optimism, Avalanche, Base) + Solana
- Supports native token and ERC20/SPL token transfers
- Supports batch transfers with per-transfer confirmation

## Tool List

| # | Tool Name | Function | Key Parameters |
|---|-----------|----------|----------------|
| 1 | `wallet.get_token_list` | Query balance (cross-Skill) | `account_id`, `chain`, `mcp_token` |
| 2 | `tx.gas` | Gas fee estimation | `chain`, `from_address`, `to_address`, `mcp_token` |
| 3 | `tx.transfer_preview` | Build transaction preview | `chain`, `from_address`, `to_address`, `token_address`, `amount`, `mcp_token` |
| 4 | `wallet.sign_transaction` | Server-side signing | `raw_tx`, `chain`, `account_id`, `mcp_token` |
| 5 | `tx.send_raw_transaction` | Broadcast transaction | `signed_tx`, `chain`, `mcp_token` |

## Operation Flow

| Flow | Scenario | Tools Used |
|------|----------|------------|
| A | Standard transfer (main flow) | `wallet.get_token_list` → `tx.gas` → `tx.transfer_preview` → confirm → `wallet.sign_transaction` → `tx.send_raw_transaction` |
| B | Batch transfer | Each transfer runs flow A independently, confirm one by one |

MCP Server connection check before first operation in session; runtime error fallback for subsequent operations.

## Skill Routing

Post-transfer routing based on user intent:

| User Intent | Target Skill |
|-------------|--------------|
| View updated balance | `gate-dex-mcpwallet` |
| View transaction details / history | `gate-dex-mcpwallet` |
| Continue transfer to another address | Stay in this Skill |
| Swap tokens | `gate-dex-mcpswap` |
| Login / auth expired | `gate-dex-mcpauth` |

## Cross-Skill Collaboration

| Direction | Skill | Scenario | Tools Used |
|-----------|-------|----------|------------|
| Call | `gate-dex-mcpwallet` | Query balance before transfer | `wallet.get_token_list` |
| Call | `gate-dex-mcpwallet` | Get sender address before transfer | `wallet.get_addresses` |
| Call | `gate-dex-mcpwallet` | View updated balance / tx details after transfer | `wallet.get_token_list` / `tx.detail` |
| Call | `gate-dex-mcpauth` | Not logged in or Token expired | `auth.refresh_token` |
| Called by | `gate-dex-mcpwallet` | User wants to transfer after viewing balance | — |
| Called by | `gate-dex-mcpswap` | User wants to transfer out tokens after Swap | — |

## Supported Chains

| Chain ID | Network Name | Type | Native Gas Token |
|----------|--------------|------|------------------|
| `eth` | Ethereum | EVM | ETH |
| `bsc` | BNB Smart Chain | EVM | BNB |
| `polygon` | Polygon | EVM | MATIC |
| `arbitrum` | Arbitrum One | EVM | ETH |
| `optimism` | Optimism | EVM | ETH |
| `avax` | Avalanche C-Chain | EVM | AVAX |
| `base` | Base | EVM | ETH |
| `sol` | Solana | Non-EVM | SOL |

## Prerequisites

Ensure Gate DEX MCP Server is configured in your AI coding tool before use:

```
Name: gate-wallet
Type: HTTP
URL: https://your-mcp-server-domain/mcp
```

See [README.md](../../README.md) for detailed configuration.

## File Structure

```
gate-dex-mcptransfer/
├── README.md          # This file — Skill overview
├── SKILL.md           # Agent instruction file (tool specs, flow, security rules)
└── CHANGELOG.md       # Change log
```

## Related Skills

- [gate-dex-mcpauth](../gate-dex-mcpauth/) — Authentication (Google OAuth)
- [gate-dex-mcpwallet](../gate-dex-mcpwallet/) — Wallet / assets / transaction history
- [gate-dex-mcpswap](../gate-dex-mcpswap/) — Swap / DEX
- [gate-dex-mcpdapp](../gate-dex-mcpdapp/) — DApp interaction
- [gate-dex-mcpmarket](../gate-dex-mcpmarket/) — Market / tokens
