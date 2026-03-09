---
name: gate-dex-mcpswap
version: "2026.3.6-1"
updated: "2026-03-06"
description: "Gate Wallet Swap/DEX trading. Get quotes, execute Swap. Use when user wants to 'swap USDT for ETH', 'swap', 'exchange tokens', 'buy tokens', 'sell tokens'. Includes mandatory three-step confirmation gate. Supports EVM multi-chain + Solana, supports cross-chain Swap."
---

# Gate Wallet Swap Skill

> Swap/DEX domain — Quote fetching, slippage control, route display, Swap execution (One-shot), status tracking, with mandatory three-step confirmation gate. 3 MCP tools + 2 cross-Skill calls + 1 MCP Resource.

**Trigger scenarios**: User mentions "swap", "exchange", "convert", "buy", "sell", "convert X to Y", "cross-chain", or when other Skills guide the user to perform token exchange operations.

## Step 0: MCP Server Connection Check (Mandatory)

**Before executing any operation, Gate Wallet MCP Server availability must be confirmed. This step cannot be skipped.**

Probe call:

```
CallMcpTool(server="gate-wallet", toolName="chain.config", arguments={chain: "ETH"})
```

| Result | Handling |
|--------|----------|
| Success | MCP Server available, proceed to subsequent steps |
| `server not found` / `unknown server` | Cursor not configured → Show configuration guide (see below) |
| `connection refused` / `timeout` | Remote unreachable → Prompt to check URL and network |
| `401` / `unauthorized` | API Key authentication failed → Prompt to check auth configuration |

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

If you don't have an MCP Server URL yet, please contact the administrator.
```

### Display when remote service is unreachable

```
⚠️  Gate Wallet MCP Server connection failed

MCP Server config found, but unable to connect to remote service. Please check:
1. Confirm service URL is correct (is the configured URL accessible)
2. Check network connection (VPN / firewall impact)
3. Confirm remote service is running normally
```

### Display when API Key authentication fails

```
🔑 Gate Wallet MCP Server authentication failed

MCP Server connected but API Key validation failed. The service uses AK/SK authentication (x-api-key header).
Please contact the administrator for a valid API Key and confirm server-side configuration.
```

## Authentication

All operations in this Skill **require `mcp_token`**. User must be logged in before calling any tool.

- If no `mcp_token` → Guide to `gate-dex-mcpauth` to complete login, then return.
- If `mcp_token` expired (MCP Server returns token expired error) → First try `auth.refresh_token` silent refresh, on failure guide to re-login.

## MCP Resource

### `swap://supported_chains` — List of chains supported for Swap

**Before** calling `tx.quote` or `tx.swap`, this Resource must be read to verify chain_id supports Swap and determine address grouping (EVM vs Solana).

```
FetchMcpResource(server="gate-wallet", uri="swap://supported_chains")
```

Returns chain list grouped by address type (evm / solana), used for:
- Verifying user-specified chain supports Swap
- Determining whether `user_wallet` should use EVM address or SOL address
- Cross-chain Swap: determining if source and target chains belong to different address groups (requires `to_wallet`)

## MCP Tool Call Specification

### 1. `wallet.get_token_list` (Cross-Skill call) — Query balance for validation

**Must** call this tool before Swap to validate input token balance and Gas token balance. This tool belongs to `gate-dex-mcpwallet` domain, called here cross-Skill.

| Field | Description |
|-------|-------------|
| **Tool name** | `wallet.get_token_list` |
| **Parameters** | `{ chain?: string, network_keys?: string, account_id?: string, mcp_token: string, page?: number, page_size?: number }` |
| **Return value** | Token array, each item contains `symbol`, `balance`, `price`, `value`, `chain`, `contract_address`, etc. |

Parameter description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain` | No | Single-chain query (e.g. `"ETH"`), backward compatible |
| `network_keys` | No | Multi-chain query, comma-separated (e.g. `"ETH,SOL,ARB"`) |
| `account_id` | No | User account ID, can be auto-detected from login session |
| `mcp_token` | Yes | Auth token |
| `page` | No | Page number, default 1 |
| `page_size` | No | Page size, default 20 |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="wallet.get_token_list",
  arguments={ chain: "ETH", mcp_token: "<mcp_token>" }
)
```

Agent behavior: Extract input token (sell token) balance and chain native token balance (for Gas) from returned list, prepare for subsequent balance validation. Also resolve token symbol to contract address.

---

### 2. `wallet.get_addresses` (Cross-Skill call) — Get chain-specific wallet addresses

Both `tx.quote` and `tx.swap` **require** `user_wallet` parameter. This tool must be called first to get user wallet addresses on different chain types. This tool belongs to `gate-dex-mcpwallet` domain, called here cross-Skill.

| Field | Description |
|-------|-------------|
| **Tool name** | `wallet.get_addresses` |
| **Parameters** | `{ account_id: string, mcp_token: string }` |
| **Return value** | Address mapping, e.g. `{ "EVM": "0x...", "SOL": "5x..." }` |

Parameter description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `account_id` | Yes | User account ID |
| `mcp_token` | Yes | Auth token |

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
  "EVM": "0x1234567890abcdef1234567890abcdef12345678",
  "SOL": "5xAbCdEf1234567890abcdef1234567890abcdef12"
}
```

Agent behavior:
- EVM chains (ETH/BSC/Polygon/Arbitrum/Base/Avalanche) → Use `addresses["EVM"]` as `user_wallet`
- Solana (chain_id=501) → Use `addresses["SOL"]` as `user_wallet`
- Cross-chain Swap with source and target different address groups → Source chain address as `user_wallet`, target chain address as `to_wallet`

---

### 3. `tx.quote` — Get Swap quote

Get Swap quote from input token to output token, including exchange rate, slippage, route path, estimated Gas, etc. **Before calling: ① User must confirm slippage (via AskQuestion or explicitly in message); ② Read `swap://supported_chains` Resource to verify chain support; ③ Call `wallet.get_addresses` to get wallet address. Do not call this tool until slippage is confirmed.**

| Field | Description |
|-------|-------------|
| **Tool name** | `tx.quote` |
| **Parameters** | `{ chain_id_in: number, chain_id_out: number, token_in: string, token_out: string, amount: string, slippage: number, user_wallet: string, native_in: number, native_out: number, mcp_token: string, to_wallet?: string }` |
| **Return value** | Quote info, including estimated output amount, route path (`routes`), Gas fee, price impact, etc. `routes[].need_approved` value 2 means token approval required |

