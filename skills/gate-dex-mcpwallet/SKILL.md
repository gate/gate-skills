---
name: gate-dex-mcpwallet
version: "2026.3.6-1"
updated: "2026-03-06"
description: "Gate Wallet portfolio assets and transaction history. Query balance, total assets, token holdings, wallet address, transfer history, transaction details, Swap history. Use when user asks 'how much ETH do I have', 'check balance', 'total assets', 'wallet address', 'transaction history', 'transfer records'. Supports EVM multi-chain + Solana."
---

# Gate Wallet Portfolio Skill

> Wallet/Assets/History domain — Query token balance, total asset value, wallet address, chain config, transfer history, transaction details, Swap history. 7 MCP tools.

**Trigger scenarios**: User mentions "check balance", "how much do I have", "assets", "holdings", "address", "transaction history", "transfer records", "Swap history", "transaction details", "balance", "portfolio", "wallet address", "history", or when other Skills need balance verification / address retrieval / transaction history query.

## Step 0: MCP Server Connection Check (Mandatory)

**Before executing any operation, Gate Wallet MCP Server availability must be confirmed. This step cannot be skipped.**

Probe call:

```
CallMcpTool(server="gate-wallet", toolName="chain.config", arguments={chain: "eth"})
```

| Result | Action |
|--------|--------|
| Success | MCP Server available, proceed with subsequent steps |
| `server not found` / `unknown server` | Cursor not configured → Show configuration guide (see below) |
| `connection refused` / `timeout` | Remote unreachable → Prompt to check URL and network |
| `401` / `unauthorized` | API Key authentication failed → Prompt to check auth config |

### Display when Cursor is not configured

```
❌ Gate Wallet MCP Server not configured

The MCP Server named "gate-wallet" was not found in Cursor. Please configure as follows:

Method 1: Configure via Cursor Settings (recommended)
  1. Open Cursor → Settings → MCP
  2. Click "Add new MCP server"
  3. Fill in:
     - Name: gate-wallet
     - Type: HTTP
     - URL: https://your-mcp-server-domain/mcp
  4. Save and retry

Method 2: Edit config file manually
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

MCP Server config was found, but connection to remote service failed. Please check:
1. Confirm the service URL is correct (is the configured URL accessible)
2. Check network connection (VPN / firewall impact)
3. Confirm the remote service is running
```

### Display when API Key authentication fails

```
🔑 Gate Wallet MCP Server authentication failed

MCP Server connected but API Key validation failed. This service uses AK/SK authentication (x-api-key header).
Please contact your administrator for a valid API Key and confirm server-side configuration.
```

## Authentication

All operations in this Skill **require `mcp_token`**. User must be logged in before calling any tool.

- If no `mcp_token` is present → Guide user to `gate-dex-mcpauth` to complete login, then return.
- If `mcp_token` is expired (MCP Server returns token expired error) → First try `auth.refresh_token` for silent refresh, on failure guide user to re-login.

## MCP Tool Call Specification

### 1. `wallet.get_token_list` — Query token list (with balance)

Get the list of tokens held by the specified account on a chain (or all chains), including balance and price info.

| Field | Description |
|-------|-------------|
| **Tool name** | `wallet.get_token_list` |
| **Parameters** | `{ account_id: string, chain?: string, mcp_token: string }` |
| **Return value** | Token array, each item contains `symbol`, `balance`, `price`, `value`, `chain`, `contract_address`, etc. |

Parameter description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `account_id` | Yes | User account ID (obtained at login) |
| `chain` | No | Chain identifier (e.g. `"eth"`, `"bsc"`, `"sol"`). Omit to query all supported chains |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="wallet.get_token_list",
  arguments={ account_id: "acc_12345", chain: "eth", mcp_token: "<mcp_token>" }
)
```

Return example:

```json
[
  {
    "symbol": "ETH",
    "balance": "2.5",
    "price": 1920.50,
    "value": 4801.25,
    "chain": "eth",
    "contract_address": "native"
  },
  {
    "symbol": "USDT",
    "balance": "5000",
    "price": 1.0,
    "value": 5000.00,
    "chain": "eth",
    "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7"
  }
]
```

---

### 2. `wallet.get_total_asset` — Query total asset value

Get the total USD value of account assets across all chains and its change.

| Field | Description |
|-------|-------------|
| **Tool name** | `wallet.get_total_asset` |
| **Parameters** | `{ account_id: string, mcp_token: string }` |
| **Return value** | `{ total_value: number, change_value: number, change_percent: number }` |

Parameter description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `account_id` | Yes | User account ID |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="wallet.get_total_asset",
  arguments={ account_id: "acc_12345", mcp_token: "<mcp_token>" }
)
```

