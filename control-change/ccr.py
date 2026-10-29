#!/usr/bin/env python3
"""Check an EXIT Control-Change Record (format exit.control-change/1) and derive its evidence-log record.

Python standard library only.

  python3 ccr.py check RECORD.json [--settings control-change-settings.json]
  python3 ccr.py log-record RECORD.json [--settings control-change-settings.json]

check prints {"valid": true} or {"valid": false, "errors": [...]} and exits 0 or 1. A record file must hold the record's
canonical JSON bytes exactly (sorted keys, "," and ":" separators, UTF-8, no trailing newline), so that the SHA-256 of the file
equals the result_sha256 of its log record. log-record prints the log record that binds this change into the EXIT evidence log
(SPEC.txt, version 1): kind research_observation, with result_sha256 = SHA-256 of the canonical record bytes.
"""
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

FORMAT = 'exit.control-change/1'
SETTINGS_FORMAT = 'exit.control-change-settings/1'
FIELDS = {'format', 'chain', 'subject', 'setting', 'scope', 'old_value', 'new_value', 'valid_at', 'known_at', 'evidence', 'reader'}
CHAINS = {'solana-mainnet', 'ethereum-mainnet'}
MAX_UINT = 2 ** 53 - 1
MAX_U64 = 2 ** 64 - 1
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
HEX64 = re.compile(r'[0-9a-f]{64}\Z')
EVM_ADDRESS = re.compile(r'0x[0-9a-f]{40}\Z')
EVM_TX = re.compile(r'0x[0-9a-f]{64}\Z')
BYTES32 = re.compile(r'0x[0-9a-f]{64}\Z')
U64_STRING = re.compile(r'(0|[1-9][0-9]{0,19})\Z')
UTC_TIME = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.([0-9]{3}|[0-9]{6}))?\+00:00\Z')   # ASCII digits only
READER_NAME = re.compile(r'[a-z0-9][a-z0-9.\-]{0,62}/[0-9]{1,4}\Z')
VOTE_KINDS = {'YesVotePercentage', 'QuorumPercentage', 'Disabled'}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()


