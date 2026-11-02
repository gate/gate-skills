# Affiliate statistics and transactions Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-agencytransaction"></a>
### AgencyTransaction

`transaction_time?`: `int64`; `user_id?`: `int64`; `group_name?`: `string`; `fee?`: `string`; `fee_asset?`: `string`; `currency_pair?`: `string`; `amount?`: `string`; `amount_asset?`: `string`; `source?`: `string`.

<a id="model-agencytransactionhistory"></a>
### AgencyTransactionHistory

`currency_pair?`: `string`; `total?`: `int64`; `list?`: [][AgencyTransaction](#model-agencytransaction).

<a id="model-brokercommissionsubbrokerinfo"></a>
### BrokerCommissionSubBrokerInfo

`user_id?`: `int64`; `original_commission_rate?`: `string`; `relative_commission_rate?`: `string`; `commission_rate?`: `string`.

<a id="model-brokertransaction"></a>
### BrokerTransaction

`transaction_time?`: `int64`; `user_id?`: `int64`; `group_name?`: `string`; `fee?`: `string`; `currency_pair?`: `string`; `amount?`: `string`; `fee_asset?`: `string`; `source?`: `string`; `sub_broker_info?`: [BrokerCommissionSubBrokerInfo](#model-brokercommissionsubbrokerinfo); `alpha_contract_addr?`: `string`.

<a id="model-brokertransactionhistory"></a>
### BrokerTransactionHistory

`total?`: `int64`; `list?`: [][BrokerTransaction](#model-brokertransaction).

<a id="model-partnerdataaggregated"></a>
### PartnerDataAggregated

`rebate_amount`: `string`; `trade_volume`: `string`; `net_fee`: `string`; `customer_count`: `int32`; `trading_user_count`: `*string`; `time_range_desc`: `string`; `business_type`: `int32`; `business_type_desc`: `string`.

<a id="model-partnerdataaggregatedresponse"></a>
### PartnerDataAggregatedResponse

`code`: `int32`; `message`: `string`; `data`: [PartnerDataAggregated](#model-partnerdataaggregated); `timestamp`: `int64`.

<a id="model-partnertransactionhistory"></a>
### PartnerTransactionHistory

`total?`: `int64`; `list?`: [][AgencyTransaction](#model-agencytransaction).
