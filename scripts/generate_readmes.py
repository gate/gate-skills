#!/usr/bin/env python3
"""Generate README.md and README_zh.md from skills/*/SKILL.md frontmatter + selected full bodies."""
from __future__ import annotations

import os
import re
import sys

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")

FULL_BODY_DIRS = frozenset({"gate-mcp-installer", "gate-exchange-pay"})

GATE_SKILLS_OPENCLAW = (
    "https://github.com/gate/gate-skills/tree/master/skills/gate-mcp-openclaw-installer"
)


def parse_frontmatter_block(raw: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.DOTALL)
    if not m:
        return {}, raw
    fm = yaml.safe_load(m.group(1)) or {}
    body = raw[m.end() :]
    return fm, body


def parse_skill(path: str, dirname: str) -> dict:
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    fm, _ = parse_frontmatter_block(raw)
    desc = (fm.get("description") or "").strip()
    desc_zh = (fm.get("description_zh") or "").strip()
    if not desc_zh and desc:
        desc_zh = desc
    version = str(fm.get("version") or "").strip() or "—"
    status = str(fm.get("status") or "").strip() or "✅ Active"
    name = (fm.get("name") or dirname).strip()
    return {
        "dir": dirname,
        "name": name,
        "description": desc,
        "description_zh": desc_zh,
        "version": version,
        "status": status,
    }


