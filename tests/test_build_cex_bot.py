"""Exercise the standalone package builder through its command-line interface."""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class StandaloneBotPackageTests(unittest.TestCase):
    """Use disposable source checkouts so rejection tests cannot alter maintained rules."""

    def repository(self):
        """Copy only builder inputs into a fresh fixture with no credentials or Git state."""
        temporary = tempfile.TemporaryDirectory(prefix="cex-bot-package-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        repo = root / "repo"
        original = Path(__file__).resolve().parents[1]
        (repo / "scripts").mkdir(parents=True)
        for name in ("build_cex_bot.py", "cex_skills.py"):
            shutil.copyfile(original / "scripts" / name, repo / "scripts" / name)
        (repo / "tests/cex").mkdir(parents=True)
        shutil.copyfile(original / "tests/cex/cli-contract.json", repo / "tests/cex/cli-contract.json")
        for relative in ("skills/gate-cex-bot", "skills/_shared/cex"):
            shutil.copytree(original / relative, repo / relative)
        return root, repo

    def run_builder(self, repo, output):
        """Run the public CLI with a bounded lifetime and capture its artifact/error contract."""
        return subprocess.run(
            [sys.executable, str(repo / "scripts/build_cex_bot.py"), "--output", str(output)],
            cwd=repo, capture_output=True, text=True, timeout=20,
        )

    def test_rejects_symlinked_source_roots_and_parents(self):
        """An approved-looking directory path must not import rules through a symlink."""
        for relative in ("skills/gate-cex-bot", "skills/_shared/cex", "skills/_shared", "skills"):
            with self.subTest(source=relative):
                root, repo = self.repository()
                source = repo / relative
                relocated = root / "outside-source"
                source.rename(relocated)
                source.symlink_to(relocated, target_is_directory=True)
                output = root / "gate-cex-bot"

                result = self.run_builder(repo, output)

                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("symlink", result.stderr.lower())
                self.assertFalse(output.exists(), "rejected source must not produce an installed package")

    def test_package_is_reproducible_and_independent_of_source_checkout(self):
        """Two builds have identical content and retain all six rules after checkout removal."""
        root, repo = self.repository()
        first, second = root / "first/gate-cex-bot", root / "second/gate-cex-bot"
        for output in (first, second):
            result = self.run_builder(repo, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertGreaterEqual(json.loads(result.stdout)["files"], 22)

        manifest = json.loads((first / "manifest.json").read_text())
        self.assertEqual((first / "manifest.json").read_bytes(), (second / "manifest.json").read_bytes())
        self.assertIn("command_contract_sha256", manifest)
        self.assertNotIn("cli_baseline", manifest)
        self.assertNotIn("cli_commit", manifest)
        self.assertGreaterEqual(len(manifest["files"]), 22)
        shutil.rmtree(repo)

        for relative, digest in manifest["files"].items():
            with self.subTest(installed_file=relative):
                self.assertEqual(hashlib.sha256((first / relative).read_bytes()).hexdigest(), digest)
                self.assertEqual((first / relative).read_bytes(), (second / relative).read_bytes())
        for name in ("preflight.md", "cli-setup.md", "cli-auth.md", "execution-cli.md", "safety.md", "templates.md"):
            self.assertTrue((first / "references/_shared/cex" / name).is_file(), name)
        self.assertIn("(references/_shared/cex/preflight.md)", (first / "SKILL.md").read_text())

    def test_existing_artifact_is_not_overwritten(self):
        """A repeated destination fails without replacing the user's existing files."""
        root, repo = self.repository()
        output = root / "gate-cex-bot"
        output.mkdir()
        sentinel = output / "keep.txt"
        sentinel.write_text("existing review artifact\n")

        result = self.run_builder(repo, output)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(sentinel.read_text(), "existing review artifact\n")
        self.assertEqual(sorted(p.name for p in output.iterdir()), ["keep.txt"])

    def test_missing_common_rule_cannot_produce_a_package(self):
        """Each required common rule must be local before any installable output exists."""
        for name in ("preflight.md", "cli-setup.md", "cli-auth.md", "execution-cli.md", "safety.md", "templates.md"):
            with self.subTest(missing=name):
                root, repo = self.repository()
                (repo / "skills/_shared/cex" / name).unlink()
                output = root / "gate-cex-bot"

                result = self.run_builder(repo, output)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(name, result.stderr)
                self.assertFalse(output.exists())

    def test_baseline_models_are_bundled_and_checked(self):
        """A real source build must retain the four baseline model contracts and their links."""
        root, repo = self.repository()
        output = root / "gate-cex-bot"
        result = self.run_builder(repo, output)
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ("spot-grid.md", "futures-grid.md", "martingale.md", "bot-lifecycle.md"):
            self.assertEqual((output / "references/models" / name).read_bytes(),
                             (repo / "skills/gate-cex-bot/references/models" / name).read_bytes())

    def test_public_content_failures_leave_no_partial_installation(self):
        """Private URLs, personal paths, branch provenance and broken links cannot publish a package."""
        for pollution in (
            "https://dev.example.invalid/private-route",
            "/Users/fixture-operator/private-checkout",
            "feature/req-synthetic-only",
            "CLI commit: `0123456789abcdef0123456789abcdef01234567`",
            'api_key = "fixture-only-not-a-real-credential"',
            "[missing dependency](does-not-exist.md)",
            "[missing anchor](models/spot-grid.md#missing-model)",
        ):
            with self.subTest(pollution=pollution):
                root, repo = self.repository()
                reference = repo / "skills/gate-cex-bot/references/compatibility.md"
                reference.write_text(reference.read_text() + "\n" + pollution + "\n")
                output = root / "gate-cex-bot"
                result = self.run_builder(repo, output)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertFalse(output.exists(), "failure left an install-looking directory")
                self.assertFalse(list(root.glob(".bot-build-*")))
                self.assertFalse(list(root.glob(".cex-build-*")))

    def test_wrong_installation_name_is_rejected(self):
        """A successful artifact must keep the registered skill-directory identity."""
        root, repo = self.repository()
        output = root / "wrong-name"
        result = self.run_builder(repo, output)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())

    def test_json_cannot_hide_private_sources(self):
        """Decoded attachments use the same public-content scan as Markdown."""
        root, repo = self.repository()
        (repo / "skills/gate-cex-bot/references/extra.json").write_text(
            '{"url":"https://dev.example.invalid/private-route"}'.replace("example", r"example"))
        output = root / "gate-cex-bot"
        result = self.run_builder(repo, output)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
