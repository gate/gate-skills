# Shared Skill Update Workflow

> Mirrors the legacy `gate-info-business-skills` Trigger-update pattern, simplified for this repo. Every primary skill ships `scripts/update-skill.sh` (+ `.ps1`) so developers can check the remote **master** branch on [gate/gate-skills](https://github.com/gate/gate-skills) and apply an update with an explicit two-step confirmation.

> **Status: OPT-IN, not part of the default agent flow.** Each `SKILL.md` has the `Step 0.5 — Update check` block wrapped in an HTML comment, so agents skip it by default. Skill authors can still run the script manually; to re-enable inside the agent flow, just delete the `<!-- ... -->` wrapper in the skill's `SKILL.md`.

## Remote source (public GitHub)

| Field | Value |
|---|---|
| Canonical repo (HTTPS) | `https://github.com/gate/gate-skills.git` |
| Branch tracked | **`master`** |
| Version-check (raw `SKILL.md` head) | `https://raw.githubusercontent.com/gate/gate-skills/master/skills/<name>/SKILL.md` |
| Archive fallback (zip / tar.gz) | `https://github.com/gate/gate-skills/archive/refs/heads/master.zip` and `.../master.tar.gz` — when `git` is not installed. Extracted root folder: `gate-skills-master/`. |

1. **`apply` (overwrite skill files)** — `git clone --depth 1 --branch master` from the HTTPS URL, or download the archive. No personal access token is required for the public repo.
2. **`check` (compare remote vs local `version` / `updated`)** — `curl` / `Invoke-WebRequest` the **raw** URL above. Anonymous access is enough for the default upstream.

If you point the scripts at a **private** fork, set `GATE_SKILL_GITLAB_TOKEN` (legacy name; sent as a generic auth header in some code paths) or `GATE_SKILL_HTTP_AUTH` as documented in `scripts/update-skill.sh`.

### Behavior without private-mirror auth

`check` degrades gracefully to `Result=check_failed` (exit `0`) → `GATE_SKILL_UPDATE_AGENT_ACTION=CONTINUE_SKILL_EXECUTION` when the **remote** is unreachable — the skill main flow proceeds unchanged on the locally-installed version. The only exception is when the **local** `$DEST/SKILL.md` itself is missing: the script still prints `Result=check_failed` but exits `1`, signalling a broken install that requires re-clone / re-install before Step 1 can run. See the full table below for exit-code semantics. `apply` can still fail if the network or git tools are missing.

## When the workflow runs

- **On each skill invocation**, Step 0 (Preflight) runs first. Update check runs **after** Preflight returned `route == "CLI"` and **before** Step 1 (Intent routing).
- The agent runs `check` ONLY; it never runs `apply` or `run` in the same turn — if `check` reports `update_available`, the agent asks the user, and in the user's next turn executes `apply` (approved) or `revoke-pending` (declined).
- Update check failures MUST NOT be surfaced to the user. Fall through to the skill execution on the current local version.

## Command forms

```bash
# macOS / Linux / WSL / Git Bash
bash "$SKILL_ROOT/scripts/update-skill.sh" check        <name>
bash "$SKILL_ROOT/scripts/update-skill.sh" apply        <name>
bash "$SKILL_ROOT/scripts/update-skill.sh" revoke-pending <name>
```

```powershell
# Windows PowerShell
powershell -ExecutionPolicy Bypass -File "$SKILL_ROOT\scripts\update-skill.ps1" check        <name>
powershell -ExecutionPolicy Bypass -File "$SKILL_ROOT\scripts\update-skill.ps1" apply        <name>
powershell -ExecutionPolicy Bypass -File "$SKILL_ROOT\scripts\update-skill.ps1" revoke-pending <name>
```

`<name>` is the skill id (folder name and frontmatter `name`), e.g. `gate-info-research`.

## Result semantics (agent-parseable)

The script prints one of these tokens to stdout as its last line. Tokens + exit codes below are verified against both `update-skill.sh` and `update-skill.ps1` as of 2026-04-18.

| `Result=` token | Exit code | Condition | Next action |
|---|---|---|---|
| `skipped` | `0` | `check`: local and remote `version` + `updated` are equal. | Proceed to Step 1 silently. |
| `update_available` | `0` (normal) / **`3` (strict)** | `check`: remote newer than local. In strict mode (`GATE_SKILL_CHECK_STRICT=1`) the script additionally prints `GATE_SKILL_CHECK_EXIT=3` and returns `3`. | STOP — ask user. On the user's next turn run `apply` (approved) or `revoke-pending` (declined). **Never** chain `apply` in the same turn. |
| `success` | `0` | `apply`: files replaced OK; local SKILL.md now matches remote. | Proceed to Step 1 on the new version. |
| `check_failed` (remote branch) | `0` | Remote fetch failed (network / auth / proxy) OR remote SKILL.md missing `version:` header. | Proceed silently to Step 1 on the **current local** version. Do NOT surface this to the user. |
| `check_failed` (local branch) | **`1`** | Local skill install is broken: `$DEST/SKILL.md` does NOT exist. | Step 1 CANNOT run — there is no local skill to execute. Surface as "skill install incomplete; re-clone or re-install to `$DEST` before retrying". |
| `failure` | `1` (most) / `2` (missing confirm token in strict two-step) | `apply` error — download failed, copy failed, or `GATE_SKILL_CONFIRM_TOKEN` missing / wrong in strict mode. | Tell user **once**, do NOT retry in the same turn. Proceed to Step 1 only if user explicitly asks. |
| `revoke_pending_ok` | `0` | `revoke-pending`: the strict-mode apply token was cleared (user declined the update). | Proceed to Step 1 on the current version. |

### Exit-code contract summary

| Exit | Semantic |
|---|---|
| `0` | Normal non-blocking path: `skipped`, `update_available` (non-strict), `success`, `check_failed` (remote branch), `revoke_pending_ok`. Agent proceeds to Step 1. |
| `1` | Hard failure: `apply` download/copy failed, OR `check_failed` local branch (local SKILL.md missing — skill install broken). Step 1 may not be runnable; surface actionable error to user. |
| `2` | Strict two-step gate: `apply` invoked without matching `GATE_SKILL_CONFIRM_TOKEN`. Agent should re-run `check` strictly, surface the token, wait for user confirm. |
| `3` | Strict `check` saw `update_available` — **success path that requires user input**, NOT a crash. Agent ends the current turn and waits for user confirmation. |

> Two `check_failed` branches exist on purpose: "remote unreachable" is a transient / network issue (exit 0, keep executing on local copy), while "local SKILL.md missing" is a broken install (exit 1, user must fix their install before Step 1 is even possible). Both still print `Result=check_failed` for backward compatibility with log parsers; read the exit code to disambiguate.
>
> Agents MUST NOT surface exit code `3` to the user as an error. When exit is `3`, end the current turn and wait for user confirmation. When exit is `0` with `Result=check_failed`, proceed to Step 1 without mentioning the check. When exit is `1` with `Result=check_failed`, surface the `missing <path>` message verbatim and ask the user to re-install or re-clone.

## Install roots the script recognizes

Single-arg `check`/`apply` auto-resolves `$DEST` to the first directory that contains `SKILL.md` from this list:

```
~/.cursor/skills/<name>/
~/.codex/skills/<name>/
~/.openclaw/skills/<name>/
~/.agents/skills/<name>/
~/.gemini/antigravity/skills/<name>/
```

If the skill lives only inside the source repo (`gate-cli-skills/skills/<name>/`), pass `$DEST` explicitly:

```bash
bash scripts/update-skill.sh check "$PWD/skills/<name>" <name>
```

## Hard rules for agents

1. NEVER download and run `update-skill.sh` from the network on the fly. Only run the copy that was installed alongside the skill.
2. NEVER chain `check` and `apply` in one message when `Result=update_available` is possible. Two-step gate is mandatory.
3. When the script exits non-zero with `GATE_SKILL_CHECK_EXIT=3`, treat it as **success that needs user input**, NOT an error.
4. Set `GATE_SKILL_UPDATE_MODE=auto` only in CI / unattended automation. Never in interactive agent turns.

> Canonical script source: `skills/<name>/scripts/update-skill.sh` and `scripts/update-skill.ps1`.
