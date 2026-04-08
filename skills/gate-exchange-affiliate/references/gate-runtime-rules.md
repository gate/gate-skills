---
name: gate-exchange-affiliate-runtime-rules
version: "2026.4.8-1"
updated: "2026-04-08"
description: "Packaged runtime rules for gate-exchange-affiliate so the published skill bundle contains every mandatory guardrail referenced by SKILL.md."
---

# Gate Exchange Affiliate Runtime Rules

> Packaged runtime rules for `gate-exchange-affiliate`.
> This file is included in the skill bundle so ClawHub reviewers can audit every mandatory runtime artifact without relying on files outside this directory.

## 1. MCP Session and Authentication

- Use the already configured Gate MCP session for the current host.
- Local Gate MCP deployments use `GATE_API_KEY` and `GATE_API_SECRET`; never ask the user to paste these secrets into chat.
- Minimal permission for this skill is `Rebate:Read`.
- If the required Gate rebate tools are missing, stop and switch to setup guidance only.
- If the MCP session returns an auth or permission error, stop and guide the user to repair the configured local MCP credentials before continuing.

## 2. Tool Scope

- Use only the MCP tools documented in `SKILL.md` and `references/mcp.md`.
- Do not call undocumented Gate tools, browser flows, or unrelated system tools.
- This skill only handles partner-affiliate read flows. Do not use it for writes, account changes, or agency-only operations.

## 3. Read-only Safety

- This skill is read-only.
- Query only the authenticated partner's data.
- Do not infer results beyond the returned partner records.

## 4. Failure Handling

- On missing MCP configuration, auth failure, permission failure, or unsupported partner context, stay in read-only explanation mode.
- Explain why execution is blocked and what must be fixed.

## 5. Persistence and Secrets

- This skill does not install software or modify host configuration during normal execution.
- This skill does not store, rotate, export, or paste API secrets in chat.
