# Withdrawals Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-uidpushwithdrawal"></a>
### UidPushWithdrawal

`receive_uid`: `int64`; `currency`: `string`; `amount`: `string`.

<a id="model-uidpushwithdrawalresp"></a>
### UidPushWithdrawalResp

`id?`: `string`.

Field semantics: `id` — Order ID.

<a id="model-withdrawalrecord"></a>
### WithdrawalRecord

`id?`: `string`; `txid?`: `string`; `block_number?`: `string`; `withdraw_order_id?`: `string`; `timestamp?`: `string`; `amount`: `string`; `fee?`: `string`; `currency`: `string`; `address?`: `string`; `type?`: `string`; `fail_reason?`: `string`; `timestamp2?`: `string`; `memo?`: `string`; `status?`: `string`; `chain`: `string`.

Field semantics: `status` — Transaction Status - BCODE: Deposit Code Operation - CANCEL: Cancelled - CANCELPEND: Withdrawal Cancellation Pending - DONE: Completed - EXTPEND: Sent and Waiting for Confirmation - FAIL: On-Chain Failure Pending Confirmation - FVERIFY: Facial Verification in Progress - LOCKED: Wallet-Side Order Locked - MANUAL: Pending Manual Review - REJECT: Rejected - REQUEST: Request in Progress - REVIEW: Under Review.

<a id="model-withdrawstatus"></a>
### WithdrawStatus

`currency?`: `string`; `name?`: `string`; `name_cn?`: `string`; `deposit?`: `string`; `withdraw_percent?`: `string`; `withdraw_fix?`: `string`; `withdraw_day_limit?`: `string`; `withdraw_amount_mini?`: `string`; `withdraw_day_limit_remain?`: `string`; `withdraw_eachtime_limit?`: `string`; `withdraw_fix_on_chains?`: `map[string]string`; `withdraw_percent_on_chains?`: `map[string]string`.
