# Proper MCP Data Usage Examples

## Problem Description

Older welfare templates only covered identity lookup and beginner-task listing. They also used outdated status mapping and omitted phase-2 newcomer actions such as task claim and reward claim.

This skill must now support:
- Identity lookup
- Beginner task list query
- Single task claim
- Newcomer reward claim
- Completion guidance for KYC / deposit / first trade flows

## Correct Implementation Method

### 1. Always gate welfare flows by identity

```javascript
const identity = await cex_welfare_get_user_identity();

if (identity.code !== 0) {
  // map 1001 / 1002 / 1003 / 1004 / 1005 / 1006 / 1008
  // and stop the newcomer flow
}
```

### 2. Query the real newcomer task list before any claim/completion decision

```javascript
const taskList = await cex_welfare_get_beginner_task_list();

if (taskList.code === 1007 || !taskList.data?.tasks?.length) {
  // no active newcomer tasks
}
```

### 3. Claim a single task only from real status=`0` task data

```javascript
const claimableTasks = taskList.data.tasks.filter((task) => task.status === 0);

if (claimableTasks.length === 1) {
  await cex_welfare_claim_task({
    welfare_task_id: claimableTasks[0].welfare_task_id,
  });
}
```

### 4. Claim rewards only from real status=`2` task data

```javascript
const rewardableTasks = taskList.data.tasks.filter((task) => task.status === 2);

for (const task of rewardableTasks) {
  const result = await cex_welfare_claim_reward({
    welfare_task_id: task.welfare_task_id,
  });

  if (result.data?.has_m_n_task) {
    // redirect user to Gate web/App rewards hub
    continue;
  }

  const rewardLabel =
    result.data?.coupon_full_name || `${task.reward_num} ${task.reward_unit}`;
}
```

## Real Data Fields

| Display Content | MCP Field | Notes |
|----------------|-----------|-------|
| Task title | `task_name` | Use real task name |
| Task description | `task_desc` | Remove HTML tags first |
| Reward amount | `reward_num` | Use real amount from task list |
| Reward unit | `reward_unit` | Use real unit from task list |
| Reward title after claim | `coupon_full_name` | Prefer this when reward claim returns it |
| Task status | `status` | Use the current phase-2 mapping |
| Task id for writes | `welfare_task_id` | Required by both write tools |

## Status Mapping

| Status | Meaning | Action |
|--------|---------|--------|
| `0` | Unclaimed | Can claim task |
| `1` | Claimed / in progress | Complete the task |
| `2` | Completed, reward claimable | Can claim reward |
| `3` | Reward distributing | Wait |
| `4` | Completed / settled | Done |
| `5` | Expired | Expired |

## Prohibited Wrong Practices

❌ Do not fabricate newcomer task names, reward numbers, coupon names, or thresholds.

❌ Do not claim a task without first confirming from the current task list that it is `status=0`.

❌ Do not claim a reward without first confirming from the current task list that it is `status=2`.

❌ Do not mark an M-select-N reward as claimed when `has_m_n_task=true`.

✅ Use the real MCP task list and real claim responses.

✅ Use response `code` as the source of truth, even when HTTP status is `200`.

## Summary

This update ensures the `gate-exchange-welfare` skill:
1. Uses the latest four-tool welfare MCP surface
2. Applies the current newcomer task status semantics
3. Supports task claim and reward claim safely
4. Still forbids fabricated reward information
