# Acceptance scenarios

Static package checks establish local links, dependency hashes and command spelling. They do not establish API deployment or trading success.

| Scenario | Required observation |
|---|---|
| Eight manual product drafts | Complete parameters still produce a draft and zero first-turn writes; the immediately following approval permits one create, subject to verified authority |
| Account-detail unavailable | No separate account-detail or UID lookup is required; preserve the selected account context and check the requested operation's authentication, permission and user authority |
| Existing complete authorization | Reuse verified scope checks, but still show and obtain next-turn approval of each Bot draft; an already approved unexecuted draft needs no third confirmation turn |
| Changed or interrupted draft | Parameter changes or an intervening request produce a current draft and zero writes; a later bare approval does not execute the older draft |
| Consumed approval | Repeating approval after the create/stop has executed produces no second write; unknown results enter reconciliation, not replay |
| Four reported complete first requests | Independently test futures grid, contract martingale, smart-position and futures-combo: turn 1 zero writes, turn 2 approval exactly one intended write |
| Stop with an existing grant | Present one exact instance and its exit effects in turn 1; no stop before next-turn approval |
| Running-list answer | Unfiltered first query and filtered query both display applied filters plus response page/page_size/total, alongside actual instances; next-page requests preserve filters and page size |
| Empty or adjusted running page | Empty page retains response total and pagination; adjusted page size uses the response value; absent pagination is explicitly unavailable, never inferred from request flags or item count |
| Detail stop capability | Complete and partial detail answers explicitly show support for true, no support for false, and unverified for missing/null/invalid stop_supported; ended/unsettled commentary does not substitute for this statement; no stop is executed by a detail query |
| Six official source types | Real source identity; requested exact rebalance asset before ranking; no fake candidate when absent |
| Another candidate | Previous logical candidate excluded; same metrics refresh not counted; no alternatives retains constraints |
| Contract fixed stop | Missing basis rejects before effects; last/index/mark and buy/sell survive to persisted rule |
| Spot fixed stop | Explain unsupported fixed-price intent; no silent ratio conversion or disabled-value protection |
| Contract budget | Full ladder, fee, direction, adds, step and minimum checked by business formula; no budget edits |
| Rebalance exit | Explicit three-mode choice; atomic options/signal; repeat cannot reset expiration; old-writer contention/cancel tested |
| Combo lifecycle | Dedicated allocation and stop path; unknown transfer retains ID; no duplicate transfer; final refund verified separately |
| HTTP200 business failure | Nonzero CLI exit, original label/trace/ID retained |
| HTML404/truncated/unknown enum | Unverified result, no fabricated empty/zero or production fallback |
| Null collection compatibility | Exit0 may be tolerated; retain the actual result and invent no items |
| Code200 pending write | Preserve ID/unknown/pending/recovery flags; query original ID; one write, no false running/settled claim |
| Single installed package | Works with local six-file rules and no sibling business Skill or remote rules download |
| Rollback/migration | Package changes preserve existing instances; old name only guides migration after new package passes release gates |

Record static, synthetic command traces, local isolated database writes, real authenticated reads and real isolated-funds integration separately. Required unexecuted checks stay NOT_EVALUATED or BLOCKED. Eight-type integration and SDK/gateway compatibility must pass before release.
