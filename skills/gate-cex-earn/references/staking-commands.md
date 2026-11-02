# Staking

Use command identifiers such as `pid` only to execute the CLI call. For normal
answers, apply the user-facing mapping in [staking models](models/staking.md) and
refer to the product name, asset, amount, and verified business outcome instead.

## Scope and source

Read find/assets/awards for the requested coin, product, lockup, conversion
rate and reward timing. `staking swap` is a state-changing stake/redeem conversion
under its side field, not a public quote. Verify its actual amount and side contract,
then inspect assets and awards. Liquid staking claims, wrapped-token identities,
reward claims and guaranteed yields must not be inferred from similar product names.
No dedicated SOL Boost claim or WBETH wrap/unwrap command is registered.

## Intent routing and product semantics

| User intent | Route | Required handling |
| --- | --- | --- |
| Products / APY / lockup / minimum | `earn.staking.find` | Compare the returned product's asset, minimum, lockup/redemption window and reward timing. Resolve the internal product identifier only for a later command. A high APY is not a guarantee or a liquidity ranking. |
| My staking assets / redeemable amount | `earn.staking.assets` | Show positions by product; distinguish staked, redeeming/locked and redeemable values. Do not call all assets a withdrawable balance. |
| Rewards / dividend history | `earn.staking.awards` | Present reward asset, amount and distribution date. Empty results do not prove that a product will not accrue rewards. |
| Stake / mint | `earn.staking.find` then `earn.staking.swap` with `side=0` | Resolve exactly one product internally, plus amount and source asset, before the Action Draft. `mint` is only an alias for stake in this product context. |
| Redeem / unstake | `earn.staking.assets` then `earn.staking.swap` with `side=1` | Resolve exactly one held product internally and verify redeemable amount before the Action Draft. |
| Cancel a redemption | No CLI route | Do not submit another swap as a substitute; direct the user to the official product interface. |

If the returned product supports more than one funding coin, require the user to
choose the exact coin rather than guessing. If a coin has multiple product IDs,
present those products and ask the user to select one before a write. A dynamic
conversion rate may make received/redeemable units differ from principal; display
the returned rate and units rather than assuming a 1:1 conversion.

Command contract: use the currently installed and registered Gate CLI command surface. Run the exact leaf with `--help` immediately before execution; its registered flags and required fields are authoritative when they differ from this reference.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `earn.staking.assets` | `gate-cli cex earn staking assets` | read |
| `earn.staking.awards` | `gate-cli cex earn staking awards` | read |
| `earn.staking.find` | `gate-cli cex earn staking find` | read |
| `earn.staking.swap` | `gate-cli cex earn staking swap` | write |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="earn.staking.assets"></a>
### `gate-cli cex earn staking assets`

Operation ID: `earn.staking.assets`. Effect: **read**.

List staking assets

```text
gate-cli cex earn staking assets [flags]
```

API: `GET /api/v4/earn/staking/assets` (private).

Returns: [][StakingAsset](models/staking.md#model-stakingasset).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--coin` | `string` | No | Unset | Currency name |

<a id="earn.staking.awards"></a>
### `gate-cli cex earn staking awards`

Operation ID: `earn.staking.awards`. Effect: **read**.

List staking dividend records

```text
gate-cli cex earn staking awards [flags]
```

API: `GET /api/v4/earn/staking/award_list` (private).

Returns: [AwardListStruct](models/staking.md#model-awardliststruct).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--coin` | `string` | No | Unset | Currency name |
| `--page` | `int32` | No | `0` | Page number |
| `--pid` | `int32` | No | `0` | Product ID |

<a id="earn.staking.find"></a>
### `gate-cli cex earn staking find`

Operation ID: `earn.staking.find`. Effect: **read**.

List staking coins

```text
gate-cli cex earn staking find [flags]
```

API: `GET /api/v4/earn/staking/coins` (private).

Returns: [][StakingProduct](models/staking.md#model-stakingproduct).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--cointype` | `string` | No | Unset | Currency type: swap (voucher), lock (locked), debt (US Treasury) |

<a id="earn.staking.swap"></a>
### `gate-cli cex earn staking swap`

Operation ID: `earn.staking.swap`. Effect: **write**.

Swap staking coin (stake or redeem)

```text
gate-cli cex earn staking swap [flags]
```

API: `POST /api/v4/earn/staking/swap` (private).

Returns: [SwapCoinStruct](models/staking.md#model-swapcoinstruct).

API request model(s), assembled by the command: [SwapCoin](models/staking.md#model-swapcoin). JSON flags supply only the field described by that flag.

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--amount` | `string` | Yes | Unset | Amount (required) |
| `--coin` | `string` | Yes | Unset | Currency name (required) |
| `--pid` | `int32` | No | `0` | DeFi protocol ID |
| `--side` | `int32` | Yes | `0` | 0=stake, 1=redeem (required) |

## Verification and recovery

Use assets and awards for the selected coin. Distinguish credited staking units and
distributed rewards from an accepted write response. The consolidated staking order
query is excluded from this release; do not substitute it with an unrelated order
endpoint.

For a stake or redeem, the Action Draft must state product ID, input coin, amount,
side, applicable lock/redemption window and any displayed conversion-rate effect.
Verify that the Action Draft remains within the existing authorization grant. On a
rejected or ambiguous write, do not retry or submit a compensating swap; read the
matching asset state first.
Report quoted product rates separately from credited staking units and distributed
rewards. Never create a compensating stake or redemption automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex earn staking assets  --format json
```

Write template (fill required and conditional fields from the action contract):

```text
gate-cli cex earn staking swap --amount <amount> --coin <coin> --side <side> --format json
```
