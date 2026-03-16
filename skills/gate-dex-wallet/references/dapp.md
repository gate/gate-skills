---
name: gate-dex-dapp
version: "2026.3.12-1"
updated: "2026-03-12"
description: "Gate Wallet interaction with external DApps. Connect wallet, sign messages (EIP-712/personal_sign), sign and send DApp-generated transactions, ERC20 Approve authorization. Use when users need to interact with DeFi protocols, NFT platforms, or any DApp. Includes transaction confirmation gate and security review."
---

# Gate DEX DApp

> DApp interaction domain — connect wallet, sign messages, execute DApp transactions, ERC20 Approve authorization, includes mandatory confirmation gates and contract security review. 4 MCP tools + cross-Skill calls.

**Trigger scenarios**: Users mention "connect DApp", "sign message", "authorization", "approve", "DApp interaction", "NFT mint", "DeFi operations", "add liquidity", "staking", "stake", "claim", "contract calls", or when other Skills guide users to perform DApp-related operations.

## MCP Server Connection Detection

### First Session Detection

**Before the first MCP tool call in a session, perform one connection probe to confirm Gate DEX MCP Server availability. Subsequent operations do not need repeated detection.**

```
CallMcpTool(server="gate-dex", toolName="chain.config", arguments={chain: "eth"})
```

| Result | Handling |
|--------|----------|
| Success | MCP Server available, subsequent operations directly call business tools without re-probing |
| Failure | Display configuration guidance based on error type (see error handling below) |

### Runtime Error Fallback

If business tool calls fail during subsequent operations (returning connection errors, timeouts, etc.), handle according to the following rules:

| Error Type | Keywords | Handling |
|------------|----------|----------|
| MCP Server not configured | `server not found`, `unknown server` | Display MCP Server configuration guidance |
| Remote service unreachable | `connection refused`, `timeout`, `DNS error` | Prompt to check server status and network connection |
| Authentication failed | `401`, `unauthorized` | Prompt to contact administrator for authorization |

## Authentication Notes

All operations in this Skill **require `mcp_token`**. Before calling any tool, must confirm user is logged in.

- If currently no `mcp_token` → Guide to `references/auth.md` to complete login then return.
- If `mcp_token` expired (MCP Server returns token expiration error) → Try `auth.refresh_token` silent refresh first, guide to re-login if failed.

## DApp Interaction Scenario Overview

| Scenario | Description | Core MCP Tools |
|----------|-------------|----------------|
| Wallet Connection | DApp requests wallet address | `wallet.get_addresses` |
| Message Signing | DApp login verification / EIP-712 typed data signing | `wallet.sign_message` |
| DApp Transaction Execution | Execute DApp-generated on-chain transactions (mint, stake, claim...) | `wallet.sign_transaction` → `tx.send_raw_transaction` |
| ERC20 Approve | Authorize DApp contracts to use specified tokens | `wallet.sign_transaction` → `tx.send_raw_transaction` |

## MCP Tool Call Specifications

### 1. `wallet.get_addresses` (Cross-Skill Call) — Get Wallet Addresses

Get account wallet addresses on various chains for DApp connection. This tool belongs to `gate-dex-wallet` domain, called cross-Skill here.

| Field | Description |
|-------|-------------|
| **Tool Name** | `wallet.get_addresses` |
| **Parameters** | `{ account_id: string, mcp_token: string }` |
| **Return Value** | `{ addresses: { [chain: string]: string } }` |

Call example:

```
CallMcpTool(
  server="gate-dex",
  toolName="wallet.get_addresses",
  arguments={ account_id: "acc_12345", mcp_token: "<mcp_token>" }
)
```

Return example:

```json
{
  "addresses": {
    "eth": "0xABCdef1234567890ABCdef1234567890ABCdef12",
    "bsc": "0xABCdef1234567890ABCdef1234567890ABCdef12",
    "sol": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU"
  }
}
```

Agent behavior: EVM chains share the same address. Provide target chain address to DApp to complete wallet connection.

---

### 2. `wallet.sign_message` — Sign Messages

Use server-side custodial private keys to sign arbitrary messages, supports personal_sign and EIP-712 typed data signing.

