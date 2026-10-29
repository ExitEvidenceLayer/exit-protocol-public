"""Keyless public evidence tools. Uses the published verifier, never the private engine.

No environment API key, arbitrary URL, local evidence file or private binding is
accepted. Inclusion, published consistency and actual chain checks are distinct.
"""
import hashlib
import http.client
import importlib.util
import io
import json
import re
import ssl
import time
from pathlib import Path

from exit_client import ExitError

API_HOST = 'api.exit-protocol.io'
LOG_PATH = '/v0/log/'
RPC_HOST = 'solana-rpc.publicnode.com'
GENESIS = '5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d'
VERIFIER_SHA256 = '9381318713af86ff3be6c83960bf4528b4c218e6f088a31379fd011b830f42a6'
MAX_BYTES = 2 * 1024 * 1024
MAX_LEAVES, MAX_ROOTS, MAX_ANCHORS = 8192, 128, 256
MAX_SECONDS, MAX_CALLS = 20, 7
_HEX = re.compile('[0-9a-f]{64}')
_SIG = re.compile('[1-9A-HJ-NP-Za-km-z]{64,88}')


def refuse(code):
    raise ExitError(0, code)


def verifier():
    path = Path(__file__).resolve().parent / 'tools' / 'exit_log_verify.py'
    try:
        if hashlib.sha256(path.read_bytes()).hexdigest() != VERIFIER_SHA256:
            refuse('PUBLIC_VERIFIER_PIN_MISMATCH')
    except OSError:
        refuse('PUBLIC_VERIFIER_FILE_REQUIRED')
    spec = importlib.util.spec_from_file_location('exit_public_log_verifier', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def number(value, *, positive=False):
    if not isinstance(value, str) or not re.fullmatch('0|[1-9][0-9]{0,4}', value):
        refuse('PUBLIC_PROOF_INDEX_INVALID')
    n = int(value)
    if n > MAX_LEAVES or (positive and n == 0):
        refuse('PUBLIC_LOG_RESOURCE_LIMIT')
    return n


def strict(raw):
    def pairs(items):
        out = {}
        for k, value in items:
            if k in out:
                raise ValueError()
            out[k] = value
        return out
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except (ValueError, UnicodeError, RecursionError):
        refuse('PUBLIC_JSON_INVALID')


class _Reader(io.RawIOBase):
    def __init__(self, sock, deadline, clock):
        self.sock, self.deadline, self.clock = sock, deadline, clock
        self.raw = sock.makefile('rb', buffering=0)

    def readable(self):
        return True

    def readinto(self, b):
        left = self.deadline - self.clock()
        if left <= 0:
            refuse('PUBLIC_FETCH_DEADLINE')
        self.sock.settimeout(min(3, left))
        return self.raw.readinto(b)

    def close(self):
        try:
            self.raw.close()
        finally:
            super().close()


class _Socket:
    def __init__(self, sock, deadline, clock):
        self.sock, self.deadline, self.clock = sock, deadline, clock

    def makefile(self, mode='rb', *args, **kwargs):
        if mode != 'rb':
            refuse('PUBLIC_FETCH_MODE_REFUSED')
        return io.BufferedReader(_Reader(self.sock, self.deadline, self.clock))

    def __getattr__(self, name):
        return getattr(self.sock, name)


def _connect(host, timeout):
    return http.client.HTTPSConnection(host, timeout=timeout, context=ssl.create_default_context())


class PublicSession:
    def __init__(self, *, _connector=_connect, _clock=time.monotonic):
        self.connect, self.clock = _connector, _clock
        self.deadline, self.calls = self.clock() + MAX_SECONDS, 0

    def _request(self, host, path, body=None):
        # No caller-controlled destination, authorization, redirects or proxies.
        if ((host == API_HOST and not re.fullmatch(
                r'/v0/log/(leaves|roots|anchors|notaries)\.json|/v0/log/proofs/[1-9][0-9]{0,4}/[0-9]{8}\.json', path))
                or host not in (API_HOST, RPC_HOST) or (host == RPC_HOST and path != '/')
                or (host == API_HOST and body is not None)):
            refuse('PUBLIC_FETCH_TARGET_REFUSED')
        left = self.deadline - self.clock()
        if self.calls >= MAX_CALLS or left <= 0:
            refuse('PUBLIC_FETCH_BUDGET_EXHAUSTED')
        self.calls += 1
        connection = self.connect(host, min(3, left))
        try:
            connection.connect()
            connection.sock = _Socket(connection.sock, self.deadline, self.clock)
            headers = {'User-Agent': 'exit-evidence-tools/1', 'Accept': 'application/json', 'Accept-Encoding': 'identity'}
            if body is not None:
                headers['Content-Type'] = 'application/json'
            connection.request('POST' if body is not None else 'GET', path, body=body, headers=headers)
            response = connection.getresponse()
            try:
                if response.status != 200:
                    code = 'PUBLIC_PROOF_NOT_AVAILABLE' if response.status == 404 else 'PUBLIC_FETCH_REFUSED'
                    raise ExitError(response.status, code)
                if response.headers.get('Content-Encoding', 'identity') != 'identity':
                    refuse('PUBLIC_RESPONSE_ENCODING_REFUSED')
                raw = bytearray()
                while True:
                    if self.clock() >= self.deadline:
                        refuse('PUBLIC_FETCH_DEADLINE')
                    piece = response.read1(min(65536, MAX_BYTES + 1 - len(raw)))
                    raw.extend(piece)
                    if len(raw) > MAX_BYTES:
                        refuse('PUBLIC_RESPONSE_TOO_LARGE')
                    if not piece:
                        break
                if self.clock() >= self.deadline:
                    refuse('PUBLIC_FETCH_DEADLINE')
                return strict(bytes(raw))
            finally:
                response.close()
        except ExitError:
            raise
        except (OSError, http.client.HTTPException):
            refuse('PUBLIC_FETCH_UNAVAILABLE_NO_RETRY')
        finally:
            connection.close()

    def log(self, name):
        return self._request(API_HOST, LOG_PATH + name)

    def rpc(self, method, params):
        if method not in ('getGenesisHash', 'getTransaction'):
            refuse('PUBLIC_RPC_METHOD_REFUSED')
        request = {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}
        value = self._request(RPC_HOST, '/', json.dumps(request).encode())
        if (not isinstance(value, dict) or value.get('jsonrpc') != '2.0' or type(value.get('id')) is not int
                or value['id'] != 1 or 'error' in value or 'result' not in value):
            refuse('PUBLIC_RPC_RESPONSE_INVALID')
        return value


class EvidenceClient:
    def __init__(self, *, _session=PublicSession):
        self.session, self.v = _session, verifier()

    def _snapshot(self, s):
        docs = [s.log(name + '.json') for name in ('leaves', 'roots', 'anchors', 'notaries')]
        v = self.v
        try:
            v._check_log_documents(*docs)
            leaves, roots, anchors, notaries = [doc[key] for doc, key in zip(docs, ('leaves', 'roots', 'anchors', 'notaries'))]
            if (len(leaves) > MAX_LEAVES or not 1 <= len(roots) <= MAX_ROOTS or len(anchors) > MAX_ANCHORS
                    or not 1 <= len(notaries) <= 32):
                refuse('PUBLIC_LOG_RESOURCE_LIMIT')
            if [x['index'] for x in leaves] != list(range(len(leaves))):
                refuse('PUBLIC_LEAF_SEQUENCE_INVALID')
            hashes, by_size, previous = [bytes.fromhex(x['leaf']) for x in leaves], {}, 0
            for root in roots:
                size = root['size']
                if (size <= previous or size > len(hashes) or root['prev_size'] != previous
                        or v.mth(hashes[:size]).hex() != root['root']):
                    refuse('PUBLIC_ROOT_INVALID')
                if previous and not v.consistent(previous, size, bytes.fromhex(by_size[previous]),
                                                bytes.fromhex(root['root']),
                                                [bytes.fromhex(x) for x in root['consistency_from_prev']]):
                    refuse('PUBLIC_CONSISTENCY_INVALID')
                previous, by_size[size] = size, root['root']
            if any(by_size.get(a['size']) != a['root'] for a in anchors):
                refuse('PUBLIC_ANCHOR_ROOT_MISMATCH')
            return docs, hashes, by_size
        except (ValueError, TypeError, KeyError, OverflowError):
            refuse('PUBLIC_LOG_DOCUMENTS_INVALID')

    def history(self):
        s = self.session()
        docs, hashes, _ = self._snapshot(s)
        return {'scope': 'published_log_consistency_only', 'consistency_ok': True, 'anchor_verified': False,
                'leaves': len(hashes), 'roots': docs[1]['roots'], 'anchors_listed': docs[2]['anchors'],
                'log_url': 'https://' + API_HOST + LOG_PATH, 'requests': s.calls,
                'does_not_prove': self.v.NOT_PROVEN,
                'note': 'Published roots match these leaves and consistency paths. Chain transactions were not fetched.'}

    def _cite(self, leaf_index, tree_size, expected_root=None):
        index, size = number(leaf_index), number(tree_size, positive=True)
        if index >= size or (expected_root is not None and (
                not isinstance(expected_root, str) or not _HEX.fullmatch(expected_root))):
            refuse('PUBLIC_PROOF_INDEX_INVALID')
        s = self.session()
        docs, hashes, roots = self._snapshot(s)
        root = roots.get(size)
        if root is None or (expected_root is not None and root != expected_root):
            refuse('PUBLIC_EXPECTED_ROOT_MISMATCH')
        name = 'proofs/%d/%08d.json' % (size, index)
        b = s.log(name)
        try:
            if (not isinstance(b, dict) or b.get('format') != 'exit.evidence-proof/1'
                    or type(b.get('leaf_index')) is not int or b['leaf_index'] != index
                    or type(b.get('tree_size')) is not int or b['tree_size'] != size or b.get('root') != root
                    or not isinstance(b.get('record'), dict) or not isinstance(b.get('salt'), str)
                    or not re.fullmatch('[0-9a-f]{32}', b['salt']) or not isinstance(b.get('audit_path'), list)
                    or len(b['audit_path']) > 32 or any(not isinstance(x, str) or not _HEX.fullmatch(x) for x in b['audit_path'])):
                refuse('PUBLIC_PROOF_INVALID')
            leaf = self.v.leaf_data(b['record'], b['salt'])
            if (leaf != hashes[index] or not self.v.included(index, size, leaf,
                    [bytes.fromhex(x) for x in b['audit_path']], bytes.fromhex(root))):
                refuse('PUBLIC_INCLUSION_FAILED')
            anchor = b.get('anchor')
            self.v._check_log_documents(docs[0], docs[1], {'anchors': [anchor]}, docs[3])
            fields = ('size', 'root', 'signature', 'slot', 'block_time', 'notary')
            identity = {k: anchor[k] for k in fields}
            if (not any(identity == {k: a[k] for k in fields} for a in docs[2]['anchors'])
                    or anchor.get('root') != root or anchor.get('size') != size):
                refuse('PUBLIC_PROOF_ANCHOR_MISMATCH')
            out = {'scope': 'public_record_inclusion', 'leaf_index': index, 'tree_size': size, 'root': root,
                   'leaf': leaf.hex(), 'record': b['record'], 'inclusion_ok': True, 'consistency_ok': True,
                   'anchor_verified': False, 'anchor_listed': anchor,
                   'proof_url': 'https://' + API_HOST + LOG_PATH + name,
                   'does_not_prove': self.v.NOT_PROVEN,
                   'note': 'Inclusion checked against the published root. The chain anchor has not been fetched.'}
            return s, docs[3], anchor, out
        except (TypeError, ValueError, KeyError, OverflowError):
            refuse('PUBLIC_PROOF_INVALID')

    def cite(self, leaf_index, tree_size, expected_root=None):
        s, _, _, out = self._cite(leaf_index, tree_size, expected_root)
        return dict(out, requests=s.calls)

    def verify(self, leaf_index, tree_size, expected_root=None):
        s, notaries, anchor, out = self._cite(leaf_index, tree_size, expected_root)
        out.update(scope='public_record_and_chain_anchor', verified=False, chain_identity_verified=False)
        if not _SIG.fullmatch(anchor['signature']):
            refuse('PUBLIC_ANCHOR_SIGNATURE_INVALID')
        try:
            if s.rpc('getGenesisHash', [])['result'] != GENESIS:
                refuse('PUBLIC_CHAIN_IDENTITY_MISMATCH')
            out['chain_identity_verified'] = True
            tx = s.rpc('getTransaction', [anchor['signature'], {'encoding': 'jsonParsed', 'commitment': 'finalized',
                                                               'maxSupportedTransactionVersion': 0}])
            check = self.v.check_anchor(tx, anchor, out['tree_size'], out['root'], notaries)
            out.update(anchor_check=check, anchor_verified=check['anchor_ok'], verified=check['anchor_ok'])
            out['note'] = self.v.PROVES if out['verified'] else 'Chain anchor check failed; no verified anchor claim.'
        except ExitError as e:
            out.update(anchor_verified=False, verified=False, failure=e.error,
                       note='Chain evidence was unavailable or refused. Inclusion alone is not chain verification.')
        return dict(out, requests=s.calls, rpc_url='https://' + RPC_HOST)
