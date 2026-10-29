"""Tests for ccr.py (exit.control-change/1). Standard library only; no network, no host paths."""
import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import ccr  # noqa: E402

SETTINGS = ccr.load_settings(os.path.join(ROOT, 'control-change-settings.json'))
EXAMPLES = sorted(os.path.join(ROOT, f) for f in os.listdir(ROOT) if f.startswith('example-') and f.endswith('.json'))
LOG_FIELDS = {'kind', 'chain', 'subject', 'observed_at', 'known_at', 'evidence', 'result_sha256'}


def example(name):
    with open(os.path.join(ROOT, name), 'rb') as fh:
        return json.loads(fh.read())


SOL = example('example-solana-bracketing.json')
ETH = example('example-ethereum-transaction.json')
LZ = example('example-layerzero-bracketing.json')


def errors_of(base, **changes):
    r = copy.deepcopy(base)
    for k, v in changes.items():
        if v is KeyError:
            r.pop(k)
        else:
            r[k] = v
    return ccr.check(r, SETTINGS)


class Examples(unittest.TestCase):
    def test_examples_are_valid_and_canonical(self):
        self.assertEqual(len(EXAMPLES), 3)
        for path in EXAMPLES:
            record, errs = ccr.read_record(path)
            self.assertEqual(errs, [], path)
            self.assertEqual(ccr.check(record, SETTINGS), [], path)

    def test_log_record_matches_the_log_spec_and_the_file_digest(self):
        for path in EXAMPLES:
            record, _ = ccr.read_record(path)
            lr = ccr.log_record(record)
            self.assertEqual(set(lr), LOG_FIELDS)
            self.assertEqual(lr['kind'], 'research_observation')
            with open(path, 'rb') as fh:
                self.assertEqual(lr['result_sha256'], hashlib.sha256(fh.read()).hexdigest())
            self.assertEqual(lr['evidence'], record['evidence'])
            va = record['valid_at']
            self.assertEqual(lr['observed_at'], va.get('position', va.get('new_read_position')))

    def test_cli(self):
        for cmd, want in (('check', 0), ('log-record', 0)):
            p = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'ccr.py'), cmd, EXAMPLES[0]],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, want, p.stderr)
        with tempfile.TemporaryDirectory() as d:
            bad = os.path.join(d, 'bad.json')
            with open(bad, 'wb') as fh:
                fh.write(json.dumps(SOL, indent=1).encode())
            p = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'ccr.py'), 'log-record', bad],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 1)
            self.assertIn('canonical', p.stdout)
        p = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'ccr.py'), 'check', EXAMPLES[0], '--settings'],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)


class FileRules(unittest.TestCase):
    def write(self, data):
        d = tempfile.mkdtemp()
        path = os.path.join(d, 'r.json')
        with open(path, 'wb') as fh:
            fh.write(data)
        return path

    def test_non_canonical_bytes_refused(self):
        canon = ccr.canonical(SOL)
        for data in (canon + b'\n', json.dumps(SOL, sort_keys=True).encode(), json.dumps(SOL).encode()):
            _, errs = ccr.read_record(self.write(data))
            self.assertTrue(errs and 'canonical' in errs[0], data[:40])

    def test_duplicate_key_refused(self):
        canon = ccr.canonical(SOL)
        data = canon[:-1] + b',"format":"exit.control-change/1"}'
        _, errs = ccr.read_record(self.write(data))
        self.assertTrue(errs)

    def test_nan_and_infinity_refused(self):
        for token in (b'NaN', b'Infinity', b'-Infinity', b'1e400'):
            data = ccr.canonical(dict(SOL, scope={})).replace(b'"scope":{}', b'"scope":' + token)
            _, errs = ccr.read_record(self.write(data))
            self.assertTrue(errs and 'canonical' in errs[0], (token, errs))

    def test_deep_nesting_is_refused_not_a_crash(self):
        _, errs = ccr.read_record(self.write(b'[' * 100000 + b']' * 100000))
        self.assertTrue(errs and 'not JSON' in errs[0])

    def test_cli_never_passes_on_an_internal_failure(self):
        path = self.write(ccr.canonical(dict(SOL, chain=[])))
        p = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'ccr.py'), 'check', path], capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertEqual(p.stderr, '')
        self.assertFalse(json.loads(p.stdout)['valid'])

    def test_cli_turns_an_unexpected_failure_into_a_refusal(self):
        import contextlib
        import io
        real = ccr.check
        ccr.check = lambda record, settings: (_ for _ in ()).throw(TypeError('simulated'))
        try:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rc = ccr.main(['check', EXAMPLES[0]])
        finally:
            ccr.check = real
        self.assertEqual(rc, 1)
        self.assertEqual(json.loads(out.getvalue()), {'valid': False, 'errors': ['refused: TypeError']})

    def test_not_utf8_refused(self):
        _, errs = ccr.read_record(self.write(b'\xff\xfe{}'))
        self.assertTrue(errs and 'UTF-8' in errs[0])


