---
name: gate-dex-trade/references/mcp.md
version: "2026.3.12-1"
updated: "2026-03-12"
description: "Gate Wallet Swap/DEX trading. Get quotes, execute Swap. Use when users want to 'swap USDT to ETH', 'swap', 'exchange tokens', 'buy tokens', 'sell tokens'. Includes mandatory three-step confirmation gate. Supports EVM multi-chain + Solana, supports cross-chain Swap."
---

# Gate Wallet Swap Skill

> Swap/DEX Domain — Quote retrieval, slippage control, route display, Swap execution (One-shot), status tracking, includes mandatory three-step confirmation gateway. 3 MCP tools + 2 cross-Skill calls + 1 MCP Resource.

**Trigger Scenarios**: When users mention "swap", "exchange", "buy", "sell", "convert", "swap X for Y", "cross-chain", or when other Skills guide users to execute token swaps.

## Step 0: MCP Server Connection Detection (Mandatory)

**Before executing any operations, must first confirm Gate Wallet MCP Server availability. This step cannot be skipped.**

Detection call:

```
CallMcpTool(server="gate-dex", toolName="chain.config", arguments={chain: "ETH"})
```

| Result | Handling |
|--------|----------|
| Success | MCP Server available, proceed to subsequent steps |
| `server not found` / `unknown server` | Cursor not configured → Show configuration guide (see below) |
| `connection refused` / `timeout` | Remote unreachable → Prompt to check URL and network |
| `401` / `unauthorized` | API Key authentication failed → Prompt to check authentication configuration |

### Display when Cursor not configured

```
❌ Gate DEX MCP Server not configured

No MCP Server named "gate-dex" found in current Cursor. Please configure following these steps:

Method 1: Configure through Cursor Settings (Recommended)
  1. Open Cursor → Settings → MCP
  2. Click "Add new MCP server"
  3. Fill in:
     - Name: gate-dex
     - Type: HTTP
     - URL: https://your-mcp-server-domain/mcp
  4. Save and retry

Method 2: Manual configuration file editing
  Edit ~/.cursor/mcp.json, add:
  {
    "mcpServers": {
      "gate-dex": {
        "url": "https://your-mcp-server-domain/mcp"
      }
    }
  }

If you don't have MCP Server service address yet, please contact administrator to obtain it.
```

### Display when remote service unreachable

```
⚠️  Gate DEX MCP Server connection failed

MCP Server configuration found, but cannot connect to remote service. Please check:
1. Confirm service URL is correct (whether currently configured URL is accessible)
2. Check network connection (whether VPN / firewall affects)
3. Confirm remote service is running normally
```

### Display when authentication fails

```
🔑 Gate Wallet MCP Server authentication failed

MCP Server connected but identity verification failed. This service requires valid authentication token.
Please contact administrator for authorization and confirm server-side configuration is correct.
```

## Authentication Instructions

All operations of this Skill **require `mcp_token`**. Must confirm user is logged in before calling any tools.

- If currently no `mcp_token` → Guide to `gate-dex-wallet/references/auth.md` to complete login then return.
- If `mcp_token` expired (MCP Server returns token expired error) → First try `auth.refresh_token` silent refresh, guide re-login on failure.

**Supported Authentication Methods**:
- Google OAuth login (Google Device Flow)
- Gate OAuth login (Gate account system)

**Authentication URL Display Rules**:
- When MCP returns login authorization URL, display complete clickable link directly
- Do not add extra decorative symbols around URL (such as quotes, brackets, etc.)
- Do not escape URL content, ensure users see complete copyable links
- Display format example:

```
Please open the following link in your browser to complete login:

https://accounts.google.com/o/oauth2/device?user_code=ABCD-EFGH

or

https://gate.io/oauth/authorize?client_id=xxx&redirect_uri=xxx

Complete authentication and return here to continue.
```

**Important**: URL must be displayed as plain text, do not use Markdown link format or other decorations.

**Claude Code CLI Specific**: In Claude Code CLI environment, ensure URLs are displayed without any formatting to maintain clickability:

```
🔗 Authentication required. Please visit:

https://accounts.google.com/o/oauth2/device?user_code=ABCD-EFGH

Complete the login and return here to continue trading.
```

## MCP Resource

### `swap://supported_chains` — List of Swap-supported chains

**Must** read this Resource before calling `tx.quote` or `tx.swap` to verify if chain_id supports Swap and determine address grouping (EVM vs Solana).

```
FetchMcpResource(server="gate-dex", uri="swap://supported_chains")
```

Returns chain list grouped by address type (evm / solana), used for:
- Verifying if user-specified chain supports Swap
- Determining whether `user_wallet` should use EVM address or SOL address
- Determining if source and target chains belong to different address groups for cross-chain Swap (requiring `to_wallet`)

## MCP Tool Call Specifications

### 1. `wallet.get_token_list` (Cross-Skill Call) — Query balance for validation

**Must** call this tool before Swap to validate input token balance and Gas token balance. This tool belongs to `gate-dex-wallet` domain, called cross-Skill here.

| Field | Description |
|-------|-------------|
| **Tool Name** | `wallet.get_token_list` |
| **Parameters** | `{ chain?: string, network_keys?: string, account_id?: string, mcp_token: string, page?: number, page_size?: number }` |
| **Return Value** | Token array, each item contains `symbol`, `balance`, `price`, `value`, `chain`, `contract_address`, etc. |

Parameter descriptions:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | No | Single chain query (e.g., `"ETH"`), backward compatible |
| `network_keys` | No | Multi-chain query, comma-separated (e.g., `"ETH,SOL,ARB"`) |
| `account_id` | No | User account ID, can be auto-detected from login session |
| `mcp_token` | Yes | Authentication token |
| `page` | No | Page number, default 1 |
| `page_size` | No | Page size, default 20 |

Call example:

```
CallMcpTool(
  server="gate-dex",
  toolName="wallet.get_token_list",
  arguments={ chain: "ETH", mcp_token: "<mcp_token>" }
)
```

Agent behavior: Extract input token (sell token) balance and chain native token balance (for Gas) from returned list for subsequent balance validation. Also resolve token symbols to contract addresses.

---

### 2. `wallet.get_addresses` (Cross-Skill Call) — Get chain-specific wallet addresses

Both `tx.quote` and `tx.swap` **require** `user_wallet` parameter, must call this tool first to get user wallet addresses on different chain types. This tool belongs to `gate-dex-wallet` domain, called cross-Skill here.

| Field | Description |
|-------|-------------|
| **Tool Name** | `wallet.get_addresses` |
| **Parameters** | `{ account_id: string, mcp_token: string }` |
| **Return Value** | Address mapping, e.g., `{ "EVM": "0x...", "SOL": "5x..." }` |

