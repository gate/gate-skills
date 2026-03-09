# Gate DEX Auth Skill

Authentication Skill that manages Google OAuth login, Token refresh, and logout.

## Overview

`gate-dex-mcpauth` is the authentication domain Skill in the Gate DEX MCP Skill set. Based on 5 auth tools from the Gate DEX MCP Server, it provides AI Agents with user identity authentication and session management.

**Key features:**

- Supports Google OAuth Device Flow login and Authorization Code login
- Token auto-refresh, transparent to the user
- After successful login, passes `mcp_token` and `account_id` to other Skills that require authentication
- Other Skills automatically route here when they detect unauthenticated state or expired Token

## Tool List

| # | Tool name | Function | Key parameters |
|---|-----------|----------|----------------|
| 1 | `auth.google_login_start` | Initiate Google Device Flow login | None |
| 2 | `auth.google_login_poll` | Poll login result | `flow_id` |
| 3 | `auth.login_google_wallet` | Authorization Code login | `code`, `redirect_url` |
| 4 | `auth.refresh_token` | Refresh Token | `refresh_token` |
| 5 | `auth.logout` | Logout | `mcp_token` |

## Operation Flows

| Flow | Scenario | Tools involved |
|------|----------|----------------|
| A | Google Device Flow login (primary) | `auth.google_login_start` → `auth.google_login_poll` |
| B | Token auto-refresh | `auth.refresh_token` |
| C | Logout | `auth.logout` |
| D | Authorization Code login (alternative) | `auth.login_google_wallet` |

MCP Server connection check runs before first session operation; runtime errors are handled as fallback.

## Skill Routing

Post-authentication operation routing:

| User intent | Target Skill |
|-------------|--------------|
| Check balance, assets, address | `gate-dex-mcpwallet` |
| Transfer, send tokens | `gate-dex-mcptransfer` |
| Swap, exchange tokens | `gate-dex-mcpswap` |
| DApp interaction, sign messages | `gate-dex-mcpdapp` |
| Check market, token info | `gate-dex-mcpmarket` |

## Cross-Skill Collaboration

This Skill serves as the **auth entry point** and is depended on by all Skills that require `mcp_token`:

| Caller | Scenario |
|--------|----------|
| `gate-dex-mcpwallet` | Route to login when unauthenticated or Token expired |
| `gate-dex-mcptransfer` | Route to login when unauthenticated or Token expired |
| `gate-dex-mcpswap` | Route to login when unauthenticated or Token expired |
| `gate-dex-mcpdapp` | Route to login when unauthenticated or Token expired |

## Prerequisites

Ensure the Gate DEX MCP Server is configured in your AI coding tool before use:

```
Name: gate-wallet
Type: HTTP
URL: https://your-mcp-server-domain/mcp
```

For detailed configuration, see [README.md](../../README.md).

## File Structure

```
gate-dex-mcpauth/
├── README.md          # This file — Skill overview
├── SKILL.md           # Agent instruction file (tool spec, flows, security rules)
└── CHANGELOG.md       # Change log
```

## Related Skills

- [gate-dex-mcpwallet](../gate-dex-mcpwallet/) — Wallet / assets / transaction history
- [gate-dex-mcptransfer](../gate-dex-mcptransfer/) — Transfer
- [gate-dex-mcpswap](../gate-dex-mcpswap/) — Swap / DEX
- [gate-dex-mcpdapp](../gate-dex-mcpdapp/) — DApp interaction
- [gate-dex-mcpmarket](../gate-dex-mcpmarket/) — Market / tokens
