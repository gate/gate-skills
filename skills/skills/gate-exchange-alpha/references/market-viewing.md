# Market Viewing

This module handles Alpha token market data queries including all-market overview and single-token price checks.

## Workflow

### Step 1: Identify Query Type

Classify the request into one of two cases:
1. View all market tickers (overview)
2. View specific token price and market data

### Step 2: Call Tools and Extract Data

Use the minimal tool set required:
- All tickers: `cex_alpha_list_alpha_tickers`
- Specific token ticker: `cex_alpha_list_alpha_tickers` with `currency` parameter

Key data to extract:
- `currency`: token symbol
- `last`: latest price (USDT)
- `change`: 24h price change percentage
- `volume`: 24h trading volume (USDT)
- `market_cap`: market capitalization (USDT)

### Step 3: Return Formatted Result

Present market data in a clear, scannable format.

## Report Template

```markdown
## Alpha Market Overview

| Currency | Price (USDT) | 24h Change | 24h Volume (USDT) | Market Cap |
|----------|-------------|------------|-------------------|------------|
| {currency} | {last} | {change}% | {volume} | {market_cap} |
```

For single token:

```markdown
## {Currency} Market Data

| Item | Value |
|------|-------|
| Latest Price | {last} USDT |
| 24h Change | {change}% |
| 24h Volume | {volume} USDT |
| Market Cap | {market_cap} USDT |
```

---

## Scenario 6: View All Market Tickers

**Context**: User wants a broad overview of the Alpha market.

**Prompt Examples**:
- "How's the Alpha market doing?"
- "Show me all Alpha token prices."
- "What's the market like right now?"

**Expected Behavior**:
1. Call `cex_alpha_list_alpha_tickers` with pagination (default `page=1`, `limit=20`).
2. Extract latest price (`last`), 24h change (`change`), and 24h volume (`volume`) for each token.
3. Present a paginated market overview table sorted by default order. If there are more pages, inform the user.

## Scenario 7: View Specific Token Price

**Context**: User wants the current price and market data for a specific Alpha token.

**Prompt Examples**:
- "What's the price of trump?"
- "How much is ELON right now?"
- "Check the current price of memeboxtrump."

**Expected Behavior**:
1. Call `cex_alpha_list_alpha_tickers` with `currency={token_symbol}`.
2. Extract latest price (`last`), 24h change (`change`), volume, and market cap.
3. Present a detailed market data card for the specific token.
4. If the token is not found, suggest checking the token symbol via `cex_alpha_list_alpha_currencies`.
