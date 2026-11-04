"""Offline Git/mcporter boundary for the real installer subprocess tests."""

import json
import os
from pathlib import Path
import shutil
import sys


def main():
    """Never execute package managers, network requests or business MCP calls."""
    mode, *arguments = sys.argv[1:]
    events = Path(os.environ["INSTALL_TEST_EVENTS"])
    with events.open("a") as stream:
        stream.write(json.dumps({"command": mode, "arguments": arguments}) + "\n")
    if mode == "git":
        if arguments[:1] != ["clone"] or os.environ.get("INSTALL_TEST_CLONE_FAIL") == "1":
            return 1
        shutil.copytree(os.environ["INSTALL_TEST_SOURCE"], arguments[-1], dirs_exist_ok=True)
        return 0
    if mode == "mcporter":
        registry_path = Path(os.environ["INSTALL_TEST_REGISTRY"])
        registry = json.loads(registry_path.read_text())
        if arguments[:2] == ["config", "list"]:
            print("\n".join(registry))
            return 0
        if arguments[:2] == ["config", "add"]:
            registry[arguments[2]] = arguments[3:]
            registry_path.write_text(json.dumps(registry))
            return 0
        if arguments[:1] == ["list"]:
            return 0
    if mode in {"claude", "codex"}:
        # Mock only vendor registration; routing and fallback files remain real.
        endpoints = {
            "gate-dex": "https://api.gatemcp.ai/mcp/dex",
            "gate-dex-sec": "https://api.gatemcp.ai/mcp/dex/sec",
        }
        for name, url in endpoints.items():
            expected = (["mcp", "add", "--transport", "http", name, "--scope", "project", url]
                        if mode == "claude" else
                        ["mcp", "add", name, "--transport", "http", "--url", url])
            if arguments == expected:
                failed = os.environ.get("INSTALL_TEST_FAIL_CLIENT") in {mode, "all"}
                failed = failed or os.environ.get("INSTALL_TEST_FAIL_SERVER") == name
                return 1 if failed else 0
    # Availability checks may find npx/gate-mcp, but the installer must not execute them.
    return 99


if __name__ == "__main__":
    raise SystemExit(main())