Return example:

```json
{
  "total_value": 15230.75,
  "change_value": 320.50,
  "change_percent": 2.15
}
```

---

### 3. `wallet.get_addresses` — Get wallet addresses

Get wallet addresses for the account on each chain.

| Field | Description |
|-------|-------------|
| **Tool name** | `wallet.get_addresses` |
| **Parameters** | `{ account_id: string, mcp_token: string }` |
| **Return value** | `{ addresses: { [chain: string]: string } }` |

Parameter description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `account_id` | Yes | User account ID |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-wallet",
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
    "polygon": "0xABCdef1234567890ABCdef1234567890ABCdef12",
    "sol": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU"
  }
}
```

Agent behavior: EVM chains share the same address, Solana has a separate address. Display grouped by chain name.

---

### 4. `chain.config` — Query chain configuration

Get network configuration info for the specified chain (RPC endpoint, chain ID, etc.). Mainly for internal validation and auxiliary operations.

| Field | Description |
|-------|-------------|
| **Tool name** | `chain.config` |
| **Parameters** | `{ chain: string, mcp_token: string }` |
| **Return value** | `{ networkKey: string, endpoint: string, chainID: number }` |

Parameter description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | Yes | Chain identifier (e.g. `"eth"`, `"bsc"`, `"polygon"`, `"sol"`) |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="chain.config",
  arguments={ chain: "eth", mcp_token: "<mcp_token>" }
)
```

Return example:

```json
{
  "networkKey": "ethereum",
  "endpoint": "https://mainnet.infura.io/v3/...",
  "chainID": 1
}
```

---

### 5. `tx.list` — Query transfer transaction list

Get the user's transfer transaction history.

| Field | Description |
|-------|-------------|
| **Tool name** | `tx.list` |
| **Parameters** | `{ account_id: string, chain?: string, page?: number, limit?: number, mcp_token: string }` |
| **Return value** | Transaction array, each item contains `hash_id`, `chain`, `from`, `to`, `amount`, `token_symbol`, `status`, `timestamp` |

Parameter description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `account_id` | Yes | User account ID |
| `chain` | No | Chain identifier. Omit to query all chains |
| `page` | No | Page number. Default 1 |
| `limit` | No | Items per page. Default 20 |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="tx.list",
  arguments={
    account_id: "acc_12345",
    chain: "eth",
    limit: 10,
    mcp_token: "<mcp_token>"
  }
)
```

Return example:

```json
[
  {
    "hash_id": "0xa1b2c3d4...",
    "chain": "eth",
    "from": "0xABC...1234",
    "to": "0xDEF...5678",
    "amount": "1000",
    "token_symbol": "USDT",
    "status": "success",
    "timestamp": 1700000000
  }
]
```

---

### 6. `tx.detail` — Query transaction details

Get detailed information for a specific transaction.

| Field | Description |
|-------|-------------|
| **Tool name** | `tx.detail` |
| **Parameters** | `{ hash_id: string, chain: string, mcp_token: string }` |
| **Return value** | `{ hash_id: string, chain: string, from: string, to: string, amount: string, token_symbol: string, status: string, gas_used: string, gas_price: string, block_number: number, timestamp: number }` |

Parameter description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `hash_id` | Yes | Transaction hash |
| `chain` | Yes | Chain identifier |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="tx.detail",
  arguments={
    hash_id: "0xa1b2c3d4e5f6...7890",
    chain: "eth",
    mcp_token: "<mcp_token>"
  }
)
```

Return example:

```json
{
  "hash_id": "0xa1b2c3d4e5f6...7890",
  "chain": "eth",
  "from": "0xABC...1234",
  "to": "0xDEF...5678",
  "amount": "1000",
  "token_symbol": "USDT",
  "status": "success",
  "gas_used": "65000",
  "gas_price": "30000000000",
  "block_number": 18500000,
  "timestamp": 1700000000
}
```

---

### 7. `tx.history_list` — Query Swap history

Get the user's Swap transaction history.

