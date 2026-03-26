---
name: gate-dex-trade-openapi
version: "2026.3.12-1"
updated: "2026-03-12"
description: "Gate DEX OpenTrade trading skill. Directly calls Gate DEX aggregated trading API via AK/SK authentication, centered on Swap, covering quotes, authorization, transaction building, signing, submission, and status queries. Supports EVM (Ethereum/BSC/Arbitrum/Base and 13 other chains), Solana, SUI, Tron, Ton. Triggered when users mention swap, exchange, buy, sell, DEX trading, OpenAPI, AK/SK, quotes, Gas price, order status, transaction history."
---

# Gate DEX OpenTrade

Gate DEX OpenTrade trading skill. Directly calls Gate DEX aggregated trading API via AK/SK authentication, centered on Swap, covering quotes, authorization, transaction building, signing, submission, and status queries. Supports EVM (Ethereum/BSC/Arbitrum/Base and 13 chains), Solana, SUI, Tron, Ton. Triggered when users mention swap, exchange, buy, sell, DEX trading, OpenAPI, AK/SK, quotes, Gas prices, order status, transaction history.

---

## I. Trigger Scenarios

This Skill is triggered when the following intents appear in user conversations:

| Category | Example Keywords |
|----------|------------------|
| Direct Trigger | "OpenAPI", "AK/SK", "API Key", "DEX API", "gate dex", "gate-dex-opentrade" |
| Trading Intent | "swap", "exchange", "trade", "swap X for Y", "buy", "sell", "trading" |
| Query Intent | "quote", "Gas price", "which chains supported", "gas fee" |
| Status Query | "order status", "transaction status", "order history", "swap records", "transaction records" |
| Configuration Intent | "configure API", "set keys", "update AK", "change SK", "configure openapi" |

Additional rule: When `~/.gate-dex-openapi/config.json` file already exists, prioritize routing to this Skill.

---

## II. Step 0 — Environment Detection (Mandatory, must execute every trigger)

**This step must be executed first every time the Skill is triggered, cannot be skipped.**

### 2.1 Check Configuration File

Read `~/.gate-dex-openapi/config.json` (absolute path, not in workspace).

**If file does not exist**:

1. Create directory `~/.gate-dex-openapi/` (if not exists)
2. Automatically create configuration file using built-in default credentials:

```json
{
  "api_key": "7RAYBKMG5MNMKK7LN6YGCO5UDI",
  "secret_key": "COnwcshYA3EK4BjBWWrvwAqUXrvxgo0wGNvmoHk7rl4.6YLniz4h",
  "default_slippage": 0.03,
  "default_slippage_type": 1
}
```

3. Use Shell `mkdir -p ~/.gate-dex-openapi && chmod 700 ~/.gate-dex-openapi` to create directory and set permissions
4. Use Write tool to write above JSON to `~/.gate-dex-openapi/config.json`
5. Use Shell `chmod 600 ~/.gate-dex-openapi/config.json` to restrict file permissions (owner read/write only)
6. Display the following prompt to user:

```
Configuration file ~/.gate-dex-openapi/config.json created with default credentials, ready to use.
Configuration file is stored in user home directory (not workspace), won't be tracked by git.

To create exclusive AK/SK for better service experience, please visit Gate DEX developer platform:
https://web3.gate.com/zh/api-config
Steps: Connect wallet to register → Settings bind email and phone → API Key Management create keys
Detailed instructions: https://gateweb3.gitbook.io/gate_dex_api/exploredexapi/en/api-access-and-usage/developer-platform
```

**If file already exists**:

1. Read and parse JSON
2. Check if `api_key` equals `7RAYBKMG5MNMKK7LN6YGCO5UDI` (i.e., default credentials)
   - Yes → Append a line in subsequent response: `"Currently using public default credentials (Basic tier 2 RPS limit), recommend visiting https://web3.gate.com/zh/api-config to create exclusive AK/SK"`
   - No → No prompt

### 2.2 Verify Credentials Validity

Send a test request using `trade.swap.chain` (see Chapter 4 API Call Specifications). If returns `code: 0` then credentials valid; otherwise prompt user based on error code (see Chapter 10 Error Handling).

---

## III. Credential Management

### 3.1 Configuration File Format

File path: `~/.gate-dex-openapi/config.json` (absolute path, shared across all workspaces)

```json
{
  "api_key": "Your API Key",
  "secret_key": "Your Secret Key",
  "default_chain_id": 1,
  "default_slippage": 0.03,
  "default_slippage_type": 1
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| api_key | string | Yes | API Key (built-in default, user can replace) |
| secret_key | string | Yes | Secret Key (built-in default, user can replace) |
| default_chain_id | int | No | Default chain ID, ask user each time if omitted |
| default_slippage | float | No | Default slippage recommendation, 0.03 = 3% |
| default_slippage_type | int | No | 1 = percentage mode, 2 = fixed value mode |

### 3.2 Built-in Default Credentials

```
AK: 7RAYBKMG5MNMKK7LN6YGCO5UDI
SK: COnwcshYA3EK4BjBWWrvwAqUXrvxgo0wGNvmoHk7rl4.6YLniz4h
```

### 3.3 Secure Display Rules

- **Never display complete SK in conversation**. Only show last 4 digits, format: `sk_****z4h`
- When user requests to view current configuration, AK can be fully displayed, SK must be masked
- Configuration file stored in `~/.gate-dex-openapi/config.json` (user home directory, not in workspace), naturally won't be tracked by git
- Recommend setting file permission `chmod 600`, owner read/write only

### 3.4 Update Credentials

When user says "update AK/SK" or "replace keys":
1. Use AskQuestion tool to ask for new AK
2. Use AskQuestion tool to ask for new SK
3. Update `api_key` and `secret_key` fields in `~/.gate-dex-openapi/config.json`
4. Verify new credentials validity using `trade.swap.chain`
5. Verification success → prompt "credentials updated"; verification failure → rollback and prompt error reason

---

## IV. API Call Specifications

### 4.1 Basic Information

- **Unified Endpoint**: `POST https://openapi.gateweb3.cc/api/v1/dex`
- **Content-Type**: `application/json`
- **All interfaces share the same endpoint**, distinguished by the `action` field in request body

