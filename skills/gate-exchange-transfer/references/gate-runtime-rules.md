---
name: gate-exchange-transfer-runtime-rules
version: "2026.4.3-1"
updated: "2026-04-03"
description: "Packaged runtime rules for gate-exchange-transfer so the published skill bundle contains every mandatory guardrail referenced by SKILL.md."
---

# Gate Internal Transfer Runtime Rules

> Packaged runtime rules for `gate-exchange-transfer`.
> This file is included in the skill bundle so ClawHub reviewers can audit every mandatory runtime artifact without relying on files outside this directory.

## 1. MCP Session and Authentication

- Use the already configured Gate MCP session for the current host.
- Local Gate MCP deployments use `GATE_API_KEY` and `GATE_API_SECRET`; never ask the user to paste these secrets into chat.
- Minimal permissions for this skill are `Wallet:Write`, `Spot:Read`, `Margin:Read`, `Fx:Read`, `Delivery:Read`, and `Options:Read`.
- If the required Gate MCP tools are missing, stop write actions and switch to setup guidance only.
- If the MCP session returns an auth or permission error, stop write actions and guide the user to repair the configured local MCP credentials before continuing.

## 2. Tool Scope

- Use only the MCP tools documented in `SKILL.md` and `references/mcp.md`.
- Do not call undocumented Gate tools, browser flows, or unrelated system tools.
- This skill only handles same-UID internal transfers. Do not use it for withdrawals, third-party transfers, or fiat settlement flows.

## 3. Mandatory Confirmation Gate

- Before any write action, present a transfer draft first.
- The draft must include source account, destination account, asset, amount semantics, estimated post-transfer balances when available, and a risk note.
- Execute a write only after explicit confirmation in the immediately previous user turn.
- Confirmation is single-use. Any parameter change or topic shift invalidates prior confirmation.

## 4. Failure Handling

- On missing MCP configuration, auth failure, unsupported account routes, or invalid balance constraints, stay in read-only explanation mode.
- Explain why execution is blocked and what must be fixed.
- Surface technical failures that affect fund safety.

## 5. Persistence and Secrets

- This skill does not install software or modify host configuration during normal execution.
- This skill does not store, rotate, export, or paste API secrets in chat.