Parameter description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain_id_in` | Yes | Source chain ID (ETH=1, BSC=56, Polygon=137, Arbitrum=42161, Base=8453, Avalanche=43114, Solana=501) |
| `chain_id_out` | Yes | Target chain ID. Same-chain Swap: same as `chain_id_in`; Cross-chain Swap: target chain ID |
| `token_in` | Yes | Input token contract address. Native token use `"-"`. If `native_in=1` auto-normalizes to `"-"` |
| `token_out` | Yes | Output token contract address. Native token use `"-"`. If `native_out=1` auto-normalizes to `"-"` |
| `amount` | Yes | Input token amount (human-readable format, e.g. `"100"`, do not convert to wei/lamports) |
| `slippage` | Yes | Slippage tolerance, **decimal ratio** (`0.01` = 1%, `0.03` = 3%). Range 0.001~0.499. Default `0.03` (3%) |
| `user_wallet` | Yes | User source chain wallet address, from `wallet.get_addresses` |
| `native_in` | Yes | **⚠️ Critical field, wrong value causes tx failure or fund loss.** Check if token_in is native: Native (ETH, BNB, MATIC, AVAX, SOL) = `1`, Contract token (USDT, USDC, WETH, WBNB, etc.) = `0`. User saying "BNB" defaults to native; only explicit "WBNB" is contract token. See "native_in / native_out rules" below |
| `native_out` | Yes | **⚠️ Critical field, wrong value causes tx failure or fund loss.** Check if token_out is native: Native (ETH, BNB, MATIC, AVAX, SOL) = `1`, Contract token (USDT, USDC, WETH, WBNB, etc.) = `0`. User saying "SOL" defaults to native; only explicit "WSOL" is contract token. See "native_in / native_out rules" below |
| `mcp_token` | Yes | Auth token |
| `to_wallet` | Required for cross-chain | Target chain receiving address. Only needed when cross-chain and source/target belong to different address groups (e.g. EVM→Solana) |

#### native_in / native_out rules

**These fields determine how the backend normalizes token addresses; wrong values cause tx failure.** Rules are simple:

**Check if token_in / token_out itself is native (Gas token):**
- `native_in`: token_in is native → `1`, is contract token → `0`
- `native_out`: token_out is native → `1`, is contract token → `0`

Native vs contract token reference:

| Native (native=1) | Corresponding Wrapped contract token (native=0) | Note |
|------------------|------------------------------------------------|------|
| ETH | WETH | User saying "ETH" defaults to native; only explicit "WETH" is contract token |
| BNB | WBNB | User saying "BNB" defaults to native; only explicit "WBNB" is contract token |
| MATIC | WMATIC | User saying "MATIC" defaults to native |
| AVAX | WAVAX | User saying "AVAX" defaults to native |
| SOL | WSOL | User saying "SOL" defaults to native |

Common contract tokens (**always native=0**): USDT, USDC, DAI, CAKE, ARB, OP, RAY, JUP, etc.

**Cross-chain examples:**
- USDT(BSC) → SOL(Solana): token_in=USDT is contract token → `native_in=0`, token_out=SOL is native → `native_out=1`
- ETH(Ethereum) → USDT(BSC): token_in=ETH is native → `native_in=1`, token_out=USDT is contract token → `native_out=0`
- USDC(Ethereum) → USDC(Polygon): both contract tokens → `native_in=0`, `native_out=0`
- ETH(Ethereum) → SOL(Solana): both native → `native_in=1`, `native_out=1`
- BNB(BSC) → ETH(Ethereum): both native → `native_in=1`, `native_out=1`

**Common mistakes:**
- ❌ Treating "BNB" as WBNB (contract token) when user says "BNB"; should be native=1
- ❌ Treating WETH/WBNB/WSOL etc. as native (they are contract tokens, native=0)
- ❌ Cross-chain: native_out not passed or default 0, causing backend to misidentify target token

Call example (same-chain Swap: USDT→ETH on ETH):

```
CallMcpTool(
  server="gate-wallet",
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
  server="gate-wallet",
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
1. **Must** show quote summary table to user after getting quote (see "Quote display template" below)
2. Calculate **exchange value difference** (see formula below), warn user prominently when > 5%
3. Check `need_approved`: when value is 2, inform user token approval needed and emphasize
4. **Do not execute Swap directly**, must wait for user confirmation

#### `tx.quote` return value key field mapping

| Field path | Type | Description | Display use |
|------------|------|-------------|-------------|
| `amount_in` | string | Input token amount (human-readable) | Pay amount |
| `amount_out` | string | Estimated output token amount (human-readable) | Receive amount |
| `min_amount_out` | string | Minimum receive amount (with slippage protection) | Min receive |
| `slippage` | string | Actual slippage used (decimal, e.g. `"0.010000"` = 1%) | Slippage info |
| `from_token.token_symbol` | string | Input token symbol | Token name |
| `from_token.token_price` | string | Input token unit price (USD) | Value diff calculation |
| `from_token.chain_name` | string | Input token chain name | Chain info |
| `from_token.chain_id` | number | Input token chain ID | Chain info |
| `to_token.token_symbol` | string | Output token symbol | Token name |
| `to_token.token_price` | string | Output token unit price (USD) | Value diff calculation |
| `to_token.chain_name` | string | Output token chain name | Chain info (different for cross-chain) |
| `estimate_gas_fee_amount` | string | Gas fee (native token amount) | Gas display |
| `estimate_gas_fee_amount_usd` | string | Gas fee (USD) | Gas display |
| `estimate_tx_time` | string | Estimated tx confirmation time (seconds) | Arrival time |
| `need_approved` | number | Whether token approval needed (2=needs approval, other=no approval) | Approval prompt |
| `is_signal_chain` | number | 1=same chain, 2=cross-chain | Cross-chain flag |
| `provider.name` | string | DEX/aggregator/bridge name | Route display |
| `provider.fee` | string | Service/bridge fee (has value for cross-chain) | Fee display |
| `provider.fee_symbol` | string | Fee token symbol (has value for cross-chain) | Fee display |
| `handlers[].type` | string | `"swap"` = DEX exchange, `"bridge"` = cross-chain bridge | Route type |
| `handlers[].routes[].sub_routes[][].name` | string | Specific DEX/bridge name (e.g. `PANCAKE_V2`, `Bridgers`) | Route detail |
| `handlers[].routes[].sub_routes[][].name_in` | string | Route intermediate input token name | Route path |
| `handlers[].routes[].sub_routes[][].name_out` | string | Route intermediate output token name | Route path |
| `trading_fee.rate` | number | Platform trading fee rate (e.g. `0.003` = 0.3%, may have value for single-chain) | Fee display |
| `trading_fee.enable` | boolean | Whether trading fee enabled | Fee display |
| `pool.liquidity` | string | Pool total liquidity (USD, has value for single-chain) | Liquidity reference |
| `quote_id` | string | Quote ID (internal identifier) | Log tracking |

#### Exchange value difference calculation

```
input_value_usd  = float(amount_in) × float(from_token.token_price)
output_value_usd = float(amount_out) × float(to_token.token_price)
price_diff_pct   = (input_value_usd - output_value_usd) / input_value_usd × 100
```

This value difference includes all costs (DEX fee, bridge fee, slippage loss, price impact, etc.), the total cost ratio actually borne by the user.

| Value diff range | Handling |
|------------------|----------|
| < 1% | Normal, no extra prompt |
| 1% ~ 3% | Normal range, can note in quote |
| 3% ~ 5% | Prompt "exchange value difference is high" |
| > 5% | **Prominent warning**: Show value diff details, use AskQuestion for user confirmation (see "Exchange value diff > 5% mandatory warning" template) |

---

### 4. `tx.swap` — Execute Swap (One-shot)

One-shot Swap: Quote→Build→Sign→Submit completed in single call. Eliminates multiple round-trip delays (solves Solana blockhash expiry). Internal retry up to 3 times.

**Only call after completing three-step confirmation SOP (see operation flow below).**

| Field | Description |
|-------|-------------|
| **Tool name** | `tx.swap` |
| **Parameters** | `{ chain_id_in: number, chain_id_out: number, token_in: string, token_out: string, amount: string, slippage: number, user_wallet: string, native_in: number, native_out: number, account_id: string, mcp_token: string, to_wallet?: string }` |

#### Success return value

| Field | Type | Description |
|-------|------|-------------|
| `tx_hash` | string | On-chain tx hash |
| `tx_order_id` | string | Internal order ID, for `tx.swap_detail` polling |
| `amount_in` | string | Actual input amount (human-readable) |
| `amount_out` | string | Estimated output amount (human-readable) |
| `from_token` | string | Input token symbol |
| `to_token` | string | Output token symbol |
| `slippage` | number | Slippage used (decimal) |
| `route_path` | string[] | List of DEX names in route |
| `need_approved` | boolean | Whether ERC20 approval was executed |
| `status` | string | Fixed `"submitted"` |
| `message` | string | `"Transaction submitted. Poll tx.swap_detail with tx_order_id every 5s."` |

#### Failure return value (all 3 retries failed)

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Fixed `"failed"` |
| `message` | string | `"Swap failed after 3 attempts"` |
| `attempts` | array | Detail array for each attempt, each with `attempt` (sequence), `error` (error message) |

Parameter description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `chain_id_in` | Yes | Source chain ID |
| `chain_id_out` | Yes | Target chain ID. Same-chain Swap same as `chain_id_in` |
| `token_in` | Yes | Input token contract address, native token `"-"` |
| `token_out` | Yes | Output token contract address, native token `"-"` |
| `amount` | Yes | Human-readable amount (e.g. `"0.01"`) |
| `slippage` | Yes | Slippage, decimal ratio (`0.01`=1%, `0.03`=3%) |
| `user_wallet` | Yes | Source chain wallet address |
| `native_in` | Yes | **⚠️ Critical field, same rules as tx.quote.** Check if token_in is native: Native (ETH/BNB/MATIC/AVAX/SOL) = `1`, contract token = `0`. User saying "BNB" defaults to native. See "native_in / native_out rules" in tx.quote above |
| `native_out` | Yes | **⚠️ Critical field, same rules as tx.quote.** Check if token_out is native: Native (ETH/BNB/MATIC/AVAX/SOL) = `1`, contract token = `0`. User saying "SOL" defaults to native. See "native_in / native_out rules" in tx.quote above |
| `account_id` | Yes | User account ID (UUID) |
| `mcp_token` | Yes | Auth token |
| `to_wallet` | Required for cross-chain | Target chain receiving address (needed when crossing different address groups) |

Call example:

```
CallMcpTool(
  server="gate-wallet",
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

| Field | Example value |
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

| Field | Example value |
|-------|---------------|
| `status` | `failed` |
| `message` | `Swap failed after 3 attempts` |
| `attempts[0].error` | `insufficient balance` |
| `attempts[1].error` | `quote failed: liquidity too low` |
| `attempts[2].error` | `quote failed: liquidity too low` |

Agent behavior:
- Success (`status == "submitted"`) → Show user `tx_hash`, `from_token`/`to_token`, `amount_in`/`amount_out`, with block explorer link, then poll `tx.swap_detail` with `tx_order_id`
- Failure (`status == "failed"`) → Show `message` and each `attempts[].error`, no auto retry, suggest user re-fetch quote

---

### 5. `tx.swap_detail` — Query Swap status

Query execution result and details of submitted Swap transaction. Use `tx_order_id` returned by `tx.swap`.

| Field | Description |
|-------|-------------|
| **Tool name** | `tx.swap_detail` |
| **Parameters** | `{ tx_order_id: string, mcp_token: string }` |
| **Return value** | Swap transaction details, including status, token info, timestamp, Gas fee, etc. |

Parameter description:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `tx_order_id` | Yes | `tx_order_id` returned by `tx.swap` |
| `mcp_token` | Yes | Auth token |

Return value key fields:

| Field | Type | Description |
|-------|------|-------------|
| `status` | number | Tx status: 0=success, 3=failed |
| `tokenInSymbol` | string | Input token symbol |
| `tokenOutSymbol` | string | Output token symbol |
| `amountIn` | string | Input amount (min unit) |
| `amountOut` | string | Output amount (min unit) |
| `tokenInDecimals` | number | Input token decimals |
| `tokenOutDecimals` | number | Output token decimals |
| `srcHash` | string | On-chain tx hash |
| `srcHashExplorerUrl` | string | Block explorer URL prefix |
| `unifyGasFee` | string | Actual Gas fee (min unit) |
| `unifyGasFeeDecimal` | number | Gas token decimals |
| `unifyGasFeeSymbol` | string | Gas token symbol |
| `gasFeeUsd` | string | Actual Gas fee (USD) |
| `creationTime` | string | Tx creation time (ISO8601) |
| `errorCode` | number | Error code (0=no error) |
| `errorMsg` | string | Error message (has value on failure) |

Gas fee human-readable conversion: `float(unifyGasFee) / 10^unifyGasFeeDecimal`, unit is `unifyGasFeeSymbol`.

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="tx.swap_detail",
  arguments={
    tx_order_id: "order_abc123",
    mcp_token: "<mcp_token>"
  }
)
```

Return value `status` meaning:

| status | Meaning | Next action |
|--------|---------|-------------|
| `pending` | Tx pending confirmation | Poll every 5 seconds, max 3 minutes; on timeout guide user to view via `tx.history_list` |
| `success` | Swap completed successfully | Show final result to user |
| `failed` | Swap failed | Show failure reason, suggest re-fetch quote |

## Supported chains

| chain_id | Network name | Type | Native Gas token | Block explorer | chain.config identifier |
|----------|--------------|------|------------------|----------------|-------------------------|
| `1` | Ethereum | EVM | ETH | etherscan.io | `ETH` |
| `56` | BNB Smart Chain | EVM | BNB | bscscan.com | `BSC` |
| `137` | Polygon | EVM | MATIC | polygonscan.com | `POLYGON` |
| `42161` | Arbitrum One | EVM | ETH | arbiscan.io | `ARB` |
| `10` | Optimism | EVM | ETH | optimistic.etherscan.io | `OP` |
| `43114` | Avalanche C-Chain | EVM | AVAX | snowtrace.io | `AVAX` |
| `8453` | Base | EVM | ETH | basescan.org | `BASE` |
| `501` | Solana | Non-EVM | SOL | solscan.io | `SOL` |

Common chain_id can be used directly; only call `chain.config` for uncommon chains.

**Before calling `tx.quote` / `tx.swap`, always read `swap://supported_chains` Resource to confirm chain supports Swap.**

## Token address resolution

Agent needs to convert user-provided token name/symbol to contract address and native flag when collecting Swap parameters:

| User input | Resolution | `token_in`/`token_out` | `native_in`/`native_out` |
|------------|-------------|------------------------|-------------------------|
| Native token (ETH, BNB, SOL, MATIC, AVAX) | Mark as native | `"-"` | `1` |
| Token symbol (e.g. USDT, USDC) | Match `symbol` from `wallet.get_token_list` holdings to get `contract_address` | Contract address | `0` |
| Contract address (e.g. `0xdAC17...`) | Use directly | Pass as-is | `0` |

**⚠️ Native flag rule: Check if token itself is native**
- `native_in`: token_in is native (ETH/BNB/SOL/MATIC/AVAX) → `1`, contract token → `0`
- `native_out`: token_out is native → `1`, contract token → `0`
- User saying "BNB" defaults to native (native=1); only explicit "WBNB" is contract token (native=0). Same for ETH vs WETH, SOL vs WSOL
- WETH, WBNB, WSOL etc. are **contract tokens** (native=0), not native

When user-provided token symbol not found in holdings:
- Prompt user to confirm token name is correct
- Prompt user to provide contract address
- Suggest using `gate-dex-mcpmarket` (`token_get_coin_info`) to query token info for contract address

## MCP tool call chain overview

Complete Swap flow calls the following tools in sequence, forming a strict linear pipeline:

```
0.  chain.config                                      ← Step 0: MCP Server pre-check
1.  FetchMcpResource(swap://supported_chains)         ← Verify chain supports Swap + address grouping
2.  wallet.get_token_list                             ← Cross-Skill: query balance (input token + Gas token) + resolve token address
3.  wallet.get_addresses                              ← Cross-Skill: get chain-specific wallet address (user_wallet / to_wallet)
4.  [Agent balance validation: input token balance >= amount]            ← Agent internal logic, not MCP call
5.  [Agent show trade pair confirmation Table, wait for user confirm]         ← tx.swap SOP Step 1 (mandatory gate)
6.  tx.quote                                          ← Get quote (estimated output, route, Gas, price impact)
7.  [Agent show quote details + check need_approved]          ← tx.swap SOP Step 2 (mandatory gate)
8.  [Agent sign approval confirm, wait for user confirm]                  ← tx.swap SOP Step 3 (mandatory gate)
9.  tx.swap                                           ← One-shot execution (Quote→Build→Sign→Submit)
10. tx.swap_detail (by tx_order_id, poll every 5s)       ← Query Swap result (optional, poll as needed)
```

## Skill routing

Route to corresponding Skill based on user intent after Swap:

| User intent | Route target |
|-------------|--------------|
| View updated balance | `gate-dex-mcpwallet` |
| View Swap tx history | `gate-dex-mcpwallet` (`tx.history_list`) |
| Continue Swap other tokens | Stay in this Skill |
| Transfer just-swapped tokens | `gate-dex-mcptransfer` |
| View token market / K-line | `gate-dex-mcpmarket` |
| Login / auth expired | `gate-dex-mcpauth` |

## Operation flow

### Flow A: Standard Swap (main flow)

```
Step 0: MCP Server pre-check
  Call chain.config({chain: "ETH"}) to probe availability
  ↓ Success

Step 1: Auth check
  Confirm valid mcp_token and account_id
  No token → Guide to gate-dex-mcpauth login
  ↓

Step 2: Intent recognition + parameter collection
  Extract Swap intent from user input, collect required parameters:
  - from_token: Input token (required, e.g. USDT)
  - to_token: Output token (required, e.g. ETH)
  - amount: Input amount (required, e.g. 100)
  - chain: Target chain (optional, infer from token or context, default Ethereum chain_id=1)
  - slippage: Slippage tolerance (optional, see interactive selection below)

  When from_token / to_token / amount missing, ask user item by item.

  **Slippage selection**: If user already specified slippage in message, use directly, no need to ask.
  If not specified, use AskQuestion for user to select:

  ```
  AskQuestion({
    title: "Slippage setting",
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

  User selects "Custom" → Ask for specific value (input percentage, Agent converts to decimal ratio)
  ↓ Parameters complete

Step 3: Verify chain support
  Read swap://supported_chains Resource
  Confirm user-specified chain chain_id in support list
  Determine address grouping (EVM / Solana)
  ↓

Step 4: Query balance (Cross-Skill: gate-dex-mcpwallet)
  Call wallet.get_token_list({ chain: "ETH", mcp_token })
  Extract:
  - Input token balance (e.g. USDT balance)
  - Chain native Gas token balance (e.g. ETH balance)
  Also resolve user-provided token symbol to contract address (token_in, token_out) and native flag
  ↓

Step 5: Get wallet address (Cross-Skill: gate-dex-mcpwallet)
  Call wallet.get_addresses({ account_id, mcp_token })
  Get user_wallet by source chain type:
  - EVM chain → addresses["EVM"]
  - Solana → addresses["SOL"]
  Cross-chain Swap with different address groups → Also get to_wallet
  ↓

Step 6: Agent balance validation (mandatory)
  Validation rules:
  a) Input token is native: balance >= amount + estimated_gas (Gas precisely validated after quote)
  b) Input token is ERC20/SPL: token_balance >= amount and native_balance > 0 (ensure Gas available)

  Validation failed → Abort Swap, show insufficient info:

  ────────────────────────────
  ❌ Insufficient balance, cannot execute Swap

  Input token: USDT
  Swap amount: 100 USDT
  Current USDT balance: 80 USDT (insufficient, short 20 USDT)

  Suggestions:
  - Reduce Swap amount
  - Deposit tokens to wallet first
  ────────────────────────────

  ↓ Validation passed

Step 7: SOP Step 1 — Confirm trade pair (mandatory gate)
  Show trade pair confirmation Table to user, use AskQuestion for confirmation:

  | Field | Value |
  |-------|------|
  | from_token | {symbol}({contract_address}) |
  | to_token | {symbol}({contract_address}) |
  | amount | {amount} |
  | chain | {chain_name} (chain_id={chain_id}) |
  | slippage | {slippage}% (user selected) |

  AskQuestion({
    title: "Trade pair confirmation",
    questions: [{
      id: "trade_confirm",
      prompt: "Please confirm the above trade information is correct",
      options: [
        { id: "confirm", label: "Confirm, continue to get quote" },
        { id: "modify_slippage", label: "Modify slippage" },
        { id: "modify_amount", label: "Modify amount" },
        { id: "cancel", label: "Cancel trade" }
      ]
    }]
  })

  User selects confirm → Continue
  User selects modify_slippage → Re-show AskQuestion slippage selection
  User selects modify_amount → Ask for new amount then re-show Table
  User selects cancel → Abort Swap
  (Fallback to text reply when AskQuestion unavailable)
  ↓ User confirmed

Step 8: SOP Step 2 — Get quote and display (mandatory gate, cannot skip)
  Call tx.quote({
    chain_id_in, chain_id_out, token_in, token_out, amount, slippage,
    user_wallet, native_in, native_out, mcp_token, to_wallet?
  })

  Must show user:
  - Estimated to_token receive amount
  - Route/DEX path
  - Estimated Gas fee
  - Price impact (warn when > 5%)
  - Approval requirement (when need_approved == 2, inform token approval needed)
  ↓

Step 9: Quote risk assessment (Agent internal logic)
  Check risk indicators in quote:
  a) Exchange value difference (price_diff_pct):
     input_value_usd  = float(amount_in) × float(from_token.token_price)
     output_value_usd = float(amount_out) × float(to_token.token_price)
     price_diff_pct   = (input_value_usd - output_value_usd) / input_value_usd × 100
     - < 1%: Normal
     - 1% ~ 3%: Normal range
     - 3% ~ 5%: Prompt "exchange value difference is high"
     - > 5%: **Prominent warning** — Show input_value_usd, output_value_usd, difference, use AskQuestion for user to confirm (see "Exchange value diff > 5% mandatory warning" template)
  b) Slippage:
     - User setting > 5% (i.e. > 0.05): Warn "slippage set high, actual execution price may deviate significantly"
  c) Gas fee:
     - Gas fee as % of Swap amount > 10%: Prompt "Gas fee ratio high, suggest larger Swap amount or wait for network idle"
  d) Native token Gas balance precise validation:
     - native_balance < estimated_gas → Abort, prompt Gas insufficient
  ↓