Request body format:

```json
{"action":"trade.swap.xxx","params":{...}}
```

### 4.2 API Call Method

Use the helper script for all API calls (handles HMAC-SHA256 signing automatically):

```bash
python3 gate-dex-trade/scripts/gate-api-call.py "<action>" '<params_json>'
```

The script reads AK/SK from ~/.gate-dex-openapi/config.json, computes signature, and sends the request.

### 4.5 Universal Response Format

All APIs return unified format:

```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- `code == 0` means success
- `code != 0` means error, see Chapter 10 Error Handling

---

## V. Tool Specifications (9 Actions)

### Action 1: trade.swap.chain

**Function**: Query all supported chain lists.

**Request Parameters**: None

**Request Example**:

```json
{"action":"trade.swap.chain","params":{}}
```

**Response Example**:

```json
{
  "code": 0,
  "message": "success",
  "data": [
    {"chain_id": "1", "chain": "eth", "chain_name": "Ethereum", "native_currency": "ETH", "native_decimals": 18, "native_address": ""},
    {"chain_id": "56", "chain": "bsc", "chain_name": "BNB Smart Chain", "native_currency": "BNB", "native_decimals": 18},
    {"chain_id": "501", "chain": "solana", "chain_name": "Solana", "native_currency": "SOL", "native_decimals": 9}
  ]
}
```

**Agent Behavior**:
- Before call: No special prerequisites, already called once during Step 0 credential verification
- After call: Display all chains in table format (chain_name, chain_id, native_currency)
- On error: See Chapter 10 general error handling

---

### Action 2: trade.swap.gasprice

**Function**: Query real-time Gas price for specified chain. Does not support Ton chain.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |

**Request Example**:

```json
{"action":"trade.swap.gasprice","params":{"chain_id":56}}
```

**Response Example (EVM chains)**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "native_coin_price": "1000.12",
    "native_decimal": 18,
    "low_pri_wei_per_gas": 50000000,
    "avg_pri_wei_per_gas": 52762481,
    "fast_pri_wei_per_gas": 100000000,
    "base_wei_fee": 0,
    "support_eip1559": true
  }
}
```

**Response format varies by chain type**:
- EVM: `low/avg/fast_pri_wei_per_gas`, `base_wei_fee`, `support_eip1559`
- Solana: `low/avg/fast/super_fast_microlp_per_cu`, `base_microlp_per_signature`
- Tron: `base_energy_price`, `base_bandwidth_price`
- SUI: `low/avg/fast_mist_per_gas`

**Agent Behavior**:
- Before call: If user didn't specify chain, use `default_chain_id` from config file; if not configured, use AskQuestion to inquire
- After call: Convert Gas prices to human-readable format (Gwei etc.), display low/medium/fast tiers
- On error: See Chapter 10 general error handling

---

### Action 3: trade.swap.quote

**Function**: Get Swap optimal quotes and route splits. The returned `quote_id` is required for subsequent steps.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |
| token_in | string | Yes | Input token contract address. **Native token uniformly use `"-"`** |
| token_out | string | Yes | Output token contract address. **Native token uniformly use `"-"`** |
| amount_in | string | Yes | Input amount, human-readable format (e.g., `"0.1"`, not wei) |
| slippage | float | Yes | Slippage, 0.01 = 1% |
| slippage_type | int | Yes | 1 = percentage mode, 2 = fixed value mode |
| user_wallet | string | Yes | User wallet address |
| fee_recipient | string | No | Custom fee recipient address |
| fee_rate | string | No | Custom trading fee rate (max 3%) |

**Request Example (Solana: SOL → USDC)**:

```json
{"action":"trade.swap.quote","params":{"chain_id":501,"token_in":"-","token_out":"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v","amount_in":"0.001","slippage":0.05,"slippage_type":1,"user_wallet":"2ycvS9CiMZfNyoGoR6nsxDkdxZwzjLaWB9Pa5G8dxZ5d"}}
```

