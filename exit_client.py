"""EXIT free research API — minimal client for agents and scripts (Python standard library only).

The access key comes from the EXIT_API_KEY environment variable (get it in a browser at https://api.exit-protocol.io); it is never
printed, logged or returned. Account actions (enrol, rotate, revoke) stay in the browser on purpose. Every research call sends a fresh
X-EXIT-Request-Id; nothing is retried automatically (each attempt counts against the account's daily limits).
"""
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime

MAX_RESPONSE = 2 * 1024 * 1024


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


DEFAULT_BASE = "https://api.exit-protocol.io"
SUBJECTS = ("usdc-mint-authorities", "pyusd-mint-authorities", "pump-fun-program-upgrade-authority")
_MINT = re.compile(r"[1-9A-HJ-NP-Za-km-z]{32,44}")
_RID = re.compile(r"[A-Za-z0-9._:-]{8,128}")
_EVM = re.compile(r"0x[0-9a-fA-F]{40}")
_KEY = re.compile(r"exit_free_[A-Za-z0-9_-]{43}")
_RECORD = re.compile(r"rr-[0-9a-f]{24}")
_WATCH = re.compile(r"watch-[0-9a-f]{24}")
_CODE = re.compile(r"[A-Z][A-Z0-9_]{0,127}")
_STATES = ("OPEN", "RESULT_READY", "REASON_RECORDED")


class ExitError(Exception):
    """A refusal or failure from the service (status 0 = refused locally before any request). research_record is the research
    record the service opened for this unresolved request ({id, state, gap}), or None."""

    def __init__(self, status, error, research_record=None):
        super().__init__(f"{status} {error}")
        self.status, self.error, self.research_record = status, error, research_record


def _record(h):
    """The research-record headers of a response, accepted only in their documented shape."""
    rid, state, gap = h.get("X-EXIT-Research-Record"), h.get("X-EXIT-Research-Record-State"), h.get("X-EXIT-Research-Gap")
    if not (isinstance(rid, str) and _RECORD.fullmatch(rid)):
        return None
    return {"id": rid, "state": state if state in _STATES else None, "gap": gap if isinstance(gap, str) and _CODE.fullmatch(gap) else None}


def _instant(name, value):
    try:
        dt = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        raise ExitError(0, f"{name} must be an ISO-8601 instant") from None
    if dt.tzinfo is None:
        raise ExitError(0, f"{name} needs an explicit timezone, e.g. 2026-08-01T00:00:00+00:00")
    return value


