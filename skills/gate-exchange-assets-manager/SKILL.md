---
name: gate-exchange-assets-manager
version: "2026.3.25-1"
updated: "2026-03-25"
description: "Gate multi-account asset manager L2 skill. Use when the user asks to check total assets combined with margin/liquidation risk or earnings snapshots. Triggers on 'total assets', 'margin check', 'liquidation risk', 'earn interest', 'staking rewards', 'affiliate commissions', 'borrow USDT', 'add margin', 'set collateral'."
---

# Gate Account and Asset Manager

This is an L2 composite skill that orchestrates 58 deduplicated MCP tool calls (54 read + 4 write) across 7 L1 skills. It provides a unified entry point for account and asset overview, margin and liquidation risk assessment, SimpleEarn and staking earnings snapshots, affiliate commission queries, and unified-account write operations (borrowing, collateral, leverage settings).

This skill is intended for users aged 18 or above with full civil capacity.

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

- cex_alpha_list_alpha_accounts
- cex_alpha_list_alpha_currencies
- cex_alpha_list_alpha_tickers
- cex_alpha_list_alpha_tokens
- cex_earn_asset_list
- cex_earn_award_list
- cex_earn_find_coin
- cex_earn_get_uni_currency
- cex_earn_get_uni_interest
- cex_earn_list_dual_balance
- cex_earn_list_dual_orders
- cex_earn_list_structured_orders
- cex_earn_list_uni_currencies
- cex_earn_list_uni_rate
- cex_earn_list_user_uni_lends
- cex_earn_order_list
- cex_fx_get_fx_accounts
- cex_fx_get_fx_candlesticks
- cex_fx_get_fx_contract
- cex_fx_get_fx_funding_rate
- cex_fx_get_fx_order_book
- cex_fx_get_fx_premium_index
- cex_fx_get_fx_tickers
- cex_fx_get_fx_trades
- cex_fx_list_fx_liq_orders
- cex_fx_list_fx_positions
- cex_margin_list_margin_accounts
- cex_options_list_options_account
- cex_rebate_broker_commission_history
- cex_rebate_broker_transaction_history
- cex_rebate_partner_commissions_history
- cex_rebate_partner_sub_list
- cex_rebate_partner_transaction_history
- cex_rebate_user_info
- cex_rebate_user_sub_relation
- cex_spot_get_spot_accounts
- cex_spot_get_spot_candlesticks
- cex_spot_get_spot_order_book
- cex_spot_get_spot_tickers
- cex_spot_get_spot_trades
- cex_spot_list_spot_account_book
- cex_tradfi_query_user_assets
- cex_unified_get_unified_accounts
- cex_unified_get_unified_borrowable
- cex_unified_get_unified_estimate_rate
- cex_unified_get_unified_mode
- cex_unified_get_unified_transferable
- cex_unified_get_user_leverage_currency_setting
- cex_unified_list_currency_discount_tiers
- cex_unified_list_unified_currencies
- cex_unified_list_unified_loan_interest_records
- cex_unified_list_unified_loan_records
- cex_wallet_get_total_balance

**Execution Operations (Write)**

- cex_unified_create_unified_loan
- cex_unified_set_unified_collateral
- cex_unified_set_unified_mode
- cex_unified_set_user_leverage_currency_setting

### Authentication
- API Key Required: Yes (see skill doc/runtime MCP deployment)
- Permissions: Alpha:Read, Earn:Read, Fx:Read, Margin:Read, Options:Read, Rebate:Read, Spot:Read, Tradfi:Read, Unified:Write, Wallet:Read
- Get API Key: https://www.gate.io/myaccount/profile/api-key/manage

### Installation Check
- Required: Gate (main)
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute module routing in this skill.

- `SKILL.md` keeps orchestration/routing logic across account domains.
- `references/mcp.md` is the authoritative MCP execution layer for module aggregation, partial degradation strategy, and unified mutation safeguards.

## Sub-Modules