**Response Example**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "amount_in": "0.001",
    "amount_out": "0.169966",
    "min_amount_out": "0.161467",
    "slippage": "0.050000",
    "system_slippage": "0.010000",
    "slippage_type": 1,
    "quote_id": "137a3700c558a584e73b2ed18fd77d79",
    "from_token": {
      "token_symbol": "WSOL",
      "chain_id": 501,
      "token_contract_address": "So11111111111111111111111111111111111111112",
      "decimal": 9,
      "token_price": "169.77",
      "is_native_token": 1
    },
    "to_token": {
      "token_symbol": "USDC",
      "chain_id": 501,
      "token_contract_address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
      "decimal": 6,
      "token_price": "0.9999",
      "is_native_token": 0
    },
    "protocols": [
      [[{"name": "ORCA", "part": 100, "fromTokenAddress": "So11...", "toTokenAddress": "EPjF..."}]]
    ],
    "trading_fee": {"rate": "0.003", "enable": true}
  }
}
```

**Key Response Fields**:
- `quote_id` — Required for subsequent approve/build
- `amount_out` — Estimated output amount
- `min_amount_out` — Minimum output amount after deducting slippage
- `from_token` / `to_token` — Token details (symbol, price, decimal, is_native_token)
- `protocols` — Three-level nested array: route splits → multi-hop paths → single step (name, part percentage, from/to addresses)
- `system_slippage` — System automatically added extra slippage
- `trading_fee` — Trading fee information

**Agent Behavior**:
- Before call:
  1. Determine chain (smart inference: user says ETH → chain_id=1; says SOL → chain_id=501; says USDT etc. multi-chain tokens → must use AskQuestion to inquire which chain to operate on)
  2. **Cross-chain detection**: If user intends to swap A chain tokens for B chain tokens (like "swap USDT on ETH for SOL on Solana"), **immediately intercept and prompt**:
     ```
     Current OpenAPI does not support cross-chain swaps, only supports Swap within same chain.
     For cross-chain transactions, please install Gate MCP service: https://github.com/gate/gate-mcp
     ```
     **Terminate process, do not continue calling quote.**
  3. Determine token contract addresses (see Chapter 6 token address resolution rules)
  4. Determine wallet address (see Chapter 9 signature strategy to get address)
  5. Determine slippage (use AskQuestion to inquire, provide recommended values: EVM chains recommend 1-3%, Solana recommend 3-5%, small chains recommend 3-5%)
  6. **After all above determined, execute SOP Step 1 trading pair confirmation** (see Chapter 8)
- After call: **Execute SOP Step 2 quote details display** (see Chapter 8), transparently display complete routing path
- On error:
  - 31104 (trading pair not found) → Prompt user to check if token contract addresses are correct
  - 31105/31503 (insufficient liquidity) → Suggest reducing amount or retry later
  - 31111 (Gas fee exceeds output) → Prompt transaction not cost-effective
  - 31109 (price impact too large) → Display risk warning
  - Others → See Chapter 10

---

### Action 4: trade.swap.approve_transaction

**Function**: Get approve calldata for ERC20 tokens. Only required for EVM and Tron chains, and only when token_in is not native token.

**When to call this interface**:

Must satisfy all of the following conditions simultaneously:
1. Chain type is EVM or Tron (Solana/SUI/Ton don't need approve)
2. `token_in` is not native token (i.e., token_in is not `"-"`, or quote returned `from_token.is_native_token != 1`)
3. On-chain queried allowance is insufficient (see Chapter 9 ERC20 Allowance Check)

**If token_in is native token (ETH/BNB/POL etc.), skip this step directly.**

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_wallet | string | Yes | User wallet address |
| approve_amount | string | Yes | Approve amount (human-readable format, equal to transaction amount) |
| quote_id | string | Yes | quote_id obtained from quote step |

**Request Example**:

```json
{"action":"trade.swap.approve_transaction","params":{"user_wallet":"0xBb43e9e205139A8bB849d6f408A07461A1E92af8","approve_amount":"0.001","quote_id":"6e7b2c16f500dd58e794a28e0b339eee"}}
```

**Response Example**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "data": "0x095ea7b3000000000000000000000000459e945e8d06c1ed6bffa8b9d135973a98a864e800000000000000000000000000000000000000000000000000000000000003e8",
    "approve_address": "0x459E945e8D06c1ed6BfFa8B9D135973A98A864E8",
    "gas_limit": "63601"
  }
}
```

