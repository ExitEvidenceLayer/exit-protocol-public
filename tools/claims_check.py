#!/usr/bin/env python3
"""Compare EXIT's public claims with the live service (standard library only; read-only; one GET per document).

  python3 -I claims_check.py --repo DIR [--live-dir DIR] [--now EPOCH]

Checks (each a named boolean; the exit code is 0 only when all hold):
  api_description_version   the repository's openapi.json info.version equals the live https://api.exit-protocol.io/openapi.json version
  live_rows_match_flags     every STATUS.md table row whose status says LIVE and names a reader has its live_* flag true on the status
                            route, and every true live_* flag has such a row (a route that is live but undocumented is also a mismatch)
  free_period_wording       when the status route reports a continuation with no end date, no sentence of the homepage or the roadmap may say
                            the service is open "until"/"to" the first period's end without also saying it continues; STATUS.md's free-API row
                            must say the service continues
  sitemap_not_behind_pages  every sitemap <lastmod> is not earlier than the HTTP Last-Modified date of the page it names (the file's time on
                            the server: a redeploy that rewrote the file counts as a change), and not in the future
DIR for --repo is a checkout (or a folder holding STATUS.md and openapi.json). --live-dir replaces every network read with files of the same
names under that folder (early-access.json, openapi.json, index.html, ROADMAP.html, sitemap.xml, headers.json) — used by the tests only."""
import json, os, re, sys, time, urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

SITE = 'https://exit-protocol.io'; API = 'https://api.exit-protocol.io'
ROW_FLAGS = {                     # STATUS.md row label fragment -> live_* flags on /v0/early-access
    'Any Solana token mint': ('live_mint_research',), 'Ethereum own-contract reader': ('live_contract_research',),
    'Issuer freeze status': ('live_freeze_research',), 'SPL Governance realm and proposals': ('live_governance_research', 'live_governance_proposals'),
    'LayerZero V2 pathway and peer': ('live_layerzero_research', 'live_layerzero_peer')}
UNTIL = re.compile(r'(open|runs|available)\s+(until|to|through)\s+24\s+November\s+2026', re.I)


