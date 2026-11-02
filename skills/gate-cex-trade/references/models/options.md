# Options trading Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-amendoptionsorderrequest"></a>
### AmendOptionsOrderRequest

`contract`: `string`; `price`: `string`; `size`: `int64`.

<a id="model-countdowncancelalloptionstask"></a>
### CountdownCancelAllOptionsTask

`timeout`: `int32`; `contract?`: `string`; `underlying?`: `string`.

Field semantics: `timeout` — Countdown time in seconds At least 5 seconds, 0 means cancel countdown.

<a id="model-optionsaccount"></a>
### OptionsAccount

`user?`: `int64`; `total?`: `string`; `position_value?`: `string`; `equity?`: `string`; `short_enabled?`: `bool`; `mmp_enabled?`: `bool`; `liq_triggered?`: `bool`; `margin_mode?`: `int32`; `unrealised_pnl?`: `string`; `init_margin?`: `string`; `maint_margin?`: `string`; `order_margin?`: `string`; `ask_order_margin?`: `string`; `bid_order_margin?`: `string`; `available?`: `string`; `point?`: `string`; `currency?`: `string`; `orders_limit?`: `int32`; `position_notional_limit?`: `int64`.

<a id="model-optionsaccountbook"></a>
### OptionsAccountBook

`time?`: `float64`; `change?`: `string`; `balance?`: `string`; `type?`: `string`; `text?`: `string`.

<a id="model-optionsmmp"></a>
### OptionsMmp

`underlying`: `string`; `window`: `int32`; `frozen_period`: `int32`; `qty_limit`: `string`; `delta_limit`: `string`; `trigger_time_ms?`: `int64`; `frozen_until_ms?`: `int64`.

Field semantics: `trigger_time_ms` — Trigger freeze time (milliseconds), 0 means no freeze is triggered.

<a id="model-optionsmmpreset"></a>
### OptionsMmpReset

`underlying`: `string`; `window?`: `int32`; `frozen_period?`: `int32`; `qty_limit?`: `string`; `delta_limit?`: `string`; `trigger_time_ms?`: `int64`; `frozen_until_ms?`: `int64`.

Field semantics: `trigger_time_ms` — Trigger freeze time (milliseconds), 0 means no freeze is triggered.

<a id="model-optionsmysettlements"></a>
### OptionsMySettlements

`time?`: `float64`; `underlying?`: `string`; `contract?`: `string`; `strike_price?`: `string`; `settle_price?`: `string`; `size?`: `int64`; `settle_profit?`: `string`; `fee?`: `string`; `realised_pnl?`: `string`.

<a id="model-optionsmytrade"></a>
### OptionsMyTrade

`id?`: `int64`; `create_time?`: `float64`; `contract?`: `string`; `order_id?`: `int32`; `size?`: `int64`; `price?`: `string`; `underlying_price?`: `string`; `role?`: `string`.

<a id="model-optionsorder"></a>
### OptionsOrder

`id?`: `int64`; `user?`: `int32`; `create_time?`: `float64`; `finish_time?`: `float64`; `finish_as?`: `string`; `status?`: `string`; `contract`: `string`; `size`: `int64`; `iceberg?`: `int64`; `price?`: `string`; `close?`: `bool`; `is_close?`: `bool`; `reduce_only?`: `bool`; `is_reduce_only?`: `bool`; `is_liq?`: `bool`; `mmp?`: `bool`; `is_mmp?`: `bool`; `tif?`: `string`; `left?`: `int64`; `fill_price?`: `string`; `text?`: `string`; `tkfr?`: `string`; `mkfr?`: `string`; `refu?`: `int32`; `refr?`: `string`.

Field semantics: `id` — Options order ID; `finish_as` — Order finish reason: - filled: Fully filled - cancelled: User cancelled - liquidated: Cancelled due to liquidation - ioc: Not immediately fully filled due to IOC time-in-force setting - auto_deleveraged: Cancelled due to auto-deleveraging - reduce_only: Cancelled due to position increase while reduce-only is set - position_closed: Cancelled because the position was closed - reduce_out: Only reduce positions by excluding hard-to-fill orders - mmp_cancelled: Cancelled by MMP; `status` — Order status - `open`: Pending - `finished`: Completed; `size` — Required. Trading quantity. Positive for buy, negative for sell. Set to 0 for close position orders..

<a id="model-optionsposition"></a>
### OptionsPosition

`user?`: `int32`; `underlying?`: `string`; `underlying_price?`: `string`; `contract?`: `string`; `size?`: `int64`; `entry_price?`: `string`; `mark_price?`: `string`; `mark_iv?`: `string`; `realised_pnl?`: `string`; `unrealised_pnl?`: `string`; `pending_orders?`: `int32`; `close_order?`: *[OptionsPositionCloseOrder](#model-optionspositioncloseorder); `delta?`: `string`; `gamma?`: `string`; `vega?`: `string`; `theta?`: `string`.

Field semantics: `size` — Position size (contract quantity).

<a id="model-optionspositionclose"></a>
### OptionsPositionClose

`time?`: `float64`; `contract?`: `string`; `side?`: `string`; `pnl?`: `string`; `text?`: `string`; `settle_size?`: `string`.

Field semantics: `side` — Position side - `long`: Long position - `short`: Short position.

<a id="model-optionspositioncloseorder"></a>
### OptionsPositionCloseOrder

`id?`: `int64`; `price?`: `string`; `is_liq?`: `bool`.

Field semantics: `id` — Order ID.

<a id="model-triggertime"></a>
### TriggerTime

`triggerTime?`: `int64`.
