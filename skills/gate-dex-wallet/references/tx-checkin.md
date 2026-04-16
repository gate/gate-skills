---
name: gate-dex-wallet-tx-checkin
version: "2.2.0"
updated: "2026-04-16"
description: "Mandatory transaction check-in before wallet signing via Gate Verify (tool tx_checkin or /v1/tx/checkin). Pass mcp_token as tool argument authorization (not wallet MCP HTTP headers on the Verify server). For x402 EVM EIP-3009, use dex_tx_x402_checkin_preview first to obtain message. Applies before dex_wallet_sign_transaction, dex_wallet_sign_message, and dex_tx_x402_fetch."
---

# Gate DEX Tx Check-in (Gate Verify MCP)

> **Mandatory execution path**: check-in is performed by calling the **Gate Verify** MCP server over HTTP. The agent uses **`CallMcpTool`** (or platform equivalent) against tool **`/v1/tx/checkin`** (some gateways expose the same endpoint as **`tx_checkin`**). **Do not** run the legacy **`tx-checkin`** shell binary or ask the user to execute check-in commands for this flow.

## MCP server

| Item | Value |
|------|--------|
| **HTTP URL** | `https://api.gatemcp.ai/mcp/dex/sec` |
| **Server id** | User-defined in MCP config (e.g. `gate-dex-sec`, `dex-sec`); discover by **`tools/list`** containing **`/v1/tx/checkin`** or **`tx_checkin`** |
| **Tool name** | **`/v1/tx/checkin`** or **`tx_checkin`** (title may show *Transaction Checkin*) |

**Authentication (required for live `tx_checkin`):** pass session credentials in the tool **`arguments`**, not by mirroring the wallet MCP’s HTTP **`headers`** onto the Verify server. Include **`authorization`** with the **same `mcp_token`** you use for **Gate wallet / DEX MCP** tools (`dex_chain_config`, `dex_wallet_*`, etc.). Use the **exact** string shape required by the live MCP **`inputSchema`** (often the raw token; if the schema shows `Bearer …`, prefix accordingly). The Verify MCP server entry in `mcp.json` does **not** need a copy of the wallet server’s **`headers`** for this check-in flow. If check-in returns 401/403 or empty `checkin_token`, re-check **`authorization`** matches the current session token after login or refresh.

**Streamable HTTP / raw POST:** If you call Verify **outside** the MCP client (e.g. `curl` against the HTTP gateway), some deployments return **HTTP 400** unless the request includes **`Accept: application/json, text/event-stream`**. MCP transports usually set transport headers for you; this note applies mainly to manual HTTP debugging.

## Tool: `/v1/tx/checkin`

**Purpose**: Create a transaction-signing check-in before downstream signing on the wallet MCP.

**Required arguments** (see live MCP `inputSchema`):

| Field | Notes |
|-------|--------|
| `authorization` | Session **`mcp_token`** (same as wallet MCP). Passed as a **tool argument**, not via HTTP `Authorization` header on the Verify server config. Format per live **`inputSchema`**. |
| `wallet_address` | Signing wallet; must match the operation (e.g. preview `from_address` / `key_info`). |
| `type` | Business transaction type string — use a plain token (do not embed quotes or semicolons in the value). Prefer a value from preview **`key_info`** when the wallet MCP returns one; otherwise use a stable label for the flow: e.g. **`transfer`** after `dex_tx_transfer_preview`, **`sign_message`** for `dex_wallet_sign_message`, **`x402`** for payment fetch when no finer type is specified. |
| `source` | **Always `3`** (AI agent) for agent-driven flows. |
| `message` **or** `intent` | **One is required** (mutually exclusive per schema). |

**Optional**: `chain`, `chain_category`, `token_change` — supply when preview / context provides them (align with `dex_tx_transfer_preview` / `key_info`).

**Success response** (shape per server): structured JSON with **`code`**, **`msg`**, and **`data`** containing at least **`checkin_token`** and optionally **`need_otp`**. Parse the MCP tool result text as JSON to read **`data.checkin_token`**.

If `need_otp` is true, follow product OTP guidance before continuing.

## Hard rule (wallet skill policy)

- **Before every** `dex_wallet_sign_transaction`, **every** `dex_wallet_sign_message`, and **every** `dex_tx_x402_fetch` call, the agent **MUST** complete a **successful** Gate Verify check-in (`/v1/tx/checkin` or `tx_checkin`) in the same user session (after user confirmation, immediately before that wallet MCP call).
- **Do not skip** check-in because a previous transaction succeeded without it, or because no error appeared yet.
- **x402:** **Do not** call `dex_tx_x402_fetch` first to probe 402. For **EVM EIP-3009** (e.g. CoinGecko Pro x402 on Base), call **`dex_tx_x402_checkin_preview`** first, then call Gate Verify **`/v1/tx/checkin`** / **`tx_checkin`** with arguments from the preview **`tx_checkin`** object, then **`dex_tx_x402_fetch`** with **`checkin_token`** and the **same** **`x402_payment_required_b64`** from preview ([x402.md](./x402.md)).
- If check-in fails (MCP error, non-success `code`, missing `checkin_token` when required), **abort** — do not call signing tools or `dex_tx_x402_fetch`.

