# gate-info-research — Scenarios & Prompt Examples

> Read this file whenever the agent is unsure which playbook to pick. Every row pins a concrete prompt to a playbook id and the expected behavior.

## Scenario 1 — Single-coin analysis

**Playbook**: `single_coin`

**Prompts**:
- "Analyze SOL"
- "Analyze BTC"
- "How is ETH doing?"
- "How is SOL right now"

**Expected behavior**:
1. Extract `symbol`. If user gives a project name ("Solana"), resolve to ticker.
2. Run in parallel:
   - `gate-cli info coin get-coin-info --query {symbol} --scope full --format json`
   - `gate-cli info marketsnapshot get-market-snapshot --symbol {symbol} --scope full --format json`
   - `gate-cli info markettrend get-technical-analysis --symbol {symbol} --format json`
3. Optionally (when CLI returns non-empty) also:
   - `gate-cli news feed search-news --coin {symbol} --limit 5 --sort-by importance --time-range 24h --format json`
   - `gate-cli news feed get-social-sentiment --coin {symbol} --time-range 24h --format json`
4. Emit the 6-section report. If news/sentiment commands were skipped or returned empty, mark Section 4 as **no data**.

## Scenario 2 — Market overview

**Playbook**: `market_overview`

**Prompts**:
- "Market right now"
- "How is the market right now"
- "Which sectors are hot"

**Expected behavior**:
1. No required slot.
2. Run in parallel:
   - `gate-cli info marketsnapshot get-market-overview --format json`
   - `gate-cli info coin get-coin-rankings --ranking-type popular --limit 20 --format json`
   - `gate-cli info coin get-coin-rankings --ranking-type top_gainers --time-range 24h --limit 10 --format json`
   - `gate-cli info coin get-coin-rankings --ranking-type top_losers --time-range 24h --limit 10 --format json`
3. Section 2 (Fundamentals and Market Position) focuses on breadth / dominance / rotation; Section 3 on gainers / losers boards.

## Scenario 3 — Multi-coin comparison

**Playbook**: `multi_coin`

**Prompts**:
- "Compare BTC and ETH"
- "BTC vs SOL vs ARB"
- "Compare BTC ETH SOL AVAX"

**Expected behavior**:
1. Extract `symbols`. Guard: 2 ≤ len ≤ 20.
2. Run once: `gate-cli info marketsnapshot batch-market-snapshot --symbols BTC --symbols ETH ... --scope full --format json`.
3. For each symbol in parallel: `gate-cli info coin get-coin-info --query {symbol} --scope basic --format json` (and optionally `get-technical-analysis`).
4. Report still uses the 6-section template; Section 3 becomes a side-by-side comparison table.

## Scenario 4 — Trend / technical analysis

**Playbook**: `trend`

**Prompts**:
- "BTC RSI"
- "SOL MACD"
- "Help me do a technical analysis on BTC"

**Expected behavior**:
1. Required: `symbol`. Optional: `period` (default `3d`; enum `1h|4h|24h|3d|5d|7d|10d|all`), `timeframe` (default `1d`), `indicators` (default `rsi,macd,ma30,ma200` — lowercase, server-populated only).
2. Commands (parallel):
   - `gate-cli info markettrend get-technical-analysis --symbol {symbol} --period {period|3d} --format json`
   - `gate-cli info markettrend get-kline --symbol {symbol} --timeframe {timeframe|1d} --size 120 --with-indicators true --format json`
   - `gate-cli info markettrend get-indicator-history --symbol {symbol} --timeframe {timeframe|1d} --indicators rsi --indicators macd --indicators ma30 --indicators ma200 --limit 120 --format json`
3. Section 3 (Trend Analysis) becomes the primary focus; other sections may be thin.

## Scenario 5 — Macro impact

**Playbook**: `macro`

**Prompts**:
- "Impact of CPI on the market"
- "Impact of NFP on BTC"
- "Fed rate decision"

**Expected behavior**:
1. Optional slots: `symbol`, `country` (default `US`), `indicator` (default `CPI`), `start_date`, `end_date`.
2. Commands:
   - `gate-cli info macro get-macro-summary --format json`
   - `gate-cli info macro get-economic-calendar --start-date {today} --end-date {today+14d} --importance high --format json`
   - `gate-cli info macro get-macro-indicator --indicator {indicator} --country {country} --mode series --size 12 --format json`
3. When `symbol` is provided, also: `gate-cli info marketsnapshot get-market-snapshot --symbol {symbol} --scope basic --format json`.
4. Section 3 discusses the macro delta; Section 4 can cite relevant calendar items.

## Scenario 6 — Research + news synthesis

**Playbook**: `research_plus_news`

**Prompts**:
- "Analyze SOL and also check recent news and sentiment"
- "Analyze ETH and check recent events and community sentiment"

**Expected behavior**:
1. Run the `single_coin` body first.
2. Additionally in parallel:
   - `gate-cli news feed search-news --coin {symbol} --limit 10 --sort-by importance --time-range 24h --format json`
   - `gate-cli news feed get-social-sentiment --coin {symbol} --time-range 24h --format json`
   - `gate-cli news feed search-ugc --coin {symbol} --time-range 7d --platform all --limit 20 --format json` (optional)
   - `gate-cli news events get-latest-events --coin {symbol} --time-range 7d --limit 15 --format json` (optional)
3. Section 4 is expanded; MUST keep fact events and community views separated (see [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md) rule 7).

## Anti-patterns

| User prompt | Do NOT route here |
|---|---|
| "Is SOL a scam" / "Is SOL contract safe" | NOT `single_coin`. Route to ``gate-info-risk``. |
| "Who is 0x...fd9...a" | NOT any `gate-info-research` playbook. Route to ``gate-info-web3`` for address-first intent. |
| "Why did BTC crash" | NOT `macro`. Route to ``gate-news-intel``. |
| "BTC price" only | Do NOT fire the full `single_coin` playbook. Run `gate-cli info marketsnapshot get-market-snapshot --symbol BTC --scope basic` only and answer in one line. |

## Degradation rules

- If a **required** command fails (e.g. `get-coin-info` returns error for `single_coin`), abort the playbook and surface the trimmed CLI error verbatim.
- If an **optional** command fails (news / sentiment), mark the corresponding section **no data** and continue.
- If `gate-cli preflight` returned `status: fallback_to_mcp`, emit `__FALLBACK__` and halt — a legacy wrapper takes over (not shipped this round).
