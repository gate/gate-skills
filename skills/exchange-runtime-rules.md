# Exchange Common Runtime Rules

> Shared runtime rules for all `gate-exchange-*` skills.
> Each skill's SKILL.md should include: `Read and follow [exchange-runtime-rules.md](../exchange-runtime-rules.md) first.`

---

## 1. Auto Update (Silent)

Every time a `gate-exchange-*` skill is triggered, silently check for a newer version — **do not ask the user for permission**, just update automatically:

1. Read the local `version` field from the frontmatter of the currently installed SKILL.md (e.g. `~/.cursor/skills/<skill-name>/SKILL.md`).
2. Read the source version from the local gate-skills repository at `/Users/kobin/bitbucket/gate-skills/skills/<skill-name>/SKILL.md` and extract its `version` field.
3. If the source version is newer than the installed version:
   a. Copy the entire `<skill-name>/` directory from `/Users/kobin/bitbucket/gate-skills/skills/<skill-name>/` to `~/.cursor/skills/<skill-name>/` (overwrite).
   b. Also copy `exchange-runtime-rules.md` from `/Users/kobin/bitbucket/gate-skills/skills/exchange-runtime-rules.md` to `~/.cursor/skills/exchange-runtime-rules.md` (overwrite) to keep shared rules in sync.
   c. **Re-read the updated SKILL.md** so the current session immediately uses the new version's rules and tools.
   d. Briefly inform the user that the skill has been auto-updated to the latest version.
4. If the source path does not exist or the read fails, silently skip and continue with the current version.
5. The update process must not block the user's request — after updating, continue processing the original request.

---

## 2. MCP Installation Check

Before using any MCP-dependent tool, verify that the Gate MCP server is available (e.g. the expected `cex_spot_*`, `cex_fx_*` tools exist and respond).

If the Gate MCP server is **not** available (tools not found, MCP connection fails, or the `gate-mcp` command is missing):

1. Inform the user that Gate MCP is not installed yet.
2. Show the one-click installer page: https://github.com/gate/gate-skills/tree/master/skills
3. **Ask the user if they would like you to run the one-click installer** to set up all Gate MCP servers and skills automatically.
4. If the user agrees, invoke the corresponding installer skill for the current IDE:
   - **Cursor**: `gate-mcp-cursor-installer`
   - **Claude Code**: `gate-mcp-claude-installer`
   - **Codex**: `gate-mcp-codex-installer`
   - **OpenClaw**: `gate-mcp-openclaw-installer`
5. Install all MCPs (main/dex/info/news) + all gate-skills.
6. After installation completes, prompt the user to restart the IDE, then resume the original request.

---

## 3. Error-First Documentation Lookup

When encountering **any** error from MCP tool calls:

1. Read the relevant documentation or error details first.
2. Try documented solutions (see [General Error Table](#6-general-error-table) below) before asking the user or retrying blindly.
3. Only escalate to the user when documentation does not cover the error or automated recovery fails.

---

## 4. Authorization Error Handling

When any MCP tool call returns an authentication/authorization error (e.g. `INVALID_KEY`, `UNAUTHORIZED`, `API key is required`, HTTP 401/403), **do not retry silently**. Instead, guide the user through the authorization process:

1. Explain that the operation requires a valid Gate API Key and Secret.
2. Provide the API Key management page — both desktop and mobile are supported:
   - **Desktop (gate.com)**: https://www.gate.com/zh/myaccount/profile/api-key/manage
   - **Mobile (Gate APP)**: Open the Gate APP, tap the search bar and search for **"API"** to find the API management page.
3. When creating the API Key, the user should enable at least the **relevant trading permission** (e.g. Spot Trading, Futures Trading) and **Read** permission.
4. Ask the user to provide the API Key and Secret so you can configure them (set `GATE_API_KEY` and `GATE_API_SECRET` in the MCP environment).
5. **Do not** ask the user to paste the Secret Key directly into chat in plain text — prefer secure local configuration when possible.
6. After authorization is completed, continue the original task.

Recommended response template:

```
Your request requires a Gate API Key, but the current session is not authorized.

To set up authorization:
1. **Desktop** — Visit https://www.gate.com/zh/myaccount/profile/api-key/manage to create an API Key (enable the relevant trading permission + Read permission).
2. **Mobile** — Open the Gate APP → search "API" in the search bar → go to API management to create a key.

Both desktop (gate.com) and mobile (Gate APP) can be used to manage your API keys.
After creating the key, please provide me with your API Key and Secret so I can configure them for you.
```

---

## 5. Confirmation Before Execution

For any **write operation** (order placement, cancellation, amendment, transfer), always:

1. Present a clear **order/action draft** summarizing all key parameters.
2. Wait for explicit user confirmation before executing.
3. Treat each confirmation as single-use — require fresh confirmation for every new operation.
4. If confirmation is missing, ambiguous, or negative, stay in read-only/draft mode and do not execute.

---

## 6. General Error Table

| Error Type | Typical Cause | Handling Strategy |
|---|---|---|
| MCP not installed / tools not found | Gate MCP server not configured or expected tools unavailable | Follow [MCP Installation Check](#2-mcp-installation-check) above |
| Unauthorized / no API Key | API Key not configured or invalid | Follow [Authorization Error Handling](#4-authorization-error-handling) above |
| Insufficient balance | Not enough available funds | Return shortfall amount and suggest reducing order size or depositing |
| Minimum trade constraint | Below minimum amount/size | Return threshold and suggest increasing order size |
| Rate limit / throttling | Too many requests in a short period | Wait and retry with exponential backoff; inform user if persistent |
| Network / timeout | MCP connection interrupted | Retry once; if still failing, inform user and suggest checking connection |
| Invalid parameter | Wrong format, precision, or value range | Read error details, correct parameter, and retry |
| Pair / contract unavailable | Currency suspended or abnormal status | Clearly state the asset is currently not tradable |
| Unknown error | Unrecognized error code | Log error details, inform user, and suggest retrying or checking Gate status |

---

## 7. Safety Rules

- For all-in / full-balance / one-click requests, always restate key amount and symbol before execution.
- For condition-based requests, explicitly show how the trigger threshold is calculated.
- Do not fabricate or assume capabilities that are not supported — clearly state limitations.
- Never execute a trade without explicit user confirmation in the immediately previous turn.
- For chained / multi-step actions, report step-by-step results clearly.
- If any pre-condition is not met, do not force execution — explain and provide alternatives.

---

## Usage

Each `gate-exchange-*` SKILL.md should reference this file in its **General Rules** section:

```markdown
## General Rules

Read and follow the shared runtime rules before proceeding:
→ [exchange-runtime-rules.md](../exchange-runtime-rules.md)

(Skill-specific rules below, if any.)
```

This ensures consistent behavior across all exchange skills while allowing each skill to add its own domain-specific rules.
