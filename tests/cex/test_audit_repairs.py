"""Regressions for the four reviewed CEX request/response contract defects.

The E2E boundary is source -> real builder -> isolated installation -> checker
subprocess. No business CLI, account, network peer or trading action is invoked.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('audit_repair_tools', ROOT / 'scripts/cex_skills.py')
TOOLS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOLS)
CONTRACT = json.loads((ROOT / 'tests/cex/cli-contract.json').read_text())
MINIMUM = 'gate-cli cex earn auto-invest min-amount'
PRODUCTS = 'gate-cli cex earn fixed products'


class ReviewedContractTests(unittest.TestCase):
    """Keep the independent oracle complete, including omission and JSON types."""

    def test_four_reviewed_models_are_bound(self):
        expected = {
            ('gate-cex-earn', 'AutoInvestMinInvestAmount'): ('asset_type', 'int32'),
            ('gate-cex-subaccount', 'AccountKeyInfo'): ('name', 'string'),
            ('gate-cex-assets', 'TransactionItem'): ('detail', 'map[string]any'),
            ('gate-cex-trade', 'TransactionItem'): ('detail', 'map[string]any'),
        }
        specs = {(s['owner'], s['model']): s for s in CONTRACT['model_contracts']}
        self.assertEqual(set(specs), set(expected))
        for key, (field, kind) in expected.items():
            self.assertEqual(specs[key]['fields'][field]['type'], kind)
        asset = specs[('gate-cex-earn', 'AutoInvestMinInvestAmount')]
        self.assertEqual(asset['request_command'], MINIMUM)
        self.assertEqual(asset['fields']['asset_type'],
                         {'type': 'int32', 'required': True, 'enum': [1, 2]})

    def test_fixed_filter_flags_preserve_types_and_registered_defaults(self):
        flags = {f['name']: f for f in next(c for c in CONTRACT['commands']
                                          if c['path'] == PRODUCTS)['flags']}
        for name, kind, default in (('status', 'int32', '0'), ('show-status', 'string', '')):
            self.assertEqual(flags[name]['type'], kind)
            self.assertEqual(flags[name]['default'], default)
            self.assertFalse(flags[name]['required'])

    def test_explicit_empty_string_is_a_value_but_missing_value_is_an_error(self):
        spec = next(c for c in CONTRACT['commands'] if c['path'] == PRODUCTS)
        self.assertEqual(TOOLS.invocation_values([], spec), {})
        for argv in (['--show-status', ''], ['--show-status=']):
            self.assertEqual(TOOLS.invocation_values(argv, spec), {'show-status': ''})
        self.assertEqual(TOOLS.invocation_values(['--status', '0'], spec), {'status': '0'})
        # A permitted empty optional filter must not relax required JSON bodies.
        required = next(c for c in CONTRACT['commands'] if c['path'] == MINIMUM)
        for argv in (['--json', ''], ['--json=']):
            with self.subTest(required_argv=argv), self.assertRaises(ValueError):
                TOOLS.invocation_values(argv, required)
        for argv in (['--show-status'], ['--show-status', '--status', '0'], ['--status=']):
            with self.subTest(argv=argv), self.assertRaises(ValueError):
                TOOLS.invocation_values(argv, spec)

    def test_minimum_amount_accepts_explicit_integer_families_and_templates(self):
        for family in (1, 2):
            request = {'money': 'USDT', 'asset_type': family,
                       'items': [{'asset': 'BTC', 'ratio': '1'}]}
            self.assertEqual(TOOLS.request_contract_errors(MINIMUM, {'json': json.dumps(request)}, CONTRACT), [])
        self.assertEqual(TOOLS.request_contract_errors(MINIMUM, {'json': '<validated-body>'}, CONTRACT), [])
        self.assertEqual(TOOLS.request_contract_errors('unrelated', {'json': 'malformed'}, CONTRACT), [])
        self.assertEqual(TOOLS.request_contract_errors(MINIMUM, {}, CONTRACT), [])

    def test_minimum_amount_rejects_ambiguous_invalid_and_oversized_requests(self):
        raw_cases = ['{}', '', '{', '[]', 'null',
                     '{"asset_type":1,"asset_type":2}',
                     '{"asset_type":1,"Asset_type":2}',
                     '{"asset_type":1,"text":"' + ('x' * 65536) + '"}']
        raw_cases += [json.dumps({'asset_type': value})
                      for value in (None, True, False, '1', '2', 0, -1, 3,
                                    -(2**31)-1, 2**31, 1.0, [], {})]
        raw_cases += ['{"asset_type":' + value + '}' for value in ('NaN', 'Infinity', '1e1000')]
        for raw in raw_cases:
            with self.subTest(raw=raw[:80]):
                errors = TOOLS.request_contract_errors(MINIMUM, {'json': raw}, CONTRACT)
                self.assertTrue(errors)
                if raw:
                    self.assertNotIn(raw, '\n'.join(errors))

    def test_model_checker_catches_missing_wrong_optional_and_duplicate_fields(self):
        spec = next(s for s in CONTRACT['model_contracts'] if s['owner'] == 'gate-cex-earn')
        self.assertEqual(TOOLS.model_contract_errors('### AutoInvestMinInvestAmount\n\n`asset_type`: `int32`.\n', spec), [])
        for body in ('', '### WrongModel\n`asset_type`: `int32`.',
                     '### AutoInvestMinInvestAmount\n`money`: `string`.',
                     '### AutoInvestMinInvestAmount\n`asset_type?`: `int32`.',
                     '### AutoInvestMinInvestAmount\n`asset_type`: `string`.',
                     '### AutoInvestMinInvestAmount\n`asset_type`: `int32`; `asset_type`: `int32`.'):
            with self.subTest(body=body):
                self.assertTrue(TOOLS.model_contract_errors(body, spec))


class ReviewedPackageE2ETests(unittest.TestCase):
    """Assert corrected and regressed behavior through published checker entrypoints."""

    @classmethod
    def setUpClass(cls):
        cls.workspace = tempfile.TemporaryDirectory(prefix='cex-audit-repair-')
        cls.base = Path(cls.workspace.name)
        cls.packages = cls.base / 'packages'
        TOOLS.build(ROOT, cls.packages, CONTRACT)

    @classmethod
    def tearDownClass(cls):
        cls.workspace.cleanup()

    def setUp(self):
        self.case = tempfile.TemporaryDirectory(prefix='cex-audit-install-')
        self.install = Path(self.case.name)

    def tearDown(self):
        self.case.cleanup()

    def installed(self, profile):
        target = self.install / ('gate-cex-' + profile)
        shutil.copytree(self.packages / target.name, target)
        return target

    def seal(self, target):
        # Recompute the manifest so a negative case must hit semantic validation,
        # rather than merely reporting stale hashes after a synthetic mutation.
        manifest = json.loads((target / 'manifest.json').read_text())
        manifest['files'] = {str(p.relative_to(target)): hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in target.rglob('*') if p.is_file() and p.name != 'manifest.json'}
        (target / 'manifest.json').write_text(json.dumps(manifest))

    def check(self, target, expected_rule=None):
        args = [sys.executable, '-B', '-I', str(ROOT / 'scripts/cex_skills.py'), 'check',
                '--target', str(target), '--package', '--contract', str(ROOT / 'tests/cex/cli-contract.json')]
        result = subprocess.run(args, capture_output=True, text=True, timeout=30)
        payload = json.loads(result.stdout)
        if expected_rule:
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertTrue(any(f['rule'] == expected_rule for f in payload['findings']), payload)
        else:
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertEqual(payload['status'], 'PASS')
        return payload

    def test_six_independent_installations_pass(self):
        for profile in CONTRACT['profiles']:
            with self.subTest(profile=profile):
                target = self.installed(profile)
                self.assertEqual(list(self.install.iterdir()), [target])
                self.check(target)
                self.assertFalse(list(target.rglob('*.pyc')))
                shutil.rmtree(target)

    def test_each_reviewed_model_regression_fails_even_with_a_valid_manifest(self):
        cases = [('earn', 'models/auto-invest.md', '`asset_type`: `int32`', '`asset_type?`: `int32`'),
                 ('subaccount', 'models/permissions.md', '`name?`: `string`', '`name?`: `[]string`'),
                 ('assets', 'models/transfers.md', '`detail?`: `map[string]any`', '`detail?`: `map[string]map[string]any`'),
                 ('trade', 'models/stocks.md', '`detail?`: `map[string]any`', '`detail?`: `map[string]map[string]any`')]
        for profile, relative, correct, wrong in cases:
            with self.subTest(profile=profile):
                target = self.installed(profile)
                path = target / 'references' / relative
                text = path.read_text()
                self.assertIn(correct, text)
                path.write_text(text.replace(correct, wrong, 1))
                self.seal(target)
                payload = self.check(target, 'C5')
                self.assertFalse(any(f['rule'] == 'C6' for f in payload['findings']))
                shutil.rmtree(target)

    def test_invalid_minimum_example_is_rejected_and_fixed_filters_keep_presence(self):
        target = self.installed('earn')
        path = target / 'references/auto-invest-commands.md'
        original = path.read_text()
        path.write_text(original + '\n```text\n' + MINIMUM + ' --json \'{"money":"USDT","items":[]}\' --format json\n```\n')
        self.seal(target)
        self.check(target, 'C8')
        path.write_text(original)
        fixed = target / 'references/simple-earn-commands.md'
        fixed.write_text(fixed.read_text() + '\n```text\n' + PRODUCTS + " --status 0 --show-status '' --format json\n```\n")
        self.seal(target)
        self.check(target)
        fixed.write_text(fixed.read_text().replace('| `--status` | `int32` |', '| `--status` | `string` |'))
        self.seal(target)
        self.check(target, 'C4')

    def test_bad_source_model_prevents_publication_and_leaves_no_staging(self):
        source = self.install / 'source'
        shutil.copytree(ROOT / 'skills/gate-cex-earn', source / 'skills/gate-cex-earn')
        shutil.copytree(ROOT / 'skills/_shared/cex', source / 'skills/_shared/cex')
        model = source / 'skills/gate-cex-earn/references/models/auto-invest.md'
        model.write_text(model.read_text().replace('`asset_type`: `int32`;', ''))
        output = self.install / 'rejected'
        with self.assertRaises(ValueError):
            TOOLS.build(source, output, CONTRACT, profiles=('earn',))
        self.assertFalse(output.exists())
        self.assertEqual(list(self.install.glob('.cex-build-*')), [])
