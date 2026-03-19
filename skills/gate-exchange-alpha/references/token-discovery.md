# Token Discovery & Browsing

This module handles all token browsing, filtering, and detail lookup on Gate Alpha.

## Workflow

### Step 1: Identify Query Type

Classify the request into one of five cases:
1. Browse all tradable currencies
2. Filter tokens by blockchain
3. Filter tokens by launch platform
4. Look up token by contract address
5. View specific token details (chain, address, precision, status)

### Step 2: Call Tools and Extract Data

Use the minimal tool set required:
- All currencies list: `cex_alpha_list_alpha_currencies`
- Token filtering (chain/platform/address): `cex_alpha_list_alpha_tokens`
- Specific currency details: `cex_alpha_list_alpha_currencies` with `currency` parameter

Key data to extract:
- `currency`: token symbol
- `name`: display name
- `chain`: blockchain network (note: may be uppercase like `SOLANA` or lowercase like `solana` depending on endpoint)
- `address`: contract address
- `precision`: price decimal places
- `amount_precision`: quantity decimal places
- `status`: 1 = trading, 2 = suspended, 3 = delisted

### Step 3: Return Formatted Result

Present results in a clear table format with relevant fields.

## Report Template

```markdown
## Token Discovery Result

| Item | Value |
|------|-------|
| Query Type | {query_type} |
| Filter | {filter_criteria} |
| Results Found | {count} |

### Token List

| Currency | Chain | Status | Contract Address |
|----------|-------|--------|-----------------|
| {currency} | {chain} | {status_text} | {address} |
```

---

## Scenario 1: Browse Tradable Currencies

**Context**: User wants to see all available currencies on Gate Alpha.

**Prompt Examples**:
- "What coins can I trade on Alpha?"
- "Show me all Alpha tokens."
- "List available currencies."

**Expected Behavior**:
1. Call `cex_alpha_list_alpha_currencies` with pagination (default `page=1`, `limit=20`).
2. Extract currency symbols, chains, contract addresses, and trading status.
3. Present a paginated table of tradable currencies. If there are more pages, inform the user and offer to show the next page.

## Scenario 2: Filter Tokens by Chain

**Context**: User wants to see tokens available on a specific blockchain.

**Prompt Examples**:
- "Show me Solana tokens on Alpha."
- "What coins are on BSC?"
- "List Alpha tokens on Ethereum."

**Expected Behavior**:
1. Normalize the chain name to the supported value (e.g., "Solana" → `solana`, "Ethereum" → `eth`, "BSC" → `bsc`).
2. Call `cex_alpha_list_alpha_tokens` with `chain={normalized_chain}`.
3. Present a filtered list of tokens on that chain with currency symbol, launch platform, and contract address.

## Scenario 3: Filter Tokens by Launch Platform

**Context**: User wants to see tokens from a specific launch platform.

**Prompt Examples**:
- "What new coins are on pump?"
- "Show me tokens from moonshot."
- "Any gatefun tokens available?"

**Expected Behavior**:
1. Normalize the platform name to the supported value (e.g., "pump" → `pump`, "Moonshot" → `moonshot`).
2. Call `cex_alpha_list_alpha_tokens` with `launch_platform={normalized_platform}`.
3. Present a filtered list of tokens from that platform with currency symbol, chain, and contract address.

## Scenario 4: Look Up Token by Contract Address

**Context**: User provides a contract address and wants to identify the token.

**Prompt Examples**:
- "What token is at this address 6p6xgH...?"
- "Look up contract 0xabc123..."
- "Check this address for me: So11111..."

**Expected Behavior**:
1. Call `cex_alpha_list_alpha_tokens` with `address={contract_address}`.
2. If found, return token details: currency symbol, chain, launch platform, and full contract address.
3. If not found, inform the user that no token matches the given address on Gate Alpha.

## Scenario 5: View Token Details

**Context**: User wants detailed information about a specific token including its chain and contract address.

**Prompt Examples**:
- "What chain is trump on? What's the contract address?"
- "Tell me about the ELON token on Alpha."
- "Show me details for memeboxtrump."

**Expected Behavior**:
1. Call `cex_alpha_list_alpha_currencies` with `currency={token_symbol}`.
2. Extract chain, contract address, precision, amount_precision, and status.
3. Present a detailed summary including trading status interpretation (1 = actively trading, 2 = suspended, 3 = delisted).

**Note**: When the API returns an empty result for a non-existent currency, it may return `[{}, {}]` (array with empty objects) instead of `[]`. Check if the returned objects have valid fields before processing.
