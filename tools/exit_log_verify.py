#!/usr/bin/env python3
"""Verify EXIT's public evidence log yourself. Python 3.9 or later, standard library only. It imports nothing from EXIT: the leaf
rule and the RFC 6962 / RFC 9162 Merkle algorithms are restated here, so the check is independent of EXIT's own code.

  python3 exit_log_verify.py proof BUNDLE [--tx TX.json | --rpc URL] [--notaries NOTARIES]
  python3 exit_log_verify.py log SOURCE [--rpc URL]
  python3 exit_log_verify.py leaf BINDING --log SOURCE [--rpc URL] [--event EVENT | --answer BODY]

proof  Checks one record: the record and its salt give the leaf, the audit path leads to the stated root, and the anchor transaction
       on Solana carries exactly that tree size and root in an EXIT-ROOT-v1 memo, signed by the stated notary key. TX.json is a
       getTransaction reply (encoding jsonParsed) you fetched yourself from any provider; --rpc fetches it at finalized commitment.
       --notaries is notaries.json from the log (file or URL); the signer must be listed there.
log    Checks the whole log: every root in roots.json is the Merkle root of the first N published leaves, every consistency proof
       shows that each tree extends the previous one (nothing removed or rewritten), and every anchor names a published root. With
       --rpc it also fetches every anchor transaction and checks its memo and signer.
leaf   Checks a private record you hold (a binding {record, salt} that EXIT gave your account, for example in a watch change or a
       webhook): it recomputes the leaf, finds it in the published leaves, computes the audit path from those leaves (no private
       bundle is published or needed), checks it against the first anchored root that contains it, and with --rpc checks that
       anchor's transaction and signer (notaries.json of the same log). BINDING may also be the saved value of an answer's
       X-EXIT-Log-Binding header. --answer BODY is a local file with the exact response body bytes you received; it must hash to
       the record's result_sha256. --event EVENT is the full watch event (all parts) for a radar binding.
BUNDLE, BINDING, NOTARIES and SOURCE may be local paths or https URLs; SOURCE is the log folder, e.g. https://exit-protocol.io/log/

Exit code 0 only if every check passed. What a passing check proves and does not prove is printed with the result."""
import base64
import hashlib
import json
import re
import sys
import urllib.request
import urllib.error
import time
from datetime import datetime, timezone

DOMAIN = b'EXIT-LEAF-v1'
MEMO_PROGRAMS = ('MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr', 'Memo1UhkJRfHyvLMcVucJwxXeuD728EqVDDwQDxFMNo')
MEMO = re.compile(r'EXIT-ROOT-v1 ([0-9]+) ([0-9a-f]{64}) ([0-9]{4}-[0-9]{2}-[0-9]{2}) ([0-9]+)')
PROVES = ('The supplied record matches a leaf committed by the verified anchor no later than its block time, under the fetched chain evidence. This does not establish possession of the raw evidence bytes named in the record.')
NOT_PROVEN = ['that the chain state described by the evidence is true: check the evidence at its own slot or block',
              'that EXIT knew it earlier than the anchor: known_at is EXIT\'s own statement',
              'that leaf index order is chronological knowledge order (append-sequence/2 may admit late records)', 'that nothing was left out of the log', 'who controls any address', 'possession of all raw evidence bytes named by their hashes']


def _h(b):
    return hashlib.sha256(b).digest()


def load(src):
    if src.startswith('https://'):
        req = urllib.request.Request(src, headers={'User-Agent': 'exit-log-verify/1'})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    with open(src, encoding='utf-8') as fh:
        return json.load(fh)


def load_binding(src):
    """A binding as JSON, or the saved value of an X-EXIT-Log-Binding header (base64url; a byte-order mark, the header name and
    surrounding quotes are tolerated). Raises ValueError with a reason when the file holds no usable binding."""
    if src.startswith('https://'):
        value = load(src)
    else:
        with open(src, 'rb') as fh:
            raw = fh.read()
        try:
            value = json.loads(raw)            # JSON in UTF-8, UTF-16 or UTF-32, with or without a byte-order mark
        except ValueError:
            value = None
        text = raw.decode(json.detect_encoding(raw)).lstrip('\ufeff').strip()
        if isinstance(value, str):             # a quoted header value is valid JSON text: use the string itself
            text, value = value.strip(), None
        if text.lower().startswith('x-exit-log-binding:'):
            text = text.split(':', 1)[1].strip()
        if len(text) >= 2 and text[0] == text[-1] and text[0] in '"\'':
            text = text[1:-1].strip()
        if value is None:
            try:
                value = json.loads(text)
            except ValueError:
                try:
                    value = json.loads(base64.urlsafe_b64decode(text + '=' * (-len(text) % 4)))
                except (ValueError, TypeError) as e:
                    raise ValueError('not a binding: neither JSON nor a base64url header value') from e
    if isinstance(value, dict) and value.get('status') == 'NOT_BOUND':
        raise ValueError('this answer was not bound to the log (NOT_BOUND %s)' % value.get('reason'))
    if not (isinstance(value, dict) and isinstance(value.get('record'), dict) and isinstance(value.get('salt'), str)):
        raise ValueError('not a binding: record and salt are required')
    return value


