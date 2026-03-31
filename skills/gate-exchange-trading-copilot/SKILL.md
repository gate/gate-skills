---
name: gate-exchange-trading-copilot
version: "2026.3.28-14"
updated: "2026-03-28"
description: "Gate Trading Copilot L2 (spec v1.3): spot, futures, margin, flash swap, Alpha, TradFi; pre-trade checks and Action Draft plus Y/N before every write. Use this skill whenever the user wants to trade, cancel or amend orders, borrow or repay margin, flash convert, or query positions and open orders. Trigger phrases include \"market buy\", \"open long\", \"take profit\", \"margin borrow\", \"flash swap\", \"TradFi\", \"Alpha\", \"cancel order\", or spot-plus-futures combos."
---

# gate-exchange-trading-copilot

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.


---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- cex_alpha_get_alpha_order
- cex_alpha_list_alpha_account_book
- cex_alpha_list_alpha_accounts
- cex_alpha_list_alpha_orders
- cex_alpha_quote_alpha_order
- cex_fc_get_fc_order
- cex_fc_list_fc_currency_pairs
- cex_fc_list_fc_orders
- cex_fc_preview_fc_multi_currency_many_to_one_order
- cex_fc_preview_fc_multi_currency_one_to_many_order
- cex_fx_get_fx_accounts
- cex_fx_get_fx_contract
- cex_fx_get_fx_dual_position
- cex_fx_get_fx_order
- cex_fx_get_fx_order_book
- cex_fx_get_fx_position
- cex_fx_get_fx_price_triggered_order
- cex_fx_get_fx_tickers
- cex_fx_list_fx_my_trades
- cex_fx_list_fx_orders
- cex_fx_list_fx_positions
- cex_fx_list_price_triggered_orders
- cex_margin_get_auto_repay_status
- cex_margin_get_margin_transferable
- cex_margin_get_margin_uni_estimate_rate
- cex_margin_get_uni_borrowable
- cex_margin_get_user_margin_tier
- cex_margin_list_cross_margin_loans
- cex_margin_list_cross_margin_repayments
- cex_margin_list_funding_accounts
- cex_margin_list_margin_account_book
- cex_margin_list_margin_accounts
- cex_margin_list_margin_user_account
- cex_margin_list_uni_loan_interest_records
- cex_margin_list_uni_loan_records
- cex_margin_list_uni_loans
- cex_spot_get_currency
- cex_spot_get_currency_pair
- cex_spot_get_spot_accounts
- cex_spot_get_spot_batch_fee
- cex_spot_get_spot_candlesticks
- cex_spot_get_spot_order_book
- cex_spot_get_spot_price_triggered_order
- cex_spot_get_spot_tickers
- cex_spot_list_spot_account_book
- cex_spot_list_spot_my_trades
- cex_spot_list_spot_orders
- cex_spot_list_spot_price_triggered_orders
- cex_tradfi_query_categories
- cex_tradfi_query_mt5_account_info
- cex_tradfi_query_order_history_list
- cex_tradfi_query_order_list
- cex_tradfi_query_position_history_list
- cex_tradfi_query_position_list
- cex_tradfi_query_symbol_detail
- cex_tradfi_query_symbol_kline
- cex_tradfi_query_symbol_ticker
- cex_tradfi_query_symbols
- cex_tradfi_query_user_assets
- cex_unified_get_unified_accounts
- cex_unified_get_unified_mode
- cex_unified_get_unified_borrowable
- cex_unified_list_unified_loan_records
- cex_wallet_get_wallet_fee

**Execution Operations (Write)**

- cex_alpha_place_alpha_order
- cex_fc_create_fc_multi_currency_many_to_one_order
- cex_fc_create_fc_multi_currency_one_to_many_order
- cex_fx_amend_fx_order
- cex_fx_cancel_all_fx_orders
- cex_fx_cancel_fx_order
- cex_fx_cancel_fx_price_triggered_order
- cex_fx_cancel_fx_price_triggered_order_list
- cex_fx_create_fx_order
- cex_fx_create_fx_price_triggered_order
- cex_fx_update_fx_dual_position_cross_mode
- cex_fx_update_fx_dual_position_leverage
- cex_fx_update_fx_position_cross_mode
- cex_fx_update_fx_position_leverage
- cex_fx_update_fx_price_triggered_order
- cex_margin_create_uni_loan
- cex_margin_set_auto_repay
- cex_margin_set_user_market_leverage
- cex_spot_amend_spot_batch_orders
- cex_spot_amend_spot_order
- cex_spot_cancel_all_spot_orders
- cex_spot_cancel_spot_batch_orders
- cex_spot_cancel_spot_order
- cex_spot_cancel_spot_price_triggered_order
- cex_spot_cancel_spot_price_triggered_order_list
- cex_spot_create_spot_batch_orders
- cex_spot_create_spot_order
- cex_spot_create_spot_price_triggered_order
- cex_tradfi_close_position
- cex_tradfi_create_tradfi_order
- cex_tradfi_delete_order
- cex_tradfi_update_order
- cex_tradfi_update_position
- cex_unified_create_unified_loan

