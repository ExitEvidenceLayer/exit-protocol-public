"""Synthetic tests of tools/exit_log_verify.py --trust github,dns,site. No network: every socket call raises, and the three public
copies are served by an in-memory stub of the verifier's _get. Synthetic keys only."""
import contextlib
import importlib.util
import io
import json
import os
import socket
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

_spec = importlib.util.spec_from_file_location('exit_log_verify_under_test', Path(__file__).resolve().parent / 'tools' / 'exit_log_verify.py')
v = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v)

K1, K2, K3 = 'B' * 44, 'C' * 43, 'D' * 44
TRUST = ['--trust', 'github,dns,site']


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


def hub_md(keys, row=None):
    rows = ''.join('| `%s` | role | 1 |\n' % k for k in keys) if row is None else row
    return ('# EXIT evidence log: notary keys\n\nintro text\n\n| Solana public key | Role | Anchors signed (tree size) |\n|---|---|---|\n'
            + rows + '\nA third copy is the DNS TXT record.\n\n## Key-change memos\n| Date | Memo | Signed by | Transaction signature |\n'
            '|---|---|---|---|\n| (none yet) | | | |\n').encode()


def txt(keys):
    return 'v=exit-notary1; keys=%s; list=github.com/ExitEvidenceLayer/exit-protocol-public' % ','.join(keys)


def doh(records, status=0, ad=True, name=v.DNS_NAME + '.', quoted=False):
    answers = [{'name': name, 'type': 16, 'TTL': 3600, 'data': ('"%s"' % r) if quoted else r} for r in records]
    doc = {'Status': status, 'AD': ad, 'Question': [{'name': name, 'type': 16}]}
    if answers:
        doc['Answer'] = answers
    return json.dumps(doc).encode()


class Copies:
    """The in-memory public copies; each value is bytes or an exception to raise."""
    def __init__(self, hub=None, dns=None):
        self.served = {v.HUB_NOTARIES: hub_md([K1, K2]) if hub is None else hub, v.DOH: doh([txt([K1, K2])]) if dns is None else dns}
        self.calls = []

    def __call__(self, url, accept=None, limit=None):
        self.calls.append(url)
        if url not in self.served:
            raise urllib.error.URLError('not served in this test: ' + url)
        value = self.served[url]
        if isinstance(value, BaseException):
            raise value
        return value


class Log:
    """A two-leaf synthetic log folder with one anchor signed by K1, a proof bundle and a matching transaction."""
    def __init__(self, d, notary_keys=(K1, K2), signer=K1):
        self.d = Path(d)
        self.record = {'kind': 'technical_observation', 'subject': 'synthetic', 'known_at': '2026-11-13T00:00:00Z'}
        self.salt = 'ab' * 16
        leaves = [v.leaf_data(self.record, self.salt), b'\x42' * 32]
        root = v.mth(leaves).hex()
        anchor = {'size': 2, 'root': root, 'signature': 'A' * 88, 'slot': 100, 'block_time': 1793233800, 'notary': signer}
        docs = {'leaves.json': {'leaves': [{'index': i, 'leaf': h.hex()} for i, h in enumerate(leaves)]},
                'roots.json': {'roots': [{'size': 2, 'prev_size': 0, 'root': root, 'consistency_from_prev': []}]},
                'anchors.json': {'anchors': [anchor]},
                'notaries.json': {'format': 'exit.evidence-log-notaries/1', 'notaries': [{'public_key': k} for k in notary_keys]},
                'bundle.json': {'leaf_index': 0, 'tree_size': 2, 'root': root, 'record': self.record, 'salt': self.salt,
                                'audit_path': [p.hex() for p in v.audit_path(0, leaves)], 'anchor': anchor},
                'binding.json': {'record': self.record, 'salt': self.salt},
                'tx.json': {'result': {'slot': 100, 'blockTime': 1793233800, 'meta': {'err': None},
                                       'transaction': {'signatures': ['A' * 88], 'message': {
                                           'accountKeys': [{'pubkey': signer, 'signer': True}],
                                           'instructions': [{'programId': v.MEMO_PROGRAMS[0],
                                                             'parsed': 'EXIT-ROOT-v1 2 %s 2026-11-13 0' % root}]}}}}}
        for name, doc in docs.items():
            (self.d / name).write_text(json.dumps(doc), encoding='utf-8')

    def p(self, name):
        return str(self.d / name)


