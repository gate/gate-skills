# CFD trading Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-categories"></a>
### Categories

`timestamp?`: `int64`; `data?`: [CategoriesData](#model-categoriesdata).

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-categoriesdata"></a>
### CategoriesData

`list?`: [][CategoriesDataList](#model-categoriesdatalist).

<a id="model-categoriesdatalist"></a>
### CategoriesDataList

`category_id?`: `int32`; `is_favorite?`: `bool`; `category_name?`: `string`.

<a id="model-contractdetail"></a>
### ContractDetail

`timestamp?`: `int64`; `data?`: [ContractDetailData](#model-contractdetaildata).

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-contractdetaildata"></a>
### ContractDetailData

`list?`: [][ContractDetailDataList](#model-contractdetaildatalist).

<a id="model-contractdetaildatalist"></a>
### ContractDetailDataList

`symbol?`: `string`; `symbol_desc?`: `string`; `category_name?`: `string`; `contract_volume?`: `string`; `settlement_currency?`: `string`; `max_order_volume?`: `string`; `min_order_volume?`: `string`; `leverage?`: `string`; `price_precision?`: `int32`; `price_sl_level?`: `string`; `swap_cost_type?`: `string`; `buy_swap_cost_rate?`: `string`; `sell_swap_cost_rate?`: `string`; `swap_cost_3day?`: `string`; `trade_timezone?`: `string`; `trade_mode?`: `string`; `icon_link?`: `string`.

<a id="model-createorder2"></a>
### CreateOrder2

`timestamp?`: `int64`; `data?`: [CreateOrder2Data](#model-createorder2data).

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-createorder2data"></a>
### CreateOrder2Data

`id?`: `string`.

Field semantics: `id` — Queue Task ID (not order ID).

<a id="model-deleteposition"></a>
### DeletePosition

`timestamp?`: `int64`; `data?`: `map[string]any`.

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-klines"></a>
### Klines

`timestamp?`: `int64`; `data?`: [KlinesData](#model-klinesdata).

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-klinesdata"></a>
### KlinesData

`list?`: [][KlinesDataList](#model-klinesdatalist).

<a id="model-klinesdatalist"></a>
### KlinesDataList

`o?`: `string`; `c?`: `string`; `h?`: `string`; `l?`: `string`; `t?`: `int64`.

Field semantics: `t` — Timestamp (Unix seconds).

<a id="model-mt5account"></a>
### Mt5Account

`code?`: `int32`; `message?`: `string`; `timestamp?`: `int64`; `data?`: [Mt5AccountData](#model-mt5accountdata).

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-mt5accountdata"></a>
### Mt5AccountData

`leverage?`: `int32`; `stop_out_level?`: `string`; `status?`: `int32`.

Field semantics: `status` — Account status (1=not opened, 2=pending review, 3=active).

<a id="model-orderhistorylist"></a>
### OrderHistoryList

`timestamp?`: `int64`; `data?`: [OrderHistoryListData](#model-orderhistorylistdata).

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-orderhistorylistdata"></a>
### OrderHistoryListData

`list?`: [][OrderHistoryListDataList](#model-orderhistorylistdatalist).

<a id="model-orderhistorylistdatalist"></a>
### OrderHistoryListDataList

`order_id?`: `int64`; `symbol?`: `string`; `symbol_desc?`: `string`; `price_type?`: `string`; `order_opt_type?`: `int32`; `state?`: `int32`; `state_desc?`: `string`; `side?`: `int32`; `volume?`: `string`; `fill_volume?`: `string`; `close_pnl?`: `string`; `price?`: `string`; `trigger_price?`: `string`; `price_tp?`: `string`; `price_sl?`: `string`; `time_setup?`: `int64`; `time_done?`: `int64`.

Field semantics: `price_type` — Trade type (market=market price, trigger=trigger price); `side` — Side (1=sell, 2=buy); `time_setup` — Order time (Unix timestamp in seconds); `time_done` — End time (Unix timestamp in seconds).

<a id="model-orderlist"></a>
### OrderList

`timestamp?`: `int64`; `data?`: [OrderListData](#model-orderlistdata).

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-orderlistdata"></a>
### OrderListData

`list?`: [][OrderListDataList](#model-orderlistdatalist).

<a id="model-orderlistdatalist"></a>
### OrderListDataList

`order_id?`: `int64`; `symbol?`: `string`; `symbol_desc?`: `string`; `price_type?`: `string`; `state?`: `int32`; `state_desc?`: `string`; `finished?`: `int32`; `side?`: `int32`; `volume?`: `string`; `price?`: `string`; `price_tp?`: `string`; `price_sl?`: `string`; `time_setup?`: `int64`.

Field semantics: `price_type` — Trade type (market=market price, trigger=trigger price); `side` — Side (1=sell, 2=buy); `time_setup` — Order time (Unix timestamp in seconds).

<a id="model-positionhistorylist"></a>
### PositionHistoryList

`timestamp?`: `int64`; `data?`: [PositionHistoryListData](#model-positionhistorylistdata).

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-positionhistorylistdata"></a>
### PositionHistoryListData

`total?`: `int32`; `total_page?`: `int32`; `list?`: [][PositionHistoryListDataList](#model-positionhistorylistdatalist).

<a id="model-positionhistorylistdataclosedetail"></a>
### PositionHistoryListDataCloseDetail

`margin_level?`: `string`; `margin?`: `string`; `equity?`: `string`; `stop_out_level?`: `string`.

<a id="model-positionhistorylistdatalist"></a>
### PositionHistoryListDataList

`position_id`: `int64`; `symbol`: `string`; `realized_pnl`: `string`; `realized_pnl_rate?`: `string`; `volume`: `string`; `volume_closed`: `string`; `price_open`: `string`; `position_dir`: `string`; `price_tp?`: `string`; `price_sl?`: `string`; `counterparty_price?`: `string`; `close_price`: `string`; `time_create`: `string`; `time_close`: `string`; `position_status`: `string`; `close_detail?`: *[PositionHistoryListDataCloseDetail](#model-positionhistorylistdataclosedetail); `realized_pnl_detail`: [PositionHistoryListDataRealizedPnlDetail](#model-positionhistorylistdatarealizedpnldetail).

Field semantics: `position_dir` — Position Direction - Long: Long Position - Short: Short Position; `time_create` — Open time (timestamp in seconds); `time_close` — Close time (timestamp in seconds).

<a id="model-positionhistorylistdatarealizedpnldetail"></a>
### PositionHistoryListDataRealizedPnlDetail

`closed_pnl?`: `string`; `swap?`: `string`; `fee?`: `string`.

<a id="model-positionlist"></a>
### PositionList

`label?`: `string`; `message?`: `string`; `timestamp?`: `int64`; `data?`: [PositionListData](#model-positionlistdata).

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-positionlistdata"></a>
### PositionListData

`list?`: [][PositionListDataList](#model-positionlistdatalist).

<a id="model-positionlistdatalist"></a>
### PositionListDataList

`position_id?`: `int64`; `symbol?`: `string`; `symbol_desc?`: `string`; `margin?`: `string`; `unrealized_pnl?`: `string`; `unrealized_pnl_rate?`: `string`; `volume?`: `string`; `price_open?`: `string`; `position_dir?`: `string`.

Field semantics: `position_dir` — Position direction (Long=long position, Short=short position).

<a id="model-symbols"></a>
### Symbols

`timestamp?`: `int64`; `data?`: [SymbolsData](#model-symbolsdata).

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-symbolsdata"></a>
### SymbolsData

`list?`: [][SymbolsDataList](#model-symbolsdatalist).

<a id="model-symbolsdatalist"></a>
### SymbolsDataList

`symbol?`: `string`; `symbol_desc?`: `string`; `category_id?`: `int32`; `status?`: `string`; `trade_mode?`: `string`; `icon_link?`: `string`; `close_time?`: `int64`; `open_time?`: `int64`; `next_open_time?`: `int64`; `settlement_currency?`: `string`; `settlement_currency_symbol?`: `string`; `price_precision?`: `int32`.

Field semantics: `status` — Trading status (open=tradable, closed=non-tradable); `close_time` — Close time (Unix timestamp in seconds); `open_time` — Open time (Unix timestamp in seconds); `next_open_time` — Next open time (Unix timestamp in seconds, 0 means none).

<a id="model-tradficlosepositionrequest"></a>
### TradFiClosePositionRequest

`close_type`: `int32`; `close_volume?`: `*string`.

<a id="model-tradfiorderrequest"></a>
### TradFiOrderRequest

`price`: `string`; `price_type`: `string`; `side`: `int32`; `symbol`: `string`; `volume`: `string`; `price_tp?`: `string`; `price_sl?`: `string`; `leverage?`: `int32`.

Field semantics: `price_type` — Price type (trigger=trigger price, market=market price); `side` — Side (1=sell, 2=buy).

<a id="model-tradfiorderupdaterequest"></a>
### TradFiOrderUpdateRequest

`price`: `string`; `price_tp?`: `*string`; `price_sl?`: `*string`.

<a id="model-tradfipositionupdaterequest"></a>
### TradFiPositionUpdateRequest

`price_tp?`: `*string`; `price_sl?`: `*string`.

<a id="model-tradfiticker"></a>
### TradFiTicker

`label?`: `string`; `message?`: `string`; `timestamp?`: `int64`; `data?`: [TradFiTickerData](#model-tradfitickerdata).

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-tradfitickerdata"></a>
### TradFiTickerData

`highest_price?`: `string`; `lowest_price?`: `string`; `price_change?`: `string`; `price_change_amount?`: `string`; `today_open_price?`: `string`; `last_today_close_price?`: `string`; `last_price?`: `string`; `bid_price?`: `string`; `ask_price?`: `string`; `favorite?`: `bool`; `status?`: `string`; `close_time?`: `int64`; `open_time?`: `int64`; `next_open_time?`: `int64`; `trade_mode?`: `string`; `category_name?`: `string`.

Field semantics: `status` — Trading status (open=tradable, closed=non-tradable); `close_time` — Close time (Unix timestamp in seconds); `open_time` — Open time (Unix timestamp in seconds).

<a id="model-updateorder"></a>
### UpdateOrder

`timestamp?`: `int64`; `data?`: [UpdateOrderData](#model-updateorderdata).

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-updateorderdata"></a>
### UpdateOrderData

`order_id?`: `int64`; `symbol?`: `string`; `state?`: `string`; `volume?`: `string`; `price?`: `string`; `price_tp?`: `string`; `price_sl?`: `string`.

<a id="model-updateposition"></a>
### UpdatePosition

`timestamp?`: `int64`; `data?`: `map[string]any`.

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-userassetresp"></a>
### UserAssetResp

`timestamp?`: `int64`; `data?`: [UserAssetRespData](#model-userassetrespdata).

Field semantics: `timestamp` — Server timestamp (milliseconds).

<a id="model-userassetrespdata"></a>
### UserAssetRespData

`equity?`: `string`; `margin_level?`: `string`; `balance?`: `string`; `margin?`: `string`; `margin_free?`: `string`; `unrealized_pnl?`: `string`.

<a id="model-orderlog"></a>
### OrderLog

`timestamp?`: `int64`; `data?`: [OrderLogData](#model-orderlogdata).

<a id="model-orderlogdata"></a>
### OrderLogData

`order_id?`: `int64`; `log_id?`: `int64`; `symbol?`: `string`; `price_type?`: `string`; `state?`: `int32`; `side?`: `int32`; `volume?`: `string`; `price?`: `string`.

Field semantics: `price` is average fill price; `side` is 1 sell or 2 buy; `state` is 1 placed, 2 cancelled, 3 partially filled, 4 filled or 5 rejected. Keep `order_id` and `log_id` distinct.

<a id="model-symbolcommissions"></a>
### SymbolCommissions

`timestamp?`: `int64`; `data?`: [SymbolCommissionsData](#model-symbolcommissionsdata).

<a id="model-symbolcommissionsdata"></a>
### SymbolCommissionsData

`list?`: [][SymbolCommissionsDataList](#model-symbolcommissionsdatalist).

<a id="model-symbolcommissionsdatalist"></a>
### SymbolCommissionsDataList

`category_code?`: `string`; `symbol?`: `string`; `fee_per_lot?`: `string`.