| Field | Description |
|-------|-------------|
| **Tool Name** | `wallet.sign_message` |
| **Parameters** | `{ message: string, chain: string, account_id: string, mcp_token: string }` |
| **Return Value** | `{ signature: string }` |

Parameter descriptions:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `message` | Yes | Message to be signed. personal_sign passes raw text, EIP-712 passes JSON string |
| `chain` | Yes | Chain identifier (e.g. `"eth"`, `"bsc"`) |
| `account_id` | Yes | User account ID |
| `mcp_token` | Yes | Authentication token |

Call example (personal_sign):

```
CallMcpTool(
  server="gate-dex",
  toolName="wallet.sign_message",
  arguments={
    message: "Welcome to Uniswap! Sign this message to verify your wallet. Nonce: abc123",
    chain: "eth",
    account_id: "acc_12345",
    mcp_token: "<mcp_token>"
  }
)
```

Call example (EIP-712):

```
CallMcpTool(
  server="gate-dex",
  toolName="wallet.sign_message",
  arguments={
    message: "{\"types\":{\"EIP712Domain\":[{\"name\":\"name\",\"type\":\"string\"}],\"Permit\":[{\"name\":\"owner\",\"type\":\"address\"},{\"name\":\"spender\",\"type\":\"address\"},{\"name\":\"value\",\"type\":\"uint256\"}]},\"primaryType\":\"Permit\",\"domain\":{\"name\":\"USDC\"},\"message\":{\"owner\":\"0xABC...\",\"spender\":\"0xDEF...\",\"value\":\"1000000000\"}}",
    chain: "eth",
    account_id: "acc_12345",
    mcp_token: "<mcp_token>"
  }
)
```

Return example:

```json
{
  "signature": "0x1234abcd...ef5678"
}
```

Agent behavior: Display message content to user before signing, explain signing purpose. Return signature to user after completion.

---

### 3. `wallet.sign_transaction` — Sign DApp Transactions

Use server-side custodial private keys to sign DApp-built unsigned transactions. **Only call after explicit user confirmation**.

| Field | Description |
|-------|-------------|
| **Tool Name** | `wallet.sign_transaction` |
| **Parameters** | `{ raw_tx: string, chain: string, account_id: string, mcp_token: string }` |
| **Return Value** | `{ signed_tx: string }` |

Parameter descriptions:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `raw_tx` | Yes | Unsigned transaction serialized data (hex format) |
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

### 4. `tx.send_raw_transaction` — Broadcast Signed Transactions

Broadcast signed DApp transactions to the on-chain network.

| Field | Description |
|-------|-------------|
| **Tool Name** | `tx.send_raw_transaction` |
| **Parameters** | `{ signed_tx: string, chain: string, mcp_token: string }` |
| **Return Value** | `{ hash_id: string }` |

Parameter descriptions:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `signed_tx` | Yes | Signed transaction returned by `wallet.sign_transaction` |
| `chain` | Yes | Chain identifier |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-dex",
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

## Supported DApp Interaction Types

| Type | Example Scenarios | Description |
|------|------------------|-------------|
| DeFi Liquidity | Uniswap add/remove liquidity | Build Router contract addLiquidity / removeLiquidity calls |
| DeFi Lending | Aave deposit/borrow/repay | Build Pool contract supply / borrow / repay calls |
| DeFi Staking | Lido stake ETH | Build stETH contract submit calls |
| NFT Mint | Custom NFT minting | Build mint contract calls |
| NFT Trading | Buy/sell NFTs | Build Marketplace contract calls |
| Token Approve | Authorize arbitrary contracts to use tokens | Build ERC20 approve(spender, amount) calldata |
| Arbitrary Contract Calls | User provides ABI + parameters | Agent encodes calldata and builds transactions |
| Message Signing | DApp login verification | `wallet.sign_message`, no on-chain transactions |

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

## Skill Routing

Based on user intent after DApp operations completion, route to corresponding Skills:

