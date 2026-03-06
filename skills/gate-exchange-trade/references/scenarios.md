# Gate Trading Intelligence — Scenarios & Prompt Examples

---

## Part 1: Basis Monitor Scenarios

### Scenario 1: Single-Coin Basis Check

**Context**: User wants to quickly check the current basis status of a specific coin.

**Prompt Examples**:
- "how is BTC basis?"
- "check ETH spot-futures spread"
- "is SOL futures at premium or discount now?"
- "What's the current BTC basis?"

**Expected Behavior**:
1. Fetch spot price via `get_spot_tickers(currency_pair="BTC_USDT")`
2. Fetch futures price via `get_futures_tickers(settle="usdt", contract="BTC_USDT")`
3. Calculate basis and basis rate
4. Fetch premium index history for trend context
5. Output single-coin report

---

### Scenario 2: Full-Market Basis Scan

**Context**: User wants to scan the entire market for coins with unusual basis levels.

**Prompt Examples**:
- "full-market basis scan"
- "which coins have large spot-futures spreads?"
- "help me find coins with abnormal basis"
- "Scan all coins for extreme basis"

**Expected Behavior**:
1. Fetch all spot tickers and all futures tickers
2. Match spot-futures pairs and calculate basis for each
3. Rank by |basis_rate| descending
4. Show Top 10 positive and Top 10 negative basis coins
5. Only fetch premium index history for top anomalies (top 5 by |basis_rate|)

---

### Scenario 3: Arbitrage Opportunity Assessment

**Context**: User is interested in basis-based arbitrage and wants to evaluate whether the current basis provides a tradeable opportunity.

**Prompt Examples**:
- "is BTC basis arbitrage tradable now?"
- "are there cash-and-carry opportunities?"
- "what is ETH carry annualized return roughly?"
- "Is there a cash-and-carry opportunity on BTC right now?"

**Expected Behavior**:
1. Run full single-coin basis analysis
2. Emphasize the arbitrage section in the report
3. Calculate annualized return based on current basis
4. Cross-reference with funding rate for complete cost picture
5. Provide practical execution guidance (direction, costs, risks)

---

### Scenario 4: Basis Trend Monitoring

**Context**: User wants to understand how the basis has been changing over time, not just the current snapshot.

**Prompt Examples**:
- "is BTC basis widening or narrowing recently?"
- "how is ETH spot-futures spread trend?"
- "is SOL basis showing mean-reversion signs?"
- "Show me the BTC basis trend over the past week"

**Expected Behavior**:
1. Fetch premium index history with `interval=1h`, `limit=168` (7 days)
2. Calculate 24h average vs 7-day average for trend direction
3. Calculate Z-score for deviation assessment
4. Present trend visualization description (widening/narrowing/stable)

---

### Scenario 5: Multi-Coin Comparative Basis

**Context**: User wants to compare the basis of several specific coins side by side.

**Prompt Examples**:
- "compare basis for BTC, ETH, and SOL"
- "what are spot-futures spreads for major coins?"
- "Compare basis for BTC ETH SOL DOGE"

**Expected Behavior**:
1. Fetch spot and futures data for each specified coin
2. Calculate basis for each
3. Present in a comparative table
4. Highlight which coin has the most extreme basis
5. Add brief context for each (trend direction, Z-score if available)

---

## Part 2: Funding Rate Arbitrage Scenarios

### Scenario 6: Full-Market Arbitrage Scan

**Context**: User wants to scan all contracts for the best funding rate arbitrage opportunities.

**Prompt Examples**:
- "are there arbitrage opportunities now?"
- "funding-rate arbitrage scan"
- "help me find funding arbitrage opportunities"
- "Scan for funding rate arbitrage opportunities"

**Expected Behavior**:
1. Fetch all futures tickers, pre-filter by volume > $10M
2. Fetch funding rates for candidates, filter by |rate| > 0.05%
3. Fetch spot prices for basis calculation
4. Check order book depth for execution feasibility
5. Rank by estimated annualized return
6. Present structured arbitrage report with Top-N opportunities

---

### Scenario 7: Extreme Funding Rate Discovery

**Context**: User wants to find coins with abnormally high or low funding rates, not necessarily for arbitrage.

**Prompt Examples**:
- "which coinsabnormal funding rate？"
- "coins with highest funding rates"
- "any coins with large negative funding rates?"
- "Which coins have extreme funding rates?"

**Expected Behavior**:
1. Fetch all futures tickers
2. Fetch funding rates, sort by |rate| descending
3. Present both extreme positive and extreme negative rates
4. Add context: what high/low rates imply about market positioning
5. Flag any rate that's been consistently extreme (not a one-time spike)

---

### Scenario 8: Single-Coin Arbitrage Assessment

**Context**: User wants to evaluate whether a specific coin presents an arbitrage opportunity.

