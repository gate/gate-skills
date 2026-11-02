# Alpha trading

## Scope and source

Use Alpha-specific currencies, quotes, balances and orders. Alpha belongs to CEX trading even when its token has an on-chain address; it is not a DEX wallet-signing task. Resolve the exact currency, chain and contract address from market metadata. Trade only a normal-status asset; do not match a symbol alone when metadata is ambiguous.

`--side buy` spends USDT through `--amount`; `--side sell` uses the base-token quantity through the same flag. Never copy spot's `--quote`/`--pair` syntax. Keep decimal strings and check precision, available funds, quote limits and estimated costs. Do not apply token-quantity precision to USDT spending without product evidence or silently round the budget. Gas mode is `speed` (smart selection) or `custom`; custom requires an explicit percentage slippage (`10` means 10%, not 0.10). Do not silently choose a looser tolerance. A smart quote does not establish a user-requested hard slippage cap.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [preflight](../../_shared/cex/preflight.md), [authentication](../../_shared/cex/cli-auth.md), [execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Market reads are public. Account/order reads are private. Quote is an authenticated calculation, not an order; the current Agentic route requires `spot_trade` for quote and place, while account verification can also need `base`. A scope grant is not user authorization to place an order.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `alpha.account.balances` | `gate-cli cex alpha account balances` | read |
| `alpha.account.book` | `gate-cli cex alpha account book` | read |
| `alpha.market.currencies` | `gate-cli cex alpha market currencies` | read |
| `alpha.market.tickers` | `gate-cli cex alpha market tickers` | read |
| `alpha.market.tokens` | `gate-cli cex alpha market tokens` | read |
| `alpha.order.get` | `gate-cli cex alpha order get` | read |
| `alpha.order.list` | `gate-cli cex alpha order list` | read |
| `alpha.order.place` | `gate-cli cex alpha order place` | write |
| `alpha.order.quote` | `gate-cli cex alpha order quote` | read |

## Invocation and parameter rules

Append `--format json`; pass values as separate argv items. Syntax blocks are templates. Defaults are registered values, not evidence that every zero/empty field is transmitted. No Alpha amend, cancel, limit-price, TP/SL or order client-reference command is registered in this skill contract.

A quote ID is valid for one minute. Record receipt time and use it promptly; receipt time cannot prove the server's exact expiry. Review `error_type`, amount limits, expected received range, fees and slippage before placement. A failed/expired quote must not be submitted. The SDK may omit zero `error_type` during JSON encoding; absence alone does not prove success. Require a nonempty quote ID and verified material bounds and terms. Requote only within the existing task budget and authority; material changes require renewed authority. Bind quote and place to the same selected account context, origin, currency, side, amount, gas mode and custom slippage.

<a id="alpha.account.balances"></a>
### `gate-cli cex alpha account balances`

Operation ID: `alpha.account.balances`. Effect: **read**.

List Alpha account balances

```text
gate-cli cex alpha account balances
```

API: `GET /api/v4/alpha/accounts` (private).

