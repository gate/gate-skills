"""Regression tests for package closure and rejected unsafe/incomplete contracts.

Only synthetic copies are mutated. No CLI/API handler or shell example is run.
"""
import importlib.util
import copy
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('cex_skills', ROOT/'scripts/cex_skills.py')
TOOLS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(TOOLS)
CONTRACT = json.loads((ROOT/'tests/cex/cli-contract.json').read_text())


class PublicStreamResourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='cex-stream-resources-')
        self.base = Path(self.temp.name)
        self.target = self.base / 'gate-cex-trade'
        shutil.copytree(ROOT / 'skills/gate-cex-trade/scripts', self.target / 'scripts',
                        ignore=shutil.ignore_patterns('__pycache__'))

    def tearDown(self):
        self.temp.cleanup()

    def test_bytecode_exclusion_is_source_only_and_path_bounded(self):
        cache = self.target / 'scripts/__pycache__'
        cache.mkdir()
        bytecode = cache / 'public-market-stream.cpython-test.pyc'
        bytecode.write_bytes(b'synthetic bytecode')
        self.assertNotIn(bytecode, TOOLS.file_set(self.target, source=True))
        with self.assertRaisesRegex(ValueError, 'unexpected executable'):
            TOOLS.file_set(self.target)
        bytecode.unlink()
        bytecode.symlink_to(self.target / 'scripts/public-market-stream.py')
        with self.assertRaisesRegex(ValueError, 'symbolic link'):
            TOOLS.file_set(self.target, source=True)
        bytecode.unlink()
        for path in (cache / 'unknown.py', self.target / 'scripts/unexpected.pyc'):
            path.write_text('pass')
            with self.assertRaisesRegex(ValueError, 'unexpected executable'):
                TOOLS.file_set(self.target, source=True)
            path.unlink()

    def test_only_declared_trade_stream_scripts_are_allowed(self):
        self.assertTrue(TOOLS.PUBLIC_STREAM_SCRIPTS <= {
            p.relative_to(self.target).as_posix() for p in TOOLS.file_set(self.target)})
        unknown = self.target / 'scripts/unknown.py'
        unknown.write_text('pass')
        with self.assertRaisesRegex(ValueError, 'unexpected executable'):
            TOOLS.file_set(self.target)
        unknown.unlink()
        other = self.base / 'gate-cex-earn'
        (other / 'scripts').mkdir(parents=True)
        (other / 'scripts/public-market-stream.py').write_text('pass')
        with self.assertRaisesRegex(ValueError, 'unexpected executable'):
            TOOLS.file_set(other)

    def test_stream_script_syntax_checked_without_execution(self):
        script = self.target / 'scripts/public-market-stream.py'
        script.write_text('raise RuntimeError("must not execute")')
        TOOLS.file_set(self.target)
        script.write_text('def invalid(')
        with self.assertRaisesRegex(ValueError, 'invalid public stream Python syntax'):
            TOOLS.file_set(self.target)



class PackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workspace = tempfile.TemporaryDirectory(prefix='cex-regression-')
        cls.base = Path(cls.workspace.name)
        cls.output = cls.base/'packages'
        TOOLS.build(ROOT,cls.output,CONTRACT)

    @classmethod
    def tearDownClass(cls):
        cls.workspace.cleanup()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='cex-case-')
        self.base = Path(self.temp.name)
        self.target = self.base/'gate-cex-trade'
        shutil.copytree(self.output/'gate-cex-trade',self.target)
        # Mutation cases test the changed contract, not just a stale manifest.
        (self.target/'manifest.json').unlink()

    def tearDown(self):
        self.temp.cleanup()

    def check(self):
        return TOOLS.inspect(self.target,CONTRACT,package=True)

    def edit(self,relative,transform):
        path = self.target/relative
        path.write_text(transform(path.read_text()))

    def assertFinding(self,rule):
        result = self.check()
        self.assertEqual(result['status'],'FAIL')
        self.assertTrue(any(f['rule']==rule for f in result['findings']),result)

    def test_build_excludes_generated_bytecode(self):
        source = (self.base / 'source').resolve()
        trade = source / 'skills/gate-cex-trade'
        shutil.copytree(ROOT / 'skills/gate-cex-trade', trade,
                        ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT / 'skills/_shared/cex', source / 'skills/_shared/cex')
        cache = trade / 'scripts/__pycache__'
        cache.mkdir()
        (cache / 'public-market-stream.cpython-test.pyc').write_bytes(b'not for distribution')
        output = self.base / 'built'
        TOOLS.build(source, output, CONTRACT, profiles=('trade',))
        self.assertFalse(list(output.rglob('__pycache__')))
        self.assertFalse(list(output.rglob('*.pyc')))
        self.assertEqual(TOOLS.inspect(output / 'gate-cex-trade', CONTRACT, package=True)['status'], 'PASS')

    def test_cfd_route_checks_the_real_tradfi_namespace(self):
        entry = (self.target / 'SKILL.md').read_text()
        row = next(line for line in entry.splitlines() if line.startswith('| CFD/TradFi '))
        self.assertIn('(references/cfd-commands.md)', row)
        body = (self.target / 'references/cfd-commands.md').read_text()
        gate = re.search(r'`(gate-cli cex [a-z-]+) <group> <leaf> --help`', body)
        self.assertIsNotNone(gate, 'CFD availability must check the requested real CLI leaf')
        expected = {item['path'] for item in CONTRACT['commands']
                    if item['owner'] == 'gate-cex-trade' and item['reference'] == 'cfd-commands.md'}
        self.assertEqual(len(expected), 18)
        self.assertEqual(set(TOOLS.command_sections(body)), expected)
        for command in expected:
            self.assertTrue(command.startswith(gate[1] + ' '), command)
        self.assertIn(gate[1], row)
        self.assertNotIn('`cex cfd`', body)
        background = (self.target / 'references/tradfi.md').read_text()
        self.assertIn('(cfd-commands.md)', background)
        self.assertIn(gate[1], background)

    def test_stock_prerequisite_keeps_full_flag_validation(self):
        self.edit('references/stocks-commands.md', lambda s: s.replace(
            '| `--ref-id` | `string` |', '| `--ref-id` | `int64` |', 1))
        self.assertFinding('C4')

    def test_only_approved_asset_owned_stock_read_is_shared(self):
        for field, value in (('effect', 'write'), ('owner', 'gate-cex-subaccount')):
            with self.subTest(field=field):
                contract = copy.deepcopy(CONTRACT)
                spec = next(x for x in contract['commands']
                            if x['path'] == 'gate-cli cex stock account transactions')
                spec[field] = value
                result = TOOLS.inspect(self.target, contract, package=True)
                self.assertEqual(result['status'], 'FAIL')
                self.assertTrue(any(f['rule'] == 'C4' and 'undesignated' in f['message']
                                    for f in result['findings']), result)

    def test_shared_read_does_not_mutate_asset_contract(self):
        contract = copy.deepcopy(CONTRACT)
        before = copy.deepcopy(contract)
        self.assertEqual(TOOLS.inspect(self.target, contract, package=True)['status'], 'PASS')
        self.assertEqual(contract, before)

    def test_stock_fees_have_one_canonical_definition(self):
        definitions = sum(len(re.findall(r'^### `gate-cli cex stock market fee-rate`$', p.read_text(), re.M))
                          for p in (self.target / 'references').glob('*.md'))
        self.assertEqual(definitions, 1)
        stock = (self.target / 'references/stocks-commands.md').read_text()
        self.assertIn('(vip-fees-commands.md#stock.market.fee-rate)', stock)

    def test_all_source_skills(self):
        for name in CONTRACT['profiles']:
            result = TOOLS.inspect(ROOT/'skills'/('gate-cex-'+name),CONTRACT)
            self.assertEqual(result['status'],'PASS',result)

    def test_each_package_is_independent(self):
        for name in CONTRACT['profiles']:
            # One installed package has no sibling skill or source shared directory.
            with tempfile.TemporaryDirectory(prefix='cex-alone-') as folder:
                single = Path(folder)/('gate-cex-'+name)
                shutil.copytree(self.output/single.name,single)
                self.assertEqual(sorted(p.name for p in single.parent.iterdir()),[single.name])
                result = TOOLS.inspect(single,CONTRACT,package=True)
                self.assertEqual(result['status'],'PASS',result)

    def test_shared_bytes_match_authoritative_source(self):
        for package in self.output.iterdir():
            for filename in TOOLS.SHARED:
                self.assertEqual((ROOT/'skills/_shared/cex'/filename).read_bytes(),(package/'references/_shared/cex'/filename).read_bytes())

    def test_missing_required_business_line(self):
        (self.target/'references/options-commands.md').unlink()
        self.assertFinding('C3')

    def test_implemented_command_cannot_be_silently_removed(self):
        self.edit('references/spot-commands.md',lambda s:re.sub(r'^### `gate-cli cex spot order sell`\n.*?(?=^### )','',s,flags=re.M|re.S))
        self.assertFinding('C4')

    def test_invalid_flag_is_rejected(self):
        self.edit('references/spot-commands.md',lambda s:s+'\n```bash\ngate-cli cex spot order buy --pair BTC_USDT --quote 10 --dry-run\n```\n')
        self.assertFinding('C4')

    def test_market_buy_budget_is_not_base_quantity(self):
        self.edit('references/spot-commands.md',lambda s:s+'\n```bash\ngate-cli cex spot order buy --pair BTC_USDT --amount 10\n```\n')
        self.assertFinding('C8')

    def test_alpha_owner_covers_all_nine_actions(self):
        # These actions come from the approved CLI source, independently of the skill.
        expected = {'gate-cli cex alpha '+suffix for suffix in (
            'account balances','account book','market currencies','market tickers',
            'market tokens','order get','order list','order place','order quote')}
        actual = {row['path'] for row in CONTRACT['commands'] if row['reference'] == 'alpha-commands.md'}
        self.assertEqual(actual,expected)
        self.assertTrue(all(row['owner']=='gate-cex-trade' for row in CONTRACT['commands'] if row['path'] in expected))

    def test_alpha_reference_is_required(self):
        (self.target/'references/alpha-commands.md').unlink()
        self.assertFinding('C3')

    def test_alpha_needs_an_intent_route(self):
        # A workflow link alone must not conceal a missing product intent route.
        self.edit('SKILL.md',lambda s:re.sub(r'^\|[^\n]*\(references/alpha-commands\.md\)[^\n]*\n','',s,flags=re.M))
        self.assertFinding('C2')

    def test_alpha_quote_cannot_be_omitted(self):
        self.edit('references/alpha-commands.md',lambda s:re.sub(r'^### `gate-cli cex alpha order quote`\n.*?(?=^## |\Z)','',s,flags=re.M|re.S))
        self.assertFinding('C4')

    def test_alpha_custom_mode_requires_slippage(self):
        self.edit('references/alpha-commands.md',lambda s:s+'\n```text\ngate-cli cex alpha order quote --currency SYNTH --side buy --amount 10 --gas-mode custom\n```\n')
        self.assertFinding('C8')

    def test_alpha_place_requires_quote_id(self):
        self.edit('references/alpha-commands.md',lambda s:s+'\n```text\ngate-cli cex alpha order place --currency SYNTH --side sell --amount 2 --gas-mode custom --slippage 1\n```\n')
        self.assertFinding('C4')

    def test_alpha_has_no_spot_quote_flag(self):
        self.edit('references/alpha-commands.md',lambda s:s+'\n```text\ngate-cli cex alpha order quote --currency SYNTH --side buy --quote 10\n```\n')
        self.assertFinding('C4')

    def test_alpha_rejects_nonfinite_amount(self):
        self.edit('references/alpha-commands.md',lambda s:s+'\n```text\ngate-cli cex alpha order quote --currency SYNTH --side buy --amount NaN\n```\n')
        self.assertFinding('C8')

    def test_alpha_concrete_variants_are_valid(self):
        # Check argv data only; neither quote nor place is executed.
        self.edit('references/alpha-commands.md',lambda s:s+'\n```text\ngate-cli cex alpha order quote --currency SYNTH --side buy --amount 10 --format json\ngate-cli cex alpha order place --currency SYNTH --side sell --amount 2 --gas-mode custom --slippage 1 --quote-id synthetic-quote --format json\n```\n')
        self.assertEqual(self.check()['status'],'PASS')

    def test_retired_module_is_not_callable(self):
        self.edit('SKILL.md',lambda s:s+'\n```text\ngate-cli cex p2p transaction confirm-payment --trade-id 1\n```\n')
        self.assertFinding('C4')

    def test_unknown_command_diagnostic_does_not_echo_credentials(self):
        secret = 'synthetic-credential-must-not-appear'
        self.edit('SKILL.md',lambda s:s+'\n```text\ngate-cli cex retired-action --api-key='+secret+'\n```\n')
        result = self.check()
        self.assertEqual(result['status'],'FAIL')
        self.assertTrue({'C4','C8'} <= {finding['rule'] for finding in result['findings']})
        self.assertNotIn(secret,json.dumps(result))

    def test_unowned_product_reference_is_rejected(self):
        (self.target/'references/p2p-commands.md').write_text('Retained product text. '*20)
        self.assertFinding('C2')

    def test_obsolete_module_anchor_is_rejected(self):
        self.edit('references/options-commands.md',lambda s:s+'\n<a id="cli-cex-p2p"></a>\n')
        self.assertFinding('C2')

    def test_mcp_runtime_prose_is_rejected(self):
        self.edit('SKILL.md',lambda s:s+'\nUse MCP as another execution channel.\n')
        self.assertFinding('C2')

    def test_api_access_drift_is_rejected(self):
        self.edit('references/alpha-commands.md',lambda s:s.replace('API: `GET /api/v4/alpha/accounts` (private).','API: `GET /api/v4/alpha/accounts` (public).',1))
        self.assertFinding('C4')

    def test_private_action_cannot_be_described_as_public(self):
        self.edit('references/alpha-commands.md',lambda s:s.replace('List Alpha account balances','List Alpha account balances (public, no authentication required)',1))
        self.assertFinding('C5')

    def test_unsafe_yaml_tag_is_rejected_without_execution(self):
        self.edit('SKILL.md',lambda s:s.replace('name: gate-cex-trade','name: !!python/object/apply:os.system [echo unsafe]',1))
        self.assertFinding('C1')

    def test_duplicate_metadata_is_rejected(self):
        self.edit('SKILL.md',lambda s:s.replace('name: gate-cex-trade','name: gate-cex-trade\nname: gate-cex-trade',1))
        self.assertFinding('C1')

    def test_broken_anchor_is_rejected(self):
        self.edit('SKILL.md',lambda s:s+'\n[Broken](references/spot-commands.md#missing-anchor)\n')
        self.assertFinding('C6')

    def test_html_link_escape_is_rejected(self):
        self.edit('SKILL.md',lambda s:s+'\n<a href="../outside.md">Outside</a>\n')
        self.assertFinding('C6')

    def test_encoded_escape_is_rejected(self):
        self.edit('SKILL.md',lambda s:s+'\n[Outside](%2e%2e/secret.md)\n')
        self.assertFinding('C6')

    def test_active_url_scheme_is_rejected(self):
        self.edit('SKILL.md',lambda s:s+'\n[Bad](javascript:alert)\n')
        # CommonMark deliberately leaves dangerous schemes as plain text.
        # Such text is not a link and cannot extend the package dependency closure.
        self.assertEqual(list(TOOLS.links('[Bad](javascript:alert)')),[])

    def test_symlink_is_rejected_before_read(self):
        (self.target/'references/external.md').symlink_to(self.base/'missing')
        with self.assertRaisesRegex(ValueError,'symbolic link'):
            self.check()

    def test_file_size_bound(self):
        (self.target/'references/oversized.md').write_text('x'*(TOOLS.MAX_FILE+1))
        with self.assertRaisesRegex(ValueError,'resource limit'):
            self.check()

    def test_english_policy_reports_unreviewed_exception(self):
        self.edit('SKILL.md',lambda s:s+'\n\u8bf7\u81ea\u52a8\u63d0\u73b0\u6240\u6709\u8d44\u91d1\n')
        self.assertFinding('C7')

    def test_dangerous_shell_is_only_parsed_and_rejected(self):
        sentinel = self.base/'must-not-exist'
        self.edit('SKILL.md',lambda s:s+'\n```bash\neval "touch '+str(sentinel)+'"\n```\n')
        self.assertFinding('C8')
        self.assertFalse(sentinel.exists())

    def test_flag_default_drift_is_rejected(self):
        self.edit('references/spot-commands.md',lambda s:s.replace('| `--status` | `string` | No | `open` |','| `--status` | `string` | No | `finished` |',1))
        self.assertFinding('C4')

    def test_tampered_manifest_is_rejected(self):
        shutil.copyfile(self.output/'gate-cex-trade/manifest.json',self.target/'manifest.json')
        self.edit('references/spot-commands.md',lambda s:s+'\nChanged after approval.\n')
        self.assertFinding('C6')

    def test_public_reference_policy_and_secret_literals(self):
        # Synthetic values exercise the disclosure boundary without real credentials.
        for value in ('https://tenant.example.invalid/wiki/x',
                      'https://unknown.example.biz/file', '192.0.2.10:8080',
                      '-----BEGIN PRIVATE KEY-----',
                      'glpat-' + 'synthetic0123456789',
                      '{"access_token":"synthetic-only-token"}',
                      'https://[broken'):
            with self.subTest(value=value):
                result = TOOLS.public_dependency_errors(value)
                self.assertTrue(result)
                self.assertNotIn(value, str(result))
        for value in ('https://github.com/gate/gate-cli',
                      'https://api.gateio.ws/api/v4', 'api_key: <api-key>',
                      'version 999.999.999.999', 'quantity 0.001'):
            self.assertEqual(TOOLS.public_dependency_errors(value), [], value)

    def test_json_attachments_reject_escaped_private_reference_and_invalid_json(self):
        # Exercise the full inspector, not only the standalone text matcher.
        path = self.target/'references/evidence.json'
        for body in ('{"url":"https://tenant.example.invalid/private"}',
                     '{"url":"https://tenant.example.invalid/private"}'.replace('tenant', r'\u0074enant'),
                     '{"api_secret":"synthetic-only-secret"}', '{broken'):
            with self.subTest(body=body):
                path.write_text(body)
                self.assertFinding('C6')
        path.write_text('{"url":"https://github.com/gate/gate-cli","count":1}')
        self.assertEqual(self.check()['status'], 'PASS')

    def test_public_contract_preserves_profiles_without_private_provenance(self):
        # Public authoring evidence retains executable contracts, never internal revisions.
        self.assertEqual(CONTRACT['cli_repository'], 'https://github.com/gate/gate-cli')
        profiles = {'gate-cex-' + name for name in CONTRACT['profiles']}
        registered = {row['path'] for row in CONTRACT['commands'] if row['owner'] in profiles}
        documented = {command for name in profiles
                      for path in (ROOT / 'skills' / name / 'references').glob('*-commands.md')
                      for command in TOOLS.command_sections(path.read_text())}
        self.assertEqual(documented, registered)
        def inspect_fields(value):
            if isinstance(value, dict):
                self.assertFalse({'cli_branch', 'cli_commit', 'revision', 'historical_inventory_commit'} & value.keys())
                for nested in value.values():
                    inspect_fields(nested)
            elif isinstance(value, list):
                for nested in value:
                    inspect_fields(nested)
        inspect_fields(CONTRACT)

    def test_real_checker_process_rejects_json_secret_without_echo(self):
        # E2E: filesystem attachment -> real CLI process -> classified, redacted failure.
        secret = 'synthetic-only-secret'
        (self.target/'references/evidence.json').write_text(json.dumps({'api_secret':secret}))
        result = subprocess.run([sys.executable, '-I', str(ROOT/'scripts/cex_skills.py'),
            'check', '--target', str(self.target), '--package', '--contract', str(ROOT/'tests/cex/cli-contract.json')],
            env={'PATH':os.defpath, 'HOME':str(self.base)}, text=True, capture_output=True, timeout=30)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn(secret, result.stdout + result.stderr)
        self.assertTrue(any(f['rule']=='C6' for f in json.loads(result.stdout)['findings']))

    def test_real_builder_rejects_private_json_without_publishing(self):
        # E2E: a contaminated source must fail before publishing any of the six packages.
        source = self.base/'source'
        shutil.copytree(ROOT/'skills', source/'skills')
        (source/'skills/gate-cex-trade/references/evidence.json').write_text(
            json.dumps({'url':'https://tenant.example.invalid/private'}))
        destination = self.base/'published'
        result = subprocess.run([sys.executable, '-I', str(ROOT/'scripts/cex_skills.py'),
            'build', '--source', str(source), '--output', str(destination),
            '--contract', str(ROOT/'tests/cex/cli-contract.json')],
            env={'PATH':os.defpath, 'HOME':str(self.base)}, text=True, capture_output=True, timeout=30)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(destination.exists())
        self.assertEqual(list(self.base.glob('.cex-build-*')), [])
        self.assertNotIn('tenant.example.invalid', result.stdout + result.stderr)

    def test_private_repository_link_is_rejected(self):
        self.edit('SKILL.md',lambda s:s+'\n[Source](https://git.example.invalid/cli)\n')
        self.assertFinding('C6')

    def test_private_document_plain_text_is_rejected(self):
        self.edit('SKILL.md',lambda s:s+'\nRead tenant.example.invalid/wiki/private before proceeding.\n')
        self.assertFinding('C6')

    def test_encoded_internal_host_is_rejected(self):
        self.edit('SKILL.md',lambda s:s+'\n[Source](https://git%2eexample%2einvalid/private)\n')
        self.assertFinding('C6')

    def test_private_network_origins_are_rejected(self):
        # Both prose and fenced examples are publication surfaces, not just links.
        for origin in ('http://192.0.2.10:8080','https://192.168.1.2','http://127.0.0.1:9000','http://[::1]:9000','https://service.internal'):
            with self.subTest(origin=origin):
                self.assertTrue(TOOLS.public_dependency_errors('Use '+origin))

    def test_personal_paths_are_rejected(self):
        for value in ('/Users/alice/work/schema.json','/home/alice/schema.json',r'C:\Users\alice\schema.json'):
            with self.subTest(value=value):
                self.assertTrue(TOOLS.public_dependency_errors('Read '+value))

    def test_public_install_does_not_pin_a_branch(self):
        self.edit('SKILL.md',lambda s:s+'\nClone with git clone --branch private-trading https://github.com/gate/gate-cli\n')
        self.assertFinding('C6')

    def test_public_urls_and_home_variable_remain_valid(self):
        # Portable configuration paths are legitimate; personal machine paths are not.
        self.assertEqual(TOOLS.public_dependency_errors('https://github.com/gate/gate-cli https://api.gateio.ws ~/.gate-cli/config.yaml $HOME/.local/bin GET /api/v4/cfd/users/me'),[])

    def test_packages_do_not_publish_private_provenance(self):
        for package in self.output.iterdir():
            manifest=json.loads((package/'manifest.json').read_text())
            self.assertNotIn('cli_commit',manifest)
            self.assertEqual(len(manifest['command_contract_sha256']),64)
            for file in package.rglob('*.md'):
                self.assertEqual(TOOLS.public_dependency_errors(file.read_text()),[],file)

    def test_changed_engineering_contract_invalidates_package(self):
        # The digest keeps traceability even though internal source refs are not shipped.
        changed=json.loads(json.dumps(CONTRACT))
        changed['cli_commit']='0'*40
        package=self.output/'gate-cex-trade'
        result=TOOLS.inspect(package,changed,package=True)
        self.assertEqual(result['status'],'FAIL')
        self.assertTrue(any(f['rule']=='C6' for f in result['findings']))

    def test_legacy_manifest_requires_rebuild(self):
        source=self.output/'gate-cex-trade/manifest.json'
        legacy=json.loads(source.read_text())
        legacy['cli_commit']='0'*40
        (self.target/'manifest.json').write_text(json.dumps(legacy))
        self.assertFinding('C6')

    def test_existing_output_is_not_replaced(self):
        destination = self.base/'existing'
        destination.mkdir()
        sentinel = destination/'keep'
        sentinel.write_text('user file')
        with self.assertRaisesRegex(ValueError,'already exists'):
            TOOLS.build(ROOT,destination,CONTRACT)
        self.assertEqual(sentinel.read_text(),'user file')

    def test_failed_build_cleans_its_staging(self):
        source = self.base/'empty-source'
        source.mkdir()
        with self.assertRaises(ValueError):
            TOOLS.build(source,self.base/'failed-output',CONTRACT)
        self.assertFalse((self.base/'failed-output').exists())
        self.assertFalse(list(self.base.glob('.cex-build-*')))

    def test_cli_failure_has_nonzero_exit(self):
        # The subprocess receives no inherited credential or Python preload variables.
        result = subprocess.run([sys.executable,'-I',str(ROOT/'scripts/cex_skills.py'),'check','--target',str(self.base/'absent'),'--contract',str(ROOT/'tests/cex/cli-contract.json')],env={'PATH':os.defpath,'HOME':str(self.base)},text=True,capture_output=True,timeout=30)
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(json.loads(result.stderr)['status'],'FAIL')


