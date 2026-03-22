---
name: gate-dex-wallet
version: "2026.3.19-2"
updated: "2026-03-19"
description: "Gate DEX wallet ACCOUNT MANAGEMENT skill. For personal wallet operations: login/logout authentication, check token balances, view wallet addresses, transfer/send tokens to addresses, x402 payment (402: EVM exact/upto, Solana exact/upto via dex_tx_x402_fetch), transaction history, swap history, DApp wallet-connect and contract interactions, CLI tool. This skill manages wallet state and identity — it does not provide market data lookups or execute token swaps."
---

# Gate DEX Wallet

> **Pure Routing Layer** — Wallet ACCOUNT MANAGEMENT only. Handles identity, balances, transfers, DApp, CLI. All sub-modules in `references/`.

**Trigger Scenarios**: Use when the user wants to **manage their wallet account or identity**:
- Auth: "login", "logout", "authenticate", "token expired", "OAuth"
- Balance: "check balance", "my assets", "total portfolio", "wallet address"
- History: "transaction history", "swap history", "past transactions"
- Transfer: "transfer ETH to 0xABC", "send tokens", "batch transfer"
- x402: "pay for 402 API", "x402 payment", "payment required", "pay and fetch URL"
- DApp: "connect wallet to DApp", "sign message", "contract call", "approve spending"
- CLI: "gate-wallet command", "CLI tool", "openapi-swap", "hybrid swap"

**NOT this skill** (common misroutes):
- "what is ETH price" → `gate-dex-market` (market data lookup)
- "swap ETH for USDT" → `gate-dex-trade` (swap execution)
- "is this token safe" → `gate-dex-market` (security audit)

---

## Auto-Update (Session Start Only)

On session start (not during interactions), check for updates once:

1. Read this file's frontmatter `version` and `updated` fields.
2. Fetch remote SKILL.md from `https://raw.githubusercontent.com/gateio/web3_wallet_skill/master/skills/gate-dex-wallet/SKILL.md`.
3. Compare: update if remote version > local version, or same version but remote `updated` date is newer.
4. On update: fetch and overwrite all skill files (`SKILL.md`, `README.md`, `CHANGELOG.md`, `install.sh`, `install_cli.sh`, `references/auth.md`, `references/transfer.md`, `references/dapp.md`, `references/cli.md`, `references/x402.md`).
5. On failure: silently continue — never block user interactions.
6. Skip if: already checked this session, or skill was installed < 24h ago.

---

## Module Routing

Route to corresponding sub-module based on user intent:

| User Intent | Keywords | Target |
|-------------|----------|--------|
| **Authentication** | "login", "logout", "token expired", "OAuth" | `references/auth.md` |
| **Asset Queries** | "check balance", "total assets", "wallet address", "transaction history", "swap history" | This file (see below) |
| **Transfer** | "transfer", "send", "batch transfer", "gas fee" | `references/transfer.md` |
| **x402 Payment** | "402 payment", "x402 pay", "payment required", "pay for API/URL" | `references/x402.md` |
| **DApp Interactions** | "DApp", "sign message", "approve", "connect wallet", "contract call" | `references/dapp.md` |
| **CLI Tool** | "gate-wallet command", "CLI", "command line", "openapi-swap", "hybrid swap" | `references/cli.md` |

---

## MCP Server Connection Detection

Before the first MCP tool call in a session, perform one connection probe:

1. **Server Discovery**: Scan configured MCP servers for tools `dex_wallet_get_token_list`, `dex_tx_quote`, `dex_tx_swap`
2. **Record Identifier**: Supports flexible naming (gate-wallet, gate-dex, dex, wallet, custom names)
3. **Verify Connection**: `CallMcpTool(server="<identifier>", toolName="dex_chain_config", arguments={chain: "eth"})`

| Result | Action | Next |
|--------|--------|------|
| Success | Record server identifier | Use for all subsequent calls this session |
| Failure | Display setup guide below | Re-detect next session |

**Setup guide** (show at most once per session when detection fails):

```
Gate Wallet MCP Server:
  - URL: https://api.gatemcp.ai/mcp/dex
  - Type: HTTP

  Cursor: Settings -> MCP -> Add server, or edit ~/.cursor/mcp.json
  Claude Code: claude mcp add --transport http gate-dex --scope project https://api.gatemcp.ai/mcp/dex
```

