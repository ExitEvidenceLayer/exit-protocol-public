#!/usr/bin/env python3
"""Re-read the main chain facts of the EXIT case note "Arbitrum Security Council, 30 October 2026"
(cases/arbitrum-security-council-2026-10-30.md). Read-only JSON-RPC to two public providers per chain, no keys, standard library only.
A check passes only when BOTH providers return the expected value. Expected values come from the case result file next to this
script (arbitrum-security-council-2026-10-30.json); its SHA-256 is printed so it can be compared with the result_sha256 of the case's
evidence-log records. Exit code 0 only if every check passes.
  python3 arbitrum-security-council-2026-10-30-reread.py [--eth URL URL] [--arb URL URL]"""
import hashlib, http.client, json, sys, time, urllib.request
from pathlib import Path

# Constants: addresses from the case's recorded reads; selectors, role id and event topic are keccak-256 of their signatures.
INBOX = '0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f'
INBOX_PA = '0x554723262467f125ac9e1cdfa9ce15cc53822dbd'
ARB_L1 = '0xb50721bcf8d664c30412cfbc6cf7a15145234ad1'
ARB_PA = '0x5613af0474eb9c528a34701a5b1662e3c8fa0678'
UE = '0x3fffbadaf827559da092217e474760e2b2c3cedd'
SAFE = '0xf06e95ef589d9c38af242a8aaee8375f14023f85'
TL = '0xe6841d92b0c345144506576ec13ecf5103ac7f49'
PE = '0x30668ee252a28986ee6dc21b26e4018ac0e339b9'
USDT = '0xdac17f958d2ee523a2206206994597c13d831ec7'
SEL_OWNER = '0x8da5cb5b'
SEL_HASROLE = '0x91d14854'
SEL_THRESHOLD = '0xe75235b8'
SEL_OWNERS = '0xa0e67e2b'
SEL_MINDELAY = '0xf27a0c92'
SEL_BALANCEOF = '0x70a08231'
SEL_USDT_BL = '0xe47d6060'
SEL_USDC_BL = '0xfe575a87'
EXECUTOR_ROLE = '0xd8aa0f3194971a2a116679f7c2090f6939c8d4e01a2a8d7e41d55e5351469e63'
TOPIC_UPGRADED = '0xbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b'
IMPL_SLOT = '0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc'    # EIP-1967 implementation slot
ADMIN_SLOT = '0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103'   # EIP-1967 admin slot
ETH = ['https://eth.drpc.org', 'https://rpc.mevblocker.io']
ARB = ['https://arb1.arbitrum.io/rpc', 'https://arbitrum.drpc.org']


CACHE = {}


def rpc(url, method, params):
    body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}).encode()
    if (url, body) in CACHE:                    # the same request is asked once per provider
        return CACHE[(url, body)]
    last = None
    for i in range(8):
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


def both(urls, method, params, f=lambda x: x):
    """The value only if both providers agree; otherwise an explicit DISAGREE marker (never one provider's value)."""
    a, b = (f(rpc(u, method, params)) for u in urls)
    return a if a == b else ('DISAGREE', a, b)


addr = lambda word: '0x' + word[-40:]  # noqa: E731