Parameter descriptions:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `account_id` | Yes | User account ID |
| `mcp_token` | Yes | Authentication token |

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
  "EVM": "0x1234567890abcdef1234567890abcdef12345678",
  "SOL": "5xAbCdEf1234567890abcdef1234567890abcdef12"
}
```

Agent behavior:
- EVM chains (ETH/BSC/Polygon/Arbitrum/Base/Avalanche) → Use `addresses["EVM"]` as `user_wallet`
- Solana (chain_id=501) → Use `addresses["SOL"]` as `user_wallet`
- Cross-chain Swap and source chain differs from target chain address group → Source chain address as `user_wallet`, target chain address as `to_wallet`

---

### 3. `tx.quote` — Get Swap Quote

Get Swap quote from input token to output token, including exchange rate, slippage, route path, estimated Gas and other key information. **Must before calling: ①User confirmed slippage (through AskQuestion selection or explicitly specified in message); ②Read `swap://supported_chains` Resource to verify chain support; ③Call `wallet.get_addresses` to get wallet addresses. Do not call this tool without slippage confirmation.**

| Field | Description |
|-------|-------------|
| **Tool Name** | `tx.quote` |
| **Parameters** | `{ chain_id_in: number, chain_id_out: number, token_in: string, token_out: string, amount: string, slippage: number, user_wallet: string, native_in: number, native_out: number, mcp_token: string, to_wallet?: string }` |
| **Return Value** | Quote information, including estimated output amount, route paths (`routes`), Gas fees, price impact, etc. When `routes[].need_approved` value is 2, it indicates token authorization is needed |

