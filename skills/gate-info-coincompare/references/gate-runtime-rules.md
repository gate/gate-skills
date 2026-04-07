---
name: gate-info-coincompare-runtime-rules
version: "2026.4.6-1"
updated: "2026-04-06"
description: "Packaged runtime rules for gate-info-coincompare so every mandatory artifact referenced by SKILL.md is included in the published bundle."
---

# Gate Info Coin Compare Runtime Rules

> Packaged runtime rules for `gate-info-coincompare`.
> This file is bundled with the skill so reviewers can audit the required guardrails without depending on files outside this directory.

## 1. Intent and Scope

- Use this skill only for explicit 2-5 coin comparison requests.
- If the user asks for a single coin, sector overview, contract safety, or another dedicated dimension, route to the matching skill instead of stretching this one.

## 2. Tool Scope

- Use only the MCP tools documented in `SKILL.md`.
- Do not call undocumented tools, browser flows, or unrelated system tools.

## 3. Installation and Fallback

- This skill requires the Gate Info MCP server.
- If the required MCP tools are unavailable, stop and provide setup guidance or graceful partial output as documented in `SKILL.md`.

## 4. Persistence and Secrets

- This skill is read-only.
- This skill does not install software, write local files, or handle API secrets during normal execution.