Returns: [][AccountsResponse](models/alpha.md#model-accountsresponse).

Parameters: shared options only.

<a id="alpha.account.book"></a>
### `gate-cli cex alpha account book`

Operation ID: `alpha.account.book`. Effect: **read**.

List Alpha account transaction history

```text
gate-cli cex alpha account book [flags]
```

API: `GET /api/v4/alpha/account_book` (private).

Returns: [][AccountBookResponse](models/alpha.md#model-accountbookresponse).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--from` | `int64` | Yes | `0` | Start timestamp (Unix seconds, required) |
| `--limit` | `int32` | No | `100` | Maximum number of records |
| `--page` | `int32` | No | `1` | Page number |
| `--to` | `int64` | No | `0` | End timestamp (Unix seconds) |

<a id="alpha.market.currencies"></a>
### `gate-cli cex alpha market currencies`

Operation ID: `alpha.market.currencies`. Effect: **read**.

List Alpha currencies

```text
gate-cli cex alpha market currencies [flags]
```

API: `GET /api/v4/alpha/currencies` (public).

Returns: [][AlphaCurrency](models/alpha.md#model-alphacurrency).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Canonical Alpha currency ID returned in metadata `currency`, not the display symbol |
| `--limit` | `int32` | No | `100` | Maximum number of records |
| `--page` | `int32` | No | `1` | Page number |

For a price request using only a display symbol (such as USDS or PUMP), first resolve the asset through currency metadata with a finite page/record budget. Match the available name, chain and address fields, then pass the unique returned `currency` value to `alpha market tickers --currency`. Do not use the display symbol as the filter or construct an ID from it. If several candidates match, ask for chain/address; if the budget ends without a match, report incomplete lookup and request identifying information rather than claiming the asset is unsupported.

<a id="alpha.market.tickers"></a>
### `gate-cli cex alpha market tickers`

Operation ID: `alpha.market.tickers`. Effect: **read**.

List Alpha tickers

```text
gate-cli cex alpha market tickers [flags]
```

API: `GET /api/v4/alpha/tickers` (public).

Returns: [][AlphaTicker](models/alpha.md#model-alphaticker).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Canonical Alpha currency ID; resolve display symbols using [currency metadata](#alpha.market.currencies) first |
| `--limit` | `int32` | No | `100` | Maximum number of records |
| `--page` | `int32` | No | `1` | Page number |

<a id="alpha.market.tokens"></a>
### `gate-cli cex alpha market tokens`

Operation ID: `alpha.market.tokens`. Effect: **read**.

List Alpha tokens

```text
gate-cli cex alpha market tokens [flags]
```

API: `GET /api/v4/alpha/tokens` (public).

Returns: [][Tokens](models/alpha.md#model-tokens).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--address` | `string` | No | Unset | Filter by contract address |
| `--chain` | `string` | No | Unset | Filter by API chain code; convert every chain code to lowercase before querying, e.g. `ETH` → `eth`, `SOLANA` → `solana` |
| `--page` | `int32` | No | `1` | Page number |
| `--platform` | `string` | No | Unset | Filter by launch platform (e.g. pump, gatefun) |

Convert every chain code to lowercase before passing `--chain`, whether supplied by the user or returned by metadata; the CLI forwards the value unchanged. Preserve contract addresses. Lowercasing does not resolve aliases or establish API support: `SOL` becomes `sol`, not `solana`; do not map aliases without verified metadata.

This leaf has `--page` but no `--limit`. Keep a finite page/record budget and stop on oversized or truncated output; never add an invented limit flag.

<a id="alpha.order.get"></a>
### `gate-cli cex alpha order get`

Operation ID: `alpha.order.get`. Effect: **read**.

Get an Alpha order by ID

```text
gate-cli cex alpha order get [flags]
```

API: `GET /api/v4/alpha/order` (private).

Returns: [OrderResponse](models/alpha.md#model-orderresponse).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--id` | `string` | Yes | Unset | Order ID (required) |

The SDK sends `--id` as the `order_id` query parameter to `/alpha/order`; the CLI error label mentions a different path and is not the wire contract.

<a id="alpha.order.list"></a>
### `gate-cli cex alpha order list`

Operation ID: `alpha.order.list`. Effect: **read**.

List Alpha orders

```text
gate-cli cex alpha order list [flags]
```

API: `GET /api/v4/alpha/orders` (private).

Returns: [][OrderResponse](models/alpha.md#model-orderresponse).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | No | Unset | Canonical Alpha currency ID from metadata `currency`, not a display symbol |
| `--from` | `int64` | No | `0` | Start timestamp (Unix seconds) |
| `--limit` | `int32` | No | `100` | Maximum number of records |
| `--page` | `int32` | No | `1` | Page number |
| `--side` | `string` | No | Unset | Filter by side: buy or sell |
| `--status` | `int32` | No | `0` | Filter by status: 0=all, 1=processing, 2=successful, 3=failed, 4=cancelled |
| `--to` | `int64` | No | `0` | End timestamp (Unix seconds) |

The help text lists statuses 0–4, but the response model also defines 5 and 6 for incomplete transfers. Omit the status filter when reconciling an unknown outcome; do not interpret the help enumeration as proof that these states cannot occur.

<a id="alpha.order.place"></a>
### `gate-cli cex alpha order place`

Operation ID: `alpha.order.place`. Effect: **write**.

Place an Alpha order using a quote ID

```text
gate-cli cex alpha order place [flags]
```

API: `POST /api/v4/alpha/orders` (private).

Returns: [PlaceOrderResponse](models/alpha.md#model-placeorderresponse).

API request model(s), assembled by the command: [PlaceOrderRequest](models/alpha.md#model-placeorderrequest). The CLI assembles this model from scalar flags; there is no raw JSON/body flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--amount` | `string` | Yes | Unset | Buy: USDT to spend; sell: base-token quantity (required) |
| `--currency` | `string` | Yes | Unset | Canonical Alpha currency ID from metadata `currency`, not a display symbol (required) |
| `--gas-mode` | `string` | No | `speed` | Trading mode: speed (smart) or custom |
| `--quote-id` | `string` | Yes | Unset | Quote ID from the quote command (required) |
| `--side` | `string` | Yes | Unset | Order side: buy or sell (required) |
| `--slippage` | `string` | Conditional | Unset | Slippage tolerance in percent, required when gas-mode=custom |

<a id="alpha.order.quote"></a>
### `gate-cli cex alpha order quote`

Operation ID: `alpha.order.quote`. Effect: **read**.

Calculate a private Alpha quote without placing an order

```text
gate-cli cex alpha order quote [flags]
```

API: `POST /api/v4/alpha/quote` (private).

Returns: [QuoteResponse](models/alpha.md#model-quoteresponse).

API request model(s), assembled by the command: [QuoteRequest](models/alpha.md#model-quoterequest). The CLI assembles this model from scalar flags; there is no raw JSON/body flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--amount` | `string` | Yes | Unset | Buy: USDT to spend; sell: base-token quantity (required) |
| `--currency` | `string` | Yes | Unset | Canonical Alpha currency ID from metadata `currency`, not a display symbol (required) |
| `--gas-mode` | `string` | No | `speed` | Trading mode: speed (smart) or custom |
| `--side` | `string` | Yes | Unset | Order side: buy or sell (required) |
| `--slippage` | `string` | Conditional | Unset | Slippage tolerance in percent (e.g. 10 for 10%), required when gas-mode=custom |

Read `error_type`: 0 is a successful quote, 1 exceeds the maximum and 2 is below the minimum. Verify the quote before using its ID. The SDK can omit `error_type` when it is zero; do not accept a response with a missing quote ID or unverifiable terms. `order_fee` has no explicit unit in this SDK. Verify its denomination and whether fees are included or charged separately before presenting an exact debit. Until deduction semantics are established, amount plus estimated fees is only a conservative funding reserve. A hard total-spending cap requires verified fee semantics.

## Verification and recovery

Keep the returned order ID and use `alpha.order.get`; use bounded `alpha.order.list` only when an ID is unavailable. Status 1 is processing, 2 successful, 3 failed, 4 cancelled, 5 buy placed but transfer incomplete, and 6 cancelled but transfer incomplete. Status 0 is the list filter for all, not a completion state. A placed order or transaction hash does not by itself prove transfer completion. Check the matched order, Alpha balances and account book as applicable; never claim a unique match from similar amount/time alone.

Do not replay `place` after a timeout, missing ID or truncated response. Quote IDs are not a documented idempotency guarantee. Retain an unknown outcome until uniquely reconciled; this CLI cannot amend or cancel it. Do not route an Alpha cancellation to spot, a DEX wallet or a retired module.
