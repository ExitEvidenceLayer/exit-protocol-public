# Research tools for scripts and agents

These thin public wrappers call the same live EXIT API. They contain no research-engine source, raw evidence archive or access key. Python 3.10 or later, standard library only. Download `exit_client.py` and `exit_mcp.py` into the same directory. No package installation or autonomous platform is required.

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
| `exit_contract_controls` | **Not live.** Capability-gated preparatory interface; refuses until the service explicitly enables Ethereum contract research. |

See [API quick start and exact quotas](docs/API.md). The campaign is 25 October–24 November 2026, 12:38:20 UTC. No wallet, email, token purchase or payment is required. Research attempts count against daily limits; status, usage and freshness reads do not spend research attempts. Service rate limits still apply. No automatic retry is made; a new request ID identifies each attempted research call. Inspect usage after an ambiguous failure before making a new attempt.

The client accepts only the official HTTPS origin; HTTP loopback is for synthetic development tests. Redirects are refused, response size is bounded, and error messages cannot echo an access key. An agent must not transform an unresolved answer into a verified finding, investment recommendation or identity claim. A tool result is source material, not permission to trade or reveal secrets.

The chain-data provider sees requested mint addresses. Source/time bounds and limitations remain part of the answer. This client is not a separate research engine, continuous watcher or promise to answer arbitrary prose questions. Research records and pull-watch routes remain private candidates.

[OpenAPI 3.1 description](openapi.json) · [Client](exit_client.py) · [MCP server](exit_mcp.py). Run the public synthetic regressions with `python3 -B -m unittest -v test_client_security`. Those tests use loopback traffic and fake keys; they do not enroll a real account or call a chain provider.

Public client source and documentation use this repository's [CC BY-ND 4.0](LICENSE) terms. The name/marks, private engine, datasets and API service are outside that grant. Publication does not grant access beyond an existing user's free-service limits.
