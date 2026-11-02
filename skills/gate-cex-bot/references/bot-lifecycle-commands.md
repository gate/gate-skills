# Bot discovery and lifecycle

## Scope and source

recommend reads suggested parameters; it neither approves a strategy nor guarantees profit. Preserve strategy type and returned portfolio reference for detail/running/stop. Stop affects continuing execution; verify terminal state plus residual holdings/positions. Do not auto-liquidate, restart or compensate. List only the requested portfolio set and redact unrelated trading data.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the trusted installed binary for the exact command and parameters before execution, including an existing dev build; this catalog does not establish capability availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `bot.detail` | `gate-cli cex bot detail` | read |
| `bot.recommend` | `gate-cli cex bot recommend` | read |
| `bot.running` | `gate-cli cex bot running` | read |
| `bot.stop` | `gate-cli cex bot stop` | write |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="bot.detail"></a>
### `gate-cli cex bot detail`

Operation ID: `bot.detail`. Effect: **read**.

Get strategy details

```text
gate-cli cex bot detail [flags]
```

API: `GET /api/v4/bot/portfolio/detail` (private).

Returns: [AiHubPortfolioDetailSuccessResponse](models/bot-lifecycle.md#model-aihubportfoliodetailsuccessresponse).

Apply [detail output requirements](#detail-and-stop-output), including the explicit stop-capability statement, when presenting the result.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `--strategy-id` | `string` | Yes | Unset | Strategy ID (required) |
| `--strategy-type` | `string` | Yes | Unset | Strategy type (required); used to dispatch to the underlying detail implementation |

<a id="bot.recommend"></a>
### `gate-cli cex bot recommend`

Operation ID: `bot.recommend`. Effect: **read**.

List AI Hub recommended strategies

```text
gate-cli cex bot recommend [flags]
```

API: `GET /api/v4/bot/strategy/recommend` (private).

Returns: [AiHubDiscoverSuccessResponse](models/bot-lifecycle.md#model-aihubdiscoversuccessresponse).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `--backtest-apr-gte` | `string` | No | Unset | Backtest annualized return lower bound |
| `--direction` | `string` | No | Unset | Market direction |
| `--exclude-recommendation-id` | `string` | No | Unset | Previous returned recommendation ID to exclude in refresh scene |
| `--invest-amount` | `string` | No | Unset | Investment amount |
| `--limit` | `int32` | No | `0` | Max results returned (filter scene capped at 10) |
| `--market` | `string` | No | Unset | Trading pair, e.g. BTC_USDT |
| `--max-drawdown-lte` | `string` | No | Unset | Max drawdown upper bound |
| `--refresh-recommendation-id` | `string` | No | Unset | Recommendation ID for scene=refresh; format strategy_type\|market[\|backtest_id] |
| `--scene` | `string` | No | Unset | Recommend scene: top1 / bundle / filter / refresh |
| `--strategy-type` | `string` | No | Unset | Recommendation type: spot_grid, margin_grid, infinite_grid, futures_grid, spot_martingale, smart_position |

<a id="bot.running"></a>
### `gate-cli cex bot running`

Operation ID: `bot.running`. Effect: **read**.

List currently-running strategies

```text
gate-cli cex bot running [flags]
```

API: `GET /api/v4/bot/portfolio/running` (private).

Returns: [AiHubPortfolioRunningSuccessResponse](models/bot-lifecycle.md#model-aihubportfoliorunningsuccessresponse).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `--market` | `string` | No | Unset | Filter by trading pair |
| `--page` | `int32` | No | `0` | Page number |
| `--page-size` | `int32` | No | `0` | Page size |
| `--strategy-type` | `string` | No | Unset | Filter by strategy type (six existing types, smart_position, futures_combo) |

<a id="bot.stop"></a>
### `gate-cli cex bot stop`

Operation ID: `bot.stop`. Effect: **write**.

Stop a running strategy

```text
gate-cli cex bot stop [flags]
```

API: `POST /api/v4/bot/portfolio/stop` (private).

Returns: [AiHubPortfolioStopSuccessResponse](models/bot-lifecycle.md#model-aihubportfoliostopsuccessresponse).

API request model(s), assembled by the command: [AiHubPortfolioStopRequest](models/bot-lifecycle.md#model-aihubportfoliostoprequest). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `--stop-mode` | `string` | No | Unset | smart_position only: market, limit, no_close (required for this type) |
| `--stop-options` | `string` | No | Unset | limit mode JSON: price and expiration (seconds), optional slip |
| `--strategy-id` | `string` | Yes | Unset | Strategy ID (required) |
| `--strategy-type` | `string` | Yes | Unset | Strategy type (required) |

## Verification and recovery

Use `bot.detail` for the exact type/portfolio and bounded `bot.running`; after `bot.stop`, verify stopped status and remaining orders/positions/funds. Residual exposure is a separate user decision.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex bot detail --strategy-id <strategy-id> --strategy-type <strategy-type> --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex bot stop --strategy-id <strategy-id> --strategy-type <strategy-type> --format json
```

An agent grant expiring does not stop an already running backend strategy. If the user requires a hard deadline or cumulative spending cap that the actual creation model/backend cannot enforce, stop that variant or obtain a different explicit instruction; do not promise an automatic stop, local timer or cross-session budget control.



## Product workflow requirements


Read [execution](../../_shared/cex/execution-cli.md). Supported leaves:

- `gate-cli cex bot running --strategy-type <type> --market <market> --page 1 --page-size 20` (filters optional; maximum size 50).
- `gate-cli cex bot detail --strategy-id '<id>' --strategy-type <type>`.
- `gate-cli cex bot stop --strategy-id '<id>' --strategy-type <type>` for existing default exits.

Use exact IDs as strings. Types are spot_grid, margin_grid, infinite_grid, futures_grid, spot_martingale, contract_martingale, smart_position and futures_combo, using the matching candidate and deployment. Instances are managed by authenticated owner regardless of whether Web/App/CLI or another supported client created them. Ambiguous targets require reading the running list and selecting one instance before a stop draft. Bulk stop is outside scope.

### Running list output

Every successful running-list answer includes the applied filters, current page, page size and total, followed by the actual returned instances. This also applies to an unfiltered first query, follow-up pages and empty pages. Use `data.page`, `data.page_size` and `data.total` from the response; a backend-adjusted page size takes precedence over the requested size. Describe omitted market/type filters as all markets/all types. Preserve the current filters and page size when the user asks for the next page.

For example, a response with page=1, page_size=20 and total=9, without filters, starts: "Filters: all markets, all types. Page 1, 20 per page, 9 total." Render this summary in the user's language and replace every value with the actual query/response values. For an empty page, retain that summary and say this page has no matching instances; an empty page alone does not mean total=0. If a pagination field is absent, label that value unavailable rather than deriving it from the requested flags or item count. A failed or malformed response remains an error, not an empty list.

Unified pages keep actual total and filters; do not independently paginate products and merge them. Portfolio market="" denotes multiple members: show assets/markets and per-member positions. Missing metrics stay absent; positions_status partial/unverified is not a zero balance. Ended instances use historical composition, not a recycled account.

### Detail and stop output

Every successful detail answer explicitly states the selected instance's stop capability from `data.stop_supported`: `true` means "Currently supports stopping"; `false` means "Currently does not support stopping". Render the statement in the user's language, alongside the instance ID/type, market, status and available base information, metrics and holdings. This requirement applies to both complete and partial details. A missing, null or invalid stop-capability field means "Stop capability unverified"; preserve an explicit `false` rather than treating it as missing. Lifecycle or settlement commentary does not replace this statement. Stop capability alone does not establish user authorization, approve a stop or prove funds have returned; retain the separate checks and confirmation gate below.

Detail may provide an owner-verified base while optional data is unavailable. If detail_status=partial, show unavailable_parts and their reasons; do not present the result as complete, infer zero holdings/profit, or infer permission to stop. Older SDKs may omit these new fields: preserve and display a message beginning with "partial detail; unavailable:" and explain its missing sections. Absence of a completeness marker does not prove a full result. A critical identity/ownership failure remains an error, never a partial result.

Before stopping, read the product-specific exit behavior in [spot grids](spot-grid-commands.md), [smart position](smart-position-commands.md) or [combo](futures-combo-commands.md) and [Bot confirmation gate](bot-workflows.md#bot-confirmation-gate). Extra mode/options require verified new flags; the old ID/type leaf must not silently drop them. Preserve refusal/advice, real ID and observed state. Stopping is accepted work, finished is a lifecycle observation, and funds return needs separate product facts. Never infer settlement merely from either status.

For a default exit that depends on a previously saved instance setting (such as a spot-grid sell/keep flag), verify that setting before an executable draft; an unspecified default cannot replace the missing fact. For smart_position, the explicitly selected stop-mode/options define the new exit behavior; verify the target/type and those actual CLI capabilities, then confirm that complete choice. It does not require a previously persisted stop configuration before the first stop. Futures combo uses its documented whole-portfolio exit. Missing holdings or settlement details remain unverified and must not be reported as zero or completed.

For martingale protection verification, a compatible generated SDK/CLI must preserve `data.configuration`. Spot configuration returns the saved `stop_loss_per_cycle`, `take_profit_ratio`, `price_deviation` and `max_orders` (additional entries, excluding the first); zero/negative stop-loss values are disabled legacy values, not effective protection. Contract configuration separates `invest_amount` from `first_order_size` and returns the persisted `stop_loss_price_rule.price`, `price_type` and `is_gte`. Keep all decimal strings unchanged. Missing configuration, an absent rule, an empty quantity or an unknown basis remains unverified; do not derive the rule from the create draft or claim that configuration proves execution. SDK v7.2.167 preserves configuration; an absent field in an actual response remains unverified. Readback proves saved settings, not that protection orders executed.

An exit0/code200 write with status unknown, operation_status pending or recovery_required=true is still unresolved. Preserve its ID/type and query that exact instance; do not announce running, stopped or settled and do not resend the write. An exit code alone cannot establish a lifecycle state. Explicit false progress values remain false; omitted progress is unverified.

## Bot response and route contract

These rules apply to the Bot APIs in this reference, not to other CEX products. Bot success requires a valid code=200 business envelope, correctly shaped data and the expected identity/state for the action. HTTP success or process exit alone is insufficient. Keep real IDs, label, trace_id, operation_status and recovery_required; reconcile the original instance on pending or unknown outcomes. A null collection tolerated by the CLI does not create any items or establish missing metrics as zero.

All Bot methods here require authentication. Current Bot mappings use legacy read for GET and POST; Agentic base includes that permission and can authorize Bot writes. It is not a read-only scope. Verify exact-route permission and preserve the selected account context through shared preflight. A request-side UID or confirmation field cannot authenticate an account.