| Module | L1 Source | Tool Count | Read/Write | Purpose |
|--------|-----------|------------|------------|---------|
| S1 Assets / Overview | gate-exchange-assets, gate-exchange-alpha | 10+ | Read only | Multi-account balance panorama |
| S2 Risk / Margin | gate-exchange-unified, gate-exchange-marketanalysis | 6+ | Read only | Margin ratio, liquidation price, unrealised PnL |
| S3 Earn / Yield | gate-exchange-simpleearn, gate-exchange-staking | 4 | Read only | Current SimpleEarn and staking position/interest snapshots |
| S4 Affiliate / Rebate | gate-exchange-affiliate | 7 | Read only | Rebate user info (may be empty), partner commissions history, sub-relations |
| S5 Borrow / Transfer (Write) | gate-exchange-unified | 6 | 2 Read + 4 Write | Borrow, set collateral, set leverage, switch mode |

Note: TradFi tools (from gate-exchange-tradfi, 10 read tools) are all read-only and used for asset inventory queries. They are included in the deduplicated 58-tool count but not listed as a separate L1 module in the sub-module table above.

## Routing Rules

### Design Principle

User queries often span multiple dimensions (e.g. "check my earn interest and will I get liquidated" covers S3 and S2). Instead of forcing single-intent classification, this skill uses **signal overlay**: each of 5 signal dimensions is independently detected from the query, and the activated dimensions contribute their respective tool sets. The final tool set is the union of all activated signals, deduplicated before execution.

### Signal Dimension Definitions

| Signal | Dimension | Trigger Condition | Trigger Keywords | Tool Subset |
|--------|-----------|-------------------|------------------|-------------|
| S1 | Assets / Overview | User asks about overall assets, multi-account balances, asset inventory; also covers read-only borrowable/rate inquiry (no execution intent) and transferable limit snapshots | assets, balance, account, how much, total assets, inventory; borrowable (inquiry only), transferable limit | `cex_wallet_get_total_balance`, `cex_spot_get_spot_accounts`, `cex_unified_get_unified_accounts`, `cex_fx_get_fx_accounts`, `cex_margin_list_margin_accounts`, `cex_options_list_options_account`, `cex_earn_list_user_uni_lends`, `cex_earn_asset_list`, `cex_alpha_list_alpha_accounts`, `cex_tradfi_query_user_assets`; inquiry subset: + `cex_unified_get_unified_borrowable`, `cex_unified_get_unified_estimate_rate`, `cex_unified_get_unified_transferable` |
| S2 | Risk / Margin | User asks about liquidation, margin, liquidation price, unrealised PnL, position risk | liquidation, margin, liquidation price, unrealised PnL, position, risk, margin call | `cex_unified_get_unified_accounts`, `cex_fx_list_fx_positions`, `cex_fx_get_fx_tickers`, `cex_fx_get_fx_contract`, `cex_fx_get_fx_funding_rate`, `cex_fx_get_fx_premium_index` |
| S3 | Earn / Yield | User asks about existing SimpleEarn or staking positions, accrued interest and rewards (snapshot only, not product selection) | earn position, staking position, interest, yield, rewards | `cex_earn_list_user_uni_lends`, `cex_earn_get_uni_interest`, `cex_earn_asset_list`, `cex_earn_award_list` (Note: does not include `list_uni_currencies` / `list_uni_rate` / `find_coin` which are product-selection tools; those requests route to smart earn) |
| S4 | Affiliate / Rebate | User asks about affiliate status, partner data, commissions | rebate, affiliate, commission, partner, broker, referral | `cex_rebate_user_info`, `cex_rebate_partner_commissions_history`, `cex_rebate_partner_sub_list`, `cex_rebate_partner_transaction_history`, `cex_rebate_user_sub_relation`, `cex_rebate_broker_commission_history`, `cex_rebate_broker_transaction_history` |
| S5 | Borrow / Transfer (Write) | User has explicit execution intent: borrow amount, add margin, set collateral, switch mode. Does NOT activate for inquiry-only queries like "how much can I borrow" with negation like "don't borrow yet" | borrow [amount], add margin, transfer to futures, set collateral, switch mode | `cex_unified_get_unified_borrowable`, `cex_unified_get_unified_estimate_rate`, `cex_unified_create_unified_loan`, `cex_unified_set_unified_collateral`, `cex_unified_set_unified_mode`, `cex_unified_set_user_leverage_currency_setting` |

### Routing Flow

