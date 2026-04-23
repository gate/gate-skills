# Gate Exchange CandyDrop Skill

A comprehensive skill for browsing CandyDrop activities, viewing activity rules, registering for activities, checking task progress, and querying participation and airdrop reward history on Gate.

## Overview

This skill provides users with complete access to Gate CandyDrop activity operations, including activity discovery, rules viewing, registration, task progress tracking, and historical record queries. It supports filtering activities by status, token, task type, and registration status, as well as managing activity participation with a secure confirmation flow.

### Core Capabilities

| Capability | Description | `gate-cli` commands |
|------------|-------------|-----------|
| Browse CandyDrop activities | View activities, filter by status/token/task type | `gate-cli cex launch candy-drop activities` |
| View activity rules | See prize pools, tasks, and reward details | `gate-cli cex launch candy-drop rules` |
| Register for activities | Join CandyDrop activities (with confirmation) | `gate-cli cex launch candy-drop register` |
| Check task progress | View task completion progress for enrolled activities | `gate-cli cex launch candy-drop progress` |
| Query participation records | View registration/participation history | `gate-cli cex launch candy-drop participations` |
| Query airdrop records | View airdrop reward distribution history | `gate-cli cex launch candy-drop airdrops` |

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
│   `gate-cli` command Call     │
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

## gate-cli command index Used

- `gate-cli cex launch candy-drop activities`: Browse available CandyDrop activities (public)
- `gate-cli cex launch candy-drop rules`: View activity rules and prize pools (public)
- `gate-cli cex launch candy-drop register`: Register for an activity (auth required)
- `gate-cli cex launch candy-drop progress`: Check task completion progress (auth required)
- `gate-cli cex launch candy-drop participations`: Query participation history (auth required)
- `gate-cli cex launch candy-drop airdrops`: Query airdrop reward history (auth required)

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
