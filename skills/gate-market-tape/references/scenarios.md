# Gate Market Tape Intelligence — Scenarios & MCP Call Specs

This document defines the **MCP call order, parameters, required fields, and output format** for each scenario. Implementations must call Gate MCP in the order specified under each Case and produce reports according to the templates below.

| Case | Scenario | Core MCP Call Order |
|------|----------|---------------------|
| 1 | Liquidity analysis | list_order_book → list_candlesticks → list_tickers (use futures APIs when user says perpetual/contract) |
| 2 | Momentum (buy vs sell) | list_trades → list_tickers → list_candlesticks → list_order_book → list_futures_funding_rate (futures APIs when contract) |
| 3 | Liquidation monitoring | list_futures_liq_orders → list_futures_candlesticks → list_futures_tickers |
| 4 | Funding rate arbitrage | list_futures_tickers → list_futures_funding_rate → list_tickers → list_order_book |
| 5 | Basis (spot vs futures) | list_tickers(spot) → list_futures_tickers → list_futures_premium_index |
| 6 | Manipulation risk | Spot: list_order_book → list_tickers → list_trades. When user says perpetual/contract: list_futures_order_book → list_futures_tickers → list_futures_trades |
| 7 | Order book explainer | list_order_book(limit=10) → list_tickers |

---

## Case 1: Liquidity Analysis

### MCP Call Spec (document-aligned)

For liquidity analysis, **call Gate MCP in this order** and extract the listed fields; output must follow the Report Template below.

| Step | MCP Tool | Parameters | Required Fields |
|------|----------|------------|----------------|
| 1 | `list_order_book` (spot) | `currency_pair={BASE}_USDT`, `limit=20` | Number of ask/bid levels; top 10 bid/ask depth totals; bid1/ask1 (for spread and slippage) |
| 2 | `list_candlesticks` (spot) | `currency_pair={BASE}_USDT`, `interval=1d`, `limit=30` | Last 30 days volume (for 30d avg); latest candle for 24h volume reference |
| 3 | `list_tickers` (spot) | `currency_pair={BASE}_USDT` | `last`; `quoteVolume` 24h (USDT); `changePercentage` 24h; `high24h`/`low24h` |
| 4 (optional) | `list_trades` (spot) | `currency_pair={BASE}_USDT`, `limit=100` | Recent trade size distribution for "recent flow" and participation |

**Calculation & judgment** (aligned with SKILL):

- **API choice**: Use futures APIs (e.g. list_futures_order_book) when user says "perpetual" or "contract"; otherwise spot.
- **Slippage** = `2×(ask1−bid1)/(bid1+ask1)×100%`; if > 0.5% → flag "high slippage risk".
- **Depth**: asks/bids depth < 10 levels → flag "low liquidity".
- **24h volume** < 30-day volume average → flag "cold pair".
- **Liquidity rating**: Combine above into 1–5 ⭐.

**Output**: Must include a "Core metrics" table (order book depth, 24h volume, 30d avg volume, bid-ask spread, slippage + status), "Assessment" (liquidity rating x/5 ⭐), and short "Recommendation".

---

### Scenario 1.1: Spot liquidity query

**Context**: User wants to know ETH spot trading conditions.

**Prompt examples**:
- "How is ETH liquidity?"
- "当前 ETH 的流动性如何"

**Expected behavior**:
1. Call in order per **MCP Call Spec**: `list_order_book` → `list_candlesticks` → `list_tickers` (optional `list_trades`).
2. From order book: level count, top 10 depth, bid1/ask1.
3. From candlesticks: 30d avg volume, 24h volume.
4. From tickers: last, 24h quote volume, change.
5. Compute slippage; apply document logic for status and rating.
6. Output core metrics table + assessment + recommendation per Report Template.

