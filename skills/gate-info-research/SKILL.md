---
name: gate-info-research
version: "2026.3.23-1"
updated: "2026-03-23"
description: "Market Research Copilot (L2): multi-dimension briefs across Gate Info and News. Use when the user asks to research the market, compare coins, or combine fundamentals with technicals, news, or risk in one request. Triggers on 'market brief', 'research', 'compare coins', 'daily brief', 'worth buying'. Do NOT use for strictly single-dimension-only queries — use the matching gate-info-* or gate-news-* skill."
---

# Market Research Copilot

> L2 composite skill — orchestrates 12 read-only MCP Tool Calls across **Gate-Info MCP** (8 tools) and **Gate-News MCP** (4 tools) to aggregate multi-source market intelligence into structured, citation-backed reports. **No trading, swaps, staking, or any fund-moving operations.**

**Trigger Scenarios**: User intent is "research / understand / analyze" — market overview, single-coin analysis, multi-coin comparison, technical trends, event attribution, risk check, or daily briefing.

**Target Users**: Casual / beginner traders, content-oriented users, and pre-decision users who need to quickly understand the market, a coin, or risk before acting.

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate-Info | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- info_coin_get_coin_info
- info_compliance_check_token_security
- info_marketsnapshot_get_market_snapshot
- info_markettrend_get_indicator_history
- info_markettrend_get_kline
- info_markettrend_get_technical_analysis
- info_onchain_get_token_onchain
- info_platformmetrics_get_defi_overview
- news_events_get_event_detail
- news_events_get_latest_events
- news_feed_get_social_sentiment
- news_feed_search_news

### Authentication
- API Key Required: No

### Installation Check
- Required: Gate-Info
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this skill's research-copilot workflow.

- `SKILL.md` keeps routing logic, signal design, and report semantics.
- `references/mcp.md` is the authoritative MCP orchestration layer for signal-to-tool execution, parallel strategy, and fallback policy.

## Domain Knowledge

### Common Misconceptions

| Misconception | Truth |
|---------------|-------|
| "Analyze BTC then buy it for me" will trigger a trade | This Skill only produces analysis. Execution intent is routed to trading skills (e.g., `gate-exchange-spot`). |
| Analysis conclusions = investment advice | Output must distinguish "data-driven analysis" from "investment advice". Never promise returns. |

### Design Rationale: 5-Dimension Signal Stacking

User queries often span multiple analysis dimensions (e.g., "How is BTC doing?" implies fundamentals + technicals + news). Forcing a single-intent classification is fragile. This Skill uses **dimension signal stacking** instead of N-choose-1 classification: independently detect 5 signal dimensions from the query, each activated dimension contributes a set of Tool Calls, and the final tool set is their union. Running 5 independent binary classifiers is far more stable than 1 nine-way classifier.

### Tool Inventory (12 unique tools, all read-only, no auth required)

| # | MCP Service | Tool Name | Purpose |
|---|-------------|-----------|---------|
| 1 | Gate-Info | `info_marketsnapshot_get_market_snapshot` | Real-time coin snapshot (price, change, OI, funding rate) |
| 2 | Gate-Info | `info_coin_get_coin_info` | Coin fundamentals (project, funding, tokenomics) |
| 3 | Gate-Info | `info_markettrend_get_kline` | K-line OHLCV data |
| 4 | Gate-Info | `info_markettrend_get_indicator_history` | Technical indicator history (RSI/MACD/Bollinger/MA) |
| 5 | Gate-Info | `info_markettrend_get_technical_analysis` | Multi-timeframe composite signals |
| 6 | Gate-Info | `info_platformmetrics_get_defi_overview` | DeFi overview (TVL, DEX volume, stablecoin supply) |
| 7 | Gate-Info | `info_compliance_check_token_security` | Token contract security audit (30+ risk flags) |
| 8 | Gate-Info | `info_onchain_get_token_onchain` | On-chain anomalies (large transfers, exchange flows) |
| 9 | Gate-News | `news_events_get_latest_events` | Major event list with impact analysis |
| 10 | Gate-News | `news_events_get_event_detail` | Event detail (cause, impact, timeline) |
| 11 | Gate-News | `news_feed_search_news` | News search (by importance or time) |
| 12 | Gate-News | `news_feed_get_social_sentiment` | Social media sentiment (KOL volume, bias) |

