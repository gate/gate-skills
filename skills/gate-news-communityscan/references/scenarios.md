# gate-news-communityscan — Scenarios & Prompt Examples

## Scenario 1: Community opinion on a coin

**Context**: User wants social/community takes on a specific asset.

**Prompt Examples**:
- "What does the community think about ETH?"
- "Twitter sentiment on SOL today"

**Expected Behavior**:
1. Parallel `news_feed_search_x` with query from coin/topic and `news_feed_get_social_sentiment` with `coin` when applicable.
2. Produce **Community Sentiment Scan** report with X/Twitter discussion + sentiment metrics.
3. Label coverage **X/Twitter only** per **Known Limitations**.

## Scenario 2: General social sentiment

**Context**: User asks for broad market social mood without naming one coin.

**Prompt Examples**:
- "Overall crypto social sentiment"
- "Is the crowd bullish or bearish?"

**Expected Behavior**:
1. Build `query` from topic or general market terms; call both tools in parallel per `SKILL.md`.
2. If `coin` is absent, still run `news_feed_search_x`; use sentiment tool parameters as supported by MCP for general scans.
3. Note limitations if sentiment tool requires a specific coin.

## Scenario 3: Reddit / Discord / UGC request

**Context**: User asks for non-X platforms.

**Prompt Examples**:
- "Reddit discussion on this coin"
- "What is Discord saying about the ETF?"

**Expected Behavior**:
1. State that **UGC** (Reddit/Discord/Telegram) is **not** available; output remains **X/Twitter only** (`SKILL.md` **Known Limitations**).
2. Optionally still run X/Twitter tools with an adjusted query if helpful; do not claim Reddit/Discord data.

## Scenario 4: Route to general news

**Context**: User wants headlines, not community sentiment framing.

**Prompt Examples**:
- "Any crypto news today?"
- "Latest headlines on Bitcoin"

**Expected Behavior**:
1. Route to `gate-news-briefing` per **Routing Rules**; do not treat as community scan unless the user asks for social/community/Twitter angle.
