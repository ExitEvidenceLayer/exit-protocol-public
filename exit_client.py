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
_EVM = re.compile(r"0x[0-9a-fA-F]{40}")
_KEY = re.compile(r"exit_free_[A-Za-z0-9_-]{43}")


class ExitError(Exception):
    """A refusal or failure from the service (status 0 = refused locally before any request)."""

    def __init__(self, status, error):
        super().__init__(f"{status} {error}")
        self.status, self.error = status, error


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
        req = urllib.request.Request(url, headers=headers, method=method)
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
            raise ExitError(status, code)
        return {"meta": {"http_status": status, "research_state": h.get("X-EXIT-Research-State"),
                         "replayed": h.get("X-EXIT-Replayed") == "1", "request_id": rid}, "value": value}

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