```
Input: User Query
Output: activated_signals[] + params{action_type, accounts[]}

1. Parameter Extraction
   Extract accounts[] (account types mentioned, 0-N)
   Extract action_type (borrow / transfer / add margin / setting / none)

2. Signal Detection (each dimension independent, non-exclusive, multi-select)
   S1 <- contains asset/balance/account/inventory expressions
   S2 <- contains liquidation/margin/position/risk expressions
   S3 <- contains earn/staking position/interest/rewards expressions
   S4 <- contains rebate/affiliate/commission/partner expressions
   S5 <- contains borrow/transfer/add-margin/setting expressions AND execution intent

3. Fallback Rules (if no signal explicitly activated)
   Vague account intent (e.g. "check my account") -> default S1 (asset overview)
   Account + risk keywords (e.g. "is it safe") -> default S1 + S2

4. Execution Mode
   S5 not activated -> read-only mode (query and summarise)
   S5 activated -> read+write mode (query -> Action Draft -> confirm -> execute)

5. Tool Set Assembly
   Tool Set = Union(all activated signal tool subsets)
   Deduplicate same tool + same parameters
   Independent tools run in parallel; S5 write operations run serially after reads
```

### External Routing (Out of Scope)

| User Intent | Route To |
|-------------|----------|
| Trade execution (spot/futures open/close) | Trading copilot skill |
| Coin research, market analysis, news | Market research skill |
| Idle fund allocation, product selection, APY comparison | Smart earn skill |
| Flash swap / coin exchange | Flash swap skill |
| Sub-account management | Not in scope |
| Asset weekly report, cross-period analysis | Not supported by current API; guide to App reports |
| Total PnL ledger across all business lines | Data source calibration unreliable; display per-module snapshots |

### Routing Example Table

| User Query | accounts | Activated Signals | Explanation |
|------------|----------|-------------------|-------------|
| "Check my account" | [] | S1 (fallback) | No explicit dimension keyword; fallback to asset overview |
| "How much do I have, will I get liquidated?" | [] | S1 + S2 | "how much" triggers S1, "liquidated" triggers S2 |
| "Is my unified margin sufficient?" | [unified] | S2 | "margin" triggers risk |
| "Show liquidation prices and unrealised PnL" | [] | S2 | "liquidation price / unrealised PnL" triggers risk |
| "How much did earn and staking make?" | [] | S3 | "earn / staking / how much" triggers yield |
| "Should I put idle funds in SimpleEarn or staking?" | [] | — | Route to smart earn; this skill does not do fund allocation |
| "How much rebate do I have?" | [] | S4 | "rebate" triggers affiliate |
| "Margin is low, help me add margin" | [] | S2 + S5 | "margin low" triggers S2, "add margin" triggers S5 write |
| "How much can I borrow? Don't borrow yet" | [] | S1 | Negation of execution -> does NOT activate S5; uses borrowable + estimate_rate (inquiry subset) |
| "How much can I borrow? Borrow 500 USDT" | [] | S5 | Execution intent -> query then Action Draft -> confirm -> create_loan |
| "How much USDT can I transfer out? (don't transfer)" | [unified] | S1 | Transferable limit read-only -> transferable + unified_accounts; not a transfer execution |
| "Show total assets + futures margin together (no analysis)" | [] | S1 + S2 | Factual snapshot, no S3, no health/PnL narrative |
| "Make me an asset weekly report / total PnL ledger" | [] | — | Not accepted: API cannot support reliable asset analysis or total PnL; explain boundary and guide to App reports |
| "About to get liquidated, any spare spot balance? Can I add margin?" | [] | S2 + S1 + S5 | "liquidated" triggers S2, "spot balance" triggers S1, "add margin" triggers S5 |

### L1/L2 Coexistence Strategy

Some user queries can be satisfied by a single L1 skill's tools (e.g. "how much do I have" only needs a few assets tools). This L2 provides a more comprehensive aggregated report through cross-L1 orchestration.

- **Recommended strategy**: All "account/asset/risk" requests enter this L2 as a unified entry point. If the sub-intent only needs a single L1's tool set, call that subset only and output normally (short-circuit optimisation).
- **Principle**: Unified entry ensures consistent user experience for all account/asset/risk queries; internally call 1-N tools as needed without forcing full orchestration.

### Mixed Intent Handling

When a user query contains both account/risk intent and other L2 intents (e.g. "check my account, then buy BTC"):

