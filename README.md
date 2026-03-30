# Gate Skills

[English](README.md) | [中文](README_zh.md)

Gate Skills is an open skills marketplace that empowers AI agents with native access to Gate cryptocurrency ecosystem. From market analysis and derivatives monitoring to one-click MCP setup — all through natural language.

Built by Gate. Built for the crypto community.

### One-Click Installation

Get started in seconds with our installer skills:

- **Cursor Users**: Use `gate-mcp-cursor-installer` — installs all Gate MCP servers + skills with a single command
- **OpenClaw Users**: Use `gate-mcp-openclaw-installer` — complete Gate MCP setup with interactive selection
- **Claude Code (Claude CLI) Users**: Use `gate-mcp-claude-installer` — one-click install all Gate MCP + Gate Skills
- **Codex Users**: Use `gate-mcp-codex-installer` — one-click install all Gate MCP + Gate Skills

**Quick Start**: Just say to your AI assistant:

> **"Help me auto install Gate Skills and MCPs: https://github.com/gate/gate-skills"**

Or run the install script directly from the repository.

### Framework Compatibility

These skills are designed to work with any AI agent framework. Whether you're using Cursor, OpenClaw, or your own stack, your agents can plug into Gate crypto intelligence with minimal configuration.

---

## Skills Overview

