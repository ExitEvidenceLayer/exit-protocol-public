#!/usr/bin/env python3
"""Re-read the chain facts of the EXIT note "Two mint-authority changes recorded on 20 November 2026"
(cases/control-changes-2026-11-20.md). Read-only, public providers, no keys, standard library only. Expected values come from the
result file next to this script (control-changes-2026-11-20.json); its SHA-256 is printed so it can be compared with the one the
note gives.

Kinds of line:
  MATCH / MISMATCH       one source: the two Control-Change Record files on exit-protocol.io, by their SHA-256 and their fields.
  PASS                   a fixed fact (a block time, a transaction, a list of transactions) that BOTH providers returned as expected.
  ONE_PROVIDER           a fixed fact that one provider returned as expected while the other says it no longer holds that part of the
                         history: an error that says so, or a null answer for a transaction whose slot is before that provider's first
                         available block. A null answer from a provider whose first available block is not after the slot is a FAIL.
  FAIL                   a provider returned something else, or no provider served the fact.
  SAME / CHANGED         a value that can change (a mint's authorities, an account, the token program). Each provider answers at its
                         own finalized slot; both slots are printed. The value is shown next to its value of 21 November 2026. A change
                         is reported, not failed. DISAGREE (the two providers differ) and NO_ANSWER are failures.
Exit code 0 only if no line is MISMATCH, FAIL, DISAGREE or NO_ANSWER.

Known limit: the start of a provider's history is not one sharp number, and it moves forward. On 21 November 2026
solana-rpc.publicnode.com named first available block 471,411,493 inside an error message at 01:35:19 UTC and returned 471,412,567 from
getFirstAvailableBlock at 01:35:20 UTC. A run made in the minutes when that start crosses the slot of a transaction named here can
print FAIL once for that transaction; a later run prints ONE_PROVIDER.

  python3 control-changes-2026-11-20-reread.py [--rpc URL URL] [--save DIR] [--replay DIR] [--curl]

  --rpc URL URL   two Solana JSON-RPC providers of your choice in place of the two public endpoints below
  --save DIR      keep every request and every reply in DIR, with an index (time, URL, file names, SHA-256)
  --replay DIR    answer every request from a DIR written by --save; no network is used
  --curl          send the requests with the curl program instead of Python's urllib
"""
import base64
import datetime
import hashlib
import http.client
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PROVIDERS = ['https://api.mainnet-beta.solana.com', 'https://solana-rpc.publicnode.com']
RESULT_FILE = 'control-changes-2026-11-20.json'
UA = 'exit-case-reread/1'
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
TOKEN_PROGRAMS = ('TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb', 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA')
RETRY_CODES = (429, -32005, -32603, -32014, -32016)            # busy, behind or internal: ask again
GONE_CODES = (-32001, -32004, -32009, -32011)                  # block cleaned up, not available, not in long-term storage, no history
TX_OPTS = {'encoding': 'jsonParsed', 'commitment': 'finalized', 'maxSupportedTransactionVersion': 1}


class NotServed(Exception):
    """The provider answered, and the answer is that it does not hold this part of the history."""


class NoAnswer(Exception):
    """No usable answer after the retries."""


def b58encode(raw):
    n, out = int.from_bytes(raw, 'big'), ''
    while n:
        n, r = divmod(n, 58)
        out = B58[r] + out
    return '1' * (len(raw) - len(raw.lstrip(b'\0'))) + out


def utc(ts):
    return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def host(url):
    return url.split('//', 1)[1].split('/', 1)[0]


class Net:
    """HTTP with an optional record of every request and reply (--save) or answers from such a record (--replay)."""

    def __init__(self, save=None, replay=None, use_curl=False, pause=0.5):
        self.save, self.replay, self.use_curl, self.pause, self.n = save, replay, use_curl, pause, 0
        self.index, self.served = {}, {}
        if replay:
            for line in (Path(replay) / 'INDEX.jsonl').read_text().splitlines():
                row = json.loads(line)
                self.index.setdefault((row['url'], row['request_sha256']), []).append(row)
        if save:
            Path(save).mkdir(parents=True, exist_ok=True)

    def _wire(self, url, body):
        if self.use_curl:
            cmd = ['curl', '-sS', '--max-time', '60', '-A', UA, '-H', 'Accept: application/json']
            if body is not None:
                cmd += ['-H', 'Content-Type: application/json', '--data-binary', '@-']
            r = subprocess.run(cmd + [url], input=body, capture_output=True)
            if r.returncode:
                raise OSError('curl exit %d: %s' % (r.returncode, r.stderr.decode(errors='replace')[:120]))
            return r.stdout
        headers = {'User-Agent': UA, 'Accept': 'application/json', 'Accept-Encoding': 'identity', 'Connection': 'close'}
        if body is not None:
            headers['Content-Type'] = 'application/json'
        try:
            with urllib.request.urlopen(urllib.request.Request(url, body, headers), timeout=40) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            return e.read()                                    # a JSON-RPC error body is an answer; anything else fails to parse

    def fetch(self, url, body=None, label=''):
        """One request, one reply (bytes). Replay: the kept reply, checked against its SHA-256."""
        digest = hashlib.sha256(body if body is not None else b'').hexdigest()
        if self.replay:
            rows = self.index.get((url, digest))
            if not rows:
                raise NoAnswer('no kept reply for %s %s' % (url, label))
            i = self.served.get((url, digest), 0)                # a request sent more than once gets its kept replies in the kept order
            self.served[(url, digest)] = i + 1
            row = rows[min(i, len(rows) - 1)]
            raw = (Path(self.replay) / row['reply_file']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != row['reply_sha256']:
                raise NoAnswer('kept reply %s does not match its SHA-256' % row['reply_file'])
            return raw
        raw = self._wire(url, body)
        time.sleep(self.pause)
        if self.save:
            self.n += 1
            stem = '%04d-%s-%s' % (self.n, host(url), label or 'get')
            if body is not None:
                (Path(self.save) / (stem + '.request.json')).write_bytes(body)
            (Path(self.save) / (stem + '.reply')).write_bytes(raw)
            row = {'n': self.n, 'time_utc': utc(time.time()), 'url': url, 'label': label,
                   'request_file': stem + '.request.json' if body is not None else None, 'request_sha256': digest,
                   'reply_file': stem + '.reply', 'reply_sha256': hashlib.sha256(raw).hexdigest(), 'reply_bytes': len(raw)}
            with open(Path(self.save) / 'INDEX.jsonl', 'a') as f:
                f.write(json.dumps(row, sort_keys=True) + '\n')
        return raw

    def rpc(self, url, method, params, label=''):
        """The JSON-RPC result. NotServed when the provider says it does not hold that history; NoAnswer after the retries."""
        body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}, separators=(',', ':')).encode()
        last = None
        for i in range(8):
            try:
                j = json.loads(self.fetch(url, body, method + ('-' + label if label else '')))
            except NoAnswer:
                raise
            except (OSError, ValueError, http.client.HTTPException) as e:
                last = str(e)[:140]
            else:
                if isinstance(j, dict) and 'result' in j:
                    return j['result']
                err = j.get('error') if isinstance(j, dict) else None
                code = err.get('code') if isinstance(err, dict) else None
                if code in GONE_CODES:
                    raise NotServed(str(err.get('message'))[:140])
                last = str(err)[:140]
                if code not in RETRY_CODES:
                    break
            if not self.replay:
                time.sleep(min(1 + 2 * i, 10))
        raise NoAnswer('%s %s: %s' % (host(url), method, last))


