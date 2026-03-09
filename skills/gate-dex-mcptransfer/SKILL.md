---
name: gate-dex-mcptransfer
version: "2026.3.5-1"
updated: "2026-03-05"
description: "Gate Wallet transfer execution. Build transaction, sign, broadcast. Use when user wants to 'send ETH', 'transfer USDT', 'transfer', 'send tokens'. Includes mandatory balance verification and user confirmation gate. Supports EVM multi-chain + Solana native/token transfers."
---

# Gate Wallet Transfer Skill

> Transfer domain — Gas estimation, transaction preview, balance verification, signing, broadcast, with mandatory user confirmation gate. 4 MCP tools + 1 cross-Skill call.

**Trigger scenarios**: When user mentions "transfer", "send", "transfer", "send ETH", "send tokens", or when other Skills guide the user to perform on-chain transfer operations.

## Step 0: MCP Server Connection Check (Mandatory)

**Before executing any operation, Gate Wallet MCP Server availability must be confirmed. This step cannot be skipped.**

Probe call:

```
CallMcpTool(server="gate-wallet", toolName="chain.config", arguments={chain: "eth"})
```

| Result | Action |
|--------|--------|
| Success | MCP Server available, proceed to next steps |
| `server not found` / `unknown server` | Cursor not configured → Show configuration guide (see below) |
| `connection refused` / `timeout` | Remote unreachable → Prompt to check URL and network |
| `401` / `unauthorized` | API Key auth failed → Prompt to check auth config |

### Display when Cursor is not configured

```
❌ Gate Wallet MCP Server not configured

The MCP Server named "gate-wallet" was not found in Cursor. Please configure as follows:

Method 1: Via Cursor Settings (recommended)
  1. Open Cursor → Settings → MCP
  2. Click "Add new MCP server"
  3. Fill in:
     - Name: gate-wallet
     - Type: HTTP
     - URL: https://your-mcp-server-domain/mcp
  4. Save and retry

Method 2: Manual config file edit
  Edit ~/.cursor/mcp.json, add:
  {
    "mcpServers": {
      "gate-wallet": {
        "url": "https://your-mcp-server-domain/mcp"
      }
    }
  }

If you don't have an MCP Server URL yet, please contact your administrator.
```

### Display when remote service is unreachable

```
⚠️  Gate Wallet MCP Server connection failed

MCP Server config was found, but the remote service could not be reached. Please check:
1. Confirm the service URL is correct (is the configured URL accessible)
2. Check network connection (VPN / firewall impact)
3. Confirm the remote service is running
```

### Display when API Key auth fails

```
🔑 Gate Wallet MCP Server authentication failed

MCP Server connected but API Key validation failed. The service uses AK/SK auth (x-api-key header).
Please contact your administrator for a valid API Key and confirm server-side config.
```

## Authentication

All operations in this Skill **require `mcp_token`**. User must be logged in before calling any tool.

- If no `mcp_token` → Guide to `gate-dex-mcpauth` to complete login, then return.
- If `mcp_token` expired (MCP Server returns token expired error) → Try `auth.refresh_token` silent refresh first, if that fails then guide to re-login.

## MCP Tool Call Conventions

### 1. `wallet.get_token_list` (cross-Skill call) — Query balance for verification

**Must** call this tool before transfer to verify sender token balance and Gas token balance. This tool belongs to `gate-dex-mcpwallet` domain, called cross-Skill here.

