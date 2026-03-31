# Trading Copilot Scenarios

Global rule: any scenario that ends with a write tool requires an **Action Draft** and explicit **Y** before execution. Query-only scenarios never call write tools. All **26** scenario slots match **Trading Copilot L2 Tool Calls spec v1.3** (15 base + 7 composite + 4 extended); **scenarios 6 and 19 are temporarily hidden**—they invoke **no** MCP tools in this skill and must not name exchange tools in the reply (see below).

**Signal detection (summary):** Extract `symbol`, `side`, `amount`, `price`, `leverage` when present; activate **S1–S8** independently (non-exclusive). Explicit **cross-margin leveraged long or short** (spot-margin wording) → **S3**, **not** **S2** futures. **Only S5** (plus read-only S7/S8) → query-only; **S1–S6** or TradFi/Alpha **writes** → Action Draft → **Y** → execute. See **`SKILL.md`** **Signal detection workflow** and **Execution mode**.

## Scenario 1: Spot Market Buy by USDT Notional

**Context**: User wants to spend a fixed USDT amount on a spot pair at market (signal **S1**).

**Prompt Examples**:
- "Market buy 1000 USDT of BTC for me."
- "Buy BTC with 1000 USDT at market."

**Expected Behavior**:
1. Call `cex_spot_get_spot_accounts` and `cex_spot_get_spot_tickers` for the pair.
2. Build an Action Draft with side `buy`, market notional in quote (USDT), estimated fill, fees, and slippage risk.
3. After Y, call `cex_spot_create_spot_order`.

## Scenario 2: Spot Limit Sell

**Context**: User wants to sell a base quantity at a limit price (**S1**).

**Prompt Examples**:
- "Limit sell 0.5 BTC at 92000."
- "Place a limit sell for 2 ETH at 3200."

**Expected Behavior**:
1. Call `cex_spot_get_spot_accounts` for the base currency; use `cex_spot_get_currency_pair` if rules need confirmation.
2. Draft limit fields (pair, price, size) and show estimated proceeds and fees if available.
3. After Y, call `cex_spot_create_spot_order` with `type=limit` and `side=sell`.

## Scenario 3: Futures Open Long With Leverage

**Context**: User wants a leveraged long with stated margin and leverage (**S2**). Spec: if the user says "leverage long" with a multiplier and **no** borrow/repay wording, treat as **futures** first (not isolated margin borrow).

**Prompt Examples**:
- "Open 10x long on ETH with 500 USDT."
- "Use 500 USDT margin for a 10x ETH long."

**Expected Behavior**:
1. If **perpetual vs delivery** is unclear, ask which contract type; then call `cex_fx_get_fx_accounts`, `cex_fx_get_fx_contract`, `cex_fx_get_fx_tickers`, and `cex_fx_get_fx_dual_position` (or `cex_fx_list_fx_positions`) to infer position mode.
2. If dual-position mode applies and isolated vs cross must be chosen for the new order, ask; otherwise use the active position settings.
3. Build Action Draft with leverage, estimated liquidation risk, and margin source; after Y, call `cex_fx_update_fx_position_leverage` / dual-position leverage tools if required, then `cex_fx_create_fx_order`.

## Scenario 4: Futures Take-Profit on Open Position

**Context**: User sets a take-profit on an existing futures long (**S2**).

**Prompt Examples**:
- "Set take profit on my BTC long at 95000."
- "When BTC hits 95000, take profit on my long."

**Expected Behavior**:
1. If contract type (perpetual vs delivery) is unclear, ask; then call `cex_fx_list_fx_positions` and use `cex_fx_get_fx_dual_position` with positions to disambiguate **isolated vs cross** when both exist for the same direction.
2. Draft price-triggered order parameters (contract, trigger price, linkage to position side and margin mode).
3. After Y, call `cex_fx_create_fx_price_triggered_order`.

## Scenario 5: Isolated Margin Short (Borrow Then Sell Spot)

**Context**: User wants isolated margin short exposure: borrow then sell spot (**S3**).

**Prompt Examples**:
- "Margin short SOL with 5x and 200 USDT principal."
- "Isolated margin: short SOL with 200 USDT."

**Expected Behavior**:
1. If **isolated vs cross** margin is unclear, ask (spec: isolated path uses isolated margin account funding).
2. Call `cex_margin_list_margin_accounts` and `cex_margin_get_uni_borrowable` (or equivalent borrowable reads for the pair/currency).
3. Draft borrow size and spot sell leg with margin and liquidation warnings; after Y, call `cex_margin_create_uni_loan` (borrow) then `cex_spot_create_spot_order` (sell on margin account per API).

## Scenario 6: (Hidden) Single-Leg Flash Swap

