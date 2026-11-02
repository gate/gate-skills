# Gate CEX Market Interfaces

Read-only interface reference for Gate CEX market data. This file documents
commands, API routes, parameters, response fields, units, and compatibility.
This catalog covers REST/CLI snapshots and history. For bounded public WS
subscriptions across products, use [streams.md](streams.md). Local order-book
reconstruction and complete stock intraday history are not included.

## Sources and Capability Boundary

Use the [package command contract](market-commands.md),
[shared execution rules](../../_shared/cex/execution-cli.md),
[official Gate CLI](https://github.com/gate/gate-cli), and
[official API v4 documentation](https://www.gate.com/docs/developers/apiv4/en/).
The default public API base is `https://api.gateio.ws/api/v4`.

The official API, installed CLI and public WebSocket helper are separate
capability layers. Verify the exact installed leaf and flags before using any
CLI example; a documented API does not establish CLI availability. Prefer a
compatible installed CLI. Public compatibility reads below cover statistics,
insurance and stock metadata/orderbooks only when the CLI loses fields or lacks
a leaf. They do not authorize private data or configuration changes.

## Reference Layout

The accepted minimal implementation keeps this interface catalog and one shared
`streams.md`, with `futures-streams.md` retained for compatibility. Product
sections provide the required capabilities without eight duplicated files or a
replacement of this catalog. Preserve the CrossEx/Flash Swap/compatibility anchors in this catalog. This is the implementation delivery layout; file
names/headings in older proposal examples do not define additional capabilities.

## Interface Composition Boundary

The tables list independent interfaces, required parameters and actual API/CLI
defaults. Resolve canonical identifiers from instrument metadata and the user's
context. Products and settlement paths are distinct; data or errors from one
are not values for another.

## Missing Inputs and Default Resolution

Use the current conversation's confirmed instrument and original intent before
asking again. With no asset/context, ask one concise question for all missing
identity choices; treat the turn as awaiting_user_input, not an API failure.
After the reply, continue the original lookup/read rather than repeating solved
questions. Keep this internal state out of the user's market-data answer.

For a bare base asset with no product or quote currency, resolve Spot-first:
perform a directed metadata lookup for `<BASE>_USDT`. If it exists uniquely,
use it and disclose Gate Spot/USDT as the selected default. Only when metadata
explicitly confirms that Spot pair does not exist, discover the same-name
USDT-settled perpetual; use it only if unique and disclose both the missing Spot
pair and the Perpetual fallback. Ambiguous candidates require a choice. A
timeout, HTTP error, rate limit, closed market or empty history/book does not
establish nonexistence and never triggers this fallback.

Explicit product, quote currency, settlement or expiry always overrides defaults.
An explicit Leverage request reuses Spot market data and may resolve a bare base
to `<BASE>_USDT`, but must stay Leverage and cannot fall back to Perpetual. An
explicit Perpetual request goes directly to Perpetual; if settlement is omitted,
use only a documented CLI settlement default and disclose it. Options/Delivery
need a returned canonical contract or an explicit user selection rule; do not
invent expiry/strike. Do not turn a stock into a CFD or resolve an ambiguous
Alpha symbol without chain/address identity.

Preserve supplied periods/counts across clarification. Apply documented interface
defaults only to still-missing nonidentity parameters and disclose material ones.
Once a user supplies ETH or ETH_USDT after a rules question, apply these rules
and perform the actual metadata read; do not ask the same product/pair question
again when the declared resolution already makes it unique.

## REST Environment and Compatibility Reads

All CLI and fallback reads in one result must use the same effective API base.
`GATE_BASE_URL` overrides the selected CLI profile's base; the built-in production
base applies only if neither is configured. Before a fallback, explicitly set
`GATE_BASE_URL` to that already-selected base (scheme/host/optional configured
prefix, without `/api/v4`, credentials, query or fragment). The examples fail
when it is unset; never silently fall back to production. Do not change saved
profiles or print credentials to discover a base. Use the masked `config list`
if profile selection needs checking. HTTP is permitted only for an explicitly
configured testing base; production uses HTTPS. Keep paths below fixed, send no
credentials/cookies and follow no redirects. Label environment and observation
time in the answer; an unavailable testing field remains unavailable there.

When production WS is explicitly selected separately, validate canonical
instruments with a per-command production CLI override, e.g.
`GATE_BASE_URL=https://api.gateio.ws gate-cli cex stock market symbol --symbols AAPL --format json`.
This does not change the saved testing configuration. Keep that production
metadata and WS result separate from testing REST; never use subscription ACK
alone as proof of metadata, activity or complete history.

## Command and Parameter Conventions

Prefix every command in the tables with `gate-cli cex`; use `--format json` for
business reads. For example, `spot market ticker` means
`gate-cli cex spot market ticker --pair BTC_USDT --format json`.

- Bare parameter names are required CLI flags; `[name, ...]` are optional flags.
  `[]` means no leaf-specific flags. `<table-id>` is a positional argument,
  **not** a `--table-id` flag.
- API routes are relative to the base URL. `public` means no API key is required;
  `auth` means APIv4 authentication is required. Neither status grants permission
  to configure credentials, log in, or perform writes.
- Flag names are CLI names, not necessarily HTTP parameter names. Spot `--pair`
  maps to `currency_pair`; order-book `--depth` maps to `limit`; stock
  `--page-size` maps to `page_size`; CFD `--type` maps to `kline_type`.
- Check `gate-cli --version` and the exact leaf's `--help`. An unknown child can
  print parent help and exit zero: the `Usage` line must name the requested leaf.
- Required/optional notation describes the source CLI inventory. The official
  API can require a parameter that the CLI defaults, or expose parameters that
  this CLI does not forward. Do not invent flags from HTTP parameter names.
- Record stdout, stderr, exit status, observation time, and source data time
  separately. Exit zero is not sufficient if stdout is empty or stderr contains
  a structured error. Do not use `--debug` routinely: CLI builds can
  print raw HTTP headers/body; never expose credentials or private payloads.

## Field and Time Contracts

- Preserve product, canonical identity and settlement/quote currency. Leveraged
  Spot shares Spot prices; account margin mode is separate. A symbol alone does
  not identify a chain token or make a CFD equivalent to a stock.
- Spot candle arrays are `[t, quote_volume, close, high, low, open, base_volume, closed]`
  when present; `closed` can be absent. Futures/Delivery use `t,o,h,l,c,v`;
  contract volume is not automatically base-asset volume. Open bars can change.
- Bar time, message/envelope time and observation time are distinct. Stock
  trading dates use the exchange calendar/timezone, not the receipt date.
- Last, mark and index are different price fields. Option premium is not the
  underlying price or necessarily cash paid per contract.
- For a verified USDT linear contract, notional is `abs(contracts) * quanto_multiplier * price`;
  other contract types require their own unit conversion. Preserve exact decimals.
- Funding rate applies to its funding cycle, not account counts or directional bias.
  Public liquidation limits define observed samples, not a complete market window
  or historical severity baseline. Risk-limit-table IDs must come from metadata.
- Missing fields remain unavailable, not zero. HTTP/CLI errors, decode failures,
  empty arrays and stale bars are distinct outcomes. Disclose actual returned
  coverage; limited or empty data does not justify replacing the user's product.

## Spot

Insurance history requires explicit `from` and `to` Unix seconds with
`0 < from <= to`. The CLI requires both flags and rejects zero, negative or
reversed ranges. Ask for a missing time range rather than inventing one.
The full currency list can exceed transport/output limits. Output truncation is
a separate limit; a truncated list never proves exhaustive coverage. For a
single known currency prefer the directed `currency` lookup. For complete
currency/pair counts, use the bounded catalog exception in
[CLI execution](../../_shared/cex/execution-cli.md): fetch the full list to a
local file with an 8MiB output cap and count the complete JSON array locally.
Report the count of returned entries with the environment and query time;
do not equate it with currently tradable assets or count a truncated result.

| CLI endpoint | Key params | API route | Access | Description |
| --- | --- | --- | --- | --- |
| `spot market time` | `[]` | `GET /spot/time` | public | Get server time |
| `spot market currencies` | `[]` | `GET /spot/currencies` | public | List currencies |
| `spot market currency` | `currency` | `GET /spot/currencies/{currency}` | public | Get one currency |
| `spot market pairs` | `[]` | `GET /spot/currency_pairs` | public | List spot pairs and trading rules |
| `spot market pair` | `pair` | `GET /spot/currency_pairs/{currency_pair}` | public | Get one pair's status, precision, and limits |
| `spot market ticker` | `pair` | `GET /spot/tickers` | public | Get one pair's ticker |
| `spot market tickers` | `[]` | `GET /spot/tickers` | public | Get all spot tickers |
| `spot market orderbook` | `pair [depth]` | `GET /spot/order_book` | public | Get a bids/asks snapshot |
| `spot market trades` | `pair [limit]` | `GET /spot/trades` | public | Get recent public trades |
| `spot market candlesticks` | `pair [interval, limit]` | `GET /spot/candlesticks` | public | Get OHLC history |
| `spot market insurance` | `currency, from, to [business, limit]` | `GET /spot/insurance_history` | public | Get spot insurance history |

Response and unit notes:

- Pair metadata provides precision and limits. Ticker prices are quote-currency
  prices per base unit; preserve base volume and quote volume labels.
- Order books use bids/asks snapshots; trades have their own record times.
- Spot candlesticks are positional arrays. Read the selected API's array layout
  rather than interpreting them as futures `{t,o,h,l,c,v}` objects.

## Futures

| CLI endpoint | Key params | API route | Access | Description |
| --- | --- | --- | --- | --- |
| `futures market contracts` | `[limit, offset, settle]` | `GET /futures/{settle}/contracts` | public | List contracts |
| `futures market contract` | `contract [settle]` | `GET /futures/{settle}/contracts/{contract}` | public | Get multiplier, precision, limits, and status |
| `futures market index-constituents` | `index [settle]` | `GET /futures/{settle}/index_constituents/{index}` | public | Get index constituents |
| `futures market risk-limit-tiers` | `[contract, limit, settle]` | `GET /futures/{settle}/risk_limit_tiers` | public | Get risk tiers |
| `futures market risk-limit-table` | `<table-id> [settle]` | `GET /futures/{settle}/risk_limit_table` | public | Get one risk-limit table |
| `futures market ticker` | `contract [settle]` | `GET /futures/{settle}/tickers` | public | Get one contract's ticker |
| `futures market tickers` | `[settle]` | `GET /futures/{settle}/tickers` | public | Get all contract tickers |
| `futures market orderbook` | `contract [depth, settle]` | `GET /futures/{settle}/order_book` | public | Get a bids/asks snapshot |
| `futures market trades` | `contract [limit, settle]` | `GET /futures/{settle}/trades` | public | Get recent public trades |
| `futures market candlesticks` | `contract [interval, limit, settle]` | `GET /futures/{settle}/candlesticks` | public | Get trade, mark, or index OHLC; see contract convention below |
| `futures market stats` | `contract [interval, limit, settle]` | `GET /futures/{settle}/contract_stats` | public | Get time-series volume, open-interest, long/short, and taker-flow statistics |
| `futures market funding-rate` | `contract [limit, settle]` | `GET /futures/{settle}/funding_rate` | public | Get historical funding rates |
| `futures market batch-funding-rates` | `contracts [settle]` | `POST /futures/{settle}/funding_rates` | public | Get funding rates for several contracts |
| `futures market premium` | `contract [interval, limit, settle]` | `GET /futures/{settle}/premium_index` | public | Get premium-index history |
| `futures market liquidations` | `[contract, limit, settle]` | `GET /futures/{settle}/liq_orders` | public | Get recent public liquidation orders |
| `futures market insurance` | `[limit, settle]` | `GET /futures/{settle}/insurance` | public | Get insurance-fund history |

`settle` is optional in this inventory (default `usdt`); preserve the selected
settlement currency. CLI help lists `usdt` and `btc`; newer API enums may differ.
`batch-funding-rates` is a **read-only public POST**, not an order-writing route.
See [series conventions](#mark-and-index-candlesticks),
[statistics fields](#futures-statistics-fields), and
[insurance compatibility](#insurance-response-compatibility).

## Delivery

| CLI endpoint | Key params | API route | Access | Description |
| --- | --- | --- | --- | --- |
| `delivery market contracts` | `[]` | `GET /delivery/{settle}/contracts` | public | List delivery contracts |
| `delivery market contract` | `contract` | `GET /delivery/{settle}/contracts/{contract}` | public | Get one contract, including expiry and rules |
| `delivery market risk-limit-tiers` | `contract` | `GET /delivery/{settle}/risk_limit_tiers` | public | Get risk tiers |
| `delivery market tickers` | `[contract]` | `GET /delivery/{settle}/tickers` | public | Get one or all delivery tickers |
| `delivery market order-book` | `contract [limit]` | `GET /delivery/{settle}/order_book` | public | Get a bids/asks snapshot |
| `delivery market trades` | `contract [limit]` | `GET /delivery/{settle}/trades` | public | Get recent public trades |
| `delivery market candlesticks` | `contract [interval, limit]` | `GET /delivery/{settle}/candlesticks` | public | Get OHLC history |
| `delivery market insurance` | `[limit]` | `GET /delivery/{settle}/insurance` | public | Get insurance-fund history |

The API uses a settlement path parameter; this inventory exposes no `--settle`
leaf flag for delivery. The current official delivery API documents `usdt`.
Do not infer delivery settlement from a perpetual contract or invent a CLI flag.
Contract metadata includes `expire_time`, `settle_price`, `settle_price_interval`,
and `settle_price_duration`. `mark_type` is deprecated; it is not a reliable
settlement-method field. `settle_price_interval` and `settle_price_duration` are
timing parameters, not a specification of the settlement price source or aggregation
algorithm. Mark/index prefixes also apply to delivery candles.

## Options

| CLI endpoint | Key params | API route | Access | Description |
| --- | --- | --- | --- | --- |
| `options market underlyings` | `[]` | `GET /options/underlyings` | public | List option underlyings |
| `options market expirations` | `underlying` | `GET /options/expirations` | public | List expirations |
| `options market contracts` | `underlying [expiration]` | `GET /options/contracts` | public | List contracts for an underlying |
| `options market contract` | `contract` | `GET /options/contracts/{contract}` | public | Get contract details |
| `options market underlying-tickers` | `underlying` | `GET /options/underlying/tickers/{underlying}` | public | Get the underlying ticker |
| `options market underlying-candlesticks` | `underlying [interval, limit]` | `GET /options/underlying/candlesticks` | public | Get underlying OHLC |
| `options market tickers` | `underlying` | `GET /options/tickers` | public | List option tickers |
| `options market order-book` | `contract [interval, limit]` | `GET /options/order_book` | public | Get an option order-book snapshot |
| `options market trades` | `[contract, limit]` | `GET /options/trades` | public | Get recent option trades |
| `options market candlesticks` | `contract [interval, limit]` | `GET /options/candlesticks` | public | Get option OHLC |
| `options market settlements` | `underlying` | `GET /options/settlements` | public | List settlement history |
| `options market settlement` | `at, contract, underlying` | `GET /options/settlements/{contract}` | public | Get one settlement record |

Use API-returned underlying and contract identifiers. `expiration` and `at`
are Unix seconds; sort expiration timestamps before describing the nearest one.
Contract `multiplier`, quote unit, and premium-per-contract semantics are separate
facts: do not infer the cash cost of one contract from a displayed quote alone.

## Stocks

| CLI endpoint | Key params | API route | Access | Description |
| --- | --- | --- | --- | --- |
| `stock market exchanges` | `[]` | `GET /stock/exchanges` | public | List supported exchanges |
| `stock market symbols` | `[exchange, page, page-size, symbols, with-desc-i18n]` | `GET /stock/symbols` | public | List stock symbols |
| `stock market symbol` | `symbols [exchange, page, page-size]` | `GET /stock/symbols/detail` | public | Get stock symbol details |
| `stock market fee-rate` | `[]` | `GET /stock/fee-rate` | public | Get public fee-rate data |
| `stock market orderbook` | `symbol` | `GET /stock/market/{symbol}/orderbook` | public | Get a stock order-book snapshot |

Check whether the installed CLI exposes each of these five leaves; prefer
compatible leaves when available. Otherwise use the bounded public compatibility
reads below for metadata and orderbooks only.
The official order-book response is `{data: {symbol, bids, asks}, timestamp}`;
level price is `p`, and envelope `timestamp` is Unix milliseconds. The documented
book does not guarantee a quantity field on every level. This inventory has no
stock ticker, candlestick, or public trade-tape leaf. A stock order-book quote is
not a last-traded ticker. Stock and similarly named CFD instruments are distinct.
Stock last-trade/session and candle subscriptions are outside this REST/CLI catalog.
These REST/CLI gaps are not proof that public Stock WS is unavailable.

## TradFi / CFD

| CLI endpoint | Key params | API route | Access | Description |
| --- | --- | --- | --- | --- |
| `tradfi market categories` | `[]` | `GET /tradfi/symbols/categories` | public | List symbol categories |
| `tradfi market symbols` | `[]` | `GET /tradfi/symbols` | public | List TradFi symbols |
| `tradfi market symbol` | `symbol` | `GET /tradfi/symbols/detail` | auth | Get symbol details; private in the current CLI |
| `tradfi market ticker` | `symbol` | `GET /tradfi/symbols/{symbol}/tickers` | public | Get one symbol's ticker |
| `tradfi market kline` | `symbol [limit, type]` | `GET /tradfi/symbols/{symbol}/klines` | public | Get OHLC history |

Symbol detail is authenticated; categories, symbol list, ticker, and K-line
are public in the referenced API. CFD ticker fields include `last_price`,
`bid_price`, `ask_price`, `highest_price`, and `lowest_price` inside `data`.
Envelope `timestamp` is milliseconds; candle `t` is seconds.

For `kline`, CLI `--type` is forwarded as HTTP `kline_type`. The current API
requires `kline_type` in `1m, 15m, 1h, 4h, 1d, 7d, 30d`; `limit` is at most 500.
The CLI defaults to `1m` and maps legacy aliases `M1/M15/H1/H4/D1` to
`1m/15m/1h/4h/1d`. Prefer explicit API intervals, e.g. `--type 1m` for one minute.
The API itself does not accept these aliases; five-minute and thirty-minute
periods remain unsupported. API `begin_time` and `end_time` are seconds but are not
exposed as flags in this inventory. No public order-book or trade-tape leaf is
listed; ticker bid/ask are not an order-book depth response.

## CrossEx

**CLI availability:** CrossEx may be unpublished in the installed CLI. The six
command names below are historical inventory, not an availability guarantee.
Do not invoke them or treat parent help with exit 0 as leaf discovery; verify
that the returned Usage names the exact requested command. API/quantity notes
remain reference material, not authorization to bypass release restrictions.

| CLI endpoint | Key params | API route | Access | Description |
| --- | --- | --- | --- | --- |
| `cross-ex market symbols` | `[symbols]` | `GET /crossex/rule/symbols` | public | Get CrossEx symbol rules |
| `cross-ex market risk-limits` | `symbols` | `GET /crossex/rule/risk_limits` | public | Get risk-limit information |
| `cross-ex market transfer-coins` | `[coin]` | `GET /crossex/transfers/coin` | public | Get supported transfer currencies |
| `cross-ex market fee` | `[]` | `GET /crossex/fee` | auth | Get cross-exchange fee rates |
| `cross-ex market discount-rate` | `[coin, exchange-type]` | `GET /crossex/coin_discount_rate` | auth | Get collateral discount rates |
| `cross-ex market interest-rate` | `[coin, exchange-type]` | `GET /crossex/interest_rate` | auth | Get margin-interest rates |

Use canonical CrossEx identifiers such as `BINANCE_FUTURE_ADA_USDT`. Public
rules and authenticated rates have different access requirements. The source inventory has no market ticker leaf; this does not imply that the API lacks one. Ticker/funding API additions requiring authentication are outside these public compatibility paths.
Do not describe the CLI gap as absence of the API or substitute Gate-native prices.

### CrossEx Quantity Units

`qty`, `min_size`, `lot_size`, `max_market_size`, and `max_limit_size` use
CrossEx's normalized **quantity**, not the native venue's contract count.
`contract_size` is deprecated (the official schema says quantities are unified);
an empty value does not authorize inventing a multiplier. Do not import
Gate-native `quanto_multiplier` or label these fields as contracts.

For `BINANCE_FUTURE_ADA_USDT`, show `min_size=1` and `lot_size=1` as quantity
rules. Distinguish `min_notional` (quote-currency value) and `tick_size` (price
step). Name a base-asset unit only when established for the instrument; otherwise
retain the raw `qty` unit and explain the boundary. If the user explicitly gives
native contracts, obtain a verified conversion or clarify the normalized amount;
never silently pass that count as `qty`. Use decimal arithmetic for conversions
and step validation. Public rule queries do not require account/fee probes.

## Alpha

`--currency` is the canonical Alpha currency ID returned by metadata, not a
display ticker such as USDS. Resolve symbols using paginated currency metadata
and available name/chain/address fields; use a unique returned ID or ask for
chain/address when ambiguous. Do not invent an ID from a symbol or silently
scan an unbounded list. Before querying tokens, convert every chain code from
user input or metadata to lowercase explicitly; the CLI forwards it unchanged.
Preserve addresses. Lowercasing does not establish API support or resolve
aliases: SOL becomes sol, not solana; verify aliases through metadata.
A successful HTTP status carrying an error object is still a business failure.

| CLI endpoint | Key params | API route | Access | Description |
| --- | --- | --- | --- | --- |
| `alpha market currencies` | `[currency, limit, page]` | `GET /alpha/currencies` | public | List Alpha currencies |
| `alpha market tickers` | `[currency, limit, page]` | `GET /alpha/tickers` | public | List Alpha tickers |
| `alpha market tokens` | `[address, chain, page, platform]` | `GET /alpha/tokens` | public | Resolve Alpha token metadata |

Currency and token metadata provide identifiers, chain and address context;
a display symbol is not globally unique. Ticker access does not imply that this
CLI exposes Alpha order books, public trades, or K-lines: none are in this inventory.
Pagination is explicit; one page is not an exhaustive supported-asset list.

## Flash Swap

| CLI endpoint | Key params | API route | Access | Description |
| --- | --- | --- | --- | --- |
| `flash-swap pairs` | `[currency, limit, page]` | `GET /flash_swap/currency_pairs` | public | List supported flash-swap pairs |

Pair records include `sell_currency`, `buy_currency`, `sell_min_amount`,
`sell_max_amount`, `buy_min_amount`, and `buy_max_amount`. Check the requested
direction; `A → B` does not prove `B → A`. The pair list is not a conversion quote.
Quote/preview and execution endpoints are outside this market-interface catalog.

### Direction-Aware Pair Pagination

- `currency` selects related pairs, not a sell direction. Match both
  `sell_currency` and `buy_currency`; each row's min/max applies to that direction.
- Use `page`/`limit`, preserving the same currency filter across pages. The CLI
  default limit is 1000. A successful empty JSON array ends traversal; a short
  nonempty page does not prove exhaustion.
- De-duplicate on `(currency_pair, sell_currency, buy_currency)`. An error,
  malformed body, repeated page or a reached local request/page budget means
  partial coverage, never an exhausted list or proof of non-support.
- Retain fetched rows for counts and labelled samples. Report the observed
  pages and coverage; a changing pair list is not an atomic or executable quote.

## Mark and Index Candlesticks

Both `GET /futures/{settle}/candlesticks` and
`GET /delivery/{settle}/candlesticks` define the following contract convention:

| Series | Futures example | Delivery example |
| --- | --- | --- |
| Traded price | `BTC_USDT` | A returned dated contract such as `BTC_USDT_YYYYMMDD` |
| Mark price | `mark_BTC_USDT` | `mark_<canonical dated contract>` |
| Index price | `index_BTC_USDT` | `index_<canonical dated contract>` |

Validate the underlying contract before adding a prefix. Candles from these APIs
have `t` (Unix seconds), `o/h/l/c` (quote-currency prices) and `v` (contracts when
applicable). Mark/index series do not represent traded volume. Do not label
traded candles as mark/index candles or interpret a zero mark volume as no trading.

The APIs document at most 2,000 points per request. `limit` is mutually exclusive
with `from` / `to`; those time filters are API parameters and are not exposed as
flags by these inventory leaves. Use the selected product's documented interval
enum; do not copy spot, futures, delivery, and CFD enums across products.

```bash
gate-cli cex futures market candlesticks --contract mark_BTC_USDT --settle usdt --interval 1h --limit 3 --format json
gate-cli cex futures market candlesticks --contract index_BTC_USDT --settle usdt --interval 1h --limit 3 --format json
```

## Futures Statistics Fields

API: `GET /futures/{settle}/contract_stats`. CLI: `futures market stats`.
API query parameters are `contract` (required), `from`, `interval`, and `limit`;
`from` is not exposed by this inventory's CLI leaf. Statistics intervals in the
CLI inventory are `5m, 15m, 30m, 1h, 4h, 1d`.

| Field | Meaning / unit |
| --- | --- |
| `time` | Statistics timestamp, Unix seconds |
| `open_interest` | Total open interest, contracts |
| `open_interest_usd` | Open interest in quote-currency notional |
| `lsr_account` | Long/short position-user ratio |
| `lsr_taker` | Long/short taker ratio; a ratio, not an absolute volume |
| `top_lsr_account` | Top-trader long/short account ratio |
| `top_lsr_size` | Top-trader long/short position-size ratio |
| `top_long_size`, `top_short_size` | Top-trader long/short position sizes, contracts |
| `long_taker_size`, `short_taker_size` | Long/short taker traded volume, contracts |
| `top_long_account`, `top_short_account` | Top-trader long/short account counts |
| `long_users`, `short_users` | Long/short user counts |
| `mark_price` | Mark price in quote currency |
| `long_liq_size`, `short_liq_size` | Long/short liquidations, contracts |
| `long_liq_amount`, `short_liq_amount` | Long/short liquidations in base currency |
| `long_liq_usd`, `short_liq_usd` | Long/short liquidations in quote currency |
| `long_liq_usd_new`, `short_liq_usd_new` | New quote-currency liquidation notionals; USDT formula uses liquidation contracts × contract multiplier × mark price |

The official schema marks these fields optional. Preserve newly returned fields,
explicit zero values, interval, timestamp, settlement, and units. Do not replace
period statistics with funding rates or an arbitrarily short trade sample.
`position_size` from a contract-detail response is the total held by long users;
it must not silently replace the `contract_stats.open_interest` measure.

**CLI compatibility:** typed SDK-backed adapters may omit newer fields or
serialized zeros, including fields
needed for taker flow and large-trader ratios. A missing CLI field is not an API
gap or proof of zero. Preserve optional/new API fields when using raw GET.

### Statistics Read and Compatibility Path

`contract_stats` provides contract OI, long/short ratios and interval taker flow.
The request accepts a canonical contract, settlement, interval and limit. The
example below uses `interval=5m`, `limit=3`; these sample arguments are not a
mandatory user-request default. Ticker funding, contract `position_size` and
trade samples are different datasets.

Prefer a full-field CLI result when available. If the installed adapter is known
to drop requested statistics fields, use the raw public GET below directly.
Otherwise inspect the fields once and use the same GET if required fields are absent. Do not repeat a known
lossy CLI request or scrape `--debug` logs. No keys, account setup or signing are needed for this narrow compatibility read, and no private endpoint is covered by this exception.

```bash
: "${GATE_BASE_URL:?Set the same effective API base used by this CLI query}"
curl --disable --fail --silent --show-error --proto '=http,https' --max-redirs 0 \
  --connect-timeout 5 --max-time 20 --get \
  "${GATE_BASE_URL%/}/api/v4/futures/usdt/contract_stats" \
  --data-urlencode 'contract=BTC_USDT' \
  --data-urlencode 'interval=5m' --data-urlencode 'limit=3' \
  --header 'Accept: application/json' --header 'X-Gate-Size-Decimal: 1'
```

Keep `--disable` first; do not load curl configuration, follow redirects, attach
credentials/cookies, or accept an arbitrary host/path. The only compatibility
route is `${GATE_BASE_URL}/api/v4/futures/{settle}/contract_stats`, using
the selected `usdt` or `btc` settlement and documented query parameters. Do not
invent CLI flags for API-only parameters. HTTP errors, non-array JSON and parse
errors are failures, not successful empty statistics.

Retain the original response and all fields, including unknown future fields
and explicit zeros. Keep decimal strings and large quantities exact; do not
round-trip the raw evidence through binary floats or an old typed SDK. Show
`open_interest`, requested ratio fields, `long_taker_size` and
`short_taker_size` when returned, with timestamp, interval and units. Missing
optional API fields remain unknown, never zero. Label computed percentages as
derived; taker buy/sell size is traded volume, not newly opened long/short OI.

```bash
gate-cli cex futures market stats --contract BTC_USDT --settle usdt --interval 5m --limit 3 --format json
```

## Insurance Response Compatibility

Futures insurance is public `GET /futures/{settle}/insurance`, with `limit`.
SDK-backed CLI builds can fail to decode numeric
`b` despite HTTP 200: exit 1, error on stderr and no business JSON on stdout.
Prefer a verified fixed CLI; if decoding still fails, use the same-environment
GET below. Do not infer capability from the version string alone.
Do not count parsing stderr/error payload as successful CLI business output.

```bash
: "${GATE_BASE_URL:?Set the same effective API base used by this CLI query}"
curl --disable --fail --silent --show-error --proto '=http,https' --max-redirs 0 \
  --connect-timeout 5 --max-time 20 --get \
  "${GATE_BASE_URL%/}/api/v4/futures/usdt/insurance" \
  --data-urlencode 'limit=3' --header 'Accept: application/json'
```

This exception permits only the selected API base and fixed insurance path,
`usdt` or `btc` settlement, and `limit=1..100` (default 3). No credentials, curl configuration,
redirects, retries or private HTTP. The successful body must be an array of
records with `t` (Unix seconds) and `b` (settlement-currency balance). Preserve
numeric/string balances, exact decimals, explicit zero and new fields. Missing
`b`, HTTP errors, malformed/non-array responses are unavailable, never zero.
Show the settlement unit, each data timestamp and query observation time.
The response provides original t/b records. Balance changes and returns are
derived values, not API fields; decimal parsing preserves exact balance values
(`parse_float=Decimal` for numeric JSON).
Delivery uses the separate fixed public route `/delivery/usdt/insurance`. Select the product explicitly
and never substitute one insurance balance for the other.

## Stock Read Compatibility

Stock symbols and quotes belong to the stock product, not same-name TradFi/CFD
or crypto instruments. If available and compatible, prefer
`stock market symbol` and `stock market orderbook`.
The two independent public GET templates below expose metadata and orderbook;
metadata defines canonical symbols and quote units used to interpret the book.
The compatibility path permits at most one call to each, not a requirement to
call both when only one capability is needed:

```bash
: "${GATE_BASE_URL:?Set the same effective API base used by this CLI query}"
curl --disable --fail --silent --show-error --proto '=http,https' --max-redirs 0 \
  --connect-timeout 5 --max-time 20 --get \
  "${GATE_BASE_URL%/}/api/v4/stock/symbols/detail" \
  --data-urlencode 'symbols=AAPL' --header 'Accept: application/json'
: "${GATE_BASE_URL:?Set the same effective API base used by this CLI query}"
curl --disable --fail --silent --show-error --proto '=http,https' --max-redirs 0 \
  --connect-timeout 5 --max-time 20 --get \
  "${GATE_BASE_URL%/}/api/v4/stock/market/AAPL/orderbook" \
  --header 'Accept: application/json'
```

Only replace AAPL with **one validated canonical symbol** matching
`[A-Z][A-Z0-9.-]{0,15}`. Resolve it against returned metadata, not a CFD list.
Keep the selected API base and fixed path templates; encode the metadata query,
never derive an origin or arbitrary path from the instrument. No login, keys, redirects, retries, pagination, account
queries or config writes. Unknown/ambiguous symbols require clarification.
A nonempty error `label`, invalid/missing `data`, HTTP or parse error is a
failure, not a successful empty stock book.

Metadata is `data.list` with `symbol`, `exchange`, `quote_currency`,
`settlement_currency`, and trading rules; do not conflate quote and settlement.
Book data is `{symbol, bids, asks}` with level price `p` and level `type` when
returned. Verify the returned symbol. Show available bid/ask price samples in
the metadata quote currency and the response envelope's millisecond timestamp,
plus observation time. Sizes are **unknown when absent**, never zero: do not
invent quantity, depth, spread-weighted execution, last trade or turnover.
An empty side is unavailable for that side. No stock last-traded ticker, candles
or trades are provided by these two routes. A book midpoint is not a last-trade or session-state field.
A book price is not proof of an executable quote or a fresh exchange trade.

## Official References

- [Spot](https://www.gate.com/docs/developers/apiv4/zh_CN/spot/)
- [Futures / ContractStat / InsuranceRecord](https://www.gate.com/docs/developers/apiv4/zh_CN/futures/)
- [Delivery](https://www.gate.com/docs/developers/apiv4/zh_CN/delivery/)
- [Options](https://www.gate.com/docs/developers/apiv4/zh_CN/options/)
- [Stocks](https://www.gate.com/docs/developers/apiv4/zh_CN/stock/)
- [CFD](https://www.gate.com/docs/developers/apiv4/zh_CN/cfd/)
- [CrossEx](https://www.gate.com/docs/developers/apiv4/zh_CN/crossex/)