def body_after_frontmatter(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    _, body = parse_frontmatter_block(raw)
    return body.lstrip("\n")


def escape_table_cell(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def brandify(s: str) -> str:
    s = s.replace("Gate.IO", "Gate.com")
    s = s.replace("gate.io", "gate.com")
    return s


def collect_rows() -> list[dict]:
    rows = []
    for name in sorted(os.listdir(SKILLS)):
        p = os.path.join(SKILLS, name, "SKILL.md")
        if os.path.isfile(p):
            rows.append(parse_skill(p, name))
    return rows


def build_readme_en(rows: list[dict]) -> str:
    lines: list[str] = []
    lines.append("# Gate Skills")
    lines.append("")
    lines.append("**[中文](README_zh.md)** | English")
    lines.append("")
    lines.append(
        "Gate Skills is an open marketplace of AI Agent skills that connect natively to "
        "Gate's crypto ecosystem. From market analytics and derivatives monitoring to "
        "one-click MCP configuration—accomplish it all through natural language."
    )
    lines.append("")
    lines.append("Built by Gate for the crypto community.")
    lines.append("")
    lines.append("### One-click install")
    lines.append("")
    lines.append("Use our installer skills to configure in seconds:")
    lines.append("")
    lines.append(
        "- **Unified installer**: [`gate-mcp-installer`](./skills/gate-mcp-installer/) — "
        "Cursor, Claude Code, Codex, and OpenClaw/mcporter in one skill. "
        'Triggers include "install Gate MCP", "setup Gate skills".'
    )
    lines.append(
        f"- **OpenClaw installer**: [`gate-mcp-openclaw-installer`]({GATE_SKILLS_OPENCLAW}) — "
        "maintained in the [`gate-skills`](https://github.com/gate/gate-skills) repository "
        "(not shipped in this repo). Use for OpenClaw-focused MCP + skills setup."
    )
    lines.append("")
    lines.append("**Quick start**: tell your assistant:")
    lines.append("")
    lines.append(
        "> **\"Help me install Gate skills and MCP from https://github.com/gate/gate-github-skills\"**"
    )
    lines.append("")
    lines.append("Or run the installer workflow documented in `gate-mcp-installer`.")
    lines.append("")
    lines.append("### Framework compatibility")
    lines.append("")
    lines.append(
        "These skills are designed to work across AI Agent frameworks—Cursor, OpenClaw, "
        "or custom stacks—with minimal configuration."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Skills overview")
    lines.append("")
    lines.append(
        "| Skill | Description | 描述 (ZH) | Version | Status |"
    )
    lines.append("|-------|-------------|-----------|---------|--------|")
    for r in rows:
        d = r["dir"]
        link = f"[{d}](./skills/{d}/)"
        lines.append(
            "| "
            + " | ".join(
                [
                    link,
                    escape_table_cell(r["description"]),
                    escape_table_cell(r["description_zh"]),
                    escape_table_cell(r["version"]),
                    escape_table_cell(r["status"]),
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append(f"*Total: {len(rows)} skills (each `skills/<name>/SKILL.md`).*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Skill details")
    lines.append("")
    for r in rows:
        d = r["dir"]
        lines.append(f"## {d}")
        lines.append("")
        path = os.path.join(SKILLS, d, "SKILL.md")
        if d in FULL_BODY_DIRS:
            body = body_after_frontmatter(path)
            lines.append(body.rstrip())
        else:
            lines.append(r["description"])
        lines.append("")
    text = "\n".join(lines)
    return brandify(text)


def build_readme_zh(rows: list[dict]) -> str:
    lines: list[str] = []
    lines.append("# Gate Skills")
    lines.append("")
    lines.append("[English](README.md) | **中文**")
    lines.append("")
    lines.append(
        "Gate Skills 是一个开放的技能市场，让 AI Agent 能够原生接入 Gate 的加密生态。"
        "从市场分析、衍生品监控到一键 MCP 配置，全部可通过自然语言完成。"
    )
    lines.append("")
    lines.append("由 Gate 构建，为加密社区而生。")
    lines.append("")
    lines.append("### 一键安装")
    lines.append("")
    lines.append("使用安装器 skill，快速完成配置：")
    lines.append("")
    lines.append(
        "- **统一安装器**：[`gate-mcp-installer`](./skills/gate-mcp-installer/) — "
        "覆盖 Cursor、Claude Code、Codex、OpenClaw/mcporter。触发语示例：「安装 Gate MCP」「配置 Gate skills」。"
    )
    lines.append(
        f"- **OpenClaw 安装器**：[`gate-mcp-openclaw-installer`]({GATE_SKILLS_OPENCLAW}) — "
        "位于 [`gate-skills`](https://github.com/gate/gate-skills) 仓库（本仓库不包含该目录）。"
    )
    lines.append("")
    lines.append("**快速开始**：对 AI 助手说：")
    lines.append("")
    lines.append(
        "> **「帮我从 https://github.com/gate/gate-github-skills 安装 Gate Skills 和 MCP」**"
    )
    lines.append("")
    lines.append("或按 `gate-mcp-installer` 文档执行安装流程。")
    lines.append("")
    lines.append("### 框架兼容性")
    lines.append("")
    lines.append(
        "这些 skills 可与多种 AI Agent 框架配合使用：Cursor、OpenClaw 或自研 Agent 栈，仅需少量配置。"
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Skills 总览")
    lines.append("")
    lines.append("| 技能 | 英文描述 | 中文描述 | 版本 | 状态 |")
    lines.append("|------|----------|----------|------|------|")
    for r in rows:
        d = r["dir"]
        link = f"[{d}](./skills/{d}/)"
        lines.append(
            "| "
            + " | ".join(
                [
                    link,
                    escape_table_cell(r["description"]),
                    escape_table_cell(r["description_zh"]),
                    escape_table_cell(r["version"]),
                    escape_table_cell(r["status"]),
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append(f"*共 {len(rows)} 个技能（对应 `skills/<名称>/SKILL.md`）。*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 技能详情")
    lines.append("")
    for r in rows:
        d = r["dir"]
        lines.append(f"## {d}")
        lines.append("")
        path = os.path.join(SKILLS, d, "SKILL.md")
        if d in FULL_BODY_DIRS:
            body = body_after_frontmatter(path)
            lines.append(body.rstrip())
        else:
            lines.append(r["description_zh"])
        lines.append("")
    text = "\n".join(lines)
    return brandify(text)


def main() -> None:
    rows = collect_rows()
    en_path = os.path.join(ROOT, "README.md")
    zh_path = os.path.join(ROOT, "README_zh.md")
    with open(en_path, "w", encoding="utf-8") as f:
        f.write(build_readme_en(rows))
    with open(zh_path, "w", encoding="utf-8") as f:
        f.write(build_readme_zh(rows))
    print(f"Wrote {en_path} and {zh_path} ({len(rows)} skills).")


if __name__ == "__main__":
    main()
