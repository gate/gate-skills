# gate-news-intel — CLI reference

> Legacy leaves on **gate-cli v0.5.2+**. News aggregates ship in **v0.7.6+** — see [cli-version-routing.md](../../_shared/cli-version-routing.md).

## Aggregates (>= 0.7.6)

| Command | Flags | Playbook |
|---------|-------|----------|
| `gate-cli news +brief` | `--coin` or `--query`; `--time-range` (default `24h`) | `news_brief`, `intel_plus_market` |
| `gate-cli news +event-explain` | `--event-id` when slot set; else `--coin` + `--time-range` | `event_explain` — `market_interpretation` = search-x, not sentiment |
| `gate-cli news +community-scan` | `--coin` (ticker) or `--query`; `--time-range` | `community_intel`, `token_onchain_social` |
| `gate-cli info +coin-overview` | `--symbol` | `intel_plus_market` (`info_shortcut`) |
| `gate-cli info +market-overview` | optional `--benchmark` | `market_wide_intel` |

`market_move_explain` still uses `news events explain-market-move` (no `+market-move-explain` in v0.7.6).

## News — feed

| Command | Role |
|---------|------|
| `gate-cli news feed search-news` | Headlines and articles |
| `gate-cli news feed get-social-sentiment` | Polarity / mentions |
| `gate-cli news feed search-ugc` | Reddit, Discord, Telegram, YouTube UGC |
| `gate-cli news feed search-x` | X/Twitter discussion |
| `gate-cli news feed get-exchange-announcements` | Official exchange notices |
| `gate-cli news feed web-search` | Open-web bundle |

## News — events

| Command | Role |
|---------|------|
| `gate-cli news events get-latest-events` | Event timeline |
| `gate-cli news events get-event-detail` | Single event by id |
| `gate-cli news events explain-market-move` | Market move attribution: Tavily real-time search + internal event pool. Flags: `--query` (required, user question), `--coin` (required), `--time-range` (enum: `30m`/`1h`/`2h`/`4h`/`24h`, default `2h`). Returns `summary`, `latest_news[]`, `supporting_events[]`, `data_status`. |

## Info (optional, intel_plus_market / market_wide)

| Command | Role |
|---------|------|
| `gate-cli info marketsnapshot get-market-overview` | Broad market snapshot |
| `gate-cli info coin get-coin-info` | Coin profile |
| `gate-cli info marketsnapshot get-market-snapshot` | Per-symbol snapshot |
| `gate-cli info markettrend get-technical-analysis` | TA signal |

## Legacy-only path (< 0.7.6)

When `shortcuts_enabled` is false, use the leaf commands in the tables above instead of the Aggregates section. `explain-market-move` has no aggregate shortcut in v0.7.6.
