---
name: gate-info-research
version: "2026.4.18-1"
updated: "2026-04-18"
description: "Use this skill whenever the user wants Gate.info / Gate.news research via gate-cli: single-coin, market overview, multi-coin compare, TA, macro, or research+news. Trigger phrases include: analyze SOL, how is BTC, compare BTC and ETH, technical analysis, NFP impact, research with news. Info primary; news auxiliary. Delegate: gate-info-risk (safety), gate-info-web3 (on-chain primary), gate-news-intel (news-first). Aligned to gate-cli v0.5.2; no aggregate +shortcut."
---

# gate-info-research

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
→ Also read [info-news-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/info-news-runtime-rules.md) for **gate-info** and **gate-news** shared rules (tool degradation, report standards, security, routing).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

## CLI and playbook contract

1. Every CLI command in this skill MUST exist under `gate-cli v0.5.2`. Do not invent `+coin-overview` / `+market-overview` / other aggregate shortcuts. If a shortcut ships in a later CLI, it will be opt-in via the playbook's `cli_future_shortcut` field, not by editing this file.
2. Call `gate-cli info …` / `gate-cli news …` only as listed in [playbooks/gate-info-research.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-research.yaml). This primary skill does **not** call Gate MCP tools when preflight `route` is `CLI` (MCP is for legacy wrapper skills only).
3. Always pass `--format json` on data-collection commands. Never mix JSON and pretty output in the same pipeline.
4. If a required slot (e.g. `symbol` for `single_coin`) cannot be parsed with high confidence, ask the user to clarify. Never guess a ticker from a project name.
5. Cross-domain allowed: `gate-info-research` MAY call `gate-cli news …` when the `research_plus_news` playbook fires. It MUST NOT take over user queries whose primary intent is news / events / community; those route to `gate-news-intel`.
6. Final user-facing reports may use the user’s locale; this `SKILL.md` stays English for discovery and indexing (see repository `CLAUDE.md` rule 1).

---

## Step 0 — Preflight

Follow the shared contract in [skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md) verbatim. Summary:

1. Run `gate-cli preflight --format json`; parse `.route`, `.status`, `.user_message`.
2. Branch: `CLI` → continue; `MCP_FALLBACK` → emit `__FALLBACK__` and halt; `BLOCK` → echo `user_message` and halt.
3. When `status == "ready_with_migration_warning"`, remember it — Step 3 appends one migrate hint at the end of the report.

Do NOT run the first data-collection command until Step 0 returns `route == "CLI"`.

---

<!--
Step 0.5 — Skill update check (OPT-IN, disabled by default).

