---
title: Gate Skills Intent Disambiguation Rules
version: v1.0.0
last_updated: 2026-03-26
scope: "gate-mcp / CEX × DEX × Info × News"
---

# Intent Disambiguation Rules

> Shared routing rules for all Gate Skills (CEX / DEX / Info / News).
> This document is referenced by `gate-runtime-rules.md` Rule 0 and loaded automatically for all skills that follow the shared runtime rules.

This document is only responsible for determining which domain a user's intent belongs to. The specific skill to call is determined by each domain's skill list.

**Versioning:**

- Minor +1 (v1.x): New or modified scenario rules
- Major +1 (v2.0): Structural overhaul

---

## I. Domain Definitions


| Domain   | Meaning                                                                                                                                                                                                                                                                              |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **CEX**  | Gate centralized exchange: market data queries (spot/futures/options/delivery tickers, order books, K-line, funding rates, etc.) need no login; trading, account management, wallet operations (balance, orders, transfers, withdrawals, etc.) require authorization                 |
| **DEX**  | On-chain decentralized context: on-chain data queries (including token info, liquidity, market data, chip / position distribution, holders, leaderboards, token security checks, same-name / similar-token analysis, etc.) need no login; wallet, swap, transfer, withdraw to exchange (DEX to CEX), UID binding, etc. require login |
| **Info** | Market information & analysis, including coin info, technical analysis, on-chain data, compliance checks, etc., no login required                                                                                                                                                    |
| **News** | News & announcements, including exchange announcements, industry news, social sentiment, etc., no login required                                                                                                                                                                     |


---

## II. Signal Word Routing Table

When identifying user intent, prioritize matching the following signal words to determine the target domain:


| Signal Words / Expressions                                                                                                                                                                                                                                                                                                                                                                                             | Route to                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| account, spot, futures, perpetual, options, delivery, margin, collateral, exchange balance                                                                                                                                                                                                                                                                                                                             | → **CEX**                                        |
| withdraw, deposit, transfer, internal transfer, withdrawal fee, deposit address                                                                                                                                                                                                                                                                                                                                        | → **CEX**                                        |
| staking, flexible savings, dual investment                                                                                                                                                                                                                                                                                                                                                                             | → **CEX** (earn products, not DEX)               |
| on-chain market data, token market leaderboards / rankings, price, chip / position distribution, holders, holder concentration, token security check, honeypot, rug, malicious token, rug-pull risk, compliance check, security audit, tax, blacklist + contract address, same-name / similar token, copycat, fake vs real, knockoff, contract comparison, official contract, same contract, whether same contract, CA | → **DEX** (on-chain queries, no login)           |
| on-chain operation, on-chain, broadcast, send transaction, gas fee, on-chain swap                                                                                                                                                                                                                                                                                                                                      | → **DEX** (wallet & on-chain tx, login required) |
| on-chain wallet login, Google login, Gate OAuth, connect wallet account, session expired, re-login                                                                                                                                                                                                                                                                                                                    | → **DEX** (auth)                                 |
| on-chain balance, wallet balance, token holdings, portfolio value, wallet address, my address, transaction history, swap history                                                                                                                                                                                                                                                                                            | → **DEX** (asset query)                          |
| on-chain transfer, on-chain send, send tokens to address, batch transfer, pay someone crypto                                                                                                                                                                                                                                                                                                                           | → **DEX** (transfer)                             |
| 402 payment, x402, payment required, pay for API, pay for URL, HTTP 402, Permit2 payment, paid endpoint, pay for access                                                                                                                                                                                                                                                                                              | → **DEX** (x402)                                 |
| connect DApp, sign message, approve token, revoke approval, contract call, EIP-712, personal_sign, add liquidity, stake on Lido, mint NFT                                                                                                                                                                                                                                                                             | → **DEX** (DApp)                                 |
| gate-wallet CLI, command line, terminal, openapi-swap, hybrid swap, script automation                                                                                                                                                                                                                                                                                                                                  | → **DEX** (CLI)                                  |
| withdraw to exchange, cash out to Gate, bind UID, link Gate account                                                                                                                                                                                                                                                                                                                                                    | → **DEX** (withdraw to CEX)                      |
| technical analysis, RSI, MACD, Bollinger Bands, moving average, KDJ, indicators                                                                                                                                                                                                                                                                                                                                        | → **Info**                                       |
| news, announcement, listing, social sentiment                                                                                                                                                                                                                                                                                                                                                                          | → **News**                                       |
| compliance check + no contract address                                                                                                                                                                                                                                                                                                                                                                                 | → **Info**                                       |


