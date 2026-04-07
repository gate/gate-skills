---
name: gate-exchange-dual-runtime-rules
version: "2026.4.3-1"
updated: "2026-04-03"
description: "Packaged runtime rules for gate-exchange-dual so the published skill bundle contains every mandatory guardrail referenced by SKILL.md."
---

# Gate Dual Investment Runtime Rules

> Packaged runtime rules for `gate-exchange-dual`.
> This file is included in the skill bundle so ClawHub reviewers can audit every mandatory runtime artifact without relying on files outside this directory.

## 1. MCP Session and Authentication

- Use the already configured Gate MCP session for the current host.
- Local Gate MCP deployments use `GATE_API_KEY` and `GATE_API_SECRET`; never ask the user to paste these secrets into chat.
- Minimal permission for this skill is `Earn:Write`.
- If the required Gate MCP tools are missing, stop write actions and switch to setup guidance only.
- If the MCP session returns an auth or permission error, stop write actions and guide the user to repair the configured local MCP credentials before continuing.

## 2. Tool Scope

- Use only the MCP tools documented in `SKILL.md` and `references/mcp.md`.
- Do not call undocumented Gate tools, browser flows, or unrelated system tools.
- If the user asks for spot, futures, or unrelated account operations, route to the appropriate skill instead of forcing dual-investment actions here.

## 3. Mandatory Confirmation Gate

- Before any write action, present a subscription draft first.
- The draft must include settlement currency, product direction, APR or yield context when available, lock period, expected settlement condition, and a risk note.
- Execute a write only after explicit confirmation in the immediately previous user turn.
- Confirmation is single-use. Any parameter change or topic shift invalidates prior confirmation.

## 4. Failure Handling

- On missing MCP configuration, auth failure, or invalid subscription constraints, stay in read-only explanation or estimation mode.
- Explain why execution is blocked and what must be fixed.
- Surface technical failures that affect product safety.

## 5. Persistence and Secrets

- This skill does not install software or modify host configuration during normal execution.
- This skill does not store, rotate, export, or paste API secrets in chat.