### Authentication
- API Key Required: Yes (authenticated Gate Exchange MCP)
- Permissions: Combined Spot, Futures, Flash swap, Alpha, TradFi, Margin, and Unified loan scopes as required by the chosen action (configure keys accordingly)
- Get API Key: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

### MCP descriptor coverage (local vs release)


## Domain Knowledge

### What this skill is (L2 execution copilot)

- Orchestrates **trade execution** on Gate: spot, USDT-margined futures, isolated margin (uni loan), unified-account borrow/repay, flash swap, Alpha tokens, and TradFi orders.
- Uses **light pre-trade reads** (balances, tickers, contract specs, borrowable limits) for risk context only. It does **not** replace deep market research, full portfolio inventory, earn/staking, or copy-trading flows.
- Every **write** path follows: parallel reads where useful → **Action Draft** → explicit **Y / N** → then call write tools.

### L1 vs L2 skill routing

- When a user intent **overlaps** both an **L1** domain skill (for example `gate-exchange-spot`, `gate-exchange-futures`, or other product-specific Gate exchange skills) and this **L2** Trading Copilot, **prefer L2 (this skill)** first: use this skill’s workflow, tool list, and Action Draft rules.
- If the intent is **not** covered here (missing signals, tools, or scope), **then** use the appropriate **L1** skill or the routes in **Out of scope** below.

### L1 skill invocation chain (aligned with L2 Tool Calls spec v1.3)

The L2 spec maps **nine** L1 domains to one Trading Copilot. This repository may not package every L1 name as a folder; when a folder is missing, use the **MCP tool families** in the third column and **`gate-exchange-unified`** / **`gate-exchange-spot`** for margin-and-spot legs.

| # | L1 skill (spec name) | Signals | Role in L2 |
|---|----------------------|---------|------------|
| 1 | `gate-exchange-spot` | S1; spot legs after borrow | Spot orders, tickers, accounts, cancel/amend, spot triggers |
| 2 | `gate-exchange-futures` | S2 | Futures orders, positions, price-triggered orders, leverage |
| 3 | `gate-exchange-margin` | S3 | Isolated margin borrow/repay semantics (`cex_margin_*`); pair with spot tools for sell/buy legs |
| 4 | `gate-exchange-flashswap` | S4 | Flash and multi-currency execution in that L1 package; **scenarios 6 and 19** (standalone single-leg flash; futures reduce plus flash) are **hidden** in this skill—route to **`gate-exchange-flashswap`** / **`gate-exchange-futures`** as below (do **not** call any MCP tool here for those intents) |
| 5 | `gate-exchange-assets` | Pre-trade | Balance checks beyond a single product line |
| 6 | `gate-exchange-marketanalysis` | With S1–S2 | Light tickers only; deep research is **Out of scope** |
| 7 | `gate-exchange-unified` | S3 | Unified account, `cex_unified_get_unified_mode`, unified loan borrow/repay with spot |
| 8 | `gate-exchange-alpha` | S8 | Alpha accounts, quote, place order |
| 9 | `gate-exchange-tradfi` | S7 | TradFi assets, symbols, orders |

**Typical L2 → L1 consultation order (non-exclusive):** parse signals (**Signal detection workflow**) → for each leg, open the matching L1 `SKILL.md` when it exists to normalize pair formats and minimums → **Step 3** reads from this L2 allowlist → **Action Draft** → **Y** → **Step 5** writes.

### Pre-trade clarification (L2 Tool Calls spec v1.3)

Apply **before** Action Draft when the user leaves product scope ambiguous:

