# Spot, margin and infinite grids Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-aihubcreatedata"></a>
### AiHubCreateData

`strategy_id`: `string`; `strategy_type`: [StrategyType](#model-strategytype); `market`: `string`; `status`: `string`; `jump_url?`: `string`; `operation_status?`: `string`; `recovery_required?`: `bool`.

<a id="model-aihubcreatesuccessresponse"></a>
### AiHubCreateSuccessResponse

`code`: `int32`; `message`: `string`; `data`: [AiHubCreateData](#model-aihubcreatedata); `trace_id`: `string`.

<a id="model-futuresdirection"></a>
### FuturesDirection

Representation: `string`. Values: `long`, `short`, `neutral`.

<a id="model-infinitegridcreateparams"></a>
### InfiniteGridCreateParams

`money`: `string`; `price_floor`: `string`; `profit_per_grid`: `string`; `grid_num?`: `int32`; `price_type?`: `int32`; `trigger_price?`: `string`; `stop_profit?`: `string`; `stop_loss?`: `string`; `profit_sharing_ratio?`: `string`; `is_use_base?`: `bool`.

<a id="model-infinitegridcreaterequest"></a>
### InfiniteGridCreateRequest

`strategy_type`: `string`; `market`: `string`; `create_params`: [InfiniteGridCreateParams](#model-infinitegridcreateparams).

<a id="model-margingridcreateparams"></a>
### MarginGridCreateParams

`money`: `string`; `low_price`: `string`; `high_price`: `string`; `grid_num`: `int32`; `price_type`: `int32`; `leverage`: `string`; `direction?`: [FuturesDirection](#model-futuresdirection); `trigger_price?`: `string`; `stop_profit?`: `string`; `stop_loss?`: `string`; `profit_sharing_ratio?`: `string`; `is_use_base?`: `bool`.

<a id="model-margingridcreaterequest"></a>
### MarginGridCreateRequest

`strategy_type`: `string`; `market`: `string`; `create_params`: [MarginGridCreateParams](#model-margingridcreateparams).

<a id="model-spotgridcreateparams"></a>
### SpotGridCreateParams

`money`: `string`; `low_price`: `string`; `high_price`: `string`; `grid_num`: `int32`; `price_type`: `int32`; `trigger_price?`: `string`; `stop_profit?`: `string`; `stop_loss?`: `string`; `profit_sharing_ratio?`: `string`; `is_use_base?`: `bool`.

<a id="model-spotgridcreaterequest"></a>
### SpotGridCreateRequest

`strategy_type`: `string`; `market`: `string`; `create_params`: [SpotGridCreateParams](#model-spotgridcreateparams).

<a id="model-strategytype"></a>
### StrategyType

Representation: `string`. Values: `spot_grid`, `margin_grid`, `infinite_grid`, `futures_grid`, `spot_martingale`, `contract_martingale`, `smart_position`, `futures_combo`. Match the selected creation endpoint.

## Grid field constraints

The bundled request model restricts `grid_num` to at least 1 and `price_type` to integer `0` or `1`. Infinite grid requires only `money`, `price_floor` and `profit_per_grid`; its optional `price_type` means `0` for arithmetic spacing and `1` for geometric spacing. Other grid schemas declare the two accepted integers without a textual mapping: use verified selected-product terms or an explicitly chosen/recommended value before translating a spacing preference. Do not invent further enum values.
