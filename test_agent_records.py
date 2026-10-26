"""ODA 1 agent interface v3 (2026-10-26): research-record and watch tools. Synthetic loopback traffic only; no campaign or real key."""
import http.server
import json
import threading
import unittest
from urllib.parse import parse_qs, urlsplit

import exit_client as c
import exit_mcp as m

KEY = "exit_free_" + "x" * 43
RID = "rr-" + "a" * 24
WID = "watch-" + "b" * 24
MINT = "5vPz2s8NtkasmVRDz5ySz27V1E8UdSpzqc9xN678jups"


class Recorder(http.server.BaseHTTPRequestHandler):
    """A stand-in API: records every request; answers per path; research_records flag configurable."""
    seen, flag, mode = [], True, "ok"

    def log_message(self, *a):
        pass

    def reply(self, code, value, headers=()):
        raw = json.dumps(value).encode()
        self.send_response(code)
        for k, v in headers:
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def handle_any(self, method):
        u = urlsplit(self.path)
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        Recorder.seen.append({"method": method, "path": u.path, "query": parse_qs(u.query), "auth": self.headers.get("Authorization"),
                              "rid": self.headers.get("X-EXIT-Request-Id"), "length": self.headers.get("Content-Length"), "body": body})
        if u.path == "/v0/early-access":
            return self.reply(200, {"phase": "OPEN", "research_records": Recorder.flag})
        if Recorder.mode == "failure":
            return self.reply(503, {"error": "RPC_UNAVAILABLE_NO_AUTOMATIC_RETRY"}, [("X-EXIT-Research-Record", RID),
                              ("X-EXIT-Research-Record-State", "OPEN"), ("X-EXIT-Research-Gap", "PROVIDER_UNAVAILABLE")])
        if Recorder.mode == "forged":
            return self.reply(200, {"ok": True}, [("X-EXIT-Research-Record", "rr-<script>"), ("X-EXIT-Research-Intake", "FULL")])
        return self.reply(200, {"ok": True}, [("X-EXIT-Research-Record", RID), ("X-EXIT-Research-Record-State", "REASON_RECORDED"),
                                              ("X-EXIT-Research-Gap", "HISTORY_RANGE")])

    def do_GET(self):
        self.handle_any("GET")

    def do_POST(self):
        self.handle_any("POST")

    def do_DELETE(self):
        self.handle_any("DELETE")