**Output**:
```markdown
## ETH Liquidity Analysis

### Core metrics

| Metric | Value | Status |
|--------|-------|--------|
| Order book depth | 20 levels | OK |
| 24h volume | $485M | Active |
| 30d avg volume | $320M | - |
| Bid-ask spread | 0.02% | Excellent |
| Slippage risk | 0.03% | Very low |

### Assessment

**Liquidity rating**: 5/5 ⭐

ETH liquidity is excellent, suitable for large size.
```

---

### Scenario 1.2: Futures liquidity query

**Context**: User asks about perpetual/contract depth.

**Prompt examples**:
- "How is BTC perpetual depth?"
- "BTC永续合约深度怎么样"

**Expected behavior**:
1. Detect "perpetual/contract" and use **futures** MCP: `list_futures_order_book` (`settle=usdt`, `contract=BTC_USDT`, `limit=20`) → optional `list_futures_tickers`, `list_futures_candlesticks`(1d, 30).
2. Extract level count, top 10 depth, bid1/ask1; compute slippage.
3. Output core metrics table + liquidity rating per liquidity criteria.

**Output**:
```markdown
## BTC_USDT Perpetual — Liquidity Analysis

| Metric | Value | Status |
|--------|-------|--------|
| Order book depth | 50 levels | Excellent |
| Slippage risk | 0.01% | Very low |

Liquidity rating: 5/5 ⭐
```

---

### Scenario 1.3: Low-liquidity / cold pair warning

**Context**: User queries a low-cap or illiquid pair.

**Prompt examples**:
- "How is XYZ liquidity?"
- "XYZ币的流动性如何"

**Expected behavior**:
1. Still follow **Case 1 MCP Call Spec**: order_book → candlesticks → tickers.
2. If depth < 10 levels, or 24h volume < 30d avg, or slippage > 0.5%, mark 🔴 in core metrics and output risk note + low liquidity rating.

**Output**:
```markdown
## XYZ Liquidity Analysis

### Risk notice

| Metric | Value | Status |
|--------|-------|--------|
| Order book depth | 5 levels | Insufficient depth |
| 24h volume | $15K | Cold pair |
| Slippage risk | 2.3% | High |

**Liquidity rating**: 1/5 ⭐

⚠️ This pair has poor liquidity; large orders will incur significant slippage.
```

---

## Case 2: Momentum (buy vs sell)

### MCP Call Spec (document-aligned)

**Trigger**: "Is BTC more long or short in 24h, and is it sustainable?" For momentum analysis, **call in this order**; use futures APIs when user asks about contract.

| Step | MCP Tool | Parameters | Required Fields |
|------|----------|------------|----------------|
| 1 | `list_trades` (spot/futures) | `currency_pair` or `contract`+`settle`, `limit=1000` | Buy/sell volume; buy share = buy_volume / total_volume |
| 2 | `list_tickers` (spot/futures) | Same pair | 24h volume, 24h change |
| 3 | `list_candlesticks` (spot/futures) | `interval=1d`, `limit=30` | 30-day average volume |
| 4 | `list_order_book` (spot/futures) | `limit=20` | Top 10 bid/ask depth for long/short balance |
| 5 | `list_futures_funding_rate` or equivalent | When contract | Funding rate; positive → long bias, negative → short bias |

**Calculation & judgment** (aligned with SKILL):

- **Buy share > 70%** → "buy-side strong"; sell share > 70% → "sell-side strong".
- **24h volume > 30d avg** → "active".
- **Funding rate** sign + **order book top 10** balance → overall bias and sustainability.

**Output**: Must include "Buy/sell forces" table, momentum direction, sustainability, and short analysis.

---

### Scenario 2.1: Basic momentum query

**Context**: User wants to judge short-term long vs short strength.

**Prompt examples**:
- "Is BTC more long or short in 24h, and is it sustainable?"
- "BTC 近 24h 多头厉害还是空头厉害，可持续吗"

