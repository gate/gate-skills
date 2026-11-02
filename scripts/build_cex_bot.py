#!/usr/bin/env python3
"""Build one Bot package with the canonical CEX contract, content checks and manifest."""
import argparse
import json
from pathlib import Path
import tempfile

from cex_skills import build as build_packages


def build(output):
    """Validate in disposable staging; publish once without overwriting or leaving partial output."""
    repo = Path(__file__).resolve().parents[1]
    output = output.absolute()
    if output.name != "gate-cex-bot":
        raise ValueError("output directory must be named gate-cex-bot to match Skill registration")
    if output.exists() or output.is_symlink():
        raise ValueError("output must be a new directory; existing artifacts are never overwritten")
    if output.resolve().is_relative_to(repo / "skills"):
        raise ValueError("build output must be outside the maintained Skill source")
    # Reject redirected source roots before either validator or copier traverses them.
    for relative in ("skills/gate-cex-bot", "skills/_shared/cex"):
        source = repo / relative
        if any(p.is_symlink() for p in (source, *source.parents) if p.is_relative_to(repo)):
            raise ValueError("source symlinks are not permitted")
    contract = json.loads((repo / "tests/cex/cli-contract.json").read_text())
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".bot-build-", dir=output.parent) as folder:
        staging = Path(folder) / "packages"
        build_packages(repo, staging, contract, profiles=("bot",))
        package = staging / "gate-cex-bot"
        manifest = json.loads((package / "manifest.json").read_text())
        # Keep a destination created during validation intact as well as one present at entry.
        if output.exists() or output.is_symlink():
            raise ValueError("output appeared during validation; existing artifacts are never overwritten")
        # Same-filesystem rename publishes only a fully validated artifact; cleanup owns only our staging.
        package.rename(output)
    return manifest


def main():
    """Expose output-only offline packaging; never install a Skill or execute a business command."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = build(args.output)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"package build failed: {error}\n")
    print(json.dumps({"package": str(args.output.absolute()), "files": len(manifest["files"]),
                      "command_contract_sha256": manifest["command_contract_sha256"]}))


if __name__ == "__main__":
    main()
