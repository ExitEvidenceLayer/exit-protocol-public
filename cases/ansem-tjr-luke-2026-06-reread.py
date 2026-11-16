#!/usr/bin/env python3
"""Re-read the main facts of the EXIT case note "ANSEM, TJR and LUKE, June 2026" on two public Solana RPC providers.

Read-only. Python standard library only; no keys, no accounts, no writes on chain. It needs the result file
ansem-tjr-luke-2026-06.json next to it (or --result PATH), which lists every transaction the note relies on with the values the chain
returned on 15 November 2026.

  python3 ansem-tjr-luke-2026-06-reread.py [--result PATH] [--save DIR] [--transport curl]

What it does:
  1. Transactions (fixed facts). For every transaction in the result file it asks both providers for getTransaction with the params the
     result file records (encoding jsonParsed, the same maxSupportedTransactionVersion, commitment finalized), and compares the slot, the
     block time, the transaction index, the version, the error, the signers, the lamport changes and token changes the file lists, and the
     logged instruction names it lists. A transaction PASSES only when both providers return exactly those values.
  2. Current values. The three fee-sharing configs (decoded with the published pump_fees layout), the ANSEM mint (authorities, extensions,
     name and symbol), the ANSEM supply, five token balances, and the fee-sharing config and metadata of the other coin that uses the
     symbol ANSEM. Each is read from both providers (again, up to three times, if the two differ because they answered at different slots)
     and printed next to its value of 15 November 2026 as SAME or CHANGED. A change on chain is not a failure; two providers that keep
     disagreeing are.
  3. One later transaction (15 November 2026, 18:19:39 UTC), checked like the fixed facts.
The exit code is 0 only when every transaction passes on both providers and both providers agree on every current value.
--save DIR writes every reply as received, with an index (method, params, provider, UTC time, sha256), for an audit trail.
--transport curl sends each call through /usr/bin/curl instead of urllib (for a network path that cuts long urllib reads)."""
import hashlib, json, os, struct, subprocess, sys, time, base64
import http.client, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROVIDERS = ('api.mainnet-beta.solana.com', 'public.rpc.solanavibestation.com')
GAP = 0.3                       # seconds between calls to one provider
TRIES = 10                      # a cut or refused reply is asked again
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
LATER = {'signature': '3WTMRP8LPQJDGoHSCfiKPW2gdEeJVuzS2kn1Hp2ZKHA33buwvYsyUQWPxD7whWQm5zFAeh5UPMWg2uTFySu4KyBa', 'slot': 469827596,
         'block_time': 1794766779, 'version': 1, 'signers': ['HpKUzxQetUfbEMRRt96HfGZ5w1MjqYaQkhZaLyxDooDW'],
         'instructions': ['SweepCreatorFee', 'CreateFeeSharingConfig', 'MigrateBondingCurveCreator', 'UpdateFeeSharesV2', 'DistributeCreatorFeesV2'],
         'deployer_ansem_account': '4T8fGRJtHQeDn4PhXAehEvFYrXho21h8RPYWsbkmpTLA'}
OTHER = {'mint': '6r1BRGRNS6mWDz7FLR8s1SQsT9XiXp6MSMdNAzarpump', 'config': 'AZ4auxKRdmA8QuE9PnYmGNi6d4sc2hSDrSLUuPr2acZM',
         'name': 'The Xmas Bull', 'symbol': 'ANSEM'}
_last = {}
_save = {'dir': None, 'n': 0}
_transport = {'curl': False}


def b58(b):
    n = int.from_bytes(b, 'big'); s = ''
    while n:
        n, r = divmod(n, 58); s = B58[r] + s
    return '1' * (len(b) - len(b.lstrip(b'\0'))) + s


