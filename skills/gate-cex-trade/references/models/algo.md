# Algorithm Execution Models

Read only models linked by the selected action. `?` denotes SDK JSON omission, not API optionality. Request-only and response-only fields are separate. Monetary values remain decimal strings; sizes are contract quantities.

For chase results, require a nonempty `id` on create, an `order` with its ID on
detail/stop, or an `orders` array on list/stop-all. The CLI exposes an empty result
as `{"orders":[]}`. A service business error must produce a failed CLI exit even
when HTTP status is 200; do not treat a silently decoded `{}` as success.

<a id="model-chaseorder"></a>
### ChaseOrder

`id?`: `string`; `user?`: `string`; `contract?`: `string`; `settle?`: `string`; `amount?`: `string`; `price_limit?`: `string`; `reduce_only?`: `bool`; `text?`: `string`; `create_time?`: `int64`; `finish_time?`: `int64`; `original_status?`: `int32`; `status?`: `string`; `reason?`: `string`; `fill_amount?`: `string`; `average_fill_price?`: `string`; `suborder_id?`: `string`; `is_dual_mode?`: `bool`; `side_label?`: `string`; `position_side_output?`: `string`; `chase_price?`: `string`; `interval_sec?`: `int32`; `updated_at?`: `int64`; `suborder_price?`: `string`; `suborder_ongoing?`: `bool`; `suborder_finish_as?`: `string`; `price_type?`: `int32`; `price_gap_type?`: `string`; `price_gap_value?`: `string`; `status_code?`: `string`; `create_time_precise?`: `string`; `finish_time_precise?`: `string`; `pos_margin_mode?`: `string`; `position_mode?`: `string`; `leverage?`: `string`; `error_label?`: `string`.

<a id="model-createchaseorderreq"></a>
### CreateChaseOrderReq

`contract`: `string`; `settle?`: `string`; `amount`: `string`; `price_limit`: `string`; `offset_limit?`: `string`; `reduce_only?`: `bool`; `text?`: `string`; `is_dual_mode?`: `bool`; `price_type?`: `int64`; `price_gap_type?`: `int64`; `price_gap_value?`: `string`; `pos_margin_mode?`: `string`; `position_mode?`: `string`.

<a id="model-createchaseorderresp"></a>
### CreateChaseOrderResp

`id?`: `string`.

<a id="model-getchaseorderdetailresp"></a>
### GetChaseOrderDetailResp

`order?`: [ChaseOrder](#model-chaseorder).

<a id="model-getchaseordersresp"></a>
### GetChaseOrdersResp

`orders?`: [][ChaseOrder](#model-chaseorder).

<a id="model-spotpovorder"></a>
### SpotPovOrder

`id`: `string`; `currency_pair`: `string`; `side`: `string`; `amount`: `string`; `participation_rate`: `int32`; `ttl`: `string`; `limit_price?`: `string`; `trigger_price?`: `string`; `status`: `string`; `terminated_as?`: `string`; `start_time_ms?`: `int64`; `end_time_ms?`: `int64`; `expire_time_ms?`: `int64`; `create_time_ms`: `int64`; `update_time_ms?`: `int64`; `text?`: `string`.

<a id="model-spotpovordercreator"></a>
### SpotPovOrderCreator

`currency_pair`: `string`; `side`: `string`; `amount`: `string`; `participation_rate`: `int32`; `ttl`: `string`; `limit_price?`: `string`; `trigger_price?`: `string`; `text?`: `string`.

<a id="model-stopallchaseordersresp"></a>
### StopAllChaseOrdersResp

`orders?`: [][ChaseOrder](#model-chaseorder).

<a id="model-stopchaseorderresp"></a>
### StopChaseOrderResp

`order?`: [ChaseOrder](#model-chaseorder).