# ---- projections: the part of a reply that the note states ----

def p_mint(v):
    info = v['data']['parsed']['info']
    return {'owner_program': v['owner'], 'executable': v['executable'], 'data_length': v['space'], 'type': v['data']['parsed']['type'],
            'mint_authority': info['mintAuthority'], 'freeze_authority': info['freezeAuthority']}


def p_account(v):
    """Kind of account: owner program, executable flag, data length; for a token-program multisig also m, n and the signers."""
    if v is None:
        return {'exists': False}
    out = {'exists': True, 'owner_program': v['owner'], 'executable': v['executable'], 'data_length': v['space']}
    d = v['data']
    if isinstance(d, dict) and d.get('parsed', {}).get('type') == 'multisig':
        info = d['parsed']['info']
        out.update({'type': 'multisig', 'm': info['numRequiredSigners'], 'n': info['numValidSigners'], 'signers': info['signers']})
    if isinstance(d, dict) and d.get('parsed', {}).get('type') == 'program':
        out.update({'type': 'program', 'program_data': d['parsed']['info']['programData']})
    return out


def p_signer(v):
    """Kind of a signer account: whether the System Program owns it, executable flag, data length. The owner program's address is not kept."""
    if v is None:
        return {'exists': False}
    return {'exists': True, 'owned_by_system_program': v['owner'] == '11111111111111111111111111111111', 'executable': v['executable'], 'data_length': v['space']}