1. Split into two segments: **account/risk part** is handled by this skill and output conclusions
2. **Trading/research part** routes to the corresponding L2 (trading copilot / market research), each executes independently
3. Example: "Check my account, then buy some BTC" -> this skill completes asset overview -> prompts "trading part has been routed to trading copilot"

### Edge Case Handling

| Scenario | Handling |
|----------|----------|
| User says "check my account" with no details | Fallback S1 (asset overview), output full asset panorama |
| User says "is it safe" / "am I OK" | Fallback S1 + S2, output asset panorama + margin/liquidation assessment |
| User asks about sub-accounts | Explicitly state "this skill does not cover sub-account management" |
| Write operation parameters incomplete (e.g. "borrow" without amount) | Ask to complete: "Please confirm the currency and amount to borrow"; do not guess |
| Multilingual / mixed Chinese-English prompts | Parse intent and parameters normally; if identifiable as account/asset/risk, enter this skill |
| User asks "which earn product is best" | Product recommendation scope; route to smart earn. This skill only queries existing positions/yields |
| `cex_rebate_user_info` returns an empty object | Still produce the S4 section from `cex_rebate_partner_commissions_history` and other S4 tools; do not treat empty user_info as "no affiliate data". See Domain Knowledge: Affiliate / rebate data (S4). |

## Execution

### Read-Only Scenarios (S1-S4, no S5)

1. Activate signal dimensions from user query
2. Assemble deduplicated tool set from all activated dimensions
3. Execute all tools in parallel (no serial dependencies)
4. LLM aggregates multi-source results, annotates data timestamp and source
5. Output structured report per activated dimension

### Write Scenarios (S5 activated)

1. Phase 1 (Parallel Read): Execute S1/S2 tools to get current account state
2. LLM evaluates feasibility and generates Action Draft (follow **G. Write operation grading**: medium-risk = risk note + irreversibility for mode switch; high-risk borrow/repay = amount + currency + rate)
3. Present Action Draft to user with key parameters and risk notes
4. Wait for explicit user confirmation (Y/N)
5. Phase 2 (Execute): Submit write tool call only after confirmation
6. Output execution result

### Tool Deduplication Rules

- Same tool + same parameters within one request: execute once, reuse result for multiple aggregation steps
- Example: `cex_unified_get_unified_accounts` needed by both S1 and S2 only executes once

## MCP Tools

### Full Deduplicated Tool Inventory (58 tools: 54 read + 4 write)

#### Assets Domain (11 tools, all read)

| # | Tool Name | R/W | Purpose |
|---|-----------|-----|---------|
| 1 | `cex_wallet_get_total_balance` | R | Total balance in USDT equivalent |
| 2 | `cex_spot_get_spot_accounts` | R | Spot account per-currency balances |
| 3 | `cex_unified_get_unified_accounts` | R | Unified account equity/margin/loans |
| 4 | `cex_fx_get_fx_accounts` | R | Futures account available balance |
| 5 | `cex_options_list_options_account` | R | Options account balance |
| 6 | `cex_margin_list_margin_accounts` | R | Isolated margin accounts |
| 7 | `cex_tradfi_query_user_assets` | R | TradFi account equity |
| 8 | `cex_earn_list_dual_balance` | R | Dual investment balance |
| 9 | `cex_earn_list_dual_orders` | R | Dual investment orders |
| 10 | `cex_earn_list_structured_orders` | R | Structured product orders |
| 11 | `cex_spot_list_spot_account_book` | R | Spot account ledger |

#### Unified Account Domain (14 tools, 10 read + 4 write)

