# Spot and contract martingale Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-aihubcreatedata"></a>
### AiHubCreateData

`strategy_id`: `string`; `strategy_type`: [StrategyType](#model-strategytype); `market`: `string`; `status`: `string`; `jump_url?`: `string`; `operation_status?`: `string`; `recovery_required?`: `bool`.

<a id="model-aihubcreatesuccessresponse"></a>
### AiHubCreateSuccessResponse

`code`: `int32`; `message`: `string`; `data`: [AiHubCreateData](#model-aihubcreatedata); `trace_id`: `string`.

<a id="model-contractmartingalecreateparams"></a>
### ContractMartingaleCreateParams

`invest_amount`: `string`; `price_deviation`: `string`; `max_orders`: `int32`; `take_profit_ratio`: `string`; `direction`: [ContractMartingaleDirection](#model-contractmartingaledirection); `leverage`: `string`; `stop_loss_price?`: `string`; `stop_loss_price_type?`: `string` (last/index/mark, required with a fixed stop price); `profit_sharing_ratio?`: `string`.

<a id="model-contractmartingalecreaterequest"></a>
### ContractMartingaleCreateRequest

`strategy_type`: `string`; `market`: `string`; `create_params`: [ContractMartingaleCreateParams](#model-contractmartingalecreateparams).

<a id="model-contractmartingaledirection"></a>
### ContractMartingaleDirection

Representation: `string`. Values: `buy`, `sell`.

<a id="model-spotmartingalecreateparams"></a>
### SpotMartingaleCreateParams

`invest_amount`: `string`; `price_deviation`: `string`; `max_orders`: `int32`; `take_profit_ratio`: `string`; `stop_loss_per_cycle?`: `string`; `trigger_price?`: `string`; `profit_sharing_ratio?`: `string`.

<a id="model-spotmartingalecreaterequest"></a>
### SpotMartingaleCreateRequest

`strategy_type`: `string`; `market`: `string`; `create_params`: [SpotMartingaleCreateParams](#model-spotmartingalecreateparams).

<a id="model-strategytype"></a>
### StrategyType

Representation: `string`. Values: `spot_grid`, `margin_grid`, `infinite_grid`, `futures_grid`, `spot_martingale`, `contract_martingale`, `smart_position`, `futures_combo`. Match the selected creation endpoint.

## Martingale field constraints

The bundled request model requires `max_orders` of at least 1. Spot `price_deviation` and `take_profit_ratio` are decimal ratios: a 2% deviation is `"0.02"`. `stop_loss_per_cycle` is the optional per-round loss ratio; the contract describes an approximate positive validation range of 0.001 through 0.9999, so verify the exact current boundary before using it. Contract `invest_amount` is allocated margin, converted by the backend using price, multiplier and lot size; it is not contract quantity. `stop_loss_price` is a fixed price and requires `stop_loss_price_type` (last/index/mark). The backend validates total ladder budget; max_orders counts additions after the first entry. Missing or unsupported protection remains unexecuted.
