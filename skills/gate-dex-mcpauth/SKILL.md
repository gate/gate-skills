---
name: gate-dex-mcpauth
version: "2026.3.5-1"
updated: "2026-03-05"
description: "Gate Wallet authentication. Use when the user needs to log in, log out, refresh session, or when other Skills detect unauthenticated state (no mcp_token). Supports Google OAuth login. First use will verify that the MCP Server connection is configured."
---

# Gate Wallet Auth Skill

> Auth domain — Manage Google OAuth login, Token refresh, and logout. 5 MCP tools.

**Trigger scenarios**: User mentions "login", "logout", "authentication", "sign in", or when other Skills detect no `mcp_token`.

## Step 0: MCP Server Connection Check (Mandatory)

**Before executing any operation, you must first confirm that the Gate Wallet MCP Server is available. This step cannot be skipped.**

Probe call:

```
CallMcpTool(server="gate-wallet", toolName="chain.config", arguments={chain: "eth"})
```

| Result | Action |
|--------|--------|
| Success | MCP Server available, proceed to next steps |
| `server not found` / `unknown server` | Cursor not configured → Show configuration guide (see below) |
| `connection refused` / `timeout` | Remote unreachable → Prompt to check URL and network |
| `401` / `unauthorized` | API Key auth failed → Prompt to check auth configuration |

### When Cursor is Not Configured

```
❌ Gate Wallet MCP Server Not Configured

The MCP Server named "gate-wallet" was not found in Cursor. Please configure it as follows:

Option 1: Configure via Cursor Settings (Recommended)
  1. Open Cursor → Settings → MCP
  2. Click "Add new MCP server"
  3. Fill in:
     - Name: gate-wallet
     - Type: HTTP
     - URL: https://your-mcp-server-domain/mcp
  4. Save and retry

Option 2: Edit config file manually
  Edit ~/.cursor/mcp.json and add:
  {
    "mcpServers": {
      "gate-wallet": {
        "url": "https://your-mcp-server-domain/mcp"
      }
    }
  }

If you don't have an MCP Server URL yet, please contact your administrator.
```

### When Remote Service is Unreachable

```
⚠️  Gate Wallet MCP Server Connection Failed

MCP Server configuration was found, but the remote service cannot be reached. Please check:
1. Confirm the service URL is correct (is the configured URL accessible?)
2. Check network connection (does VPN / firewall affect access?)
3. Confirm the remote service is running
```

### When API Key Authentication Fails

```
🔑 Gate Wallet MCP Server Authentication Failed

MCP Server is connected but API Key validation failed. The service uses AK/SK authentication (x-api-key header).
Please contact your administrator for a valid API Key and confirm the server configuration is correct.
```

## Authentication Overview

This Skill is the auth entry point. **Executing login itself does not require `mcp_token`**. `auth.refresh_token` and `auth.logout` require an existing token.

After successful login, the obtained `mcp_token` and `account_id` will be passed to other Skills that require authentication (portfolio, transfer, swap, dapp).

## MCP Tool Call Specification

### 1. `auth.google_login_start` — Start Google OAuth Login

Initiates Google Device Flow login and returns the verification URL the user needs to visit.

| Field | Description |
|-------|-------------|
| **Tool name** | `auth.google_login_start` |
| **Parameters** | None |
| **Return value** | `{ verification_url: string, flow_id: string }` |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="auth.google_login_start",
  arguments={}
)
```

Return example:

```json
{
  "verification_url": "https://accounts.google.com/o/oauth2/device?user_code=ABCD-EFGH",
  "flow_id": "flow_abc123"
}
```

Agent behavior: Display `verification_url` to the user and guide them to complete Google authorization in the browser.

---

### 2. `auth.google_login_poll` — Poll Login Status

Uses `flow_id` to poll Google OAuth login result and determine whether the user has completed browser-side authorization.

| Field | Description |
|-------|-------------|
| **Tool name** | `auth.google_login_poll` |
| **Parameters** | `{ flow_id: string }` |
| **Return value** | `{ status: string, mcp_token?: string, refresh_token?: string, account_id?: string }` |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="auth.google_login_poll",
  arguments={ flow_id: "flow_abc123" }
)
```

