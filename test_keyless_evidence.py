"""Synthetic protocol and loopback transport tests. No user keys or providers."""
import copy
import hashlib
import http.client
import http.server
import json
import os
import threading
import unittest
from unittest.mock import Mock, patch

import exit_client as c
import exit_evidence as e
import exit_mcp as m


class Fixture:
    def __init__(self):
        self.v = e.verifier()
        self.record = {'kind': 'technical_observation', 'subject': 'synthetic-subject', 'known_at': '2026-10-29T00:00:00Z'}
        self.salt = 'ab' * 16
        self.leaves = [self.v.leaf_data(self.record, self.salt), b'\x42' * 32]
        root = self.v.mth(self.leaves).hex()
        self.anchor = {'size': 2, 'root': root, 'signature': 'A' * 88, 'slot': 100, 'block_time': 1793233800, 'notary': 'B' * 44}
        self.docs = {
            'leaves.json': {'leaves': [{'index': i, 'leaf': h.hex()} for i, h in enumerate(self.leaves)]},
            'roots.json': {'roots': [{'size': 2, 'prev_size': 0, 'root': root, 'consistency_from_prev': []}]},
            'anchors.json': {'anchors': [self.anchor]},
            'notaries.json': {'notaries': [{'public_key': 'B' * 44}]},
            'proofs/2/00000000.json': {'format': 'exit.evidence-proof/1', 'leaf_index': 0, 'tree_size': 2,
                'record': self.record, 'salt': self.salt, 'root': root, 'anchor': self.anchor,
                'audit_path': [h.hex() for h in self.v.audit_path(0, self.leaves)]}}
        self.tx = {'jsonrpc': '2.0', 'id': 1, 'result': {'slot': 100, 'blockTime': 1793233800,
             'meta': {'err': None}, 'transaction': {'signatures': ['A' * 88], 'message': {
             'accountKeys': [{'pubkey': 'B' * 44, 'signer': True}],
             'instructions': [{'programId': self.v.MEMO_PROGRAMS[0], 'parsed': 'EXIT-ROOT-v1 2 %s 2026-10-29 0' % root}]}}}}
        self.genesis = e.GENESIS
        self.calls, self.names = 0, []

    def log(self, name):
        self.calls += 1; self.names.append(name)
        return copy.deepcopy(self.docs[name])

    def rpc(self, method, params):
        self.calls += 1; self.names.append(method)
        return {'result': self.genesis} if method == 'getGenesisHash' else copy.deepcopy(self.tx)

    def client(self):
        return e.EvidenceClient(_session=lambda: self)


