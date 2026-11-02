# Small-balance conversion Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-convertsmallbalance"></a>
### ConvertSmallBalance

`currency?`: `[]string`; `is_all?`: `bool`.

<a id="model-smallbalance"></a>
### SmallBalance

`currency?`: `string`; `available_balance?`: `string`; `estimated_as_btc?`: `string`; `convertible_to_gt?`: `string`.

<a id="model-smallbalancehistory"></a>
### SmallBalanceHistory

`id?`: `string`; `currency?`: `string`; `amount?`: `string`; `gt_amount?`: `string`; `create_time?`: `int64`.

Field semantics: `id` — Order ID; `create_time` — Exchange time (in seconds).