The script [scripts/update-skill.sh](https://github.com/gate/gate-skills/blob/master/scripts/update-skill.sh) is shipped and functional, but agents
do NOT run it as part of the normal flow (zero overhead, no token needed).
Skill authors can still invoke it manually when they want to sync SKILL.md
from upstream:

    bash "$SKILL_ROOT/scripts/update-skill.sh" check gate-info-research

Result semantics, strict-check mode (`GATE_SKILL_CHECK_STRICT=1`) and the
auto-apply path (`GATE_SKILL_UPDATE_MODE=auto`) are documented in
[skills/_shared/update-workflow.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/update-workflow.md). To re-enable
this step inside the agent flow, delete this HTML comment wrapper so the
block becomes part of the rendered SKILL.md again.
-->

---

## Step 1 — Intent routing

Map the user's query to exactly one playbook id. Read the playbook definitions from [playbooks/gate-info-research.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-info-research.yaml). The mapping below is authoritative.

| Playbook id           | When to pick                                                                                   | Required slots | Legacy skill it covers                   |
|-----------------------|------------------------------------------------------------------------------------------------|----------------|------------------------------------------|
| `single_coin`         | "analyze SOL", "how is BTC", "is ETH worth watching", no explicit extra dimension.             | `symbol`       | `gate-info-coinanalysis`                 |
| `market_overview`     | "market right now", "how is the broad market", "which sectors are hot", no specific coin.                 | —              | `gate-info-marketoverview`               |
| `multi_coin`          | "compare BTC and ETH", "BTC vs SOL vs ARB", 2–20 tickers.                                      | `symbols`      | `gate-info-coincompare`                  |
| `trend`               | "give me a technical analysis of BTC", "SOL RSI / MACD", "BTC price direction / TA view".                          | `symbol`       | `gate-info-trendanalysis`                |
| `macro`               | "impact of NFP on BTC", "CPI impact on markets", "Fed rate decision and crypto".                                     | —              | `gate-info-macroimpact`                  |
| `research_plus_news`  | "analyze SOL and also check recent news and sentiment", "analysis plus sentiment / news".                | `symbol`       | multi-legacy fan-out                     |

### Slot extraction rules

- `symbol` is the ticker (`BTC`, `ETH`, `SOL`). If the user gives a project name ("Solana", "Arbitrum"), confirm or ask.
- `symbols` is a list; strip duplicates; keep display casing consistent.
- `time_range` is the user's broad news-context window. PER-COMMAND ENUM narrowing — the super-set is `1h / 24h / 7d / 30d`, but individual commands accept narrower sets. Before forwarding a user-supplied `time_range` to any command, clamp it against that command's `arg_enums` in the playbook (CLAUDE.md rule 9): `search-news` accepts `1h / 24h / 7d / 30d`, `search-ugc` accepts `1h / 24h / 7d / 30d / all`, **`get-social-sentiment` and `get-latest-events` accept ONLY `1h / 24h / 7d`** (CLI rejects `30d` with `INVALID_ARGUMENTS`). For longer windows on `get-latest-events`, switch to `--start-time` / `--end-time` (unix-ms).
- `period` (the **analysis window** consumed by `markettrend get-technical-analysis --period` and `get-kline --period`). Server enum: `1h / 4h / 24h / 3d / 5d / 7d / 10d / all`. Default `3d`. Legacy aliases `1d` → use `24h`; `1w` → use `7d`. Do NOT pass `1d` or `1w` — CLI returns `INTEL_RESULT_ERROR: invalid period`.
- `timeframe` has two variants:
  - `get-kline --timeframe` enum: `1m / 5m / 15m / 1h / 4h / 1d` (required, no default).
  - `get-market-snapshot --timeframe` and `get-indicator-history --timeframe` enum: `15m / 1h / 4h / 1d` (get-market-snapshot default `1h`; get-indicator-history required). `1m` / `5m` are NOT valid on these two.
- `indicators` (for `trend`) defaults to `rsi,macd,ma30,ma200` — **lowercase only**. Uppercase (`RSI`, `MACD`) passes CLI validation but the server returns empty rows silently. Unsupported windows (`ma20`, `ma50`) also return empty rows — use the server-populated set: `rsi`, `macd`, `macd_difference`, `ma7`, `ma30`, `ma120`, `ma200`, `ema7`, `ema30`, `ema200`, `boll_upper_band`, `boll_middle_band`, `boll_lower_band`. See [skills/gate-info-research/references/cli-reference.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-research/references/cli-reference.md) (section `get-indicator-history`) for the full field list.
- If a required slot is missing, STOP and ask the user.

### Cross-skill routing at Step 1

| User signal                                                                                     | Route to                              |
|-------------------------------------------------------------------------------------------------|---------------------------------------|
| "is this coin / contract / address safe", "honeypot / blacklist / has risk" (safety-first).                               | `gate-info-risk` (primary; ship round 1).      |
| "who is this address", "smart money", "whale", "DeFi TVL", "protocol metrics", "exchange reserves". | `gate-info-web3` (primary) |
| "why did BTC crash", "latest news", "community view", "Reddit", "YouTube".                       | `gate-news-intel` (primary) |

---

## Step 2 — Data collection

Execute the chosen playbook. Each command MUST include `--format json`. Commands in the same `parallel_group` run concurrently; the agent waits for the group before entering the next group or synthesis.

### 2.A `single_coin`

| Command                                                   | Required args                        | Notes |
|-----------------------------------------------------------|--------------------------------------|-------|
| `gate-cli info coin get-coin-info`                        | `--query {symbol} --scope full`      | Fundamentals, sector, tokenomics, investors. |
| `gate-cli info marketsnapshot get-market-snapshot`        | `--symbol {symbol} --scope full`     | Price, 24h / 7d change, OI, funding, sentiment bundle. |
| `gate-cli info markettrend get-technical-analysis`        | `--symbol {symbol}`                  | Multi-timeframe bull / bear / neutral. |
| `gate-cli news feed search-news` *(optional)*             | `--coin {symbol} --limit 5 --sort-by importance --time-range 24h` | Top 5 news. |
| `gate-cli news feed get-social-sentiment` *(optional)*    | `--coin {symbol} --time-range 24h`   | Social polarity + mention volume. |

### 2.B `market_overview`

| Command                                           | Required args                                     |
|---------------------------------------------------|---------------------------------------------------|
| `gate-cli info marketsnapshot get-market-overview` | (no flags)                                       |
| `gate-cli info coin get-coin-rankings`             | `--ranking-type popular --limit 20`              |
| `gate-cli info coin get-coin-rankings`             | `--ranking-type top_gainers --time-range 24h --limit 10` |
| `gate-cli info coin get-coin-rankings`             | `--ranking-type top_losers  --time-range 24h --limit 10` |

### 2.C `multi_coin`

Run once:

- `gate-cli info marketsnapshot batch-market-snapshot --symbols {s1} --symbols {s2} … --scope full` (the `--symbols` flag is a repeatable stringArray).

Then run per symbol in parallel:

- `gate-cli info coin get-coin-info --query {symbol} --scope basic`
- `gate-cli info markettrend get-technical-analysis --symbol {symbol}` *(optional)*

### 2.D `trend`

- `gate-cli info markettrend get-technical-analysis --symbol {symbol} --period {period|3d}`
- `gate-cli info markettrend get-kline --symbol {symbol} --timeframe {timeframe|1d} --size 120 --with-indicators true`
- `gate-cli info markettrend get-indicator-history --symbol {symbol} --timeframe {timeframe|1d} --indicators rsi --indicators macd --indicators ma30 --indicators ma200 --limit 120`

### 2.E `macro`

- `gate-cli info macro get-macro-summary`
- `gate-cli info macro get-economic-calendar --start-date {today} --end-date {today+14d} --importance high`
- `gate-cli info macro get-macro-indicator --indicator {indicator|CPI} --country {country|US} --mode series --size 12` *(optional)*
- If the user names a coin, also: `gate-cli info marketsnapshot get-market-snapshot --symbol {symbol} --scope basic`.

### 2.F `research_plus_news`

Run everything from `single_coin` **plus** (parallel):

- `gate-cli news feed search-news --coin {symbol} --limit 10 --sort-by importance --time-range {time_range|24h}`
- `gate-cli news feed get-social-sentiment --coin {symbol} --time-range {time_range|24h}` — clamp `time_range` to `1h / 24h / 7d` before sending
- `gate-cli news feed search-ugc --coin {symbol} --time-range {time_range|7d} --platform all --limit 20` *(optional)*
- `gate-cli news events get-latest-events --coin {symbol} --time-range {time_range|7d} --limit 15` *(optional)* — clamp `time_range` to `1h / 24h / 7d` before sending

### Failure policy

- If a **required** command fails or returns an error payload, abort the playbook and surface the user-actionable CLI error.
- If an **optional** command fails, continue and mark the corresponding section as **no data** in Step 3.
- Never fabricate numbers; never fill a missing dimension with inferred values.

---

## Step 3 — Synthesis

Aggregate the JSON payloads into the fixed 6-section report. Section order is mandatory and matches the product requirements spec.

### Report template

```markdown
## {subject} — Research report

### 1. Executive summary
- Core view (neutral framing: **stronger / softer / needs monitoring**; not investment advice)
- Up to 3 supporting data points
- Up to 2 main risk observations

### 2. Fundamentals and market position
{Positioning, sector, valuation (MC / FDV), funding / investors, unlocks. Sources: `info coin get-coin-info`.}

### 3. Market and trend
**Snapshot**
| Field | Value | Read |
|------|------|------|
| Price | ... | ... |
| 24h / 7d change | ... | ... |
| Funding | ... | ... |
| Sentiment / fear-greed | ... | ... |

**Technicals**
- Short term (1h / 4h): {bull / bear / neutral}
- Medium term (1d / 1w): {bull / bear / neutral}
- Key support / resistance: ...

Sources: `get-market-snapshot`, `get-technical-analysis`, `get-kline`, `get-indicator-history`, `get-market-overview`, `get-coin-rankings`, `batch-market-snapshot`, `get-macro-summary`, `get-economic-calendar`, `get-macro-indicator` as applicable to the chosen playbook.

### 4. Recent news and market tone
- **Factual events** (from `news feed search-news` / `news events get-latest-events`): ...
- **Community tone** (from `news feed get-social-sentiment` / `news feed search-ugc`): ...

Keep facts and community tone in separate subsections. If no news commands ran, mark **no data** for this section.

### 5. Risk notes
- Data-backed risk bullets (e.g. elevated RSI, near-term unlock, extreme funding, related incidents)
- Cite the originating command for each item

### 6. What to watch next
- Macro / unlock / protocol events in the next 7–14 days
- Technical triggers (e.g. “if price loses X, bias turns weaker”)

> This report is based on public data and tool output; it is not investment advice.
```

### Decision thresholds (applied inside section 3 and 5)

| Condition                                                                             | Flag in report                                            |
|---------------------------------------------------------------------------------------|-----------------------------------------------------------|
| RSI > 70 (latest row of `get-indicator-history`)                                      | "RSI overbought — elevated short-term pullback risk"      |
| RSI < 30                                                                              | "RSI oversold — potential bounce"                         |
| 24h volume > 2× 7d avg volume                                                         | "Significant volume surge"                                |
| 24h volume < 0.5× 7d avg volume                                                       | "Notable volume decline"                                  |
| `funding_rate` > 0.05% (from `get-market-snapshot`)                                   | "High funding rate — long crowding"                       |
| `funding_rate` < -0.05%                                                               | "Negative funding rate — short crowding"                  |
| Fear & Greed > 75                                                                     | "Extreme Greed — exercise caution"                        |
| Fear & Greed < 25                                                                     | "Extreme Fear — potential opportunity"                    |
| Upcoming token unlock within 30 days > 5% of circulating supply (from `get-coin-info`) | "Large upcoming token unlock — potential sell pressure"   |

### Migrate hint (only if Step 0 status was `ready_with_migration_warning`)

At the very end of the final user-facing report, append **verbatim** the single migration blockquote line defined under **Migration hint** in [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md) (the line that begins with `⚙️` and references `gate-cli migrate --dry-run`). Do not paraphrase.

---

## Cross-skill routing + Safety rules

### Routing

Follow the shared matrix in [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md). Research-skill-specific follow-ups:

| Follow-up intent                               | Target                                                           |
|------------------------------------------------|------------------------------------------------------------------|
| "is it safe", "honeypot", "blacklist", "compliance"        | `gate-info-risk` (primary)                          |
| "trace this address", "smart money", "whale"   | `gate-info-web3` (primary)                          |
| "why did it crash", "community take"                 | `gate-news-intel` (primary)                         |
| "only need the technical read"                 | Re-enter `trend` playbook                                        |
| "only need the latest news feed"               | Re-enter `research_plus_news` with `time_range 24h`              |

### Safety rules

Follow the shared contract in [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md). Research-specific reminders:

1. No buy / sell advice — strongest allowed phrasing is **stronger / softer / needs monitoring** (neutral).
2. No specific price targets.
3. Every section cites at least one command id from Step 2 (sources are named in the playbook's `report_sections[*].source_commands`).
4. Missing data → mark **no data**; never fabricate.

---

## References

| File | Load when... |
|---|---|
| [skills/gate-info-research/references/scenarios.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-research/references/scenarios.md) | Unsure which playbook id to pick. Each row maps a concrete prompt to a playbook + expected behavior. |
| [skills/gate-info-research/references/cli-reference.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-research/references/cli-reference.md) | You need a full flag table (types / required / defaults) for any `gate-cli info` or `gate-cli news` command this skill uses. |
| [skills/gate-info-research/references/troubleshooting.md](https://github.com/gate/gate-skills/blob/master/skills/gate-info-research/references/troubleshooting.md) | A command failed, a slot is ambiguous, or a report-integrity rule might be about to break. |
| [skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md) | Step 0 contract (verbatim snippet + 5-status matrix). |
| [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md) | Cross-skill routing matrix. |
| [skills/_shared/report-style.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/report-style.md) | Safety + report-format rules shared across all primaries. |
| [skills/_shared/update-workflow.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/update-workflow.md) | Skill update check/apply workflow. |
