# Recurring investment Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-autoinvestcoinsitem"></a>
### AutoInvestCoinsItem

`key`: `string`; `value`: `string`; `asset_icon_url`: `string`; `sort?`: `int64`.

<a id="model-autoinvestmininvestamount"></a>
### AutoInvestMinInvestAmount

`money`: `string`; `asset_type`: `int32`; `items`: [][AutoInvestMinInvestAmountItems](#model-autoinvestmininvestamountitems).

`asset_type` is required: integer `1` selects cryptocurrency and integer `2` selects TradFi stocks. There is no implicit default. Choose the requested asset family explicitly; strings, booleans, null and other integers are invalid. Keep `money`, `items[].asset` and `items[].ratio` unchanged.

<a id="model-autoinvestmininvestamountitems"></a>
### AutoInvestMinInvestAmountItems

`asset`: `string`; `ratio`: `string`.

<a id="model-autoinvestmininvestamountresp"></a>
### AutoInvestMinInvestAmountResp

`min_amount`: `string`.

<a id="model-autoinvestorderitem"></a>
### AutoInvestOrderItem

`id`: `int64`; `type`: `string`; `amount`: `string`; `plan_id`: `int64`; `side`: `int64`; `asset`: `string`; `record_id`: `int64`; `total_money`: `string`; `market`: `string`; `price`: `string`; `create_time`: `int64`; `total`: `string`; `fund_flow`: `string`; `error_code`: `int64`; `error_msg`: `string`; `status`: `int64`.

Field semantics: `id` — Order ID.

## User-facing field mapping

Present supported assets by asset symbol and the minimum required investment as a
minimum investment amount in the selected funding currency. For an execution
record, present asset, amount, execution price when returned, execution time, and
the business outcome. Do not show `id`, `plan_id`, `record_id`, raw `side`, raw
`status`, `error_code`, `fund_flow`, or implementation timestamps by default. If
the service gives only an undocumented code, state that the execution outcome needs
verification rather than translating the code.
