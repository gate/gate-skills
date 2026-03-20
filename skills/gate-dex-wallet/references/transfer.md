---
name: gate-dex-wallet-transfer
version: "2026.3.12-1"
updated: "2026-03-12"
description: "Gate Wallet transfer execution. Build transactions, sign, broadcast. Use when users want to 'send ETH', 'transfer USDT', 'transfer', 'send tokens'. Includes mandatory balance verification and user confirmation gate. Supports EVM multi-chain + Solana native/token transfers."
---

# Gate DEX Transfer

> Transfer domain — Gas estimation, transaction preview, balance verification, signing, broadcasting, includes mandatory user confirmation gates. 4 MCP tools + 1 cross-Skill call.

**Trigger scenarios**: Users mention "transfer", "send", "transfer", "send ETH", "send tokens", "send coins", "withdraw", or when other Skills guide users to perform on-chain transfer operations.

**Prerequisites**: MCP Server available (see parent SKILL.md for detection). If not configured, see parent SKILL.md for setup guide.

## Authentication Notes

All operations in this Skill **require `mcp_token`**. Before calling any tool, must confirm user is logged in.

- If currently no `mcp_token` → Guide to `gate-dex-wallet/references/auth.md` to complete login then return.
- If `mcp_token` expired (MCP Server returns token expiration error) → Try `dex_auth_refresh_token` silent refresh first, guide to re-login if failed.

## MCP Tool Call Specifications

### 1. `dex_wallet_get_token_list` (Cross-Skill Call) — Query Balance for Verification

Before transfer **must** call this tool first to verify sending token balance and Gas token balance. This tool belongs to `gate-dex-wallet` domain, called cross-Skill here.

| Field | Description |
|-------|-------------|
| **Tool Name** | `dex_wallet_get_token_list` |
| **Parameters** | `{ account_id: string, chain: string, mcp_token: string }` |
| **Return Value** | Token array, each item contains `symbol`, `balance`, `price`, `value`, `chain`, `contract_address`, etc. For correct amounts use **`orignCoinNumber`** from the API item; avoid **`coinNumber`** for balance math (may be display-formatted). |

Call example:

```
CallMcpTool(
  server="gate-dex",
  toolName="dex_wallet_get_token_list",
  arguments={ account_id: "acc_12345", chain: "eth", mcp_token: "<mcp_token>" }
)
```

Agent behavior: Extract transfer token balance and chain native token balance (for Gas) from returned list to prepare for subsequent balance verification.

---

### 2. `tx.gas` — Estimate Gas Fees

Estimate Gas fees for transactions on specified chain, returns gas price and estimated consumption.

| Field | Description |
|-------|-------------|
| **Tool Name** | `tx.gas` |
| **Parameters** | `{ chain: string, from_address: string, to_address: string, value?: string, data?: string, mcp_token: string }` |
| **Return Value** | `{ gas_limit: string, gas_price: string, estimated_fee: string, fee_usd: number }` |

Parameter descriptions:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier (e.g. `"eth"`, `"bsc"`, `"sol"`) |
| `from_address` | Yes | Sender address |
| `to_address` | Yes | Recipient address |
| `value` | No | Native token transfer amount (wei / lamports format). ERC20 transfers can be `"0"` |
| `data` | No | Transaction data (transfer calldata for ERC20 transfers) |
| `mcp_token` | Yes | Authentication token |

Call example (native token transfer):

