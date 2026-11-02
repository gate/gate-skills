# Affiliate relationships Models

Read only models linked by the selected action. These are CLI/SDK field contracts, not display templates. `?` means Go JSON omission (`omitempty`); it does not waive required API fields. String amounts preserve decimal precision. Response-only fields must not be copied into requests.

<a id="model-eligibility"></a>
### Eligibility

`eligible`: `bool`; `block_reasons`: `[]string`; `block_reason_codes`: `[]string`.

<a id="model-eligibilityresponse"></a>
### EligibilityResponse

`code`: `int32`; `message`: `string`; `data`: [Eligibility](#model-eligibility); `timestamp`: `int64`.

<a id="model-othercontact"></a>
### OtherContact

`type?`: `int32`; `value?`: `string`.

<a id="model-partnerapplication"></a>
### PartnerApplication

`id?`: `int32`; `uid?`: `int32`; `language?`: `string`; `country_id?`: `int32`; `firstname?`: `string`; `lastname?`: `string`; `email?`: `string`; `join_uid?`: `int32`; `join_country_id?`: `int32`; `identity_comment?`: `string`; `promotion_channels?`: `string`; `contact_details?`: `string`; `know_details?`: `string`; `question_lang?`: `string`; `create_timest?`: `time.Time`; `update_timest?`: `time.Time`; `apply_type?`: `int32`; `audit_status?`: `int32`; `edit_counts?`: `int32`; `proof_images?`: `string`; `proof_videos?`: `string`; `proof_url?`: `string`; `audit_reason?`: `int32`; `channel_type?`: `int32`; `region?`: `string`; `phone?`: `string`; `telegram?`: `string`; `other_contact?`: [OtherContact](#model-othercontact); `proof_images_url_list?`: `[]string`; `proof_videos_url_list?`: `[]string`; `apply_msg?`: `string`; `jump_url?`: `string`.

<a id="model-partnerapplicationresponse"></a>
### PartnerApplicationResponse

`code`: `int32`; `message`: `string`; `data`: [PartnerApplication](#model-partnerapplication); `timestamp`: `int64`.

<a id="model-partnersub"></a>
### PartnerSub

`user_id?`: `int64`; `user_join_time?`: `int64`; `type?`: `int64`.

Field semantics: `user_join_time` — Time when user joined the system, Unix timestamp in seconds.

<a id="model-partnersublist"></a>
### PartnerSubList

`total?`: `int64`; `list?`: [][PartnerSub](#model-partnersub).

<a id="model-rebateuserinfo"></a>
### RebateUserInfo

`invite_uid?`: `int64`.

<a id="model-usersub"></a>
### UserSub

`uid?`: `int64`; `belong?`: `string`; `type?`: `int64`; `ref_uid?`: `int64`.

<a id="model-usersubrelation"></a>
### UserSubRelation

`list?`: [][UserSub](#model-usersub).
