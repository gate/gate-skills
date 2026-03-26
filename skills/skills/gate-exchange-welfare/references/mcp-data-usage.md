# Proper MCP Data Usage Examples

## Problem Description

Previous skill templates contained hardcoded fake reward information, such as:
- "10 points" 
- "5 USDT trial voucher"
- "20 USDT bonus"

These are all fabricated data and should not appear in skill responses.

## Correct Implementation Method

### 1. Must Call Real MCP Interface

```javascript
// Step 1: Determine user identity
const userIdentity = await cex_welfare_get_user_identity();

// Step 2: If new user (code=0), get real task list
if (userIdentity.code === 0) {
    const taskList = await cex_welfare_get_beginner_task_list();
    // Use real returned task data
}
```

### 2. Use Real MCP Data Fields

Real data structure returned from MCP interface:
```json
{
    "message": "success",
    "data": {
        "tasks": [
            {
                "welfare_task_id": 128,
                "task_type": 26,
                "task_name": "Sign Up",
                "task_desc": "Sign up and log in to receive 10 USDT", 
                "reward_num": "10",
                "reward_unit": "USDT",
                "prize_type": 2,
                "status": 2
            },
            {
                "welfare_task_id": 133,
                "task_center_id": 1590,
                "task_type": 1,
                "task_name": "Identity Verification",
                "task_desc": "Complete identity verification",
                "reward_num": "1", 
                "reward_unit": "USDT",
                "prize_type": 2,
                "status": 1
            }
        ]
    }
}
```

### 3. Correct Response Format

```
🎁 Your exclusive new user tasks are as follows. Complete tasks to claim corresponding rewards:

📌 Sign Up
   Sign up and log in to receive 10 USDT
   💰 Reward: 10 USDT
   Status: Completed

📌 Identity Verification  
   Complete identity verification
   💰 Reward: 1 USDT
   Status: Pending

---

⚠️ Non-agent, non-institutional users and users with normal account status can complete tasks and claim rewards. Specific tasks and rewards are subject to final display on Gate official website/App.
```

## Prohibited Wrong Practices

❌ **Absolutely cannot use template example data**:
- "Complete Identity Verification / KYC" + "10 points"
- "Download Gate App" + "5 USDT trial voucher"  
- "First Deposit" + "20 USDT bonus"

❌ **Cannot fabricate any reward information**

✅ **Must use real return data from MCP interface**

## Data Mapping Relationships

| Display Content | MCP Field | Description |
|----------------|-----------|-------------|
| Task Title | `task_name` | Real task name from interface |
| Task Description | `task_desc` | Real task description from interface |
| Reward Amount | `reward_num` | Real reward amount from interface |
| Reward Unit | `reward_unit` | Real reward unit from interface |
| Completion Status | `status` | 1=Pending, 2=Completed |

## Summary

This fix ensures the `gate-exchange-welfare` skill:
1. Must call real MCP interface to get data
2. Cannot use any fabricated reward information
3. Strictly format responses according to real data
4. Provide accurate user task status information