| Field | Description |
|-------|-------------|
| **Tool name** | `tx.history_list` |
| **Parameters** | `{ account_id: string, chain?: string, page?: number, limit?: number, mcp_token: string }` |
| **Return value** | Swap record array, each item contains `hash_id`, `chain`, `from_token`, `from_amount`, `to_token`, `to_amount`, `status`, `timestamp` |

Parameter description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `account_id` | Yes | User account ID |
| `chain` | No | Chain identifier. Omit to query all chains |
| `page` | No | Page number. Default 1 |
| `limit` | No | Items per page. Default 20 |
| `mcp_token` | Yes | Authentication token |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="tx.history_list",
  arguments={
    account_id: "acc_12345",
    chain: "eth",
    limit: 10,
    mcp_token: "<mcp_token>"
  }
)
```

Return example:

```json
[
  {
    "hash_id": "0xc3d4e5f6...",
    "chain": "eth",
    "from_token": "USDT",
    "from_amount": "100",
    "to_token": "ETH",
    "to_amount": "0.0521",
    "status": "success",
    "timestamp": 1700000000
  }
]
```

## Supported Chains

| Chain ID | Network Name | Type |
|----------|--------------|------|
| `eth` | Ethereum | EVM |
| `bsc` | BNB Smart Chain | EVM |
| `polygon` | Polygon | EVM |
| `arbitrum` | Arbitrum One | EVM |
| `optimism` | Optimism | EVM |
| `avax` | Avalanche C-Chain | EVM |
| `base` | Base | EVM |
| `sol` | Solana | Non-EVM |

When querying balance, if `chain` parameter is not specified, token data from all supported chains will be aggregated.

## Skill Routing

Based on user intent after viewing assets, route to the corresponding Skill:

| User Intent | Route Target |
|-------------|--------------|
| View token market data, K-line, price trend | `gate-dex-mcpmarket` |
| View token security audit info | `gate-dex-mcpmarket` (`token_get_risk_info`) |
| Transfer, send tokens to another address | `gate-dex-mcptransfer` |
| Swap tokens | `gate-dex-mcpswap` |
| Interact with DApp, sign messages | `gate-dex-mcpdapp` |
| Login / auth expired | `gate-dex-mcpauth` |

## Operation Flows

### Flow A: Query token balance

```
Step 0: MCP Server pre-check
  Call chain.config({chain: "eth"}) to probe availability
  ↓ Success

Step 1: Auth check
  Confirm valid mcp_token and account_id
  No token → Guide to gate-dex-mcpauth for login
  ↓

Step 2: Intent recognition + parameter collection
  Determine user query scope:
  - Specific chain balance (e.g. "how much USDT do I have on Ethereum") → chain = "eth"
  - Specific token balance (e.g. "how much ETH do I have") → Query all first, then filter
  - All assets (e.g. "show my balance") → Don't specify chain
  ↓

Step 3: Execute query
  Call wallet.get_token_list({ account_id, chain?, mcp_token })
  ↓

Step 4: Format display
  Sort by USD value descending, display:

  ────────────────────────────
  📊 Wallet Balance (Ethereum)

  | Token  | Balance     | Price (USD)  | Value (USD)    |
  |--------|-------------|-------------|----------------|
  | USDT   | 5,000.00    | $1.00       | $5,000.00      |
  | ETH    | 2.50        | $1,920.50   | $4,801.25      |
  | USDC   | 1,000.00    | $1.00       | $1,000.00      |

  Total: $10,801.25
  ────────────────────────────

  If querying all chains, display grouped by chain.
  ↓

Step 5: Suggest next actions
  - View market trend for a token → gate-dex-mcpmarket
  - Transfer tokens → gate-dex-mcptransfer
  - Swap tokens → gate-dex-mcpswap
```

### Flow B: Query total asset value

```
Step 0: MCP Server pre-check
  ↓ Success

Step 1: Auth check
  Confirm valid mcp_token and account_id
  ↓

Step 2: Execute query
  Call wallet.get_total_asset({ account_id, mcp_token })
  ↓

Step 3: Format display

  ────────────────────────────
  💰 Total Assets Overview

  Total asset value: $15,230.75
  24h change: +$320.50 (+2.15%)
  ────────────────────────────

  ↓

Step 4: Suggest next actions
  - View holdings by chain → Flow A (wallet.get_token_list)
  - View token market data → gate-dex-mcpmarket
  - Transfer / Swap → gate-dex-mcptransfer / gate-dex-mcpswap
