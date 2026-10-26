"""Public client regressions. Synthetic loopback traffic only; no campaign or real key."""
import http.server,json,threading,unittest
from unittest.mock import patch
import exit_client as c
import exit_mcp as m
KEY='exit_free_'+'x'*43
class ClientSafety(unittest.TestCase):
 def server(self,handler):
  server=http.server.HTTPServer(('127.0.0.1',0),handler);threading.Thread(target=server.serve_forever,daemon=True).start()
  self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
  return server,'http://127.0.0.1:'+str(server.server_port)
 def test_cross_origin_redirect_never_sends_bearer_to_destination(self):
  seen=[]
  class Sink(http.server.BaseHTTPRequestHandler):
   def log_message(self,*a):pass
   def do_GET(self):seen.append(self.headers.get('Authorization'));self.send_response(200);self.end_headers();self.wfile.write(b'{}')
  _,destination=self.server(Sink)
  class Origin(http.server.BaseHTTPRequestHandler):
   def log_message(self,*a):pass
   def do_GET(self):self.send_response(302);self.send_header('Location',destination);self.end_headers()
  _,origin=self.server(Origin)
  with self.assertRaises(c.ExitError) as e:c.Client(key=KEY,base=origin).usage()
  self.assertEqual((e.exception.status,e.exception.error),(302,'REDIRECT_REFUSED'));self.assertEqual(seen,[])
 def test_remote_origin_or_embedded_url_data_is_refused_before_network(self):
  for base in ['https://other.example','https://api.exit-protocol.io.evil.example','https://user:secret@api.exit-protocol.io','https://api.exit-protocol.io/path','https://api.exit-protocol.io?key=x','https://api.exit-protocol.io#x','https://api.exit-protocol.io:444']:
   with self.subTest(base=base),self.assertRaises(ValueError):c.Client(key=KEY,base=base)
 def test_response_size_is_bounded(self):
  class Origin(http.server.BaseHTTPRequestHandler):
   def log_message(self,*a):pass
   def do_GET(self):self.send_response(200);self.end_headers();self.wfile.write(b' '*1025)
  _,origin=self.server(Origin)
  with patch.object(c,'MAX_RESPONSE',1024),self.assertRaises(c.ExitError) as e:c.Client(key=KEY,base=origin).usage()
  self.assertEqual(e.exception.error,'RESPONSE_TOO_LARGE')
 def test_server_echo_cannot_leak_key_in_exception(self):
  class Origin(http.server.BaseHTTPRequestHandler):
   def log_message(self,*a):pass
   def do_GET(self):self.send_response(400);self.end_headers();self.wfile.write(json.dumps({'error':self.headers['Authorization']}).encode())
  _,origin=self.server(Origin)
  with self.assertRaises(c.ExitError) as e:c.Client(key=KEY,base=origin).usage()
  self.assertEqual(e.exception.error,'SERVICE_ERROR');self.assertNotIn(KEY,str(e.exception))
 def test_disabled_ethereum_is_refused_without_authenticated_route(self):
  client=c.Client(key=KEY)
  with patch.object(client,'status',return_value={'value':{'live_mint_research':True}}),patch.object(client,'_call') as call,self.assertRaises(c.ExitError) as e:client.contract_controls('0x'+'1'*40)
  self.assertEqual(e.exception.error,'ETHEREUM_RESEARCH_NOT_ENABLED');call.assert_not_called()
 def test_ethereum_enabled_capability_routes_exactly_once(self):
  client=c.Client(key=KEY)
  with patch.object(client,'status',return_value={'value':{'live_contract_research':True}}),patch.object(client,'_call',return_value={}) as call:client.contract_controls('0x'+'1'*40)
  self.assertEqual(call.call_count,1);self.assertEqual(call.call_args.args[:2],('GET','/v0/research/ethereum/contract'))
 def test_invalid_mcp_shapes_are_refused_without_network(self):
  client=c.Client(key=KEY)
  for value in [[],None,42,{'jsonrpc':'1.0','id':1},{'jsonrpc':'2.0','id':1,'method':'tools/call','params':[]}]:
   out=m.handle(client,value);self.assertIn('error',out)
  with patch.object(client,'mint_controls') as call:
   for args in [{'mint':'x','extra':'x'},{'mint':42},['x']]:
    out=m.handle(client,{'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'exit_mint_controls','arguments':args}});self.assertIn('error',out)
   call.assert_not_called()
 def test_no_retries_on_server_error(self):
  seen=[]
  class Origin(http.server.BaseHTTPRequestHandler):
   def log_message(self,*a):pass
   def do_GET(self):seen.append(1);self.send_response(503);self.end_headers();self.wfile.write(b'{"error":"UNAVAILABLE"}')
  _,origin=self.server(Origin)
  with self.assertRaises(c.ExitError):c.Client(key=KEY,base=origin).usage()
  self.assertEqual(len(seen),1)
 def test_finite_timeout_and_secret_free_repr(self):
  for timeout in [0,-1,61,True]:
   with self.assertRaises(ValueError):c.Client(key=KEY,timeout=timeout)
  self.assertNotIn(KEY,repr(c.Client(key=KEY)))
if __name__=='__main__':unittest.main()
