---
name: gate-exchange-flashswap-assistant
version: "2026.3.31-2"
updated: "2026-03-31"
description: "L2 flash swap orchestration: fc preview and create (1:1, 1:N, N:1), spot balance checks, min/max gates, optional dust-to-GT, order history. Use this skill whenever the user wants flash swap, instant convert, consolidate alts to one coin, split one asset into several via flash, diagnose below-minimum flash size, or convert wallet dust to GT. Trigger phrases include \"flash swap\", \"flash convert\", \"swap to USDT\", \"consolidate to USDT\", \"dust to GT\", \"small balance to GT\", or \"flash swap history\"."
---

# gate-exchange-flashswap-assistant

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
| Gate (main) | Required |

### MCP Tools Used

**Query Operations (Read-only)**

- `cex_fc_get_fc_order`
- `cex_fc_list_fc_currency_pairs`
- `cex_fc_list_fc_orders`
- `cex_fc_preview_fc_multi_currency_many_to_one_order`
- `cex_fc_preview_fc_multi_currency_one_to_many_order`
- `cex_fc_preview_fc_order_v1`
- `cex_spot_get_spot_accounts`
- `cex_wallet_list_small_balance`
- `cex_wallet_list_small_balance_history`

**Execution Operations (Write)**

- `cex_fc_create_fc_multi_currency_many_to_one_order`
- `cex_fc_create_fc_multi_currency_one_to_many_order`
- `cex_fc_create_fc_order_v1`
- `cex_wallet_convert_small_balance`

### Authentication

- API Key Required: Yes (authenticated Gate Exchange MCP)
- Permissions: Flash convert (`cex_fc_*`) write, spot account read, wallet small-balance read and convert as required by the gateway (configure keys with least privilege)
- Get API Key: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check

- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

---

## Domain Knowledge

### What this skill covers

- **Flash swap (fc)**: Instant convert using preview then create. Three modes: **one-to-one**, **one-to-many** (one sell asset to multiple buy assets), **many-to-one** (multiple sell assets to one buy asset, consolidation).
- **On-path balance checks**: Use `cex_spot_get_spot_accounts` for the sell-side (and USDT side for one-to-many) **only** for this flow. Do **not** pull full portfolio views here.
- **Two different “small balance” paths (must explain to the user)**:
  - **Flash swap**: Subject to per-pair `sell_min_amount` / `sell_max_amount` from `cex_fc_list_fc_currency_pairs`. If below minimum, **do not** call fc preview to fake a quote.
  - **Wallet dust → GT**: `cex_wallet_list_small_balance` / `cex_wallet_convert_small_balance` converts platform-classified dust to **GT** (not USDT). Rules differ from flash minima; never silently substitute this when the user asked for USDT flash swap.

### Core concepts

- **quote_id**: From preview; required for create. Validity comes from `valid_timestamp` in the response — never assume a fixed TTL.
- **sell_amount / buy_amount**: Use one per leg as required by the API; one-to-many can use per-target `sell_amount` or `buy_amount`; many-to-one uses per-source `sell_amount`.
- **Order status**: `status=1` success, `status=2` failure — verify after each create.
- **Precision**: Show tiny receive amounts with clear precision; optional rough fiat hint only when clearly justified.

### Explicitly out of scope for tools in this skill

- Do **not** call `cex_spot_get_spot_tickers`, `cex_spot_get_spot_order_book`, or `cex_wallet_get_total_balance` from this skill. Market depth, “is it a good time”, and full asset audits belong to other skills (see Judgment Logic Summary).

### Regulatory and risk notices

- Digital asset trading involves significant risk and may result in partial or total loss of your investment.
- This skill is intended for users aged 18 or above with full civil capacity. Users must comply with applicable laws in their jurisdiction.
- AI-assisted outputs and tool results are for general information only and do not constitute investment, financial, tax, or legal advice, or any representation or warranty by Gate.
- Prompts and trading-related inputs are processed to call the Gate API via MCP; do not collect unnecessary personal data.

---

## Atomic Tool Call Chains (mandatory)

**Execution rule:** Map the user request to **scenario #1–#21** below when possible. **Follow the listed tool order.** Do not skip gates (balance, `sell_min_amount`, preview before create).

**Notation**

