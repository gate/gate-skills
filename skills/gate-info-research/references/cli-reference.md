# gate-info-research — CLI Command Reference

> Full flag tables for every `gate-cli` command this skill invokes. Verified against `gate-cli dev` (post-v0.5.2, enum/default metadata expansion). Aspirational aggregate shortcuts (`+coin-overview`, etc.) are NOT listed — see ``docs/gate-cli-commands-summary.md`` for the repo-wide rule.
>
> All flags below are real on this version of the CLI; agents MUST pass `--format json` on every data-collection call. Enum and default values below are copied verbatim from `gate-cli <cmd> --help`.

## Info · coin

### `gate-cli info coin get-coin-info`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--query` | string | ✅ | Ticker (`BTC`), project name (`Solana`), or contract address (`0x...`). |
| `--query-type` | string |  | Enum: `address / auto / gate_symbol / name / project / source_id / symbol`. Default `auto`. Pass `symbol` (not "ticker"), `address` (not "contract_address"). |
| `--chain` | string |  | Needed when `--query-type=address` and you want a specific chain. |
| `--scope` | string |  | Enum: `basic / detailed / full / with_project / with_tokenomics`. Default `basic`. `full` includes project + tokenomics + unlock. |
| `--size` | int |  | Default `10`, max `100`. |
| `--symbol` | string |  | Alias for `--query` when the value is strictly a ticker. |
| `--fields` | stringArray |  | Projection on returned columns. |

### `gate-cli info coin get-coin-rankings`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--ranking-type` | string | ✅ | Enum: `popular / top_gainers / top_losers / twitter_hot / airdrop / new_listing`. **Use `top_gainers` / `top_losers` — `gainers` / `losers` are INVALID** (CLI returns `INVALID_ARGUMENTS`). |
| `--time-range` | string |  | Enum: `1h / 24h / 7d`. Only meaningful for `top_gainers` / `top_losers`. No `30d` option. |
| `--limit` | int |  | Default `50`, max `100`. |
| `--listing-from`, `--listing-query`, `--listing-tickers` | various |  | Advanced filters for listing-style boards. |

### `gate-cli info coin search-coins`

Not called directly by the playbook, but available for slot clarification. Known enums: `--asset-type: all|crypto|tradefi` (default `crypto`); `--sort-by: circulating_supply|fdv|market_cap` (default `market_cap`); `--limit` default `20`, max `100`.

## Info · marketsnapshot

### `gate-cli info marketsnapshot get-market-snapshot`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--symbol` | string | ✅ | Ticker. |
| `--quote` | string |  | Quote currency, default `USDT`. |
| `--scope` | string |  | Enum: `basic / detailed / full`. Default `basic`. `full` returns kline + indicators bundle and project_info. |
| `--source` | string |  | Enum: `alpha / future / futures / fx / spot`. Default `spot`. |
| `--timeframe` | string |  | Enum: `15m / 1h / 4h / 1d`. Default `1h`. **`1m` / `5m` are NOT valid** on this endpoint (they are valid for `get-kline`). |
| `--indicator-timeframe` | string |  | Enum: `15m / 1h / 4h / 1d`. Override embedded indicators timeframe. |

### `gate-cli info marketsnapshot get-market-overview`

No required flags. Returns total market cap, volume, dominance, fear & greed. Used by `market_overview` playbook.

### `gate-cli info marketsnapshot batch-market-snapshot`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--symbols` | stringArray | ✅ | Repeat the flag per symbol (`--symbols BTC --symbols ETH`). **`maxItems=20`** per request. |
| `--scope` | string |  | Enum: `basic / detailed / full`. Default `basic`. |
| `--source` | string |  | Enum: `alpha / future / futures / fx / spot`. Default `spot`. |
| `--timeframe` | string |  | Enum: `15m / 1h / 4h / 1d`. Default `1h`. |
| `--quote` | string |  | Quote currency, default `USDT`. |

## Info · markettrend

### `gate-cli info markettrend get-technical-analysis`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--symbol` | string | ✅ | Ticker. |
| `--period` | string |  | Enum: `1h / 4h / 24h / 3d / 5d / 7d / 10d / all`. Default `3d`. **`1d` and `1w` are INVALID** — substitute `24h` and `7d` respectively (CLI returns `INTEL_RESULT_ERROR: invalid period`). The returned `timeframes` bundle always covers `15m / 1h / 4h / 1d` regardless of the selected window. |
| `--start-time`, `--end-time` | string |  | Override the analysis window. ISO-8601 or unix-ms per CLI help. |

### `gate-cli info markettrend get-kline`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--symbol` | string | ✅ | Ticker. |
| `--timeframe` | string | ✅ | Enum: `1m / 5m / 15m / 1h / 4h / 1d`. This is the ONLY markettrend shortcut that accepts `1m` / `5m`. |
| `--period` | string |  | Enum: `1h / 4h / 24h / 3d / 5d / 7d / 10d / all`. Default `24h`. |
| `--size` | int |  | Default `100`, max `2000`. |
| `--limit` | int |  | Default `100`, max `2000`. |
| `--with-indicators` | flexBool |  | `true` to include RSI/MACD/BOLL/MA/EMA bundled on each row. |
| `--start-time`, `--end-time` | string |  | Fine-grained window control. |

