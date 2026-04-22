# Changelog

All notable changes to the Gate Exchange TradFi Query skill are documented here.

Format: version with date-based suffix (`YYYY.M.DD-N`). Each release uses a sequential suffix: `YYYY.M.DD-1`, `YYYY.M.DD-2`, etc.

---

## [2026.3.13-13] - 2026-03-13

### Changed

- **Order id for cancel/amend**: Documented that the `id` and `log_id` returned by `gate-cli cex tradfi order create` **must not** be used as the order id for `gate-cli cex tradfi order cancel` or `gate-cli cex tradfi order update`. The cancel and amend APIs require the order id from **`gate-cli cex tradfi order list`**. Updated `references/place-order.md` (report note), `references/cancel-order.md` (order id source), `references/amend-order.md` (order id source), and SKILL.md Domain Knowledge.

---

## [2026.3.13-12] - 2026-03-13

### Changed

- **Place order (`gate-cli cex tradfi order create`)**: Before placing an order, **must** call **`gate-cli cex tradfi market symbol`** with the symbol. If no result or error, do not place order (symbol may not exist). From the response: validate order size **≥** `min_order_volume` and size is an **integer multiple of** `step_order_volume`; if leverage is passed, it **must** be in the `leverages` array. Leverage is optional. Updated `references/place-order.md` (symbol config validation, workflow, all scenarios) and SKILL.md (added `gate-cli cex tradfi market symbol` to query tools; place-order tool note). Query tool numbering 8–11, trading 12–16.

---

## [2026.3.13-11] - 2026-03-13

### Changed

- **`gate-cli cex tradfi position close`**: Full close (全部平仓) does not require size or close_volume — pass position identifier only. Updated `references/close-position.md`: parameters table, conditions, workflow, Scenario 1 (full close), and response template to state that full close omits size/close_volume; partial close still passes close size/close_volume per `gate-cli`.

---

## [2026.3.13-10] - 2026-03-13

### Changed

- **`gate-cli cex tradfi order create`**: Documented that the tool **supports setting take-profit and stop-loss price** when placing an order. Updated `references/place-order.md`: intro, parameters table, pre-execution confirmation, workflow, report template, and added Scenario 3 (place order with take-profit/stop-loss). Updated SKILL.md Sub-Modules and `gate-cli` commands table.

---

## [2026.3.13-9] - 2026-03-13

### Changed

- **`gate-cli cex tradfi position update`**: Documented that the tool supports **take-profit price** and **stop-loss price** only; **leverage, margin mode, and other fields are not supported**. Updated `references/modify-position.md`: parameters table, workflow, and scenarios now only cover take-profit/stop-loss; removed leverage and margin-mode scenarios; added Scenario 3 for both take-profit and stop-loss. If user asks to change leverage or margin, agent must reply that the tool only supports take-profit and stop-loss. Updated SKILL.md Sub-Modules, Routing, and `gate-cli` commands table accordingly.

---

## [2026.3.13-8] - 2026-03-13

### Changed

- **`gate-cli cex tradfi order update`**: Documented that the tool supports **price** and **take-profit / stop-loss price** only; **size is not supported**. Updated `references/amend-order.md` (parameters table, workflow, scenarios): removed amend-size and amend-price-and-size scenarios; added Scenario 2 for take-profit/stop-loss. If user asks to change size, agent must reply that the tool does not support it. Updated SKILL.md Sub-Modules, Routing, and `gate-cli` commands table accordingly.

---

## [2026.3.13-7] - 2026-03-13

### Added

- **Trading modules**: Place order, amend order, cancel order, modify position, close position. New sub-modules and routing to `references/place-order.md`, `references/amend-order.md`, `references/cancel-order.md`, `references/modify-position.md`, `references/close-position.md`. `gate-cli` commands: `gate-cli cex tradfi order create`, `gate-cli cex tradfi order update`, `gate-cli cex tradfi order cancel` (one order per call; no batch), `gate-cli cex tradfi position update`, `gate-cli cex tradfi position close`.
- **Parameter conditions and limits**: Skill and each trading reference must declare input conditions and value limits from the `gate-cli`; only `gate-cli`-documented parameters may be used.
- **User confirmation**: Before any trading `gate-cli` call, output all parameters to the user and require explicit confirmation; do not execute until confirmed.
- **Response parameter explanation**: After each trading operation, explain in the response the parameters that were used and the outcome (success or error).

### Changed

- **SKILL.md**: Extended from read-only query suite to full TradFi suite (query + trading). Description, Sub-Modules, Routing Rules, `gate-cli` commands, Execution, Domain Knowledge, Error Handling, Safety Rules, and Report Template updated. Existing query content unchanged.

### Fixed

