---
name: gate-exchange-alpha
description: "Gate Alpha token market skill. Use when the user specifically asks to browse, trade, or check Alpha market tokens. Triggers on 'alpha tokens', 'alpha market', 'buy alpha', 'alpha history'."
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "💱"
    os:
      - darwin
      - linux
    primaryEnv: GATE_API_KEY
    requires:
      bins:
        - gate-cli
      env:
        - GATE_API_KEY
        - GATE_API_SECRET

    install:
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux x64)"
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux arm64)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Intel)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Apple Silicon)"
---

### Resolving `gate-cli` (binary path)

Resolve **`gate-cli`** in order: **(1)** **`command -v gate-cli`** and **`gate-cli --version`** succeeds; **(2)** **`${HOME}/.local/bin/gate-cli`** if executable; **(3)** **`${HOME}/.openclaw/skills/bin/gate-cli`** if executable. Canonical rules: [`exchange-runtime-rules.md`](../exchange-runtime-rules.md) §4 (or [`gate-runtime-rules.md`](../gate-runtime-rules.md) §4).


# Gate Alpha Assistant

This skill is the single entry for Gate Alpha operations. It supports **seven modules**: Token Discovery, Market Viewing, Trading (Buy), Trading (Sell), Account & Holdings, Account Book, and Order Management. User intent is routed to the matching workflow.

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

## Skill Dependencies


### gate-cli commands used

**Query Operations (Read-only)**

- `gate-cli cex alpha order get`
- `gate-cli cex alpha account book`
- `gate-cli cex alpha account balances`
- `gate-cli cex alpha market currencies`
- `gate-cli cex alpha order list`
- `gate-cli cex alpha market tickers`
- `gate-cli cex alpha market tokens`
- `gate-cli cex alpha order quote`

**Execution Operations (Write)**

- `gate-cli cex alpha order place`

