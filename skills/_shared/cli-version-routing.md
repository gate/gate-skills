# Shared CLI Version Routing (gate-cli >= 0.7.6 shortcuts)

> Run immediately after the preflight route branch in Step 0 (`route == CLI`). Sets `cli_version` and `shortcuts_enabled` for Step 2 playbook execution.

## Why

- `gate-cli preflight` reports `cli_version` but has **no shortcut capability flag**.
- Aggregate shortcuts (`info +coin-overview`, `news +brief`, …) ship in **v0.7.6**. Skills MUST gate them deterministically — not by LLM guess.
- Below 0.7.6, every skill falls back to the legacy multi-step `commands` blocks in playbooks.

## Version source

Use `.cli_version` from the **same** `PREFLIGHT_JSON` blob — do not call `gate-cli --version` separately unless preflight omitted the field.

Strip a leading `v` before comparing (e.g. `v0.7.6` → `0.7.6`).

## Step 0.5 snippet (after preflight `CLI` branch)

```bash
CLI_VER=$(printf '%s' "$PREFLIGHT_JSON" | jq -r '.cli_version' | sed 's/^v//')
shortcuts_enabled=false

compare_version_ge() {
  local ver="$1" min="$2"
  local IFS=.
  local -a v=($ver) m=($min)
  local i
  for i in 0 1 2; do
    local vi=${v[$i]:-0} mi=${m[$i]:-0}
    if ((10#$vi > 10#$mi)); then return 0; fi
    if ((10#$vi < 10#$mi)); then return 1; fi
  done
  return 0
}

if compare_version_ge "$CLI_VER" "0.7.6"; then
  shortcuts_enabled=true
fi
```

Store `cli_version` and `shortcuts_enabled` for Step 1 / Step 2.

## Feature gates

| Threshold | Variable / use |
|-----------|----------------|
| `>= 0.7.6` | `shortcuts_enabled=true` → prefer playbook shortcut blocks when guards pass |
| `>= 0.7.2` | `market_move_explain` may call `news events explain-market-move` (gate-news-intel only) |
| `>= 0.6.0` | `preflight.version_ok` (doctor minimum; unrelated to shortcuts) |
| `< 0.7.6` | Legacy `commands` / `news_addons` / `additional_commands` only |

## Resolving shortcuts on `extends` playbooks

When a playbook has `extends: <parent_id>`, the orchestrator MUST collect shortcuts from:

1. Walk the `extends` chain (child → parent → …) and gather every `shortcut` block on ancestors.
2. Apply the current playbook’s `shortcut`, `additional_shortcut`, and `info_shortcut` (if any).
3. Optional explicit hint: `inherits_shortcuts_from: <parent_id>` (same as `extends` when both present).

**`extends` order**: run ancestor shortcuts **before** the child’s own blocks. Example `research_plus_news`: parent `single_coin.shortcut` (`info +coin-overview`) **then** child `additional_shortcut` (`news +brief`).

## Shortcut block order (same playbook)

When one playbook defines multiple shortcut blocks, run them in this **fixed key order** (independent blocks MAY run in parallel — order is for fallback/logging only):

1. `shortcut`
2. `additional_shortcut`
3. `info_shortcut`

Example `intel_plus_market`: `shortcut` (`news +brief`) **then** `info_shortcut` (`info +coin-overview`). Do **not** assume info-before-news unless using the `extends` rule above.

## Step 2 shortcut contract (all primary skills)

When **all** of the following hold:

1. `shortcuts_enabled == true`
2. Resolved shortcut list (see above) is non-empty and `min_cli_version: "0.7.6"` on each block
3. Playbook `shortcut.guards` pass (if any)

Then for **each** shortcut block in resolution order (a playbook may run **multiple** shortcuts — e.g. `research_plus_news`: parent `+coin-overview` then child `+brief`):

1. Pick `args` and `replaces_command_ids` for this block (see **`args_when`** and **slot serialization** below).
2. Run **one** `shortcut.cmd` per block with resolved args and `--format json`.
3. **Accumulate** each block’s active `replaces_command_ids` (including `args_when` branch overrides) into a playbook-level **`skip_ids` union** — do not run legacy commands yet except on per-block `fallback_on_error`.
4. Run ids listed in `post_shortcut_optional_ids` **after** all shortcut blocks succeed (even when shortcuts succeeded).

**After all shortcut blocks** (success path):

5. Collect every legacy command entry for the active playbook: walk `extends` parent chain and merge all buckets — `commands`, `news_addons`, `additional_commands`, `per_symbol_commands`, `coin_addon` (dedupe by command `id`; child entry wins on id collision).
6. Run entries whose `id` ∉ **`skip_ids`** (and not skipped by optional/conditional rules), respecting `parallel_group`.
7. On per-block shortcut failure (**non-zero exit** and/or stderr `{"error":…}`): if `fallback_on_error`, run legacy entries for **that block’s** replaced ids only (merge into run queue; do not duplicate ids already executed).

