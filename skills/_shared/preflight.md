# Shared Preflight Contract

> Shared across every primary skill in `gate-cli-skills`. A skill's "Step 0" MUST follow this contract before calling any `gate-cli info` / `gate-cli news` data-collection command.

## Why

- Agents MUST NOT guess whether the CLI is installed, whether the version is new enough, or whether legacy MCP entries still hijack routing. `gate-cli preflight --format json` gives a machine-readable answer.
- Every skill branches on the same 5 status values so behavior is deterministic across skills and locales.

## Step 0 snippet (reuse verbatim)

```bash
PREFLIGHT_JSON=$(gate-cli preflight --format json)
ROUTE=$(printf '%s' "$PREFLIGHT_JSON"   | jq -r '.route')
STATUS=$(printf '%s' "$PREFLIGHT_JSON"  | jq -r '.status')
USER_MSG=$(printf '%s' "$PREFLIGHT_JSON" | jq -r '.user_message')

case "$ROUTE" in
  CLI)
    # STATUS is either "ready" or "ready_with_migration_warning".
    # Remember $STATUS — Step 3 appends a migrate hint when it's the latter.
    ;;
  MCP_FALLBACK)
    # Primary skills in this repo do not implement MCP fallback.
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

## Status × action matrix

| `status` | `route` | Skill action |
|---|---|---|
| `ready` | `CLI` | Proceed silently to Step 1. |
| `ready_with_migration_warning` | `CLI` | **Most common daily state.** Proceed normally. In Step 3, append one line to the final report: `⚙️ 检测到本地仍加载 Gate MCP，建议运行 gate-cli migrate --dry-run 清理旧配置.` Never halt. |
| `fallback_to_mcp` | `MCP_FALLBACK` | Emit `__FALLBACK__` on stdout and halt. Legacy-wrapper skills (future round) pick this up. |
| `install_cli_required` | `BLOCK` | Halt. Print `user_message` and a pointer to the CLI install docs. |
| `run_doctor_required` | `BLOCK` | Halt. Print `user_message` and recommend `gate-cli doctor --format json`. |

## Hard rules

1. Step 0 MUST run before the first data-collection command.
2. Never rely on `preflight` exit code alone — `preflight` can exit `0` with `route: BLOCK`.
3. After a user runs `gate-cli migrate`, the skill MUST re-run `preflight` on the next turn; never cache a prior result.
4. When surfacing `user_message`, do NOT append inferred reasons. The message is authoritative.

> Canonical contract detail: `docs/preflight-and-diagnostics.md` (repository root).