def leaf_data(record, salt_hex):
    body = json.dumps(record, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()
    return _h(DOMAIN + bytes.fromhex(salt_hex) + body)


def mth(leaves):
    """RFC 6962 Merkle tree hash over leaf data: H(0x00||d) for leaves, H(0x01||l||r) for nodes, split at the largest power of
    two below n."""
    if not leaves:
        return _h(b'')
    if len(leaves) == 1:
        return _h(b'\x00' + leaves[0])
    k = 1
    while k << 1 < len(leaves):
        k <<= 1
    return _h(b'\x01' + mth(leaves[:k]) + mth(leaves[k:]))


def audit_path(m, leaves):
    """RFC 6962 section 2.1.1 PATH(m, D[n]) over leaf data, restated independently of EXIT's log code."""
    n = len(leaves)
    if n <= 1:
        return []
    k = 1
    while k << 1 < n:
        k <<= 1
    if m < k:
        return audit_path(m, leaves[:k]) + [mth(leaves[k:])]
    return audit_path(m - k, leaves[k:]) + [mth(leaves[:k])]


def included(index, size, data, path, root):
    """RFC 9162 section 2.1.3.2."""
    if not _nat(index) or not _nat(size) or not 0 <= index < size:
        return False
    fn, sn, r = index, size - 1, _h(b'\x00' + data)
    for p in path:
        if sn == 0:
            return False
        if fn & 1 or fn == sn:
            r = _h(b'\x01' + p + r)
            if not fn & 1:
                while fn and not fn & 1:
                    fn >>= 1
                    sn >>= 1
        else:
            r = _h(b'\x01' + r + p)
        fn >>= 1
        sn >>= 1
    return sn == 0 and r == root


def consistent(first, second, first_root, second_root, path):
    """RFC 9162 section 2.1.4.2."""
    if not 0 < first <= second:
        return False
    if first == second:
        return path == [] and first_root == second_root
    if not path:
        return False
    if first & (first - 1) == 0:
        path = [first_root] + list(path)
    fn, sn = first - 1, second - 1
    while fn & 1:
        fn >>= 1
        sn >>= 1
    fr = sr = path[0]
    for c in path[1:]:
        if sn == 0:
            return False
        if fn & 1 or fn == sn:
            fr = _h(b'\x01' + c + fr)
            sr = _h(b'\x01' + c + sr)
            if not fn & 1:
                while fn and not fn & 1:
                    fn >>= 1
                    sn >>= 1
        else:
            sr = _h(b'\x01' + sr + c)
        fn >>= 1
        sn >>= 1
    return fr == first_root and sr == second_root and sn == 0


def fetch_tx(rpc, signature, attempts=5, sleep=time.sleep):
    """getTransaction at finalized commitment. A rate limit (HTTP 429) or a provider error is retried with backoff (honouring
    Retry-After up to 30 s); if every attempt fails, the result names the failure instead of crashing, and the anchor check
    reports it as not verified."""
    body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'getTransaction',
                       'params': [signature, {'encoding': 'jsonParsed', 'commitment': 'finalized',
                                              'maxSupportedTransactionVersion': 0}]}).encode()
    last = 'no attempt'
    for i in range(attempts):
        req = urllib.request.Request(rpc, data=body, headers={'Content-Type': 'application/json', 'User-Agent': 'exit-log-verify/1'})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                reply = json.loads(r.read())
            if not isinstance(reply, dict) or reply.get('error') is not None:
                # A 200 response may still be a JSON-RPC provider failure. Do not mistake it for a missing transaction.
                err = reply.get('error') if isinstance(reply, dict) else None
                code = err.get('code') if isinstance(err, dict) else None
                last = 'JSON-RPC provider error' + (' %s' % code if type(code) is int else '')
                delay = min(30.0, 2.0 ** i)
            else:
                return reply
        except urllib.error.HTTPError as e:
            last = 'HTTP %d' % e.code
            if e.code != 429 and e.code < 500:
                break
            wait = e.headers.get('Retry-After') if e.headers else None
            delay = min(30.0, float(wait)) if wait and wait.replace('.', '', 1).isdigit() else min(30.0, 2.0 ** i)
        except (urllib.error.URLError, OSError, ValueError) as e:
            last = type(e).__name__
            delay = min(30.0, 2.0 ** i)
        if i + 1 < attempts:
            sleep(delay)
    return {'rpc_error': '%s after %d attempt(s); retry later or use another provider' % (last, attempts)}


