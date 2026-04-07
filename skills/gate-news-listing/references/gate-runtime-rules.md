---
name: gate-news-listing-runtime-rules
version: "2026.4.6-1"
updated: "2026-04-06"
description: "Packaged runtime rules for gate-news-listing so every mandatory artifact referenced by SKILL.md is included in the published bundle."
---

# Gate News Listing Runtime Rules

> Packaged runtime rules for `gate-news-listing`.
> This file is bundled with the skill so reviewers can audit the required guardrails without depending on files outside this directory.

## 1. Intent and Scope

- Use this skill only for exchange listing, delisting, and maintenance announcements.
- If the user asks for deeper coin analysis or contract risk checks, route to the matching skill after handling the announcement scope.

## 2. Tool Scope

- Use only the MCP tools documented in `SKILL.md` and `references/mcp.md`.
- Do not call undocumented tools, browser flows, or unrelated system tools.

## 3. Installation and Fallback

- This skill requires Gate News and may supplement with documented Gate Info read-only tools.
- If the required announcement tool is unavailable, stop and provide setup guidance or graceful partial output as documented in `SKILL.md`.

## 4. Persistence and Secrets

- This skill is read-only.
- This skill does not install software, write local files, or handle API secrets during normal execution.