**Response Fields**:
- `data` — approve call's calldata (hex encoded), needs signing
- `approve_address` — Approve target contract address (signed transaction's `to` field)
- `gas_limit` — Recommended gas limit

**Agent Behavior**:
- Before call: First execute ERC20 Allowance check (see Chapter 9), confirm approve is indeed needed
- After call:
  1. Display approve information to user: "Need to approve [token_symbol] to routing contract [approve_address], approve amount [approve_amount]"
  2. Use AskQuestion for confirmation: options are "Confirm Approve"/"Cancel"
  3. After confirmation, go through signing path to sign approve transaction (construct unsigned_tx: to=approve_address, data=returned data, value=0, gas_limit=returned gas_limit)
- On error: See Chapter 10 general error handling

---

### Action 5: trade.swap.build

**Function**: Build unsigned Swap transaction. Returns `unsigned_tx` (needs local signing) and `order_id` (required for submission).

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |
| amount_in | string | Yes | Input amount (human-readable format) |
| token_in | string | Yes | Input token contract address, native token use `"-"` |
| token_out | string | Yes | Output token contract address, native token use `"-"` |
| slippage | string | Yes | Slippage (0.01 = 1%) |
| slippage_type | string | Yes | 1 = percentage, 2 = fixed value |
| user_wallet | string | Yes | User wallet address |
| receiver | string | Yes | Receiver address (defaults to same as user_wallet) |
| quote_id | string | No | ID obtained from quote (strongly recommend passing for price consistency) |
| sol_tip_amount | string | No | Solana MEV protection Tip amount (lamports) |
| sol_priority_fee | string | No | Solana Priority Fee (micro-lamports per CU) |

**Request Example (EVM: USDT → WETH)**:

```json
{"action":"trade.swap.build","params":{"chain_id":1,"amount_in":"0.01","token_in":"0xdAC17F958D2ee523a2206206994597C13D831ec7","token_out":"0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2","slippage":"0.50","slippage_type":"1","user_wallet":"0xBb43e9e205139A8bB849d6f408A07461A1E92af8","receiver":"0xBb43e9e205139A8bB849d6f408A07461A1E92af8","quote_id":"c0a8c273945488ad1edcc4bdbaf8f9a8"}}
```

**Response Example**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "unsigned_tx": {
      "to": "0x459E945e8D06c1ed6BfFa8B9D135973A98A864E8",
      "data": "0x140a50ef0000...",
      "value": "0",
      "chain_id": 1,
      "gas_limit": 314090
    },
    "order_id": "0x4202a80fa66e7c906d003f39037ee81d772e076d178455244d5038bfc1c05a02",
    "ts": 1762855061,
    "amount_in": "0.01",
    "amount_out": "0.000003850827713117",
    "min_amount_out": "0.000001925413856558",
    "slippage": "0.500000",
    "system_slippage": "0.050000",
    "slippage_type": 1,
    "quote_id": "c0a8c273945488ad1edcc4bdbaf8f9a8",
    "from_token": {"token_symbol": "USDT", "decimal": 6, "token_price": "0.9999"},
    "to_token": {"token_symbol": "WETH", "decimal": 18, "token_price": "3554.17"},
    "protocols": [[
      [{"name": "UNISWAP_V2", "part": 100, "fromTokenAddress": "0xdac17f...", "toTokenAddress": "0x438532..."}],
      [{"name": "UNISWAP_V2", "part": 100, "fromTokenAddress": "0x438532...", "toTokenAddress": "0xc02aaa..."}]
    ]]
  }
}
```

**Key Response Fields**:
- `unsigned_tx.to` — Target contract address
- `unsigned_tx.data` — Call data (hex encoded)
- `unsigned_tx.value` — Native token send value ("0" for non-native tokens)
- `unsigned_tx.gas_limit` — Gas limit
- `unsigned_tx.chain_id` — Chain ID (used for signing)
- `order_id` — Order unique identifier, must pass to submit and status steps

**Solana Special Handling**:
- Build request can pass `sol_tip_amount` (Jito MEV protection Tip, unit lamports, recommend 10000-100000) and `sol_priority_fee` (priority fee, unit micro-lamports per CU, recommend 50000-500000)
- Returned `unsigned_tx.data` is base64 encoded VersionedTransaction bytes
- Must refresh `recentBlockhash` before signing (Solana's blockhash validity period is about 60-90 seconds)

**Agent Behavior**:
- Before call: Ensure quote step completed and passed SOP Step 1 and Step 2 confirmation
- After call: **Execute SOP Step 3 signature authorization confirmation** (see Chapter 8), display unsigned_tx summary
- On error:
  - 31501 (insufficient balance) → Prompt user insufficient balance
  - 31502 (slippage too low) → Prompt user to increase slippage
  - 31500 (parameter error) → Display message field content
  - Others → See Chapter 10

---

### Action 6: trade.swap.submit

**Function**: Submit signed transaction. Supports two modes: API broadcast on behalf, or client self-broadcast then report tx_hash.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| order_id | string | Yes | order_id returned from build step |
| signed_tx_string | string | Either/Or | Signed transaction string (let API broadcast on behalf). **Must be JSON array format string**, like `'["0x02f8b2..."]'`. EVM chain internal hex must be EIP-1559 Type 2 format (`0x02` prefix) |
| tx_hash | string | Either/Or | Transaction hash (client self-broadcast then report, API only tracks status) |
| signed_approve_tx_string | string | No | Signed approve transaction (pass together when approve needed, only for signed_tx_string mode). **Also must be JSON array format**, like `'["0x02f871..."]'` |

> **`signed_tx_string` and `tx_hash` choose one**: If client self-broadcast transaction, pass `tx_hash`; if want API to broadcast on behalf, pass `signed_tx_string`.
>
> **Important: `signed_tx_string` and `signed_approve_tx_string` values must be JSON array format strings** (like `'["0x02f8..."]'`), not raw hex strings. Server will do `json.Unmarshal` parsing on this field, raw hex will cause `error_code: 50005` (`invalid character 'x' after top-level value`).

**Request Example (Mode A: API broadcast on behalf)**:

```json
{"action":"trade.swap.submit","params":{"order_id":"0x4202a80fa66e7c906d003f39037ee81d772e076d178455244d5038bfc1c05a02","signed_tx_string":"[\"0x02f8b20181...\"]","signed_approve_tx_string":"[\"0x02f8710181...\"]"}}
```

If no approve needed, omit `signed_approve_tx_string` field:

```json
{"action":"trade.swap.submit","params":{"order_id":"0x4202...","signed_tx_string":"[\"0x02f8b20181...\"]"}}
```

**Request Example (Mode B: Client self-broadcast then report)**:

```json
{"action":"trade.swap.submit","params":{"order_id":"0x7d13dd777858b0633e590f4944b6837489e9ffa9c7b9255c120645b51b5dfbed","tx_hash":"0x3911b4f30175ef041ffb6ad035a8ca9124192355a0600ad2b9f0d2d9c3785bb7"}}
```

**Response Example**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "order_id": "0x4202a80fa66e7c906d003f39037ee81d772e076d178455244d5038bfc1c05a02",
    "tx_hash": "0x3911b4f30175ef041ffb6ad035a8ca9124192355a0600ad2b9f0d2d9c3785bb7"
  }
}
```

**Agent Behavior**:
- Before call: Ensure signing completed (swap transaction + optional approve transaction)
- After call: Display "Transaction submitted, tx_hash: [hash]", then automatically enter status polling (Action 7)
- Submission strategy selection: See Chapter 9 9.3.4 Submission Strategy
- On error:
  - 31601 (order_id expired / signature verification failed) → Prompt user need to re-execute build step
  - Others → See Chapter 10

---

### Action 7: trade.swap.status

**Function**: Query order execution status. Automatically polled after submit.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |
| order_id | string | Yes | Order ID |
| tx_hash | string | Yes | Transaction hash (can pass empty string `""`) |

**Request Example**:

```json
{"action":"trade.swap.status","params":{"chain_id":1,"order_id":"0x4202a80fa66e7c906d003f39037ee81d772e076d178455244d5038bfc1c05a02","tx_hash":""}}
```

**Key Response Fields**:

| Field | Description |
|-------|-------------|
| order_id | Order ID |
| status | Transaction status |
| tx_hash | Transaction hash |
| tx_hash_explorer_url | Block explorer link |
| amount_in / amount_out | Actual input/output amounts |
| expect_amount_out | Expected output amount |
| gas_fee / gas_fee_symbol | Gas fee and token symbol |
| pools[] | Used liquidity pool list (name, dex, address) |
| creationTime / endTime | Creation and end time |

**Agent Behavior (Auto Polling)**:
- Automatically start polling after submit success
- Call `trade.swap.status` every 5 seconds
- Display waiting status to user during polling: "Waiting for on-chain confirmation... (waited Xs)"
- Poll maximum 60 seconds (12 times)
- Polling end conditions:
  - status not pending → Display final result
  - Still pending after 60 seconds → Display "Transaction still processing" and provide block explorer link for user to check manually
- Display final result including: status, actual output amount, Gas fee, block explorer link

---

### Action 8: trade.swap.history

