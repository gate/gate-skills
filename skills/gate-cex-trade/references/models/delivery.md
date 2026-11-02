# Delivery futures Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-deliveryaccount"></a>
### DeliveryAccount

`total?`: `string`; `unrealised_pnl?`: `string`; `position_margin?`: `string`; `order_margin?`: `string`; `available?`: `string`; `point?`: `string`; `currency?`: `string`; `in_dual_mode?`: `bool`; `enable_credit?`: `bool`; `position_initial_margin?`: `string`; `maintenance_margin?`: `string`; `bonus?`: `string`; `enable_evolved_classic?`: `bool`; `cross_order_margin?`: `string`; `cross_initial_margin?`: `string`; `cross_maintenance_margin?`: `string`; `cross_unrealised_pnl?`: `string`; `cross_available?`: `string`; `cross_margin_balance?`: `string`; `cross_mmr?`: `string`; `cross_imr?`: `string`; `isolated_position_margin?`: `string`; `enable_new_dual_mode?`: `bool`; `margin_mode?`: `int32`; `enable_tiered_mm?`: `bool`; `history?`: [DeliveryAccountHistory](#model-deliveryaccounthistory).

<a id="model-deliveryaccountbook"></a>
### DeliveryAccountBook

`time?`: `float64`; `change?`: `string`; `balance?`: `string`; `type?`: `string`; `text?`: `string`; `contract?`: `string`; `trade_id?`: `string`; `id?`: `string`.

<a id="model-deliveryaccounthistory"></a>
### DeliveryAccountHistory

`dnw?`: `string`; `pnl?`: `string`; `fee?`: `string`; `refr?`: `string`; `fund?`: `string`; `point_dnw?`: `string`; `point_fee?`: `string`; `point_refr?`: `string`; `bonus_dnw?`: `string`; `bonus_offset?`: `string`.

<a id="model-deliveryliquidate"></a>
### DeliveryLiquidate

`time?`: `int64`; `contract?`: `string`; `leverage?`: `string`; `size?`: `int64`; `margin?`: `string`; `entry_price?`: `string`; `liq_price?`: `string`; `mark_price?`: `string`; `order_id?`: `int64`; `order_price?`: `string`; `fill_price?`: `string`; `left?`: `int64`.

<a id="model-deliverymytrade"></a>
### DeliveryMyTrade

`id?`: `int64`; `create_time?`: `float64`; `contract?`: `string`; `order_id?`: `string`; `size?`: `int64`; `close_size?`: `int64`; `price?`: `string`; `role?`: `string`; `text?`: `string`; `fee?`: `string`; `point_fee?`: `string`.

<a id="model-deliveryorder"></a>
### DeliveryOrder

`id?`: `int64`; `user?`: `int32`; `create_time?`: `float64`; `finish_time?`: `float64`; `finish_as?`: `string`; `status?`: `string`; `contract`: `string`; `size`: `int64`; `iceberg?`: `int64`; `price?`: `string`; `close?`: `bool`; `is_close?`: `bool`; `reduce_only?`: `bool`; `is_reduce_only?`: `bool`; `is_liq?`: `bool`; `tif?`: `string`; `left?`: `int64`; `fill_price?`: `string`; `text?`: `string`; `tkfr?`: `string`; `mkfr?`: `string`; `refu?`: `int32`; `auto_size?`: `string`; `stp_id?`: `int32`; `stp_act?`: `string`; `amend_text?`: `string`.

Field semantics: `id` — Futures order ID; `finish_as` — How the order was finished: - filled: all filled - cancelled: manually cancelled - liquidated: cancelled because of liquidation - ioc: time in force is `IOC`, finish immediately - auto_deleveraged: finished by ADL - reduce_only: cancelled because of increasing position while `reduce-only` set - position_closed: cancelled because the position was closed - reduce_out: only reduce positions by excluding hard-to-fill orders - stp: cancelled because self trade prevention; `status` — Order status - `open`: Pending - `finished`: Completed; `size` — Required. Trading quantity. Positive for buy, negative for sell. Set to 0 for close position orders..

<a id="model-deliveryposition"></a>
### DeliveryPosition

`user?`: `int64`; `contract?`: `string`; `size?`: `int64`; `leverage?`: `string`; `risk_limit?`: `string`; `leverage_max?`: `string`; `maintenance_rate?`: `string`; `value?`: `string`; `margin?`: `string`; `entry_price?`: `string`; `liq_price?`: `string`; `mark_price?`: `string`; `initial_margin?`: `string`; `maintenance_margin?`: `string`; `unrealised_pnl?`: `string`; `realised_pnl?`: `string`; `pnl_pnl?`: `string`; `pnl_fund?`: `string`; `pnl_fee?`: `string`; `history_pnl?`: `string`; `last_close_pnl?`: `string`; `realised_point?`: `string`; `history_point?`: `string`; `adl_ranking?`: `int32`; `pending_orders?`: `int32`; `close_order?`: *[PositionCloseOrder](#model-positioncloseorder); `mode?`: `string`; `cross_leverage_limit?`: `string`; `update_time?`: `int64`; `update_id?`: `int64`; `open_time?`: `int64`; `risk_limit_table?`: `string`; `average_maintenance_rate?`: `string`.

<a id="model-deliverypositionclose"></a>
### DeliveryPositionClose

`time?`: `float64`; `contract?`: `string`; `side?`: `string`; `pnl?`: `string`; `pnl_pnl?`: `string`; `pnl_fund?`: `string`; `pnl_fee?`: `string`; `text?`: `string`; `max_size?`: `int64`; `accum_size?`: `int64`; `first_open_time?`: `int64`; `long_price?`: `string`; `short_price?`: `string`.

Field semantics: `side` — Position side - `long`: Long position - `short`: Short position.

<a id="model-deliverysettlement"></a>
### DeliverySettlement

`time?`: `int64`; `contract?`: `string`; `leverage?`: `string`; `size?`: `int64`; `margin?`: `string`; `entry_price?`: `string`; `settle_price?`: `string`; `profit?`: `string`; `fee?`: `string`.

<a id="model-futuresinitialorder"></a>
### FuturesInitialOrder

`contract`: `string`; `size?`: `int64`; `amount?`: `string`; `price`: `string`; `close?`: `bool`; `tif?`: `string`; `text?`: `string`; `reduce_only?`: `bool`; `auto_size?`: `string`; `is_reduce_only?`: `bool`; `is_close?`: `bool`.

Field semantics: `size` — Represents the number of contracts that need to be closed, full closing: size=0 Partial closing: plan-close-short-position size>0 Partial closing: plan-close-long-position size<0; `amount` — Same as `size`; used for decimal contract size. When both `size` and `amount` are provided, `amount` takes precedence..

<a id="model-futurespricetrigger"></a>
### FuturesPriceTrigger

`strategy_type?`: `int32`; `price_type?`: `int32`; `price`: `string`; `rule`: `int32`; `expiration?`: `int32`.

<a id="model-futurespricetriggeredorder"></a>
### FuturesPriceTriggeredOrder

`initial`: [FuturesInitialOrder](#model-futuresinitialorder); `trigger`: [FuturesPriceTrigger](#model-futurespricetrigger); `id?`: `int64`; `id_string?`: `string`; `user?`: `int32`; `create_time?`: `float64`; `finish_time?`: `float64`; `trade_id?`: `int64`; `status?`: `string`; `finish_as?`: `string`; `reason?`: `string`; `order_type?`: `string`; `me_order_id?`: `int64`; `pos_margin_mode?`: `string`.

Field semantics: `id` — Auto order ID; `status` — Order status - `open`: Active - `finished`: Finished - `inactive`: Inactive, only applies to order take-profit/stop-loss - `invalid`: Invalid, only applies to order take-profit/stop-loss; `finish_as` — Finish status: cancelled - Cancelled; succeeded - Succeeded; failed - Failed; expired - Expired.

<a id="model-positioncloseorder"></a>
### PositionCloseOrder

`id?`: `int64`; `price?`: `string`; `is_liq?`: `bool`.

Field semantics: `id` — Order ID.

<a id="model-triggerorderresponse"></a>
### TriggerOrderResponse

`id?`: `int64`; `id_string?`: `string`.

Field semantics: `id` — Auto order ID.
