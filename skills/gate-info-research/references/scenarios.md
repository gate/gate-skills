# gate-info-research — Scenarios & Prompt Examples

## Scenario 1: Daily Market Briefing (High Complexity)

**Context**: User requests a comprehensive daily market briefing covering price overview, DeFi, events, and sentiment. Activates S1 + S4 + S3(BTC). Multi-phase serial execution.

**Prompt Examples**:
- "Give me a daily market briefing with price overview, hot sectors, and tomorrow's outlook"
- "What's happening in the crypto market today?"
- "Market summary please — include major events and sentiment"

**Expected Behavior**:
1. Activate signals S1 (Market/Macro) + S4 (News/Sentiment). If user mentions trend/outlook, also activate S3 for BTC.
2. Phase 1 (parallel): Call `info_marketsnapshot_get_market_snapshot`(BTC), `info_marketsnapshot_get_market_snapshot`(ETH), `info_platformmetrics_get_defi_overview`, `news_events_get_latest_events`(24h, 10), `news_feed_search_news`(importance, 10).
3. Phase 2 (parallel): Call `news_feed_get_social_sentiment`().
4. Phase 3 (parallel, if S3 activated): Call `info_markettrend_get_kline`(BTC, 1d, 90), `info_markettrend_get_technical_analysis`(BTC).
5. LLM aggregates all tool results into Template A (Market Overview Brief) with price snapshot, DeFi overview, key events, sentiment, and outlook.
6. Output includes data timestamps and disclaimer.

## Scenario 2: Single-Coin Deep Dive (Medium Complexity)

**Context**: User wants a full research report on one specific coin. Activates S2 + S3 + S4 + S5. All tools in one parallel Phase.

**Prompt Examples**:
- "Give me a weekend research report on XRP — price, news, and risk"
- "Analyze SOL — fundamentals, technicals, and sentiment"
- "Full analysis of ETH please"

**Expected Behavior**:
1. Extract symbol (e.g., XRP). Activate all signals: S2 (fundamentals) + S3 (technicals) + S4 (news/sentiment) + S5 (risk).
2. Phase 1 (all parallel): Call `info_coin_get_coin_info`(XRP), `info_marketsnapshot_get_market_snapshot`(XRP), `info_markettrend_get_technical_analysis`(XRP), `info_markettrend_get_kline`(XRP, 1d, 90), `info_markettrend_get_indicator_history`(XRP), `news_feed_search_news`(XRP, 5), `news_feed_get_social_sentiment`(XRP), `news_events_get_latest_events`(XRP, 7d), `info_compliance_check_token_security`(XRP).
3. LLM aggregates into Template B (Single-Coin Deep Dive) with fundamentals, technicals, news, risk alerts, and overall assessment.
4. Output includes data timestamps and disclaimer.

## Scenario 3: Token Risk Check (Low Complexity)

**Context**: User wants to check whether a token is safe. Activates S5 + S2. Simple parallel execution.

**Prompt Examples**:
- "Is ADA safe? Check the token risk"
- "Run a security check on LINK"
- "Is this coin a honeypot? Check SHIB"

**Expected Behavior**:
1. Extract symbol (e.g., ADA). Activate S5 (Security/Risk) + S2 (Fundamentals for cross-check).
2. Phase 1 (all parallel): Call `info_compliance_check_token_security`(ADA, chain=eth), `info_coin_get_coin_info`(ADA), `info_marketsnapshot_get_market_snapshot`(ADA), `info_markettrend_get_technical_analysis`(ADA).
3. LLM aggregates into Template E (Risk Check) with contract audit results, fundamentals cross-check, and risk summary.
4. Output includes data timestamps and disclaimer.

## Scenario 4: Multi-Coin Comparison (Medium Complexity)

**Context**: User wants to compare multiple coins for long-term holding. Activates S2 x N with optional S3 and S5.

**Prompt Examples**:
- "Compare BTC, ETH, and SOL — which one should I hold long term?"
- "Side-by-side comparison of AVAX and MATIC"
- "Which is better, BNB or SOL? Compare fundamentals and risk"

**Expected Behavior**:
1. Extract symbols (e.g., [BTC, ETH, SOL]). Activate S2 x 3 (fundamentals). If user mentions risk, also activate S5 x 3.
2. Phase 1 (all parallel): For each coin, call `info_marketsnapshot_get_market_snapshot`({coin}), `info_coin_get_coin_info`({coin}). Optionally `info_markettrend_get_technical_analysis`({coin}) and `info_compliance_check_token_security`({coin}).
3. LLM aggregates into Template C (Multi-Coin Comparison) with comparison table, per-coin highlights, and comparative assessment.
4. Output includes data timestamps and disclaimer.

## Scenario 5: Technical Trend + Sentiment (Medium Complexity)

**Context**: User asks about support/resistance levels combined with news outlook. Activates S3 + S4.

**Prompt Examples**:
- "What are DOT's support and resistance levels? Also check the latest news"
- "Show me BTC technical analysis with sentiment"
- "Is ETH oversold? What does the news say?"