**`skip_ids` scope**: the union MUST include replaces from **every** resolved shortcut block (parent `extends` + child). Example `research_plus_news`: `+coin-overview` adds `coin_info`, `market_snapshot`, `technical_analysis`; `+brief` adds `news_brief`, `social_sentiment`, `latest_events` — parent `single_coin.news_addons` shares ids with `+brief` and MUST be skipped too (same id = same skip).

### `args_when` branch selection

Evaluate `args_when[]` **top to bottom**. Use the **first** branch whose machine `when` predicate is true; use that branch’s `args` and (if present) `replaces_command_ids`. The human `condition` string is documentation for agents — **not** the match key.

If no branch matches, use the block’s top-level `args` and `replaces_command_ids`.

| Playbook `when` | Predicate (deterministic) |
|-----------------|---------------------------|
| `contract_address` | Any of: (1) EVM `^0x[0-9a-fA-F]{40}$`; (2) Tron `^T[1-9A-HJ-NP-Za-km-z]{33}$`; (3) `chain` normalized ∈ `{solana,sol,sui,apt,aptos,near,algo,algorand,ton,cosmos,atom}` **and** `token` matches `^[1-9A-HJ-NP-Za-km-z]{32,44}$`; (4) **fallback** — `token` matches `^[1-9A-HJ-NP-Za-km-z]{32,44}$` and does **not** match ticker shape `^[A-Z0-9]{2,10}$` (covers Solana SPL mint when `chain` missing/wrong) |
| `event_id_present` | `event_id` slot is non-empty after trim |
| `symbol_present` | `symbol` slot is non-empty after trim |

**Never** pass a contract-shaped `token` through default `--symbol` or `--coin` args — use the `contract_address` branch (`--address` + `--chain` for info) or resolve ticker first for news.

### Slot serialization (`symbols` → CLI)

| Command | `symbols` slot (`string_array`) → CLI |
|---------|----------------------------------------|
| `info +coin-compare` | **One** flag, comma-separated uppercase tickers: derive `symbols_csv = join(symbols, ",")` → `--symbols BTC,ETH` |
| `info marketsnapshot batch-market-snapshot` | **Repeatable** `--symbols` per element: `--symbols BTC --symbols ETH` (legacy `multi_coin` only) |

Playbooks may expose `{symbols_csv}` in shortcut `args`; orchestrator MUST compute it before invoking `+coin-compare`.

### Shortcut `time-range` clamp

News shortcuts (`+brief`, `+event-explain`, `+community-scan`) pass `--time-range` into internal leaves with **narrower** enums than the global `time_range` slot. Before each shortcut call, clamp user `time_range` against the block’s `arg_enums.time-range` (when present) — same rule as legacy `commands` (CLAUDE.md rule 9).

| Shortcut | `arg_enums.time-range` (playbook) | Why |
|----------|-----------------------------------|-----|
| `news +brief` | `1h`, `24h`, `7d` | Internal `get-latest-events` / `get-social-sentiment` reject `30d` — passing `30d` yields RC=0 with `partial: true`, `missing_sections` including `top_events`. |
| `news +event-explain` | `1h`, `24h`, `7d` | Same for events leg + `search-x`. |
| `news +community-scan` | `1h`, `24h`, `7d` | Narrowest of UGC / X / sentiment internals. |

If the user insists on `30d` and shortcut path is active: clamp to `7d` (or nearest allowed value) and note the clamp in the report; or skip shortcut and use legacy `search-news` / `search-ugc` which accept `30d`.

**Token shape for `+token-risk` / `+token-onchain` / news `--coin`:**

- Ticker: default `--symbol` / `--coin` with `{symbol}` when `symbol_present`; use `{symbol\|{token}}` only when `token` is **not** `contract_address`.
- Contract: `--address` + `--chain` for info shortcuts (`args_when` / `when: contract_address`).
- **`news +community-scan` / `+brief`**: `--coin` MUST be a ticker. When user supplied contract-only `token`, run parent `+token-onchain` (or `get-coin-info`) first and set `symbol` from payload `coin_context`. If `symbol_present` is still false, **skip** the news shortcut **and** legacy news commands that take `--coin` — mark community/news sections unavailable. Do **not** pass contract `{token}` to `--coin` (legacy calls return empty data, not a hard error).

On shortcut failure:

- **Non-zero exit**, and/or **stderr** parses as `{"error":{...}}` (stdout is usually empty).
- Do **not** check stdout for `status != "success"` on info/news/shortcut calls — that shape applies to **`gate-cli preflight --format json` only**, not leaf or shortcut results.
- If `fallback_on_error: true` → run the full legacy `commands` chain for replaced ids.
- Otherwise → abort per `failure_policy`.

On success with top-level `partial: true` or `missing_sections` in the payload: mark affected sections; do not auto re-run legacy unless required data is empty.

## JSON output contract (info / news / shortcuts)

**Not the same as preflight.** `gate-cli preflight --format json` prints a routing object on stdout (`.status`, `.route`, …). **`gate-cli info …` / `gate-cli news …` (leaves and `+shortcuts`) use a different stdout shape.**