Parameter descriptions:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain_id_in` | Yes | Source chain ID (ETH=1, BSC=56, Polygon=137, Arbitrum=42161, Base=8453, Avalanche=43114, Solana=501) |
| `chain_id_out` | Yes | Target chain ID. For same-chain Swap set same as `chain_id_in`; for cross-chain Swap set to target chain ID |
| `token_in` | Yes | Input token contract address. Use `"-"` for native tokens. Will be auto-normalized to `"-"` if `native_in=1` |
| `token_out` | Yes | Output token contract address. Use `"-"` for native tokens. Will be auto-normalized to `"-"` if `native_out=1` |
| `amount` | Yes | Input token amount (human-readable format, e.g., `"100"`, do not convert to wei/lamports) |
| `slippage` | Yes | Slippage tolerance, **decimal ratio** (`0.01` = 1%, `0.03` = 3%). Range 0.001~0.499. Default `0.03` (3%) |
| `user_wallet` | Yes | User source chain wallet address, obtained from `wallet.get_addresses` |
| `native_in` | Yes | **⚠️ Critical field, wrong value causes transaction failure or fund loss.** Directly check if token_in is native token: native tokens (ETH, BNB, MATIC, AVAX, SOL) = `1`, contract tokens (USDT, USDC, WETH, WBNB, etc.) = `0`. When user says "BNB" default means native token, only explicitly saying "WBNB" means contract token. See below "native_in / native_out judgment rules" |
| `native_out` | Yes | **⚠️ Critical field, wrong value causes transaction failure or fund loss.** Directly check if token_out is native token: native tokens (ETH, BNB, MATIC, AVAX, SOL) = `1`, contract tokens (USDT, USDC, WETH, WBNB, etc.) = `0`. When user says "SOL" default means native token, only explicitly saying "WSOL" means contract token. See below "native_in / native_out judgment rules" |
| `mcp_token` | Yes | Authentication token |
| `to_wallet` | Required for cross-chain | Target chain receiving address. Only needed when cross-chain and source/target chains belong to different address groups (e.g., EVM→Solana) |

#### native_in / native_out Judgment Rules

**These two fields determine how backend handles token address normalization, wrong values will cause transaction failure.** Rules are simple:

**Directly check if token_in / token_out itself is native token (native Gas token):**
- `native_in`: token_in is native token → `1`, is contract token → `0`
- `native_out`: token_out is native token → `1`, is contract token → `0`

Native vs Contract Token Reference Table:

| Native Token (native=1) | Corresponding Wrapped Contract Token (native=0) | Description |
|-------------------------|--------------------------------------------------|-------------|
| ETH | WETH | When user says "ETH" default means native token, only explicitly saying "WETH" means contract token |
| BNB | WBNB | When user says "BNB" default means native token, only explicitly saying "WBNB" means contract token |
| MATIC | WMATIC | When user says "MATIC" default means native token |
| AVAX | WAVAX | When user says "AVAX" default means native token |
| SOL | WSOL | When user says "SOL" default means native token |

Common contract tokens (**always native=0**): USDT, USDC, DAI, CAKE, ARB, OP, RAY, JUP, etc.

**Cross-chain judgment examples:**
- USDT(BSC) → SOL(Solana): token_in=USDT is contract token → `native_in=0`, token_out=SOL is native token → `native_out=1`
- ETH(Ethereum) → USDT(BSC): token_in=ETH is native token → `native_in=1`, token_out=USDT is contract token → `native_out=0`
- USDC(Ethereum) → USDC(Polygon): both are contract tokens → `native_in=0`, `native_out=0`
- ETH(Ethereum) → SOL(Solana): both are native tokens → `native_in=1`, `native_out=1`
- BNB(BSC) → ETH(Ethereum): both are native tokens → `native_in=1`, `native_out=1`

**Common mistakes:**
- ❌ Treating "BNB" as WBNB (contract token) when user says "BNB", should actually be native token native=1
- ❌ Treating WETH/WBNB/WSOL and other Wrapped versions as native tokens (they are contract tokens, native=0)
- ❌ For cross-chain, native_out not passed or defaults to 0, causing backend unable to correctly identify target token

Call example (same-chain Swap: USDT→ETH on ETH):

```
CallMcpTool(
  server="gate-dex",
  toolName="tx.quote",
  arguments={
    chain_id_in: 1,
    chain_id_out: 1,
    token_in: "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    token_out: "-",
    amount: "100",
    slippage: 0.03,
    user_wallet: "0x1234567890abcdef1234567890abcdef12345678",
    native_in: 0,
    native_out: 1,
    mcp_token: "<mcp_token>"
  }
)
```

Call example (cross-chain Swap: ETH→Solana SOL):

```
CallMcpTool(
  server="gate-dex",
  toolName="tx.quote",
  arguments={
    chain_id_in: 1,
    chain_id_out: 501,
    token_in: "-",
    token_out: "-",
    amount: "0.1",
    slippage: 0.03,
    user_wallet: "0x1234...5678",
    native_in: 1,
    native_out: 1,
    to_wallet: "5xAbCd...ef12",
    mcp_token: "<mcp_token>"
  }
)
```

Agent behavior:
1. After getting quote, **must** show quote summary table to user (see "Quote Display Template" below)
2. Calculate **swap value difference** (see calculation formula below), warn user when > 5%
3. Check `need_approved`: when value is 2, inform user token authorization is needed with emphasis
4. **Must not execute Swap directly**, must wait for user confirmation

#### `tx.quote` Return Value Key Field Mapping

| Field Path | Type | Description | Display Purpose |
|------------|------|-------------|-----------------|
| `amount_in` | string | Input token amount (human-readable) | Payment amount |
| `amount_out` | string | Estimated output token amount (human-readable) | Receive amount |
| `min_amount_out` | string | Minimum receive amount (with slippage protection) | Minimum receive |
| `slippage` | string | Actual slippage used (decimal, e.g., `"0.010000"` = 1%) | Slippage info |
| `from_token.token_symbol` | string | Input token symbol | Token name |
| `from_token.token_price` | string | Input token unit price (USD) | Value difference calculation |
| `from_token.chain_name` | string | Input token chain name | Chain info |
| `from_token.chain_id` | number | Input token chain ID | Chain info |
| `to_token.token_symbol` | string | Output token symbol | Token name |
| `to_token.token_price` | string | Output token unit price (USD) | Value difference calculation |
| `to_token.chain_name` | string | Output token chain name | Chain info (different for cross-chain) |
| `estimate_gas_fee_amount` | string | Gas fee (native token amount) | Gas display |
| `estimate_gas_fee_amount_usd` | string | Gas fee (USD) | Gas display |
| `estimate_tx_time` | string | Estimated transaction confirmation time (seconds) | Arrival time |
| `need_approved` | number | Whether token authorization needed (2=needs authorization, other values=no authorization needed) | Authorization prompt |
| `is_signal_chain` | number | 1=same-chain, 2=cross-chain | Cross-chain identifier |
| `provider.name` | string | DEX/aggregator/bridge name | Route display |
| `provider.fee` | string | Service/bridge fee (has value for cross-chain) | Fee display |
| `provider.fee_symbol` | string | Fee token symbol (has value for cross-chain) | Fee display |
| `handlers[].type` | string | `"swap"` = DEX exchange, `"bridge"` = cross-chain bridge | Route type |
| `handlers[].routes[].sub_routes[][].name` | string | Specific DEX/bridge name (e.g., `PANCAKE_V2`, `Bridgers`) | Route details |
| `handlers[].routes[].sub_routes[][].name_in` | string | Route intermediate input token name | Route path |
| `handlers[].routes[].sub_routes[][].name_out` | string | Route intermediate output token name | Route path |
| `trading_fee.rate` | number | Platform trading fee rate (e.g., `0.003` = 0.3%, may have value for same-chain) | Fee display |
| `trading_fee.enable` | boolean | Whether trading fee is enabled | Fee display |
| `pool.liquidity` | string | Total liquidity pool liquidity (USD, has value for same-chain) | Liquidity reference |
| `quote_id` | string | Quote ID (internal identifier) | Log tracking |

#### Swap Value Difference Calculation

```
input_value_usd  = float(amount_in) × float(from_token.token_price)
output_value_usd = float(amount_out) × float(to_token.token_price)
price_diff_pct   = (input_value_usd - output_value_usd) / input_value_usd × 100
```

This value difference includes all comprehensive costs (DEX fees, bridge fees, slippage loss, price impact, etc.), representing the total cost percentage actually borne by the user.

| Value Difference Range | Handling |
|------------------------|----------|
| < 1% | Normal, no additional prompt needed |
| 1% ~ 3% | Normal range, can be noted in quote |
| 3% ~ 5% | Prompt "high swap value difference" |
| > 5% | **Key warning**: Show value difference details, use AskQuestion to let user confirm acceptance (see "Swap Value Difference > 5% Mandatory Warning" template) |

---

### 4. `tx.swap` — Execute Swap (One-shot)

One-shot Swap: Quote→Build→Sign→Submit completed in single call. Eliminates multiple round-trip delays (solves Solana blockhash expiration issue). Internal maximum 3 retries.

**Only call after completing three-step confirmation SOP (see operation flow below).**

| Field | Description |
|-------|-------------|
| **Tool Name** | `tx.swap` |
| **Parameters** | `{ chain_id_in: number, chain_id_out: number, token_in: string, token_out: string, amount: string, slippage: number, user_wallet: string, native_in: number, native_out: number, account_id: string, mcp_token: string, to_wallet?: string }` |

#### Success Return Value

| Field | Type | Description |
|-------|------|-------------|
| `tx_hash` | string | On-chain transaction hash |
| `tx_order_id` | string | Internal order ID for `tx.swap_detail` polling |
| `amount_in` | string | Actual input amount (human-readable) |
| `amount_out` | string | Estimated output amount (human-readable) |
| `from_token` | string | Input token symbol |
| `to_token` | string | Output token symbol |
| `slippage` | number | Slippage used (decimal) |
| `route_path` | string[] | List of DEX names in route |
| `need_approved` | boolean | Whether ERC20 authorization was executed |
| `status` | string | Fixed as `"submitted"` |
| `message` | string | `"Transaction submitted. Poll tx.swap_detail with tx_order_id every 5s."` |

#### Failure Return Value (all 3 retries failed)

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Fixed as `"failed"` |
| `message` | string | `"Swap failed after 3 attempts"` |
| `attempts` | array | Details array for each attempt, each item contains `attempt` (sequence number), `error` (error message) |

Parameter descriptions:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain_id_in` | Yes | Source chain ID |
| `chain_id_out` | Yes | Target chain ID. Same as `chain_id_in` for same-chain Swap |
| `token_in` | Yes | Input token contract address, native token `"-"` |
| `token_out` | Yes | Output token contract address, native token `"-"` |
| `amount` | Yes | Human-readable amount (e.g., `"0.01"`) |
| `slippage` | Yes | Slippage, decimal ratio (`0.01`=1%, `0.03`=3%) |
| `user_wallet` | Yes | Source chain wallet address |
| `native_in` | Yes | **⚠️ Critical field, same rules as tx.quote.** Directly check if token_in is native token: native tokens (ETH/BNB/MATIC/AVAX/SOL) = `1`, contract tokens = `0`. When user says "BNB" default means native token. See tx.quote "native_in / native_out judgment rules" above |
| `native_out` | Yes | **⚠️ Critical field, same rules as tx.quote.** Directly check if token_out is native token: native tokens (ETH/BNB/MATIC/AVAX/SOL) = `1`, contract tokens = `0`. When user says "SOL" default means native token. See tx.quote "native_in / native_out judgment rules" above |
| `account_id` | Yes | User account ID (UUID) |
| `mcp_token` | Yes | Authentication token |
| `to_wallet` | Required for cross-chain | Target chain receiving address (needed when crossing different address groups) |

Call example:

```
CallMcpTool(
  server="gate-dex",
  toolName="tx.swap",
  arguments={
    chain_id_in: 1,
    chain_id_out: 1,
    token_in: "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    token_out: "-",
    amount: "100",
    slippage: 0.03,
    user_wallet: "0x1234567890abcdef1234567890abcdef12345678",
    native_in: 0,
    native_out: 1,
    account_id: "acc_12345",
    mcp_token: "<mcp_token>"
  }
)
```

Return example (success):

| Field | Example Value |
|-------|---------------|
| `tx_hash` | `0xa1b2c3d4e5f6...7890` |
| `tx_order_id` | `order_abc123` |
| `amount_in` | `100` |
| `amount_out` | `0.052` |
| `from_token` | `USDT` |
| `to_token` | `ETH` |
| `slippage` | `0.03` |
| `route_path` | `["PANCAKE_V2"]` |
| `need_approved` | `false` |
| `status` | `submitted` |
| `message` | `Transaction submitted. Poll tx.swap_detail with tx_order_id every 5s.` |

