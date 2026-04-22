---
name: gate-exchange-spot
description: "Gate spot trading and account operations skill. Use when the user asks to buy/sell crypto on spot, check account value, or place conditional/trigger orders. Triggers on 'buy coin', 'sell spot', 'take profit', 'stop loss', or 'cancel order'."
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "💱"
    os:
      - darwin
      - linux
    primaryEnv: GATE_API_KEY
    requires:
      bins:
        - gate-cli
      env:
        - GATE_API_KEY
        - GATE_API_SECRET

    install:
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux x64)"
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux arm64)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Intel)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Apple Silicon)"
---

### Resolving `gate-cli` (binary path)

Resolve **`gate-cli`** in order: **(1)** **`command -v gate-cli`** and **`gate-cli --version`** succeeds; **(2)** **`${HOME}/.local/bin/gate-cli`** if executable; **(3)** **`${HOME}/.openclaw/skills/bin/gate-cli`** if executable. Canonical rules: [`exchange-runtime-rules.md`](../exchange-runtime-rules.md) §4 (or [`gate-runtime-rules.md`](../gate-runtime-rules.md) §4).


# Gate Spot Trading Assistant

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read `./references/gate-runtime-rules.md`
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.


---

## Skill Dependencies

This skill depends on the **`gate-cli`** binary and the documented subcommands below. Command strings align with `gate-cli/cmd/cex/GATE_EXCHANGE_SKILLS_MCP_TO_GATE_CLI.md`.

- **Before any `gate-cli` invocation:** ensure `gate-cli` is installed. Let `GATE_CLI_BIN="${GATE_OPENCLAW_SKILLS_BIN:-$HOME/.openclaw/skills/bin}/gate-cli"`. If **`[ ! -x "$GATE_CLI_BIN" ]`** (and `command -v gate-cli` also fails if you rely on `PATH`), **run** [`setup.sh`](./setup.sh) (e.g. `sh ./setup.sh` from this skill directory), then re-check. **Do not** continue with trading or account reads that require auth until `gate-cli` runs successfully (e.g. `gate-cli --version`).
- **No MCP servers** are required for this skill; execution is **`gate-cli` only**.

### gate-cli commands used

**Query Operations (Read-only)**

- `gate-cli cex spot market currency`
- `gate-cli cex spot market pair`
- `gate-cli cex spot account get`
- `gate-cli cex spot account batch-fee`
- `gate-cli cex spot market candlesticks`
- `gate-cli cex spot market orderbook`
- `gate-cli cex spot price-trigger get`
- `gate-cli cex spot market tickers`
- `gate-cli cex spot account book`
- `gate-cli cex spot order my-trades`
- `gate-cli cex spot order list`
- `gate-cli cex spot price-trigger list`
- `gate-cli cex wallet market trade-fee`

**Execution Operations (Write)**

- `gate-cli cex spot order batch-amend`
- `gate-cli cex spot order amend`
- `gate-cli cex spot order cancel`
- `gate-cli cex spot order batch-cancel`
- `gate-cli cex spot price-trigger cancel`
- `gate-cli cex spot price-trigger cancel-all`
- `gate-cli cex spot order batch-create`
- `gate-cli cex spot order buy` / `gate-cli cex spot order sell`
- `gate-cli cex spot price-trigger create`

