# gate-news-intel — Scenarios

## Scenario 1 — News brief (ticker required)

**Playbook**: `news_brief`

**Prompts**: "What happened to BTC recently", "headlines for ETH"

**Behavior**: Run `search-news` + `get-latest-events` + `get-social-sentiment` in parallel.

## Scenario 2 — Why crash / event chain

**Playbook**: `event_explain`

**Prompts**: "Why did BTC crash"

**Behavior**: Events + news + sentiment; causal narrative in Section 2 before Section 4. Optional `get-event-detail` only if `event_id` is known.

## Scenario 3 — Listings / announcements

**Playbook**: `exchange_listings`

**Prompts**: "Any new coins listed recently", "Delisting announcements"

**Behavior**: `get-exchange-announcements`; add `--coin` when user names a symbol (see `--help`).

## Scenario 4 — Community-first

**Playbook**: `community_intel`

**Prompts**: "What does the community think about SOL", "What is Reddit saying", "What is YouTube saying"

**Behavior**: `search-ugc` + `search-x` + `get-social-sentiment` — Section 3 before any market overview.

## Scenario 5 — News + market context

**Playbook**: `intel_plus_market`

**Prompts**: "News and market background", "What happened and check the market"

**Behavior**: News group first; optional `info` group — if info fails, still ship news sections.

## Scenario 6 — No ticker

**Playbook**: `market_wide_intel`

**Prompts**: "Recent crypto news", "overall crypto narrative"

**Behavior**: `web-search` + optional `get-market-overview`.
