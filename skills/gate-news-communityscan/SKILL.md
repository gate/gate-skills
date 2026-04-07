---
name: gate-news-communityscan
version: "2026.4.7-1"
updated: "2026-04-07"
description: "Community sentiment via Gate-News MCP, X/Twitter-first. Use for social discussion, KOL takes, or opinion on a coin or topic. Triggers: what does the community think about ETH, Twitter or X sentiment, what are people saying, KOL opinions. Reddit, Discord, Telegram when search_ugc is available; until then label output as X/Twitter-only. Tools: news_feed_search_x, news_feed_get_social_sentiment."
required_credentials: []
required_env_vars: []
required_permissions: []
---

# gate-news-communityscan

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read `./references/gate-runtime-rules.md`
→ Also read `./references/info-news-runtime-rules.md` for gate-info / gate-news shared rules (tool degradation, report standards, security, and output standards).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

> Community Sentiment Scan Skill (**X/Twitter focused**). Parallel calls fetch X/Twitter discussion analysis and quantitative social sentiment; LLM aggregates into a community insights report.

**Trigger Scenarios**: Community opinions, Twitter/X discussions, KOL views, social sentiment, etc.

## Known Limitations

- UGC platforms: Reddit, Discord, and Telegram depend on `search_ugc` availability. Until that API is online, label reports as X/Twitter-only.
- Historical sentiment trend may degrade to a single-point snapshot depending on upstream API coverage.

---

## MCP Dependencies

### Required MCP Servers

| MCP Server | Status |
|------------|--------|
| Gate-News | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- news_feed_search_x (X/Twitter discussion — e.g., Grok-backed analysis per upstream)
- news_feed_get_social_sentiment

### Authentication
- API Key Required: No
- Credentials Source: None; this skill uses read-only Gate Info / Gate News MCP access only.

### Installation Check
- Required: Gate-News
- Install: Use the local Gate MCP installation flow for the current host IDE before continuing.
- Continue only after the required Gate MCP server is available in the current environment.

## Routing Rules

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Community opinion on a coin | "what does community think about ETH" | Execute with `coin` |
| X/Twitter discussion | "Twitter discussion" "KOL views" | Execute (X-focused) |
| General social sentiment | "overall market sentiment" | Execute (no specific coin) |
| Reddit/Discord specific | "Reddit discussion" | Inform: X now; UGC coming |
| News only | "any crypto news" | Route to `gate-news-briefing` |
| Coin analysis | "analyze SOL" | Route to `gate-info-coinanalysis` |
| Why price moved | "why did BTC pump" | Route to `gate-news-eventexplain` |

---

## Execution Workflow

### Step 0: Multi-Dimension Intent Check

- Community/social sentiment → this Skill.
- Coin fundamentals + technicals + macro together → `gate-info-research` (if available).

### Step 1: Intent Recognition & Parameter Extraction

- `coin` (optional)
- `topic` (optional): e.g., ETF, regulation, Layer 2
- `query`: constructed from coin + topic for X search; if neither, general market social scan

### Step 2: Call MCP Tools in Parallel

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `news_feed_search_x` | `query={coin or topic}` | X discussion / narratives / KOL angles | Yes |
| 1b | `news_feed_get_social_sentiment` | `coin={coin}` if specified | Sentiment score, ratios, mention volume | Yes |

### Step 3: LLM Aggregation

- Synthesize qualitative X discussion with quantitative sentiment
- Dominant narratives and KOL themes
- Sentiment vs price alignment or divergence

---

## Report Template

```markdown
## Community Sentiment Scan: {coin or topic}

> Generated: {timestamp} | Platforms: X/Twitter only
> Note: Reddit/Discord/Telegram not yet supported.

### X/Twitter Discussion

{Summary from news_feed_search_x}

**Key Narratives**: ...
**Notable KOL Views**: ...

### Sentiment Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| Sentiment Score | {score} | {Bullish/Bearish/Neutral} |

### Sentiment vs Price

| Dimension | Current |
|-----------|---------|
| Social Sentiment | ... |
| Price Trend (24h) | ... |
| Alignment | {Aligned / Divergent} |

### Key Takeaways

{2–3 insights}

> Community sentiment is not a reliable price predictor. This does not constitute investment advice.
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| Sentiment score > 70 | Strongly bullish — contrarian caution |
| Sentiment score < 30 | Strongly bearish — possible capitulation or opportunity |
| Positive ratio > 80% | Strong positive consensus — watch for reversal |
| Discussion volume > 2x 7d average | Unusual activity — possible catalyst |
| KOL opinions divided | Broken consensus — uncertainty |
| Sentiment bullish but price falling | Divergence — sentiment may lag |
| Sentiment bearish but price rising | Divergence — market defying expectations |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| `news_feed_search_x` fails | Sentiment metrics only; note X discussion unavailable |
| `news_feed_get_social_sentiment` fails | X discussion only; skip metrics |
| Both Tools fail | Return error; suggest retry |
| No X discussions for query | Broaden query; note limited data |
| User asks for Reddit/Discord | State UGC not available; X-only for now |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Analyze this coin" | `gate-info-coinanalysis` |
| "Any news about this?" | `gate-news-briefing` |
| "Why is it pumping/dumping?" | `gate-news-eventexplain` |
| "Technical analysis?" | `gate-info-trendanalysis` |
| "On-chain data?" | `gate-info-tokenonchain` |
| "How's the overall market?" | `gate-info-marketoverview` |

---

## Safety Rules

1. **No fabricated opinions**: Only report what data supports; do not invent KOL quotes.
2. **Source attribution**: Attribute generically to KOL/community unless public figure is clearly named in data.
3. **Neutral presentation**: Show bullish and bearish views.
4. **Sentiment ≠ prediction**: State limitations clearly.
5. **Platform transparency**: Label X/Twitter-only coverage.
6. **Misinformation**: Prefer "unverified claims circulating" over stating rumors as fact.
7. **Age & eligibility**: Intended for users **aged 18 or above** with **full civil capacity** in their jurisdiction.
8. **Data flow**: The host agent processes user prompts; this skill directs **read-only** **Gate-News** MCP tools listed above. The LLM synthesizes from tool results. This skill does not invoke additional third-party data services.