| User Intent | Route Target |
|-------------|--------------|
| View updated balance | `gate-dex-wallet` |
| View transaction details / history | `gate-dex-wallet` (`tx.detail`, `tx.list`) |
| View contract security info | `gate-dex-market` (`token_get_risk_info`) |
| Transfer tokens | `gate-dex-wallet` (`references/transfer.md`) |
| Swap exchange tokens | `gate-dex-trade` |
| Login / authentication expired | `gate-dex-wallet` (`references/auth.md`) |

## Operation Flows

### Flow A: DApp Wallet Connection

```
Step 0: MCP Server Connection Detection
  Call chain.config({chain: "eth"}) to probe availability
  ↓ Success

Step 1: Authentication Check
  Confirm valid mcp_token and account_id
  No token → Guide to references/auth.md login
  ↓

Step 2: Get Wallet Address
  Call wallet.get_addresses({ account_id, mcp_token })
  Extract target chain address
  ↓

Step 3: Display Address

  ────────────────────────────
  🔗 Wallet Connection Info

  Chain: {chain_name}
  Address: {address}

  Please use this address for DApp connection.
  EVM chains (Ethereum/BSC/Polygon etc.) share the same address.
  ────────────────────────────
```

### Flow B: Message Signing

```
Step 0: MCP Server Connection Detection
  ↓ Success

Step 1: Authentication Check
  ↓

Step 2: Intent Recognition + Parameter Collection
  Extract signing request from user input:
  - message: Content to be signed (required)
  - chain: Target chain (optional, default eth)
  - Signing type: personal_sign or EIP-712 (auto-detect from message format)
  ↓

Step 3: Display Signing Content Confirmation

  ────────────────────────────
  ✍️ Message Signing Request

  Chain: {chain_name}
  Signing Type: {personal_sign / EIP-712}
  Signing Content:
  {message_content}

  This signature will not generate on-chain transactions or consume Gas.
  Reply "confirm" to sign, "cancel" to abort.
  ────────────────────────────

  ↓ User confirms

Step 4: Execute Signing
  Call wallet.sign_message({ message, chain, account_id, mcp_token })
  ↓

Step 5: Display Signing Result

  ────────────────────────────
  ✅ Signing Complete

  Signature Result: {signature}

  Please submit this signature to the DApp to complete verification.
  ────────────────────────────
```

### Flow C: DApp Transaction Execution (Main Flow)

```
Step 0: MCP Server Connection Detection
  ↓ Success

Step 1: Authentication Check
  ↓

Step 2: Intent Recognition + Parameter Collection
  Extract DApp operation intent from user input:
  - Operation type (e.g. "add liquidity", "stake ETH", "mint NFT")
  - Target protocol/contract (e.g. Uniswap, Aave, Lido)
  - Amount and tokens
  - Chain (optional, infer from context)

  When parameters missing, ask user item by item:

  ────────────────────────────
  Please provide DApp interaction info:
  - Operation: (required, e.g. "Add ETH-USDC liquidity on Uniswap")
  - Chain: (optional, default Ethereum)
  - Amount: (may need multiple amounts based on operation type)
  ────────────────────────────

  ↓ Parameters complete

Step 3: Get Wallet Info (Cross-Skill: gate-dex-wallet)
  Call wallet.get_addresses({ account_id, mcp_token }) → get from_address
  Call wallet.get_token_list({ account_id, chain, mcp_token }) → get balance
  ↓

Step 4: Security Review (Recommended Step)
  Call token_get_risk_info({ chain, address: contract_address }) (Cross-Skill: gate-dex-market)
  Evaluate contract risk level
  ↓

Step 5: Agent Build Transaction
  Based on DApp operation type, Agent encodes contract call calldata:
  a) Known protocols (Uniswap/Aave/Lido etc.): encode by protocol ABI
  b) User provides ABI + parameters: Agent parses and encodes
  c) User provides complete calldata: use directly

  Build transaction parameters:
  - to: contract address
  - data: calldata
  - value: native token amount to send (if any)
  ↓

Step 6: Check if Approve Needed
  If operation involves ERC20 tokens (non-native):
  - Check current allowance is sufficient
  - Insufficient → Execute Approve transaction first (see Flow D)
  ↓

Step 7: Agent Balance Validation (Mandatory)
  Validation rules:
  a) Operation involves native tokens: native_balance >= amount + estimated_gas
  b) Operation involves ERC20 tokens: token_balance >= amount AND native_balance >= estimated_gas
  c) Gas only: native_balance >= estimated_gas

  Validation failed → Abort transaction:

  ────────────────────────────
  ❌ Insufficient balance, cannot execute DApp operation

  Required {symbol}: {required_amount}
  Current balance: {current_balance}
  Shortfall: {shortfall}

  Suggestions:
  - Reduce operation amount
  - Top up tokens to wallet first
  ────────────────────────────

  ↓ Validation passed

Step 8: Display DApp Transaction Confirmation Summary (Mandatory Gate)
  Display content as per "DApp Transaction Confirmation Template" below.
  Must wait for user explicit "confirm" reply before continuing.
  ↓

  User replies "confirm" → Continue Step 9
  User replies "cancel" → Abort transaction
  User requests modification → Return to Step 2

Step 9: Sign Transaction
  Call wallet.sign_transaction({ raw_tx, chain, account_id, mcp_token })
  Get signed_tx
  ↓

Step 10: Broadcast Transaction
  Call tx.send_raw_transaction({ signed_tx, chain, mcp_token })
  Get hash_id
  ↓

Step 11: Display Result + Follow-up Suggestions

  ────────────────────────────
  ✅ DApp transaction broadcast successful!

  Operation: {operation_description}
  Transaction Hash: {hash_id}
  Block Explorer: https://{explorer}/tx/{hash_id}

  Transaction submitted to network, confirmation time depends on network congestion.

**Output Format**: Display transaction hash and block explorer URL as plain text, not as hyperlinks.

  You can:
  - View updated balance
  - View transaction details
  - Continue other operations
  ────────────────────────────
```