class EvidenceTests(unittest.TestCase):
    def test_history_is_consistency_not_chain_verification(self):
        f = Fixture(); out = f.client().history()
        self.assertTrue(out['consistency_ok']); self.assertFalse(out['anchor_verified'])
        self.assertEqual(out['requests'], 4); self.assertNotIn('getTransaction', f.names)

    def test_cite_checks_record_path_root_and_explicit_limit(self):
        f = Fixture(); out = f.client().cite('0', '2')
        self.assertTrue(out['inclusion_ok']); self.assertFalse(out['anchor_verified'])
        self.assertEqual(out['record'], f.record); self.assertEqual(out['requests'], 5)
        self.assertTrue(out['proof_url'].endswith('/proofs/2/00000000.json'))

    def test_verify_checks_genesis_and_exact_transaction(self):
        f = Fixture(); out = f.client().verify('0', '2', f.anchor['root'])
        self.assertTrue(out['verified']); self.assertTrue(out['chain_identity_verified'])
        self.assertEqual(out['requests'], 7)
        self.assertIn('known_at is EXIT', ' '.join(out['does_not_prove']))

    def test_chain_unavailable_is_not_a_verified_result(self):
        f = Fixture(); f.tx['result'] = None
        out = f.client().verify('0', '2')
        self.assertFalse(out['verified']); self.assertTrue(out['inclusion_ok'])

    def test_rpc_failure_is_not_inclusion_failure_or_false_success(self):
        f = Fixture()
        def fail(*a):
            raise c.ExitError(429, 'PUBLIC_FETCH_REFUSED')
        f.rpc = fail
        out = f.client().verify('0', '2')
        self.assertFalse(out['verified']); self.assertTrue(out['inclusion_ok'])
        self.assertEqual(out['failure'], 'PUBLIC_FETCH_REFUSED')

    def test_wrong_chain_never_requests_transaction(self):
        f = Fixture(); f.genesis = 'other-chain'
        out = f.client().verify('0', '2')
        self.assertFalse(out['verified']); self.assertNotIn('getTransaction', f.names)

    def test_wrong_memo_signer_signature_or_metadata_refused(self):
        for change in [lambda tx: tx['result']['transaction'].update(signatures=['C' * 88]),
                       lambda tx: tx['result']['transaction']['message']['accountKeys'][0].update(signer=False),
                       lambda tx: tx['result']['meta'].update(err={'failure': True}),
                       lambda tx: tx['result'].pop('meta'),
                       lambda tx: tx['result'].update(slot=101),
                       lambda tx: tx['result']['transaction']['message']['instructions'][0].update(parsed='EXIT-ROOT-v1 2 ' + '0'*64 + ' 2026-10-29 0')]:
            f = Fixture(); change(f.tx)
            with self.subTest(change=change): self.assertFalse(f.client().verify('0', '2')['verified'])

    def test_rehashed_record_tampering_does_not_match_leaf(self):
        f = Fixture(); f.docs['proofs/2/00000000.json']['record']['subject'] = 'different'
        with self.assertRaisesRegex(c.ExitError, 'PUBLIC_INCLUSION_FAILED'): f.client().cite('0', '2')

    def test_expected_root_mismatch_stops_before_proof(self):
        f = Fixture()
        with self.assertRaisesRegex(c.ExitError, 'PUBLIC_EXPECTED_ROOT_MISMATCH'): f.client().cite('0', '2', '0' * 64)
        self.assertEqual(f.calls, 4)

    def test_bool_proof_index_refused(self):
        f = Fixture(); f.docs['proofs/2/00000000.json']['leaf_index'] = False
        with self.assertRaisesRegex(c.ExitError, 'PUBLIC_PROOF_INVALID'): f.client().cite('0', '2')

    def test_bad_indexes_fail_before_network(self):
        for val in [True, 0, '-1', '01', '１', '../secret', 'http://localhost', '8193']:
            f = Fixture()
            with self.subTest(val=val), self.assertRaises(c.ExitError): f.client().cite(val, '2')
            self.assertEqual(f.calls, 0)

    def test_bad_size_or_range_fail_before_network(self):
        for index, size in [('0', '0'), ('2', '2'), ('0', '90000')]:
            f = Fixture()
            with self.assertRaises(c.ExitError): f.client().cite(index, size)
            self.assertEqual(f.calls, 0)

    def test_root_tampering_and_duplicate_size_refused(self):
        for action in [lambda f: f.docs['roots.json']['roots'][0].update(root='0' * 64),
                       lambda f: f.docs['roots.json']['roots'].append(copy.deepcopy(f.docs['roots.json']['roots'][0]))]:
            f = Fixture(); action(f)
            with self.assertRaises(c.ExitError): f.client().history()

    def test_leaf_sequence_and_boolean_types_refused(self):
        for index in [False, 1, -1]:
            f = Fixture(); f.docs['leaves.json']['leaves'][0]['index'] = index
            with self.assertRaises(c.ExitError): f.client().history()

    def test_anchor_must_match_published_bundle_exactly(self):
        f = Fixture(); f.docs['proofs/2/00000000.json']['anchor'] = dict(f.anchor, slot=101)
        with self.assertRaisesRegex(c.ExitError, 'PUBLIC_PROOF_ANCHOR_MISMATCH'): f.client().cite('0', '2')

    def test_published_anchor_presentation_metadata_is_not_identity(self):
        f = Fixture()
        f.docs['anchors.json']['anchors'][0] = dict(f.anchor, memo='same commitment',
            explorers=['https://explorer.solana.com/'], block_time_utc='2026-10-29T00:30:00Z')
        self.assertTrue(f.client().verify('0', '2')['verified'])

    def test_bundle_anchor_float_fields_are_not_integer_identity(self):
        f = Fixture(); f.docs['proofs/2/00000000.json']['anchor'] = dict(f.anchor, slot=100.0)
        with self.assertRaises(c.ExitError): f.client().cite('0', '2')

    def test_unlisted_notary_fails_chain_verification(self):
        f = Fixture(); f.docs['notaries.json']['notaries'][0]['public_key'] = 'C' * 44
        self.assertFalse(f.client().verify('0', '2')['verified'])

    def test_resource_limits_fail(self):
        f = Fixture()
        with patch.object(e, 'MAX_LEAVES', 1), self.assertRaises(c.ExitError): f.client().history()

    def test_malformed_json_rejects_duplicates_nan_and_depth(self):
        for raw in [b'{"x":1,"x":2}', b'{"x":NaN}', b'\xff', b'[' * 2000 + b']' * 2000]:
            with self.assertRaises(c.ExitError): e.strict(raw)

    def test_missing_or_altered_verifier_refused(self):
        with patch.object(e, 'VERIFIER_SHA256', '0' * 64), self.assertRaisesRegex(c.ExitError, 'PUBLIC_VERIFIER_PIN_MISMATCH'):
            e.EvidenceClient()

    def test_keyless_mcp_never_uses_authenticated_client(self):
        f = Fixture(); research = Mock()
        with patch.object(e, 'EvidenceClient', return_value=f.client()):
            out = m.handle(research, {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
                            'params': {'name': 'exit_verify', 'arguments': {'leaf_index': '0', 'tree_size': '2'}}})
        self.assertFalse(out['result']['isError']); self.assertTrue(json.loads(out['result']['content'][0]['text'])['verified'])
        self.assertEqual(research.mock_calls, [])

    def test_mcp_invalid_empty_args_no_longer_coerced_to_object(self):
        for args in [[], 0, None, '', False]:
            out = m.handle(Mock(), {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
                           'params': {'name': 'exit_history', 'arguments': args}})
            self.assertIn('error', out)

    def test_mcp_extra_path_and_numeric_args_refused_before_network(self):
        for args in [{'leaf_index': 0, 'tree_size': '2'}, {'leaf_index': '0', 'tree_size': '2', 'url': 'http://localhost'}]:
            with patch.object(e, 'EvidenceClient') as client:
                out = m.handle(Mock(), {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call',
                                'params': {'name': 'exit_cite', 'arguments': args}})
                self.assertIn('error', out); client.assert_not_called()


