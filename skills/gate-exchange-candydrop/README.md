# Gate Exchange CandyDrop Skill

A comprehensive skill for browsing CandyDrop activities, viewing activity rules, registering for activities, checking task progress, and querying participation and airdrop reward history on Gate.

## Overview

This skill provides users with complete access to Gate CandyDrop activity operations, including activity discovery, rules viewing, registration, task progress tracking, and historical record queries. It supports filtering activities by status, token, task type, and registration status, as well as managing activity participation with a secure confirmation flow.

### Core Capabilities

| Capability | Description | MCP Tools |
|------------|-------------|-----------|
| Browse CandyDrop activities | View activities, filter by status/token/task type | `cex_launch_get_candy_drop_activity_list_v4` |
| View activity rules | See prize pools, tasks, and reward details | `cex_launch_get_candy_drop_activity_rules_v4` |
| Register for activities | Join CandyDrop activities (with confirmation) | `cex_launch_register_candy_drop_v4` |
| Check task progress | View task completion progress for enrolled activities | `cex_launch_get_candy_drop_task_progress_v4` |
| Query participation records | View registration/participation history | `cex_launch_get_candy_drop_participation_records_v4` |
| Query airdrop records | View airdrop reward distribution history | `cex_launch_get_candy_drop_airdrop_records_v4` |

### 1. Browse CandyDrop Activities
- View all available CandyDrop activities
- Filter by status (ongoing, upcoming, ended)
- Filter by token (USDT, BTC, etc.)
- Filter by task type (spot, futures, deposit, invite, etc.)
- Filter by registration status (registered/unregistered)

### 2. View Activity Rules
- See prize pool details (total prize, per-user cap)
- View task list with descriptions and exclusive labels
- Check activity period and total rewards

### 3. Register for Activities
- Register for a specific CandyDrop activity
- Preview registration before confirmation
- Secure confirmation flow required

### 4. Check Task Progress
- View completion progress for registered tasks
- Track trading volume, deposit amounts, etc.
- See current progress values

### 5. Query Participation Records
- View registration and participation history
- Filter by time range, token, or status
- Pagination support

### 6. Query Airdrop Records
- View airdrop reward distribution history
- Filter by time range or token
- Show reward amounts with token units (no flash-convert USDT column)

## Architecture

```
┌─────────────────────┐
│   User Request      │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Intent Detection   │
│  - Browse Activities│
│  - Activity Rules   │
│  - Register         │
│  - Task Progress    │
│  - Participation Rec│
│  - Airdrop Records  │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│   MCP Tool Call     │
│  - activity_list    │
│  - activity_rules   │
│  - register         │
│  - task_progress    │
│  - participation_rec│
│  - airdrop_records  │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Response Format    │
│  - Tables           │
│  - Previews         │
│  - Confirmations    │
└─────────────────────┘
```

## MCP Tools Used

- `cex_launch_get_candy_drop_activity_list_v4`: Browse available CandyDrop activities (public)
- `cex_launch_get_candy_drop_activity_rules_v4`: View activity rules and prize pools (public)
- `cex_launch_register_candy_drop_v4`: Register for an activity (auth required)
- `cex_launch_get_candy_drop_task_progress_v4`: Check task completion progress (auth required)
- `cex_launch_get_candy_drop_participation_records_v4`: Query participation history (auth required)
- `cex_launch_get_candy_drop_airdrop_records_v4`: Query airdrop reward history (auth required)

## Error Handling

The skill gracefully handles various error scenarios:
- Empty results: Suggests alternative queries or actions
- Compliance restrictions: Displays friendly regional restriction message
- API failures: Provides retry guidance
- Missing parameters: Asks clarifying questions (e.g. missing currency for registration)
- Activity not found: Guides user to check token name or activity ID

## Security Considerations

- **Confirmation required**: Registration requires explicit user confirmation
- **Authentication required**: Registration, task progress, and records queries need user authentication
- **Public access**: Activity list and rules are publicly accessible
- **Compliance handling**: Regional restrictions are respected and communicated clearly
- **No fabrication**: Only displays data from actual API responses

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
