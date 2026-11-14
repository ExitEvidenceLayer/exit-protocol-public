"""Tests of tools/claims_check.py check 8, readme_hash_table (README.md SHA-256 values against the files of the same checkout), and
check 9, api_md_schema_ids (the schema ids docs/API.md names against the live API description, here a fixture).
No network: every socket call raises. Run with `python3 -B -m unittest -v test_claims_check`."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('claims_check_under_test', HERE / 'tools' / 'claims_check.py')
cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cc)


def _no_network(*args, **kwargs):
    raise AssertionError('a test tried to use the network')


_GUARDS = [patch.object(socket.socket, 'connect', _no_network), patch.object(socket, 'create_connection', _no_network),
           patch.object(socket, 'getaddrinfo', _no_network)]


def setUpModule():
    for g in _GUARDS:
        g.start()


def tearDownModule():
    for g in _GUARDS:
        g.stop()


def sha(data):
    return hashlib.sha256(data).hexdigest()


CLIENT, MCP, VERIFY = b'print("client")\n', b'print("mcp")\n', b'print("verifier")\n'


def evidence(pin):
    return ("VERIFIER_SHA256 = '%s'\n" % pin).encode()


def readme(client=None, mcp=None, verify=None, evidence_value=None, commands=True):
    ev = evidence_value or sha(evidence(verify or sha(VERIFY)))
    lines = ['# Hub', '', '| File | SHA-256 |', '|---|---|',
             '| `exit_client.py` | `%s` |' % (client or sha(CLIENT)),
             '| `exit_mcp.py` | `%s` |' % (mcp or sha(MCP)),
             '| `exit_evidence.py` | `%s` |' % ev, '']
    if commands:
        lines += ['On macOS or Linux, `shasum -a 256 exit_client.py exit_mcp.py exit_evidence.py` must print these values; on Windows,',
                  '`Get-FileHash -Algorithm SHA256 exit_client.py, exit_mcp.py, exit_evidence.py`.']
    lines += ['exit_evidence.py pins the SHA-256 of `tools/exit_log_verify.py` (`%s`)' % (verify or sha(VERIFY)), '']
    return '\n'.join(lines)


class Tree:
    """A temporary checkout: README.md plus the three client files and the verifier."""

    def __init__(self, text=None, pin=None, files=('exit_client.py', 'exit_mcp.py', 'exit_evidence.py', 'tools/exit_log_verify.py')):
        self.tmp = tempfile.TemporaryDirectory(); self.dir = self.tmp.name
        data = {'exit_client.py': CLIENT, 'exit_mcp.py': MCP, 'exit_evidence.py': evidence(pin or sha(VERIFY)), 'tools/exit_log_verify.py': VERIFY}
        for name in files:
            p = os.path.join(self.dir, name); os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'wb') as fh:
                fh.write(data[name])
        self.write(text if text is not None else readme())

    def write(self, text):
        with open(os.path.join(self.dir, 'README.md'), 'w', encoding='utf-8') as fh:
            fh.write(text)

    def check(self):
        return cc.readme_hashes(self.dir)

    def close(self):
        self.tmp.cleanup()


class ReadmeHashes(unittest.TestCase):
    def tree(self, *a, **k):
        t = Tree(*a, **k); self.addCleanup(t.close); return t

    def test_matching_table_passes(self):
        r = self.tree().check()
        self.assertEqual(r['problems'], [])
        self.assertEqual([x['file'] for x in r['rows']], ['exit_client.py', 'exit_mcp.py', 'exit_evidence.py', 'tools/exit_log_verify.py'])
        self.assertTrue(all(x['readme'] == x['actual'] for x in r['rows']))

    def test_stale_value_fails_and_names_the_file(self):
        r = self.tree(readme(client='30c92ac0' + '0' * 56)).check()
        self.assertEqual(len(r['problems']), 1)
        self.assertIn('exit_client.py as 30c92ac0', r['problems'][0])

    def test_two_stale_rows_both_reported(self):            # the 2-10 Nov state: exit_client and exit_mcp both behind
        r = self.tree(readme(client='a' * 64, mcp='b' * 64)).check()
        self.assertEqual(len(r['problems']), 2)

    def test_uppercase_value_of_the_right_file_passes(self):
        r = self.tree(readme(client=sha(CLIENT).upper())).check()
        self.assertEqual(r['problems'], [])

    def test_listed_file_missing_from_checkout_fails(self):
        r = self.tree(files=('exit_client.py', 'exit_evidence.py', 'tools/exit_log_verify.py')).check()
        self.assertTrue(any('exit_mcp.py, which is not in the checkout' in p for p in r['problems']), r['problems'])

    def test_value_pairs_with_the_nearest_file_before_it(self):
        t = self.tree(); t.write(readme() + '\n`exit_client.py` loads `exit_mcp.py` (`%s`).\n' % sha(MCP))
        r = t.check()
        self.assertEqual(r['problems'], [])
        self.assertEqual(r['rows'][-1]['file'], 'exit_mcp.py')

    def test_value_with_no_file_before_it_fails(self):
        t = self.tree(); t.write(readme() + '\nAn orphan value: `%s`.\n' % ('c' * 64))
        self.assertTrue(any('names no file before it' in p for p in t.check()['problems']))

    def test_file_outside_the_checkout_fails(self):
        t = self.tree(); t.write(readme() + '\n| `../exit_client.py` | `%s` |\n' % sha(CLIENT))
        self.assertTrue(any('../exit_client.py, which is outside the checkout' in p for p in t.check()['problems']), t.check()['problems'])

    def test_absolute_path_fails(self):
        t = self.tree(); t.write(readme() + '\n| `/etc/exit_client.py` | `%s` |\n' % sha(CLIENT))
        self.assertTrue(any('/etc/exit_client.py, which is outside the checkout' in p for p in t.check()['problems']), t.check()['problems'])

    def test_symlink_to_outside_fails(self):
        t = self.tree(); outside = tempfile.NamedTemporaryFile(delete=False); outside.write(CLIENT); outside.close()
        self.addCleanup(os.unlink, outside.name)
        os.symlink(outside.name, os.path.join(t.dir, 'linked.py'))
        t.write(readme() + '\n| `linked.py` | `%s` |\n' % sha(CLIENT))
        self.assertTrue(any('linked.py, which is outside the checkout' in p for p in t.check()['problems']))

    def test_readme_without_any_value_fails(self):
        t = self.tree(); t.write('# Hub\n\nNo table here.\n')
        self.assertEqual(t.check()['problems'], ['README.md lists no file SHA-256'])

    def test_command_naming_a_file_without_a_value_fails(self):
        t = self.tree(); t.write(readme().replace('| `exit_evidence.py` |', '| exit_evidence.py |'))   # the row lost its file name
        problems = t.check()['problems']
        self.assertTrue(any('hash exit_evidence.py but lists no SHA-256' in p for p in problems), problems)
        self.assertTrue(any('names no file before it' in p for p in problems), problems)

    def test_get_filehash_comma_list_is_read(self):
        text = readme().replace('`shasum -a 256 exit_client.py exit_mcp.py exit_evidence.py`', 'shasum')
        text = text.replace('exit_mcp.py, exit_evidence.py`', 'exit_mcp.py, exit_evidence.py, exit_extra.py`')
        problems = self.tree(text).check()['problems']
        self.assertEqual(problems, ['README.md tells readers to hash exit_extra.py but lists no SHA-256 for it'])

    def test_verifier_pin_must_equal_exit_evidence(self):
        other = 'd' * 64        # exit_evidence.py pins another verifier; README's pin is the file's real hash
        t = self.tree(text=readme(evidence_value=sha(evidence(other))), pin=other)
        self.assertTrue(any('VERIFIER_SHA256 is dddddddd' in p for p in t.check()['problems']), t.check()['problems'])

    def test_verifier_pin_without_exit_evidence_fails(self):
        text = '\n'.join(x for x in readme(commands=False).splitlines() if not x.startswith('| `exit_evidence.py`'))
        t = self.tree(text=text, files=('exit_client.py', 'exit_mcp.py', 'tools/exit_log_verify.py'))
        self.assertTrue(any('exit_evidence.py is not in the checkout, so its pin was not compared' in p for p in t.check()['problems']), t.check()['problems'])

    def test_missing_readme_raises(self):
        t = self.tree(); os.unlink(os.path.join(t.dir, 'README.md'))
        with self.assertRaises(OSError):
            t.check()


class MainReportsTheCheck(unittest.TestCase):
    """main() with an empty --live-dir: the other eight checks (1-7 and 9) fail without fixtures; only readme_hash_table is asserted."""

    def run_main(self, repo):
        with tempfile.TemporaryDirectory() as live:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = cc.main(['claims_check.py', '--repo', repo, '--live-dir', live, '--now', '1763000000'])
        return rc, json.loads(buf.getvalue())

    def test_good_table_true(self):
        t = Tree(); self.addCleanup(t.close)
        rc, out = self.run_main(t.dir)
        self.assertIs(out['checks']['readme_hash_table'], True)
        self.assertFalse([m for m in out['mismatches'] if m['check'] == 'readme_hash_table'])
        self.assertEqual(len(out['readme_hashes']), 4)
        self.assertEqual(rc, 1)                               # the live checks have no fixtures here

    def test_stale_table_false(self):
        t = Tree(readme(mcp='e' * 64)); self.addCleanup(t.close)
        rc, out = self.run_main(t.dir)
        self.assertIs(out['checks']['readme_hash_table'], False)
        self.assertTrue(any(m['check'] == 'readme_hash_table' and 'exit_mcp.py as eeeeeeee' in m['detail'] for m in out['mismatches']))
        self.assertEqual(rc, 1)

    def test_missing_readme_is_a_mismatch_not_a_skip(self):
        t = Tree(); self.addCleanup(t.close); os.unlink(os.path.join(t.dir, 'README.md'))
        rc, out = self.run_main(t.dir)
        self.assertIs(out['checks']['readme_hash_table'], False)
        self.assertIn({'check': 'readme_hash_table', 'detail': 'unreadable: FileNotFoundError'}, out['mismatches'])


class ThisCheckout(unittest.TestCase):
    """The checkout this test file is in: its README table must equal its own files (the release gate N3 asked for)."""

    def test_published_table_matches_published_files(self):
        r = cc.readme_hashes(str(HERE))
        self.assertEqual(r['problems'], [])
        self.assertGreaterEqual(len(r['rows']), 4)



# Check 9 -------------------------------------------------------------------------------------------------------------------------

def described(*texts, version='2026-11-12.1'):
    """An API description shaped like openapi.json: each text is one route's 200 description."""
    return {'openapi': '3.1.0', 'info': {'version': version},
            'paths': {'/r%d' % i: {'get': {'responses': {'200': {'description': t}}}} for i, t in enumerate(texts)}}