def now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def rpc(provider, method, params, opener=None):
    """One JSON-RPC call with retries; returns the parsed reply and its raw bytes."""
    body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}).encode()
    last = None
    for attempt in range(TRIES):
        wait = GAP - (time.time() - _last.get(provider, 0))
        if wait > 0:
            time.sleep(wait)
        _last[provider] = time.time()
        try:
            if _transport['curl'] and opener is None:
                q = subprocess.run(['/usr/bin/curl', '-sS', '--fail', '--max-time', '60', '-H', 'Content-Type: application/json', '-A', 'exit-case-reread/1',
                                    '--data-binary', '@-', 'https://' + provider], input=body, capture_output=True)
                if q.returncode != 0:
                    raise OSError('curl exit %d: %s' % (q.returncode, q.stderr.decode(errors='replace')[:200]))
                raw = q.stdout
            else:
                req = urllib.request.Request('https://' + provider, data=body, headers={'Content-Type': 'application/json', 'User-Agent': 'exit-case-reread/1'})
                with (opener or urllib.request.urlopen)(req, timeout=60) as r:
                    raw = r.read()
            d = json.loads(raw)
            if 'error' in d and d['error'].get('code') in (429, -32429, -32005, -32007, -32014) or 'error' in d and 'rate' in str(d['error']).lower():
                last = d['error']; time.sleep(1 + attempt); continue
            save(provider, method, params, raw)
            return d, raw
        except (urllib.error.URLError, http.client.HTTPException, ValueError, OSError) as e:
            last = e; time.sleep(1 + attempt)
    raise RuntimeError('%s %s: no complete reply after %d tries (%s)' % (provider, method, TRIES, last))


def save(provider, method, params, raw):
    if not _save['dir']:
        return
    _save['n'] += 1
    name = '%05d_%s_%s.json' % (_save['n'], {'api.mainnet-beta.solana.com': 'mainnet-beta', 'public.rpc.solanavibestation.com': 'solanavibestation'}.get(provider, 'other'), method)
    d = Path(_save['dir'])
    fd = os.open(d / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, 'wb') as fh:
        fh.write(raw)
    with open(d / 'INDEX.jsonl', 'a', encoding='utf-8') as fh:
        fh.write(json.dumps({'file': name, 'sha256': hashlib.sha256(raw).hexdigest(), 'provider': provider, 'method': method, 'params': params, 'utc': now()}) + '\n')


def keys_of(r):
    ks = [k['pubkey'] if isinstance(k, dict) else k for k in r['transaction']['message']['accountKeys']]
    la = r['meta'].get('loadedAddresses') or {}
    return ks + la.get('writable', []) + la.get('readonly', [])


def signers_of(r):
    return [k['pubkey'] for k in r['transaction']['message']['accountKeys'] if isinstance(k, dict) and k.get('signer')]


def lamport_delta(r, addr):
    m = r['meta']
    return sum(m['postBalances'][i] - m['preBalances'][i] for i, k in enumerate(keys_of(r)) if k == addr)


def token_delta(r, owner, mint):
    m = r['meta']
    f = lambda bs: sum(int(b['uiTokenAmount']['amount']) for b in bs or [] if b.get('owner') == owner and b['mint'] == mint)  # noqa: E731
    return f(m.get('postTokenBalances')) - f(m.get('preTokenBalances'))


def instr_names(r):
    return [l.split('Instruction: ', 1)[1] for l in r['meta'].get('logMessages') or [] if 'Program log: Instruction: ' in l]


def check_tx(want, r):
    """The differences between what the result file lists and one provider's reply; [] means equal."""
    if not isinstance(r, dict) or 'meta' not in r:
        return ['no transaction returned']
    diffs = []
    for k, got in (('slot', r.get('slot')), ('block_time', r.get('blockTime')), ('transaction_index', r.get('transactionIndex')),
                   ('version', r.get('version')), ('err', r['meta'].get('err')), ('signers', signers_of(r))):
        if k in want and want[k] != got:
            diffs.append('%s: want %r, got %r' % (k, want[k], got))
    for a, v in (want.get('lamport_changes') or {}).items():
        if lamport_delta(r, a) != v:
            diffs.append('lamports %s: want %d, got %d' % (a, v, lamport_delta(r, a)))
    for t in want.get('token_changes') or []:
        got = token_delta(r, t['owner'], t['mint'])
        if got != t['raw']:
            diffs.append('tokens %s %s: want %d, got %d' % (t['owner'], t['mint'], t['raw'], got))
    names = instr_names(r)
    for x in want.get('instructions_logged') or []:
        if x not in names:
            diffs.append('instruction %s not logged' % x)
    return diffs


def decode_config(raw):
    n = struct.unpack('<I', raw[76:80])[0]
    return {'discriminator': raw[:8].hex(), 'version': raw[9], 'status': ('Paused', 'Active')[raw[10]], 'mint': b58(raw[11:43]), 'admin': b58(raw[43:75]),
            'admin_revoked': bool(raw[75]),
            'shareholders': [{'address': b58(raw[80 + 34 * i:112 + 34 * i]), 'share_bps': struct.unpack('<H', raw[112 + 34 * i:114 + 34 * i])[0]} for i in range(n)]}


