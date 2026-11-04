"""DEX usage-only contracts and offline wallet-installer regressions.

Only client registration is synthetic. Real Bash functions and the full installer
generate routing/configuration in disposable child homes. Package managers and
wallet commands are guarded mocks; the parent environment remains untouched.
"""

import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import tomllib
from types import SimpleNamespace
import unittest

from test_skill_content import HELPERS, local_link_errors


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "skills/gate-dex-wallet/install.sh"
PEER = ROOT / "tests/fixtures/installer_host.py"
ROUTING = {"claude": "CLAUDE.md", "codex": "AGENTS.md"}
ENDPOINTS = {"https://api.gatemcp.ai/mcp/dex", "https://api.gatemcp.ai/mcp/dex/sec"}


class DexCliUsageContentTests(unittest.TestCase):
    """Keep runtime guidance available without restoring retired installers."""

    def test_cli_packages_have_no_download_metadata_or_setup_entry(self):
        for domain in ("market", "trade", "wallet"):
            with self.subTest(domain=domain):
                package = ROOT / "skills" / f"gate-dex-{domain}-cli"
                body = (package / "SKILL.md").read_text()
                metadata = HELPERS.header(body)
                self.assertEqual(metadata["name"], package.name)
                self.assertNotIn("install", metadata.get("metadata", {}).get("openclaw", {}))
                self.assertFalse((package / "setup.sh").exists())
                # Each package README owns the executable prerequisite; runtime routes remain in SKILL.md.
                self.assertRegex((package / "README.md").read_text(), r"`gate-dex`.*`PATH`")
                for name in ("SKILL.md", "README.md"):
                    self.assertEqual(local_link_errors(package / name), [])
                    self.assertNotIn("gate-dex-cli.gateweb3.cc", (package / name).read_text())

    def test_wallet_cli_routes_resolve_without_a_binary_installation_flow(self):
        package = ROOT / "skills/gate-dex-wallet"
        self.assertFalse((package / "install_cli.sh").exists())
        for name in ("README.md", "references/cli.md"):
            with self.subTest(document=name):
                body = (package / name).read_text()
                self.assertEqual(local_link_errors(package / name), [])
                for domain in ("wallet", "trade", "market"):
                    self.assertIn(f"gate-dex-{domain}-cli", body)
                for retired in ("install_cli.sh", "npm install", "build:binary"):
                    self.assertNotIn(retired, body)
        wallet = (package / "SKILL.md").read_text()
        self.assertIn("../gate-dex-wallet-cli/SKILL.md", wallet)
        self.assertIn("references/tx-checkin.md", wallet)


class WalletInstallerFixture(unittest.TestCase):
    """Bound every child to its own files and reuse the client boundary fixture."""

    def fixture(self):
        temporary = tempfile.TemporaryDirectory(prefix="dex-wallet-installer-")
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name)
        project, child_home, binaries = base / "project with spaces", base / "home", base / "bin"
        for path in (project, child_home, binaries):
            path.mkdir()
        config = child_home / ".codex/config.toml"
        config.parent.mkdir()
        config.write_text('[other]\ncommand = "preserve"\n')
        registry, events = base / "registry.json", base / "events.jsonl"
        registry.write_text('{"unrelated-server": ["preserve"]}')
        for command in ("claude", "codex", "cursor", "mcporter", "git", "curl", "wget",
                        "npm", "npx", "pnpm", "gate-dex", "gate-wallet", "gate-mcp"):
            wrapper = binaries / command
            wrapper.write_text("#!/bin/sh\nexec " + shlex.quote(sys.executable) + " -B " +
                               shlex.quote(str(PEER)) + " " + command + ' "$@"\n')
            wrapper.chmod(0o755)
        jq = shutil.which("jq")
        if jq:
            (binaries / "jq").symlink_to(jq)
        # Isolate HOME only in the child so real client configurations cannot be touched.
        env = {"PATH": str(binaries) + os.pathsep + os.defpath, "HOME": str(child_home),
               "PYTHONDONTWRITEBYTECODE": "1", "INSTALL_TEST_REGISTRY": str(registry),
               "INSTALL_TEST_EVENTS": str(events)}
        return SimpleNamespace(base=base, project=project, home=child_home, config=config,
                               registry=registry, events=events, env=env)

    def run_installer(self, fixture, *arguments):
        return subprocess.run(["bash", str(INSTALLER), *arguments], cwd=fixture.project,
                              env=fixture.env, input="a\n", capture_output=True, text=True, timeout=20)

    def run_function(self, fixture, platform):
        # Load production definitions without dispatching the interactive main entry point.
        prefix, separator, _ = INSTALLER.read_text().partition("# Parse arguments\n")
        self.assertTrue(separator)
        return subprocess.run(["bash", "-c", prefix + f"\ninstall_{platform}\n"],
                              cwd=fixture.project, env=fixture.env,
                              capture_output=True, text=True, timeout=10)

    def assert_cli_route(self, fixture, platform):
        body = (fixture.project / ROUTING[platform]).read_text()
        targets = re.findall(r"^- .*`gate-dex` CLI.*?→ `([^`]+)`$", body, re.M)
        self.assertEqual(targets, ["gate-dex-wallet-cli/SKILL.md"])
        self.assertEqual(HELPERS.header((ROOT / "skills" / targets[0]).read_text())["name"],
                         "gate-dex-wallet-cli")
        self.assertNotIn("install_cli.sh", body)
        self.assertNotIn("openapi-swap", body)

    def assert_only_registration(self, fixture):
        events = [json.loads(line) for line in fixture.events.read_text().splitlines()]
        self.assertTrue(events)
        self.assertTrue(all(row["command"] in {"claude", "codex", "mcporter"} for row in events),
                        events)

    def assert_fallback_configs(self, fixture):
        claude = json.loads((fixture.project / ".mcp.json").read_text())["mcpServers"]
        self.assertEqual({row["url"] for row in claude.values()}, ENDPOINTS)
        codex = tomllib.loads(fixture.config.read_text())
        self.assertEqual(codex["other"]["command"], "preserve")
        self.assertEqual(set(re.findall(r'https://api\.gatemcp\.ai/mcp/dex(?:/sec)?',
                                        fixture.config.read_text())), ENDPOINTS)