| Situation | Action |
|-----------|--------|
| User says leveraged long/short with a multiplier but **not** “borrow/repay” | Prefer **futures** first; ask **perpetual vs delivery** if the contract type is unclear. |
| User describes **cross-margin leveraged long or short** (e.g. explicit cross-margin spot-margin borrow) | **Default to spot margin**: treat as **unified-account / cross-margin borrow + spot leg** (signal **S3**), **not** USDT-margined futures—unless the user clearly asks for futures (perpetual/delivery, contracts, positions). |
| User references a futures position (long/short, TP/SL, add/reduce) without contract type | Ask **perpetual vs delivery** before sizing or triggers. |
| **Dual-position mode** (infer from `cex_fx_get_fx_dual_position` / positions) and **both** isolated and cross long (or short) exist for the same contract | Ask whether to target **isolated** or **cross** margin for that position. |
| **One-way or dual holding mode** without duplicate isolated/cross legs | Use current position data; do **not** ask isolated vs cross. |
| User says **cross-margin / unified** leveraged long and unified mode matters | Call `cex_unified_get_unified_mode`. If mode is not suitable for cross-margin-style borrow (spec: **multi_currency** or **portfolio**), **stop** and tell the user to switch unified account mode in the app; do not write. |
| User asks **only** to **repay unified-account borrow** (e.g. “repay 10 USDT unified loan”) | **Scenario 14** path: **not** a spot “close position” unwind—use **`cex_unified_list_unified_loan_records`** / **`cex_unified_get_unified_accounts`** to validate liability and balance, then Action Draft → **Y** → **`cex_unified_create_unified_loan`** (`type=repay`). If the user instead asks to **sell cross-margin spot + repay** in one story, that is a **different** margin+spot chain—see **`gate-exchange-margin`** / **`gate-exchange-unified`**, not the repay-only row. |
| **`cex_unified_get_unified_borrowable`** fails (scenario 11) with a message matching **single currency mode** not supported (e.g. contains `operation not support for single currency mode`, case-insensitive) | **Stop** the write path. Tell the user to switch the unified account to **cross-currency margin mode** or **portfolio margin mode** in the Gate app (or web), then retry; do not draft or execute borrow/spot legs. |

### L2 spec chain names vs MCP (futures mode)

The HTML spec may describe a **position-mode lookup** using a label that does **not** appear as a registered MCP tool in this skill. Use **`cex_fx_get_fx_dual_position`** together with **`cex_fx_list_fx_positions`** to infer mode and disambiguate positions.

### Out of scope (route to other skills)

| User intent | Route |
|-------------|--------|
| Deep research, narrative market reports, multi-asset screens | `gate-info-*` / `gate-news-*` skills as appropriate |
| Full cross-account asset audit, sub-account management | `gate-exchange-assets` / `gate-exchange-assets-manager` / `gate-exchange-subaccount` |
| Earn, staking, dual investment | `gate-exchange-simpleearn`, `gate-exchange-dual`, or related finance skills |
| Dedicated single-product depth (spot-only cases) | `gate-exchange-spot` |
| Futures-only advanced workflows | `gate-exchange-futures` |
| Unified mode switching, collateral matrix management | `gate-exchange-unified` |

### Signal dimensions (non-exclusive)

Detect **one or more** signals from the user query. Signals can stack (for example S5 then S2).

| Signal | Dimension | Typical triggers | Primary tool families |
|--------|-----------|------------------|------------------------|
| S1 | Spot trading | buy, sell, spot, limit, market, resting order | `cex_spot_*` |
| S2 | Futures | long, short, perp, contract, open, close, TP, SL, add/reduce size | `cex_fx_*` |
| S3 | Margin / borrow | isolated margin, borrow, repay, unified-account repay, leverage on spot margin | `cex_margin_*`, `cex_unified_*`, `cex_spot_*` (margin account) |
| S4 | Flash swap | flash swap, convert, swap coins | `cex_fc_*` |
| S5 | Positions / orders / history | show, view, positions, PnL, **orders**, **entrustments / working orders**, history, trades | `cex_fx_*`, `cex_spot_*`, `cex_margin_*`, `cex_alpha_*`, `cex_tradfi_query_*` |
| S6 | Order management | cancel, amend, replace | `cex_spot_*`, `cex_fx_*` |
| S7 | TradFi | gold, FX, stocks, MT5, TradFi | `cex_tradfi_*` |
| S8 | Alpha tokens | Alpha, on-chain token on Gate Alpha | `cex_alpha_*` |

**Scope note (L2 Tool Calls spec v1.3):** This skill focuses trading execution and **order / entrustment** reads. A **full cross-account asset inventory** (deep balance audit) belongs in **`gate-exchange-assets`**—do not expand S5 queries into asset-skill breadth unless the user clearly needs merged balances for a **drafted write** in this skill.

### Signal detection workflow (L2 Tool Calls spec v1.3)

Apply **before** Step 3 routing:

1. **Extract parameters** where present: `symbol` / `currency_pair`, `side`, `amount` / notional, `price` (for limits), `leverage` (futures / margin).
2. **Activate signals independently** (non-exclusive, multi-select): evaluate **S1–S6** from the table above; add **S7** / **S8** when TradFi / Alpha wording appears.
3. **Cross-margin wording rule:** If the user **explicitly** describes **cross-margin leverage** long or short in the **spot-margin** sense, activate **S3** (spot margin borrow + spot leg)—**do not** route that phrasing to **S2** futures. (See also **Pre-trade clarification** for default-to-spot-margin.)
4. **If no signal matches:** ask a short clarifying question, or route to **`gate-exchange-assets`** when the ask is account-wide audit with no trade intent.
5. **Execution mode (below)** follows activated signals.

### Execution mode

| Condition | Mode |
|-----------|------|
| **S5** (and/or **S7** / **S8**) **only** for **query**—no **S1**–**S6** execution intent and no **S7**/**S8** order placement | **Query-only**: fetch and summarize, no Action Draft for writes |
| Any **S1**–**S6** execution intent, **or** **S7**/**S8** execution (place/cancel/amend TradFi or Alpha orders) | **Write mode**: reads → Action Draft → **Y** → writes |

### Pair and amount conventions

- Spot and futures pairs use `BASE_QUOTE`, for example `BTC_USDT`.
- For `cex_spot_create_spot_order` with `type=market`: `side=buy` uses **quote** notional (USDT); `side=sell` uses **base** quantity.
- Futures sizes follow contract rules from `cex_fx_get_fx_contract` and account state from `cex_fx_get_fx_accounts`.
- **Isolated margin borrow/repay** maps to `cex_margin_create_uni_loan` (borrow and repay per tool contract). **Unified account** borrow/repay maps to `cex_unified_create_unified_loan`.

### L2 document names vs MCP tools (flash swap)

The L2 HTML spec may label the flash **quote** and **execute** steps with text that **does not** match registered MCP tool filenames. **Do not** treat those document strings as invocable MCP tools—use **only** the tools below (see **MCP Dependencies**).


### Flash swap tool families (multi-currency and composite legs)

**Scenario 6** (standalone single-leg flash, e.g. 500 USDT→ETH) and **scenario 19** (futures reduce plus flash in one plan) are **hidden** in this skill: **do not call any MCP tool** in this package for those intents, and **do not list tool names** when explaining the handoff—route users only to **`gate-exchange-flashswap`** and/or **`gate-exchange-futures`** or the Gate app as in **Workflow** Step 2 (see **Case Routing Map** rows 6 and 19).

| Flow | Signals | MCP tools |
|------|---------|-----------|
| Multi-currency flash (e.g. scenario 25) | S4 | `cex_fc_preview_fc_multi_currency_*` / `cex_fc_create_fc_multi_currency_*` |

### Regulatory, privacy, and risk notices (mandatory in replies)

- This skill is intended for users **aged 18 or above** with full civil capacity.
- **Digital asset trading involves significant risk and may result in partial or total loss of your investment.**
- **Leveraged trading (futures, margin, unified loans) may result in losses exceeding your initial margin. Small market movements can cause total margin loss.**
- **The above is for informational purposes only and does not constitute investment, financial, tax, or legal advice.**
- **AI-assisted outputs are for general information only and do not constitute any representation, warranty, or guarantee by Gate.**
- Users must comply with laws in their jurisdiction; Gate operates under multiple licenses and maintains restricted-region policies.
- Prompts and trading parameters are processed through the agent and MCP to reach Gate APIs only as needed to fulfill the request (no extra personal data collection beyond what the user supplies for trading).

## Workflow

### Step 1: Parse intent and parameters

Key data to extract:
- `currency_pair` or symbol, `side`, size or notional, `price`, `leverage`, time window for history queries
- Whether the user wants **query-only** or **execution** after pre-checks

Call `cex_spot_get_currency_pair` with:
- `currency_pair`: **only when** the user gives an ambiguous base-only symbol and you must confirm tradability before Step 3 — skip when the pair is already explicit (for example `BTC_USDT`).

Call `cex_spot_get_currency` with:
- `currency`: **only when** you need currency-level metadata to disambiguate a symbol — otherwise skip.

If required parameters are still missing, ask a short clarifying question instead of guessing.

### Step 2: Activate signals

Key data to extract:
- Which of `S1`–`S8` apply from the **Signal dimensions** table
- **Query-only** vs **write** mode (only S5 with no write intent → query-only)

**Hidden routes (evaluate before any MCP call in this step):**

- **Hidden scenario 6 (Case Routing row 6):** If the user intent is **only** standalone single-leg flash (quote asset to one base, e.g. 500 USDT→ETH) and matches that row, **stop**—do **not** call any MCP tool in this skill and do **not** display tool names to the user; hand off with **`gate-exchange-flashswap`** or the Gate app only. Skip Step 3–5 for this intent.