`status` value meanings:

| status | Meaning | Next action |
|--------|---------|-------------|
| `pending` | User has not completed authorization | Wait a few seconds and retry |
| `success` | Login successful | Extract `mcp_token`, `refresh_token`, `account_id` |
| `expired` | Login flow timed out | Prompt user to restart login |
| `error` | Login error | Display error message |

---

### 3. `auth.login_google_wallet` — Google Authorization Code Login

Uses Google OAuth authorization code to log in directly (for scenarios where a code is already available).

| Field | Description |
|-------|-------------|
| **Tool name** | `auth.login_google_wallet` |
| **Parameters** | `{ code: string, redirect_url: string }` |
| **Return value** | `MCPLoginResponse` (includes `mcp_token`, `refresh_token`, `account_id`) |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="auth.login_google_wallet",
  arguments={ code: "4/0AX4XfW...", redirect_url: "http://localhost:8080/callback" }
)
```

---

### 4. `auth.refresh_token` — Refresh Token

When `mcp_token` expires, use `refresh_token` to obtain a new valid token.

| Field | Description |
|-------|-------------|
| **Tool name** | `auth.refresh_token` |
| **Parameters** | `{ refresh_token: string }` |
| **Return value** | `RefreshTokenResponse` (includes new `mcp_token`, new `refresh_token`) |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="auth.refresh_token",
  arguments={ refresh_token: "rt_xyz789..." }
)
```

Agent behavior: After successful refresh, silently update the internally held `mcp_token`; user is unaware.

---

### 5. `auth.logout` — Logout

Revokes the current session and invalidates `mcp_token`.

| Field | Description |
|-------|-------------|
| **Tool name** | `auth.logout` |
| **Parameters** | `{ mcp_token: string }` |
| **Return value** | `"session revoked"` |

Call example:

```
CallMcpTool(
  server="gate-wallet",
  toolName="auth.logout",
  arguments={ mcp_token: "<current_mcp_token>" }
)
```

## Skill Routing

After authentication completes, route to the corresponding Skill based on the user's original intent:

| User intent | Route target |
|-------------|--------------|
| Check balance, assets, address | `gate-dex-mcpwallet` |
| Transfer, send tokens | `gate-dex-mcptransfer` |
| Swap, exchange tokens | `gate-dex-mcpswap` |
| DApp interaction, sign messages | `gate-dex-mcpdapp` |
| Check market, token info | `gate-dex-mcpmarket` |

When other Skills detect missing or expired `mcp_token`, they also route to this Skill for authentication before returning to the original operation.

## Operation Flows

### Flow A: Google Device Flow Login (Primary)

```
Step 0: MCP Server pre-check
  ↓ Success
Step 1: Intent recognition
  Agent determines user needs to log in (direct login request, or redirected by another Skill)
  ↓
Step 2: Initiate login
  Call auth.google_login_start → Get verification_url + flow_id
  ↓
Step 3: Guide user authorization
  Display verification link to user, ask them to complete Google authorization in browser:

  ────────────────────────────
  Please open the following link in your browser to complete Google login:
  {verification_url}

  After completing, please tell me and I will confirm the login status.
  ────────────────────────────

  ↓
Step 4: Poll login result
  After user confirms authorization is complete, call auth.google_login_poll({ flow_id })
  - status == "pending" → Prompt user to confirm if complete, poll again later (max 10 retries, 3 sec interval)
  - status == "success" → Extract mcp_token, refresh_token, account_id, proceed to Step 5
  - status == "expired" → Prompt timeout, suggest restarting login
  - status == "error" → Display error message
  ↓
Step 5: Login success
  Store mcp_token, refresh_token, account_id internally (do not show token plaintext to user)
  Confirm login success to user:

  ────────────────────────────
  ✅ Login successful!
  Account: {account_id} (masked display)

  You can now:
  - View wallet balance and assets
  - Transfer and send tokens
  - Swap and exchange tokens
  - Interact with DApps
  - View market data

  What would you like to do?
  ────────────────────────────

  ↓
Step 6: Route to user's original intent
  Guide to the corresponding Skill based on user's initial request or follow-up instruction
```

