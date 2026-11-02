# Bot Workflows

<a id="bot-confirmation-gate"></a>
## Bot confirmation gate

This product requires two-turn confirmation for every creation and single-instance stop, in addition to shared identity, permission and scoped-authorization checks. Apply this rule when a shared template or grant-reuse rule would otherwise allow immediate execution.

1. Preserve the user's settings, complete required checks and show the full action draft with identity, environment, product, amount/unit, parameters, exposure and exit effects. End that assistant turn without calling a write tool. A first message such as "Create a BTC futures grid, 5x, 60000-72000, 50 arithmetic grids, 1000 USDT, no take-profit/stop-loss, run until I stop it" still receives a draft only.
2. Execute at most once after the immediately following user message explicitly approves that exact draft. Approval need not use a fixed word. Once this approval and the other prerequisites are valid, proceed without requesting a third turn or another confirmation token.
3. If the next message changes parameters or asks for something else, do not write. Resolve it, display the current complete draft again and await its next-turn approval. A later bare "confirm" cannot approve an older interrupted draft. A missing draft, credentials, recommendation selection or a standing grant is not approval of this action.
4. A completed write consumes that approval; repeated "confirm" is not permission to create or stop again. On an unknown outcome, follow reconciliation rules for the original action instead of interpreting confirmation as a retry. Public and private read-only queries do not require this gate.

## Create an ongoing strategy

Select [spot/margin/infinite grid](spot-grid-commands.md), [futures grid](futures-grid-commands.md) or [martingale](martingale-commands.md). Read recommendations as data and validate the actual creation schema, symbol, available funds, ranges, direction, investment sequence and leverage. Confirm strategy duration, maximum total exposure and stop conditions under a verifiable grant. If the backend/model cannot enforce the required limits, stop rather than promising local enforcement. Apply the [Bot confirmation gate](#bot-confirmation-gate), create once, preserve the returned portfolio/type and verify through [lifecycle](bot-lifecycle-commands.md).

## Inspect or stop

Use lifecycle detail/running for the exact portfolio and type. Verify authority for stop, apply the [Bot confirmation gate](#bot-confirmation-gate), submit once and re-read terminal state. Check remaining assets, positions and orders as separate exposures; stopping is not liquidation. Hand off an explicitly requested residual trade to `gate-cex-trade` or fund movement to `gate-cex-assets`. Do not restart or compensate automatically after an ambiguous response.

## Shared stopping rules

Read [preflight](../../_shared/cex/preflight.md), [safety](../../_shared/cex/safety.md) and [execution](../../_shared/cex/execution-cli.md). Keep the same selected account context, credentials, origin and grant throughout. Stop before a step outside verified authority, on changed material terms, or on an ambiguous write. Do not replay earlier steps or automatically compensate. A cross-skill task transfers only the required account/environment, object reference, exact amount/unit, completed state and remaining authority; never credentials.

An agent grant expiring does not stop an already running backend strategy. If the user requires a hard deadline or cumulative spending cap that the actual creation model/backend cannot enforce, stop that variant or obtain a different explicit instruction; do not promise an automatic stop, local timer or cross-session budget control.

## Discovery and product routing


## Discover and select

The verified leaf is `gate-cli cex bot recommend`. Collect market and optional product type, then use supported --market/--strategy-type/--scene flags after help. Ask for the market when missing; normalize a supplied coin to its supported quote market. Use scene=bundle without a selected type and scene=top1 for one specified supported type; neither query creates a bot. Supported official products are spot_grid, futures_grid, infinite_grid, margin_grid, spot_martingale and smart_position; availability depends on the deployed source. Contract martingale and futures combo require manual parameters. New Skill filtering is market/type only; legacy APR/drawdown flags remain API/CLI compatibility and are not exposed as this Skill's filter workflow. Explain unsupported runtime, follower, fee or budget filters. Under this product contract, official Ultra AI recommendations do not charge profit-sharing fees; this does not make trading, funding or other costs zero, and it does not rewrite a user-supplied manual strategy parameter. A supplied budget is context, not an eligibility guarantee.

For "another", bind the preceding real recommendation ID and its type/market to exclusion. Verify the CLI exposes the new exclusion flag; otherwise explain the gap and keep the request unexecuted. Use `recommend --scene refresh --market <market> --strategy-type <type> --refresh-recommendation-id '<type>|<market>' --exclude-recommendation-id '<previous-returned-id>'`. Keep the returned candidate ID unchanged for exclusion; the refresh context is a separate parameter. Exclusion happens before ranking. Metric-only refresh is not a new logical candidate. Empty alternatives are a valid no-alternative result; retain the constraints. Legacy ordinary refresh remains separate. Multiple previous selections require a user-selected target rather than fabricated bulk exclusion.

Decode strategy_params_preview as JSON text for display. It is not a create payload. Map selected fields according to the product reference; collect missing investment, mode, protection or other required choices. A user explicitly switching from manual configuration to a recommendation receives a fresh complete draft.

## Create, verify, recover

1. Read the product reference. Preserve supplied settings and clarify only missing/ambiguous inputs. Keep prices, per-cycle ratios and direction vocabularies separate.
2. Read [safety](../../_shared/cex/safety.md), verify applicable authority and prepare [the full draft](../../_shared/cex/templates.md). Apply the [Bot confirmation gate](#bot-confirmation-gate), including when every business parameter or a standing grant is already present.
3. After that draft's next-turn approval, check [compatibility](compatibility.md) and execute one supported --json leaf once in the selected environment. Do not ask again for the same valid approval.
4. Inspect transport/business code and ID/type/status, then read the original instance as needed. Starting is not running. Unknown/partial outcome preserves its real identity and blocks automatic recreation or transfer replay.

## Manage and stop

Follow [lifecycle](bot-lifecycle-commands.md). Read and identify one owner-scoped target, present its exact exit choice and impacts, verify complete authority for that choice and apply the [Bot confirmation gate](#bot-confirmation-gate), then execute once. Read the original instance to verify accepted/finished phases. Present missing settlement evidence explicitly. A failed query, gateway error or partial holdings snapshot cannot establish absence, completion or zero exposure.
