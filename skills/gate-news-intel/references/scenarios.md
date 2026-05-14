# gate-news-intel — Scenarios

## Scenario 1 — News brief (ticker required)

**Playbook**: `news_brief`

**Prompts**: "What happened to BTC recently", "headlines for ETH"

**Behavior**: Run `search-news` + `get-latest-events` + `get-social-sentiment` in parallel.

## Scenario 2 — Event timeline / detail lookup

**Playbook**: `event_explain`

**Prompts**: "What events happened around ETH recently", "event timeline for SOL"

**Behavior**: Events + news + sentiment; causal narrative in Section 2 before Section 4. Optional `get-event-detail` only if `event_id` is known. For price-move attribution queries like "Why did BTC crash", use `market_move_explain` (Scenario 7).

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

## Scenario 7 — Market move attribution

**Playbook**: `market_move_explain`

**Prompts**: "Why did BTC crash", "ETH why pump", "行情为什么大涨", "what caused the SOL dump", "这波行情怎么回事"

**Behavior**: Two-group execution:
- Group A (parallel): `explain-market-move` (core attribution with Tavily + internal event pool) + `get-market-snapshot` (price/volume context) + `get-orderbook` (depth/liquidity).
- Group B (after Group A, parallel): `get-technical-analysis` + `get-coin-info` + community (`search-x` + `get-social-sentiment` only for non-BTC; skipped for BTC).

Coin fallback: if no coin specified for broad-market queries, default to `BTC` with a visible notice. For vague references, ask the user.

Report uses the 6-section Market move analysis template: Summary, Primary drivers, Supporting context, Technical signals, Community perspective, What to watch. Partial data from data_status.is_partial is surfaced in the report footer.