def current_reads(res):
    """name -> (method, params, function(result) -> value, the 15 November value)."""
    out = {}
    for tok, c in res['fee_configs_15_nov'].items():
        want = {k: c[k] for k in ('mint', 'admin', 'admin_revoked', 'shareholders', 'status')}
        out['fee config %s %s' % (tok, c['config'])] = ('getAccountInfo', [c['config'], {'encoding': 'base64', 'commitment': 'finalized'}],
                                                         lambda v: {k: decode_config(base64.b64decode(v['value']['data'][0]))[k] for k in ('mint', 'admin', 'admin_revoked', 'shareholders', 'status')},
                                                         want)
    m = res['ansem_mint_15_nov']

    def mint_view(v):
        info = v['value']['data']['parsed']['info']; ext = {e['extension']: e.get('state') or {} for e in info.get('extensions', [])}
        md = ext.get('tokenMetadata', {})
        return {'owner_program': v['value']['owner'], 'decimals': info['decimals'], 'mint_authority': info.get('mintAuthority'), 'freeze_authority': info.get('freezeAuthority'),
                'metadata_update_authority': md.get('updateAuthority'), 'name': md.get('name'), 'symbol': md.get('symbol'), 'extensions': sorted(ext)}
    out['ANSEM mint %s' % m['mint']] = ('getAccountInfo', [m['mint'], {'encoding': 'jsonParsed', 'commitment': 'finalized'}], mint_view,
                                        {'owner_program': m['token_program'], 'decimals': m['decimals'], 'mint_authority': None, 'freeze_authority': None,
                                         'metadata_update_authority': None, 'name': m['name'], 'symbol': m['symbol'], 'extensions': m['extensions']})
    out['ANSEM supply'] = ('getTokenSupply', [m['mint'], {'commitment': 'finalized'}], lambda v: v['value']['amount'], m['supply_at_slot_469840902']['raw'])
    for k, b in res['balances_15_nov'].items():
        out['balance %s' % k] = ('getTokenAccountsByOwner', [b['owner'], {'mint': b['mint']}, {'encoding': 'jsonParsed', 'commitment': 'finalized'}],
                                 lambda v: str(sum(int(x['account']['data']['parsed']['info']['tokenAmount']['amount']) for x in v['value'])), b['balance']['raw'])
    out['other coin with the symbol ANSEM: fee config %s' % OTHER['config']] = (
        'getAccountInfo', [OTHER['config'], {'encoding': 'base64', 'commitment': 'finalized'}],
        lambda v: {k: decode_config(base64.b64decode(v['value']['data'][0]))[k] for k in ('mint', 'shareholders')},
        {'mint': OTHER['mint'], 'shareholders': [{'address': res['accounts']['deployer'], 'share_bps': 10000}]})
    out['other coin with the symbol ANSEM: mint %s' % OTHER['mint']] = (
        'getAccountInfo', [OTHER['mint'], {'encoding': 'jsonParsed', 'commitment': 'finalized'}],
        lambda v: {k: mint_view(v)[k] for k in ('name', 'symbol')}, {'name': OTHER['name'], 'symbol': OTHER['symbol']})
    return out


