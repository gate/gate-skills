# gate-news-intel

## Overview

Primary **news and intelligence** skill for `gate-cli news`, with optional `gate-cli info` for market or coin context when the playbook says so. Covers briefings, event explanation, **market move attribution** (via `explain-market-move`), exchange announcements/listings, UGC and cross-platform social (X, Reddit, YouTube via `search-ugc` / `search-x`), and social sentiment — aligned to v0.5.2 **without** relying on unshipped shortcuts (`+brief`, `+event-explain`, `+community-scan`, `+market-overview`, `+coin-overview`).

## Runtime requirements

- **CLI**: `gate-cli` v0.5.2 on `PATH`.
- **Shell** (optional): for packaged `scripts/update-skill.*` only.
- **Network / auth**: per your `gate-cli` and preflight configuration.

## Core capabilities

| Capability | Typical trigger | Playbook id |
|------------|-----------------|-------------|
| News briefing | "what happened recently" (with a ticker) | `news_brief` |
| Event / pure timeline | "what events happened" | `event_explain` |
| **Market move attribution** | "why did BTC crash", "why pump", "market move reason" | `market_move_explain` |
| Listings / announcements | "new listings", "exchange announcements" | `exchange_listings` |
| Community / UGC / X / sentiment first | "community take", "Reddit", "YouTube" | `community_intel` |
| News + market or coin background | "news plus market context" | `intel_plus_market` |
| Market-wide without a ticker | "what is happening in crypto broadly" | `market_wide_intel` |

## Inputs / outputs

- **Input**: natural language + slots per playbook (`symbol`, `query`, `time_range`, optional `event_id`, `topic_query`). `query` is required for `market_move_explain`; coin fallback defaults to BTC for broad-market queries with a notice.
- **Output**: five-section intel briefing report or six-section market move analysis report (see `SKILL.md` for both templates).

## Routing (when NOT to use)

| Intent | Route to |
|--------|----------|
| Investment research, fundamentals, TA, macro | `gate-info-research` |
| On-chain / protocol / address behavior | `gate-info-web3` |
| Safety / compliance verdict | `gate-info-risk` |

Full matrix: [skills/_shared/routing.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/routing.md).

## Acceptance criteria

1. Preflight contract ([skills/_shared/preflight.md](https://github.com/gate/gate-skills/blob/master/skills/_shared/preflight.md)).
2. Every command appears under `gate-cli news list` / `gate-cli info list` for the documented baseline.
3. Facts vs community opinions are separated; UGC/X/sentiment are first-class when the playbook includes those tools.
4. Optional `info` failures do not block the news-led report.

## Source

- [SKILL.md](https://github.com/gate/gate-skills/blob/master/skills/gate-news-intel/SKILL.md)
- [playbooks/gate-news-intel.yaml](https://github.com/gate/gate-skills/blob/master/playbooks/gate-news-intel.yaml) (repository root)
