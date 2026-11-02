#!/usr/bin/env python3
"""Build isolated CEX packages and check one skill against an independent contract.

This tool never runs a documented command or certifies legal/product eligibility.
The agent-led gate-cex-skill-audit supplies the semantic and safety review.
"""
import argparse
import ast
from collections import deque
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
from functools import lru_cache
import hashlib
import ipaddress
import json
from pathlib import Path
import re
import shlex
import shutil
import sys
import tempfile
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
import yaml

PARSER = MarkdownIt('commonmark').enable('table')
MAX_FILE = 1024 * 1024
MAX_TOTAL = 20 * MAX_FILE
MAX_FILES = 10000
SHARED = ('preflight.md', 'cli-setup.md', 'cli-auth.md', 'execution-cli.md', 'safety.md', 'templates.md')
PUBLIC_STREAM_SCRIPTS = frozenset('scripts/' + name for name in (
    'public-market-stream.py', 'futures-market-stream.py', 'test_futures_market_stream.py',
))
WORKFLOWS = {'trade':'order', 'earn':'earn', 'assets':'asset', 'subaccount':'subaccount', 'affiliate':'affiliate', 'bot':'bot'}
ROOT_FLAGS = {'format', 'profile', 'debug', 'verbose', 'max-output-bytes', 'api-key', 'api-secret', 'help', 'version'}


def public_dependency_errors(body):
    """Reject private runtime dependencies without fetching URLs or echoing secrets.

    Engineering provenance belongs in review evidence, not installable instructions.
    Scan prose and code as well as clickable links so plain addresses cannot bypass it.
    """
    errors = set()
    decoded = unquote(body)
    # Runtime references are limited to the public providers used by these packages.
    # A closed set avoids publishing company-specific infrastructure deny lists.
    public_hosts = {'github.com', 'raw.githubusercontent.com', 'agentskills.io',
                    'api.gateio.ws', 'fx-ws.gateio.ws', 'op-ws.gateio.live', 'gate.com', 'www.gate.com'}
    for host in re.findall(r'(?i)\b(?:[a-z0-9-]+\.)+(?:com|net|org|io|ws|cn|link|xyz|invalid|internal|local|lan)\b', decoded):
        if host.lower() not in public_hosts:
            errors.add('unapproved reference host in runtime content')
    for literal in re.findall(r'(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])', decoded):
        try:
            if not ipaddress.ip_address(literal).is_global:
                errors.add('non-public service address in runtime content')
        except ValueError:
            pass  # Version-like text that is not an address has no network meaning.
    # Scan literal secrets without reflecting their values into diagnostic output.
    if (re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', decoded)
            or re.search(r'\b(?:ghp_|glpat-|sk-proj-)[A-Za-z0-9_-]{12,}', decoded)
            or re.search(r'\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', decoded)
            or re.search(r'''(?i)["']?(?:api[_-]?(?:key|secret)|password|access_token|refresh_token|client_secret)["']?\s*[:=]\s*["'][^"'<>\s]{8,}["']''', decoded)):
        errors.add('credential literal in runtime content')
    # Anchor at a path boundary: /api/v4/cfd/users/me is an API route, not a home.
    if re.search(r'(?i)(?<![\w/])/(?:Users|home)/[\w.-]+|[A-Z]:[\\/]Users[\\/][\w.-]+', decoded):
        errors.add('personal absolute path in runtime content')
    for value in re.findall(r'https?://[^\s<>`"\)]+', decoded, re.I):
        try:
            host = (urlsplit(value).hostname or '').rstrip('.').lower()
            if host not in public_hosts:
                errors.add('unapproved reference host in runtime content')
            private = host == 'localhost' or host.endswith(('.localhost', '.local', '.internal', '.lan'))
            try:
                private = private or not ipaddress.ip_address(host).is_global
            except ValueError:
                private = private or '.' not in host
            if private:
                errors.add('non-public service address in runtime content')
        except ValueError:
            errors.add('malformed service address in runtime content')
    if re.search(r'feature/[A-Za-z0-9_.-]+|(?:CLI baseline|Command contract):[^\n]*(?:[0-9a-f]{40}|`v\d+\.)|git clone[^\n]*(?:--branch\b|\s-b\s)|git checkout\s+--detach\s+[0-9a-f]{7,40}', decoded, re.I):
        errors.add('fixed development branch/revision in public CLI instructions')
    if re.search(r'(?i)\bCLI(?:[_ -]+(?:baseline|commit|revision))?\s*[:=@]?\s*[`\"\x27]?[0-9a-f]{7,40}\b', decoded):
        errors.add('fixed development branch/revision in public CLI instructions')
    return sorted(errors)


