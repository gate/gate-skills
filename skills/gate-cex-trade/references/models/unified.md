# Unified trading account settings Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-accountdetail"></a>
### AccountDetail

`ip_whitelist?`: `[]string`; `currency_pairs?`: `[]string`; `user_id?`: `int64`; `tier?`: `int64`; `key?`: [AccountDetailKey](#model-accountdetailkey); `copy_trading_role?`: `int32`.

<a id="model-accountdetailkey"></a>
### AccountDetailKey

`mode?`: `int32`.

<a id="model-margintiers"></a>
### MarginTiers

`tier?`: `string`; `margin_rate?`: `string`; `lower_limit?`: `string`; `upper_limit?`: `string`; `leverage?`: `string`.

<a id="model-mockfuturesorder"></a>
### MockFuturesOrder

`contract`: `string`; `size`: `string`; `left`: `string`.

Field semantics: `size` — Contract quantity, representing the initial order quantity, not involved in actual settlement.

<a id="model-mockfuturesposition"></a>
### MockFuturesPosition

`contract`: `string`; `size`: `string`.

Field semantics: `size` — Position size, measured in contract quantity.

<a id="model-mockmarginresult"></a>
### MockMarginResult

`type?`: `string`; `profit_loss_ranges?`: [][ProfitLossRange](#model-profitlossrange); `max_loss?`: [ProfitLossRange](#model-profitlossrange); `mr1?`: `string`; `mr2?`: `string`; `mr3?`: `string`; `mr4?`: `string`.

<a id="model-mockoptionsorder"></a>
### MockOptionsOrder

`options_name`: `string`; `size`: `string`; `left`: `string`.

<a id="model-mockoptionsposition"></a>
### MockOptionsPosition

`options_name`: `string`; `size`: `string`.

Field semantics: `size` — Position size, measured in contract quantity.

<a id="model-mockriskunit"></a>
### MockRiskUnit

`symbol?`: `string`; `spot_in_use?`: `string`; `maintain_margin?`: `string`; `initial_margin?`: `string`; `margin_result?`: [][MockMarginResult](#model-mockmarginresult); `delta?`: `string`; `gamma?`: `string`; `theta?`: `string`; `vega?`: `string`.

<a id="model-mockspotbalance"></a>
### MockSpotBalance

`currency`: `string`; `equity`: `string`.

<a id="model-mockspotorder"></a>
### MockSpotOrder

`currency_pairs`: `string`; `order_price`: `string`; `count?`: `string`; `left`: `string`; `type`: `string`.

<a id="model-profitlossrange"></a>
### ProfitLossRange

`price_percentage?`: `string`; `implied_volatility_percentage?`: `string`; `profit_loss?`: `string`.

<a id="model-riskunits"></a>
### RiskUnits

`symbol?`: `string`; `spot_in_use?`: `string`; `maintain_margin?`: `string`; `initial_margin?`: `string`; `delta?`: `string`; `gamma?`: `string`; `theta?`: `string`; `vega?`: `string`.

<a id="model-stpgroup"></a>
### StpGroup

`id?`: `int64`; `name`: `string`; `creator_id?`: `int64`; `create_time?`: `int64`.

<a id="model-stpgroupuser"></a>
### StpGroupUser

`user_id?`: `int64`; `stp_id?`: `int64`; `create_time?`: `int64`.

<a id="model-transferablesresult"></a>
### TransferablesResult

`currency?`: `string`; `amount?`: `string`.

<a id="model-unifiedaccount"></a>
### UnifiedAccount

`mode?`: `string`; `user_id?`: `int64`; `refresh_time?`: `int64`; `locked?`: `bool`; `balances?`: map[string][UnifiedBalance](#model-unifiedbalance); `total?`: `string`; `borrowed?`: `string`; `total_initial_margin?`: `string`; `total_margin_balance?`: `string`; `total_maintenance_margin?`: `string`; `total_initial_margin_rate?`: `string`; `total_maintenance_margin_rate?`: `string`; `total_available_margin?`: `string`; `unified_account_total?`: `string`; `unified_account_total_liab?`: `string`; `unified_account_total_equity?`: `string`; `leverage?`: `string`; `spot_order_loss?`: `string`; `options_order_loss?`: `string`; `spot_hedge?`: `bool`; `use_funding?`: `bool`; `is_all_collateral?`: `bool`.

<a id="model-unifiedbalance"></a>
### UnifiedBalance

`available?`: `string`; `freeze?`: `string`; `borrowed?`: `string`; `negative_liab?`: `string`; `futures_pos_liab?`: `string`; `equity?`: `string`; `total_freeze?`: `string`; `total_liab?`: `string`; `spot_in_use?`: `string`; `funding?`: `string`; `funding_version?`: `string`; `cross_balance?`: `string`; `iso_balance?`: `string`; `im?`: `string`; `mm?`: `string`; `imr?`: `string`; `mmr?`: `string`; `margin_balance?`: `string`; `available_margin?`: `string`; `enabled_collateral?`: `bool`; `balance_version?`: `float32`.

<a id="model-unifiedborrowable"></a>
### UnifiedBorrowable

`currency?`: `string`; `amount?`: `string`.

<a id="model-unifiedcollateralreq"></a>
### UnifiedCollateralReq

`collateral_type?`: `int32`; `enable_list?`: `[]string`; `disable_list?`: `[]string`.

<a id="model-unifiedcollateralres"></a>
### UnifiedCollateralRes

`is_success?`: `bool`.

<a id="model-unifiedcurrency"></a>
### UnifiedCurrency

`name?`: `string`; `prec?`: `string`; `min_borrow_amount?`: `string`; `user_max_borrow_amount?`: `string`; `total_max_borrow_amount?`: `string`; `loan_status?`: `string`.

<a id="model-unifieddiscount"></a>
### UnifiedDiscount

`currency?`: `string`; `discount_tiers?`: [][UnifiedDiscountTiers](#model-unifieddiscounttiers).

<a id="model-unifieddiscounttiers"></a>
### UnifiedDiscountTiers

`tier?`: `string`; `discount?`: `string`; `lower_limit?`: `string`; `upper_limit?`: `string`; `leverage?`: `string`.

<a id="model-unifiedleverageconfig"></a>
### UnifiedLeverageConfig

`current_leverage?`: `string`; `min_leverage?`: `string`; `max_leverage?`: `string`; `debit?`: `string`; `available_margin?`: `string`; `borrowable?`: `string`; `except_leverage_borrowable?`: `string`.

<a id="model-unifiedleveragesetting"></a>
### UnifiedLeverageSetting

`currency`: `string`; `leverage`: `string`.

<a id="model-unifiedmargintiers"></a>
### UnifiedMarginTiers

`currency?`: `string`; `margin_tiers?`: [][MarginTiers](#model-margintiers).

<a id="model-unifiedmodeset"></a>
### UnifiedModeSet

`mode`: `string`; `settings?`: [UnifiedSettings](#model-unifiedsettings).

<a id="model-unifiedportfolioinput"></a>
### UnifiedPortfolioInput

`spot_balances?`: [][MockSpotBalance](#model-mockspotbalance); `spot_orders?`: [][MockSpotOrder](#model-mockspotorder); `futures_positions?`: [][MockFuturesPosition](#model-mockfuturesposition); `futures_orders?`: [][MockFuturesOrder](#model-mockfuturesorder); `options_positions?`: [][MockOptionsPosition](#model-mockoptionsposition); `options_orders?`: [][MockOptionsOrder](#model-mockoptionsorder); `spot_hedge?`: `bool`.

<a id="model-unifiedportfoliooutput"></a>
### UnifiedPortfolioOutput

`maintain_margin_total?`: `string`; `initial_margin_total?`: `string`; `calculate_time?`: `int64`; `risk_unit?`: [][MockRiskUnit](#model-mockriskunit).

<a id="model-unifiedriskunits"></a>
### UnifiedRiskUnits

`user_id?`: `int64`; `spot_hedge?`: `bool`; `risk_units?`: [][RiskUnits](#model-riskunits).

<a id="model-unifiedsettings"></a>
### UnifiedSettings

`usdt_futures?`: `bool`; `spot_hedge?`: `bool`; `use_funding?`: `bool`; `options?`: `bool`.

<a id="model-unifiedtransferable"></a>
### UnifiedTransferable

`currency?`: `string`; `amount?`: `string`.

<a id="model-deltaneutralenabled"></a>
### DeltaNeutralEnabled

`enabled`: `bool`.

<a id="model-leveragefailedcurrencies"></a>
### LeverageFailedCurrencies

`currency?`: `string`; `reason?`: `string`.

<a id="model-quickestimatedrepayment"></a>
### QuickEstimatedRepayment

`debt_currencies?`: [][UnifiedQuickRepayDebtItem](#model-unifiedquickrepaydebtitem); `available_currencies?`: [][UnifiedQuickRepayAvailableItem](#model-unifiedquickrepayavailableitem).

<a id="model-quickrepaymentrequest"></a>
### QuickRepaymentRequest

`debt_currencies`: `[]string`; `available_currencies`: `[]string`.

<a id="model-quickrepaymentresponse"></a>
### QuickRepaymentResponse

`order_id`: `string`; `repaid_infos`: [][UnifiedQuickRepayRepaidInfo](#model-unifiedquickrepayrepaidinfo); `used_infos`: [][UnifiedQuickRepayUsedInfo](#model-unifiedquickrepayusedinfo).

<a id="model-unifiedquickrepayavailableitem"></a>
### UnifiedQuickRepayAvailableItem

`currency?`: `string`; `available?`: `string`; `estimated_usd?`: `string`.

<a id="model-unifiedquickrepaydebtitem"></a>
### UnifiedQuickRepayDebtItem

`currency?`: `string`; `debt_amount?`: `string`; `estimated_usd?`: `string`; `borrowed?`: `string`; `neg_balance?`: `string`.

<a id="model-unifiedquickrepayrepaidinfo"></a>
### UnifiedQuickRepayRepaidInfo

`currency`: `string`; `repaid`: `string`; `left`: `string`.

<a id="model-unifiedquickrepayusedinfo"></a>
### UnifiedQuickRepayUsedInfo

`currency`: `string`; `used`: `string`.

<a id="model-userleveragesetting"></a>
### UserLeverageSetting

`leverage?`: `string`.
