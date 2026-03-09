# Gate DEX Wallet Skill

Wallet assets and transaction history query Skill, providing read-only query capabilities for balance, address, transaction records, etc.

## Overview

`gate-dex-mcpwallet` is the wallet/assets/history domain Skill in the Gate DEX MCP Skill collection. Based on 7 query tools from the Gate DEX MCP Server, it provides AI Agent with token balance, total assets, wallet address, chain config, transfer history, and Swap history query capabilities.

**Key features:**

- All operations **require authentication** (need `mcp_token`)
- Read-only operations, no on-chain writes
- Supports EVM multi-chain (ETH, BSC, Polygon, Arbitrum, Optimism, Avalanche, Base) + Solana
- Often called by other Skills (transfer, swap, dapp) for cross-Skill balance verification and address retrieval

## Tool List

| # | Tool Name | Function | Key Parameters |
|---|-----------|----------|----------------|
| 1 | `wallet.get_token_list` | Token list (with balance) | `account_id`, `chain?`, `mcp_token` |
| 2 | `wallet.get_total_asset` | Total asset value | `account_id`, `mcp_token` |
| 3 | `wallet.get_addresses` | Wallet addresses | `account_id`, `mcp_token` |
| 4 | `chain.config` | Chain config info | `chain`, `mcp_token` |
| 5 | `tx.list` | Transfer transaction list | `account_id`, `chain?`, `mcp_token` |
| 6 | `tx.detail` | Transaction details | `hash_id`, `chain`, `mcp_token` |
| 7 | `tx.history_list` | Swap history records | `account_id`, `chain?`, `mcp_token` |

## Operation Flows

| Flow | Scenario | Tools Used |
|------|----------|------------|
| A | Query token balance | `wallet.get_token_list` |
| B | Query total asset value | `wallet.get_total_asset` |
| C | Get wallet addresses | `wallet.get_addresses` |
| D | Query chain config (auxiliary) | `chain.config` |
| E | View transfer history | `tx.list` |
| F | View transaction details | `tx.detail` |
| G | View Swap history | `tx.history_list` |

MCP Server connection check before first operation in session; runtime error fallback for subsequent operations.

## Skill Routing

Post-asset-view action guidance:

| User Intent | Target Skill |
|-------------|--------------|
| View token market data, K-line | `gate-dex-mcpmarket` |
| View token security audit | `gate-dex-mcpmarket` |
| Transfer, send tokens | `gate-dex-mcptransfer` |
| Swap tokens | `gate-dex-mcpswap` |
| Interact with DApp | `gate-dex-mcpdapp` |
| Login / auth expired | `gate-dex-mcpauth` |

## Cross-Skill Collaboration

This Skill often acts as an **asset data provider** for other Skills:

| Caller | Scenario | Tools Used |
|--------|----------|------------|
| `gate-dex-mcptransfer` | Verify balance before transfer | `wallet.get_token_list` |
| `gate-dex-mcpswap` | Verify balance before Swap, resolve token address | `wallet.get_token_list` |
| `gate-dex-mcpswap` | Get chain-specific wallet address | `wallet.get_addresses` |
| `gate-dex-mcpdapp` | Get wallet address for DApp connection | `wallet.get_addresses` |
| `gate-dex-mcpdapp` | Verify balance before DApp transaction | `wallet.get_token_list` |
| `gate-dex-mcptransfer` / `gate-dex-mcpswap` / `gate-dex-mcpdapp` | View updated balance after operation | `wallet.get_token_list` |

## Supported Chains

| Chain ID | Network Name | Type |
|----------|--------------|------|
| `eth` | Ethereum | EVM |
| `bsc` | BNB Smart Chain | EVM |
| `polygon` | Polygon | EVM |
| `arbitrum` | Arbitrum One | EVM |
| `optimism` | Optimism | EVM |
| `avax` | Avalanche C-Chain | EVM |
| `base` | Base | EVM |
| `sol` | Solana | Non-EVM |

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
gate-dex-mcpwallet/
├── README.md          # This file — Skill description
├── SKILL.md           # Agent instruction file (tool spec, flows, security rules)
└── CHANGELOG.md       # Change log
```

## Related Skills

- [gate-dex-mcpauth](../gate-dex-mcpauth/) — Authentication (Google OAuth)
- [gate-dex-mcptransfer](../gate-dex-mcptransfer/) — Transfer
- [gate-dex-mcpswap](../gate-dex-mcpswap/) — Swap/DEX
- [gate-dex-mcpdapp](../gate-dex-mcpdapp/) — DApp interaction
- [gate-dex-mcpmarket](../gate-dex-mcpmarket/) — Market/tokens
