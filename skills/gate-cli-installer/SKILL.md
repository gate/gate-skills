---
name: gate-cli-installer
version: "2026.11.5-1"
updated: "2026-11-05"
description: "Installs or upgrades gate-cli to the latest official GitHub release and sets up gate-skills on Cursor, Claude Code, Codex, or OpenClaw/mcporter. Triggers on 'install gate-cli', 'upgrade gate-cli', 'update gate-cli', 'Gate skills', 'Gate Verify', 'tx check-in', 'setup Gate Cursor', 'Gate Claude Code', 'Gate Codex', 'OpenClaw Gate', 'mcporter Gate'."
---

# gate-cli-installer (Cursor / Claude Code / Codex / OpenClaw)

## General rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding. These rules have the highest priority.  
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)

- **Do not** document or require legacy Gate MCP server setup in this flow. The supported path is **`gate-cli` + [gate-skills](https://github.com/gate/gate-skills)**.
- If the user previously used Gate MCP, optional cleanup is **`gate-cli migrate`** (see *Legacy MCP* below) — do not let migration block a fresh `gate-cli` + skills install.

---

## Which `gate-cli` runs (agents / shells)

Canonical rules (same text as [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) §4):

1. **Prefer the system binary:** If **`command -v gate-cli`** resolves to an executable **and** **`gate-cli --version`** succeeds, use that as **`gate-cli`** everywhere.
2. **User local bin:** If step 1 fails, **if** **`${HOME}/.local/bin/gate-cli`** exists **and** is executable, **`gate-cli`** refers to **`"${HOME}/.local/bin/gate-cli"`** for this session (invoke with full path when PATH may be incomplete).
3. **OpenClaw skills bin:** If steps 1–2 fail, **if** **`${HOME}/.openclaw/skills/bin/gate-cli`** exists **and** is executable, **`gate-cli`** refers to **`"${HOME}/.openclaw/skills/bin/gate-cli"`**.

Assume nothing about a single install location — always resolve in this order before reporting “`gate-cli` not found.” The same rules are in shared **[gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)** §4.

Use this order to locate the current executable; then apply the latest-release check below. A successful version command establishes that the binary runs, not that installation or upgrade is complete.

---

## What to install (two parts)

1. **`gate-cli`** — Gate CLI for CEX, info, news, config, and diagnostics. Install using this skill’s **`setup.sh`** (see below).
2. **gate-skills** — Agent skills from [https://github.com/gate/gate-skills](https://github.com/gate/gate-skills). Use your client’s normal skills workflow (`npx skills add …` or copy into the per-client skills directory).

---

## 1. Install or upgrade `gate-cli` to the latest release (`setup.sh`)

Script path: **`skills/gate-cli-installer/setup.sh`**

For the default latest-release flow, resolve the latest official release on **every installation or upgrade**, including when a working CLI already exists:

1. Query **`https://api.github.com/repos/gate/gate-cli/releases/latest`** and read **`tag_name`**. Use that live result as the target; do not infer it from this skill's version/date, an example, a cached tag, a Git branch, or the local CLI version. This targets GitHub's latest published release, not an unreleased default-branch commit.
2. Resolve the current executable using **Which `gate-cli` runs** and inspect its **`--version`** output. Compare the version with the target tag, ignoring only a leading `v`. Reuse the binary only if it matches. If missing, broken, or older, run the installer below. If a development/custom build or a version newer than the target is found, explain the difference and obtain an explicit replacement decision; do not silently downgrade it or call it the latest official release.
3. Run **`setup.sh` without `--version`** for the default flow. The script queries the latest-release endpoint, downloads that release's OS/architecture asset and `checksums.txt`, verifies the checksum when a supported checksum tool is available, and installs the executable. Ensure `shasum` or `sha256sum` is available before running it; do not accept a run that skips verification.
4. Verify the installed executable and the executable selected by the shell as described below. Do not finish merely because an older executable still runs.
5. If the latest-release lookup, download, checksum verification, or final version check fails, report the failed step and leave installation/upgrade incomplete. Do not fall back silently to an older release or claim that an existing CLI is current.

The script downloads the binary at run time; the skill does not bundle a fixed CLI version. On later runs, repeat the live lookup so newly published releases can be installed without editing this skill.

```bash
# From the repo root, install or upgrade using GitHub's latest release.
bash skills/gate-cli-installer/setup.sh
```

Use **`--version <release-tag>`** only when the user explicitly requests a particular release or rollback. In that exceptional flow, verify that the requested tag is an official published release, use it as the installation and verification target instead of the latest tag, and report the explicit version selection without claiming it is latest unless the live lookup confirms that. Never supply a fixed tag as the default installation or upgrade command.

**Make `gate-cli` available on your PATH (system / shell):**

- **`setup.sh`** installs to **`${HOME}/.local/bin/gate-cli`** first. If **`~/.local/bin`** is **not** already on your **`PATH`**, the script prints a reminder to add:  
  `export PATH="$HOME/.local/bin:$PATH"`  
  Put that in `~/.zshrc`, `~/.bashrc`, or your shell profile, then restart the terminal or **`source`** the file.
- If **`~/.local/bin`** cannot be written, the script falls back to **`/usr/local/bin`** (typically already on **`PATH`** on macOS/Linux).
- Older installs may leave **`${HOME}/.openclaw/skills/bin/gate-cli`**; agents must still resolve **`gate-cli`** using **Which \`gate-cli\` runs** above — do not assume only one directory.

**Verify the installed version and the active executable**

Use the absolute installation path printed by the script to run **`--version`** first. For the usual user-local installation:

```bash
# Verify the new file before checking which binary the shell selects.
"$HOME/.local/bin/gate-cli" --version
command -v gate-cli
gate-cli --version
```

Require both the installed file and the active executable to report the target release version (allowing a leading `v`). If the installer reports a different release because a new release appeared during the run, recheck the live endpoint before accepting it. If PATH still selects an older installation, put the new installation directory first for the session, refresh the shell's command cache, and repeat the path/version checks. Do not overwrite or delete unrelated installations or edit shell startup files automatically. When the client's PATH cannot be changed, select and verify the new binary's absolute path for all subsequent commands and report that the bare `gate-cli` command still needs PATH setup. Report the verified release and executable path; do not claim global PATH is fixed when only the absolute-path invocation works.

---

## 2. Install **gate-skills** (per client)

For the six `gate-cex-*` skills, build the standalone packages using the repository README and install only the selected generated directories. Source directories rely on sibling shared files and must not be copied directly. The source/marketplace examples below apply to other products.

| Client | Typical skills location | Common approach |
|--------|-------------------------|-----------------|
| **Cursor** | `~/.cursor/skills/` | e.g. `npx skills add https://github.com/gate/gate-skills` or copy skill folders from the repo into that directory |
| **Claude Code** | `~/.claude/skills/` | same pattern |
| **Codex** | `~/.codex/skills/` | same pattern |
| **OpenClaw** | e.g. `~/.openclaw/skills/` (default) | e.g. `npx clawhub@latest add https://github.com/gate/gate-skills` or manual copy |

Point users at the [gate-skills](https://github.com/gate/gate-skills) repository and, if they need step-by-step UI flows, the **Skills Installation** section in that repo’s README. Restart the client after copying or installing skills so it reloads the skill list.

**Gate Verify / tx check-in** phrasing in triggers: those features are provided through the **product skills** and **`gate-cli`**-backed flows described in the relevant DEX / wallet skills — not via a separate MCP-install step in this installer.

---

## 3. API keys and errors → `gate-cli config init`

- When **`gate-cli`** returns auth or configuration errors (missing key, invalid secret, 401, etc.), guide the user to run **`gate-cli config init`** interactively. That wizard sets the API key and secret in the CLI config (do not ask users to paste secrets into chat).
- For creating keys in the browser: [Gate API key management](https://www.gate.com/myaccount/profile/api-key/manage).
- Optional: **`gate-cli config set api-key ...`** / **`config set api-secret ...`** if the user prefers non-interactive config (still avoid echoing secrets in chat).
- For a broader check: **`gate-cli doctor`**.

---

## 4. Legacy MCP (optional)

If the user still has old **Gate MCP** entries in IDE configs and wants to move toward CLI-first tooling:

```bash
gate-cli migrate --dry-run
# Then when satisfied:
gate-cli migrate --apply
```

This does **not** replace installing **`gate-cli`** and **gate-skills**; it is optional cleanup.

---

## 5. Supersedes (naming / docs)

This skill is the **gate-cli + skills** one-click story for Cursor, Claude Code, Codex, and OpenClaw. Older “MCP-only” installer documentation may still exist in the same repo for backwards compatibility; prefer **`setup.sh` + skills install + `gate-cli config init`** for new users.
