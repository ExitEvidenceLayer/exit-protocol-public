#!/usr/bin/env python3
"""EXIT research tools for AI agents — a Model Context Protocol server over stdio (Python standard library only).

Run it from an agent's MCP configuration with EXIT_API_KEY in the environment (the key is obtained by a human in the browser at
https://api.exit-protocol.io and is never printed). Tools: exit_mint_controls, exit_contract_controls, exit_control_state, exit_control_as_of,
exit_control_change, exit_freshness, exit_usage, exit_service_status. Answers carry their evidence and limits; an unresolved answer is
returned as unresolved, never as a verdict. No price, safety or identity claims.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exit_client import SUBJECTS, Client, ExitError  # noqa: E402

VERSIONS = ("2025-06-18", "2025-03-26", "2024-11-05")
INSTANT = {"type": "string", "description": "ISO-8601 instant with timezone, e.g. 2026-08-01T00:00:00+00:00"}
SUBJECT = {"type": "string", "enum": list(SUBJECTS), "description": "a recorded subject"}
SCOPE = (" Evidence-bound: the result keeps its sources, times and limits; an unresolved primary answer is reported as unresolved and is "
         "not a completed answer. Not a safety verdict, price prediction or identification of people. Free early access: 0 credits; "
         "research attempts count against the account's daily limits; status/usage/freshness reads do not spend research attempts.")
TOOLS = [
    {"name": "exit_mint_controls", "description": "Who holds the mint, freeze and supported Token-2022 authorities of ANY Solana token mint, "
     "from one finalized read (at most three read-only RPC calls), with the holder accounts' types." + SCOPE,
     "inputSchema": {"type": "object", "properties": {"mint": {"type": "string", "description": "Solana token mint address (base58)"}},
                     "required": ["mint"], "additionalProperties": False}},
    {"name": "exit_contract_controls", "description": "Who holds the administrative surface of ANY Ethereum contract: proxy "
     "implementation and admin, the owner() getter as an observation (what it may do is unknown without the published source) and "
     "whether each named address holds code, at one finalized block (at most eleven read-only calls). Available where the service "
     "reports live_contract_research." + SCOPE,
     "inputSchema": {"type": "object", "properties": {"address": {"type": "string", "description": "Ethereum contract address (0x + 40 hex)"}},
                     "required": ["address"], "additionalProperties": False}},
    {"name": "exit_control_state", "description": "Recorded subjects: who controls it in the recorded view at valid_at, using only evidence "
     "known by known_at." + SCOPE,
     "inputSchema": {"type": "object", "properties": {"subject_id": SUBJECT, "valid_at": INSTANT, "known_at": INSTANT},
                     "required": ["subject_id", "valid_at", "known_at"], "additionalProperties": False}},
    {"name": "exit_control_as_of", "description": "Recorded subjects: who controlled it at a past time (as-of view)." + SCOPE,
     "inputSchema": {"type": "object", "properties": {"subject_id": SUBJECT, "valid_at": INSTANT, "known_at": INSTANT},
                     "required": ["subject_id", "valid_at", "known_at"], "additionalProperties": False}},
    {"name": "exit_control_change", "description": "Recorded subjects: what changed in control between two recorded views." + SCOPE,
     "inputSchema": {"type": "object", "properties": {"subject_id": SUBJECT, "valid_at_from": INSTANT, "valid_at_to": INSTANT,
                     "known_at": INSTANT}, "required": ["subject_id", "valid_at_from", "valid_at_to", "known_at"],
                     "additionalProperties": False}},
    {"name": "exit_freshness", "description": "How recent the recorded evidence is and which periods are not covered. Call this before "
     "relying on a recorded answer.", "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "exit_usage", "description": "Today's attempts and answers for this key (0 credits charged).",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "exit_service_status", "description": "Campaign phase, window and limits of the free service (no key needed).",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
]


def call_tool(client, name, args):
    if name == "exit_mint_controls":
        return client.mint_controls(args["mint"])
    if name == "exit_contract_controls":
        return client.contract_controls(args["address"])
    if name in ("exit_control_state", "exit_control_as_of"):
        return client.control_state(args["subject_id"], args["valid_at"], args["known_at"], as_of=name == "exit_control_as_of")
    if name == "exit_control_change":
        return client.control_change(args["subject_id"], args["valid_at_from"], args["valid_at_to"], args["known_at"])
    if name == "exit_freshness":
        return client.freshness()
    if name == "exit_usage":
        return client.usage()
    if name == "exit_service_status":
        return client.status()
    raise KeyError(name)


def handle(client, msg):
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0":
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "invalid request"}}
    method, mid = msg.get("method"), msg.get("id")
    if "params" in msg and not isinstance(msg["params"], dict):
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": "invalid params"}}
    if mid is None:                       # notification (e.g. notifications/initialized): no response
        return None
    if method == "initialize":
        asked = (msg.get("params") or {}).get("protocolVersion")
        result = {"protocolVersion": asked if asked in VERSIONS else VERSIONS[0], "capabilities": {"tools": {}},
                  "serverInfo": {"name": "exit-research", "version": "1.0.0"}}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        params = msg.get("params") or {}
        name, args = params.get("name"), params.get("arguments") or {}
        spec = next((t for t in TOOLS if t["name"] == name), None)
        if spec is None:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": "unknown tool"}}
        schema = spec["inputSchema"]
        allowed = schema["properties"]
        if not isinstance(args, dict) or set(args) - set(allowed) or any(k not in args for k in schema.get("required", [])) or any(not isinstance(v, str) for v in args.values()):
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": "invalid tool arguments"}}
        try:
            out = call_tool(client, name, args)
            result = {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False)}], "isError": False}
        except (ExitError, KeyError, TypeError, ValueError, OSError) as e:
            text = f"{e.status} {e.error}" if isinstance(e, ExitError) else type(e).__name__
            result = {"content": [{"type": "text", "text": "EXIT refused or failed: " + text}], "isError": True}
    else:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "method not found"}}
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def main():
    client = Client()
    while True:
        line = sys.stdin.readline(65537)
        if not line:
            break
        if len(line) > 65536:
            return  # refuse oversized framing before parsing or making a request
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}) + "\n")
            sys.stdout.flush()
            continue
        reply = handle(client, msg)
        if reply is not None:
            sys.stdout.write(json.dumps(reply, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