**Expected behavior**:
1. Call per **MCP Call Spec**: `list_trades` → `list_tickers` → `list_candlesticks` → `list_order_book` → `list_futures_funding_rate` (futures when contract).
2. From trades: buy/sell volume, buy share; tickers: 24h volume and change; candlesticks: 30d avg; order book: top 10 long/short depth; funding rate for bias.
3. Apply logic (buy > 70% → buy-side strong; 24h > 30d avg → active; funding + book → direction and sustainability).
4. Output buy/sell table + direction + analysis per Report Template.

**Output**:
```markdown
## BTC Momentum Analysis

### Buy/sell forces

| Metric | Value |
|--------|-------|
| Buy share | 65% |
| Sell share | 35% |
| 24h volume | $2.1B |
| 30d avg volume | $1.8B |
| Activity | Active |

### Conclusion

**Momentum direction**: Buy-side slightly ahead

Buy share 65% but below 70% "strong" threshold; currently long-leaning but not one-sided. Volume above 30d avg; activity is rising.
```

---

### Scenario 2.2: One-sided strong buy

**Context**: User asks whether buy side is strong.

**Prompt examples**:
- "Is ETH buy side strong?"
- "ETH买盘强吗"

**Expected behavior**:
1. Call per **MCP Call Spec**: `list_trades`(ETH_USDT) → `list_tickers` → `list_candlesticks`.
2. Compute buy/sell share; if buy > 70% mark as buy-side strong.
3. Output buy/sell table + direction (buy-side strong).

**Output**:
```markdown
## ETH Momentum Analysis

### Buy/sell forces

| Metric | Value |
|--------|-------|
| Buy share | 78% |
| Sell share | 22% |

### Conclusion

**Momentum direction**: Buy-side strong

Buy share 78%, well above 70% threshold; clear long-dominated tape. With volume expansion, trend may extend.
```

---

### Scenario 2.3: Futures momentum query

**Context**: User explicitly asks about contract momentum.

**Prompt examples**:
- "BTC contract momentum"
- "BTC合约动能判断"

**Expected behavior**:
1. Detect "contract" and use **futures** MCP: `list_trades` (futures, `settle=usdt`, `contract=BTC_USDT`) → `list_futures_tickers` → `list_futures_candlesticks`.
2. Extract buy/sell share, 24h volume, 30d avg per MCP Call Spec; same output structure, data from futures.

---

## Case 3: Liquidation Monitoring

### MCP Call Spec (document-aligned)

**Trigger**: "Recent liquidations?", "Which coins liquidated most?" For liquidation monitoring, **call in this order** (futures only).

| Step | MCP Tool | Parameters | Required Fields |
|------|----------|------------|----------------|
| 1 | `list_futures_liq_orders` | `settle=usdt`, time range (last 1h; optional 24h for daily baseline) | Liq volume by contract; long (size>0) / short (size<0); 1h total liq |
| 2 | `list_futures_candlesticks` | `settle=usdt`, `contract`, `interval=5m`, `limit=12` | Price during liq window, current price, recovery |
| 3 | `list_futures_tickers` | `settle=usdt` (or specific contract) | Current price, 24h change |

**Calculation & judgment** (aligned with SKILL):

- **1h liq > 3× daily avg** → flag "anomaly".
- **One-sided liq > 80%** (long or short) → flag "long squeeze" or "short squeeze".
- **Price recovered** (vs wick low/high) → flag "wick / spike".

**Output**: Must include "Market overview" table, "Anomaly contracts" table, and wick analysis when relevant (low, current price, recovery).

---

### Scenario 3.1: Market-wide liquidation overview

**Context**: User wants a market-wide liquidation view.

**Prompt examples**:
- "Recent liquidations?"
- "最近爆仓情况"

**Expected behavior**:
1. Call per **MCP Call Spec**: `list_futures_liq_orders` → `list_futures_candlesticks` → `list_futures_tickers`.
2. Aggregate liq by contract; long/short share; if daily baseline available, compute 1h vs daily multiple.
3. Apply logic: 1h liq > 3× daily → anomaly; one-sided > 80% → long/short squeeze; price recovered → wick.
4. Output market overview table + anomaly contracts table.

