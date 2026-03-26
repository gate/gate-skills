# Account & Holdings

This module handles Alpha account balance queries and portfolio valuation.

## Workflow

### Step 1: Identify Query Type

Classify the request into one of two cases:
1. View all holdings (balances per currency)
2. Calculate total portfolio market value

### Step 2: Call Tools and Extract Data

Use the minimal tool set required:
- Account balances: `cex_alpha_list_alpha_accounts`
- Market prices (for valuation): `cex_alpha_list_alpha_tickers`

Key data to extract from accounts:
- `currency`: token symbol
- `available`: available balance
- `locked`: locked balance (in pending orders)
- `chain`: blockchain network
- `token_address`: contract address

Key data to extract from tickers (for valuation):
- `last`: latest price per token

### Step 3: Return Formatted Result

Present holdings or valuation in a clear format.

## Report Template

For holdings:

```markdown
## Alpha Holdings

| Currency | Available | Locked | Chain | Contract Address |
|----------|-----------|--------|-------|-----------------|
| {currency} | {available} | {locked} | {chain} | {token_address} |
```

For portfolio valuation:

```markdown
## Alpha Portfolio Valuation

| Currency | Quantity | Price (USDT) | Value (USDT) |
|----------|---------|-------------|-------------|
| {currency} | {available + locked} | {last} | {value} |

| **Total Portfolio Value** | **{total_value} USDT** |
```

---

## Scenario 14: View Holdings

**Context**: User wants to see all tokens held in their Alpha account.

**Prompt Examples**:
- "What coins do I have on Alpha?"
- "Show me my Alpha holdings."
- "What's in my Alpha account?"

**Expected Behavior**:
1. Call `cex_alpha_list_alpha_accounts`.
2. Extract all currency balances including available and locked amounts.
3. Present a table of all holdings with currency symbol, available balance, locked balance, chain, and contract address.
4. If no holdings exist, inform the user that their Alpha account is empty.

## Scenario 15: View Portfolio Market Value

**Context**: User wants to know the total USDT value of their Alpha holdings.

**Prompt Examples**:
- "How much is my Alpha portfolio worth?"
- "What's the total value of my Alpha holdings?"
- "Calculate my Alpha portfolio in USDT."

**Expected Behavior**:
1. Call `cex_alpha_list_alpha_accounts` to get all holdings.
2. Call `cex_alpha_list_alpha_tickers` to get latest prices for all held tokens.
3. For each holding, calculate value as `(available + locked) * last_price`.
4. Sum all values to get total portfolio value in USDT.
5. Present a per-token value breakdown table and the total portfolio value.
6. If any token's price is unavailable from tickers, note it as "price unavailable" and exclude from total.