def p_program_data(v):
    """First 45 bytes of an upgradeable loader ProgramData account: tag 3, slot of the last deployment, optional upgrade authority."""
    raw = base64.b64decode(v['data'][0])
    if len(raw) != 45 or raw[:4] != b'\x03\x00\x00\x00':
        raise ValueError('not a ProgramData header')
    return {'owner_program': v['owner'], 'data_length': v['space'], 'last_deployed_slot': int.from_bytes(raw[4:12], 'little'),
            'upgrade_authority': b58encode(raw[13:45]) if raw[12] == 1 else None}


def token_instructions(tx):
    """Every token-program instruction of a transaction, outer and inner, as (type, info); one a provider returns unparsed is ('unparsed', {})."""
    found = []
    groups = [tx['transaction']['message']['instructions']] + [g['instructions'] for g in (tx['meta'].get('innerInstructions') or [])]
    for group in groups:
        for ins in group:
            if ins.get('programId') in TOKEN_PROGRAMS:
                p = ins.get('parsed')
                found.append((p['type'], p.get('info', {})) if isinstance(p, dict) else ('unparsed', {}))
    return found


def p_change_tx(tx):
    if tx is None:
        raise NotServed('getTransaction returned null')
    msg = tx['transaction']['message']
    sets = [info for kind, info in token_instructions(tx) if kind == 'setAuthority']
    outer = [(i.get('program'), i['parsed']['type'] if isinstance(i.get('parsed'), dict) else 'unparsed') for i in msg['instructions']]
    nonce = [i['parsed']['info'] for i in msg['instructions'] if i.get('program') == 'system' and isinstance(i.get('parsed'), dict)
             and i['parsed']['type'] == 'advanceNonce']
    return {'slot': tx['slot'], 'block_time': tx['blockTime'], 'block_time_utc': utc(tx['blockTime']), 'err': tx['meta']['err'],
            'version': tx.get('version'), 'signatures': len(tx['transaction']['signatures']),
            'transaction_signers': [k['pubkey'] for k in msg['accountKeys'] if k['signer']], 'fee_payer': msg['accountKeys'][0]['pubkey'],
            'instructions': ['%s:%s' % o for o in outer], 'inner_instructions': sum(len(g['instructions']) for g in (tx['meta'].get('innerInstructions') or [])),
            'nonce_account': nonce[0]['nonceAccount'] if len(nonce) == 1 else None,
            'nonce_authority': nonce[0]['nonceAuthority'] if len(nonce) == 1 else None,
            'set_authority': [{'authority_type': s.get('authorityType'), 'mint': s.get('mint'),
                               'authority': s.get('multisigAuthority') or s.get('authority'),
                               'authority_is_multisig': 'multisigAuthority' in s, 'new_authority': s.get('newAuthority'),
                               'signers': s.get('signers', [])} for s in sets]}