def run(args, copies):
    buf = io.StringIO()
    with patch.object(v, '_get', copies), contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
        rc = v.main(['exit_log_verify.py'] + args)
    text = buf.getvalue()
    return rc, (json.loads(text) if text.strip() else None)


class TrustBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.log = Log(self.tmp.name)

    def refused(self, args, copies, *words):
        try:
            rc, out = run(args, copies)
        except Exception as e:           # an escaped exception is a failed refusal, not a test error
            self.fail('not refused cleanly: %r' % e)
        self.assertEqual(rc, 1)
        self.assertIs(out['verified'], False)
        self.assertIn('trust', out, 'refused, but not by the trust check')
        self.assertIs(out['trust']['trust_ok'], False)
        self.assertTrue(out['why'].startswith('notary keys refused: '), out['why'])
        for w in words:
            self.assertIn(w, out['why'])
        self.assertNotIn('leaves', out)            # refused before any other check
        return out


class Positive(TrustBase):
    def test_log_all_three_agree(self):
        c = Copies()
        rc, out = run(['log', str(self.log.d)] + TRUST, c)
        self.assertEqual(rc, 0, out)
        self.assertIs(out['verified'], True)
        t = out['trust']
        self.assertIs(t['trust_ok'], True)
        self.assertEqual(t['problems'], [])
        self.assertEqual(t['keys'], {'site': sorted([K1, K2]), 'github': sorted([K1, K2]), 'dns': sorted([K1, K2])})
        self.assertIs(t['dns_dnssec_validated'], True)
        self.assertIn('does_not_prove', t)
        self.assertEqual(sorted(c.calls), sorted([v.HUB_NOTARIES, v.DOH]))

    def test_order_of_names_does_not_matter(self):
        rc, out = run(['log', str(self.log.d), '--trust', 'site,github,dns'], Copies())
        self.assertEqual(rc, 0, out)

    def test_proof_with_tx_uses_the_published_list_by_default(self):
        c = Copies()
        c.served[v.SITE_NOTARIES] = (self.log.d / 'notaries.json').read_bytes()
        rc, out = run(['proof', self.log.p('bundle.json'), '--tx', self.log.p('tx.json')] + TRUST, c)
        self.assertEqual(rc, 0, out)
        self.assertIs(out['anchor_ok'], True)
        self.assertEqual(out['trust']['sources']['site'], v.SITE_NOTARIES)
        self.assertEqual(c.calls.count(v.SITE_NOTARIES), 1)          # read once: the agreed bytes are the checked bytes

    def test_proof_with_local_notaries(self):
        rc, out = run(['proof', self.log.p('bundle.json'), '--tx', self.log.p('tx.json'), '--notaries', self.log.p('notaries.json')] + TRUST,
                      Copies())
        self.assertEqual(rc, 0, out)
        self.assertEqual(out['trust']['sources']['site'], self.log.p('notaries.json'))

    def test_leaf(self):
        rc, out = run(['leaf', self.log.p('binding.json'), '--log', str(self.log.d)] + TRUST, Copies())
        self.assertEqual(rc, 0, out)
        self.assertIn('trust', out)
        self.assertIs(out['trust']['trust_ok'], True)

    def test_dns_from_own_resolver_file(self):
        f = self.log.d / 'dig.txt'
        rec = txt([K2, K1])
        f.write_text('"%s" "%s"\n\n"v=spf1 -all"\n' % (rec[:20], rec[20:]), encoding='utf-8')       # dig splits long records
        c = Copies(dns=AssertionError('DNS-over-HTTPS must not be used with --dns-txt'))
        rc, out = run(['log', str(self.log.d), '--dns-txt', str(f)] + TRUST, c)
        self.assertEqual(rc, 0, out)
        self.assertIsNone(out['trust']['dns_dnssec_validated'])
        self.assertEqual(out['trust']['sources']['dns'], str(f))
        self.assertNotIn(v.DOH, c.calls)

    def test_hub_from_saved_copy(self):
        f = self.log.d / 'NOTARIES.md'
        f.write_bytes(hub_md([K1, K2]))
        c = Copies(hub=AssertionError('the repository must not be read with --hub'))
        rc, out = run(['log', str(self.log.d), '--hub', str(f)] + TRUST, c)
        self.assertEqual(rc, 0, out)
        self.assertNotIn(v.HUB_NOTARIES, c.calls)

    def test_quoted_doh_data_and_other_records(self):
        body = json.loads(doh([txt([K1, K2])], quoted=True))
        body['Answer'] += [{'name': v.DNS_NAME + '.', 'type': 5, 'data': 'elsewhere.example.'},
                           {'name': 'other.' + v.DNS_NAME + '.', 'type': 16, 'data': txt([K3])},
                           {'name': v.DNS_NAME + '.', 'type': 16, 'data': 'v=spf1 -all'},
                           {'name': v.DNS_NAME + '.', 'type': 99, 'data': txt([K3])}]
        rc, out = run(['log', str(self.log.d)] + TRUST, Copies(dns=json.dumps(body).encode()))
        self.assertEqual(rc, 0, out)

    def test_dnssec_not_reported(self):
        rc, out = run(['log', str(self.log.d)] + TRUST, Copies(dns=doh([txt([K1, K2])], ad=False)))
        self.assertEqual(rc, 0, out)
        self.assertIs(out['trust']['dns_dnssec_validated'], False)

    def test_without_trust_nothing_extra_is_read(self):
        c = Copies()
        rc, out = run(['log', str(self.log.d)], c)
        self.assertEqual(rc, 0, out)
        self.assertNotIn('trust', out)
        self.assertEqual(c.calls, [])