class RecordRules(unittest.TestCase):
    def assertRefused(self, errs, fragment):
        self.assertTrue(any(fragment in e for e in errs), (fragment, errs))

    def test_not_an_object(self):
        self.assertRefused(ccr.check([], SETTINGS), 'JSON object')

    def test_field_set(self):
        self.assertRefused(errors_of(SOL, reader=KeyError), 'fields differ')
        self.assertRefused(errors_of(SOL, note='free text'), 'fields differ')

    def test_format_and_chain(self):
        self.assertRefused(errors_of(SOL, format='exit.control-change/2'), 'format must be')
        self.assertRefused(errors_of(SOL, chain='solana-devnet'), 'chain must be')

    def test_subject(self):
        self.assertRefused(errors_of(SOL, subject=ETH['subject']), 'subject')
        self.assertRefused(errors_of(ETH, subject=ETH['subject'].upper().replace('0X', '0x')), 'subject')
        self.assertRefused(errors_of(SOL, subject=SOL['subject'][:20]), 'subject')
        self.assertRefused(errors_of(SOL, subject=SOL['subject'] + 'zz'), 'subject')
        self.assertRefused(errors_of(SOL, subject='0' + SOL['subject'][1:]), 'subject')

    def test_setting_must_exist_and_match_chain(self):
        self.assertRefused(errors_of(SOL, setting='spl-token:mintauthority'), 'not in the registry')
        self.assertRefused(errors_of(SOL, setting=7), 'not in the registry')
        self.assertRefused(errors_of(SOL, setting='evm:eip1967.admin'), 'belongs to ethereum-mainnet')

    def test_scope(self):
        self.assertRefused(errors_of(SOL, scope={'eid': 1}), 'scope keys')
        self.assertRefused(errors_of(LZ, scope={'library': LZ['scope']['library']}), 'scope keys')
        self.assertRefused(errors_of(LZ, scope=dict(LZ['scope'], eid='30101')), 'scope eid')
        self.assertRefused(errors_of(LZ, scope=dict(LZ['scope'], eid=True)), 'scope eid')
        self.assertRefused(errors_of(SOL, scope=[]), 'scope keys')

    def test_values_by_type(self):
        self.assertRefused(errors_of(SOL, new_value=''), 'new_value')
        self.assertRefused(errors_of(SOL, old_value=ETH['subject']), 'old_value')
        self.assertRefused(errors_of(ETH, new_value=None), 'new_value')
        self.assertRefused(errors_of(ETH, new_value=ETH['new_value'].upper().replace('0X', '0x')), 'new_value')
        unsorted = list(reversed(LZ['new_value']))
        self.assertRefused(errors_of(LZ, new_value=unsorted), 'new_value')
        self.assertRefused(errors_of(LZ, new_value=LZ['new_value'] + LZ['new_value'][:1]), 'new_value')

    def test_equal_values_are_not_a_change(self):
        self.assertRefused(errors_of(SOL, new_value=SOL['old_value']), 'equal')
        self.assertRefused(errors_of(LZ, new_value=list(LZ['old_value'])), 'equal')

    def test_value_type_rules(self):
        e = {'values': ['Strict', 'Early', 'Disabled']}
        ok, bad = ccr.value_ok, lambda k, v, x={}: not ccr.value_ok(k, v, x)
        self.assertTrue(ok('uint', 0, {}) and ok('uint', 2 ** 53 - 1, {}))
        self.assertTrue(bad('uint', 2 ** 53) and bad('uint', -1) and bad('uint', True) and bad('uint', 1.0))
        self.assertTrue(ok('u64_string', '0', {}) and ok('u64_string', '18446744073709551615', {}))
        self.assertTrue(bad('u64_string', '18446744073709551616') and bad('u64_string', '01') and bad('u64_string', 1)
                        and bad('u64_string', '-1') and bad('u64_string', ''))
        self.assertTrue(ok('bytes32', '0x' + 'a' * 64, {}) and bad('bytes32', '0x' + 'A' * 64) and bad('bytes32', '0x' + 'a' * 63))
        self.assertTrue(ok('bool', False, {}) and bad('bool', 0))
        self.assertTrue(ok('enum', 'Early', e) and bad('enum', 'early', e) and bad('enum', 'Early', {}))
        self.assertTrue(ok('vote_threshold', {'kind': 'YesVotePercentage', 'percentage': 60}, {}))
        self.assertTrue(ok('vote_threshold', {'kind': 'Disabled', 'percentage': None}, {}))
        self.assertTrue(bad('vote_threshold', {'kind': 'Disabled', 'percentage': 0}))
        self.assertTrue(bad('vote_threshold', {'kind': 'YesVotePercentage', 'percentage': None}))
        self.assertTrue(bad('vote_threshold', {'kind': 'YesVotePercentage', 'percentage': 101}))
        self.assertTrue(bad('vote_threshold', {'kind': 'YesVotePercentage', 'percentage': 60, 'supported_in_pinned_source': True}))
        self.assertTrue(bad('vote_threshold', {'kind': 'Veto', 'percentage': 60}))
        self.assertTrue(ok('solana_address_or_null', None, {}) and ok('solana_address_or_null', '1' * 32, {}))
        self.assertTrue(bad('solana_address_or_null', '1' * 31) and bad('solana_address_or_null', 'O' * 44))
        self.assertTrue(ok('evm_address_list', [], {}) and bad('no_such_type', 1))
        self.assertTrue(bad('vote_threshold', {'kind': [], 'percentage': 1}) and bad('vote_threshold', {'kind': {}, 'percentage': 1}))
        z = {'zero_key_is_null': True}
        self.assertTrue(bad('solana_address_or_null', '1' * 32, z) and ok('solana_address_or_null', None, z)
                        and ok('solana_address_or_null', SOL['subject'], z))

    def test_token_2022_zero_key_is_not_a_value(self):
        r = dict(SOL, setting='token-2022:permanentDelegate.delegate', old_value='1' * 32, new_value=None)
        self.assertTrue(any('old_value' in e for e in ccr.check(r, SETTINGS)))
        self.assertEqual(ccr.check(dict(r, old_value=SOL['old_value']), SETTINGS), [])
        self.assertEqual(ccr.check(dict(SOL, old_value='1' * 32), SETTINGS), [])   # spl-token COption: the zero key is a key
        for n, e in SETTINGS.items():
            self.assertEqual(bool(e.get('zero_key_is_null')), n.startswith('token-2022:'), n)

    def test_unhashable_and_odd_types_are_refused_not_crashes(self):
        for k, v in (('chain', []), ('chain', {}), ('setting', []), ('scope', None), ('valid_at', []), ('reader', []),
                     ('evidence', None), ('known_at', 7), ('subject', [])):
            errs = errors_of(SOL, **{k: v})
            self.assertTrue(errs, k)

    def test_known_at(self):
        self.assertRefused(errors_of(SOL, known_at='2026-01-15T00:31:07Z'), 'known_at')
        self.assertRefused(errors_of(SOL, known_at='2026-01-15T03:31:07+03:00'), 'known_at')
        self.assertRefused(errors_of(SOL, known_at='2026-01-15T00:31:07.1234+00:00'), 'known_at')
        self.assertRefused(errors_of(SOL, known_at='2026-02-30T00:31:07+00:00'), 'known_at')
        self.assertEqual(errors_of(SOL, known_at='2026-01-15T00:31:07+00:00'), [])
        # the format check must not depend on the Python version's fromisoformat
        for text in ('2026-01-15T00:31:07.1234+00:00', '2026-01-15T00:31:07Z', '2026-01-15T00:31:07.1+00:00',
                     '2026-01-15 00:31:07+00:00', '2026-01-15T00:31:07+0000'):
            self.assertIsNone(ccr.UTC_TIME.match(text), text)
            self.assertIsNone(ccr.utc_time(text), text)
        self.assertIsNone(ccr.UTC_TIME.match('\u0662\u0660\u0662\u0666-01-15T00:31:07+00:00'))   # non-ASCII digits
        self.assertEqual(errors_of(SOL, known_at='2026-01-15T00:31:07.123+00:00'), [])

    def test_transaction_basis(self):
        va = ETH['valid_at']
        self.assertRefused(errors_of(ETH, valid_at=dict(va, basis='guess')), 'basis')
        self.assertRefused(errors_of(ETH, valid_at={k: v for k, v in va.items() if k != 'block_time'}), 'exactly basis')
        self.assertRefused(errors_of(ETH, valid_at=dict(va, transaction=va['transaction'][:-1])), 'transaction id')
        self.assertRefused(errors_of(SOL, valid_at=dict(va, transaction=va['transaction'])), 'transaction id')
        self.assertRefused(errors_of(ETH, valid_at=dict(va, position=-1)), 'position')
        self.assertRefused(errors_of(ETH, valid_at=dict(va, position='21000000')), 'position')
        self.assertRefused(errors_of(ETH, valid_at=dict(va, block_time='2026-01-15T10:00:11Z')), 'block_time')
        self.assertRefused(errors_of(ETH, known_at='2026-01-15T10:00:10+00:00'), 'earlier than the block time')
        self.assertEqual(errors_of(ETH, known_at='2026-01-15T10:00:11+00:00'), [])

    def test_solana_transaction_signature(self):
        sig = '1' * 64
        good = dict(SOL, valid_at={'basis': 'transaction', 'transaction': sig, 'position': 1, 'block_time': '2026-01-15T00:00:00+00:00'})
        self.assertEqual(ccr.check(good, SETTINGS), [])
        bad = dict(good, valid_at=dict(good['valid_at'], transaction='1' * 63))
        self.assertTrue(any('transaction id' in e for e in ccr.check(bad, SETTINGS)))

    def test_bracketing_basis(self):
        va = SOL['valid_at']
        self.assertRefused(errors_of(SOL, valid_at=dict(va, new_read_position=va['old_read_position'])), 'earlier than')
        self.assertRefused(errors_of(SOL, valid_at=dict(va, old_read_position=va['new_read_position'] + 1)), 'earlier than')
        self.assertRefused(errors_of(SOL, valid_at=dict(va, extra=1)), 'exactly basis')
        self.assertRefused(errors_of(SOL, valid_at=dict(va, old_read_position=1.5)), 'read positions')
        self.assertRefused(errors_of(SOL, valid_at='300000450'), 'basis')
        self.assertRefused(errors_of(SOL, evidence=SOL['evidence'][:1]), 'both reads')

    def test_evidence(self):
        ev = SOL['evidence']
        self.assertRefused(errors_of(SOL, evidence=[]), 'non-empty')
        self.assertRefused(errors_of(SOL, evidence=list(reversed(ev))), 'sorted')
        self.assertRefused(errors_of(SOL, evidence=ev + ev[:1]), 'sorted')
        self.assertRefused(errors_of(SOL, evidence=[ev[0], ev[0], ev[1]]), 'without duplicates')
        self.assertRefused(errors_of(SOL, evidence=[ev[0].upper(), ev[1]]), 'lowercase hex')
        self.assertRefused(errors_of(SOL, evidence='%s' % ev[0]), 'non-empty')
        self.assertEqual(errors_of(ETH, evidence=ETH['evidence'][:1]), [])

    def test_reader(self):
        rd = SOL['reader']
        self.assertRefused(errors_of(SOL, reader=dict(rd, version=2)), 'reader has exactly')
        self.assertRefused(errors_of(SOL, reader=dict(rd, name='Mint Reader')), 'reader.name')
        self.assertRefused(errors_of(SOL, reader=dict(rd, name='exit.solana-mint-research')), 'reader.name')
        self.assertRefused(errors_of(SOL, reader=dict(rd, implementation_sha256='0' * 63)), 'implementation_sha256')


