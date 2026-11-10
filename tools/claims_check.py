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
                            the server: a redeploy that rewrote the file counts as a change), and not in the future. v3 (4 Nov): every
                            <url> entry is accounted for (XML parse, any element order); a page date that cannot be read is a mismatch, never
                            a skip (one HEAD request per page); an entry without <lastmod> fails unless UNDATED_OK names the check that covers
                            it (only /log/); no dated entry checked at all fails; sitemap_coverage in the output states what was checked
  status_client_row_version the STATUS.md row "Public script/agent client" names the API description version it describes, and that
                            version equals the repository's openapi.json info.version (the sentence about the copy, checked against the copy —
                            added 2 November after that sentence was found a version behind); when exit_mcp.py is in the checkout, the row's
                            "(N tools, server X)" must also match the MCP server's own tool list and version; since 10 Nov the server versions the row names are
                            compared (the row must name only the current server; forms this check does not read fail), and a row naming a
                            server fails when exit_mcp.py is absent (the sentinel had skipped it: it fetched only
                            STATUS.md, openapi.json and this file)
  spec_version_matches      STATUS.md's "(SPEC.txt) is version X" equals the version in the first line of the live log/SPEC.txt (added 3 Nov
                            after STATUS still said 1.4 while the specification was 1.5)
  reanchor_wording          when the live log/runs.json shows a heartbeat run (outcome HEARTBEAT_*), no sentence of STATUS.md (or ROADMAP.md
                            when present in the checkout) may say that re-anchoring an unchanged root has not been needed yet (added 3 Nov)