> "CA" / contract address is only a supporting signal when paired with clear intent (security check, name comparison, token info). Do not route by address shape alone. See **Scenario 16**.

> ⚠️ **Address format (0x / Solana address) alone is NOT a routing criterion.** CEX deposit addresses and DEX on-chain addresses can look the same. Route by **verbs and business object**, not address format alone.

---

## III. Scenario-Based Disambiguation Rules

### Scenario 1: Check Balance / Assets / Position

**Trigger words:** balance, assets, position, how much do I have, in account, portfolio value, holdings, net worth

**Rules:**

1. If CEX signal words appear → **CEX**
2. If DEX signal words appear (on-chain balance, wallet balance, token holdings, my tokens) → **DEX** (asset query)
3. If no clear signal words → Must confirm:
> "Would you like to check your Gate exchange account balance or on-chain wallet balance?"

---

### Scenario 2: Check Wallet Address

**Trigger words:** wallet address, my address, deposit address, receiving address

**Background:** CEX has deposit addresses (inbound addresses generated by Gate for users), DEX has on-chain wallet addresses (EVM / Solana). Both can be in 0x or Solana format; do not distinguish by address format alone.

**Rules:**

- "deposit address" / "address to receive from others" → **CEX**
- "my on-chain address" / "DEX wallet address" / "my ETH address" / "my Solana address" → **DEX** (asset query)
- Only says "my address" / "wallet address" with no other context → Must confirm:
  > "Do you need your Gate exchange deposit address or your on-chain wallet address?"

---

### Scenario 3: Check Price / Market Data

**Trigger words:** how much, price, market, how much up/down, how much it moved, current price

**Rules:**

1. "futures price" / "perpetual price" / "contract price" → **CEX** (futures)
2. "on-chain price" / mentions specific DEX trading pair → **DEX** (on-chain queries)
3. Needs market overview (market cap, fear & greed index, etc.) → **Info**
4. **Default (no qualifier) → CEX** (use exchange spot price as baseline)

---

### Scenario 4: Check K-line / Chart

**Trigger words:** K-line, candlestick, chart, daily, hourly

**Rules:**

1. "futures K-line" / "perpetual K-line" / "options K-line" → **CEX** (corresponding category)
2. "on-chain K-line" / mentions specific DEX trading pair → **DEX** (on-chain queries)
3. **Default (no qualifier) → Info** (more comprehensive data, multi-timeframe)
4. Within CEX, if category not specified, default to **spot** K-line

---

### Scenario 5: Check Gainers / Losers / Trending

**Trigger words:** gainers list, losers list, top gainers, trending, top performers

**Rules:**

1. "exchange listed coins" → **CEX**
2. "on-chain token gainers/losers" → **DEX** (on-chain queries)
3. **Default → Info** (widest coverage)

---

### Scenario 6: Check Coin Info (including token research)

**Trigger words:** how is this coin, tell me about XXX, XXX basic info, token research, token info

**Rules:**

- **Default → Info** (most comprehensive; **token research** here means **token info lookup**)
- "what trading pairs does Gate support for this coin" → **CEX**
- "on-chain holders / on-chain activity" → **DEX** (on-chain queries)
- Explicit **token security check** or **same-name / similar-token / contract comparison** → **DEX** (on-chain queries; same as **Scenario 16**)