def check_anchor(tx, anchor, size, root_hex, notaries=None):
    """The anchor transaction must be the named one, succeed, carry exactly one EXIT-ROOT-v1 memo with this size and root, and be
    signed by the named notary key (listed in notaries.json when given)."""
    fail = lambda why: {'anchor_ok': False, 'why': why}
    integer = lambda x: type(x) is int and x >= 0
    if not isinstance(tx, dict):
        return fail('not a getTransaction result (missing, or not finalized yet)')
    if tx.get('rpc_error') or tx.get('error') is not None:
        return fail('RPC unavailable: provider error or request failure')
    if not isinstance(anchor, dict) or not integer(size):
        return fail('anchor size must be a non-negative integer (not boolean)')
    if not isinstance(root_hex, str) or not re.fullmatch('[0-9a-f]{64}', root_hex):
        return fail('anchor root must be a 32-byte lowercase hexadecimal hash')
    if ('size' in anchor and (not integer(anchor['size']) or anchor['size'] != size)) or ('root' in anchor and anchor['root'] != root_hex):
        return fail('published anchor names a different or malformed size or root')
    if not isinstance(anchor.get('signature'), str) or not anchor['signature']:
        return fail('published anchor signature is missing or malformed')
    keys = None
    if notaries is not None:
        if (not isinstance(notaries, dict) or not isinstance(notaries.get('notaries'), list)
                or any(not isinstance(n, dict) or not isinstance(n.get('public_key'), str) or not n['public_key']
                       for n in notaries['notaries'])):
            return fail('malformed notaries.json')
        keys = {n['public_key'] for n in notaries['notaries']}
    res = tx.get('result')
    if not isinstance(res, dict):
        return fail('not a getTransaction result (missing, or not finalized yet)')
    if any(not integer(x) for x in (res.get('slot'), res.get('blockTime'), anchor.get('slot'), anchor.get('block_time'))):
        return fail('anchor slot and block time must be non-negative integers (not boolean)')
    meta = res.get('meta')
    if not isinstance(meta, dict) or 'err' not in meta:
        return fail('transaction success metadata is missing or malformed')
    if meta['err'] is not None:
        return fail('the transaction failed')
    txn = res.get('transaction')
    if (not isinstance(txn, dict) or not isinstance(txn.get('signatures'), list) or not txn['signatures']
            or any(not isinstance(sig, str) or not sig for sig in txn['signatures'])):
        return fail('transaction signatures are missing or malformed')
    msg = txn.get('message')
    if (not isinstance(msg, dict) or not isinstance(msg.get('accountKeys'), list)
            or not isinstance(msg.get('instructions'), list)
            or any(not isinstance(k, dict) or not isinstance(k.get('pubkey'), str)
                   or type(k.get('signer')) is not bool for k in msg['accountKeys'])
            or any(not isinstance(i, dict) for i in msg['instructions'])):
        return fail('transaction message is malformed')
    signers = [k['pubkey'] for k in msg['accountKeys'] if k['signer'] is True]
    memos = [i.get('parsed') for i in msg['instructions'] if i.get('programId') in MEMO_PROGRAMS]
    hits = [MEMO.fullmatch(m) for m in memos if isinstance(m, str) and MEMO.fullmatch(m)]
    out = {'anchor_signature': (txn.get('signatures') or [None])[0], 'anchor_slot': res.get('slot'),
           'anchor_block_time_utc': None, 'signers': signers}
    if isinstance(res.get('blockTime'), int):
        try:
            out['anchor_block_time_utc'] = datetime.fromtimestamp(res['blockTime'], timezone.utc).isoformat()
        except (ValueError, OverflowError, OSError):
            return fail('anchor block time is outside the supported UTC range')
    problems = []
    if len(hits) != 1:
        problems.append('not exactly one EXIT-ROOT-v1 memo')
    else:
        m = hits[0]
        out['memo'] = m.group(0)
        if int(m.group(1)) != size or m.group(2) != root_hex:
            problems.append('the memo names another tree size or root')
        if int(m.group(4)) >= int(m.group(1)) and int(m.group(1)) > 0:
            problems.append('the memo\'s previous size is not smaller than its size')
    if out['anchor_signature'] != anchor.get('signature'):
        problems.append('this is not the named anchor transaction')
    if anchor.get('notary') not in signers:
        problems.append('the named notary key did not sign it')
    if keys is not None and anchor.get('notary') not in keys:
        problems.append('the signer is not in notaries.json')
    if anchor.get('slot') != res.get('slot') or anchor.get('block_time') != res.get('blockTime'):
        problems.append('slot or block time differs from the published anchor')
    out['anchor_ok'] = not problems
    out['why'] = '; '.join(problems) or None
    return out