Step 10: SOP Step 3 — Sign approval confirmation (mandatory gate)
  Inform user:
  "The next step involves contract approval or transaction signing. This is necessary to execute the trade.
   After confirmation, the system will automatically complete Quote→Build→Sign→Submit full flow."

  Use AskQuestion for final confirmation:

  AskQuestion({
    title: "Sign approval confirmation",
    questions: [{
      id: "sign_confirm",
      prompt: "Confirm execute trade? System will automatically complete signing and submission",
      options: [
        { id: "confirm", label: "Confirm execute" },
        { id: "modify", label: "Modify slippage/amount" },
        { id: "cancel", label: "Cancel trade" }
      ]
    }]
  })

  (Fallback to text reply when AskQuestion unavailable)
  ↓

  User selects confirm → Continue Step 11
  User selects cancel → Abort Swap, show cancel prompt
  User selects modify → Return to Step 7 re-show trade pair Table and re-fetch quote

Step 11: Execute Swap (One-shot)
  Call tx.swap({
    chain_id_in, chain_id_out, token_in, token_out, amount, slippage,
    user_wallet, native_in, native_out, account_id, mcp_token, to_wallet?
  })
  Get tx_hash and tx_order_id
  ↓

Step 12: Query Swap result (as needed)
  Call tx.swap_detail({ tx_order_id, mcp_token })
  Poll every 5 seconds, max 3 minutes (~36 times), until terminal state:
  - status == "pending" → Inform user tx pending, continue polling
  - status == "success" → Show final execution result
  - status == "failed" → Show failure info
  - Still "pending" after 3 minutes → Stop polling, inform user:
    "Transaction still processing, please check result later via transaction list."
    Guide user to call tx.history_list({ account_id, mcp_token }) to view Swap tx history
  ↓