### Authentication
- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- **Permissions:** Spot:Write, Wallet:Read on the key used by `gate-cli`.
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- **Required:** `gate-cli` (install via [`setup.sh`](./setup.sh) when missing, per Skill Dependencies).
- GateClaw / OpenClaw: [`setup.sh`](./setup.sh) installs to `$HOME/.openclaw/skills/bin/gate-cli` by default; add that directory to **`PATH`** if agents invoke `gate-cli` by name.
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`** — that is equivalent valid config for `gate-cli`. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Do not proceed with authenticated calls until the CLI behaves as expected for the setup (e.g. **`gate-cli cex spot market tickers`**); confirm credentials resolve before trades.

## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute this skill's routing/case logic.

- `SKILL.md` remains the intent routing and scenario map.
- `references/gate-cli.md` is the authoritative execution contract for `gate-cli` usage, pre-checks, confirmation gates, and degraded handling.

## Domain Knowledge

### Tool Mapping by Domain

| Group | gate-cli commands |
|------|------|
| Account and balances | `gate-cli cex spot account get`, `gate-cli cex spot account book` |
| Place/cancel/amend orders | `gate-cli cex spot order buy` / `gate-cli cex spot order sell`, `gate-cli cex spot order batch-create`, `gate-cli cex spot order cancel`, `gate-cli cex spot order batch-cancel`, `gate-cli cex spot order amend`, `gate-cli cex spot order batch-amend` |
| Trigger orders (price orders) | `gate-cli cex spot price-trigger create`, `gate-cli cex spot price-trigger list`, `gate-cli cex spot price-trigger get`, `gate-cli cex spot price-trigger cancel`, `gate-cli cex spot price-trigger cancel-all` |
| Open orders and fills | `gate-cli cex spot order list`, `gate-cli cex spot order my-trades` |
| Market data | `gate-cli cex spot market tickers`, `gate-cli cex spot market orderbook`, `gate-cli cex spot market candlesticks` |
| Trading rules | `gate-cli cex spot market currency`, `gate-cli cex spot market pair` |
| Fees | `gate-cli cex wallet market trade-fee`, `gate-cli cex spot account batch-fee` |

### Key Trading Rules

- Use `BASE_QUOTE` format for trading pairs, for example `BTC_USDT`.
- Check quote-currency balance first before buy orders (for example USDT).
- Amount-based buys must satisfy `min_quote_amount` (commonly 10U).
- Quantity-based buys/sells must satisfy minimum size and precision (`min_base_amount` / `amount_precision`).
- Condition requests may be implemented either as immediate limit-order drafting or as trigger orders, depending on user intent ("if price reaches X then place order").
- Take-profit/stop-loss (TP/SL)-style requests are handled via spot price-trigger commands with explicit trigger and execution parameters.

### Market Order Parameter Extraction Rules (Mandatory)

When calling `gate-cli cex spot order buy` / `gate-cli cex spot order sell` with `type=market`, fill `amount` by side:

| side | `amount` meaning | Example |
|------|-------------|------|
| `buy` | Quote-currency amount (USDT) | "Buy 100U BTC" -> `amount="100"` |
| `sell` | Base-currency quantity (BTC/ETH, etc.) | "Sell 0.01 BTC" -> `amount="0.01"` |

Pre-check before execution:
- `buy` market order: verify quote-currency balance can cover `amount` (USDT).
- `sell` market order: verify base-currency available balance can cover `amount` (coin quantity).
## Workflow

When the user asks for any spot trading operation, follow this sequence.

### Step 1: Identify Task Type

Classify the request into one of these six categories:
1. Buy (market/limit/full-balance buy)
2. Sell (full-position sell/conditional sell)
3. Account query (total assets, balance checks, tradability checks)
4. Order management (list open orders, amend, cancel)
5. Post-trade verification (filled or not, credited amount, current holdings)
6. Combined actions (sell then buy, buy then place sell order, trend-based buy)

### Step 2: Extract Parameters and Run Pre-checks

Extract key fields:
- `currency` / `currency_pair`
- `side` (`buy`/`sell`)
- `amount` (coin quantity) or `quote_amount` (USDT amount)
- `price` or price condition (for example "2% below current")
- trigger condition (execute only when condition is met)

When `type=market`, normalize parameters as:
- `side=buy`: `amount = quote_amount` (USDT amount)
- `side=sell`: `amount = base_amount` (base-coin quantity)

Pre-check order:
1. Trading pair/currency tradability status
2. Minimum order amount/size and precision
3. Available balance sufficiency
4. User condition satisfaction (for example "buy only below 60000")

### Step 3: Final User Confirmation Before Any Order Placement (Mandatory)

Before every `gate-cli cex spot order buy` / `gate-cli cex spot order sell`, `gate-cli cex spot order batch-create`, or `gate-cli cex spot price-trigger create`, always provide an **Order Draft** first, then wait for explicit confirmation.

Required execution flow:
1. Send order draft (no trading call yet)
2. Wait for explicit user approval
3. Only after approval, submit the real order
4. Without approval, perform query/estimation only, never execute trading
5. Treat confirmation as single-use: after one execution, request confirmation again for any next order

Required confirmation fields:
- trading pair (`currency_pair`)
- side and order type (`buy/sell`, `market/limit`)
- `amount` meaning and value
- limit price (if applicable) or pricing basis
- estimated fill / estimated cost or proceeds
- main risk note (for example slippage)

Recommended draft wording:
- `Order Draft: BTC_USDT, buy, market, amount=100 USDT, estimated fill around current ask, risk: slippage in fast markets. Reply "Confirm order" to place it.`

Allowed confirmation responses (examples):
- `Confirm order`, `Confirm`, `Proceed`, `Yes, place it`

Hard blocking rules (non-bypassable):
- NEVER call `gate-cli cex spot order buy` / `gate-cli cex spot order sell`, `gate-cli cex spot order batch-create`, or `gate-cli cex spot price-trigger create` unless the user explicitly confirms in the immediately previous turn.
- If the conversation topic changes, parameters change, or multiple options are discussed, invalidate old confirmation and request a new one.
- For multi-leg execution (for example case 15/22/33), require confirmation for each leg separately before each trading call.

If user confirmation is missing, ambiguous, or negative:
- do not place the order
- return a pending status and ask for explicit confirmation
- continue with read-only actions only (balance checks, market quotes, fee estimation)

### Step 4: Run commands by scenario

Use only the minimal `gate-cli` command set required for the task:
- Balance and available funds: `gate-cli cex spot account get`
- Rule validation: `gate-cli cex spot market pair`
- Live price and moves: `gate-cli cex spot market tickers`
- Order placement: `gate-cli cex spot order buy` / `gate-cli cex spot order sell` / `gate-cli cex spot order batch-create`
- Trigger-order placement/query/cancel: `gate-cli cex spot price-trigger create` / `gate-cli cex spot price-trigger list` / `gate-cli cex spot price-trigger get` / `gate-cli cex spot price-trigger cancel` / `gate-cli cex spot price-trigger cancel-all`
- Cancel/amend: `gate-cli cex spot order cancel` / `gate-cli cex spot order batch-cancel` / `gate-cli cex spot order amend` / `gate-cli cex spot order batch-amend`
- Open order query: `gate-cli cex spot order list` (use `status=open`)
- Fill verification: `gate-cli cex spot order my-trades`
- Account change history: `gate-cli cex spot account book`
- Batch fee query: `gate-cli cex spot account batch-fee`

### Step 5: Return Actionable Result and Status

The response must include:
- Whether execution succeeded (or why it did not execute)
- Core numbers (price, quantity, amount, balance change)
- If condition not met, clearly explain why no order is placed now

## Case Routing Map (1-36)

### A. Buy and Account Queries (1-8)

| Case | User Intent | Core Decision | Tool Sequence |
|------|----------|----------|----------|
| 1 | Market buy | Place market buy if USDT is sufficient | `gate-cli cex spot account get` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 2 | Buy at target price | Create a `limit buy` order | `gate-cli cex spot account get` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 3 | Buy with all balance | Use all available USDT balance to buy | `gate-cli cex spot account get` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 4 | Buy readiness check | Currency status + min size + current unit price | `gate-cli cex spot market currency` → `gate-cli cex spot market pair` → `gate-cli cex spot market tickers` |
| 5 | Asset summary | Convert all holdings to USDT value | `gate-cli cex spot account get` → `gate-cli cex spot market tickers` |
| 6 | Cancel all then check balance | Cancel all open orders for the user’s pair (`gate-cli cex spot order cancel` with `--all` on that `--pair`) and return balances | `gate-cli cex spot order cancel` → `gate-cli cex spot account get` |
| 7 | Sell dust | Sell only if minimum size is met | `gate-cli cex spot account get` → `gate-cli cex spot market pair` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 8 | Balance + minimum buy check | Place order only if account balance and `min_quote_amount` are both satisfied | `gate-cli cex spot account get` → `gate-cli cex spot market pair` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |

### B. Smart Monitoring and Trading (9-16)

| Case | User Intent | Core Decision | Tool Sequence |
|------|----------|----------|----------|
| 9 | Buy 2% lower | Place limit buy at current price -2% | `gate-cli cex spot market tickers` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 10 | Sell at +500 | Place limit sell at current price +500 | `gate-cli cex spot market tickers` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 11 | Buy near today's low | Buy only if current price is near 24h low | `gate-cli cex spot market tickers` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 12 | Sell on 5% drop request | Calculate target drop price and place sell limit order | `gate-cli cex spot market tickers` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 13 | Buy top gainer | Auto-pick highest 24h gainer and buy | `gate-cli cex spot market tickers` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 14 | Buy larger loser | Compare BTC/ETH daily drop and buy the bigger loser | `gate-cli cex spot market tickers` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 15 | Buy then place sell | Market buy, then place sell at +2% reference price | `gate-cli cex spot order buy` / `gate-cli cex spot order sell` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 16 | Fee estimate | Estimate total cost from fee rate and live price | `gate-cli cex wallet market trade-fee` → `gate-cli cex spot market tickers` |

### C. Order Management and Amendment (17-25)

| Case | User Intent | Core Decision | Tool Sequence |
|------|----------|----------|----------|
| 17 | Raise price for unfilled order | Confirm how much to raise (or target price), locate unfilled buy orders, confirm which order to amend if multiple, then amend limit price | `gate-cli cex spot order list`(status=open) → `gate-cli cex spot order amend` |
| 18 | Verify fill and holdings | Last buy fill quantity + current total holdings | `gate-cli cex spot order my-trades` → `gate-cli cex spot account get` |
| 19 | Cancel if not filled | If still open, cancel and then recheck balance | `gate-cli cex spot order list`(status=open) → `gate-cli cex spot order cancel` → `gate-cli cex spot account get` |
| 20 | Rebuy at last price | Use last fill price, check balance, then place limit buy | `gate-cli cex spot order my-trades` → `gate-cli cex spot account get` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 21 | Sell at break-even or better | Sell only if current price is above cost basis | `gate-cli cex spot order my-trades` → `gate-cli cex spot market tickers` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 22 | Asset swap | Estimate value, if >=10U then sell then buy | `gate-cli cex spot account get` → `gate-cli cex spot market tickers` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell`(sell) → `gate-cli cex spot order buy` / `gate-cli cex spot order sell`(buy) |
| 23 | Buy if price condition met | Buy only when `current < 60000`, then report balance | `gate-cli cex spot market tickers` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` → `gate-cli cex spot account get` |
| 24 | Buy on trend condition | Buy only if 3 of last 4 hourly candles are bullish | `gate-cli cex spot market candlesticks` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| 25 | Fast-fill limit buy | Use best opposite-book price for fast execution | `gate-cli cex spot market orderbook` → `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |

### D. Advanced Spot Utilities (26-31)

| Case | User Intent | Core Decision | Tool Sequence |
|------|----------|----------|----------|
| 26 | Filter and batch-cancel selected open orders | Verify target order ids exist in open orders, show candidate list, cancel only after user verification | `gate-cli cex spot order list`(status=open) → `gate-cli cex spot order batch-cancel` |
| 27 | Market slippage simulation | Simulate average fill from order-book asks for a notional buy, compare to last price | `gate-cli cex spot market orderbook` → `gate-cli cex spot market tickers` |
| 28 | Batch buy placement | Check total required quote amount vs available balance, then place multi-order basket | `gate-cli cex spot account get` → `gate-cli cex spot order batch-create` |
| 29 | Fee-rate comparison across pairs | Compare fee tiers and translate fee impact into estimated cost | `gate-cli cex spot account batch-fee` → `gate-cli cex spot market tickers` |
| 30 | Account-book audit + current balance | Show recent ledger changes for a coin and current remaining balance | `gate-cli cex spot account book` → `gate-cli cex spot account get` |
| 31 | Batch amend open buy orders by +1% | Filter open orders by pair, select up to 5 target buy orders, reprice and batch amend after user verification | `gate-cli cex spot order list`(status=open) → `gate-cli cex spot order batch-amend` |