- **Hidden scenario 19 (Case Routing row 19):** If the user intent combines **futures position reduction** (trim, reduce, partial close) **with** a **flash swap / convert** leg in one plan (**S2** + **S4** composite), **stop**—do **not** call any MCP tool in this skill and do **not** display tool names; hand off with **`gate-exchange-futures`** and **`gate-exchange-flashswap`** (or the Gate app) only. Skip Step 3–5 for this intent.

Call `cex_spot_get_spot_accounts` with:
- `currency`: **only when** balance facts are required to disambiguate intent (for example sell-all or max-size wording) before Step 3 — skip when signals are clear from language alone.

### Step 3: Pre-trade reads (parallel when independent)

Run the minimal **Query Operations** set for the active signals (see **Case Routing Map**). Invoke independent calls in parallel when safe.

Call `cex_spot_get_spot_accounts` with: `currency` filters appropriate to spot or margin spot legs.

Call `cex_fx_get_fx_accounts` with: `settle` (typically `usdt`) when futures are in scope.

Call `cex_fx_get_fx_contract` with: `settle`, `contract` when sizing or margin rules for a futures leg.

Call `cex_fx_get_fx_tickers` with: `settle`, `contract` for futures reference prices.

Call `cex_spot_get_spot_tickers` with: `currency_pair` for spot reference prices.

Call `cex_margin_list_margin_accounts` with: API filters when isolated margin is in scope.

Call `cex_margin_get_uni_borrowable` with: borrow currency when planning isolated borrow.

Call `cex_margin_get_margin_uni_estimate_rate` with: parameters per API when interest context is needed.

Call `cex_unified_get_unified_accounts` with: per API when unified account state matters.

Call `cex_unified_get_unified_mode` with: per API **before** cross-margin / unified leveraged-long drafts (scenario 11 pattern); abort the write path if mode blocks that product.

Call `cex_unified_get_unified_borrowable` with: `currency` when planning unified borrow. **Scenario 11:** If the tool returns an error whose message indicates **single currency mode** is unsupported (e.g. contains `operation not support for single currency mode`, case-insensitive), do **not** continue to Action Draft—follow **Error Handling** (`unified_borrowable_single_currency_mode`) and prompt the user to enable **cross-currency margin mode** or **portfolio margin mode** on the unified account.

Call `cex_unified_list_unified_loan_records` with: filters per API when planning **unified-account loan repayment** (**scenario 14**): verify outstanding borrow and currency before drafting **`cex_unified_create_unified_loan`** (`type=repay`).

Call `cex_alpha_list_alpha_accounts` with: per API when Alpha is in scope.

Call `cex_alpha_quote_alpha_order` with: per API when Alpha pricing is needed before a draft.

Call `cex_tradfi_query_user_assets` with: per API when TradFi is in scope.

Call `cex_tradfi_query_symbols` / `cex_tradfi_query_symbol_ticker` / `cex_tradfi_query_symbol_detail` with: symbol resolution fields per API.


Call `cex_wallet_get_wallet_fee` with: per API **only if** fee display in the draft requires it and it was not yet fetched.

Key data to extract:
- Balances, borrowable limits, contract multipliers, reference prices, flash `quote_id` (if previewing), any API error codes

If a read fails, follow **Error Handling**; do not invent balances or prices.

### Step 4: Action Draft (mandatory before every write)

Key data to extract:
- Draft lines the user must confirm: product leg, pair/symbol, side, size/notional, price, fees/slippage, liquidation or margin warnings

Call no tool from **Execution Operations** in this step.

Call `cex_spot_get_spot_order_book` with: `currency_pair`, `limit` **only if** spread depth is required in the draft and was not fetched in Step 3.

Ask explicitly: **Reply Y to execute or N to cancel.** Treat confirmation as **single-use**; invalidate if parameters or intent change after the draft.

### Step 5: Execute after Y only

Pre-condition: explicit **Y** in the immediately previous user turn for this confirmation scope.

Call the matching write tool(s) after Y, for example:

Call `cex_spot_create_spot_order` / `cex_spot_create_spot_batch_orders` / `cex_spot_create_spot_price_triggered_order` with: confirmed order payload.

Call `cex_fx_create_fx_order` with: confirmed futures payload (including leverage updates via `cex_fx_update_fx_position_leverage` or dual-position tools **before** the order if required).

Call `cex_fx_create_fx_price_triggered_order` with: confirmed trigger payload.

Call `cex_margin_create_uni_loan` with: borrow/repay body per API.

Call `cex_unified_create_unified_loan` with: borrow/repay body per API.