LIVE = described('exit.solana-mint-research/2 (a replay of an earlier request returns its stored body, which can be /1)',
                 'exit.ethereum-contract-research/5 since 4 November 2026. A replay can be /1, /2, /3 or /4.',
                 'Two answers into one graph (schema exit.research-graph/1).', 'exit.solana-governance-research/1')
API_MD = ('# Free research API\n\nResponses use `exit.solana-mint-research/2` (a replay can be `/1`).\n\n'
          'Since 30 October 2026 (schema `/4`) ... Responses use\n`exit.ethereum-contract-research/5` since 4 November 2026.\n\n'
          '- `GET /v0/research/graph?request_id=` (`exit.research-graph/1`): one typed graph.\n')


class Docs:
    """A temporary checkout holding docs/API.md (and, when given, a repository openapi.json)."""

    def __init__(self, text=API_MD, repo_api=None):
        self.tmp = tempfile.TemporaryDirectory(); self.dir = self.tmp.name
        os.makedirs(os.path.join(self.dir, 'docs'))
        if text is not None:
            with open(os.path.join(self.dir, 'docs', 'API.md'), 'w', encoding='utf-8') as fh:
                fh.write(text)
        if repo_api is not None:
            with open(os.path.join(self.dir, 'openapi.json'), 'w', encoding='utf-8') as fh:
                json.dump(repo_api, fh)

    def close(self):
        self.tmp.cleanup()