| Skill | Description | Version | Status |
|-------|-------------|---------|--------|
| [gate-exchange-tradfi](#-gate-exchange-tradfi) | Gate TradFi (traditional finance) read-only queries: orders, positions, market data, assets and MT5 account info | `2026.3.13-6` | ✅ Active |
| [gate-exchange-simpleearn](#-gate-exchange-simpleearn) | Gate Simple Earn (Uni) flexible earn queries: positions, interest, top APY rate lookup (subscribe/redeem not supported) | `2026.3.12-2` | ✅ Active |
| [gate-exchange-affiliate](#-gate-exchange-affiliate) | Gate Exchange affiliate/partner program: commission, volume, net fees, customer count, trading users query and application guidance | `2026.3.13` | ✅ Active |
| [gate-exchange-unified](#-gate-exchange-unified) | Gate unified account: equity, borrow/repay, loan & interest, mode switch, leverage & collateral | `2026.3.13-4` | ✅ Active |
| [gate-exchange-assets](#-gate-exchange-assets) | Gate Exchange asset queries: total balance, spot holdings, account valuation, account book (read-only) | `2026.3.12-3` | ✅ Active |
| [gate-info-coinanalysis](#-gate-info-coinanalysis) | Single-coin comprehensive analysis: fundamentals, technicals, news, sentiment | `2026.3.25-1` | ✅ Active |
| [gate-exchange-dual](#-gate-exchange-dual) | Gate dual investment: product discovery, settlement simulation, position summary, balance (read-only) | `2026.3.12-1` | ✅ Active |
| [gate-exchange-staking](#-gate-exchange-staking) | Gate staking (earn): positions, rewards, products, order history (read-only) | `2026.3.12-1` | ✅ Active |
| [gate-exchange-subaccount](#-gate-exchange-subaccount) | Gate sub-account management: query status, list, create, lock/unlock (write ops need confirmation) | `2026.3.12-1` | ✅ Active |
| [gate-info-addresstracker](#-gate-info-addresstracker) | On-chain address tracking: profile, transaction history, fund flow analysis | `2026.3.25-1` | ✅ Active |
| [gate-info-coincompare](#-gate-info-coincompare) | Multi-coin comparison with multi-dimensional analysis table | `2026.3.25-1` | ✅ Active |
| [gate-info-defianalysis](#-gate-info-defianalysis) | DeFi ecosystem: TVL rankings, protocol metrics, yield/APY, stablecoins, bridges, exchange reserves, liquidation heatmaps (Gate-Info; read-only) | `2026.3.30-6` | ✅ Active |
| [gate-info-macroimpact](#-gate-info-macroimpact) | Macro ↔ crypto: economic calendar, indicators, related news, and market snapshot linkage (Gate-Info + Gate-News; read-only) | `2026.3.30-6` | ✅ Active |
| [gate-info-marketoverview](#-gate-info-marketoverview) | Crypto market overview: sector rankings, DeFi, events, macro summary | `2026.3.25-1` | ✅ Active |
| [gate-info-riskcheck](#-gate-info-riskcheck) | Token & contract risk assessment: honeypot, rug pull, tax, holder concentration | `2026.3.25-1` | ✅ Active |
| [gate-info-tokenonchain](#-gate-info-tokenonchain) | Token on-chain: holder distribution, activity, large transfers (Smart Money not in this version; Gate-Info; read-only) | `2026.3.30-5` | ✅ Active |
| [gate-info-trendanalysis](#-gate-info-trendanalysis) | Trend & technical analysis: K-line, RSI, MACD, multi-timeframe signals | `2026.3.25-1` | ✅ Active |
| [gate-news-briefing](#-gate-news-briefing) | Crypto news briefing: major events, trending news, social sentiment | `2026.3.25-1` | ✅ Active |
| [gate-news-communityscan](#-gate-news-communityscan) | Community / X sentiment: discussion scan + quantitative social sentiment (UGC beyond X when available; Gate-News; read-only) | `2026.3.30-5` | ✅ Active |
| [gate-news-eventexplain](#-gate-news-eventexplain) | Event attribution & explanation: why did X crash/pump, impact chain analysis | `2026.3.25-1` | ✅ Active |
| [gate-news-listing](#-gate-news-listing) | Exchange listing/delisting tracker with fundamental supplements | `2026.3.25-1` | ✅ Active |
| [gate-dex-market](#-gate-dex-market) | Gate DEX market data via OpenAPI: token info, K-line, rankings, security audit | `2026.3.12-1` | ✅ Active |
| [gate-dex-trade](#-gate-dex-trade) | Gate DEX trading: MCP + OpenAPI dual mode, smart routing for Swap execution | `2026.3.12-1` | ✅ Active |
| [gate-mcp-claude-installer](#-gate-mcp-claude-installer) | One-click installer for Gate MCP and Skills for Claude Code (Claude CLI) | `2026.3.11-1` | ✅ Active |
| [gate-mcp-codex-installer](#-gate-mcp-codex-installer) | One-click installer for Gate MCP and Skills for Codex | `2026.3.11-1` | ✅ Active |
| [gate-exchange-marketanalysis](#-gate-exchange-marketanalysis) | Market tape analysis: liquidity, momentum, liquidation, funding arbitrage, basis, manipulation risk, order book explainer, slippage simulation, breakout, and weekend vs weekday | `2026.3.11-1` | ✅ Active |
| [gate-mcp-cursor-installer](#-gate-mcp-cursor-installer) | One-click installer for Gate MCP and Skills for Cursor | `2026.3.10-1` | ✅ Active |
| [gate-mcp-openclaw-installer](#-gate-mcp-openclaw-installer) | Complete Gate MCP server installer for OpenClaw | `2026.3.10-1` | ✅ Active |
| [gate-exchange-spot](#-gate-exchange-spot) | Gate spot trading: buy/sell, order management, account queries, and asset swaps | `2026.3.10-1` | ✅ Active |
| [gate-dex-wallet](#-gate-dex-wallet) | Gate DEX comprehensive wallet: authentication, assets, transfers, DApp interactions | `2026.3.10-1` | ✅ Active |
| [gate-exchange-trading-copilot](#-gate-exchange-trading-copilot) | End-to-end trading copilot: market judgment, risk control, order drafting, execution, and post-trade management | `2026.3.14-3` | ✅ Active |
| [gate-exchange-alpha](#-gate-exchange-alpha) | Gate Alpha token discovery, market viewing, and account holdings query | `2026.3.13-1` | ✅ Active |
| [gate-exchange-coupon](#-gate-exchange-coupon) | Gate coupon/voucher management: list, detail, usage rules, and acquisition source query | `2026.3.13-1` | ✅ Active |
| [gate-exchange-crossex](#-gate-exchange-crossex) | Gate CrossEx cross-exchange operations: orders, positions, and history across Gate, Binance, OKX | `2026.3.12-1` | ✅ Active |
| [gate-exchange-transfer](#-gate-exchange-transfer) | Gate internal transfer: move funds between spot, margin, perpetual, delivery, and options accounts | `2026.3.16-2` | ✅ Active |
| [gate-exchange-flashswap](#-gate-exchange-flashswap) | Gate Flash Swap query: currency pairs, swap limits, order history, and order details | `2026.3.11-5` | ✅ Active |
| [gate-exchange-vipfee](#-gate-exchange-vipfee) | Gate VIP tier and trading fee rate query: spot fees, futures fees, VIP level | `2026.3.11-2` | ✅ Active |
| [gate-info-liveroomlocation](#-gate-info-liveroomlocation) | Gate live stream & replay listing: filter by tag, coin, sort order, and count | `2026.3.13-1` | ✅ Active |
| [gate-exchange-futures](#-gate-exchange-futures) | USDT perpetual futures trading: open/close position, cancel/amend order | `2026.3.5-1` | ✅ Active |
| [gate-exchange-referral](#-gate-exchange-referral) | Invite-friends campaigns and rules: Earn Together, Help & Get Coupons, Super Commission; read-only guidance | `2026.3.26-1` | ✅ Active |
| [gate-exchange-assets-manager](#-gate-exchange-assets-manager) | L2 composite: multi-account assets, margin/liquidation risk, earn/staking/affiliate, unified borrow & collateral | `2026.3.25-1` | ✅ Active |
| [gate-info-research](#-gate-info-research) | L2 Market Research Copilot: Gate-Info + Gate-News read-only briefs, comparisons, and risk checks | `2026.3.23-1` | ✅ Active |
| [gate-exchange-welfare](#-gate-exchange-welfare) | Welfare center new-user tasks and rewards (MCP-backed; no fabricated numbers) | `2026.3.23-1` | ✅ Active |
| [gate-exchange-launchpool](#-gate-exchange-launchpool) | LaunchPool: browse projects, stake/redeem, pledge records, airdrop reward history | `2026.3.23-1` | ✅ Active |
| [gate-exchange-kyc](#-gate-exchange-kyc) | KYC portal guidance (complete verification on the official site only) | `2026.3.23-1` | ✅ Active |
| [gate-exchange-collateralloan](#-gate-exchange-collateralloan) | Multi-collateral loan: query, repay, add collateral, redeem collateral | `2026.3.23-1` | ✅ Active |
| [gate-exchange-activitycenter](#-gate-exchange-activitycenter) | Platform activity center: campaigns, recommendations, and my activities | `2026.3.23-1` | ✅ Active |

---

## 🤝 gate-exchange-affiliate

> **Path**: `skills/gate-exchange-affiliate/`

Gate Exchange affiliate/partner program data query and management: commission tracking, team performance analysis, and application guidance. Supports up to 30 days per request and up to 180 days total (agent splits requests when >30 days). Requires partner-privilege authentication.

**Example Prompts**:
- `Show my affiliate data`
- `Commission this week`
- `Partner earnings`
- `Team performance`
- `Customer trading volume`
- `Rebate income`
- `Apply for affiliate program`

---

## 📈 gate-exchange-marketanalysis

> **Path**: `skills/gate-exchange-marketanalysis/`

Read-only market tape analysis across ten scenarios: liquidity, momentum, liquidation, funding arbitrage, basis, manipulation risk, order book explainer, slippage simulation, K-line breakout/support–resistance, and weekend vs weekday volume comparison.

**Example Prompts**:
- `Check BTC liquidity and slippage`
- `What is the momentum of ETH?`
- `Simulate a $10K market buy on ETH`
- `Is there manipulation risk on DOGE?`
- `Compare BTC weekend vs weekday volume`

---

## 📊 gate-exchange-futures

> **Path**: `skills/gate-exchange-futures/`

USDT perpetual futures trading on Gate Exchange. Supports four operations: open position, close position, cancel order, and amend order — with pre-flight checks, margin/leverage handling, and confirmation before execution.

**Example Prompts**:
- `Long BTC 1 contract with 10x leverage`
- `Close all ETH positions`
- `Cancel my BTC buy order`
- `Change order price to 60000`

---

## 🤖 gate-exchange-trading-copilot

> **Path**: `skills/gate-exchange-trading-copilot/`

End-to-end cryptocurrency trading copilot for Gate Exchange. Completes the full trading loop in one skill: market judgment → risk control → order drafting → explicit confirmation → execution → post-trade management. Works with both spot and futures.

**Example Prompts**:
- `Analyze BTC before placing an order`
- `Is it safe to buy ETH now? If yes, help me buy`
- `Check risk and then long BTC futures 10x`
- `Analyze before buying SOL`

---

## 🔮 gate-exchange-alpha

> **Path**: `skills/gate-exchange-alpha/`

Gate Alpha token discovery, market viewing, and account operations. Browse tradable Alpha tokens, check Alpha market tickers/prices, and view Alpha holdings and portfolio value.

**Example Prompts**:
- `What coins are on Alpha?`
- `Alpha token price for SOL`
- `Show my Alpha holdings`
- `Alpha portfolio value`
- `Which Alpha tokens are on Solana?`

---

## 🎟️ gate-exchange-coupon

> **Path**: `skills/gate-exchange-coupon/`

Gate coupon/voucher management: list available coupons, search by type, view expired/used history, check coupon details, read usage rules, and trace acquisition source.

**Example Prompts**:
- `My coupons`
- `Do I have any coupons?`
- `Coupon details`
- `When does my coupon expire?`
- `How did I get this coupon?`

---

## 🌐 gate-exchange-crossex

> **Path**: `skills/gate-exchange-crossex/`

Gate CrossEx cross-exchange operations: order queries, position queries, and history queries across Gate, Binance, and OKX. Supports order management, position monitoring, and trade/interest history retrieval.

**Example Prompts**:
- `Query all open CrossEx orders`
- `Check my CrossEx positions`
- `CrossEx order history`
- `CrossEx trade history`

---

## 💸 gate-exchange-transfer

> **Path**: `skills/gate-exchange-transfer/`

Gate same-UID internal transfer between trading accounts: spot, isolated margin, perpetual (USDT/BTC-margined), delivery, and options. Execution requires explicit user confirmation and source balance pre-check.

**Example Prompts**:
- `Transfer 100 USDT from spot to futures`
- `Move funds from spot to perpetual`
- `Transfer BTC to delivery account`
- `Move USDT from margin to spot`

---

## ⚡ gate-exchange-flashswap

> **Path**: `skills/gate-exchange-flashswap/`

Gate Flash Swap query: browse supported currency pairs, validate swap amount limits, view flash swap order history, and look up specific order details. Read-only; no swap execution.

**Example Prompts**:
- `What pairs support flash swap?`
- `Flash swap limits for BTC/USDT`
- `Show my flash swap order history`
- `Look up flash swap order #12345`

---

## 👑 gate-exchange-vipfee

> **Path**: `skills/gate-exchange-vipfee/`

Query Gate VIP tier and trading fee rates, including spot and futures fee information.

**Example Prompts**:
- `What is my VIP level?`
- `Show me the spot and futures trading fees`
- `Check my VIP level and trading fees`
- `What's my fee rate?`

---

## 🎬 gate-info-liveroomlocation

> **Path**: `skills/gate-info-liveroomlocation/`

Gate live stream and replay listing. Filter by business type (Market Analysis, Hot Topics, Blockchain, Others), coin, sort order (hottest/newest), and count.

**Example Prompts**:
- `Show me the hottest live streams`
- `Find 5 SOL-related live rooms`
- `Latest market analysis replays`
- `Any live streams about BTC?`

---

## 💱 gate-exchange-spot

> **Path**: `skills/gate-exchange-spot/`

Gate spot trading covering buy/sell (market & limit), smart condition-based orders, order management (amend/cancel), account queries, fill verification, and coin-to-coin swaps. All order placements require explicit user confirmation.

**Example Prompts**:
- `Buy 100 USDT worth of BTC`
- `Sell ETH when price hits 3500`
- `Cancel my unfilled BTC order and check balance`
- `Swap USDT to SOL`

---

## 📦 gate-exchange-assets

> **Path**: `skills/gate-exchange-assets/`

Read-only asset and balance queries for Gate Exchange: total account balance, spot holdings, account valuation in USDT, and account book. No trading or transfers.

**Example Prompts**:
- `How much is my account worth?`
- `Check my USDT balance`
- `Show my total assets`
- `What's my BTC balance?`
- `Show recent BTC account book and current balance`

---

## 📋 gate-exchange-dual

> **Path**: `skills/gate-exchange-dual/`

Dual investment on Gate Exchange: browse plans (APY, target price), simulate settlement outcomes, view positions and balance. Read-only; no order placement.

**Example Prompts**:
- `What BTC dual investment plans are available?`
- `Sell-high target 62000 — what if price goes to 65000?`
- `Dual position summary`
- `How much is locked in dual?`

---

## 🪙 gate-exchange-staking

> **Path**: `skills/gate-exchange-staking/`

Staking (earn) query on Gate: positions, rewards, product discovery, and order history. Read-only; no stake/redeem execution.

**Example Prompts**:
- `Show my staking positions`
- `What are my staking rewards?`
- `Find BTC staking products`
- `Show staking history`

---

## 💸 gate-exchange-simpleearn

> **Path**: `skills/gate-exchange-simpleearn/`

Gate Simple Earn (Uni) flexible earn read operations: query single/all positions, single-currency interest, and top APY rate data. Subscribe and redeem APIs are currently disabled in this skill.

**Example Prompts**:
- `My USDT Simple Earn position`
- `Show all Simple Earn positions`
- `How much USDT interest have I earned?`
- `Which Simple Earn currency has the top APY?`
- `Subscribe 100 USDT to Simple Earn` (will reply not supported)

---

## 🏦 gate-exchange-tradfi

> **Path**: `skills/gate-exchange-tradfi/`

Gate TradFi (traditional finance) read-only query skill for orders, positions, market data, assets, and MT5 account information. This skill does not place/cancel orders or transfer funds.

**Example Prompts**:
- `My TradFi open orders`
- `Show my position history`
- `TradFi category list`
- `Ticker for EURUSD`
- `Show my MT5 account info`

---

## 🔗 gate-exchange-unified

> **Path**: `skills/gate-exchange-unified/`

Gate unified account: account overview & mode, borrow/repay, loan & interest records, transferable limits, leverage and collateral settings. Mutation actions require explicit user confirmation.

**Example Prompts**:
- `Query my unified account total equity and current mode`
- `How much USDT can I borrow?`
- `Borrow 200 USDT — check max borrowable first`
- `Repay all my BTC loan`
- `Set my ETH leverage to 5x`

---

## 👥 gate-exchange-subaccount

> **Path**: `skills/gate-exchange-subaccount/`

Sub-account management on Gate Exchange: query status by UID, list all sub-accounts, create sub-account, lock/unlock. Write operations require explicit user confirmation.

**Example Prompts**:
- `Show me all my sub-accounts`
- `What is the status of sub-account UID 123456?`
- `Create a new sub-account`
- `Lock sub-account UID 123456`

---

## 📊 gate-dex-market

> **Path**: `skills/gate-dex-market/`

Gate DEX market data skill using OpenAPI mode with AK/SK authentication. Provides read-only queries for token info, K-line data, rankings, and security audits.

**Example Prompts**:
- `Get BTC token info`
- `Show me ETH K-line data`
- `What are the top trending tokens?`
- `Check security audit for this token`

---

## 🔄 gate-dex-trade

> **Path**: `skills/gate-dex-trade/`

Gate DEX trading comprehensive skill with MCP + OpenAPI dual mode support. Smart routing automatically selects the optimal trading method based on environment. Supports Swap execution across EVM and Solana.

**Example Prompts**:
- `Swap 100 USDT for ETH`
- `Exchange BNB for PEPE`
- `Get a quote for swapping SOL to USDC`
- `Buy some tokens using OpenAPI mode`

---

## 💼 gate-dex-wallet

> **Path**: `skills/gate-dex-wallet/`

Gate DEX comprehensive wallet skill. Unified entry point for authentication, asset queries, transfer execution, and DApp interactions. Routes to specific sub-modules based on user intent.

**Example Prompts**:
- `Log in to my wallet`
- `Check my wallet balance`
- `Transfer 0.1 ETH to 0x...`
- `Connect my wallet to Uniswap`
- `Sign this message`

---

## 🔍 gate-info-addresstracker

> **Path**: `skills/gate-info-addresstracker/`

On-chain address tracking and analysis. Fetches address profile, transaction history, and fund flow tracing. Supports basic queries and deep tracking modes across multiple chains.

**Example Prompts**:
- `Track this address 0x...`
- `Who owns this address?`
- `Show fund flow for bc1...`
- `Check address activity`

---

## 📊 gate-info-coinanalysis

> **Path**: `skills/gate-info-coinanalysis/`

Single-coin comprehensive analysis. Fetches fundamentals, market data, technicals, news, and social sentiment in parallel, then generates a structured analysis report.

**Example Prompts**:
- `Analyze ETH`
- `How is SOL doing?`
- `Is BTC worth buying right now?`
- `Give me a full analysis of DOGE`

---

## ⚖️ gate-info-coincompare

> **Path**: `skills/gate-info-coincompare/`

Multi-coin comparison (2–5 coins). Fetches market snapshots and fundamentals for each coin, then generates a multi-dimensional comparison table and summary.

**Example Prompts**:
- `Compare BTC vs ETH`
- `Which is better: SOL or AVAX?`
- `Compare BTC, ETH, SOL, and BNB`
- `What's the difference between DOGE and SHIB?`

---

## 🌐 gate-info-marketoverview

> **Path**: `skills/gate-info-marketoverview/`

Crypto market overview. Fetches global market data, sector rankings, DeFi overview, upcoming events, and macro summary in parallel, then generates a market briefing report.

**Example Prompts**:
- `How is the market today?`
- `Give me a market overview`
- `What's happening in crypto?`
- `Show me the overall market status`

---

## 🛡️ gate-info-riskcheck

> **Path**: `skills/gate-info-riskcheck/`

Token and contract risk assessment. Runs 30+ risk checks including honeypot detection, tax analysis, holder concentration, and naming risks. Generates a structured risk report.

**Example Prompts**:
- `Is this token safe? 0x...`
- `Check contract risk for PEPE`
- `Is this a honeypot?`
- `Could this be a rug pull?`

---

## 📉 gate-info-trendanalysis

> **Path**: `skills/gate-info-trendanalysis/`

Trend and technical analysis. Fetches K-line data, indicator history, multi-timeframe signals, and market snapshots in parallel. Generates a multi-dimensional technical analysis report.

**Example Prompts**:
- `Technical analysis for BTC`
- `Show me ETH RSI and MACD`
- `What's the trend for SOL?`
- `Check support and resistance levels for BNB`

---

## 🏗️ gate-info-defianalysis

> **Path**: `skills/gate-info-defianalysis/`

DeFi ecosystem analysis via Gate-Info MCP. Routes by intent to overview, single-protocol detail, yield pools, stablecoins, bridges, exchange reserves, or liquidation heatmaps; progressive loading where applicable. Read-only.

**Example Prompts**:
- `DeFi overview and top protocols by TVL`
- `Uniswap TVL and volume`
- `Best USDC lending APY`
- `Binance BTC reserves`
- `BTC liquidation heatmap`

---

## 🗓️ gate-info-macroimpact

> **Path**: `skills/gate-info-macroimpact/`

Macro-driven crypto analysis via Gate-Info and Gate-News MCP: economic calendar, macro indicator or summary, related news, and correlated coin market snapshot in parallel. Read-only.

**Example Prompts**:
- `How does CPI affect BTC?`
- `Any macro data today?`
- `Fed meeting impact on crypto`
- `Latest NFP and risk assets`

---

## ⛓️ gate-info-tokenonchain

> **Path**: `skills/gate-info-tokenonchain/`

Token-level on-chain analysis (holders, activity, large transfers) via Gate-Info MCP. Smart Money / `smart_money` scope not available in this version — use holders, activity, transfers only. Read-only.

**Example Prompts**:
- `ETH holder distribution`
- `On-chain activity for SOL`
- `Large transfers for BTC`
- `Full on-chain picture for ARB`

---

## 📰 gate-news-briefing

> **Path**: `skills/gate-news-briefing/`

Crypto news briefing. Fetches major events, trending news, and social sentiment in parallel, then generates a layered news briefing report.

**Example Prompts**:
- `What happened in crypto recently?`
- `Today's crypto highlights`
- `Any new updates in the market?`
- `Give me the latest crypto news`

---

## 🗣️ gate-news-communityscan

> **Path**: `skills/gate-news-communityscan/`

Community and social sentiment with **X/Twitter** as the primary surface via Gate-News MCP. Combines X discussion search and quantitative social sentiment. When multi-platform UGC is unavailable, label output **X/Twitter only**. Read-only.

**Example Prompts**:
- `What does the community think about ETH?`
- `Twitter sentiment on Bitcoin`
- `What are people saying about the ETF?`
- `KOL takes on SOL today`

---

## 💡 gate-news-eventexplain

> **Path**: `skills/gate-news-eventexplain/`

Event attribution and explanation. When users ask about price anomalies, traces event sources and combines market and on-chain data to generate an "Event → Impact Chain → Market Reaction" analysis report.

**Example Prompts**:
- `Why did BTC crash?`
- `What just happened to ETH?`
- `Why is SOL pumping?`
- `What caused the DOGE dump?`

---

## 📋 gate-news-listing

> **Path**: `skills/gate-news-listing/`

Exchange listing/delisting tracker. Fetches exchange announcements for new listings, delistings, and maintenance, then supplements high-interest new coins with fundamentals and market data.

**Example Prompts**:
- `Any new coins listed recently?`
- `What did Binance list this week?`
- `Show me recent delistings`
- `New token listings today`

---

## 🛠️ gate-mcp-cursor-installer

> **Path**: `skills/gate-mcp-cursor-installer/`

One-click installer for Gate MCP servers and Skills specifically tailored for Cursor.

**Quick Start**:
```bash
bash scripts/install.sh
```

---

## 🛠️ gate-mcp-openclaw-installer

> **Path**: `skills/gate-mcp-openclaw-installer/`

Complete Gate MCP server installer for OpenClaw. Supports spot/futures trading, wallet, market info, and news servers.

**Quick Start**:
```bash
./scripts/install.sh
```

---

## 🛠️ gate-mcp-claude-installer

> **Path**: `skills/gate-mcp-claude-installer/`

One-click installer for **Claude Code (Claude CLI)**: all Gate MCP servers + all Gate Skills.

**Quick Start**:
```bash
# From repo root
bash skills/gate-mcp-claude-installer/scripts/install.sh
```

Optional: `--no-skills` to install MCP only; `--mcp main --mcp dex` etc. to install selected MCPs.

---

## 🛠️ gate-mcp-codex-installer

> **Path**: `skills/gate-mcp-codex-installer/`

One-click installer for **Codex**: all Gate MCP servers + all Gate Skills.

**Quick Start**:
```bash
# From repo root
bash skills/gate-mcp-codex-installer/scripts/install.sh
```

Optional: `--no-skills` to install MCP only; `--mcp main --mcp dex` etc. to install selected MCPs.

---

## 🎁 gate-exchange-referral

> **Path**: `skills/gate-exchange-referral/`

Invite-friends activity recommendation and rule interpretation. Introduces Gate's main referral programs (Earn Together, Help & Get Coupons, Super Commission), explains rules and rewards, and links to the official invite page.

**Example Prompts**:
- `How does the referral program work?`
- `Earn Together referral rules`
- `Where is my referral link?`
- `What rewards do I get for inviting friends?`

---

## 🗂️ gate-exchange-assets-manager

> **Path**: `skills/gate-exchange-assets-manager/`

L2 composite skill: orchestrates multi-account balance overview, margin and liquidation risk, SimpleEarn/staking snapshots, affiliate commissions, and unified-account borrow/collateral/leverage actions (writes require confirmation).

**Example Prompts**:
- `Show my total assets across all accounts`
- `What's my liquidation risk on ETH?`
- `Summarize my staking and SimpleEarn earnings`
- `I want to borrow USDT on unified account`

---

## 🔬 gate-info-research

> **Path**: `skills/gate-info-research/`

Market Research Copilot — an L2 composite skill that combines Gate-Info and Gate-News tools for structured market briefs, single-coin deep dives, multi-coin comparisons, trends, events, and risk checks (read-only; no trading).

**Example Prompts**:
- `Give me a market research brief`
- `Compare BTC and ETH fundamentals and risk`
- `Why is SOL pumping today?`
- `Daily brief on the crypto market`

---

## 🎉 gate-exchange-welfare

> **Path**: `skills/gate-exchange-welfare/`

Welfare center for new-user tasks and rewards using MCP data. Never fabricates reward amounts; guides new vs existing users.

**Example Prompts**:
- `What welfare tasks can I do?`
- `How do I claim new user rewards?`
- `What benefits are available for new users?`

---

## 🌊 gate-exchange-launchpool

> **Path**: `skills/gate-exchange-launchpool/`

LaunchPool suite: browse projects, stake and redeem, query pledge history, and airdrop reward records.

**Example Prompts**:
- `What LaunchPool projects are running?`
- `Stake into LaunchPool for project X`
- `My LaunchPool airdrop history`
- `Redeem my staked tokens from LaunchPool`

---

## 🪪 gate-exchange-kyc

> **Path**: `skills/gate-exchange-kyc/`

Guides users to the Gate KYC portal for identity verification. Does not perform KYC inside chat.

**Example Prompts**:
- `Where do I complete KYC?`
- `Why can't I withdraw?`
- `Link to verify my identity`

---

## 💰 gate-exchange-collateralloan

> **Path**: `skills/gate-exchange-collateralloan/`

Multi-collateral loan: flexible or fixed-term loans, repay, add collateral, or redeem collateral (writes require explicit confirmation).

**Example Prompts**:
- `My collateral loan orders`
- `Repay part of my loan`
- `Add collateral to loan order ...`
- `Current loan interest rate and LTV`

---

## 🎯 gate-exchange-activitycenter

> **Path**: `skills/gate-exchange-activitycenter/`

Platform activity center: campaign types, hot recommendations, activity lists, and my entries (trading competitions, airdrops, newcomer events, etc.).

**Example Prompts**:
- `What activities are running on Gate?`
- `Recommend trading competitions`
- `Show my activity entries`

---

## Getting Started

### Prerequisites

- An AI agent environment that supports skill loading (e.g., Cursor, OpenClaw)
- Node.js & npm

### Setup

Choose the installer skill based on your environment:

#### For Cursor Users

Use the `gate-mcp-cursor-installer` skill to install Gate MCP and Skills with one click:

```bash
# Run the install script
bash skills/gate-mcp-cursor-installer/scripts/install.sh
```

Or simply ask the AI assistant:
```
Help me install Gate MCP
```

#### For OpenClaw Users

Use the `gate-mcp-openclaw-installer` skill:

```bash
# Install all Gate MCP servers (default)
./skills/gate-mcp-openclaw-installer/scripts/install.sh

# Selective installation
./skills/gate-mcp-openclaw-installer/scripts/install.sh --select
```

#### For Claude Code (Claude CLI) Users

Use `gate-mcp-claude-installer` to install all Gate MCP and Gate Skills:

```bash
# From repo root
bash skills/gate-mcp-claude-installer/scripts/install.sh
```

MCP only: `bash skills/gate-mcp-claude-installer/scripts/install.sh --no-skills`

#### For Codex Users

Use `gate-mcp-codex-installer` to install all Gate MCP and Gate Skills:

```bash
# From repo root
bash skills/gate-mcp-codex-installer/scripts/install.sh
```

MCP only: `bash skills/gate-mcp-codex-installer/scripts/install.sh --no-skills`

### Start Using Skills

After installation, ask your AI agent any market or trading question in natural language.

---

## Skills Installation Guide

### General Skills Installation (Recommended)

1. Check whether `npx` is already installed (if not, see the appendix):

   ```bash
   npx -v
   ```

   If a version number is returned (for example, `11.8.0`), `npx` is installed.

![Check npx version](image/general-install-1.png)

2. Install skills with interactive selection:

   ```bash
   npx skills add https://github.com/gate/gate-skills
   ```
   
![Select and install skills](image/general-install-2.png)

3. Install a specific skill (example: `gate-market`):

   ```bash
   npx skills add https://github.com/gate/gate-skills --skill gate-market
   ```
   
![Install a specific skill](image/general-install-3.png)

### Install Skills in Claude CLI

#### Option 1: Natural Language Installation (Recommended)

```text
help me to install skills, github url is: https://github.com/gate/gate-skills
```

![Claude natural language installation](image/claude-install-1.png)

Installation complete.

![Claude installation complete](image/claude-install-2.png)

#### Option 2: Manual Installation

Step 1: Download the skills package (GitHub: <https://github.com/gate/gate-skills>)

Step 2: Unzip the package and copy it to `~/.claude/skills/`.

- Show hidden folders: open your user home folder, then press `Command + Shift + .` (press again to hide)
- Copy folders to target path: copy the `skills` subfolders from `gate-skills-master` into `~/.claude/skills/`
- Verify installation: run `/skills` in Claude CLI, or ask `how many skills have I installed?`

### Install Skills in Codex CLI

#### Option 1: Natural Language Installation (Recommended)

```text
help me to install skills, github url is: https://github.com/gate/gate-skills
```

![Codex natural language installation step](image/codex-nl-install-1.png)

Changes take effect after restarting Codex.

![Codex natural language installation complete](image/codex-nl-install-2.png)

#### Option 2: Terminal Installation

1. In terminal, type `/skills`, choose `1. List skills`, select `Skill Installer`, and enter `https://github.com/gate/gate-skills`

   ![Codex terminal install - open skills menu](image/codex-terminal-install-1.png)
   ![Codex terminal install - select Skill Installer](image/codex-terminal-install-2.png)
   ![Codex terminal install - input repository URL](image/codex-terminal-install-3.png)
   ![Codex terminal install - installation process](image/codex-terminal-install-4.png)

2. Verify installation: restart the terminal and run `/skills` -> `List Skills`

   ![Codex terminal install - verify installed skills](image/codex-terminal-install-5.png)

#### Option 3: Manual Installation

Step 1: Download the skills package (GitHub: <https://github.com/gate/gate-skills>)

![Codex manual install - download repository](image/codex-manual-install-1.png)

Step 2: Unzip the package and copy it to `~/.codex/skills/`.

1. Show hidden folders: open your user home folder, then press `Command + Shift + .` (press again to hide)

   ![Codex manual install - show hidden folders](image/codex-manual-install-2.png)

2. Copy folders to target path: copy all `skills` subfolders from `gate-skills-master` into `~/.codex/skills/`

   ![Codex manual install - copy skills subfolders](image/codex-manual-install-3.png)

3. Verify installation: restart the terminal and run `/skills` -> `List Skills`

   ![Codex manual install - verify installation](image/codex-manual-install-4.png)

### Install Skills in OpenClaw

#### Option 1: Install via Chat (Recommended)

In the OpenClaw chat interface (such as Telegram or Feishu), send the GitHub URL directly to the assistant, for example:

```text
Help me install this skill: https://github.com/gate/gate-skills
```

The assistant will automatically pull the repository, configure the environment, and try to load the skill.

#### Option 2: Auto-install with ClawHub (Recommended)

- Official marketplace (requires `npx`; see appendix for installation):

  ```bash
  npx clawhub@latest install gate-skills
  ```

- GitHub repository:

  ```bash
  npx clawhub@latest add https://github.com/gate/gate-skills
  ```

#### Option 3: Manual Installation

Step 1: Download the skills package (GitHub: <https://github.com/gate/gate-skills>)

![OpenClaw manual install - download repository](image/openclaw-manual-install-1.png)

Step 2: Unzip the package and copy it to `~/.openclaw/skills/`.

1. Show hidden folders: open your user home folder, then press `Command + Shift + .` (press again to hide)
2. Copy folders to target path: copy all `skills` subfolders from `gate-skills-master` into `~/.openclaw/skills/`

Step 3: Restart OpenClaw Gateway.

### Appendix: Install npx on macOS

1. Check whether `npx` is already installed:

   ```bash
   npx -v
   ```

   If a version number is returned (for example, `11.8.0`), `npx` is installed.

2. If `npx` is not installed, use one of the following methods:

   - Option 1: Install via Homebrew

     ```bash
     # Install Homebrew (official)
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

     # Install Homebrew (China mirror)
     /bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"

     # Verify Homebrew
     brew --version

     # Install Node.js (includes npx)
     brew install node

     # Verify npx
     npx -v
     ```

   - Option 2: Install Node.js from the official website (download page):
     <https://nodejs.org/en/download>

---

## Repository Structure

```
gate-github-skills/
├── README.md
├── README_zh.md
├── image/                              # Installation screenshots
└── skills/
    ├── gate-dex-market/                # DEX market data skill (OpenAPI mode)
    ├── gate-dex-trade/                 # DEX trading skill (MCP + OpenAPI dual mode)
    ├── gate-dex-wallet/                # DEX comprehensive wallet skill
    ├── gate-exchange-affiliate/        # Exchange affiliate/partner program
    ├── gate-exchange-alpha/            # Alpha token discovery, market & account
    ├── gate-exchange-assets/           # Exchange asset/balance queries (read-only)
    ├── gate-exchange-coupon/           # Coupon/voucher management & query
    ├── gate-exchange-crossex/          # CrossEx cross-exchange trading operations
    ├── gate-exchange-dual/             # Dual investment query (read-only)
    ├── gate-exchange-flashswap/        # Flash Swap query: pairs, limits, history
    ├── gate-exchange-futures/          # Futures trading skill
    ├── gate-exchange-marketanalysis/   # Market tape analysis skill
    ├── gate-exchange-simpleearn/       # Simple Earn (Uni) query: positions, interest, rates (read-only)
    ├── gate-exchange-spot/             # Spot trading skill
    ├── gate-exchange-staking/          # Staking (earn) query (read-only)
    ├── gate-exchange-subaccount/       # Sub-account management: list, create, lock/unlock
    ├── gate-exchange-tradfi/           # TradFi query: orders, positions, market, assets, MT5 (read-only)
    ├── gate-exchange-trading-copilot/  # End-to-end trading copilot (judgment → execution)
    ├── gate-exchange-transfer/         # Internal transfer between trading accounts
    ├── gate-exchange-unified/          # Unified account: borrow/repay, leverage, collateral
    ├── gate-exchange-vipfee/           # VIP tier & trading fee rate query
    ├── gate-info-addresstracker/       # On-chain address tracking skill
    ├── gate-info-coinanalysis/         # Single-coin analysis skill
    ├── gate-info-coincompare/          # Multi-coin comparison skill
    ├── gate-info-defianalysis/         # DeFi TVL, platforms, yield, bridges, reserves, liquidation skill
    ├── gate-info-liveroomlocation/     # Live stream & replay listing skill
    ├── gate-info-macroimpact/          # Macro calendar, indicators, news + market linkage skill
    ├── gate-info-marketoverview/       # Market overview skill
    ├── gate-info-riskcheck/            # Token risk assessment skill
    ├── gate-info-tokenonchain/         # Token on-chain holders, activity, transfers skill
    ├── gate-info-trendanalysis/        # Trend & technical analysis skill
    ├── gate-news-briefing/             # News briefing skill
    ├── gate-news-communityscan/       # Community / X sentiment skill
    ├── gate-news-eventexplain/         # Event explanation skill
    ├── gate-news-listing/              # Listing/delisting tracker skill
    ├── gate-mcp-cursor-installer/      # Cursor MCP installer skill
    ├── gate-mcp-openclaw-installer/    # OpenClaw MCP installer skill
    ├── gate-mcp-claude-installer/      # Claude Code (Claude CLI) MCP + Skills installer
    └── gate-mcp-codex-installer/       # Codex MCP + Skills installer
```

---

## About This Repository

Each skill lives in its own folder under `skills/` and contains:

- **`SKILL.md`** — Skill definition with YAML frontmatter (name, version, description, trigger phrases) and structured instructions including routing rules and workflows.
- **`references/`** — Detailed sub-module documentation with step-by-step workflows and report templates.
- **`CHANGELOG.md`** — Version history and change log.

---

## Contribution

We welcome contributions! To add a new skill:

1. **Fork the repository** and create a new branch:
   ```bash
   git checkout -b feature/<skill-name>
   ```

2. **Create a new folder** under `skills/` containing at least a `SKILL.md` file.

3. **Follow the required format**:
   ```markdown
   ---
   name: <skill-name>
   version: "<version>"
   updated: "<YYYY-MM-DD>"
   description: A clear description of what the skill does and when to trigger it.
   ---

   # <Skill Title>

   [Add instructions, routing rules, workflows, and report templates here]
   ```

4. **Add reference documents** in a `references/` subfolder for complex sub-modules.

5. **Open a Pull Request** to `main` for review.

---

## Disclaimer

Gate Skills is an informational tool only. All outputs are provided on an "as is" and "as available" basis, without representation or warranty of any kind. It does not constitute investment, financial, trading, or any other form of advice, nor does it represent a recommendation to buy, sell, or hold any assets. Digital asset prices are subject to high market risk and price volatility. You are solely responsible for your investment decisions. Past performance is not a reliable predictor of future performance. Please consult an independent financial adviser prior to making any investment.