---

## Authentication State

All operations requiring auth need valid `mcp_token`:

- No `mcp_token` -> Route to `references/auth.md` for login
- Token expired -> Try `dex_auth_refresh_token` silent refresh; if failed, guide to re-login

---

## Asset Query Module (MCP Tools)

### Tools

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `dex_wallet_get_token_list` | Token balances | `chain?`, `mcp_token` |
| `dex_wallet_get_total_asset` | Total asset value | `account_id`, `mcp_token` |
| `dex_wallet_get_addresses` | Wallet addresses | `account_id`, `mcp_token` |
| `dex_chain_config` | Chain configuration | `chain`, `mcp_token` |
| `dex_tx_list` | Transaction history | `account_id`, `chain?`, `page?`, `limit?`, `mcp_token` |
| `dex_tx_detail` | Transaction details | `hash_id`, `chain`, `mcp_token` |
| `dex_tx_history_list` | Swap history | `account_id`, `chain?`, `page?`, `limit?`, `mcp_token` |

### Token list: use `orignCoinNumber` for balance (not `coinNumber`)

Wallet / token-list APIs may return both a display-oriented `coinNumber` and a raw amount `orignCoinNumber`. **Do not rely on `coinNumber` for balances** — it can be formatted for UI and cause rounding or parsing errors. **For any balance display, comparison, or downstream math, use `orignCoinNumber`** (raw numeric string/amount as returned by the API), then apply decimals/`symbol` for human-readable formatting. See internal spec: [Lark wiki](https://gtglobal.jp.larksuite.com/wiki/ObSnwDsMlieSCEk7h2sjGtsCp2e).

### Query Flow

```text
Step 0: MCP Server connection detection (once per session)
  |
Step 1: Authentication check
  |- No mcp_token -> Route to references/auth.md
  +- Valid token -> Continue
  |
Step 2: Execute query
  |- Balance: dex_wallet_get_token_list({ chain?, mcp_token })
  |- Total assets: dex_wallet_get_total_asset({ account_id, mcp_token })
  |- Addresses: dex_wallet_get_addresses({ account_id, mcp_token })
  |- Tx history: dex_tx_list({ account_id, chain?, mcp_token })
  +- Swap history: dex_tx_history_list({ account_id, chain?, mcp_token })
  |
Step 3: Format and display results
```

---

## Follow-up Routing

| User Intent After Query | Target |
|------------------------|--------|
| View token quotes / K-line | `gate-dex-market` |
| Token security audit | `gate-dex-market` |
| Transfer / send tokens | `references/transfer.md` |
| Exchange / Swap tokens | `gate-dex-trade` |
| x402 / pay for 402 API | `references/x402.md` |
| DApp interaction | `references/dapp.md` |
| Login / auth expired | `references/auth.md` |
| CLI / command line | `references/cli.md` |

---

## Cross-Skill Collaboration

This skill serves as the **wallet data center**, called by other skills:

| Caller | Scenario | Tools Used |
|--------|----------|------------|
| `gate-dex-trade` | Balance verification, token address resolution | `dex_wallet_get_token_list` |
| `gate-dex-trade` | Get chain-specific wallet address | `dex_wallet_get_addresses` |
| `gate-dex-market` | Guide to view holdings after market query | `dex_wallet_get_token_list` |

---

## Supported Chains

| Chain ID | Network | Type |
|----------|---------|------|
| `eth` | Ethereum | EVM |
| `bsc` | BNB Smart Chain | EVM |
| `polygon` | Polygon | EVM |
| `arbitrum` | Arbitrum One | EVM |
| `optimism` | Optimism | EVM |
| `avax` | Avalanche C-Chain | EVM |
| `base` | Base | EVM |
| `sol` | Solana | Non-EVM |

---

## Security Rules

1. **Authentication check**: Verify `mcp_token` validity before all operations
2. **Sensitive info**: `mcp_token` must not be displayed in plain text
3. **Auto refresh**: Prioritize silent refresh when token expires
4. **Auth guidance**: Route to `references/auth.md` when authentication fails
5. **Cross-skill security**: Provide secure balance verification and address retrieval for other skills