### L1 Skill to Tool Mapping

| L1 Skill | Tools Used |
|----------|------------|
| gate-info-marketoverview | `info_marketsnapshot_get_market_snapshot`, `info_platformmetrics_get_defi_overview`, `news_events_get_latest_events` |
| gate-info-coinanalysis | `info_coin_get_coin_info`, `info_marketsnapshot_get_market_snapshot`, `info_markettrend_get_technical_analysis`, `news_feed_search_news`, `news_feed_get_social_sentiment` |
| gate-info-trendanalysis | `info_markettrend_get_kline`, `info_markettrend_get_indicator_history`, `info_markettrend_get_technical_analysis`, `info_marketsnapshot_get_market_snapshot` |
| gate-info-coincompare | `info_marketsnapshot_get_market_snapshot` x N, `info_coin_get_coin_info` x N, `info_markettrend_get_technical_analysis` x N (optional) |
| gate-info-riskcheck | `info_compliance_check_token_security`, `info_coin_get_coin_info` |
| gate-news-briefing | `news_events_get_latest_events`, `news_feed_search_news`, `news_feed_get_social_sentiment` |
| gate-news-eventexplain | `news_events_get_latest_events`, `info_marketsnapshot_get_market_snapshot`, `news_events_get_event_detail`, `info_onchain_get_token_onchain`, `news_feed_search_news` |

### Key Parameter Notes

- `info_marketsnapshot_get_market_snapshot`: Always pass `source="spot"` to avoid non-standard pair data contamination.
- `info_markettrend_get_kline`: Always pass `source="spot"` — without this constraint, price data may include DEX non-standard pairs, producing incorrect prices. **This is a mandatory parameter.**
- `info_compliance_check_token_security`: Requires `chain` parameter; skip for major coins (BTC/ETH) where contract audit is not applicable.
- `info_onchain_get_token_onchain`: Some tokens return empty results — this is expected; skip the on-chain section and annotate "On-chain data unavailable".

---

## Workflow

For concrete prompt examples and expected behavior per scenario, see `references/scenarios.md`.

**MCP tool calls**: Only **Step 3** invokes Gate-Info / Gate-News MCP tools (`info_*`, `news_*`). **Steps 1, 2, 4, and 5** are orchestration, signal planning, aggregation, and formatting — **no MCP tool call in those steps**.

### Step 1: Intent Gate — Research vs. Execution

Determine if the user wants to **research** or **execute**.

- **Research intent** (enter this Skill): understand, analyze, compare, briefing, risk check, trend, why pumping/dumping, sentiment, fundamentals, worth buying, overview, report.
- **Execution intent** (route away): buy, sell, swap, stake, transfer, withdraw, place order, close position.

If the user mixes both (e.g., "analyze BTC then buy"), split into two phases: complete the research phase within this Skill, then route the execution phase to the appropriate trading skill (e.g., `gate-exchange-spot`).

Key data to extract:
- `intent_type`: "research" or "execution"

### Step 2: Parameter Extraction & 5-Dimension Signal Detection

Extract parameters from the user query:
- `symbols[]`: Coin tickers (0 to N). Map project names to tickers (Solana -> SOL, Chainlink -> LINK).
- `sector`: Optional sector (DeFi, Layer2, Meme, etc.)
- `time_range`: Time scope (default 24h)

Then independently evaluate each of the 5 signal dimensions (non-exclusive, multiple can fire):