| Field | Description |
|-------|-------------|
| **Tool name** | `wallet.get_token_list` |
| **Parameters** | `{ account_id: string, chain: string, mcp_token: string }` |
| **Returns** | Token array, each with `symbol`, `balance`, `price`, `value`, `chain`, `contract_address`, etc. |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="wallet.get_token_list",
  arguments={ account_id: "acc_12345", chain: "eth", mcp_token: "<mcp_token>" }
)
```

Agent behavior: Extract transfer token balance and chain native token balance (for Gas) from the returned list for subsequent balance verification.

---

### 2. `tx.gas` — Estimate Gas fee

Estimate Gas fee for a transaction on the specified chain. Returns gas price and estimated consumption.

| Field | Description |
|-------|-------------|
| **Tool name** | `tx.gas` |
| **Parameters** | `{ chain: string, from_address: string, to_address: string, value?: string, data?: string, mcp_token: string }` |
| **Returns** | `{ gas_limit: string, gas_price: string, estimated_fee: string, fee_usd: number }` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier (e.g. `"eth"`, `"bsc"`, `"sol"`) |
| `from_address` | Yes | Sender address |
| `to_address` | Yes | Recipient address |
| `value` | No | Native token transfer amount (wei / lamports format). Can be `"0"` for ERC20 transfer |
| `data` | No | Transaction data (transfer calldata for ERC20 transfer) |
| `mcp_token` | Yes | Auth token |

Call example (native token transfer):

```
CallMcpTool(
  server="gate-wallet",
  toolName="tx.gas",
  arguments={
    chain: "eth",
    from_address: "0xABCdef1234567890ABCdef1234567890ABCdef12",
    to_address: "0xDEF4567890ABCdef1234567890ABCdef12345678",
    value: "1000000000000000000",
    mcp_token: "<mcp_token>"
  }
)
```

Return example:

```json
{
  "gas_limit": "21000",
  "gas_price": "30000000000",
  "estimated_fee": "0.00063",
  "fee_usd": 1.21
}
```

Call example (ERC20 token transfer):

```
CallMcpTool(
  server="gate-wallet",
  toolName="tx.gas",
  arguments={
    chain: "eth",
    from_address: "0xABCdef1234567890ABCdef1234567890ABCdef12",
    to_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    value: "0",
    data: "0xa9059cbb000000000000000000000000DEF4567890ABCdef1234567890ABCdef123456780000000000000000000000000000000000000000000000000000000077359400",
    mcp_token: "<mcp_token>"
  }
)
```

Agent behavior: Solana chain has different Gas structure (fee in lamports). Parameters and return fields may differ; handle according to actual response.

---

### 3. `tx.transfer_preview` — Build transaction preview

Build unsigned transaction and return confirmation summary, including server `confirm_message`. This is the final preview step before signing.

| Field | Description |
|-------|-------------|
| **Tool name** | `tx.transfer_preview` |
| **Parameters** | `{ chain: string, from_address: string, to_address: string, token_address: string, amount: string, account_id: string, mcp_token: string }` |
| **Returns** | `{ raw_tx: string, confirm_message: string, estimated_gas: string, nonce: number }` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier |
| `from_address` | Yes | Sender address |
| `to_address` | Yes | Recipient address |
| `token_address` | Yes | Token contract address. Use `"native"` for native token |
| `amount` | Yes | Transfer amount (human-readable format, e.g. `"1.5"` not wei) |
| `account_id` | Yes | User account ID |
| `mcp_token` | Yes | Auth token |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="tx.transfer_preview",
  arguments={
    chain: "eth",
    from_address: "0xABCdef1234567890ABCdef1234567890ABCdef12",
    to_address: "0xDEF4567890ABCdef1234567890ABCdef12345678",
    token_address: "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    amount: "1000",
    account_id: "acc_12345",
    mcp_token: "<mcp_token>"
  }
)
```

Return example:

```json
{
  "raw_tx": "0x02f8...",
  "confirm_message": "Transfer 1000 USDT to 0xDEF4...5678 on Ethereum",
  "estimated_gas": "0.003",
  "nonce": 42
}
```

Agent behavior: After obtaining `raw_tx`, **do not sign directly**. Must show confirmation summary to user and wait for explicit confirmation first.

---

### 4. `wallet.sign_transaction` — Server-side signing

Sign unsigned transaction using server-hosted private key. **Only call after user explicitly confirms.**