def main(argv, opener=None):
    args = dict(zip(argv[1::2], argv[2::2]))
    path = Path(args.get('--result') or Path(__file__).with_name('ansem-tjr-luke-2026-06.json'))
    raw = path.read_bytes(); res = json.loads(raw)
    if res.get('format') != 'exit.case-observation/2' or res.get('case') != 'ansem-tjr-luke-2026-06':
        raise SystemExit('not the ANSEM, TJR and LUKE result file: ' + str(path))
    _transport['curl'] = args.get('--transport') == 'curl'
    if args.get('--save'):
        Path(args['--save']).mkdir(parents=True, exist_ok=False); _save['dir'] = args['--save']
    print('result file %s, sha256 %s' % (path.name, hashlib.sha256(raw).hexdigest()))
    started = now()
    report = {'transactions': {}, 'current': {}, 'later': None}
    fixed_ok = True
    print('\n1. Transactions, on %s and %s' % PROVIDERS)
    for t in res['transactions']:
        p = t['evidence']['params']
        per, shas = [], []
        for prov in PROVIDERS:
            try:
                d, rb = rpc(prov, 'getTransaction', p, opener)
                per.append(check_tx(t, d.get('result'))); shas.append(hashlib.sha256(rb).hexdigest())
            except RuntimeError as e:
                per.append(['not served: %s' % e]); shas.append(None)
        ok = not per[0] and not per[1]
        fixed_ok &= ok
        report['transactions'][t['signature']] = {'id': t['id'], 'status': 'PASS' if ok else 'FAIL', 'diffs': per, 'sha256': shas}
        print('  %-4s %-32s %s%s' % ('PASS' if ok else 'FAIL', t['id'], t['signature'][:16] + '...', '' if ok else '  ' + json.dumps(per)))
    print('\n2. Current values (15 November 2026 value in brackets)')
    agree_ok = True
    for name, (method, params, view, want) in current_reads(res).items():
        vals = None
        for attempt in range(3):
            try:
                vals = [view(rpc(prov, method, params, opener)[0]['result']) for prov in PROVIDERS]
            except (RuntimeError, KeyError, TypeError, IndexError, ValueError) as e:
                vals = ['ERROR %s' % e, None]
            if vals[0] == vals[1]:
                break
            time.sleep(2)
        agree = vals[0] == vals[1] and not str(vals[0]).startswith('ERROR')
        agree_ok &= agree
        state = ('SAME' if vals[0] == want else 'CHANGED') if agree else 'PROVIDERS_DIFFER'
        report['current'][name] = {'state': state, 'values': vals, 'value_15_nov': want}
        print('  %-16s %s: %s  [%s]' % (state, name, json.dumps(vals[0]), json.dumps(want)))
    print('\n3. Later transaction of 15 November 2026, 18:19:39 UTC')
    per, shas = [], []
    p = [LATER['signature'], {'encoding': 'jsonParsed', 'maxSupportedTransactionVersion': 1, 'commitment': 'finalized'}]
    for prov in PROVIDERS:
        try:
            d, rb = rpc(prov, 'getTransaction', p, opener); r = d.get('result')
            diffs = check_tx({'slot': LATER['slot'], 'block_time': LATER['block_time'], 'version': LATER['version'], 'err': None, 'signers': LATER['signers'],
                              'instructions_logged': LATER['instructions']}, r)
            if not diffs:
                acct = [b for b in r['meta']['postTokenBalances'] if b['owner'] == res['accounts']['deployer'] and b['mint'] == res['ansem_mint_15_nov']['mint']]
                ks = keys_of(r)
                if not acct or ks[acct[0]['accountIndex']] != LATER['deployer_ansem_account'] or acct[0]['uiTokenAmount']['amount'] != '0':
                    diffs.append("the deployer's ANSEM token account is not created with 0 ANSEM in this transaction")
            per.append(diffs); shas.append(hashlib.sha256(rb).hexdigest())
        except RuntimeError as e:
            per.append(['not served: %s' % e]); shas.append(None)
    later_ok = not per[0] and not per[1]
    report['later'] = {'signature': LATER['signature'], 'status': 'PASS' if later_ok else 'FAIL', 'diffs': per, 'sha256': shas}
    print('  %-4s %s' % ('PASS' if later_ok else 'FAIL', LATER['signature'][:16] + '...'))
    n_pass = sum(1 for v in report['transactions'].values() if v['status'] == 'PASS')
    summary = {'transactions': len(report['transactions']), 'pass_on_both_providers': n_pass, 'later_transaction': report['later']['status'],
               'current_values': len(report['current']), 'same': sum(1 for v in report['current'].values() if v['state'] == 'SAME'),
               'changed': sum(1 for v in report['current'].values() if v['state'] == 'CHANGED'),
               'providers_differ': sum(1 for v in report['current'].values() if v['state'] == 'PROVIDERS_DIFFER'), 'utc_from': started, 'utc_to': now()}
    print('\n' + json.dumps(summary))
    if _save['dir']:
        rec = dict(summary, providers=list(PROVIDERS), transactions=report['transactions'], current=report['current'], later=report['later'],
                   result_sha256=hashlib.sha256(raw).hexdigest())
        fd = os.open(Path(_save['dir']) / 'SECOND-PROVIDER.json', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(fd, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(rec, indent=1, sort_keys=True) + '\n')
    return 0 if fixed_ok and agree_ok and later_ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
