---
name: gate-dex-wallet-auth
version: "2026.3.12-1"
updated: "2026-03-12"
description: "Gate Wallet authentication. Use when users need to login, logout, refresh session, or when other Skills detect not logged in (no mcp_token). Supports Google OAuth and Gate OAuth login. First use will detect if MCP Server is configured and connected."
---

# Gate DEX Auth

> Authentication domain — manages Google OAuth and Gate OAuth login, token refresh and logout. 5 MCP tools.

**Trigger scenarios**: Users mention "login", "logout", "authentication", "sign in", or other Skills detect missing `mcp_token`.

**Prerequisites**: MCP Server available (see parent SKILL.md for detection). If not configured, see parent SKILL.md for setup guide.

## Authentication Notes

This Skill is the authentication entry point, **performing login operations themselves does not require `mcp_token`**. `dex_auth_refresh_token` and `dex_auth_logout` require existing tokens.

The `mcp_token` and `account_id` obtained after successful login will be passed to other Skills requiring authentication (portfolio, transfer, swap, dapp).

## MCP Tool Call Specifications

### 1. `dex_auth_google_login_start` — Start Google OAuth Login

Initiates Google Device Flow login, returns the verification URL users need to visit.

| Field | Description |
|-------|-------------|
| **Tool Name** | `dex_auth_google_login_start` |
| **Parameters** | None |
| **Return Value** | `{ verification_url: string, flow_id: string }` |

Call example:

```
CallMcpTool(
  server="gate-dex",
  toolName="dex_auth_google_login_start",
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

Agent behavior: Display `verification_url` directly to user, guiding them to complete Google authorization in browser.

**Important**: URL display format must ensure the link is complete, copyable and clickable, do not add quotes, parentheses or other decorators, do not escape URL content.

---

### 2. `dex_auth_google_login_poll` — Poll Login Status

Uses `flow_id` to poll Google OAuth login results, determining if user has completed browser-side authorization.

| Field | Description |
|-------|-------------|
| **Tool Name** | `dex_auth_google_login_poll` |
| **Parameters** | `{ flow_id: string }` |
| **Return Value** | `{ status: string, mcp_token?: string, refresh_token?: string, account_id?: string }` |

Call example:

```
CallMcpTool(
  server="gate-dex",
  toolName="dex_auth_google_login_poll",
  arguments={ flow_id: "flow_abc123" }
)
```

Return value `status` meanings:

| status | Meaning | Next Action |
|--------|---------|-------------|
| `pending` | User has not completed authorization yet | Wait a few seconds then retry |
| `success` | Login successful | Extract `mcp_token`, `refresh_token`, `account_id` |
| `expired` | Login process timed out | Prompt user to initiate login again |
| `error` | Login error | Display error message |

---

### 3. `auth.login_google_wallet` — Google Authorization Code Login

Uses Google OAuth authorization code to login directly (suitable for scenarios with existing code).

| Field | Description |
|-------|-------------|
| **Tool Name** | `auth.login_google_wallet` |
| **Parameters** | `{ code: string, redirect_url: string }` |
| **Return Value** | `MCPLoginResponse` (containing `mcp_token`, `refresh_token`, `account_id`) |

Call example:

```
CallMcpTool(
  server="gate-dex",
  toolName="auth.login_google_wallet",
  arguments={ code: "4/0AX4XfW...", redirect_url: "http://localhost:8080/callback" }
)
```

---

### 4. `dex_auth_refresh_token` — Refresh Token

When `mcp_token` expires, use `refresh_token` to obtain a new valid token.

| Field | Description |
|-------|-------------|
| **Tool Name** | `dex_auth_refresh_token` |
| **Parameters** | `{ refresh_token: string }` |
| **Return Value** | `RefreshTokenResponse` (containing new `mcp_token`, new `refresh_token`) |

Call example:

```
CallMcpTool(
  server="gate-dex",
  toolName="dex_auth_refresh_token",
  arguments={ refresh_token: "rt_xyz789..." }
)
```

Agent behavior: After successful refresh, silently update internally held `mcp_token`, transparent to user.

---

### 5. `dex_auth_logout` — Logout

Revokes current session, invalidating `mcp_token`.

| Field | Description |
|-------|-------------|
| **Tool Name** | `dex_auth_logout` |
| **Parameters** | `{ mcp_token: string }` |
| **Return Value** | `"session revoked"` |

Call example:

```
CallMcpTool(
  server="gate-dex",
  toolName="dex_auth_logout",
  arguments={ mcp_token: "<current_mcp_token>" }
)
```

## Skill Routing

After authentication completion, route to corresponding Skill based on user's original intent:

| User Intent | Route Target |
|-------------|--------------|
| Check balance, assets, address | `gate-dex-wallet` |
| Transfer, send tokens | `gate-dex-wallet/references/transfer.md` |
| Exchange, swap tokens | `gate-dex-trade` |
| DApp interaction, sign messages | `gate-dex-wallet/references/dapp.md` |
| Check quotes, token info | `gate-dex-market` |

When other Skills detect missing or expired `mcp_token`, they will also route to this Skill for authentication before returning to original operations.

## Operation Flows

### Flow A: Google Device Flow Login (Main Flow)

```
First session detection (if needed)
  ↓ Success
