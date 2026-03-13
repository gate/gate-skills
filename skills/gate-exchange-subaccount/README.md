# Gate Exchange Sub-Account

## Overview

An AI Agent skill that enables sub-account management on Gate, including querying sub-account status, listing all sub-accounts, creating new sub-accounts, and locking/unlocking sub-accounts.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Query Status** | Check the current status and details of a specific sub-account by UID | "What is the status of sub-account UID 123456?" |
| **List Sub-Accounts** | View all sub-accounts under the main account with their status | "Show me all my sub-accounts" |
| **Create Sub-Account** | Create a new normal sub-account with a login name | "Create a new sub-account" |
| **Lock Sub-Account** | Lock a sub-account to disable login and trading | "Lock sub-account UID 123456" |
| **Unlock Sub-Account** | Unlock a previously locked sub-account to restore access | "Unlock sub-account UID 123456" |

## Architecture

```
User Query
    │
    ▼
┌─────────────────────┐
│  gate-exchange-      │
│  subaccount Skill    │
│  (Intent Detection   │
│   + Workflow)        │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Gate MCP Tools      │
│  (API v4 Endpoints)  │
│                      │
│  • cex_sa_get_sa     │
│  • cex_sa_list_sas   │
│  • cex_sa_create_sa  │
│  • cex_sa_lock_sa    │
│  • cex_sa_unlock_sa  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Gate Platform       │
│  (Sub-Account Mgmt)  │
└─────────────────────┘
```

## MCP Tools

| Tool | Method | Endpoint | Auth | Description |
|------|--------|----------|------|-------------|
| `cex_sa_get_sa` | GET | `/api/v4/sub_accounts/{user_id}` | Yes | Get sub-account details |
| `cex_sa_list_sas` | GET | `/api/v4/sub_accounts` | Yes | List all sub-accounts |
| `cex_sa_create_sa` | POST | `/api/v4/sub_accounts` | Yes | Create a new sub-account |
| `cex_sa_lock_sa` | POST | `/api/v4/sub_accounts/{user_id}/lock` | Yes | Lock a sub-account |
| `cex_sa_unlock_sa` | POST | `/api/v4/sub_accounts/{user_id}/unlock` | Yes | Unlock a sub-account |

## Quick Start

1. Install the [Gate MCP server](https://github.com/gate/gate-mcp)
2. Load this skill into your AI Agent (Claude, ChatGPT, etc.)
3. Try: _"Show me all my sub-accounts"_

## Safety & Compliance

- All write operations (create/lock/unlock) require explicit user confirmation before execution
- Sub-account UID is validated before lock/unlock operations
- Current state is checked to avoid redundant operations
- Only normal sub-accounts can be created through this skill
- Sensitive user data (API keys, balances) is never logged or exposed in responses
