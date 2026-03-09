# Gate DEX Swap Skill

Swap/DEX trading Skill, providing quote fetching, slippage control, route display, and Swap execution capabilities.

## Overview

`gate-dex-mcpswap` is the Swap/DEX domain Skill in the Gate DEX MCP Skill collection, based on 3 tools from Gate DEX MCP Server (+ 2 cross-Skill calls + 1 MCP Resource), providing complete token exchange capabilities for AI Agent.

**Key features:**

- All operations **require authentication** (need `mcp_token`)
- One-shot Swap: Quote→Build→Sign→Submit completed in single call
- Includes **mandatory three-step confirmation SOP** (trade pair confirmation → quote display → sign approval confirmation)
- Supports EVM multi-chain + Solana, supports cross-chain Swap
- Mandatory warning when exchange value diff > 5%, high slippage MEV risk prompt

## Tool list

| # | Tool name | Function | Key parameters |
|---|-----------|----------|-----------------|
| 1 | `wallet.get_token_list` | Query balance (cross-Skill) | `chain`, `mcp_token` |
| 2 | `wallet.get_addresses` | Get wallet address (cross-Skill) | `account_id`, `mcp_token` |
| 3 | `tx.quote` | Get Swap quote | `chain_id_in`, `chain_id_out`, `token_in`, `token_out`, `amount`, `slippage`, `user_wallet`, `native_in`, `native_out`, `mcp_token` |
| 4 | `tx.swap` | Execute Swap (One-shot) | Same as `tx.quote` + `account_id` |
| 5 | `tx.swap_detail` | Query Swap status | `tx_order_id`, `mcp_token` |

**MCP Resource:**

| Resource URI | Function |
|--------------|----------|
| `swap://supported_chains` | Get list of chains supported for Swap and address grouping |

## Operation flow

| Flow | Scenario | Tools involved |
|------|----------|----------------|
| A | Standard Swap (main flow) | Balance validation → trade pair confirmation → `tx.quote` → quote display → sign confirmation → `tx.swap` → `tx.swap_detail` |
| B | Re-quote after modifying slippage | Update slippage → re-call `tx.quote` → quote display |
| C | Query Swap transaction status | `tx.swap_detail` |
| D | Cross-chain Swap | Verify cross-chain support → get `to_wallet` → same as flow A |

MCP Server connection check before first session operation, runtime error fallback for subsequent operations.

## Skill routing

Post-Swap operation guidance:

| User intent | Target Skill |
|-------------|--------------|
| View updated balance | `gate-dex-mcpwallet` |
| View Swap transaction history | `gate-dex-mcpwallet` |
| Continue Swap other tokens | Stay in this Skill |
| Transfer just-swapped tokens | `gate-dex-mcptransfer` |
| View token market / K-line | `gate-dex-mcpmarket` |
| Login / auth expired | `gate-dex-mcpauth` |

## Cross-Skill collaboration

| Direction | Skill | Scenario | Tools used |
|-----------|-------|----------|------------|
| Call | `gate-dex-mcpwallet` | Query balance, resolve token address before Swap | `wallet.get_token_list` |
| Call | `gate-dex-mcpwallet` | Get chain-specific wallet address | `wallet.get_addresses` |
| Call | `gate-dex-mcpmarket` | Security review target token before Swap | `token_get_risk_info` |
| Call | `gate-dex-mcpmarket` | Query token info to help resolve address | `token_get_coin_info` |
| Call | `gate-dex-mcpauth` | Not logged in or Token expired | `auth.refresh_token` |
| Called by | `gate-dex-mcpwallet` | User wants to exchange after viewing balance | — |
| Called by | `gate-dex-mcpmarket` | User wants to buy token after viewing market | — |

## Supported chains

| chain_id | Network name | Type | Native Gas token |
|----------|--------------|------|------------------|
| `1` | Ethereum | EVM | ETH |
| `56` | BNB Smart Chain | EVM | BNB |
| `137` | Polygon | EVM | MATIC |
| `42161` | Arbitrum One | EVM | ETH |
| `10` | Optimism | EVM | ETH |
| `43114` | Avalanche C-Chain | EVM | AVAX |
| `8453` | Base | EVM | ETH |
| `501` | Solana | Non-EVM | SOL |

## Prerequisites

Ensure Gate DEX MCP Server is configured in your AI coding tool before use:

```
Name: gate-wallet
Type: HTTP
URL: https://your-mcp-server-domain/mcp
```

See [README.md](../../README.md) for detailed configuration.

## File structure

```
gate-dex-mcpswap/
├── README.md          # This file — Skill description
├── SKILL.md           # Agent instruction file (tool spec, flow, security rules)
└── CHANGELOG.md       # Change log
```

## Related Skills

- [gate-dex-mcpauth](../gate-dex-mcpauth/) — Authentication (Google OAuth)
- [gate-dex-mcpwallet](../gate-dex-mcpwallet/) — Wallet/assets/transaction history
- [gate-dex-mcptransfer](../gate-dex-mcptransfer/) — Transfer
- [gate-dex-mcpdapp](../gate-dex-mcpdapp/) — DApp interaction
- [gate-dex-mcpmarket](../gate-dex-mcpmarket/) — Market/tokens