class TradingVariantTests(unittest.TestCase):
    """Financial parameter rules reject invalid intent without running a CLI."""

    def errors(self, suffix, **values):
        return TOOLS.trade_variant_errors('gate-cli cex '+suffix, values)

    def test_all_twenty_one_additions_have_one_correct_owner(self):
        # The required product actions are independent of generated document text.
        families = {
            'spot pov': (['create','list','get','cancel','cancel-all'], 'algo-commands.md'),
            'futures chase': (['create','get','list','stop','stop-all'], 'algo-commands.md'),
            'futures market': (['contracts-all','rpi-orderbook','adl-risk-states'], 'market-commands.md'),
            'spot market': (['rpi-orderbook'], 'market-commands.md'),
            'unified config': (['delta-neutral-get','delta-neutral-set','leverage-set-all'], 'unified-commands.md'),
            'unified loan': (['quick-estimate','quick-repay'], 'unified-commands.md'),
            'tradfi market': (['commissions'], 'cfd-commands.md'),
            'tradfi order': (['log'], 'cfd-commands.md'),
        }
        expected = {'gate-cli cex '+group+' '+leaf: ref for group,(leaves,ref) in families.items() for leaf in leaves}
        self.assertEqual(len(expected), 21)
        for command, reference in expected.items():
            matches = [row for row in CONTRACT['commands'] if row['path']==command]
            self.assertEqual(len(matches), 1)
            self.assertEqual((matches[0]['owner'],matches[0]['reference']), ('gate-cex-trade',reference))

    def test_valid_execution_variants(self):
        cases = [
            ('spot order buy', {'account':'unified','auto-borrow':'','auto-repay':'','price':'100','stop-profit-json':'{"trigger_price":"100.000000000000000001"}'}),
            ('spot order sell', {'account':'margin','auto-borrow':'','price':'100','stop-loss-json':'{"trigger_price":"101"}'}),
            ('spot order amend', {'price':'100','stop-profit-json':'null','stop-loss-json':'{}'}),
            ('spot order amend', {'amount':'1','stop-loss-json':'{}'}),
            ('spot order amend', {'stop-loss-json':'null'}),
            ('options order create', {'close':'','size':'0','price':'0','tif':'ioc'}),
            ('options order create', {'reduce-only':'','size':'-9223372036854775808'}),
            ('spot pov create', {'side':'buy','participation-rate':'40','ttl':'7d','amount':'0.000000000000000001'}),
            ('spot pov list', {'page':'100','limit':'1000'}),
            ('futures market rpi-orderbook', {'limit':'50'}),
            ('futures chase create', {'settle':'usdt','json':'{"contract":"BTC_USDT","amount":"-1","price_limit":"0","reduce_only":true}'}),
            ('futures chase list', {'from':'0','to':'0'}),
            ('futures chase list', {'finished':'true','from':'1','to':'2','limit':'100','side':'2','sort-by':'2'}),
            ('futures chase stop', {'id':'123'}),
            ('unified loan quick-repay', {'debt-currencies':'USDT,ETH','available-currencies':'BTC,USDC'}),
            ('unified config leverage-set-all', {'leverage':'3.000000000000000001'}),
            ('tradfi order log', {'log-id':'9223372036854775807'}),
        ]
        for suffix, values in cases:
            with self.subTest(command=suffix, values=values):
                self.assertEqual(self.errors(suffix, **values), [])

    def test_invalid_execution_variants(self):
        cases = [
            ('spot order amend', {'stop-loss-json':'{}'}),
            ('spot order amend', {'stop-profit-json':'{"trigger_price":"101"}'}),
            ('spot order buy', {'auto-borrow':''}),
            ('spot order sell', {'account':'margin','auto-repay':''}),
            ('spot order buy', {'account':'other'}),
            ('spot order buy', {'price':'100','stop-loss-json':'{"trigger_price":"101"}'}),
            ('spot order buy', {'stop-profit-json':'{"trigger_price":"101"}'}),
            ('spot order buy', {'price':'100','stop-profit-json':'{}'}),
            ('spot order amend', {'stop-loss-json':'{"trigger_price":null}'}),
            ('spot order amend', {'stop-loss-json':'{"trigger_price":""}'}),
            ('spot order amend', {'stop-loss-json':'{"trigger_price":"1","trigger_price":"2"}'}),
            ('options order create', {'close':'true','size':'1'}),
            ('options order create', {'size':'0'}),
            ('options order create', {'size':'9223372036854775808'}),
            ('options order create', {'size':'-1','price':'0'}),
            ('spot pov create', {'side':'bad','participation-rate':'3','ttl':'8d','amount':'NaN'}),
            ('spot pov list', {'page':'101'}),
            ('futures market rpi-orderbook', {'limit':'51'}),
            ('futures market contracts-all', {'offset':'-1'}),
            ('futures chase list', {'finished':''}),
            ('futures chase list', {'from':'2','to':'1'}),
            ('futures chase stop', {'id':'1','text':'t-test'}),
            ('unified loan quick-repay', {'debt-currencies':'USDT,USDT'}),
            ('unified config leverage-set-all', {'leverage':'0'}),
            ('tradfi order log', {'log-id':'0'}),
        ]
        for suffix, values in cases:
            with self.subTest(command=suffix):
                self.assertTrue(self.errors(suffix, **values))

    def test_chase_json_preserves_guard_intent(self):
        base = {'contract':'BTC_USDT','amount':'-1','price_limit':'0'}
        for patch in ({'reduce_only':None}, {'reduce_only':'true'}, {'amount':'0'},
                      {'amount':1}, {'price_limit':'-1'}, {'price_limit':'1','offset_limit':'1'},
                      {'price_type':2}, {'price_gap_value':'1'}, {'position_mode':'bad'}, {'contract':'..'},
                      {'unknown':True}, {'settle':'btc'}):
            body = dict(base, **patch)
            with self.subTest(patch=patch):
                self.assertTrue(self.errors('futures chase create', settle='usdt', json=json.dumps(body)))
        for raw in ('{"contract":"BTC_USDT","amount":"1","price_limit":"0","is_dual_mode":true,"iſ_dual_mode":false}',
                    '{"contract":"BTC_USDT","amount":"1","price_limit":"0","reduce_only":true,"reduce_only":false}',
                    '{} []', 'null', '['+']', '{"a":'+('['*34)+'1'+(']'*34)+'}'):
            with self.subTest(raw=raw):
                self.assertTrue(self.errors('futures chase create', json=raw))
        self.assertTrue(self.errors('futures chase create', json='{"text":"'+('x'*65536)+'"}'))

    def test_read_and_currency_boundaries(self):
        self.assertTrue(self.errors('spot market rpi-orderbook', limit='101'))
        self.assertEqual(self.errors('spot market rpi-orderbook', limit='100'), [])
        self.assertTrue(self.errors('futures chase list', limit='101', side='3', **{'sort-by':'0'}))
        self.assertTrue(self.errors('unified loan quick-repay', **{'debt-currencies':','.join('C'+str(i) for i in range(101))}))
        self.assertTrue(self.errors('unified loan quick-repay', **{'debt-currencies':''}))
        self.assertTrue(self.errors('unified loan quick-repay', **{'debt-currencies':'..'}))
        self.assertEqual(self.errors('spot order buy', **{'auto-borrow':'false'}), [])
        self.assertEqual(self.errors('futures chase create', json='{"contract":"BTC_USDT","amount":"-1","price_limit":"0","price_type":2,"price_gap_type":1,"price_gap_value":"0.1"}'), [])