Return example (failure):

| Field | Example Value |
|-------|---------------|
| `status` | `failed` |
| `message` | `Swap failed after 3 attempts` |
| `attempts[0].error` | `insufficient balance` |
| `attempts[1].error` | `quote failed: liquidity too low` |
| `attempts[2].error` | `quote failed: liquidity too low` |

Agent behavior:
- Success (`status == "submitted"`) → Show user `tx_hash` with label, `from_token`/`to_token`, `amount_in`/`amount_out`, display block explorer URL as plain text (no hyperlinks), then poll `tx.swap_detail` with `tx_order_id`
- Failure (`status == "failed"`) → Show `message` and each `attempts[].error`, do not auto-retry, suggest user re-get quote

**Output Format Requirements**:
- Display transaction hash and block explorer URL as plain text, never as clickable hyperlinks
- Use labels "Transaction Hash:" and "Block Explorer:" for clarity
- Preserve the exact hash string without modifications or escaping

---

### 5. `tx.swap_detail` — Query Swap Status

Query execution result and detailed information of submitted Swap transaction. Use `tx_order_id` returned by `tx.swap` to query.

| Field | Description |
|-------|-------------|
| **Tool Name** | `tx.swap_detail` |
| **Parameters** | `{ tx_order_id: string, mcp_token: string }` |
| **Return Value** | Swap transaction details, including status, token information, timestamp, Gas fees, etc. |

Parameter descriptions:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `tx_order_id` | Yes | `tx_order_id` returned by `tx.swap` |
| `mcp_token` | Yes | Authentication token |

Return value key fields:

| Field | Type | Description |
|-------|------|-------------|
| `status` | number | Transaction status: 0=success, 3=failed |
| `tokenInSymbol` | string | Input token symbol |
| `tokenOutSymbol` | string | Output token symbol |
| `amountIn` | string | Input amount (minimum unit) |
| `amountOut` | string | Output amount (minimum unit) |
| `tokenInDecimals` | number | Input token decimals |
| `tokenOutDecimals` | number | Output token decimals |
| `srcHash` | string | On-chain transaction hash |
| `srcHashExplorerUrl` | string | Block explorer URL prefix |
| `unifyGasFee` | string | Actual Gas fee (minimum unit) |
| `unifyGasFeeDecimal` | number | Gas token decimals |
| `unifyGasFeeSymbol` | string | Gas token symbol |
| `gasFeeUsd` | string | Actual Gas fee (USD) |
| `creationTime` | string | Transaction creation time (ISO8601) |
| `errorCode` | number | Error code (0=no error) |
| `errorMsg` | string | Error message (has value when failed) |

Gas fee human-readable conversion: `float(unifyGasFee) / 10^unifyGasFeeDecimal`, unit is `unifyGasFeeSymbol`.

Call example:

```
CallMcpTool(
  server="gate-dex",
  toolName="tx.swap_detail",
  arguments={
    tx_order_id: "order_abc123",
    mcp_token: "<mcp_token>"
  }
)
```

Return value `status` meanings:

| status | Meaning | Next Action |
|--------|---------|-------------|
| `pending` | Transaction pending confirmation | Poll every 5 seconds, maximum 3 minutes; if timeout, guide user to check via `tx.history_list` |
| `success` | Swap completed successfully | Show final result to user |
| `failed` | Swap failed | Show failure reason, suggest re-getting quote |

## Supported Chains

| chain_id | Network Name | Type | Native Gas Token | Block Explorer | chain.config Identifier |
|----------|--------------|------|------------------|----------------|-------------------------|
| `1` | Ethereum | EVM | ETH | etherscan.io | `ETH` |
| `56` | BNB Smart Chain | EVM | BNB | bscscan.com | `BSC` |
| `137` | Polygon | EVM | MATIC | polygonscan.com | `POLYGON` |
| `42161` | Arbitrum One | EVM | ETH | arbiscan.io | `ARB` |
| `10` | Optimism | EVM | ETH | optimistic.etherscan.io | `OP` |
| `43114` | Avalanche C-Chain | EVM | AVAX | snowtrace.io | `AVAX` |
| `8453` | Base | EVM | ETH | basescan.org | `BASE` |
| `501` | Solana | Non-EVM | SOL | solscan.io | `SOL` |

Common chain_ids can be used directly, only need to call `chain.config` query for uncommon chains.

**Before calling `tx.quote` / `tx.swap`, must first read `swap://supported_chains` Resource to confirm chain supports Swap.**

## Token Address Resolution

When Agent collects Swap parameters, need to convert user-provided token names/symbols to contract addresses and native flags:

| User Input | Resolution Method | `token_in`/`token_out` | `native_in`/`native_out` |
|------------|-------------------|------------------------|--------------------------|
| Native tokens (ETH, BNB, SOL, MATIC, AVAX) | Mark as native | `"-"` | `1` |
| Token symbols (like USDT, USDC) | Match `symbol` from `wallet.get_token_list` returned holdings to get `contract_address` | Contract address | `0` |
| Contract address (like `0xdAC17...`) | Use directly | Pass as-is | `0` |

**⚠️ Native flag judgment rule: directly check if token itself is native token**
- `native_in`: token_in is native token (ETH/BNB/SOL/MATIC/AVAX) → `1`, contract token → `0`
- `native_out`: token_out is native token → `1`, contract token → `0`
- When user says "BNB" default means native token (native=1), only explicitly saying "WBNB" means contract token (native=0). ETH vs WETH, SOL vs WSOL same logic
- WETH, WBNB, WSOL and other Wrapped versions are **contract tokens** (native=0), not native tokens

When user-provided token symbol not found in holdings:
- Prompt user to confirm token name is correct
- Prompt user to provide contract address
- Suggest using `gate-dex-market` (`token_get_coin_info`) to query token information for contract address

## MCP Tool Call Chain Overview

Complete Swap flow calls following tools in sequence, forming strict linear pipeline:

```
0.  chain.config                                      ← Step 0: MCP Server prerequisite check
1.  FetchMcpResource(swap://supported_chains)         ← Verify chain supports Swap + address grouping
2.  wallet.get_token_list                             ← Cross-Skill: Check balance (input token + Gas token) + resolve token addresses
3.  wallet.get_addresses                              ← Cross-Skill: Get chain-specific wallet addresses (user_wallet / to_wallet)
4.  [Agent balance validation: input token balance >= amount]  ← Agent internal logic, not MCP call
5.  [Agent display trading pair confirmation Table, wait user confirmation]  ← tx.swap SOP Step 1 (mandatory gate)
6.  tx.quote                                          ← Get quote (estimated output, route, Gas, price impact)
7.  [Agent display quote details + check need_approved]  ← tx.swap SOP Step 2 (mandatory gate)
8.  [Agent signature authorization confirmation, wait user confirmation]  ← tx.swap SOP Step 3 (mandatory gate)
9.  tx.swap                                           ← One-shot execution (Quote→Build→Sign→Submit)
10. tx.swap_detail (by tx_order_id, poll every 5s)    ← Query Swap execution result (optional, poll as needed)
```