These two are the last rules added for now: a public claim is checked here only when it was found wrong on the live surface.
DIR for --repo is a checkout (or a folder holding STATUS.md, openapi.json and exit_mcp.py). --live-dir replaces every network read with files of the same
names under that folder (early-access.json, openapi.json, index.html, ROADMAP.html, sitemap.xml, headers.json, SPEC.txt, runs.json) — used by
the tests only."""
import json, os, re, sys, time, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

SITE = 'https://exit-protocol.io'; API = 'https://api.exit-protocol.io'
ROW_FLAGS = {                     # STATUS.md row label fragment -> live_* flags on /v0/early-access
    'Any Solana token mint': ('live_mint_research',), 'Ethereum own-contract reader': ('live_contract_research',),
    'Issuer freeze status': ('live_freeze_research',), 'SPL Governance realm and proposals': ('live_governance_research', 'live_governance_proposals'),
    'LayerZero V2 pathway and peer': ('live_layerzero_research', 'live_layerzero_peer')}
UNDATED_OK = {'/log/': 'anchor_within_26h and run_within_26h of the log sentinel (the daily run rewrites /log/ at 00:30 UTC)'}
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

    def head(self, url, name):
        """Headers only (v3): a page's date needs no body, and a cut-short body must not turn into a skipped check."""
        if self.dir:
            return self.headers[name]                             # KeyError when the fixture has no headers for the page: unreadable
        req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'exit-claims-check/1', 'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(req, timeout=30) as r:
            return {k.lower(): v for k, v in r.headers.items()}


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
    # 4. sitemap vs pages (v3: every entry accounted for; an unreadable page date or an uncovered undated entry is a mismatch)
    try:
        sm = live.get(SITE + '/sitemap.xml', 'sitemap.xml')[0].decode(); out['checks']['sitemap_not_behind_pages'] = True; out['sitemap'] = []
        if '<!DOCTYPE' in sm or '<!ENTITY' in sm:
            raise ValueError('DOCTYPE in sitemap')
        name_of = lambda e: e.tag.rsplit('}', 1)[-1]  # noqa: E731
        urls = [u for u in ET.fromstring(sm) if name_of(u) == 'url']
        cov = out['sitemap_coverage'] = {'entries': len(urls), 'dated_checked': 0, 'undated_allowed': {}}
        for u in urls:
            f = {name_of(c): (c.text or '').strip() for c in u}; loc, lastmod = f.get('loc', ''), f.get('lastmod')
            if not loc.startswith(SITE):
                miss('sitemap_not_behind_pages', 'an entry without an exit-protocol.io <loc>: %r' % loc[:80]); continue
            path = loc[len(SITE):] or '/'
            if not lastmod:
                if path in UNDATED_OK:
                    cov['undated_allowed'][path] = UNDATED_OK[path]; out['sitemap'].append({'path': path, 'lastmod': None, 'covered_by': UNDATED_OK[path]})
                else:
                    miss('sitemap_not_behind_pages', '%s has no <lastmod> and no other check covers it' % path)
                continue
            lm = datetime.fromisoformat(lastmod).replace(tzinfo=timezone.utc)
            if lm.timestamp() > now + 86400: miss('sitemap_not_behind_pages', '%s lastmod %s is in the future' % (path, lastmod))
            try:
                page_mod = parsedate_to_datetime(live.head(loc, 'headers:' + path)['last-modified'])
            except Exception as e:
                miss('sitemap_not_behind_pages', '%s: the page Last-Modified is unreadable (%s)' % (path, type(e).__name__))
                out['sitemap'].append({'path': path, 'lastmod': lastmod, 'page_last_modified': None}); continue
            cov['dated_checked'] += 1; out['sitemap'].append({'path': path, 'lastmod': lastmod, 'page_last_modified': page_mod.isoformat()})
            if page_mod.date() > lm.date(): miss('sitemap_not_behind_pages', '%s changed %s but the sitemap says %s' % (path, page_mod.date(), lastmod))
        if not cov['dated_checked']: miss('sitemap_not_behind_pages', 'no dated sitemap entry was checked')
    except Exception as e:
        miss('sitemap_not_behind_pages', 'unreadable: ' + type(e).__name__)
    # 5. the status row about the client/API copy, checked against the copy itself (and the MCP server file when present)
    try:
        crow = [(l, st, b) for l, st, b in rows if 'script/agent client' in l.lower()]
        if not crow: miss('status_client_row_version', 'no STATUS row names the public script/agent client')
        else:
            cell = crow[0][2]; m = re.search(r'version (\d{4}-\d{2}-\d{2}\.\d+)', cell)
            out['client_row'] = {'version_in_row': m.group(1) if m else None, 'repository_openapi_version': repo_v, 'files_checked': False}
            out['checks']['status_client_row_version'] = True
            if not m: miss('status_client_row_version', 'the client row names no API description version')
            elif m.group(1) != repo_v: miss('status_client_row_version', 'the client row says version %s; the repository copy is %s' % (m.group(1), repo_v))
            mcp = os.path.join(repo, 'exit_mcp.py'); tm = re.search(r'\((\d+) tools?, server v?(\d+\.\d+\.\d+)\)', cell)
            strict = re.findall(r'(?i)\bserver\b[\s:*`]*(?:version[\s:*`]*)?v?(\d+(?:\.\d+)+(?:-[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*)?)', cell)
            broad = re.findall(r'(?i)\bservers?\b\W{0,6}(?:version\W{0,3})?v?\d+\.\d', cell)   # every mention that looks like a server version
            named = sorted(set(strict)); out['client_row']['row_servers_named'] = named
            if len(broad) > len(strict):                # 10 Nov (L-524): a mention in a form this check does not read fails, never passes silently
                miss('status_client_row_version', 'the client row names a server in a form this check does not read')
            if named and not os.path.exists(mcp):       # a row that names a server is checked against exit_mcp.py, or fails
                miss('status_client_row_version', 'the client row names server %s, but exit_mcp.py is not in the checkout, so it was not checked' % ', '.join(named))
            elif os.path.exists(mcp) and named:
                src = open(mcp, encoding='utf-8').read(); sv = re.search(r'"serverInfo":\s*\{[^}]*"version":\s*"([^"]+)"', src)
                n = len(set(re.findall(r'\{\s*"name":\s*"(exit_[a-z0-9_]+)",\s*"description"', src)))   # every tool entry (TOOLS = [...] and TOOLS.extend([...])) starts name, description
                out['client_row'].update({'files_checked': True, 'mcp_server_version': sv.group(1) if sv else None, 'mcp_tools': n, 'row_tools': int(tm.group(1)) if tm else None, 'row_server': tm.group(2) if tm else None, 'row_servers_named': named})
                for v in named:
                    if not sv or v != sv.group(1): miss('status_client_row_version', 'the client row says server %s; exit_mcp.py says %s' % (v, sv.group(1) if sv else None))
                if not tm: miss('status_client_row_version', 'the client row names a server but not as "(N tools, server X.Y.Z)", so its tool count was not checked')
                elif n != int(tm.group(1)): miss('status_client_row_version', 'the client row says %s tools; exit_mcp.py lists %d' % (tm.group(1), n))
    except Exception as e:
        miss('status_client_row_version', 'unreadable: ' + type(e).__name__)
    # 6. log specification version
    try:
        spec = live.get(SITE + '/log/SPEC.txt', 'SPEC.txt')[0].decode('utf-8', 'replace')
        sv = re.search(r'specification, version (\d+\.\d+)', spec.split('\n', 1)[0]); st = re.findall(r'\(SPEC\.txt\) is version (\d+\.\d+)', md)
        out['spec'] = {'live': sv.group(1) if sv else None, 'status_md': st}; out['checks']['spec_version_matches'] = True
        if not sv: miss('spec_version_matches', 'the live SPEC.txt names no version in its first line')
        elif not st: miss('spec_version_matches', 'STATUS.md names no log specification version')
        elif any(v != sv.group(1) for v in st): miss('spec_version_matches', 'STATUS.md says %s; SPEC.txt is %s' % (', '.join(st), sv.group(1)))
    except Exception as e:
        miss('spec_version_matches', 'unreadable: ' + type(e).__name__)
    # 7. re-anchoring wording
    try:
        runs = json.loads(live.get(SITE + '/log/runs.json', 'runs.json')[0]).get('runs', [])
        beats = [r.get('at') for r in runs if str(r.get('outcome') or '').startswith('HEARTBEAT')]
        out['checks']['reanchor_wording'] = True; out['heartbeat_runs'] = len(beats)
        if beats:
            bad = re.compile(r're-anchor\w*[^.|]{0,200}?not (?:yet )?(?:been )?needed|NOT YET NEEDED[^.|\n]{0,160}re-anchor', re.I)
            texts = {'STATUS.md': md}
            if os.path.exists(os.path.join(repo, 'ROADMAP.md')): texts['ROADMAP.md'] = open(os.path.join(repo, 'ROADMAP.md'), encoding='utf-8').read()
            for name, t in texts.items():
                m = bad.search(t)
                if m: miss('reanchor_wording', '%s says re-anchoring is not needed yet, but %d heartbeat run(s) exist: "%s"' % (name, len(beats), m.group(0)[:120]))
    except Exception as e:
        miss('reanchor_wording', 'unreadable: ' + type(e).__name__)
    out['ok'] = all(out['checks'].values()) and not out['mismatches']
    print(json.dumps(out, indent=1, sort_keys=True)); return 0 if out['ok'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