Call `cex_alpha_place_alpha_order` with: confirmed Alpha payload.

Call `cex_tradfi_create_tradfi_order` with: confirmed TradFi payload.

Call `cex_spot_cancel_spot_order`, `cex_spot_cancel_all_spot_orders`, `cex_spot_amend_spot_order`, `cex_fx_cancel_fx_order`, `cex_fx_amend_fx_order`, or other listed cancel/amend tools with: confirmed ids/parameters.

Key data to extract:
- Order ids, `status`, error fields; **do not** auto-retry failed writes

Multi-leg flows need **separate** drafts and **separate** Y unless one combined draft lists every leg and receives one Y.

**Scenario 20 (S6 → S1) — confirmation is mandatory for each write:** Even if the user gives **one sentence** (“cancel all BTC orders and re-list limit …”), you MUST still issue **Action Draft 1** → wait for **Y** → call cancel-all → then **Action Draft 2** → wait for **Y** → call create. **Never** execute cancel or new limit **without** the matching **Y** after that draft (same rule as a standalone limit order).

### Step 6: Post-trade summary

Key data to extract:
- Filled size, remaining exposure, balances relevant to the user question

Call `cex_spot_list_spot_orders` with: `status` and pair filters **if** verifying spot open orders.

Call `cex_fx_list_fx_orders` with: per API **if** verifying futures open orders.

Call `cex_fx_list_fx_positions` with: `settle`, `holding` **if** verifying futures exposure.

Call `cex_spot_list_spot_my_trades` / `cex_fx_list_fx_my_trades` with: time range **if** reporting recent fills.

Return a concise summary plus mandatory disclaimers from **Domain Knowledge**.

## Case Routing Map (atomic chains, scenarios 1–26)

Use as patterns; always substitute real symbols and normalize API parameters. Aligns with **Trading Copilot L2 Tool Calls spec v1.3** (HTML source in the repository `docs/` folder): **15** base + **7** composite + **4** extended = **26** scenario slots; **scenarios 6 and 19 are hidden** (not routed here—hand off per **Workflow** Step 2 without naming tools). Apply **Pre-trade clarification** for futures and cross-margin rows before writes.

### Base scenarios (1–15)

| # | Intent | Signal | Read chain (parallel where possible) | Write chain (after Y) |
|---|--------|--------|--------------------------------------|------------------------|
| 1 | Spot market buy by USDT notional | S1 | `cex_spot_get_spot_accounts`, `cex_spot_get_spot_tickers` | `cex_spot_create_spot_order` |
| 2 | Spot limit sell | S1 | `cex_spot_get_spot_accounts` | `cex_spot_create_spot_order` |
| 3 | Futures open long with leverage | S2 | `cex_fx_get_fx_accounts`, `cex_fx_get_fx_contract`, `cex_fx_get_fx_tickers` | `cex_fx_create_fx_order` (and `cex_fx_update_fx_position_leverage` or dual-position tools first if required) |
| 4 | Futures take-profit on open position | S2 | `cex_fx_list_fx_positions`, `cex_fx_get_fx_tickers` | `cex_fx_create_fx_price_triggered_order` |
| 5 | Isolated margin short (borrow then sell spot) | S3 | `cex_margin_list_margin_accounts`, `cex_margin_get_uni_borrowable` | `cex_margin_create_uni_loan` (borrow) → `cex_spot_create_spot_order` (sell) |
| 6 | **HIDDEN** — single-leg flash (e.g. 500 USDT→ETH) | — | **No MCP tools** in this skill | **No writes** — hand off to **`gate-exchange-flashswap`** or app **without naming tools** |
| 7 | **Recent futures orders / entrustments** (open + recent finished; query) | S5 | `cex_fx_list_fx_orders` (e.g. open; **finished** with time window such as last 7 days or user range)—summarize **current working orders + recent ended entrustments**; if **no** contract filter, ask pair or return API-allowed scope | none |
| 8 | Cancel a specific spot order | S6 | `cex_spot_list_spot_orders` (open) | `cex_spot_cancel_spot_order` |
| 9 | List open orders (spot + futures) | S5 | `cex_spot_list_spot_orders`, `cex_fx_list_fx_orders` | none |
| 10 | Recent fills / history window | S5 | `cex_spot_list_spot_my_trades`, `cex_fx_list_fx_my_trades` (and `cex_spot_list_spot_orders` / `cex_fx_list_fx_orders` with finished filters if needed) | none |
| 11 | Cross-style leverage long (borrow quote then buy base) | S3 | `cex_unified_get_unified_mode` · `cex_unified_get_unified_accounts`, `cex_unified_get_unified_borrowable`, `cex_spot_get_spot_tickers` — if **`cex_unified_get_unified_borrowable`** error message matches single-currency-mode unsupported, stop (see **Error Handling**) | `cex_unified_create_unified_loan` (borrow) → `cex_spot_create_spot_order` (buy, cross_margin / unified per API) |
| 12 | Futures add to position | S2 | `cex_fx_list_fx_positions`, `cex_fx_get_fx_accounts`, `cex_fx_get_fx_contract`, `cex_fx_get_fx_tickers` | `cex_fx_create_fx_order` |
| 13 | Futures reduce position (for example half) | S2 | `cex_fx_list_fx_positions`, `cex_fx_get_fx_tickers` | `cex_fx_create_fx_order` (`reduce_only` semantics per API) |
| 14 | **Unified-account loan repayment** (e.g. repay 10 USDT of borrow) | S3 | `cex_unified_list_unified_loan_records`, `cex_unified_get_unified_accounts` — confirm currency (e.g. **USDT** for “10U”) and outstanding borrow vs available balance | **`cex_unified_create_unified_loan`** (`type=repay`, amount per draft) after **Y** |
| 15 | Futures stop / trigger when price breaches level | S2 | `cex_fx_list_fx_positions` | `cex_fx_create_fx_price_triggered_order` |