class Live:
    def __init__(self, live_dir=None):
        self.dir = live_dir; self.headers = {}
        if live_dir:
            p = os.path.join(live_dir, 'headers.json'); self.headers = json.load(open(p)) if os.path.exists(p) else {}

    def get(self, url, name):
        if self.dir:
            if name.startswith('headers:'):                       # a HEAD-like lookup: fixtures carry only the headers
                return b'', self.headers.get(name, {})
            with open(os.path.join(self.dir, name), 'rb') as fh:
                return fh.read(), self.headers.get(name, {})
        req = urllib.request.Request(url, headers={'User-Agent': 'exit-claims-check/1', 'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read(), {k.lower(): v for k, v in r.headers.items()}


def status_rows(md):
    rows = []
    for line in md.splitlines():
        if line.startswith('|') and line.count('|') >= 4 and not set(line) <= set('|-: '):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if len(cells) >= 2 and cells[0] not in ('Surface',):
                rows.append((cells[0], cells[1], cells[2] if len(cells) > 2 else ''))
    return rows


def main(argv):
    args = dict(zip(argv[1::2], argv[2::2]))
    repo = args.get('--repo') or '.'; live = Live(args.get('--live-dir')); now = float(args.get('--now') or time.time())
    out = {'format': 'exit.claims-check/1', 'run_at': datetime.fromtimestamp(now, timezone.utc).isoformat(), 'checks': {}, 'mismatches': []}
    def miss(check, text):
        out['checks'][check] = False; out['mismatches'].append({'check': check, 'detail': text})
    # 1. API description version
    try:
        repo_v = json.load(open(os.path.join(repo, 'openapi.json')))['info']['version']
        live_v = json.loads(live.get(API + '/openapi.json', 'openapi.json')[0])['info']['version']
        out['api_description'] = {'repository': repo_v, 'live': live_v}
        out['checks']['api_description_version'] = repo_v == live_v
        if repo_v != live_v: miss('api_description_version', 'repository %s, live %s' % (repo_v, live_v))
    except Exception as e:
        miss('api_description_version', 'unreadable: ' + type(e).__name__)
    # 2. LIVE rows vs flags
    try:
        ea = json.loads(live.get(API + '/v0/early-access', 'early-access.json')[0]); flags = {k: v for k, v in ea.items() if k.startswith('live_')}
        md = open(os.path.join(repo, 'STATUS.md'), encoding='utf-8').read(); rows = status_rows(md)
        out['checks']['live_rows_match_flags'] = True; covered = set()
        for label, status, _ in rows:
            for frag, fl in ROW_FLAGS.items():
                if frag.lower() in label.lower():
                    covered |= set(fl); is_live = 'LIVE' in status.upper()
                    for f in fl:
                        if is_live and not flags.get(f): miss('live_rows_match_flags', 'STATUS row "%s" says LIVE but %s is %r' % (label, f, flags.get(f)))
                        if not is_live and flags.get(f): miss('live_rows_match_flags', 'STATUS row "%s" is not LIVE but %s is true' % (label, f))
        for f, v in flags.items():
            if v and f not in covered: miss('live_rows_match_flags', 'live flag %s true but no STATUS row documents it' % f)
        out['live_flags'] = flags
    except Exception as e:
        miss('live_rows_match_flags', 'unreadable: ' + type(e).__name__)
    # 3. free-period wording
    try:
        cont = ea.get('continuation') or {}; continuing = bool(cont.get('enabled_at')) and cont.get('ends_at') is None
        out['continuation'] = {'enabled_at': cont.get('enabled_at'), 'ends_at': cont.get('ends_at'), 'continuing': continuing}
        out['checks']['free_period_wording'] = True
        if continuing:
            for name, url in (('index.html', SITE + '/'), ('ROADMAP.html', SITE + '/ROADMAP.html')):
                text = re.sub(r'<[^>]+>', ' ', live.get(url, name)[0].decode('utf-8', 'replace'))
                for sentence in re.split(r'(?<=[.!?])\s+', text):
                    if UNTIL.search(sentence) and 'continu' not in sentence.lower():   # "runs to 24 November; access then continues" is correct wording
                        miss('free_period_wording', '%s says "%s" without saying the service continues' % (name, UNTIL.search(sentence).group(0)))
            free_rows = [s + ' ' + b for l, s, b in rows if '30-day free' in l.lower() or 'free first api' in l.lower()]
            if not free_rows or not any('continu' in r.lower() for r in free_rows): miss('free_period_wording', 'STATUS.md free-API row does not say the service continues')
    except Exception as e:
        miss('free_period_wording', 'unreadable: ' + type(e).__name__)
    # 4. sitemap vs pages
    try:
        sm = live.get(SITE + '/sitemap.xml', 'sitemap.xml')[0].decode(); out['checks']['sitemap_not_behind_pages'] = True; out['sitemap'] = []
        for loc, lastmod in re.findall(r'<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>', sm):
            path = loc.replace(SITE, '') or '/'; name = 'headers:' + path
            lm = datetime.fromisoformat(lastmod).replace(tzinfo=timezone.utc)
            if lm.timestamp() > now + 86400: miss('sitemap_not_behind_pages', '%s lastmod %s is in the future' % (path, lastmod))
            try:
                hdr = live.get(loc, name)[1] if live.dir else live.get(loc, name)[1]
                page_mod = parsedate_to_datetime(hdr.get('last-modified')) if hdr.get('last-modified') else None
            except Exception:
                page_mod = None
            out['sitemap'].append({'path': path, 'lastmod': lastmod, 'page_last_modified': page_mod.isoformat() if page_mod else None})
            if page_mod and page_mod.date() > lm.date(): miss('sitemap_not_behind_pages', '%s changed %s but the sitemap says %s' % (path, page_mod.date(), lastmod))
    except Exception as e:
        miss('sitemap_not_behind_pages', 'unreadable: ' + type(e).__name__)
    out['ok'] = all(out['checks'].values()) and not out['mismatches']
    print(json.dumps(out, indent=1, sort_keys=True)); return 0 if out['ok'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
