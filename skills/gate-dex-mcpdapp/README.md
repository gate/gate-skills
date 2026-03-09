# Gate DEX DApp Skill

DApp interaction Skill providing wallet connection, message signing, DApp transaction execution, and ERC20 Approve authorization capabilities.

## Overview

`gate-dex-mcpdapp` is the DApp interaction domain Skill in the Gate DEX MCP Skill collection. Based on 4 tools from the Gate DEX MCP Server (+ cross-Skill invocation), it provides AI Agent with the ability to interact with external DApps (DeFi, NFT, governance, etc.).

**Key features:**

- All operations **require authentication** (need `mcp_token`)
- Supports personal_sign and EIP-712 typed data signing
- DApp transactions and Approve include **mandatory confirmation gating** and **contract security review**
- Supports multiple EVM chains (ETH, BSC, Polygon, Arbitrum, Optimism, Avalanche, Base) + Solana
- Default exact authorization; unlimited authorization requires secondary confirmation

## Tool List

| # | Tool name | Function | Key parameters |
|---|-----------|----------|----------------|
| 1 | `wallet.get_addresses` | Get wallet addresses (cross-Skill) | `account_id`, `mcp_token` |
| 2 | `wallet.sign_message` | Sign message | `message`, `chain`, `account_id`, `mcp_token` |
| 3 | `wallet.sign_transaction` | Sign DApp transaction | `raw_tx`, `chain`, `account_id`, `mcp_token` |
| 4 | `tx.send_raw_transaction` | Broadcast transaction | `signed_tx`, `chain`, `mcp_token` |

## DApp Interaction Scenarios

| Scenario | Description | Core tools |
|----------|-------------|------------|
| Wallet connection | DApp requests wallet address | `wallet.get_addresses` |
| Message signing | DApp login verification / EIP-712 signing | `wallet.sign_message` |
| DApp transaction execution | mint, stake, claim, add liquidity, etc. | `wallet.sign_transaction` → `tx.send_raw_transaction` |
| ERC20 Approve | Authorize DApp contract to use specified token | `wallet.sign_transaction` → `tx.send_raw_transaction` |

## Operation Flows

| Flow | Scenario | Tools involved |
|------|----------|----------------|
| A | DApp wallet connection | `wallet.get_addresses` |
| B | Message signing | Confirm → `wallet.sign_message` |
| C | DApp transaction execution (main flow) | Security review → Balance validation → Confirm → `wallet.sign_transaction` → `tx.send_raw_transaction` |
| D | ERC20 Approve authorization | Confirm authorization amount → `wallet.sign_transaction` → `tx.send_raw_transaction` |
| E | Arbitrary contract call (user provides ABI) | Agent encodes calldata → Same as Flow C |

MCP Server connection check before first operation in session; runtime error fallback for subsequent operations.

## Skill Routing

Post-DApp operation follow-up guidance:

| User intent | Target Skill |
|-------------|--------------|
| View updated balance | `gate-dex-mcpwallet` |
| View transaction details / history | `gate-dex-mcpwallet` |
| View contract security info | `gate-dex-mcpmarket` |
| Transfer tokens | `gate-dex-mcptransfer` |
| Swap tokens | `gate-dex-mcpswap` |
| Login / authentication expired | `gate-dex-mcpauth` |

## Cross-Skill Collaboration

| Direction | Skill | Scenario | Tools used |
|-----------|-------|----------|------------|
| Invoke | `gate-dex-mcpwallet` | Get wallet address for DApp connection | `wallet.get_addresses` |
| Invoke | `gate-dex-mcpwallet` | Validate balance before DApp transaction | `wallet.get_token_list` |
| Invoke | `gate-dex-mcpmarket` | Contract security review | `token_get_risk_info` |
| Invoke | `gate-dex-mcpauth` | Not logged in or Token expired | `auth.refresh_token` |
| Invoked by | `gate-dex-mcpwallet` | User wants to connect DApp after viewing address | — |
| Invoked by | `gate-dex-mcpmarket` | User wants to participate in DeFi after viewing token | — |
| Invoked by | `gate-dex-mcpswap` | User wants to participate in DeFi after Swap | — |

## Supported Chains

| Chain ID | Network name | Type | Native Gas token |
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

Before use, ensure Gate DEX MCP Server is configured in your AI coding tool:

```
Name: gate-wallet
Type: HTTP
URL: https://your-mcp-server-domain/mcp
```

For detailed configuration, see [README.md](../../README.md).

## File Structure

```
gate-dex-mcpdapp/
├── README.md          # This file — Skill overview
├── SKILL.md           # Agent instruction file (tool spec, flows, security rules)
└── CHANGELOG.md       # Change log
```

## Related Skills

- [gate-dex-mcpauth](../gate-dex-mcpauth/) — Authentication (Google OAuth)
- [gate-dex-mcpwallet](../gate-dex-mcpwallet/) — Wallet/Assets/Transaction history
- [gate-dex-mcptransfer](../gate-dex-mcptransfer/) — Transfer
- [gate-dex-mcpswap](../gate-dex-mcpswap/) — Swap/DEX
- [gate-dex-mcpmarket](../gate-dex-mcpmarket/) — Market/Tokens
