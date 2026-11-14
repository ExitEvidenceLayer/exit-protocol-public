"""Tests of tools/claims_check.py check 8, readme_hash_table (README.md SHA-256 values against the files of the same checkout).
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
    """main() with an empty --live-dir: the seven live checks fail without fixtures; only readme_hash_table is asserted."""

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


if __name__ == '__main__':
    unittest.main()