### Flow B: Token Refresh (Auto-triggered)

```
Trigger: Other Skill's MCP tool call returns token expired error
  ↓
Step 1: Auto refresh
  Call auth.refresh_token({ refresh_token })
  ↓
Step 2a: Refresh success
  Silently update mcp_token, retry original operation; user unaware
  ↓
Step 2b: Refresh failed
  refresh_token also expired → Guide user to re-login (Flow A)

  ────────────────────────────
  ⚠️ Session has expired. Please log in again.
  Initiating Google login for you...
  ────────────────────────────
```

### Flow C: Logout

```
Step 0: MCP Server pre-check
  ↓ Success
Step 1: Intent recognition
  User requests logout / sign out
  ↓
Step 2: Execute logout
  Call auth.logout({ mcp_token })
  ↓
Step 3: Clear state
  Clear internally held mcp_token, refresh_token, account_id
  ↓
Step 4: Confirm logout

  ────────────────────────────
  ✅ Successfully logged out.
  To use wallet features again, please log in.
  ────────────────────────────
```

### Flow D: Authorization Code Login (Alternative)

```
Step 0: MCP Server pre-check
  ↓ Success
Step 1: User provides Google authorization code
  ↓
Step 2: Execute login
  Call auth.login_google_wallet({ code, redirect_url })
  ↓
Step 3: Login success
  Extract mcp_token, refresh_token, account_id → Same as Flow A Step 5
```

## Cross-Skill Workflow

### Called by Other Skills (Auth Pre-requisite)

All Skills that require `mcp_token` should route to this Skill when they detect unauthenticated state:

```
Any Skill operation (requires mcp_token)
  → Detect no mcp_token or token expired
    → Auto try auth.refresh_token (if refresh_token exists)
      → Refresh success → Return to original Skill to continue
      → Refresh failed → gate-dex-mcpauth Flow A (login)
        → Login success → Return to original Skill to continue
```

### Typical Post-Login Workflow

```
gate-dex-mcpauth (login)
  → gate-dex-mcpwallet (check balance/assets)   # Most common follow-up
  → gate-dex-mcptransfer (transfer)             # User explicitly wants transfer
  → gate-dex-mcpswap (Swap)                      # User explicitly wants swap
  → gate-dex-mcpdapp (DApp interaction)          # User explicitly wants DApp interaction
```

## Edge Cases and Error Handling

| Scenario | Handling |
|----------|----------|
| MCP Server not configured | Abort all operations, show Cursor configuration guide |
| MCP Server unreachable | Abort all operations, show network check prompt |
| `auth.google_login_start` failed | Display error, suggest retry later or check MCP Server status |
| User did not complete authorization in browser | Poll returns `pending`, prompt user to complete browser-side step first |
| Login flow timeout (`expired`) | Prompt timeout, auto re-call `auth.google_login_start` to start new flow |
| `auth.google_login_poll` repeated failures | Max 10 retries (3 sec interval), then prompt user to check network or retry |
| `auth.refresh_token` failed | refresh_token expired or invalid → Guide to full login flow |
| `auth.logout` failed | Display error, still clear locally held token state |
| User logs in again | If already holding valid `mcp_token`, prompt that already logged in, ask if need to switch account |
| Invalid code for `auth.login_google_wallet` | Display error, suggest user re-obtain authorization code or use Device Flow |
| Network interruption | Display network error, suggest checking network and retrying |

## Security Rules

1. **`mcp_token` confidentiality**: Never display `mcp_token` or `refresh_token` in plaintext to the user; use placeholder `<mcp_token>` in conversation only.
2. **`account_id` masking**: When displaying, show only partial characters (e.g. `acc_12...89`).
3. **Token auto-refresh**: When `mcp_token` expires, try silent refresh first; only require re-login if refresh fails.
4. **No silent login retries**: After login failure, clearly show error to user; do not retry repeatedly in background.
5. **No operations when MCP Server not configured or unreachable**: If Step 0 connection check fails, abort all subsequent steps.
6. **Single session, single account**: Maintain only one active `mcp_token` at a time; switching accounts requires logout first.
7. **MCP Server error transparency**: All MCP Server error messages are shown to the user as-is; do not hide or alter them.
