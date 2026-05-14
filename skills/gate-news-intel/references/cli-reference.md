# gate-news-intel — CLI reference

> Verify flags with `gate-cli news feed <cmd> --help` / `gate-cli news events <cmd> --help` / `gate-cli info <group> <cmd> --help` on **gate-cli v0.5.2**. Always add `--format json` for collection calls.

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

## Not used as hard dependencies

`news +brief`, `news +event-explain`, `news +community-scan`, `info +market-overview`, `info +coin-overview` — see playbook `cli_future_shortcut`.