class ApiMdSchemaIds(unittest.TestCase):
    def check(self, text, live=LIVE):
        d = Docs(text); self.addCleanup(d.close)
        return cc.api_md_schema_ids(d.dir, live)

    def test_matching_ids_pass(self):
        r = self.check(API_MD)
        self.assertEqual(r['problems'], [])
        self.assertEqual([(x['line'], x['id']) for x in r['rows']],
                         [(3, 'exit.solana-mint-research/2'), (6, 'exit.ethereum-contract-research/5'), (8, 'exit.research-graph/1')])
        self.assertEqual(r['rows'][1]['live'], ['exit.ethereum-contract-research/5'])

    def test_the_2_november_case_fails(self):              # docs/API.md said /3 after the description had moved to /4
        r = self.check(API_MD.replace('contract-research/5', 'contract-research/3'),
                       described('exit.ethereum-contract-research/4', 'exit.solana-mint-research/2', 'exit.research-graph/1'))
        self.assertEqual(r['problems'], ['docs/API.md line 6 says exit.ethereum-contract-research/3; the live API description names '
                                         'exit.ethereum-contract-research/4'])

    def test_newer_version_in_docs_fails(self):
        r = self.check(API_MD.replace('contract-research/5', 'contract-research/6'))
        self.assertEqual(len(r['problems']), 1)
        self.assertIn('says exit.ethereum-contract-research/6', r['problems'][0])

    def test_schema_the_description_does_not_name_fails(self):
        r = self.check(API_MD + 'Watches use `exit.watch-list/1`.\n')
        self.assertEqual(r['problems'], ['docs/API.md line 9 names exit.watch-list/1; the live API description names no exit.watch-list schema'])

    def test_docs_without_a_full_id_fails(self):
        r = self.check('# API\n\nSchema `/4` was used from 30 October; policy `solana-finalized-mint-pair-hop/2`.\n')
        self.assertEqual(r['rows'], [])
        self.assertEqual(r['problems'], ['docs/API.md names no schema id in full (exit.<name>/<number>)'])

    def test_newest_version_the_description_names_is_the_reference(self):
        live = described('exit.ethereum-contract-research/5 now; stored bodies replay as exit.ethereum-contract-research/4',
                         'exit.solana-mint-research/2', 'exit.research-graph/1')
        self.assertEqual(self.check(API_MD, live)['problems'], [])
        r = self.check(API_MD.replace('contract-research/5', 'contract-research/4'), live)
        self.assertEqual(r['problems'], ['docs/API.md line 6 says exit.ethereum-contract-research/4; the live API description names '
                                         'exit.ethereum-contract-research/4, exit.ethereum-contract-research/5'])

    def test_versions_compare_as_numbers(self):
        live = described('exit.solana-mint-research/9 and exit.solana-mint-research/10', 'exit.ethereum-contract-research/5',
                         'exit.research-graph/1')
        self.assertEqual(self.check(API_MD.replace('mint-research/2', 'mint-research/10'), live)['problems'], [])
        r = self.check(API_MD.replace('mint-research/2', 'mint-research/9'), live)
        self.assertEqual(len(r['problems']), 1)
        self.assertIn('says exit.solana-mint-research/9', r['problems'][0])

    def test_every_id_on_a_line_is_read(self):
        r = self.check(API_MD + 'Both: `exit.solana-mint-research/2` and `exit.ethereum-contract-research/3`.\n')
        self.assertEqual([x['id'] for x in r['rows'] if x['line'] == 9], ['exit.solana-mint-research/2', 'exit.ethereum-contract-research/3'])
        self.assertEqual(len(r['problems']), 1)
        self.assertIn('line 9 says exit.ethereum-contract-research/3', r['problems'][0])

    def test_ids_in_lists_nested_values_and_keys_are_read(self):
        live = {'info': {'version': 'x'}, 'paths': {'/a': {'get': {'responses': {'200': {'content': {'application/json': {'schema': {
            'properties': {'schema': {'enum': ['exit.solana-mint-research/2']}}}}}}}}}},
            'x-index': {'exit.ethereum-contract-research/5': 'contract'}, 'tags': [{'description': ['exit.research-graph/1']}]}
        self.assertEqual(self.check(API_MD, live)['problems'], [])

    def test_short_forms_policy_ids_and_lookalikes_are_not_read(self):
        text = API_MD + ('Policy `ethereum-finalized-issuer-freeze/2`, `ordering=append-sequence/2`, `/1` to `/4`, '
                         'notexit.thing/1, exit.thing/1x, exit.thing/2/3, exit.thing/1.5 and `EXIT-ROOT-v1`.\n')
        r = self.check(text)
        self.assertEqual(len(r['rows']), 3)
        self.assertEqual(r['problems'], [])

    def test_id_at_the_end_of_a_sentence_is_read(self):
        r = self.check(API_MD + 'The format is exit.made-up/1.\n')
        self.assertEqual(r['rows'][-1]['id'], 'exit.made-up/1')
        self.assertEqual(len(r['problems']), 1)

    def test_live_schemas_missing_from_docs_are_listed_not_failed(self):
        r = self.check(API_MD)
        self.assertEqual(r['live_not_in_docs'], ['exit.solana-governance-research/1'])
        self.assertEqual(r['problems'], [])

    def test_missing_api_md_raises(self):
        d = Docs(text=None); self.addCleanup(d.close)
        with self.assertRaises(OSError):
            cc.api_md_schema_ids(d.dir, LIVE)