def contract_digest(contract):
    """Bind package validation to engineering evidence without publishing private refs."""
    data = json.dumps(contract, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(data).hexdigest()


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys rather than silently accepting the last value."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key, value in node.value:
        name = loader.construct_object(key, deep=deep)
        if name in result:
            raise ValueError('duplicate YAML key: ' + str(name))
        result[name] = loader.construct_object(value, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def contained(path, root):
    return path.resolve().is_relative_to(root.resolve())


def file_set(target, source=False):
    """Bound input before parsing; links and symlinks cannot expand the read boundary."""
    files = []
    total = 0
    for path in target.rglob('*'):
        if path.name == '.DS_Store':
            continue
        if path.is_symlink():
            raise ValueError('symbolic link is not allowed: ' + str(path))
        if not path.is_file():
            continue
        if not contained(path, target):
            raise ValueError('file escapes target')
        if (source and target.name == 'gate-cex-trade'
                and path.parent == target / 'scripts/__pycache__' and path.suffix == '.pyc'):
            continue
        size = path.stat().st_size
        total += size
        files.append(path)
        if size > MAX_FILE or total > MAX_TOTAL or len(files) > MAX_FILES:
            raise ValueError('input resource limit exceeded')
        if path.suffix not in ('.md', '.json'):
            if target.name != 'gate-cex-trade' or path.relative_to(target).as_posix() not in PUBLIC_STREAM_SCRIPTS:
                raise ValueError('unexpected executable/binary content: ' + str(path))
            try:
                ast.parse(path.read_text(), filename=str(path))
            except (SyntaxError, UnicodeError) as error:
                raise ValueError('invalid public stream Python syntax: ' + str(path)) from error
    return sorted(files)


def tokens(text):
    return PARSER.parse(text)


class HTMLLinks(HTMLParser):
    """Extract declared HTML references without evaluating markup or scripts."""
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attributes):
        self.hrefs.extend(value for key,value in attributes if key in ('href','src') and value)


def links(text):
    for block in tokens(text):
        html = HTMLLinks()
        if block.type == 'html_block':
            html.feed(block.content)
        for node in block.children or []:
            if node.type == 'link_open':
                yield node.attrGet('href')
            elif node.type == 'image':
                yield node.attrGet('src')
            elif node.type == 'html_inline':
                html.feed(node.content)
        yield from html.hrefs


@lru_cache(maxsize=256)
def anchors(text):
    result = set(re.findall(r'<a\s+id=["\']([^"\']+)["\']', text))
    seen = {}
    ts = tokens(text)
    for index, node in enumerate(ts):
        if node.type == 'heading_open':
            content = ts[index + 1].content.replace('`', '')
            slug = re.sub(r'[^\w\- ]', '', content.lower()).replace(' ', '-')
            number = seen.get(slug, 0)
            seen[slug] = number + 1
            result.add(slug + (f'-{number}' if number else ''))
    return result


def target_link(path, href):
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return None, None
    # Decode before containment checks so encoded traversal cannot bypass them.
    return (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve(), unquote(parsed.fragment)


def header(text):
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    if not match:
        raise ValueError('SKILL.md needs YAML frontmatter')
    value = yaml.load(match[1], Loader=UniqueLoader)
    if not isinstance(value, dict):
        raise ValueError('frontmatter must be a mapping')
    return value


def command_sections(text):
    return {m[1]:m[2] for m in re.finditer(r'^### `(gate-cli [^`]+)`\n(.*?)(?=^### |^## |\Z)', text, re.M | re.S)}


def invocation_values(argv, spec):
    """Parse documented argv as data; never invoke a shell or the business CLI."""
    values = {}
    types = {flag['name']:flag['type'] for flag in spec['flags']}
    required = {flag['name'] for flag in spec['flags'] if flag['required']}
    for index, arg in enumerate(argv):
        if not arg.startswith('--'):
            continue
        name, equal, value = arg[2:].partition('=')
        has_value = bool(equal)
        if not equal:
            has_value = index+1 < len(argv) and not argv[index+1].startswith('--')
            value = argv[index+1] if has_value else ''
        # Optional strings can carry explicit empty values (--show-status '').
        # Retain the existing nonempty guard for required business inputs.
        if (types.get(name) != 'bool' and name not in ('help','version','debug','verbose')
                and (not has_value or not value and (types.get(name) != 'string' or name in required))):
            raise ValueError('missing value for --'+name)
        values[name] = value
    return values


def alpha_variant_errors(command, values):
    """Check concrete Alpha examples; templates and live eligibility stay separate."""
    if command not in ('gate-cli cex alpha order quote', 'gate-cli cex alpha order place'):
        return []
    errors = []
    literal = lambda value: bool(value) and not any(char in value for char in '<>$[]')
    side, mode = values.get('side',''), values.get('gas-mode','speed')
    if literal(side) and side not in ('buy','sell'):
        errors.append('Alpha side must be buy or sell')
    if literal(mode) and mode not in ('speed','custom'):
        errors.append('Alpha gas mode must be speed or custom')
    if mode == 'custom' and not values.get('slippage'):
        errors.append('Alpha custom mode requires explicit percentage slippage')
    for name in ('amount','slippage'):
        value = values.get(name,'')
        if not literal(value):
            continue
        try:
            number = Decimal(value)
            valid = number.is_finite() and (number > 0 if name == 'amount' else number >= 0)
        except InvalidOperation:
            valid = False
        if not valid:
            errors.append('Alpha --'+name+' must be a finite decimal with a valid sign')
    return errors


def _decimal_value(value, positive=False):
    """Validate the CLI's bounded decimal strings without a float conversion."""
    if not isinstance(value, str) or len(value) > 80 or not re.fullmatch(r'-?[0-9]+(?:\.[0-9]+)?', value):
        raise ValueError('expected a bounded decimal string')
    result = Decimal(value)
    if positive and result <= 0:
        raise ValueError('expected a positive decimal')
    return result


def _trading_json(raw):
    """Parse documentation as data; malformed intent must not become clear/default."""
    def unique(pairs):
        result, seen = {}, set()
        for key, value in pairs:
            if not key.isascii() or key.lower() in seen:
                raise ValueError('ambiguous JSON key')
            seen.add(key.lower())
            result[key] = value
        return result

    def bounded(value, depth=0):
        if depth > 32 or value is None:
            raise ValueError('null field or excessive nesting')
        if isinstance(value, dict):
            for child in value.values():
                bounded(child, depth+1)
        elif isinstance(value, list):
            for child in value:
                bounded(child, depth+1)

    if len(raw.encode()) > 65536:
        raise ValueError('JSON exceeds 64KiB')
    value = json.loads(raw, object_pairs_hook=unique, parse_float=Decimal)
    if not isinstance(value, dict):
        raise ValueError('expected a JSON object')
    bounded(value)
    return value


def trade_variant_errors(command, values):
    """Check concrete new trade variants against the independently reviewed CLI.

    This validates documented argv, not permissions, live eligibility or execution.
    Diagnostic text never echoes an untrusted JSON value or credential.
    """
    errors = []
    concrete = lambda value: isinstance(value, str) and not re.search(r'<[^>]+>|\$\{?\w', value)

    def enabled(name):
        if name not in values:
            return False
        value = values[name]
        if value not in ('', 'true', 'false'):
            errors.append('--'+name+' must use true or false')
        return value in ('', 'true')

    def integer(name, low, high):
        if name not in values or not concrete(values[name]):
            return
        try:
            value = int(values[name])
            if not low <= value <= high:
                raise ValueError('range')
        except ValueError:
            errors.append('--'+name+' is outside the supported integer range')

    if command.startswith('gate-cli cex spot order '):
        account = values.get('account', '')
        if concrete(account) and account not in ('', 'spot', 'margin', 'unified', 'cross_margin'):
            errors.append('invalid order account')
        if enabled('auto-borrow') and concrete(account) and account not in ('margin', 'unified', 'cross_margin'):
            errors.append('automatic borrowing needs an explicit eligible account')
        if enabled('auto-repay') and concrete(account) and account not in ('unified', 'cross_margin'):
            errors.append('order automatic repayment needs unified or cross_margin')
        side = command.split()[-1]
        # The deployed API requires an explicit price or amount even when only
        # protection changes. Do not teach agents to resend an inferred stale value.
        if side == 'amend' and any(values.get(flag, 'null').strip() != 'null'
                                  for flag in ('stop-profit-json', 'stop-loss-json')):
            if not values.get('price') and not values.get('amount'):
                errors.append('protection amendment needs an explicitly authorized --price or --amount')
        for flag, profit in (('stop-profit-json', True), ('stop-loss-json', False)):
            raw = values.get(flag)
            if raw is None or not concrete(raw) or raw.strip() == 'null':
                continue
            try:
                protection = _trading_json(raw)
                if not protection:
                    if side != 'amend':
                        raise ValueError('clear only applies to amendment')
                    continue
                if set(protection)-{'trigger_price', 'order_price'}:
                    raise ValueError('unknown protection key')
                trigger = _decimal_value(protection.get('trigger_price'), positive=True)
                if 'order_price' in protection and _decimal_value(protection['order_price']) < 0:
                    raise ValueError('negative execution price')
                if side in ('buy', 'sell'):
                    if not values.get('price'):
                        raise ValueError('limit order required')
                    if concrete(values['price']):
                        price = _decimal_value(values['price'], positive=True)
                        above = (side == 'buy') == profit
                        if (above and trigger <= price) or (not above and trigger >= price):
                            raise ValueError('wrong trigger side')
            except (ValueError, TypeError, InvalidOperation, RecursionError):
                errors.append('invalid attached protection or unsafe clear semantics')

    if command == 'gate-cli cex options order create':
        integer('size', -(2**63), 2**63-1)
        if concrete(values.get('size')):
            try:
                size = int(values['size'])
                close = enabled('close')
                if (close and size != 0) or (not close and size == 0):
                    errors.append('full close requires --close --size 0; other orders need nonzero size')
            except ValueError:
                pass  # The integer-range diagnostic above owns this error.
        if values.get('price') == '0' and values.get('tif') != 'ioc':
            errors.append('options market execution requires price 0 with tif ioc')

    if command == 'gate-cli cex spot pov create':
        if concrete(values.get('side')) and values['side'] not in ('buy', 'sell'):
            errors.append('POV side must be buy or sell')
        if concrete(values.get('participation-rate')) and values['participation-rate'] not in ('5', '10', '20', '40'):
            errors.append('POV participation percentage must be 5, 10, 20 or 40')
        if concrete(values.get('ttl')) and values['ttl'] not in ('1h', '6h', '12h', '1d', '2d', '3d', '4d', '5d', '6d', '7d'):
            errors.append('invalid POV lifetime')
        for field in ('amount', 'limit-price', 'trigger-price'):
            if field in values and concrete(values[field]):
                try:
                    _decimal_value(values[field], positive=True)
                except (ValueError, InvalidOperation):
                    errors.append('POV --'+field+' must be a positive decimal string')
    if command == 'gate-cli cex spot pov list':
        integer('page', 1, 100)
        integer('limit', 1, 1000)
    if command.endswith('market rpi-orderbook'):
        integer('limit', 1, 50 if ' cex futures ' in command else 100)
    if command == 'gate-cli cex futures market contracts-all':
        integer('limit', 1, 1000)
        integer('offset', 0, 100000)

    if command == 'gate-cli cex futures chase create' and concrete(values.get('json')):
        try:
            request = _trading_json(values['json'])
            string_fields = {'contract', 'settle', 'amount', 'price_limit', 'offset_limit', 'text', 'price_gap_value', 'pos_margin_mode', 'position_mode'}
            bool_fields = {'reduce_only', 'is_dual_mode'}
            int_fields = {'price_type', 'price_gap_type'}
            if set(request)-(string_fields | bool_fields | int_fields):
                raise ValueError('unknown chase field')
            for key, value in request.items():
                kind = str if key in string_fields else bool if key in bool_fields else int
                if type(value) is not kind:
                    raise ValueError('wrong field type')
            if not re.fullmatch(r'[A-Za-z0-9_.-]{1,128}', request.get('contract', '')) or request.get('contract') in ('.', '..'):
                raise ValueError('invalid contract')
            if _decimal_value(request.get('amount')) == 0:
                raise ValueError('zero amount')
            price = _decimal_value(request.get('price_limit'))
            if price < 0:
                raise ValueError('negative price')
            if request.get('offset_limit'):
                _decimal_value(request['offset_limit'], positive=True)
                if price != 0:
                    raise ValueError('conflicting limits')
            price_type = request.get('price_type', 0)
            if price_type not in (0, 1, 2):
                raise ValueError('invalid price type')
            if price_type == 2:
                if request.get('price_gap_type') not in (1, 2):
                    raise ValueError('missing gap type')
                _decimal_value(request.get('price_gap_value'), positive=True)
            elif request.get('price_gap_type', 0) != 0 or request.get('price_gap_value', ''):
                raise ValueError('unexpected gap')
            if request.get('pos_margin_mode', '') not in ('', 'isolated', 'cross') or request.get('position_mode', '') not in ('', 'single', 'dual', 'dual_plus'):
                raise ValueError('invalid position mode')
            if request.get('settle') and values.get('settle') and request['settle'] != values['settle']:
                raise ValueError('settlement mismatch')
        except (ValueError, TypeError, InvalidOperation, RecursionError):
            errors.append('invalid chase request; verify types, required fields and execution variants')
    if command == 'gate-cli cex futures chase stop' and (not values.get('id')) == (not values.get('text')):
        errors.append('chase stop needs exactly one of id or text')
    if command == 'gate-cli cex futures chase list':
        for name, low, high in [('page',1,100000), ('limit',1,100), ('sort-by',1,2), ('side',0,2), ('reduce-only',0,2)]:
            integer(name, low, high)
        start, end = values.get('from', '0'), values.get('to', '0')
        finished = enabled('finished')
        if concrete(start) and concrete(end):
            try:
                lower, upper = int(start), int(end)
                if not 0 <= lower <= upper <= 2**63-1 or (lower == 0) != (upper == 0) or (finished and lower == 0):
                    raise ValueError('invalid range')
            except ValueError:
                errors.append('finished/ranged chase history requires valid paired time bounds')
    if command == 'gate-cli cex unified config leverage-set-all' and concrete(values.get('leverage')):
        try:
            _decimal_value(values['leverage'], positive=True)
        except (ValueError, InvalidOperation):
            errors.append('leverage must be a positive decimal string')
    if command == 'gate-cli cex unified loan quick-repay':
        for name in ('debt-currencies', 'available-currencies'):
            if not concrete(values.get(name)):
                continue
            currencies = values[name].split(',')
            if not 1 <= len(currencies) <= 100 or len(set(currencies)) != len(currencies) or any(not re.fullmatch(r'[A-Za-z0-9_.-]{1,128}', c) or c in ('.', '..') for c in currencies):
                errors.append('repayment currency lists need 1 to 100 unique identifiers')
    if command == 'gate-cli cex tradfi order log':
        integer('log-id', 1, 2**63-1)
    return errors


def model_contract_errors(body, spec):
    """Check reviewed model fields as well as command flags, without executing code.

    A CLI help table cannot establish a nested request or response field's type.
    Only independently reviewed fields belong in this development contract.
    """
    match = re.search(r'^### ' + re.escape(spec['model']) + r'\s*\n(.*?)(?=^#{1,3} |\Z)',
                      body, re.M | re.S)
    if not match:
        return ['required model is missing: ' + spec['model']]
    fields = {}
    for name, optional, kind in re.findall(r'`([A-Za-z_]\w*)(\?)?`:\s*`([^`]+)`', match[1]):
        fields.setdefault(name, []).append((kind, bool(optional)))
    errors = []
    for name, expected in spec['fields'].items():
        actual = fields.get(name, [])
        if (len(actual) != 1 or actual[0][0] != expected['type']
                or (expected.get('required') and actual[0][1])):
            errors.append('model field contract differs: ' + spec['model'] + '.' + name)
    return errors


def request_contract_errors(command, values, contract):
    """Reject concrete examples that lose a reviewed required request field.

    Templates remain data. Strict integer checks exclude bool/float coercion;
    diagnostic messages never include the untrusted body or secret values.
    """
    raw = values.get('json')
    specs = [spec for spec in contract.get('model_contracts', [])
             if spec.get('request_command') == command]
    if not specs or raw is None or re.search(r'<[^>]+>|\$\{?\w', raw):
        return []
    try:
        request = _trading_json(raw)
        for spec in specs:
            for name, field in spec['fields'].items():
                if name not in request:
                    if field.get('required'):
                        raise ValueError('missing field')
                    continue
                value = request[name]
                if field['type'] == 'int32' and (type(value) is not int or not -(2**31) <= value < 2**31):
                    raise ValueError('invalid integer')
                if 'enum' in field and value not in field['enum']:
                    raise ValueError('invalid enum')
    except (ValueError, TypeError, InvalidOperation, RecursionError):
        return ['request model field mismatch for ' + command]
    return []


def inspect(target, contract, package=False):
    """Return deterministic findings only; prose meaning is reviewed by the auditor."""
    target = target.absolute()
    if target.name == 'SKILL.md':
        target = target.parent
    findings = []
    def fail(rule, path, message):
        findings.append({'rule':rule, 'file':str(path), 'message':message})
    if target.is_symlink() or not target.is_dir():
        raise ValueError('target must be an existing, non-symlink skill directory')
    files = file_set(target, source=not package)
    entry = target / 'SKILL.md'
    if not entry.is_file():
        return {'status':'FAIL', 'findings':[{'rule':'C1', 'file':str(entry), 'message':'missing SKILL.md'}]}
    text = entry.read_text()
    try:
        metadata = header(text)
    except (ValueError, yaml.YAMLError) as error:
        fail('C1', entry, str(error))
        metadata = {}
    name = metadata.get('name')
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64 or name != target.name:
        fail('C1', entry, 'invalid or mismatched skill name')
    description = metadata.get('description')
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        fail('C1', entry, 'description must contain 1-1024 characters')
    if 'compatibility' in metadata and (not isinstance(metadata['compatibility'], str) or len(metadata['compatibility']) > 500):
        fail('C1', entry, 'invalid compatibility field')
    if 'metadata' in metadata and (not isinstance(metadata['metadata'], dict) or any(not isinstance(k,str) or not isinstance(v,str) for k,v in metadata['metadata'].items())):
        fail('C1', entry, 'metadata must map strings to strings')
    profile = name.removeprefix('gate-cex-') if isinstance(name,str) else ''
    if profile not in contract['profiles']:
        fail('C2', entry, 'unknown six-business profile')
        return {'status':'FAIL','findings':findings}
    if profile == 'trade':
        spot = target / 'references/spot-commands.md'
        if spot.is_file():
            # Guard a known semantic regression separately from correct flag tables.
            claim = spot.read_text()
            if re.search(r'(?is)Simple `spot\.order\.buy`/sell.{0,240}expose no.{0,100}--account|Ordinary get/list/cancel.{0,180}lack an account-selection', claim):
                fail('C5', spot, 'obsolete unconditional account-capability denial contradicts current flags')
    shared = target / 'references/_shared/cex' if package else target.parent / '_shared/cex'
    expected = [target / 'references' / (topic + '-commands.md') for topic in contract['profiles'][profile]]
    expected.append(target / 'references' / (WORKFLOWS[profile] + '-workflows.md'))
    # Extra product/workflow files must not smuggle retired or wrongly owned domains
    # into an otherwise complete package. Optional prose/model references remain valid.
    for path in files:
        if path.parent == target/'references' and path.name.endswith(('-commands.md','-workflows.md')) and path not in expected:
            fail('C2',path,'product/workflow reference is outside the approved profile')
    for path in expected + [shared / x for x in SHARED]:
        if not path.is_file():
            fail('C3', path, 'required reference is missing')
        elif path.stat().st_size < 180:
            fail('C3', path, 'reference has no substantive contract')
    # Source mode may read only the explicitly approved shared CEX dependency.
    if shared.is_symlink() or (not package and not contained(shared,target.parent)):
        raise ValueError('shared dependency escapes its approved directory')
    shared_files = [shared / x for x in SHARED if (shared / x).is_file()]
    all_files = sorted(set(files + shared_files))
    text_by_path = {}
    total = 0
    for path in all_files:
        if path.is_symlink() or path.stat().st_size > MAX_FILE:
            fail('C6', path, 'invalid shared dependency or file size')
            continue
        total += path.stat().st_size
        if total > MAX_TOTAL:
            fail('C6', path, 'input resource limit exceeded')
            break
        try:
            text_by_path[path.resolve()] = path.read_text()
        except (UnicodeError, OSError):
            fail('C6', path, 'file is not readable UTF-8')
    edges = {}
    for path, body in text_by_path.items():
        # JSON attachments and manifests are just as public as Markdown references.
        scan_body = body
        if path.suffix == '.json':
            try:
                # Decode escaped keys/strings so JSON cannot hide a private reference.
                scan_body = json.dumps(json.loads(body), ensure_ascii=False)
            except (ValueError, RecursionError):
                fail('C6', path, 'invalid JSON attachment')
        for message in public_dependency_errors(scan_body):
            fail('C6', path, message)
        if path.suffix != '.md':
            continue
        if re.search(r'[\u3400-\u9fff]', body):
            fail('C7', path, 'non-English text needs an explicit auditor-reviewed localized-data exception')
        if re.search(r'(?im)^\s*(?:TODO|TBD|FIXME)\b', body):
            fail('C3', path, 'unfinished authoring placeholder')
        edges[path] = []
        for href in links(body):
            dest, fragment = target_link(path, href)
            if dest is None:
                if urlsplit(href).scheme not in ('http','https','mailto') or urlsplit(href).netloc == '':
                    if urlsplit(href).scheme != 'mailto':
                        fail('C6',path,'unsafe external link scheme: '+href)
                continue
            allowed = contained(dest,target) or (not package and contained(dest,shared))
            if not allowed or not dest.is_file() or dest.is_symlink() or dest not in text_by_path:
                fail('C6',path,'missing or escaping link: '+href)
                continue
            if fragment and fragment not in anchors(text_by_path[dest]):
                fail('C6',path,'missing anchor: '+href)
            edges[path].append(dest)
        if re.search(r'(?i)\bmcp\b|\bmcp__[a-z_]+\b|\bcex_[a-z_]+\s*\(', body):
            fail('C2',path,'business runtime content must be CLI-only')
        if re.search(r'<a\s+id=["\']cli-cex-',body):
            fail('C2',path,'obsolete module-boundary anchor; use action/model anchors')
        for block in tokens(body):
            if block.type != 'fence' or block.info not in ('bash','sh','shell','text'):
                continue
            for line in block.content.splitlines():
                if line.startswith('#'):
                    continue
                if re.search(r'\beval\b|curl\s+.*\|\s*(?:sh|bash)|--(?:api-key|api-secret|password)(?:=|\s+)[^<\s]',line):
                    fail('C8',path,'unsafe executable example')
                if not line.startswith('gate-cli cex '):
                    continue
                try:
                    argv = shlex.split(line)
                except ValueError:
                    fail('C9',path,'malformed command quoting')
                    continue
                registry = {item['path']:item for item in contract['commands']}
                candidates = [x for x in registry if argv[:len(x.split())] == x.split()]
                if not candidates:
                    # Unknown examples may contain credentials. Point to the file
                    # without reflecting the untrusted argv into audit output.
                    fail('C4',path,'unknown or retired CEX command in executable example')
                    continue
                command = max(candidates,key=len)
                spec = registry[command]
                flags = {f['name'] for f in spec['flags']} | ROOT_FLAGS
                provided = {arg[2:].split('=')[0] for arg in argv[len(command.split()):] if arg.startswith('--')}
                if provided - flags:
                    fail('C4',path,'unknown flags for '+command+': '+','.join(sorted(provided-flags)))
                missing = {f['name'] for f in spec['flags'] if f['required']} - provided
                if missing and '[flags]' not in line and 'help' not in provided:
                    fail('C4',path,'missing registered required flags: '+','.join(sorted(missing)))
                if '[flags]' not in line and 'help' not in provided:
                    try:
                        values = invocation_values(argv[len(command.split()):],spec)
                    except ValueError as error:
                        fail('C4',path,str(error))
                    else:
                        for message in (alpha_variant_errors(command,values) + trade_variant_errors(command,values)
                                        + request_contract_errors(command, values, contract)):
                            fail('C8',path,message)
                if '[flags]' not in line and 'help' not in provided and command == 'gate-cli cex spot order buy' and 'price' not in provided and ('quote' not in provided or 'amount' in provided):
                    fail('C8',path,'market buy must use quote spending, not base amount')
    # Model rules share the same authority as argv checks in source and installed
    # packages; a valid manifest must not hide a wrong nested field contract.
    for spec in contract.get('model_contracts', []):
        if spec['owner'] != name:
            continue
        path = (target / 'references' / spec['reference']).resolve()
        for message in model_contract_errors(text_by_path.get(path, ''), spec):
            fail('C5', path, message)
    reachable = set()
    pending = deque([(entry.resolve(),0)])
    while pending:
        path,depth = pending.popleft()
        if path in reachable:
            continue
        if depth > 8:
            fail('C6',path,'reference depth exceeds eight levels')
            continue
        reachable.add(path)
        pending.extend((dest,depth+1) for dest in edges.get(path, []))
    for path in expected:
        if path.is_file() and path.resolve() not in reachable:
            fail('C6',path,'required business reference is not reachable from entry')
        if path.name.endswith('-commands.md') and path.is_file() and path.resolve() not in edges.get(entry.resolve(),[]):
            fail('C2',path,'product reference needs a direct intent route from SKILL.md')
    if package and (target/'manifest.json').exists():
        manifest = json.loads((target/'manifest.json').read_text())
        hashes = {p.relative_to(target).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.name != 'manifest.json'}
        if hashes != manifest.get('files') or manifest.get('command_contract_sha256') != contract_digest(contract) or 'cli_commit' in manifest:
            fail('C6',target/'manifest.json','package contents or contract digest differ; rebuild legacy manifests')
    # A complete flag table does not establish coverage of conditional behavior.
    for variant in contract.get('required_variants', []):
        if variant['owner'] != name:
            continue
        path = (target/'references'/variant['reference']).resolve()
        body = text_by_path.get(path, '')
        marker = re.search(r"<a\s+id=[\"']"+re.escape(variant['anchor'])+r"[\"']></a>", body)
        headings = body[marker.end():].split('\n## ', 2) if marker else []
        section = headings[1] if len(headings) > 1 else ''
        if variant['anchor'] not in anchors(body) or len(section.strip()) < 180:
            fail('C5',path,'missing substantive parameter variant: '+variant['anchor'])
    actual = {}
    ids = set()
    for path in files:
        if path.suffix != '.md':
            continue
        body = text_by_path.get(path.resolve(),'')
        for command, section in command_sections(body).items():
            if command in actual:
                fail('C2',path,'duplicate canonical command: '+command)
            actual[command] = (path,section)
        for operation in re.findall(r'^Operation ID: `([^`]+)`',body,re.M):
            if operation in ids:
                fail('C2',path,'duplicate operation ID: '+operation)
            ids.add(operation)
    expected_commands = {x['path']:x for x in contract['commands'] if x['owner'] == name}
    # Trade reuses this asset-owned ledger read; never share a write owner.
    if name == 'gate-cex-trade':
        for spec in contract['commands']:
            if (spec['path'] == 'gate-cli cex stock account transactions'
                    and spec['owner'] == 'gate-cex-assets' and spec['effect'] == 'read'):
                expected_commands[spec['path']] = dict(spec, reference='stocks-commands.md')
    for command,spec in expected_commands.items():
        if command not in actual:
            fail('C4',entry,'implemented in-scope command is undocumented: '+command)
            continue
        path,section = actual[command]
        if path.name != spec['reference']:
            fail('C2',path,'command belongs in '+spec['reference'])
        if f"Operation ID: `{spec['operation_id']}`" not in section or f"Effect: **{spec['effect']}**" not in section:
            fail('C4',path,'operation identity or effect mismatch: '+command)
        listed = dict(re.findall(r'^\| `--([^`]+)` \| `([^`]+)`', section, re.M))
        flag_types = {f['name']:f['type'] for f in spec['flags']}
        if listed != flag_types:
            fail('C4',path,'flag table differs from Cobra: '+command)
        rows = {r[0]:r for r in re.findall(r'^\| `--([^`]+)` \| `([^`]+)` \| ([^|]+) \| ([^|]+) \|',section,re.M)}
        for flag in spec['flags']:
            row = rows.get(flag['name'])
            if not row:
                continue
            default = row[3].strip().strip('`')
            if default == 'Unset':
                default = ''
            required = row[2].strip()
            if default != flag['default'] or (flag['required'] and required != 'Yes') or (not flag['required'] and required not in ('No','Conditional')):
                fail('C4',path,'flag requirement/default differs from registration: '+command+' --'+flag['name'])
        if 'Returns:' not in section:
            fail('C5',path,'missing output contract: '+command)
        api = re.search(r'^API:\s*(.+)$',section,re.M)
        if not api or api[1] != spec['api']:
            fail('C4',path,'API method/path/access differs from approved contract: '+command)
        if '(private)' in spec['api'] and re.search(r'(?i)\bpublic\b|\bno auth(?:entication)?\b',section.split('```',1)[0]):
            fail('C5',path,'summary contradicts private CLI access: '+command)
    for command,(path,_) in actual.items():
        if command not in expected_commands:
            fail('C4',path,'undesignated command implementation: '+command)
    return {'status':'FAIL' if findings else 'PASS','level':'offline-structural-and-contract', 'target':name,'mode':'package' if package else 'source','files':len(all_files),'commands':len(expected_commands),'findings':findings,'not_evaluated':['agent behavior','backend integration','product eligibility','human compliance approval','jurisdiction-specific legal applicability']}


def build(source, output, contract, profiles=None):
    """Atomically publish selected profiles through the same source/package checks as the six-profile build."""
    selected = tuple(contract['profiles']) if profiles is None else tuple(profiles)
    if not selected or len(set(selected)) != len(selected) or any(p not in contract['profiles'] for p in selected):
        raise ValueError('select unique, known CEX profiles')
    # Refuse recursive publication before mkdir or staging can change any input.
    source, output = source.resolve(), output.absolute()
    maintained = source / 'skills'
    if output.resolve().is_relative_to(maintained.resolve()):
        raise ValueError('build output must be outside the maintained Skill source')
    for relative in [Path('skills') / ('gate-cex-' + p) for p in selected] + [Path('skills/_shared/cex')]:
        target = source / relative
        if any(parent.is_symlink() for parent in (target, *target.parents) if parent.is_relative_to(source)):
            raise ValueError('source symlinks are not permitted')
    if output.exists() or output.is_symlink():
        raise ValueError('output already exists; use a new directory instead of overwriting')
    output.parent.mkdir(parents=True,exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.cex-build-',dir=output.parent))
    try:
        for profile in selected:
            name = 'gate-cex-' + profile
            target = source / 'skills' / name
            result = inspect(target,contract)
            if result['status'] != 'PASS':
                raise ValueError(json.dumps(result,ensure_ascii=False))
            destination = staging / name
            shutil.copytree(target,destination,ignore=shutil.ignore_patterns('.DS_Store', '__pycache__'))
            shared = source / 'skills/_shared/cex'
            shutil.copytree(shared,destination / 'references/_shared/cex',ignore=shutil.ignore_patterns('.DS_Store'))
            for file in destination.rglob('*.md'):
                original = target / file.relative_to(destination)
                if 'references/_shared/cex' in str(file.relative_to(destination)):
                    continue
                body = file.read_text()
                replacements = {}
                # Use parsed link nodes; preserve original Markdown text and formatting.
                for href in links(body):
                    dest,fragment = target_link(original,href)
                    if dest is not None and contained(dest,shared):
                        local = Path('references/_shared/cex') / dest.relative_to(shared)
                        import os
                        rewritten = Path(os.path.relpath(destination/local,file.parent)).as_posix()
                        replacements[href] = rewritten + ('#'+fragment if fragment else '')
                for before,after in replacements.items():
                    body = body.replace('('+before+')','('+after+')')
                file.write_text(body)
            result = inspect(destination,contract,package=True)
            if result['status'] != 'PASS':
                raise ValueError(json.dumps(result,ensure_ascii=False))
            manifest = {p.relative_to(destination).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.rglob('*')) if p.is_file()}
            (destination/'manifest.json').write_text(json.dumps({'command_contract_sha256':contract_digest(contract),'files':manifest},indent=2)+'\n')
        staging.rename(output)
    finally:
        # Cleanup is confined to this invocation's unpublished staging directory.
        if staging.exists():
            shutil.rmtree(staging)
    return {'status':'PASS','packages':len(selected),'output':str(output)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('check','build'))
    parser.add_argument('--contract',required=True,type=Path,help='Independent, approved CLI contract export')
    parser.add_argument('--target',type=Path,help='One source or installed skill, or its SKILL.md')
    parser.add_argument('--package',action='store_true',help='Require all references to stay inside the selected skill')
    parser.add_argument('--source',type=Path,help='Source repository for building all six packages')
    parser.add_argument('--output',type=Path,help='New output directory; existing directories are never replaced')
    args = parser.parse_args()
    try:
        if args.contract.stat().st_size > MAX_TOTAL:
            raise ValueError('contract exceeds resource limit')
        contract = json.loads(args.contract.read_text())
        if args.action == 'check':
            if not args.target:
                parser.error('--target is required for check')
            result = inspect(args.target,contract,args.package)
        else:
            if not args.source or not args.output:
                parser.error('--source and --output are required for build')
            result = build(args.source.resolve(),args.output.absolute(),contract)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0 if result['status'] == 'PASS' else 1
    except (ValueError,OSError,KeyError,TypeError,yaml.YAMLError) as error:
        print(json.dumps({'status':'FAIL','error':str(error)},ensure_ascii=False),file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