**Function**: Query historical Swap orders with pagination.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_wallet | string[] | Yes | User wallet address array |
| page_number | int | No | Page number (default 1) |
| page_size | int | No | Items per page (default 100, max 100) |
| chain_id | int | No | Filter by chain (optional) |

**Request Example**:

```json
{"action":"trade.swap.history","params":{"user_wallet":["0xBb43e9e205139A8bB849d6f408A07461A1E92af8"],"pageNum":1,"pageSize":10}}
```

**Response Format**: Paginated order list (`total`, `page_number`, `page_size`, `orders[]`), each record contains same fields as `trade.swap.status`.

**Agent Behavior**:
- Before call: Need user wallet address. If known (used in previous flow) use directly, otherwise ask user
- After call: Display history in table format (time, chain, from_token → to_token, amount, status)
- On error: 31701 (no transaction history) → Prompt "No history records"

---

## VI. Supported Chains & Token Address Resolution

### 6.1 Supported Chain List

| chain_id | Short Name | Full Name | Native Token | Chain Type |
|----------|------------|-----------|--------------|------------|
| 1 | eth | Ethereum | ETH | EVM |
| 56 | bsc | BNB Smart Chain | BNB | EVM |
| 137 | polygon | Polygon | POL | EVM |
| 42161 | arbitrum | Arbitrum One | ETH | EVM |
| 10 | optimism | Optimism | ETH | EVM |
| 8453 | base | Base | ETH | EVM |
| 43114 | avalanche | Avalanche C | AVAX | EVM |
| 59144 | linea | Linea | ETH | EVM |
| 324 | zksync | zkSync Era | ETH | EVM |
| 81457 | blast | Blast | ETH | EVM |
| 4200 | merlin | Merlin | BTC | EVM |
| 480 | world | World Chain | ETH | EVM |
| 10088 | gatelayer | Gate Layer | GT | EVM |
| 501 | solana | Solana | SOL | Solana |
| 784 | sui | Sui | SUI | SUI |
| 195 | tron | Tron | TRX | Tron |
| 607 | ton | Ton | TON | Ton |

> Subject to real-time returns from `trade.swap.chain` interface.

### 6.2 Smart Chain Inference Rules

When user doesn't explicitly specify chain, Agent infers by following rules:

**Situations where chain can be determined** (use directly, no need to ask):
- User says "ETH" → chain_id=1 (Ethereum)
- User says "SOL" → chain_id=501 (Solana)
- User says "BNB" → chain_id=56 (BSC)
- User says "AVAX" → chain_id=43114 (Avalanche C)
- User says "GT" → chain_id=10088 (Gate Layer)
- User says "POL" → chain_id=137 (Polygon)
- User says "SUI" → chain_id=784 (Sui)
- User says "TRX" → chain_id=195 (Tron)
- User says "TON" → chain_id=607 (Ton)
- User says "BTC" and context is Merlin → chain_id=4200 (Merlin)
- User says "on Arbitrum" or "arb chain" → chain_id=42161

**Situations where chain cannot be determined** (must use AskQuestion to inquire):
- USDT, USDC, WETH, DAI etc. tokens exist on multiple chains
- User doesn't mention any chain-related information

AskQuestion chain inquiry example:

```
Please select which chain to trade on:
A. Ethereum (chain_id: 1)
B. BSC (chain_id: 56)
C. Arbitrum (chain_id: 42161)
D. Base (chain_id: 8453)
E. Solana (chain_id: 501)
F. Other (please tell me chain name or chain_id)
```

### 6.3 Token Address Resolution Rules

API requires token contract addresses, but users usually only provide token symbols. Resolution priority:

**Step 1: Native Token Judgment**

If token is the chain's native token (ETH on Ethereum, BNB on BSC, SOL on Solana etc.), use `"-"` as token address.

**Step 2: Query Market Skill**

Try calling `gate-dex-openmarket` Skill to query token contract addresses. This Skill uses same AK/SK credentials.

> Note: If `gate-dex-openmarket` Skill is currently unavailable, skip to Step 3.

**Step 3: Common Token Quick Reference**

The following are contract addresses of common tokens on major chains, Agent can use directly:

**Ethereum (chain_id: 1)**:

| Token | Contract Address |
|-------|------------------|
| USDT | 0xdAC17F958D2ee523a2206206994597C13D831ec7 |
| USDC | 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 |
| WETH | 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 |
| WBTC | 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599 |
| DAI | 0x6B175474E89094C44Da98b954EedeAC495271d0F |

**BSC (chain_id: 56)**:

| Token | Contract Address |
|-------|------------------|
| USDT | 0x55d398326f99059fF775485246999027B3197955 |
| USDC | 0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d |
| WBNB | 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c |
| BUSD | 0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56 |

**Arbitrum (chain_id: 42161)**:

| Token | Contract Address |
|-------|------------------|
| USDT | 0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9 |
| USDC | 0xaf88d065e77c8cC2239327C5EDb3A432268e5831 |
| WETH | 0x82aF49447D8a07e3bd95BD0d56f35241523fBab1 |

**Base (chain_id: 8453)**:

| Token | Contract Address |
|-------|------------------|
| USDC | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 |
| WETH | 0x4200000000000000000000000000000000000006 |

**Solana (chain_id: 501)**:

| Token | Contract Address |
|-------|------------------|
| USDC | EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v |
| USDT | Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB |
| WSOL | So11111111111111111111111111111111111111112 |

**Step 4: Request User to Provide**

If none of above can resolve, inform user: "Cannot automatically identify [token name] contract address on [chain name], please provide contract address."

**Step 5: Confirmation**

Regardless of which method obtained contract address, **must confirm with user**: "About to use [token symbol] ([contract address first 6 digits...last 4 digits]) on [chain name] for trading, confirm?"

---

## VII. Operational Flows

### Flow A: Query Operations (No Confirmation Gate)

Applicable to: trade.swap.chain, trade.swap.gasprice, trade.swap.status, trade.swap.history