### `gate-cli info markettrend get-indicator-history`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--symbol` | string | ✅ | Ticker. |
| `--timeframe` | string | ✅ | Enum: `15m / 1h / 4h / 1d`. **Narrower than `get-kline`** — no `1m` / `5m`. |
| `--indicators` | stringArray | ✅ | ES `_source` field names — **lowercase ONLY**. Server-populated fields: `rsi`, `macd`, `macd_difference`, `ma7`, `ma30`, `ma120`, `ma200`, `ema7`, `ema30`, `ema200`, `boll_upper_band`, `boll_middle_band`, `boll_lower_band`, `adx`, `cci`, `sar`, `wr`, `di_plus`, `di_minus`. Uppercase (`RSI`, `MACD`) passes validation but returns empty rows silently. Unsupported windows (`ma20`, `ma50`) also return empty rows — pick from the populated set above. |
| `--limit` | int |  | Default `100`, max `500`. |
| `--start-time`, `--end-time` | string |  | Window override. |

## Info · macro

### `gate-cli info macro get-macro-summary`

No required flags. Zero-arg dashboard of key indicators + upcoming releases.

### `gate-cli info macro get-economic-calendar`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--start-date` | string |  | `YYYY-MM-DD`. Defaults to today. |
| `--end-date` | string |  | `YYYY-MM-DD`. |
| `--importance` | string |  | `low` / `medium` / `high`. |
| `--event-type` | string |  | Category filter. |
| `--size` | int |  | Default `50`, max `200`. |

### `gate-cli info macro get-macro-indicator`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--indicator` | string | ✅ | `CPI`, `PPI`, `NFP`, `FEDRATE`, `UNEMP`, ... |
| `--country` / `--country-code` | string |  | `US`, `CN`, `EU`, `JP`, ... (`--country-code` takes the ISO code). |
| `--mode` | string |  | `snapshot` / `series`. |
| `--size` | int |  | Series length (when `--mode series`). |
| `--start-date`, `--end-date`, `--start-time`, `--end-time` | various |  | Either date-style or timestamp-style bounds. |

## News · feed (auxiliary, for `research_plus_news`)

### `gate-cli news feed search-news`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--coin` | string |  | Ticker filter. Prefer over `--query` when subject is a coin. |
| `--query` | string |  | Free-text search. |
| `--limit` | int |  | Default `10`, max `100`. |
| `--page` | int |  | Default `1`. |
| `--sort-by` | string |  | Default `time`. Known accepted values: `time`, `importance`, `similarity_score`. No enum constraint at CLI level. |
| `--time-range` | string |  | Enum: `1h / 24h / 7d / 30d`. Default `24h`. |
| `--lang` | string |  | `zh` / `en`. Omit to let the server decide. |
| `--platform` / `--platform-type` | string |  | Narrow by news source. |
| `--similarity-score` | string |  | Upstream default ~`0.6` when `--query` is non-empty. |

### `gate-cli news feed get-social-sentiment`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--coin` | string |  | Ticker. Default `BTC` (be explicit to avoid server-side default). |
| `--time-range` | string |  | Enum: `1h / 24h / 7d`. Default `24h`. |

### `gate-cli news feed search-ugc`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--coin` | string |  | Ticker. |
| `--query` | string |  | Free-text. Coin + empty query is valid (hits OpenSearch path). |
| `--platform` | string |  | Enum: `all / discord / reddit / telegram / youtube`. Default `all`. |
| `--domain` | string |  | Enum: `ai_agent / all / crypto / defi / finance / macro / web3_dev`. Default `all`. |
| `--time-range` | string |  | Enum: `1h / 24h / 7d / 30d / all`. Default `7d`. |
| `--limit` | int |  | Default `10`, max `50`. |
| `--sort-by` | string |  | Enum: `recent / relevance / upvotes`. Default `relevance`. |
| `--quality-tier` | string |  | Enum: `A / B / all`. Default `A`. |

### `gate-cli news feed get-exchange-announcements`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--coin` | string |  | Ticker. |
| `--exchange` | string |  | Narrow to a specific venue. |
| `--announcement-type` | string |  | Enum: `all / delisting / listing / maintenance`. |
| `--limit` | int |  | Max `100`. |

## News · events (auxiliary, for `research_plus_news`)

### `gate-cli news events get-latest-events`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--coin` | string |  | Ticker. |
| `--time-range` | string |  | Enum: `1h / 24h / 7d`. **No `30d`** — for longer windows fall back to `--start-time` / `--end-time` (unix-ms). |
| `--event-type` | string |  | Category filter: `unlock`, `mainnet`, `funding`, `exploit`, `rug`, `depeg`, etc. |
| `--limit` | int |  | Default `20`, max `100`. |
| `--start-time`, `--end-time` | string |  | Window override. |

## Global flags (any `gate-cli info|news` command)

| Flag | Notes |
|---|---|
| `--format json` | **Required** on every data-collection call in this skill. |
| `--max-output-bytes N` | Cap response size (`0` = unlimited). |
| `--verbose` | Print transport lines to stderr (useful for debugging, does not change stdout JSON). |
| `--debug` | HTTP debug summary. Never redirect this to the user verbatim — may contain auth headers. |
| `--api-key` / `--api-secret` | Override auth. **NEVER** surface in user-facing output. |
| `--profile` | CLI profile; the skill inherits whatever the user selected. |

## Invoke fallback

Every shortcut above also works via:

```bash
gate-cli info invoke --name <tool_name> --params '{"key":"value"}' --format json
```

Use this only when a flag renaming edge case breaks the shortcut form — otherwise the shortcut form is preferred because it validates required args at parse time.