## Skill Routing

Based on user intent after Swap completion, guide to corresponding Skill:

| User Intent | Routing Target |
|-------------|----------------|
| View updated balance | `gate-dex-wallet` |
| View Swap transaction history | `gate-dex-wallet` (`tx.history_list`) |
| Continue Swap other tokens | Stay in this Skill |
| Transfer newly swapped tokens | `gate-dex-wallet/references/transfer.md` |
| View token market / K-line | `gate-dex-market` |
| Login / authentication expired | `gate-dex-wallet/references/auth.md` |

## Operation Flows

### Flow A: Standard Swap (Main Flow)

```
Step 0: MCP Server prerequisite check
  Call chain.config({chain: "ETH"}) to test availability
  ↓ Success

Step 1: Authentication check
  Confirm holding valid mcp_token and account_id
  No token → Guide to gate-dex-wallet/references/auth.md login
  ↓

Step 2: Intent recognition + parameter collection
  Extract Swap intent from user input, collect following necessary parameters:
  - from_token: Input token (required, like USDT)
  - to_token: Output token (required, like ETH)
  - amount: Input amount (required, like 100)
  - chain: Target chain (optional, can be inferred from token or context, default Ethereum chain_id=1)
  - slippage: Slippage tolerance (optional, see interactive selection below)

  When missing from_token / to_token / amount, ask user for each item.

  **Slippage Selection**: If user already specified slippage in message, use directly without asking.
  If not specified, use AskQuestion tool for user interactive selection:

  ```
AskQuestion({
title: "Slippage Settings",
questions: [{
id: "slippage",
prompt: "Please select slippage tolerance (affects minimum receive amount)",
options: [
{ id: "0.005", label: "0.5% (recommended for stablecoins)" },
{ id: "0.01",  label: "1% (recommended for major tokens)" },
{ id: "0.03",  label: "3% (default, recommended for volatile tokens)" },
{ id: "0.05",  label: "5% (low liquidity tokens)" },
{ id: "custom", label: "Custom" }
]
}]
})
  ```

  User selects "Custom" → Follow up for specific value (input percentage, Agent converts to decimal ratio)
  ↓ Parameters complete

Step 3: Verify chain support
  Read swap://supported_chains Resource
  Confirm user-specified chain chain_id is in supported list
  Determine address grouping (EVM / Solana)
  ↓

Step 4: Query balance (Cross-Skill: gate-dex-wallet)
  Call wallet.get_token_list({ chain: "ETH", mcp_token })
  Extract:
  - Input token balance (like USDT balance)
  - Chain native Gas token balance (like ETH balance)
  Also resolve user-provided token symbols to contract addresses (token_in, token_out) and native flags
  ↓

Step 5: Get wallet addresses (Cross-Skill: gate-dex-wallet)
  Call wallet.get_addresses({ account_id, mcp_token })
  Get user_wallet based on source chain type:
  - EVM chains → addresses["EVM"]
  - Solana → addresses["SOL"]
  Cross-chain Swap and different address groups → Also need to get to_wallet
  ↓

Step 6: Agent balance validation (mandatory)
  Validation rules:
  a) Input token is native token: balance >= amount + estimated_gas (Gas precisely validated after quote)
  b) Input token is ERC20/SPL: token_balance >= amount and native_balance > 0 (ensure has Gas)

  Validation failed → Abort Swap, show insufficient information:

  ────────────────────────────
  ❌ Insufficient balance, cannot execute Swap

  Input token: USDT
  Swap amount: 100 USDT
  Current USDT balance: 80 USDT (insufficient, short 20 USDT)

  Suggestions:
  - Reduce Swap amount
  - First deposit tokens to wallet
  ────────────────────────────

  ↓ Validation passed

Step 7: SOP Step 1 — Confirm trading pair (mandatory gate)
  Show trading pair confirmation Table to user, use AskQuestion for user confirmation:

  | Field | Value |
  |-------|-------|
  | from_token | {symbol}({contract_address}) |
  | to_token | {symbol}({contract_address}) |
  | amount | {amount} |
  | chain | {chain_name} (chain_id={chain_id}) |
  | slippage | {slippage}% (user selected) |

  AskQuestion({
    title: "Trading Pair Confirmation",
    questions: [{
      id: "trade_confirm",
      prompt: "Please confirm the above transaction information is correct",
      options: [
        { id: "confirm", label: "Confirm, continue to get quote" },
        { id: "modify_slippage", label: "Modify slippage" },
        { id: "modify_amount", label: "Modify amount" },
        { id: "cancel", label: "Cancel transaction" }
      ]
    }]
  })

  User selects confirm → Continue
  User selects modify_slippage → Re-popup AskQuestion slippage selection
  User selects modify_amount → Ask for new amount then re-display Table
  User selects cancel → Abort Swap
  (When AskQuestion unavailable, fallback to text reply)
  ↓ User confirmed

Step 8: SOP Step 2 — Get quote and display (mandatory gate, cannot skip)
  Call tx.quote({
    chain_id_in, chain_id_out, token_in, token_out, amount, slippage,
    user_wallet, native_in, native_out, mcp_token, to_wallet?
  })

  Must show user:
  - Estimated received to_token amount
  - Route/DEX path
  - Estimated Gas fee
  - Price impact (warn when > 5%)
  - Authorization requirement (inform when need_approved == 2 about token authorization needed)
  ↓

Step 9: Quote risk assessment (Agent internal logic)
  Check risk indicators in quote:
  a) Swap value difference (price_diff_pct):
     input_value_usd  = float(amount_in) × float(from_token.token_price)
     output_value_usd = float(amount_out) × float(to_token.token_price)
     price_diff_pct   = (input_value_usd - output_value_usd) / input_value_usd × 100
     - < 1%: Normal
     - 1% ~ 3%: Normal range
     - 3% ~ 5%: Prompt "high swap value difference"
     - > 5%: **Key warning** — Show input_value_usd, output_value_usd, difference, use AskQuestion for user confirmation (see "Swap Value Difference > 5% Mandatory Warning" template)
  b) Slippage:
     - User setting > 5% (i.e., > 0.05): Warn "high slippage setting, actual execution price may deviate significantly"
  c) Gas fee:
     - Gas fee percentage of Swap amount > 10%: Prompt "Gas fee percentage is high, suggest increasing Swap amount or waiting for network idle"
  d) Native token Gas balance precise validation:
     - native_balance < estimated_gas → Abort, prompt Gas insufficient
  ↓

Step 10: SOP Step 3 — Signature authorization confirmation (mandatory gate)
  Inform user:
  "Next step will involve contract authorization or transaction signing. This is necessary step for executing transaction.
   After confirmation, system will automatically complete Quote→Build→Sign→Submit full process."

  Use AskQuestion for user final confirmation:

  AskQuestion({
    title: "Signature Authorization Confirmation",
    questions: [{
      id: "sign_confirm",
      prompt: "Confirm execute transaction? System will automatically complete signing and submission",
      options: [
        { id: "confirm", label: "Confirm execute" },
        { id: "modify", label: "Modify slippage/amount" },
        { id: "cancel", label: "Cancel transaction" }
      ]
    }]
  })

  (When AskQuestion unavailable, fallback to text reply)
  ↓

  User selects confirm → Continue Step 11
  User selects cancel → Abort Swap, show cancellation prompt
  User selects modify → Return to Step 7 re-display trading pair Table and re-get quote

Step 11: Execute Swap (One-shot)
  Call tx.swap({
    chain_id_in, chain_id_out, token_in, token_out, amount, slippage,
    user_wallet, native_in, native_out, account_id, mcp_token, to_wallet?
  })
  Get tx_hash and tx_order_id
  ↓

Step 12: Query Swap result (as needed)
  Call tx.swap_detail({ tx_order_id, mcp_token })
  Poll every 5 seconds, maximum 3 minutes (about 36 times), until final state:
  - status == "pending" → Inform user transaction pending confirmation, continue polling
  - status == "success" → Show final execution result
  - status == "failed" → Show failure information
  - Over 3 minutes still "pending" → Stop polling, inform user:
    "Current transaction still processing, please check result later via transaction list."
    Guide user to call tx.history_list({ account_id, mcp_token }) to view Swap transaction history
  ↓

Step 13: Display result + follow-up suggestions

  ────────────────────────────
  ✅ Swap executed successfully!

  Input: 100 USDT
  Received: 0.0521 ETH
  Gas fee: 0.00069778 ETH (≈ $1.46)
  Transaction Hash: {tx_hash}
  Block Explorer: https://{explorer}/tx/{tx_hash}

  You can:
  - View updated balance
  - View Swap history
  - Continue other operations
  ────────────────────────────
```