**Output**:
```markdown
## Liquidation Monitoring

**Time**: 2026-03-05 15:30

### Market overview

| Metric | Value |
|--------|-------|
| 1h total liq | $45M |
| Long liq | $38M (84%) |
| Short liq | $7M (16%) |

### Anomaly contracts

| Contract | Liq volume | Multiple | Type |
|----------|------------|----------|------|
| ETH_USDT | $18M | 4.2x | Long squeeze |
| SOL_USDT | $8M | 3.5x | Long squeeze |

Long liq 84%; current move is squeezing long leverage.
```

---

### Scenario 3.2: Wick / spike detection

**Context**: User suspects a wick/spike (e.g. BTC).

**Prompt examples**:
- "Did BTC just wick?"
- "刚才BTC是不是插针了"

**Expected behavior**:
1. Call per **MCP Call Spec**: `list_futures_liq_orders`(1h, optional filter contract=BTC_USDT) → `list_futures_candlesticks`(BTC_USDT, 5m, 12) → `list_futures_tickers`.
2. From liq: long/short share; from candlesticks: low, current price; recovery = (current − low) / (pre-spike high − low) or similar.
3. If long-dominated liq and recovery > 80%, output wick analysis (liq table + low/current/recovery + wick conclusion).

**Output**:
```markdown
## BTC Wick Analysis

### Liquidation data

| Metric | Value |
|--------|-------|
| 1h liq | $25M |
| Long liq | $23M (92%) |
| Low | $62,100 |
| Current | $63,800 |
| Recovery | 85% |

### Conclusion

**Type**: Wick / spike

- Long-dominated liq (92%)
- Price recovered 85%
- Typical short wick squeezing long leverage
```

---

## Case 4: Funding Rate Arbitrage Scan

### MCP Call Spec (document-aligned)

**Trigger**: "Any arbitrage opportunities?", "Which coins have extreme funding?" For arbitrage scan, **call in this order**.

| Step | MCP Tool | Parameters | Required Fields |
|------|----------|------------|----------------|
| 1 | `list_futures_tickers` | `settle=usdt` | All contracts' funding_rate, 24h volume |
| 2 | `list_futures_funding_rate` or equivalent | For candidates / full market | Rate details |
| 3 | `list_tickers` (spot) | Per candidate `currency_pair={BASE}_USDT` | Spot last; spot–futures spread |
| 4 | `list_order_book` (spot) | For top candidates `currency_pair`, `limit=20` | Top 10 depth; exclude if depth too thin |

**Calculation & judgment** (aligned with SKILL):

- **|rate| > 0.05% and 24h vol > $10M** → candidate.
- **Spot–futures spread > 0.2%** → bonus.
- **Book depth too thin** → exclude.

**Output**: Must include "Arbitrage opportunities" table, strategy note (long basis / short basis), and risk disclaimer.

---

### Scenario 4.1: Market-wide arbitrage scan

**Context**: User wants to find funding arbitrage opportunities.

**Prompt examples**:
- "Any arbitrage opportunities?"
- "现在有没有套利机会"

**Expected behavior**:
1. Call per **MCP Call Spec**: `list_futures_tickers` → `list_futures_funding_rate` → `list_tickers`(candidates) → `list_order_book`(top candidates).
2. Logic: |rate|>0.05% and 24h vol>$10M → candidate; spot–futures spread>0.2% → bonus; thin depth → exclude.
3. Output arbitrage table + strategy + risk note.

**Output**:
```markdown
## Funding Rate Arbitrage Scan

**Time**: 2026-03-05 15:30

### Top 5 opportunities

| Contract | Rate | Ann. | Basis | Depth | Strategy |
|----------|------|------|-------|-------|----------|
| DOGE_USDT | +0.15% | 164% | +0.3% | OK | Long basis |
| PEPE_USDT | +0.12% | 131% | +0.2% | Fair | Long basis |
| WIF_USDT | -0.10% | 109% | -0.1% | OK | Short basis |

### Strategy

**Long basis**: Short futures + long spot  
**Short basis**: Long futures + short spot (borrow)

⚠️ Risk: Actual PnL must account for fees and execution.
```