| Signal | Dimension | Trigger Condition | Trigger Keywords (illustrative English cues only; match **intent** in **any** human language, not literal string-only) | Activated Tools |
|--------|-----------|-------------------|-------------------------------------------------------------------------------------------------------------|-----------------|
| S1 | Market / Macro | No specific coin + broad market focus | market, overall, sector, broad market, majors, macro, daily brief, today, rates / policy, hot sectors, tape, whole-market view | `info_marketsnapshot_get_market_snapshot`(BTC/ETH/top coins), `info_platformmetrics_get_defi_overview`, `news_events_get_latest_events` |
| S2 | Fundamentals / Project | Specific coin + project attribute focus | fundamentals, project, funding, team, tokenomics, worth buying, upside, quality, how is it | `info_coin_get_coin_info`({symbol}), `info_marketsnapshot_get_market_snapshot`({symbol}) |
| S3 | Technicals / K-line | Specific coin + price/indicator focus; **or** user wording (any language) **semantically** asks for a **holistic / comprehensive** read that includes **market or technical** stance per coin (often alongside fundamentals). **Intent-based**, not a closed keyword list. | **Price / indicators**: K-line, candlestick, support, resistance, levels, overbought, oversold, RSI, MACD, Bollinger, technicals, trend, pattern, trajectory, outlook, follow-up path · **Holistic**: comprehensive, holistic, full picture, overall | `info_markettrend_get_kline`, `info_markettrend_get_indicator_history`, `info_markettrend_get_technical_analysis`, `info_marketsnapshot_get_market_snapshot` |
| S4 | News / Sentiment / Attribution | Event or reason focus (coin optional) | why pumping, dumping, up, down, reason, catalyst, news, narrative, sentiment, event, what happened, rebound, recovery | `news_events_get_latest_events`, `news_feed_search_news`, `news_feed_get_social_sentiment`, `news_events_get_event_detail` (conditional), `info_onchain_get_token_onchain` (conditional) |
| S5 | Security / Risk | Contract security / scam-risk focus; **or** the user’s wording (any language) **semantically** expresses **long-term holding** of the token(s) under discussion, **or** **coin selection** (choosing / comparing which coin(s) to favor). Use **intent semantics**, not a fixed keyword list. **Do not** treat a bare English "long-term" **by itself** as sufficient for the long-term-holding branch without clearer hold / selection intent. | **Security**: safe, risk, contract security, honeypot, rug, scam, audit, trustworthy, screen, token risk, due diligence · **Long-term / selection**: infer meaning from context — **no** closed keyword list | `info_compliance_check_token_security`, `info_coin_get_coin_info` |

**Fallback rules** (when no signal is explicitly activated):
- `symbols == 0` -> activate S1 (market overview)
- `symbols == 1` -> activate S2 + S3 (single-coin comprehensive = fundamentals + technicals)
- `symbols >= 2` -> activate S2 x N (multi-coin comparison)
- `symbols >= 2` **and** the user **semantically** asks for a **comprehensive / holistic** multi-coin view (same spirit as single-coin S2+S3) -> also activate **S3 x N** (i.e. S2 x N + S3 x N)

**Screening mode** (when `symbols == 0` and the query contains screening cues — e.g. filter, find, recommend, which, ranking, top, screen, pick, best, shortlist, highest potential):
- Phase 1: Activate S1 to fetch top-coin snapshots
- LLM intermediate aggregation: Extract symbols from Phase 1 results
- Phase 2: Activate S2/S3/S4/S5 per remaining signal keywords

Key data to extract:
- `symbols[]`: List of coin tickers
- `sector`: Sector filter if any
- `time_range`: Time scope
- `activated_signals[]`: List of activated signal dimensions (S1-S5)
- `screening_mode`: Boolean

**Signal Routing Examples** (English phrasing; same routing logic applies to equivalent questions in any language):