## Applicable scenarios

- **Always** before `dex_wallet_sign_transaction` (transfers, withdraws, DApp txs, any raw tx signing).
- **Always** before `dex_wallet_sign_message` (personal_sign, EIP-712, DApp login). **`message`** argument to **`/v1/tx/checkin`** / **`tx_checkin`** must match the **exact** payload to be signed (see **Check-in message rules** below).
- **Always** before `dex_tx_x402_fetch`. For **EVM exact / EIP-3009**, the **`message`** passed to Gate Verify **`/v1/tx/checkin`** / **`tx_checkin`** **must** be **`tx_checkin.message`** from the **`dex_tx_x402_checkin_preview`** result (64-hex digest) — **do not** compute that digest in the agent. For Solana or Permit2 **upto**, use **`message`** / **`intent`** per backend ([x402.md](./x402.md)); then pass **`checkin_token`** into `dex_tx_x402_fetch`.
- If the gateway returns an error mentioning check-in / registration, re-run **`/v1/tx/checkin`** / **`tx_checkin`** and retry only after success.

## Check-in message rules (aligned with signature type)

1. **`dex_wallet_sign_message`**: pass the **exact** string the wallet MCP will sign as **`message`** to **`/v1/tx/checkin`** / **`tx_checkin`** (same as former CLI `-message`).
2. **`dex_wallet_sign_transaction`** after **`dex_tx_transfer_preview`**: pass preview field **`txBundle`** **as-is** as **`message`**. **Do not** assemble txbundle JSON from `unsigned_tx_hex` or other fields.
3. **Structured intent**: if the backend expects an object instead of a flat message, pass **`intent`** (not `message`) per live schema and product docs.
4. **`dex_tx_x402_fetch` (EVM EIP-3009)**: call **`dex_tx_x402_checkin_preview`** first; pass **`message`** = preview result **`tx_checkin.message`** into Gate Verify **`/v1/tx/checkin`** / **`tx_checkin`**. This **`message`** is the EIP-3009 digest that **`dex_tx_x402_fetch`** will sign — it must not be invented or hashed by the agent. Rationale and **`PAYMENT-REQUIRED` b64** / **415** notes: [x402.md](./x402.md) § *Design notes*.

## Agent flow

1. Confirm the user intends to proceed to signing (preview / message text / payment intent).
2. **Resolve verify MCP `server` id** once per session if needed: scan configured MCP servers until **`tools/list`** includes **`/v1/tx/checkin`** or **`tx_checkin`**.
3. **Call** `CallMcpTool(server="<verify-server-id>", toolName="/v1/tx/checkin" | "tx_checkin", arguments={ authorization: <mcp_token>, wallet_address, type, source: 3, message **or** intent, chain?, chain_category?, token_change? })` (use the tool name your gateway exposes; include every required field from **`inputSchema`**).
4. Parse the tool result; on success read **`data.checkin_token`**.
5. **Then** call the wallet MCP signing tool with **`checkin_token`** when the tool exposes it (`dex_wallet_sign_transaction`, `dex_wallet_sign_message`, `dex_tx_x402_fetch` — see [transfer.md](./transfer.md), [dapp.md](./dapp.md), [x402.md](./x402.md)).

### Example (transfer after preview)

```text
CallMcpTool(
  server="<gate-dex-sec-mcp>",
  toolName="/v1/tx/checkin",
  arguments={
    authorization: "<mcp_token per inputSchema>",
    wallet_address: "<from_address>",
    type: "transfer",
    source: 3,
    message: "<exact txBundle string from dex_tx_transfer_preview>",
    chain: "<chain>",
    chain_category: "<evm|solana|... per preview/key_info>"
  }
)
# Then: dex_wallet_sign_transaction({ raw_tx: unsigned_tx_hex, ..., checkin_token: data.checkin_token })
```

### OpenClaw / mcporter

```text
CallMcpTool(server="mcporter", toolName="call_tool", arguments={
  server: "<gate-dex-sec-mcp>",
  tool: "/v1/tx/checkin",
  arguments: { authorization: "<mcp_token per inputSchema>", ... }
})
```

## Further reading

- Parent router: [SKILL.md](../SKILL.md) — verify MCP URL, discovery, and ordering rules.
- x402 ordering: [x402.md](./x402.md).

