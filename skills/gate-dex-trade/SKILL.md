---
name: gate-dex-trade
version: "2026.3.24-1"
updated: "2026-03-24"
description: "Gate DEX swap EXECUTION skill. For on-chain token exchange transactions that MODIFY blockchain state: swap, buy, sell, exchange, convert tokens, cross-chain bridge. Every operation here results in an on-chain transaction requiring signing. This skill EXECUTES trades — it does not provide read-only data lookups or manage wallet accounts."
---

# Gate DEX Trade


> **Pure Routing Layer** — Swap EXECUTION only. Every operation produces an on-chain transaction. All specifications in `references/`.

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)

**Trigger Scenarios**: Use when the user wants to **execute a token exchange** that modifies blockchain state:
- Swap: "swap ETH for USDT", "exchange 100 USDC to DAI", "convert my BNB"
- Buy/Sell: "buy ETH", "sell my USDT", "purchase SOL"
- Cross-chain: "bridge ETH from Arbitrum to Base", "cross-chain swap"
- Swap quote: "how much USDT will I get for 1 ETH" (with intent to trade)


---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate-Dex | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- dex_chain_config
- dex_tx_quote

**Execution Operations (Write)**

- dex_tx_swap

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)
- Permissions: Dex:Read

### Installation Check
- Required: Gate-Dex
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## Project convention — MCP only (this workspace)

**Do not use OpenAPI** for swap unless user explicitly asks OpenAPI/AK/SK. MCP unavailable → [`references/setup.md`](./references/setup.md) only.

---

**NOT this skill** (common misroutes):
- "what is the price of ETH" → `gate-dex-market` (read-only lookup, no trade intent)
- "check my swap history" → `gate-dex-wallet` (account query)
- "transfer ETH to 0xABC..." → `gate-dex-wallet` (direct transfer, not swap)
- "approve contract" (outside swap context) → `gate-dex-wallet` (DApp interaction)

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
Step 4: MCP unavailable → setup guide only ([`references/setup.md`](./references/setup.md)), no OpenAPI fallback
```

---

## Mode Dispatch

### MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), execute according to its complete workflow.

Includes: connection detection, authentication (mcp_token), MCP Resource/tool calls (dex_tx_quote / dex_tx_swap / dex_tx_swap_detail), token address resolution, native_in/native_out rules, three-step confirmation gateway (SOP), quote templates, risk warnings, cross-Skill collaboration, security rules.

### OpenAPI Mode (Progressive Loading)

**Default off in this workspace** — explicit OpenAPI request only.

**Limitation: OpenAPI mode only supports same-chain Swap, does not support cross-chain exchanges.**

Load files progressively — only load what the current step needs:

1. **Always load first**: [`references/openapi/_shared.md`](./references/openapi/_shared.md) — env detection, credentials, API call method (via helper script)
2. **Then load based on swap stage**:

| Stage | Load File | When |
|-------|-----------|------|
| Query (chain/gas) | [`openapi/quote.md`](./references/openapi/quote.md) | User asks about chains or gas |
| Swap: get quote | [`openapi/quote.md`](./references/openapi/quote.md) + [`openapi/sop.md`](./references/openapi/sop.md) | User initiates swap |
| Swap: build tx | [`openapi/build.md`](./references/openapi/build.md) | After quote confirmed (SOP Step 2) |
| Swap: sign tx | [`openapi/sign.md`](./references/openapi/sign.md) | After build confirmed (SOP Step 3) |
| Swap: submit | [`openapi/submit.md`](./references/openapi/submit.md) | After signing complete |
| History | [`openapi/submit.md`](./references/openapi/submit.md) | User asks for swap history |

3. **On error**: [`openapi/errors.md`](./references/openapi/errors.md)

> Legacy monolithic file preserved at [`references/openapi.md`](./references/openapi.md) for backward compatibility.

### MCP Server Setup Guide

When MCP detection fails and a setup guide is needed, **read and display** [`references/setup.md`](./references/setup.md). Show only the configuration for the user's current platform when identifiable. Display at most once per session.

---

## Supported Chains

Actual supported chains are determined by runtime API/Resource returns:
- **MCP Mode**: `swap://supported_chains` Resource
- **OpenAPI Mode**: `trade.swap.chain` interface

For uncommon chains: MCP calls `dex_chain_config`, OpenAPI calls `trade.swap.chain`.

---

## Security Rules

1. **Three-step confirmation gateway**: Trading pair confirmation → quote display → signature authorization — cannot be skipped
2. **Balance pre-check**: Mandatory verification of asset and Gas token sufficiency before trading
3. **Risk warnings**: Forced warning for exchange value difference > 5%, high slippage (> 5%) MEV attack warnings
4. **Authentication & credentials**: Follow §3 of [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md); MCP uses `mcp_token`, OpenAPI uses AK/SK — never mix
5. **No OpenAPI fallback** when MCP fails (this project)
