# Multi-collateral loans Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-borrowcurrencyinfo"></a>
### BorrowCurrencyInfo

`currency?`: `string`; `index_price?`: `string`; `left_repay_principal?`: `string`; `left_repay_interest?`: `string`; `left_repay_usdt?`: `string`.

<a id="model-collateraladjust"></a>
### CollateralAdjust

`order_id`: `int64`; `type`: `string`; `collaterals?`: [][CollateralCurrency](#model-collateralcurrency).

`type` is `append` to add collateral or `redeem` to withdraw it. Verify the exact order and resulting collateral/LTV; do not reverse direction to resolve a rejection.

<a id="model-collateraladjustres"></a>
### CollateralAdjustRes

`order_id?`: `int64`; `collateral_currencies?`: [][CollateralCurrencyRes](#model-collateralcurrencyres).

<a id="model-collateralcurrency"></a>
### CollateralCurrency

`currency?`: `string`; `amount?`: `string`.

<a id="model-collateralcurrencyinfo"></a>
### CollateralCurrencyInfo

`currency?`: `string`; `index_price?`: `string`; `left_collateral?`: `string`; `left_collateral_usdt?`: `string`.

<a id="model-collateralcurrencyres"></a>
### CollateralCurrencyRes

`succeeded?`: `bool`; `label?`: `string`; `message?`: `string`; `currency?`: `string`; `amount?`: `string`.

<a id="model-collateralltv"></a>
### CollateralLtv

`init_ltv?`: `string`; `alert_ltv?`: `string`; `liquidate_ltv?`: `string`.

<a id="model-createmulticollateralorder"></a>
### CreateMultiCollateralOrder

`order_id?`: `string`; `order_type?`: `string`; `fixed_type?`: `string`; `fixed_rate?`: `string`; `auto_renew?`: `bool`; `auto_repay?`: `bool`; `borrow_currency`: `string`; `borrow_amount`: `string`; `collateral_currencies?`: [][CollateralCurrency](#model-collateralcurrency).

`order_type` is `current` or `fixed`; omission defaults to `current`. A fixed-rate request requires both `fixed_type` (`7d` or `30d`) and `fixed_rate`. Never downgrade a fixed loan to current-rate lending after a failure. Verify the rate's unit and terms before forming the request. `auto_renew` and `auto_repay` require explicit user authority for their continuing/fund effects.

<a id="model-multicollateralorder"></a>
### MultiCollateralOrder

`order_id?`: `string`; `order_type?`: `string`; `fixed_type?`: `string`; `fixed_rate?`: `string`; `expire_time?`: `int64`; `auto_renew?`: `bool`; `auto_repay?`: `bool`; `current_ltv?`: `string`; `status?`: `string`; `borrow_time?`: `int64`; `total_left_repay_usdt?`: `string`; `total_left_collateral_usdt?`: `string`; `borrow_currencies?`: [][BorrowCurrencyInfo](#model-borrowcurrencyinfo); `collateral_currencies?`: [][CollateralCurrencyInfo](#model-collateralcurrencyinfo).

Field semantics: `expire_time` — Expiration time, timestamp, unit in seconds; `status` — Order status: - initial: Initial state after placing the order - collateral_deducted: Collateral deduction successful - collateral_returning: Loan failed - Collateral return pending - lent: Loan successful - repaying: Repayment in progress - liquidating: Liquidation in progress - finished: Order completed - closed_liquidated: Liquidation and repayment completed; `borrow_time` — Borrowing time, timestamp in seconds.

## User-facing field mapping

For a loan position, show borrowed asset and outstanding principal/interest,
collateral asset and amount, current LTV, alert LTV, liquidation LTV, maturity when
applicable, and a translated state. Use business phrases such as “loan active”,
“repayment in progress”, “liquidation in progress”, or “completed”; flag
liquidation exposure prominently. For a repayment or collateral adjustment, show
the affected asset, amount, resulting LTV when returned, and verified outcome.
Do not show `order_id`, `record_id`, raw enum values, internal timestamps, index
prices, or response labels by default. `auto_renew` and `auto_repay` must be
described as enabled or disabled continuing instructions, not raw booleans.

<a id="model-multicollateralrecord"></a>
### MultiCollateralRecord

`order_id?`: `int64`; `record_id?`: `int64`; `before_ltv?`: `string`; `after_ltv?`: `string`; `operate_time?`: `int64`; `borrow_currencies?`: [][MultiCollateralRecordCurrency](#model-multicollateralrecordcurrency); `collateral_currencies?`: [][MultiCollateralRecordCurrency](#model-multicollateralrecordcurrency).

Field semantics: `operate_time` — Operation time, timestamp in seconds.

<a id="model-multicollateralrecordcurrency"></a>
### MultiCollateralRecordCurrency

`currency?`: `string`; `index_price?`: `string`; `before_amount?`: `string`; `before_amount_usdt?`: `string`; `after_amount?`: `string`; `after_amount_usdt?`: `string`.

<a id="model-multiloanrepayitem"></a>
### MultiLoanRepayItem

`currency?`: `string`; `amount?`: `string`; `repaid_all`: `bool`.

<a id="model-multirepayrecord"></a>
### MultiRepayRecord

`order_id?`: `int64`; `record_id?`: `int64`; `init_ltv?`: `string`; `before_ltv?`: `string`; `after_ltv?`: `string`; `borrow_time?`: `int64`; `repay_time?`: `int64`; `borrow_currencies?`: [][RepayRecordCurrency](#model-repayrecordcurrency); `collateral_currencies?`: [][RepayRecordCurrency](#model-repayrecordcurrency); `repaid_currencies?`: [][RepayRecordRepaidCurrency](#model-repayrecordrepaidcurrency); `total_interest_list?`: [][RepayRecordTotalInterest](#model-repayrecordtotalinterest); `left_repay_interest_list?`: [][RepayRecordLeftInterest](#model-repayrecordleftinterest).

Field semantics: `borrow_time` — Borrowing time, timestamp in seconds; `repay_time` — Repayment time, timestamp in seconds.

<a id="model-multirepayresp"></a>
### MultiRepayResp

`order_id?`: `int64`; `repaid_currencies?`: [][RepayCurrencyRes](#model-repaycurrencyres).

<a id="model-orderresp"></a>
### OrderResp

`order_id?`: `int64`.

<a id="model-repaycurrencyres"></a>
### RepayCurrencyRes

`succeeded?`: `bool`; `label?`: `string`; `message?`: `string`; `currency?`: `string`; `repaid_principal?`: `string`; `repaid_interest?`: `string`.

<a id="model-repaymultiloan"></a>
### RepayMultiLoan

`order_id`: `int64`; `repay_items`: [][MultiLoanRepayItem](#model-multiloanrepayitem).

<a id="model-repayrecordcurrency"></a>
### RepayRecordCurrency

`currency?`: `string`; `index_price?`: `string`; `before_amount?`: `string`; `before_amount_usdt?`: `string`; `after_amount?`: `string`; `after_amount_usdt?`: `string`.

<a id="model-repayrecordleftinterest"></a>
### RepayRecordLeftInterest

`currency?`: `string`; `index_price?`: `string`; `before_amount?`: `string`; `before_amount_usdt?`: `string`; `after_amount?`: `string`; `after_amount_usdt?`: `string`.

<a id="model-repayrecordrepaidcurrency"></a>
### RepayRecordRepaidCurrency

`currency?`: `string`; `index_price?`: `string`; `repaid_amount?`: `string`; `repaid_principal?`: `string`; `repaid_interest?`: `string`; `repaid_amount_usdt?`: `string`.

<a id="model-repayrecordtotalinterest"></a>
### RepayRecordTotalInterest

`currency?`: `string`; `index_price?`: `string`; `amount?`: `string`; `amount_usdt?`: `string`.
