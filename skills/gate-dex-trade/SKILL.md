---
name: gate-dex-trade
version: "2026.3.19-1"
updated: "2026-03-19"
description: "Gate DEX swap EXECUTION skill. For on-chain token exchange transactions that MODIFY blockchain state: swap, buy, sell, exchange, convert tokens, cross-chain bridge. Every operation here results in an on-chain transaction requiring signing. This skill EXECUTES trades — it does not provide read-only data lookups or manage wallet accounts."
---

# Gate DEX Trade

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

> **Pure Routing Layer** — Swap EXECUTION only. Every operation produces an on-chain transaction. All specifications in `references/`.

**Trigger Scenarios**: Use when the user wants to **execute a token exchange** that modifies blockchain state:
- Swap: "swap ETH for USDT", "exchange 100 USDC to DAI", "convert my BNB"
- Buy/Sell: "buy ETH", "sell my USDT", "purchase SOL"
- Cross-chain: "bridge ETH from Arbitrum to Base", "cross-chain swap"
- Swap quote: "how much USDT will I get for 1 ETH" (with intent to trade)

## Project convention — MCP only (this workspace)

**Do not use OpenAPI** for swap unless user explicitly asks OpenAPI/AK/SK. MCP unavailable → `references/setup.md` only.

---

**NOT this skill** (common misroutes):
- "what is the price of ETH" → `gate-dex-market` (read-only lookup, no trade intent)
- "check my swap history" → `gate-dex-wallet` (account query)
- "transfer ETH to 0xABC..." → `gate-dex-wallet` (direct transfer, not swap)
- "approve contract" (outside swap context) → `gate-dex-wallet` (DApp interaction)

---

## Auto-Update (Session Start Only)

On session start (not during interactions), check for updates once:

1. Read this file's frontmatter `version` and `updated` fields.
2. Fetch remote SKILL.md from `https://raw.githubusercontent.com/gateio/web3_wallet_skill/master/skills/gate-dex-trade/SKILL.md`.
3. Compare: update if remote version > local version, or same version but remote `updated` date is newer.
4. On update: fetch and overwrite all skill files (`SKILL.md`, `README.md`, `CHANGELOG.md`, `install.sh`, `references/mcp.md`, `references/openapi.md`).
5. On failure: silently continue — never block user interactions.
6. Skip if: already checked this session, or skill was installed < 24h ago.

---

## Routing Flow

```text
User triggers trading intent
  ↓
Step 1: Has user explicitly specified a mode?
  ├─ Explicitly mentions "OpenAPI" / "AK/SK" / "API Key" → OpenAPI mode
  ├─ Otherwise → MCP only (Step 2)
  └─ Not specified → Step 2
  ↓
Step 2: Is this a cross-chain swap?
  ├─ Cross-chain → Must use MCP mode (OpenAPI doesn't support cross-chain), proceed to Step 3
  └─ Same-chain / uncertain → Step 3
  ↓
Step 3: Gate Wallet MCP Server Discovery & Detection
  a) Scan configured MCP Server list for Servers providing both `dex_tx_quote` and `dex_tx_swap` tools
  b) If found → Record server identifier, verify with:
     CallMcpTool(server="<identifier>", toolName="dex_chain_config", arguments={chain: "ETH"})
     ├─ Success → MCP mode
     └─ Failed → Step 4
  c) No matching Server → Step 4
  ↓
Step 4: MCP unavailable → setup guide only (`references/setup.md`), no OpenAPI fallback
```

---

## Mode Dispatch

### MCP Mode

**Read and strictly follow** `references/mcp.md`, execute according to its complete workflow.

Includes: connection detection, authentication (mcp_token), MCP Resource/tool calls (dex_tx_quote / dex_tx_swap / dex_tx_swap_detail), token address resolution, native_in/native_out rules, three-step confirmation gateway (SOP), quote templates, risk warnings, cross-Skill collaboration, security rules.

### OpenAPI Mode (Progressive Loading)

**Default off in this workspace** — explicit OpenAPI request only.

**Limitation: OpenAPI mode only supports same-chain Swap, does not support cross-chain exchanges.**

Load files progressively — only load what the current step needs:

1. **Always load first**: `references/openapi/_shared.md` — env detection, credentials, API call method (via helper script)
2. **Then load based on swap stage**:

| Stage | Load File | When |
|-------|-----------|------|
| Query (chain/gas) | `references/openapi/quote.md` | User asks about chains or gas |
| Swap: get quote | `references/openapi/quote.md` + `references/openapi/sop.md` | User initiates swap |
| Swap: build tx | `references/openapi/build.md` | After quote confirmed (SOP Step 2) |
| Swap: sign tx | `references/openapi/sign.md` | After build confirmed (SOP Step 3) |
| Swap: submit | `references/openapi/submit.md` | After signing complete |
| History | `references/openapi/submit.md` | User asks for swap history |

3. **On error**: `references/openapi/errors.md`

> Legacy monolithic file preserved at `references/openapi.md` for backward compatibility.

### MCP Server Setup Guide

When MCP detection fails and a setup guide is needed, **read and display** `references/setup.md`. Show only the configuration for the user's current platform when identifiable. Display at most once per session.

---

## Supported Chains

Actual supported chains are determined by runtime API/Resource returns:
- **MCP Mode**: `swap://supported_chains` Resource
- **OpenAPI Mode**: `trade.swap.chain` interface

For uncommon chains: MCP calls `dex_chain_config`, OpenAPI calls `trade.swap.chain`.

---

## Cross-Skill Collaboration

| Source | Scenario | Routing |
|--------|----------|---------|
| `gate-dex-wallet` | Exchange tokens after viewing balance | Carry context, follow routing flow |
| `gate-dex-market` | Buy token after viewing market data | Carry token info, follow routing flow |
| `gate-dex-wallet/references/transfer.md` | Exchange remaining tokens after transfer | Carry chain/token context |

---

## Security Rules

1. **Mode selection transparency**: Clearly inform users of the current mode and reasons
2. **Authentication isolation**: MCP uses `mcp_token`, OpenAPI uses AK/SK — never mix
3. **Three-step confirmation gateway**: Trading pair confirmation → quote display → signature authorization — cannot be skipped
4. **Balance pre-check**: Mandatory verification of asset and Gas token sufficiency before trading
5. **Risk warnings**: Forced warning for exchange value difference > 5%, high slippage (> 5%) MEV attack warnings
6. **No OpenAPI fallback** when MCP fails (this project)
7. **No repeated guidance**: MCP setup guide displayed at most once per session
