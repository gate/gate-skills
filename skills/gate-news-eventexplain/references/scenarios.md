# gate-news-eventexplain — Scenarios & Prompt Examples

## Scenario 1: Why did a coin dump (English)

**Context**: User asks why BTC or another coin crashed.

**Prompt Examples**:
- "Why did BTC crash"
- "What caused the ETH drop"
- "Why is SOL dumping"

**Expected Behavior**:
1. Extract coin (e.g. BTC), direction (down), time_hint (default 24h). Call in parallel: `news_events_get_latest_events`(coin=BTC, time_range=24h), `info_marketsnapshot_get_market_snapshot`(symbol=BTC, scope=full).
2. If a matching event is found (event time before move), call `news_events_get_event_detail` and `info_onchain_get_token_onchain` in parallel; else call `news_feed_search_news` and `info_onchain_get_token_onchain`.
3. Output **attribution report**: Volatility Summary, Core Triggering Event, Event→Impact Chain, On-chain Verification, Ripple Effects, Forward Outlook. Use "likely caused by" language; no definitive causal claims.

## Scenario 2: Why did a coin pump (Chinese)

**Context**: User asks why a coin surged.

**Prompt Examples**:
- "Why did ETH pump"
- "Why is SOL pumping"

**Expected Behavior**:
1. Extract coin, direction (up). Same two-phase workflow as Scenario 1.
2. Return structured attribution analysis; if no clear event, use "No event identified" template with possible factors and composite assessment.

## Scenario 3: No clear event found

**Context**: Events and news do not yield a single clear trigger.

**Prompt Examples**:
- "Why did PEPE move so much today"

**Expected Behavior**:
1. After Phase 1 and Step 4b, if no event aligns temporally, LLM produces **Possible Cause Analysis** with multiple factors and likelihoods, plus On-chain Clues and Composite Assessment.
2. Explicitly state "No single clear triggering event was found"; do not fabricate a cause.

## Scenario 4: General news (route away)

**Context**: User asks for recent news without asking why a move happened.

**Prompt Examples**:
- "Any recent news"
- "What happened in crypto today"

**Expected Behavior**:
1. Route to **gate-news-briefing**; do not run event-attribution workflow.
2. Do not call eventexplain tools.