def p_create_tx(tx):
    if tx is None:
        raise NotServed('getTransaction returned null')
    msg = tx['transaction']['message']
    out = {'slot': tx['slot'], 'block_time': tx['blockTime'], 'block_time_utc': utc(tx['blockTime']), 'err': tx['meta']['err'],
           'version': tx.get('version'), 'transaction_signers': [k['pubkey'] for k in msg['accountKeys'] if k['signer']],
           'fee_payer': msg['accountKeys'][0]['pubkey'], 'create_account': None, 'initialize_multisig': None}
    for ins in msg['instructions']:
        p = ins.get('parsed')
        if isinstance(p, dict) and ins.get('program') == 'system' and p['type'] == 'createAccount':
            i = p['info']
            out['create_account'] = {'new_account': i['newAccount'], 'owner_program': i['owner'], 'data_length': i['space'], 'funded_by': i['source']}
        if isinstance(p, dict) and ins.get('programId') in TOKEN_PROGRAMS and p['type'] == 'initializeMultisig':
            i = p['info']
            out['initialize_multisig'] = {'multisig': i['multisig'], 'm': i['m'], 'signers': i['signers']}
    return out


def p_window_tx(tx, mint):
    """What a transaction does about the mint authority: every SetAuthority instruction of a token program (whatever its target), every
    MintTo or MintToChecked instruction for this mint with the authority it names, and the names of the other token-program instructions."""
    if tx is None:
        raise NotServed('getTransaction returned null')
    acts, other = [], set()
    for kind, info in token_instructions(tx):
        if kind == 'setAuthority':
            acts.append({'instruction': kind, 'target': info.get('mint') or info.get('account'), 'authority_type': info.get('authorityType'),
                         'authority': info.get('multisigAuthority') or info.get('authority'), 'new_authority': info.get('newAuthority')})
        elif kind in ('mintTo', 'mintToChecked') and info.get('mint') == mint:
            acts.append({'instruction': kind, 'authority': info.get('multisigMintAuthority') or info.get('mintAuthority')})
        else:
            other.add(kind)
    return {'slot': tx['slot'], 'err': tx['meta']['err'], 'authority_instructions': acts, 'other_token_instructions': sorted(other)}


def window_counts(transactions, address):
    """(transactions with a SetAuthority instruction, transactions with only mint instructions that name `address` as authority)."""
    sets = sum(1 for r in transactions if any(a['instruction'] == 'setAuthority' for a in r['authority_instructions']))
    mints = sum(1 for r in transactions if r['authority_instructions'] and all(
        a['instruction'] in ('mintTo', 'mintToChecked') and a['authority'] == address for a in r['authority_instructions']))
    return sets, mints


