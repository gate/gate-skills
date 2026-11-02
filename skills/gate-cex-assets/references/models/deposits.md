# Deposit information and records Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-currencychain"></a>
### CurrencyChain

`chain?`: `string`; `name_cn?`: `string`; `name_en?`: `string`; `contract_address?`: `string`; `is_disabled?`: `int32`; `is_deposit_disabled?`: `int32`; `is_withdraw_disabled?`: `int32`; `decimal?`: `string`; `is_tag?`: `int32`.

<a id="model-depositaddress"></a>
### DepositAddress

`currency`: `string`; `address`: `string`; `min_deposit_amount?`: `string`; `multichain_addresses?`: [][MultiChainAddressItem](#model-multichainaddressitem).

<a id="model-depositrecord"></a>
### DepositRecord

`id?`: `string`; `txid?`: `string`; `timestamp?`: `string`; `amount`: `string`; `currency`: `string`; `address?`: `string`; `memo?`: `string`; `status?`: `string`; `refund_status?`: `string`; `chain`: `string`.

Field semantics: `status` — Transaction Status - BLOCKED: Deposit Blocked - DEP_CREDITED: Deposit Credited, Withdrawal Pending Unlock - DONE: Funds Credited to Spot Account - INVALID: Invalid Transaction - MANUAL: Manual Review Required - PEND: Processing - REVIEW: Under Compliance Review - TRACK: Tracking Block Confirmations, Pending Spot Account Credit.

<a id="model-multichainaddressitem"></a>
### MultiChainAddressItem

`chain?`: `string`; `address?`: `string`; `payment_id?`: `string`; `payment_name?`: `string`; `obtain_failed?`: `int32`; `min_confirms?`: `int32`.

<a id="model-savedaddress"></a>
### SavedAddress

`currency?`: `string`; `chain?`: `string`; `address?`: `string`; `name?`: `string`; `tag?`: `string`; `verified?`: `string`.

<a id="model-uidpushorder"></a>
### UidPushOrder

`id?`: `int64`; `push_uid?`: `int64`; `receive_uid?`: `int64`; `currency?`: `string`; `amount?`: `string`; `create_time?`: `int64`; `status?`: `string`; `message?`: `string`; `transaction_type?`: `string`.

Field semantics: `id` — Order ID; `status` — Withdrawal status: - CREATING: Creating - PENDING: Waiting for recipient (Please contact the recipient to accept the transfer on Gate official website) - CANCELLING: Cancelling - CANCELLED: Cancelled - REFUSING: Refusing - REFUSED: Refused - RECEIVING: Receiving - RECEIVED: Success.