class Mismatch(TrustBase):
    def test_github_lacks_a_key(self):
        out = self.refused(['log', str(self.log.d)] + TRUST, Copies(hub=hub_md([K1])), 'github copy lacks ' + K2)
        self.assertEqual(out['trust']['keys']['github'], [K1])

    def test_dns_has_an_extra_key(self):
        self.refused(['log', str(self.log.d)] + TRUST, Copies(dns=doh([txt([K1, K2, K3])])), 'site copy lacks ' + K3, 'github copy lacks ' + K3)

    def test_site_has_an_extra_key(self):
        Log(self.tmp.name, notary_keys=(K1, K2, K3))
        self.refused(['log', str(self.log.d)] + TRUST, Copies(), 'github copy lacks ' + K3, 'dns copy lacks ' + K3)

    def test_same_count_other_key_each_source(self):
        for which in ('github', 'dns', 'site'):
            with self.subTest(which=which):
                Log(self.tmp.name, notary_keys=(K1, K3) if which == 'site' else (K1, K2))
                c = Copies(hub=hub_md([K1, K3]) if which == 'github' else None, dns=doh([txt([K1, K3])]) if which == 'dns' else None)
                out = self.refused(['log', str(self.log.d)] + TRUST, c, which + ' copy lacks ' + K2)
                for other in set(v.TRUST_SOURCES) - {which}:
                    self.assertIn(other + ' copy lacks ' + K3, out['why'])
                    self.assertNotIn(other + ' copy lacks ' + K2, out['why'])

    def test_proof_refused_on_mismatch(self):
        c = Copies(hub=hub_md([K1]))
        c.served[v.SITE_NOTARIES] = (self.log.d / 'notaries.json').read_bytes()
        rc, out = run(['proof', self.log.p('bundle.json'), '--tx', self.log.p('tx.json')] + TRUST, c)
        self.assertEqual(rc, 1)
        self.assertNotIn('inclusion_ok', out)

    def test_leaf_refused_on_mismatch(self):
        rc, out = run(['leaf', self.log.p('binding.json'), '--log', str(self.log.d)] + TRUST, Copies(dns=doh([txt([K1])])))
        self.assertEqual(rc, 1)
        self.assertIs(out['trust']['trust_ok'], False)
        self.assertNotIn('leaf_index', out)

    def test_signer_outside_the_agreed_keys(self):
        Log(self.tmp.name, signer=K3)
        c = Copies()
        c.served[v.SITE_NOTARIES] = (self.log.d / 'notaries.json').read_bytes()
        rc, out = run(['proof', self.log.p('bundle.json'), '--tx', self.log.p('tx.json')] + TRUST, c)
        self.assertEqual(rc, 1)
        self.assertIs(out['trust']['trust_ok'], True)
        self.assertIs(out['anchor_ok'], False)
        self.assertIn('the signer is not in notaries.json', out['why'])


