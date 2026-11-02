# Affiliate commissions Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-agencycommission"></a>
### AgencyCommission

`commission_time?`: `int64`; `user_id?`: `int64`; `group_name?`: `string`; `commission_amount?`: `string`; `commission_asset?`: `string`; `source?`: `string`.

Field semantics: `commission_time` — Commission time (Unix timestamp in seconds).

<a id="model-agencycommissionhistory"></a>
### AgencyCommissionHistory

`currency_pair?`: `string`; `total?`: `int64`; `list?`: [][AgencyCommission](#model-agencycommission).

<a id="model-brokercommission"></a>
### BrokerCommission

`total?`: `int64`; `list?`: [][BrokerCommissionItem](#model-brokercommissionitem).

<a id="model-brokercommissionitem"></a>
### BrokerCommissionItem

`commission_time?`: `int64`; `user_id?`: `int64`; `group_name?`: `string`; `amount?`: `string`; `fee?`: `string`; `fee_asset?`: `string`; `rebate_fee?`: `string`; `source?`: `string`; `currency_pair?`: `string`; `sub_broker_info?`: [BrokerCommissionSubBrokerInfo](#model-brokercommissionsubbrokerinfo); `alpha_contract_addr?`: `string`.

Field semantics: `commission_time` — Commission time (Unix timestamp in seconds).

<a id="model-brokercommissionsubbrokerinfo"></a>
### BrokerCommissionSubBrokerInfo

`user_id?`: `int64`; `original_commission_rate?`: `string`; `relative_commission_rate?`: `string`; `commission_rate?`: `string`.

<a id="model-partnercommissionhistory"></a>
### PartnerCommissionHistory

`total?`: `int64`; `list?`: [][AgencyCommission](#model-agencycommission).
