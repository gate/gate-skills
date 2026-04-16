# Gate Exchange CandyDrop — Scenario Index

This document is a cross-reference index of all scenarios defined in the sub-module documents. Each sub-module owns its scenarios with full detail (Context, Prompt Examples, Expected Behavior, Response Template). Do **not** duplicate scenario content here.

## Scenario distribution

| Sub-module | Scenarios | Coverage |
|------------|-----------|----------|
| `activities.md` | 6 | Activities: by status, by token, by task type, by registration status, activity rules, empty list |
| `register.md` | 2 | Register: normal registration, missing parameters |
| `progress.md` | 2 | Task Progress: by token, by activity ID |
| `records.md` (Part 1) | 4 | Participation Records: by time, by token, by status, empty records |
| `records.md` (Part 2) | 3 | Airdrop Records: by time, by token, empty records |
| **Total** | **17** | |

## Quick lookup by user intent

### Activity List

| Scenario | Sub-module | ID |
|----------|------------|----|
| Query activities by status | activities.md | Scenario 1 |
| Query activities by token | activities.md | Scenario 2 |
| Query activities by task type | activities.md | Scenario 3 |
| Query activities by registration status | activities.md | Scenario 4 |
| Query activity rules | activities.md | Scenario 5 |
| Empty activity list | activities.md | Scenario 6 |

### Registration

| Scenario | Sub-module | ID |
|----------|------------|----|
| Normal registration with confirmation | register.md | Scenario 1 |
| Missing parameters | register.md | Scenario 2 |

### Task Progress

| Scenario | Sub-module | ID |
|----------|------------|----|
| Query by token | progress.md | Scenario 1 |
| Query by activity ID | progress.md | Scenario 2 |

### Participation Records

| Scenario | Sub-module | ID |
|----------|------------|----|
| Query by time range | records.md (Part 1) | Scenario 1 |
| Query by token | records.md (Part 1) | Scenario 2 |
| Query by status | records.md (Part 1) | Scenario 3 |
| Empty participation records | records.md (Part 1) | Scenario 4 |

### Airdrop Records

| Scenario | Sub-module | ID |
|----------|------------|----|
| Query by time range | records.md (Part 2) | Scenario 5 |
| Query by token | records.md (Part 2) | Scenario 6 |
| Empty airdrop records | records.md (Part 2) | Scenario 7 |

## Error scenarios (summary)

Error handling is embedded within the sub-module scenarios listed above. Key error paths:

| Error condition | Handled in |
|-----------------|------------|
| No activities found | activities.md Scenario 6 |
| No participation records | records.md (Part 1) Scenario 4 |
| No airdrop records | records.md (Part 2) Scenario 7 |
| Missing currency for registration | register.md Scenario 2 |
| Activity not found | SKILL.md Error Handling → API error labels |
| API error / 401 | SKILL.md Safety rules → Errors table |
| Compliance restriction | SKILL.md Safety rules → Compliance |