### Flow B: Modify slippage then re-quote

```
Trigger condition: User requests to modify slippage during confirmation steps
  ↓
Step 1: Record new slippage value
  User specifies new slippage (like "change slippage to 1%")
  Convert to decimal ratio (1% → 0.01)
  ↓
Step 2: Re-get quote
  Re-call tx.quote with new slippage (other parameters unchanged)
  ↓
Step 3: Re-display quote details
  Show updated quote information (new minimum output amount will change)
  ↓
  Wait for user confirmation again or continue modification
  After confirmation enter signature authorization confirmation (SOP Step 3)
```

### Flow C: Query Swap transaction status

```
Step 0: MCP Server prerequisite check
  ↓ Success

Step 1: Authentication check
  ↓

Step 2: Query Swap status
  Call tx.swap_detail({ tx_order_id, mcp_token })
  ↓

Step 3: Display status

  ── Swap Status ──────────────
  Order ID: {tx_order_id}
  Status: {status} (success / pending confirmation / failed)
  Input: {from_amount} {from_token}
  Output: {to_amount} {to_token}
  Gas fee: {gas_fee} {gas_symbol} (≈ ${gas_fee_usd})
  Transaction Hash: {tx_hash}
  Block Explorer: https://{explorer}/tx/{tx_hash}
  ────────────────────────────
```

### Flow D: Cross-chain Swap

```
Trigger condition: User wants to swap A chain assets to B chain (like USDT on ETH → SOL on Solana)
  ↓
Step 1: Verify cross-chain support
  Read swap://supported_chains Resource
  Confirm both chain_id_in and chain_id_out are in supported list
  Determine address grouping: whether source and target chains belong to different address groups
  ↓

Step 2: Get wallet addresses
  Call wallet.get_addresses({ account_id, mcp_token })
  - user_wallet = source chain address (like EVM address)
  - to_wallet = target chain address (like SOL address, only needed when crossing different address groups)
  ↓

Step 3: Follow same process as Flow A from Step 6 onwards
  Set chain_id_in != chain_id_out in tx.quote and tx.swap
  And pass to_wallet parameter
```

## Swap Confirmation Templates

**Must complete three-step confirmation SOP before `tx.swap` execution, each step is mandatory gate that cannot be skipped.**

### Interaction Strategy

For all gate steps requiring user confirmation/cancellation input, **prioritize using `AskQuestion` tool** for structured options to improve interaction efficiency:
- When `AskQuestion` available: Let users quickly select via option buttons (confirm, cancel, modify parameters, etc.)
- When `AskQuestion` unavailable (tool call failed or platform unsupported): Fallback to text reply mode, prompt user to reply "confirm"/"cancel"

### SOP Step 1: Trading Pair Confirmation Table

Display following Table, then use `AskQuestion` for user confirmation or modification:

```
| Field | Value |
|-------|-------|
| from_token | {from_symbol}({from_contract_address}) |
| to_token | {to_symbol}({to_contract_address}) |
| amount | {amount} |
| chain | {chain_name} (chain_id={chain_id_in}) |
| slippage | {slippage}% (user selected) |
```

**Interaction Method (prioritize AskQuestion)**:

```
AskQuestion({
  title: "Trading Pair Confirmation",
  questions: [{
    id: "trade_confirm",
    prompt: "Please confirm the above transaction information is correct",
    options: [
      { id: "confirm", label: "Confirm, continue to get quote" },
      { id: "modify_slippage", label: "Modify slippage" },
      { id: "modify_amount", label: "Modify amount" },
      { id: "cancel", label: "Cancel transaction" }
    ]
  }]
})
```

| User Selection | Handling |
|----------------|----------|
| `confirm` | Continue to SOP Step 2 (get quote) |
| `modify_slippage` | Popup slippage selection AskQuestion, update and re-display Table |
| `modify_amount` | Ask for new amount, update and re-display Table |
| `cancel` | Abort Swap, show cancellation prompt |

**Fallback Mode**: If `AskQuestion` unavailable, prompt user to reply "confirm" to continue, "cancel" to abort, or directly specify parameters to modify.

### SOP Step 2: Quote Details Display

After calling `tx.quote`, must display quote summary in table format. Same template for same-chain/cross-chain, automatically adapts display items based on return data.

#### Universal Quote Template

```
Quote Summary

| Item | Content |
|------|---------|
| Chain | {chain info} |
| Pay | {amount_in} {from_token.token_symbol} |
| Receive | ≈ {amount_out} {to_token.token_symbol} |
| Minimum Receive | ≈ {min_amount_out} {to_token.token_symbol} (with {slippage×100}% slippage protection) |
| Exchange Rate | 1 {from_token.token_symbol} ≈ {amount_out/amount_in} {to_token.token_symbol} |
| Swap Value Difference | ≈ {price_diff_pct}% |
| Route | {route info} |
| Fees | {fee info} |
| Estimated Gas | {estimate_gas_fee_amount} {gas_symbol} (≈ ${estimate_gas_fee_amount_usd}) |
| Estimated Time | ≈ {estimate_tx_time} seconds |
| Liquidity | ${pool.liquidity} |
| Authorization | {need_approved description} |
```

#### Field Value Rules