class Reread:
    def __init__(self, net, providers, expected):
        self.net, self.urls, self.x = net, providers, expected
        self.lines = {'MATCH': 0, 'MISMATCH': 0, 'PASS': 0, 'ONE_PROVIDER': 0, 'FAIL': 0, 'SAME': 0, 'CHANGED': 0, 'DISAGREE': 0, 'NO_ANSWER': 0}
        self.first_available = {}

    def out(self, kind, text):
        self.lines[kind] += 1
        print('%-12s %s' % (kind, text), flush=True)

    # -- a fixed fact: every provider that serves it must return the expected value --
    def fixed(self, name, want, fn):
        got, gone = {}, {}
        for url in self.urls:
            try:
                got[url] = fn(url)
            except NotServed as e:
                gone[url] = str(e)
            except (NoAnswer, KeyError, TypeError, ValueError, IndexError) as e:
                got[url] = 'NO_ANSWER: %s' % str(e)[:120]
        wrong = {host(u): v for u, v in got.items() if v != want}
        if wrong:
            self.out('FAIL', '%s  (expected %s; got %s)' % (name, json.dumps(want)[:200], json.dumps(wrong)[:400]))
        elif len(got) == len(self.urls):
            self.out('PASS', name)
        elif got:
            self.out('ONE_PROVIDER', '%s  (served by %s only; %s)' % (name, ', '.join(host(u) for u in got),
                                                                     '; '.join('%s: %s' % (host(u), m) for u, m in gone.items())))
        else:
            self.out('FAIL', '%s  (no provider serves it: %s)' % (name, '; '.join('%s: %s' % (host(u), m) for u, m in gone.items())))
        return 0 if wrong or not got else 2 if len(got) == len(self.urls) else 1

    def transaction(self, url, signature, slot, label):
        tx = self.net.rpc(url, 'getTransaction', [signature, TX_OPTS], label)
        if tx is None and self.first_available[url] <= slot:
            raise ValueError('getTransaction returned null although its first available block %s is not after slot %s'
                             % (format(self.first_available[url], ','), format(slot, ',')))
        return tx

    # -- a current value: both providers, each at its own finalized slot --
    def current(self, name, want, method, params, project, label):
        vals, slots = [], []
        for url in self.urls:
            try:
                r = self.net.rpc(url, method, params, label)
                slots.append(r['context']['slot'])
                v = r['value']
                vals.append([project(a) for a in v] if isinstance(v, list) else project(v))
            except (NotServed, NoAnswer, KeyError, TypeError, ValueError, IndexError) as e:
                self.out('NO_ANSWER', '%s  (%s: %s)' % (name, host(url), str(e)[:140]))
                return None
        if vals[0] != vals[1]:
            self.out('DISAGREE', '%s  (slots %s: %s | %s)' % (name, slots, json.dumps(vals[0])[:300], json.dumps(vals[1])[:300]))
            return None
        if vals[0] == want:
            self.out('SAME', '%s  at finalized slots %s and %s' % (name, format(slots[0], ','), format(slots[1], ',')))
        else:
            self.out('CHANGED', '%s  at finalized slots %s and %s: now %s  |  21 Nov 2026 %s'
                     % (name, format(slots[0], ','), format(slots[1], ','), json.dumps(vals[0]), json.dumps(want)))
        return vals[0]

    def signatures(self, url, address, low_slot, until, label):
        """Signatures of an address newer than `until`, newest first, paged until the list is exhausted; refused when the provider's
        history does not reach `low_slot`."""
        if self.first_available[url] > low_slot:
            raise NotServed('its first available block %s is after slot %s' % (format(self.first_available[url], ','), format(low_slot, ',')))
        rows, before = [], None
        while True:
            opts = {'limit': 1000, 'commitment': 'finalized', 'until': until}
            if before:
                opts['before'] = before
            page = self.net.rpc(url, 'getSignaturesForAddress', [address, opts], label)
            rows += page
            if len(page) < 1000:
                return rows
            before = page[-1]['signature']

    def run(self):
        x = self.x
        print('== Providers: %s' % ' + '.join(host(u) for u in self.urls))
        for url in self.urls:
            try:
                self.first_available[url] = self.net.rpc(url, 'getFirstAvailableBlock', [], 'first')
            except (NotServed, NoAnswer) as e:
                self.first_available[url] = 0
                print('   %s: first available block not answered (%s)' % (host(url), str(e)[:100]))
            else:
                print('   %s: first available block %s' % (host(url), format(self.first_available[url], ',')))

        print('== The two Control-Change Records (one source: exit-protocol.io)')
        for c in x['changes']:
            rec = c['record']
            try:
                raw = self.net.fetch(rec['url'], None, 'record-%04d' % c['record_number'])
                got = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
                j = json.loads(raw)
                got.update({'format': j['format'], 'chain': j['chain'], 'subject': j['subject'], 'setting': j['setting'], 'old_value': j['old_value'],
                            'new_value': j['new_value'], 'basis': j['valid_at']['basis'], 'old_read_position': j['valid_at']['old_read_position'],
                            'new_read_position': j['valid_at']['new_read_position'], 'known_at': j['known_at']})
            except (NoAnswer, OSError, ValueError, KeyError, TypeError) as e:
                got = 'NO_ANSWER: %s' % str(e)[:120]
            want = {k: rec[k] for k in ('sha256', 'bytes', 'format', 'chain', 'subject', 'setting', 'old_value', 'new_value', 'basis',
                                        'old_read_position', 'new_read_position', 'known_at')}
            ok = got == want
            self.out('MATCH' if ok else 'MISMATCH', 'record %s of row %d (%s)%s' % (rec['url'].rsplit('/', 1)[-1], c['row'], c['token'],
                                                                                 '' if ok else '  (got %s)' % json.dumps(got)[:400]))

        print('== Fixed facts: every provider that still serves them must return the expected value')
        for c in x['changes']:
            rec, tag, mint = c['record'], c['symbol'], c['mint']
            for side in ('old', 'new'):
                slot = rec['%s_read_position' % side]
                self.fixed('%s: block time of the %s read position, slot %s = %s' % (tag, 'earlier' if side == 'old' else 'later', format(slot, ','),
                                                                                    rec['%s_read_block_time_utc' % side]),
                           rec['%s_read_block_time_utc' % side], lambda u, s=slot: utc(self.net.rpc(u, 'getBlockTime', [s], 'slot-%d' % s)))
            t = c['change_transaction']
            want = {k: t[k] for k in ('slot', 'block_time', 'block_time_utc', 'err', 'version', 'signatures', 'transaction_signers', 'fee_payer',
                                      'instructions', 'inner_instructions', 'nonce_account', 'nonce_authority', 'set_authority')}
            ok = self.fixed('%s: transaction %s at slot %s (%s) holds one SetAuthority instruction: %s of %s from %s to %s'
                            % (tag, t['signature'], format(t['slot'], ','), t['block_time_utc'], t['set_authority'][0]['authority_type'], mint,
                               t['set_authority'][0]['authority'], t['set_authority'][0]['new_authority']),
                            want, lambda u, s=t['signature'], sl=t['slot']: p_change_tx(self.transaction(u, s, sl, 'change-' + s[:8])))
            s0 = t['set_authority'][0]
            inside = (ok and rec['old_read_position'] < t['slot'] <= rec['new_read_position'] and s0['mint'] == rec['subject']
                      and s0['authority'] == rec['old_value'] and s0['new_authority'] == rec['new_value'] and s0['authority_type'] == 'mintTokens')
            self.out(('PASS' if ok == 2 else 'ONE_PROVIDER') if inside else 'FAIL', '%s: that slot lies after the record\'s earlier read position %s and not after its later one %s, '
                     'and the instruction names the record\'s subject, old value and new value (derived from the lines above)'
                     % (tag, format(rec['old_read_position'], ','), format(rec['new_read_position'], ',')))
            m = t['in_mint_signature_list']
            self.fixed('%s: the mint\'s own signature list holds that transaction (10 entries before %s...)' % (tag, m['before'][:12]), True,
                       lambda u, m=m, s=t['signature'], sl=t['slot']: any(
                           r['signature'] == s and r['slot'] == sl and r['err'] is None for r in self.signatures_before(u, mint, m, sl)))
            cr = c['new_authority']['created']
            want = {k: cr[k] for k in ('slot', 'block_time', 'block_time_utc', 'err', 'version', 'transaction_signers', 'fee_payer', 'create_account',
                                      'initialize_multisig')}
            self.fixed('%s: transaction %s at slot %s (%s) created the new authority account as a multisig, %d of %d'
                       % (tag, cr['signature'], format(cr['slot'], ','), cr['block_time_utc'], cr['initialize_multisig']['m'],
                          len(cr['initialize_multisig']['signers'])),
                       want, lambda u, s=cr['signature'], sl=cr['slot']: p_create_tx(self.transaction(u, s, sl, 'create-' + s[:8])))
            w = c['window']
            for side in ('old', 'new'):
                part = w['%s_authority' % side]
                address = c['%s_authority' % side]['address']
                want_list = [[r['signature'], r['slot']] for r in part['transactions']]
                ok = self.fixed('%s: the %s authority account %s is named in %d transactions after slot %s up to slot %s'
                                % (tag, side, address, len(want_list), format(w['after_slot'], ','), format(w['up_to_slot'], ',')), want_list,
                                lambda u, a=address, p=part, w=w, side=side: sorted(
                                    [[r['signature'], r['slot']] for r in self.signatures(u, a, w['after_slot'], p['until'], '%s-%s' % (tag, side))
                                     if w['after_slot'] < r['slot'] <= w['up_to_slot']], key=lambda e: (e[1], e[0])))
                want_acts = [[r['signature'], {k: r[k] for k in ('slot', 'err', 'authority_instructions', 'other_token_instructions')}]
                             for r in part['transactions']]
                self.fixed('%s: among these %d transactions, a SetAuthority instruction is in %d; the other %d hold mint instructions for the mint '
                           'with that account as authority and no SetAuthority instruction'
                           % (tag, len(want_list), part['set_authority_transactions'], part['mint_only_transactions']), want_acts,
                           lambda u, p=part: [[r['signature'], p_window_tx(self.transaction(u, r['signature'], r['slot'],
                                                                                            'window-' + r['signature'][:8]), mint)] for r in p['transactions']])
                counted = window_counts(part['transactions'], address)
                if counted != (part['set_authority_transactions'], part['mint_only_transactions']) or sum(counted) != len(part['transactions']):
                    self.out('FAIL', '%s: the counts in the result file do not follow from its own transaction list (%s)' % (tag, counted))

        print('== Current values, next to their value of 21 November 2026 (each provider at its own finalized slot)')
        fin = {'encoding': 'jsonParsed', 'commitment': 'finalized'}
        for c in x['changes']:
            tag = c['symbol']
            self.current('%s mint %s: owner program, mint authority, freeze authority' % (tag, c['mint']), c['state_21nov']['mint'],
                         'getAccountInfo', [c['mint'], fin], p_mint, 'mint-' + tag)
            for side in ('new', 'old'):
                a = c['%s_authority' % side]
                self.current('%s %s authority account %s: kind, m of n, signers' % (tag, side, a['address']), a['account'],
                             'getAccountInfo', [a['address'], fin], p_account, '%s-%s-authority' % (tag, side))
        s = x['signer_accounts']
        for i in range(0, len(s['addresses']), 6):
            part = s['addresses'][i:i + 6]
            self.current('kind of the signer accounts %s' % ', '.join(a[:6] + '...' for a in part), [s['accounts'][a] for a in part],
                         'getMultipleAccounts', [part, fin], p_signer, 'signers-%d' % (i // 6 + 1))
        tp = x['token_program']
        self.current('token program %s: executable, owner program, program data account' % tp['address'], tp['account'],
                     'getAccountInfo', [tp['address'], fin], p_account, 'token-program')
        self.current('program data account %s: slot of the last deployment, upgrade authority' % tp['account']['program_data'], tp['program_data'],
                     'getAccountInfo', [tp['account']['program_data'], {'encoding': 'base64', 'commitment': 'finalized',
                                                                       'dataSlice': {'offset': 0, 'length': 45}}], p_program_data, 'program-data')
        n = self.lines
        print('records: %d match, %d mismatch; fixed facts: %d pass, %d one provider, %d fail; current values: %d same, %d changed, %d disagree, %d not answered'
              % (n['MATCH'], n['MISMATCH'], n['PASS'], n['ONE_PROVIDER'], n['FAIL'], n['SAME'], n['CHANGED'], n['DISAGREE'], n['NO_ANSWER']))
        return 1 if n['MISMATCH'] or n['FAIL'] or n['DISAGREE'] or n['NO_ANSWER'] else 0

    def signatures_before(self, url, mint, m, slot):
        if self.first_available[url] > slot:
            raise NotServed('its first available block %s is after slot %s' % (format(self.first_available[url], ','), format(slot, ',')))
        return self.net.rpc(url, 'getSignaturesForAddress', [mint, {'limit': m['limit'], 'commitment': 'finalized', 'before': m['before']}],
                            'mint-list')


def main(argv):
    def opt(name, count):
        if name not in argv:
            return None
        i = argv.index(name)
        vals = argv[i + 1:i + 1 + count]
        del argv[i:i + 1 + count]
        return vals
    argv = list(argv)
    providers = opt('--rpc', 2) or PROVIDERS
    save, replay = opt('--save', 1), opt('--replay', 1)
    use_curl = opt('--curl', 0) is not None
    if argv or len(providers) != 2 or providers[0] == providers[1]:
        print(__doc__)
        return 64
    path = Path(__file__).resolve().parent / RESULT_FILE
    raw = path.read_bytes()
    print('result file %s  sha256 %s' % (RESULT_FILE, hashlib.sha256(raw).hexdigest()))
    net = Net(save[0] if save else None, replay[0] if replay else None, use_curl)
    return Reread(net, providers, json.loads(raw)).run()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