class TransportTests(unittest.TestCase):
    def server(self, status=200, body=b'{}', encoding=None):
        self.seen = []
        outer = self
        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args): pass
            def do_GET(self):
                outer.seen.append(dict(self.headers)); self.send_response(status)
                if encoding: self.send_header('Content-Encoding', encoding)
                self.end_headers(); self.wfile.write(body)
        server = http.server.HTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        self.addCleanup(server.server_close); self.addCleanup(server.shutdown)
        return e.PublicSession(_connector=lambda host, timeout: http.client.HTTPConnection('127.0.0.1', server.server_port, timeout=timeout))

    def test_no_auth_cookie_proxy_or_redirect(self):
        session = self.server()
        with patch.dict(os.environ, {'EXIT_API_KEY': 'exit_free_' + 'x' * 43, 'HTTPS_PROXY': 'http://127.0.0.1:1'}):
            self.assertEqual(session.log('roots.json'), {})
        self.assertNotIn('Authorization', self.seen[0]); self.assertNotIn('Cookie', self.seen[0])

    def test_redirects_errors_and_held_proof_no_retry(self):
        for status in [302, 404, 429, 503]:
            session = self.server(status=status)
            with self.assertRaises(c.ExitError): session.log('proofs/2/00000000.json')
            self.assertEqual(session.calls, 1); self.assertEqual(len(self.seen), 1)

    def test_response_limit_and_encoding(self):
        session = self.server(body=b' ' * 1025)
        with patch.object(e, 'MAX_BYTES', 1024), self.assertRaisesRegex(c.ExitError, 'PUBLIC_RESPONSE_TOO_LARGE'):
            session.log('roots.json')
        session = self.server(encoding='gzip')
        with self.assertRaisesRegex(c.ExitError, 'PUBLIC_RESPONSE_ENCODING_REFUSED'): session.log('roots.json')

    def test_target_budget_and_deadline_before_connect(self):
        connect = Mock(); s = e.PublicSession(_connector=connect)
        for host, path in [('169.254.169.254', '/'), (e.API_HOST, '/v0/log/../private'), (e.RPC_HOST, '/private'),
                           (e.API_HOST, '/v0/log/proofs/2/../../etc/passwd')]:
            with self.assertRaises(c.ExitError): s._request(host, path)
        s.calls = e.MAX_CALLS
        with self.assertRaises(c.ExitError): s.log('roots.json')
        s.calls = 0; s.deadline = 0
        with self.assertRaises(c.ExitError): s.log('roots.json')
        connect.assert_not_called()

    def test_unsupported_rpc_method_before_connect(self):
        connect = Mock(); s = e.PublicSession(_connector=connect)
        with self.assertRaises(c.ExitError): s.rpc('sendTransaction', [])
        connect.assert_not_called()


if __name__ == '__main__':
    unittest.main()