| User Query (example) | symbols | Activated Signals | Explanation |
|----------------------|---------|-------------------|-------------|
| "How is BTC doing?" | [BTC] | S2 + S3 (fallback) | No explicit dimension keywords; fallback: single-coin comprehensive |
| "Show me DOT support and resistance" | [DOT] | S3 | Support / resistance wording triggers Technicals |
| "DOT support levels plus the latest news" | [DOT] | S3 + S4 | Technicals + News dual activation |
| "Why did the market crash yesterday?" | [] | S4 + S1 | Why / crash triggers S4; market context triggers S1 |
| "Is sentiment recovering?" | [] | S4 (+ S1 if "market" scope) | Recovery / sentiment triggers S4; add S1 if query is market-wide |
| "Is ADA safe?" | [ADA] | S5 | Safety wording triggers Security |
| "Full weekend research report on XRP — price, news, and risk" | [XRP] | S2 + S3 + S4 + S5 | Full research report implies all dimensions |
| "Compare BTC, ETH, and SOL" | [BTC,ETH,SOL] | S2 x 3 (fallback) | Multi-coin, no extra keywords; fallback: comparison |
| "Comprehensive comparison of BTC, ETH, and SOL" | [BTC,ETH,SOL] | S2 x 3 + S3 x 3 | Comprehensive multi-coin -> stack technicals per coin |
| "Long-term hold: compare BTC, ETH, and SOL holistically" | [BTC,ETH,SOL] | S2 x 3 + S3 x 3 + S5 x 3 | Long-term selection + holistic view often implies fundamentals + technicals + risk |
| "Daily market brief — majors, hot sectors, drivers, and tomorrow's outlook" | [] | S1 + S4 + S3(BTC) | Macro brief + causes + outlook -> S1, S4, optional S3 for trend |
| "Screen the top 5 gainers today and analyze the most promising one" | [] | S1 -> S2 + S3 (screening) | Screening + top gainers / potential -> P1 snapshots, P2 deep dive on picked symbol |
| "Why is DeFi up? Leader coin fundamentals and technicals" | [] (+ sector) | S1 + S4 -> S2 + S3 | Sector + why -> S1/S4 then leader symbol -> S2 + S3 |
| "Which coins are oversold? Pick two and analyze them" | [] | S1 -> S3 + S2 (screening) | Open-ended which + oversold/overbought + pick -> screening; P2 S3 + S2 |
| "Check ADA token risk and fundamentals" | [ADA] | S5 + S2 | Due diligence + token safety + fundamentals -> S5 + S2 |

### Step 3: Assemble Tool Set & Execute

Combine all activated signal tool sets into a union, deduplicate by tool name + parameters, then execute:

**Parallel execution** (tools within the same Phase have no dependencies — call simultaneously):
- All tools in a Phase are dispatched in parallel.

**Serial dependencies** (next Phase depends on previous Phase LLM aggregation):
- Screening mode: Phase 1 snapshot results -> LLM extracts symbols -> Phase 2 uses those symbols.
- Attribution branch (S4): `news_events_get_latest_events` result determines whether to call `news_events_get_event_detail` (event found) or skip (no event).

**Deduplication rule**: Same tool + same parameters within one request is called only once; the result is reused across multiple aggregation steps.

Call each activated tool with the parameter conventions below:

Call `info_marketsnapshot_get_market_snapshot` with: `symbol={symbol}, timeframe="1d", source="spot"`
Call `info_coin_get_coin_info` with: `query={symbol}, scope="full"`
Call `info_markettrend_get_kline` with: `symbol={symbol}, timeframe="1d", limit=90, source="spot"`
Call `info_markettrend_get_indicator_history` with: `symbol={symbol}, indicators=["rsi","macd","bollinger","ma"]`
Call `info_markettrend_get_technical_analysis` with: `symbol={symbol}`
Call `info_platformmetrics_get_defi_overview` with: `category="all"`
Call `info_compliance_check_token_security` with: `token={symbol}, chain={chain}`
Call `info_onchain_get_token_onchain` with: `token={symbol}`
Call `news_events_get_latest_events` with: `time_range={time_range}, limit=10`
Call `news_events_get_event_detail` with: `event_id={event_id}`
Call `news_feed_search_news` with: `coin={symbol}, limit=5, sort_by="importance"`
Call `news_feed_get_social_sentiment` with: `coin={symbol}`

Key data to extract:
- `tool_results{}`: Map of tool name to response data
- `failed_tools[]`: Tools that timed out or returned errors

### Step 4: LLM Multi-Source Aggregation

Pass all tool responses to the LLM for aggregation:

1. **Merge** data from all dimensions into a coherent narrative.
2. **Deduplicate** overlapping information (e.g., price from multiple snapshot calls).
3. **Conflict resolution**: If sources contradict each other, present both viewpoints with attribution — never merge contradictory conclusions into one sentence.
4. **Data timestamp**: Label each data point with its approximate data time (e.g., "as of 2026-03-21 12:00 UTC"). Do NOT include internal tool names or API field names in the output.
5. **Missing data**: If a tool failed or returned empty, annotate "Data unavailable for this section" — never fabricate data.

Key data to extract:
- `aggregated_report`: Structured report content
- `data_sources[]`: List of tools that contributed data
- `data_timestamps`: Approximate data freshness

### Step 5: Output Structured Report

Select the appropriate report template based on the activated signals, then output the final report. Always include the disclaimer at the end.

