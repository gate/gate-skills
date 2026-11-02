# Spot margin and trading loans Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-autorepaysetting"></a>
### AutoRepaySetting

`status?`: `string`.

Field semantics: `status` — Auto repayment status: `on` - enabled, `off` - disabled.

<a id="model-createuniloan"></a>
### CreateUniLoan

`currency`: `string`; `type`: `string`; `amount`: `string`; `repaid_all?`: `bool`; `currency_pair`: `string`.

<a id="model-crossmarginloan"></a>
### CrossMarginLoan

`id?`: `string`; `create_time?`: `int64`; `update_time?`: `int64`; `currency`: `string`; `amount`: `string`; `text?`: `string`; `status?`: `int32`; `repaid?`: `string`; `repaid_interest?`: `string`; `unpaid_interest?`: `string`.

Field semantics: `create_time` — Creation timestamp, in milliseconds; `update_time` — Update timestamp, in milliseconds; `status` — Deprecated. Currently, all statuses have been set to 2. Borrow loan status, which includes: - 1: failed to borrow - 2: borrowed but not repaid - 3: repayment complete.

<a id="model-crossmarginrepayment"></a>
### CrossMarginRepayment

`id?`: `string`; `create_time?`: `int64`; `loan_id?`: `string`; `currency?`: `string`; `principal?`: `string`; `interest?`: `string`; `repayment_type?`: `string`.

<a id="model-fundingaccount"></a>
### FundingAccount

`currency?`: `string`; `available?`: `string`; `locked?`: `string`; `lent?`: `string`; `total_lent?`: `string`.

<a id="model-liquidateorder"></a>
### LiquidateOrder

`text?`: `string`; `currency_pair`: `string`; `amount`: `string`; `price`: `string`; `action_mode?`: `string`.

<a id="model-marginaccount"></a>
### MarginAccount

