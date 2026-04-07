---
name: gate-exchange-spot-runtime-rules
version: "2026.4.3-1"
updated: "2026-04-03"
description: "Packaged runtime rules for gate-exchange-spot so the published skill bundle contains every mandatory guardrail referenced by SKILL.md."
---

# Gate Spot Runtime Rules

> Packaged runtime rules for `gate-exchange-spot`.
> This file is included in the skill bundle so ClawHub reviewers can audit every mandatory runtime artifact without relying on files outside this directory.

## 1. MCP Session and Authentication

- Use the already configured Gate MCP session for the current host.
- Local Gate MCP deployments use `GATE_API_KEY` and `GATE_API_SECRET`; never ask the user to paste these secrets into chat.
- Minimal permissions for this skill are `Spot:Write` and `Wallet:Read`.
- If the required Gate MCP tools are missing, stop write actions and switch to setup guidance only.
- If the MCP session returns an auth or permission error, stop write actions and guide the user to repair the configured local MCP credentials before continuing.

## 2. Tool Scope

- Use only the MCP tools documented in `SKILL.md` and `references/mcp.md`.
- Do not call undocumented Gate tools, browser flows, or unrelated system tools.
- If the user asks for futures, DEX, or analysis-only work, route to the appropriate skill instead of forcing spot-trading actions through this skill.

## 3. Mandatory Confirmation Gate

- Before any write action, present an order draft first.
- The draft must include pair, side, order type, amount semantics, pricing basis, estimated cost or proceeds, and a risk note.
- Execute a write only after explicit confirmation in the immediately previous user turn.
- Confirmation is single-use. Any parameter change or topic shift invalidates prior confirmation.
- For multi-leg flows, require a fresh confirmation before each leg.

## 4. Failure Handling

- On missing MCP configuration, auth failure, or invalid order constraints, stay in read-only draft or estimation mode.
- Explain why execution is blocked and what must be fixed.
- Surface technical failures that affect trade safety.

## 5. Persistence and Secrets

- This skill does not install software or modify host configuration during normal execution.
- This skill does not store, rotate, export, or paste API secrets in chat.
- If the user wants to change API keys or permissions, direct them to manage keys outside the chat in their normal Gate account settings.
