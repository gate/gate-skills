# gate-news-intel — Troubleshooting

## `get-exchange-announcements` requires `--coin`

If the CLI errors without `--coin`, ask the user for a listing scope (asset or “global” if supported) or narrow the question.

## `get-event-detail` without `event_id`

Do not invoke `get-event-detail` with an empty id — rely on `get-latest-events` + `search-news`.

## `web-search` parameter name

Confirm the query flag via `gate-cli news feed web-search --help` (may be `--query` or similar).

## MCP fallback (`preflight` → `MCP_FALLBACK`)

Primary skills in this repo emit `__FALLBACK__`; actual MCP execution is for legacy wrappers — do not invent MCP tools from `gate-news-intel` when route is `CLI`.

## “What happened recently” without a symbol

Use `market_wide_intel` or ask which asset to focus — do not guess a ticker.

## explain-market-move time_range mismatch

The valid --time-range for explain-market-move is 30m / 1h / 2h / 4h / 24h (default 2h). The global slot default of 24h / 7d / 30d does NOT apply here. The playbook enforces this via arg_enums. If the user provides an unsupported value outside the enum, reject it and tell the user the supported values.

## explain-market-move data_status.is_partial

When the response has data_status.is_partial = true, the report footer MUST include the degraded-data notice: "Partial data: {data_status.note}". List any missing_sources if available. Do NOT hide this from the user -- it impacts the reliability of the attribution.

## Companion command failure in market_move_explain

If get-market-snapshot, get-orderbook, get-technical-analysis, get-coin-info, search-x, or get-social-sentiment fail during market_move_explain: mark the corresponding report section as "unavailable" and continue. Only explain-market-move failure is fatal (or if both explain-market-move and all companions fail).

## Coin fallback for market move queries

When the user asks about market moves without naming a coin: broad-market / general market queries default to BTC with a notice; vague references like "this coin" require asking the user; traditional finance names (e.g. S&P 500) are passed through as the coin value.