class Client:
    def __init__(self, key=None, base=None, timeout=30):
        self.base = (base or os.environ.get("EXIT_API_BASE") or DEFAULT_BASE).rstrip("/")
        u = urllib.parse.urlsplit(self.base)
        official = u.scheme == "https" and u.hostname == "api.exit-protocol.io" and u.port in (None, 443)
        local = u.scheme == "http" and u.hostname in ("127.0.0.1", "localhost", "::1")
        if not (official or local) or u.username or u.password or u.path or u.query or u.fragment:
            raise ValueError("EXIT_API_BASE must be the official HTTPS origin (loopback HTTP only for local testing)")
        if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or not 0 < timeout <= 60:
            raise ValueError("timeout must be greater than 0 and at most 60 seconds")
        self._opener = urllib.request.build_opener(_NoRedirect())
        self._key = key if key is not None else os.environ.get("EXIT_API_KEY", "")
        self.timeout = timeout

    def __repr__(self):
        return f"Client(base={self.base!r}, key={'set' if self._key else 'missing'})"

    def _call(self, method, path, query=None, auth=True, request_id=False):
        url = self.base + path + ("?" + urllib.parse.urlencode(query) if query else "")
        headers = {"User-Agent": "exit-agent-client/1", "Accept": "application/json"}
        if auth:
            if not _KEY.fullmatch(self._key or ""):
                raise ExitError(0, "EXIT_API_KEY is missing or not an EXIT access key")
            headers["Authorization"] = "Bearer " + self._key
        rid = str(uuid.uuid4()) if request_id else None
        if rid:
            headers["X-EXIT-Request-Id"] = rid
        req = urllib.request.Request(url, data=b"" if method == "POST" else None, headers=headers, method=method)
        try:
            with self._opener.open(req, timeout=self.timeout) as r:
                status, raw, h = r.status, r.read(MAX_RESPONSE + 1), r.headers
        except urllib.error.HTTPError as e:
            with e:
                status, raw, h = e.code, e.read(MAX_RESPONSE + 1), e.headers
        if 300 <= status < 400:
            raise ExitError(status, "REDIRECT_REFUSED")
        if len(raw) > MAX_RESPONSE:
            raise ExitError(status, "RESPONSE_TOO_LARGE")
        try:
            value = json.loads(raw)
        except ValueError:
            raise ExitError(status, "NON_JSON_RESPONSE") from None
        if status >= 400:
            code = value.get("error", "ERROR") if isinstance(value, dict) else "ERROR"
            if not isinstance(code, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]{0,127}", code):
                code = "SERVICE_ERROR"
            raise ExitError(status, code, _record(h))
        return {"meta": {"http_status": status, "research_state": h.get("X-EXIT-Research-State"),
                         "replayed": h.get("X-EXIT-Replayed") == "1", "request_id": rid, "research_record": _record(h),
                         "research_intake_full": h.get("X-EXIT-Research-Intake") == "FULL"}, "value": value}

    # --- service and account (read-only) ---
    def status(self):
        return self._call("GET", "/v0/early-access", auth=False)

    def usage(self):
        return self._call("GET", "/v0/early-access/usage")

    def freshness(self):
        return self._call("GET", "/v0/freshness")

    # --- research ---
    def mint_controls(self, mint):
        """Any Solana token mint: one finalized read of mint/freeze/supported Token-2022 authorities and their holder accounts."""
        if not isinstance(mint, str) or not _MINT.fullmatch(mint):
            raise ExitError(0, "a Solana mint address (base58, 32-44 characters) is required")
        return self._call("GET", "/v0/research/solana/mint", {"mint": mint}, request_id=True)

    def contract_controls(self, address):
        """Any Ethereum contract: proxy implementation/admin, the owner() getter as an observation and the named holders' account types
        at one finalized block (answered only where the service reports live_contract_research)."""
        if not isinstance(address, str) or not _EVM.fullmatch(address):
            raise ExitError(0, "an Ethereum contract address (0x + 40 hex characters) is required")
        if not self.status()["value"].get("live_contract_research", False):
            raise ExitError(0, "ETHEREUM_RESEARCH_NOT_ENABLED")
        return self._call("GET", "/v0/research/ethereum/contract", {"address": address}, request_id=True)

    # --- research records and pull-model watches (where the service reports research_records) ---
    def _records_enabled(self):
        if not self.status()["value"].get("research_records", False):
            raise ExitError(0, "RESEARCH_RECORDS_NOT_ENABLED")

    def research_records(self):
        """This key's research records (unanswered questions): id, state, gap, subject, times. Reading spends no research attempt."""
        self._records_enabled()
        return self._call("GET", "/v0/research/records")

    def research_record(self, record_id):
        """One record: state (OPEN, RESULT_READY, REASON_RECORDED), gap, recorded reason, follow-ups used, next possible check and,
        for 24 hours, a verified result. Another key's record answers exactly like an unknown id."""
        if not isinstance(record_id, str) or not _RECORD.fullmatch(record_id):
            raise ExitError(0, "a research record id (rr- + 24 hex characters) is required")
        self._records_enabled()
        return self._call("GET", "/v0/research/record", {"id": record_id})

    def check_research_record(self, record_id):
        """Explicitly re-check an OPEN record (provider failures only: at most three times, at least an hour apart). It counts as one
        research attempt; a record without a follow-up path is refused (409 RESEARCH_CHECK_NOT_AVAILABLE)."""
        if not isinstance(record_id, str) or not _RECORD.fullmatch(record_id):
            raise ExitError(0, "a research record id (rr- + 24 hex characters) is required")
        self._records_enabled()
        return self._call("POST", "/v0/research/record", {"id": record_id}, request_id=True)

    def watches(self):
        """This key's watched Solana mints with their recorded authority changes (no reading happens here)."""
        self._records_enabled()
        return self._call("GET", "/v0/research/watch")

    def add_watch(self, mint):
        """Watch a Solana token mint for authority changes (at most three per key; a watch ends after seven days). Adding reads nothing."""
        if not isinstance(mint, str) or not _MINT.fullmatch(mint):
            raise ExitError(0, "a Solana mint address (base58, 32-44 characters) is required")
        self._records_enabled()
        return self._call("POST", "/v0/research/watch", {"mint": mint})

    def check_watch(self, watch_id):
        """Explicitly re-read a watched mint now (at most every six hours, even after a failed attempt; counts as one research attempt).
        Changes are semantic authority/holder changes with evidence; an incomplete read records no change. Not continuous monitoring."""
        if not isinstance(watch_id, str) or not _WATCH.fullmatch(watch_id):
            raise ExitError(0, "a watch id (watch- + 24 hex characters) is required")
        self._records_enabled()
        return self._call("POST", "/v0/research/watch", {"id": watch_id}, request_id=True)

    def stop_watch(self, watch_id):
        """Stop a watch (its stored changes are deleted)."""
        if not isinstance(watch_id, str) or not _WATCH.fullmatch(watch_id):
            raise ExitError(0, "a watch id (watch- + 24 hex characters) is required")
        self._records_enabled()
        return self._call("DELETE", "/v0/research/watch", {"id": watch_id})

    # --- readers added 2026-10-29 … 2026-11-02 (v4 of the agent tools; all bearer, one X-EXIT-Request-Id each) ---
    def freeze_status(self, address):
        """One Ethereum address against the USDT, USDC and PYUSD issuer lists at one finalized block (schema exit.stablecoin-freeze-research/1)."""
        if not isinstance(address, str) or not _EVM.fullmatch(address):
            raise ExitError(0, "an Ethereum address (0x + 40 hex characters) is required")
        return self._call("GET", "/v0/research/ethereum/freeze", {"address": address}, request_id=True)

    def governance(self, governance):
        """One SPL Governance V2 account and its paired realm/config at one finalized slot (schema exit.solana-governance-research/1)."""
        if not isinstance(governance, str) or not _MINT.fullmatch(governance):
            raise ExitError(0, "a Solana governance account address (base58, 32-44 characters) is required")
        return self._call("GET", "/v0/research/solana/governance", {"governance": governance}, request_id=True)

    def governance_proposals(self, governance):
        """Proposals of one SPL Governance V2 account: counts by state, open ones decoded (schema exit.solana-governance-proposals-research/1)."""
        if not isinstance(governance, str) or not _MINT.fullmatch(governance):
            raise ExitError(0, "a Solana governance account address (base58, 32-44 characters) is required")
        return self._call("GET", "/v0/research/solana/governance/proposals", {"governance": governance}, request_id=True)

    def layerzero_path(self, oapp, eid, direction):
        """One LayerZero V2 OApp pathway on Ethereum: delegate, message libraries and verifier configuration for one remote endpoint id and
        direction (schema exit.layerzero-path-service/1)."""
        if not isinstance(oapp, str) or not _EVM.fullmatch(oapp):
            raise ExitError(0, "an OApp contract address (0x + 40 hex characters) is required")
        if not isinstance(eid, int) or isinstance(eid, bool) or not 0 < eid < 2 ** 32:
            raise ExitError(0, "a LayerZero endpoint id (positive integer) is required")
        if direction not in ("send", "receive"):
            raise ExitError(0, "direction must be 'send' or 'receive'")
        return self._call("GET", "/v0/research/ethereum/layerzero", {"oapp": oapp, "eid": eid, "direction": direction}, request_id=True)

    def layerzero_peer(self, oapp, eid):
        """Which peer one LayerZero V2 OApp holds for one remote endpoint id (schema exit.layerzero-peer-research/1)."""
        if not isinstance(oapp, str) or not _EVM.fullmatch(oapp):
            raise ExitError(0, "an OApp contract address (0x + 40 hex characters) is required")
        if not isinstance(eid, int) or isinstance(eid, bool) or not 0 < eid < 2 ** 32:
            raise ExitError(0, "a LayerZero endpoint id (positive integer) is required")
        return self._call("GET", "/v0/research/ethereum/layerzero/peer", {"oapp": oapp, "eid": eid}, request_id=True)

    # --- this key's own answers: graph, comparison, evidence view, log binding (no research attempt is spent) ---
    def research_graph(self, request_ids):
        """Join one to four of this key's own answers into one typed graph (schema exit.research-graph/1)."""
        ids = list(request_ids) if isinstance(request_ids, (list, tuple)) else None
        if not ids or not 1 <= len(ids) <= 4 or not all(isinstance(r, str) and _RID.fullmatch(r) for r in ids):
            raise ExitError(0, "one to four of this key's own request ids are required")
        return self._call("GET", "/v0/research/graph", [("request_id", r) for r in ids])

    def compare_answers(self, a, b):
        """Compare two of this key's own answers of the same kind (schema exit.research-comparison/1)."""
        if not all(isinstance(x, str) and _RID.fullmatch(x) for x in (a, b)) or a == b:
            raise ExitError(0, "two different request ids of this key's own answers are required")
        return self._call("GET", "/v0/research/compare", {"a": a, "b": b})

    def evidence_view(self, request_id):
        """Answer-to-source view of one of this key's own answers (schema exit.private-evidence-view/2)."""
        if not isinstance(request_id, str) or not _RID.fullmatch(request_id):
            raise ExitError(0, "a request id of this key's own answer is required")
        return self._call("GET", "/v0/research/evidence", {"request_id": request_id})

    def log_binding(self, request_id):
        """The evidence-log binding (leaf hash, index, proof availability) of one of this key's own answered requests (schema exit.log-binding/1)."""
        if not isinstance(request_id, str) or not _RID.fullmatch(request_id):
            raise ExitError(0, "a request id of this key's own answer is required")
        return self._call("GET", "/v0/research/log-binding", {"request_id": request_id})

    # --- Ethereum contract watches and owned webhook receivers ---
    def add_contract_watch(self, contract):
        """Watch an Ethereum mainnet contract for administrative-surface changes (shares the watch limits; pull checks remain the general scope)."""
        if not isinstance(contract, str) or not _EVM.fullmatch(contract):
            raise ExitError(0, "an Ethereum contract address (0x + 40 hex characters) is required")
        return self._call("POST", "/v0/research/watch", {"contract": contract}, request_id=True)

    def webhooks(self, delivery=None):
        """Own receiver, event and delivery metadata, or one own delivery payload part when a delivery id is given."""
        if delivery is not None and (not isinstance(delivery, str) or not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", delivery)):
            raise ExitError(0, "a delivery id is required when given")
        return self._call("GET", "/v0/research/webhook", {"delivery": delivery} if delivery else None)

    def delete_webhook(self, receiver_id):
        """Delete an owned receiver configuration and its queued deliveries."""
        if not isinstance(receiver_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", receiver_id):
            raise ExitError(0, "a receiver id is required")
        return self._call("DELETE", "/v0/research/webhook", {"id": receiver_id})

    def control_state(self, subject_id, valid_at, known_at, as_of=False):
        """Recorded subjects only (SUBJECTS): who controlled it at valid_at, using only evidence known by known_at."""
        if subject_id not in SUBJECTS:
            raise ExitError(0, "subject_id must be one of " + ", ".join(SUBJECTS))
        q = {"subject_id": subject_id, "valid_at": _instant("valid_at", valid_at), "known_at": _instant("known_at", known_at)}
        return self._call("GET", "/v0/control_as_of" if as_of else "/v0/control_state", q, request_id=True)

    def control_change(self, subject_id, valid_at_from, valid_at_to, known_at):
        if subject_id not in SUBJECTS:
            raise ExitError(0, "subject_id must be one of " + ", ".join(SUBJECTS))
        q = {"subject_id": subject_id, "valid_at_from": _instant("valid_at_from", valid_at_from),
             "valid_at_to": _instant("valid_at_to", valid_at_to), "known_at": _instant("known_at", known_at)}
        return self._call("GET", "/v0/control_change", q, request_id=True)
