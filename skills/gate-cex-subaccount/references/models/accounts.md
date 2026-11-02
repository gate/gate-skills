# Subaccount administration Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-subaccount"></a>
### SubAccount

`remark?`: `string`; `login_name`: `string`; `password?`: `string`; `email?`: `string`; `state?`: `int32`; `type?`: `int32`; `user_id?`: `int64`; `create_time?`: `int64`.

Field semantics: `state` — Sub-account status: 1-normal, 2-locked.

<a id="model-subusermode"></a>
### SubUserMode

`user_id?`: `int64`; `is_unified?`: `bool`; `mode?`: `string`.