Step 13: Show result + follow-up suggestions

  ────────────────────────────
  ✅ Swap executed successfully!

  Input: 100 USDT
  Received: 0.0521 ETH
  Gas fee: 0.00069778 ETH (≈ $1.46)
  Tx Hash: {tx_hash}
  Block explorer: https://{explorer}/tx/{tx_hash}

  You can:
  - View updated balance
  - View Swap history
  - Continue other operations
  ────────────────────────────
```

### Flow B: Re-quote after modifying slippage

```
Trigger: User requests slippage change at confirmation step
  ↓
Step 1: Record new slippage value
  User specifies new slippage (e.g. "change slippage to 1%")
  Convert to decimal ratio (1% → 0.01)
  ↓
Step 2: Re-fetch quote
  Re-call tx.quote with new slippage (other params unchanged)
  ↓
Step 3: Re-display quote details
  Show updated quote info (new min output amount will change)
  ↓
  Wait for user to confirm again or continue modifying
  After confirm, proceed to sign approval confirmation (SOP Step 3)
```

### Flow C: Query Swap transaction status

```
Step 0: MCP Server pre-check
  ↓ Success

Step 1: Auth check
  ↓

Step 2: Query Swap status
  Call tx.swap_detail({ tx_order_id, mcp_token })
  ↓