def owners(ret):
    """ABI-decode an address[] return value: offset word, length word, then one word per address."""
    w = [ret[2 + 64 * i:66 + 64 * i] for i in range((len(ret) - 2) // 64)]
    n = int(w[1], 16)
    return ['0x' + x[-40:] for x in w[2:2 + n]]
pad = lambda a: a[2:].lower().rjust(64, '0')  # noqa: E731


def main(argv):
    eth = argv[argv.index('--eth') + 1:argv.index('--eth') + 3] if '--eth' in argv else ETH
    arb = argv[argv.index('--arb') + 1:argv.index('--arb') + 3] if '--arb' in argv else ARB
    raw = (Path(__file__).resolve().parent / 'arbitrum-security-council-2026-10-30.json').read_bytes()
    R = json.loads(raw); P = R['path_at_27oct_block_26285184']; T = R['transaction_30oct']; L2 = R['l2_landing_30oct']
    print('case result file sha256', hashlib.sha256(raw).hexdigest())
    b27, before, txb = 26285184, T['block'] - 1, T['block']
    call = lambda to, data, b: both(eth, 'eth_call', [{'to': to, 'data': data}, hex(b)])  # noqa: E731
    slot = lambda a, s, b: both(eth, 'eth_getStorageAt', [a, s, hex(b)], addr)  # noqa: E731
    checks = [
        ('Inbox proxy admin at block 26,285,184', lambda: slot(INBOX, ADMIN_SLOT, b27), P['inbox_admin']),
        ('owner of the Inbox proxy admin at 26,285,184 = UpgradeExecutor', lambda: addr(call(INBOX_PA, SEL_OWNER, b27)), P['inbox_admin_owner']),
        ('ARB token proxy admin at 26,285,184', lambda: slot(ARB_L1, ADMIN_SLOT, b27), P['arb_l1_admin']),
        ('owner of the ARB proxy admin at 26,285,184 = UpgradeExecutor', lambda: addr(call(ARB_PA, SEL_OWNER, b27)), P['arb_l1_admin_owner']),
        ('executor role: Council Safe, L1 Timelock, pause executor (block before the transaction)',
         lambda: [int(call(UE, SEL_HASROLE + EXECUTOR_ROLE[2:] + pad(a), before), 16) == 1 for a in (SAFE, TL, PE)], [True, True, True]),
        ('Council Safe threshold and its twelve owners at 26,285,184',
         lambda: [int(call(SAFE, SEL_THRESHOLD, b27), 16), owners(call(SAFE, SEL_OWNERS, b27))], [P['council_safe']['threshold'], P['council_safe']['owners']]),
        ('L1 Timelock minimum delay, seconds', lambda: int(call(TL, SEL_MINDELAY, before), 16), P['l1_timelock_min_delay_seconds']),
        ('Inbox implementation at 26,285,184, before and after the transaction',
         lambda: [slot(INBOX, IMPL_SLOT, b) for b in (b27, before, txb)], [P['inbox_implementation']] * 3),
        ('30 October transaction: status, block, sent to the Council Safe',
         lambda: both(eth, 'eth_getTransactionReceipt', [T['hash']], lambda r: [r['status'], int(r['blockNumber'], 16), r['to']]), [T['status'], txb, T['to']]),
        ('Inbox Upgraded events in the transaction, in order',
         lambda: both(eth, 'eth_getTransactionReceipt', [T['hash']], lambda r: [addr(l['topics'][1]) for l in r['logs'] if l['address'].lower() == INBOX
                                                                                   and l['topics'][0] == TOPIC_UPGRADED]), T['inbox_upgrades_in_order']),
        ('USDT blacklist of 0x5227f603... the block before and at the freeze',
         lambda: [int(call(USDT, SEL_USDT_BL + pad(R['usdt_freeze']['added_blacklist'][0]), b), 16) for b in (R['usdt_freeze']['block'] - 1, R['usdt_freeze']['block'])], [0, 1]),
        ('USDC blacklist of 0x5227f603... the block before and at the freeze',
         lambda: [int(call(R['usdc_freeze']['to'], SEL_USDC_BL + pad(R['usdc_freeze']['blacklisted'][0]), b), 16) for b in (R['usdc_freeze']['block'] - 1, R['usdc_freeze']['block'])], [0, 1]),
    ]
    for x in L2:
        checks.append(('Arbitrum One %s: type, sender, nonce, v/r/s, block' % x['hash'][:10],
                       (lambda x=x: both(arb, 'eth_getTransactionByHash', [x['hash']], lambda t: [t['type'], t['from'], int(t['nonce'], 16), [int(t[k], 16) for k in 'vrs'], int(t['blockNumber'], 16)])),
                       [x['type'], x['from'], x['nonce'], [0, 0, 0], x['block']]))
    dest = L2[1]['to']; arb_token = L2[0]['to']
    checks.append(('0x...0DA0 on Arbitrum One holds at least the 74,559,805.2 ARB (latest block)',
                   lambda: int(both(arb, 'eth_call', [{'to': arb_token, 'data': SEL_BALANCEOF + pad(dest)}, 'latest'], lambda r: r), 16) >= 74559805200000000000000000, True))
    checks.append(('0x...0DA0 on Arbitrum One: no code (latest block)', lambda: both(arb, 'eth_getCode', [dest, 'latest']), '0x'))
    failed = 0
    for name, fn, want in checks:
        try:
            got = fn()
        except Exception as e:  # a provider failure is reported as such, never as a pass or a fact
            got = 'NO_ANSWER: %s' % str(e)[:120]
        ok = got == want; failed += not ok
        print('%s  %s%s' % ('PASS' if ok else 'FAIL', name, '' if ok else '  (got %r, expected %r)' % (got, want)))
    print('%d of %d checks passed' % (len(checks) - failed, len(checks)))
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