---

### Scenario 4.2: Extreme funding query

**Context**: User wants coins with extreme funding rates.

**Prompt examples**:
- "Which coins have extreme funding?"
- "哪些币费率异常"

**Expected behavior**:
1. Call `list_futures_tickers`(settle=usdt); filter |funding_rate| > 0.001 (0.1%).
2. Sort by |rate|; label severity (e.g. extreme positive, high negative).
3. Output "Extreme funding" table (contract, rate, status).

**Output**:
```markdown
## Extreme Funding

| Contract | Rate | Status |
|----------|------|--------|
| DOGE_USDT | +0.18% | Extreme positive |
| SHIB_USDT | +0.15% | High positive |
| WIF_USDT | -0.12% | High negative |

Positive rate > 0.1% means high cost to long; may signal short-term pullback risk.
```

---

## Case 5: Basis (Spot vs Futures) Monitoring

### MCP Call Spec (document-aligned)

**Trigger**: "What is the basis?", "Spot–futures spread." For basis monitoring, **call in this order**.

| Step | MCP Tool | Parameters | Required Fields |
|------|----------|------------|----------------|
| 1 | `list_tickers` (spot) | `currency_pair={BASE}_USDT` | Spot `last` |
| 2 | `list_futures_tickers` | `settle=usdt`, optional `contract={BASE}_USDT` | Futures price, mark_price, index_price |
| 3 | `list_futures_premium_index` or equivalent | `settle=usdt`, `contract={BASE}_USDT` | premium_index; if history available, for mean and deviation |

**Calculation & judgment** (aligned with SKILL):

- **Current basis vs historical mean** (deviation).
- **Basis widening / narrowing** (widening → sentiment heating; narrowing → mean reversion).

**Output**: Must include "Basis data" table, current vs historical mean, widening/narrowing conclusion, and short recommendation.

---

### Scenario 5.1: Single-coin basis query

**Context**: User asks for BTC spot–futures spread.

**Prompt examples**:
- "What is BTC basis?"
- "BTC基差怎么样"

**Expected behavior**:
1. Call per **MCP Call Spec**: `list_tickers`(BTC_USDT) → `list_futures_tickers`(usdt, BTC_USDT) → optional `list_futures_premium_index`.
2. Compute basis, basis rate; if premium history available, historical mean.
3. Output basis table + analysis + recommendation per Report Template.

**Output**:
```markdown
## BTC Spot–Futures Basis

### Basis data

| Metric | Value |
|--------|-------|
| Spot | $63,500 |
| Futures | $63,700 |
| Basis | +$200 |
| Basis rate | +0.31% |
| Historical mean | +0.15% |

### Analysis

Current basis rate 0.31%, above historical mean 0.15%; **elevated positive basis**. Possible reasons: strong bullish sentiment; suitable for long-basis arbitrage.
```

---

### Scenario 5.2: Negative basis warning

**Context**: User queries ETH basis.

**Prompt examples**:
- "ETH spot–futures spread"
- "ETH期现价差"

**Expected behavior**:
1. Call per **MCP Call Spec**: `list_tickers`(ETH_USDT) → `list_futures_tickers`(usdt, ETH_USDT).
2. Compute basis and basis rate; if negative, output basis table + ⚠️ negative basis warning (bearish / short crowding).

**Output**:
```markdown
## ETH Spot–Futures Basis

### Basis data

| Metric | Value |
|--------|-------|
| Spot | $3,200 |
| Futures | $3,185 |
| Basis | -$15 |
| Basis rate | -0.47% |

### Notice

Currently **negative basis** (futures below spot), which often indicates:
- Bearish sentiment
- Or short crowding
```

---

## Case 6: Manipulation Risk Analysis (Is the coin easy to manipulate?)