Key data to extract:
- `final_report`: Markdown string — user-facing report body (template-filled; may refine `aggregated_report` from Step 4); must include the standard disclaimer.

---

## Report Template

### Template A: Market Overview Brief (S1 dominant)

```markdown
## Market Overview Brief

**Data Time**: {timestamp}

### Market Snapshot

| Metric | Value | 24h Change |
|--------|-------|------------|
| BTC | ${btc_price} | {btc_change_24h}% |
| ETH | ${eth_price} | {eth_change_24h}% |
| Total Crypto Market Cap | ${total_mcap} | {mcap_change}% |
| Fear & Greed Index | {fear_greed} | {sentiment_label} |

### DeFi Overview

| Metric | Value |
|--------|-------|
| Total TVL | ${tvl} |
| DEX 24h Volume | ${dex_volume} |
| Stablecoin Total Supply | ${stablecoin_supply} |
| Long/Short Ratio | {long_short_ratio} |

### Key Events (Past 24h)

1. **{event_title}** — {impact_summary}
2. ...

### Market Sentiment

- Social Sentiment Score: {score} ({bias})
- Key Discussions: {summary of trending topics}

### Summary & Outlook

{LLM 3-5 sentence synthesis: current market phase, primary drivers, key risks}

> Data sourced from Gate-Info MCP and Gate-News MCP. Analysis is data-driven and does not constitute investment advice.
```

### Template B: Single-Coin Deep Dive (S2+S3 dominant)

```markdown
## {symbol} Research Report

**Data Time**: {timestamp}

### 1. Fundamentals

| Metric | Value |
|--------|-------|
| Project | {project_name} |
| Sector | {category} |
| Market Cap | ${market_cap} |
| FDV | ${fdv} |
| Circulating / Total Supply | {circulating} / {total} |
| Key Investors | {investors} |

{Tokenomics summary; flag upcoming large unlocks}

### 2. Market & Technical Analysis

| Metric | Value | Status |
|--------|-------|--------|
| Price | ${price} | — |
| 24h Change | {change_24h}% | {Up/Down/Flat} |
| 7d Change | {change_7d}% | {Up/Down/Flat} |
| RSI(14) | {rsi} | {Overbought/Oversold/Neutral} |

**Technical Signals**:
- Short-term (1h/4h): {signal}
- Medium-term (1d): {signal}
- Support: ${support} | Resistance: ${resistance}

### 3. News & Sentiment

**Recent News**:
1. {title} — {summary} ({source}, {time})
2. ...

**Social Sentiment**: {sentiment_score} ({bias}) — {summary}

### 4. Risk Alerts

{Data-driven alerts: RSI extremes, volume anomalies, funding rate, upcoming unlocks, low liquidity}

### 5. Overall Assessment

{LLM 3-5 sentence synthesis: market phase, drivers, risks}

> Data sourced from Gate-Info MCP and Gate-News MCP. Analysis is data-driven and does not constitute investment advice.
```

### Template C: Multi-Coin Comparison (S2 x N)

```markdown
## Multi-Coin Comparison: {coin1} vs {coin2} vs ...

**Data Time**: {timestamp}

### Comparison Table

| Metric | {coin1} | {coin2} | {coin3} |
|--------|---------|---------|---------|
| Price | ${price1} | ${price2} | ${price3} |
| Market Cap | ${mcap1} | ${mcap2} | ${mcap3} |
| 24h Change | {chg1}% | {chg2}% | {chg3}% |
| RSI(14) | {rsi1} | {rsi2} | {rsi3} |
| Sector | {cat1} | {cat2} | {cat3} |
| Risk Level | {risk1} | {risk2} | {risk3} |

### Per-Coin Highlights

**{coin1}**: {1-2 sentence highlight}
**{coin2}**: {1-2 sentence highlight}

### Comparative Assessment

{LLM analysis: relative strengths/weaknesses, risk comparison, suitability for different strategies}

> Data sourced from Gate-Info MCP and Gate-News MCP. Analysis is data-driven and does not constitute investment advice.
```

### Template D: Event Attribution (S4 dominant)

