---
name: gate-news-intel
version: "2026.5.13-1"
updated: "2026-05-13"
description: "Use this skill whenever the user’s main ask is news, events, listings, social/UGC, or market move attribution. Primary gate-cli news (optional info for market context). Covers briefings, event explain, market move attribution via explain-market-move, exchange announcements, UGC X/Reddit/YouTube, sentiment. Triggers: what happened, why crash, why pump, market move reason, new listings, community take. Delegate: gate-info-research (research-first), gate-info-web3 (on-chain), gate-info-risk (safety). v0.5.2; do not use unshipped +brief +event-explain +community-scan +market +coin shortcuts."
---

# gate-news-intel

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** and **gate-news** shared rules.
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

## CLI and playbook contract

1. **Primary boundary**: **news, events, announcements, and social/UGC intelligence**. Optional **`info`** calls appear only in playbooks that explicitly add market or coin background (`intel_plus_market`, `market_wide_intel`).
2. Every command MUST exist under **`gate-cli v0.5.2`**. Call only what is listed in [playbooks/gate-news-intel.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-news-intel.yaml). When preflight `route` is `CLI`, do **not** use Gate MCP from this skill.
3. Always pass **`--format json`** on data-collection commands.
4. **Separate fact from opinion**: label **facts** (dated events, official announcements, news wires) vs **community / UGC / X / social** (always cite source type: UGC, X, Reddit, YouTube, sentiment index).
5. **Synthesis order (PRD 5.6.7)**:
   - **“Why did it drop / crash?”** → causal **event chain first** (Section 2), then optionally market/coin background (Section 4).
   - **“How does the community see ...?”** → **Section 3 (community / UGC / X / sentiment) before** broad market overview (Section 4).
6. Final user-facing reports may use the user’s locale; this `SKILL.md` stays English for discovery (repository `CLAUDE.md` rule 1).

---

## Step 0 — Preflight

Follow [skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md) verbatim:

1. Run `gate-cli preflight --format json`; parse `.route`, `.status`, `.user_message`.
2. Branch: `CLI` → continue; `MCP_FALLBACK` → emit `__FALLBACK__` and halt (legacy MCP fallback is outside this repo’s primary skills); `BLOCK` → echo `user_message` and halt.
3. When `status == "ready_with_migration_warning"`, remember it — Step 3 appends one migrate hint at the end of the report.

4. **Version detection**: Run `gate-cli --version 2>&1` and extract the version number (e.g. `0.7.2` from `"gate-cli version 0.7.2 (build ...)"`). Store as `cli_version`. This is used in Step 1 to decide whether `market_move_explain` can use `explain-market-move` (requires v0.7.2+) or must fall back.

Do NOT run `news` / `info` data collection until `route == "CLI"`.

---

## Step 1 — Intent routing

Map the user query to **exactly one** playbook id from [playbooks/gate-news-intel.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-news-intel.yaml).

| Playbook id | When to pick | Required slots |
|-------------|----------------|----------------|
| `news_brief` | Headlines / “what happened recently” **with a named asset** | `symbol` |
| `event_explain` | Pure event timeline / detail lookup **without** price-move attribution | `symbol` |
| `market_move_explain` | “Why did X move / crash / pump / dump”, price-move attribution, market move reason | `symbol`, `query` |
| `exchange_listings` | Listings, delistings, maintenance, **announcements** | — |
| `community_intel` | “Community take”, Reddit, YouTube, X, social / sentiment (social-first) | `symbol` |
| `intel_plus_market` | User wants **news + market or coin background** | `symbol` |
| `market_wide_intel` | Broad “what is happening in crypto” **without** a ticker | — |

#### Version-dependent routing

`market_move_explain` requires `gate-cli` **v0.7.2+** (the earliest version that ships `explain-market-move`). The playbook's `cli_baseline` field documents this. All other playbooks remain compatible with v0.5.2.

**If routed to `market_move_explain` but `cli_version` < 0.7.2**: fall back to `event_explain` and include this notice in the report footer:
> explain-market-move requires gate-cli v0.7.2+. Falling back to event_explain with manual news/event stitching. Upgrade gate-cli for server-side Tavily-powered attribution with AI summary.

### Slot extraction