### MCP Call Spec (document-aligned)

**Trigger**: "这个币深度和成交比怎么样" / "容易操控吗" / "How is this coin’s depth vs volume?" / "Is it easy to manipulate?"

**API choice**: When user mentions **perpetual, contract, futures** (永续、合约), use **futures** tools; otherwise use **spot** tools.

| Step | MCP Tool (spot) | MCP Tool (futures, when user says perpetual/contract) | Parameters | Required Fields |
|------|-----------------|--------------------------------------------------------|------------|----------------|
| 1 | `list_order_book` | `list_futures_order_book` | Spot: `currency_pair={BASE}_USDT`. Futures: `settle=usdt`, `contract={BASE}_USDT`. `limit=20` | Top 10 bid depth sum, top 10 ask depth sum |
| 2 | `list_tickers` | `list_futures_tickers` | Same pair / contract + settle | 24h quote volume (quoteVolume) |
| 3 | `list_trades` | `list_futures_trades` or equivalent | Same pair; `limit=500` (or 24h window) | Trade size distribution; consecutive same-direction large orders |

**Calculation & judgment** (aligned with SKILL):

- **Top 10 depth total / 24h volume < 0.5%** → "thin depth" (深度薄).
- **24h trades have consecutive same-direction large orders** → "possible manipulation / 可能有主力在控盘".

**Output**: Must include "Depth analysis" table (top 10 depth, 24h volume, depth ratio, assessment), "Large order" summary, and "Manipulation risk" conclusion.

---

### Scenario 6.1: Manipulation risk query

**Context**: User is concerned about small-cap coin manipulation.

**Prompt examples**:
- "Is PEPE easy to manipulate?"
- "PEPE这个币容易被操控吗"

**Expected behavior**:
1. Call per **MCP Call Spec**: `list_order_book`(PEPE_USDT) → `list_tickers` → `list_trades`(limit=500).
2. Compute depth ratio; from trades identify large and consecutive same-side.
3. Output depth table + large order summary + risk conclusion per Report Template.

**Output**:
```markdown
## PEPE Manipulation Risk

### Depth analysis

| Metric | Value | Assessment |
|--------|-------|------------|
| Top 10 depth | $850K | - |
| 24h volume | $320M | - |
| Depth ratio | 0.27% | Thin |

### Large orders

In last 500 trades:
- 3 consecutive large buys (15% of sample)
- Max single: $125K

### Risk conclusion

**Manipulation risk**: High

- Depth ratio < 0.5% implies small size can move price
- Consecutive same-side large orders suggest possible manipulation
```

---

### Scenario 6.2: Healthy pair (low risk)

**Context**: User queries a major pair (e.g. BTC).

**Prompt examples**:
- "How is BTC depth vs volume?"
- "BTC深度成交比怎么样"

**Expected behavior**:
1. Call per **MCP Call Spec**: `list_order_book`(BTC_USDT) → `list_tickers` → optional `list_trades`.
2. Compute depth ratio; if > 2% assess as good depth, low manipulation risk.
3. Output depth table + risk conclusion (low).

**Output**:
```markdown
## BTC Manipulation Risk

### Depth analysis

| Metric | Value | Assessment |
|--------|-------|------------|
| Top 10 depth | $85M | - |
| 24h volume | $2.1B | - |
| Depth ratio | 4.0% | Good |

### Risk conclusion

**Manipulation risk**: Low

BTC has ample depth; large size would be needed to move price; manipulation risk is low.
```

---

### Scenario 6.3: Futures manipulation risk (perpetual/contract)

**Context**: User asks about manipulation for a **perpetual/contract** (e.g. "BTC contract easy to manipulate?").

**Prompt examples**:
- "BTC永续容易操控吗"
- "ETH合约深度和成交比怎么样"