```markdown
## Market Movement Attribution

**Data Time**: {timestamp}

### What Happened

{Brief description of the price movement or market event}

### Root Cause Analysis

1. **{event/cause 1}**: {explanation with data}
2. **{event/cause 2}**: {explanation}

### On-Chain Evidence

{On-chain flow data if available, otherwise "On-chain data unavailable"}

### Current Sentiment

- Social Score: {score} ({bias})
- Recovery Signal: {recovering/still negative/neutral}

### Outlook

{LLM forward-looking assessment based on event + sentiment + technical data}

> Data sourced from Gate-Info MCP and Gate-News MCP. Analysis is data-driven and does not constitute investment advice.
```

### Template E: Risk Check (S5 dominant)

```markdown
## {symbol} Security & Risk Report

**Data Time**: {timestamp}

### Contract Security Audit

| Check | Result | Detail |
|-------|--------|--------|
| Honeypot | {Yes/No} | {detail} |
| Hidden Owner | {Yes/No} | {detail} |
| Buy/Sell Tax | {buy_tax}% / {sell_tax}% | {normal/abnormal} |
| Holder Concentration | {top10_pct}% | {concentrated/distributed} |
| Overall Risk Level | {Low/Medium/High} | {flags_count} flags |

### Fundamentals Cross-Check

| Metric | Value |
|--------|-------|
| Project | {project_name} |
| Market Cap | ${market_cap} |
| Active Addresses | {address_count} |

### Risk Summary

{LLM synthesis: overall risk assessment, specific concerns, red flags}

> Data sourced from Gate-Info MCP and Gate-News MCP. Analysis is data-driven and does not constitute investment advice.
```

---

## Judgment Logic Summary

| Condition | Action |
|-----------|--------|
| User intent is "execute" (buy/sell/swap/stake) | Route to appropriate trading skill; do NOT enter this Skill |
| User mentions DEX / on-chain address / liquidity pool | Route to `gate-dex-market` or DEX-related skill |
| No symbols and no explicit dimension keywords | Fallback: activate S1 (market overview) |
| 1 symbol and no explicit dimension keywords | Fallback: activate S2 + S3 (single-coin comprehensive) |
| 2+ symbols and no explicit dimension keywords | Fallback: activate S2 x N (multi-coin comparison) |
| 2+ symbols and user semantically asks for comprehensive/holistic multi-coin analysis (same intent may be expressed in any language) | Activate S2 x N + S3 x N |
| Symbols == 0 + screening keywords (filter/find/top/which) | Enter screening mode: S1 in P1 -> extract symbols -> targeted signals in P2 |
| Query contains "research report" or "full report" | Activate all signals: S2 + S3 + S4 + S5 |
| A single tool times out or returns empty | Skip that dimension; annotate "Data unavailable" |
| All tools fail | Return error; suggest retry later |
| `info_markettrend_get_kline` returns abnormal prices | Likely missing `source=spot` constraint; retry with parameter |
| User asks "analyze then buy" | Complete research (this Skill) then route execution to trading skill |
| Contradictory data from multiple sources | Present both viewpoints with attribution; do not merge |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Coin not found | Ask user to verify the coin name or ticker |
| Single tool timeout | Skip that dimension; note "This dimension is temporarily unavailable" |
| All tools fail | Return error message; suggest retry later |
| No Gate-News MCP configured | Use only Gate-Info tools (8 tools); mark news/sentiment sections as "No data" |
| No Gate-Info MCP configured | Critical — cannot proceed; guide user to install Gate-Info MCP |
| `info_onchain_get_token_onchain` returns empty | Expected for some tokens; skip on-chain section with note |
| `info_compliance_check_token_security` on BTC/ETH | Skip contract audit for major coins; note "Not applicable for native chain assets" |
| User asks about NFT / options / other uncovered categories | Explain coverage boundary; route to specialized skill if available |

---

## L1/L2 Routing Strategy

When a user query can be handled by a single L1 Skill's tool set (e.g., "How is BTC?" only needs coinanalysis's 5 tools), this L2 still serves as the unified entry point for all "research" intents:

- **Short-circuit optimization**: If the activated signals map to only one L1's tools, call only that subset and produce the report — no need to invoke all 12 tools.
- **Principle**: Unified entry via this L2 ensures consistent "research" experience; internally, 1 to 12 tools are called as needed.

### DEX / On-Chain Boundary Handling

This Skill uses only Gate-Info MCP and Gate-News MCP. It does **not** include `gate-dex-*` or on-chain address tracking capabilities.