```
CallMcpTool(
  server="gate-dex",
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
  server="gate-dex",
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

Agent behavior: Solana chain's Gas structure differs (fee in lamports), parameters and return fields may vary, handle according to actual returns.

---

### 3. `tx.transfer_preview` — Build Transaction Preview

Build unsigned transaction and return confirmation summary, includes server-side `confirm_message`. This is the final preview step before signing.

| Field | Description |
|-------|-------------|
| **Tool Name** | `tx.transfer_preview` |
| **Parameters** | `{ chain: string, from_address: string, to_address: string, token_address: string, amount: string, account_id: string, mcp_token: string }` |
| **Return Value** | `{ raw_tx: string, confirm_message: string, estimated_gas: string, nonce: number }` |

Parameter descriptions:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier |
| `from_address` | Yes | Sender address |
| `to_address` | Yes | Recipient address |
| `token_address` | Yes | Token contract address. Use `"native"` for native tokens |
| `amount` | Yes | Transfer amount (human-readable format, e.g. `"1.5"` not wei) |
| `account_id` | Yes | User account ID |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-dex",
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

Agent behavior: After getting `raw_tx`, **must not sign directly**, must first display confirmation summary to user and wait for explicit confirmation.

---

### 4. `wallet.sign_transaction` — Server-side Signing

Use server-side custodial private keys to sign unsigned transactions. **Only call after explicit user confirmation**.

| Field | Description |
|-------|-------------|
| **Tool Name** | `wallet.sign_transaction` |
| **Parameters** | `{ raw_tx: string, chain: string, account_id: string, mcp_token: string }` |
| **Return Value** | `{ signed_tx: string }` |

Parameter descriptions:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `raw_tx` | Yes | Unsigned transaction from `tx.transfer_preview` |
| `chain` | Yes | Chain identifier |
| `account_id` | Yes | User account ID |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-dex",
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

### 5. `dex_tx_send_raw_transaction` — Broadcast Signed Transaction

Broadcast signed transaction to on-chain network.

| Field | Description |
|-------|-------------|
| **Tool Name** | `dex_tx_send_raw_transaction` |
| **Parameters** | `{ signed_tx: string, chain: string, mcp_token: string }` |
| **Return Value** | `{ hash_id: string }` |

Parameter descriptions:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `signed_tx` | Yes | Signed transaction from `wallet.sign_transaction` |
| `chain` | Yes | Chain identifier |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-dex",
  toolName="dex_tx_send_raw_transaction",
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

Agent behavior: After successful broadcast, display transaction hash to user and provide block explorer link.

Supported chains: eth, bsc, polygon, arbitrum, optimism, avax, base, sol. See parent SKILL.md.

## MCP Tool Call Chain Overview

Complete transfer flow calls the following tools in sequence, forming a strict linear pipeline:

```
0. dex_chain_config                         ← First session detection (if needed)
1. dex_wallet_get_token_list                ← Cross-Skill: Query balance (token + Gas token)
2. tx.gas                               ← Estimate Gas fees
3. [Agent balance validation: balance >= amount + Gas]  ← Agent internal logic, not MCP call
4. tx.transfer_preview                  ← Build unsigned transaction + server confirmation info
5. [Agent display confirmation summary, wait for user confirmation]     ← Mandatory gate, not MCP call
6. wallet.sign_transaction              ← Sign after user confirmation
7. dex_tx_send_raw_transaction              ← Broadcast on-chain
```

## Skill Routing

Based on user intent after transfer completion, guide to corresponding Skill:

| User Intent | Route Target |
|-------------|-------------|
| View updated balance | `gate-dex-wallet` |
| View transaction details / history | `gate-dex-wallet` (`dex_tx_detail`, `dex_tx_list`) |
| Continue transfer to other addresses | Stay in this Skill |
| Swap tokens | `gate-dex-trade` |
| Login / authentication expired | `gate-dex-wallet/references/auth.md` |

## Operation Flow

### Flow A: Standard Transfer (Main Flow)

```
First session detection (if needed)
  Call dex_chain_config({chain: "eth"}) to probe availability
  ↓ Success

Step 1: Authentication Check
  Confirm valid mcp_token and account_id
  No token → Guide to gate-dex-wallet/references/auth.md login
  ↓

Step 2: Intent Recognition + Parameter Collection
  Extract transfer intent from user input, collect necessary parameters:
  - to_address: Recipient address (required)
  - amount: Transfer amount (required)
  - token: Transfer token (required, e.g. ETH, USDT)
  - chain: Target chain (optional, infer from token or context)

  When parameters missing, ask user item by item:

  ────────────────────────────
  Please provide transfer information:
  - Recipient address: (required, provide complete address)
  - Transfer amount: (required, e.g. 1.5)
  - Token: (required, e.g. ETH, USDT)
  - Chain: (optional, default Ethereum. Supports eth/bsc/polygon/arbitrum/optimism/avax/base/sol)
  ────────────────────────────

  ↓ Parameters complete

Step 3: Get Wallet Address
  Call dex_wallet_get_addresses({ account_id, mcp_token })
  Extract target chain's from_address
  ↓

Step 4: Query Balance (Cross-Skill: gate-dex-wallet)
  Call dex_wallet_get_token_list({ account_id, chain, mcp_token })
  Extract:
  - Transfer token balance (e.g. USDT balance)
  - Chain native Gas token balance (e.g. ETH balance)
  ↓

Step 5: Estimate Gas Fees
  Call tx.gas({ chain, from_address, to_address, value?, data?, mcp_token })
  Get estimated_fee (native token pricing) and fee_usd
  ↓

