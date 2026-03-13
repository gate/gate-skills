# Changelog

All notable changes to the Gate Exchange TradFi Query skill are documented here.

Format: version with date-based suffix (`YYYY.M.DD-N`). Each release uses a sequential suffix: `YYYY.M.DD-1`, `YYYY.M.DD-2`, etc.

---

## [2026.3.13-6] - 2026-03-13

### Changed

- **Terminology**: TradFi-only wording. Removed "currency", "pair", and crypto symbols (e.g. BTC_USDT, USDT) from all docs. Use "symbol" for instruments (e.g. EURUSD, XAUUSD); "asset" for balance/account; table headers and error messages use "symbol" / "asset" instead of "pair" / "currency". Example prompts use TradFi symbols (EURUSD, XAUUSD).

---

## [2026.3.13-5] - 2026-03-13

### Changed

- **MCP tool names**: Updated all skill docs to use the actual Gate TradFi MCP tool names: `cex_tradfi_query_order_list`, `cex_tradfi_query_position_list`, `cex_tradfi_query_position_history_list`, `cex_tradfi_query_symbols`, `cex_tradfi_query_symbol_ticker`, `cex_tradfi_query_symbol_kline`, `cex_tradfi_query_user_assets`, `cex_tradfi_query_mt5_account_info`. Removed previous naming (list_orders, list_positions, get_tickers, get_accounts, etc.) so the agent invokes the correct MCP tools.

---

## [2026.3.13-4] - 2026-03-13

### Added

- **Order history**: Added MCP tool `cex_tradfi_query_order_history_list` for querying order history (filled/cancelled). Open orders use `cex_tradfi_query_order_list`; order history uses `cex_tradfi_query_order_history_list`.

---

## [2026.3.13-3] - 2026-03-13

### Changed

- **Query orders**: Removed single-order-by-ID flow and any use of `order_id` parameter. `cex_tradfi_query_order_list` does not support order_id; use only parameters documented in the MCP. Order module now supports only: order list (open) and order history.
- **All modules**: Skill now states that only MCP-documented parameters may be used for each tool; no unsupported parameters (e.g. order_id, or optional filters not in the MCP) may be added.

---

## [2026.3.13-2] - 2026-03-13

### Changed

- **Query market** — `references/query-market.md`: now covers **category list** (`cex_tradfi_query_categories`), **symbol list** (`cex_tradfi_query_symbols`), **ticker** (`cex_tradfi_query_symbol_ticker`), and **symbol kline** (`cex_tradfi_query_symbol_kline`). Replaced prior pair list with category + symbol list (`cex_tradfi_query_symbols`).
- **Query assets** — `references/query-assets.md`: added **MT5 account info** via `cex_tradfi_query_mt5_account_info`; user assets still via `cex_tradfi_query_user_assets`.
- **SKILL.md**: frontmatter fixed (name without `##`); description and routing updated for category/symbol/MT5; MCP tool table extended to 10 tools (all `cex_tradfi_*`). Domain Knowledge updated for categories, symbols, and MT5.
- **README**: Core Capabilities and Example Prompts updated; scope clarified (no order placement, no fund transfer).

### Scope

- Read-only only; no order placement, no fund or balance transfer. All tools prefixed with `cex_tradfi`.

---

## [2026.3.13-1] - 2026-03-13

### Added

- **Query orders** — `references/query-orders.md`: open orders → `cex_tradfi_query_order_list`; order history → `cex_tradfi_query_order_history_list`. No order_id; use only MCP-documented parameters.
- **Query positions** — `references/query-positions.md`: list current positions, list position history. MCP tools: `cex_tradfi_query_position_list`, `cex_tradfi_query_position_history_list`.
- **Query market** — `references/query-market.md`: category list, symbol list, ticker, symbol kline (see 2026.3.13-2). MCP tools: `cex_tradfi_query_categories`, `cex_tradfi_query_symbols`, `cex_tradfi_query_symbol_ticker`, `cex_tradfi_query_symbol_kline`.
- **Query assets** — `references/query-assets.md`: user account/balance and MT5 account info. MCP tools: `cex_tradfi_query_user_assets`, `cex_tradfi_query_mt5_account_info`.
- Routing-based SKILL.md with Sub-Modules, Routing Rules, MCP tool table, Execution, Domain Knowledge, Error Handling, and Safety Rules.
- README with Overview, Core Capabilities table, and Architecture.

### Scope

- Read-only skill; no order placement, cancel, amend, or transfer.
- All content in English; no deprecated brand text (Gate only).