**Expected behavior**:
1. Detect "永续" or "合约" (or "perpetual"/"contract") and use **futures** MCP: `list_futures_order_book`(`settle=usdt`, `contract=BTC_USDT`, `limit=20`) → `list_futures_tickers` → `list_futures_trades` (or equivalent, limit=500).
2. Extract top 10 depth total and 24h volume; from futures trades detect consecutive same-direction large orders.
3. Apply same judgment: depth ratio < 0.5% → thin; consecutive same-side large → possible manipulation.
4. Output depth analysis table + large order summary + manipulation risk conclusion (same structure as 6.1/6.2, data from futures).

**Output**: Same structure as Scenario 6.1 or 6.2; data source is futures order book, tickers, and trades.

---

## Case 7: Order Book Explainer

### MCP Call Spec (document-aligned)

**Trigger**: "Explain the order book", "What is the order book?", "How to read the book?" For order book explainer, **call in this order**.

| Step | MCP Tool | Parameters | Required Fields |
|------|----------|------------|----------------|
| 1 | `list_order_book` (spot/futures) | `currency_pair` or `contract`+`settle`, `limit=10` | bids/asks sample (price and size per level) |
| 2 | `list_tickers` (same market) | Same pair | `last` for spread explanation |

**Interpretation** (aligned with SKILL):

- Show sample bids/asks (levels and sizes).
- Explain **spread** (bid–ask) using ticker last.
- Fast moves + deep depth → good liquidity.

**Output**: Must include order book tutorial, live order book example, key metrics (best bid, best ask, spread), and short takeaways.

---

### Scenario 7.1: Beginner explainer

**Context**: User is new and needs a tutorial.

**Prompt examples**:
- "Explain the order book"
- "帮我解释一下订单簿"

**Expected behavior**:
1. Call per **MCP Call Spec**: `list_order_book` (e.g. BTC_USDT, limit=10) → `list_tickers`.
2. Fill order book table and key metrics with live data; add tutorial text (Bids/Asks/Spread, what spread means).
3. Output tutorial + live example + takeaways.

**Output**:
```markdown
## Order Book Explained

### What is the order book

The order book is the exchange’s "list of orders":

- **Asks**: Sell orders, sorted by price low to high
- **Bids**: Buy orders, sorted by price high to low
- **Spread**: Gap between best ask and best bid

### Live example (BTC)

**Asks** ↑
| Price | Size | Cumulative |
|-------|------|------------|
| 63,550 | 2.5 | 7.8 |
| 63,530 | 1.8 | 5.3 |
| 63,510 | 3.5 | 3.5 | ← Best ask

------- Last: 63,505 -------

**Bids** ↓
| Price | Size | Cumulative |
|-------|------|------------|
| 63,500 | 4.2 | 4.2 | ← Best bid
| 63,480 | 2.1 | 6.3 |
| 63,460 | 3.0 | 9.3 |

### Takeaways

- **Spread** = 63,510 − 63,500 = $10 (0.016%)
- Tighter spread → better liquidity
- Deeper book → less impact from large orders
```

---

### Scenario 7.2: Specific pair order book

**Context**: User wants to see a specific pair’s book (e.g. ETH).

**Prompt examples**:
- "Show ETH order book"
- "看下ETH的盘口"

**Expected behavior**:
1. Call per **MCP Call Spec**: `list_order_book`(ETH_USDT, limit=10) → `list_tickers`(ETH_USDT).
2. Output ETH live table (asks/bids, price, size, cumulative) + last + spread and short comment (e.g. liquidity, support).

**Output**:
```markdown
## ETH Order Book

**Asks**
| Price | Size | Cumulative |
|-------|------|------------|
| 3,205 | 45 | 120 |
| 3,203 | 32 | 75 |
| 3,201 | 43 | 43 | ← Best ask

--- Last: 3,200 ---

**Bids**
| Price | Size | Cumulative |
|-------|------|------------|
| 3,200 | 55 | 55 | ← Best bid
| 3,198 | 28 | 83 |
| 3,196 | 40 | 123 |

Spread: $1 (0.03%) — liquidity good. Bid depth heavier than asks; support below is stronger.
```