| # | Tool Name | R/W | Purpose |
|---|-----------|-----|---------|
| 12 | `cex_unified_get_unified_accounts` | R | Unified account equity/margin ratio/loan balance |
| 13 | `cex_unified_get_unified_mode` | R | Current unified account mode |
| 14 | `cex_unified_get_unified_borrowable` | R | Borrowable limit per currency |
| 15 | `cex_unified_get_unified_transferable` | R | Transferable limit |
| 16 | `cex_unified_get_unified_estimate_rate` | R | **Hourly** estimated unified-account borrow rate per currency (API string decimals; **not** annualized APR/APY). See Domain Knowledge: Unified account estimated borrow rate. |
| 17 | `cex_unified_list_unified_currencies` | R | Supported unified currencies |
| 18 | `cex_unified_list_unified_loan_records` | R | Loan records |
| 19 | `cex_unified_list_unified_loan_interest_records` | R | Loan interest records |
| 20 | `cex_unified_get_user_leverage_currency_setting` | R | Per-currency leverage setting |
| 21 | `cex_unified_list_currency_discount_tiers` | R | Collateral discount tiers |
| 22 | `cex_unified_set_unified_mode` | W | Switch unified account mode |
| 23 | `cex_unified_create_unified_loan` | W | Execute borrow/repay |
| 24 | `cex_unified_set_user_leverage_currency_setting` | W | Set per-currency leverage |
| 25 | `cex_unified_set_unified_collateral` | W | Set collateral currencies |

#### SimpleEarn Domain (5 tools, all read)

| # | Tool Name | R/W | Purpose |
|---|-----------|-----|---------|
| 26 | `cex_earn_list_uni_currencies` | R | SimpleEarn supported currencies |
| 27 | `cex_earn_get_uni_currency` | R | Single currency SimpleEarn details |
| 28 | `cex_earn_list_user_uni_lends` | R | User SimpleEarn positions |
| 29 | `cex_earn_get_uni_interest` | R | SimpleEarn interest earnings |
| 30 | `cex_earn_list_uni_rate` | R | SimpleEarn APY rates |

#### Staking Domain (4 tools, all read)

| # | Tool Name | R/W | Purpose |
|---|-----------|-----|---------|
| 31 | `cex_earn_asset_list` | R | Staking positions |
| 32 | `cex_earn_award_list` | R | Staking reward records |
| 33 | `cex_earn_find_coin` | R | Stakeable coin search |
| 34 | `cex_earn_order_list` | R | Staking order history |

#### Market Analysis Domain (12 tools, all read)

| # | Tool Name | R/W | Purpose |
|---|-----------|-----|---------|
| 35 | `cex_spot_get_spot_order_book` | R | Spot order book |
| 36 | `cex_spot_get_spot_candlesticks` | R | Spot K-line data |
| 37 | `cex_spot_get_spot_tickers` | R | Spot ticker snapshot |
| 38 | `cex_spot_get_spot_trades` | R | Spot trade records |
| 39 | `cex_fx_get_fx_contract` | R | Futures contract specs |
| 40 | `cex_fx_get_fx_order_book` | R | Futures order book |
| 41 | `cex_fx_get_fx_candlesticks` | R | Futures K-line data |
| 42 | `cex_fx_get_fx_tickers` | R | Futures ticker (mark price) |
| 43 | `cex_fx_get_fx_trades` | R | Futures trade records |
| 44 | `cex_fx_get_fx_funding_rate` | R | Funding rate |
| 45 | `cex_fx_list_fx_liq_orders` | R | Liquidation orders |
| 46 | `cex_fx_get_fx_premium_index` | R | Basis/premium index |

#### Futures Positions (1 tool, read)

| # | Tool Name | R/W | Purpose |
|---|-----------|-----|---------|
| 47 | `cex_fx_list_fx_positions` | R | All futures positions (unrealised PnL, liquidation price) |

#### Affiliate Domain (7 tools, all read)

| # | Tool Name | R/W | Purpose |
|---|-----------|-----|---------|
| 48 | `cex_rebate_user_info` | R | User rebate summary (may return an empty object; rely on commissions history when empty) |
| 49 | `cex_rebate_user_sub_relation` | R | User affiliate relationship |
| 50 | `cex_rebate_partner_sub_list` | R | Partner client list |
| 51 | `cex_rebate_partner_commissions_history` | R | Partner commission history |
| 52 | `cex_rebate_partner_transaction_history` | R | Client transaction history |
| 53 | `cex_rebate_broker_commission_history` | R | Broker commission history |
| 54 | `cex_rebate_broker_transaction_history` | R | Broker transaction history |

#### Alpha Domain (4 tools, all read)

| # | Tool Name | R/W | Purpose |
|---|-----------|-----|---------|
| 55 | `cex_alpha_list_alpha_currencies` | R | Alpha supported currencies |
| 56 | `cex_alpha_list_alpha_tokens` | R | Alpha token list |
| 57 | `cex_alpha_list_alpha_tickers` | R | Alpha ticker snapshot |
| 58 | `cex_alpha_list_alpha_accounts` | R | User Alpha positions |