**Context**: **This scenario is disabled in `gate-exchange-tradingcopilot`.** For standalone “flash quote→one base” requests (e.g. 500 USDT to ETH), this skill must **not** invoke **any** MCP tool and must **not** name or list exchange tools in the reply—only hand off.

**Prompt Examples**:
- "Flash swap 500 USDT to ETH."
- "Convert 500 USDT into ETH via flash swap."

**Expected Behavior**:
1. **Do not call any MCP tool** in this skill for this intent (no reads, no writes).
2. Reply by directing the user to the **`gate-exchange-flashswap`** skill or the Gate app for execution; keep the message free of tool identifiers.

## Scenario 7: Recent Futures Orders and Entrustments (Query)

**Context**: User wants **futures working orders plus recent finished entrustments** (**S5**, query-only). This skill does **not** replace a full cross-account asset / PnL merge (use **`gate-exchange-assets`** for inventory-style “all balances + PnL”).

**Prompt Examples**:
- "Show my recent futures entrustments."
- "List my open perp orders and recent ended futures orders."

**Expected Behavior**:
1. Call `cex_fx_list_fx_orders` for **open** orders and for **finished** orders in a **time window** (e.g. default last 7 days or user-specified); sort by update time as appropriate.
2. If the user names **no** contract, ask for a pair **or** return what the API allows and summarize.
3. No write tools unless the user adds execution intent.

## Scenario 8: Cancel a Specific Spot Order

**Context**: User cancels one identifiable open spot order (**S6**).

**Prompt Examples**:
- "Cancel that BTC limit order I just placed."
- "Remove my open ETH_USDT buy order."

**Expected Behavior**:
1. Call `cex_spot_list_spot_orders` with open status; disambiguate if several orders match ("the BTC order" → pick latest or ask).
2. Action Draft naming order id and key fields; after Y, call `cex_spot_cancel_spot_order`.

## Scenario 9: List Open Orders (Spot and Futures)

**Context**: User wants all working orders across spot and futures (**S5**).

**Prompt Examples**:
- "Show all my open orders."
- "List unfilled spot and perp orders."

**Expected Behavior**:
1. Call `cex_spot_list_spot_orders` and `cex_fx_list_fx_orders` with open filters; summarize in one view.
2. No writes.

## Scenario 10: Recent Trade History Window

**Context**: User wants fills or finished activity over a time window (**S5**).

**Prompt Examples**:
- "Show my trades from the last three days."
- "Pull recent spot and futures fills."

**Expected Behavior**:
1. Call `cex_spot_list_spot_my_trades` and `cex_fx_list_fx_my_trades` with time filters; add order-list calls with `finished` if the user needs order objects.
2. No writes.

## Scenario 11: Cross-Margin / Unified Leveraged Long

**Context**: User wants a **cross-margin style** leveraged long using unified account borrow and spot buy (**S3**).

**Prompt Examples**:
- "Cross margin long ETH at 3x with 1000 USDT principal."
- "Unified account: borrow USDT and buy ETH up to 3x leverage."

**Expected Behavior**:
1. Call `cex_unified_get_unified_mode`. If the mode does **not** support this flow (spec: require **multi_currency** or **portfolio**), stop and instruct the user to switch unified mode in the app—no writes.
2. Call `cex_unified_get_unified_accounts`, then `cex_unified_get_unified_borrowable`, then `cex_spot_get_spot_tickers`. If **`cex_unified_get_unified_borrowable`** fails and the returned message indicates **single currency mode** is not supported (e.g. contains `operation not support for single currency mode`, case-insensitive), **stop**: tell the user to switch the unified account to **cross-currency margin mode** or **portfolio margin mode** in the Gate app or web, then retry—no Action Draft and no writes.
3. If borrowable succeeds, compute borrow need from principal × leverage vs notional.
4. Action Draft with interest and liquidation context; after Y, call `cex_unified_create_unified_loan` (borrow) then `cex_spot_create_spot_order` (buy with cross_margin / unified account per API).

## Scenario 12: Futures Add to Open Position

**Context**: User adds contracts to an existing futures position (**S2**).

**Prompt Examples**:
- "Add 2 contracts to my ETH long."
- "Scale into my SOL long by 5 contracts."

**Expected Behavior**:
1. If perpetual vs delivery is unclear, ask; call `cex_fx_list_fx_positions`, `cex_fx_get_fx_accounts`, `cex_fx_get_fx_contract`, `cex_fx_get_fx_tickers`, and `cex_fx_get_fx_dual_position` as needed.
2. If dual-mode creates duplicate isolated/cross longs for the same contract, ask which position to add to.
3. Draft added size and updated liquidation context; after Y, call `cex_fx_create_fx_order`.

## Scenario 13: Futures Reduce Open Position (e.g. Half)

**Context**: User reduces size on a position (e.g. "reduce half", "take some profit") (**S2**).

