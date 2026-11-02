"""Boundary unit/E2E tests use disposable real builder inputs and public CLI."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("builder_boundaries", ROOT / "scripts/cex_skills.py")
TOOLS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOLS)
CONTRACT = json.loads((ROOT / "tests/cex/cli-contract.json").read_text())


class BuildBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="builder-boundary-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "repo"
        shutil.copytree(ROOT / "skills/gate-cex-bot", self.repo / "skills/gate-cex-bot")
        shutil.copytree(ROOT / "skills/_shared/cex", self.repo / "skills/_shared/cex")

    def test_rejects_input_descendants_before_mkdir_or_copy(self):
        """Missing parents, relative paths and symlink aliases must share the same gate."""
        alias = self.base / "alias"
        alias.symlink_to(self.repo / "skills/gate-cex-bot", target_is_directory=True)
        for output in (self.repo / "skills/gate-cex-bot/new-output",
                       self.repo / "skills/_shared/cex/new-parent/out",
                       self.repo / "skills/gate-cex-bot/../gate-cex-earn/out",
                       alias / "new-output"):
            with self.subTest(output=output), mock.patch.object(TOOLS.shutil, "copytree") as copy:
                before = sorted(str(p) for p in self.repo.rglob("*"))
                with self.assertRaisesRegex(ValueError, "outside the maintained"):
                    TOOLS.build(self.repo, output, CONTRACT, profiles=("bot",))
                copy.assert_not_called()
                self.assertEqual(sorted(str(p) for p in self.repo.rglob("*")), before)
                self.assertFalse(output.exists())

    def test_public_six_profile_cli_rejects_nested_output_before_validation(self):
        output = self.repo / "skills/gate-cex-bot/new-output"
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts/cex_skills.py"), "build",
             "--source", str(self.repo), "--contract", str(ROOT / "tests/cex/cli-contract.json"),
             "--output", str(output)], capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("outside the maintained", result.stderr)
        self.assertFalse(output.exists())
        self.assertFalse(list(self.repo.rglob(".cex-build-*")))

    def test_normal_package_existing_destination_and_source_alias(self):
        output = self.base / "packages"
        TOOLS.build(self.repo, output, CONTRACT, profiles=("bot",))
        package = output / "gate-cex-bot"
        self.assertEqual(TOOLS.inspect(package, CONTRACT, package=True)["status"], "PASS")
        before = (package / "manifest.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "already exists"):
            TOOLS.build(self.repo, output, CONTRACT, profiles=("bot",))
        self.assertEqual((package / "manifest.json").read_bytes(), before)
        src = self.repo / "skills/_shared/cex"
        relocated = self.base / "real-shared"
        src.rename(relocated)
        src.symlink_to(relocated, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            TOOLS.build(self.repo, self.base / "rejected", CONTRACT, profiles=("bot",))
        self.assertFalse((self.base / "rejected").exists())


if __name__ == "__main__":
    unittest.main()