### Flow D: ERC20 Approve Authorization

```
Step 0: MCP Server Connection Detection
  ↓ Success

Step 1: Authentication Check
  ↓

Step 2: Determine Approve Parameters
  - token_address: Token contract address to be authorized
  - spender: Spender contract address (e.g. Uniswap Router)  
  - amount: Authorization amount

  Agent recommends exact amount over unlimited:

  ────────────────────────────
  💡 Authorization Amount Recommendation

  This operation requires authorizing {spender_name} to use your {token_symbol}.

  Recommended options:
  1. Exact authorization: {exact_amount} {token_symbol} (sufficient for this operation only, safer)
  2. Unlimited authorization: unlimited (no need to re-authorize for future operations, but higher risk)

  Please choose authorization method or specify custom amount.
  ────────────────────────────

  ↓

Step 3: Build Approve Calldata
  Encode ERC20 approve(spender, amount) function call:
  - function selector: 0x095ea7b3
  - spender: contract address (32 bytes padded)
  - amount: authorization amount (uint256)
  ↓

Step 4: Display Approve Confirmation

  ────────────────────────────
  ========== Token Authorization Confirmation ==========
  Chain: {chain_name}
  Token: {token_symbol} ({token_address})
  Authorize to: {spender_name} ({spender_address})
  Authorization Amount: {amount} {token_symbol}
  Estimated Gas: {estimated_gas} {gas_symbol}
  ===============================
  Reply "confirm" to execute authorization, "cancel" to abort.
  ────────────────────────────

  ↓ User confirms

Step 5: Sign + Broadcast Approve Transaction
  Call wallet.sign_transaction({ raw_tx: approve_tx, chain, account_id, mcp_token })
  Call tx.send_raw_transaction({ signed_tx, chain, mcp_token })
  ↓

Step 6: Approve Success
  Display Approve transaction hash, continue subsequent DApp operations (Flow C Step 9)
```

### Flow E: Arbitrary Contract Calls (User Provides ABI)

