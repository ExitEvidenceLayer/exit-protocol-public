#!/usr/bin/env python3
"""Re-read the main chain facts of the EXIT case note "Kava Lend, 14 November 2026" (cases/kava-lend-2026-11-14.md). Read-only, public
providers, no keys, standard library only. Expected values come from the case result file next to this script
(kava-lend-2026-11-14.json); its SHA-256 is printed so it can be compared with the one the note gives.

Three kinds of line:
  PASS / FAIL          a fixed fact (a transaction, a receipt, a delivery, a past balance read on two Kava EVM archives). It passes only
                       when BOTH providers return the expected value.
  SAME / CHANGED       a value that can change (the BUSD supply index, Kava Lend's KAVA cash, the community pool's deposit, an open
                       auction, a bridge setting, a Safe, a balance). Both providers are read at the same height or block (a Kava REST reply
                       must echo that height), and the value is printed next to its value of 14 November 2026. A change is reported, not
                       failed: a fix shows as CHANGED. DISAGREE (the two providers differ) and NO_ANSWER are failures; an empty 0x reply to
                       a contract call (peers, owner, a Safe, a balance) counts as NO_ANSWER.
  MATCH / MISMATCH     historical Kava Lend module state at a past height. Only one public archive operator (polkachu) serves it, so these
                       lines are labelled "one provider" and never count as two-provider checks.
Exit code 0 only if every PASS/FAIL check passes, every current value is read alike by both providers, and every one-provider read
matches.
  python3 kava-lend-2026-11-14-reread.py [--kava-rest URL URL] [--kava-evm URL URL] [--bsc URL URL] [--archive URL]"""
import hashlib, http.client, json, sys, time, urllib.error, urllib.request
from pathlib import Path

KAVA_REST = ['https://api2.kava.io', 'https://kava-api.polkachu.com']
KAVA_EVM = ['https://evm.kava-rpc.com', 'https://kava.drpc.org']          # also usable: https://rpc.ankr.com/kava_evm, https://kava.api.onfinality.io/public
BSC = ['https://bsc-dataseed1.binance.org', 'https://bsc-rpc.publicnode.com']
ARCHIVE = 'https://kava-api.polkachu.com'                                    # the one public archive of past Kava Lend module state
# Event topics and selectors: keccak-256 of their signatures.
T_OFT_SENT = '0x85496b760a4b7f8d66384b9df21b381f5d1b1e79f229a47aaf4c232edc2fe59a'      # OFTSent(bytes32,uint32,address,uint256,uint256)
T_PACKET_SENT = '0x1ab700d4ced0c005b164c0f789fd09fcbb0156d4c2041b8a3bfbcd961cd1567f'   # PacketSent(bytes,bytes,address)
T_TRANSFER = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'      # Transfer(address,address,uint256)
T_DELIVERED = '0x3cd5e48f9730b129dc7550f0fcea9c767b7be37837cd10e55eb35f734f4bca04'     # PacketDelivered((uint32,bytes32,uint64),address)
SEL_PEERS, SEL_OWNER, SEL_GET_OWNERS, SEL_THRESHOLD, SEL_BALANCE_OF = '0xbb0b6a53', '0x8da5cb5b', '0xa0e67e2b', '0xe75235b8', '0x70a08231'
UA = {'User-Agent': 'exit-case-reread/1', 'Accept': 'application/json', 'Accept-Encoding': 'identity', 'Connection': 'close'}


def fetch(url, body=None, headers=None):
    """One HTTP request with retries (a reply cut short is asked again); returns (parsed JSON or None for HTTP 404, response headers).
    Raises after 10 tries."""
    last = None
    for i in range(10):
        try:
            req = urllib.request.Request(url, body, dict(UA, **(headers or {}), **({'Content-Type': 'application/json'} if body else {})))
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read()), {k.lower(): v for k, v in r.headers.items()}
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None, {}
            last = e
        except (OSError, ValueError, http.client.HTTPException) as e:
            last = e
        time.sleep(min(1 + i, 5))
    raise RuntimeError('%s: %s' % (url, str(last)[:160]))