def _nat(value):
    return type(value) is int and value >= 0


def _hex32(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def _list_document(doc, key):
    if not isinstance(doc, dict) or not isinstance(doc.get(key), list) or any(not isinstance(x, dict) for x in doc[key]):
        raise ValueError('malformed ' + key + ' document')
    return doc[key]


def _check_log_documents(leaves_doc, roots_doc, anchors_doc, notaries=None):
    leaves = _list_document(leaves_doc, 'leaves')
    roots = _list_document(roots_doc, 'roots')
    anchors = _list_document(anchors_doc, 'anchors')
    if any(not _nat(x.get('index')) or not _hex32(x.get('leaf')) for x in leaves):
        raise ValueError('leaf indexes must be non-negative integers; leaves must be SHA-256 hashes')
    if any(not _nat(x.get('size')) or not _nat(x.get('prev_size')) or not _hex32(x.get('root'))
           or not isinstance(x.get('consistency_from_prev'), list)
           or any(not _hex32(y) for y in x['consistency_from_prev']) for x in roots):
        raise ValueError('malformed root sizes, hash or consistency proof')
    if any(not _nat(x.get('size')) or not _nat(x.get('slot')) or not _nat(x.get('block_time'))
           or not _hex32(x.get('root')) or not isinstance(x.get('signature'), str) or not x['signature']
           or not isinstance(x.get('notary'), str) or not x['notary'] for x in anchors):
        raise ValueError('malformed anchor document')
    if notaries is not None:
        if any(not isinstance(x.get('public_key'), str) or not x['public_key'] for x in _list_document(notaries, 'notaries')):
            raise ValueError('malformed notaries document')


def cmd_proof(argv):
    b = load(argv[0])
    notaries = load(argv[argv.index('--notaries') + 1]) if '--notaries' in argv else None
    out = {'leaf_index': b['leaf_index'], 'tree_size': b['tree_size'], 'root': b['root'], 'record': b['record']}
    out['inclusion_ok'] = included(b['leaf_index'], b['tree_size'], leaf_data(b['record'], b['salt']),
                                   [bytes.fromhex(x) for x in b['audit_path']], bytes.fromhex(b['root']))
    a = b.get('anchor') or {}
    if a.get('size') != b['tree_size'] or a.get('root') != b['root']:
        out.update(anchor_ok=False, why='the bundle\'s anchor names another tree')
    elif '--tx' in argv:
        out.update(check_anchor(load(argv[argv.index('--tx') + 1]), a, b['tree_size'], b['root'], notaries))
    elif '--rpc' in argv:
        out.update(check_anchor(fetch_tx(argv[argv.index('--rpc') + 1], a['signature']), a, b['tree_size'], b['root'], notaries))
    out['verified'] = bool(out['inclusion_ok'] and out.get('anchor_ok', False))
    out['proves'] = PROVES if out['verified'] else ('Inclusion in the stated root only; the anchor was not checked.'
                                                     if out['inclusion_ok'] and 'anchor_ok' not in out else 'Nothing: a check failed.')
    out['does_not_prove'] = NOT_PROVEN
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if out['verified'] else 1


def cmd_log(argv):
    base = argv[0] if argv[0].endswith('/') else argv[0] + '/'
    leaves_doc, roots_doc, anchors_doc = load(base + 'leaves.json'), load(base + 'roots.json'), load(base + 'anchors.json')
    notaries = load(base + 'notaries.json')
    _list_document(notaries, 'notaries')
    if any(not isinstance(n.get('public_key'), str) or not n['public_key'] for n in notaries['notaries']):
        raise ValueError('malformed notaries document')
    _check_log_documents(leaves_doc, roots_doc, anchors_doc)
    leaves = [bytes.fromhex(x['leaf']) for x in leaves_doc['leaves']]
    problems, by_size = [], {}
    if [x['index'] for x in leaves_doc['leaves']] != list(range(len(leaves))):
        problems.append('leaf indexes are not 0..n-1 in order')
    for r in roots_doc['roots']:
        by_size[r['size']] = r['root']
        if r['size'] > len(leaves) or mth(leaves[:r['size']]).hex() != r['root']:
            problems.append('root at size %d is not the hash of the first %d leaves' % (r['size'], r['size']))
        if r['prev_size']:
            if r['prev_size'] not in by_size or not consistent(r['prev_size'], r['size'], bytes.fromhex(by_size[r['prev_size']]),
                                                                 bytes.fromhex(r['root']),
                                                                 [bytes.fromhex(x) for x in r['consistency_from_prev']]):
                problems.append('consistency proof %d -> %d fails' % (r['prev_size'], r['size']))
    anchors = []
    for a in anchors_doc['anchors']:
        if by_size.get(a['size']) != a['root']:
            problems.append('anchor %s names a root that is not in roots.json' % a['signature'][:12])
        if '--rpc' in argv:
            time.sleep(0.3)                              # pace public providers (one request per anchor)
            res = check_anchor(fetch_tx(argv[argv.index('--rpc') + 1], a['signature']), a, a['size'], a['root'], notaries)
            anchors.append({'size': a['size'], 'anchor_ok': res['anchor_ok'], 'why': res['why'], 'memo': res.get('memo')})
            if not res['anchor_ok']:
                problems.append('anchor %s: %s' % (a['signature'][:12], res['why']))
    out = {'leaves': len(leaves), 'roots_checked': len(roots_doc['roots']), 'anchors_listed': len(anchors_doc['anchors']),
           'anchors_fetched': anchors, 'problems': problems, 'verified': not problems,
           'proves': 'Every published root is built from the published leaves, and each tree extends the previous one.'
                     + (' Every anchor transaction carries its root.' if '--rpc' in argv else ' Anchors were not fetched.')
           if not problems else 'Nothing: a check failed.'}
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if out['verified'] else 1


def event_digest(value):
    """Independent full-event reconstruction; no EXIT service imports. Lists must contain every consistent multipart part."""
    if isinstance(value,list):
        if not value:raise ValueError('empty event parts')
        count=value[0].get('parts');base={k:v for k,v in value[0].items() if k not in ('part','parts','objects','states')}
        if type(count) is not int or count!=len(value) or sorted(p.get('part') for p in value)!=list(range(1,count+1)):raise ValueError('incomplete or duplicate parts')
        ordered=sorted(value,key=lambda p:p['part'])
        if any(p.get('parts')!=count or {k:v for k,v in p.items() if k not in ('part','parts','objects','states')}!=base for p in ordered):raise ValueError('inconsistent event parts')
        objects=[o for p in ordered for o in p['objects']]
        value=dict(base,objects=objects,states=[[o['signal_id'],o['state_hash']] for o in objects])
    if not isinstance(value,dict) or 'part' in value or 'parts' in value:raise ValueError('complete event required')
    payload={k:v for k,v in value.items() if k not in ('log','webhook_id')}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()


def cmd_leaf(argv):
    try:
        b = load_binding(argv[0])
        leaf_data(b['record'], b['salt'])
    except (OSError, ValueError, UnicodeError, TypeError) as e:
        print(json.dumps({'verified': False, 'why': str(e) or type(e).__name__}, indent=1, sort_keys=True))
        return 1
    base = argv[argv.index('--log') + 1]
    base = base if base.endswith('/') else base + '/'
    leaves_doc, roots_doc, anchors_doc = load(base + 'leaves.json'), load(base + 'roots.json'), load(base + 'anchors.json')
    d = leaf_data(b['record'], b['salt'])
    out = {'record': b['record'], 'leaf': d.hex(), 'leaf_matches_binding': d.hex() == b.get('leaf', d.hex())}
    if '--event' in argv:
        try:out['event_matches_binding']=event_digest(load(argv[argv.index('--event')+1]))==b['record'].get('result_sha256')
        except (ValueError,KeyError,TypeError,IndexError):out['event_matches_binding']=False
        if not out['event_matches_binding']:
            out.update(verified=False,why='event content does not match the committed record');print(json.dumps(out,indent=1,sort_keys=True));return 1
    if '--answer' in argv:
        try:
            with open(argv[argv.index('--answer') + 1], 'rb') as fh:
                out['answer_matches_binding'] = hashlib.sha256(fh.read()).hexdigest() == b['record'].get('result_sha256')
        except (OSError, IndexError):
            out['answer_matches_binding'] = False
        if not out['answer_matches_binding']:
            out.update(verified=False, why='the answer body does not match the committed record (use the exact bytes received)')
            print(json.dumps(out, indent=1, sort_keys=True))
            return 1
    _check_log_documents(leaves_doc, roots_doc, anchors_doc)
    leaves = [bytes.fromhex(x['leaf']) for x in leaves_doc['leaves']]
    if d not in leaves:
        out.update(verified=False, why='the leaf is not in the published log yet (it is appended at the next daily anchor)')
        try:
            known = datetime.fromisoformat(b['record']['known_at'].replace('Z', '+00:00'))
            # r1.6 (review R15-F4): judge against the date of this copy of the log (its newest anchor), not today's clock, so an
            # old downloaded copy never says 'will not be' about a leaf appended after the copy was taken
            times = [a['block_time'] for a in anchors_doc.get('anchors', []) if type(a.get('block_time')) is int]
            copy_time = datetime.fromtimestamp(max(times), timezone.utc) if times else datetime.now(timezone.utc)
            if (copy_time - known).total_seconds() > 8 * 86400:
                out['why'] = ('the leaf is not in this copy of the log, which is more than eight days newer than the record: a private '
                              'record that is not admitted within seven days is discarded, so it will not be appended')
        except (KeyError, TypeError, ValueError, AttributeError, OverflowError, OSError):
            pass
        print(json.dumps(out, indent=1, sort_keys=True))
        return 1
    i = leaves.index(d)
    roots = {r['size']: r['root'] for r in roots_doc['roots']}
    anchored = [a for a in anchors_doc['anchors'] if a['size'] > i and roots.get(a['size']) == a['root']]
    if not anchored:
        out.update(verified=False, leaf_index=i, why='the leaf is in the log but no anchored root contains it yet')
        print(json.dumps(out, indent=1, sort_keys=True))
        return 1
    a = min(anchored, key=lambda x: x['size'])
    path = audit_path(i, leaves[:a['size']])
    out.update(leaf_index=i, tree_size=a['size'], root=a['root'], audit_path=[p.hex() for p in path],
               inclusion_ok=included(i, a['size'], d, path, bytes.fromhex(a['root'])))
    if '--rpc' in argv:
        out.update(check_anchor(fetch_tx(argv[argv.index('--rpc') + 1], a['signature']), a, a['size'], a['root'],
                                load(base + 'notaries.json')))
    out['verified'] = bool(out['inclusion_ok'] and out['leaf_matches_binding'] and out.get('anchor_ok', '--rpc' not in argv))
    out['proves'] = PROVES if out['verified'] and '--rpc' in argv else ('Inclusion in an anchored root of the published log; '
                                                                       'the anchor transaction was not fetched.' if out['verified'] else 'Nothing: a check failed.')
    out['does_not_prove'] = NOT_PROVEN
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if out['verified'] else 1


FLAGS = {'proof': {'--tx', '--rpc', '--notaries'}, 'log': {'--rpc'}, 'leaf': {'--log', '--rpc', '--event', '--answer'}}


def arguments_ok(mode, rest):
    """Every option is a known flag followed by a value, at most once; a misspelled option must not silently skip a check."""
    seen = set()
    if len(rest) % 2:
        return False
    for flag, value in zip(rest[::2], rest[1::2]):
        if flag not in FLAGS[mode] or flag in seen or value.startswith('--'):
            return False
        seen.add(flag)
    return (mode != 'leaf' or '--log' in seen) and not {'--tx', '--rpc'} <= seen


def main(argv):
    if len(argv) < 3 or argv[1] not in FLAGS or argv[2].startswith('--') or not arguments_ok(argv[1], argv[3:]):
        print(__doc__, file=sys.stderr)
        return 2
    try:
        return {'proof': cmd_proof, 'log': cmd_log, 'leaf': cmd_leaf}[argv[1]](argv[2:])
    except (ValueError, TypeError, KeyError, IndexError, OSError) as e:
        print(json.dumps({'verified': False, 'why': 'input or provider response is malformed or unavailable: ' + type(e).__name__}, sort_keys=True))
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
