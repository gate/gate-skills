# gate-news-communityscan — Scenarios & Prompt Examples

## Scenario 1: Community opinion on a coin

**Context**: User wants social/community take on a specific asset.

**Prompt Examples**:
- "What does the community think about ETH"
- "X sentiment on SOL"

**Expected Behavior**:
1. Parallel `news_feed_search_x` (query from coin/topic) and `news_feed_get_social_sentiment` (with `coin` when specified).
2. Output SKILL.md template; label **Platforms: X/Twitter only**.

## Scenario 2: General market social mood

**Context**: No single coin — broad social scan.

**Prompt Examples**:
- "What are people saying on crypto Twitter"
- "Overall market sentiment on X"

**Expected Behavior**:
1. Build a general query; call both tools; synthesize narratives + metrics.
2. If sentiment tool lacks coin, still deliver X discussion section.

## Scenario 3: One tool empty or fails

**Context**: Partial API failure.

**Prompt Examples**:
- "Community thoughts on BTC" (X search fails)

**Expected Behavior**:
1. Per **Error Handling**: sentiment-only or X-only section; note which part is unavailable; do not fabricate KOL quotes.

## Scenario 4: User asks for Reddit / Discord

**Context**: UGC platforms not supported.

**Prompt Examples**:
- "Reddit discussion on this token"

**Expected Behavior**:
1. State UGC search is **not** online; offer X/Twitter-only scan or route to `gate-news-briefing` for general news.

## Scenario 5: Route away

**Context**: User wants headlines or full coin research, not social-only.

**Prompt Examples**:
- "Latest crypto news" → `gate-news-briefing`
- "Full analysis of BTC" → `gate-info-coinanalysis` or `gate-info-research` if multi-dimension

**Expected Behavior**:
1. Apply SKILL.md **Routing Rules** before executing this skill.