---

### Scenario 7: Trading / Place Order

**Trigger words:** buy, sell, long, short, open position, place order, submit order

**Pre-check: Is it a conditional order?**

First identify if there's a price trigger condition, then determine domain:


| Trigger Words                                                                                | Route                                                                  |
| -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| "when...", "at price X", "if price reaches", "take profit", "stop loss", "conditional order" | → **CEX** (conditional order), do NOT route to regular order placement |
| No trigger condition + DEX signal words                                                      | → **DEX** (on-chain swap, see Scenario 8)                              |
| No trigger condition + no clear signal words                                                 | → **CEX**, further confirm spot or futures                             |


**Ambiguous Phrasing:**

- "sell-in" / "buy-out" (contradictory terms) → Must confirm buy or sell direction, do not infer
- Spot/futures not specified → Ask "Spot or futures?", do not call futures tools directly

---

### Scenario 8: Swap / Buy / Sell

**Trigger words:** swap, exchange, convert, buy, sell

**Rules:**
1. DEX signal words + swap/buy/sell → **DEX** (swap)
2. buy/sell + chain name or on-chain context → **DEX** (swap)
3. "convert" / "flash swap" (no chain context) → **CEX**
4. No clear signal words → Must confirm:
   > "Would you like to use Gate's flash swap (CEX) or execute an on-chain swap (DEX)?"
5. buy/sell + no qualifier → **CEX**, further confirm spot or futures

---

### Scenario 9: Transfer / Withdraw【⚠️ Mandatory Double Confirmation】

**Trigger words:** transfer, send to, send to address, withdraw, cash out, cashout (off-exchange withdrawal), send tokens, pay someone, move tokens

> **Regardless of context clarity, transfer operations MUST be double-confirmed. Never auto-execute.**
> CEX and DEX both have withdrawal scenarios. CEX withdraws to on-chain; DEX withdraws to CEX or custom addresses.

**Route by operation verb, NOT by destination address format:**


| User Expression                                                      | Route                         |
| -------------------------------------------------------------------- | ----------------------------- |
| "withdraw to 0x123..." / "cash out to Solana address"              | → **CEX** (withdrawal)        |
| "withdraw 100 USDT to 0x123... via ERC20"                            | → **CEX** (withdrawal)        |
| Transfer from spot to futures account / internal transfer            | → **CEX** (internal transfer) |
| "withdraw to exchange" / "cash out to Gate" / "withdraw to my deposit address" | → **DEX** (withdraw to exchange module) |
| "on-chain transfer" / "on-chain send" / "broadcast this transaction" | → **DEX** (transfer)          |
| "send 1 ETH to 0x..." / "transfer USDT" / "pay someone crypto" / "batch transfer" (with on-chain context or DEX session) | → **DEX** (transfer) |


**Must display and confirm before execution:**

- CEX withdrawal: destination address, network, amount, fee, actual receipt amount, warn irreversible
- DEX transfer / withdraw to exchange: destination address, chain, Gate UID (if to exchange), token, amount, estimated gas fee, warn irreversible
- DEX on-chain transfer supports both native assets (ETH / SOL / BNB) and token transfers (ERC20 / SPL)

---

### Scenario 10: Check Orders / Trade History

**Trigger words:** my orders, trade history, order history, recent trades, transaction history, swap history, past swaps

**Rules:**

1. If this session has already established CEX context → **CEX** (corresponding category, default spot if not specified)
2. If this session has already established DEX context → **DEX** (asset query)
3. "on-chain transaction history" / "swap history" / "past transactions on-chain" → **DEX** (asset query)
4. No context → Must confirm:
> "Are you checking exchange order records or on-chain transaction history?"

---

### Scenario 11: Technical Analysis

**Trigger words:** technical analysis, RSI, MACD, moving average, Bollinger Bands, KDJ, indicators