### E. Trigger Orders and TP/SL Automation (32-36)

| Case | User Intent | Core Decision | Tool Sequence |
|------|----------|----------|----------|
| 32 | Conditional buy trigger order | Read current BTC price, compute 5% drop trigger, place buy trigger after confirmation | `gate-cli cex spot market tickers` → `gate-cli cex spot price-trigger create` |
| 33 | Dual TP/SL trigger placement | Check ETH available balance, build TP and SL trigger legs, confirm then place both | `gate-cli cex spot account get` → `gate-cli cex spot price-trigger create` → `gate-cli cex spot price-trigger create` |
| 34 | Single trigger order progress query | Read trigger-order detail and compare against live market price to compute distance to trigger | `gate-cli cex spot price-trigger get` → `gate-cli cex spot market tickers` |
| 35 | Batch cancel BTC buy trigger orders | List open trigger orders, filter BTC buy side, confirm scope, then batch cancel | `gate-cli cex spot price-trigger list`(status=open) → `gate-cli cex spot price-trigger cancel-all` |
| 36 | Single trigger/TP-SL order cancel | Verify one target trigger order is active, then cancel after confirmation | `gate-cli cex spot price-trigger get` → `gate-cli cex spot price-trigger cancel` |

## Judgment Logic Summary

| Condition | Action |
|-----------|--------|
| User asks to check balance before buying | Must call `gate-cli cex spot account get` first; place order only if sufficient |
| User specifies buy/sell at target price | Use `type=limit` at user-provided price |
| User asks for fastest fill at current market | Prefer `market`; if "fast limit" is requested, use best book price |
| Market buy (`buy`) | Fill `amount` with USDT quote amount, not base quantity |
| Market sell (`sell`) | Fill `amount` with base-coin quantity, not USDT amount |
| User requests take-profit/stop-loss | Use trigger-order workflow: validate position size, draft TP+SL legs, then place after explicit confirmation |
| Any order placement request | Require explicit final user confirmation before `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| User has not replied with clear confirmation | Keep order as draft; no trading execution |
| Confirmation is stale or not from the immediately previous turn | Invalidate it and require a fresh confirmation |
| Multi-leg trading flow | Require per-leg confirmation before each `gate-cli cex spot order buy` / `gate-cli cex spot order sell` |
| User asks to amend an unfilled buy order | Confirm price increase amount or exact target price before `gate-cli cex spot order amend` |
| Multiple open buy orders match amendment request | Ask user to choose which order to amend before executing |
| User requests selected-order batch cancellation | Verify each order id exists/open, present list, and run `gate-cli cex spot order batch-cancel` only after user verification |
| User requests batch amend for open orders | Filter target pair open buy orders (max 5), compute repriced levels, and run `gate-cli cex spot order batch-amend` only after user verification |
| User requests trigger-order progress | Read one trigger order and compare current ticker price to trigger condition; return numeric distance |
| User requests trigger-order batch cancellation | Filter trigger orders by pair+side, present cancellation scope, then call `gate-cli cex spot price-trigger cancel-all` after confirmation |
| User requests single trigger-order cancellation | Verify order is active/matching intent, then call `gate-cli cex spot price-trigger cancel` after confirmation |
| User requests market slippage simulation | Use order-book depth simulation and compare weighted fill vs ticker last price |
| User requests multi-coin one-click buy | Validate summed quote requirement, then use `gate-cli cex spot order batch-create` |
| User requests fee comparison for multiple pairs | Use `gate-cli cex spot account batch-fee` and convert to cost impact with latest prices |
| User requests account flow for a coin | Use `gate-cli cex spot account book` and then reconcile with `gate-cli cex spot account get` |
| User amount is too small | Check `min_quote_amount`; if not met, ask user to increase amount |
| User requests all-in buy/sell | Use available balance, then trim by minimum trade rules |
| Trigger condition not met | Do not place order; return current vs target price gap |

## Report Template

```markdown
## Execution Result