```

### Flow C: Get wallet addresses

```
Step 0: MCP Server pre-check
  ↓ Success

Step 1: Auth check
  Confirm valid mcp_token and account_id
  ↓

Step 2: Intent recognition
  Determine user needs:
  - Specific chain address (e.g. "my Ethereum address") → Return that chain's address
  - All chain addresses → Return all
  ↓

Step 3: Execute query
  Call wallet.get_addresses({ account_id, mcp_token })
  ↓

Step 4: Format display

  ────────────────────────────
  🔑 Wallet Addresses

  EVM chains (shared address):
    0xABCdef1234567890ABCdef1234567890ABCdef12
    Applies to: Ethereum, BSC, Polygon, Arbitrum, Optimism, Avalanche, Base

  Solana:
    7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU
  ────────────────────────────

  Note: EVM chains share the same address, Solana has a separate address.
  ↓

Step 5: Suggest next actions
  - View balance for this address → Flow A
  - Receive tokens to this address → Provide address to counterparty
  - Send tokens from this address → gate-dex-mcptransfer
  - Connect DApp with this address → gate-dex-mcpdapp
```

### Flow D: Query chain config (auxiliary flow)

```
Step 0: MCP Server pre-check
  ↓ Success

Step 1: Execute query
  Call chain.config({ chain, mcp_token })
  ↓

Step 2: Return config info
  Usually used as internal auxiliary info, not displayed to user separately.
  Used when other Skills need chain RPC info.
```

### Flow E: View transfer history

```
Step 0: MCP Server connection check
  ↓ Success

Step 1: Auth check
  Confirm valid mcp_token and account_id
  No token → Guide to gate-dex-mcpauth for login
  ↓

Step 2: Parameter collection
  Determine query scope (chain, page)
  ↓

Step 3: Execute query
  Call tx.list({ account_id, chain?, page?, limit?, mcp_token })
  ↓

Step 4: Format display

  ────────────────────────────
  📋 Transfer History

  | Time | Chain | Direction | Amount | Token | Status | Hash |
  |------|-------|-----------|--------|-------|--------|------|
  | {time} | {chain} | Sent/Received | {amount} | {symbol} | ✅/{status} | {hash_short} |
  ────────────────────────────

  ↓

Step 5: Suggest next actions
  - View transaction details → Flow F (tx.detail)
  - View Swap history → Flow G (tx.history_list)
  - View current balance → Flow A (wallet.get_token_list)
```

### Flow F: View transaction details

```
Step 0: MCP Server connection check
  ↓ Success

Step 1: Auth check
  ↓

Step 2: Execute query
  Call tx.detail({ hash_id, chain, mcp_token })
  ↓

Step 3: Format display

  ────────────────────────────
  🔍 Transaction Details

  Transaction Hash: {hash_id}
  Chain: {chain_name}
  Status: {status}
  Block: {block_number}
  Time: {timestamp}
  From: {from}
  To: {to}
  Amount: {amount} {token_symbol}
  Gas used: {gas_used}
  Gas price: {gas_price}
  Block explorer: https://{explorer}/tx/{hash_id}
  ────────────────────────────
```

### Flow G: View Swap history

```
Step 0: MCP Server connection check
  ↓ Success

Step 1: Auth check
  ↓

Step 2: Execute query
  Call tx.history_list({ account_id, chain?, page?, limit?, mcp_token })
  ↓

Step 3: Format display

  ────────────────────────────
  🔄 Swap History

  | Time | Chain | Input | Output | Gas Fee | Status | Hash |
  |------|-------|-------|--------|---------|--------|------|
  | {time} | {chain} | {from_amount} {from_token} | {to_amount} {to_token} | {gas_fee} {gas_symbol} (≈ ${gas_fee_usd}) | ✅ | {hash_short} |
  ────────────────────────────