class MainReportsCheck9(unittest.TestCase):
    """main() with a --live-dir holding only the live openapi.json: only api_md_schema_ids is asserted."""

    def run_main(self, docs, live_api=LIVE):
        self.addCleanup(docs.close)
        with tempfile.TemporaryDirectory() as live:
            if live_api is not None:
                with open(os.path.join(live, 'openapi.json'), 'w', encoding='utf-8') as fh:
                    json.dump(live_api, fh)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = cc.main(['claims_check.py', '--repo', docs.dir, '--live-dir', live, '--now', '1763000000'])
        return rc, json.loads(buf.getvalue())

    def mine(self, out):
        return [m['detail'] for m in out['mismatches'] if m['check'] == 'api_md_schema_ids']

    def test_matching_docs_true(self):
        rc, out = self.run_main(Docs(repo_api=LIVE))
        self.assertIs(out['checks']['api_md_schema_ids'], True)
        self.assertEqual(self.mine(out), [])
        self.assertEqual(len(out['api_md_schema_ids']['rows']), 3)
        self.assertEqual(out['api_md_schema_ids']['live_not_in_docs'], ['exit.solana-governance-research/1'])
        self.assertEqual(rc, 1)                               # the other live checks have no fixtures here

    def test_stale_docs_false(self):
        rc, out = self.run_main(Docs(API_MD.replace('contract-research/5', 'contract-research/3'), repo_api=LIVE))
        self.assertIs(out['checks']['api_md_schema_ids'], False)
        self.assertEqual(len(self.mine(out)), 1)
        self.assertIn('says exit.ethereum-contract-research/3', self.mine(out)[0])

    def test_compared_with_the_live_description_not_the_repository_copy(self):
        old = described('exit.ethereum-contract-research/3', 'exit.solana-mint-research/2', 'exit.research-graph/1')
        rc, out = self.run_main(Docs(API_MD.replace('contract-research/5', 'contract-research/3'), repo_api=old))
        self.assertIs(out['checks']['api_md_schema_ids'], False)
        self.assertIn('names exit.ethereum-contract-research/5', self.mine(out)[0])

    def test_unread_live_description_is_a_mismatch(self):
        rc, out = self.run_main(Docs(repo_api=LIVE), live_api=None)
        self.assertIs(out['checks']['api_md_schema_ids'], False)
        self.assertEqual(self.mine(out), ['unreadable: the live API description was not read (see api_description_version)'])

    def test_check_1_stopped_before_the_live_read(self):     # no repository openapi.json: check 1 stops before its live read
        calls = []; real = cc.Live.get
        def counting(live, url, name):
            calls.append(url); return real(live, url, name)
        with patch.object(cc.Live, 'get', counting):
            rc, out = self.run_main(Docs())
        self.assertIs(out['checks']['api_md_schema_ids'], False)
        self.assertEqual(self.mine(out), ['unreadable: check 1 stopped at the repository openapi.json, before any live read '
                                          '(see api_description_version)'])
        self.assertEqual(calls.count(cc.API + '/openapi.json'), 0)

    def test_missing_api_md_is_a_mismatch_not_a_skip(self):
        rc, out = self.run_main(Docs(text=None, repo_api=LIVE))
        self.assertIs(out['checks']['api_md_schema_ids'], False)
        self.assertEqual(self.mine(out), ['unreadable: FileNotFoundError'])

    def test_the_live_description_is_read_once(self):
        calls = []; real = cc.Live.get
        def counting(live, url, name):
            calls.append(url); return real(live, url, name)
        with patch.object(cc.Live, 'get', counting):
            rc, out = self.run_main(Docs(repo_api=LIVE))
        self.assertIs(out['checks']['api_md_schema_ids'], True)
        self.assertEqual(calls.count(cc.API + '/openapi.json'), 1)


class ThisCheckoutApiMd(unittest.TestCase):
    """The checkout this test file is in: docs/API.md names the schema ids of the repository copy of the API description."""

    def test_api_md_matches_the_repository_copy(self):
        with open(HERE / 'openapi.json', encoding='utf-8') as fh:
            r = cc.api_md_schema_ids(str(HERE), json.load(fh))
        self.assertEqual(r['problems'], [])
        self.assertGreaterEqual(len(r['rows']), 1)


if __name__ == '__main__':
    unittest.main()