Step 6: Agent Balance Validation (Mandatory)
  Validation rules:
  a) Native token transfer: balance >= amount + estimated_fee
  b) ERC20 token transfer: token_balance >= amount AND native_balance >= estimated_fee
  c) Solana SPL token transfer: token_balance >= amount AND sol_balance >= estimated_fee

  Validation failed → Abort transaction, display insufficient info:

  ────────────────────────────
  ❌ Insufficient balance, cannot execute transfer

  Transfer amount: 1000 USDT
  Current USDT balance: 800 USDT (insufficient, short 200 USDT)

  Or:

  Transfer amount: 1.0 ETH
  Estimated Gas: 0.003 ETH
  Total needed: 1.003 ETH
  Current ETH balance: 0.9 ETH (insufficient, short 0.103 ETH)

  Suggestions:
  - Reduce transfer amount
  - Top up tokens to wallet first
  ────────────────────────────

  ↓ Validation passed

Step 7: Build Transaction Preview
  Call tx.transfer_preview({ chain, from_address, to_address, token_address, amount, account_id, mcp_token })
  Get raw_tx and confirm_message
  ↓

Step 8: Display Confirmation Summary (Mandatory Gate)
  Must display complete confirmation information to user and wait for explicit "confirm" reply before continuing.
  Display content per "Transaction Confirmation Template" below.
  ↓

  User replies "confirm" → Continue Step 9
  User replies "cancel" → Abort transaction, display cancellation notice
  User requests modification → Return to Step 2 to re-collect modified parameters

Step 9: Sign Transaction
  Call wallet.sign_transaction({ raw_tx, chain, account_id, mcp_token })
  Get signed_tx
  ↓

Step 10: Broadcast Transaction
  Call dex_tx_send_raw_transaction({ signed_tx, chain, mcp_token })
  Get hash_id
  ↓

Step 11: Display Result + Follow-up Suggestions

  ────────────────────────────
  ✅ Transfer broadcast successful!

  Transaction Hash: {hash_id}
  Block Explorer: https://{explorer}/tx/{hash_id}

  Transaction submitted to network, confirmation time depends on network congestion.

  You can:
  - View updated balance
  - View transaction details
  - Continue other operations
  ────────────────────────────
```

### Flow B: Batch Transfer

```
First session detection (if needed)
  ↓ Success

Step 1-2: Authentication + Parameter Collection
  Identify multiple transfer intents, collect to_address, amount, token, chain for each transfer
  ↓

Step 3-8: Execute individually for each transfer
  Each transfer independently goes through Step 3 ~ Step 8 (check balance → Gas → validate → preview → confirm)
  Display confirmation summary for each transfer individually, confirm one by one:

  ────────────────────────────
  📦 Batch Transfer (1/3 transfers)

  [Display confirmation summary for this transaction]

  Reply "confirm" to execute this one, "skip" to skip this one, "cancel all" to abort remaining transfers.
  ────────────────────────────

  ↓ User confirms one by one

Step 9-10: Sign + Broadcast individually (only for confirmed transfers)
  ↓

Step 11: Summary Results

  ────────────────────────────
  📦 Batch Transfer Results

  | # | Recipient Address | Amount | Status | Hash |
  |---|-------------------|--------|--------|------|
  | 1 | 0xDEF...5678 | 100 USDT | ✅ Success | 0xa1b2... |
  | 2 | 0x123...ABCD | 200 USDT | ✅ Success | 0xc3d4... |
  | 3 | 0x456...EF01 | 50 USDT  | ⏭ Skipped | — |

  Successful: 2/3 transfers
  ────────────────────────────
