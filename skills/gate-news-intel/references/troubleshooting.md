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