class Missing(TrustBase):
    def test_github_unreachable(self):
        self.refused(['log', str(self.log.d)] + TRUST, Copies(hub=urllib.error.URLError('down')), 'github copy missing or unreachable')

    def test_github_404(self):
        self.refused(['log', str(self.log.d)] + TRUST,
                     Copies(hub=urllib.error.HTTPError(v.HUB_NOTARIES, 404, 'Not Found', None, None)), 'github copy missing or unreachable')

    def test_dns_nxdomain(self):
        self.refused(['log', str(self.log.d)] + TRUST, Copies(dns=doh([], status=3)), 'dns copy missing or unreachable', 'NXDOMAIN')

    def test_dns_no_answer(self):
        self.refused(['log', str(self.log.d)] + TRUST, Copies(dns=doh([])), 'dns copy missing or unreachable')

    def test_dns_only_another_version(self):
        self.refused(['log', str(self.log.d)] + TRUST, Copies(dns=doh([txt([K1, K2]).replace('exit-notary1', 'exit-notary2')])),
                     'dns copy missing')

    def test_dns_record_at_another_name_only(self):
        self.refused(['log', str(self.log.d)] + TRUST, Copies(dns=doh([txt([K1, K2])], name='other.' + v.DNS_NAME + '.')), 'dns copy missing')

    def test_dns_unreachable(self):
        self.refused(['log', str(self.log.d)] + TRUST, Copies(dns=urllib.error.URLError('down')), 'dns copy missing or unreachable')

    def test_site_list_absent(self):
        os.remove(self.log.p('notaries.json'))
        self.refused(['log', str(self.log.d)] + TRUST, Copies(), 'site copy missing or unreachable')

    def test_dns_txt_file_absent(self):
        self.refused(['log', str(self.log.d), '--dns-txt', self.log.p('none.txt')] + TRUST, Copies(), 'dns copy missing or unreachable')

    def test_incomplete_read(self):
        import http.client
        self.refused(['log', str(self.log.d)] + TRUST, Copies(hub=http.client.IncompleteRead(b'')), 'github copy missing or unreachable')


