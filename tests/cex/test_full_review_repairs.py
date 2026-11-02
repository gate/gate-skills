"""Prevent the reviewed Spot prose conflict in both source and installed artifacts."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("cex_prose", ROOT / "scripts/cex_skills.py")
TOOLS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOLS)
CONTRACT = json.loads((ROOT / "tests/cex/cli-contract.json").read_text())
BT = chr(96)
OLD = (f"Simple {BT}spot.order.buy{BT}/sell expose no {BT}--account{BT}, auto-borrow or auto-repay flags.",
       "Ordinary get/list/cancel leaves also lack an account-selection flag.")


class SpotProseRegressionTests(unittest.TestCase):
    def test_source_and_package_cli_reject_old_denials_but_keep_installed_build_gate(self):
        """Exercise real build/check; only temporary documentation is mutated."""
        with tempfile.TemporaryDirectory(prefix="spot-prose-") as directory:
            base = Path(directory)
            repo = base / "source"
            target = repo / "skills/gate-cex-trade"
            shutil.copytree(ROOT / "skills/gate-cex-trade", target)
            shutil.copytree(ROOT / "skills/_shared/cex", repo / "skills/_shared/cex")
            output = base / "packages"
            TOOLS.build(repo, output, CONTRACT, profiles=("trade",))
            for selected, package in ((target, False), (output / "gate-cex-trade", True)):
                file = selected / "references/spot-commands.md"
                good = file.read_text()
                self.assertIn("Older builds may omit", good)
                self.assertIn('<a id="spot-account-selection">', good)
                for denial in OLD:
                    file.write_text(good + "\n" + denial + "\n")
                    argv = [sys.executable, "-B", str(ROOT / "scripts/cex_skills.py"), "check",
                            "--target", str(selected), "--contract", str(ROOT / "tests/cex/cli-contract.json")]
                    if package:
                        argv.append("--package")
                    result = subprocess.run(argv, capture_output=True, text=True, timeout=20)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertTrue(any(f["rule"] == "C5" for f in json.loads(result.stdout)["findings"]))
                file.write_text(good)
                self.assertEqual(TOOLS.inspect(selected, CONTRACT, package=package)["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