def b58decode(text):
    if not isinstance(text, str) or not text or any(c not in B58 for c in text):
        return None
    n = 0
    for c in text:
        n = n * 58 + B58.index(c)
    body = n.to_bytes((n.bit_length() + 7) // 8, 'big') if n else b''
    return b'\x00' * (len(text) - len(text.lstrip('1'))) + body


def solana_address(v):
    raw = b58decode(v)
    return raw is not None and len(raw) == 32


def solana_signature(v):
    raw = b58decode(v)
    return raw is not None and len(raw) == 64


def is_uint(v, top=MAX_UINT):
    return type(v) is int and 0 <= v <= top


def utc_time(v):
    if not isinstance(v, str) or not UTC_TIME.match(v):
        return None
    try:
        return datetime.fromisoformat(v)
    except ValueError:
        return None


def address_ok(chain, v):
    return solana_address(v) if chain == 'solana-mainnet' else isinstance(v, str) and bool(EVM_ADDRESS.match(v))


def value_ok(kind, v, entry):
    """True when v is a canonical value of the registry value type kind."""
    if kind == 'solana_address_or_null':
        if v is None:
            return True
        if entry.get('zero_key_is_null') and b58decode(v) == bytes(32):
            return False                       # stored as a non-zero optional key: the all-zero key means none, written null
        return solana_address(v)
    if kind == 'evm_address':
        return isinstance(v, str) and bool(EVM_ADDRESS.match(v))
    if kind == 'evm_address_list':
        return (isinstance(v, list) and all(isinstance(x, str) and EVM_ADDRESS.match(x) for x in v)
                and v == sorted(set(v)))
    if kind == 'uint':
        return (is_uint(v) and entry.get('minimum', 0) <= v <= entry.get('maximum', MAX_UINT)
                and v not in entry.get('excluded', []))
    if kind == 'u64_string':
        return isinstance(v, str) and bool(U64_STRING.match(v)) and int(v) <= MAX_U64
    if kind == 'bytes32':
        return isinstance(v, str) and bool(BYTES32.match(v))
    if kind == 'bool':
        return type(v) is bool
    if kind == 'enum':
        return isinstance(v, str) and v in entry.get('values', [])
    if kind == 'vote_threshold':
        if not (isinstance(v, dict) and set(v) == {'kind', 'percentage'} and isinstance(v['kind'], str) and v['kind'] in VOTE_KINDS):
            return False
        if v['kind'] == 'Disabled':
            return v['percentage'] is None
        return is_uint(v['percentage'], 100) and v['percentage'] >= 1
    return False


def load_settings(path):
    with open(path, 'rb') as fh:
        reg = json.loads(fh.read())
    if not isinstance(reg, dict) or reg.get('format') != SETTINGS_FORMAT or not isinstance(reg.get('settings'), list):
        raise ValueError('not a %s registry' % SETTINGS_FORMAT)
    out = {}
    for e in reg['settings']:
        name = e.get('name') if isinstance(e, dict) else None
        if not isinstance(name, str) or name in out:
            raise ValueError('registry entry without a unique name')
        if e.get('chain') not in CHAINS or not isinstance(e.get('scope'), dict) or e.get('value_type') not in reg.get('value_types', {}):
            raise ValueError('registry entry %s is malformed' % name)
        def constraints_ok(spec):
            if not isinstance(spec, dict) or not set(spec) <= {'minimum', 'maximum', 'excluded'}:
                return False
            lo, hi = spec.get('minimum', 0), spec.get('maximum', MAX_UINT)
            excluded = spec.get('excluded', [])
            return (is_uint(lo) and is_uint(hi) and lo <= hi and isinstance(excluded, list)
                    and all(is_uint(x) and lo <= x <= hi for x in excluded) and len(set(excluded)) == len(excluded))
        numeric = {k: e[k] for k in ('minimum', 'maximum', 'excluded') if k in e}
        scope_specs = e.get('scope_constraints', {})
        if (numeric and (e['value_type'] != 'uint' or not constraints_ok(numeric))
                or not isinstance(scope_specs, dict) or not set(scope_specs) <= set(e['scope'])
                or any(e['scope'][k] != 'uint' or not constraints_ok(v) for k, v in scope_specs.items())):
            raise ValueError('invalid numeric constraints for %s' % name)
        out[name] = e
    return out


def check(record, settings):
    """Every rule of exit.control-change/1 that can be checked from the record itself; returns a list of errors."""
    if not isinstance(record, dict):
        return ['a record is a JSON object']
    errors = []
    keys = set(record)
    if keys != FIELDS:
        missing, extra = sorted(FIELDS - keys), sorted(keys - FIELDS)
        return ['fields differ from the format: missing %s, unexpected %s' % (missing, extra)]
    if record['format'] != FORMAT:
        errors.append('format must be %s' % FORMAT)
    chain = record['chain']
    if not isinstance(chain, str) or chain not in CHAINS:
        return errors + ['chain must be one of %s' % sorted(CHAINS)]
    if not address_ok(chain, record['subject']):
        errors.append('subject is not a canonical %s address' % chain)
    entry = settings.get(record['setting']) if isinstance(record['setting'], str) else None
    if entry is None:
        errors.append('setting is not in the registry')
    elif entry['chain'] != chain:
        errors.append('setting %s belongs to %s, not %s' % (record['setting'], entry['chain'], chain))
    else:
        scope = record['scope']
        if not isinstance(scope, dict) or set(scope) != set(entry['scope']):
            errors.append('scope keys must be exactly %s' % sorted(entry['scope']))
        else:
            for k, kind in entry['scope'].items():
                if not value_ok(kind, scope[k], entry.get('scope_constraints', {}).get(k, {})):
                    errors.append('scope %s is not a canonical %s' % (k, kind))
        for side in ('old_value', 'new_value'):
            if not value_ok(entry['value_type'], record[side], entry):
                errors.append('%s is not a canonical %s' % (side, entry['value_type']))
        if canonical(record['old_value']) == canonical(record['new_value']):
            errors.append('old_value and new_value are equal: a record states a change')
    known = utc_time(record['known_at'])
    if known is None:
        errors.append('known_at must be a UTC time written with +00:00')
    va = record['valid_at']
    if not isinstance(va, dict) or va.get('basis') not in ('transaction', 'bracketing_reads'):
        errors.append('valid_at.basis must be transaction or bracketing_reads')
    elif va['basis'] == 'transaction':
        if set(va) != {'basis', 'transaction', 'position', 'block_time'}:
            errors.append('a transaction valid_at has exactly basis, transaction, position and block_time')
        else:
            tx_ok = solana_signature(va['transaction']) if chain == 'solana-mainnet' else (
                isinstance(va['transaction'], str) and bool(EVM_TX.match(va['transaction'])))
            if not tx_ok:
                errors.append('valid_at.transaction is not a canonical %s transaction id' % chain)
            if not is_uint(va['position']):
                errors.append('valid_at.position must be a slot or block number')
            block_time = utc_time(va['block_time'])
            if block_time is None:
                errors.append('valid_at.block_time must be a UTC time written with +00:00')
            elif known is not None and known < block_time:
                errors.append('known_at is earlier than the block time: a change cannot be known before it happened')
    else:
        if set(va) != {'basis', 'old_read_position', 'new_read_position'}:
            errors.append('a bracketing_reads valid_at has exactly basis, old_read_position and new_read_position')
        elif not (is_uint(va['old_read_position']) and is_uint(va['new_read_position'])):
            errors.append('read positions must be slot or block numbers')
        elif va['old_read_position'] >= va['new_read_position']:
            errors.append('old_read_position must be earlier than new_read_position')
    ev = record['evidence']
    if not (isinstance(ev, list) and ev and all(isinstance(x, str) and HEX64.match(x) for x in ev)):
        errors.append('evidence must be a non-empty list of SHA-256 digests in lowercase hex')
    elif ev != sorted(set(ev)):
        errors.append('evidence must be sorted and without duplicates')
    elif isinstance(va, dict) and va.get('basis') == 'bracketing_reads' and len(ev) < 2:
        errors.append('bracketing reads need the evidence of both reads (at least two digests)')
    rd = record['reader']
    if not (isinstance(rd, dict) and set(rd) == {'name', 'implementation_sha256'}):
        errors.append('reader has exactly name and implementation_sha256')
    else:
        if not (isinstance(rd['name'], str) and READER_NAME.match(rd['name'])):
            errors.append('reader.name must be a schema id such as exit.solana-mint-research/2')
        if not (isinstance(rd['implementation_sha256'], str) and HEX64.match(rd['implementation_sha256'])):
            errors.append('reader.implementation_sha256 must be a SHA-256 digest in lowercase hex')
    return errors


def log_record(record):
    """The evidence-log record (SPEC.txt version 1) that binds a valid Control-Change Record."""
    va = record['valid_at']
    position = va['position'] if va['basis'] == 'transaction' else va['new_read_position']
    return {'kind': 'research_observation', 'chain': record['chain'], 'subject': record['subject'], 'observed_at': position,
            'known_at': record['known_at'], 'evidence': list(record['evidence']),
            'result_sha256': hashlib.sha256(canonical(record)).hexdigest()}


def read_record(path):
    """(record, errors): the file must parse and hold exactly the record's canonical bytes."""
    with open(path, 'rb') as fh:
        raw = fh.read()
    try:
        record = json.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError, ValueError, RecursionError) as e:
        return None, ['not JSON in UTF-8: %s' % (str(e) or type(e).__name__)]
    try:                                       # NaN and Infinity parse, but canonical() refuses them
        if canonical(record) != raw:
            return record, ['the file is not the canonical JSON bytes of its record']
    except ValueError as e:
        return None, ['not canonical JSON: %s' % e]
    return record, []


def main(argv):
    if len(argv) < 2 or argv[0] not in ('check', 'log-record'):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'control-change-settings.json')
    if '--settings' in argv:
        i = argv.index('--settings')
        if i + 1 >= len(argv):
            print('--settings needs a path', file=sys.stderr)
            return 2
        settings_path = argv[i + 1]
    try:
        settings = load_settings(settings_path)
        record, errors = read_record(argv[1])
        if record is not None and not errors:
            errors = check(record, settings)
    except OSError as e:
        record, errors = None, ['cannot read the file: %s' % e]
    except Exception as e:                     # any other failure is a refusal, never a pass and never a traceback
        record, errors = None, ['refused: %s' % type(e).__name__]
    if argv[0] == 'check' or errors:
        print(json.dumps({'valid': not errors, 'errors': errors} if errors else {'valid': True}, indent=1))
        return 0 if not errors else 1
    print(json.dumps(log_record(record), indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
