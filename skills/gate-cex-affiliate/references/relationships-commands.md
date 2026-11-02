# Affiliate relationships

## Scope and source

Use only the relationship/role and current application reads exposed here. partner application retrieves the recent application; it does not submit an application. Verify the managing role before viewing subordinate data. Affiliate relationships are distinct from consumer referral campaigns and do not grant trading or account-management authority.

CLI reference: [Gate CLI](https://github.com/gate/gate-cli). Check the installed official release for the exact command and parameters before execution; this catalog does not establish release availability.

Read [shared execution](../../_shared/cex/execution-cli.md) and [safety](../../_shared/cex/safety.md) once. Public operations need no credential; private reads need an applicable read grant, writes need the product grant and user authority. The backend determines exact route access; see [authentication](../../_shared/cex/cli-auth.md) for scope families. Command existence never proves account eligibility.

## Action index

| Operation ID | CLI command | Effect |
|---|---|---|
| `rebate.partner.application` | `gate-cli cex rebate partner application` | read |
| `rebate.partner.eligibility` | `gate-cli cex rebate partner eligibility` | read |
| `rebate.partner.sub-list` | `gate-cli cex rebate partner sub-list` | read |
| `rebate.sub-relation` | `gate-cli cex rebate sub-relation` | read |
| `rebate.user-info` | `gate-cli cex rebate user-info` | read |

## Invocation and parameter rules

Append `--format json` to business commands. Syntax blocks are templates; replace placeholders with validated values and pass each value as a separate argv item. Registration defaults below do not prove that an omitted value is sent: handlers can omit fields or impose conditional requirements. Never infer a write body from a response model. JSON request-model links define nested keys and types; `?` denotes SDK omission behavior, not permission to omit an API-required business field. Keep exact decimal amounts and identifiers.

Bound every read to the requested instrument/account/time and a limited record count. Use each leaf's actual pagination flags; if only offset exists, keep it within a small explicit task budget rather than crawling deeply.

<a id="rebate.partner.application"></a>
### `gate-cli cex rebate partner application`

Operation ID: `rebate.partner.application`. Effect: **read**.

Get recent partner application

```text
gate-cli cex rebate partner application
```

API: `GET /api/v4/rebate/partner/applications/recent` (private).

Returns: [PartnerApplicationResponse](models/relationships.md#model-partnerapplicationresponse).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="rebate.partner.eligibility"></a>
### `gate-cli cex rebate partner eligibility`

Operation ID: `rebate.partner.eligibility`. Effect: **read**.

Check partner eligibility

```text
gate-cli cex rebate partner eligibility
```

API: `GET /api/v4/rebate/partner/eligibility` (private).

Returns: [EligibilityResponse](models/relationships.md#model-eligibilityresponse).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

<a id="rebate.partner.sub-list"></a>
### `gate-cli cex rebate partner sub-list`

Operation ID: `rebate.partner.sub-list`. Effect: **read**.

Partner subordinate list

```text
gate-cli cex rebate partner sub-list [flags]
```

API: `GET /api/v4/rebate/partner/sub_list` (private).

Returns: [PartnerSubList](models/relationships.md#model-partnersublist).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--limit` | `int32` | No | `0` | Max records |
| `--offset` | `int32` | No | `0` | List offset |
| `--user-id` | `int64` | No | `0` | User ID filter |

<a id="rebate.sub-relation"></a>
### `gate-cli cex rebate sub-relation`

Operation ID: `rebate.sub-relation`. Effect: **read**.

Query user subordinate relation

```text
gate-cli cex rebate sub-relation [flags]
```

API: `GET /api/v4/rebate/user/sub_relation` (private).

Returns: [UserSubRelation](models/relationships.md#model-usersubrelation).

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--user-id-list` | `string` | Yes | Unset | Comma-separated user ID list (required) |

<a id="rebate.user-info"></a>
### `gate-cli cex rebate user-info`

Operation ID: `rebate.user-info`. Effect: **read**.

Get rebate user info

```text
gate-cli cex rebate user-info
```

API: `GET /api/v4/rebate/user/info` (private).

Returns: [][RebateUserInfo](models/relationships.md#model-rebateuserinfo).

Parameters: none beyond shared options and any positional arguments shown in the syntax.

## Verification and recovery

Report only the returned role, eligibility, subordinate relation or recent application state. None of these reads submits an application or grants a role.

For borrowed or conditional state, also verify remaining debt, active protections or exposure. Report estimates separately from charged fees and settled balances. Never create a compensating transaction automatically.

## Call templates

Templates are not executable examples. Replace angle-bracket values with validated inputs; JSON inputs must satisfy the linked nested model. Read the conditional product rules before a write.

Read template (fill required and conditional fields from the action contract):

```text
gate-cli cex rebate partner application  --format json
```