class Malformed(TrustBase):
    def check(self, words, hub=None, dns=None):
        return self.refused(['log', str(self.log.d)] + TRUST, Copies(hub=hub, dns=dns), *words)

    def test_hub_without_key_table(self):
        self.check(['github copy malformed', 'no key table'], hub=b'# notary keys\n\nnothing here\n')

    def test_hub_two_key_tables(self):
        self.check(['github copy malformed', 'more than one'], hub=hub_md([K1, K2]) + hub_md([K1, K2]))

    def test_hub_row_without_backticks(self):
        self.check(['github copy malformed', 'malformed key row'], hub=hub_md([], row='| `%s` | r | 1 |\n| %s | r | 1 |\n' % (K1, K2)))

    def test_hub_without_separator(self):
        self.check(['github copy malformed', 'separator'], hub=hub_md([K1, K2]).replace(b'|---|---|---|\n', b'', 1))

    def test_hub_empty_table(self):
        self.check(['github copy malformed', 'lists no key'], hub=hub_md([], row=''))

    def test_hub_not_utf8(self):
        self.check(['github copy malformed'], hub=b'\xff\xfe\xfa')

    def test_bad_key_characters(self):
        for bad in ('0' * 44, 'O' * 44, 'B' * 31, 'B' * 45, 'B' * 43 + '_', 'B' * 20 + ' ' + 'B' * 20):
            with self.subTest(bad=bad):
                self.check(['dns copy malformed', 'malformed key'], dns=doh([txt([K1, bad])]))

    def test_duplicate_key(self):
        self.check(['dns copy malformed', 'twice'], dns=doh([txt([K1, K2, K1])]))
        self.check(['github copy malformed', 'twice'], hub=hub_md([K1, K2, K2]))

    def test_dns_empty_key_in_list(self):
        self.check(['dns copy malformed'], dns=doh(['v=exit-notary1; keys=%s,,%s' % (K1, K2)]))

    def test_dns_two_records(self):
        self.check(['dns copy malformed', 'more than one'], dns=doh([txt([K1, K2]), txt([K1, K2])]))

    def test_dns_no_keys_field(self):
        self.check(['dns copy malformed', 'no keys field'], dns=doh(['v=exit-notary1; list=x']))

    def test_dns_duplicate_field(self):
        self.check(['dns copy malformed'], dns=doh([txt([K1, K2]) + '; keys=' + K3]))

    def test_dns_field_without_equals(self):
        self.check(['dns copy malformed'], dns=doh([txt([K1, K2]) + '; junk']))

    def test_dns_garbage(self):
        self.check(['dns copy malformed'], dns=b'<html>not json</html>')

    def test_dns_status_not_int(self):
        self.check(['dns copy malformed'], dns=json.dumps({'Status': '0'}).encode())

    def test_dns_servfail(self):
        self.check(['dns copy malformed', 'status 2'], dns=doh([txt([K1, K2])], status=2))

    def test_dns_data_not_text(self):
        body = json.loads(doh([txt([K1, K2])]))
        body['Answer'][0]['data'] = 7
        self.check(['dns copy malformed'], dns=json.dumps(body).encode())

    def test_dns_unbalanced_quotes(self):
        self.check(['dns copy malformed'], dns=doh(['"%s' % txt([K1, K2])]))

    def test_site_list_malformed(self):
        for doc in ({'notaries': {}}, {'notaries': [{'public_key': 7}]}, {'notaries': ['x']}, [], {'notaries': []},
                    {'notaries': [{'public_key': K1}, {'public_key': K2}, {'role': 'no key'}]}):
            with self.subTest(doc=doc):
                (self.log.d / 'notaries.json').write_text(json.dumps(doc), encoding='utf-8')
                self.check(['site copy malformed'])


class Arguments(TrustBase):
    def test_refused_values(self):
        for args in (['--trust', 'github,dns'], ['--trust', 'github,dns,site,site'], ['--trust', 'github,dns,web'], ['--trust', ''],
                     ['--trust', 'github, dns, site'], ['--hub', 'x'], ['--dns-txt', 'x'], ['--trust', 'github,dns,site', '--trust', 'site,dns,github']):
            with self.subTest(args=args):
                rc, out = run(['log', str(self.log.d)] + args, Copies())
                self.assertEqual(rc, 2)
                self.assertIsNone(out)

    def test_flags_known_to_every_mode(self):
        for mode in ('proof', 'log', 'leaf'):
            self.assertTrue({'--trust', '--hub', '--dns-txt'} <= v.FLAGS[mode])


