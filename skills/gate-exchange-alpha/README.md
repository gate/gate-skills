# Gate Exchange Alpha

## Overview

A token discovery, market viewing, and account management skill for Gate Alpha platform, supporting early-stage token browsing across multiple blockchains.

### Core Capabilities

| Capability | Description |
|------------|-------------|
| Token Discovery | Browse all tradable currencies, filter by chain/platform/address, view token details |
| Market Viewing | Check all or specific Alpha token prices, 24h changes, and trading volumes |
| Account & Holdings | View Alpha account balances and calculate portfolio market value |

## Architecture

```
gate-exchange-alpha/
├── SKILL.md              # Routing entry + MCP tools + domain knowledge
├── README.md             # Human-readable documentation
├── CHANGELOG.md          # Version history
└── references/
    ├── token-discovery.md    # Cases 1-5: Token browsing and filtering
    ├── market-viewing.md     # Cases 6-7: Market tickers and prices
    └── account-holdings.md   # Cases 14-15: Account balances and portfolio valuation
```

## MCP Tools Used

| Tool | Auth Required | Purpose |
|------|--------------|---------|
| `cex_alpha_list_alpha_currencies` | No | List tradable currencies with details |
| `cex_alpha_list_alpha_tokens` | No | Filter tokens by chain, platform, or address |
| `cex_alpha_list_alpha_tickers` | No | Get market tickers and prices |
| `cex_alpha_list_alpha_accounts` | Yes | Query account balances |

## Usage Examples

```
"What coins can I trade on Alpha?"
"Show me Solana tokens."
"What's the price of trump?"
"What coins do I hold on Alpha?"
"How much is my Alpha portfolio worth?"
```

## Trigger Phrases

- alpha tokens / alpha coins / what's on alpha
- alpha price / alpha market / alpha ticker
- alpha holdings / alpha balance / alpha portfolio
- token on solana / pump tokens / token address lookup
