#!/usr/bin/env python3
"""Extract SKILL.md frontmatter for README generation. Run from repo root."""
from __future__ import annotations

import json
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


def parse_skill(path: str, dirname: str) -> dict:
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.DOTALL)
    fm: dict = {}
    if m:
        fm = yaml.safe_load(m.group(1)) or {}
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


def main() -> None:
    rows = []
    for name in sorted(os.listdir(SKILLS)):
        p = os.path.join(SKILLS, name, "SKILL.md")
        if os.path.isfile(p):
            rows.append(parse_skill(p, name))
    print(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
