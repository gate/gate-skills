---
name: gate-exchange-subaccount
description: "Gate Exchange sub-account management skill. Use when the user asks to manage, create, lock, unlock, or list their sub-accounts. Triggers on 'sub-account status', 'create sub-account', 'lock sub-account', 'my sub-accounts'."
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "💱"
    os:
      - darwin
      - linux
    primaryEnv: GATE_API_KEY
    requires:
      bins:
        - gate-cli
      env:
        - GATE_API_KEY
        - GATE_API_SECRET

    install:
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux x64)"
      - kind: download
        os:
          - linux
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_linux_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (Linux arm64)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_amd64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Intel)"
      - kind: download
        os:
          - darwin
        url: "https://github.com/gate/gate-cli/releases/download/v0.6.2/gate-cli_0.6.2_darwin_arm64.tar.gz"
        bins:
          - gate-cli
        targetDir: "bin"
        label: "Download gate-cli (macOS Apple Silicon)"
---

### Resolving `gate-cli` (binary path)

Resolve **`gate-cli`** in order: **(1)** **`command -v gate-cli`** and **`gate-cli --version`** succeeds; **(2)** **`${HOME}/.local/bin/gate-cli`** if executable; **(3)** **`${HOME}/.openclaw/skills/bin/gate-cli`** if executable. Canonical rules: [`exchange-runtime-rules.md`](../exchange-runtime-rules.md) §4 (or [`gate-runtime-rules.md`](../gate-runtime-rules.md) §4).


# Gate Exchange Sub-Account Skill

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only use the `gate-cli` commands explicitly listed in this skill.** Commands not documented here must NOT be run for these workflows, even if other interfaces expose them.

## Skill Dependencies


### gate-cli commands used

**Query Operations (Read-only)**

- `gate-cli cex sub-account get`
- `gate-cli cex sub-account list`
- `gate-cli cex sub-account lock`
- `gate-cli cex sub-account unlock`

**Execution Operations (Write)**

- `gate-cli cex sub-account create`

