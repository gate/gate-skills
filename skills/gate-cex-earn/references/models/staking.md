# Staking Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-stakingproduct"></a>
### StakingProduct

`pid?`: `int32`; `protocolName?`: `string`; `currency?`: `string`;
`estimateApr?`: `string`; `minStakeAmount?`: `string`;
`maxStakeAmount?`: `number`; `redeemPeriod?`: `int32`;
`productType?`: `int32`; `isDefi?`: `int32`; `exchangeRate?`: `string`;
`exchangeRateReserve?`: `string`; `currencyRewards?`: `[]map[string]any`.

This is the product shape used by `staking find`. Compare a product by its exact
`pid`, funding currency, lock/redemption period and conversion rate. Do not assume
the return is 1:1 when `exchangeRate` differs from 1.

<a id="model-stakingasset"></a>
### StakingAsset

`pid?`: `int32`; `mortgage_coin?`: `string`; `mortgage_amount?`: `string`;
`freeze_amount?`: `string`; `income_total?`: `string`;
`yesterday_income?`: `string`; `yesterday_income_multi?`: `[]map[string]any`;
`reward_coins?`: `[]map[string]any`; `defi_income?`: `map[string]any`;
`type?`: `int32`; `protocol_name?`: `string`; `redeem_amount?`: `string`;
`status?`: `int32`.

This is the position shape used by `staking assets`. `mortgage_amount` and
`freeze_amount` must not be subtracted to fabricate a redeemable amount. Prefer a
documented returned `redeem_amount`; otherwise reconcile the product conversion
rate for the same `pid` before explaining available redemption.

## User-facing field mapping

Use these labels in normal answers; retain the raw keys only for command execution
or an explicitly requested technical receipt.

| Raw response field | User-facing meaning | Display rule |
| --- | --- | --- |
| `protocolName` / `protocol_name` | Product name | Show as the product label. |
| `currency` / `mortgage_coin` | Staked asset | Show with the relevant amount. |
| `estimateApr` | Estimated annual rate | Label as estimated, not guaranteed. |
| `minStakeAmount` / `maxStakeAmount` | Minimum / maximum participation amount | Show only when evaluating eligibility or an action. |
| `mortgage_amount` | Position amount | Show as “staked amount” or “current position”; it is not automatically redeemable. |
| `freeze_amount` | Locked amount | Show only when non-zero; do not call it a completed redemption. |
| `income_total` / `yesterday_income` | Accumulated / previous-day earnings | Include the asset and period; omit when unavailable. |
| `redeem_amount` | Available redemption amount | Prefer this field for a redemption answer when it is returned. |
| Asset-list `status` | Product availability | `1` means listed and `2` means delisted; do not show the numeric code or use it as an operation result. |
| `type` | Product category | `0` voucher, `1` locked position, `2` US Treasury bond; use a product label only when it helps the request. |
| `pid`, `id`, `uid`, `protocol_type`, timestamps | Internal product, operation, identity, or transport metadata | Do not display by default. |

For reward records, show `reward_coin` as the reward asset, `interest` as the
credited reward amount, `fee` as a fee only when non-zero, and `bonus_date` as the
distribution date. Its `status` value `4` means the reward record succeeded; show
that as “reward distributed successfully,” never as the numeric code. Treat
`amount` as the returned record amount only when its business meaning is confirmed
by the action context. For a stake or redemption response, describe `coin` and
`amount` as the requested asset and quantity, and `exchange_amount` as the
converted quantity when returned. Its `status` value `1` means the swap succeeded;
state the requested stake or redemption succeeded, then still verify the resulting
position when the workflow requires it. Describe `exchange_rate` as the conversion
rate, not a yield. `side`, `subtype`, `source`, `client_order_id`, raw `status`,
and all timestamps are command or transport detail and must not be shown by default.

<a id="model-awardliststruct"></a>
### AwardListStruct

`page`: `int32`; `pageSize`: `int32`; `pageCount`: `int32`; `totalCount`: `int32`; `list`: [][AwardListStructList](#model-awardliststructlist).

<a id="model-awardliststructlist"></a>
### AwardListStructList

`pid`: `int32`; `mortgage_coin`: `string`; `amount`: `string`; `reward_coin`: `string`; `interest`: `string`; `fee`: `string`; `status`: `int32`; `bonus_date`: `string`; `should_bonus_stamp`: `int32`.

<a id="model-swapcoin"></a>
### SwapCoin

`coin`: `string`; `side`: `int32`; `amount`: `string`; `pid?`: `int32`.

<a id="model-swapcoinstruct"></a>
### SwapCoinStruct

`id?`: `int32`; `pid?`: `int32`; `uid?`: `int32`; `coin?`: `string`; `type?`: `int32`; `subtype?`: `string`; `amount?`: `string`; `exchange_rate?`: `string`; `exchange_amount?`: `string`; `updateStamp?`: `int32`; `createStamp?`: `int32`; `status?`: `int32`; `protocol_type?`: `int32`; `client_order_id?`: `string`; `source?`: `string`.

Field semantics: `id` — Order ID.
