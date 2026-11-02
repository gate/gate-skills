# Market data

## Scope and source

These are public point-in-time market reads. Resolve the exact spot/perpetual/delivery/options instrument and keep timestamps and product units. Select a bounded interval, symbol and record count; do not fetch every market when one suffices. Funding, mark/index price, last trade and order-book prices are different values. No websocket subscription, user-data stream, listen-key renewal or reconnect lifecycle is registered in this CLI snapshot. A poll is not a continuous subscription. For optional bounded public WS observation, see [public streams](streams.md); this helper does not add a CLI subscription command.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `delivery.market.candlesticks` | `gate-cli cex delivery market candlesticks` | read |
| `delivery.market.contract` | `gate-cli cex delivery market contract` | read |
| `delivery.market.contracts` | `gate-cli cex delivery market contracts` | read |
| `delivery.market.insurance` | `gate-cli cex delivery market insurance` | read |
| `delivery.market.order-book` | `gate-cli cex delivery market order-book` | read |
| `delivery.market.risk-limit-tiers` | `gate-cli cex delivery market risk-limit-tiers` | read |
| `delivery.market.tickers` | `gate-cli cex delivery market tickers` | read |
| `delivery.market.trades` | `gate-cli cex delivery market trades` | read |
| `futures.market.batch-funding-rates` | `gate-cli cex futures market batch-funding-rates` | read |
| `futures.market.candlesticks` | `gate-cli cex futures market candlesticks` | read |
| `futures.market.contract` | `gate-cli cex futures market contract` | read |
| `futures.market.contracts` | `gate-cli cex futures market contracts` | read |
| `futures.market.funding-rate` | `gate-cli cex futures market funding-rate` | read |
| `futures.market.index-constituents` | `gate-cli cex futures market index-constituents` | read |
| `futures.market.insurance` | `gate-cli cex futures market insurance` | read |
| `futures.market.liquidations` | `gate-cli cex futures market liquidations` | read |
| `futures.market.orderbook` | `gate-cli cex futures market orderbook` | read |
| `futures.market.premium` | `gate-cli cex futures market premium` | read |
| `futures.market.risk-limit-table` | `gate-cli cex futures market risk-limit-table` | read |
| `futures.market.risk-limit-tiers` | `gate-cli cex futures market risk-limit-tiers` | read |
| `futures.market.stats` | `gate-cli cex futures market stats` | read |
| `futures.market.ticker` | `gate-cli cex futures market ticker` | read |
| `futures.market.tickers` | `gate-cli cex futures market tickers` | read |
| `futures.market.trades` | `gate-cli cex futures market trades` | read |
| `options.market.candlesticks` | `gate-cli cex options market candlesticks` | read |
| `options.market.contract` | `gate-cli cex options market contract` | read |
| `options.market.contracts` | `gate-cli cex options market contracts` | read |
| `options.market.expirations` | `gate-cli cex options market expirations` | read |
| `options.market.order-book` | `gate-cli cex options market order-book` | read |
| `options.market.settlement` | `gate-cli cex options market settlement` | read |
| `options.market.settlements` | `gate-cli cex options market settlements` | read |
| `options.market.tickers` | `gate-cli cex options market tickers` | read |
| `options.market.trades` | `gate-cli cex options market trades` | read |
| `options.market.underlying-candlesticks` | `gate-cli cex options market underlying-candlesticks` | read |
| `options.market.underlying-tickers` | `gate-cli cex options market underlying-tickers` | read |
| `options.market.underlyings` | `gate-cli cex options market underlyings` | read |
| `spot.market.candlesticks` | `gate-cli cex spot market candlesticks` | read |
| `spot.market.currencies` | `gate-cli cex spot market currencies` | read |
| `spot.market.currency` | `gate-cli cex spot market currency` | read |
| `spot.market.insurance` | `gate-cli cex spot market insurance` | read |
| `spot.market.orderbook` | `gate-cli cex spot market orderbook` | read |
| `spot.market.pair` | `gate-cli cex spot market pair` | read |
| `spot.market.pairs` | `gate-cli cex spot market pairs` | read |
| `spot.market.ticker` | `gate-cli cex spot market ticker` | read |
| `spot.market.tickers` | `gate-cli cex spot market tickers` | read |
| `spot.market.time` | `gate-cli cex spot market time` | read |
| `spot.market.trades` | `gate-cli cex spot market trades` | read |
| `futures.market.adl-risk-states` | `gate-cli cex futures market adl-risk-states` | read |
| `futures.market.contracts-all` | `gate-cli cex futures market contracts-all` | read |
| `futures.market.rpi-orderbook` | `gate-cli cex futures market rpi-orderbook` | read |
| `spot.market.rpi-orderbook` | `gate-cli cex spot market rpi-orderbook` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="delivery.market.candlesticks"></a>
### `gate-cli cex delivery market candlesticks`

