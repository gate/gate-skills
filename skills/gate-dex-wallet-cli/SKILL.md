---
name: gate-dex-wallet-cli
version: "2026.4.24-1"
updated: "2026-04-24"
description: "Gate Wallet CLI — pure REST command-line tool. Auth (OAuth), balance, wallet addresses,Account Address, token list, transaction history, token transfers, and signing. GV security checkin is built into signing commands — no separate binary required. For swaps use gate-dex-trade-cli; for market data use gate-dex-market-cli."
homepage: https://github.com/gate/gate-wallet-cli
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "💼",
        "os": ["linux", "darwin"],
        "requires": {
          "bins": ["gate-wallet"]
        },
        "install": [
          {
            "id": "download-linux-x64",
            "kind": "download",
            "os": ["linux"],
            "url": "https://github.com/gate/gate-wallet-cli/releases/download/v2.0.0/gate-wallet-linux-x64",
            "bins": ["gate-wallet"],
            "label": "Download gate-wallet (Linux x64)"
          },
          {
            "id": "download-macos-arm64",
            "kind": "download",
            "os": ["darwin"],
            "url": "https://github.com/gate/gate-wallet-cli/releases/download/v2.0.0/gate-wallet-darwin-arm64",
            "bins": ["gate-wallet"],
            "label": "Download gate-wallet (macOS arm64)"
          }
        ]
      }
  }
---

# Gate Wallet CLI

> **Pure Routing Layer** — This SKILL.md is a lightweight router. Sub-module details live in `references/`.

## Overview

`gate-wallet` is a standalone CLI tool that communicates with Gate DEX services via REST APIs. **No MCP server is required.** All signing operations (transfer, sign-msg, swap) include built-in GV security checkin — the agent does not need to run any external binary.

Auth: login via Gate/Google OAuth, token stored in `~/.gate-wallet/auth.json`.

The CLI also supports an **interactive REPL** — running `gate-wallet` with no arguments opens a prompt.

## Applicable Scenarios

Use this skill when the user wants to:

- Authenticate (login/logout) via Gate OAuth or Google OAuth
- Query token balances, total portfolio value, or wallet addresses
- View transaction history
- Transfer or send tokens to an on-chain address (EVM + Solana)
- Sign raw messages or raw transactions
- Use `gate-wallet` CLI commands directly

---

## Capability Boundaries

| Supported | Route elsewhere |
|-----------|----------------|
| Authentication & session management | Token swap → `gate-dex-trade-cli` skill |
| Balance, address & token list queries | Market data / token info / K-line → `gate-dex-market-cli` skill |
| Transaction history | DApp interactions → `gate-dex-wallet-cli` |
| Token transfers (EVM + Solana) | x402 payments → `gate-dex-wallet-cli` |
| Sign 32-byte hex messages / raw tx | MCP tool calls → `gate-dex-wallet-cli` |

**Prerequisites**: A `gate-wallet` binary on PATH.

- **GateClaw managed scenario** — `skill/setup.sh` runs automatically on install and drops a pre-built Linux binary into `/home/node/.openclaw/skills/bin/gate-wallet`. Environment variables (`RUN_ENV`, `*_URL`) are collected via the GateClaw Web form and injected into `process.env` at runtime.
- **Personal OpenClaw scenario** — the frontmatter `install` spec downloads the binary for the host OS automatically (no Node.js required).
- **Local development** — build from source:
  ```bash
  cd cli && pnpm install
  pnpm build:binary                  # production binary (no baked env)
  pnpm build:binary -- --bake-env    # bake root .env into the binary (test env)
  ```

---

## Installation

The published binary is a single self-contained executable (no Node.js runtime required).

```bash
# GateClaw / OpenClaw: auto-installed via setup.sh or frontmatter.install
# Manual download (example):
curl -fsSL https://github.com/gate/gate-wallet-cli/releases/download/v2.0.0/gate-wallet-linux-x64 \
  -o /usr/local/bin/gate-wallet
chmod +x /usr/local/bin/gate-wallet

# Login
gate-wallet login           # Gate OAuth (default)
gate-wallet login --google  # Google OAuth
```