class AgentRecords(unittest.TestCase):
    def setUp(self):
        Recorder.seen, Recorder.flag, Recorder.mode = [], True, "ok"
        self.server = http.server.HTTPServer(("127.0.0.1", 0), Recorder)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.client = c.Client(key=KEY, base="http://127.0.0.1:" + str(self.server.server_port))

    def calls(self):
        return [(x["method"], x["path"]) for x in Recorder.seen if x["path"] != "/v0/early-access"]

    def test_every_tool_is_gated_on_the_service_flag_without_touching_its_route(self):
        Recorder.flag = False
        for call in (lambda: self.client.research_records(), lambda: self.client.research_record(RID),
                     lambda: self.client.check_research_record(RID), lambda: self.client.watches(), lambda: self.client.add_watch(MINT),
                     lambda: self.client.check_watch(WID), lambda: self.client.stop_watch(WID)):
            with self.subTest(call=call), self.assertRaises(c.ExitError) as e:
                call()
            self.assertEqual((e.exception.status, e.exception.error), (0, "RESEARCH_RECORDS_NOT_ENABLED"))
        self.assertEqual(self.calls(), [])

    def test_malformed_ids_and_mints_are_refused_before_any_request(self):
        for call in (lambda: self.client.research_record("rr-1"), lambda: self.client.check_research_record(WID),
                     lambda: self.client.check_watch(RID), lambda: self.client.stop_watch("watch-../x"), lambda: self.client.add_watch("https://x")):
            with self.subTest(call=call), self.assertRaises(c.ExitError) as e:
                call()
            self.assertEqual(e.exception.status, 0)
        self.assertEqual(Recorder.seen, [])

    def test_routes_methods_request_ids_and_empty_post_bodies(self):
        self.client.research_records(); self.client.research_record(RID); self.client.check_research_record(RID)
        self.client.watches(); self.client.add_watch(MINT); self.client.check_watch(WID); self.client.stop_watch(WID)
        self.assertEqual(self.calls(), [("GET", "/v0/research/records"), ("GET", "/v0/research/record"), ("POST", "/v0/research/record"),
                                        ("GET", "/v0/research/watch"), ("POST", "/v0/research/watch"), ("POST", "/v0/research/watch"),
                                        ("DELETE", "/v0/research/watch")])
        routed = [x for x in Recorder.seen if x["path"] != "/v0/early-access"]
        self.assertTrue(all(x["auth"] == "Bearer " + KEY for x in routed))
        checks = [x for x in routed if x["method"] == "POST" and "id" in x["query"]]
        self.assertTrue(checks and all(x["rid"] and x["length"] == "0" and x["body"] == b"" for x in checks))
        self.assertTrue(all(x["rid"] is None for x in routed if not (x["method"] == "POST" and "id" in x["query"])))
        self.assertEqual(routed[4]["query"], {"mint": [MINT]})

    def test_record_headers_reach_the_agent_on_answers_and_on_refusals(self):
        out = self.client.research_records()
        self.assertEqual(out["meta"]["research_record"], {"id": RID, "state": "REASON_RECORDED", "gap": "HISTORY_RANGE"})
        Recorder.mode = "failure"
        with self.assertRaises(c.ExitError) as e:
            self.client.check_watch(WID)
        self.assertEqual((e.exception.status, e.exception.research_record), (503, {"id": RID, "state": "OPEN", "gap": "PROVIDER_UNAVAILABLE"}))

    def test_forged_record_headers_are_not_passed_through(self):
        Recorder.mode = "forged"
        out = self.client.watches()
        self.assertIsNone(out["meta"]["research_record"])
        self.assertTrue(out["meta"]["research_intake_full"])

    def test_mcp_lists_and_routes_the_seven_tools_and_reports_the_record_on_refusal(self):
        names = [t["name"] for t in m.handle(self.client, {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})["result"]["tools"]]
        for n in ("exit_research_records", "exit_research_record", "exit_research_record_check", "exit_watch_list", "exit_watch_add",
                  "exit_watch_check", "exit_watch_stop"):
            self.assertIn(n, names)
        out = m.handle(self.client, {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "exit_watch_add", "arguments": {"mint": MINT}}})
        self.assertFalse(out["result"]["isError"])
        Recorder.mode = "failure"
        out = m.handle(self.client, {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                                     "params": {"name": "exit_research_record_check", "arguments": {"record_id": RID}}})
        self.assertTrue(out["result"]["isError"])
        self.assertIn(RID, out["result"]["content"][0]["text"])
        self.assertNotIn(KEY, json.dumps(out))
        bad = m.handle(self.client, {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "exit_watch_stop", "arguments": {}}})
        self.assertIn("error", bad)

    def test_mcp_each_new_tool_reaches_its_route(self):
        plan = [("exit_research_records", {}, ("GET", "/v0/research/records")), ("exit_research_record", {"record_id": RID}, ("GET", "/v0/research/record")),
                ("exit_research_record_check", {"record_id": RID}, ("POST", "/v0/research/record")), ("exit_watch_list", {}, ("GET", "/v0/research/watch")),
                ("exit_watch_add", {"mint": MINT}, ("POST", "/v0/research/watch")), ("exit_watch_check", {"watch_id": WID}, ("POST", "/v0/research/watch")),
                ("exit_watch_stop", {"watch_id": WID}, ("DELETE", "/v0/research/watch"))]
        for i, (name, args, route) in enumerate(plan):
            with self.subTest(tool=name):
                Recorder.seen = []
                out = m.handle(self.client, {"jsonrpc": "2.0", "id": 10 + i, "method": "tools/call", "params": {"name": name, "arguments": args}})
                self.assertFalse(out["result"]["isError"], out)
                self.assertEqual(self.calls(), [route])


if __name__ == "__main__":
    unittest.main()
