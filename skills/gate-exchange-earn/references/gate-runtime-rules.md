---
name: gate-exchange-earn-runtime-rules
version: "2026.4.28-1"
updated: "2026-04-28"
description: "Packaged runtime rules for gate-exchange-earn so the published skill bundle contains mandatory guardrails referenced by SKILL.md."
---

# Gate Earn runtime rules

> Packaged runtime rules for `gate-exchange-earn`.
> This file is included in the skill bundle so reviewers can audit runtime artifacts without relying on files outside this directory.

## 1. Session and authentication

- Use **`gate-cli`** on the current host with credentials from **`gate-cli config init`**, environment variables, or profiles. Never ask the user to paste API secrets into chat.
- Typical env vars: **`GATE_API_KEY`** and **`GATE_API_SECRET`**. Align with `references/gate-cli.md` §3.
- Use a key with at least earn-related access for reads/writes used here, plus spot **read** when checking balances before subscriptions.
- If `gate-cli` is missing or broken, stop write actions and switch to install / `setup.sh` guidance only.
- If `gate-cli` returns auth or permission errors, stop writes and guide the user to repair keys before continuing.

## 2. Command scope

- Use only the `gate-cli` commands documented in `SKILL.md` and `references/gate-cli.md`.
- Before any documented **`gate-cli cex …`** invocation, follow **`references/gate-cli.md` §2.1** (`--help` first, then required flags, then real run).
- Do not call undocumented tools, unrelated exchange namespaces, or browser automation for these workflows.
- If the user asks for unrelated trading or research, route to the appropriate skill instead of stretching earn commands.

## 3. Mandatory confirmation gate (writes)

- Before any earn **write**, present an **Action Draft** first.
- The draft must include product type, currency, amount (or full redeem flag if applicable), indicative APR or term, and material risks (including dual settlement/exercise narrative when relevant).
- Execute a write only after explicit **Y** in the immediately previous user turn.
- Confirmation is single-use. Any parameter or intent change invalidates prior confirmation.
- For chained writes (for example redeem then subscribe), require **separate** confirmation per write leg.

## 4. Failure handling

- On missing `gate-cli`, failed configuration, or insufficient balance, stay in read-only or draft mode.
- Explain why execution is blocked and what must be fixed.
- Surface technical failures that affect safety; do not fabricate balances or yields.

## 5. Persistence and secrets

- Install `gate-cli` only via the documented `setup.sh` flow when the operator runs it.
- This skill does not store, rotate, export, or paste API secrets in chat.
- Direct users to the Gate account API key page to create or rotate keys outside the chat.

## 6. Gate CLI binary resolution (host)

When invoking **`gate-cli`** by name in shell, resolve the executable **in order**:

1. **System / PATH:** If **`command -v gate-cli`** succeeds and **`gate-cli --version`** works, use that binary.
2. **`${HOME}/.local/bin/gate-cli`:** If step 1 fails and this path is executable, use it.
3. **`${HOME}/.openclaw/skills/bin/gate-cli`:** If steps 1–2 fail and this path is executable, use it.

Prefer detection in this order; do not assume a single install location.