- **`[P1] Parallel`**: Invoke the listed tools in the same wave (any order among them is acceptable unless a later step depends on their output).
- **`→`**: Serial — complete the previous step before starting the next.
- **`[P0] Plan`**: No MCP call — parse amounts, split ratios, or restrict the coin set (e.g. user-supplied list only).
- **`[Confirm]`**: Present Action Draft; wait for explicit **Y** before any **write** tool in that branch.
- **`(W)`**: Write tool — only after **Confirm** unless the scenario explicitly ends at preview-only.

**Routing reminders (from spec)**

- One-to-many rows **#4**, **#5**, **#11**: If the user uses **only** spot **buy / market buy** language with **no** flash swap / convert / swap anchor, route **`gate-exchange-trading`** instead of fc tools.
- **#8**, **#20**: Preview-only until the user opts in to create.
- **#21**: Never mix dust→GT silently into a “swap to USDT” story without explaining the different product path.

### Base scenarios (#1–#8)

| # | User intent (paraphrase) | Mode | Signal | Atomic chain |
|---|--------------------------|------|--------|----------------|
| 1 | Swap a fixed amount (e.g. 1 BTC) to USDT | 1→1 | S1 | **[P1]** `cex_fc_list_fc_currency_pairs`(sell asset) · `cex_spot_get_spot_accounts`(sell asset) **→** Check available ≥ sell amount and sell amount ≥ `sell_min_amount` **→** `cex_fc_preview_fc_order_v1`(sell_asset, sell_amount, buy_asset) **→** Show rate, estimated receive, validity → Action Draft **→** **[Confirm]** **→** **(W)** `cex_fc_create_fc_order_v1`(quote_id, matching amounts) **→** Verify `status` **→** Report result |
| 2 | Swap **full** available balance of one asset to USDT (e.g. take-profit SOL) | 1→1 | S1 | **[P1]** `cex_spot_get_spot_accounts`(asset) · `cex_fc_list_fc_currency_pairs`(asset) **→** Set `sell_amount` = available; check ≥ `sell_min_amount` **→** `cex_fc_preview_fc_order_v1` **→** Action Draft **→** **[Confirm]** **→** **(W)** `cex_fc_create_fc_order_v1` **→** Verify `status` |
| 3 | After deposit, swap asset A to USDT | 1→1 | S1 | **[P1]** `cex_spot_get_spot_accounts`(A) · `cex_fc_list_fc_currency_pairs`(A) **→** Confirm balance and min/max **→** `cex_fc_preview_fc_order_v1`(A→USDT) **→** Action Draft **→** **[Confirm]** **→** **(W)** `cex_fc_create_fc_order_v1` **→** Verify `status` |
| 4 | One source (e.g. 3000 USDT) flash into multiple targets with set spend per target (e.g. 1000 USDT each to BTC, ETH, SOL) | 1→N | S2 | **[P1]** `cex_spot_get_spot_accounts`(USDT) · `cex_fc_list_fc_currency_pairs`(each target asset) **→** Check USDT ≥ total spend; each leg `sell_amount` ≥ that pair’s `sell_min_amount` **→** `cex_fc_preview_fc_multi_currency_one_to_many_order`(params for each leg) **→** Show per-leg quote; highlight failures **→** Action Draft **→** **[Confirm]** **→** **(W)** `cex_fc_create_fc_multi_currency_one_to_many_order`(params, exclude failed preview legs) **→** Verify each leg `status` |
| 5 | One source split by ratio (e.g. 1000 USDT: half BTC, half ETH) | 1→N | S2 | **[P0]** Compute per-leg `sell_amount` from user ratio **→** **[P1]** `cex_spot_get_spot_accounts`(USDT) · `cex_fc_list_fc_currency_pairs`(each target) **→** `cex_fc_preview_fc_multi_currency_one_to_many_order` **→** Action Draft **→** **[Confirm]** **→** **(W)** `cex_fc_create_fc_multi_currency_one_to_many_order` **→** Verify `status` |
| 6 | Named multiple assets → one target (e.g. BTC, ETH, DOGE → USDT), full balances | N→1 | S3 | **[P1]** `cex_spot_get_spot_accounts`(each source) · `cex_fc_list_fc_currency_pairs`(each source) **→** Drop legs with balance &lt; `sell_min_amount` or zero; tell user which are skipped **→** `cex_fc_preview_fc_multi_currency_many_to_one_order`(remaining legs) **→** Action Draft **→** **[Confirm]** **→** **(W)** `cex_fc_create_fc_multi_currency_many_to_one_order` **→** Verify each leg `status` |
| 7 | List recent flash swap history | Query | S4 | **[P1]** `cex_fc_list_fc_orders`(e.g. limit=20) **→** Format table: time / sell / buy / amounts / `status` |
| 8 | Preview only: how much USDT for asset X (e.g. SOL), decide later | 1→1 | S1 | **[P1]** `cex_fc_list_fc_currency_pairs`(X) · `cex_spot_get_spot_accounts`(X) **→** `cex_fc_preview_fc_order_v1`(full or partial amount) **→** Show rate, estimated receive, validity **only** **→** If user **Y** → Action Draft **→** **[Confirm]** **→** **(W)** `cex_fc_create_fc_order_v1`; if **N** → stop (no write) |

