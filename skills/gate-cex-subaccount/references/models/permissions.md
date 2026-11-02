# Permission boundaries Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-accountdetailkey"></a>
### AccountDetailKey

`mode?`: `int32`.

<a id="model-accountkeyinfo"></a>
### AccountKeyInfo

`state?`: `int32`; `mode?`: `int32`; `name?`: `string`; `currency_pairs?`: `[]string`; `user_id?`: `int64`; `ip_whitelist?`: `[]string`; `perms?`: [][AccountKeyInfoPerms](#model-accountkeyinfoperms); `key?`: [AccountDetailKey](#model-accountdetailkey); `created_at?`: `string`; `updated_at?`: `string`; `last_access?`: `string`.

Field semantics: `state` — API key status: 1 - Normal, 2 - Locked, 3 - Frozen (can only be modified, default is 1 when creating)API Key Status: 1 - Normal, 2 - Locked, 3 - Frozen (can only be modified; default is 1 upon creation).

<a id="model-accountkeyinfoperms"></a>
### AccountKeyInfoPerms

`name?`: `string`; `read_only?`: `bool`.
