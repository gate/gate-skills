# gate-news-intel

## Overview

Primary **news and intelligence** skill for `gate-cli news`, with optional `gate-cli info` for market or coin context when the playbook says so. Covers briefings, event explanation, **market move attribution** (via `explain-market-move`), exchange announcements/listings, UGC and cross-platform social (X, Reddit, YouTube via `search-ugc` / `search-x`), and social sentiment.

**CLI paths**: legacy leaf commands align to **v0.5.2+**. Aggregate shortcuts (`news +brief`, `+event-explain`, `+community-scan`; `info +market-overview`, `+coin-overview` where the playbook adds info context) ship in **v0.7.6+** and are used when `shortcuts_enabled` (see [skills/_shared/cli-version-routing.md](../_shared/cli-version-routing.md)). Below 0.7.6, playbooks fall back to multi-step legacy `commands` only.

## Runtime requirements

- **CLI**: `gate-cli` on `PATH` — v0.5.2+ for legacy; **v0.7.6+** recommended for shortcut paths.
- **Shell** (optional): for packaged `scripts/update-skill.*` only.
- **Network / auth**: per your `gate-cli` and preflight configuration.

## Core capabilities

| Capability | Typical trigger | Playbook id | Shortcut (>= 0.7.6) |
|------------|-----------------|-------------|---------------------|
| News briefing | "what happened recently" (with a ticker) | `news_brief` | `news +brief` |
| Event / pure timeline | "what events happened" | `event_explain` | `news +event-explain` |
| **Market move attribution** | "why did BTC crash", "why pump", "market move reason" | `market_move_explain` | *(no shortcut in v0.7.6)* |
| Listings / announcements | "new listings", "exchange announcements" | `exchange_listings` | — |
| Community / UGC / X / sentiment first | "community take", "Reddit", "YouTube" | `community_intel` | `news +community-scan` |
| News + market or coin background | "news plus market context" | `intel_plus_market` | `news +brief` then `info +coin-overview` |
| Market-wide without a ticker | "what is happening in crypto broadly" | `market_wide_intel` | `info +market-overview` (+ legacy `web-search`) |

## Inputs / outputs

- **Input**: natural language + slots per playbook (`symbol`, `query`, `time_range`, optional `event_id`, `topic_query`). `query` is required for `market_move_explain`; coin fallback defaults to BTC for broad-market queries with a notice.
- **Output**: five-section intel briefing report or six-section market move analysis report (see `SKILL.md` for both templates).

## Routing (when NOT to use)

| Intent | Route to |
|--------|----------|
| Investment research, fundamentals, TA, macro | `gate-info-research` |
| On-chain / protocol / address behavior | `gate-info-web3` |
| Safety / compliance verdict | `gate-info-risk` |

Full matrix: [skills/_shared/routing.md](../_shared/routing.md).

## Acceptance criteria

1. Preflight contract ([skills/_shared/preflight.md](../_shared/preflight.md)); Step 0.5 sets `shortcuts_enabled` when `cli_version >= 0.7.6`.
2. Legacy commands appear under `gate-cli news list` / `gate-cli info list`; shortcuts validated via `--help` (not listed as MCP leaves).
3. Shortcut success: parse **top-level** JSON payload on stdout (not `.data.*` on default binary); failures use stderr `{"error":…}`.
4. Facts vs community opinions are separated; UGC/X/sentiment are first-class when the playbook includes those tools.
5. Optional `info` failures do not block the news-led report.

## Source

- [SKILL.md](SKILL.md)
- [playbooks/gate-news-intel.yaml](../../playbooks/gate-news-intel.yaml)
- [skills/_shared/cli-version-routing.md](../_shared/cli-version-routing.md)
