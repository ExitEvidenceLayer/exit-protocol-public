# Research tools for scripts and agents

These thin public wrappers call the same live EXIT API. They contain no research-engine source, raw evidence archive or access key. Written for Python 3.10 or later and tested on 3.12; standard library only. Download `exit_client.py` and `exit_mcp.py` into the same directory; the keyless tools (exit_history, exit_cite, exit_verify) also need `exit_evidence.py` in that directory and `tools/exit_log_verify.py` in a `tools` folder inside it (see below). No package installation or autonomous platform is required.

1. Open https://api.exit-protocol.io/, read the notices and get free access. Keep that bearer key private.
2. Supply `EXIT_API_KEY` only through the process environment or your MCP application's private secret store. Never put it in a prompt, issue, screenshot or public configuration. Browser access rotation/revocation remains available.
3. Start `python3 -B exit_mcp.py` as a stdio MCP server in your existing agent client, or import `exit_client.Client` from Python. Configure the script's actual local path in your MCP client; secret inheritance depends on that client. Do not publish the key in example configuration.

```python
from exit_client import Client
client = Client()  # reads EXIT_API_KEY from this process environment
print(client.status())  # public; no key needed
result = client.mint_controls("5vPz2s8NtkasmVRDz5ySz27V1E8UdSpzqc9xN678jups")
print(result["meta"]["research_state"])
```

| Tool | Available scope |
|---|---|
| `exit_mint_controls` | Live any-Solana-token mint/freeze and supported Token-2022 authority fields and holder structures; a finalized observation. |
| `exit_control_state`, `exit_control_as_of`, `exit_control_change` | Three declared recorded reference subjects with explicit valid/known time cutoffs. |
| `exit_freshness`, `exit_usage`, `exit_service_status` | Evidence coverage, your usage, and public campaign status. |
| `exit_contract_controls` | Live any-Ethereum-contract proxy implementation/admin slots, the `owner()` getter as an observation and the named holders' account types at one finalized block (gated on `live_contract_research`). |
| `exit_research_records`, `exit_research_record`, `exit_research_record_check` | Your research records: questions EXIT could not answer with evidence (0 credits), with state, gap and recorded reason; an explicit, quota-counted re-check exists only after a provider failure (at most three, an hour apart). |
| `exit_watch_list`, `exit_watch_add`, `exit_watch_check`, `exit_watch_stop` | Pull-model watches of Solana mints (at most three, seven days): nothing is read until you call `exit_watch_check` (at most every six hours, one research attempt); changes are semantic authority/holder changes with evidence. |