| Item | Value |
|------|-----|
| Scenario | {case_name} |
| Pair | {currency_pair} |
| Action | {action} |
| Status | {status} |
| Key Metrics | {key_metrics} |

{decision_text}
```

Example `decision_text`:
- `✅ Condition met. Your order has been placed.`
- `📝 Order draft ready. Reply "Confirm order" to execute.`
- `⏸️ No order placed yet: current price is 60200, above your target 60000.`
- `❌ Not executed: minimum order amount is 10U, your input is 5U.`

## Error Handling

| Error Type | Typical Cause | Handling Strategy |
|----------|----------|----------|
| Insufficient balance | Not enough available USDT/coins | Return shortfall and suggest reducing order size |
| Minimum trade constraint | Below minimum amount/size | Return threshold and suggest increasing order size |
| Trigger-order parameter mismatch | Trigger rule/price/side is inconsistent with user intent | Return normalized trigger draft and require user reconfirmation |
| Missing final confirmation | User has not clearly approved final order summary | Keep order pending and request explicit confirmation |
| Stale confirmation | Confirmation does not match the current draft or is not in the previous turn | Reject execution and ask for reconfirmation |
| Draft-only mode | User has not confirmed yet | Only run query/estimation tools; do not call `gate-cli cex spot order buy` / `gate-cli cex spot order sell`, `gate-cli cex spot order batch-create`, or `gate-cli cex spot price-trigger create` |
| Ambiguous amendment target | Multiple candidate open buy orders | Keep pending and ask user to confirm order ID/row |
| Batch-cancel ambiguity | Some requested order ids are missing/not-open | Return matched vs unmatched ids and request reconfirmation |
| Batch-amend ambiguity | Candidate order set is unclear or exceeds max selection | Ask user to confirm exact order ids (up to 5) before execution |
| Order missing/already filled | Amendment/cancellation target is invalid | Ask user to refresh open orders and retry |
| Market condition not met | Trigger condition is not satisfied | Return current price, target price, and difference |
| Pair unavailable | Currency suspended or abnormal status | Clearly state pair is currently not tradable |

## Cross-Skill Workflows

### Workflow A: Buy Then Amend

1. Place order with `gate-exchange-spot` (Case 2/9/23)
2. If still unfilled, amend price (Case 17)

### Workflow B: Cancel Then Rebuy

1. Cancel all open orders to release funds (Case 6)
2. Re-enter with updated strategy (Case 1/2/9)

## Safety Rules

- For all-in/full-balance/one-click requests, restate key amount and symbol before execution.
- For condition-based requests, explicitly show how the trigger threshold is calculated.
- For TP/SL-style requests on spot, use the price-trigger workflow in this skill; do not imply unsupported CEX features—draft trigger legs and confirm before `gate-cli cex spot price-trigger create`.
- Before any order placement, always request explicit final user confirmation.
- Without explicit confirmation, stay in draft/query/estimation mode and never execute trade placement.
- Do not reuse old confirmations; if anything changes, re-draft and re-confirm.
- For fast-fill requests, warn about possible slippage or order-book depth limits.
- For chained actions (sell then buy), report step-by-step results clearly.
- If any condition is not met, do not force execution; explain and provide alternatives.
