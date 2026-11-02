# Gate Flash Swap

Supplementary product background. Use the [canonical command contract](convert-commands.md) for registered leaves, exact flags, units and safety variants, and [runtime rules](runtime.md) for execution. API fields in this file do not authorize direct private API calls or imply matching CLI flags.

## Scope

Flash Swap quote, preview, acceptance, status, and history. It is an instant conversion flow; it is not a limit Convert order and does not use ordinary spot order semantics.

## Protocol matrix

Gate API v4 is authoritative for the endpoint and field names. The one-to-one contract is documented below. Multi-currency support is a distinct protocol: keep its `params[]` body and per-leg response data, and block writes if the current API v4 page and installed adapter disagree about the endpoint or response contract.

| Protocol | Preview request | Create request | Identifier and expiry | Boundary |
| --- | --- | --- | --- | --- |
| One-to-one | `POST /flash_swap/orders/preview` with `sell_currency`, `buy_currency`, and exactly one of `sell_amount` or `buy_amount` | `POST /flash_swap/orders` with `preview_id`, both currencies, and the exact preview amounts | One `preview_id`; use any returned expiry/validity data | The standard API v4 flow. |
| One-to-one v1 | `GET /flash_swap/orders/preview_v1` with explicit `sell_asset`, `buy_asset`, and one amount | `POST /flash_swap/orders_v1` with the v1 JSON schema returned by the selected API | Use only the ID and validity fields returned by v1 | Check installed protocol-specific CLI support, actual SDK mapping and service eligibility. Do not pass the standard body to v1. |
| Multi one-to-many | Protocol-specific preview body: `{"params":[{"sell_asset":"…","sell_amount":"…","buy_asset":"…","buy_amount":"…"}, …]}`; each leg supplies only the amount required by the selected direction | Protocol-specific create body with the same `params[]` legs and the exact amounts/metadata returned by preview | Do not require a top-level `preview_id`. A preview response may return `quote_id` and `valid_timestamp` per leg; use them only when the current API v4 schema requires them | Check installed protocol-specific CLI support, actual SDK mapping and service eligibility. |
| Multi many-to-one | Same `params[]` shape with one source leg per input asset and the target amount on the destination leg | Same protocol-specific `params[]` shape, preserving every source leg and the target amount | Reconcile every returned leg/order and balance; no implicit single preview ID | Check installed protocol-specific CLI support, actual SDK mapping and service eligibility. |

The multi-currency body is not a standard one-to-one body. Never collapse a list of legs into `sell_currency`, `buy_currency`, and one `preview_id`; never invent a top-level ID when the selected multi protocol does not define one. If the API v4 documentation omits or conflicts with the multi endpoint, report the compatibility blocker and do not write. When multi-currency is blocked, do not split it into multiple one-to-one swaps or claim that the result is equivalent; return the unavailable-operation toast and wait for a separately requested one-to-one operation.

## API / CLI index

| Scenario | Endpoint / method | Required inputs | CLI |
| --- | --- | --- | --- |
| Supported pairs | `GET /flash_swap/currency_pairs` | none | `gate-cli cex flash-swap pairs` |
| One-to-one preview | `POST /flash_swap/orders/preview` | sell/buy currency and one amount | `gate-cli cex flash-swap preview` |
| One-to-one create | `POST /flash_swap/orders` | preview ID, currencies, exact preview amounts | `gate-cli cex flash-swap create` |
| One-to-one v1 preview/create | `GET /flash_swap/orders/preview_v1`, `POST /flash_swap/orders_v1` | v1 asset/amount fields and v1 JSON body | `gate-cli cex flash-swap preview-v1`, `create-v1 --json`; check the installed leaf, protocol-specific JSON and actual SDK request; diagnostic labels are not wire paths |
| Multi one-to-many preview/create | `POST /flash_swap/multi_currency/one_to_many/preview`, `POST /flash_swap/multi_currency/one_to_many` | `params[]` legs | `gate-cli cex flash-swap preview-one-to-many --json`, `create-one-to-many --json`; check the installed leaf, protocol-specific JSON and actual SDK request; diagnostic labels are not wire paths |
| Multi many-to-one preview/create | `POST /flash_swap/multi_currency/many_to_one/preview`, `POST /flash_swap/multi_currency/many_to_one` | `params[]` legs | `gate-cli cex flash-swap preview-many-to-one --json`, `create-many-to-one --json`; check the installed leaf, protocol-specific JSON and actual SDK request; diagnostic labels are not wire paths |
| Order status/history | `GET /flash_swap/orders` | status/currency filters | `gate-cli cex flash-swap orders` |
| Order detail | `GET /flash_swap/orders/{order_id}` | order ID | `gate-cli cex flash-swap order` |

## Workflow

1. Read supported pairs and limits.
2. Select one protocol family. For one-to-one, request a fresh preview and show its `preview_id`, quote, amounts, and expiry. For multi-currency, validate the `params[]` legs and show per-leg quote/validity data returned by that protocol.
3. Confirm the complete unchanged payload once. Do not reuse a one-to-one confirmation for a multi-currency payload.
4. Submit the matching create operation. Preserve every currency and amount from the preview; never translate multi-currency legs into a standard `preview_id` body.
5. Query conversion order/status and all affected balances. For multi-currency, reconcile each returned leg/order and report partial or per-leg failure separately.

## Enums and constraints

- Standard Flash Swap status: `1` success, `2` failed. Keep the raw status and response message in the report.
- Quote expiry is protocol-specific. Reject a stale one-to-one preview or any multi-leg quote whose returned validity has passed; do not retry a stale write.
- Common blocks: pair unsupported, amount outside limits, missing/ambiguous multi endpoint, quote expired, balance changed, duplicate acceptance, or verified CLI/SDK request or response-contract mismatch. Validate every multi-currency leg against its pair limit before attributing a failure to the route. The canonical contract contains standard, v1 and multi-currency leaves. Check the requested installed leaf and its own protocol; no package-wide prohibition follows from an old error label. Source support does not prove online availability. A missing required field, actual protocol mismatch or unavailable service stops that operation; never issue a speculative write to probe availability.
- Small-balance conversion is a separate wallet feature, not Flash Swap.

Any expired quote, failed acceptance, compatibility blocker, or balance error must use the two-line toast in `workflows.md`.
