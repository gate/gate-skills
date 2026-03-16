---
name: gate-exchange-alpha
version: "2026.3.13-1"
updated: "2026-03-13"
description: "Gate Alpha token discovery, market viewing, and account operations skill. Use this skill whenever the user asks to browse Alpha tokens, check Alpha market tickers, view Alpha holdings, or calculate Alpha portfolio value. Trigger phrases include 'alpha tokens', 'alpha market', 'alpha holdings', 'alpha portfolio', 'what coins on alpha', 'alpha balance', or any request involving Gate Alpha token browsing or account queries."
---

# Gate Alpha Assistant

This skill is the single entry for Gate Alpha operations. Phase 1 supports **three modules**: Token Discovery, Market Viewing, and Account & Holdings. User intent is routed to the matching workflow.

## General Rules

Read and follow the shared runtime rules before proceeding:

→ [exchange-runtime-rules.md](../exchange-runtime-rules.md)

---

## Module Overview

| Module | Description | Trigger Keywords |
|--------|-------------|------------------|
| **Token Discovery** | Browse tradable currencies, filter tokens by chain/platform/address, check token details | `alpha tokens`, `what coins`, `which chain`, `token address`, `token details` |
| **Market Viewing** | Check all or specific Alpha token tickers, prices, 24h changes | `alpha price`, `market`, `ticker`, `how much is`, `what price` |
| **Account & Holdings** | View Alpha account balances and calculate portfolio market value | `my holdings`, `my balance`, `portfolio value`, `how much do I have` |

## Routing Rules

| Intent | Example Phrases | Route To |
|--------|-----------------|----------|
| **Token discovery** | "What coins can I trade on Alpha?", "Show me Solana tokens", "Look up this address" | Read `references/token-discovery.md` |
| **Market viewing** | "What's the price of trump?", "How's the Alpha market?" | Read `references/market-viewing.md` |
| **Account & holdings** | "What coins do I hold?", "How much is my Alpha portfolio worth?" | Read `references/account-holdings.md` |
| **Unclear** | "Tell me about Alpha", "Help with Alpha" | **Clarify**: ask whether user wants to browse tokens, check prices, or view holdings |

## MCP Tools

| # | Tool | Auth | Purpose |
|---|------|------|---------|
| 1 | `cex_alpha_list_alpha_currencies` | No | List all tradable Alpha currencies with chain, address, precision, status |
| 2 | `cex_alpha_list_alpha_tokens` | No | Filter tokens by chain, launch platform, or contract address |
| 3 | `cex_alpha_list_alpha_tickers` | No | Get latest price, 24h change, volume, market cap for Alpha tokens |
| 4 | `cex_alpha_list_alpha_accounts` | Yes | Query Alpha account balances (available + locked per currency) |

## Domain Knowledge

### Alpha Platform Overview

- Gate Alpha is a platform for early-stage token trading, supporting tokens across multiple blockchains.
- Tokens are identified by `currency` symbol (e.g., `memeboxtrump`) rather than standard ticker symbols.
- Trading status values: `1` = actively trading, `2` = suspended, `3` = delisted.

### Supported Chains

solana, eth, bsc, base, world, sui, arbitrum, avalanche, polygon, linea, optimism, zksync, gatelayer

### Supported Launch Platforms

meteora_dbc, fourmeme, moonshot, pump, raydium_launchlab, letsbonk, gatefun, virtuals

### Key Constraints

- All market data endpoints (`currencies`, `tickers`, `tokens`) are public and do not require authentication.
- Account endpoints (`accounts`) require API Key authentication.
- Pagination: use `page` and `limit` parameters for large result sets.

## Execution

### 1. Intent Classification

Classify the user request into one of three modules: Token Discovery, Market Viewing, or Account & Holdings.

### 2. Route and Load

Load the corresponding reference document and follow its workflow.

### 3. Return Result

Return the result using the report template defined in each sub-module.

## Error Handling

| Error Type | Typical Cause | Handling Strategy |
|------------|---------------|-------------------|
| Currency not found | Invalid or misspelled currency symbol | Suggest searching via `cex_alpha_list_alpha_currencies` or `cex_alpha_list_alpha_tokens` |
| Token suspended | Trading status is 2 (suspended) | Inform user that the token is currently suspended from trading |
| Token delisted | Trading status is 3 (delisted) | Inform user that the token has been delisted |
| Empty result | No tokens match the filter criteria | Clarify filter parameters (chain, platform, address) and suggest alternatives |
| Authentication required | Calling account endpoint without credentials | Inform user that API Key authentication is needed for account queries |
| Pagination overflow | Requested page beyond available data | Return last available page and inform user of total count |

## Safety Rules

- This skill is read-only in Phase 1. No trading operations are executed.
- Never fabricate token data. If a query returns empty results, report it honestly.
- When displaying token addresses, show the full address to avoid confusion between similarly named tokens.
- Always verify trading status before suggesting a token is tradable.