| Display Item | Value Logic |
|-------------|-------------|
| **Chain** | Same-chain (`is_signal_chain == 1`) → `from_token.chain_name`; Cross-chain (`is_signal_chain == 2`) → `from_token.chain_name → to_token.chain_name` |
| **Exchange Rate** | `float(amount_out) / float(amount_in)`, add chain name after token symbol for cross-chain distinction |
| **Swap Value Difference** | `(input_value_usd - output_value_usd) / input_value_usd × 100` (see calculation method above) |
| **Route** | `provider.name` + `handlers[].routes[].sub_routes[][].name`; mark "cross-chain bridge" for cross-chain |
| **Fees** | `trading_fee.enable == true` → `trading_fee.rate × 100`% (trading fee); `provider.fee` has value → `provider.fee provider.fee_symbol` (bridge/service fee); omit if none |
| **Gas Token** | Source chain native token (BSC=BNB, ETH=ETH, Solana=SOL, etc.) |
| **Liquidity** | Display when `pool.liquidity` has value, omit this row when no value |
| **Authorization** | `need_approved == 2` → "⚠️ Need to authorize {from_symbol} contract first (Token Approval), system will handle automatically"; other values → "No authorization needed ✅" |
| **Cross-chain Note** | When `is_signal_chain == 2`, append below table: "Cross-chain transactions involve bridging, actual arrival time may extend due to network congestion." |

#### Example 1: Same-chain Swap (BNB → DOGE on BSC)

```
Quote Summary

| Item | Content |
|------|---------|
| Chain | BNB Smart Chain |
| Pay | 0.001 BNB |
| Receive | ≈ 4.634 DOGE |
| Minimum Receive | ≈ 4.588 DOGE (with 1% slippage protection) |
| Exchange Rate | 1 BNB ≈ 4634 DOGE |
| Swap Value Difference | ≈ 0.67% |
| Route | PancakeSwap V2 (PANCAKE_V2) |
| Fees | 0.3% (trading fee) |
| Estimated Gas | 0.0000063 BNB (≈ $0.0041) |
| Estimated Time | ≈ 49 seconds |
| Liquidity | $878,530 |
| Authorization | Need to authorize BNB contract |
```

#### Example 2: Cross-chain Swap (Solana USDT → Ethereum USDT)

```
Quote Summary

| Item | Content |
|------|---------|
| Chain | Solana → Ethereum |
| Pay | 1.707168 USDT |
| Receive | ≈ 1.652046 USDT |
| Minimum Receive | ≈ 1.569443 USDT (with 5% slippage protection) |
| Exchange Rate | 1 USDT (Solana) ≈ 0.9677 USDT (ETH) |
| Swap Value Difference | ≈ 3.27% |
| Route | MetaPath (via Bridgers cross-chain bridge) |
| Fees | 0.005122 USDT (bridge/service fee) |
| Estimated Gas | 0.00000687 SOL (≈ $0.022) |
| Estimated Time | ≈ 10 seconds |
| Authorization | No authorization needed ✅ |

Note: Swap value difference is 3.27%, meaning pay ≈ $1.71 value tokens,
receive ≈ $1.65 value tokens, difference mainly from cross-chain bridge fees and slippage.
Cross-chain transaction actual arrival time may extend due to network congestion.
```

#### Swap Value Difference > 5% Mandatory Warning

When swap value difference exceeds 5%, **must** append prominent warning below quote table and confirm via `AskQuestion`:

```
⚠️ Important Warning: Swap value difference reaches {price_diff_pct}%!
Pay ≈ ${input_value_usd} value tokens, only receive ≈ ${output_value_usd} value tokens.
Difference ≈ ${diff_usd}, mainly from DEX fees, bridge fees, slippage loss and other comprehensive costs.
Strongly suggest: reduce transaction volume, batch execution, or wait for better quotes.
```

**Interaction Method (prioritize AskQuestion)**:

```
AskQuestion({
  title: "⚠️ High Value Difference Warning",
  questions: [{
    id: "price_diff_confirm",
    prompt: "Swap value difference reaches {price_diff_pct}%, confirm accept this swap rate?",
    options: [
      { id: "confirm", label: "I understand risks, continue execution" },
      { id: "reduce", label: "Reduce transaction amount" },
      { id: "cancel", label: "Cancel transaction" }
    ]
  }]
})
```

| User Selection | Handling |
|----------------|----------|
| `confirm` | Continue to SOP Step 3 signature confirmation |
| `reduce` | Ask for new amount, return to SOP Step 1 to re-run process |
| `cancel` | Abort Swap |

**Fallback Mode**: If `AskQuestion` unavailable, prompt user to reply "confirm" to continue, "cancel" to abort.

### SOP Step 3: Signature Authorization Confirmation

Display prompt text, then use `AskQuestion` for user final confirmation:

```
Next step will involve contract authorization and transaction signing. This is necessary step for executing transaction.
After confirmation, system will automatically complete Quote→Build→Sign→Submit full process.
```

**Interaction Method (prioritize AskQuestion)**:

```
AskQuestion({
  title: "Signature Authorization Confirmation",
  questions: [{
    id: "sign_confirm",
    prompt: "Confirm execute transaction? System will automatically complete signing and submission",
    options: [
      { id: "confirm", label: "Confirm execute" },
      { id: "modify", label: "Modify slippage/amount" },
      { id: "cancel", label: "Cancel transaction" }
    ]
  }]
})
```

| User Selection | Handling |
|----------------|----------|
| `confirm` | Execute `tx.swap` |
| `modify` | Return to SOP Step 1 re-display trading pair Table and re-get quote |
| `cancel` | Abort Swap, show cancellation prompt |

**Fallback Mode**: If `AskQuestion` unavailable, prompt user to reply "confirm" to execute, "cancel" to abort, or specify parameters to modify.

### High Slippage Warning (slippage > 5%, i.e., > 0.05)

In SOP Step 1 Table and Step 2 quote display, additionally append:

```
⚠️ Warning: Current slippage setting is {slippage×100}%, far higher than normal level (3%).
This means actual execution price may deviate significantly from quote. Unless you confirm need high slippage (like trading low liquidity tokens), suggest reducing slippage.
⚠️ High slippage settings may be subject to MEV/sandwich attacks.
```

## Cross-Skill Workflows

### Complete Swap Flow (from login to completion)

```
gate-dex-wallet/references/auth.md (login, get mcp_token + account_id)
  → gate-dex-wallet (wallet.get_token_list → validate balance + resolve token addresses)
  → gate-dex-wallet (wallet.get_addresses → get chain-specific wallet addresses)
    → gate-dex-trade/references/mcp.md (trading pair confirmation → tx.quote → quote display → signature authorization confirmation → tx.swap → tx.swap_detail)
      → gate-dex-wallet (view updated balance)
```

### Query and Buy Workflow

```
gate-dex-market (token_get_coin_info → query token info/market)
  → gate-dex-market (token_get_risk_info → security audit)
    → gate-dex-wallet (wallet.get_token_list → validate balance)
      → gate-dex-trade/references/mcp.md (quote → confirm → execute)
```

### Security Audit then Trade Workflow

```
gate-dex-market (token_get_risk_info → token security audit)
  → gate-dex-market (token_get_coin_info → token details)
    → gate-dex-trade/references/mcp.md (execute Swap if safe)
```

### Guided by Other Skills

