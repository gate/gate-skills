# Perpetual futures Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-batchamendorderreq"></a>
### BatchAmendOrderReq

`order_id?`: `int64`; `text?`: `string`; `size?`: `string`; `price?`: `string`; `amend_text?`: `string`; `action_mode?`: `string`.

<a id="model-batchfuturesorder"></a>
### BatchFuturesOrder

`succeeded?`: `bool`; `label?`: `string`; `detail?`: `string`; `id?`: `int64`; `user?`: `int32`; `create_time?`: `float64`; `finish_time?`: `float64`; `finish_as?`: `string`; `status?`: `string`; `contract?`: `string`; `size?`: `string`; `iceberg?`: `string`; `price?`: `string`; `close?`: `bool`; `is_close?`: `bool`; `reduce_only?`: `bool`; `is_reduce_only?`: `bool`; `is_liq?`: `bool`; `tif?`: `string`; `left?`: `string`; `fill_price?`: `string`; `text?`: `string`; `tkfr?`: `string`; `mkfr?`: `string`; `refu?`: `int32`; `auto_size?`: `string`; `stp_act?`: `string`; `stp_id?`: `int32`; `market_order_slip_ratio?`: `string`.

Field semantics: `id` — Futures order ID; `finish_as` — How the order was finished: - filled: all filled - cancelled: manually cancelled - liquidated: cancelled because of liquidation - ioc: time in force is `IOC`, finish immediately - auto_deleveraged: finished by ADL - reduce_only: cancelled because of increasing position while `reduce-only` set - position_closed: cancelled because the position was closed - reduce_out: only reduce positions by excluding hard-to-fill orders - stp: cancelled because self trade prevention; `status` — Order status - `open`: Pending - `finished`: Completed; `size` — Required. Trading quantity. Positive for buy, negative for sell. Set to 0 for close position orders..

<a id="model-countdowncancelallfuturestask"></a>
### CountdownCancelAllFuturesTask

`timeout`: `int32`; `contract?`: `string`.

Field semantics: `timeout` — Countdown time in seconds At least 5 seconds, 0 means cancel countdown.

<a id="model-createtrailorder"></a>
### CreateTrailOrder

`contract`: `string`; `amount`: `string`; `activation_price?`: `string`; `is_gte?`: `bool`; `price_type?`: `int32`; `price_offset?`: `string`; `reduce_only?`: `bool`; `position_related?`: `bool`; `text?`: `string`; `pos_margin_mode?`: `string`; `position_mode?`: `string`.

Field semantics: `amount` — Trading quantity in contracts, positive for buy, negative for sell; `price_type` — Activation price type: 1-latest price, 2-index price, 3-mark price; `position_mode` — Position mode: single, dual, and dual_plus.

<a id="model-createtrailorderresponse"></a>
### CreateTrailOrderResponse

