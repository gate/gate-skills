---
name: gate-exchange-welfare-runtime-rules
version: "2026.4.3-1"
updated: "2026-04-03"
description: "Packaged runtime rules for gate-exchange-welfare so the published skill bundle contains every mandatory guardrail referenced by SKILL.md."
---

# Gate Welfare Runtime Rules

> Packaged runtime rules for `gate-exchange-welfare`.
> This file is included in the skill bundle so ClawHub reviewers can audit every mandatory runtime artifact without relying on files outside this directory.

## 1. MCP Session and Authentication

- Use the already configured Gate MCP session for the current host.
- Local Gate MCP deployments use `GATE_API_KEY` and `GATE_API_SECRET`; never ask the user to paste these secrets into chat.
- Minimal permission for this skill is `Welfare:Read`.
- If the required Gate MCP tools are missing, stop and switch to setup guidance only.
- If the MCP session returns an auth or permission error, stop and guide the user to repair the configured local MCP credentials before continuing.

## 2. Tool Scope

- Use only the MCP tools documented in `SKILL.md` and `references/mcp.md`.
- Do not call undocumented Gate tools, browser flows, or unrelated system tools.
- This skill is read-only. Do not attempt trading, coupon redemption, or other write actions through this skill.

## 3. Failure Handling

- On missing MCP configuration, auth failure, or unsupported welfare filters, explain why the requested query cannot proceed.
- Surface technical failures that affect result accuracy.

## 4. Persistence and Secrets

- This skill does not install software or modify host configuration during normal execution.
- This skill does not store, rotate, export, or paste API secrets in chat.