| Source Skill | Scenario | Description |
|--------------|----------|-------------|
| `gate-dex-wallet` | User wants to swap tokens after viewing balance | Carries account_id, chain and holdings information |
| `gate-dex-market` | User wants to buy certain token after viewing market | Carries token information and chain context |
| `gate-dex-wallet/references/transfer.md` | Want to swap remaining tokens after transfer | Carries chain and token context |

### Calling Other Skills

| Target Skill | Call Scenario | Used Tools |
|--------------|---------------|------------|
| `gate-dex-wallet` | Check balance and resolve token addresses before Swap | `wallet.get_token_list` |
| `gate-dex-wallet` | Get chain-specific wallet addresses before Swap | `wallet.get_addresses` |
| `gate-dex-wallet` | View updated balance after Swap | `wallet.get_token_list` |
| `gate-dex-wallet/references/auth.md` | Not logged in or token expired | `auth.refresh_token` or complete login process |
| `gate-dex-market` | Query token info to help resolve addresses | `token_get_coin_info` |
| `gate-dex-market` | Security audit target token before Swap | `token_get_risk_info` |
| `gate-dex-wallet` | View Swap history | `tx.history_list` |

## Slippage Instructions

Slippage is key parameter in Swap transactions, controlling maximum allowed deviation between actual execution price and quoted price. Pass to `tx.quote` / `tx.swap` using **decimal ratio** (like `0.03` means 3%), convert to percentage when displaying to users.

| Slippage Range | Decimal Ratio | Applicable Scenarios | Description |
|----------------|---------------|---------------------|-------------|
| 0.5% ~ 1% | 0.005 ~ 0.01 | Stablecoin pairs (USDT/USDC, etc.) | Sufficient liquidity, low slippage can execute |
| 1% ~ 3% | 0.01 ~ 0.03 | Volatile tokens | Default recommended range |
| 3% ~ 5% | 0.03 ~ 0.05 | Low liquidity tokens / meme tokens | Need to prompt user about price deviation |
| > 5% | > 0.05 | Extremely low liquidity / high volatility | Need to warn user, may be subject to MEV/sandwich attacks |

**Default Slippage**: `0.03` (3%). If user already specified slippage in message, use directly without asking. Only ask for confirmation when not provided.

## Edge Cases and Error Handling

| Scenario | Handling Method |
|----------|-----------------|
| MCP Server not configured | Abort all operations, show Cursor configuration guide |
| MCP Server unreachable | Abort all operations, show network check prompt |
| Not logged in (no `mcp_token`) | Guide to `gate-dex-wallet/references/auth.md` complete login then auto-return continue Swap |
| `mcp_token` expired | First try `auth.refresh_token` silent refresh, guide re-login on failure |
| Chain not support Swap | After reading `swap://supported_chains` find unsupported → Show supported chain list, ask user re-select |
| Input token balance insufficient | Abort Swap, show current balance vs required amount difference, suggest reducing amount or deposit first |
| Gas token balance insufficient | Abort Swap, show Gas token insufficient info, suggest getting Gas token first |
| Token symbol cannot resolve to contract address | Prompt user confirm token name or provide contract address, suggest using `gate-dex-market` query |
| `tx.quote` failed | Show error info (possible reasons: token pair doesn't exist, insufficient liquidity, network congestion). Suggest changing token pair or retry later |
| Swap value difference > 5% | **Key warning** user, show USD value comparison and difference, suggest reducing transaction volume or batch execution. Can still continue after user insists |
| Slippage > 5% (i.e., > 0.05) | Warn user high slippage risk and MEV attack risk, suggest reducing. Can still continue after user insists |
| Gas fee percentage of Swap amount > 10% | Prompt user Gas cost is high, suggest increasing Swap amount or waiting for network idle |
| `tx.swap` failed | Show failure reason (like balance change, slippage exceeded, network issues). Don't auto-retry, suggest re-getting quote |
| `tx.swap_detail` returns `failed` after Swap | Show failure reason, suggest re-getting quote to execute Swap. Token balance may be unchanged |
| `tx.swap_detail` continues `pending` after Swap | Poll maximum 3 minutes; after timeout stop polling, inform user transaction still processing, guide to check result via `tx.history_list` |
| Input and output tokens are same | Refuse execution, prompt input and output tokens cannot be same |
| Input amount is 0 or negative | Refuse execution, prompt enter valid positive amount |
| Cannot find specified token pair on target chain | Prompt this chain doesn't support this token pair Swap, suggest trying on other chains |
| User cancels confirmation (any step of three-step SOP) | Immediately abort, don't execute Swap. Show cancellation prompt, stay friendly |
| Cross-chain Swap different address groups but missing to_wallet | Auto-get target chain address from `wallet.get_addresses` as `to_wallet` |
| EVM address mistakenly used for Solana (or vice versa) | Auto-select correct address based on chain_id and `swap://supported_chains` address grouping |
| Network interruption | Show network error, suggest checking network then retry |

## Security Rules

1. **`mcp_token` Confidentiality**: Never show `mcp_token` in plain text to users, only use placeholder `<mcp_token>` in call examples.
2. **`account_id` Desensitization**: When displaying to users only show partial characters (like `acc_12...89`).
3. **Token Auto-refresh**: When `mcp_token` expires, prioritize silent refresh attempt, only require re-login on failure.
4. **Authentication URL Correct Display**: When MCP returns login authorization URL, display complete clickable link directly, don't add extra decorations (quotes, brackets, etc.), don't escape URL content, ensure users can directly copy and click.
5. **Multiple Authentication Method Support**: Support Google OAuth and Gate OAuth login, users can choose either method.
6. **Balance Validation Mandatory**: **Must** validate input token balance and Gas token balance before Swap, **prohibit** Swap execution when balance insufficient.
7. **Three-step Confirmation SOP Mandatory**: **Must** complete three-step confirmation (trading pair confirmation → quote display → signature authorization confirmation) before executing `tx.swap`, cannot skip, simplify or auto-confirm any step.
8. **Swap Value Difference and Slippage Risk Prompt**: When swap value difference > 5% **must** prominently warn user (show USD value comparison); when slippage > 5% (0.05) **must** warn high slippage risk and MEV attack risk.
9. **Don't Auto-retry Failed Transactions**: After `tx.swap` execution failure, clearly show error info to user, don't auto-retry in background. Suggest re-getting quote.
10. **Prohibit Operations When MCP Server Not Configured or Unreachable**: Abort all subsequent steps when Step 0 connection detection fails.
11. **Transparent MCP Server Errors**: Show all MCP Server returned error messages to users truthfully, don't hide or tamper.
12. **MEV Risk Awareness**: Transactions may be subject to MEV/sandwich attacks under high slippage settings. Remind users of this risk when setting high slippage.
13. **Don't Recommend Unlimited Authorization**: If Swap process involves token Approve (`routes[].need_approved` is 2), suggest users use precise authorization amount rather than unlimited.
14. **Strict Chain Address Type Matching**: EVM chains must use EVM addresses (`addresses["EVM"]`), Solana must use SOL addresses (`addresses["SOL"]`), never mix.