```

## Transaction Confirmation Template

**This confirmation summary is mandatory gate - Agent must not execute signing before user explicitly replies "confirm". This cannot be skipped.**

### Native Token Transfer Confirmation

```
========== Transaction Confirmation ==========
Chain: {chain_name} (e.g. Ethereum)
Type: Native token transfer
Sender Address: {from_address}
Recipient Address: {to_address}
Transfer Amount: {amount} {symbol} (e.g. 1.5 ETH)
---------- Balance Info ----------
{symbol} Balance: {balance} {symbol} (Sufficient ✅)
---------- Fee Info ----------
Estimated Gas: {estimated_fee} {gas_symbol} (≈ ${fee_usd})
Remaining After Transfer: {remaining_balance} {symbol}
---------- Server Confirmation ----------
{confirm_message from tx.transfer_preview}
===============================
Reply "confirm" to execute, "cancel" to abort, or tell me what to modify.
```

### ERC20 / SPL Token Transfer Confirmation

```
========== Transaction Confirmation ==========
Chain: {chain_name} (e.g. Ethereum)
Type: ERC20 token transfer
Sender Address: {from_address}
Recipient Address: {to_address}
Transfer Amount: {amount} {token_symbol} (e.g. 1000 USDT)
Token Contract: {token_address}
---------- Balance Info ----------
{token_symbol} Balance: {token_balance} {token_symbol} (Sufficient ✅)
{gas_symbol} Balance (Gas): {gas_balance} {gas_symbol} (Sufficient ✅)
---------- Fee Info ----------
Estimated Gas: {estimated_fee} {gas_symbol} (≈ ${fee_usd})
Remaining After Transfer: {remaining_token} {token_symbol} / {remaining_gas} {gas_symbol}
---------- Server Confirmation ----------
{confirm_message from tx.transfer_preview}
===============================
Reply "confirm" to execute, "cancel" to abort, or tell me what to modify.
```


## Address Validation Rules

Before initiating transfer, Agent must validate recipient address format:

| Chain Type | Format Requirements | Validation Rules |
|-----------|---------------------|------------------|
| EVM (eth/bsc/polygon/...) | Starts with `0x`, 40 hex characters (42 total) | Regex `^0x[0-9a-fA-F]{40}$`, recommend EIP-55 checksum validation |
| Solana | Base58 encoded, 32-44 characters | Regex `^[1-9A-HJ-NP-Za-km-z]{32,44}$` |

When validation fails:

```
❌ Invalid recipient address format

Provided address: {user_input}
Expected format: {expected_format}

Please check if the address is correct, complete, and matches the target chain.
```

## Edge Cases and Error Handling

| Scenario | Handling |
|----------|----------|
| Transfer token balance insufficient | Abort transaction, display current balance vs required amount difference, suggest reducing amount or topping up first |
| Gas token balance insufficient | Abort transaction, display Gas token insufficient info, suggest getting Gas tokens first |
| Invalid recipient address format | Refuse to initiate transaction, prompt correct address format |
| Recipient address same as sender address | Warn user and confirm if intentional operation, avoid mistakes |
| `tx.gas` estimation failed | Display error info, possible causes: network congestion, contract call exception. Suggest retry later |
| `tx.transfer_preview` failed | Display server-returned error message, do not silently retry |
| `wallet.sign_transaction` failed | Display signing error, possible causes: account permissions, server exception. Do not auto-retry |
| `dex_tx_send_raw_transaction` failed | Display broadcast error (e.g. nonce conflict, insufficient gas, network congestion), suggest appropriate measures based on error type |
| User cancels confirmation | Immediately abort, do not execute signing and broadcast. Display cancellation notice, stay friendly |
| Amount exceeds token precision | Prompt token precision limitation, auto-truncate or ask user to correct |
| Transfer amount is 0 or negative | Refuse to execute, prompt to input valid positive amount |
| Token doesn't match target chain | Prompt token doesn't exist on target chain, suggest correct chain |
| Broadcast successful but transaction unconfirmed for long time | Tell user transaction submitted, confirmation time depends on network conditions, can track via block explorer |
| Some transfers fail in batch transfer | Mark those as failed, continue processing subsequent transfers, finally display summary results for each transfer |

## Safety Rules

1. **`mcp_token` confidentiality**: Never display `mcp_token` in plaintext to users, only use placeholders like `<mcp_token>` in call examples.
2. **`account_id` masking**: When displaying to users, only show partial characters (e.g. `acc_12...89`).
3. **Auto token refresh**: When `mcp_token` expires, prioritize silent refresh, only require re-login if refresh fails.
4. **Mandatory balance validation**: Before each transfer **must** validate balance (token + Gas), **prohibit** initiating signing and broadcasting when balance insufficient.
5. **Mandatory user confirmation**: Before signing **must** display complete confirmation summary to users and get explicit "confirm" reply. Cannot skip, simplify or auto-confirm.
6. **Individual confirmation for batches**: For batch transfers, each transaction displays confirmation summary individually, wait for user confirmation one by one.
7. **No auto-retry failed transactions**: After signing or broadcasting failures, clearly display error messages to users, don't auto-retry in background.
8. **Address validation**: Validate recipient address format before sending to prevent asset loss due to incorrect addresses.
9. **Prohibit operations when MCP Server not configured or unreachable**: If Step 0 connection detection fails, abort all subsequent steps.
10. **Transparent MCP Server errors**: All error messages returned by MCP Server should be displayed to users truthfully, without hiding or tampering.
11. **`raw_tx` confidentiality**: Unsigned transaction raw data should only flow between Agent and MCP Server, do not display hex raw content to users.
12. **Broadcast immediately after signing**: After successful signing, should broadcast immediately, should not hold signed transactions for long periods.