# Gate Exchange LaunchPool Skill

A comprehensive skill for browsing LaunchPool projects, staking tokens, redeeming staked assets, and querying participation and airdrop reward history on Gate.

## Overview

This skill provides users with complete access to Gate LaunchPool operations, including project discovery, token staking, early redemption, and historical record queries. It supports filtering projects by status, estimated APR, staking coin, and pool type, as well as managing staking positions with a secure confirmation flow.

### Core Capabilities

| Capability | Description | MCP Tools |
|------------|-------------|-----------|
| Browse LaunchPool projects | View projects, filter by status/APR/coin/pool type | `cex_launch_list_launch_pool_projects` |
| Stake tokens | Participate in LaunchPool by staking tokens | `cex_launch_create_launch_pool_order` |
| Redeem staked assets | Early withdraw staked tokens from a project | `cex_launch_redeem_launch_pool` |
| Query pledge records | View staking/redemption participation history | `cex_launch_list_launch_pool_pledge_records` |
| Query reward records | View airdrop reward distribution history | `cex_launch_list_launch_pool_reward_records` |

### 1. Browse LaunchPool Projects
- View all available LaunchPool projects
- Filter by status (ongoing, warming up, ended)
- Sort by estimated APR (highest/lowest)
- Filter by staking coin or pool type (newbie/normal)

### 2. Stake Tokens
- Stake tokens to a specific LaunchPool project
- Preview order before confirmation
- Secure confirmation flow required

### 3. Redeem Staked Assets
- Early redeem staked tokens from a project
- Preview redemption before confirmation
- Early redemption warning included

### 4. Query Pledge Records
- View staking and redemption history
- Filter by time range or coin
- Pagination support

### 5. Query Reward Records
- View airdrop reward distribution history
- Filter by time range or coin
- Track base and bonus airdrops

## Architecture

```
┌─────────────────────┐
│   User Request      │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Intent Detection   │
│  - Browse Projects  │
│  - Stake            │
│  - Redeem           │
│  - Pledge Records   │
│  - Reward Records   │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│   MCP Tool Call     │
│  - list_projects    │
│  - create_order     │
│  - redeem           │
│  - pledge_records   │
│  - reward_records   │
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

- `cex_launch_list_launch_pool_projects`: Browse available LaunchPool projects
- `cex_launch_create_launch_pool_order`: Create staking order
- `cex_launch_redeem_launch_pool`: Redeem staked assets
- `cex_launch_list_launch_pool_pledge_records`: Query pledge history
- `cex_launch_list_launch_pool_reward_records`: Query reward history

## Error Handling

The skill gracefully handles various error scenarios:
- Empty results: Suggests alternative queries or actions
- Compliance restrictions: Displays friendly regional restriction message
- Insufficient balance: Guides user to check balance or reduce amount
- API failures: Provides retry guidance
- Missing parameters: Asks clarifying questions

## Security Considerations

- **Confirmation required**: Stake and redeem operations require explicit user confirmation
- **Authentication required**: All operations except project browsing need user authentication
- **Compliance handling**: Regional restrictions are respected and communicated clearly
- **No fabrication**: Only displays data from actual API responses

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