```

## Cross-Skill Workflows

### Called by other Skills

This Skill acts as an asset data provider and is often called by:

| Caller | Call scenario | Tools used |
|--------|---------------|------------|
| `gate-dex-mcptransfer` | Verify sufficient balance before transfer | `wallet.get_token_list` |
| `gate-dex-mcpswap` | Verify input token balance before Swap | `wallet.get_token_list` |
| `gate-dex-mcpdapp` | Get wallet address for DApp connection | `wallet.get_addresses` |
| `gate-dex-mcpdapp` | Verify balance before DApp transaction | `wallet.get_token_list` |
| `gate-dex-mcptransfer` | View updated balance after transaction | `wallet.get_token_list` |
| `gate-dex-mcptransfer` | View transaction details after transfer | `tx.detail`, `tx.list` |
| `gate-dex-mcpswap` | View updated balance after Swap | `wallet.get_token_list` |
| `gate-dex-mcpswap` | View history after Swap | `tx.history_list` |
| `gate-dex-mcpdapp` | View updated balance after DApp transaction | `wallet.get_token_list` |
| `gate-dex-mcpdapp` | View transaction details after DApp transaction | `tx.detail`, `tx.list` |

### Typical combined workflows

**Query and buy**:

```
gate-dex-mcpwallet (check balance, confirm sufficient tokens)
  → gate-dex-mcpmarket (check target token market / security info)
    → gate-dex-mcpswap (execute buy)
      → gate-dex-mcpwallet (view updated balance)
```

**Portfolio overview**:

```
gate-dex-mcpwallet (wallet.get_total_asset → total assets)
  → gate-dex-mcpwallet (wallet.get_token_list → holdings detail)
    → gate-dex-mcpmarket (supplement token market / K-line)
```

**Full transfer flow**:

```
gate-dex-mcpwallet (wallet.get_token_list → verify balance)
  → gate-dex-mcpwallet (wallet.get_addresses → get sender address)
    → gate-dex-mcptransfer (build → confirm → sign → broadcast)
      → gate-dex-mcpwallet (view updated balance)
```

## Display Rules

### Balance display rules

- **Sorting**: By USD value descending
- **Zero balance filter**: Hide tokens with 0 balance by default, show only when user explicitly requests
- **Precision**:
  - Token balance: Max 8 decimal places, trim trailing zeros
  - USD value: 2 decimal places, thousand separators
  - Price change percent: 2 decimal places
- **Per-chain display**: When querying multiple chains, display grouped by chain with subtotal per group

### Address display rules

- EVM address shown in full (42 chars), with shared chain list
- Solana address shown in full (32-44 chars)
- Use masked format for short reference: `0xABCD...ef12`

## Edge Cases and Error Handling

| Scenario | Action |
|----------|--------|
| MCP Server not configured | Abort all operations, show Cursor config guide |
| MCP Server unreachable | Abort all operations, show network check prompt |
| Not logged in (no `mcp_token`) | Guide to `gate-dex-mcpauth` to complete login, then auto-return to continue query |
| `mcp_token` expired | First try `auth.refresh_token` for silent refresh, on failure guide to re-login |
| `wallet.get_token_list` returns empty list | Inform user no token holdings on this chain/account, suggest checking chain selection |
| Specified `chain` not supported | Show supported chain list, ask user to choose again |
| Invalid `account_id` | Show error, suggest re-login to get valid account_id |
| `tx.list` returns empty list | Prompt no transfer records, confirm chain selection |
| `tx.history_list` returns empty list | Prompt no Swap records |
| `tx.detail` query failed | Confirm transaction hash and chain identifier are correct |
| Query timeout | Prompt network issue, suggest retry later or specify single chain to reduce data |
| Token price data missing | Display balance normally, show "N/A" in price column, exclude from total USD value |
| MCP Server returns unknown error | Display error message as-is, do not silently swallow |
| User-requested token not in holdings | Clearly inform token not found, suggest confirming token name/chain |

## Security Rules

1. **`mcp_token` confidentiality**: Never display `mcp_token` in plain text to user; use placeholder `<mcp_token>` in call examples.
2. **`account_id` masking**: When displaying to user, show only partial chars (e.g. `acc_12...89`).
3. **Token auto-refresh**: When `mcp_token` expires, try silent refresh first; only require re-login on failure.
4. **Read-only operations**: This Skill only involves queries, no on-chain write operations; no transaction confirmation gating needed.
5. **No operations when MCP Server not configured or unreachable**: Abort all subsequent steps if Step 0 connection check fails.
6. **MCP Server error transparency**: All MCP Server error messages are displayed to user as-is; do not hide or alter.
7. **Address integrity**: When displaying wallet address, ensure it is complete and accurate; avoid truncation that could cause user to copy wrong address. Use masked format for short reference, but provide a way to copy full address.
