# Gate Market Intelligence — Scenarios & Prompt Examples

---

## Part 1: Coin Deep Analysis Scenarios

### Scenario 1: Standard Coin Analysis

**Context**: User wants a comprehensive analysis of a specific cryptocurrency.

**Prompt Examples**:
- "帮我分析一下 BTC"
- "分析 ETH"
- "SOL 深度分析"
- "Analyze BTC for me"

**Expected Behavior**:
1. Execute full 6-step data pipeline (currency → pair → candlesticks → order book → trades → funding rate)
2. Apply all three judgment checks (多头拥挤, 卖压较重, 异常放量)
3. Generate complete structured report covering all six sections
4. Include risk flags and overall summary

---

### Scenario 2: Quick Coin Assessment

**Context**: User wants a brief opinion on whether a coin is worth looking at, not a full deep dive.

**Prompt Examples**:
- "DOGE 怎么样？"
- "看看 PEPE"
- "XRP 值得买吗？"
- "What do you think about SOL?"

**Expected Behavior**:
1. Run the same data pipeline but present a condensed summary
2. Focus on key metrics: price trend, volume, risk flags
3. Provide a brief verdict at the end
4. Offer to run full deep analysis if the user wants more detail

---

### Scenario 3: Altcoin / Small-Cap Analysis

**Context**: User asks about a less well-known coin that may not have a futures contract.

**Prompt Examples**:
- "帮我看看 PEPE2"
- "分析一下 FLOKI"
- "这个新币 XXX 怎么样？"
- "Analyze this small-cap token: ARB"

**Expected Behavior**:
1. Attempt all 6 steps; gracefully handle if futures contract doesn't exist
2. Skip funding rate section with a note
3. Pay extra attention to liquidity (order book depth, spread)
4. Flag low-liquidity concerns if applicable
5. Note the absence of futures data as a limitation

---

### Scenario 4: Pre-Trade Analysis

**Context**: User is considering a trade and wants data-driven input before deciding.

**Prompt Examples**:
- "我想做多 ETH，帮我看看"
- "BTC 能不能做空？"
- "现在买 SOL 合适吗？"
- "Should I long BTC here?"

**Expected Behavior**:
1. Run full analysis pipeline
2. Emphasize relevant risk flags for the intended direction
3. Highlight support/resistance levels relevant to the trade
4. Note funding rate cost if the user plans to use futures
5. Remind: analysis is data-based, not investment advice

---

### Scenario 5: Comparative Analysis

**Context**: User wants to compare two or more coins to decide which to focus on.

**Prompt Examples**:
- "BTC 和 ETH 哪个更值得关注？"
- "对比一下 SOL 和 AVAX"
- "Compare BTC vs ETH"

**Expected Behavior**:
1. Run the analysis pipeline for each coin
2. Present key metrics side by side in a comparison table
3. Highlight differences in trend, volume, sentiment, risk
4. Provide a comparative verdict (which one looks stronger on data)

---

### Scenario 6: Anomaly Investigation

**Context**: User notices something unusual and wants to understand what's happening with a coin.

**Prompt Examples**:
- "BTC 今天怎么突然放量了？"
- "ETH 为什么跌了？帮我看看"
- "DOGE 异动分析"
- "BTC volume spiked, what's going on?"

**Expected Behavior**:
1. Run full analysis with emphasis on recent data
2. Focus on volume analysis and recent trade patterns
3. Check for whale activity in recent trades
4. Cross-reference with funding rate for sentiment shifts
5. Present findings in a "what happened" narrative format

---

## Part 2: Multi-Coin Screener Scenarios

### Scenario 7: Top Gainers / Losers

**Context**: User wants to find the biggest movers in the market.

**Prompt Examples**:
- "今天涨幅最大的币有哪些？"
- "找出24h涨幅超过10%的币"
- "哪些币跌得最多？"
- "Top 20 gainers today"
- "Show me coins that dropped more than 5%"

**Expected Behavior**:
1. Fetch all spot tickers
2. Filter `_USDT` pairs, exclude stablecoins
3. Apply change_percentage threshold
4. Sort by change_percentage desc (gainers) or asc (losers)
5. Return Top N results with price, change%, volume

---

### Scenario 8: Volume-Based Screening

**Context**: User wants to find coins with the highest trading activity.

**Prompt Examples**:
- "成交量最大的20个币"
- "哪些币今天放量了？"
- "成交额超过1亿美元的币"
- "Find coins with volume over $100M"

**Expected Behavior**:
1. Fetch all spot tickers
2. Filter by quote_volume threshold
3. Sort by quote_volume descending
4. Show volume alongside price and change data

---

### Scenario 9: Funding Rate Screening

**Context**: User wants to find coins with extreme funding rates across the futures market.

**Prompt Examples**:
- "费率最高的币有哪些？"
- "哪些币的资金费率超过0.1%？"
- "找出负费率的币"
- "Which coins have the highest funding rates?"

**Expected Behavior**:
1. Fetch all futures tickers
2. For candidates, fetch funding rate via `get_futures_funding_rate`
3. Filter by |funding_rate| threshold
4. Sort by rate descending
5. Include rate direction (多头付费 / 空头付费) in output

---

### Scenario 10: Composite Conditions

**Context**: User applies multiple criteria simultaneously to find coins matching a complex profile.

**Prompt Examples**:
- "跌了很多但量很大的币"
- "价格低于1美元且涨幅超过5%的币"
- "找出放量上涨的币"
- "Coins under $1 with >10% gain and >$10M volume"

**Expected Behavior**:
1. Parse all conditions from user query
2. Fetch spot (and futures if needed) data
3. Apply all filters as AND conditions
4. Sort by user's preferred metric or default to volume
5. Clearly state the applied criteria in the report header

---

### Scenario 11: Sector / Pattern Discovery

**Context**: User wants to identify market-wide patterns or sector trends from screening results.

**Prompt Examples**:
- "今天哪个板块涨得多？"
- "AI 概念币表现怎么样？"
- "有没有集体异动的板块？"
- "Are there any sector-wide moves today?"

**Expected Behavior**:
1. Fetch all tickers, apply broad filter (e.g., change > 5%)
2. Group results by sector/category if recognizable
3. Highlight concentration patterns in the data highlights section
4. Note if results are spread across sectors or concentrated

---

### Scenario 12: Vague / Broad Queries

**Context**: User gives an imprecise query that requires reasonable default thresholds.

**Prompt Examples**:
- "帮我找找有意思的币"
- "有什么值得关注的？"
- "最近有什么异动？"
- "Anything interesting in the market?"

**Expected Behavior**:
1. Apply sensible defaults: change > 5% OR volume spike > 2x
2. Explain chosen thresholds to the user
3. Show a mix of gainers, volume spikes, and notable movers
4. Suggest the user can refine with more specific criteria
