# Gate CLI Preflight & Diagnostics Guide

This document details the JSON contracts for the three diagnostic commands
provided by `gate-cli` — `preflight`, `doctor`, `migrate` — and the strategies
that AI skills / agents MUST use when interacting with them.

> **All new skills MUST run `gate-cli preflight --format json` in their
> "Step 0" to verify environment health before executing business logic.**

Samples may show **`gate-cli v0.5.2`** or **`v0.7.6`**; field names are stable.

### Shortcut version gate (Step 0.5)

`preflight` returns `cli_version` but **no shortcut capability flag**. Primary skills parse `cli_version` (strip leading `v`) and set `shortcuts_enabled=true` when `>= 0.7.6` — see [`skills/_shared/cli-version-routing.md`](../skills/_shared/cli-version-routing.md). `version_ok` only reflects the doctor minimum (`0.6.0`), not shortcut availability.

---

## 1. `gate-cli preflight` (agent entry point)

`preflight` is a silent, fast diagnostic designed to be called by AI agents
before every primary skill invocation. It checks CLI availability, version
gating, and scans AI-client config files for legacy Gate MCP entries.

### 1.1 Example output

Real output on a machine that still has legacy Gate MCP entries configured in
Cursor (the most common daily state):

```json
{
  "status": "ready_with_migration_warning",
  "route": "CLI",
  "action_code": "SHOW_MIGRATE_HINT",
  "cli_installed": true,
  "cli_version": "v0.5.2",
  "version_ok": true,
  "legacy_mcp_detected": true,
  "legacy_mcp_entries": [
    {
      "provider_id": "cursor",
      "file_path": "/Users/<username>/.cursor/mcp.json",
      "server_name": "gate-info"
    },
    {
      "provider_id": "cursor",
      "file_path": "/Users/<username>/.cursor/mcp.json",
      "server_name": "gate-news"
    }
  ],
  "providers_scanned": [
    {
      "provider_id": "codex",
      "files_checked": [
        "/home/<username>/.codex/config.toml",
        "/home/<username>/.config/codex/config.toml"
      ],
      "entries_found": 0
    },
    {
      "provider_id": "cursor",
      "files_checked": [
        "/Users/<username>/.cursor/mcp.json",
        "/Users/<username>/.cursor/config.json"
      ],
      "entries_found": 2
    },
    {
      "provider_id": "claude_desktop",
      "files_checked": [
        "/Users/<username>/Library/Application Support/Claude/claude_desktop_config.json"
      ],
      "entries_found": 0
    }
  ],
  "fallback_enabled": true,
  "blocking_reason": "",
  "user_message": "检测到本地仍加载 Gate MCP，建议运行 gate-cli migrate"
}
```

### 1.2 Branching strategy — all 5 `status` values

Skills MUST parse `route` and `status` and branch deterministically. Do NOT
infer from `cli_version` alone.

| `status`                         | `route`        | Meaning                                                                 | Skill action |
|----------------------------------|----------------|-------------------------------------------------------------------------|--------------|
| `ready`                          | `CLI`          | Environment perfect.                                                    | Proceed silently to Step 1. |
| `ready_with_migration_warning`   | `CLI`          | CLI is ready, but legacy Gate MCP entries still exist. **Most common daily state.** | Proceed to Step 1 normally; append a one-line migrate hint at the end of the final report. Do NOT halt. |
| `fallback_to_mcp`                | `MCP_FALLBACK` | CLI not installed, but legacy MCP detected and `fallback_enabled=true`. | Primary skills in this repo do not implement MCP fallback; emit `__FALLBACK__` on stdout and halt so a legacy wrapper can take over. |
| `install_cli_required`           | `BLOCK`        | CLI not installed and no MCP fallback available.                        | Halt. Echo `user_message` and point the user at CLI install docs. |
| `run_doctor_required`            | `BLOCK`        | CLI installed but version below minimum, or config unreadable.          | Halt. Echo `user_message` and recommend `gate-cli doctor`. |

### 1.3 Minimal bash snippet for Step 0

Every primary SKILL.md Step 0 can reuse the same parsing pattern:

```bash
PREFLIGHT_JSON=$(gate-cli preflight --format json)
ROUTE=$(printf '%s' "$PREFLIGHT_JSON"  | jq -r '.route')
STATUS=$(printf '%s' "$PREFLIGHT_JSON" | jq -r '.status')
USER_MSG=$(printf '%s' "$PREFLIGHT_JSON" | jq -r '.user_message')

case "$ROUTE" in
  CLI)
    # status is either "ready" or "ready_with_migration_warning".
    # Record $STATUS so Step 3 can append the migrate hint when needed.
    ;;
  MCP_FALLBACK)
    echo "__FALLBACK__"
    exit 0
    ;;
  BLOCK)
    echo "$USER_MSG"
    exit 1
    ;;
  *)
    echo "unexpected preflight route: $ROUTE" >&2
    exit 2
    ;;
esac
```

The agent may implement the same logic in pure prompting as long as it reads
exactly these two fields and does not introduce any extra branches. Do NOT
rely on exit codes from `preflight` alone — `preflight` can legitimately exit
`0` with `route=BLOCK`.

---

## 2. `gate-cli doctor` (human-readable diagnosis)

If `preflight` returned `route=BLOCK`, the user (or agent, on explicit
request) runs `doctor` for a deeper diagnosis.

### 2.1 Example output

```json
{
  "status": "fail",
  "summary": {
    "cli_installed": true,
    "cli_version": "v0.5.2",
    "minimum_required_version": "0.3.0",
    "legacy_mcp_detected": true,
    "providers_affected": ["cursor"]
  },
  "checks": [
    {
      "id": "cli.binary",
      "status": "pass",
      "blocking": true,
      "message": "gate-cli found in PATH"
    },
    {
      "id": "cli.connectivity",
      "status": "fail",
      "blocking": true,
      "message": "intel endpoint env not configured"
    }
  ],
  "recommended_actions": [
    {
      "action_code": "RUN_MIGRATE",
      "command": "gate-cli migrate --dry-run",
      "reason": "legacy Gate MCP entries detected"
    }
  ]
}
```

### 2.2 Exit codes

| Exit code | Meaning |
|-----------|---------|
| `0`       | All blocking checks pass and there are no warnings. |
| `10`      | All blocking checks pass but one or more non-blocking checks raised warnings (typically `legacy_mcp.*`). |
| `20`      | At least one blocking check failed. |
| `30`      | `doctor` itself failed to run (unparseable config, etc.). |

### 2.3 Agent strategy

- **Do not** run `doctor` automatically inside primary skill execution paths.
  Only run it when the user explicitly asks for troubleshooting, or when
  `preflight` returned `BLOCK` and you want to present an actionable summary.
- Iterate `checks[]`; for every `status == "fail"` with `blocking == true`,
  translate `message` into a clear user-facing line
  (e.g. "you need to set `GATE_INTEL_INFO_MCP_URL`").
- Always surface the `recommended_actions[].command` list verbatim.

---

## 3. `gate-cli migrate` (automated legacy-config cleanup)

Used to safely comment out (or flag for manual edit) legacy Gate MCP entries
in AI-client configuration files so they stop hijacking request routing.

### 3.1 Example output

```json
{
  "mode": "apply",
  "status": "warn",
  "providers": [
    {
      "provider_id": "cursor",
      "file_path": "/Users/<username>/.cursor/mcp.json",
      "action": "manual_patch",
      "status": "warn",
      "manual_patch": "auto-change not safe for this file format; apply manual patch"
    }
  ],
  "recommended_next_step": "rerun_doctor"
}
```

### 3.2 Agent strategy

- **JSON safety**: pure JSON config files (e.g. Cursor's `mcp.json`) will
  always come back as `action: "manual_patch"` with `status: "warn"` — even
  with `--apply`. This is intentional so the CLI cannot corrupt a JSON file by
  injecting comments.
- **Handling `manual_patch`**: guide the user to open `file_path` and remove
  the `gate-info` / `gate-news` blocks themselves. If the user consents, the
  agent MAY use its own JSON-aware editing tools to remove those blocks.
- **Success (`action: "comment"` + `status: "pass"`)**: TOML / line-oriented
  config files; safe to announce completion.
- After any apply, re-run `gate-cli preflight` before continuing any skill
  flow — do NOT reuse the previous preflight result.