Default **release** binary (`gate-cli v0.7.6+`, `--format json`):

| Outcome | Exit | stdout | stderr |
|---------|------|--------|--------|
| Success | `0` | **Business payload only** — shortcut aggregates expose top-level keys such as `basic_info`, `market_snapshot`; leaf tools expose their tool fields directly | empty (unless `--verbose`) |
| Failure | non-zero | usually empty | `{"error":{"status", "error_type", "label", "message", …}}` |

Internal rendering builds `{ status, data, meta }` then **`printJSONToolResult` prints only `data` to stdout** (see gate-cli `internal/toolrender/render.go`). Agents MUST parse the **stdout payload root**, not a `data` wrapper.

**Agent-tagged build only** (`go build -tags agent` **and** `GATE_CLI_AGENT=1`): success stdout is `{ "data": <payload>, "meta": {…} }` — still **no** top-level `status`. Use `.data.*` for fields in that mode only.

```bash
# Default binary — failure detection
set +e
ERR=$(mktemp)
PAYLOAD=$(gate-cli info +coin-overview --symbol BTC --format json 2>"$ERR")
RC=$?
if [[ $RC -ne 0 ]] || jq -e '.error' "$ERR" >/dev/null 2>&1; then
  : # shortcut failed → fallback_on_error or abort
else
  jq '.basic_info' <<<"$PAYLOAD"   # top-level field, not .data.basic_info
fi
rm -f "$ERR"
```

## Shortcut JSON field mapping (synthesis)

Map **top-level payload fields** from successful stdout (or `.data.*` only in agent-tagged mode). Do **not** assume legacy command id names appear as JSON keys.

| Shortcut | Payload field(s) | Legacy id | Notes |
|----------|-----------------|-----------|-------|
| `info +coin-overview` | `basic_info` | `coin_info` | |
| | `market_snapshot` | `market_snapshot` | |
| | `technical_view` | `technical_analysis` | |
| `info +market-overview` | `market_summary` | `market_overview` | |
| | `benchmark_snapshots` | — | **Not** gainers/losers boards; cite as benchmark context |
| | `trend_anchor` | — | Partial TA for benchmarks only |
| | — | `popular_board`, `gainers_board`, `losers_board` | **Not in shortcut.** In `gate-info-research.market_overview` these run via `post_shortcut_optional_ids` AFTER the shortcut, so ranking boards are still collected — map them from the legacy `get-coin-rankings` outputs. Only when those optional calls fail, state "rankings boards unavailable this run". |
| `info +coin-compare` | `compare_matrix[]` (each row: `symbol`, `basic_info`, `market_snapshot`, `technical_view`) | `batch_snapshot`, `coin_info_each`, `technical_each` | Also `dropped_symbols` when a symbol lacks enough data |
| `info +trend-analysis` | `indicator_snapshot` | `technical_analysis` | Lightweight only |
| | `price_context` | partial `market_snapshot` | |
| | — | `kline`, `indicator_history` | **Not included** — use legacy if user needs deep TA |
| `info +token-risk` | `risk_level`, `risk_items` | `token_security` | Both mirror full `check-token-security` object (duplicate in v0.7.6); not scalars. Top-level stdout — not `.data.*`. |
| | `token_identity` | `coin_info_basic` | |
| | — | `token_onchain` | **Not included** — run `post_shortcut_optional_ids` or legacy `token_onchain` |
| `info +address-tracker` | `entity_guess`, `defi_context` | `address_info` | |
| | `recent_activity` | `address_transactions` | |
| `info +token-onchain` | `token_distribution`, `holder_structure`, `activity_snapshot` | `token_onchain` | |
| | `coin_context` | — | Ticker resolved from address when applicable |
| `news +brief` | `top_events`, `news_digest`, `sentiment_summary` | `latest_events`, `search_news`, `social_sentiment` | |
| `news +event-explain` | `event_summary`, `timeline` | `event_detail`, `latest_events` | When `--event-id` passed |
| | `source_coverage` | `search_news` | |
| | `market_interpretation` | `search_x` (X) | **Not** `social_sentiment` |
| | — | `social_sentiment` | Run legacy optional if sentiment index needed |
| `news +community-scan` | UGC + X + sentiment fields in payload | `ugc_scan`, `search_x`, `social_sentiment` | `--coin` must be ticker. Does **NOT** cover `search-news` headlines — never put `news_brief`/`search_news` in its `replaces_command_ids`; fetch headlines via `post_shortcut_optional_ids` or a separate `+brief` instead. |

## Hard rules

1. Never call a `+shortcut` when `shortcuts_enabled` is false.
2. Never put `+shortcut` in playbook `commands` — only in `shortcut` / `additional_shortcut` / `info_shortcut`.
3. `address_risk` playbook MUST NOT use `+address-tracker`.
4. Re-run preflight each turn — do not cache across sessions.

> Playbook YAML: `playbooks/*.yaml`. Canonical preflight: `docs/preflight-and-diagnostics.md`.
