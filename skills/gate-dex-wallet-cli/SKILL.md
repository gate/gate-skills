---
name: gate-dex-wallet-cli
version: "2026.5.7-1"
updated: "2026-05-07"
description: "Gate DEX CLI wallet skill (pure REST). Auth via OAuth, balance, wallet/account addresses, token list, tx history, transfers, and signing. GV checkin is built into signing commands. Use this skill whenever the user wants to log in, check balance/address, view tx history, transfer tokens, or sign messages via the gate-dex CLI. Trigger phrases include login, logout, balance, address, tokens, tx history, transfer, send, sign-msg, sign-tx. For swaps use gate-dex-trade-cli; for market data use gate-dex-market-cli."
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "💼",
        "os": ["linux", "darwin"],
        "requires": {
          "bins": ["gate-dex"]
        },
        "install": [
          {
            "id": "download-linux-x64",
            "kind": "download",
            "os": ["linux"],
            "url": "https://gate-dex-cli.gateweb3.cc/latest/gate-dex-linux-x64",
            "bins": ["gate-dex"],
            "label": "Download gate-dex (Linux x64)"
          },
          {
            "id": "download-macos-arm64",
            "kind": "download",
            "os": ["darwin"],
            "url": "https://gate-dex-cli.gateweb3.cc/latest/gate-dex-darwin-arm64",
            "bins": ["gate-dex"],
            "label": "Download gate-dex (macOS arm64)"
          }
        ]
      }
  }
---

# Gate DEX CLI

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.
- **Only use the `gate-dex` CLI subcommands explicitly listed in this skill and its references.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

> **Pure Routing Layer** — This SKILL.md is a lightweight router. Sub-module details live in `references/`.

## Overview

`gate-dex` is a standalone CLI tool that communicates with Gate DEX services via REST APIs. **No MCP server is required.** All signing operations (transfer, sign-msg, swap) include built-in GV security checkin — the agent does not need to run any external binary.

Auth: login via Gate/Google OAuth, token stored in `~/.gate-dex/auth.json`.

The CLI also supports an **interactive REPL** — running `gate-dex` with no arguments opens a prompt.

## Applicable Scenarios

Use this skill when the user wants to:

- Authenticate (login/logout) via Gate OAuth or Google OAuth
- Query token balances, total portfolio value, or wallet addresses
- View transaction history
- Transfer or send tokens to an on-chain address (EVM + Solana)
- Sign raw messages or raw transactions
- Use `gate-dex` CLI commands directly

---

## Capability Boundaries

| Supported | Route elsewhere |
|-----------|----------------|
| Authentication & session management | Token swap → `gate-dex-trade-cli` skill |
| Balance, address & token list queries | Market data / token info / K-line → `gate-dex-market-cli` skill |
| Transaction history | DApp interactions → `gate-dex-wallet` skill (MCP-based) |
| Token transfers (EVM + Solana) | x402 payments → `gate-dex-wallet` skill (MCP-based) |
| Sign 32-byte hex messages / raw tx | MCP tool calls → `gate-dex-wallet` skill (MCP-based) |

**Prerequisites**: A `gate-dex` binary on PATH.

- **GateClaw managed scenario** — `skill/setup.sh` runs automatically on install and drops a pre-built Linux binary into `/home/node/.openclaw/skills/bin/gate-dex`. Environment variables (`RUN_ENV`, `*_URL`) are collected via the GateClaw Web form and injected into `process.env` at runtime.
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
curl -fsSL https://gate-dex-cli.gateweb3.cc/latest/gate-dex-linux-x64 \
  -o /usr/local/bin/gate-dex
chmod +x /usr/local/bin/gate-dex