`code?`: `int32`; `message?`: `string`; `data?`: [CreateTrailOrderResult](#model-createtrailorderresult); `timestamp?`: `int64`.

Field semantics: `timestamp` — Response timestamp (milliseconds).

<a id="model-createtrailorderresult"></a>
### CreateTrailOrderResult

`id?`: `string`.

Field semantics: `id` — Order ID.

<a id="model-futurecancelorderresult"></a>
### FutureCancelOrderResult

`id?`: `string`; `user_id?`: `int64`; `succeeded?`: `bool`; `message?`: `string`.

Field semantics: `id` — Order ID.

<a id="model-futuresaccount"></a>
### FuturesAccount

`total?`: `string`; `unrealised_pnl?`: `string`; `position_margin?`: `string`; `order_margin?`: `string`; `available?`: `string`; `point?`: `string`; `currency?`: `string`; `in_dual_mode?`: `bool`; `enable_credit?`: `bool`; `position_initial_margin?`: `string`; `maintenance_margin?`: `string`; `bonus?`: `string`; `enable_evolved_classic?`: `bool`; `cross_order_margin?`: `string`; `cross_initial_margin?`: `string`; `cross_maintenance_margin?`: `string`; `cross_unrealised_pnl?`: `string`; `cross_available?`: `string`; `cross_margin_balance?`: `string`; `cross_mmr?`: `string`; `cross_imr?`: `string`; `isolated_position_margin?`: `string`; `enable_new_dual_mode?`: `bool`; `margin_mode?`: `int32`; `enable_tiered_mm?`: `bool`; `enable_dual_plus?`: `bool`; `position_mode?`: `string`; `history?`: [FuturesAccountHistory](#model-futuresaccounthistory).

<a id="model-futuresaccountbook"></a>
### FuturesAccountBook

`time?`: `float64`; `change?`: `string`; `balance?`: `string`; `type?`: `string`; `text?`: `string`; `contract?`: `string`; `trade_id?`: `string`; `id?`: `string`.

<a id="model-futuresaccounthistory"></a>
### FuturesAccountHistory

`dnw?`: `string`; `pnl?`: `string`; `fee?`: `string`; `refr?`: `string`; `fund?`: `string`; `point_dnw?`: `string`; `point_fee?`: `string`; `point_refr?`: `string`; `bonus_dnw?`: `string`; `bonus_offset?`: `string`; `cross_settle?`: `string`.

<a id="model-futuresautodeleverage"></a>
### FuturesAutoDeleverage

`time?`: `int64`; `user?`: `int64`; `order_id?`: `int64`; `contract?`: `string`; `leverage?`: `string`; `cross_leverage_limit?`: `string`; `entry_price?`: `string`; `fill_price?`: `string`; `trade_size?`: `string`; `position_size?`: `string`.

<a id="model-futuresbboorder"></a>
### FuturesBboOrder

`contract`: `string`; `size`: `int64`; `direction`: `string`; `iceberg?`: `int64`; `level`: `int64`; `close?`: `bool`; `is_close?`: `bool`; `reduce_only?`: `bool`; `is_reduce_only?`: `bool`; `is_liq?`: `bool`; `tif?`: `string`; `left?`: `int64`; `fill_price?`: `string`; `text?`: `string`; `tkfr?`: `string`; `mkfr?`: `string`; `refu?`: `int32`; `auto_size?`: `string`; `stp_id?`: `int32`; `stp_act?`: `string`; `amend_text?`: `string`; `pid?`: `int64`.

Field semantics: `size` — Required. Trading quantity. Positive for buy, negative for sell. Set to 0 for close position orders..

<a id="model-futuresinitialorder"></a>
### FuturesInitialOrder

`contract`: `string`; `size?`: `int64`; `amount?`: `string`; `price`: `string`; `close?`: `bool`; `tif?`: `string`; `text?`: `string`; `reduce_only?`: `bool`; `auto_size?`: `string`; `is_reduce_only?`: `bool`; `is_close?`: `bool`.

Field semantics: `size` — Represents the number of contracts that need to be closed, full closing: size=0 Partial closing: plan-close-short-position size>0 Partial closing: plan-close-long-position size<0; `amount` — Same as `size`; used for decimal contract size. When both `size` and `amount` are provided, `amount` takes precedence..

<a id="model-futuresleverage"></a>
### FuturesLeverage

`Lever?`: `string`.

<a id="model-futuresliquidate"></a>
### FuturesLiquidate

`time?`: `int64`; `contract?`: `string`; `leverage?`: `string`; `size?`: `string`; `margin?`: `string`; `entry_price?`: `string`; `liq_price?`: `string`; `mark_price?`: `string`; `order_id?`: `int64`; `order_price?`: `string`; `fill_price?`: `string`; `left?`: `string`.

<a id="model-futuresorder"></a>
### FuturesOrder

`id?`: `int64`; `user?`: `int32`; `create_time?`: `float64`; `update_time?`: `float64`; `finish_time?`: `float64`; `finish_as?`: `string`; `status?`: `string`; `contract`: `string`; `size`: `string`; `iceberg?`: `string`; `price`: `string`; `close?`: `bool`; `is_close?`: `bool`; `reduce_only?`: `bool`; `is_reduce_only?`: `bool`; `is_liq?`: `bool`; `tif?`: `string`; `left?`: `string`; `fill_price?`: `string`; `text?`: `string`; `tkfr?`: `string`; `mkfr?`: `string`; `refu?`: `int32`; `auto_size?`: `string`; `stp_id?`: `int32`; `stp_act?`: `string`; `amend_text?`: `string`; `pid?`: `int64`; `market_order_slip_ratio?`: `string`; `pos_margin_mode?`: `string`; `action_mode?`: `string`; `tpsl_tp_trigger_price?`: `string`; `tpsl_sl_trigger_price?`: `string`; `tpsl_tp_bbo_type?`: `string`; `tpsl_sl_bbo_type?`: `string`.

Field semantics: `id` — Futures order ID; `finish_as` — How the order was finished: - filled: all filled - cancelled: manually cancelled - liquidated: cancelled because of liquidation - ioc: time in force is `IOC`, finish immediately - auto_deleveraged: finished by ADL - reduce_only: cancelled because of increasing position while `reduce-only` set - position_closed: cancelled because the position was closed - reduce_out: only reduce positions by excluding hard-to-fill orders - stp: cancelled because self trade prevention; `status` — Order status - `open`: Pending - `finished`: Completed; `size` — Required. Trading quantity. Positive for buy, negative for sell. Set to 0 for close position orders..

<a id="model-futuresorderamendment"></a>
### FuturesOrderAmendment

`size?`: `string`; `price?`: `string`; `amend_text?`: `string`; `text?`: `string`; `action_mode?`: `string`.

<a id="model-futuresordertimerange"></a>
### FuturesOrderTimerange

`id?`: `int64`; `user?`: `int32`; `create_time?`: `float64`; `update_time?`: `string`; `finish_time?`: `string`; `finish_as?`: `string`; `status?`: `string`; `contract`: `string`; `size`: `string`; `iceberg?`: `string`; `price`: `string`; `close?`: `bool`; `is_close?`: `bool`; `reduce_only?`: `bool`; `is_reduce_only?`: `bool`; `is_liq?`: `bool`; `tif?`: `string`; `left?`: `string`; `fill_price?`: `string`; `text?`: `string`; `tkfr?`: `string`; `mkfr?`: `string`; `refu?`: `int32`; `auto_size?`: `string`; `stp_id?`: `int32`; `stp_act?`: `string`; `amend_text?`: `string`; `pid?`: `int64`; `market_order_slip_ratio?`: `string`; `pos_margin_mode?`: `string`; `tpsl_tp_trigger_price?`: `string`; `tpsl_sl_trigger_price?`: `string`.

Field semantics: `id` — Futures order ID; `finish_as` — How the order was finished: - filled: all filled - cancelled: manually cancelled - liquidated: cancelled because of liquidation - ioc: time in force is `IOC`, finish immediately - auto_deleveraged: finished by ADL - reduce_only: cancelled because of increasing position while `reduce-only` set - position_closed: cancelled because the position was closed - reduce_out: only reduce positions by excluding hard-to-fill orders - stp: cancelled because self trade prevention; `status` — Order status - `open`: Pending - `finished`: Completed; `size` — Required. Trading quantity. Positive for buy, negative for sell. Set to 0 for close position orders..

<a id="model-futurespositioncrossmode"></a>
### FuturesPositionCrossMode

`mode`: `string`; `contract`: `string`.

<a id="model-futurespricetrigger"></a>
### FuturesPriceTrigger

`strategy_type?`: `int32`; `price_type?`: `int32`; `price`: `string`; `rule`: `int32`; `expiration?`: `int32`.

<a id="model-futurespricetriggeredorder"></a>
### FuturesPriceTriggeredOrder

`initial`: [FuturesInitialOrder](#model-futuresinitialorder); `trigger`: [FuturesPriceTrigger](#model-futurespricetrigger); `id?`: `int64`; `id_string?`: `string`; `user?`: `int32`; `create_time?`: `float64`; `finish_time?`: `float64`; `trade_id?`: `int64`; `status?`: `string`; `finish_as?`: `string`; `reason?`: `string`; `order_type?`: `string`; `me_order_id?`: `int64`; `pos_margin_mode?`: `string`.

Field semantics: `id` — Auto order ID; `status` — Order status - `open`: Active - `finished`: Finished - `inactive`: Inactive, only applies to order take-profit/stop-loss - `invalid`: Invalid, only applies to order take-profit/stop-loss; `finish_as` — Finish status: cancelled - Cancelled; succeeded - Succeeded; failed - Failed; expired - Expired.

<a id="model-futuresupdatepricetriggeredorder"></a>
### FuturesUpdatePriceTriggeredOrder

`settle?`: `string`; `order_id`: `int64`; `size?`: `int64`; `amount?`: `string`; `price?`: `string`; `trigger_price?`: `string`; `price_type?`: `int32`; `auto_size?`: `string`; `close?`: `bool`.

Field semantics: `size` — Modified Contract Quantity. Full Close: 0; Partial Close: Positive/Negative values indicate direction (consistent with the creation interface logic).; `amount` — Same as `size`; used for decimal contract size. When both `size` and `amount` are provided, `amount` takes precedence..

<a id="model-myfuturestrade"></a>
### MyFuturesTrade

`id?`: `int64`; `create_time?`: `float64`; `contract?`: `string`; `order_id?`: `string`; `size?`: `string`; `close_size?`: `string`; `price?`: `string`; `role?`: `string`; `text?`: `string`; `fee?`: `string`; `point_fee?`: `string`; `trade_value?`: `string`.

<a id="model-myfuturestradetimerange"></a>
### MyFuturesTradeTimeRange

`trade_id?`: `string`; `create_time?`: `float64`; `contract?`: `string`; `order_id?`: `string`; `size?`: `string`; `close_size?`: `string`; `price?`: `string`; `role?`: `string`; `text?`: `string`; `fee?`: `string`; `point_fee?`: `string`.

<a id="model-position"></a>
### Position

`user?`: `int64`; `contract?`: `string`; `size?`: `string`; `hedge_status?`: `string`; `hedged_size?`: `string`; `unhedged_size?`: `string`; `leverage?`: `string`; `risk_limit?`: `string`; `leverage_max?`: `string`; `maintenance_rate?`: `string`; `value?`: `string`; `margin?`: `string`; `entry_price?`: `string`; `liq_price?`: `string`; `mark_price?`: `string`; `initial_margin?`: `string`; `maintenance_margin?`: `string`; `unrealised_pnl?`: `string`; `realised_pnl?`: `string`; `pnl_pnl?`: `string`; `pnl_fund?`: `string`; `pnl_fee?`: `string`; `history_pnl?`: `string`; `last_close_pnl?`: `string`; `realised_point?`: `string`; `history_point?`: `string`; `adl_ranking?`: `int32`; `pending_orders?`: `int32`; `close_order?`: *[PositionCloseOrder](#model-positioncloseorder); `mode?`: `string`; `cross_leverage_limit?`: `string`; `update_time?`: `int64`; `update_id?`: `int64`; `open_time?`: `int64`; `risk_limit_table?`: `string`; `average_maintenance_rate?`: `string`; `pid?`: `int64`; `pos_margin_mode?`: `string`; `lever?`: `string`.

<a id="model-positionclose"></a>
### PositionClose

`time?`: `float64`; `contract?`: `string`; `side?`: `string`; `pnl?`: `string`; `pnl_pnl?`: `string`; `pnl_fund?`: `string`; `pnl_fee?`: `string`; `text?`: `string`; `max_size?`: `string`; `accum_size?`: `string`; `first_open_time?`: `int64`; `long_price?`: `string`; `short_price?`: `string`.

Field semantics: `side` — Position side - `long`: Long position - `short`: Short position.

<a id="model-positioncloseorder"></a>
### PositionCloseOrder

`id?`: `int64`; `price?`: `string`; `is_liq?`: `bool`.

Field semantics: `id` — Order ID.

<a id="model-positiontimerange"></a>
### PositionTimerange

`contract?`: `string`; `size?`: `string`; `leverage?`: `string`; `risk_limit?`: `string`; `leverage_max?`: `string`; `maintenance_rate?`: `string`; `margin?`: `string`; `liq_price?`: `string`; `realised_pnl?`: `string`; `history_pnl?`: `string`; `last_close_pnl?`: `string`; `realised_point?`: `string`; `history_point?`: `string`; `mode?`: `string`; `cross_leverage_limit?`: `string`; `entry_price?`: `string`; `time?`: `int64`.

<a id="model-stopalltrailorders"></a>
### StopAllTrailOrders

`contract?`: `string`; `related_position?`: `int32`.

<a id="model-stoptrailorder"></a>
### StopTrailOrder

`id?`: `int64`; `text?`: `string`.

Field semantics: `id` — Order ID, if ID is specified, text is not needed.

<a id="model-trailchangelog"></a>
### TrailChangeLog

`updated_at?`: `int64`; `amount?`: `string`; `is_gte?`: `bool`; `activation_price?`: `string`; `price_type?`: `int32`; `price_offset?`: `string`; `is_create?`: `bool`.

Field semantics: `amount` — Trading quantity in contracts, positive for buy, negative for sell; `price_type` — Activation price type: 0-unknown, 1-latest price, 2-index price, 3-mark price.

<a id="model-trailorder"></a>
### TrailOrder

`id?`: `int64`; `user_id?`: `int64`; `user?`: `int64`; `contract?`: `string`; `settle?`: `string`; `amount?`: `string`; `is_gte?`: `bool`; `activation_price?`: `string`; `price_type?`: `int32`; `price_offset?`: `string`; `text?`: `string`; `reduce_only?`: `bool`; `position_related?`: `bool`; `created_at?`: `int64`; `activated_at?`: `int64`; `finished_at?`: `int64`; `create_time?`: `int64`; `active_time?`: `int64`; `finish_time?`: `int64`; `reason?`: `string`; `suborder_text?`: `string`; `is_dual_mode?`: `bool`; `trigger_price?`: `string`; `suborder_id?`: `int64`; `side_label?`: `string`; `original_status?`: `int32`; `status?`: `string`; `position_side_output?`: `string`; `updated_at?`: `int64`; `extremum_price?`: `string`; `status_code?`: `string`; `created_at_precise?`: `string`; `finished_at_precise?`: `string`; `activated_at_precise?`: `string`; `status_label?`: `string`; `pos_margin_mode?`: `string`; `position_mode?`: `string`; `error_label?`: `string`; `leverage?`: `string`.

Field semantics: `id` — Order ID; `amount` — Trading quantity in contracts, positive for buy, negative for sell; `price_type` — Activation price type: 0-unknown, 1-latest price, 2-index price, 3-mark price; `status` — Simplified order status: open/finished; `position_mode` — Position mode: single, dual, and dual_plus.

<a id="model-trailorderchangelogresponse"></a>
### TrailOrderChangeLogResponse

`change_log?`: [][TrailChangeLog](#model-trailchangelog).

<a id="model-trailorderdetailresponse"></a>
### TrailOrderDetailResponse

`code?`: `int32`; `message?`: `string`; `data?`: [TrailOrderResponse](#model-trailorderresponse); `timestamp?`: `int64`.

Field semantics: `timestamp` — Response timestamp (milliseconds).

<a id="model-trailorderlistresponse"></a>
### TrailOrderListResponse

`orders?`: [][TrailOrder](#model-trailorder).

<a id="model-trailorderresponse"></a>
### TrailOrderResponse

`order?`: [TrailOrder](#model-trailorder).

<a id="model-triggerorderresponse"></a>
### TriggerOrderResponse

`id?`: `int64`; `id_string?`: `string`.

Field semantics: `id` — Auto order ID.

<a id="model-triggertime"></a>
### TriggerTime

`triggerTime?`: `int64`.

<a id="model-updatedualcomppositioncrossmoderequest"></a>
### UpdateDualCompPositionCrossModeRequest

`mode`: `string`; `contract`: `string`.

<a id="model-updatetrailorder"></a>
### UpdateTrailOrder

`id`: `int64`; `amount?`: `string`; `activation_price?`: `string`; `is_gte_str?`: `string`; `price_type?`: `int32`; `price_offset?`: `string`.

Field semantics: `id` — Order ID; `amount` — Total trading quantity in contracts, positive for buy, negative for sell, 0 means no modification.