def rest(base, path, height=None):
    """Cosmos REST GET; with a height, the provider must echo it (a provider that ignores the height header would answer for the latest block)."""
    j, h = fetch(base + path, headers={'x-cosmos-block-height': str(height)} if height else None)
    if height and h.get('grpc-metadata-x-cosmos-block-height') != str(height):
        raise RuntimeError('%s did not answer for height %s' % (base, height))
    return j


def rpc(url, method, params):
    j, _ = fetch(url, json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}).encode())
    if not isinstance(j, dict) or 'result' not in j:
        raise RuntimeError('%s: %s' % (url, str(j)[:160]))
    return j['result']


def both(urls, f):
    """The value only when both providers give the same; otherwise a DISAGREE marker (never one provider's value)."""
    a, b = f(urls[0]), f(urls[1])
    return a if a == b else ('DISAGREE', a, b)


word = lambda data, i: data[2 + 64 * i:2 + 64 * (i + 1)]  # noqa: E731
addr = lambda w: '0x' + w[-40:]  # noqa: E731
pad = lambda a: a[2:].lower().rjust(64, '0')  # noqa: E731


def addresses(ret):
    """ABI address[]: offset word, length word, then one word per address."""
    n = int(word(ret, 1), 16)
    return [addr(word(ret, 2 + i)) for i in range(n)]


def coin(coins, denom):
    v = [c['amount'] for c in coins if c['denom'] == denom]
    return v[0] if len(v) == 1 else None


def tx_summary(j):
    """Height, time, code, fee payer and signer count of a Cosmos transaction from the REST tx endpoint."""
    r, a = j['tx_response'], j['tx']['auth_info']
    return [int(r['height']), r['timestamp'], r['code'], a['fee'].get('payer'), len(a['signer_infos'])]


def send_receipt(r):
    oft = [l for l in r['logs'] if l['topics'][0] == T_OFT_SENT]
    ps = [l for l in r['logs'] if l['topics'][0] == T_PACKET_SENT]
    raw = bytes.fromhex(ps[0]['data'][2:]) if len(ps) == 1 else b''
    off = int.from_bytes(raw[0:32], 'big') if raw else 0
    payload = raw[off + 32:off + 32 + int.from_bytes(raw[off:off + 32], 'big')] if raw else b''
    return [r['status'], int(r['blockNumber'], 16), r['from'], r['to'], [int(word(l['data'], 0), 16) for l in oft], [str(int(word(l['data'], 1), 16)) for l in oft],
            int.from_bytes(payload[1:9], 'big') if payload else None]


def delivery_receipt(r, token, recipient):
    mints = [str(int(l['data'], 16)) for l in r['logs'] if l['address'].lower() == token and l['topics'][0] == T_TRANSFER
             and int(l['topics'][1], 16) == 0 and addr(l['topics'][2]) == recipient]
    pd = [l['data'] for l in r['logs'] if l['topics'][0] == T_DELIVERED]
    return [r['status'], int(r['blockNumber'], 16), mints, [[int(word(d, 0), 16), addr(word(d, 1)), int(word(d, 2), 16)] for d in pd]]