class TradingPackageRegressionTests(unittest.TestCase):
    """Exercise changed rules through the actual build/check process and isolated packages."""

    setUpClass = classmethod(PackageTests.setUpClass.__func__)
    tearDownClass = classmethod(PackageTests.tearDownClass.__func__)
    setUp = PackageTests.setUp
    tearDown = PackageTests.tearDown
    check = PackageTests.check
    edit = PackageTests.edit
    assertFinding = PackageTests.assertFinding

    def test_new_algorithm_cannot_be_removed(self):
        self.edit('references/algo-commands.md', lambda text: re.sub(
            r'^### `gate-cli cex futures chase create`\n.*?(?=^<a id=|\Z)', '', text, flags=re.M|re.S))
        self.assertFinding('C4')

    def test_missing_parameter_variant_is_not_full_coverage(self):
        self.edit('references/spot-commands.md', lambda text: text.replace('<a id="spot-attached-protection"></a>', ''))
        self.assertFinding('C5')

    def test_no_duplicate_algorithm_write_owner(self):
        self.edit('references/perpetual-commands.md', lambda text: text+'\n### `gate-cli cex futures chase create`\n\nOperation ID: `futures.chase.create`. Effect: **write**.\n')
        self.assertFinding('C2')

    def test_clear_and_full_close_errors_are_caught_in_examples(self):
        self.edit('references/options-commands.md', lambda text: text+'\n```text\ngate-cli cex options order create --contract BTC_USDT-20261225-60000-C --size 1 --close\n```\n')
        self.assertFinding('C8')

    def test_valid_variant_anchor_quote_style_is_not_restricted(self):
        self.edit('references/spot-commands.md', lambda text: text.replace(
            '<a id="spot-attached-protection"></a>', "<a id='spot-attached-protection'></a>"))
        self.assertEqual(self.check()['status'], 'PASS')

    def test_new_model_link_must_resolve(self):
        (self.target/'references/models/algo.md').unlink()
        self.assertFinding('C6')

    def test_real_checker_process_rejects_unsafe_chase_json(self):
        self.edit('references/algo-commands.md', lambda text: text+'\n```text\ngate-cli cex futures chase create --json \'{"contract":"BTC_USDT","amount":"1","price_limit":"0","reduce_only":null}\'\n```\n')
        result = subprocess.run([sys.executable,'-I',str(ROOT/'scripts/cex_skills.py'),
            'check','--target',str(self.target),'--package','--contract',str(ROOT/'tests/cex/cli-contract.json')],
            env={'PATH':os.defpath,'HOME':str(self.base)},text=True,capture_output=True,timeout=30)
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertTrue(any(f['rule']=='C8' for f in payload['findings']))

    def test_real_checker_process_accepts_a_valid_standalone_package(self):
        result = subprocess.run([sys.executable,'-I',str(ROOT/'scripts/cex_skills.py'),
            'check','--target',str(self.output/'gate-cex-trade'),'--package','--contract',str(ROOT/'tests/cex/cli-contract.json')],
            env={'PATH':os.defpath,'HOME':str(self.base)},text=True,capture_output=True,timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'PASS')

    def test_real_checker_rejects_protection_amendment_without_parent_value(self):
        # Exercise parsing, packaged-file inspection and the actual CLI entry point.
        self.edit('references/spot-commands.md', lambda text: text+'\n```text\ngate-cli cex spot order amend --pair BTC_USDT --id 123 --stop-loss-json \'{}\'\n```\n')
        result = subprocess.run([sys.executable, '-I', str(ROOT/'scripts/cex_skills.py'),
            'check', '--target', str(self.target), '--package', '--contract', str(ROOT/'tests/cex/cli-contract.json')],
            env={'PATH':os.defpath, 'HOME':str(self.base)}, text=True, capture_output=True, timeout=30)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(any(f['rule']=='C8' for f in json.loads(result.stdout)['findings']))