| Field | Description |
|-------|-------------|
| **Tool name** | `wallet.sign_transaction` |
| **Parameters** | `{ raw_tx: string, chain: string, account_id: string, mcp_token: string }` |
| **Returns** | `{ signed_tx: string }` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `raw_tx` | Yes | Unsigned transaction from `tx.transfer_preview` |
| `chain` | Yes | Chain identifier |
| `account_id` | Yes | User account ID |
| `mcp_token` | Yes | Auth token |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="wallet.sign_transaction",
  arguments={
    raw_tx: "0x02f8...",
    chain: "eth",
    account_id: "acc_12345",
    mcp_token: "<mcp_token>"
  }
)
```

Return example:

```json
{
  "signed_tx": "0x02f8b2...signed..."
}
```

---

### 5. `tx.send_raw_transaction` — Broadcast signed transaction

Broadcast the signed transaction to the chain network.

| Field | Description |
|-------|-------------|
| **Tool name** | `tx.send_raw_transaction` |
| **Parameters** | `{ signed_tx: string, chain: string, mcp_token: string }` |
| **Returns** | `{ hash_id: string }` |

Parameter details:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `signed_tx` | Yes | Signed transaction from `wallet.sign_transaction` |
| `chain` | Yes | Chain identifier |
| `mcp_token` | Yes | Auth token |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="tx.send_raw_transaction",
  arguments={
    signed_tx: "0x02f8b2...signed...",
    chain: "eth",
    mcp_token: "<mcp_token>"
  }
)
```

Return example:

```json
{
  "hash_id": "0xa1b2c3d4e5f6...7890"
}
```

Agent behavior: After successful broadcast, show transaction hash to user and provide block explorer link.

## Supported Chains

| Chain ID | Network Name | Type | Native Gas Token | Block Explorer |
|----------|--------------|------|------------------|----------------|
| `eth` | Ethereum | EVM | ETH | etherscan.io |
| `bsc` | BNB Smart Chain | EVM | BNB | bscscan.com |
| `polygon` | Polygon | EVM | MATIC | polygonscan.com |
| `arbitrum` | Arbitrum One | EVM | ETH | arbiscan.io |
| `optimism` | Optimism | EVM | ETH | optimistic.etherscan.io |
| `avax` | Avalanche C-Chain | EVM | AVAX | snowtrace.io |
| `base` | Base | EVM | ETH | basescan.org |
| `sol` | Solana | Non-EVM | SOL | solscan.io |

## MCP Tool Call Chain Overview

The full transfer flow calls the following tools in sequence, forming a strict linear pipeline:

```
0. chain.config                         ← Step 0: MCP Server pre-check
1. wallet.get_token_list                ← Cross-Skill: query balance (token + Gas token)
2. tx.gas                               ← Estimate Gas fee
3. [Agent balance check: balance >= amount + Gas]  ← Agent internal logic, not MCP call
4. tx.transfer_preview                  ← Build unsigned tx + server confirm info
5. [Agent show confirmation summary, wait for user confirm]  ← Mandatory gate, not MCP call
6. wallet.sign_transaction              ← Sign after user confirms
7. tx.send_raw_transaction              ← Broadcast to chain
```

## Skill Routing

Based on user intent after transfer completes, route to the corresponding Skill:

| User Intent | Route Target |
|-------------|--------------|
| View updated balance | `gate-dex-mcpwallet` |
| View transaction details / history | `gate-dex-mcpwallet` (`tx.detail`, `tx.list`) |
| Continue transfer to another address | Stay in this Skill |
| Swap tokens | `gate-dex-mcpswap` |
| Login / auth expired | `gate-dex-mcpauth` |

## Operation Flow

### Flow A: Standard Transfer (Main Flow)