```
Step 0: MCP Server Connection Detection
  ↓ Success

Step 1: Authentication Check
  ↓

Step 2: Collect Contract Call Information
  User provides:
  - Contract address
  - Function name or ABI
  - Function parameters
  - value (optional, needed when sending native tokens)
  - chain
  ↓

Step 3: Agent Encode Calldata
  Encode function call data based on ABI and parameters
  ↓

Step 4: Security Review + Balance Validation + Confirmation Gate
  Same as Flow C Step 4 ~ Step 8
  ↓

Step 5: Sign + Broadcast
  Same as Flow C Step 9 ~ Step 11
```

## DApp Transaction Confirmation Template

**This confirmation summary is mandatory gate - Agent must not execute signing before user explicitly replies "confirm". This cannot be skipped.**

### Standard DApp Transaction Confirmation

```
========== DApp Transaction Confirmation ==========
Chain: {chain_name}
DApp/Protocol: {protocol_name} (e.g. Uniswap V3)
Operation: {operation} (e.g. Add Liquidity)
Contract Address: {contract_address}
---------- Transaction Details ----------
{operation_specific_details}
(e.g. Token A: 0.5 ETH, Token B: 1000 USDC)
---------- Authorization Info ----------
{approve_info_if_needed}
(e.g. Needs Approve: USDC → Uniswap Router, Amount: 1000 USDC)
(When no approval needed: No additional authorization required)
---------- Balance Info ----------
{token_symbol} Balance: {balance} (Sufficient ✅ / Insufficient ❌)
{gas_symbol} Balance (Gas): {gas_balance} (Sufficient ✅)
---------- Fee Info ----------
Estimated Gas (Approve): {approve_gas} (if needed)
Estimated Gas (Transaction): {tx_gas} {gas_symbol}
---------- Security Check ----------
Contract Security Audit: {risk_level} (e.g. Audited/Low Risk/High Risk/Unknown)
===============================
Reply "confirm" to execute, "cancel" to abort, or tell me what to modify.

Note: DApp interactions involve smart contract calls, please confirm contract address and operations are correct.
```

### Unknown Contract Warning Confirmation

When target contract is not audited or audit results indicate high risk:

```
========== ⚠️ DApp Transaction Confirmation (Security Warning) ==========
Chain: {chain_name}
Contract Address: {contract_address}

⚠️ Security Warning: This contract is not audited or marked as high risk.
Interacting with unknown contracts may lead to asset loss. Please confirm you trust this contract.

---------- Transaction Details ----------
{operation_details}
---------- Balance Info ----------
{balance_info}
---------- Fee Info ----------
{gas_info}
---------- Security Check ----------
Contract Audit Status: {risk_detail}
=================================================
Reply "confirm" to still execute (at your own risk), "cancel" to abort.
```

## Cross-Skill Workflows

### Complete DApp Interaction Flow (From Login to Completion)

```
gate-dex-wallet/references/auth.md (Login, get mcp_token + account_id)
  → gate-dex-wallet (wallet.get_addresses → get address)
    → gate-dex-wallet (wallet.get_token_list → validate balance)
      → gate-dex-market (token_get_risk_info → contract security review)
        → gate-dex-wallet/references/dapp.md (Approve? → Confirm → Sign → Broadcast)
          → gate-dex-wallet (view updated balance)
```

### DApp Message Signing (No Transactions)

```
gate-dex-wallet/references/auth.md (Login)
  → gate-dex-wallet/references/dapp.md (wallet.sign_message → return signature result)
```

### Guided by Other Skills

| Source Skill | Scenario | Description |
|-------------|---------|-------------|
| `gate-dex-wallet` | User views address then wants to connect DApp | Carries account_id and address info |
| `gate-dex-market` | User views tokens then wants to participate in DeFi | Carries token and chain context |
| `gate-dex-trade` | After Swap wants to further participate in DeFi | Carries chain and token context |

### Calling Other Skills

| Target Skill | Call Scenario | Used Tools |
|-------------|---------------|------------|
| `gate-dex-wallet` | Get wallet address for DApp connection | `wallet.get_addresses` |
| `gate-dex-wallet` | Validate balance before DApp transactions | `wallet.get_token_list` |
| `gate-dex-wallet` | View updated balance after DApp transactions | `wallet.get_token_list` |
| `gate-dex-wallet` (`references/auth.md`) | Not logged in or token expired | `auth.refresh_token` or complete login flow |
| `gate-dex-market` | Contract security review | `token_get_risk_info` |
| `gate-dex-wallet` | View transaction details after DApp transactions | `tx.detail`, `tx.list` |