**Rules:**

- **Always → Info**
- Do NOT use CEX / DEX K-line data to calculate indicators manually

---

### Scenario 12: New Coins / Recent Listings

**Trigger words:** new coins, latest listings, what's new

**Rules:**

1. "what did Gate list recently" / "exchange new listings" → **News**
2. "Gate Alpha new tokens" → **CEX** (Alpha)
3. "recently launched on-chain tokens" → **DEX**
4. **No qualifier → News** (listing announcements are most common intent)

---

### Scenario 13: Login / Authorization / Binding

**Trigger words:** login, authorize, connect account, bind UID, link account, sign in, authenticate, session expired, re-login, switch account, Google OAuth, Gate OAuth

**Rules:**

- "login to Gate" / "connect to exchange" → **CEX** OAuth2
- "connect wallet" / "connect Google wallet" / "Google OAuth wallet login" / "Gate OAuth wallet login" / "session expired" / "not logged in" / "re-login" → **DEX** (auth)
- "switch account" / "login with a different account" → **DEX** (auth, logout + re-login flow)
- "bind Gate UID" / "bind exchange account to wallet" → **DEX** (withdraw module binding flow)
- No clear signal words → Must confirm:
  > "Would you like to login to your Gate exchange account, connect your on-chain wallet, or bind your wallet to your exchange account?"

---

### Scenario 14: Earn / Staking

**Trigger words:** earn, staking, subscribe, dual investment, flexible savings, ETH2, on-chain staking

**Background:** Gate's "staking (on-chain earn)" is a **CEX earn product**. Although the name contains "on-chain", it is custodied and operated by Gate, completely unrelated to DEX on-chain staking.

**Rules:**

1. "Gate earn" / "dual investment" / "flexible savings" / "staking" → **CEX** (earn)
2. "DeFi mining" / "on-chain staking" / "on-chain LP" / mentions specific DeFi protocol name → **DEX** (DApp)
3. Only says "staking" / "earn yield" with no qualifier → Must confirm:
> "Would you like to participate in Gate's staking earn products or perform on-chain staking operations?"
4. **Prohibit routing Gate staking earn to DEX**, custody method and risks are completely different

---

### Scenario 15: Check Order Book / Liquidity Depth

**Trigger words:** order book, depth, bid/ask, order wall, liquidity pool, LP depth

**Rules:**

1. DEX signal words / "on-chain liquidity" / "DEX pool depth" → **DEX** (on-chain queries)
2. **Default → CEX**, default to **spot** order book if category not specified
3. Prohibit mixing CEX order book data with DEX liquidity pool data

---

### Scenario 16: Token Security Check & Same-Name / Similar-Token Analysis

**Trigger words:** token security, security scan, honeypot, rug, malicious token, rug-pull risk, contract risk, tax / blacklist; same-name coin, similar name, copycat, fake vs real, knockoff, official contract, is it the same as the official contract, are these two addresses the same token

**Rules:**

1. On-chain **contract** risk and security checks (honeypot, audit, tax, blacklist, compliance items, etc.) → **DEX** (on-chain queries)
2. **Same-name / similar tokens**, multi-contract comparison, copycat vs official, whether it matches the **official contract** → **DEX** (on-chain queries)
3. Only vague "how is this coin" with no security or contract comparison intent → **Scenario 6**, default **Info**
4. No contract address or no on-chain comparison target → prefer **Info** for background, then ask for **contract address** before **DEX** deep checks

---

### Scenario 17: x402 Payment (HTTP 402)

**Trigger words:** 402 payment, x402, payment required, pay for API, pay for URL, HTTP 402, paid endpoint, pay for access, Permit2 payment, upto payment

**Background:** x402 is a payment protocol for HTTP 402 Payment Required responses. The DEX wallet can automatically pay for gated APIs/resources using on-chain payment schemes.

**Rules:**