def main(argv):
    def opt(name, default, n=2):
        return argv[argv.index(name) + 1:argv.index(name) + 1 + n] if name in argv else default
    krest, kevm, bsc = opt('--kava-rest', KAVA_REST), opt('--kava-evm', KAVA_EVM), opt('--bsc', BSC)
    archive = opt('--archive', [ARCHIVE], 1)[0]
    raw = (Path(__file__).resolve().parent / 'kava-lend-2026-11-14.json').read_bytes()
    R = json.loads(raw)
    print('case result file sha256', hashlib.sha256(raw).hexdigest())
    acc, mod, con = R['accounts'], R['modules'], R['contracts']
    A1, A2, A3, Rbsc = acc['A1']['kava'], acc['A2']['kava'], acc['A3']['kava'], acc['A5']['evm']
    HARD, HARD_EVM, COMM = mod['kava_lend_x_hard']['kava'], mod['kava_lend_x_hard']['evm'], mod['community']['kava']
    ADAPTER, TOKEN = con['oft_adapter_kava_evm']['address'], con['kava_token_bsc']['address']
    fixed, state, one = [], [], []

    # pinned common heights for the current values (both providers read the same height or block)
    def kava_height():
        h = min(int(rest(u, '/cosmos/base/tendermint/v1beta1/blocks/latest')['block']['header']['height']) for u in krest)
        return h - 3

    def evm_block(urls):
        return min(int(rpc(u, 'eth_blockNumber', []), 16) for u in urls) - 3

    tr = R['trigger']
    fixed.append(('Kava: transaction 6C00E9ED... (A1 repays all 37 BUSD loans): height, time, code, fee payer, signers, MsgRepay count by A1',
                  lambda: both(krest, lambda u: (lambda j: tx_summary(j) + [sum(1 for m in j['tx']['body']['messages'] if m['@type'].endswith('MsgRepay') and m['sender'] == A1)])(
                      rest(u, '/cosmos/tx/v1beta1/txs/' + tr['repay_tx']['tx']))),
                  [tr['repay_tx']['height'], tr['repay_tx']['utc'], 0, A3, 2, 37]))
    fixed.append(('Kava: transaction D5D8F728... (A1 deposits, borrows and withdraws BUSD): height, time, code, fee payer, messages',
                  lambda: both(krest, lambda u: (lambda j: tx_summary(j)[:4] + [[[m['@type'].rsplit('.', 1)[1], m.get('depositor') or m.get('borrower'), m['amount']] for m in j['tx']['body']['messages']]])(
                      rest(u, '/cosmos/tx/v1beta1/txs/' + tr['set_tx']['tx']))),
                  [tr['set_tx']['height'], tr['set_tx']['utc'], 0, A3, [[m['type'], m['by'], [{'denom': 'busd', 'amount': m['amount']['raw']}]] for m in tr['set_tx']['messages']]]))
    for key, label in (('first', 'first'), ('last_127th', '127th')):
        x = R['loop'][key]
        fixed.append(('Kava: %s loop transaction %s...: height, time, code, fee payer, 3 signers, the KAVA borrow of A2' % (label, x['tx'][:8]),
                      (lambda x=x: both(krest, lambda u: (lambda j: tx_summary(j) + [[m['amount'] for m in j['tx']['body']['messages'] if m['@type'].endswith('MsgBorrow') and m['borrower'] == A2]])(
                          rest(u, '/cosmos/tx/v1beta1/txs/' + x['tx'])))),
                      [x['height'], x['utc'], 0, A3, 3, [[{'denom': 'ukava', 'amount': x['kava_borrowed']['raw']}]]]))
    lq = R['liquidations']['first_tx']
    fixed.append(('Kava: liquidation transaction 3F79C5AD... (auction 25188): height, time, code, MsgLiquidate keeper A1 and borrower A2',
                  lambda: both(krest, lambda u: (lambda j: tx_summary(j)[:3] + [[[m['keeper'], m['borrower']] for m in j['tx']['body']['messages'] if m['@type'].endswith('MsgLiquidate')]])(
                      rest(u, '/cosmos/tx/v1beta1/txs/' + lq['tx']))),
                  [lq['height'], lq['utc'], 0, [[A1, A2]]]))
    fixed.append(('Kava: the community account is a module account named community',
                  lambda: both(krest, lambda u: (lambda a: [a.get('@type'), a.get('name')])(rest(u, '/cosmos/auth/v1beta1/accounts/' + COMM)['account'])),
                  [mod['community']['account_type'], mod['community']['name']]))
    kl = R['kava_lend_kava']
    for h, k in ((23484000, 'cash_23484000'), (23493000, 'cash_23493000')):
        fixed.append(('Kava EVM archives: Kava Lend module KAVA at height %s (eth_getBalance of %s...)' % (format(h, ','), HARD_EVM[:10]),
                      (lambda h=h: both(kevm, lambda u: str(int(rpc(u, 'eth_getBalance', [HARD_EVM, hex(h)]), 16)))),
                      str(int(kl[k]['raw']) * 10 ** 12)))
    for s in R['to_bsc']['oft_sends']:
        fixed.append(('Kava EVM: LayerZero send %s...: status, block, from, to the adapter, OFTSent destination and amount, packet nonce' % s['tx'][:10],
                      (lambda s=s: both(kevm, lambda u: send_receipt(rpc(u, 'eth_getTransactionReceipt', [s['tx']])))),
                      [s['status'], s['block'], s['from'], s['to'], [s['dst_eid']], [s['oft_sent_amount']['raw']], s['nonce']]))
    for d in R['to_bsc']['bsc_deliveries']:
        fixed.append(('BNB Smart Chain: delivery %s...: status, block, KAVA minted to %s..., PacketDelivered source, sender and nonce' % (d['tx'][:10], Rbsc[:10]),
                      (lambda d=d: both(bsc, lambda u: delivery_receipt(rpc(u, 'eth_getTransactionReceipt', [d['tx']]), TOKEN, Rbsc))),
                      [d['status'], d['block'], [d['amount']['raw']], [[d['src_eid'], ADAPTER, d['nonce']]]]))

    # current values, next to their value of 14 November 2026
    st = R['status_1947']
    H = {}

    def kh():
        if 'k' not in H:
            H['k'] = kava_height()
        return H['k']

    state.append(('Kava Lend BUSD supply interest index', lambda: both(krest, lambda u: rest(u, '/kava/hard/v1beta1/interest-factors?denom=busd', kh())['interest_factors'][0]['supply_interest_factor']),
                  st['busd_supply_index']))
    state.append(('Kava Lend KAVA cash (module account balance, ukava)', lambda: both(krest, lambda u: rest(u, '/cosmos/bank/v1beta1/balances/%s/by_denom?denom=ukava' % HARD, kh())['balance']['amount']),
                  st['kava_lend_kava_cash']['raw']))
    state.append(('community pool deposit record in Kava Lend (ukava, as stored)', lambda: both(krest, lambda u: (lambda d: coin(d[0]['amount'], 'ukava') if d else 'no record')(
        rest(u, '/kava/hard/v1beta1/unsynced-deposits?owner=' + COMM, kh())['deposits'])), st['community_deposit_record']['raw']))
    state.append(('second group: BUSD deposit of %s... (synced, base units)' % acc['B1'][:12], lambda: both(krest, lambda u: (lambda d: coin(d[0]['amount'], 'busd') if d else 'no record')(
        rest(u, '/kava/hard/v1beta1/deposits?owner=' + acc['B1'], kh())['deposits'])), st['b1_busd_deposit_synced']['raw']))
    pm = R['kava_lend_params_23493000']
    state.append(('Kava Lend borrow limits of the KAVA and BUSD markets', lambda: both(krest, lambda u: (lambda mm: {k: mm.get(k) for k in ('ukava', 'busd')})(
        {m['denom']: m['borrow_limit'] for m in rest(u, '/kava/hard/v1beta1/params', kh())['params']['money_markets']})), {'ukava': pm['ukava'], 'busd': pm['busd']}))
    a25 = R['liquidations']['auction_25188_at_1947']
    state.append(('auction 25188: lot, maximum bid, bids received, end time', lambda: both(krest, lambda u: (lambda a: 'no such auction' if a is None else
        [a['base_auction']['lot'], a['max_bid'], a['base_auction']['has_received_bids'], a['base_auction']['end_time']])(
        rest(u, '/kava/auction/v1beta1/auctions/25188', kh())['auction'])),      # a closed auction answers {"auction": null} for the height
        [a25['lot'], a25['max_bid'], a25['has_received_bids'], a25['end_time']]))

    def eb(key, urls):
        if key not in H:
            H[key] = evm_block(urls)
        return hex(H[key])

    def nonempty(u, to, data, block):
        r = rpc(u, 'eth_call', [{'to': to, 'data': data}, block])
        if not isinstance(r, str) or len(r) < 66:          # an empty 0x reply (no code, or no such function) is no answer, never a change
            raise RuntimeError('%s: empty eth_call reply %r from %s' % (to, r, u))
        return r

    call = lambda urls, key: (lambda to, data: both(urls, lambda u: nonempty(u, to, data, eb(key, urls))))  # noqa: E731
    kcall, bcall = call(kevm, 'e'), call(bsc, 'b')
    ad, aso, ts, tso = con['oft_adapter_kava_evm'], con['adapter_owner_safe'], con['kava_token_bsc'], con['token_owner_safe']
    state.append(('Kava OFT adapter: peer for BNB Smart Chain (eid 30102), and owner', lambda: (lambda p, o: [p if isinstance(p, tuple) else addr(p), o if isinstance(o, tuple) else addr(o)])(
        kcall(ADAPTER, SEL_PEERS + pad(hex(30102))), kcall(ADAPTER, SEL_OWNER)), [ad['peer_for_eid_30102'], ad['owner']]))
    state.append(('adapter owner Safe (Kava EVM): threshold and owners', lambda: (lambda t, o: [t if isinstance(t, tuple) else int(t, 16), o if isinstance(o, tuple) else addresses(o)])(
        kcall(aso['address'], SEL_THRESHOLD), kcall(aso['address'], SEL_GET_OWNERS)), [aso['threshold'], aso['owners']]))
    state.append(('KAVA token on BNB Smart Chain: owner, and peer for Kava (eid 30177)', lambda: (lambda o, p: [o if isinstance(o, tuple) else addr(o), p if isinstance(p, tuple) else addr(p)])(
        bcall(TOKEN, SEL_OWNER), bcall(TOKEN, SEL_PEERS + pad(hex(30177)))), [ts['owner'], ts['peer_for_eid_30177']]))
    state.append(('token owner Safe (BNB Smart Chain): threshold and owners', lambda: (lambda t, o: [t if isinstance(t, tuple) else int(t, 16), o if isinstance(o, tuple) else addresses(o)])(
        bcall(tso['address'], SEL_THRESHOLD), bcall(tso['address'], SEL_GET_OWNERS)), [tso['threshold'], tso['owners']]))
    state.append(('KAVA balance of %s... on BNB Smart Chain (wei)' % Rbsc[:10], lambda: (lambda v: v if isinstance(v, tuple) else str(int(v, 16)))(bcall(TOKEN, SEL_BALANCE_OF + pad(Rbsc))),
                  R['sale']['r_kava_balance_bsc_latest']))

    # historical module state: one provider
    for h, v in sorted(R['busd_supply_index']['by_height'].items()):
        one.append(('BUSD supply interest index at height %s' % format(int(h), ','), (lambda h=h: rest(archive, '/kava/hard/v1beta1/interest-factors?denom=busd', int(h))['interest_factors'][0]['supply_interest_factor']), v))
    tm = R['busd_market']['terms_at_23484805']
    one.append(('BUSD market at height 23,484,805: cash, borrows, reserves (base units)', lambda: [
        rest(archive, '/cosmos/bank/v1beta1/balances/%s/by_denom?denom=busd' % HARD, 23484805)['balance']['amount'],
        coin(rest(archive, '/kava/hard/v1beta1/total-borrowed?denom=busd', 23484805)['borrowed_coins'], 'busd'),
        coin(rest(archive, '/kava/hard/v1beta1/reserves?denom=busd', 23484805)['amount'], 'busd')], [tm['cash']['raw'], tm['borrows']['raw'], tm['reserves']['raw']]))
    for h, v in sorted(R['a1_busd_deposit'].items()):
        one.append(("A1's synced BUSD deposit at height %s (base units)" % format(int(h), ','), (lambda h=h: coin(rest(archive, '/kava/hard/v1beta1/deposits?owner=' + A1, int(h))['deposits'][0]['amount'], 'busd')), v['raw']))
    one.append(('Kava Lend total KAVA supplied at height 23,484,000 (ukava)', lambda: coin(rest(archive, '/kava/hard/v1beta1/total-deposited?denom=ukava', 23484000)['supplied_coins'], 'ukava'),
                kl['total_supplied_23484000']['raw']))
    one.append(('community pool deposit record at height 23,484,000 (ukava)', lambda: coin(rest(archive, '/kava/hard/v1beta1/unsynced-deposits?owner=' + COMM, 23484000)['deposits'][0]['amount'], 'ukava'),
                R['community_pool']['deposit_at_23484000']['raw']))
    for h, v in sorted(R['kava_supply'].items()):
        one.append(('total KAVA supply at height %s (ukava)' % format(int(h), ','), (lambda h=h: rest(archive, '/cosmos/bank/v1beta1/supply/by_denom?denom=ukava', int(h))['amount']['amount']), v['raw']))

    failed = 0
    print('== Fixed facts: two providers each (Kava REST %s; Kava EVM %s; BNB Smart Chain %s)' % (' + '.join(krest), ' + '.join(kevm), ' + '.join(bsc)))
    for name, fn, want in fixed:
        try:
            got = fn()
        except Exception as e:  # a provider failure is reported as such, never as a pass or a fact
            got = 'NO_ANSWER: %s' % str(e)[:140]
        ok = got == want; failed += not ok
        print('%s  %s%s' % ('PASS' if ok else 'FAIL', name, '' if ok else '  (got %r, expected %r)' % (got, want)))
    print('== Current values, next to their value of 14 November 2026 (both providers at the same height or block)')
    changed = bad_state = 0
    for name, fn, want in state:
        try:
            got = fn()
        except Exception as e:
            got = 'NO_ANSWER: %s' % str(e)[:140]
        if isinstance(got, tuple) or (isinstance(got, str) and got.startswith('NO_ANSWER')) or (isinstance(got, list) and any(isinstance(x, tuple) for x in got)):
            bad_state += 1
            print('%s  %s  (%r)' % ('NO_ANSWER' if isinstance(got, str) else 'DISAGREE ', name, got))
            continue
        same = got == want; changed += not same
        print('%s  %s  now %s  |  14 Nov 2026 %s' % ('SAME   ' if same else 'CHANGED', name, json.dumps(got), json.dumps(want)))
    print('   heights read: Kava %s, Kava EVM %s, BNB Smart Chain %s' % (H.get('k'), H.get('e'), H.get('b')))
    print('== Historical Kava Lend module state: one provider (%s, the only public archive of it)' % archive)
    mism = 0
    for name, fn, want in one:
        try:
            got = fn()
        except Exception as e:
            got = 'NO_ANSWER: %s' % str(e)[:140]
        ok = got == want; mism += not ok
        print('%s  %s  (one provider)%s' % ('MATCH   ' if ok else 'MISMATCH', name, '' if ok else '  (got %r, expected %r)' % (got, want)))
    print('%d of %d two-provider checks passed; %d current values: %d same, %d changed, %d not read alike; %d of %d one-provider reads matched'
          % (len(fixed) - failed, len(fixed), len(state), len(state) - changed - bad_state, changed, bad_state, len(one) - mism, len(one)))
    return 1 if failed or bad_state or mism else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