### Composite scenarios (16–22)

| # | Intent | Signals | Read chain | Write chain (after Y; separate drafts if user prefers) |
|---|--------|---------|------------|---------------------------|
| 16 | Query PnL then reduce if above threshold | S5 → S2 | `cex_fx_list_fx_positions`, `cex_fx_get_fx_tickers` | If condition met: `cex_fx_create_fx_order` (reduce); else query-only |
| 17 | Close long then open short same contract | S2 + S2 | `cex_fx_list_fx_positions`, `cex_fx_get_fx_accounts`, `cex_fx_get_fx_contract`, `cex_fx_get_fx_tickers` | Draft 1 close → Y → `cex_fx_create_fx_order`; Draft 2 open → Y → `cex_fx_create_fx_order` |
| 18 | Spot buy plus futures open same underlying | S1 + S2 | `cex_spot_get_spot_accounts`, `cex_fx_get_fx_accounts`, `cex_spot_get_spot_tickers`, `cex_fx_get_fx_tickers`, `cex_fx_get_fx_contract` | One combined draft → Y → `cex_spot_create_spot_order` and `cex_fx_create_fx_order` (parallel if user confirmed both) |
| 19 | **HIDDEN** — futures reduce plus flash swap | — | **No MCP tools** in this skill | **No writes** — hand off to **`gate-exchange-futures`** and **`gate-exchange-flashswap`** or app **without naming tools** |
| 20 | Cancel all open on pair then limit re-place | S6 → S1 | `cex_spot_list_spot_orders`, `cex_spot_get_spot_accounts` | **Draft 1 → Y** → `cex_spot_cancel_all_spot_orders`; **Draft 2 → Y** → `cex_spot_create_spot_order` — **two confirmations required** (see **Workflow** Step 5); do **not** skip Action Draft for either leg |
| 21 | Margin sufficiency check then open plus TP | S5 → S2 | `cex_fx_get_fx_accounts`, `cex_fx_list_fx_positions`, `cex_unified_get_unified_accounts`, `cex_fx_get_fx_contract`, `cex_fx_get_fx_tickers` | Y → `cex_fx_create_fx_order` → `cex_fx_create_fx_price_triggered_order` |
| 22 | Spot sell quote proceeds then futures open | S1 → S2 | `cex_spot_get_spot_accounts`, `cex_spot_get_spot_tickers`, then after fill context `cex_fx_get_fx_contract`, `cex_fx_get_fx_tickers` | Y → `cex_spot_create_spot_order`; Y → `cex_fx_create_fx_order` |

### Extended scenarios (23–26)

| # | Intent | Signal | Read chain | Write chain (after Y) |
|---|--------|--------|------------|------------------------|
| 23 | TradFi notional buy (for example metals) | S7 | `cex_tradfi_query_user_assets`, `cex_tradfi_query_symbols` / `cex_tradfi_query_symbol_ticker` | `cex_tradfi_create_tradfi_order` |
| 24 | Alpha market buy after quote | S8 | `cex_alpha_list_alpha_accounts`, `cex_alpha_quote_alpha_order` | `cex_alpha_place_alpha_order` |
| 25 | Flash swap one-to-many (split quote asset) | S4 | Multi preview per API (MCP: `cex_fc_preview_fc_multi_currency_one_to_many_order`) | Multi create (MCP: `cex_fc_create_fc_multi_currency_one_to_many_order`) |
| 26 | Alpha positions and PnL (query) | S5 | `cex_alpha_list_alpha_accounts`, `cex_alpha_list_alpha_orders` or account book tools as needed | none |