class Registry(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(ROOT, 'control-change-settings.json'), 'rb') as fh:
            self.reg = json.loads(fh.read())

    def test_entries(self):
        names = [e['name'] for e in self.reg['settings']]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(names, sorted(names))
        for e in self.reg['settings']:
            self.assertEqual(set(e) - {'values', 'programs', 'zero_key_is_null', 'minimum', 'maximum', 'excluded', 'scope_constraints'},
                             {'name', 'chain', 'stored_in', 'scope', 'value_type', 'status', 'source', 'meaning', 'does_not_mean'}, e['name'])
            self.assertIn(e['status'], self.reg['status_values'])
            self.assertIn(e['value_type'], self.reg['value_types'])
            self.assertRegex(e['name'], r'^[a-z0-9-]+:[A-Za-z0-9_.()]+$')
            self.assertEqual('values' in e, e['value_type'] == 'enum', e['name'])
            for kind in e['scope'].values():
                self.assertIn(kind, ('evm_address', 'uint'))
            for prog in e.get('programs', []):
                self.assertTrue(ccr.solana_address(prog), prog)

    def test_registry_loader_refuses_malformed(self):
        d = tempfile.mkdtemp()
        for bad in ({'format': 'x', 'settings': []},
                    dict(self.reg, settings=self.reg['settings'] + self.reg['settings'][:1]),
                    dict(self.reg, settings=[dict(self.reg['settings'][0], value_type='nope')])):
            path = os.path.join(d, 'r.json')
            with open(path, 'w') as fh:
                json.dump(bad, fh)
            with self.assertRaises(ValueError):
                ccr.load_settings(path)


if __name__ == '__main__':
    unittest.main()
