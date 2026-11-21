#!/usr/bin/env python3
"""Re-read the key chain facts of the EXIT case note "Glamsterdam gas changes, 16 November 2026"
(cases/glamsterdam-eip-8037-8038-2026-11-16.md). Read-only JSON-RPC to two public providers, no keys, standard library only.
Every check reads one fact at Ethereum block 26,428,440 (code size and SHA-256, the seven proxy and general storage slots,
owner(), Safe threshold, owners and modules, proxiableUUID()) for the 20 named addresses and the authority paths the note
discusses. A check passes only when BOTH providers return the expected value. Expected values come from the case result
file next to this script (glamsterdam-eip-8037-8038-2026-11-16.json, list "checks"); its SHA-256 is printed first.
Reading state at a past block needs archive providers; a provider that cannot serve the block is reported as NO_ANSWER,
never as a pass. Exit code 0 only if every check passes.
  python3 glamsterdam-eip-8037-8038-2026-11-16-reread.py [--eth URL URL] [--only PREFIX]"""
import hashlib, http.client, json, sys, time, urllib.request
from pathlib import Path

ETH = ['https://rpc.mevblocker.io', 'https://eth.drpc.org']
CASE = 'glamsterdam-eip-8037-8038-2026-11-16.json'
CACHE = {}


def rpc(url, method, params):
    body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}).encode()
    if (url, body) in CACHE:
        return CACHE[(url, body)]
    last = None
    for i in range(6):
        try:
            req = urllib.request.Request(url, body, {'Content-Type': 'application/json', 'User-Agent': 'exit-case-reread/1'})
            j = json.loads(urllib.request.urlopen(req, timeout=40).read())
            if 'result' in j:
                CACHE[(url, body)] = j['result']
                return j['result']
            last = RuntimeError('%s: %s' % (url, str(j.get('error'))[:200]))
        except (OSError, ValueError, http.client.HTTPException) as e:
            last = e
        time.sleep(1 + i)
    raise last


def words(h):
    h = h[2:]
    return [h[64 * i:64 * i + 64] for i in range(len(h) // 64)]


def dec(kind, v):
    if kind == 'code':
        b = bytes.fromhex(v[2:])
        return {'size': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
    if kind == 'word':
        return '0x' + v[2:].lower().rjust(64, '0')
    if kind == 'addr':
        return '0x' + v[-40:].lower()
    if kind == 'uint':
        return int(v, 16)
    if kind in ('addr_array', 'modules_page'):
        w = words(v)
        off = int(w[0], 16) // 32
        n = int(w[off], 16)
        arr = ['0x' + x[-40:] for x in w[off + 1:off + 1 + n]]
        return arr if kind == 'addr_array' else {'modules': arr, 'next': '0x' + w[1][-40:]}
    if kind == 'block':
        return {'hash': v['hash'], 'number': int(v['number'], 16), 'timestamp': int(v['timestamp'], 16)}
    raise ValueError(kind)


def both(urls, c):
    """The value only if both providers agree; otherwise an explicit DISAGREE marker (never one provider's value)."""
    a, b = (dec(c['decode'], rpc(u, c['rpc_method'], c['rpc_params'])) for u in urls)
    return a if a == b else ('DISAGREE', a, b)


def main(argv):
    eth = argv[argv.index('--eth') + 1:argv.index('--eth') + 3] if '--eth' in argv else ETH
    only = argv[argv.index('--only') + 1] if '--only' in argv else ''
    raw = (Path(__file__).resolve().parent / CASE).read_bytes()
    R = json.loads(raw)
    print('case result file sha256', hashlib.sha256(raw).hexdigest())
    print('providers', ' and '.join(eth), '; block', R['facts_as_of']['block'])
    failed = n = 0
    for c in R['checks']:
        if not c['id'].startswith(only):
            continue
        n += 1
        try:
            got = both(eth, c)
        except Exception as e:  # a provider failure is reported as such, never as a pass or a fact
            got = 'NO_ANSWER: %s' % str(e)[:120]
        ok = got == c['expected']
        failed += not ok
        print('%s  %s %s%s' % ('PASS' if ok else 'FAIL', c['subject'] or '-', c['what'],
                               '' if ok else '  (got %r, expected %r)' % (got, c['expected'])))
    print('%d of %d checks passed' % (n - failed, n))
    return 1 if failed or n == 0 else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
