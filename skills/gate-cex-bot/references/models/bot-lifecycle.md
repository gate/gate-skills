# Bot discovery and lifecycle Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-aihubdiscoverdata"></a>
### AiHubDiscoverData

`scene`: [DiscoverScene](#model-discoverscene); `recommendations`: [][AiHubRecommendation](#model-aihubrecommendation); `unsupported_filters`: `[]string`.

<a id="model-aihubdiscoversuccessresponse"></a>
### AiHubDiscoverSuccessResponse

`code`: `int32`; `message`: `string`; `data`: [AiHubDiscoverData](#model-aihubdiscoverdata); `trace_id`: `string`.

<a id="model-aihubportfoliobaseinfo"></a>
### AiHubPortfolioBaseInfo

`strategy_name`: `string`; `created_at`: `string`; `running_duration`: `int64`; `invest_amount`: `string`; `total_profit`: `string`; `profit_rate`: `string`.

<a id="model-aihubportfoliodetaildata"></a>
### AiHubPortfolioDetailData

`strategy_id`: `string`; `strategy_type`: [StrategyType](#model-strategytype); `market`: `string`; `status`: `string`; `base_info`: [AiHubPortfolioBaseInfo](#model-aihubportfoliobaseinfo); `metrics`: [AiHubPortfolioMetrics](#model-aihubportfoliometrics); `position?`: *[AiHubPortfolioPosition](#model-aihubportfolioposition); `stop_supported`: `bool`.

<a id="model-aihubportfoliodetailsuccessresponse"></a>
### AiHubPortfolioDetailSuccessResponse

`code`: `int32`; `message`: `string`; `data`: [AiHubPortfolioDetailData](#model-aihubportfoliodetaildata); `trace_id`: `string`.

<a id="model-aihubportfoliometrics"></a>
### AiHubPortfolioMetrics

`grid_profit?`: `string`; `floating_pnl?`: `string`; `arbitrage_count?`: `int64`; `price_range?`: `string`; `grid_count?`: `int64`; `estimated_liquidation_price?`: `string`; `price_floor?`: `string`; `grid_profit_rate?`: `string`; `realized_pnl?`: `string`; `finished_rounds?`: `int64`; `avg_cost?`: `string`; `take_profit_price?`: `string`; `maintenance_margin_ratio?`: `string`.

<a id="model-aihubportfolioposition"></a>
### AiHubPortfolioPosition

`amount?`: `string`; `entry_price?`: `string`; `quote_amount?`: `string`; `position_value?`: `string`; `margin?`: `string`; `side?`: `string`.

<a id="model-aihubportfoliorunningdata"></a>
### AiHubPortfolioRunningData

`items`: [][AiHubPortfolioRunningItem](#model-aihubportfoliorunningitem); `page`: `int32`; `page_size`: `int32`; `total`: `int32`.

<a id="model-aihubportfoliorunningitem"></a>
### AiHubPortfolioRunningItem

`strategy_id`: `string`; `strategy_type`: [StrategyType](#model-strategytype); `strategy_name`: `string`; `market`: `string`; `status`: `string`; `pnl?`: `string`; `pnl_rate?`: `string`; `invest_amount?`: `string`; `created_at?`: `string`.

<a id="model-aihubportfoliorunningsuccessresponse"></a>
### AiHubPortfolioRunningSuccessResponse

`code`: `int32`; `message`: `string`; `data`: [AiHubPortfolioRunningData](#model-aihubportfoliorunningdata); `trace_id`: `string`.

<a id="model-aihubportfoliostopdata"></a>
### AiHubPortfolioStopData

`strategy_id`: `string`; `strategy_type`: [StrategyType](#model-strategytype); `status`: `string`; `result_message`: `string`.

<a id="model-aihubportfoliostoprequest"></a>
### AiHubPortfolioStopRequest

`strategy_id`: `string`; `strategy_type`: [StrategyType](#model-strategytype); `stop_mode?`: `string` (market/limit/no_close); `stop_options?`: [StopOptions](portfolios.md#model-stopoptions).

<a id="model-aihubportfoliostopsuccessresponse"></a>
### AiHubPortfolioStopSuccessResponse

`code`: `int32`; `message`: `string`; `data`: [AiHubPortfolioStopData](#model-aihubportfoliostopdata); `trace_id`: `string`.

<a id="model-aihubrecommendation"></a>
### AiHubRecommendation

`recommendation_id`: `string`; `market`: `string`; `strategy_type`: [StrategyType](#model-strategytype); `strategy_name`: `string`; `backtest_apr?`: `string`; `max_drawdown?`: `string`; `summary`: `string`; `strategy_params_preview?`: `string`.

<a id="model-discoverscene"></a>
### DiscoverScene

Representation: `string`. Values: `top1`, `bundle`, `filter`, `refresh`.

<a id="model-strategytype"></a>
### StrategyType

Representation: `string`. Values: `spot_grid`, `margin_grid`, `infinite_grid`, `futures_grid`, `spot_martingale`, `contract_martingale`, `smart_position`, `futures_combo`. Match the selected creation endpoint.

## Portfolio extension fields

Detail data may include `positions`, `positions_status`, `configuration` and `stop_progress`; running items may include `assets`, `markets` and `positions`. Preserve original JSON types and exact decimal strings. Configuration is a product-specific object, not a creation template. Explicit false progress values remain false. Unreturned or empty metrics do not establish zero exposure.

Create and stop data can include `operation_status` and `recovery_required`. ID plus unknown/pending status is an unresolved accepted operation, not permission to recreate it. Price, expiration and slip rules for smart-position are in [the portfolio request model](portfolios.md#model-stopoptions).