**Prompt Examples**:
- "is BTC funding-rate arbitrage tradable?"
- "what is ETH funding-rate arbitrage return roughly?"
- "is arbitrage in SOL worth it now?"
- "Is BTC funding rate arbitrage worth it right now?"

**Expected Behavior**:
1. Fetch the specific contract's funding rate history
2. Calculate annualized return estimate
3. Fetch spot price and compute basis spread
4. Check order book depth for execution feasibility
5. Provide specific guidance: direction, estimated return, risks, costs

---

### Scenario 9: Arbitrage Risk Evaluation

**Context**: User is considering executing an arbitrage but wants to understand the risks first.

**Prompt Examples**:
- "what are risks of funding arbitrage?"
- "what should I watch when doing ETH arbitrage?"
- "can funding rate suddenly reverse?"
- "What are the risks of funding rate arbitrage on BTC?"

**Expected Behavior**:
1. Fetch recent funding rate history to assess stability and trend
2. Check if rate has been volatile or stable
3. Evaluate liquidity and depth on both spot and futures
4. Present risk factors: rate reversal risk, slippage, margin requirements, execution costs
5. Include historical rate volatility context

---

### Scenario 10: Directional Rate Analysis

**Context**: User wants to understand the funding rate direction and what it implies about market sentiment.

**Prompt Examples**:
- "are funding rates mostly positive or negative?"
- "how are overall market funding rates?"
- "how is funding rate distribution?"
- "What's the overall funding rate sentiment across the market?"

**Expected Behavior**:
1. Fetch all futures tickers
2. Fetch funding rates for major contracts
3. Compute distribution: how many positive vs negative rates
4. Calculate average rate across the market
5. Interpret: overall market positioning (net long vs net short bias)

---

## Part 3: Liquidation Monitor Scenarios

### Scenario 11: Market-Wide Liquidation Overview

**Context**: User wants a broad picture of liquidation activity across the entire futures market.

**Prompt Examples**:
- "how are recent liquidations?"
- "full-market liquidation data"
- "how much was liquidated today?"
- "Give me the overall liquidation summary"

**Expected Behavior**:
1. Fetch recent liquidation orders via `list_futures_liq_orders(settle="usdt", limit=100)`
2. Aggregate by contract, compute totals
3. Show global overview: total liquidation value, long/short breakdown
4. Highlight any contracts with abnormal liquidation activity
5. Provide market-level interpretation

---

### Scenario 12: Single-Coin Liquidation Analysis

**Context**: User is interested in liquidation events for a specific coin.

**Prompt Examples**:
- "how are BTC liquidations?"
- "how much ETH got liquidated recently?"
- "check SOL liquidation data"
- "How much BTC got liquidated today?"

**Expected Behavior**:
1. Fetch liquidation orders filtered by contract
2. Get price context via candlestick data
3. Get current market state via futures tickers
4. Analyze directional breakdown (long vs short liquidations)
5. Check for pin-bar events and price recovery
6. Present focused single-coin liquidation report

---

### Scenario 13: Liquidation Spike Alert

**Context**: User suspects or has heard about a major liquidation event and wants details.

**Prompt Examples**:
- "was there a large liquidation event just now?"
- "which coins have abnormal liquidation?"
- "which coin had the most liquidations?"
- "Which coins had abnormal liquidations recently?"

**Expected Behavior**:
1. Fetch all recent liquidation orders
2. Apply the 3x daily average threshold to detect spikes
3. For each anomalous contract, fetch price and market data
4. Flag all triggered conditions (abnormal liquidation, Long Squeeze / Short Squeeze, wick event)
5. Sort anomalous contracts by liquidation volume

---

### Scenario 14: Directional Squeeze Detection

**Context**: User wants to know if one side (longs or shorts) is getting disproportionately liquidated.

**Prompt Examples**:
- "were longs squeezed?"
- "were short or long liquidations larger?"
- "Is there a short squeeze happening?"
- "which coins have longs being squeezed?"

**Expected Behavior**:
1. Fetch liquidation data
2. Calculate long/short liquidation percentages per contract
3. Apply 80% threshold to detect directional squeezes
4. Present directional breakdown with price context
5. Explain implications of the squeeze direction

---

### Scenario 15: Pin-Bar / Wick Event Investigation

**Context**: User saw a sudden price spike and wants to know if it was a liquidation-driven wick event.

**Prompt Examples**:
- "did BTC just have a wick event?"
- "are there wick events?"
- "SOL flash-crashed and rebounded; how much got liquidated?"
- "Was that BTC move a liquidation wick?"

**Expected Behavior**:
1. Fetch liquidation data around the event time
2. Fetch candlestick data to identify the wick candle
3. Calculate wick ratio and price recovery percentage
4. Determine if it qualifies as a pin-bar event (>50% recovery)
5. Present chronological cascade analysis if applicable