Step 1: Intent Recognition
  Agent determines user needs to login (direct login request, or guided here by other Skills)
  ↓
Step 2: Initiate Login
  Call dex_auth_google_login_start → Get verification_url + flow_id
  ↓
Step 3: Guide User Authorization
  Display verification link to user, ask user to complete Google authorization in browser:

  ────────────────────────────
  Please open the following link in your browser to complete Google login:
  
  https://accounts.google.com/o/oauth2/device?user_code=ABCD-EFGH

  After completion, please let me know and I'll confirm the login status.
  ────────────────────────────

**Note**: When displaying URLs, show complete link directly without adding quotes, parentheses or other decorators, ensuring users can directly copy and click.

  ↓
Step 4: Poll Login Results
  After user confirms completion of authorization, call dex_auth_google_login_poll({ flow_id })
  - status == "pending" → Ask user to confirm completion, poll again later (max 10 retries, 3 second intervals)
  - status == "success" → Extract mcp_token, refresh_token, account_id, proceed to Step 5
  - status == "expired" → Notify timeout, suggest re-initiating login
  - status == "error" → Display error message
  ↓
Step 5: Login Success
  Internally record mcp_token, refresh_token, account_id (do not display token plaintext to user)
  Confirm login success to user:

  ────────────────────────────
  ✅ Login successful!
  Account: {account_id} (masked display)

  You can now:
  - View wallet balance and assets
  - Transfer and send tokens
  - Swap and exchange tokens
  - Interact with DApps
  - View market quotes

  What would you like to do?
  ────────────────────────────

  ↓
Step 6: Route to User's Original Intent
  Based on user's initial request or subsequent instructions, guide to corresponding Skill
```

### Flow B: Token Refresh (Automatic Trigger)

```
Trigger condition: Other Skills return token expiration error when calling MCP tools
  ↓
Step 1: Auto Refresh
  Call dex_auth_refresh_token({ refresh_token })
  ↓
Step 2a: Refresh Success
  Silently update mcp_token, retry original operation, transparent to user
  ↓
Step 2b: Refresh Failed
  refresh_token also expired → Guide user to re-login (Flow A)

  ────────────────────────────
  ⚠️ Session has expired, need to re-login.
  Initiating Google login for you...
  ────────────────────────────
```

### Flow C: Logout

```
First session detection (if needed)
  ↓ Success
Step 1: Intent Recognition
  User requests logout / exit
  ↓
Step 2: Execute Logout
  Call dex_auth_logout({ mcp_token })
  ↓
Step 3: Clean State
  Clear internally held mcp_token, refresh_token, account_id
  ↓
Step 4: Confirm Logout

  ────────────────────────────
  ✅ Successfully logged out.
  To use wallet functions again, please re-login.
  ────────────────────────────
```

### Flow D: Authorization Code Login (Alternative)

```
First session detection (if needed)
  ↓ Success
Step 1: User provides Google authorization code
  ↓
Step 2: Execute Login
  Call auth.login_google_wallet({ code, redirect_url })
  ↓
Step 3: Login Success
  Extract mcp_token, refresh_token, account_id → Same as Flow A Step 5
```

## Edge Cases and Error Handling

| Scenario | Handling |
|----------|----------|
| `dex_auth_google_login_start` fails | Display error message, suggest retry later or check MCP Server status |
| User hasn't completed browser authorization | Poll returns `pending`, prompt user to complete browser operation first |
| Login process timeout (`expired`) | Notify timeout, automatically call `dex_auth_google_login_start` to initiate new flow |
| `dex_auth_google_login_poll` consecutive failures | Max 10 retries (3 second intervals), after exceeded prompt user to check network or retry |
| `dex_auth_refresh_token` fails | refresh_token expired or invalid → Guide through complete re-login flow |
| `dex_auth_logout` fails | Display error message, still clear local token state |
| User repeated login | If already holding valid `mcp_token`, notify already logged in, ask if need to switch accounts |
| Invalid code in `auth.login_google_wallet` | Display error, suggest user re-obtain authorization code or use Device Flow |

## Security Rules

1. **`mcp_token` confidentiality**: Never display `mcp_token` or `refresh_token` in plaintext to users, only use placeholders like `<mcp_token>` in conversations.
2. **`account_id` masking**: When displaying, only show partial characters (e.g. `acc_12...89`).
3. **Auto token refresh**: When `mcp_token` expires, prioritize silent refresh, only require re-login if refresh fails.
4. **No silent login retry**: After login failure, clearly display error to user, don't repeatedly retry in background.
5. **Prohibit operations when MCP Server not configured or unreachable**: If Step 0 connection detection fails, abort all subsequent steps.
6. **Single session single account**: Only maintain one active `mcp_token` at a time, switching accounts requires logout first.
7. **Transparent MCP Server errors**: All error messages returned by MCP Server should be displayed to users truthfully, without hiding or tampering.