```
User makes query request
    |
    v
[Step 0 Environment Detection] → Ensure credentials available
    |
    v
Call corresponding Action
    |
    v
Format and display results
```

### Flow B: Complete Swap Flow (Three-Step Confirmation Gate)

```
User: "Swap 0.1 ETH for USDT"
    |
    v
[Step 0 Environment Detection] → Ensure credentials available
    |
    v
[Parameter Collection]
    ├── Determine chain: Smart inference or AskQuestion
    ├── Determine token addresses: Quick reference / Market Skill / User provided
    ├── Determine wallet address: Agent derivation / User provided
    ├── Determine slippage: AskQuestion (with recommended values)
    └── Confirm tokens and addresses correct
    |
    v
[SOP Step 1] Trading pair confirmation → AskQuestion (see Chapter 8)
    |
    v  User confirms
[Call trade.swap.quote] Get quotes
    |
    v
[SOP Step 2] Quote details display → Transparently display routing
    |     Price impact > 5% → Risk warning AskQuestion
    v  User confirms
[Call trade.swap.build] Build unsigned transaction
    |
    v
[ERC20 Approve Judgment]
    ├── Chain is EVM/Tron and token_in not native token?
    │     ├── No → Skip approve
    │     └── Yes → On-chain query allowance
    │           ├── allowance >= transaction required amount (precision aligned comparison) → Skip approve
    │           └── allowance < transaction required amount → Need approve
    │                 1. Call trade.swap.approve_transaction get approve calldata
    │                 2. AskQuestion confirm authorization
    │                 3. Agent self-sign approve transaction
    │                 4. Record signed_approve_tx_string (pass together during submit)
    |
    v
[SOP Step 3] Signature authorization confirmation → AskQuestion (see Chapter 8)
    |
    v  User confirms
[Signing Path]
    └── Agent self-handle signing (see Chapter 9)
    |
    v  Obtain signed_tx_string (+ optional signed_approve_tx_string)
[Call trade.swap.submit] Submit transaction
    |
    v
[Auto poll trade.swap.status]
    Query every 5 seconds, max 60 seconds
    |
    v
Display final result: status, actual output amount, Gas fee, block explorer link
```

### Flow C: History Query

```
User: "View my Swap history"
    |
    v
[Step 0 Environment Detection]
    |
    v
Determine user wallet address (reuse if known, otherwise ask)
    |
    v
[Call trade.swap.history]
    |
    v
Display history in table format
```

---

## VIII. Confirmation Gate Templates (SOP Three-Step Confirmation)

All Swap operations involving funds must go through the following three-step confirmation, **cannot be skipped or merged**.

### SOP Step 1: Trading Pair Confirmation

**Trigger Timing**: After parameter collection completed, before calling quote.

**Display Template**:

```
========== Swap Trading Pair Confirmation ==========
  Chain: {chain_name} (chain_id: {chain_id})
  Sell: {amount_in} {from_token_symbol}
  Buy: {to_token_symbol}
  Slippage: {slippage}% ({slippage_type_text})
  Wallet: {user_wallet_short}
====================================================
```

Where `{user_wallet_short}` format is `0x1234...abcd` (first 6 digits + last 4 digits).

**AskQuestion Call**:

```json
{
  "questions": [{
    "id": "swap_confirm_step1",
    "prompt": "Please confirm the above trading pair information",
    "options": [
      {"id": "confirm", "label": "Confirm, get quote"},
      {"id": "change_slippage", "label": "Modify slippage"},
      {"id": "change_amount", "label": "Modify amount"},
      {"id": "cancel", "label": "Cancel transaction"}
    ]
  }]
}
```

**Agent Handling**:
- `confirm` → Call trade.swap.quote
- `change_slippage` → Re-use AskQuestion to ask for new slippage value
- `change_amount` → Re-use AskQuestion to ask for new amount
- `cancel` → Terminate process, display "Transaction cancelled"

### SOP Step 2: Quote Details

**Trigger Timing**: After quote successfully returns.

**Display Template**:

```
========== Swap Quote Details ==========
  Sell: {amount_in} {from_token_symbol} (≈ ${from_value_usd})
  Buy: ≈ {amount_out} {to_token_symbol}
  Minimum receive: {min_amount_out} {to_token_symbol} (including {slippage}% slippage)
  Price impact: {price_impact}%
  Route: {route_display}
  Estimated Gas: Subject to build return
=======================================
```

**Route Display Format** (transparently display complete path):

Single route single hop:
```
UNISWAP_V3 (100%)
```

Single route multi-hop:
```
UNISWAP_V2: USDT → WBTC → WETH (100%)
```

Multi-route split:
```
UNISWAP_V3: ETH → USDT (60%)
SUSHISWAP: ETH → USDC → USDT (40%)
```

**Price Impact Risk Judgment**:

Calculate price impact: `price_impact = abs(1 - (amount_out * to_token_price) / (amount_in * from_token_price)) * 100`

- Price impact <= 5% → Normal flow, display AskQuestion confirmation
- Price impact > 5% → **Mandatory trigger risk warning**

**Normal Flow AskQuestion**:

```json
{
  "questions": [{
    "id": "swap_confirm_step2",
    "prompt": "Please confirm the above quote information",
    "options": [
      {"id": "confirm", "label": "Confirm, build transaction"},
      {"id": "change_amount", "label": "Modify amount and re-quote"},
      {"id": "cancel", "label": "Cancel transaction"}
    ]
  }]
}
```

**Risk Warning AskQuestion** (price impact > 5%):

```json
{
  "questions": [{
    "id": "swap_risk_warning",
    "prompt": "⚠️ Risk Warning: Current price impact is {price_impact}%, exceeding 5% safety threshold. Large price impact may cause significant asset loss.",
    "options": [
      {"id": "accept_risk", "label": "I understand the risk, continue transaction"},
      {"id": "reduce_amount", "label": "Reduce transaction amount"},
      {"id": "cancel", "label": "Cancel transaction"}
    ]
  }]
}
```