1. Any mention of "402", "x402", "pay for API", "pay for URL", "payment required", "paid endpoint" → **DEX** (x402)
2. URL that returns 402 or user reports "that URL returned 402" → **DEX** (x402)
3. **Do NOT route to CEX** — x402 is exclusively an on-chain wallet payment mechanism
4. If token approval is required during x402 payment → route to **DEX** (DApp approval flow) first, then retry **DEX** (x402)

---

### Scenario 18: DApp Interaction

**Trigger words:** connect DApp, sign message, approve token, revoke approval, contract call, EIP-712, Permit, personal_sign, add liquidity, stake on protocol, mint NFT, interact with Uniswap / Aave / Lido, authorize contract

**Background:** DApp interactions include connecting wallet, message signing (personal_sign / EIP-712), DApp transaction execution, ERC20 approve / revoke, and arbitrary contract calls. All require on-chain wallet authentication.

**Rules:**

1. "connect wallet to DApp" / "sign message" / "approve token for contract" / "revoke approval" / "contract call" → **DEX** (DApp)
2. "add liquidity" / "stake ETH on Lido" / "deposit to Aave" / "mint NFT" / "buy NFT" → **DEX** (DApp)
3. "sign this Permit" / "EIP-712 typed data" / "personal_sign" → **DEX** (DApp)
4. "swap ETH for USDT" / "buy SOL" / "exchange tokens" (direct swap execution) → **DEX** (swap, not DApp)
5. "is this token safe?" / "audit this contract" (security query without executing a transaction) → **DEX** (on-chain queries, not DApp)

---

### Scenario 19: CLI / Command-Line Operations

**Trigger words:** gate-wallet, CLI, command line, terminal, openapi-swap, hybrid swap, script automation

**Background:** The gate-wallet CLI provides dual-channel command-line access to wallet operations including auth, balance, transfer, swap, approve, and market data.

**Rules:**

1. Any mention of "gate-wallet", "CLI", "command line", "terminal", "openapi-swap", "hybrid swap" → **DEX** (CLI)
2. "use openapi" / "AK/SK" / "DEX API" with logged-in MCP session → **DEX** (CLI hybrid mode)
3. "self-signing" / "use private key" → **DEX** (OpenAPI signing channel, not wallet CLI)
4. **Do NOT route to CEX** — gate-wallet CLI is an on-chain wallet tool

---

## IV. Session Context Memory Rules

1. If user has clearly chosen a domain in this conversation, subsequent ambiguous intents **prioritize continuation of that domain**, no need to re-confirm
2. When context switches (e.g., from checking CEX balance to asking about on-chain address), **explicitly identify switch signals**, do not reuse old context
3. When both CEX and DEX are connected, context memory **does not cross domains**

---

## V. Fallback Phrasing When Unable to Determine

When intent signals are insufficient and cannot route via above rules, use uniformly:

> "Your request may involve exchange account (CEX) or on-chain wallet (DEX). Which one would you like to operate?"

**Prohibited:** Randomly selecting a domain when intent is unclear, especially for fund-related operations.

---

## VI. Degradation Rules When Domain Unavailable

### 6.1 Explicitly Inform User, Do Not Fail Silently

> "Current [DEX / CEX] related tools not detected, please install the corresponding MCP first. See [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) Rule 2: MCP Installation Pre-check."

### 6.2 Prohibit Cross-Domain Degradation Substitution


| User Request                         | Prohibited Behavior                    |
| ------------------------------------ | -------------------------------------- |
| DEX balance query, DEX unavailable   | ❌ Do NOT change to check CEX balance   |
| On-chain swap, DEX unavailable       | ❌ Do NOT change to CEX flash swap      |
| CEX order placement, CEX unavailable | ❌ Do NOT change to DEX swap            |
| Market K-line, Info unavailable      | ❌ Do NOT patch data from other domains |


> Cross-domain substitution may cause users to execute operations in the wrong domain, especially dangerous for fund-related scenarios.
