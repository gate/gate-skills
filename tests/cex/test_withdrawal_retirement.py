"""Check the maintained assets instructions and real standalone package pipeline.

No business CLI or financial API is invoked: these tests exercise the artifact
users install, including the builder, rewritten links, manifest and validator.
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('withdrawal_builder', ROOT / 'scripts/cex_skills.py')
TOOLS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOLS)
CONTRACT = json.loads((ROOT / 'tests/cex/cli-contract.json').read_text())
REMOVED = {'gate-cli cex withdrawal create', 'gate-cli cex withdrawal cancel'}


class WithdrawalRetirementTests(unittest.TestCase):
    def assert_retired(self, target):
        """Reject operational templates, metadata promises and stale action contracts."""
        for path in target.rglob('*.md'):
            body = path.read_text()
            for command in REMOVED:
                self.assertNotIn(command, body, str(path))
            self.assertNotIn('Create a new withdrawal', body, str(path))
            self.assertNotIn('Cancel a pending withdrawal', body, str(path))
        entry = (target / 'SKILL.md').read_text()
        self.assertNotIn('internal transfers, withdrawals and', entry)
        workflow = (target / 'references/asset-workflows.md').read_text()
        self.assertNotRegex(workflow, r'(?m)^## Withdraw$')

    def test_source_and_independent_contract_remove_withdrawal_writes(self):
        self.assertTrue(REMOVED.isdisjoint(row['path'] for row in CONTRACT['commands']))
        self.assert_retired(ROOT / 'skills/gate-cex-assets')

    def test_retained_asset_actions_and_transfer_safeguards(self):
        """Freeze the remaining inventory independently of the edited skill index."""
        expected = {'gate-cli cex ' + path for path in (
            'stock account transactions', 'stock account transfer',
            'tradfi account transactions', 'tradfi account transfer',
            'wallet balance convert-small', 'wallet balance small',
            'wallet balance small-history', 'wallet balance sub',
            'wallet balance sub-cross-margin', 'wallet balance sub-futures',
            'wallet balance sub-margin', 'wallet balance total',
            'wallet deposit address', 'wallet deposit list',
            'wallet deposit push-orders', 'wallet deposit saved',
            'wallet deposit withdrawals', 'wallet market chains',
            'wallet market low-cap', 'wallet market trade-fee',
            'wallet market withdraw-status', 'wallet transfer create',
            'wallet transfer status', 'wallet transfer sub-list',
            'wallet transfer sub-to-sub', 'wallet transfer to-sub',
            'withdrawal push-order',
        )}
        actual = {row['path'] for row in CONTRACT['commands']
                  if row['owner'] == 'gate-cex-assets'}
        self.assertEqual(actual, expected)
        target = ROOT / 'skills/gate-cex-assets'
        self.assertEqual(TOOLS.inspect(target, CONTRACT)['status'], 'PASS')
        body = (target / 'references/withdrawals-commands.md').read_text()
        for safeguard in ('KYC/AML', 'sanctions', 'fee interpretation',
                          'transfer-information requirements', 'not proof of receipt'):
            self.assertIn(safeguard, body)

    def test_asset_package_end_to_end_and_other_profiles_still_validate(self):
        """Run the actual public builder/checker in subprocesses for all six profiles."""
        with tempfile.TemporaryDirectory(prefix='withdrawal-package-') as folder:
            output = Path(folder) / 'packages'
            result = subprocess.run(
                [sys.executable, '-B', str(ROOT / 'scripts/cex_skills.py'), 'build',
                 '--source', str(ROOT), '--contract', str(ROOT / 'tests/cex/cli-contract.json'),
                 '--output', str(output)], capture_output=True, text=True, timeout=45)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual({p.name for p in output.iterdir()},
                             {'gate-cex-' + profile for profile in CONTRACT['profiles']})
            self.assert_retired(output / 'gate-cex-assets')
            for profile in CONTRACT['profiles']:
                package = output / ('gate-cex-' + profile)
                result = subprocess.run(
                    [sys.executable, '-B', str(ROOT / 'scripts/cex_skills.py'), 'check',
                     '--target', str(package), '--package',
                     '--contract', str(ROOT / 'tests/cex/cli-contract.json')],
                    capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(json.loads(result.stdout)['status'], 'PASS')


if __name__ == '__main__':
    unittest.main()