### Extended scenarios (#9–#13)

| # | User intent (paraphrase) | Signal | Atomic chain |
|---|--------------------------|--------|----------------|
| 9 | Whether a coin (e.g. APT) supports flash swap / pair limits | S4 | **[P1]** `cex_fc_list_fc_currency_pairs`(currency) **→** If empty: not supported; suggest spot trading skill **→** If rows: show pairs and min/max |
| 10 | Did the latest flash swap succeed | S4 | **[P1]** `cex_fc_list_fc_orders`(limit=1) **→** Take newest `order_id` **→** `cex_fc_get_fc_order`(order_id) **→** Report `status` (1 success / 2 fail), fills |
| 11 | USDT flash into target **buy amounts** (e.g. 0.1 BTC and 1 ETH) | S2 | **[P0]** Build params with `buy_amount` per leg (not `sell_amount`) **→** **[P1]** `cex_spot_get_spot_accounts`(USDT) · `cex_fc_list_fc_currency_pairs`(each target) **→** `cex_fc_preview_fc_multi_currency_one_to_many_order` **→** Check total USDT consumed vs available (e.g. `total_consume_amount` or equivalent field) **→** Action Draft per leg **→** **[Confirm]** **→** **(W)** `cex_fc_create_fc_multi_currency_one_to_many_order` **→** Verify each `status` |
| 12 | One-to-one non-USDT leg (e.g. 2 ETH → BTC) | S1 | **[P1]** `cex_spot_get_spot_accounts`(ETH) · `cex_fc_list_fc_currency_pairs`(ETH) **→** Check ≥ amount and min/max **→** `cex_fc_preview_fc_order_v1`(sell ETH, buy BTC, …) **→** Action Draft (state single-hop flash, not “via USDT”) **→** **[Confirm]** **→** **(W)** `cex_fc_create_fc_order_v1` **→** Verify `status` |
| 13 | Multiple named alts → USDT; user may not know balances | N→1 | S3 | **[P1]** `cex_spot_get_spot_accounts`(each) · `cex_fc_list_fc_currency_pairs`(each) **→** Filter zero or &lt; `sell_min_amount`; explain skips **→** `cex_fc_preview_fc_multi_currency_many_to_one_order` **→** Action Draft **→** **[Confirm]** **→** **(W)** `cex_fc_create_fc_multi_currency_many_to_one_order` **→** Verify each leg |

### Dust, small size, and split scenarios (#14–#21)