# Login
gate-dex login           # Gate OAuth (default)
gate-dex login --google  # Google OAuth
```

**Storage**:
- Auth token → `~/.gate-dex/auth.json`

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
| `--auth-dir <path>` | Custom auth storage directory (overrides `~/.gate-dex`; also via `GATE_DEX_HOME` env) |
| `--auth-file <path>` | Custom auth.json file path (overrides `--auth-dir`; also via `GATE_DEX_AUTH_FILE` env) |
| `-v, --version` | Print version |

---

## Sub-Modules

| Sub-module | File | Scope |
|-----------|------|-------|
| **Auth** | `references/auth.md` | OAuth login/logout, session status, web3-domain |
| **Asset Query** | `references/asset-query.md` | balance, address, tokens, tx-history, tx-detail |
| **Transfer & Sign** | `references/transfer.md` | transfer (preview), send (one-shot), sign-msg, sign-tx, sol-tx, gas |

## Routing Rules

| User Intent | Target |
|-------------|--------|
| Login, logout, re-login, session expired, OAuth, "not logged in", switch account, web3-domain | `references/auth.md` |
| Check balance, total assets, wallet address, account address, token list, tx history, "how much do I have", "show my tokens" | `references/asset-query.md` |
| Transfer, send tokens, "send ETH to 0x...", "transfer USDT", "pay someone", "move tokens", sign-msg, sign-tx, sol-tx | `references/transfer.md` |
| Swap, exchange tokens, "swap ETH for USDT", "buy SOL", quote, "convert tokens" | → `gate-dex-trade-cli` skill |
| K-line, token price, market cap, liquidity, trading stats, token security, token rankings, new tokens | → `gate-dex-market-cli` skill |

## Execution

1. **Detect intent** using the Routing Rules table; resolve to exactly one sub-module file or a peer-skill route.
2. **Read the matched sub-module** (`references/auth.md`, `references/asset-query.md`, or `references/transfer.md`) and follow its workflow as the authoritative execution contract.
3. **Apply the safety rules in this SKILL.md** (Security Rules section) before any write command (`send`, `sign-msg`, `sign-tx`).
4. **For write paths** (`send`): require explicit user confirmation in chat before invoking the CLI; preview via `transfer` first.
5. **For peer-skill routes** (`gate-dex-trade-cli`, `gate-dex-market-cli`): hand off without invoking those skills' commands from here.

---

## Full Command Reference

### Auth & Session
| Command | Description |
|---------|-------------|
| `login` | Gate OAuth Device Flow login |
| `login --google` | Google OAuth Device Flow login |
| `login --no-open` | Print auth URL instead of opening browser |
| `logout` | Logout and clear `~/.gate-dex/auth.json` |
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

### Swap (out of scope — route to `gate-dex-trade-cli` skill)

The `quote`, `swap`, `swap-tokens`, `bridge-tokens`, `swap-history`, and `swap-detail` commands are documented in the `gate-dex-trade-cli` skill. Do not invoke them from this skill.

### Transaction History

| Command | Description |
|---------|-------------|
| `tx-history` | Transfer transaction history |
| `tx-detail <hash>` | Transaction detail by hash |

### Market & Token Data (out of scope — route to `gate-dex-market-cli` skill)

The `tx-stats`, `kline`, `liquidity`, `token-info`, `token-risk`, `token-rank`, and `new-tokens` commands are documented in the `gate-dex-market-cli` skill. Do not invoke them from this skill.

### Chain / RPC
| Command | Description |
|---------|-------------|
| `chain-config [chain]` | Chain config (networkKey, endpoint, chainID) |
| `rpc` | Raw JSON-RPC call |

### Maintenance
| Command | Description |
|---------|-------------|
| `cleanup` | Delete `~/.gate-dex` |

---

## Key Design Differences from MCP-based Skills

| Aspect | This skill (gate-dex-wallet-cli) | MCP-based skill (gate-dex-wallet) |
|--------|------------------------------|-----------------------------------|
| Transport | Pure REST (no MCP) | MCP tool calls |
| GV security checkin | Built into CLI `send`/`swap`/`sign-msg`/`sign-tx` | External `tx-checkin` binary required |
| Auth storage | `~/.gate-dex/auth.json` | MCP session `mcp_token` |
| Swap method | `gate-dex swap` one-shot | `dex_tx_swap_*` multi-step tools |
| Transfer method | `gate-dex send` one-shot | `dex_wallet_sign_transaction` + broadcast |
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

1. **Pre-check**: `gate-dex address` → `gate-dex tokens` for sufficient funds
2. **Preview**: `gate-dex transfer` (preview-only, no signing)
3. **User confirmation in chat**: Display details, wait for explicit approval
4. **Execute**: `gate-dex send ...` (GV checkin, sign, broadcast handled internally)
5. **Verify**: `gate-dex tx-detail <hash>`

**NEVER run `send` without explicit user confirmation.**

---

## Follow-up Routing

After completing an operation, **proactively suggest 2-4 relevant next actions**:

| User Intent After Operation | Target |
|-----------------------------|--------|
| Check balance / tokens | `references/asset-query.md` |
| Transfer tokens | `references/transfer.md` |
| Swap tokens | `gate-dex-trade-cli` skill |
| Token prices, K-line, token security | `gate-dex-market-cli` skill |
| Login / session issues | `references/auth.md` |

---

## NOT This Skill (Common Misroutes)

| User Intent | Correct Skill |
|-------------|---------------|
| DApp connect / sign / approve / contract call | `gate-dex-wallet` skill (MCP-based) |
| x402 payment | `gate-dex-wallet` skill (MCP-based) |
| On-chain withdraw to Gate Exchange (UID binding) | `gate-dex-wallet` skill (MCP-based) |
| MCP tool calls directly | `gate-dex-wallet` skill (MCP-based) |

---

## Supported Chains

EVM: `eth`, `bsc`, `polygon`, `arbitrum` (arb), `optimism` (op), `avax`, `base`
Non-EVM: `sol`

Chain names are case-insensitive.

---

## Security Rules

1. **Confirm before fund operations**: `send` involves real funds. Always confirm target address, amount, token, and chain with the user in chat before running the command. Without explicit user confirmation in chat, no `send` may be executed — only read-only queries (`balance`, `address`, `tokens`, `tx-history`, `tx-detail`, `transfer` preview) are allowed.
2. **Preview before execute**: Use `transfer` (preview-only) before `send`.
3. **No external checkin binary**: Do not run `tx-checkin` binary — it is not needed; CLI handles it internally.
4. **Token confidentiality**: `~/.gate-dex/auth.json` stores credentials. Never display the raw token to users. Never commit this file to Git.
5. **Transaction irreversibility**: On-chain transfers are generally irreversible. Re-verify recipient address, chain, and token contract with the user before executing `send`.

---

## Risk Disclosure

Digital asset transactions are generally irreversible. Please verify the recipient address before confirming. Outputs from this skill are for informational purposes only and do not constitute investment, financial, tax, or legal advice. AI-assisted outputs are for general information only and do not constitute any representation, warranty, or guarantee by Gate. This skill is intended for users aged 18 or above with full civil capacity; availability may vary by jurisdiction.
