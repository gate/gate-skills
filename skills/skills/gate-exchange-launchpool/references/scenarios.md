# Gate Exchange LaunchPool — Scenario Index

This document is a cross-reference index of all scenarios defined in the sub-module documents. Each sub-module owns its scenarios with full detail (Context, Prompt Examples, Expected Behavior, Response Template). Do **not** duplicate scenario content here.

## Scenario distribution

| Sub-module | Scenarios | Coverage |
|------------|-----------|----------|
| `launch-projects.md` | 5 | Projects: by status, by estimated APR, by staking coin, by pool type, empty list |
| `stake-redeem.md` | 5 | Stake: normal stake, normal redeem, missing params, compliance error, insufficient balance |
| `records.md` (Part 1) | 3 | Pledge Records: by time, by coin, empty records |
| `records.md` (Part 2) | 3 | Reward Records: by time, by coin, empty records |
| **Total** | **16** | |

## Quick lookup by user intent

### Projects

| Scenario | Sub-module | ID |
|----------|------------|----|
| Query projects by status | launch-projects.md | Scenario 1 |
| Query projects sorted by estimated APR | launch-projects.md | Scenario 2 |
| Query projects by staking coin | launch-projects.md | Scenario 3 |
| Query projects by pool type | launch-projects.md | Scenario 4 |
| Empty project list | launch-projects.md | Scenario 5 |

### Stake & Redeem

| Scenario | Sub-module | ID |
|----------|------------|----|
| Normal stake with confirmation | stake-redeem.md | Scenario 1 |
| Normal redeem with confirmation | stake-redeem.md | Scenario 2 |
| Missing parameters | stake-redeem.md | Scenario 3 |
| Compliance error | stake-redeem.md | Scenario 4 |
| Insufficient balance or limit exceeded | stake-redeem.md | Scenario 5 |

### Pledge Records

| Scenario | Sub-module | ID |
|----------|------------|----|
| Query by time range | records.md (Part 1) | Scenario 1 |
| Query by project or coin | records.md (Part 1) | Scenario 2 |
| Empty pledge records | records.md (Part 1) | Scenario 3 |

### Reward Records

| Scenario | Sub-module | ID |
|----------|------------|----|
| Query by time range | records.md (Part 2) | Scenario 4 |
| Query by project or coin | records.md (Part 2) | Scenario 5 |
| Empty reward records | records.md (Part 2) | Scenario 6 |

## Error scenarios (summary)

Error handling is embedded within the sub-module scenarios listed above. Key error paths:

| Error condition | Handled in |
|-----------------|------------|
| No projects found | launch-projects.md Scenario 5 |
| No pledge records | records.md Scenario 3 |
| No reward records | records.md Scenario 6 |
| Compliance restriction | stake-redeem.md Scenario 4 |
| Insufficient balance / limit exceeded | stake-redeem.md Scenario 5 |
| API error / 401 | SKILL.md Safety rules → Errors table |