| # | User intent (paraphrase) | Signal | Atomic chain |
|---|--------------------------|--------|----------------|
| 14 | “Too small” / may be below flash min (e.g. PEPE) | S5 | **[P1]** `cex_fc_list_fc_currency_pairs`(asset) · `cex_spot_get_spot_accounts`(asset) **→** If available &lt; `sell_min_amount`: **do not** call `cex_fc_preview_*`; show balance / min / gap **→** `cex_wallet_list_small_balance` **→** If asset in dust list: explain **S7** dust→GT path; else suggest accumulate or spot sell (trading copilot) **→** If available ≥ min: continue **scenario #1**-style S1 chain |
| 15 | Small total one-to-many (e.g. 30 USDT split across DOGE and SHIB) | S2 | **[P0]** Confirm per-leg USDT split with user if unclear **→** **[P1]** `cex_spot_get_spot_accounts`(USDT) · `cex_fc_list_fc_currency_pairs`(each target) **→** Ensure each leg ≥ `sell_min_amount`; if not, ask to adjust **→** `cex_fc_preview_fc_multi_currency_one_to_many_order` **→** Highlight failed legs; Action Draft **→** **[Confirm]** **→** **(W)** `cex_fc_create_fc_multi_currency_one_to_many_order`(confirmed params) |
| 16 | Single-asset amount exceeds `sell_max_amount` (must split batches) | S6 | **[P1]** `cex_spot_get_spot_accounts`(asset) · `cex_fc_list_fc_currency_pairs`(asset) **→** Read `sell_max_amount`; plan batches each ≤ max **→** **For batch k:** `cex_fc_preview_fc_order_v1` **→** Action Draft **→** **[Confirm]** **→** **(W)** `cex_fc_create_fc_order_v1` **→** Verify `status` **→** **Re-query** `cex_spot_get_spot_accounts` before batch k+1 **→** New preview (new `quote_id`) for next batch |
| 17 | Several tickers → USDT; “swap everything that can” | N→1 | S3 | **[P1]** For each ticker: `cex_spot_get_spot_accounts` · `cex_fc_list_fc_currency_pairs` (parallel per asset) **→** Build table **A** (execute: balance ≥ min and pair exists) and **B** (skip: zero / &lt; min / unsupported) **→** If A empty: stop with explanation **→** Else `cex_fc_preview_fc_multi_currency_many_to_one_order`(A) **→** Action Draft (include B summary) **→** **[Confirm]** **→** **(W)** `cex_fc_create_fc_multi_currency_many_to_one_order` **→** Verify each |
| 18 | Ask min flash amount and whether current balance qualifies | S4 | **[P1]** `cex_fc_list_fc_currency_pairs`(asset) · `cex_spot_get_spot_accounts`(asset) **→** Report `sell_min_amount`, `sell_max_amount`, available, pass/fail **→** If user then says swap all: run **scenario #1** or **#2** |
| 19 | User supplies an explicit coin list in session (paste / list); flash all that can to USDT | N→1 | S3 | **[P0]** Scope = coins the user named in this request; if none, ask for list **→** Same as **#17** (parallel spot + list per coin → A/B → preview many-to-one → confirm → create → verify) |
| 20 | Tiny amount preview only (e.g. 5 USDT → SAT), not urgent to fill | S1 | **[P1]** `cex_fc_list_fc_currency_pairs`(target) · `cex_spot_get_spot_accounts`(USDT) **→** If sell-side USDT &lt; `sell_min_amount`: **S5** path; no preview **→** Else `cex_fc_preview_fc_order_v1` **→** Show receive with precision note; default **no** auto-create |
| 21 | Clear wallet dust to GT | S7 | **[P1]** `cex_wallet_list_small_balance`() **→** Show convertible dust list **→** Action Draft: state **GT** outcome and `cex_wallet_convert_small_balance`; confirm `currencies` or `is_all` **→** **[Confirm]** **→** **(W)** `cex_wallet_convert_small_balance` **→** Optionally `cex_wallet_list_small_balance_history` |

---

## Workflow

### Step 1: Route intent and select signal S1–S7

**First**, try to match **Atomic Tool Call Chains** scenario **#1–#21** and execute that chain **as written** (parallel vs serial, preview gates, confirm before writes).

If no row fits, fall back: classify the request. If it belongs to **out of scope** (see **Judgment Logic Summary**), stop and name the appropriate skill without calling fc or wallet convert tools.

If in scope but not tabulated, assign one or more signals: **S1** one-to-one flash, **S2** one-to-many flash, **S3** many-to-one consolidation, **S4** query or history, **S5** below-minimum or dust diagnosis, **S6** split over `sell_max_amount`, **S7** dust to GT.

Key data to extract:

- `signal`: S1 | S2 | S3 | S4 | S5 | S6 | S7 (combinations allowed, e.g. S5 then S1)
- `sell_assets`, `buy_asset`, amounts, and whether the user asked for **preview only**
- `user_confirmed_flash_language`: user used flash swap / convert / swap narrative vs pure spot **buy** wording (see routing table)

### Step 2: Parallel gateway reads (flash paths S1–S3, S5, S6)

Call `cex_fc_list_fc_currency_pairs` with:

- `currency` (or equivalent filter per MCP): each sell asset (and targets as needed)

Call `cex_spot_get_spot_accounts` with:

- Parameters needed to read **available** balance for each relevant currency (sell side and USDT for one-to-many)

Key data to extract:

- `sell_min_amount`, `sell_max_amount` per pair
- `available` balances
- Whether each leg passes min gate **before** preview

**S5 rule**: If `available` < `sell_min_amount` for a flash leg, **do not** call `cex_fc_preview_*` for that leg. Present a clear table (balance vs min gap) and optionally call `cex_wallet_list_small_balance` to see if **S7** applies.

**S6 rule**: If amount > `sell_max_amount`, plan sequential batches; each batch needs its own preview, Action Draft, **Y**, create, and post-create balance refresh before the next preview. Cap planned batches at a reasonable maximum (for example 20) or stop if the user cancels — do not loop without bound.

### Step 3: Preview (choose one preview tool by mode)

**One-to-one (S1)** — Call `cex_fc_preview_fc_order_v1` with `sell_asset`, `buy_asset`, and either `sell_amount` or `buy_amount`.

**One-to-many (S2)** — Call `cex_fc_preview_fc_multi_currency_one_to_many_order` with `params` array (per leg amounts). Highlight per-leg preview errors.

**Many-to-one (S3)** — After filtering legs below min or zero balance, call `cex_fc_preview_fc_multi_currency_many_to_one_order` with `params` for remaining legs. Present **will execute** vs **skipped** summary.

Key data to extract:

- `quote_id` per successful leg
- Rates, receive amounts, `valid_timestamp`
- Any per-leg errors for user-visible highlighting

### Step 4: Action Draft and explicit confirmation (all writes)

Present an **Action Draft** listing sell/buy assets, amounts, effective rate or receive estimate, quote validity, and multi-leg status. For **S7**, the draft must state that the operation is **dust to GT** via `cex_wallet_convert_small_balance`, not USDT flash swap.

Wait for explicit **Y** to execute or **N** to cancel. Without **Y**, call **no** write tool.

Key data to extract:

- `user_confirmation`: Y | N
- Whether parameters still match the last preview (if not, re-preview)

### Step 5: Execute flash swap creates (after Y, one create family per request)

Use exactly one of:

Call `cex_fc_create_fc_order_v1` with body fields including `quote_id` and matching sell/buy amounts from preview.

Call `cex_fc_create_fc_multi_currency_one_to_many_order` with `params` including each leg `quote_id` and amounts — **exclude** failed preview legs.

Call `cex_fc_create_fc_multi_currency_many_to_one_order` with `params` including each leg `quote_id` and amounts — **exclude** failed preview legs.

Key data to extract:

- Per-order `status` and IDs
- Errors returned by the API

### Step 6: Verify order outcome

For each created order, read `status`. If needed, Call `cex_fc_get_fc_order` with the order id to confirm details.

Key data to extract:

- Success vs failure per leg
- Final received amounts where provided

### Step 7: Query and history paths (S4)

Call `cex_fc_list_fc_orders` with appropriate `limit` / filters for history or “latest order”.

Call `cex_fc_get_fc_order` with `order_id` when the user needs detail on a specific id or you took the latest id from list.

For supported-pair or min/max questions, use `cex_fc_list_fc_currency_pairs` and `cex_spot_get_spot_accounts` as needed.

For dust **history**, Call `cex_wallet_list_small_balance_history` with optional filters per MCP.

Key data to extract:

- Human-readable table: time, sides, amounts, status

### Step 8: Dust to GT path (S7)

Call `cex_wallet_list_small_balance` (no substitute for “list all account dust” beyond this tool’s contract).

Present the convertible list. Action Draft must specify `currencies` or `is_all` exactly as the user confirmed.

After **Y**, Call `cex_wallet_convert_small_balance` with the confirmed parameters.

Key data to extract:

- Conversion result or error; optional follow-up with `cex_wallet_list_small_balance_history`

---

## Judgment Logic Summary

### Signal definitions

