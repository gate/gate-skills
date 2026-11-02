# Currency conversion Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-errcodemsg"></a>
### ErrCodeMsg

`code`: `int32`; `message`: `string`; `extra`: `map[string]any`.

<a id="model-flashswapcurrencypair"></a>
### FlashSwapCurrencyPair

`currency_pair?`: `string`; `sell_currency?`: `string`; `buy_currency?`: `string`; `sell_min_amount?`: `string`; `sell_max_amount?`: `string`; `buy_min_amount?`: `string`; `buy_max_amount?`: `string`.

<a id="model-flashswapmulticurrencycreateparam"></a>
### FlashSwapMultiCurrencyCreateParam

`sell_asset`: `string`; `sell_amount`: `string`; `buy_asset`: `string`; `buy_amount`: `string`.

<a id="model-flashswapmulticurrencymanytooneordercreatereq"></a>
### FlashSwapMultiCurrencyManyToOneOrderCreateReq

`params`: [][FlashSwapMultiCurrencyCreateParam](#model-flashswapmulticurrencycreateparam).

<a id="model-flashswapmulticurrencymanytooneordercreateresp"></a>
### FlashSwapMultiCurrencyManyToOneOrderCreateResp

`code`: `int32`; `message`: `string`; `data`: [FlashSwapMultiCurrencyManyToOneOrderCreateRespData](#model-flashswapmulticurrencymanytooneordercreaterespdata); `timestamp?`: `int64`.

Field semantics: `timestamp` — Response timestamp (milliseconds).

<a id="model-flashswapmulticurrencymanytooneordercreaterespdata"></a>
### FlashSwapMultiCurrencyManyToOneOrderCreateRespData

`orders`: [][FlashSwapMultiCurrencyOrder](#model-flashswapmulticurrencyorder); `account_mode`: `int32`; `exchange_time_ms`: `int64`; `total_acquire_amount`: `string`.

Field semantics: `exchange_time_ms` — Exchange timestamp (in milliseconds).

<a id="model-flashswapmulticurrencymanytooneorderpreviewreq"></a>
### FlashSwapMultiCurrencyManyToOneOrderPreviewReq

`params`: [][FlashSwapMultiCurrencyPreviewParam](#model-flashswapmulticurrencypreviewparam).

<a id="model-flashswapmulticurrencymanytooneorderpreviewresp"></a>
### FlashSwapMultiCurrencyManyToOneOrderPreviewResp

`code`: `int32`; `message`: `string`; `data`: [FlashSwapMultiCurrencyManyToOneOrderPreviewRespData](#model-flashswapmulticurrencymanytooneorderpreviewrespdata); `timestamp?`: `int64`.

Field semantics: `timestamp` — Response timestamp (milliseconds).

<a id="model-flashswapmulticurrencymanytooneorderpreviewrespdata"></a>
### FlashSwapMultiCurrencyManyToOneOrderPreviewRespData

`orders`: [][FlashSwapMultiCurrencyPreviewOrder](#model-flashswapmulticurrencyprevieworder); `total_acquire_amount`: `string`.

<a id="model-flashswapmulticurrencyonetomanyordercreatereq"></a>
### FlashSwapMultiCurrencyOneToManyOrderCreateReq

`params`: [][FlashSwapMultiCurrencyCreateParam](#model-flashswapmulticurrencycreateparam).

<a id="model-flashswapmulticurrencyonetomanyordercreateresp"></a>
### FlashSwapMultiCurrencyOneToManyOrderCreateResp

`code`: `int32`; `message`: `string`; `data`: [FlashSwapMultiCurrencyOneToManyOrderCreateRespData](#model-flashswapmulticurrencyonetomanyordercreaterespdata); `timestamp?`: `int64`.

Field semantics: `timestamp` — Response timestamp (milliseconds).

<a id="model-flashswapmulticurrencyonetomanyordercreaterespdata"></a>
### FlashSwapMultiCurrencyOneToManyOrderCreateRespData

`orders`: [][FlashSwapMultiCurrencyOrder](#model-flashswapmulticurrencyorder); `account_mode`: `int32`; `exchange_time_ms`: `int64`; `total_consume_amount`: `string`; `total_acquire_amount`: `string`.

Field semantics: `exchange_time_ms` — Exchange timestamp (in milliseconds).

<a id="model-flashswapmulticurrencyonetomanyorderpreviewreq"></a>
### FlashSwapMultiCurrencyOneToManyOrderPreviewReq

`params`: [][FlashSwapMultiCurrencyPreviewParam](#model-flashswapmulticurrencypreviewparam).

<a id="model-flashswapmulticurrencyonetomanyorderpreviewresp"></a>
### FlashSwapMultiCurrencyOneToManyOrderPreviewResp

`code`: `int32`; `message`: `string`; `data`: [FlashSwapMultiCurrencyOneToManyOrderPreviewRespData](#model-flashswapmulticurrencyonetomanyorderpreviewrespdata); `timestamp?`: `int64`.

Field semantics: `timestamp` — Response timestamp (milliseconds).

<a id="model-flashswapmulticurrencyonetomanyorderpreviewrespdata"></a>
### FlashSwapMultiCurrencyOneToManyOrderPreviewRespData

`orders`: [][FlashSwapMultiCurrencyPreviewOrder](#model-flashswapmulticurrencyprevieworder); `total_consume_amount`: `string`; `total_acquire_amount`: `string`.

<a id="model-flashswapmulticurrencyorder"></a>
### FlashSwapMultiCurrencyOrder

`id?`: `int64`; `user_id?`: `int32`; `source?`: `string`; `app_id?`: `string`; `client_req_id?`: `string`; `sell_asset?`: `string`; `sell_amount?`: `string`; `sell_amount_show?`: `string`; `buy_asset?`: `string`; `buy_amount?`: `string`; `buy_amount_show?`: `string`; `price?`: `string`; `status?`: `int32`; `quote_id?`: `string`; `failed_code?`: `int32`; `failed_reason?`: `string`; `create_time?`: `string`; `create_time_ms?`: `int64`; `error`: [ErrCodeMsg](#model-errcodemsg).

Field semantics: `id` — Order ID; `create_time_ms` — Creation timestamp (in milliseconds).

<a id="model-flashswapmulticurrencyprevieworder"></a>
### FlashSwapMultiCurrencyPreviewOrder

`quote_id?`: `string`; `hedge_type?`: `int32`; `sell_asset?`: `string`; `sell_amount?`: `string`; `sell_amount_show?`: `string`; `buy_asset?`: `string`; `buy_amount?`: `string`; `buy_amount_show?`: `string`; `price?`: `string`; `price_diff?`: `string`; `reverse_price?`: `string`; `valid_timestamp?`: `int64`; `error`: [ErrCodeMsg](#model-errcodemsg).

Field semantics: `valid_timestamp` — Quote expiration timestamp (in seconds).

<a id="model-flashswapmulticurrencypreviewparam"></a>
### FlashSwapMultiCurrencyPreviewParam

`sell_asset`: `string`; `sell_amount?`: `string`; `buy_asset`: `string`; `buy_amount?`: `string`.

<a id="model-flashswaporder"></a>
### FlashSwapOrder

`id?`: `int64`; `create_time?`: `int64`; `user_id?`: `int64`; `sell_currency?`: `string`; `sell_amount?`: `string`; `buy_currency?`: `string`; `buy_amount?`: `string`; `price?`: `string`; `status?`: `int32`.

Field semantics: `id` — Flash swap order ID; `create_time` — Creation time of order (in milliseconds).

<a id="model-flashswapordercreatereq"></a>
### FlashSwapOrderCreateReq

`quote_id?`: `string`; `hedge_type?`: `int32`; `sell_asset`: `string`; `sell_amount`: `string`; `buy_asset`: `string`; `buy_amount`: `string`; `client_req_id?`: `string`; `request_time_ms?`: `int64`.

Field semantics: `request_time_ms` — Request timestamp (in milliseconds).

<a id="model-flashswapordercreateresp"></a>
### FlashSwapOrderCreateResp

`code`: `int32`; `message`: `string`; `data`: [FlashSwapOrderCreateRespData](#model-flashswapordercreaterespdata); `timestamp?`: `int64`.

Field semantics: `timestamp` — Response timestamp (milliseconds).

<a id="model-flashswapordercreaterespdata"></a>
### FlashSwapOrderCreateRespData

`id?`: `int64`; `user_id?`: `int32`; `source?`: `string`; `app_id?`: `string`; `client_req_id?`: `string`; `sell_asset?`: `string`; `sell_amount?`: `string`; `sell_amount_show?`: `string`; `buy_asset?`: `string`; `buy_amount?`: `string`; `buy_amount_show?`: `string`; `price?`: `string`; `status?`: `int32`; `quote_id?`: `string`; `failed_code?`: `int32`; `failed_reason?`: `string`; `create_time?`: `string`; `create_time_ms?`: `int64`; `account_mode`: `int32`.

Field semantics: `id` — Order ID; `create_time_ms` — Creation timestamp (in milliseconds).

<a id="model-flashswaporderpreview"></a>
### FlashSwapOrderPreview

`preview_id?`: `string`; `sell_currency?`: `string`; `sell_amount?`: `string`; `buy_currency?`: `string`; `buy_amount?`: `string`; `price?`: `string`.

<a id="model-flashswaporderpreviewresp"></a>
### FlashSwapOrderPreviewResp

`code`: `int32`; `message`: `string`; `data`: [FlashSwapOrderPreviewRespData](#model-flashswaporderpreviewrespdata); `timestamp?`: `int64`.

Field semantics: `timestamp` — Response timestamp (milliseconds).

<a id="model-flashswaporderpreviewrespdata"></a>
### FlashSwapOrderPreviewRespData

`quote_id?`: `string`; `hedge_type?`: `int32`; `sell_asset?`: `string`; `sell_amount?`: `string`; `sell_amount_show?`: `string`; `buy_asset?`: `string`; `buy_amount?`: `string`; `buy_amount_show?`: `string`; `price?`: `string`; `price_diff?`: `string`; `reverse_price?`: `string`; `valid_timestamp?`: `int64`.

Field semantics: `valid_timestamp` — Quote expiration timestamp (in seconds).

<a id="model-flashswaporderrequest"></a>
### FlashSwapOrderRequest

`preview_id`: `string`; `sell_currency`: `string`; `sell_amount`: `string`; `buy_currency`: `string`; `buy_amount`: `string`.

<a id="model-flashswappreviewrequest"></a>
### FlashSwapPreviewRequest

`sell_currency`: `string`; `sell_amount?`: `string`; `buy_currency`: `string`; `buy_amount?`: `string`.
