---
name: gate-exchange-transfer-runtime-rules
version: "2026.4.3-1"
updated: "2026-04-03"
description: "Packaged runtime rules for gate-exchange-transfer so the published skill bundle contains every mandatory guardrail referenced by SKILL.md."
---

# Gate Internal Transfer Runtime Rules

> Packaged runtime rules for `gate-exchange-transfer`.
> This file is included in the skill bundle so ClawHub reviewers can audit every mandatory runtime artifact without relying on files outside this directory.

## 1. Session and authentication

- Use **`gate-cli`** on the current host with credentials from **`gate-cli config init`**, env vars, or config profiles — never ask the user to paste API secrets into chat.
- Typical configuration uses `GATE_API_KEY` and `GATE_API_SECRET`; align with `references/gate-cli.md`.
- If `gate-cli` is missing or required commands fail, stop write actions and switch to install guidance (`skills/gate-exchange-spot/setup.sh` from the `gate-github-skills` repo root) only.
- If `gate-cli` returns an auth or permission error, stop write actions and guide the user to run **`gate-cli config init`** or repair keys before continuing.


## 2. Tool Scope
- Before any documented **`gate-cli cex …`** invocation, follow **`references/gate-cli.md` §2.1** (`--help` first → required flags if any → then real run; example `spot account get` in that section).

- Use only the `gate-cli` commands documented in `SKILL.md` and `references/gate-cli.md`.
- Do not call undocumented Gate tools, browser flows, or unrelated system tools.
- This skill only handles same-UID internal transfers. Do not use it for withdrawals, third-party transfers, or fiat settlement flows.

## 3. Mandatory Confirmation Gate

- Before any write action, present a transfer draft first.
- The draft must include source account, destination account, asset, amount semantics, estimated post-transfer balances when available, and a risk note.
- Execute a write only after explicit confirmation in the immediately previous user turn.
- Confirmation is single-use. Any parameter change or topic shift invalidates prior confirmation.

## 4. Failure Handling

- On missing `gate-cli` configuration, auth failure, unsupported account routes, or invalid balance constraints, stay in read-only explanation mode.
- Explain why execution is blocked and what must be fixed.
- Surface technical failures that affect fund safety.

## 5. Persistence and Secrets

- This skill does not install software or modify host configuration during normal execution.
- This skill does not store, rotate, export, or paste API secrets in chat.

---

## Gate CLI binary resolution (host)

When invoking **`gate-cli`** by name in shell, resolve the executable **in order**:

1. **System / PATH:** If **`command -v gate-cli`** succeeds **and** **`gate-cli --version`** exits successfully, use that binary for all documented **`gate-cli`** commands.

2. **`${HOME}/.local/bin/gate-cli`:** If step 1 fails, **if** this path exists and is executable, **`gate-cli`** refers to **`"${HOME}/.local/bin/gate-cli"`** (use full path when **`PATH`** is unreliable).

3. **`${HOME}/.openclaw/skills/bin/gate-cli`:** If steps 1–2 fail, **if** this path exists and is executable, **`gate-cli`** refers to **`"${HOME}/.openclaw/skills/bin/gate-cli"`**.

Prefer detection in this order; do not assume a single install location.

