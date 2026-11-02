# Spot trading Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-batchamenditem"></a>
### BatchAmendItem

`order_id`: `string`; `currency_pair`: `string`; `account?`: `string`; `amount?`: `string`; `price?`: `string`; `amend_text?`: `string`; `action_mode?`: `string`; `stop_profit`: *[SpotOrderStopProfit](#model-spotorderstopprofit); `stop_loss`: *[SpotOrderStopLoss](#model-spotorderstoploss).

<a id="model-batchorder"></a>
### BatchOrder

`order_id?`: `string`; `amend_text?`: `string`; `text?`: `string`; `succeeded?`: `bool`; `label?`: `string`; `message?`: `string`; `id?`: `string`; `create_time?`: `string`; `update_time?`: `string`; `create_time_ms?`: `int64`; `update_time_ms?`: `int64`; `status?`: `string`; `currency_pair?`: `string`; `type?`: `string`; `account?`: `string`; `side?`: `string`; `amount?`: `string`; `price?`: `string`; `time_in_force?`: `string`; `iceberg?`: `string`; `auto_borrow?`: `bool`; `auto_repay?`: `bool`; `left?`: `string`; `filled_amount?`: `string`; `fill_price?`: `string`; `filled_total?`: `string`; `avg_deal_price?`: `string`; `fee?`: `string`; `fee_currency?`: `string`; `point_fee?`: `string`; `gt_fee?`: `string`; `gt_discount?`: `bool`; `rebated_fee?`: `string`; `rebated_fee_currency?`: `string`; `stp_id?`: `int32`; `stp_act?`: `string`; `finish_as?`: `string`; `slippage?`: `string`; `stop_profit?`: [PatchSpotOrderStopProfit](#model-patchspotorderstopprofit); `stop_loss?`: [PatchSpotOrderStopLoss](#model-patchspotorderstoploss).

Field semantics: `id` — Order ID; `create_time_ms` — Creation time of order (in milliseconds); `update_time_ms` — Last modification time of order (in milliseconds); `status` — Order status - `open`: to be filled - `closed`: closed order - `cancelled`: cancelled; `side` — Buy or sell order; `time_in_force` — Time in force - gtc: GoodTillCancelled - ioc: ImmediateOrCancelled, taker only - poc: PendingOrCancelled, makes a post-only order that always enjoys a maker fee - fok: FillOrKill, fill either completely or none; `finish_as` — How the order finished: - open: Pending processing - filled: Fully filled - cancelled: Cancelled by user - liquidate_cancelled: Cancelled by liquidation - small: Order size too small - depth_not_enough: Cancelled due to insufficient order book depth - trader_not_enough: Cancelled due to insufficient counterparty liquidity - ioc: Not filled immediately because time-in-force is IOC - poc: Post-only requirement not met because time-in-force is set to poc (maker-only); rejected after being detected as taker - fok: Not fully filled immediately because time-in-force is FOK - stp: Cancelled due to self-trade prevention - price_protect_cancelled: Cancelled due to price protection - unknown: Unknown.

<a id="model-cancelbatchorder"></a>
### CancelBatchOrder

`currency_pair`: `string`; `id`: `string`; `account?`: `string`; `action_mode?`: `string`.

Field semantics: `id` — Order ID or user custom ID. Custom ID are accepted only within 30 minutes after order creation.

<a id="model-cancelorderresult"></a>
### CancelOrderResult

`currency_pair?`: `string`; `id?`: `string`; `text?`: `string`; `succeeded?`: `bool`; `label?`: `string`; `message?`: `string`; `account?`: `string`.

Field semantics: `id` — Order ID.

<a id="model-countdowncancelallspottask"></a>
### CountdownCancelAllSpotTask

`timeout`: `int32`; `currency_pair?`: `string`.

Field semantics: `timeout` — Countdown time in seconds At least 5 seconds, 0 means cancel countdown.

<a id="model-openorders"></a>
### OpenOrders

`currency_pair?`: `string`; `total?`: `int32`; `orders?`: [][Order](#model-order).

<a id="model-order"></a>
### Order

`id?`: `string`; `text?`: `string`; `amend_text?`: `string`; `create_time?`: `string`; `update_time?`: `string`; `create_time_ms?`: `int64`; `update_time_ms?`: `int64`; `status?`: `string`; `currency_pair`: `string`; `trade_quote?`: `string`; `type?`: `string`; `account?`: `string`; `side`: `string`; `amount`: `string`; `price?`: `string`; `time_in_force?`: `string`; `iceberg?`: `string`; `auto_borrow?`: `bool`; `auto_repay?`: `bool`; `left?`: `string`; `filled_amount?`: `string`; `fill_price?`: `string`; `filled_total?`: `string`; `avg_deal_price?`: `string`; `fee?`: `string`; `fee_currency?`: `string`; `point_fee?`: `string`; `gt_fee?`: `string`; `gt_maker_fee?`: `string`; `gt_taker_fee?`: `string`; `gt_discount?`: `bool`; `rebated_fee?`: `string`; `rebated_fee_currency?`: `string`; `stp_id?`: `int32`; `stp_act?`: `string`; `finish_as?`: `string`; `action_mode?`: `string`; `slippage?`: `string`; `stop_profit`: *[SpotOrderStopProfit](#model-spotorderstopprofit); `stop_loss`: *[SpotOrderStopLoss](#model-spotorderstoploss).

Field semantics: `id` — Order ID; `create_time_ms` — Creation time of order (in milliseconds); `update_time_ms` — Last modification time of order (in milliseconds); `status` — Order status - `open`: to be filled - `closed`: closed order - `cancelled`: cancelled; `side` — Buy or sell order; `amount` — Trade amount When `type` is `limit`, this is the base currency to trade (the currency being bought or sold), e.g. `BTC` in `BTC_USDT`. When `type` is `market`, the meaning depends on the side: - `side`: `buy` refers to the quote currency, e.g. `USDT` in `BTC_USDT` - `side`: `sell` refers to the base currency, e.g. `BTC` in `BTC_USDT`; `time_in_force` — Time in force - gtc: GoodTillCancelled - ioc: ImmediateOrCancelled, taker only - poc: PendingOrCancelled, makes a post-only order that always enjoys a maker fee - fok: FillOrKill, fill either completely or none Only `ioc` and `fok` are supported when `type`=`market`; `finish_as` — How the order finished: - open: Pending processing - filled: Fully filled - cancelled: Cancelled by user - liquidate_cancelled: Cancelled by liquidation - small: Order size too small - depth_not_enough: Cancelled due to insufficient order book depth - trader_not_enough: Cancelled due to insufficient counterparty liquidity - ioc: Not filled immediately because time-in-force is IOC - poc: Post-only requirement not met because time-in-force is set to poc (maker-only); rejected after being detected as taker - fok: Not fully filled immediately because time-in-force is FOK - stp: Cancelled due to self-trade prevention - price_protect_cancelled: Cancelled due to price protection - unknown: Unknown.

<a id="model-ordercancel"></a>
### OrderCancel

`id?`: `string`; `text?`: `string`; `amend_text?`: `string`; `succeeded?`: `bool`; `label?`: `string`; `message?`: `string`; `create_time?`: `string`; `update_time?`: `string`; `create_time_ms?`: `int64`; `update_time_ms?`: `int64`; `status?`: `string`; `currency_pair`: `string`; `type?`: `string`; `account?`: `string`; `side`: `string`; `amount`: `string`; `price?`: `string`; `time_in_force?`: `string`; `iceberg?`: `string`; `auto_borrow?`: `bool`; `auto_repay?`: `bool`; `left?`: `string`; `filled_amount?`: `string`; `fill_price?`: `string`; `filled_total?`: `string`; `avg_deal_price?`: `string`; `fee?`: `string`; `fee_currency?`: `string`; `point_fee?`: `string`; `gt_fee?`: `string`; `gt_maker_fee?`: `string`; `gt_taker_fee?`: `string`; `gt_discount?`: `bool`; `rebated_fee?`: `string`; `rebated_fee_currency?`: `string`; `stp_id?`: `int32`; `stp_act?`: `string`; `finish_as?`: `string`; `action_mode?`: `string`.

Field semantics: `id` — Order ID; `create_time_ms` — Creation time of order (in milliseconds); `update_time_ms` — Last modification time of order (in milliseconds); `status` — Order status - `open`: to be filled - `closed`: closed order - `cancelled`: cancelled; `side` — Buy or sell order; `amount` — Trading quantity When `type` is `limit`, it refers to the base currency (the currency being traded), such as `BTC` in `BTC_USDT` When `type` is `market`, it refers to different currencies based on the side: - `side`: `buy` refers to quote currency, `BTC_USDT` means `USDT` - `side`: `sell` refers to base currency, `BTC_USDT` means `BTC`; `time_in_force` — Time in force - gtc: GoodTillCancelled - ioc: ImmediateOrCancelled, taker only - poc: PendingOrCancelled, makes a post-only order that always enjoys a maker fee - fok: FillOrKill, fill either completely or none Only `ioc` and `fok` are supported when `type`=`market`; `finish_as` — How the order was finished. - open: processing - filled: filled totally - cancelled: manually cancelled - ioc: time in force is `IOC`, finish immediately - stp: cancelled because self trade prevention.

<a id="model-orderpatch"></a>
### OrderPatch

`currency_pair?`: `string`; `account?`: `string`; `amount?`: `string`; `price?`: `string`; `amend_text?`: `string`; `action_mode?`: `string`; `stop_profit`: *[SpotOrderStopProfit](#model-spotorderstopprofit); `stop_loss`: *[SpotOrderStopLoss](#model-spotorderstoploss).

<a id="model-patchspotorderstoploss"></a>
### PatchSpotOrderStopLoss

`trigger_price?`: `string`; `order_price?`: `string`.

<a id="model-patchspotorderstopprofit"></a>
### PatchSpotOrderStopProfit

`trigger_price?`: `string`; `order_price?`: `string`.

<a id="model-spotaccount"></a>
### SpotAccount

`currency?`: `string`; `available?`: `string`; `locked?`: `string`; `update_id?`: `int64`.

<a id="model-spotaccountbook"></a>
### SpotAccountBook

`id?`: `string`; `time?`: `int64`; `currency?`: `string`; `change?`: `string`; `balance?`: `string`; `type?`: `string`; `code?`: `string`; `text?`: `string`.

Field semantics: `time` — The timestamp of the change (in milliseconds).

<a id="model-spotorderstoploss"></a>
### SpotOrderStopLoss

`trigger_price?`: `string`; `order_price?`: `string`.

<a id="model-spotorderstopprofit"></a>
### SpotOrderStopProfit

`trigger_price?`: `string`; `order_price?`: `string`.

<a id="model-spotpriceputorder"></a>
### SpotPricePutOrder

`type?`: `string`; `side`: `string`; `price`: `string`; `amount`: `string`; `account`: `string`; `time_in_force`: `string`; `auto_borrow?`: `bool`; `auto_repay?`: `bool`; `text?`: `string`.

Field semantics: `side` — Order side - buy: buy side - sell: sell side; `amount` — Trading quantity, refers to the trading quantity of the trading currency, i.e., the currency that needs to be traded, for example, the quantity of BTC in BTC_USDT.; `time_in_force` — time_in_force - gtc: GoodTillCancelled - ioc: ImmediateOrCancelled, taker only.

<a id="model-spotpricetrigger"></a>
### SpotPriceTrigger

`price`: `string`; `rule`: `string`; `expiration?`: `int32`.

<a id="model-spotpricetriggeredorder"></a>
### SpotPriceTriggeredOrder

`trigger`: [SpotPriceTrigger](#model-spotpricetrigger); `put`: [SpotPricePutOrder](#model-spotpriceputorder); `id?`: `int64`; `user?`: `int32`; `market`: `string`; `ctime?`: `int64`; `ftime?`: `int64`; `fired_order_id?`: `int64`; `status?`: `string`; `reason?`: `string`.

Field semantics: `id` — Auto order ID; `status` — Status - open: Running - cancelled: Manually cancelled - finish: Successfully completed - failed: Failed to execute - expired: Expired.

<a id="model-trade"></a>
### Trade

`id?`: `string`; `create_time?`: `string`; `create_time_ms?`: `string`; `currency_pair?`: `string`; `side?`: `string`; `role?`: `string`; `amount?`: `string`; `price?`: `string`; `order_id?`: `string`; `fee?`: `string`; `fee_currency?`: `string`; `point_fee?`: `string`; `gt_fee?`: `string`; `amend_text?`: `string`; `sequence_id?`: `string`; `text?`: `string`; `deal?`: `string`; `trade_quote?`: `string`.

Field semantics: `create_time_ms` — Trading time, with millisecond precision; `side` — Buy or sell order.

<a id="model-triggerorderresponse"></a>
### TriggerOrderResponse

`id?`: `int64`; `id_string?`: `string`.

Field semantics: `id` — Auto order ID.

<a id="model-triggertime"></a>
### TriggerTime

`triggerTime?`: `int64`.
