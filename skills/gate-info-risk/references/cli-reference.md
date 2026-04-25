# gate-info-risk — CLI Command Reference

> Full flag tables for every `gate-cli` command this skill invokes. Verified against `gate-cli v0.5.2` (`gate-cli info <group> <cmd> --help`). `info compliance check-address-risk` is NOT in this list — it does NOT ship in v0.5.2.
>
> All flags below are real on this version of the CLI; agents MUST pass `--format json` on every data-collection call.

## Info · compliance

### `gate-cli info compliance check-token-security`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--token` | string |  | Ticker (`PEPE`, `USDT`) OR contract address (`0xdAC17F...`, SPL mint, TRX mint). **Polymorphic** — pass contract addresses through this flag directly. Exactly ONE of `--token` or `--address` must be set (see `--address` note below). This skill always uses `--token`. |
| `--chain` | string | ✅ | Pass the short id as input: `eth`, `bsc`, `polygon`, `arb`, `op`, `base`, `avax`, `solana`, `tron`. CLI also accepts long-form aliases (`ethereum`, `arbitrum`, `optimism`, `avalanche`, `bnb`, `matic`) on input. The response `.chain` echo is **endpoint-dependent** (e.g. `check-token-security` on ETH returns `chain="eth"` but on Arbitrum returns `chain="arbitrum"`) — parsers MUST accept both alias sets and normalize at read time, never assume a fixed echo shape. See [`references/troubleshooting.md`](troubleshooting.md#chain-aliases) for the full alias table. |
| `--address` | string |  | Explicit contract address. CLI treats `--token` and `--address` as mutually exclusive — passing both returns `INTEL_RESULT_ERROR: token 与 address 二选一，不能同时传`. **This skill does NOT use `--address`**: contract addresses are routed into `--token` instead (simpler, no XOR to manage). Documented here for completeness only. |
| `--scope` | string |  | Enum: `basic / full`. Default `basic`. `full` adds holder concentration + ownership analysis + risk_facts aggregation. |
| `--lang` | string |  | Enum: `cn / en / ja / kr / tw`. Default `en`. Localizes `risk_name` / `risk_desc` strings. |

### Return schema (verified against `gate-cli v0.5.2` on `--scope full` against USDT / PEPE / SHIB / CAKE)

**Top-level** (all string values unless noted):

| Field | Type | Notes |
|---|---|---|
| `address`, `token`, `chain` | string | Echo of request. |
| `buy_tax`, `sell_tax` | string percent | `"0"` / `"10"` / ... cast with `tonumber` before numeric compare. |
| `is_honeypot`, `is_open_source` | **JSON boolean** | `true` / `false` — NOT strings. Compare with `== true` / `== false`. Same semantic as nested `high_risk_list[?risk_key==<same>].risk_value` (which IS a string `"0"` / `"1"`). Both representations are present for convenience; pick one and stay consistent per call site. |
| `top10_percent`, `dev_holding_percent`, `holder_count` | string | Also nested under `data_analysis.*`; pick either. Cast with `tonumber` for numeric compare. |
| `data_analysis` | object | `{top10_percent, top100_percent, dev_holding_percent, insider_percent, max_holder_percent, creator_address, holder_count}` — canonical location. |
| `tax_analysis.token_tax` | object | `{buy_tax, sell_tax, transfer_tax}` — primary source for tax numbers. |
| `name_risk` | object | `{is_domain_token, is_sensitive}` — booleans. |
| `risk_facts` | string[] | Flat list of `risk_key` that are currently active (across all risk-list categories). |
| `risk_summary` | object | `{high_risk_num, middle_risk_num, low_risk_num, highest_risk_level}` — integer aggregate severity. |
| `high_risk_list` / `middle_risk_list` / `low_risk_list` / `risky_list` / `attention_list` | array or null | Each element: `{risk_key, risk_level, risk_value ("0"/"1"), risk_name, risk_desc}`. Any of these lists can be `null` on clean tokens. |

**Known `risk_key` values by list** (universe observed on mainnet tokens):

| List | `risk_key` values |
|---|---|
| `high_risk_list` | `is_honeypot`, `is_high_tax`, `is_open_source` |
| `middle_risk_list` | `owner_change_balance`, `can_take_back_ownership`, `hidden_owner`, `self_destruct`, `is_mintable`, `is_proxy`, `is_blacklisted`, `is_scam`, `is_dev_scam`, `is_airdrop_scam`, `anti_whale_modifiable`, `can_not_sell_all`, `gas_abuse`, `has_tax`, `is_anti_whale`, `is_mc_error`, `is_volume_boost_trade`, `lp_burned`, `personal_slippage_modifiable`, `slippage_modifiable`, `trading_cooldown` |
| `low_risk_list` | `is_whitelisted`, `is_in_dex` |
| `risky_list` / `attention_list` | additional categorized overlays; may be `null`. Enumerate with `jq '.risky_list[]?.risk_key, .attention_list[]?.risk_key'` when you encounter a new token. |

**Gotchas**:

- **Two type conventions for the same flag**. `check-token-security` returns flags twice:
  - Top-level `.is_honeypot` / `.is_open_source` → JSON **boolean** (`true` / `false`).
  - Nested `.high_risk_list[?risk_key=="is_honeypot"].risk_value` → **string** (`"0"` / `"1"`).
  Using the wrong comparison will silently never match. Pick the path that matches the comparison idiom you're using.
- `.risk_value` comparisons on any nested list MUST treat values as strings. `== "1"` is correct; `== true` will never match.
- `buy_tax` / `sell_tax` / `data_analysis.*_percent` are strings; cast with `tonumber` in jq or parseFloat elsewhere before comparing to a number.
- `high_risk_list[]` only contains three `risk_key` entries (`is_honeypot`, `is_high_tax`, `is_open_source`). Ownership-critical flags (`owner_change_balance`, `can_take_back_ownership`, `hidden_owner`, `self_destruct`, `is_mintable`, `is_proxy`, `is_blacklisted`, etc.) live in **`middle_risk_list`** — do NOT look for them in `high_risk_list`.

## Info · onchain

### `gate-cli info onchain get-address-info`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--address` | string | ✅ | Wallet address. |
| `--chain` | string |  | Normally required; omit only if the address format is chain-self-evident. |
| `--scope` | string |  | Enum: `basic / detailed / full / with_counterparties / with_defi / with_pnl`. Default `basic` (enough for risk-layer labels). Use `with_counterparties` to enrich with address interaction graph; `with_pnl` adds realized/unrealized PnL summary. |
| `--min-value-usd` | float |  | Filter embedded flow summary. |
| `--include-upstream-raw` | flexBool |  | Include upstream provider's raw labels. |
| `--upstream-raw-mode` | string |  | Enum: `full / lite / off`. Default `off`. |

Return fields the skill cares about:

- `risk_labels[]` — OFAC / sanctioned / mixer / scam / exchange-hack-proceeds / darknet / ... (when provided).
- `tags[]` — descriptive tags (CEX deposit, protocol router, etc.).
- `risk_score` (if present).
- `balance_summary`, `first_seen`, `last_seen`.

> **If `risk_labels` and `tags` are both empty or missing, the verdict MUST be `无法判定 (scope limited)`. See SKILL.md Verdict rules.**

### `gate-cli info onchain get-address-transactions`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--address` | string | ✅ | Wallet address. |
| `--chain` | string |  | Usually required. |
| `--time-range` | string |  | Enum: `1h / 24h / 1d / 7d / 30d / 90d`. |
| `--min-value-usd` | float |  | Threshold for flagging large transfers; `100000` is a common default. |
| `--limit` | int |  | Default `50`, max `200`. |
| `--start-time`, `--end-time` | int (unix) |  | Timestamp bounds. |
| `--tx-type` | string |  | Enum: `all / contract_call / token_transfer / transfer`. Default `all`. |
| `--from-address`, `--to-address` | string |  | Directional filters. |
| `--nonzero-value` | flexBool |  | Drop zero-value transfers. |
| `--upstream-raw-mode` | string |  | Enum: `full / lite / off`. Default `off`. |

### `gate-cli info onchain get-token-onchain`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--token` | string | ✅ | Ticker or contract. |
| `--chain` | string |  | Normally required. |
| `--scope` | string |  | Enum: `activity / full / holders / smart_money / transfers`. Default `full` — returns `holders.holder_concentration`, `smart_money`, `activity` together. Narrow to `holders` when you only need concentration data. |
| `--include-upstream-raw` | flexBool |  | Upstream raw labels passthrough. |
| `--upstream-raw-mode` | string |  | Enum: `full / lite / off`. Default `off`. |

Return fields:

- `holders.holder_count`, `holders.holder_concentration[]` (top-10 / top-11–50 / top-51–100 / top-101+ percentages), `holders.top_holders[]`.
- `activity.{daily_active_addresses, daily_transfer_volume, new_address_count_7d}`.
- `smart_money.*` when available.

## Info · coin (auxiliary context)

### `gate-cli info coin get-coin-info`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--query` | string | ✅ | Symbol or contract. |
| `--query-type` | string |  | Enum: `address / auto / gate_symbol / name / project / source_id / symbol`. Default `auto`. |
| `--chain` | string |  | Needed when `--query-type=address`. |
| `--scope` | string |  | Enum: `basic / detailed / full / with_project / with_tokenomics`. Default `basic`. |

Used in `token_risk` as optional context for project fundamentals.

## News · feed (auxiliary for `project_risk`)

### `gate-cli news feed search-news`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--coin` | string |  | Ticker. |
| `--query` | string |  | Free text. |
| `--limit` | int |  | Default `10`, max `100`. |
| `--sort-by` | string |  | Default `time`. Accepts `time`, `importance`, `similarity_score` (no strict CLI enum). |
| `--time-range` | string |  | Enum: `1h / 24h / 7d / 30d`. Default `24h`. |

### `gate-cli news feed get-exchange-announcements`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--coin` | string |  | Ticker. |
| `--exchange` | string |  | Narrow to a specific venue. |
| `--announcement-type` | string |  | Enum: `all / delisting / listing / maintenance`. |
| `--limit` | int |  | Max `100`. |

## News · events (auxiliary for `project_risk`)

### `gate-cli news events get-latest-events`

| Flag | Type | Required | Notes |
|---|---|---|---|
| `--coin` | string |  | Ticker. |
| `--time-range` | string |  | Enum: `1h / 24h / 7d`. **No `30d`** — for longer windows fall back to `--start-time` / `--end-time` (unix-ms). |
| `--event-type` | string |  | Filter: `exploit`, `rug`, `depeg`, `unlock`, ... |
| `--limit` | int |  | Default `20`, max `100`. |
| `--start-time`, `--end-time` | string |  | Window override. |

## Global flags

Same contract as in `gate-info-research CLI reference`:

- `--format json` is mandatory.
- NEVER surface `--api-key`, `--api-secret`, `Authorization:` headers.

## Explicitly NOT available

- `gate-cli info compliance check-address-risk` — **does not exist in current gate-cli (v0.5.2 / dev)**. Do NOT attempt to call it. When a future CLI adds it, update the `address_risk` playbook's `cli_future_shortcut` field, NOT this skill's execution path.
- `gate-cli info +coin-risk` / `news +risk-brief` etc. — aggregate shortcuts are not shipped; use the lower-level commands above.

## Invalid value traps to avoid

| Command | Flag | Invalid value | Use instead |
|---|---|---|---|
| `news events get-latest-events` | `--time-range` | `30d` | `7d` or `--start-time/--end-time` unix-ms |
| `info coin get-coin-rankings` | `--ranking-type` | `gainers`, `losers` | `top_gainers`, `top_losers` |