### Authentication
- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- **Permissions:** Alpha:Write
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- **Required:** `gate-cli` (run `sh ./setup.sh` from this skill directory if missing; optional `GATE_CLI_SETUP_MODE=release`).
- Add `$HOME/.openclaw/skills/bin` to **`PATH`** if you invoke `gate-cli` by name (or the directory where [`setup.sh`](./setup.sh) installs it).
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`** — that is equivalent valid config for `gate-cli`. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Do not proceed with authenticated calls until the CLI behaves as expected (e.g. **`gate-cli --version`** or a read-only **`gate-cli cex ...`** command from this skill); confirm credentials resolve before mutating operations.

## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute module routing in this skill.

- `SKILL.md` keeps module dispatch and business boundaries.
- `references/gate-cli.md` is the authoritative `gate-cli` execution contract for quote->confirm->place order flow and post-order verification.

## Module Overview

| Module | Description | Trigger Keywords |
|--------|-------------|------------------|
| **Token Discovery** | Browse tradable currencies, filter tokens by chain/platform/address, check token details | `alpha tokens`, `what coins`, `which chain`, `token address`, `token details` |
| **Market Viewing** | Check all or specific Alpha token tickers, prices, 24h changes | `alpha price`, `market`, `ticker`, `how much is`, `what price` |
| **Trading (Buy)** | Buy Alpha tokens with USDT, support default or custom slippage, optional order tracking | `buy`, `买`, `购买`, `入手`, `帮我买` |
| **Trading (Sell)** | Sell Alpha tokens (full or partial), optional order tracking | `sell`, `卖`, `卖出`, `清仓`, `卖掉` |
| **Account & Holdings** | View Alpha account balances and calculate portfolio market value | `my holdings`, `my balance`, `portfolio value`, `how much do I have` |
| **Account Book** | View Alpha account transaction history by time range | `transaction history`, `流水`, `资产变动`, `account book`, `变动记录` |
| **Order Management** | Check order status, view historical buy/sell orders, search orders by time | `order status`, `订单`, `买单`, `卖单`, `order history` |

## Routing Rules

| Intent | Example Phrases | Route To |
|--------|-----------------|----------|
| **Token discovery** | "What coins can I trade on Alpha?", "Show me Solana tokens", "Look up this address" | Read `references/token-discovery.md` |
| **Market viewing** | "What's the price of trump?", "How's the Alpha market?" | Read `references/market-viewing.md` |
| **Trading (buy)** | "帮我买 5u ELON", "Buy 100u trump with 10% slippage" | Read `references/trading-buy.md` |
| **Trading (sell)** | "把 ELON 全部卖掉", "卖掉一半的 trump" | Read `references/trading-sell.md` |
| **Account & holdings** | "What coins do I hold?", "How much is my Alpha portfolio worth?" | Read `references/account-holdings.md` |
| **Account book** | "最近一周的资产变动记录", "看看昨天的资产变动" | Read `references/account-book.md` |
| **Order management** | "我刚才那笔买单成功了吗？", "看看我买 ELON 的订单" | Read `references/order-management.md` |
| **Unclear** | "Tell me about Alpha", "Help with Alpha" | **Clarify**: ask which module the user needs |

## gate-cli command index

| # | Tool | Auth | Purpose |
|---|------|------|---------|
| 1 | `gate-cli cex alpha market currencies` | No | List all tradable Alpha currencies with chain, address, precision, status |
| 2 | `gate-cli cex alpha market tokens` | No | Filter tokens by chain, launch platform, or contract address |
| 3 | `gate-cli cex alpha market tickers` | No | Get latest price, 24h change, volume, market cap for Alpha tokens |
| 4 | `gate-cli cex alpha account balances` | Yes | Query Alpha account balances (available + locked per currency) |
| 5 | `gate-cli cex alpha order quote` | Yes | Get a price quote for a buy/sell order (returns quote_id, valid 1 min) |
| 6 | `gate-cli cex alpha order place` | Yes | Place a buy/sell order using a quote_id |
| 7 | `gate-cli cex alpha order get` | Yes | Get details of a single order by order_id |
| 8 | `gate-cli cex alpha order list` | Yes | List orders with filters (currency, side, status, time range) |
| 9 | `gate-cli cex alpha account book` | Yes | Query account transaction history by time range |

## Domain Knowledge

### Alpha Platform Overview

- Gate Alpha is a platform for early-stage token trading, supporting tokens across multiple blockchains.
- Tokens are identified by `currency` symbol (e.g., `memeboxtrump`) rather than standard ticker symbols.
- Trading status values: `1` = actively trading, `2` = suspended, `3` = delisted.

### Supported Chains

solana, eth, bsc, base, world, sui, arbitrum, avalanche, polygon, linea, optimism, zksync, gatelayer

**Note**: Chain names may be returned in different cases depending on the endpoint (e.g., `SOLANA` vs `solana`). Normalize to lowercase when comparing.

### Supported Launch Platforms

meteora_dbc, fourmeme, moonshot, pump, raydium_launchlab, letsbonk, gatefun, virtuals

### Trading Mechanics

- **Buy amount**: USDT quantity (e.g., `amount="5"` means spend 5 USDT).
- **Sell amount**: Token quantity (e.g., `amount="1000"` means sell 1000 tokens).
- **Quote validity**: `quote_id` from `gate-cli cex alpha order quote` expires after **1 minute**. Re-quote if expired.
- **Gas modes**: Input `"speed"` (default) or `"custom"` (with slippage). API returns `gasMode` as `"1"` (speed) or `"2"` (custom).
- **Order statuses**: `1` = Processing, `2` = Success, `3` = Failed, `4` = Cancelled, `5` = Transferring, `6` = Cancelling transfer. Terminal statuses: 2, 3, 4.

### API Field Naming Conventions

All API endpoints use **snake_case** naming. Key fields by endpoint:
- `/alpha/currencies`: `currency`, `name`, `chain`, `address`, `amount_precision`, `precision`, `status`
- `/alpha/tickers`: `currency`, `last`, `change`, `volume`, `market_cap`
- `/alpha/accounts`: `currency`, `available`, `locked`, `token_address`, `chain`
- `/alpha/account_book`: `id`, `time`, `currency`, `change`, `balance`
- `/alpha/orders` (GET): `order_id`, `tx_hash`, `side`, `usdt_amount`, `currency`, `currency_amount`, `status`, `gas_mode`, `chain`, `gas_fee`, `transaction_fee`, `create_time`, `failed_reason`
- Empty query results may return `[{}, {}]` (array with empty objects) instead of `[]`. Check for valid fields before processing.

### Key Constraints

- All market data endpoints (`currencies`, `tickers`, `tokens`) are public and do not require authentication.
- Account, trading, and order endpoints require API Key authentication.
- Pagination: use `page` and `limit` parameters for large result sets.
- Rate limits: quote 10r/s, place order 5r/s, other endpoints 200r/10s.

## Execution

### 1. Intent Classification

Classify the user request into one of seven modules: Token Discovery, Market Viewing, Trading (Buy), Trading (Sell), Account & Holdings, Account Book, or Order Management.

### 2. Route and Load

Load the corresponding reference document and follow its workflow.

### 3. Return Result

Return the result using the report template defined in each sub-module.

## Error Handling

| Error Type | Typical Cause | Handling Strategy |
|------------|---------------|-------------------|
| Currency not found | Invalid or misspelled currency symbol | Suggest searching via `gate-cli cex alpha market currencies` or `gate-cli cex alpha market tokens` |
| Token suspended | Trading status is 2 (suspended) | Inform user that the token is currently suspended from trading |
| Token delisted | Trading status is 3 (delisted) | Inform user that the token has been delisted |
| Empty result | No tokens match the filter criteria | Clarify filter parameters (chain, platform, address) and suggest alternatives |
| Authentication required | Calling authenticated endpoint without credentials | Inform user that API Key authentication is needed; guide to setup |
| Pagination overflow | Requested page beyond available data | Return last available page and inform user of total count |
| Quote expired | quote_id used after 1-minute validity window | Re-call `gate-cli cex alpha order quote` to obtain a fresh quote_id |
| Insufficient balance | Sell amount exceeds available balance | Inform user of actual available balance and suggest adjusting the amount |
| Order failed | On-chain transaction failed | Report the `failed_reason` from the order detail and suggest retrying |
| Order timeout | Polling exceeded 60 seconds without terminal status | Inform user the order is still processing; provide order_id for manual follow-up |
| Rate limit exceeded | Too many requests in short period | Wait briefly and retry; inform user if persistent |

## Safety Rules

- **Order confirmation**: NEVER place a buy or sell order without showing the quote details and receiving explicit user confirmation.
- **Token validation**: Always verify `status=1` before initiating a trade. Abort if suspended or delisted.
- **Balance verification**: Before selling, always confirm `available >= sell_amount`. Report actual balance if insufficient.
- **Quote freshness**: Always check quote_id validity (1-minute window). Re-quote if the user delays confirmation.
- Never fabricate token data. If a query returns empty results, report it honestly.
- When displaying token addresses, show the full address to avoid confusion between similarly named tokens.
- Always verify trading status before suggesting a token is tradable.