**Expected Behavior**:
1. Extract symbol (e.g., DOT). Activate S3 (Technicals) + S4 (News/Sentiment).
2. Phase 1 (all parallel): Call `info_markettrend_get_kline`(DOT, 1d, 90), `info_markettrend_get_indicator_history`(DOT), `info_markettrend_get_technical_analysis`(DOT), `info_marketsnapshot_get_market_snapshot`(DOT), `news_events_get_latest_events`(DOT, 24h), `news_feed_search_news`(DOT, 5), `news_feed_get_social_sentiment`(DOT).
3. LLM aggregates into a combined report with technical analysis (support/resistance, RSI, MACD) and news/sentiment outlook.
4. Output includes data timestamps and disclaimer.

## Scenario 6: Event Attribution — Why Did the Market Crash? (Medium-High Complexity)

**Context**: User asks about the cause of a recent market movement. Activates S4 + S1. Involves conditional branching.

**Prompt Examples**:
- "Why did the market crash yesterday?"
- "What caused BTC to dump?"
- "Market dropped 10% — what happened?"

**Expected Behavior**:
1. Activate S4 (News/Sentiment/Attribution) + S1 (Market/Macro).
2. Phase 1 (parallel): Call `news_events_get_latest_events`(24h, 10), `info_marketsnapshot_get_market_snapshot`(BTC, 1d).
3. LLM examines Phase 1: Are there matching events?
4. Phase 2a (if events found, parallel): Call `news_events_get_event_detail`({event_id}), `info_onchain_get_token_onchain`(BTC).
5. Phase 2b (if no events, parallel): Call `news_feed_search_news`(sort_by=time, 15), `info_onchain_get_token_onchain`(BTC).
6. Phase 3 (parallel): Call `news_feed_get_social_sentiment`(), `info_marketsnapshot_get_market_snapshot`(BTC).
7. LLM aggregates into Template D (Event Attribution) with root cause analysis, on-chain evidence, sentiment recovery assessment.
8. Output includes data timestamps and disclaimer.

## Scenario 7: Screening Mode — Oversold Coins (High Complexity)

**Context**: User wants to find oversold coins and analyze the top picks. Involves screening mode with P1 -> P2 serial dependency.

**Prompt Examples**:
- "Which coins are oversold right now? Pick 2 and analyze them"
- "Find the top 5 gainers today and analyze the best one"
- "Which DeFi coins are worth looking at? Screen and deep dive"

**Expected Behavior**:
1. No symbols provided + screening keywords detected. Enter screening mode.
2. Phase 1 (S1, parallel): Call `info_marketsnapshot_get_market_snapshot` for BTC, ETH, SOL, AVAX, DOGE, MATIC, ADA, DOT (or top coins by volume).
3. LLM intermediate aggregation: Rank by 24h change + RSI, extract top oversold candidates {sym1}, {sym2}.
4. Phase 2 (S2 + S3, parallel per coin): Call `info_markettrend_get_kline`({sym}, 1d, 90), `info_markettrend_get_indicator_history`({sym}), `info_markettrend_get_technical_analysis`({sym}), `info_coin_get_coin_info`({sym}).
5. LLM aggregates into a screening report: ranking table + deep dive on selected coins.
6. Output includes data timestamps and disclaimer.

## Scenario 8: DeFi Sector Analysis (Medium Complexity)

**Context**: User asks about a specific sector (DeFi) and wants to know why it is moving and which coins lead.

**Prompt Examples**:
- "Why is DeFi pumping recently? Analyze the leading coins"
- "Give me a DeFi sector overview and the top project"
- "What's driving the Layer 2 sector?"

**Expected Behavior**:
1. Extract sector = DeFi. Activate S1 (macro/sector) + S4 (event/attribution). Screening mode for sector leaders.
2. Phase 1 (parallel): Call `info_platformmetrics_get_defi_overview`, `info_marketsnapshot_get_market_snapshot`(UNI), `info_marketsnapshot_get_market_snapshot`(AAVE), `info_marketsnapshot_get_market_snapshot`(LINK), `news_events_get_latest_events`(24h).
3. LLM identifies sector leader {symbol} + event attribution.
4. Phase 2 (S2 + S3, parallel): Call `info_coin_get_coin_info`({symbol}), `info_markettrend_get_kline`({symbol}, 1d), `info_markettrend_get_indicator_history`({symbol}), `info_markettrend_get_technical_analysis`({symbol}).
5. LLM aggregates sector overview + leader deep dive.
6. Output includes data timestamps and disclaimer.

## Scenario 9: Route Away — Execution Intent (Boundary)

**Context**: User clearly wants to execute a trade, not research. This Skill should NOT activate.

**Prompt Examples**:
- "Buy 1 BTC for me"
- "Swap my USDT to ETH"
- "Open a 10x long on SOL futures"

**Expected Behavior**:
1. Detect execution intent (buy/sell/swap/open position). Do NOT activate this Skill.
2. Route to the appropriate trading skill: `gate-exchange-spot`, `gate-exchange-futures`, or `gate-exchange-flashswap`.
3. Do NOT call any of the 12 research tools.