```
Step 0: MCP Server pre-check
  Call chain.config({chain: "eth"}) to probe availability
  ↓ Success

Step 1: Auth check
  Confirm valid mcp_token and account_id
  No token → Guide to gate-dex-mcpauth login
  ↓

Step 2: Intent recognition + parameter collection
  Extract transfer intent from user input, collect required parameters:
  - to_address: Recipient address (required)
  - amount: Transfer amount (required)
  - token: Transfer token (required, e.g. ETH, USDT)
  - chain: Target chain (optional, can infer from token or context)

  When parameters missing, ask user one by one:

  ────────────────────────────
  Please provide transfer info:
  - Recipient address: (required, full address)
  - Amount: (required, e.g. 1.5)
  - Token: (required, e.g. ETH, USDT)
  - Chain: (optional, default Ethereum. Supports eth/bsc/polygon/arbitrum/optimism/avax/base/sol)
  ────────────────────────────

  ↓ Parameters complete

Step 3: Get wallet address
  Call wallet.get_addresses({ account_id, mcp_token })
  Extract from_address for target chain
  ↓

Step 4: Query balance (cross-Skill: gate-dex-mcpwallet)
  Call wallet.get_token_list({ account_id, chain, mcp_token })
  Extract:
  - Transfer token balance (e.g. USDT balance)
  - Chain native Gas token balance (e.g. ETH balance)
  ↓

Step 5: Estimate Gas fee
  Call tx.gas({ chain, from_address, to_address, value?, data?, mcp_token })
  Get estimated_fee (in native token) and fee_usd
  ↓

Step 6: Agent balance verification (mandatory)
  Verification rules:
  a) Native token transfer: balance >= amount + estimated_fee
  b) ERC20 token transfer: token_balance >= amount AND native_balance >= estimated_fee
  c) Solana SPL token transfer: token_balance >= amount AND sol_balance >= estimated_fee

  Verification failed → Abort transaction, show insufficient info:

  ────────────────────────────
  ❌ Insufficient balance, cannot execute transfer

  Transfer amount: 1000 USDT
  Current USDT balance: 800 USDT (insufficient, short by 200 USDT)

  Or:

  Transfer amount: 1.0 ETH
  Estimated Gas: 0.003 ETH
  Total required: 1.003 ETH
  Current ETH balance: 0.9 ETH (insufficient, short by 0.103 ETH)

  Suggestions:
  - Reduce transfer amount
  - Deposit tokens to wallet first
  ────────────────────────────

  ↓ Verification passed

Step 7: Build transaction preview
  Call tx.transfer_preview({ chain, from_address, to_address, token_address, amount, account_id, mcp_token })
  Get raw_tx and confirm_message
  ↓

Step 8: Show confirmation summary (mandatory gate)
  Must show full confirmation info to user and wait for explicit "confirm" before proceeding.
  Display content see "Transaction Confirmation Template" below.
  ↓

  User replies "confirm" → Proceed to Step 9
  User replies "cancel" → Abort transaction, show cancel message
  User requests changes → Return to Step 2 to re-collect parameters

Step 9: Sign transaction
  Call wallet.sign_transaction({ raw_tx, chain, account_id, mcp_token })
  Get signed_tx
  ↓

Step 10: Broadcast transaction
  Call tx.send_raw_transaction({ signed_tx, chain, mcp_token })
  Get hash_id
  ↓

Step 11: Show result + follow-up suggestions

  ────────────────────────────
  ✅ Transfer broadcast successful!

  Transaction Hash: {hash_id}
  Block Explorer: https://{explorer}/tx/{hash_id}

  Transaction submitted to network. Confirmation time depends on network congestion.

  You can:
  - View updated balance
  - View transaction details
  - Continue other operations
  ────────────────────────────
```

### Flow B: Batch Transfer

```
Step 0: MCP Server pre-check
  ↓ Success

Step 1-2: Auth + parameter collection
  Identify multiple transfer intents, collect to_address, amount, token, chain for each
  ↓

Step 3-8: Execute each transfer separately
  Each transfer runs Step 3 ~ Step 8 independently (query balance → Gas → verify → preview → confirm)
  Show confirmation summary for each transfer, confirm one by one:

  ────────────────────────────
  📦 Batch transfer (1/3)

  [Show this transaction confirmation summary]

  Reply "confirm" to execute this one, "skip" to skip this one, "cancel all" to abort remaining.
  ────────────────────────────

  ↓ User confirms one by one

Step 9-10: Sign + broadcast each (only for confirmed ones)
  ↓

Step 11: Summary result

  ────────────────────────────
  📦 Batch transfer result

  | # | Recipient | Amount | Status | Hash |
  |---|-----------|--------|--------|------|
  | 1 | 0xDEF...5678 | 100 USDT | ✅ Success | 0xa1b2... |
  | 2 | 0x123...ABCD | 200 USDT | ✅ Success | 0xc3d4... |
  | 3 | 0x456...EF01 | 50 USDT  | ⏭ Skipped | — |

  Success: 2/3
  ────────────────────────────
```