- `symbol`: ticker (`BTC`, `ETH`, ...). Ask if missing when the playbook requires it.
- `query`: user's original natural-language question, e.g. "Why did BTC surge?". Required for `market_move_explain`; extracted verbatim from the user's input.
- `time_range`: default `24h` / `7d` / `30d` for most playbooks; NARROWED to `30m` / `1h` / `2h` / `4h` / `24h` (default `2h`) for `market_move_explain` (see `arg_enums` in the playbook).
- `event_id`: only when the user references a concrete event for `get-event-detail`.
- `topic_query`: for `market_wide_intel` web search.

#### Coin fallback rules (market_move_explain)

When the user triggers `market_move_explain` but no coin is explicitly named:

1. **Explicit coin in query**: extract and use it (e.g. "ETH why crash" -> ETH).
2. **Context coin**: if the conversation has a unique coin, use it.
3. **Broad-market, no coin**: default to `BTC` and append a notice: "No coin specified; defaulting to BTC as the broad-market representative asset."
4. **Vague reference** ("this coin", "that altcoin"): ask the user which specific coin.
5. **Event impact, no coin**: ask the user which coin to analyze.
6. **Traditional finance** (e.g. "US stocks", "China A-shares", "S&P 500"): pass through as the `coin` value.
7. **Non-crypto, ambiguous**: ask the user or route to the appropriate domain skill.

When coin defaults to BTC, the notice MUST be visible in the final report (Section 1 of the market move template).

### Cross-skill routing at Step 1

| User signal | Route to |
|-------------|----------|
| “Is it safe / honeypot / blacklist” | `gate-info-risk` (primary) |
| “Trace this address / on-chain / TVL / reserves” | `gate-info-web3` (primary) |
| “Analyze this coin / fundamentals / technicals / macro” (research-first) | `gate-info-research` (primary) |

---

## Step 2 — Data collection

Execute the chosen playbook. Same `parallel_group` → concurrent; wait between groups.

**Shortcut fallbacks (not executed as literal commands)** — use the YAML command blocks; see `cli_future_shortcut` in the playbook for `+brief`, `+event-explain`, `+community-scan`, `+market-move-explain`.

**`exchange_listings`**: base invocation uses `limit` + `format` only; if the user supplied `symbol`, add `--coin {symbol}` when the CLI supports it (`get-exchange-announcements --help`).

**`event_explain`**: call `get-event-detail` **only** when `event_id` is known; otherwise omit that command. For price-move attribution queries, you should have already routed to `market_move_explain`.

**`market_move_explain`**: Execute in **two groups**:
- Group A (parallel, core data): `explain-market-move` (Tavily-based news/event evidence with AI summary) + `get-market-snapshot` (current price, change%, volume) + `get-orderbook` (bid/ask wall, depth imbalance).
- Group B (after Group A completes, parallel): `get-technical-analysis` (TA signals across timeframes) + `get-coin-info` (fundamentals) + community commands (`search-x` + `get-social-sentiment`) only when `symbol != BTC`. For BTC, skip community — Tavily already captures macro/geopolitical signals.

After data collection, the agent MUST perform its own final attribution synthesis using ALL collected data. Do not treat any single tool output as the authoritative conclusion. Prioritize events with higher `relevance_score` as primary drivers, cross-referencing with price/volume data from the snapshot and orderbook.

**Info failures**: In `intel_plus_market` and `market_move_explain`, info/community commands are **optional** — if they fail, mark that section as unavailable and still deliver the report.

---

## Step 3 — Synthesis

Choose the report template based on the playbook:

- **`market_move_explain`**: use the 6-section **Market move analysis** template below.
- **All other playbooks**: use the 5-section **Intel briefing** template below.

### Intel briefing template (all playbooks except market_move_explain)

Produce **five sections**, in this order:

```markdown
## Intel briefing -- {subject}

### 1. Event / news takeaway
- 3-5 bullets; separate **verified facts** from **unconfirmed** items

### 2. Key facts and timeline
- Time-ordered, verifiable items from `search-news` / `get-latest-events` / `get-event-detail` where used

### 3. Community / UGC / X / Reddit / YouTube
- **Must** cover, when the playbook includes them: UGC (`search-ugc`), X (`search-x`), and sentiment where applicable (`get-social-sentiment`)
- Label every bullet with **source type** (e.g. UGC / X / sentiment index) -- do not state opinion as on-chain fact

### 4. Market or coin background (if any)
- Only when the playbook includes `info` or `get-market-overview` in `market_wide_intel`; if not used, state **no extra market context**

### 5. Conclusion and what to watch
- Not investment advice; list follow-up items

> This report is based on public data and tool output; it is not investment advice.
```

### Market move analysis template (market_move_explain only)

Produce **six sections**, in this order:

```markdown
## Market move analysis -- {coin} ({time_range})

[If coin was defaulted to BTC, append: "No coin specified; defaulting to BTC as the broad-market representative asset."]

### 1. Summary
[One concise attribution sentence. Synthesize: explain-market-move outer summary,
supporting_events summaries, market snapshot change%, and TA signals.
Prefer events with higher relevance_score as primary drivers.
Do NOT copy-paste the entire Tavily summary verbatim -- distill the key narrative.]

### 2. Primary drivers
[2-4 latest_news items from explain-market-move. For each: title, how it likely drove
the move (from its summary field), source URL, relevance_score.
Sort by relevance_score descending. If relevance_score < 0.5, note it as weak signal.
The outer summary in explain-market-move is a concatenation of these items'
Tavily AI answers; cross-reference with individual item summaries for accuracy.]

### 3. Supporting context
[1-2 supporting_events from the internal event pool, with first_seen_time.
Pay special attention to supporting_events[].summary -- these come from the internal
event pool and are NOT included in the outer summary, making them independent evidence.
Market snapshot: current price, change%, volume.
Order book: notable bid/ask walls or depth imbalances that explain the move magnitude.]

### 4. Technical signals
[Key TA indicators from get-technical-analysis. Trend direction, support/resistance
levels, RSI/MACD crossovers if available. Coin fundamentals from get-coin-info
(market cap rank, supply, sector).]

### 5. Community perspective
[Non-BTC only. X highlights from search-x, sentiment score from get-social-sentiment.
Label each item with source type (X / sentiment index).
If BTC, state: "Community data omitted for BTC; macro/geopolitical signals are
captured in Sections 2 and 3."]

### 6. What to watch
[Follow-up catalysts, key price levels, upcoming events that could confirm or
reverse the current move.]

[If data_status.is_partial: append "Partial data notice: {note if available}.
Missing sources: {missing_sources if listed}."]

> This report is based on public data and tool output; it is not investment advice.
```

### Synthesis rules for market_move_explain

- The agent MUST perform its own final attribution -- do not treat any single tool output as authoritative.
- Cross-reference: the outer `summary` in explain-market-move is a concatenation of Tavily AI answers. `supporting_events[].summary` fields are independent evidence from the internal event pool. Both should inform the agent's attribution.
- `latest_news` items carry `relevance_score` (0-1). Prefer items above 0.5 as primary drivers; note weaker items as background context.
- Validate news-driven narratives against market snapshot price/volume data -- a large move without matching event evidence should be acknowledged as unexplained.

### Migrate hint

If Step 0 had `ready_with_migration_warning`, append **verbatim** the migration blockquote line from [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md) (line starting with `⚙️`).

---

## Cross-skill routing + Safety rules

### Routing

Follow [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md). Do not absorb **research / web3 / risk** primary intents into this skill. News-intel-specific follow-ups (after the briefing is delivered and the user asks a follow-up):

| Follow-up intent | Target |
|------------------|--------|
| "deeper research on this coin" / "is it worth attention" / "fundamentals / technicals / macro" | `gate-info-research` |
| "address from the event" / "what is on-chain" / "protocol TVL / reserves / smart money" | `gate-info-web3` |
| "is this token safe" / "honeypot" / "blacklist" / "compliance" | `gate-info-risk` |
| User changes `symbol` or time window and wants the same class of intel | Re-enter the same playbook with the new slots |

### Safety rules

Follow [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md). News-intel-specific:

1. No buy/sell advice; no price targets.
2. **Community and UGC are first-class** in Section 3 (not footnotes) when `community_intel` or relevant commands in other playbooks fire.
3. Never fabricate events or quotes — if empty, mark **no data**.

---

## References

| File | Load when... |
|------|------------|
| [skills/gate-news-intel/references/scenarios.md](https://github.com/gate/gate-skills/blob/master/skills/gate-news-intel/references/scenarios.md) | Picking among brief / event / community / listings / market-wide. |
| [skills/gate-news-intel/references/cli-reference.md](https://github.com/gate/gate-skills/blob/master/skills/gate-news-intel/references/cli-reference.md) | Flag tables for `news` and optional `info` commands. |
| [skills/gate-news-intel/references/troubleshooting.md](https://github.com/gate/gate-skills/blob/master/skills/gate-news-intel/references/troubleshooting.md) | Optional flags, `get-exchange-announcements` filters, empty `event_id`. |
| [skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md) | Step 0. |
| [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md) | Cross-skill matrix. |
| [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md) | Shared report rules. |