### SOP Step 3: Signature Authorization Confirmation

**Trigger Timing**: After build successfully returns unsigned_tx.

**Display Template**:

```
========== Signature Authorization Confirmation ==========
  Target contract: {unsigned_tx.to}
  Send amount: {unsigned_tx.value} (raw value)
  Gas limit: {unsigned_tx.gas_limit}
  Chain ID: {unsigned_tx.chain_id}
  Data prefix: {first 20 chars of unsigned_tx.data}...
  Order ID: {first 10 chars of order_id}...
==========================================================
```

**AskQuestion Call**:

```json
{
  "questions": [{
    "id": "swap_confirm_step3",
    "prompt": "Please confirm the above transaction information and authorize signing",
    "options": [
      {"id": "confirm_sign", "label": "Confirm, sign and submit"},
      {"id": "cancel", "label": "Cancel transaction"}
    ]
  }]
}
```

**Agent Handling**:
- `confirm_sign` → Enter signing path (see Chapter 9)
- `cancel` → Terminate process, display "Transaction cancelled"

---

## IX. Signing Strategy

Skill does not manage private keys, does not provide signing scripts. Signing is handled by Agent at runtime.

**Important Constraint: Agent must not create, write, or modify any code files in user's workspace (repository).** All signing operations must be completed through Shell tool executing one-time commands (like `python3 -c '...'` or `node -e '...'`), must not generate temporary script files.

### 9.1 Get Wallet Address

Both signing and transactions require wallet address. Agent should guide user to provide private key or mnemonic, then automatically derive address.

**When need user to provide private key, must first display the following security notice**:

```
🔐 Security Notice:
You can directly paste private key in conversation, private key is only used locally 
for signing, will not be uploaded to any server, nor sent to API.
Private key will not be retained or stored after signing completed.
```

### 9.2 Sign unsigned_tx

Use the helper scripts for signing (handles all chain-specific logic):

**EVM**: `echo "PRIVATE_KEY" | python3 scripts/sign-tx-evm.py '<unsigned_tx_json>' '<rpc_url>'`
**Solana**: `echo "PRIVATE_KEY" | node scripts/sign-tx-sol.js '<unsigned_tx_base64>' '<rpc_url>'`
**SUI/Ton**: Use `node -e` inline with the appropriate SDK.

All scripts output `{"signed_tx_string": "[\"...\"]"}` in the JSON array format required by submit API.

### 9.3 Agent Methods to Get Private Keys

Skill does not specify how Agent gets private keys. Agent handles flexibly based on context:

1. **Ask user to paste directly**: First display security notice from 9.1, clearly inform private key only used in local context, won't upload to any server, then wait for user to paste private key
2. **Ask user to provide file path**: Like keystore file, `PRIVATE_KEY` variable in .env file
3. **Read existing key files in user workspace**: If Agent finds .env or keystore files in context

Regardless of method, **do not retain or display private key content in conversation after signing completed**. If user pasted private key in conversation, prompt after signing completed: "Signing completed, recommend clearing private key messages in conversation history."

### 9.4 Submission Strategy (API Broadcast vs Self-Broadcast)

After signing completed, there are two ways to submit transaction on-chain:

**Strategy A: API Broadcast on Behalf (Priority)**

Pass `signed_tx_string` to `trade.swap.submit`, let Gate API server broadcast.

- Pros: Simple process, one API call completes broadcast + order association
- **Key format requirement: `signed_tx_string` must be JSON array format string** (like `'["0x02f8..."]'`), not raw hex string. Server will do `json.Unmarshal` parsing on this field, raw hex will cause `error_code: 50005`
- EVM chains: Hex inside array must be EIP-1559 Type 2 format (starts with `0x02`)
- Solana: Inside array is Base58 encoded
- SUI/Ton: Inside array is Base64 encoded
- If API returns success but status polling shows `error_code: 50005`, check if `signed_tx_string` is JSON array format, if still can't resolve then switch to Strategy B

**Strategy B: Self-Broadcast + Report tx_hash (Fallback)**

Agent first broadcasts transaction via chain's public RPC nodes (like EVM's `eth_sendRawTransaction`), get `tx_hash`, then pass `tx_hash` to `trade.swap.submit` for order status association.