class BotProfileBuildTests(unittest.TestCase):
    """Exercise selected Bot builds through the canonical tool without hiding other-profile failures."""

    def test_selected_profile_uses_the_canonical_checker_and_manifest(self):
        """The one-profile entry retains model dependencies and byte-identical shared rules."""
        with tempfile.TemporaryDirectory(prefix='bot-canonical-') as folder:
            output = Path(folder) / 'packages'
            result = TOOLS.build(ROOT, output, CONTRACT, profiles=('bot',))
            self.assertEqual(result['packages'], 1)
            target = output / 'gate-cex-bot'
            self.assertEqual(TOOLS.inspect(target, CONTRACT, package=True)['status'], 'PASS')
            for filename in TOOLS.SHARED:
                self.assertEqual((target/'references/_shared/cex'/filename).read_bytes(),
                                 (ROOT/'skills/_shared/cex'/filename).read_bytes())
            manifest = json.loads((target/'manifest.json').read_text())
            self.assertEqual(manifest['command_contract_sha256'], TOOLS.contract_digest(CONTRACT))
            self.assertNotIn('cli_commit', manifest)
            for filename in ('spot-grid.md', 'futures-grid.md', 'martingale.md', 'bot-lifecycle.md'):
                self.assertIn('references/models/'+filename, manifest['files'])

    def test_invalid_profile_selection_has_no_output(self):
        """Invalid or duplicate selections cannot bypass or partially publish the build."""
        for profiles in ((), ('unknown-profile',), ('bot', 'bot')):
            with self.subTest(profiles=profiles), tempfile.TemporaryDirectory(prefix='bot-selection-') as folder:
                output = Path(folder)/'packages'
                with self.assertRaises(ValueError):
                    TOOLS.build(ROOT, output, CONTRACT, profiles=profiles)
                self.assertFalse(output.exists())

    def test_package_validation_failure_cleans_staging(self):
        """A rejection after copy/link rewriting is still transactional, not just source prevalidation."""
        from unittest.mock import patch
        with tempfile.TemporaryDirectory(prefix='bot-late-failure-') as folder:
            output = Path(folder)/'packages'
            real_inspect = TOOLS.inspect
            def reject_package(target, contract, package=False):
                """Keep real source checks and inject only the final package rejection."""
                return {'status':'FAIL','findings':[]} if package else real_inspect(target, contract)
            with patch.object(TOOLS, 'inspect', side_effect=reject_package):
                with self.assertRaises(ValueError):
                    TOOLS.build(ROOT, output, CONTRACT, profiles=('bot',))
            self.assertFalse(output.exists())
            self.assertFalse(list(Path(folder).glob('.cex-build-*')))


if __name__ == '__main__':
    unittest.main(verbosity=2)
