---
name: gate-exchange-spot-runtime-rules
version: "2026.4.17-2"
updated: "2026-04-17"
description: "Packaged runtime rules for gate-exchange-spot so the published skill bundle contains every mandatory guardrail referenced by SKILL.md."
---

# Gate Spot Runtime Rules

> Packaged runtime rules for `gate-exchange-spot`.
> This file is included in the skill bundle so ClawHub reviewers can audit every mandatory runtime artifact without relying on files outside this directory.

## 1. Session and authentication

- Use **`gate-cli`** on the current host with credentials from **`gate-cli config init`**, env vars, or config profiles — never ask the user to paste API secrets into chat.
- Valid setups typically use `GATE_API_KEY` and `GATE_API_SECRET` (or the configured profile); align with `references/gate-cli.md` §3.
- Minimal permissions for this skill are `Spot:Write` and `Wallet:Read`.
- If `gate-cli` is missing or broken, stop write actions and switch to install / `setup.sh` guidance only.
- If `gate-cli` returns an auth or permission error, stop write actions and guide the user to run **`gate-cli config init`** or repair keys before continuing.

## 2. Command scope

- Use only the `gate-cli` commands documented in `SKILL.md` and `references/gate-cli.md`.
- Before any documented **`gate-cli cex …`** invocation, follow **`references/gate-cli.md` §2.1** (`--help` first → required flags if any → then real run; see example `spot account get` there).
- Do not call undocumented Gate tools, browser flows, or unrelated system tools.
- If the user asks for futures, DEX, or analysis-only work, route to the appropriate skill instead of forcing spot-trading actions through this skill.

## 3. Mandatory Confirmation Gate

- Before any write action, present an order draft first.
- The draft must include pair, side, order type, amount semantics, pricing basis, estimated cost or proceeds, and a risk note.
- Execute a write only after explicit confirmation in the immediately previous user turn.
- Confirmation is single-use. Any parameter change or topic shift invalidates prior confirmation.
- For multi-leg flows, require a fresh confirmation before each leg.

## 4. Failure Handling

- On missing `gate-cli`, failed **`gate-cli config init`** / auth, or invalid order constraints, stay in read-only draft or estimation mode.
- Explain why execution is blocked and what must be fixed.
- Surface technical failures that affect trade safety.

## 5. Persistence and Secrets

- During normal chat turns this skill does not silently change the host; `gate-cli` install is only via the documented [`setup.sh`](../setup.sh) flow when the operator or installer runs it.
- This skill does not store, rotate, export, or paste API secrets in chat.
- If the user wants to change API keys or permissions, direct them to manage keys outside the chat in their normal Gate account settings.

---

## Gate CLI binary resolution (host)

When invoking **`gate-cli`** by name in shell, resolve the executable **in order**:

1. **System / PATH:** If **`command -v gate-cli`** succeeds **and** **`gate-cli --version`** exits successfully, use that binary for all documented **`gate-cli`** commands.

2. **`${HOME}/.local/bin/gate-cli`:** If step 1 fails, **if** this path exists and is executable, **`gate-cli`** refers to **`"${HOME}/.local/bin/gate-cli"`** (use full path when **`PATH`** is unreliable).

3. **`${HOME}/.openclaw/skills/bin/gate-cli`:** If steps 1–2 fail, **if** this path exists and is executable, **`gate-cli`** refers to **`"${HOME}/.openclaw/skills/bin/gate-cli"`**.

Prefer detection in this order; do not assume a single install location.

