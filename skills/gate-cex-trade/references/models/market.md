# Market data Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-batchfundingratesrequest"></a>
### BatchFundingRatesRequest

`contracts`: `[]string`.

<a id="model-batchfundingratesresponse"></a>
### BatchFundingRatesResponse

`contract?`: `string`; `data?`: [][FundingRateRecord](#model-fundingraterecord).

<a id="model-contract"></a>
### Contract

`name?`: `string`; `type?`: `string`; `quanto_multiplier?`: `string`; `leverage_min?`: `string`; `leverage_max?`: `string`; `maintenance_rate?`: `string`; `mark_type?`: `string`; `mark_price?`: `string`; `index_price?`: `string`; `last_price?`: `string`; `maker_fee_rate?`: `string`; `taker_fee_rate?`: `string`; `order_price_round?`: `string`; `mark_price_round?`: `string`; `funding_rate?`: `string`; `funding_interval?`: `int32`; `funding_next_apply?`: `float64`; `risk_limit_base?`: `string`; `interest_rate?`: `string`; `risk_limit_step?`: `string`; `risk_limit_max?`: `string`; `order_size_min?`: `string`; `enable_decimal?`: `bool`; `order_size_max?`: `string`; `order_price_deviate?`: `string`; `ref_discount_rate?`: `string`; `ref_rebate_rate?`: `string`; `orderbook_id?`: `int64`; `trade_id?`: `int64`; `trade_size?`: `string`; `position_size?`: `string`; `config_change_time?`: `float64`; `in_delisting?`: `bool`; `orders_limit?`: `int32`; `enable_bonus?`: `bool`; `enable_credit?`: `bool`; `create_time?`: `float64`; `funding_cap_ratio?`: `string`; `status?`: `string`; `launch_time?`: `int64`; `delisting_time?`: `int64`; `delisted_time?`: `int64`; `market_order_slip_ratio?`: `string`; `market_order_size_max?`: `string`; `funding_rate_limit?`: `string`; `contract_type?`: `string`; `funding_impact_value?`: `string`; `enable_circuit_breaker?`: `bool`.

Field semantics: `create_time` — Created time of the contract; `status` — Contract status types include: prelaunch (pre-launch), trading (active), delisting (delisting), delisted (delisted), circuit_breaker (circuit breaker); `launch_time` — Contract expiry timestamp; `delisting_time` — Timestamp when contract enters reduce-only state; `delisted_time` — Contract delisting time.

<a id="model-contractstat"></a>
### ContractStat

`time?`: `int64`; `lsr_taker?`: `float64`; `lsr_account?`: `float64`; `long_liq_size?`: `string`; `long_liq_amount?`: `float64`; `long_liq_usd?`: `float64`; `long_liq_usd_new?`: `float64`; `short_liq_size?`: `string`; `short_liq_amount?`: `float64`; `short_liq_usd?`: `float64`; `short_liq_usd_new?`: `float64`; `open_interest?`: `string`; `open_interest_usd?`: `float64`; `top_lsr_account?`: `float64`; `top_lsr_size?`: `string`; `mark_price?`: `float64`; `top_long_size?`: `string`; `top_short_size?`: `string`; `long_taker_size?`: `string`; `short_taker_size?`: `string`; `top_long_account?`: `int64`; `top_short_account?`: `int64`; `long_users?`: `int64`; `short_users?`: `int64`.

<a id="model-currency"></a>
### Currency

`currency?`: `string`; `name?`: `string`; `delisted?`: `bool`; `withdraw_disabled?`: `bool`; `withdraw_delayed?`: `bool`; `deposit_disabled?`: `bool`; `trade_disabled?`: `bool`; `fixed_rate?`: `string`; `chain?`: `string`; `chains?`: [][SpotCurrencyChain](#model-spotcurrencychain); `total_supply?`: `string`; `market_cap?`: `string`; `category?`: `[]string`.

<a id="model-currencypair"></a>
### CurrencyPair

`id?`: `string`; `base?`: `string`; `base_name?`: `string`; `quote?`: `string`; `quote_name?`: `string`; `trade_quotes?`: `*[]string`; `fee?`: `string`; `min_base_amount?`: `string`; `min_quote_amount?`: `string`; `max_base_amount?`: `string`; `max_quote_amount?`: `string`; `amount_precision?`: `int32`; `precision?`: `int32`; `trade_status?`: `string`; `sell_start?`: `int64`; `buy_start?`: `int64`; `delisting_time?`: `int64`; `type?`: `string`; `trade_url?`: `string`; `st_tag?`: `bool`; `up_rate?`: `string`; `down_rate?`: `string`; `slippage?`: `string`; `market_order_max_stock?`: `string`; `market_order_max_money?`: `string`.

Field semantics: `delisting_time` — Expected time to remove the shelves, Unix timestamp in seconds.

<a id="model-deliverycandlestick"></a>
### DeliveryCandlestick

`t?`: `float64`; `v?`: `int64`; `c?`: `string`; `h?`: `string`; `l?`: `string`; `o?`: `string`.

Field semantics: `t` — Unix timestamp in seconds.

<a id="model-deliverycontract"></a>
### DeliveryContract

`name?`: `string`; `underlying?`: `string`; `cycle?`: `string`; `type?`: `string`; `quanto_multiplier?`: `string`; `leverage_min?`: `string`; `leverage_max?`: `string`; `maintenance_rate?`: `string`; `mark_type?`: `string`; `mark_price?`: `string`; `index_price?`: `string`; `last_price?`: `string`; `maker_fee_rate?`: `string`; `taker_fee_rate?`: `string`; `order_price_round?`: `string`; `mark_price_round?`: `string`; `basis_rate?`: `string`; `basis_value?`: `string`; `basis_impact_value?`: `string`; `settle_price?`: `string`; `settle_price_interval?`: `int32`; `settle_price_duration?`: `int32`; `expire_time?`: `int64`; `risk_limit_base?`: `string`; `risk_limit_step?`: `string`; `risk_limit_max?`: `string`; `order_size_min?`: `int64`; `order_size_max?`: `int64`; `order_price_deviate?`: `string`; `ref_discount_rate?`: `string`; `ref_rebate_rate?`: `string`; `orderbook_id?`: `int64`; `trade_id?`: `int64`; `trade_size?`: `int64`; `position_size?`: `int64`; `config_change_time?`: `float64`; `in_delisting?`: `bool`; `orders_limit?`: `int32`.

Field semantics: `expire_time` — Contract expiry timestamp.

<a id="model-deliverylimitrisktiers"></a>
### DeliveryLimitRiskTiers

`tier?`: `int32`; `risk_limit?`: `string`; `initial_rate?`: `string`; `maintenance_rate?`: `string`; `leverage_max?`: `string`; `contract?`: `string`; `deduction?`: `string`.

<a id="model-deliveryorderbook"></a>
### DeliveryOrderBook

`id?`: `int64`; `current?`: `float64`; `update?`: `float64`; `asks`: [][DeliveryOrderBookItem](#model-deliveryorderbookitem); `bids`: [][DeliveryOrderBookItem](#model-deliveryorderbookitem).

Field semantics: `id` — Order Book ID. Increases by 1 on every order book change. Set `with_id=true` to include this field in response.

<a id="model-deliveryorderbookitem"></a>
### DeliveryOrderBookItem

`p?`: `string`; `s?`: `int64`.

<a id="model-deliveryticker"></a>
### DeliveryTicker

`contract?`: `string`; `last?`: `string`; `change_percentage?`: `string`; `total_size?`: `string`; `low_24h?`: `string`; `high_24h?`: `string`; `volume_24h?`: `string`; `volume_24h_btc?`: `string`; `volume_24h_usd?`: `string`; `volume_24h_base?`: `string`; `volume_24h_quote?`: `string`; `volume_24h_settle?`: `string`; `mark_price?`: `string`; `funding_rate?`: `string`; `funding_rate_indicative?`: `string`; `index_price?`: `string`; `quanto_base_rate?`: `string`; `basis_rate?`: `string`; `basis_value?`: `string`; `lowest_ask?`: `string`; `lowest_size?`: `string`; `highest_bid?`: `string`; `highest_size?`: `string`.

<a id="model-deliverytrade"></a>
### DeliveryTrade

`id?`: `int64`; `create_time?`: `float64`; `create_time_ms?`: `float64`; `contract?`: `string`; `size?`: `int64`; `price?`: `string`; `is_internal?`: `bool`.

Field semantics: `create_time_ms` — Trade time, with millisecond precision to 3 decimal places.

<a id="model-fundingraterecord"></a>
### FundingRateRecord

`t?`: `int64`; `r?`: `string`.

Field semantics: `t` — Unix timestamp in seconds.

<a id="model-futurescandlestick"></a>
### FuturesCandlestick

`t?`: `float64`; `v?`: `string`; `c?`: `string`; `h?`: `string`; `l?`: `string`; `o?`: `string`; `sum?`: `string`.

Field semantics: `t` — Unix timestamp in seconds.

<a id="model-futuresindexconstituents"></a>
### FuturesIndexConstituents

`index?`: `string`; `constituents?`: [][IndexConstituent](#model-indexconstituent).

<a id="model-futureslimitrisktiers"></a>
### FuturesLimitRiskTiers

`tier?`: `int32`; `risk_limit?`: `string`; `initial_rate?`: `string`; `maintenance_rate?`: `string`; `leverage_max?`: `string`; `contract?`: `string`; `deduction?`: `string`.

<a id="model-futuresliqorder"></a>
### FuturesLiqOrder

`time?`: `int64`; `contract?`: `string`; `size?`: `string`; `order_size?`: `string`; `order_price?`: `string`; `fill_price?`: `string`; `left?`: `string`.

<a id="model-futuresorderbook"></a>
### FuturesOrderBook

`id?`: `int64`; `current?`: `float64`; `update?`: `float64`; `asks`: [][FuturesOrderBookItem](#model-futuresorderbookitem); `bids`: [][FuturesOrderBookItem](#model-futuresorderbookitem).

Field semantics: `id` — Order Book ID. Increases by 1 on every order book change. Set `with_id=true` to include this field in response.

<a id="model-futuresorderbookitem"></a>
### FuturesOrderBookItem

`p?`: `string`; `s?`: `string`.

<a id="model-futurespremiumindex"></a>
### FuturesPremiumIndex

`t?`: `float64`; `c?`: `string`; `h?`: `string`; `l?`: `string`; `o?`: `string`.

Field semantics: `t` — Unix timestamp in seconds.

<a id="model-futuresrisklimittier"></a>
### FuturesRiskLimitTier

`tier?`: `int32`; `risk_limit?`: `string`; `initial_rate?`: `string`; `maintenance_rate?`: `string`; `leverage_max?`: `string`; `deduction?`: `string`.

<a id="model-futuresticker"></a>
### FuturesTicker

`contract?`: `string`; `last?`: `string`; `change_percentage?`: `string`; `total_size?`: `string`; `low_24h?`: `string`; `high_24h?`: `string`; `volume_24h?`: `string`; `volume_24h_btc?`: `string`; `volume_24h_usd?`: `string`; `volume_24h_base?`: `string`; `volume_24h_quote?`: `string`; `volume_24h_settle?`: `string`; `mark_price?`: `string`; `funding_rate?`: `string`; `funding_rate_indicative?`: `string`; `index_price?`: `string`; `quanto_base_rate?`: `string`; `lowest_ask?`: `string`; `lowest_size?`: `string`; `highest_bid?`: `string`; `highest_size?`: `string`; `change_utc0?`: `string`; `change_utc8?`: `string`; `change_price?`: `string`; `change_utc0_price?`: `string`; `change_utc8_price?`: `string`.

<a id="model-futurestrade"></a>
### FuturesTrade

`id?`: `int64`; `create_time?`: `float64`; `create_time_ms?`: `float64`; `contract?`: `string`; `size?`: `string`; `price?`: `string`; `is_internal?`: `bool`.

Field semantics: `create_time_ms` — Trade time, with millisecond precision to 3 decimal places.

<a id="model-indexconstituent"></a>
### IndexConstituent

`exchange?`: `string`; `symbols?`: `[]string`.

<a id="model-insurancerecord"></a>
### InsuranceRecord

`t?`: `int64`; `b?`: `string`.

Field semantics: `t` — Unix timestamp in seconds.

<a id="model-optionscandlestick"></a>
### OptionsCandlestick

`t?`: `float64`; `v?`: `int64`; `c?`: `string`; `h?`: `string`; `l?`: `string`; `o?`: `string`.

Field semantics: `t` — Unix timestamp in seconds.

<a id="model-optionscontract"></a>
### OptionsContract

`name?`: `string`; `tag?`: `string`; `create_time?`: `float64`; `expiration_time?`: `float64`; `is_call?`: `bool`; `multiplier?`: `string`; `underlying?`: `string`; `underlying_price?`: `string`; `last_price?`: `string`; `mark_price?`: `string`; `index_price?`: `string`; `maker_fee_rate?`: `string`; `taker_fee_rate?`: `string`; `order_price_round?`: `string`; `mark_price_round?`: `string`; `order_size_min?`: `int64`; `order_size_max?`: `int64`; `order_price_deviate?`: `string`; `ref_discount_rate?`: `string`; `ref_rebate_rate?`: `string`; `orderbook_id?`: `int64`; `trade_id?`: `int64`; `trade_size?`: `int64`; `position_size?`: `int64`; `orders_limit?`: `int32`.

<a id="model-optionsorderbook"></a>
### OptionsOrderBook

`id?`: `int64`; `current?`: `float64`; `update?`: `float64`; `asks`: [][DeliveryOrderBookItem](#model-deliveryorderbookitem); `bids`: [][DeliveryOrderBookItem](#model-deliveryorderbookitem).

Field semantics: `id` — Order Book ID. Increases by 1 on every order book change. Set `with_id=true` to include this field in response.

<a id="model-optionssettlement"></a>
### OptionsSettlement

`time?`: `float64`; `contract?`: `string`; `profit?`: `string`; `fee?`: `string`; `strike_price?`: `string`; `settle_price?`: `string`.

<a id="model-optionsticker"></a>
### OptionsTicker

`name?`: `string`; `last_price?`: `string`; `mark_price?`: `string`; `index_price?`: `string`; `ask1_size?`: `int64`; `ask1_price?`: `string`; `bid1_size?`: `int64`; `bid1_price?`: `string`; `position_size?`: `int64`; `mark_iv?`: `string`; `bid_iv?`: `string`; `ask_iv?`: `string`; `leverage?`: `string`; `delta?`: `string`; `gamma?`: `string`; `vega?`: `string`; `theta?`: `string`; `rho?`: `string`.

<a id="model-optionstrade"></a>
### OptionsTrade

`id?`: `int64`; `create_time?`: `int64`; `contract?`: `string`; `size?`: `int64`; `price?`: `string`.

<a id="model-optionsunderlying"></a>
### OptionsUnderlying

`name?`: `string`; `index_price?`: `string`.

<a id="model-optionsunderlyingticker"></a>
### OptionsUnderlyingTicker

`trade_put?`: `int64`; `trade_call?`: `int64`; `index_price?`: `string`.

<a id="model-orderbook"></a>
### OrderBook

`id?`: `int64`; `current?`: `int64`; `update?`: `int64`; `asks`: `[][]string`; `bids`: `[][]string`.

Field semantics: `id` — Order book ID, which is updated whenever the order book is changed. Valid only when `with_id` is set to `true`.

<a id="model-spotcurrencychain"></a>
### SpotCurrencyChain

`name?`: `string`; `addr?`: `string`; `withdraw_disabled?`: `bool`; `withdraw_delayed?`: `bool`; `deposit_disabled?`: `bool`.

<a id="model-spotinsurancehistory"></a>
### SpotInsuranceHistory

`currency?`: `string`; `balance?`: `string`; `time?`: `int64`.

Field semantics: `time` — Creation time, timestamp, milliseconds.

<a id="model-systemtime"></a>
### SystemTime

`server_time?`: `int64`.

<a id="model-ticker"></a>
### Ticker

`currency_pair?`: `string`; `last?`: `string`; `lowest_ask?`: `string`; `lowest_size?`: `string`; `highest_bid?`: `string`; `highest_size?`: `string`; `change_percentage?`: `string`; `change_utc0?`: `string`; `change_utc8?`: `string`; `base_volume?`: `string`; `quote_volume?`: `string`; `high_24h?`: `string`; `low_24h?`: `string`; `etf_net_value?`: `string`; `etf_pre_net_value?`: `*string`; `etf_pre_timestamp?`: `*int64`; `etf_leverage?`: `*string`.

<a id="model-trade"></a>
### Trade

`id?`: `string`; `create_time?`: `string`; `create_time_ms?`: `string`; `currency_pair?`: `string`; `side?`: `string`; `role?`: `string`; `amount?`: `string`; `price?`: `string`; `order_id?`: `string`; `fee?`: `string`; `fee_currency?`: `string`; `point_fee?`: `string`; `gt_fee?`: `string`; `amend_text?`: `string`; `sequence_id?`: `string`; `text?`: `string`; `deal?`: `string`; `trade_quote?`: `string`.

Field semantics: `create_time_ms` — Trading time, with millisecond precision; `side` — Buy or sell order.

<a id="model-futuresadlriskstate"></a>
### FuturesAdlRiskState

`state`: `string`; `calculated_at_ms`: `int64`.

<a id="model-futuresadlriskstates"></a>
### FuturesAdlRiskStates

`settle`: `string`; `states`: map[string][FuturesAdlRiskState](#model-futuresadlriskstate).