Step 3: Display status

  ── Swap Status ──────────────
  Order ID: {tx_order_id}
  Status: {status} (success / pending / failed)
  Input: {from_amount} {from_token}
  Output: {to_amount} {to_token}
  Gas fee: {gas_fee} {gas_symbol} (≈ ${gas_fee_usd})
  Tx Hash: {tx_hash}
  Block explorer: https://{explorer}/tx/{tx_hash}
  ────────────────────────────
```

### Flow D: Cross-chain Swap

```
Trigger: User wants to exchange A-chain asset to B-chain (e.g. USDT on ETH → SOL on Solana)
  ↓
Step 1: Verify cross-chain support
  Read swap://supported_chains Resource
  Confirm chain_id_in and chain_id_out both in support list
  Determine address grouping: whether source and target chains belong to different address groups
  ↓

Step 2: Get wallet addresses
  Call wallet.get_addresses({ account_id, mcp_token })
  - user_wallet = Source chain address (e.g. EVM address)
  - to_wallet = Target chain address (e.g. SOL address, only when crossing different address groups)
  ↓

Step 3: Same as Flow A from Step 6 onward
  Set chain_id_in != chain_id_out in tx.quote and tx.swap
  And pass to_wallet parameter
```

## Swap confirmation templates

**Three-step confirmation SOP must be completed before `tx.swap` execution; each step is a mandatory gate that cannot be skipped.**

### Interaction strategy

For all gate steps requiring user confirmation/cancel input, **prefer `AskQuestion` tool** for structured options to improve interaction efficiency:
- When `AskQuestion` available: Let user quickly select via option buttons (confirm, cancel, modify params, etc.)
- When `AskQuestion` unavailable (tool call failed or platform unsupported): Fallback to text reply mode, prompt user to reply "confirm"/"cancel"

### SOP Step 1: Trade pair confirmation Table

After showing the Table below, use `AskQuestion` for user to confirm or modify:

```
| Field | Value |
|-------|------|
| from_token | {from_symbol}({from_contract_address}) |
| to_token | {to_symbol}({to_contract_address}) |
| amount | {amount} |
| chain | {chain_name} (chain_id={chain_id_in}) |
| slippage | {slippage}% (user selected) |
```

**Interaction (prefer AskQuestion)**:

```
AskQuestion({
  title: "Trade pair confirmation",
  questions: [{
    id: "trade_confirm",
    prompt: "Please confirm the above trade information is correct",
    options: [
      { id: "confirm", label: "Confirm, continue to get quote" },
      { id: "modify_slippage", label: "Modify slippage" },
      { id: "modify_amount", label: "Modify amount" },
      { id: "cancel", label: "Cancel trade" }
    ]
  }]
})
```

| User selection | Handling |
|----------------|----------|
| `confirm` | Continue SOP Step 2 (get quote) |
| `modify_slippage` | Show slippage selection AskQuestion, update then re-show Table |
| `modify_amount` | Ask for new amount, update then re-show Table |
| `cancel` | Abort Swap, show cancel prompt |

**Fallback mode**: If `AskQuestion` unavailable, prompt user to reply "confirm" to continue, "cancel" to abort, or specify parameter to modify.

### SOP Step 2: Quote details display

After calling `tx.quote`, must display quote summary in table form. Same template for same-chain/cross-chain, auto-adapt display items based on returned data.

#### General quote template

```
Quote Summary