### Authentication
- **Interactive file setup:** when **`GATE_API_KEY`** and **`GATE_API_SECRET`** are **not** both set on the host, run **`gate-cli config init`** to complete the wizard for API key, secret, profiles, and defaults (see [gate-cli](https://github.com/gate/gate-cli)).
- **Env / flags:** **`gate-cli config init`** is **not** required when credentials are already supplied — e.g. **both** **`GATE_API_KEY`** and **`GATE_API_SECRET`** set on the host, or **`--api-key`** / **`--api-secret`** where supported — never ask the user to paste secrets into chat.
- **Permissions:** Sa:Write
- **Portal:** create or rotate keys outside the chat: https://www.gate.com/myaccount/profile/api-key/manage

### Installation Check
- **Required:** `gate-cli` (run `sh ./setup.sh` from this skill directory if missing; optional `GATE_CLI_SETUP_MODE=release`).
- Add `$HOME/.openclaw/skills/bin` to **`PATH`** if you invoke `gate-cli` by name (or the directory where [`setup.sh`](./setup.sh) installs it).
- **Credentials:** When **`GATE_API_KEY`** and **`GATE_API_SECRET`** are both set (non-empty) for the host, **do not** require **`gate-cli config init`** — that is equivalent valid config for `gate-cli`. When **both** are unset or empty, **remind** the operator to run **`gate-cli config init`** **or** to configure **`GATE_API_KEY`** / **`GATE_API_SECRET`** in the **matching skill** from the skill library (never ask the user to paste secrets into chat).
- **Sanity check:** Do not proceed with authenticated calls until the CLI behaves as expected (e.g. **`gate-cli --version`** or a read-only **`gate-cli cex ...`** command from this skill); confirm credentials resolve before mutating operations.

## Execution mode

**Read and strictly follow** [`references/gate-cli.md`](./references/gate-cli.md), then execute this skill's sub-account workflow.

- `SKILL.md` keeps intent routing and permission boundaries.
- `references/gate-cli.md` is the authoritative `gate-cli` execution contract for create/lock/unlock confirmation gates and status verification.

## Prerequisites

- **MCP Dependency**: Requires [gate-mcp](https://github.com/gate/gate-mcp) to be installed.
- **Authentication**: All sub-account operations require API key authentication with main-account privileges.
- **Permission**: The current user must be a main account holder to manage sub-accounts.

## Available MCP Tools

| Tool | Auth | Description |
|------|------|-------------|
| `gate-cli cex sub-account get` | Yes | Get details of a specific sub-account by user ID |
| `gate-cli cex sub-account list` | Yes | List all sub-accounts under the main account |
| `gate-cli cex sub-account create` | Yes | Create a new normal sub-account |
| `gate-cli cex sub-account lock` | Yes | Lock a sub-account to disable login and trading |
| `gate-cli cex sub-account unlock` | Yes | Unlock a previously locked sub-account |

## Workflow

### Step 1: Identify User Intent

Parse the user's message to determine which sub-account operation they need.

Key data to extract:
- `intent`: One of `query_status`, `list_all`, `create`, `lock`, `unlock`
- `user_id`: Sub-account UID (required for `query_status`, `lock`, `unlock`)
- `login_name`: Desired username (for `create`, may need to ask user)

Intent detection rules:

| Signal Keywords | Intent |
|----------------|--------|
| "status of sub-account", "sub-account UID {id}", "check sub-account" | `query_status` |
| "all sub-accounts", "list sub-accounts", "my sub-accounts", "which sub-accounts" | `list_all` |
| "create sub-account", "new sub-account", "add sub-account" | `create` |
| "lock sub-account", "disable sub-account", "freeze sub-account" | `lock` |
| "unlock sub-account", "enable sub-account", "unfreeze sub-account" | `unlock` |

### Step 2: Execute by Intent

#### Case A: Query Sub-Account Status (`query_status`)

Call `gate-cli cex sub-account get` with:
- `user_id`: The sub-account UID provided by the user

Key data to extract:
- `login_name`: Sub-account username
- `remark`: Sub-account remark/note
- `state`: Account state (normal / locked)
- `type`: Account type (normal / pool)
- `create_time`: Account creation timestamp

Present the sub-account details in a structured format.

#### Case B: List All Sub-Accounts (`list_all`)

Call `gate-cli cex sub-account list` with:
- `type`: "0" (normal sub-accounts only)

Key data to extract:
- For each sub-account: `user_id`, `login_name`, `remark`, `state`, `create_time`

Present results as a table with username, UID, remark (if any), and current status.

#### Case C: Create Sub-Account (`create`)

**Pre-check**: Call `gate-cli cex sub-account list` with `type`: "0" to get the current list of normal sub-accounts. Check if the user can still create more sub-accounts based on the returned count.

If creation is available:
1. Ask the user to provide a login name for the new sub-account
2. Optionally collect: email, remark
3. Confirm all details with the user before proceeding
4. Call `gate-cli cex sub-account create` with:
 - `login_name`: User-provided login name (required)
 - `email`: User-provided email (optional)
 - `remark`: User-provided remark (optional)
5. Present the newly created sub-account details

Key data to extract:
- `user_id`: Newly created sub-account UID
- `login_name`: Confirmed username
- `state`: Should be "normal"

**Important**: Only normal sub-accounts can be created through this skill.

#### Case D: Lock Sub-Account (`lock`)

1. Validate that `user_id` is provided; if not, ask the user
2. Call `gate-cli cex sub-account get` with `user_id` to verify the sub-account exists and belongs to the main account
3. If the sub-account is already locked, inform the user and stop
4. Confirm with the user: "Are you sure you want to lock sub-account {user_id} ({login_name})? This will disable login and trading for this sub-account."
5. On confirmation, call `gate-cli cex sub-account lock` with:
 - `user_id`: The sub-account UID
6. Report the result

Key data to extract:
- Lock operation success/failure status

#### Case E: Unlock Sub-Account (`unlock`)

1. Validate that `user_id` is provided; if not, ask the user
2. Call `gate-cli cex sub-account get` with `user_id` to verify the sub-account exists and is currently locked
3. If the sub-account is already unlocked/normal, inform the user and stop
4. Confirm with the user: "Are you sure you want to unlock sub-account {user_id} ({login_name})?"
5. On confirmation, call `gate-cli cex sub-account unlock` with:
 - `user_id`: The sub-account UID
6. Report the result

Key data to extract:
- Unlock operation success/failure status

### Step 3: Format and Respond

Present results using the Report Template below. Always include relevant context and next-step suggestions.

## Judgment Logic Summary

| Condition | Action |
|-----------|--------|
| User asks for a specific sub-account status with UID | Route to Case A: `query_status` |
| User asks to see all sub-accounts | Route to Case B: `list_all` |
| User wants to create a new sub-account | Route to Case C: `create` |
| User wants to lock a sub-account with UID | Route to Case D: `lock` |
| User wants to unlock a sub-account with UID | Route to Case E: `unlock` |
| UID not provided for operations requiring it | Ask user for the sub-account UID |
| Login name not provided for creation | Ask user for a login name |
| Sub-account already in target state (lock/unlock) | Inform user, no action needed |
| API returns authentication error | Prompt user to log in |
| API returns permission error | Inform user that main account privileges are required |
| Sub-account does not exist or does not belong to user | Inform user the UID is invalid |

## Report Template

### Query Status Response

```
Sub-Account Details
---
Username: {login_name}
UID: {user_id}
Status: {state}
Type: {type}
Remark: {remark or "N/A"}
Created: {create_time}
```

### List All Sub-Accounts Response

```
Your Sub-Accounts
---
| # | Username | UID | Status | Remark |
|---|----------|-----|--------|--------|
| 1 | {login_name} | {user_id} | {state} | {remark or "-"} |
| 2 |... |... |... |... |

Total: {count} sub-account(s)
```

### Create Sub-Account Response

```
Sub-Account Created Successfully
---
Username: {login_name}
UID: {user_id}
Status: Normal
Remark: {remark or "N/A"}

Note: Only normal sub-accounts can be created through this interface.
```

### Lock/Unlock Response

```
Sub-Account {Action} Successfully
---
Username: {login_name}
UID: {user_id}
Previous Status: {previous_state}
Current Status: {new_state}
```

## Domain Knowledge

- A main account on Gate can create multiple sub-accounts for asset isolation, strategy separation, or team management.
- Sub-accounts share the main account's KYC verification but have independent trading and wallet capabilities.
- Locking a sub-account disables both login and trading; the assets remain safe but inaccessible until unlocked.
- There are two types of sub-accounts: normal (type=0) and pool (type=1). This skill only supports creating normal sub-accounts.
- Sub-account creation requires a unique login name. Email and remark are optional.

## Safety Rules

- **Write operations** (`gate-cli cex sub-account create`, `gate-cli cex sub-account lock`, `gate-cli cex sub-account unlock`): Always require explicit user confirmation before execution. Never auto-execute.
- **UID validation**: Before lock/unlock, always verify the sub-account exists and belongs to the current main account.
- **State check**: Before lock/unlock, check current state to avoid redundant operations.
- **No sensitive data exposure**: Never expose API keys, internal endpoint URLs, or raw error traces.
- **Normal sub-accounts only**: Creation is restricted to normal sub-accounts (type=0). Do not attempt to create pool sub-accounts.

## Error Handling

| Condition | Response |
|-----------|----------|
| Auth endpoint returns "not login" | "Please log in to your Gate account first." |
| User is not a main account | "Sub-account management requires main account privileges. Please switch to your main account." |
| Sub-account UID not found | "Sub-account with UID {user_id} was not found. Please verify the UID and try again." |
| Sub-account does not belong to user | "This sub-account does not belong to your main account." |
| Sub-account already locked | "Sub-account {user_id} is already locked. No action needed." |
| Sub-account already unlocked | "Sub-account {user_id} is already in normal (unlocked) state. No action needed." |
| Create sub-account fails (limit reached) | "You have reached the maximum number of sub-accounts. Please contact support if you need more." |
| Create sub-account fails (duplicate name) | "The login name '{login_name}' is already taken. Please choose a different name." |
| Unknown error | "An error occurred while processing your request. Please try again later." |

## Prompt Examples & Scenarios

See [scenarios.md](references/scenarios.md) for full prompt examples and expected behaviors.
