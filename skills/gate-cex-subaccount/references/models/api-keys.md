# Subaccount API keys Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-subaccountkey"></a>
### SubAccountKey

`user_id?`: `int64`; `mode?`: `int32`; `name?`: `string`; `perms?`: [][SubAccountKeyPerms](#model-subaccountkeyperms); `ip_whitelist?`: `[]string`; `key?`: `string`; `state?`: `int32`; `created_at?`: `int64`; `updated_at?`: `int64`; `last_access?`: `int64`.

Field semantics: `state` — Status: 1-Normal 2-Frozen 3-Locked.

<a id="model-subaccountkeyperms"></a>
### SubAccountKeyPerms

`name?`: `string`; `read_only?`: `bool`.
