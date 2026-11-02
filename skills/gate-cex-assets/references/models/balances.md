# Asset balances and histories Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-accountbalance"></a>
### AccountBalance

`amount?`: `string`; `currency?`: `string`; `unrealised_pnl?`: `string`; `borrowed?`: `string`.

<a id="model-crossmarginbalance"></a>
### CrossMarginBalance

`available?`: `string`; `freeze?`: `string`; `borrowed?`: `string`; `interest?`: `string`.

<a id="model-futuresaccount"></a>
### FuturesAccount

`total?`: `string`; `unrealised_pnl?`: `string`; `position_margin?`: `string`; `order_margin?`: `string`; `available?`: `string`; `point?`: `string`; `currency?`: `string`; `in_dual_mode?`: `bool`; `enable_credit?`: `bool`; `position_initial_margin?`: `string`; `maintenance_margin?`: `string`; `bonus?`: `string`; `enable_evolved_classic?`: `bool`; `cross_order_margin?`: `string`; `cross_initial_margin?`: `string`; `cross_maintenance_margin?`: `string`; `cross_unrealised_pnl?`: `string`; `cross_available?`: `string`; `cross_margin_balance?`: `string`; `cross_mmr?`: `string`; `cross_imr?`: `string`; `isolated_position_margin?`: `string`; `enable_new_dual_mode?`: `bool`; `margin_mode?`: `int32`; `enable_tiered_mm?`: `bool`; `enable_dual_plus?`: `bool`; `position_mode?`: `string`; `history?`: [FuturesAccountHistory](#model-futuresaccounthistory).

<a id="model-futuresaccounthistory"></a>
### FuturesAccountHistory

`dnw?`: `string`; `pnl?`: `string`; `fee?`: `string`; `refr?`: `string`; `fund?`: `string`; `point_dnw?`: `string`; `point_fee?`: `string`; `point_refr?`: `string`; `bonus_dnw?`: `string`; `bonus_offset?`: `string`; `cross_settle?`: `string`.

<a id="model-marginaccount"></a>
### MarginAccount

`currency_pair?`: `string`; `account_type?`: `string`; `leverage?`: `string`; `locked?`: `bool`; `risk?`: `string`; `mmr?`: `string`; `base?`: [MarginAccountCurrency](#model-marginaccountcurrency); `quote?`: [MarginAccountCurrency](#model-marginaccountcurrency).

<a id="model-marginaccountcurrency"></a>
### MarginAccountCurrency

`currency?`: `string`; `available?`: `string`; `locked?`: `string`; `borrowed?`: `string`; `interest?`: `string`.

<a id="model-subaccountbalance"></a>
### SubAccountBalance

`uid?`: `string`; `available?`: `map[string]string`; `locking?`: `map[string]string`.

<a id="model-subaccountcrossmarginbalance"></a>
### SubAccountCrossMarginBalance

`uid?`: `string`; `available?`: [SubCrossMarginAccount](#model-subcrossmarginaccount).

<a id="model-subaccountfuturesbalance"></a>
### SubAccountFuturesBalance

`uid?`: `string`; `available?`: map[string][FuturesAccount](#model-futuresaccount).

<a id="model-subaccountmarginbalance"></a>
### SubAccountMarginBalance

`uid?`: `string`; `available?`: [][MarginAccount](#model-marginaccount).

<a id="model-subcrossmarginaccount"></a>
### SubCrossMarginAccount

`user_id?`: `int64`; `locked?`: `bool`; `balances?`: map[string][CrossMarginBalance](#model-crossmarginbalance); `total?`: `string`; `borrowed?`: `string`; `borrowed_net?`: `string`; `net?`: `string`; `leverage?`: `string`; `interest?`: `string`; `risk?`: `string`; `total_initial_margin?`: `string`; `total_margin_balance?`: `string`; `total_maintenance_margin?`: `string`; `total_initial_margin_rate?`: `string`; `total_maintenance_margin_rate?`: `string`; `total_available_margin?`: `string`.

<a id="model-totalbalance"></a>
### TotalBalance

`total?`: [AccountBalance](#model-accountbalance); `details?`: map[string][AccountBalance](#model-accountbalance).

<a id="model-tradefee"></a>
### TradeFee

`user_id?`: `int64`; `taker_fee?`: `string`; `maker_fee?`: `string`; `rpi_maker_fee?`: `string`; `gt_discount?`: `bool`; `gt_taker_fee?`: `string`; `gt_maker_fee?`: `string`; `loan_fee?`: `string`; `point_type?`: `string`; `futures_taker_fee?`: `string`; `futures_maker_fee?`: `string`; `futures_rpi_maker_fee?`: `string`; `delivery_taker_fee?`: `string`; `delivery_maker_fee?`: `string`; `debit_fee?`: `int32`; `rpi_mm?`: `int32`.