- **`gate-cli` command names**: Corrected to actual Gate TradFi `gate-cli` names: `gate-cli cex tradfi order create` → `gate-cli cex tradfi order create`; `gate-cli cex tradfi order update` → `gate-cli cex tradfi order update`; `gate-cli cex tradfi position update` → `gate-cli cex tradfi position update`; cancel/delete uses `gate-cli cex tradfi order cancel` only (no `gate-cli cex tradfi order cancel` or `cex_tradfi_delete_orders` (no `gate-cli` mapping; see `gate-cli/cmd/cex/MCP_LEGACY_TOOL_RESOLUTION.md` §二); no batch support). Updated in SKILL.md and all trading reference docs; cancel-order doc uses single tool `gate-cli cex tradfi order cancel`, batch scenario removed.

---

## [2026.3.13-6] - 2026-03-13

### Changed

- **Terminology**: TradFi-only wording. Removed "currency", "pair", and crypto symbols (e.g. BTC_USDT, USDT) from all docs. Use "symbol" for instruments (e.g. EURUSD, XAUUSD); "asset" for balance/account; table headers and error messages use "symbol" / "asset" instead of "pair" / "currency". Example prompts use TradFi symbols (EURUSD, XAUUSD).

---

## [2026.3.13-5] - 2026-03-13

### Changed

- **`gate-cli` command names**: Updated all skill docs to use the actual Gate TradFi `gate-cli` command names: `gate-cli cex tradfi order list`, `gate-cli cex tradfi position list`, `gate-cli cex tradfi position history`, `gate-cli cex tradfi market symbols`, `gate-cli cex tradfi market ticker`, `gate-cli cex tradfi market kline`, `gate-cli cex tradfi account assets`, `gate-cli cex tradfi account info`. Removed previous naming (list_orders, list_positions, get_tickers, get_accounts, etc.) so the agent invokes the correct `gate-cli` commands.

---

## [2026.3.13-4] - 2026-03-13

### Added

- **Order history**: Added `gate-cli` command `gate-cli cex tradfi order history` for querying order history (filled/cancelled). Open orders use `gate-cli cex tradfi order list`; order history uses `gate-cli cex tradfi order history`.

---

## [2026.3.13-3] - 2026-03-13

### Changed

- **Query orders**: Removed single-order-by-ID flow and any use of `order_id` parameter. `gate-cli cex tradfi order list` does not support order_id; use only parameters documented in the `gate-cli`. Order module now supports only: order list (open) and order history.
- **All modules**: Skill now states that only `gate-cli`-documented parameters may be used for each tool; no unsupported parameters (e.g. order_id, or optional filters not in the `gate-cli`) may be added.

---

## [2026.3.13-2] - 2026-03-13

### Changed

- **Query market** — `references/query-market.md`: now covers **category list** (`gate-cli cex tradfi market categories`), **symbol list** (`gate-cli cex tradfi market symbols`), **ticker** (`gate-cli cex tradfi market ticker`), and **symbol kline** (`gate-cli cex tradfi market kline`). Replaced prior pair list with category + symbol list (`gate-cli cex tradfi market symbols`).
- **Query assets** — `references/query-assets.md`: added **MT5 account info** via `gate-cli cex tradfi account info`; user assets still via `gate-cli cex tradfi account assets`.
- **SKILL.md**: frontmatter fixed (name without `##`); description and routing updated for category/symbol/MT5; `gate-cli` command table extended to 10 tools (all `cex_tradfi_*`). Domain Knowledge updated for categories, symbols, and MT5.
- **README**: Core Capabilities and Example Prompts updated; scope clarified (no order placement, no fund transfer).

### Scope

- Read-only only; no order placement, no fund or balance transfer. All tools prefixed with `cex_tradfi`.

---

## [2026.3.13-1] - 2026-03-13

### Added

- **Query orders** — `references/query-orders.md`: open orders → `gate-cli cex tradfi order list`; order history → `gate-cli cex tradfi order history`. No order_id; use only `gate-cli`-documented parameters.
- **Query positions** — `references/query-positions.md`: list current positions, list position history. `gate-cli` commands: `gate-cli cex tradfi position list`, `gate-cli cex tradfi position history`.
- **Query market** — `references/query-market.md`: category list, symbol list, ticker, symbol kline (see 2026.3.13-2). `gate-cli` commands: `gate-cli cex tradfi market categories`, `gate-cli cex tradfi market symbols`, `gate-cli cex tradfi market ticker`, `gate-cli cex tradfi market kline`.
- **Query assets** — `references/query-assets.md`: user account/balance and MT5 account info. `gate-cli` commands: `gate-cli cex tradfi account assets`, `gate-cli cex tradfi account info`.
- Routing-based SKILL.md with Sub-Modules, Routing Rules, `gate-cli` command table, Execution, Domain Knowledge, Error Handling, and Safety Rules.
- README with Overview, Core Capabilities table, and Architecture.

### Scope

- Read-only skill; no order placement, cancel, amend, or transfer.
- All content in English; no deprecated brand text (Gate only).