## Domain Knowledge

### Key Value Propositions

- Single-query visibility into "where is my money, earn/affiliate snapshots, will I get liquidated" without multi-page navigation (does not produce asset weekly reports, total PnL ledger, or idle fund allocation plans)
- 58 tool calls orchestrated by scenario with parallel/serial awareness; conclusions and data sources are traceable
- Write operations (borrow/settings) require mandatory confirmation; zero risk of accidental execution; read operations are fully parallelised for fast response
- All tools require API Key authentication; data is limited to the authenticated user's own view

### Target Users

- Active traders with open positions who need a quick asset overview
- Users concerned about asset security and risk control (margin, liquidation)
- Users who periodically review earn/staking yields and affiliate commission summaries
- Advanced users who utilise unified-account borrowing, leverage, and collateral features

### Key Constraints

- This skill covers main account only; sub-account management is out of scope.
- Margin ratio and liquidation price calculations are reference values; always note "subject to the exchange's actual liquidation rules."
- Asset data has snapshot latency; always annotate the data timestamp in output.
- Borrowing incurs interest; users must assess their own repayment capacity.
- Asset data is limited to the user's own view and must not be leaked to other contexts.
- When a query returns no meaningful business data (empty list, no records), do not list or emphasise `cex_*` tool names in user-facing output; use natural language like "no records found" instead.

### Capability Boundaries (What This Skill Does NOT Do)

- Does NOT execute trades (spot/futures open/close) — route to trading copilot
- Does NOT perform coin research, market analysis, or news — route to market research
- Does NOT recommend earn products or handle subscriptions — route to smart earn
- Does NOT manage sub-accounts
- Does NOT produce asset weekly reports or cross-period asset analysis (API limitation)
- Does NOT produce a total PnL ledger across all business lines (inconsistent data sources)
- Does NOT provide idle fund allocation advice or product comparison — route to smart earn

### Unified account estimated borrow rate (`cex_unified_get_unified_estimate_rate`)

- **Semantics (Gate API):** The tool returns **estimated borrow interest rates for the current hour**, per currency, as **string decimals** (e.g. `"0.000002"`). This matches the public API contract: hourly estimate, not a fixed annual quote.
- **User-facing output:** Always state that the value is a **hourly estimated rate** (or equivalent). **Do not** present the raw number as **annualized APR/APY** unless you perform an explicit conversion and label it clearly as a **reference only** (e.g. simple scaling: hourly × 24 × 365 — actual accrual follows platform rules).
- **Distinction:** SimpleEarn tools such as `cex_earn_list_uni_rate` expose **product APY-style** figures; they are a different product line from unified-account **borrow** estimates. Do not mix units in one sentence without naming each source.

### Common Misconceptions

| Misconception | Reality |
|---------------|---------|
| The number from `cex_unified_get_unified_estimate_rate` is an annual percentage (APR) | It is an **hourly** estimated borrow rate per currency. Label it as hourly; only annualize with explicit conversion and “reference only” wording if the user asks. |
| "Check my account and buy BTC" will execute trades via this skill | This skill only handles account/asset/risk queries and limited write operations (borrow/settings). Trading execution routes to the trading copilot. |
| Liquidation warning equals the actual liquidation line | This skill evaluates risk based on snapshot data. Always note "subject to the exchange's actual liquidation rules." |
| This skill can query or manage sub-accounts | This skill covers main account only; sub-account management is out of scope. |
| "Should I put idle funds in SimpleEarn or staking" will be answered by this skill | Product selection and fund allocation route to the smart earn skill. This skill only provides position and yield snapshots for existing holdings. |
| Empty `cex_rebate_user_info` means I have no commissions | Partner commission rows may still exist in `cex_rebate_partner_commissions_history`; empty user_info does not block an S4 report. |

### Affiliate / rebate data (S4)