class WalletInstallerUnitTests(WalletInstallerFixture):
    """Cover routing in real functions, including registration-error branches."""

    def test_vendor_fixture_accepts_only_wallet_registration_arguments(self):
        fixture = self.fixture()
        for vendor in ROUTING:
            for server in ("gate-dex", "gate-dex-sec"):
                url = "https://api.gatemcp.ai/mcp/dex" + ("/sec" if server.endswith("-sec") else "")
                arguments = (["mcp", "add", "--transport", "http", server, "--scope", "project", url]
                             if vendor == "claude" else
                             ["mcp", "add", server, "--transport", "http", "--url", url])
                result = subprocess.run([vendor, *arguments], env=fixture.env,
                                        capture_output=True, timeout=5)
                self.assertEqual(result.returncode, 0)
            result = subprocess.run([vendor, "mcp", "list"], env=fixture.env,
                                    capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 99)

    def test_create_append_and_repeated_run_keep_one_cli_route(self):
        for platform in ROUTING:
            for existing in (False, True):
                with self.subTest(platform=platform, existing=existing):
                    fixture = self.fixture()
                    path = fixture.project / ROUTING[platform]
                    if existing:
                        path.write_text("Keep existing project guidance.\n")
                    for _ in range(2):
                        result = self.run_function(fixture, platform)
                        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                        self.assert_cli_route(fixture, platform)
                    if existing:
                        self.assertTrue(path.read_text().startswith("Keep existing project guidance.\n"))
                    self.assert_only_registration(fixture)

    def test_failed_registration_falls_back_without_losing_the_cli_route(self):
        fixture = self.fixture()
        fixture.env["INSTALL_TEST_FAIL_CLIENT"] = "all"
        for platform in ROUTING:
            for _ in range(2):
                result = self.run_function(fixture, platform)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assert_cli_route(fixture, platform)
        self.assert_fallback_configs(fixture)
        self.assert_only_registration(fixture)

    def test_secondary_registration_failure_keeps_manual_recovery_and_cli_route(self):
        for platform in ROUTING:
            with self.subTest(platform=platform):
                fixture = self.fixture()
                fixture.env["INSTALL_TEST_FAIL_SERVER"] = "gate-dex-sec"
                result = self.run_function(fixture, platform)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("gate-dex-sec not added via CLI", result.stdout)
                self.assert_cli_route(fixture, platform)
                self.assert_only_registration(fixture)


class WalletInstallerEndToEndTests(WalletInstallerFixture):
    """Run detection, selection, registration and actual routing/config writes."""

    def test_all_platforms_keep_mcp_configuration_without_installing_a_cli(self):
        fixture = self.fixture()
        result = self.run_installer(fixture)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for platform in ROUTING:
            self.assert_cli_route(fixture, platform)
        installed = fixture.home / ".cursor/skills/gate-dex-wallet"
        self.assertTrue((installed / "SKILL.md").is_file())
        self.assertFalse((installed / "install_cli.sh").exists())
        self.assertIn("gate-dex-wallet-cli", (installed / "references/cli.md").read_text())
        registry = json.loads(fixture.registry.read_text())
        self.assertEqual(set(registry), {"gate-dex", "gate-dex-sec", "unrelated-server"})
        self.assertEqual(registry["unrelated-server"], ["preserve"])
        self.assertNotIn("install_cli.sh", result.stdout)
        self.assert_only_registration(fixture)

    def test_all_platforms_keep_fallback_configuration_and_cli_routes(self):
        fixture = self.fixture()
        fixture.env["INSTALL_TEST_FAIL_CLIENT"] = "all"
        result = self.run_installer(fixture)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for platform in ROUTING:
            self.assert_cli_route(fixture, platform)
        self.assert_fallback_configs(fixture)
        self.assert_only_registration(fixture)

    def test_help_and_unknown_option_do_not_write_client_or_routing_files(self):
        fixture = self.fixture()
        for arguments, expected in ((("--help",), 0), (("--invalid-fixture",), 1)):
            with self.subTest(arguments=arguments):
                before = {str(path.relative_to(fixture.base)): path.read_bytes()
                          for folder in (fixture.project, fixture.home)
                          for path in folder.rglob("*") if path.is_file()}
                result = self.run_installer(fixture, *arguments)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                after = {str(path.relative_to(fixture.base)): path.read_bytes()
                         for folder in (fixture.project, fixture.home)
                         for path in folder.rglob("*") if path.is_file()}
                self.assertEqual(after, before)
                self.assertFalse(fixture.events.exists())


if __name__ == "__main__":
    unittest.main()
