# Simple Earn and fixed-term lending Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-createearnfixedtermlendresponse"></a>
### CreateEarnFixedTermLendResponse

`code?`: `int32`; `message?`: `string`; `data?`: [CreateEarnFixedTermLendResponseData](#model-createearnfixedtermlendresponsedata); `timestamp?`: `int32`.

Field semantics: `timestamp` — Response timestamp (in seconds).

<a id="model-createearnfixedtermlendresponsedata"></a>
### CreateEarnFixedTermLendResponseData

`order_id?`: `int64`.

<a id="model-createearnfixedtermpreredeemresponse"></a>
### CreateEarnFixedTermPreRedeemResponse

`code?`: `int32`; `message?`: `string`; `data?`: `map[string]any`; `timestamp?`: `int32`.

Field semantics: `timestamp` — Response timestamp (in seconds).

<a id="model-createunilend"></a>
### CreateUniLend

`currency`: `string`; `amount`: `string`; `type`: `string`; `min_rate?`: `string`.

`type` is `lend` or `redeem`. `min_rate` is required for `lend`, despite its SDK `omitempty` tag; an excessive value can prevent lending and interest. Verify the product's rate unit rather than assuming annual or daily percentage. Do not copy a lending rate into redemption unless the actual product requires it.

<a id="model-fixedtermbonusinfo"></a>
### FixedTermBonusInfo

`id?`: `int32`; `product_id?`: `int32`; `asset?`: `string`; `bonus_asset?`: `string`; `kyc_limit?`: `string`; `ladder_apr?`: [][LadderApr](#model-ladderapr); `total_bonus_amount?`: `string`; `user_total_bonus_amount?`: `string`; `status?`: `int32`; `start_time?`: `string`; `end_time?`: `string`; `create_time?`: `string`; `start_at?`: `int32`; `end_at?`: `int32`; `total_issued_amount?`: `string`; `user_total_issued_amount?`: `string`; `bonus_asset_price?`: `string`; `product_asset_price?`: `string`; `product_year_rate?`: `string`.

Field semantics: `status` — Activity status: 1 for unlisted, 2 for listed, 3 for delisted.

<a id="model-fixedtermcouponinfo"></a>
### FixedTermCouponInfo

`id`: `int32`; `business`: `int32`; `user_id`: `int64`; `asset`: `string`; `order_id`: `int64`; `financial_rate_id`: `int32`; `buy_limit_low`: `string`; `buy_limit_high`: `string`; `rate_day`: `int32`; `rate_ratio`: `string`; `coupon_days`: `int32`; `coupon_principal`: `string`; `coupon_year_rate`: `string`; `coupon_interest`: `string`; `status`: `int32`; `finish_time`: `string`; `create_time`: `string`.

Field semantics: `status` — Status: 1 for active, 2 for settled.

<a id="model-fixedtermhistoryrecord"></a>
### FixedTermHistoryRecord

`id`: `int32`; `order_id?`: `int64`; `user_id`: `int64`; `asset`: `string`; `uniq_time?`: `string`; `bonus_id?`: `int32`; `product_id`: `int32`; `bonus_asset?`: `string`; `total_principal?`: `string`; `amount?`: `string`; `asset_price?`: `string`; `status`: `int32`; `detail?`: `string`; `create_time`: `string`; `create_at`: `int32`; `lock_up_period?`: `int32`.

<a id="model-fixedtermlendorder"></a>
### FixedTermLendOrder

`id?`: `int32`; `business?`: `int32`; `order_id?`: `int64`; `user_id?`: `int64`; `asset?`: `string`; `product_id?`: `int32`; `lock_up_period?`: `int32`; `principal?`: `string`; `year_rate?`: `string`; `product_type?`: `int32`; `interest?`: `string`; `status?`: `int32`; `reinvest_status?`: `int32`; `redeem_account_type?`: `int32`; `origin_order?`: `string`; `redeem_type?`: `int32`; `redeem_time?`: `string`; `finish_time?`: `string`; `create_time?`: `string`; `year_rate_perent?`: `string`; `total_year_rate_percent?`: `string`; `total_interest?`: `string`; `product_info?`: [FixedTermProductInfo](#model-fixedtermproductinfo); `bonus_info?`: [FixedTermBonusInfo](#model-fixedtermbonusinfo); `coupon_info?`: [FixedTermCouponInfo](#model-fixedtermcouponinfo); `redeem_at?`: `int32`; `finish_at?`: `int32`; `create_at?`: `int32`; `icon?`: `string`.

Field semantics: `status` — Order status: 1 for holding, 2 for redeemed, 3 for matured, 4 for settled.

## User-facing field mapping

For product lists, show the asset, term, estimated annual rate, minimum amount,
early-redemption availability, and any material quota or renewal condition. For a
user position, show principal, accrued/estimated interest, maturity or redemption
time, and a translated lifecycle state: holding, redeemed, matured, or settled.
Do not display `id`, `product_id`, `order_id`, `user_id`, `business`, raw status
codes, timestamps, coupon internals, or API envelope fields unless the user asks
for a technical receipt or support reference. `year_rate` and `est_rate` are
quoted annual rates, not guaranteed earnings; `frozen_amount` is not a redeemable
balance. Display `reinvest_status` only as automatic renewal enabled or disabled.

<a id="model-fixedtermproduct"></a>
### FixedTermProduct

`id?`: `int32`; `name?`: `string`; `asset?`: `string`; `lock_up_period?`: `int32`; `min_lend_amount?`: `string`; `user_max_lend_amount?`: `string`; `total_lend_amount?`: `string`; `year_rate?`: `string`; `type?`: `int32`; `pre_redeem?`: `int32`; `reinvest?`: `int32`; `redeem_account?`: `int32`; `min_vip?`: `int32`; `max_vip?`: `int32`; `status?`: `int32`; `create_time?`: `string`; `user_max_lend_volume?`: `string`; `user_total_amount?`: `string`; `sale_status?`: `int32`.

Field semantics: `status` — Product status: 1 for unlisted, 2 for listed, 3 for delisted.

<a id="model-fixedtermproductinfo"></a>
### FixedTermProductInfo

`pre_redeem`: `int32`; `reinvest`: `int32`; `redeem_account`: `int32`; `min_vip`: `int32`; `max_vip`: `int32`.

<a id="model-ladderapr"></a>
### LadderApr

`apr`: `string`; `left`: `string`; `right`: `string`.

<a id="model-listearnfixedtermhistoryresponse"></a>
### ListEarnFixedTermHistoryResponse

`code?`: `int32`; `message?`: `string`; `data?`: [ListEarnFixedTermHistoryResponseData](#model-listearnfixedtermhistoryresponsedata); `timestamp?`: `int32`.

Field semantics: `timestamp` — Response timestamp (in seconds).

<a id="model-listearnfixedtermhistoryresponsedata"></a>
### ListEarnFixedTermHistoryResponseData

`list?`: [][FixedTermHistoryRecord](#model-fixedtermhistoryrecord); `total?`: `int32`.

<a id="model-listearnfixedtermlendsresponse"></a>
### ListEarnFixedTermLendsResponse

`code`: `int32`; `message`: `string`; `data`: [ListEarnFixedTermLendsResponseData](#model-listearnfixedtermlendsresponsedata); `timestamp`: `int32`.

Field semantics: `timestamp` — Response timestamp (in seconds).

<a id="model-listearnfixedtermlendsresponsedata"></a>
### ListEarnFixedTermLendsResponseData

`list`: [][FixedTermLendOrder](#model-fixedtermlendorder); `total`: `int32`.

<a id="model-listearnfixedtermproductsresponse"></a>
### ListEarnFixedTermProductsResponse

`code`: `int32`; `message`: `string`; `data`: [ListEarnFixedTermProductsResponseData](#model-listearnfixedtermproductsresponsedata); `timestamp`: `int32`.

Field semantics: `timestamp` — Response timestamp (in seconds).

<a id="model-listearnfixedtermproductsresponsedata"></a>
### ListEarnFixedTermProductsResponseData

`list`: [][FixedTermProduct](#model-fixedtermproduct); `total`: `int32`.

<a id="model-patchunilend"></a>
### PatchUniLend

`currency?`: `string`; `min_rate?`: `string`.

<a id="model-unicurrencyinterest"></a>
### UniCurrencyInterest

`currency?`: `string`; `interest_status?`: `string`.

<a id="model-uniestimatedrate"></a>
### UniEstimatedRate

`currency?`: `string`; `est_rate?`: `string`.

<a id="model-uniinterestrecord"></a>
### UniInterestRecord

`status?`: `int32`; `currency?`: `string`; `actual_rate?`: `string`; `interest?`: `string`; `interest_status?`: `string`; `create_time?`: `int64`.

Field semantics: `status` — Status: 0 - fail, 1 - success.

<a id="model-unilend"></a>
### UniLend

`currency?`: `string`; `current_amount?`: `string`; `amount?`: `string`; `lent_amount?`: `string`; `frozen_amount?`: `string`; `min_rate?`: `string`; `interest_status?`: `string`; `reinvest_left_amount?`: `string`; `create_time?`: `int64`; `update_time?`: `int64`.

<a id="model-unilendrecord"></a>
### UniLendRecord

`currency?`: `string`; `amount?`: `string`; `last_wallet_amount?`: `string`; `last_lent_amount?`: `string`; `last_frozen_amount?`: `string`; `type?`: `string`; `create_time?`: `int64`.

<a id="model-fixedtermlendrequest"></a>
### FixedTermLendRequest

Request schema source: `model_fixed_term_lend_request.go`.

| Field | Type | Required / meaning |
|---|---|---|
| `product_id` | integer (int32) | Required; discovered fixed-term product ID |
| `amount` | decimal string | Required; principal in the selected product currency |
| `year_rate` | string | Optional annual rate; retain the selected product's terms |
| `reinvest_status` | integer (int32) | Optional: 0 disables renewal, 1 enables it; enabling requires continuing authority |
| `redeem_account_type` | integer (int32) | Optional: 1 selects the spot payout account |
| `financial_rate_id` | integer (int32) | Optional interest-rate coupon ID; 0 means unused |
| `sub_business` | integer (int32) | Optional sub-business type; do not guess unsupported values |

Omitted optional fields are not an instruction to change an existing position. This is a creation schema, not a post-subscription settings endpoint.

<a id="model-earnfixedtermpredeemrequest"></a>
### EarnFixedTermPreRedeemRequest

Request schema source: `model_earn_fixed_term_pre_redeem_request.go`: `order_id` is a required string identifying the existing fixed-term order. Check its early-redemption terms before submission.