| Item | Content |
|------|---------|
| Chain | {chain info} |
| Pay | {amount_in} {from_token.token_symbol} |
| Receive | ≈ {amount_out} {to_token.token_symbol} |
| Min receive | ≈ {min_amount_out} {to_token.token_symbol} (with {slippage×100}% slippage protection) |
| Rate | 1 {from_token.token_symbol} ≈ {amount_out/amount_in} {to_token.token_symbol} |
| Exchange value diff | ≈ {price_diff_pct}% |
| Route | {route info} |
| Fee | {fee info} |
| Est. Gas | {estimate_gas_fee_amount} {gas_symbol} (≈ ${estimate_gas_fee_amount_usd}) |
| Est. time | ≈ {estimate_tx_time} sec |
| Liquidity | ${pool.liquidity} |
| Approval | {need_approved note} |
```

#### Field value rules

| Display item | Value logic |
|--------------|-------------|
| **Chain** | Same-chain (`is_signal_chain == 1`) → `from_token.chain_name`; Cross-chain (`is_signal_chain == 2`) → `from_token.chain_name → to_token.chain_name` |
| **Rate** | `float(amount_out) / float(amount_in)`, add chain name after token symbol for cross-chain |
| **Exchange value diff** | `(input_value_usd - output_value_usd) / input_value_usd × 100` (see calculation above) |
| **Route** | `provider.name` + `handlers[].routes[].sub_routes[][].name`; Mark "cross-chain bridge" for cross-chain |
| **Fee** | `trading_fee.enable == true` → `trading_fee.rate × 100`% (trading fee); `provider.fee` has value → `provider.fee provider.fee_symbol` (bridge/service fee); omit if both empty |
| **Gas token** | Source chain native token (BSC=BNB, ETH=ETH, Solana=SOL, etc.) |
| **Liquidity** | Show when `pool.liquidity` has value, omit row when empty |
| **Approval** | `need_approved == 2` → "⚠️ Need to approve {from_symbol} contract first (Token Approval), system will handle automatically"; Other → "No approval needed ✅" |
| **Cross-chain note** | When `is_signal_chain == 2` append below table: "Cross-chain trade involves bridging, actual arrival time may extend due to network congestion." |

#### Example 1: Same-chain Swap (BNB → DOGE on BSC)

```
Quote Summary