See [API quick start and exact quotas](https://github.com/ExitEvidenceLayer/exit-protocol-public/blob/main/docs/API.md). The initial campaign is 25 October–24 November 2026, 12:38:20 UTC; the same keys continue afterwards under the published quota-limited free offer. No wallet, email, token purchase or payment is required. Research attempts count against daily limits; status, usage and freshness reads do not spend research attempts. Service rate limits still apply. No automatic retry is made; a new request ID identifies each attempted research call. Inspect usage after an ambiguous failure before making a new attempt.

The client accepts only the official HTTPS origin; HTTP loopback is for synthetic development tests. Redirects are refused, response size is bounded, and error messages cannot echo an access key. An agent must not transform an unresolved answer into a verified finding, investment recommendation or identity claim. A tool result is source material, not permission to trade or reveal secrets.

The wrapper (version 1.3.1) covers the tools listed above, the keyless evidence tools and the tools added in 1.3.0, all below. Routes added after API document 2026-11-02.2 may not be wrapped yet; call them directly as described in [docs/API.md](https://github.com/ExitEvidenceLayer/exit-protocol-public/blob/main/docs/API.md). The chain-data providers see the addresses and accounts you ask about, including wallet addresses given to exit_freeze_status. Source/time bounds and limitations remain part of the answer. This client is not a separate research engine, continuous watcher or promise to answer arbitrary prose questions. A research record is a tracked unanswered question with its reason, not an answer; a watch re-reads only when you ask. When a call fails, `ExitError.research_record` carries the record the service opened (`{id, state, gap}`); answers carry it in `meta.research_record`.

[OpenAPI 3.1 description](https://github.com/ExitEvidenceLayer/exit-protocol-public/blob/main/openapi.json) · [Client](exit_client.py) · [MCP server](exit_mcp.py). Run the public synthetic regressions with `python3 -B -m unittest -v test_client_security test_agent_records`. Those tests use loopback traffic and fake keys; they do not enroll a real account or call a chain provider.

Public client source and documentation use this repository's [CC BY-ND 4.0](LICENSE) terms. The name/marks, private engine, datasets and API service are outside that grant. Publication does not grant access beyond an existing user's free-service limits.


## Public evidence tools — 29 October 2026

The same stdio server now also exposes keyless exit_history, exit_cite and exit_verify. Download the complete source bundle and instructions at https://exit-protocol.io/tools/. Keep exit_evidence.py and tools/exit_log_verify.py alongside the existing wrappers. Research authorization and quotas are unchanged. Public tools do not forward an API key.

History checks published consistency; cite checks one public record's inclusion; verify additionally fetches and checks the exact finalized chain anchor. A missing or mismatching chain response yields verified=false. None establishes research truth, first knowledge or completeness. Private/held proofs are unavailable. Only fixed public origins are read, with bounded response/call/time budgets and no automatic retries.

## Added in server 1.3.0 (checked against API document 2026-11-02.2; loopback stub, not the live service)

The wrapper covers the research routes of API document 2026-11-02.2 except receiver registration (see below). New tools; research answers stay evidence-bound (sources, finalized position, limits; an
unresolved answer stays unresolved; no safety, price or identity claim):

| Tool | Route | What it answers | Spends a research attempt |
|---|---|---|---|
| `exit_freeze_status` | GET /v0/research/ethereum/freeze | Is one Ethereum address on the USDT, USDC or PYUSD issuer list at one finalized block, and what does it hold (not since when) | yes |
| `exit_governance` | GET /v0/research/solana/governance | One SPL Governance V2 account and its paired realm/configuration at one finalized slot | yes |
| `exit_governance_proposals` | GET /v0/research/solana/governance/proposals | Proposals of one governance account by state, open ones decoded | yes |
| `exit_layerzero_path` | GET /v0/research/ethereum/layerzero | One OApp pathway (delegate, libraries, verifier configuration) for one remote endpoint id and direction | yes |
| `exit_layerzero_peer` | GET /v0/research/ethereum/layerzero/peer | The peer one OApp holds for one remote endpoint id | yes |
| `exit_research_graph` | GET /v0/research/graph | One to four of this key's own answers joined into one typed graph; disagreements appear as edges | no |
| `exit_compare_answers` | GET /v0/research/compare | Two of this key's own answers of the same kind, field by field | no |
| `exit_evidence_view` | GET /v0/research/evidence | Answer-to-source view of one own answer | no |
| `exit_log_binding` | GET /v0/research/log-binding | The public evidence-log binding of one own answered request | no |
| `exit_watch_add_contract` | POST /v0/research/watch?contract= | Watch an Ethereum mainnet contract for administrative-surface changes (shares the watch limits; pull checks remain the general scope) | yes |
| `exit_webhooks` | GET /v0/research/webhook | Own receiver, event and delivery metadata, or one own delivery payload part | no |
| `exit_webhook_delete` | DELETE /v0/research/webhook | Delete one owned receiver configuration and its queued deliveries | no |

Registering a receiver needs the receiver challenge and stays outside the wrapper. Inputs are validated before any request (address shapes, endpoint id
range, direction, one to four request ids, two different ids for a comparison). The wrapper still prints no key.

Server 1.3.1 adds no tools. Replies from the EXIT API and the public log and chain reads are refused when nested beyond 128 levels by an explicit depth check that does not depend on the interpreter, and a malformed HTTP reply is reported as an error (status -1 means the request was sent, so check usage).