| Signal | Meaning | Primary tools |
|--------|---------|---------------|
| S1 | One-to-one flash | `cex_fc_list_fc_currency_pairs`, `cex_spot_get_spot_accounts`, `cex_fc_preview_fc_order_v1`, `cex_fc_create_fc_order_v1` |
| S2 | One-to-many flash (user anchors flash/convert/swap, not pure spot buy) | `cex_fc_preview_fc_multi_currency_one_to_many_order`, `cex_fc_create_fc_multi_currency_one_to_many_order` |
| S3 | Many-to-one consolidation | `cex_fc_preview_fc_multi_currency_many_to_one_order`, `cex_fc_create_fc_multi_currency_many_to_one_order` |
| S4 | Queries: history, support, min check, order status | `cex_fc_list_fc_orders`, `cex_fc_get_fc_order`, `cex_fc_list_fc_currency_pairs`, `cex_wallet_list_small_balance_history` |
| S5 | Below flash minimum / fragile balance | Reads only until min met; optional `cex_wallet_list_small_balance` → offer S7 |
| S6 | Amount over `sell_max_amount` | Same create family as S1/S2/S3 but **sequential** batches with fresh preview and confirmation per batch |
| S7 | Dust to GT | `cex_wallet_list_small_balance`, `cex_wallet_convert_small_balance` |

### Out of scope routing (do not use this skill’s tool list)

| User intent | Route to |
|-------------|----------|
| Research, “why”, slippage, depth, liquidity, charts | `gate-info-research` or `gate-exchange-trading` (no tickers/order book from here) |
| Spot **buy/sell** narrative (market/limit, “buy some”, “DCA”, “bid”) without flash/convert anchor | `gate-exchange-trading` |
| Futures / margin trading | `gate-exchange-trading` or domain futures/margin skills |
| Transfers between accounts (spot ↔ futures, subaccounts) | `gate-exchange-transfer` |
| Full portfolio, margin risk, liquidation context | `gate-exchange-assets-manager` or `gate-exchange-assets` |
| Earn / staking | `gate-exchange-simpleearn` or relevant earn skill |
| On-chain DEX swap | DEX skills (e.g. `gate-dex-trade`) |

### Mode detection

- **One-to-one**: One sell asset and one buy asset; no multi-asset split wording.
- **One-to-many**: One sell asset, multiple buy assets; user must anchor **flash swap / convert**, not only “buy multiple”.
- **Many-to-one**: Multiple sell assets into one buy asset, or words like “consolidate”, “convert all to USDT”.
- If unclear: ask whether the user wants **one source → many targets** or **many sources → one target**.

---

## Report Template

### Flash swap Action Draft (before any fc create)

- Mode (one-to-one / one-to-many / many-to-one)
- Each leg: sell asset and amount → buy asset and expected receive (from preview)
- Quote validity: reference `valid_timestamp` (do not invent seconds)
- Risk line: instant execution; final result from API
- Ask: Reply **Y** to execute or **N** to cancel

### S5 diagnostic (no preview)

- Asset, available balance, `sell_min_amount`, shortfall
- Next options: accumulate, spot trade via trading copilot, or check dust list for **GT** path (S7)

### Dust to GT Action Draft

- Explicit: operation is **small balance convert to GT**, not USDT flash
- Coins or `is_all` exactly as user confirmed
- **Y** / **N**

### After execution

- Per-leg status and amounts
- Reminder: digital asset transactions are generally irreversible; flash fills are immediate

---

## Safety Rules

### Confirmation

- **No** `cex_fc_create_*` and **no** `cex_wallet_convert_small_balance` without prior Action Draft and explicit **Y**.
- **Never** use an expired or stale `quote_id`; if the user delayed, re-preview.
- **Never** call fc preview solely to mask a below-minimum balance.

### Proportionality

- Pass only minimum parameters to MCP tools. Do not send unrelated conversation content as tool input.

---

## Error Handling

| Situation | Action |
|-----------|--------|
| `cex_fc_list_fc_currency_pairs` fails | State limits unknown; warn before preview; avoid guessing min/max |
| Preview returns error | Do not create; show message; suggest adjusting size or spot path |
| Create returns failure | Do not auto-retry; suggest fresh preview |
| `cex_spot_get_spot_accounts` fails | Warn balance unknown; do not invent balances |
| `cex_wallet_list_small_balance` fails | Do not call convert; explain dust list unavailable |
| `cex_wallet_convert_small_balance` fails | Show error; no silent retry |
| User says N after draft | Stop; no writes |

---

## Reference

- **Normative tool order** for mapped stories: **Atomic Tool Call Chains** (scenarios #1–#21) above
- Human-readable scenarios and prompt examples: `references/scenarios.md`
- Shared disambiguation: read `gate-skills-disambiguation.md` from your skills root when present