**Prompt Examples**:
- "Reduce my position by half—take profits."
- "Cut my BTC perp long by 50 percent."

**Expected Behavior**:
1. If symbol and side are missing, ask; if perpetual vs delivery unclear, ask; call `cex_fx_list_fx_positions` and `cex_fx_get_fx_dual_position` to disambiguate isolated vs cross when needed.
2. Draft reduce-only size; after Y, call `cex_fx_create_fx_order` with reduce-only semantics per API.

## Scenario 14: Unified-Account Loan Repayment

**Context**: User repays **unified-account borrow** only (e.g. “repay 10 USDT on unified loan”) (**S3**). Cross-margin **spot sell + repay** in one story is a **different** flow—use **`gate-exchange-margin`** / **`gate-exchange-unified`** with spot legs, not this repay-only pattern.

**Prompt Examples**:
- "Unified account: repay 10 USDT of loan."
- "Repay 10 USDT unified borrow."

**Expected Behavior**:
1. Parse currency (e.g. **USDT** for “10U”); call `cex_unified_list_unified_loan_records` and `cex_unified_get_unified_accounts` to align outstanding borrow with available balance.
2. Action Draft (`type=repay`, currency, amount); after **Y**, call `cex_unified_create_unified_loan` with repay parameters per API.

## Scenario 15: Futures Stop / Trigger From Price Level

**Context**: User places a stop or protective trigger at a price (**S2**).

**Prompt Examples**:
- "If BTC drops below 90000, close or stop out my long."
- "Set a stop for my BTC long at 90000."

**Expected Behavior**:
1. Clarify perpetual vs delivery if needed; call `cex_fx_list_fx_positions` and disambiguate isolated vs cross when duplicate longs exist.
2. Draft trigger; after Y, call `cex_fx_create_fx_price_triggered_order`.

## Scenario 16: Conditional Reduce After PnL Check

**Context**: User queries PnL and only reduces if a threshold is met (**S5** → **S2**).

**Prompt Examples**:
- "Check my BTC contract PnL; if profit is over 10 percent, reduce half."
- "If my ETH long is up more than 500 USDT, trim a third."

**Expected Behavior**:
1. Clarify perpetual vs delivery; call `cex_fx_list_fx_positions`, `cex_fx_get_fx_tickers`, and position mode helpers; compute PnL and show status.
2. If the condition is **not** met, report only (query-only). If met, disambiguate position if needed, then Action Draft for partial close; after Y, call `cex_fx_create_fx_order` (reduce).

## Scenario 17: Close Long Then Open Short (Same Underlying)

**Context**: User flips from long to short on the same contract (**S2** + **S2**, two confirmations).

**Prompt Examples**:
- "Close all my ETH longs then open a 5x short."
- "Flatten my BTC long and short the same size."

**Expected Behavior**:
1. Clarify perpetual vs delivery; call `cex_fx_list_fx_positions`, `cex_fx_get_fx_accounts`, `cex_fx_get_fx_contract`, `cex_fx_get_fx_tickers`.
2. Action Draft 1: close long; after Y, `cex_fx_create_fx_order` to close.
3. Action Draft 2: open short with leverage; clarify isolated vs cross for the new short if dual mode requires; after Y, `cex_fx_create_fx_order` to open short (and leverage tools if required).

## Scenario 18: Spot Buy Plus Futures Open (Combined)

**Context**: User wants spot purchase and a futures leg in one plan (**S1** + **S2**).

**Prompt Examples**:
- "Buy 500 USDT of BTC on spot and open a 1000 USDT notional BTC long on perps."
- "Spot buy 500 USDT BTC and long BTC futures with 1000 USDT margin."

**Expected Behavior**:
1. Parallel read: `cex_spot_get_spot_accounts`, `cex_fx_get_fx_accounts`, `cex_spot_get_spot_tickers`, `cex_fx_get_fx_tickers`, `cex_fx_get_fx_contract`.
2. One combined Action Draft for both legs; after Y, call `cex_spot_create_spot_order` and `cex_fx_create_fx_order` in parallel if the user confirmed both.

## Scenario 19: (Hidden) Futures Reduce Plus Flash Swap

**Context**: **This scenario is disabled in `gate-exchange-tradingcopilot`.** For a single plan that combines **futures position reduction** with a **flash swap / convert** leg (**S2** + **S4**), this skill must **not** invoke **any** MCP tool and must **not** name or list exchange tools in the reply—only hand off.

**Prompt Examples**:
- "Reduce my SOL long by 50 percent and flash-convert USDT to ETH."
- "Trim my perp position then swap USDT to ETH."

**Expected Behavior**:
1. **Do not call any MCP tool** in this skill for this intent (no reads, no writes).
2. Reply by directing the user to the **`gate-exchange-futures`** and **`gate-exchange-flashswap`** skills (or the Gate app) for execution; keep the message free of tool identifiers.