## Transaction Confirmation Template

**Agent must NOT execute signing until user explicitly replies "confirm". This is a mandatory gate that cannot be skipped.**

### Native Token Transfer Confirmation

```
========== Transaction Confirmation ==========
Chain: {chain_name} (e.g. Ethereum)
Type: Native token transfer
Sender: {from_address}
Recipient: {to_address}
Amount: {amount} {symbol} (e.g. 1.5 ETH)
---------- Balance Info ----------
{symbol} balance: {balance} {symbol} (sufficient ✅)
---------- Fee Info ----------
Estimated Gas: {estimated_fee} {gas_symbol} (≈ ${fee_usd})
Remaining after transfer: {remaining_balance} {symbol}
---------- Server Confirmation ----------
{confirm_message from tx.transfer_preview}
===============================
Reply "confirm" to execute, "cancel" to abort, or specify changes.
```

### ERC20 / SPL Token Transfer Confirmation

```
========== Transaction Confirmation ==========
Chain: {chain_name} (e.g. Ethereum)
Type: ERC20 token transfer
Sender: {from_address}
Recipient: {to_address}
Amount: {amount} {token_symbol} (e.g. 1000 USDT)
Token contract: {token_address}
---------- Balance Info ----------
{token_symbol} balance: {token_balance} {token_symbol} (sufficient ✅)
{gas_symbol} balance (Gas): {gas_balance} {gas_symbol} (sufficient ✅)
---------- Fee Info ----------
Estimated Gas: {estimated_fee} {gas_symbol} (≈ ${fee_usd})
Remaining after transfer: {remaining_token} {token_symbol} / {remaining_gas} {gas_symbol}
---------- Server Confirmation ----------
{confirm_message from tx.transfer_preview}
===============================
Reply "confirm" to execute, "cancel" to abort, or specify changes.
```

## Cross-Skill Workflow

### Full Transfer Flow (from login to completion)

```
gate-dex-mcpauth (login, get mcp_token + account_id)
  → gate-dex-mcpwallet (wallet.get_token_list → verify balance)
    → gate-dex-mcpwallet (wallet.get_addresses → get sender address)
      → gate-dex-mcptransfer (tx.gas → tx.transfer_preview → confirm → sign → broadcast)
        → gate-dex-mcpwallet (view updated balance)
```

### Invoked by Other Skills

| Source Skill | Scenario | Notes |
|--------------|----------|-------|
| `gate-dex-mcpwallet` | User wants to transfer after viewing balance | Carries account_id, chain, from_address |
| `gate-dex-mcpswap` | User wants to transfer out tokens after Swap | Has chain and token context |
| `gate-dex-mcpdapp` | Tokens from DApp operation need to be transferred out | Has chain and address context |

### Calling Other Skills

| Target Skill | Call Scenario | Tools Used |
|--------------|---------------|------------|
| `gate-dex-mcpwallet` | Query balance before transfer | `wallet.get_token_list` |
| `gate-dex-mcpwallet` | Get sender address before transfer | `wallet.get_addresses` |
| `gate-dex-mcpwallet` | View updated balance after transfer | `wallet.get_token_list` |
| `gate-dex-mcpauth` | Not logged in or token expired | `auth.refresh_token` or full login flow |
| `gate-dex-mcpwallet` | View transaction details after transfer | `tx.detail`, `tx.list` |

## Address Validation Rules

Before initiating transfer, Agent must validate recipient address format:

| Chain Type | Format | Validation Rule |
|------------|--------|-----------------|
| EVM (eth/bsc/polygon/...) | `0x` prefix, 40 hex chars (42 total) | Regex `^0x[0-9a-fA-F]{40}$`, recommend EIP-55 checksum validation |
| Solana | Base58, 32-44 chars | Regex `^[1-9A-HJ-NP-Za-km-z]{32,44}$` |

When validation fails:

```
❌ Invalid recipient address format

Provided address: {user_input}
Expected format: {expected_format}

Please check the address is correct, complete, and matches the target chain.
```

## Edge Cases and Error Handling

| Scenario | Handling |
|----------|----------|
| MCP Server not configured | Abort all operations, show Cursor config guide |
| MCP Server unreachable | Abort all operations, show network check prompt |
| Not logged in (no `mcp_token`) | Guide to `gate-dex-mcpauth` to complete login, then return to continue transfer |
| `mcp_token` expired | Try `auth.refresh_token` silent refresh first, if fails guide to re-login |
| Insufficient transfer token balance | Abort transaction, show current balance vs required amount shortfall, suggest reducing amount or depositing first |
| Insufficient Gas token balance | Abort transaction, show Gas token insufficient info, suggest obtaining Gas token first |
| Invalid recipient address format | Reject transaction, prompt correct address format |
| Recipient same as sender | Warn user and confirm if intentional to avoid mistakes |
| `tx.gas` estimation failed | Show error message. Possible causes: network congestion, contract call exception. Suggest retry later |
| `tx.transfer_preview` failed | Show server error message, do not retry silently |
| `wallet.sign_transaction` failed | Show signing error. Possible causes: account permission, server exception. Do not auto-retry |
| `tx.send_raw_transaction` failed | Show broadcast error (e.g. nonce conflict, insufficient gas, network congestion). Suggest actions based on error type |
| User cancels confirmation | Abort immediately, do not sign or broadcast. Show cancel message, stay friendly |
| Amount exceeds token precision | Prompt token precision limit, auto-truncate or ask user to correct |
| Transfer amount 0 or negative | Reject, prompt for valid positive amount |
| Unsupported chain identifier | Show supported chain list, ask user to re-select |
| Target chain and token mismatch | Prompt token does not exist on target chain, suggest correct chain |
| Broadcast success but tx not confirmed for long time | Inform user tx submitted, confirmation time depends on network, can track via block explorer |
| Network interruption | Show network error, suggest check network and retry. If network lost after sign but before broadcast, note signed tx can be broadcast later |
| One transfer fails in batch | Mark that transfer as failed, continue remaining, show per-transfer result summary at end |

## Security Rules

1. **`mcp_token` confidentiality**: Never show `mcp_token` in plain text to user. Use placeholder `<mcp_token>` in examples.
2. **`account_id` masking**: When showing to user, only display partial chars (e.g. `acc_12...89`).
3. **Token auto-refresh**: When `mcp_token` expired, try silent refresh first; only require re-login if that fails.
4. **Mandatory balance verification**: **Must** verify balance (token + Gas) before each transfer. **Prohibit** signing and broadcast when insufficient.
5. **Mandatory user confirmation**: **Must** show full confirmation summary and get explicit "confirm" before signing. Cannot skip, simplify, or auto-confirm.
6. **Batch per-transfer confirmation**: For batch transfers, show confirmation summary for each transfer and wait for user confirmation one by one.
7. **No auto-retry on failed transactions**: After sign or broadcast failure, show error clearly to user. Do not retry in background.
8. **Address validation**: Validate recipient address format before sending to prevent asset loss from wrong address.
9. **Prohibit operations when MCP Server not configured or unreachable**: Abort all subsequent steps if Step 0 connection check fails.
10. **MCP Server errors transparent**: Show all MCP Server error messages to user as-is. Do not hide or alter.
11. **`raw_tx` must not leak**: Unsigned transaction raw data only flows between Agent and MCP Server. Do not show hex to user.
12. **Broadcast promptly after signing**: After successful sign, broadcast immediately. Do not hold signed transaction for long.