| Item | Content |
|------|---------|
| Chain | BNB Smart Chain |
| Pay | 0.001 BNB |
| Receive | ≈ 4.634 DOGE |
| Min receive | ≈ 4.588 DOGE (with 1% slippage protection) |
| Rate | 1 BNB ≈ 4634 DOGE |
| Exchange value diff | ≈ 0.67% |
| Route | PancakeSwap V2 (PANCAKE_V2) |
| Fee | 0.3% (trading fee) |
| Est. Gas | 0.0000063 BNB (≈ $0.0041) |
| Est. time | ≈ 49 sec |
| Liquidity | $878,530 |
| Approval | Need to approve BNB contract |
```

#### Example 2: Cross-chain Swap (Solana USDT → Ethereum USDT)

```
Quote Summary

| Item | Content |
|------|---------|
| Chain | Solana → Ethereum |
| Pay | 1.707168 USDT |
| Receive | ≈ 1.652046 USDT |
| Min receive | ≈ 1.569443 USDT (with 5% slippage protection) |
| Rate | 1 USDT (Solana) ≈ 0.9677 USDT (ETH) |
| Exchange value diff | ≈ 3.27% |
| Route | MetaPath (via Bridgers cross-chain bridge) |
| Fee | 0.005122 USDT (bridge/service fee) |
| Est. Gas | 0.00000687 SOL (≈ $0.022) |
| Est. time | ≈ 10 sec |
| Approval | No approval needed ✅ |

Note: Exchange value diff is 3.27%, i.e. paying ≈ $1.71 value in tokens,
receiving ≈ $1.65 value in tokens, difference mainly from cross-chain bridge fee and slippage.
Cross-chain trade actual arrival time may extend due to network congestion.
```

#### Exchange value diff > 5% mandatory warning

When exchange value diff exceeds 5%, **must** append prominent warning below quote table and confirm via `AskQuestion`:

```
⚠️ Important warning: Exchange value diff is {price_diff_pct}%!
Paying ≈ ${input_value_usd} value in tokens, only receiving ≈ ${output_value_usd} value in tokens.
Difference ≈ ${diff_usd}, mainly from DEX fee, bridge fee, slippage loss and other combined costs.
Strongly suggest: Reduce trade amount, execute in batches, or wait for better quote.
```

**Interaction (prefer AskQuestion)**:

```
AskQuestion({
  title: "⚠️ High value diff warning",
  questions: [{
    id: "price_diff_confirm",
    prompt: "Exchange value diff is {price_diff_pct}%, confirm accept this exchange rate?",
    options: [
      { id: "confirm", label: "I understand the risk, continue" },
      { id: "reduce", label: "Reduce trade amount" },
      { id: "cancel", label: "Cancel trade" }
    ]
  }]
})
```

| User selection | Handling |
|----------------|----------|
| `confirm` | Continue to SOP Step 3 sign confirmation |
| `reduce` | Ask for new amount, return to SOP Step 1 re-run flow |
| `cancel` | Abort Swap |

**Fallback mode**: If `AskQuestion` unavailable, prompt user to reply "confirm" to continue, "cancel" to abort.

### SOP Step 3: Sign approval confirmation

After showing prompt text, use `AskQuestion` for final confirmation:

```
The next step involves contract approval and transaction signing. This is necessary to execute the trade.
After confirmation, the system will automatically complete Quote→Build→Sign→Submit full flow.
```

**Interaction (prefer AskQuestion)**:

```
AskQuestion({
  title: "Sign approval confirmation",
  questions: [{
    id: "sign_confirm",
    prompt: "Confirm execute trade? System will automatically complete signing and submission",
    options: [
      { id: "confirm", label: "Confirm execute" },
      { id: "modify", label: "Modify slippage/amount" },
      { id: "cancel", label: "Cancel trade" }
    ]
  }]
})
```

| User selection | Handling |
|----------------|----------|
| `confirm` | Execute `tx.swap` |
| `modify` | Return to SOP Step 1 re-show trade pair Table and re-fetch quote |
| `cancel` | Abort Swap, show cancel prompt |

**Fallback mode**: If `AskQuestion` unavailable, prompt user to reply "confirm" to execute, "cancel" to abort, or specify parameter to modify.

### High slippage warning (slippage > 5%, i.e. > 0.05)

Append additionally in SOP Step 1 Table and Step 2 quote display:

```
⚠️ Warning: Current slippage is set to {slippage×100}%, much higher than normal (3%).
This means actual execution price may deviate significantly from quote. Unless you confirm high slippage is needed (e.g. low liquidity token), suggest lowering slippage.
⚠️ High slippage trades may be vulnerable to MEV/sandwich attacks.
```

## Cross-Skill workflow

### Complete Swap flow (from login to completion)

```
gate-dex-mcpauth (login, get mcp_token + account_id)
  → gate-dex-mcpwallet (wallet.get_token_list → validate balance + resolve token address)
  → gate-dex-mcpwallet (wallet.get_addresses → get chain-specific wallet address)
    → gate-dex-mcpswap (trade pair confirm → tx.quote → quote display → sign approval confirm → tx.swap → tx.swap_detail)
      → gate-dex-mcpwallet (view updated balance)
```

### Query and buy workflow

```
gate-dex-mcpmarket (token_get_coin_info → query token info/market)
  → gate-dex-mcpmarket (token_get_risk_info → security review)
    → gate-dex-mcpwallet (wallet.get_token_list → validate balance)
      → gate-dex-mcpswap (quote → confirm → execute)
```

### Post security review trade workflow

```
gate-dex-mcpmarket (token_get_risk_info → token security audit)
  → gate-dex-mcpmarket (token_get_coin_info → token details)
    → gate-dex-mcpswap (execute Swap if safe)