**Storage**:
- Auth token → `~/.gate-wallet/auth.json`

**Environment variables** (all optional; defaults target production):

| Variable | Purpose |
|----------|---------|
| `RUN_ENV` | `dev` / `pre` / `prod` — selects GV API environment and CDN candidates |
| `WALLET_SERVICE_URL` | `web3-wallet-service` endpoint (used by `balance`) |
| `BW_SERVICE_URL` | `web3-business-wallet` endpoint |
| `MARKET_TOKEN_URL` | `gateio_service_web3_trade_token` endpoint (market/token/swap) |
| `DATA_API_URL` | `web3-data-api` endpoint (token info, security audit, ranking) |
| `BIZ_WALLET_URL` | OAuth session management endpoint |

---

## Global Options

| Option | Description |
|--------|-------------|
| `--auth-dir <path>` | Custom auth storage directory (overrides `~/.gate-wallet`; also via `GATE_WALLET_HOME` env) |
| `--auth-file <path>` | Custom auth.json file path (overrides `--auth-dir`; also via `GATE_WALLET_AUTH_FILE` env) |
| `-v, --version` | Print version |

---

## Module Routing

| User Intent | Target |
|-------------|--------|
| Login, logout, re-login, session expired, OAuth, "not logged in", switch account, web3-domain | [./references/auth.md](./references/auth.md) |
| Check balance, total assets, wallet address, Account Address,token list, tx history, "how much do I have", "show my tokens" | [./references/asset-query.md](./references/asset-query.md) |
| Transfer, send tokens, "send ETH to 0x...", "transfer USDT", "pay someone", "move tokens", sign-msg, sign-tx, sol-tx | [./references/transfer.md](./references/transfer.md) |
| Swap, exchange tokens, "swap ETH for USDT", "buy SOL", quote, "convert tokens" | → `gate-dex-trade-cli` skill |
| K-line, token price, market cap, liquidity, trading stats, token security, token rankings, new tokens | → `gate-dex-market-cli` skill |

---

## Full Command Reference

### Auth & Session
| Command | Description |
|---------|-------------|
| `login` | Gate OAuth Device Flow login |
| `login --google` | Google OAuth Device Flow login |
| `login --no-open` | Print auth URL instead of opening browser |
| `logout` | Logout and clear `~/.gate-wallet/auth.json` |
| `status` | Show current session info |
| `web3-domain` | View / refresh dynamic web3_domain list |
| `web3-domain --refresh` | Force re-fetch domain list |

### Wallet Queries
| Command | Description |
|---------|-------------|
| `balance` | Total portfolio value (USD) across all chains |
| `address` | Show EVM + Solana wallet addresses |
| `tokens` | Token list with balances (gateway) |
| `tokens --chain ETH,SOL` | Filter by chain |
| `tokens --page N --size N` | Pagination |

### Transfer & Signing
| Command | Description |
|---------|-------------|
| `transfer` | Preview-only unsigned tx (no broadcast) |
| `send` | One-shot: preview → GV checkin → sign → broadcast |
| `send-tx` | Build → GV checkin → sign → broadcast (or broadcast pre-signed with `--hex`) |
| `sol-tx` | Build Solana unsigned tx locally (latest blockhash) |
| `gas [chain]` | Query gas price + gas limit |
| `sign-msg <hex>` | Sign 32-byte hex message (GV checkin built-in) |
| `sign-tx <raw_tx>` | Sign raw hex transaction (GV checkin built-in) |

### Swap
| Command | Description |
|---------|-------------|
| `quote` | Get swap quote (no signing) |
| `swap` | One-shot: quote → GV checkin → sign → broadcast |
| `swap-tokens` | List swappable tokens |
| `bridge-tokens` | List cross-chain bridge tokens |
| `swap-history` | Swap/bridge transaction history |
| `swap-detail <order_id>` | Swap order detail |

### Transaction & Market
| Command | Description |
|---------|-------------|
| `tx-history` | Transfer transaction history |
| `tx-detail <hash>` | Transaction detail by hash |
| `tx-stats` | Trading volume stats (5m/1h/4h/24h) |
| `kline` | K-line (OHLCV) data |
| `liquidity` | Liquidity pool events |
| `token-info` | Token detail (price, market cap) |
| `token-risk` | Token security audit |
| `token-rank` | Token price-change leaderboard (24h) |
| `new-tokens` | Tokens filtered by creation time |