`currency_pair?`: `string`; `account_type?`: `string`; `leverage?`: `string`; `locked?`: `bool`; `risk?`: `string`; `mmr?`: `string`; `base?`: [MarginAccountCurrency](#model-marginaccountcurrency); `quote?`: [MarginAccountCurrency](#model-marginaccountcurrency).

<a id="model-marginaccountbook"></a>
### MarginAccountBook

`id?`: `string`; `time?`: `string`; `time_ms?`: `int64`; `currency?`: `string`; `currency_pair?`: `string`; `change?`: `string`; `balance?`: `string`; `type?`: `string`.

Field semantics: `time_ms` — The timestamp of the change (in milliseconds).

<a id="model-marginaccountcurrency"></a>
### MarginAccountCurrency

`currency?`: `string`; `available?`: `string`; `locked?`: `string`; `borrowed?`: `string`; `interest?`: `string`.

<a id="model-marginleveragetier"></a>
### MarginLeverageTier

`upper_limit?`: `string`; `mmr?`: `string`; `leverage?`: `string`.

<a id="model-marginmarketleverage"></a>
### MarginMarketLeverage

`currency_pair?`: `string`; `leverage`: `string`.

<a id="model-margintransferable"></a>
### MarginTransferable

`currency?`: `string`; `currency_pair?`: `string`; `amount?`: `string`.

<a id="model-maxuniborrowable"></a>
### MaxUniBorrowable

`currency`: `string`; `currency_pair?`: `string`; `borrowable`: `string`.

<a id="model-order"></a>
### Order

`id?`: `string`; `text?`: `string`; `amend_text?`: `string`; `create_time?`: `string`; `update_time?`: `string`; `create_time_ms?`: `int64`; `update_time_ms?`: `int64`; `status?`: `string`; `currency_pair`: `string`; `trade_quote?`: `string`; `type?`: `string`; `account?`: `string`; `side`: `string`; `amount`: `string`; `price?`: `string`; `time_in_force?`: `string`; `iceberg?`: `string`; `auto_borrow?`: `bool`; `auto_repay?`: `bool`; `left?`: `string`; `filled_amount?`: `string`; `fill_price?`: `string`; `filled_total?`: `string`; `avg_deal_price?`: `string`; `fee?`: `string`; `fee_currency?`: `string`; `point_fee?`: `string`; `gt_fee?`: `string`; `gt_maker_fee?`: `string`; `gt_taker_fee?`: `string`; `gt_discount?`: `bool`; `rebated_fee?`: `string`; `rebated_fee_currency?`: `string`; `stp_id?`: `int32`; `stp_act?`: `string`; `finish_as?`: `string`; `action_mode?`: `string`; `slippage?`: `string`; `stop_profit`: *[SpotOrderStopProfit](#model-spotorderstopprofit); `stop_loss`: *[SpotOrderStopLoss](#model-spotorderstoploss).

Field semantics: `id` — Order ID; `create_time_ms` — Creation time of order (in milliseconds); `update_time_ms` — Last modification time of order (in milliseconds); `status` — Order status - `open`: to be filled - `closed`: closed order - `cancelled`: cancelled; `side` — Buy or sell order; `amount` — Trade amount When `type` is `limit`, this is the base currency to trade (the currency being bought or sold), e.g. `BTC` in `BTC_USDT`. When `type` is `market`, the meaning depends on the side: - `side`: `buy` refers to the quote currency, e.g. `USDT` in `BTC_USDT` - `side`: `sell` refers to the base currency, e.g. `BTC` in `BTC_USDT`; `time_in_force` — Time in force - gtc: GoodTillCancelled - ioc: ImmediateOrCancelled, taker only - poc: PendingOrCancelled, makes a post-only order that always enjoys a maker fee - fok: FillOrKill, fill either completely or none Only `ioc` and `fok` are supported when `type`=`market`; `finish_as` — How the order finished: - open: Pending processing - filled: Fully filled - cancelled: Cancelled by user - liquidate_cancelled: Cancelled by liquidation - small: Order size too small - depth_not_enough: Cancelled due to insufficient order book depth - trader_not_enough: Cancelled due to insufficient counterparty liquidity - ioc: Not filled immediately because time-in-force is IOC - poc: Post-only requirement not met because time-in-force is set to poc (maker-only); rejected after being detected as taker - fok: Not fully filled immediately because time-in-force is FOK - stp: Cancelled due to self-trade prevention - price_protect_cancelled: Cancelled due to price protection - unknown: Unknown.

<a id="model-spotorderstoploss"></a>
### SpotOrderStopLoss

`trigger_price?`: `string`; `order_price?`: `string`.

<a id="model-spotorderstopprofit"></a>
### SpotOrderStopProfit

`trigger_price?`: `string`; `order_price?`: `string`.

<a id="model-unicurrencypair"></a>
### UniCurrencyPair

`currency_pair?`: `string`; `base_min_borrow_amount?`: `string`; `quote_min_borrow_amount?`: `string`; `leverage?`: `string`; `status?`: `string`; `delisted_time?`: `float32`.

Field semantics: `status` — Status - enabled: Enabled - disabled: Disabled.

<a id="model-unifiedhistoryloanrate"></a>
### UnifiedHistoryLoanRate

`currency?`: `string`; `tier?`: `string`; `tier_up_rate?`: `string`; `rates?`: [][UnifiedHistoryLoanRateRates](#model-unifiedhistoryloanraterates).

<a id="model-unifiedhistoryloanraterates"></a>
### UnifiedHistoryLoanRateRates

`time?`: `int64`; `rate?`: `string`.

Field semantics: `time` — Hourly timestamp corresponding to this interest rate, in milliseconds.

<a id="model-unifiedloan"></a>
### UnifiedLoan

`currency`: `string`; `type`: `string`; `amount`: `string`; `repaid_all?`: `bool`; `text?`: `string`.

<a id="model-unifiedloanrecord"></a>
### UnifiedLoanRecord

`id?`: `int64`; `type?`: `string`; `repayment_type?`: `string`; `borrow_type?`: `string`; `currency_pair?`: `string`; `currency?`: `string`; `amount?`: `string`; `create_time?`: `int64`.

<a id="model-unifiedloanresult"></a>
### UnifiedLoanResult

`tran_id?`: `int64`.

<a id="model-uniloan"></a>
### UniLoan

`currency?`: `string`; `currency_pair?`: `string`; `amount?`: `string`; `type?`: `string`; `create_time?`: `int64`; `update_time?`: `int64`.

<a id="model-uniloaninterestrecord"></a>
### UniLoanInterestRecord

`currency?`: `string`; `currency_pair?`: `string`; `actual_rate?`: `string`; `interest?`: `string`; `status?`: `int32`; `type?`: `string`; `create_time?`: `int64`.

Field semantics: `status` — Status: 0 - fail, 1 - success.

<a id="model-uniloanrecord"></a>
### UniLoanRecord

`type?`: `string`; `currency_pair?`: `string`; `currency?`: `string`; `amount?`: `string`; `create_time?`: `int64`.