| Situation | Detection Signal | Action |
|-----------|-----------------|--------|
| User mentions DEX explicitly | "DEX", "on-chain", "liquidity pool", "Uniswap", "wallet address" | Route to `gate-dex-market` or DEX skill; do NOT enter this Skill |
| Ambiguous "liquidity" without CEX/DEX context | "this coin's liquidity" | Default to CEX interpretation; if user clarifies DEX, re-route |
| User asks about NFT / options | "NFT", "options", "derivatives" | Explain coverage boundary; route to specialized skill if available |
| User asks "Is this coin listed on Gate?" | "listed", "can I buy" | Brief listing check + risk note; or route to listing/new-coin skill |
| Multi-language or mixed-language user input | N/A | Parse intent normally; if "research" intent with no DEX/execution signals, enter this Skill |

### No Confirmation Required

This L2 does **not** involve any trading confirmation mechanism because:

- All 12 Tool Calls are **read-only queries** (`info_*` / `news_*`); zero `cex_*` write operations
- No asset changes, order placement, transfers, or mode switches
- No API Key / Secret / OAuth2 required

If the user appends execution intent (e.g., "analyze then buy"), this Skill completes the research phase only. The execution phase is routed to the appropriate trading skill (e.g., `gate-exchange-spot`), which applies its own Action Draft -> User Confirm -> Execute flow.

### Tool Degradation Matrix

| Tool | Degradation Strategy |
|------|---------------------|
| `info_onchain_get_token_onchain` | Some tokens return empty; skip on-chain section and annotate "On-chain data unavailable" |
| `info_compliance_check_token_security` | Requires `chain` parameter; skip for major coins (BTC/ETH); annotate "Not applicable for native chain assets" |
| `news_events_get_event_detail` | Depends on `event_id` from P1; if no events in P1, skip (go to P2b branch) |
| `info_marketsnapshot_get_market_snapshot` | If timeout, retry once; if still fails, skip snapshot section |
| Any other tool | Single tool failure: skip that dimension, annotate "This dimension is temporarily unavailable" |
| All tools | If all tools fail: return error message, suggest retry later |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Buy it" / "Place an order" | `gate-exchange-spot` |
| "Open a futures position" | `gate-exchange-futures` |
| "Swap it" | `gate-exchange-flashswap` |
| "Stake it" | `gate-exchange-staking` or `gate-exchange-simpleearn` |
| "Check my assets" | `gate-exchange-assets` |
| "Track this wallet address" | `gate-info-addresstracker` |
| "Show DEX data" | `gate-dex-market` |

---

## Safety Rules

1. **No investment advice**: All output is data-driven analysis. Every report must include the disclaimer: "does not constitute investment advice."
2. **No price predictions**: Do not output specific target prices or directional predictions (e.g., "will reach $100K").
3. **No fund operations**: This Skill calls only read-only `info_*` and `news_*` tools. Never call `cex_*` tools.
4. **Data transparency**: Label approximate data time for each section (e.g., "Data as of ..."). Use natural-language source labels (e.g., "Gate market data", "Gate news") instead of internal tool names or API field names. Never expose `info_*`, `news_*`, `cex_*` tool identifiers or raw JSON field names (e.g., `snapshot_time`, `total_defi_tvl`) in user-facing output.
5. **No data fabrication**: When a tool returns empty or fails, clearly state "Data unavailable" — never fabricate numbers.
6. **Conflict disclosure**: When sources contradict, present both sides with attribution rather than silently picking one.
7. **No auth required**: All 12 tools are public read-only; no API Key or OAuth2 is needed.
8. **No internal identifiers in output**: The final user-facing report must NOT contain any internal tool names (e.g., `info_marketsnapshot_get_market_snapshot`, `news_events_get_latest_events`), API field names (e.g., `snapshot_time`, `total_defi_tvl`, `total_liquidation_24h`, `market_cap`), or MCP service prefixes (`info_*`, `news_*`, `cex_*`). Present all data using natural-language descriptions only. Tool names and field names are internal orchestration details — they must never leak into the report.
9. **Age restriction**: This skill is intended for users aged 18 or above with full civil capacity, consistent with Gate's platform requirements.
10. **Data flow declaration**: All data flows exclusively through Gate MCP to Gate API. No user data is transmitted to third parties.