- **`cex_rebate_user_info` may return an empty object.** You can still build a meaningful S4 report from **`cex_rebate_partner_commissions_history`** (and other S4 read tools such as partner sub list and transaction history). Empty `user_info` does **not** mean there is no commission data.
- **Source of truth for commission flows:** `cex_rebate_partner_commissions_history` returns historical commission rows. **`commissionAsset`** is commonly **USDT** or **POINT**; rows may also carry a **source** dimension such as FUTURES, SPOT, TradFi, or ALPHA (names as returned by the API).
- **No fabricated lifetime rebate totals:** When `user_info` does not expose a ready-made cumulative rebate figure, do **not** invent a single "total rebate" number. To state **aggregate USDT and POINT** from history alone, you must **page through the full history** (use the API's offset/limit parameters, e.g. limit 100 per request), repeat until no more rows, then **sum `commissionAmount` grouped by `commissionAsset`**. If the session has **not** completed all pages, state that explicitly and **do not** guess totals.
- **Official totals:** Direct users to the Gate **App or Web** partner or rebate center for **authoritative** cumulative figures if they need a single official number without full pagination in the session.
- **Optional follow-up:** If the user asks, you may offer to **continue pagination for rebate only** and report **USDT total and POINT total** from commission history. **Do not** add those rebate totals to SimpleEarn, staking, or other yield sections (no cross-section "total income" mixing).

### Reference Documents

- `gate-runtime-rules.md` — Exchange runtime rules (precision, price limits), referenced before executing borrow operations

Note: Unified account specifications (margin ratio calculation, borrowing rules, mode switching constraints) are embedded in the Domain Knowledge and Safety Rules sections of this SKILL.md. For detailed unified-account rules, refer to the `gate-exchange-unified` L1 skill.

## Safety Rules

### G. Write Operation Confirmation Mechanism and Safety Rules

**Category: Strong confirmation · Action Draft** — All unified-account mutations below use an Action Draft plus an explicit user confirmation in the immediately preceding turn. There is no silent execution.

#### Write operation grading (by risk level)

| Risk level | Operation type | Involved tools | Confirmation requirement |
|------------|------------------|----------------|--------------------------|
| **Medium** | Switch unified account mode / set per-currency leverage / set collateral | `cex_unified_set_unified_mode`, `cex_unified_set_user_leverage_currency_setting`, `cex_unified_set_unified_collateral` | **Single confirmation** plus a **risk disclosure** in the Action Draft. If the operation includes **mode switch** (`cex_unified_set_unified_mode`), the draft **must** state that **the mode change is irreversible** (or equivalent clear wording). |
| **High** | Lending — borrow or repay | `cex_unified_create_unified_loan` | **Action Draft** must list **amount**, **currency**, and **estimated or applicable interest rate** (from `cex_unified_get_unified_estimate_rate` — **hourly** estimate — or API response), then **user confirmation** before execution. |

**Implementation notes**

- **`cex_unified_get_unified_estimate_rate`:** Treat returned rates as **hourly** estimates when quoting to the user or filling Action Drafts (see Domain Knowledge: Unified account estimated borrow rate).
- **Medium vs High**: Medium-risk tools still use an Action Draft; the difference is emphasis — medium-risk settings require a concise risk tip (and irreversibility when switching mode). High-risk lending requires the financial fields (amount, currency, rate) to be explicit in the draft before confirmation.
- **One tool per confirmation batch** if parameters differ; do not bundle unrelated writes under one generic “OK”.

### User Confirmation Requirement

All write operations require explicit user confirmation before execution. The confirmation flow is:

1. **Action Draft**: Present operation type, target, parameters, estimated impact, and risk note (see grading table above for medium vs high content)
2. **Wait for Confirmation**: User must reply with explicit approval (Y / Confirm)
3. **Execute**: Submit write tool call only after approval
4. **Single-use**: Confirmation is consumed after one use; parameter changes require re-confirmation
5. **Per-step**: Multi-step write operations require confirmation for each step separately

### Write Operation Classification (summary)

| Risk Level | Operations | Tools | Confirmation |
|------------|-----------|-------|--------------|
| Medium | Switch unified mode, set leverage, set collateral | `cex_unified_set_unified_mode`, `cex_unified_set_user_leverage_currency_setting`, `cex_unified_set_unified_collateral` | Action Draft + single confirmation + risk note; **mode switch: irreversibility must be stated** |
| High | Borrow / Repay | `cex_unified_create_unified_loan` | Action Draft with **amount, currency, interest rate** → user confirmation |

### No-Confirmation Guard

Without explicit user confirmation, no write operation is executed. Only read and query operations are allowed.

### Stale Confirmation Handling

If parameters change after confirmation (different currency, amount, or operation type), the previous confirmation is invalidated and a new Action Draft must be presented.

### Hard Blocking Rules

- NEVER call mutation tools without explicit confirmation from the immediately previous user turn
- NEVER guess parameters; if amount, currency, or direction is missing, ask the user
- NEVER fabricate data; if a tool call fails, degrade gracefully and note "data temporarily unavailable"
- Liquidation warnings are reference values only; always state "subject to the exchange's actual rules"

## Error Handling

| Error Type | Handling Strategy |
|------------|-------------------|
| Single read tool timeout/error | Skip that dimension, note "this section is temporarily unavailable", continue other dimensions |
| Write tool failure | Do not retry; explain failure reason and guide user to App/Web for manual operation |
| Missing required parameter (write) | Ask user to specify (e.g. "Please confirm the currency and amount to borrow") |
| Unrecognisable intent | Fall back to S1 (asset overview) |
| Tool call returns empty data | Use natural language "no records found"; do not display tool names |

## Risk Disclaimers

- Digital asset trading involves significant risk and may result in partial or total loss of your investment.
- Leveraged trading (futures, margin, options, delivery contracts) may result in losses exceeding your initial margin. Small market movements can cause total margin loss.
- The above is for informational purposes only and does not constitute investment, financial, tax, or legal advice.
- AI-assisted outputs are for general information only and do not constitute any representation, warranty, or guarantee by Gate.
- Users must comply with the laws and regulations of their jurisdiction. Gate services may not be available in restricted regions.

## Report Template

### Read-Only Report

```markdown
## Account and Asset Risk Report

| Dimension | Status |
|-----------|--------|
| Data Timestamp | {timestamp} |
| Activated Signals | {S1/S2/S3/S4} |

### S1 Asset Overview (if activated)
{asset_panorama_table}

### S2 Risk and Margin (if activated)
{margin_and_position_risk_table}
Note: Liquidation prices and margin ratios are reference values. Subject to the exchange's actual liquidation rules.

### S3 Earn Snapshot (if activated)
{simpleearn_and_staking_summary}

### S4 Affiliate Report (if activated)
{rebate_and_commission_summary}
Note: If `cex_rebate_user_info` is empty, rely on `cex_rebate_partner_commissions_history` (and other S4 tools). Do not fabricate lifetime USDT/POINT totals unless all history pages were fetched and summed by `commissionAsset`. Point to App/Web partner center for official cumulative figures when appropriate.
```

### Write Operation Report

**Medium-risk settings** (`set_unified_mode`, `set_user_leverage_currency_setting`, `set_unified_collateral`):

```markdown
## Action Draft (medium-risk · strong confirmation)

| Item | Value |
|------|-------|
| Operation | {set collateral / set leverage / switch unified mode} |
| Target | {currency / mode / leverage value} |
| Amount or config | {as applicable} |
| Risk warning | {e.g. impact on margin; if mode switch: **this change is irreversible**} |

Reply **Y** to confirm or **N** to cancel.
```

**High-risk lending** (`create_unified_loan` — borrow or repay):

```markdown
## Action Draft (high-risk · strong confirmation)

| Item | Value |
|------|-------|
| Operation | {borrow / repay} |
| Currency | {e.g. USDT} |
| Amount | {numeric amount} |
| Interest rate | {hourly estimated rate from `cex_unified_get_unified_estimate_rate` / API; state **hourly** — not APR unless explicitly converted and labeled reference-only} |
| Risk warning | {e.g. interest accrual, repayment obligation} |

Reply **Y** to confirm or **N** to cancel.
```

## Cross-Skill Workflows

### Workflow A: Check Risk Then Add Margin

1. This skill evaluates position risk (S2) and available spot balance (S1)
2. If margin is insufficient, generate add-margin Action Draft (S5)
3. After confirmation, execute collateral setting

### Workflow B: Check Borrowable Then Borrow

1. This skill queries borrowable limit and estimated rate (S1 inquiry subset)
2. If user confirms borrow intent, activate S5 and generate borrow Action Draft
3. After confirmation, execute borrow; if user wants to trade, route to trading copilot