### Chain / RPC
| Command | Description |
|---------|-------------|
| `chain-config [chain]` | Chain config (networkKey, endpoint, chainID) |
| `rpc` | Raw JSON-RPC call |

### Maintenance
| Command | Description |
|---------|-------------|
| `cleanup` | Delete `~/.gate-wallet` |

---

## Key Design Differences from MCP-based Skills

| Aspect | This skill (gate-dex-wallet-cli) | MCP-based skill (gate-dex-wallet-cli) |
|--------|------------------------------|-----------------------------------|
| Transport | Pure REST (no MCP) | MCP tool calls |
| GV security checkin | Built into CLI `send`/`swap`/`sign-msg`/`sign-tx` | External `tx-checkin` binary required |
| Auth storage | `~/.gate-wallet/auth.json` | MCP session `mcp_token` |
| Swap method | `gate-wallet swap` one-shot | `dex_tx_swap_*` multi-step tools |
| Transfer method | `gate-wallet send` one-shot | `dex_wallet_sign_transaction` + broadcast |
| Agent binary dependency | None | `tools/tx-checkin/bin/` |

**CRITICAL**: When using this CLI skill, the agent **MUST NOT** run `tx-checkin` binary separately. The CLI handles GV checkin internally. Just run the CLI command after user confirmation.

---

## Agent Usage Notes

- Agent runs in a non-interactive shell (no stdin). Commands that ask for confirmation will hang. For `send` and `swap`, always confirm with the user in chat **before** running the command.
- The `send` and `swap` commands are one-shot: they preview, checkin, sign, and broadcast in a single run.
- All amounts use **human-readable values**, not smallest chain units (wei/lamports).

---

## On-Chain Operation Flow

Transfer operations follow: **preview → user confirm in chat → execute one-shot command**.

1. **Pre-check**: `gate-wallet address` → `gate-wallet tokens` for sufficient funds
2. **Preview**: `gate-wallet transfer` (preview-only, no signing)
3. **User confirmation in chat**: Display details, wait for explicit approval
4. **Execute**: `gate-wallet send ...` (GV checkin, sign, broadcast handled internally)
5. **Verify**: `gate-wallet tx-detail <hash>`

**NEVER run `send` without explicit user confirmation.**

---

## Follow-up Routing

After completing an operation, **proactively suggest 2-4 relevant next actions**:

| User Intent After Operation | Target |
|-----------------------------|--------|
| Check balance / tokens | [./references/asset-query.md](./references/asset-query.md) |
| Transfer tokens | [./references/transfer.md](./references/transfer.md) |
| Swap tokens | `gate-dex-trade-cli` skill |
| Token prices, K-line, token security | `gate-dex-market-cli` skill |
| Login / session issues | [./references/auth.md](./references/auth.md) |

---

## NOT This Skill (Common Misroutes)

| User Intent | Correct Skill |
|-------------|---------------|
| DApp connect / sign / approve / contract call | `gate-dex-wallet-cli` |
| x402 payment | `gate-dex-wallet-cli` |
| On-chain withdraw to Gate Exchange (UID binding) | `gate-dex-wallet-cli` |
| MCP tool calls directly | `gate-dex-wallet-cli` |

---

## Supported Chains

EVM: `eth`, `bsc`, `polygon`, `arbitrum` (arb), `optimism` (op), `avax`, `base`
Non-EVM: `sol`

Chain names are case-insensitive.

---

## Security Rules

1. **Confirm before fund operations**: `send` and `swap` involve real funds. Always confirm target address, amount, token, and chain with the user in chat before running the command.
2. **Preview before execute**: Use `transfer` (preview-only) before `send`; use `quote` before `swap`.
3. **No external checkin binary**: Do not run `tx-checkin` binary — it is not needed; CLI handles it internally.
4. **Token confidentiality**: `~/.gate-wallet/auth.json` stores credentials. Never display the raw token to users. Never commit this file to Git.