- Applicable scenario: Fallback when Strategy A fails
- Pros: Not dependent on API's signature format parsing capability, compatible with Legacy / EIP-1559 etc. all formats
- Process:
  1. Broadcast via RPC: `w3.eth.send_raw_transaction(signed_tx.raw_transaction)`
  2. Get `tx_hash`
  3. Call `trade.swap.submit`, pass `order_id` + `tx_hash` (don't pass `signed_tx_string`)

```python
# Strategy B example (Python EVM)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
# Report to Gate API for order tracking
submit_resp = api_call({
    'action': 'trade.swap.submit',
    'params': {
        'order_id': order_id,
        'tx_hash': '0x' + tx_hash.hex()
    }
})
```

**Strategy A Python Example** (note JSON array format):

```python
import json
signed_tx_hex = '0x' + signed_tx.raw_transaction.hex()
submit_resp = api_call({
    'action': 'trade.swap.submit',
    'params': {
        'order_id': order_id,
        'signed_tx_string': json.dumps([signed_tx_hex])  # '["0x02f8..."]'
    }
})
```

**Agent Recommended Process**: First try Strategy A; if status polling finds `error_code: 50005` or similar format errors, automatically switch to Strategy B and re-execute (need to re-quote → build → sign → self-broadcast → submit tx_hash).

### 9.5 ERC20 Allowance Check

Use the helper script:
```bash
python3 scripts/check-allowance.py "<rpc_url>" "<token>" "<owner>" "<spender>" "<amount>" "<decimals>"
```
Returns `{"allowance_sufficient": true/false}`. If false, proceed with approve.

---

## X. Error Handling

When API returns `code != 0` it's an error. Agent should **display English message as-is**, and attach Chinese description and suggestions.

### 10.1 General Errors (Authentication/Signature/Rate Limiting)

| Error Code | Agent Handling |
|------------|----------------|
| 10001~10005 | Display original message. Suggest checking API call implementation, confirm 4 required Headers are complete. |
| 10008 | Display original message. Suggest: Signature mismatch, please check if SK is correct. Possible causes: JSON serialization format inconsistent (extra spaces?), signature path should be `/api/v1/dex`. |
| 10101 | Display original message. Suggest: Timestamp exceeds 30-second window, please check if system clock is accurate. |
| 10103 | Display original message. Suggest: Signature verification failed, please check if AK/SK is correct. Can use "update AK/SK" command to reconfigure. |
| 10111~10113 | Display original message. Suggest: IP whitelist issue. If using custom AK/SK, please go to developer platform (https://web3.gate.com/zh/api-config) to add current IP to whitelist. Default credentials have no such restriction. |
| 10121 | Display original message. Suggest: X-Request-Id format invalid, please confirm using standard UUIDv4 format. |
| 10122 | **Auto retry**: Generate new X-Request-Id and resend request. No need to notify user. |
| 10131~10133 | Display original message. Suggest: Requests too frequent. Default credentials are Basic tier (2 RPS), please wait 1-2 seconds and retry. For higher frequency, please create exclusive AK/SK. |

### 10.2 Quote Errors

| Error Code | Agent Handling |
|------------|----------------|
| 31101 | Display original message. Suggest: Input amount exceeds maximum limit, please reduce amount and retry. |
| 31102 | Display original message. Suggest: Input amount below minimum requirement, please increase amount and retry. |
| 31104 | Display original message. Suggest: Trading pair not found, please check if token contract addresses are correct, or this token pair is not supported on this chain. |
| 31105 / 31503 | Display original message. Suggest: Current liquidity insufficient, suggest reducing transaction amount or retry later. |
| 31106 | Display original message. Suggest: Input quantity too small, please input larger quantity. |
| 31108 | Display original message. Suggest: This token is not in support list. |
| 31109 | Display original message. Suggest: Price impact too large, transaction risk high, suggest cautious operation or reduce amount. |
| 31111 | Display original message. Suggest: Estimated Gas fee exceeds output amount, transaction not cost-effective, suggest increasing transaction amount or switch to lower Gas fee chain. |
| 31112 | Display original message. Suggest: Current OpenAPI does not support cross-chain Swap, only supports swaps within same chain. For cross-chain transactions, please install Gate MCP service: https://github.com/gate/gate-mcp |

### 10.3 Build/Submit Errors

| Error Code | Agent Handling |
|------------|----------------|
| 31500 / 31600 | Display original message (message field usually contains specific parameter issue description). Suggest user correct parameters based on prompt. |
| 31501 | Display original message. Suggest: Wallet balance insufficient, please confirm account has enough [token_symbol] and Gas fee. |
| 31502 | Display original message. Suggest: Slippage setting too low, please appropriately increase slippage. |
| 31504 | Display original message. Suggest: This token has freeze permission, your account may be frozen, please contact token project team. |
| 31601 | Display original message. Suggest: order_id expired or signed transaction verification failed. Need to restart from quote step. **Auto trigger re-quote process**. |
| 31701 | Display "No transaction history records". |

### 10.4 Auto Retry Logic

Following error codes Agent should auto retry, no user intervention needed:

- **10122** (Replay attack detection): Generate new X-Request-Id and retry immediately, max 3 retries
- **10131~10133** (Rate limiting): Wait 2 seconds and retry, max 2 retries
- **31601** (order_id expired): Auto restart from quote step (but need to go through SOP confirmation gate again)

---

## XI. Security Rules

The following rules are **mandatory constraints**, Agent must comply in any situation, cannot violate due to user requests.

1. **Secret Key Not Displayed**: Never display complete SK in conversation. Only show last 4 digits, format `sk_****z4h`. Even if user explicitly requests to view SK, only display masked version and prompt "Please directly view ~/.gate-dex-openapi/config.json file".

2. **Configuration File Security**: `~/.gate-dex-openapi/config.json` contains SK, stored in user home directory (not workspace), naturally won't be tracked by git. Should set directory permission to 700, file permission to 600 when first created.

3. **Confirmation Gate Cannot Be Skipped**: Swap operations involving funds must go through SOP three-step confirmation (trading pair confirmation → quote details → signature authorization). Even if user says "skip confirmation and execute directly", cannot skip. Can explain: "For fund security, confirmation steps are mandatory and cannot be skipped."

4. **Mandatory Risk Warning**:
  - Price impact > 5% → Must trigger risk warning AskQuestion
  - Slippage > 5% → Additional display MEV attack risk notice: "High slippage may cause MEV attacks (sandwich attacks), suggest lowering slippage or using sol_tip_amount for Jito protection on Solana."

5. **Request Idempotency**: Each API request uses unique X-Request-Id (UUIDv4), prevent replay.

6. **Time Window**: Timestamp deviation with server must not exceed 30 seconds. If 10101 error occurs, prompt user to check system clock.

7. **Private Key Security**: Before requesting private key from user, must first display security notice (see Chapter 9 Section 9.1), clearly inform private key only used in local context, won't upload to any server. Agent discards private key after obtaining and signing, don't retain in conversation history. Don't proactively write private key to files (unless user explicitly requests saving to specific location).

8. **Error Transparency**: All API errors display English message as-is, don't hide or tamper with error information. Agent attaches Chinese explanation and suggestions.

---

## Appendix: API Fee Description

| Tier | Price | Limit |
|------|-------|-------|
| Basic (Free) | Free | 2 RPS (2 requests per second) |
| Advanced (Paid) | Charged by call volume | Contact Gate team |

**Infrastructure Fee (Swap transactions only, deducted from on-chain transaction amount)**:

| Transaction Type | Rate |
|------------------|------|
| Swaps involving stablecoins | 0.3% |
| Swaps not involving stablecoins | 1.0% |