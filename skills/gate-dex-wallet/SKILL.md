---
name: gate-dex-wallet
version: "2026.4.16-1"
updated: "2026-04-16"
description: "Manages Gate DEX wallet accounts, identity, assets, and connectivity. Use when the user asks to 'log in with Google' or Gate, 'check my balance', 'show my wallet address', 'view tx history', 'send USDT', 'withdraw to Gate', 'pay an x402 URL', 'connect wallet', or 'use gate-wallet CLI'. Handles authentication, portfolio and swap history, transfers, Gate deposit flows, x402, DApp signing, approvals, contract calls, and wallet connection checks. Do NOT use for market data or token swap execution."
---

# Gate DEX Wallet

> **Pure Routing Layer** — This SKILL.md is a lightweight router. All sub-module details live in `references/`.

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)

## Signing gate — Gate Verify MCP (mandatory)

Before **any** MCP call to `dex_wallet_sign_transaction`, `dex_wallet_sign_message`, or **`dex_tx_x402_fetch`** (signing tools only — **`dex_tx_x402_checkin_preview`** is not a signing call and does **not** require prior `tx_checkin`):

1. User must pass the existing confirmation gates (preview / message text / payment intent) for that operation.
2. Agent **MUST** call the **Gate Verify** HTTP MCP server (see **Gate Verify MCP** under [MCP Server Connection Detection](#mcp-server-connection-detection)) tool **`/v1/tx/checkin`** or **`tx_checkin`** per [references/tx-checkin.md](./references/tx-checkin.md) and treat success as a **hard prerequisite**. **Do not** run the legacy **`tx-checkin`** shell binary or require the user to execute local check-in commands. Discover the verify server by scanning configured MCP servers until **`tools/list`** includes the check-in tool. **Auth:** pass **`authorization`** in the check-in tool **`arguments`** with the **same `mcp_token`** as wallet MCP calls — **not** by copying the wallet server’s HTTP **`headers`** onto the Verify MCP entry — see [references/tx-checkin.md](./references/tx-checkin.md).
3. After **`dex_tx_transfer_preview`**, the check-in **`message`** argument **must** be the preview field **`txBundle`** string **only** — **do not** assemble txbundle JSON from `unsigned_tx_hex` or other fields (see [references/tx-checkin.md](./references/tx-checkin.md)).
4. **x402 (`dex_tx_x402_fetch`)**: **Do not** call `dex_tx_x402_fetch` first to probe 402. For **EVM exact / EIP-3009** (e.g. CoinGecko Pro x402 on Base), **first** call wallet MCP **`dex_tx_x402_checkin_preview`** — it returns the **`tx_checkin`** payload (including the correct 64-hex **`message`**) and **`x402_payment_required_b64`** so the agent never hand-builds the EIP-3009 digest. **Then** complete Gate Verify **`/v1/tx/checkin`** / **`tx_checkin`** using **`authorization`** (same **`mcp_token`**) together with the **`tx_checkin`** fields returned by preview. **Then** call **`dex_tx_x402_fetch`** with the same `url` / `method` / `body` / `headers` as preview, **`checkin_token`** from Verify, and the **same** **`x402_payment_required_b64`** from the preview result. For **POST JSON**, include **`Content-Type: application/json`** in the `headers` JSON on **both** preview and fetch (avoids common **415**). Full ordering and Solana / upto exceptions: [references/x402.md](./references/x402.md), [references/tx-checkin.md](./references/tx-checkin.md).
5. Other single-step MCP tools that sign internally: same **`/v1/tx/checkin`** call **immediately before** the wallet MCP tool when the gateway requires it; follow backend docs for `checkin_token` / intent payload.

## Applicable Scenarios

Use this skill when the user wants to **manage their on-chain wallet account, identity, or assets**:

- Authenticate or manage sessions (login via Google or Gate OAuth, logout)
- Query token balances, total portfolio value, or wallet addresses
- View transaction history or past swap records
- Transfer or send tokens to an address (single or batch); **mandatory Gate Verify MCP check-in** (`/v1/tx/checkin`) before any signing ([references/tx-checkin.md](./references/tx-checkin.md))
- Withdraw or cash out **on-chain** to their Gate Exchange account (deposit address resolved for their UID; not CEX-internal balance moves from this skill)
- Pay for HTTP 402 resources via x402 protocol (EVM exact/upto, Solana exact/upto); **`dex_tx_x402_checkin_preview`** (EVM EIP-3009) then **Gate Verify MCP check-in** then **`dex_tx_x402_fetch`** ([references/x402.md](./references/x402.md), [references/tx-checkin.md](./references/tx-checkin.md))
- Interact with DApps (connect wallet, sign messages, approve tokens, call contracts)
- Use the gate-wallet CLI tool for any of the above
- Detect or configure MCP Server connectivity

---

## Capability Boundaries

| Supported | Not Supported (route elsewhere) |
|-----------|---------------------------------|
| Authentication & session management | Token price / K-line queries -> `gate-dex-market` |
| Balance & address queries | Token swap execution -> `gate-dex-trade` |
| Transaction & swap history | Token security audits -> `gate-dex-market` |
| Token transfers (EVM + Solana); on-chain withdraw to Gate Exchange (deposit address flow) | |
| x402 payment (EVM exact/upto + Solana exact/upto) | |
| DApp interactions & approvals | |
| CLI dual-channel operations | |

---

## Module Routing

Route to the corresponding sub-module based on user intent:

| User Intent | Target |
|-------------|--------|
| Login, logout, sign in, sign out, token expired, session expired, OAuth, Google login, Gate login, authenticate, re-login, switch account, "I can't access my wallet", "not logged in" | [references/auth.md](./references/auth.md) |
| Check balance, total assets, portfolio value, wallet address, my address, how much do I have, show my tokens, tx history, transaction history, swap history, past transactions, "what do I own", "how many ETH", "list my coins", "show holdings" | [references/asset-query.md](./references/asset-query.md) |
| Withdraw to Gate Exchange, cash out to my Gate account, send funds to the exchange deposit address, move coins from wallet to Gate (on-chain deposit), bind or rebind Gate UID for withdraw | [references/withdraw.md](./references/withdraw.md) |
| Transfer, send tokens, send to address, batch transfer, "send 1 ETH to 0x...", "transfer USDT", "move tokens", "pay someone", "send crypto to a friend" (arbitrary or known on-chain address — not exchange deposit resolution) | [references/transfer.md](./references/transfer.md) + [references/tx-checkin.md](./references/tx-checkin.md) before sign |
| Any signing: before `dex_wallet_sign_transaction` / `dex_wallet_sign_message`; checkin_token; Gate Verify `/v1/tx/checkin` | [references/tx-checkin.md](./references/tx-checkin.md) (read **before** signing) |
| 402 payment, x402 pay, payment required, pay for API, pay for URL, "fetch and pay", "call this URL and pay", "paid endpoint", "pay for access", "HTTP 402", Permit2 payment, upto payment | [references/x402.md](./references/x402.md) (`dex_tx_x402_checkin_preview` → [references/tx-checkin.md](./references/tx-checkin.md) → `dex_tx_x402_fetch`) |
| DApp connect, connect wallet, sign message, approve, revoke approval, contract call, EIP-712, Permit, personal_sign, "interact with Uniswap", "add liquidity", "stake on Lido", "mint NFT", "sign for DApp login", authorize contract | [references/dapp.md](./references/dapp.md) + [references/tx-checkin.md](./references/tx-checkin.md) before every sign |
| gate-wallet CLI, command line, terminal, openapi-swap, hybrid swap, "use CLI", "run command", "gate-wallet balance", script automation, npm gate-wallet | [references/cli.md](./references/cli.md) |

---

## MCP Server Connection Detection

Before the first MCP tool call in a session, perform one connection probe:

1. **Discover**: Scan configured MCP servers for tools `dex_wallet_get_token_list`, `dex_tx_quote`, and `dex_tx_swap`.
2. **Identify**: Accept flexible server names (gate-wallet, gate-dex, dex, wallet, user-gate-wallet, or any custom name).
3. **Verify**: `CallMcpTool(server="<id>", toolName="dex_chain_config", arguments={chain: "eth"})`.

| Result | Action |
|--------|--------|
| Success | Record server identifier; use for all subsequent calls this session |
| Failure | Display setup guide below (at most once per session); re-detect next session |

### OpenClaw Platform Detection

When the OpenClaw/mcporter platform is detected, route MCP calls through `mcporter`:

```text
CallMcpTool(server="mcporter", toolName="call_tool", arguments={
  server: "<gate-dex-server>",
  tool: "<tool_name>",
  arguments: { ...params }
})
```

### Setup Guide (shown once on detection failure)

```
Gate DEX MCP Server:
  URL:  https://api.gatemcp.ai/mcp/dex
  Type: HTTP

  Cursor:      Settings -> MCP -> Add server, or edit ~/.cursor/mcp.json
  Claude Code:  claude mcp add --transport http gate-dex --scope project https://api.gatemcp.ai/mcp/dex
  Codex CLI:    codex mcp add gate-dex --transport http --url https://api.gatemcp.ai/mcp/dex
```

### Gate Verify MCP (signing check-in)

Add a **second** HTTP MCP server used **only** for transaction check-in before signing ([references/tx-checkin.md](./references/tx-checkin.md)):

```
Gate Verify MCP:
  URL:  https://api.gatemcp.ai/mcp/dex/sec
  Type: HTTP

  Cursor:      Settings -> MCP -> Add server (URL only is fine for check-in; pass mcp_token as tool arg authorization per references/tx-checkin.md)
  Tool name:   /v1/tx/checkin or tx_checkin  (discover via tools/list; server name is user-defined, e.g. gate-dex-sec)
```

Before the first check-in in a session, resolve the verify server id by scanning configured MCP servers until **`tools/list`** includes **`tx_checkin`** or **`/v1/tx/checkin`**.

### Runtime Error Handling

| Error Type | Keywords | Action |
|------------|----------|--------|
| MCP Server not configured | `server not found`, `unknown server` | Show setup guide |
| Remote service unreachable | `connection refused`, `timeout`, `DNS error` | Prompt to check server status and network |
| Authentication failure | `400`, `401`, `unauthorized` | Follow §3 of [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) |

---

## Follow-up Routing

After completing an operation, **proactively suggest 2-4 relevant next actions** to the user (see each module's "Post-XXX Suggestions" section for templates). Then route based on the user's response:

| User Intent After Operation | Target |
|-----------------------------|--------|
| View token prices, K-line charts, market cap, trading volume | `gate-dex-market` |
| Run a token security audit, check if token is safe | `gate-dex-market` |
| Transfer or send tokens to an arbitrary on-chain address | [references/transfer.md](./references/transfer.md) |
| Withdraw or cash out on-chain to Gate Exchange | [references/withdraw.md](./references/withdraw.md) |
| Swap, exchange, buy, sell, convert tokens on DEX | `gate-dex-trade` |
| Pay for a 402 resource, x402 payment | [references/x402.md](./references/x402.md) (preview → [references/tx-checkin.md](./references/tx-checkin.md) → fetch) |
| Interact with a DApp, connect wallet, sign, approve | [references/dapp.md](./references/dapp.md) |
| Mandatory Gate Verify MCP check-in before any signing, checkin_token | [references/tx-checkin.md](./references/tx-checkin.md) |
| Login, re-login, fix expired auth, switch account | [references/auth.md](./references/auth.md) |
| Use CLI commands, gate-wallet terminal operations | [references/cli.md](./references/cli.md) |
| Check balance, view assets, transaction history | [references/asset-query.md](./references/asset-query.md) |

---

## NOT This Skill (Common Misroutes)

These intents should NOT trigger this skill:

| User Intent | Correct Skill |
|-------------|---------------|
| "What is the price of ETH?" / "Show BTC chart" / "Token rankings" | `gate-dex-market` |
| "Swap ETH for USDT" / "Buy SOL" / "Exchange tokens" / "DEX trade" | `gate-dex-trade` |
| "Is this token safe?" / "Audit contract 0x..." / "Honeypot check" | `gate-dex-market` |
| "Show top gainers" / "New token listings" / "Market overview" | `gate-dex-market` |

---

## Supported Chains

EVM: `eth`, `bsc`, `polygon`, `arbitrum`, `optimism`, `avax`, `base` | Non-EVM: `sol`

---

## Security Rules

1. **Authentication first**: Verify `mcp_token` validity before all operations; on failure follow §3 of [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md).
2. **Token confidentiality**: Never display `mcp_token` in plaintext; use placeholders like `<mcp_token>`.
3. **MCP Server errors**: Display all MCP Server error messages to users transparently — never hide or modify them.