```

### Guided by other Skills

| Source Skill | Scenario | Description |
|--------------|----------|-------------|
| `gate-dex-mcpwallet` | User wants to exchange after viewing balance | Carries account_id, chain and holdings info |
| `gate-dex-mcpmarket` | User wants to buy token after viewing market | Carries token info and chain context |
| `gate-dex-mcptransfer` | User wants to exchange remaining tokens after transfer | Carries chain and token context |

### Calling other Skills

| Target Skill | Call scenario | Tools used |
|--------------|---------------|------------|
| `gate-dex-mcpwallet` | Query balance and resolve token address before Swap | `wallet.get_token_list` |
| `gate-dex-mcpwallet` | Get chain-specific wallet address before Swap | `wallet.get_addresses` |
| `gate-dex-mcpwallet` | View updated balance after Swap | `wallet.get_token_list` |
| `gate-dex-mcpauth` | Not logged in or token expired | `auth.refresh_token` or full login flow |
| `gate-dex-mcpmarket` | Query token info to help resolve address | `token_get_coin_info` |
| `gate-dex-mcpmarket` | Security review target token before Swap | `token_get_risk_info` |
| `gate-dex-mcpwallet` | View Swap history | `tx.history_list` |

## Slippage

Slippage is a key parameter in Swap trades, controlling maximum allowed deviation between actual execution price and quote. Use **decimal ratio** when passing to `tx.quote` / `tx.swap` (e.g. `0.03` for 3%), convert to percentage when displaying to user.

| Slippage range | Decimal ratio | Use case | Note |
|----------------|----------------|----------|------|
| 0.5% ~ 1% | 0.005 ~ 0.01 | Stablecoin pairs (USDT/USDC etc.) | Sufficient liquidity, low slippage sufficient |
| 1% ~ 3% | 0.01 ~ 0.03 | Volatile tokens | Default recommended range |
| 3% ~ 5% | 0.03 ~ 0.05 | Low liquidity / meme tokens | Need to warn user about price deviation |
| > 5% | > 0.05 | Very low liquidity / high volatility | Need to warn user, may be vulnerable to MEV/sandwich attacks |

**Default slippage**: `0.03` (3%). If user already specified slippage in message, use directly, no need to ask. Only ask when not provided.

## Edge cases and error handling

| Scenario | Handling |
|----------|----------|
| MCP Server not configured | Abort all operations, show Cursor config guide |
| MCP Server unreachable | Abort all operations, show network check prompt |
| Not logged in (no `mcp_token`) | Guide to `gate-dex-mcpauth` to complete login, auto-return to continue Swap |
| `mcp_token` expired | First try `auth.refresh_token` silent refresh, on failure guide to re-login |
| Chain doesn't support Swap | After reading `swap://supported_chains` found unsupported → Show supported chain list, ask user to re-select |
| Input token balance insufficient | Abort Swap, show current balance vs required amount difference, suggest reduce amount or deposit first |
| Gas token balance insufficient | Abort Swap, show Gas token insufficient info, suggest get Gas token first |
| Token symbol cannot resolve to contract address | Prompt user to confirm token name or provide contract address, suggest use `gate-dex-mcpmarket` to query |
| `tx.quote` failed | Show error (possible causes: token pair doesn't exist, insufficient liquidity, network congestion). Suggest try different pair or retry later |
| Exchange value diff > 5% | **Prominently warn** user, show USD value comparison and difference, suggest reduce amount or batch execute. Can still continue if user insists |
| Slippage > 5% (i.e. > 0.05) | Warn user about high slippage risk and MEV attack risk, suggest lower. Can still continue if user insists |
| Gas fee as % of Swap amount > 10% | Prompt user Gas cost is high, suggest larger Swap amount or wait for network idle |
| `tx.swap` failed | Show failure reason (e.g. balance changed, slippage exceeded, network issue). No auto retry, suggest re-fetch quote |
| `tx.swap_detail` returns `failed` after Swap | Show failure reason, suggest re-fetch quote and execute Swap. Token balance may be unchanged |
| `tx.swap_detail` stays `pending` after Swap | Poll max 3 minutes; stop on timeout, inform user tx still processing, guide to view via `tx.history_list` |
| Input and output token same | Reject, prompt input and output token cannot be same |
| Input amount 0 or negative | Reject, prompt enter valid positive amount |
| Token pair not found on target chain | Prompt chain doesn't support this token pair Swap, suggest try on other chain |
| User cancels confirmation (any step of three-step SOP) | Abort immediately, do not execute Swap. Show cancel prompt, stay friendly |
| Cross-chain Swap different address groups but missing to_wallet | Auto get target chain address from `wallet.get_addresses` as `to_wallet` |
| EVM address used for Solana (or vice versa) | Auto select correct address based on chain_id and `swap://supported_chains` address grouping |
| Network interruption | Show network error, suggest check network and retry |

## Security rules

1. **`mcp_token` confidentiality**: Never display `mcp_token` in plain text to user; use placeholder `<mcp_token>` in call examples only.
2. **`account_id` masking**: When displaying to user, only show partial characters (e.g. `acc_12...89`).
3. **Token auto refresh**: When `mcp_token` expired, prefer silent refresh first, only require re-login on failure.
4. **Balance validation mandatory**: **Must** validate input token balance and Gas token balance before Swap; **prohibit** Swap execution when balance insufficient.
5. **Three-step confirmation SOP mandatory**: **Must** complete three-step confirmation (trade pair confirm → quote display → sign approval confirm) before executing `tx.swap`; cannot skip, simplify or auto-confirm any step.
6. **Exchange value diff and slippage risk prompts**: **Must** prominently warn user when exchange value diff > 5% (show USD value comparison); **Must** warn about high slippage risk and MEV attack risk when slippage > 5% (0.05).
7. **No auto retry on failed trades**: After `tx.swap` execution fails, clearly show error to user, no background auto retry. Suggest re-fetch quote.
8. **Prohibit operations when MCP Server not configured or unreachable**: Abort all subsequent steps if Step 0 connection check fails.
9. **MCP Server error transparency**: All MCP Server returned errors shown to user as-is, no hiding or tampering.
10. **MEV risk awareness**: Trades may be vulnerable to MEV/sandwich attacks with high slippage. Remind this risk when user sets high slippage.
11. **No unlimited approval recommendation**: If Swap flow involves token Approve (`routes[].need_approved` is 2), suggest user use exact approval amount instead of unlimited.
12. **Strict chain address type matching**: EVM chains must use EVM address (`addresses["EVM"]`), Solana must use SOL address (`addresses["SOL"]`), never mix.
