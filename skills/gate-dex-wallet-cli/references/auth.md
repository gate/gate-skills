---
name: gate-dex-wallet-cli-auth
version: "2026.4.23-2"
updated: "2026-04-23"
description: "gate-wallet CLI authentication module. Gate OAuth and Google OAuth login via Device Flow. Logout, session status, web3-domain management, and cleanup. Auth token stored in ~/.gate-wallet/auth.json. Supports --auth-file for third-party injection."
---

# Gate Wallet CLI — Auth

> Authentication module — Gate OAuth and Google OAuth Device Flow login, logout, and session status. Pure CLI; no MCP server required.

## Applicable Scenarios

- Direct login request: "login", "sign in", "authenticate", "use Gate wallet"
- Logout: "logout", "sign out", "end session"
- Session/token issues: "not logged in", "session expired", "token invalid"
- Account switching: "switch account", "login with different account"
- Routed from other modules when any command prints `Not logged in. Run: login`
- OAuth-specific: "Google login", "Gate login", "login via Google"

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `gate-wallet login` | Gate OAuth Device Flow login (default) |
| `gate-wallet login --google` | Google OAuth Device Flow login |
| `gate-wallet login --no-open` | Print authorization URL instead of opening browser |
| `gate-wallet status` | Show current session info (user_id, account_id, addresses, provider, expiry) |
| `gate-wallet logout` | Logout and clear `~/.gate-wallet/auth.json` |
| `gate-wallet web3-domain` | View dynamic web3_domain list with response times |
| `gate-wallet web3-domain --refresh` | Force re-fetch and re-test all domains |
| `gate-wallet cleanup` | Delete `~/.gate-wallet` directory |

**Storage**: `~/.gate-wallet/auth.json` — contains `mcp_token`, `access_token`, `evm_address`, `sol_address`, `user_id`, `account_id`, `provider`, expiry.

**Third-party injection**: A third party may write `auth.json` directly and point the CLI to it via `--auth-file <path>` (or `GATE_WALLET_AUTH_FILE` env). No login flow required — the CLI reads the file as-is.

```bash
gate-wallet --auth-file /path/to/auth.json status
gate-wallet --auth-file /path/to/auth.json balance
```

---

## Login Flows

### Flow A: Gate OAuth Device Flow (default)

```
Step 1: Run `gate-wallet login`
  |
Step 2: CLI calls BW OAuth start API → receives verification_url
  |
Step 3: CLI automatically opens the URL in the default browser
  Display: "Opening browser for Gate OAuth login..."
  Display the URL to the user (copyable) in case auto-open fails
  |
Step 4: CLI polls authorization status (10s intervals, 120s timeout)
  |- Waiting → display "Waiting for authorization..."
  |- Authorized → CLI prints "Login successful" and writes auth.json
  |- Timeout → display "Login timed out. Please try again."
  |
Step 5: Login success
  Auth token and addresses written to ~/.gate-wallet/auth.json automatically.
  If user had a prior intent → return to that operation.
  If no prior intent → display available actions.
```

### Flow B: Google OAuth Device Flow

```
Step 1: Run `gate-wallet login --google`
  |
Step 2-5: Same flow as Gate OAuth; uses Google as the identity provider.
```

### Flow C: Logout

```
Step 1: Run `gate-wallet logout`
  |
Step 2: CLI revokes server session (best-effort)
  |
Step 3: CLI deletes ~/.gate-wallet/auth.json
  Output: "Logged out. Token cleared."
```

---

## Agent Behavior

**Login:**
1. Run `gate-wallet login` in the terminal (non-background).
2. The CLI will open the browser and poll automatically — the agent does not need to call any API or poll separately.
3. Monitor terminal output for `Login successful` (success) or `Login timed out` (failure).
4. Max wait: 120 seconds. If timed out, prompt user to retry.

**Already logged in:**
- If `gate-wallet login` prints `Already logged in`, the session is active. No action needed.
- If the user wants to switch accounts, run `gate-wallet logout` first, then `gate-wallet login`.

**Check session:**
- `gate-wallet status` shows current user info and server URL without requiring a network call.

---

## Post-Auth Routing

After successful login, if the user was routed here from another module, return them to their original operation silently.

If the user logged in directly (no prior intent), **display available actions**:

```
Login successful!

You can now:
- Check your wallet balance: gate-wallet balance
- View your wallet addresses: gate-wallet address
- See your tokens: gate-wallet tokens
- Transfer tokens: gate-wallet send --chain ETH --to 0x... --amount 0.1
- Swap tokens: gate-wallet swap ...

What would you like to do?
```

| User Follow-up Intent | Route Target |
|----------------------|--------------|
| Check balance / tokens / address | ./asset-query.md |
| Transfer tokens | ./transfer.md |
| Swap tokens | ./swap.md |
| Token market data | ./market.md |

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| `Not logged in. Run: login` | Run `gate-wallet login` |
| Login timeout (120s) | Prompt retry; `gate-wallet login` starts a fresh flow |
| Browser fails to open | Show the URL for manual copy-paste |
| Logout network error | CLI still clears local token; inform user server session may persist briefly |
| Already logged in | Inform user; suggest `logout` if account switch needed |

---

## Security Rules

1. **Never display the raw token** from `auth.json` to users.
2. **Token confidentiality**: `~/.gate-wallet/auth.json` must never be committed to Git.
3. **Single session**: Only one active session at a time. Switching accounts requires logout first.
4. **No silent retry**: After login failure, display the error clearly — do not retry in background.
