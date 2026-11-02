# Dual investment Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-dualgetbalance"></a>
### DualGetBalance

`user_asset_usdt?`: `string`; `user_asset_btc?`: `string`; `user_total_interest_usdt?`: `string`; `user_total_interest_btc?`: `string`.

<a id="model-dualgetorders"></a>
### DualGetOrders

`id?`: `int32`; `plan_id?`: `int32`; `invest_amount?`: `string`; `settlement_amount?`: `string`; `create_time?`: `int32`; `complete_time?`: `int32`; `status?`: `string`; `invest_currency?`: `string`; `exercise_currency?`: `string`; `exercise_price?`: `string`; `settlement_price?`: `string`; `settlement_currency?`: `string`; `apy_display?`: `string`; `apy_settlement?`: `string`; `delivery_time?`: `int32`; `text?`: `string`.

Field semantics: `id` — Order ID; `status` — Status: `INIT`-Created `SETTLEMENT_SUCCESS`-Settlement Success `SETTLEMENT_PROCESSING`-Settlement Processing `CANCELED`-Canceled `FAILED`-Failed.

## User-facing field mapping

For a plan, present the subscription asset, settlement/exercise asset, exercise
price, delivery time, minimum subscription amount, and estimated annual rate.
For an order, present the subscribed amount, settlement amount when available,
delivery time, and a translated state: created, settlement in progress, settled,
cancelled, or failed. `apy_display` is an estimated annual rate and
`apy_settlement` is the realised settlement rate; neither is a promised return.
Do not show `id`, `plan_id`, raw status values, `text`, or raw timestamps unless a
user explicitly requests a technical receipt or support reference.

<a id="model-dualgetplans"></a>
### DualGetPlans

`id?`: `int32`; `instrument_name?`: `string`; `type?`: `string`; `invest_currency?`: `string`; `exercise_currency?`: `string`; `exercise_price?`: `float64`; `delivery_time?`: `int32`; `apy_display?`: `string`; `min_amount?`: `string`; `start_time?`: `int32`; `end_time?`: `int32`; `status?`: `string`.

Field semantics: `status` — Status: `NOTSTARTED` - Not started `ONGOING` - In progress `ENDED` - Ended.

<a id="model-dualmodifyorderreinvestparams"></a>
### DualModifyOrderReinvestParams

`order_id?`: `int64`; `status?`: `int32`; `effective_time_duration?`: `int64`.

Field semantics: `effective_time_duration` — Effective duration in seconds; default 1 day (86400).

<a id="model-placedualinvestmentorder"></a>
### PlaceDualInvestmentOrder

`id?`: `int32`; `plan_id?`: `int32`; `invest_amount?`: `string`; `settlement_amount?`: `string`; `create_time?`: `int32`; `complete_time?`: `int32`; `status?`: `string`; `invest_currency?`: `string`; `exercise_currency?`: `string`; `exercise_price?`: `string`; `settlement_price?`: `string`; `settlement_currency?`: `string`; `apy_display?`: `string`; `apy_settlement?`: `string`; `delivery_time?`: `int32`; `text?`: `string`.

Field semantics: `id` — Order ID; `status` — Status: `INIT`-Created `SETTLEMENT_SUCCESS`-Settlement Success `SETTLEMENT_PROCESSING`-Settlement Processing `CANCELED`-Canceled `FAILED`-Failed.

<a id="model-placedualinvestmentorderparams"></a>
### PlaceDualInvestmentOrderParams

`plan_id`: `string`; `amount`: `string`; `text?`: `string`.