Composite and multi-leg flows follow the same rule: **one Action Draft per confirmation scope**, never skip confirmation on any write; use **separate** drafts and **separate** Y when legs are independent.

## Judgment Logic Summary

| Condition | Action |
|-----------|--------|
| User asks for research-first narrative or coin deep-dive without immediate execution | Prefer dedicated info/news skills; here only assist if execution parameters are already explicit |
| Only status / PnL / orders / history | Query tools only; no write calls |
| Any create/cancel/amend/borrow/repay/swap/order | Action Draft → Y/N → write |
| User refuses, says N, or confirmation not in previous turn | No write; offer to adjust draft |
| Parameters change after Y | Invalidate confirmation; re-draft |
| Insufficient balance or borrowable | Do not write; show shortfall and options |
| Scenario 11 and `cex_unified_get_unified_borrowable` signals single-currency mode | Same as **Error Handling** row `unified_borrowable_single_currency_mode`—require cross-currency or portfolio unified mode before continuing |
| Futures or margin involved | Always surface leverage and liquidation-related risk in the draft |
| Flash preview unavailable | Explain pair unsupported or transient error; suggest spot path if appropriate |
| User intent matches **hidden scenario 6** (standalone single-leg flash only, e.g. 500 USDT→ETH) | **No MCP calls** in this skill; **do not** display tool names—direct the user to **`gate-exchange-flashswap`** or the Gate app |
| User intent matches **hidden scenario 19** (futures reduce plus flash in one plan) | **No MCP calls** in this skill; **do not** display tool names—direct the user to **`gate-exchange-futures`** and **`gate-exchange-flashswap`** (or the Gate app) |
| **Scenario 7** (recent futures orders / entrustments) | **Query-only** via `cex_fx_list_fx_orders`; **do not** substitute a full **`gate-exchange-assets`**-style merged balance/PnL pull unless the user’s write path requires it |
| **Scenario 14** (unified repay only) | Action Draft → **Y** → `cex_unified_create_unified_loan` (repay)—**not** the same as cross-margin **sell spot + repay** (route **`gate-exchange-margin`** / **`gate-exchange-unified`** for that narrative) |
| **Scenario 20** (cancel-all then re-place limit) | **Two** Action Drafts and **two** **Y** replies required—**never** auto-execute both legs from one user message without confirmations |

## Report Template

```markdown
## Trading Copilot Result

| Item | Value |
|------|-------|
| Mode | query-only / write |
| Signals | {S1..S8} |
| Legs | {spot / futures / margin / fc / alpha / tradfi} |
| Status | {executed / draft-pending / blocked / error} |

### Action Draft (if applicable)
{draft_details}

### Execution Summary
{fills, order ids, balances}

### Risk and disclaimers
Digital asset trading involves significant risk. Leveraged products may lose more than initial margin.
Information is not investment advice. AI output is not a guarantee by Gate.
```

## Error Handling

| Error type | Typical cause | Handling |
|------------|----------------|----------|
| Balance or borrowable insufficient | User size too large | Show deficit; suggest smaller size or funding |
| Minimum size / precision | Below exchange minimum | Quote `cex_spot_get_currency_pair` rules; fix amount |
| Auth or permission | API key scope | Tell user which product permission is missing |
| stale_confirmation | User said Y for an older draft | Re-issue Action Draft |
| Read partial failure | One account endpoint empty | Proceed with stated gaps; warn in draft |
| `unified_borrowable_single_currency_mode` (scenario 11) | `cex_unified_get_unified_borrowable` fails; API/message indicates operation not supported in **single currency** unified mode (e.g. message contains `operation not support for single currency mode`, case-insensitive) | Do not draft or write. Tell the user to switch the unified account to **cross-currency margin mode** or **portfolio margin mode** in the app, then try again |
| Write rejected | Exchange error | Show message; no silent retry |

## Safety Rules

### Confirmation (mandatory)

- Never call **Execution Operations (Write)** without explicit **Y** after the matching Action Draft in the conversation flow.
- Never batch unrelated writes under one Y unless the user confirmed **all** legs in one combined draft.
- If the user asks to skip confirmation, refuse writes and stay read-only.

### Best-effort checks

- Verify balances, borrowable, and contract constraints before drafting.
- Do not fabricate prices, fees, or order ids.

For additional scenario-level examples, see `references/scenarios.md`.