Operation ID: `delivery.market.candlesticks`. Effect: **read**.

List candlesticks for a delivery contract (public, no authentication required)

```text
gate-cli cex delivery market candlesticks [flags]
```

API: `GET /api/v4/delivery/{settle}/candlesticks` (public).

Returns: [][DeliveryCandlestick](models/market.md#model-deliverycandlestick).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Futures contract name (required) |
| `--interval` | `string` | No | Unset | Candlestick interval |
| `--limit` | `int32` | No | `0` | Number of records |

<a id="delivery.market.contract"></a>
### `gate-cli cex delivery market contract`

Operation ID: `delivery.market.contract`. Effect: **read**.

Get details of a delivery contract (public, no authentication required)

```text
gate-cli cex delivery market contract [flags]
```

API: `GET /api/v4/delivery/{settle}/contracts/{contract}` (public).

Returns: [DeliveryContract](models/market.md#model-deliverycontract).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Futures contract name (required) |

<a id="delivery.market.contracts"></a>
### `gate-cli cex delivery market contracts`

Operation ID: `delivery.market.contracts`. Effect: **read**.

List delivery contracts (public, no authentication required)

```text
gate-cli cex delivery market contracts
```

API: `GET /api/v4/delivery/{settle}/contracts` (public).

Returns: [][DeliveryContract](models/market.md#model-deliverycontract).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="delivery.market.insurance"></a>
### `gate-cli cex delivery market insurance`

Operation ID: `delivery.market.insurance`. Effect: **read**.

List insurance fund records (public, no authentication required)

```text
gate-cli cex delivery market insurance [flags]
```

API: `GET /api/v4/delivery/{settle}/insurance` (public).

Returns: [][InsuranceRecord](models/market.md#model-insurancerecord).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--limit` | `int32` | No | `0` | Number of records to return |

<a id="delivery.market.order-book"></a>
### `gate-cli cex delivery market order-book`

Operation ID: `delivery.market.order-book`. Effect: **read**.

Get order book for a delivery contract (public, no authentication required)

```text
gate-cli cex delivery market order-book [flags]
```

API: `GET /api/v4/delivery/{settle}/order_book` (public).

Returns: [DeliveryOrderBook](models/market.md#model-deliveryorderbook).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Futures contract name (required) |
| `--limit` | `int32` | No | `0` | Order book depth limit |

<a id="delivery.market.risk-limit-tiers"></a>
### `gate-cli cex delivery market risk-limit-tiers`

Operation ID: `delivery.market.risk-limit-tiers`. Effect: **read**.

List risk limit tiers for a contract (public, no authentication required)

```text
gate-cli cex delivery market risk-limit-tiers [flags]
```

API: `GET /api/v4/delivery/{settle}/risk_limit_tiers` (public).

Returns: [][DeliveryLimitRiskTiers](models/market.md#model-deliverylimitrisktiers).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Futures contract name (required) |

<a id="delivery.market.tickers"></a>
### `gate-cli cex delivery market tickers`

Operation ID: `delivery.market.tickers`. Effect: **read**.

List delivery tickers (public, no authentication required)

```text
gate-cli cex delivery market tickers [flags]
```

API: `GET /api/v4/delivery/{settle}/tickers` (public).

Returns: [][DeliveryTicker](models/market.md#model-deliveryticker).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |

<a id="delivery.market.trades"></a>
### `gate-cli cex delivery market trades`

Operation ID: `delivery.market.trades`. Effect: **read**.

List recent trades for a delivery contract (public, no authentication required)

```text
gate-cli cex delivery market trades [flags]
```

API: `GET /api/v4/delivery/{settle}/trades` (public).

Returns: [][DeliveryTrade](models/market.md#model-deliverytrade).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Futures contract name (required) |
| `--limit` | `int32` | No | `0` | Number of records to return |

<a id="futures.market.batch-funding-rates"></a>
### `gate-cli cex futures market batch-funding-rates`

Operation ID: `futures.market.batch-funding-rates`. Effect: **read**.

Get batch funding rates for multiple contracts (public, no authentication required)

```text
gate-cli cex futures market batch-funding-rates [flags]
```

API: `POST /api/v4/futures/{settle}/funding_rates` (public).

Returns: [][BatchFundingRatesResponse](models/market.md#model-batchfundingratesresponse).

API request model(s), assembled by the command: [BatchFundingRatesRequest](models/market.md#model-batchfundingratesrequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contracts` | `stringSlice` | Yes | `[]` | Contract names (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.candlesticks"></a>
### `gate-cli cex futures market candlesticks`

Operation ID: `futures.market.candlesticks`. Effect: **read**.

Get futures candlestick data

```text
gate-cli cex futures market candlesticks [flags]
```

API: `GET /api/v4/futures/{settle}/candlesticks` (public).

Returns: [][FuturesCandlestick](models/market.md#model-futurescandlestick).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--interval` | `string` | No | `1h` | Interval: 10s, 1m, 5m, 15m, 30m, 1h, 4h, 8h, 1d, 7d, 30d |
| `--limit` | `int32` | No | `100` | Number of candlesticks to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.contract"></a>
### `gate-cli cex futures market contract`

Operation ID: `futures.market.contract`. Effect: **read**.

Get details for a futures contract (public, no authentication required)

```text
gate-cli cex futures market contract [flags]
```

API: `GET /api/v4/futures/{settle}/contracts/{contract}` (public).

Returns: [Contract](models/market.md#model-contract).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name, e.g. BTC_USDT (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.contracts"></a>
### `gate-cli cex futures market contracts`

Operation ID: `futures.market.contracts`. Effect: **read**.

List all futures contracts (public, no authentication required)

```text
gate-cli cex futures market contracts [flags]
```

API: `GET /api/v4/futures/{settle}/contracts` (public).

Returns: [][Contract](models/market.md#model-contract).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--offset` | `int32` | No | `0` | Records to skip |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.funding-rate"></a>
### `gate-cli cex futures market funding-rate`

Operation ID: `futures.market.funding-rate`. Effect: **read**.

Get historical funding rate

```text
gate-cli cex futures market funding-rate [flags]
```

API: `GET /api/v4/futures/{settle}/funding_rate` (public).

Returns: [][FundingRateRecord](models/market.md#model-fundingraterecord).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--limit` | `int32` | No | `20` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.index-constituents"></a>
### `gate-cli cex futures market index-constituents`

Operation ID: `futures.market.index-constituents`. Effect: **read**.

Get index constituents (public, no authentication required)

```text
gate-cli cex futures market index-constituents [flags]
```

API: `GET /api/v4/futures/{settle}/index_constituents/{index}` (public).

Returns: [FuturesIndexConstituents](models/market.md#model-futuresindexconstituents).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--index` | `string` | Yes | Unset | Index name (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.insurance"></a>
### `gate-cli cex futures market insurance`

Operation ID: `futures.market.insurance`. Effect: **read**.

Get futures insurance fund history (public, no authentication required)

```text
gate-cli cex futures market insurance [flags]
```

API: `GET /api/v4/futures/{settle}/insurance` (public).

Returns: [][InsuranceRecord](models/market.md#model-insurancerecord).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.liquidations"></a>
### `gate-cli cex futures market liquidations`

Operation ID: `futures.market.liquidations`. Effect: **read**.

List recently liquidated orders (public, no authentication required)

```text
gate-cli cex futures market liquidations [flags]
```

API: `GET /api/v4/futures/{settle}/liq_orders` (public).

Returns: [][FuturesLiqOrder](models/market.md#model-futuresliqorder).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.orderbook"></a>
### `gate-cli cex futures market orderbook`

Operation ID: `futures.market.orderbook`. Effect: **read**.

Get futures order book

```text
gate-cli cex futures market orderbook [flags]
```

API: `GET /api/v4/futures/{settle}/order_book` (public).

Returns: [FuturesOrderBook](models/market.md#model-futuresorderbook).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--depth` | `int32` | No | `20` | Order book depth |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.premium"></a>
### `gate-cli cex futures market premium`

Operation ID: `futures.market.premium`. Effect: **read**.

Get premium index K-line data (public, no authentication required)

```text
gate-cli cex futures market premium [flags]
```

API: `GET /api/v4/futures/{settle}/premium_index` (public).

Returns: [][FuturesPremiumIndex](models/market.md#model-futurespremiumindex).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--interval` | `string` | No | `1h` | Interval: 10s, 1m, 5m, 15m, 30m, 1h, 4h, 8h, 1d, 7d, 30d |
| `--limit` | `int32` | No | `100` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.risk-limit-table"></a>
### `gate-cli cex futures market risk-limit-table`

Operation ID: `futures.market.risk-limit-table`. Effect: **read**.

Query a specific risk limit table (public, no authentication required)

```text
gate-cli cex futures market risk-limit-table <table-id> [flags]
```

API: `GET /api/v4/futures/{settle}/risk_limit_table` (public).

Returns: [][FuturesRiskLimitTier](models/market.md#model-futuresrisklimittier).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.risk-limit-tiers"></a>
### `gate-cli cex futures market risk-limit-tiers`

Operation ID: `futures.market.risk-limit-tiers`. Effect: **read**.

Query risk limit tiers (public, no authentication required)

```text
gate-cli cex futures market risk-limit-tiers [flags]
```

API: `GET /api/v4/futures/{settle}/risk_limit_tiers` (public).

Returns: [][FuturesLimitRiskTiers](models/market.md#model-futureslimitrisktiers).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.stats"></a>
### `gate-cli cex futures market stats`

Operation ID: `futures.market.stats`. Effect: **read**.

Get futures contract statistics (public, no authentication required)

```text
gate-cli cex futures market stats [flags]
```

API: `GET /api/v4/futures/{settle}/contract_stats` (public).

Returns: [][ContractStat](models/market.md#model-contractstat).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--interval` | `string` | No | `1h` | Stat interval: 5m, 15m, 30m, 1h, 4h, 1d |
| `--limit` | `int32` | No | `30` | Number of records to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.ticker"></a>
### `gate-cli cex futures market ticker`

Operation ID: `futures.market.ticker`. Effect: **read**.

Get ticker for a futures contract

```text
gate-cli cex futures market ticker [flags]
```

API: `GET /api/v4/futures/{settle}/tickers` (public).

Returns: [][FuturesTicker](models/market.md#model-futuresticker).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name, e.g. BTC_USDT (required) |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.tickers"></a>
### `gate-cli cex futures market tickers`

Operation ID: `futures.market.tickers`. Effect: **read**.

Get all futures tickers

```text
gate-cli cex futures market tickers [flags]
```

API: `GET /api/v4/futures/{settle}/tickers` (public).

Returns: [][FuturesTicker](models/market.md#model-futuresticker).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.trades"></a>
### `gate-cli cex futures market trades`

Operation ID: `futures.market.trades`. Effect: **read**.

Get recent futures trades

```text
gate-cli cex futures market trades [flags]
```

API: `GET /api/v4/futures/{settle}/trades` (public).

Returns: [][FuturesTrade](models/market.md#model-futurestrade).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name (required) |
| `--limit` | `int32` | No | `20` | Number of trades to return |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="options.market.candlesticks"></a>
### `gate-cli cex options market candlesticks`

Operation ID: `options.market.candlesticks`. Effect: **read**.

List candlesticks for an options contract (public, no authentication required)

```text
gate-cli cex options market candlesticks [flags]
```

API: `GET /api/v4/options/candlesticks` (public).

Returns: [][OptionsCandlestick](models/market.md#model-optionscandlestick).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Options contract name (required) |
| `--interval` | `string` | No | Unset | Candlestick interval |
| `--limit` | `int32` | No | `0` | Number of records |

<a id="options.market.contract"></a>
### `gate-cli cex options market contract`

Operation ID: `options.market.contract`. Effect: **read**.

Get details of an options contract (public, no authentication required)

```text
gate-cli cex options market contract [flags]
```

API: `GET /api/v4/options/contracts/{contract}` (public).

Returns: [OptionsContract](models/market.md#model-optionscontract).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Options contract name (required) |

<a id="options.market.contracts"></a>
### `gate-cli cex options market contracts`

Operation ID: `options.market.contracts`. Effect: **read**.

List options contracts for an underlying (public, no authentication required)

```text
gate-cli cex options market contracts [flags]
```

API: `GET /api/v4/options/contracts` (public).

Returns: [][OptionsContract](models/market.md#model-optionscontract).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--expiration` | `int64` | No | `0` | Filter by expiration Unix timestamp |
| `--underlying` | `string` | Yes | Unset | Underlying name (required) |

<a id="options.market.expirations"></a>
### `gate-cli cex options market expirations`

Operation ID: `options.market.expirations`. Effect: **read**.

List expiration dates for an underlying (public, no authentication required)

```text
gate-cli cex options market expirations [flags]
```

API: `GET /api/v4/options/expirations` (public).

Returns: `[]int64`.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--underlying` | `string` | Yes | Unset | Underlying name (required) |

<a id="options.market.order-book"></a>
### `gate-cli cex options market order-book`

Operation ID: `options.market.order-book`. Effect: **read**.

Get order book for an options contract (public, no authentication required)

```text
gate-cli cex options market order-book [flags]
```

API: `GET /api/v4/options/order_book` (public).

Returns: [OptionsOrderBook](models/market.md#model-optionsorderbook).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Options contract name (required) |
| `--interval` | `string` | No | Unset | Order book merge interval |
| `--limit` | `int32` | No | `0` | Order book depth limit |

<a id="options.market.settlement"></a>
### `gate-cli cex options market settlement`

Operation ID: `options.market.settlement`. Effect: **read**.

Get specific settlement record (public, no authentication required)

```text
gate-cli cex options market settlement [flags]
```

API: `GET /api/v4/options/settlements/{contract}` (public).

Returns: [OptionsSettlement](models/market.md#model-optionssettlement).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--at` | `int64` | Yes | `0` | Settlement time Unix timestamp (required) |
| `--contract` | `string` | Yes | Unset | Options contract name (required) |
| `--underlying` | `string` | Yes | Unset | Underlying name (required) |

<a id="options.market.settlements"></a>
### `gate-cli cex options market settlements`

Operation ID: `options.market.settlements`. Effect: **read**.

List settlement history for an underlying (public, no authentication required)

```text
gate-cli cex options market settlements [flags]
```

API: `GET /api/v4/options/settlements` (public).

Returns: [][OptionsSettlement](models/market.md#model-optionssettlement).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--underlying` | `string` | Yes | Unset | Underlying name (required) |

<a id="options.market.tickers"></a>
### `gate-cli cex options market tickers`

Operation ID: `options.market.tickers`. Effect: **read**.

List options tickers for an underlying (public, no authentication required)

```text
gate-cli cex options market tickers [flags]
```

API: `GET /api/v4/options/tickers` (public).

Returns: [][OptionsTicker](models/market.md#model-optionsticker).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--underlying` | `string` | Yes | Unset | Underlying name (required) |

<a id="options.market.trades"></a>
### `gate-cli cex options market trades`

Operation ID: `options.market.trades`. Effect: **read**.

List recent options trades (public, no authentication required)

```text
gate-cli cex options market trades [flags]
```

API: `GET /api/v4/options/trades` (public).

Returns: [][OptionsTrade](models/market.md#model-optionstrade).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | No | Unset | Filter by contract name |
| `--limit` | `int32` | No | `0` | Number of records |

<a id="options.market.underlying-candlesticks"></a>
### `gate-cli cex options market underlying-candlesticks`

Operation ID: `options.market.underlying-candlesticks`. Effect: **read**.

List candlesticks for an options underlying (public, no authentication required)

```text
gate-cli cex options market underlying-candlesticks [flags]
```

API: `GET /api/v4/options/underlying/candlesticks` (public).

Returns: [][OptionsCandlestick](models/market.md#model-optionscandlestick).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--interval` | `string` | No | Unset | Candlestick interval |
| `--limit` | `int32` | No | `0` | Number of records |
| `--underlying` | `string` | Yes | Unset | Underlying name (required) |

<a id="options.market.underlying-tickers"></a>
### `gate-cli cex options market underlying-tickers`

Operation ID: `options.market.underlying-tickers`. Effect: **read**.

Get ticker for an options underlying (public, no authentication required)

```text
gate-cli cex options market underlying-tickers [flags]
```

API: `GET /api/v4/options/underlying/tickers/{underlying}` (public).

Returns: [OptionsUnderlyingTicker](models/market.md#model-optionsunderlyingticker).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--underlying` | `string` | Yes | Unset | Underlying name (required) |

<a id="options.market.underlyings"></a>
### `gate-cli cex options market underlyings`

Operation ID: `options.market.underlyings`. Effect: **read**.

List options underlyings (public, no authentication required)

```text
gate-cli cex options market underlyings
```

API: `GET /api/v4/options/underlyings` (public).

Returns: [][OptionsUnderlying](models/market.md#model-optionsunderlying).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="spot.market.candlesticks"></a>
### `gate-cli cex spot market candlesticks`

Operation ID: `spot.market.candlesticks`. Effect: **read**.

Get candlestick data for a currency pair

```text
gate-cli cex spot market candlesticks [flags]
```

API: `GET /api/v4/spot/candlesticks` (public).

Returns: `[][]string`.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--interval` | `string` | No | `1h` | Interval: 10s, 1m, 5m, 15m, 30m, 1h, 4h, 8h, 1d, 7d, 30d |
| `--limit` | `int32` | No | `100` | Number of candlesticks to return |
| `--pair` | `string` | Yes | Unset | Currency pair (required) |

<a id="spot.market.currencies"></a>
### `gate-cli cex spot market currencies`

Operation ID: `spot.market.currencies`. Effect: **read**.

List all currencies (public, no authentication required)

```text
gate-cli cex spot market currencies
```

API: `GET /api/v4/spot/currencies` (public).

Returns: [][Currency](models/market.md#model-currency).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="spot.market.currency"></a>
### `gate-cli cex spot market currency`

Operation ID: `spot.market.currency`. Effect: **read**.

Get details for a currency (public, no authentication required)

```text
gate-cli cex spot market currency [flags]
```

API: `GET /api/v4/spot/currencies/{currency}` (public).

Returns: [Currency](models/market.md#model-currency).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--currency` | `string` | Yes | Unset | Currency symbol, e.g. BTC (required) |

<a id="spot.market.insurance"></a>
### `gate-cli cex spot market insurance`

Operation ID: `spot.market.insurance`. Effect: **read**.

Get spot insurance fund historical data (public, no authentication required)

```text
gate-cli cex spot market insurance [flags]
```

API: `GET /api/v4/spot/insurance_history` (public).

Returns: [][SpotInsuranceHistory](models/market.md#model-spotinsurancehistory).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--business` | `string` | No | `margin` | Leverage business: margin, unified |
| `--currency` | `string` | Yes | Unset | Currency name (required) |
| `--from` | `int64` | Yes | `0` | Start Unix timestamp in seconds, greater than zero (required; registered zero default is rejected) |
| `--limit` | `int32` | No | `0` | Number of records to return |
| `--to` | `int64` | Yes | `0` | End Unix timestamp in seconds, at or after `--from` (required; registered zero default is rejected) |

<a id="spot.market.orderbook"></a>
### `gate-cli cex spot market orderbook`

Operation ID: `spot.market.orderbook`. Effect: **read**.

Get order book for a currency pair

```text
gate-cli cex spot market orderbook [flags]
```

API: `GET /api/v4/spot/order_book` (public).

Returns: [OrderBook](models/market.md#model-orderbook).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--depth` | `int32` | No | `20` | Order book depth |
| `--pair` | `string` | Yes | Unset | Currency pair (required) |

<a id="spot.market.pair"></a>
### `gate-cli cex spot market pair`

Operation ID: `spot.market.pair`. Effect: **read**.

Get details for a currency pair (public, no authentication required)

```text
gate-cli cex spot market pair [flags]
```

API: `GET /api/v4/spot/currency_pairs/{currency_pair}` (public).

Returns: [CurrencyPair](models/market.md#model-currencypair).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--pair` | `string` | Yes | Unset | Currency pair, e.g. BTC_USDT (required) |

<a id="spot.market.pairs"></a>
### `gate-cli cex spot market pairs`

Operation ID: `spot.market.pairs`. Effect: **read**.

List all currency pairs (public, no authentication required)

```text
gate-cli cex spot market pairs
```

API: `GET /api/v4/spot/currency_pairs` (public).

Returns: [][CurrencyPair](models/market.md#model-currencypair).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="spot.market.ticker"></a>
### `gate-cli cex spot market ticker`

Operation ID: `spot.market.ticker`. Effect: **read**.

Get ticker for a currency pair

```text
gate-cli cex spot market ticker [flags]
```

API: `GET /api/v4/spot/tickers` (public).

Returns: [Ticker](models/market.md#model-ticker).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--pair` | `string` | Yes | Unset | Currency pair, e.g. BTC_USDT (required) |

<a id="spot.market.tickers"></a>
### `gate-cli cex spot market tickers`

Operation ID: `spot.market.tickers`. Effect: **read**.

Get all spot tickers

```text
gate-cli cex spot market tickers
```

API: `GET /api/v4/spot/tickers` (public).

Returns: [][Ticker](models/market.md#model-ticker).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="spot.market.time"></a>
### `gate-cli cex spot market time`

Operation ID: `spot.market.time`. Effect: **read**.

Get server time (public, no authentication required)

```text
gate-cli cex spot market time
```

API: `GET /api/v4/spot/time` (public).

Returns: [SystemTime](models/market.md#model-systemtime).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="spot.market.trades"></a>
### `gate-cli cex spot market trades`

Operation ID: `spot.market.trades`. Effect: **read**.

Get recent trades for a currency pair

```text
gate-cli cex spot market trades [flags]
```

API: `GET /api/v4/spot/trades` (public).

Returns: [][Trade](models/market.md#model-trade).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--limit` | `int32` | No | `20` | Number of trades to return |
| `--pair` | `string` | Yes | Unset | Currency pair (required) |

## Verification and recovery

Check the exact instrument, source timestamp, requested interval/range, returned units and stale/empty data. Do not claim continuity or an authenticated account state from public quotes.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex delivery market candlesticks --contract <contract> --format json
```

Delivery market reads are fixed to USDT settlement by the current CLI; do not invent a delivery `--settle` override.

<a id="futures.market.adl-risk-states"></a>
### `gate-cli cex futures market adl-risk-states`

Operation ID: `futures.market.adl-risk-states`. Effect: **read**.

Get futures ADL risk states

```text
gate-cli cex futures market adl-risk-states [flags]
```

API: `GET /api/v4/futures/{settle}/adl_risk_states` (public).

Returns: [FuturesAdlRiskStates](models/market.md#model-futuresadlriskstates).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.contracts-all"></a>
### `gate-cli cex futures market contracts-all`

Operation ID: `futures.market.contracts-all`. Effect: **read**.

List contracts including delisted contracts

```text
gate-cli cex futures market contracts-all [flags]
```

API: `GET /api/v4/futures/{settle}/contracts_all` (public).

Returns: [][Contract](models/market.md#model-contract).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--limit` | `int32` | No | `100` | Records per page, 1 to 1000 |
| `--offset` | `int32` | No | `0` | Record offset, 0 to 100000 |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |

<a id="futures.market.rpi-orderbook"></a>
### `gate-cli cex futures market rpi-orderbook`

Operation ID: `futures.market.rpi-orderbook`. Effect: **read**.

Get the futures RPI order book

```text
gate-cli cex futures market rpi-orderbook [flags]
```

API: `GET /api/v4/futures/{settle}/rpi_order_book` (public).

Returns: [FuturesOrderBook](models/market.md#model-futuresorderbook).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--contract` | `string` | Yes | Unset | Contract name, e.g. BTC_USDT |
| `--interval` | `string` | No | Unset | Price aggregation interval |
| `--limit` | `int32` | No | `20` | Depth limit, 1 to 50 |
| `--settle` | `string` | No | `usdt` | Settlement currency: usdt, btc |
| `--with-id` | `bool` | No | `false` | Include order book ID |

<a id="spot.market.rpi-orderbook"></a>
### `gate-cli cex spot market rpi-orderbook`

Operation ID: `spot.market.rpi-orderbook`. Effect: **read**.

Get the RPI order book

```text
gate-cli cex spot market rpi-orderbook [flags]
```

API: `GET /api/v4/spot/rpi_order_book` (public).

Returns: [OrderBook](models/market.md#model-orderbook).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--interval` | `string` | No | Unset | Price aggregation interval |
| `--limit` | `int32` | No | `20` | Depth limit, 1 to 100 |
| `--pair` | `string` | Yes | Unset | Currency pair, e.g. BTC_USDT |
| `--with-id` | `bool` | No | `false` | Include order book ID |

<a id="rpi-and-contract-market-data"></a>
## RPI books, all contracts and ADL risk

Spot and futures RPI books are separate public snapshots. Spot requires `--pair`
and depth 1–100; futures requires `--contract`, effective settlement and depth
1–50. `--with-id` controls the book ID. Preserve price/quantity units and timestamp;
RPI depth is not proof of executable liquidity or a complete regular order book.

`futures.market.contracts-all` includes delisted contracts. Its local limit accepts
1–1000 and offset 0–100000; start at offset 0 with a limit no greater than 100 and
respect any smaller backend limit. Listing a delisted contract never makes it
eligible for order entry. Fetch only the bounded metadata required by the task.

`futures.market.adl-risk-states` returns settlement plus a contract-to-risk-state
map. It is market risk information, not the account's ADL rank or a liquidation
price. If the map exceeds the output bound, mark it incomplete rather than
reporting absent contracts as safe; use an approved bounded output allowance or
stop. The endpoint has no per-contract filter; a snapshot exceeding the task's
market/record budget needs explicit bounded expansion or must remain unavailable
for that task. None of these point-in-time reads creates a subscription.
