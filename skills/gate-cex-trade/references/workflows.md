# Gate CEX workflows

Use this file with `runtime.md` and the product reference. Canonical `*-commands.md` references define callable CLI actions and parameters; supplementary API references cannot override them; this file defines intent parsing, confirmation, reconciliation, and user-facing failure messages.

## Source precedence

- Gate API v4 documentation is authoritative for REST paths, request fields, enums, response states, and API-side prerequisites. Use the current [English API v4 reference](https://www.gate.com/docs/developers/apiv4/en/) or [Chinese API v4 reference](https://www.gate.com/docs/developers/apiv4/zh_CN/) and the linked module pages.
- Reviewed source establishes only that source version's command support. Verify the installed version and required parameters separately from permissions and product eligibility. Run the exact leaf command with `--help`; parent help is not enough.
- Trace registration, parameter parsing, handler and SDK request construction when checking a suspected mismatch. A `CommandError` path is diagnostic text, not evidence of the path sent. Stop only the affected operation for a verified mismatch or missing capability. Never silently translate a missing CLI field.
- [Runtime](runtime.md) links the six shared rules governing authentication, permissions, authorization, execution deadlines and recovery; supplementary scenarios cannot weaken them. Private reads and writes use only registered CLI commands. Missing required commands or flags stop that operation, without a private HTTP/SDK/API-executor fallback.

## Intent parsing

Extract these fields before choosing a route:

`product` · `market/instrument` · `action` · `side` · `open/close/reduce` · `amount + unit` · `price/order type` · `trigger` · `leverage` · `margin mode` · `position mode/side` · `settlement` · `time-in-force` · `reduce_only` · `protection` · `scope`.

Ask one focused clarification when a missing field can change the order or product:

- “buy BTC” → ask spot, margin, or another product and the amount/unit.
- “go long with 500 USDT” → ask spot or futures, market or limit, leverage, margin mode, and whether 500U is margin or notional.
- “close my BTC position” → ask which product and position side if the account can contain more than one.
- “close all positions” → identify the snapshot of positions and whether the user means all products or one product.
- “change unified-account leverage or collateral” → ask the currency or collateral set and the target value; this is a configuration write, not an order.

Do not use a guessed default for product, quantity unit, leverage, side, trigger behavior, or scope. If there is no interactive confirmation channel, do not perform a write. Render the no-confirmation toast below in the user's language.

## Read path

1. Select the product route and the narrowest read-only command.
2. Read live market rules and status when interpreting price, size, contract value, precision, min/max, or available order types.
3. Return the value, unit, market, timestamp, and filtering assumptions. A read request must not borrow, transfer, amend, cancel, or place an order. Treat an empty object or missing required fields as a failed read when querying a specific resource.

The CLI may return exit code 0 with an error envelope. Parse the output and treat a top-level `error` object, Gate `label`/ `message`, a wrong result type, missing required result fields, or an empty object for an invalid identifier as a failed read. Validate the expected result schema before using a value in a confirmation.

### Conditional-order read validation

For a specific futures or spot conditional-order lookup, validate the identifier and the returned shape before reporting a result. `order_id` must be a positive identifier. A futures detail must contain the order identity/status plus the conditional fields returned by the route, including `initial.contract`, a non-empty `initial.price` that is parseable as a finite decimal (JSON number or decimal string), and `trigger.price` (and `trigger.rule`/`trigger.price_type` when the route returns them). An empty object, an empty `initial`/`trigger`, or a response such as `order_id=0 → {initial:{},trigger:{}}` is a failed read, even when the HTTP status or CLI exit code is zero. Preserve the raw error and trace when available; do not use the empty response for reconciliation or confirmation.

```text
Toast: Conditional-order lookup returned an empty result; state is unconfirmed
Next step: Verify order ID, market/pair and applicable settle/contract; continue only with an explicit NOT_FOUND/INVALID_PARAM or complete conditional-order result.
```

## Write classes and preflight

Classify the write before selecting the recovery path:

| Write class | Examples | Required preflight | Reconciliation key |
| --- | --- | --- | --- |
| Order or trigger | spot/futures/options/TradFi/Alpha order, amend, cancel | Product rules, account/balance, current order or position, exact scope | Returned order/trigger ID, client/text ID when exposed, then fills/position/balance |
| Loan or repayment | unified loan, margin borrow/repay (independent MCL writes hand off to Earn) | Account mode, borrowable/liability, rate, currency/pair, repayment policy | Liability, loan list/records, interest, and balance; do not require an order ID |
| Account configuration | unified mode, leverage, collateral, futures position mode/margin mode | Current setting, positions/orders/liabilities that can block the change, target value | Re-read the setting and the affected account/position state |
| Protection or kill switch | options MMP, countdown cancellation, scoped order cancel | Exact underlying/contract/pair scope, current state, thresholds | Resource state and scope response; if no read endpoint exists, report acceptance only and do not claim active state |
| Conversion | Flash Swap | Supported pair/limits, fresh quote, quote expiry, balances | Returned conversion order ID/status plus resulting balances |

For every class, normalize the exchange-native unit and preserve decimal strings. Do not run irrelevant checks merely because another product uses them. A missing deterministic lookup for a write is a blocking limitation unless the product reference explicitly defines a bounded state read.

Countdown cancellation uses its restored product-specific command contract: confirm pair/contract/underlying scope, timeout, renewal plan and stop condition; `0` disables. Do not arm a timer without reliable renewal or claim an accepted timer is verified active.

## Confirmation summaries

Show the complete summary immediately before the first write in a confirmed sequence. Use the user's language and include the fields for the selected product:

- **Spot:** pair, buy/sell, market or limit, quote amount versus base amount, price, account, and any supported auto-borrow/repay or protection fields.
- **Margin:** pair/account scope, borrow/repay action, currency and amount, loan type, leverage/LTV where applicable, interest estimate, and repayment/collateral step.
- **Futures:** settle, contract, signed contract size, position mode/side, open/close/reduce-only, price/order type, leverage, margin mode, trigger price type/rule, and protection fields.
- **Options:** underlying, expiry, strike, call/put, signed integer contracts, multiplier, price or mark-IV fields, TIF, reduce-only/close, MMP, and settlement.
- **Alpha:** chain/token identity, buy/sell amount unit, gas mode, slippage, fresh quote ID, quote expiry, and the expected status checks.
- **Flash Swap one-to-one:** sell/buy assets, source/target amounts, rate, preview ID, quote freshness/expiry if returned, and resulting balance check.
- **Flash Swap multi-currency:** protocol (`one_to_many` or `many_to_one`), every `params[]` leg with its sell/buy asset and amount, quote metadata returned for that protocol, expiry if returned, and the per-leg balance check. Do not display a single preview ID unless that protocol actually returns and requires one.
- **TradFi/CFD:** symbol, API side (`1=sell`, `2=buy`), native volume/unit, `price_type=market|trigger`, price, TP/SL, and region/session assumptions. For close, show `close_type=1` partial or `2` full and the partial volume when applicable. Do not use the legacy CLI numeric mapping when it conflicts with API v4.
- **Stock/ETF:** symbol, exchange/session, API side (`1=sell`, `2=buy`), native volume, `price_type=market|limit`, price when required, time-in-force, and close type (`1` partial or `2` full).
- **Unified/configuration:** account mode, currency or collateral scope, old value, new value, and the positions/liabilities/orders that must be clear.
- **Batch:** exact item list, side/size or target values, scope, count, and the stop condition for partial failure.

For independent MCL requests, use the [Earn handoff](vipfee.md#independent-lending-handoff); do not execute these writes in Trade.

The confirmation covers the complete displayed operation, including account, scope, parameters, quote/expiry, declared sequence, and stop condition. Reuse it for unchanged writes in the same execution context. Reads, bounded polling, reconciliation, and read retries do not trigger another confirmation. Ask again only when a parameter, account, scope, sequence step, quote, expiry, or live resource state changes in a way that affects the confirmed operation, safety, or stop condition, when execution is paused and resumed, or when a new write/cleanup action was not included in the confirmed sequence. Expected state transitions inside the declared sequence do not trigger another confirmation. If any confirmed value changes, render the changed fields and request a new complete confirmation.

## Execution and reconciliation

1. Check credentials, skill/tool availability, and a read-only sanity check.
2. Run the class-specific preflight above.
3. Present the product-specific confirmation summary and wait for explicit confirmation unless an active confirmation already covers this exact unchanged write or declared sequence.
4. Generate a unique client/text ID only where the API and installed route expose one. Do not invent flags for options, triggers, streams, configuration, or Flash Swap.
5. Execute only the registered CLI command under the shared execution policy.
6. Reconcile using the class-specific key. For an order, query the returned ID and then fills/position. For a loan or configuration write, re-read the resource state and compare before/after. For a sequence, stop when a materially different step fails and report prior state.
7. Report the raw API error code/message internally, the request fields needed to recover, and the user-facing state without secrets.

## Common scenarios

### Spot buy/sell

Resolve base quantity versus quote amount, then apply pair precision and market-order limits. After create, query the order and fills. A price-trigger order is a single trigger order; it is not an OCO/OTO/OTOCO/OPOCO relationship.

### Spot time-slice / POV

Use the registered POV leaves in [algorithm commands](algo-commands.md); validate the installed leaf and JSON contract. State that Gate's endpoint is POV-like and do not call it Binance TWAP/VP equivalent. A CLI leaf or parent help entry alone does not verify the request path, fields, or response envelope; if the installed required capability is not verified, stop with the unavailable-operation toast instead of sending repeated ordinary orders.

### Margin borrow → trade → repay

Check account mode, borrowable amount, rate, current liabilities, and transferable balance. Confirm the borrow and repayment policy, borrow, verify the liability, execute the supported margin order, and repay only when requested and supported. A failed later step leaves earlier debt visible; do not silently repay or retry.

### Futures open, close, and reverse

Read contract size, settle, position mode, leverage limits, margin mode, and current position. For close/reduce, use reduce-only or the mapped close form and verify the resulting position. For reverse, close and verify first, then open the opposite side. Remove unsupported ranking-based “top gainer/loser” selection from execution unless a market-analysis route supplies the universe, metric, snapshot time, and exact selection list.

### Trigger, TP/SL, and trailing protection

State whether the trigger opens or closes, reference price and price type, direction, execution order type, quantity, and whether funds are reserved now or at trigger time. Create protection only when the route exposes the required reduce-only/close/position-related field. Report trigger state separately from position state.

### TradFi/CFD single-side protection update

Before changing only TP or only SL on a CFD order or position, read the current resource and capture both `price_tp` and `price_sl`. Build a complete update payload: apply the requested side, and pass the other side's current API value unchanged. The API treats an omitted value or `"0"` as clearing that side, so omission is never a preservation strategy. For order updates, carry the current order price as well. If the current value cannot be read, the adapter cannot send both fields, or the post-write read does not show the untouched side unchanged, block or report the write as unresolved. The confirmation must show both before and after values and any explicit clear action.

### Cancel and amend

Resolve a unique order ID, client ID, or an explicit filtered set. “Cancel all” must state product, market/scope, count, and affected order list. Re-read before each batch item. If an item changes, pause and request fresh confirmation; never silently drop it. Amend only open/unfilled orders and re-check the amended order.

### Configuration and MMP

Read the current setting first. Confirm the exact scope and target value. After the write, read the setting/resource again when an endpoint exists. MMP reset does not restore orders already cancelled. An account-wide cancel or kill-switch request must name the exact underlying/contract/pair scope.

### Flash Swap and Alpha

Read supported pairs, limits, and a fresh quote. Show the quote ID and all expiry data returned by the service. Confirm, accept, then query the returned order/conversion status and balances. Use the standard one-to-one Flash Swap route unless the v1 or multi-currency deployment and adapter paths have been explicitly verified; do not silently fall back between protocol families. Alpha status `processing` and buy-transfer-pending are not success; a fresh confirmation is required after quote expiry.

## Failure handling

Every failure, timeout, partial result, or blocked write must render this two-line toast in the user's language:

```text
Toast: {current issue}
Next step: {next action}
```

The [reviewed Chinese examples](localized-examples.json) are a localized-data exception for user prompts and display messages only. They do not alter the English execution rules. Use these mappings:

| Situation | User-facing toast | Next step |
| --- | --- | --- |
| Write timeout with a deterministic lookup key | `Toast: Write outcome unconfirmed (queried by the available identifier)` | `Next step: Do not repeat the write. Retain the order, resource or request identifier and reconcile with the product query before continuing.` |
| Write timeout without a deterministic lookup key | `Toast: Write outcome unconfirmed (no unique lookup identifier is available)` | `Next step: Do not repeat the write. Read the resource state or request manual reconciliation.` |
| No unique lookup after bounded reconciliation | `Toast: The write outcome cannot be uniquely reconciled` | `Next step: Do not retry the write. Retain identifiers and errors, query again later, and seek manual reconciliation if needed.` |
| HTTP 429 or exchange rate limit | `Toast: Request rate limited (HTTP 429)` | `Next step: Wait for the server Retry-After interval, pause new writes, then query; do not retry in a loop.` |
| Insufficient balance, precision, closed market, or leverage conflict | `Toast: Request parameters or account state prevent execution ({field/error code})` | `Next step: Read current rules, balances, positions or limits, correct the parameters, and obtain confirmation again.` |
| Protection order failed after a partial/full entry | `Toast: The entry partially or fully took effect, but protection failed ({error summary})` | `Next step: Verify actual filled exposure, then obtain confirmation to retry protection, close reduce-only, or explicitly retain unprotected exposure.` |
| One leg of a sequence succeeded | `Toast: Some steps completed ({completed steps})` | `Next step: Reconcile orders, balances, liabilities and positions; obtain confirmation before continuing remaining steps.` |
| User changes a confirmed parameter | `Toast: Execution parameters changed ({changed fields})` | `Next step: Show the complete updated execution summary and request confirmation.` |
| Required API/command/path is unavailable or incompatible | `Toast: The installed CLI lacks a compatible command or required parameter` | `Next step: Do not substitute a similar product or simulate commands; retry only after installed CLI capability is verified; never use a private API fallback.` |
| API authentication or permission failure | `Toast: Gate API authentication or permissions are insufficient` | `Next step: Check API permissions, the IP allowlist and account permissions in Gate settings; never paste secrets into chat.` |
| Quote expired | `Toast: Quote expired` | `Next step: Obtain a fresh quote and confirmation; do not submit the old quote/preview ID.` |
| MMP frozen | `Toast: Options MMP is frozen` | `Next step: Verify the freeze reason and current orders, then obtain confirmation before MMP reset.` |
| Conditional-order lookup returns an empty or incomplete object | `Toast: Conditional-order state is unconfirmed` | `Next step: Check ID and product scope; do not use an empty or incomplete object for reconciliation.` |
| Empty or structurally invalid read result | `Toast: Read result is empty or lacks required fields` | `Next step: Verify the resource ID, query scope and response schema before continuing; an empty object is not success.` |
| No confirmation channel or valid grant | `Toast: Execution authority is unavailable` | `Next step: Retain the draft and obtain a valid grant before any write.` |
| Read query failed | `Toast: Gate state read failed ({error summary})` | `Next step: Retry the same read-only query later; do not submit new writes while state is unconfirmed.` |
| Borrow succeeded but trade failed | `Toast: Borrowing succeeded but trading did not complete; a liability remains` | `Next step: Verify the liability and interest, then obtain confirmation for repayment or further trading.` |

For a write with a deterministic key, reconcile at most three times at increasing intervals such as 1s, 2s, and 5s unless the product route defines another bound. For a write without a key, read the documented resource state instead; never claim that an order lookup occurred when it did not.

## Completion and status predicates

- **Spot:** report `open`, `finished`, `cancelled`, `failed`, or the returned product status. A terminal response is successful only when filled amount and remaining amount satisfy the request; a cancelled remainder is not a full fill. Trigger status `finish` is separate from spot order status.
- **Futures/options:** `finished` is a container state. Use `finish_as=filled` or the product-specific successful close/reduce predicate, then re-read position size. `cancelled`, `ioc`, `reduce_only`, liquidation, or MMP cancellation are not full-fill success.
- **Alpha:** `2` is success; `1` is processing; `5` is buy placed/transfer pending; `6` is cancelled/transfer pending; `3` failed; `4` cancelled. Query the Alpha order and do not collapse pending states into success.
- **Flash Swap:** `1` success and `2` failed; query the order and resulting balances.
- **TradFi:** use the official order/position response status and re-read the order or position. A submitted order or close request is not proof that the position is flat.
- **Loans/configuration/MMP:** there is no generic order terminal state. Report the accepted response only until the documented resource read confirms the target liability, mode, leverage, collateral, or MMP state.

An order or resource still open, processing, pending, or unresolved after bounded reconciliation remains pending; render the appropriate toast and next query action. Report filled quantity, remaining quantity, debt, and live exposure separately.