## Contract Address Validation Rules

Contract address validation in DApp transactions and Approve:

| Chain Type | Format Requirements | Validation Rules |
|------------|-------------------|------------------|
| EVM (eth/bsc/polygon/...) | Starts with `0x`, 40 hex characters (42 total) | Regex `^0x[0-9a-fA-F]{40}$`, recommend EIP-55 checksum validation |
| Solana | Base58 encoded, 32-44 characters | Regex `^[1-9A-HJ-NP-Za-km-z]{32,44}$` |

When validation fails:

```
❌ Invalid contract address format

Provided address: {user_input}
Expected format: {expected_format}

Please check if address is correct, complete, and matches target chain.
```

## ERC20 Approve Calldata Encoding Specification

Agent must encode calldata according to the following rules when building Approve transactions:

```
Function signature: approve(address spender, uint256 amount)
Selector: 0x095ea7b3

Calldata structure:
0x095ea7b3
+ spender address (32 bytes, left-padded with zeros)
+ amount (32 bytes, uint256)

Example (approve Uniswap Router to use 1000 USDT, 6 decimals):
0x095ea7b3
000000000000000000000000 68b3465833fb72A70ecDF485E0e4C7bD8665Fc45  ← spender
00000000000000000000000000000000000000000000000000000000 3B9ACA00  ← 1000 * 10^6
```

Exact authorization vs unlimited authorization:

| Method | amount Value | Security | Convenience |
|--------|-------------|----------|-------------|
| Exact authorization | Actual needed amount | High (stops when used up) | Low (need to re-authorize each time) |
| Unlimited authorization | `2^256 - 1` (`0xfff...fff`) | Low (contract can transfer tokens anytime) | High (one authorization permanent) |

**Recommend exact authorization**, unless user explicitly requests unlimited authorization.

## EIP-712 Signature Data Parsing Specification

Agent must parse JSON structured data into human-readable format when displaying EIP-712 signature requests:

### Parsing Key Points

1. **Domain Info**: Extract `name`, `version`, `chainId`, `verifyingContract`, display in table format
2. **Primary Type**: Clearly indicate signature data main type (e.g. `Order`, `Permit`, `Vote`)
3. **Message Fields**: Display field by field, truncate `address` types for display, try converting `uint256` types to human-readable numbers
4. **Known Type Recognition**:
   - `Permit` (EIP-2612) → Label as "Token Authorization Permit", highlight spender and value
   - `Order` (DEX orders) → Label as "Trading Order", highlight trading pair and amount
   - `Vote` (governance voting) → Label as "Governance Vote", highlight voting content

### Known EIP-712 Signature Types

| primaryType | Common Source | Risk Level | Description |
|------------|--------------|------------|-------------|
| `Permit` | ERC-2612 tokens | Medium | Off-chain signature authorization, no Gas but grants spender token usage rights |
| `Order` | DEX (e.g. 0x, Seaport) | Medium | Represents trading order, can be executed on-chain after signature |
| `Vote` | Governance protocols (e.g. Compound) | Low | Governance voting |
| `Delegation` | Governance protocols | Low | Voting right delegation |
| Unknown types | Any DApp | High | Needs additional warning for users to carefully review content |

## Boundary Cases and Error Handling

