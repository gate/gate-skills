---
name: gate-cli-installer
version: "2026.4.22-2"
updated: "2026-04-22"
description: "One-click installer for gate-cli and gate-skills on Cursor, Claude Code, Codex, or OpenClaw/mcporter. Triggers on 'install gate-cli', 'Gate skills', 'Gate Verify', 'tx check-in', 'setup Gate Cursor', 'Gate Claude Code', 'Gate Codex', 'OpenClaw Gate', 'mcporter Gate'."
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

---

## What to install (two parts)

1. **`gate-cli`** — Gate CLI for CEX, info, news, config, and diagnostics. Install using this skill’s **`setup.sh`** (see below).
2. **gate-skills** — Agent skills from [https://github.com/gate/gate-skills](https://github.com/gate/gate-skills). Use your client’s normal skills workflow (`npx skills add …` or copy into the per-client skills directory).

---

## 1. Install `gate-cli` (`setup.sh`)

Script path: **`skills/gate-cli-installer/setup.sh`**

The script downloads the latest **`gate/gate-cli`** release for your OS/arch, verifies checksums, and installs the **`gate-cli`** binary.

```bash
# From the gate-skills (or gate-github-skills) repo root
bash skills/gate-cli-installer/setup.sh
```

```bash
# Optional: pin a release tag
bash skills/gate-cli-installer/setup.sh --version v0.6.0
```

**Make `gate-cli` available on your PATH (system / shell):**

- **`setup.sh`** installs to **`${HOME}/.local/bin/gate-cli`** first. If **`~/.local/bin`** is **not** already on your **`PATH`**, the script prints a reminder to add:  
  `export PATH="$HOME/.local/bin:$PATH"`  
  Put that in `~/.zshrc`, `~/.bashrc`, or your shell profile, then restart the terminal or **`source`** the file.
- If **`~/.local/bin`** cannot be written, the script falls back to **`/usr/local/bin`** (typically already on **`PATH`** on macOS/Linux).
- Older installs may leave **`${HOME}/.openclaw/skills/bin/gate-cli`**; agents must still resolve **`gate-cli`** using **Which \`gate-cli\` runs** above — do not assume only one directory.

**Verify**

```bash
command -v gate-cli
gate-cli --version
```

---

## 2. Install **gate-skills** (per client)

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
