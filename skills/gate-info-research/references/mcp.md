---
name: gate-info-research-mcp
version: "2026.3.30-1"
updated: "2026-03-30"
description: "MCP orchestration specification for the Market Research Copilot multi-signal read-only workflow."
---

# Gate Research Copilot MCP Specification

## 1. Scope and Trigger Boundaries

In scope:
- Read-only market/coin/event/risk research
- Multi-signal orchestration across Gate-Info and Gate-News

Out of scope:
- Any trade execution, transfer, staking, or account mutation

Misroute examples:
- Requests to place orders must route to exchange execution skills.

## 2. MCP Detection and Fallback

Detection:
1. Verify key tool families: `info_*` and `news_*`.
2. Probe minimal snapshot/news endpoints before full orchestration.

Fallback:
- Continue partial analysis when some tools fail.
- Mark missing dimensions explicitly and lower confidence.

## 3. Authentication

- Standard flow is read-only and typically no API key required.
- If runtime enforces auth, request user to provide valid session.

## 4. MCP Resources

No mandatory MCP resources.

## 5. Tool Calling Specification

Supported read-only tool set:
- `info_coin_get_coin_info`
- `info_compliance_check_token_security`
- `info_marketsnapshot_get_market_snapshot`
- `info_markettrend_get_indicator_history`
- `info_markettrend_get_kline`
- `info_markettrend_get_technical_analysis`
- `info_onchain_get_token_onchain`
- `info_platformmetrics_get_defi_overview`
- `news_events_get_event_detail`
- `news_events_get_latest_events`
- `news_feed_get_social_sentiment`
- `news_feed_search_news`

Rules:
- Follow signal stacking and dedup rules from `SKILL.md`.
- Respect mandatory parameter constraints (for example `source="spot"` where required).

## 6. Execution SOP (Non-Skippable)

1. Gate intent: research vs execution.
2. Extract symbols/sector/time range and activate signals.
3. Build union tool plan with deduplication.
4. Execute in parallel by phase; serialize only dependency phases.
5. Aggregate with conflict attribution and timestamp labeling.
6. Output structured report with explicit disclaimer.

## 7. Output Templates

```markdown
## Research Summary
- Scope: {market_or_coin_or_multi_coin}
- Signals Used: {S1_to_S5}
- Key Findings: {fundamental_technical_news_risk_points}
- Data Gaps: {missing_or_failed_tools}
- Conclusion: {balanced_takeaway}
- Disclaimer: Data-driven analysis only, not investment advice.
```

## 8. Safety and Degradation Rules

1. Keep this skill strictly read-only.
2. Never fabricate data for failed tool sections.
3. Separate fact, inference, and opinion clearly.
4. Route execution intent to trading skills.
5. Use conservative language when data conflicts.