| Scenario | Handling Method |
|----------|----------------|
| MCP Server not configured | Abort all operations, display Cursor configuration guidance |
| MCP Server unreachable | Abort all operations, display network check prompt |
| Not logged in (no `mcp_token`) | Guide to `references/auth.md` to complete login then auto-return to continue DApp operations |
| `mcp_token` expired | Try `auth.refresh_token` silent refresh first, guide to re-login if failed |
| Gas token balance insufficient | Abort transaction/Approve, display Gas insufficient info, suggest top-up |
| Approve token not in holdings | Prompt user doesn't hold this token, Approve can execute but has no practical meaning. Confirm whether to continue |
| Spender contract is high risk | Strongly warn user, recommend cancellation. User insists can still continue (needs re-confirmation) |
| Spender contract is unknown (not indexed) | Display "unknown contract" warning, prompt user to verify contract source |
| Contract address format invalid | Refuse to initiate transaction, prompt correct address format |
| `wallet.sign_message` fails | Display signing error message, possible causes: incorrect message format, account anomaly. Don't auto-retry |
| EIP-712 JSON parsing fails | Display raw JSON content, prompt format may be incorrect, ask user to confirm or re-obtain from DApp |
| `wallet.sign_transaction` fails | Display signing error, possible causes: invalid transaction data, account permission issues. Don't auto-retry |
| `tx.send_raw_transaction` fails | Display broadcast error (nonce conflict, gas insufficient, network congestion, etc.), suggest corresponding measures based on error type |
| User cancels confirmation (signing/transaction/Approve) | Immediately abort, don't execute any signing or broadcasting. Display cancellation prompt, remain friendly |
| `tx.gas` estimation fails | Display error message, possible causes: contract call would revert, incorrect parameters. Suggest checking transaction data |
| Approve amount is 0 | Treat as "cancel authorization" operation, confirm with user whether to revoke authorization to this spender |
| User requests unlimited authorization | Display high-risk warning template, needs user secondary confirmation |
| Repeated Approve to same spender | Prompt existing authorization, new Approve will overwrite old authorization. Confirm whether to continue |
| Network disconnection after signing before broadcasting | Prompt signed transaction can still be broadcast later, suggest retry after network recovery |
| DApp provided raw_tx format abnormal | Refuse signing, prompt transaction data format incorrect, suggest re-generating from DApp |
| Chain identifier not supported | Display supported chain list, ask user to re-select |
| Message signing request chain is Solana | Prompt Solana message signing not yet supported, only supports EVM chains |
| Network interruption | Display network error, suggest checking network then retry |

## Safety Rules

1. **`mcp_token` confidentiality**: Never display `mcp_token` in plaintext to users, only use placeholders like `<mcp_token>` in call examples.
2. **`account_id` masking**: When displaying to users, only show partial characters (e.g. `acc_12...89`).
3. **Auto token refresh**: When `mcp_token` expires, prioritize silent refresh, only require re-login if refresh fails.
4. **Confirmation required before signing**: All signing operations (message signing, transaction signing, Approve) **must** display complete content to users and get explicit "confirm" reply before execution. Cannot skip, simplify or auto-confirm.
5. **Contract security review**: When DApp interactions involve unknown contracts, **must** call `token_get_risk_info` for security review and display results to users. High-risk contracts need additional prominent warnings.
6. **Default exact authorization**: ERC20 Approve defaults to exact authorization amount. Only use unlimited authorization when user explicitly requests it, and **must** display unlimited authorization risk warnings.
7. **EIP-712 content transparency**: EIP-712 signing requests must be completely parsed and displayed in human-readable format to users, cannot omit any key fields (especially `verifyingContract`, `spender`, amount fields).
8. **Mandatory gas balance validation**: **Must** validate gas token balance before DApp transactions and Approve, **prohibit** initiating signing and broadcasting when balance insufficient.
9. **No auto-retry failed operations**: After signing or broadcasting failures, clearly display error messages to users, don't auto-retry in background.
10. **Prohibit operations when MCP Server not configured or unreachable**: If Step 0 connection detection fails, abort all subsequent steps.
11. **MCP Server error transparency**: Display all MCP Server returned error messages to users truthfully, don't hide or tamper.
12. **`raw_tx` non-disclosure**: Unsigned transaction raw data only flows between Agent and MCP Server, don't display hex raw text to users.
13. **Prompt broadcasting after signing**: Should broadcast immediately after successful signing, shouldn't hold signed transactions for long periods.
14. **Permit signature risk notification**: EIP-2612 Permit signatures consume no Gas but are equivalent to authorization operations, must remind users to pay attention to spender and authorization amount.
15. **Phishing prevention**: Agent doesn't proactively construct transactions or signature requests pointing to unknown contracts. All DApp interaction data should be provided by users or obtained from trusted sources.