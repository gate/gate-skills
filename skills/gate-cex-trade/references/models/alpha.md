# Alpha request and response models

Read only the models linked by the selected action. Fields marked `?` use SDK JSON omission; this does not waive business requirements. Keep amounts as decimal strings and IDs exact. Response-only fields are not request inputs.

<a id="model-accountsresponse"></a>
### AccountsResponse

`currency?`: `string`; `available?`: `string`; `locked?`: `string`; `token_address?`: `string`; `chain?`: `string`.

<a id="model-accountbookresponse"></a>
### AccountBookResponse

`id?`: `int64`; `time?`: `int64`; `currency?`: `string`; `change?`: `string`; `balance?`: `string`.

Field semantics: `id` — Order ID.

<a id="model-alphacurrency"></a>
### AlphaCurrency

`currency?`: `string`; `name?`: `string`; `chain?`: `string`; `address?`: `string`; `amount_precision?`: `int32`; `precision?`: `int32`; `status?`: `int32`.

`status`: 1 normal trading, 2 suspended, 3 delisted. Read chain/address and quantity precision before selecting an asset.

<a id="model-alphaticker"></a>
### AlphaTicker

`currency?`: `string`; `last?`: `string`; `change?`: `string`; `volume?`: `string`; `market_cap?`: `string`.

`volume` is 24-hour volume in USDT; `change` is the percentage change, such as -7.45.

<a id="model-tokens"></a>
### Tokens

`currency?`: `string`; `name?`: `string`; `chain?`: `string`; `address?`: `string`; `amount_precision?`: `int32`; `precision?`: `int32`; `status?`: `int32`.

`status`: 1 normal trading, 2 suspended, 3 delisted. Read chain/address and quantity precision before selecting an asset.

<a id="model-quoterequest"></a>
### QuoteRequest

`currency`: `string`; `side`: `string`; `amount`: `string`; `gas_mode`: `string`; `slippage?`: `string`.

`side` is `buy` or `sell`. Buy `amount` spends USDT; sell `amount` is base-token quantity. `gas_mode` is `speed` or `custom`; custom requires `slippage`, expressed as a percentage (`10` = 10%).

<a id="model-quoteresponse"></a>
### QuoteResponse

`quote_id?`: `string`; `min_amount?`: `string`; `max_amount?`: `string`; `price?`: `string`; `slippage?`: `string`; `estimate_gas_fee_amount_usdt?`: `string`; `order_fee?`: `string`; `target_token_min_amount?`: `string`; `target_token_max_amount?`: `string`; `error_type?`: `int32`.

A nonempty `quote_id` is usable for one minute. `error_type`: 0 success, 1 above maximum, 2 below minimum; zero may be omitted by the SDK. Price and estimated gas fee are USDT-based. The unit of `order_fee` is not specified here; do not assume it. Check the received range and amount limits before placement.

<a id="model-placeorderrequest"></a>
### PlaceOrderRequest

`currency`: `string`; `side`: `string`; `amount`: `string`; `gas_mode`: `string`; `slippage?`: `string`; `quote_id`: `string`.

`side` is `buy` or `sell`. Buy `amount` spends USDT; sell `amount` is base-token quantity. `gas_mode` is `speed` or `custom`; custom requires `slippage`, expressed as a percentage (`10` = 10%).

<a id="model-placeorderresponse"></a>
### PlaceOrderResponse

`order_id?`: `string`; `status?`: `int32`; `side?`: `string`; `gas_mode?`: `string`; `create_time?`: `int64`; `amount?`: `string`; `token_address?`: `string`; `chain?`: `string`.

`status`: 1 processing, 2 successful, 3 failed, 4 cancelled, 5 buy placed but transfer incomplete, 6 cancelled but transfer incomplete; 0 denotes the all-status filter, not completion. Buy `amount` is USDT spending; sell `amount` is base-token quantity.

<a id="model-orderresponse"></a>
### OrderResponse

`order_id?`: `string`; `tx_hash?`: `string`; `side?`: `string`; `usdt_amount?`: `string`; `currency?`: `string`; `currency_amount?`: `string`; `status?`: `int32`; `gas_mode?`: `string`; `chain?`: `string`; `gas_fee?`: `string`; `transaction_fee?`: `string`; `failed_reason?`: `string`; `create_time?`: `int64`.

`side` is `buy` or `sell`. `usdt_amount`, `gas_fee` and `transaction_fee` are USDT-based; `currency_amount` is the token quantity. Status meanings are the same as PlaceOrderResponse. A transaction hash does not alone prove completion.