## Scenario 20: Cancel All Open Orders on Pair Then Limit Re-Place

**Context**: User clears working orders on a pair then places a new limit (**S6** → **S1**). **Each write requires its own confirmation**—even if the user states both steps in **one** sentence.

**Prompt Examples**:
- "Cancel all BTC_USDT spot orders and place a limit buy at 91000 for 0.1 BTC."
- "Pull all ETH resting orders and re-list my bid at 3000."

**Expected Behavior**:
1. Call `cex_spot_list_spot_orders` and `cex_spot_get_spot_accounts`.
2. **Action Draft 1** (cancel-all scope only) → user **Y** → `cex_spot_cancel_all_spot_orders`.
3. **Action Draft 2** (new limit only) → user **Y** → `cex_spot_create_spot_order`.
4. **Do not** skip either draft or execute both legs without **two** **Y** replies (unless one combined draft explicitly lists **both** legs and receives **one** **Y** for **both**—default for this scenario is **two** rounds).

## Scenario 21: Margin Sufficiency Check Then Open Plus Take-Profit

**Context**: User asks for a risk read first; if OK, opens and sets take-profit (**S5** → **S2**).

**Prompt Examples**:
- "Check if I have enough futures margin; if yes, open 3 SOL longs and set take profit at 95."
- "If margin is fine, long 2 BTC contracts and TP at 100k."

**Expected Behavior**:
1. Call `cex_fx_get_fx_accounts`, `cex_fx_list_fx_positions`, `cex_unified_get_unified_accounts`, `cex_fx_get_fx_contract`, `cex_fx_get_fx_tickers`; summarize margin adequacy.
2. If insufficient, stop with explanation. If sufficient, draft open plus TP; after Y, call `cex_fx_create_fx_order` then `cex_fx_create_fx_price_triggered_order`.

## Scenario 22: Spot Sell Then Futures Open (Proceeds-Aware)

**Context**: User sells spot for quote, then opens a futures leg using updated balances (**S1** → **S2**).

**Prompt Examples**:
- "Sell 0.5 BTC spot, then use the USDT to open an ETH long."
- "Market sell my BTC, then open an ETH perp long with available margin."

**Expected Behavior**:
1. Call `cex_spot_get_spot_accounts` and `cex_spot_get_spot_tickers`; Action Draft 1 for spot sell; after Y, `cex_spot_create_spot_order`.
2. After fill, re-read balances and price with `cex_fx_get_fx_contract`, `cex_fx_get_fx_tickers`; Action Draft 2 for futures; after Y, `cex_fx_create_fx_order`.

## Scenario 23: TradFi Notional Buy (e.g. Gold)

**Context**: User buys a TradFi symbol for a dollar notional (**S7**).

**Prompt Examples**:
- "Buy about 100 USD of gold on TradFi."
- "Place a TradFi buy on XAUUSD for 100 dollars."

**Expected Behavior**:
1. Call `cex_tradfi_query_user_assets` and `cex_tradfi_query_symbols` (or `cex_tradfi_query_symbol_ticker` / `cex_tradfi_query_symbol_detail`) to resolve the symbol.
2. Action Draft; after Y, call `cex_tradfi_create_tradfi_order`.

## Scenario 24: Alpha Market Buy After Quote

**Context**: User buys an Alpha token with USDT notional (**S8**). Spec document may reference tickers; MCP uses quote + place.

**Prompt Examples**:
- "Market buy 1000 USDT of TRUMP on Alpha."
- "Buy 500 USDT of the Alpha token I name."

**Expected Behavior**:
1. Call `cex_alpha_list_alpha_accounts` and `cex_alpha_quote_alpha_order` to size and price the leg.
2. Action Draft; after Y, call `cex_alpha_place_alpha_order`.

## Scenario 25: Flash Swap One-to-Many (Split Quote)

**Context**: User splits one quote amount across multiple destination assets (**S4**).

**Prompt Examples**:
- "Flash swap 500 USDT into BTC, ETH, and SOL in one go."
- "Convert 500 USDT to multiple coins via flash swap."

**Expected Behavior**:
1. Call `cex_fc_preview_fc_multi_currency_one_to_many_order`; show rates and splits.
2. Action Draft; after Y, call `cex_fc_create_fc_multi_currency_one_to_many_order`.

## Scenario 26: Alpha Positions and PnL Query

**Context**: User wants Alpha exposure and PnL without trading (**S5**).

**Prompt Examples**:
- "Show my Alpha positions and PnL."
- "List my Alpha balances and open orders."

**Expected Behavior**:
1. Call `cex_alpha_list_alpha_accounts` and `cex_alpha_list_alpha_orders` or `cex_alpha_list_alpha_account_book` as needed to show positions and unrealized outcomes.
2. No writes unless the user adds execution intent.
