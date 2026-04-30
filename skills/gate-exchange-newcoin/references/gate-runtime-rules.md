---
name: gate-exchange-newcoin-runtime-rules
version: "2026.4.29-1"
updated: "2026-04-29"
description: "Packaged runtime rules for gate-exchange-newcoin so the published skill bundle contains mandatory guardrails referenced by SKILL.md."
---

# New Coin Radar Runtime Rules

> Packaged runtime rules for `gate-exchange-newcoin`.
> This file is included in the skill bundle so reviewers can audit runtime artifacts without relying on files outside this directory.

## 1. Session and authentication

- Use **`gate-cli`** on the current host with credentials from **`gate-cli config init`**, env vars, or config profiles — never ask the user to paste API secrets into chat.
- Valid setups typically use **`GATE_API_KEY`** and **`GATE_API_SECRET`** (or the configured profile); align with `references/gate-cli.md` §3.
- **Read-heavy flows** (`info`, `news`) generally do not need trading keys; **writes** (`cex spot order`, `cex alpha order place`) require appropriately scoped API permissions.
- If `gate-cli` is missing or broken, stop write actions and switch to install / [`setup.sh`](../setup.sh) guidance only.
- If `gate-cli` returns an auth or permission error on writes, stop writes and guide the user to repair keys or permissions before continuing.

## 2. Command scope

- Use only the `gate-cli` commands documented in `SKILL.md` and `references/gate-cli.md`.
- Before any documented **`gate-cli cex …`** invocation, follow **`references/gate-cli.md` §1** (`--help` first when unsure).
- Do not call undocumented Gate tools, browser flows, or unrelated system tools.
- If the user asks for unrelated products (DEX-only, futures-only), route to the appropriate skill instead of stretching this skill.

## 3. Mandatory confirmation gate (writes)

- Before **any** spot or Alpha order placement, present an **Action Draft** first.
- Execute a write only after explicit **`Y`** (or equivalent clear confirmation) in the immediately previous user turn **for that draft**.
- Confirmation is single-use. Any parameter change or topic shift invalidates prior confirmation.

## 4. Failure handling

- On missing `gate-cli`, failed auth setup, or invalid constraints, stay in read-only or draft mode.
- Explain why execution is blocked and what must be fixed.
- Surface technical failures that affect trade safety.

## 5. Persistence and secrets

- Normal turns do not silently change the host; `gate-cli` install is via documented [`setup.sh`](../setup.sh) when the operator runs it.
- This skill does not store, rotate, export, or paste API secrets in chat.

---

## Gate CLI binary resolution (host)

When invoking **`gate-cli`** by name in shell, resolve the executable **in order**:

1. **System / PATH:** If **`command -v gate-cli`** succeeds **and** **`gate-cli --version`** exits successfully, use that binary.

2. **`${HOME}/.local/bin/gate-cli`:** If step 1 fails and this path is executable, use it.

3. **`${HOME}/.openclaw/skills/bin/gate-cli`:** If steps 1–2 fail and this path is executable, use it.

Prefer detection in this order; do not assume a single install location.