class Transport(unittest.TestCase):
    class Reply(io.BytesIO):
        def __init__(self, body, url):
            io.BytesIO.__init__(self, body)
            self.url = url

        def geturl(self):
            return self.url

    def test_redirect_away_from_https_refused(self):
        with patch.object(v.urllib.request, 'urlopen', lambda req, timeout: self.Reply(b'x', 'http://plain.example/')):
            with self.assertRaisesRegex(ValueError, 'redirected'):
                v._get('https://x.example/')

    def test_size_limit(self):
        with patch.object(v.urllib.request, 'urlopen', lambda req, timeout: self.Reply(b'x' * 11, 'https://x.example/')):
            with self.assertRaisesRegex(ValueError, 'larger'):
                v._get('https://x.example/', limit=10)
            self.assertEqual(v._get('https://x.example/'), b'x' * 11)

    def test_accept_header_sent(self):
        seen = {}

        def opener(req, timeout):
            seen['accept'] = req.get_header('Accept')
            return self.Reply(b'{}', req.full_url)
        with patch.object(v.urllib.request, 'urlopen', opener):
            v._get('https://x.example/', accept='application/dns-json')
        self.assertEqual(seen['accept'], 'application/dns-json')

    def test_https_load_goes_through_get(self):
        with patch.object(v, '_get', lambda url: b'{"a": 1}'):
            self.assertEqual(v.load('https://x.example/a.json'), {'a': 1})

    def test_file_limit(self):
        with tempfile.NamedTemporaryFile(delete=False) as fh:
            fh.write(b'x' * (v.TRUST_LIMIT + 1))
        self.addCleanup(os.remove, fh.name)
        with self.assertRaisesRegex(ValueError, 'larger'):
            v._read_file(fh.name)

    def test_network_is_blocked_in_these_tests(self):
        with self.assertRaises(AssertionError):
            socket.create_connection(('192.0.2.1', 443))


class TruncatedReply(unittest.TestCase):
    """A provider that closes the connection early: http.client raises IncompleteRead (an HTTPException, not an OSError) inside
    read(). Every mode must end in the JSON refusal (exit 1, verified false), never in a traceback."""

    @staticmethod
    def opener(req, timeout):
        import http.client

        class Sock:
            def makefile(self, mode, *args, **kwargs):
                return io.BytesIO(b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 4096\r\n\r\n{"leaves": [')
        r = http.client.HTTPResponse(Sock(), method='GET', url=req.full_url)
        r.begin()
        r.url = req.full_url
        return r

    def refused(self, args):
        buf = io.StringIO()
        try:
            with patch.object(v.urllib.request, 'urlopen', self.opener), contextlib.redirect_stdout(buf), \
                    contextlib.redirect_stderr(io.StringIO()):
                rc = v.main(['exit_log_verify.py'] + args)
        except Exception as e:           # an escaped exception is the defect under test: a failure, not a test error
            self.fail('not refused cleanly: %r' % e)
        out = json.loads(buf.getvalue())
        self.assertEqual(rc, 1)
        self.assertIs(out['verified'], False)
        self.assertEqual(out['why'], 'input or provider response is malformed or unavailable: IncompleteRead')

    def test_the_reply_really_is_truncated(self):
        import http.client
        req = v.urllib.request.Request('https://log.example/leaves.json')
        with self.assertRaises(http.client.IncompleteRead):
            with self.opener(req, 30) as r:
                r.read()

    def test_log_over_https(self):
        self.refused(['log', 'https://log.example/log/'])

    def test_proof_over_https(self):
        self.refused(['proof', 'https://log.example/log/proofs/2/00000000.json', '--notaries', 'https://log.example/log/notaries.json'])

    def test_leaf_over_https(self):
        with tempfile.TemporaryDirectory() as d:
            Log(d)
            self.refused(['leaf', str(Path(d) / 'binding.json'), '--log', 'https://log.example/log/'])


if __name__ == '__main__':
    unittest.main()
