# VIP, fees and rate limits Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-accountratelimit"></a>
### AccountRateLimit

`tier?`: `string`; `ratio?`: `string`; `main_ratio?`: `string`; `updated_at?`: `string`.

<a id="model-debitfee"></a>
### DebitFee

`enabled`: `bool`.

<a id="model-feerate"></a>
### FeeRate

`data?`: [FeeRateData](#model-feeratedata); `timestamp?`: `int64`.

<a id="model-feeratedata"></a>
### FeeRateData

`list?`: [][FeeRateDataList](#model-feeratedatalist).

<a id="model-feeratedatalist"></a>
### FeeRateDataList

`vip_level?`: `int32`; `maker_fee?`: `string`; `taker_fee?`: `string`.

<a id="model-futuresfee"></a>
### FuturesFee

`taker_fee?`: `string`; `maker_fee?`: `string`.

<a id="model-spotfee"></a>
### SpotFee

`user_id?`: `int64`; `taker_fee?`: `string`; `maker_fee?`: `string`; `rpi_maker_fee?`: `string`; `gt_discount?`: `bool`; `gt_taker_fee?`: `string`; `gt_maker_fee?`: `string`; `loan_fee?`: `string`; `point_type?`: `string`; `currency_pair?`: `string`; `debit_fee?`: `int32`; `rpi_mm?`: `int32`.
