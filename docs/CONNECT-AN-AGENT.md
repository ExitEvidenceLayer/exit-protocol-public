# Connect an AI agent to EXIT

`exit_mcp.py` gives AI agents EXIT's research tools as a Model Context Protocol (MCP) server over stdio, using only the Python standard library. Run it from your agent's MCP configuration with `EXIT_API_KEY` in its environment (a person gets the key in a browser at https://api.exit-protocol.io, and it is never printed); the public log tools `exit_history`, `exit_cite` and `exit_verify` need no key. Answers carry their evidence and limits, an unresolved answer is returned as unresolved and never as a verdict, and there are no price, safety or identity claims.

Checked on 11 November 2026: the download and file check, the terminal test and the exchange in section 6 were run with tools release `2026-11-08.1` on Python 3.12.14. The Claude Desktop and Cursor settings follow the official guides as read the same day ([MCP: connect to local servers](https://modelcontextprotocol.io/docs/develop/connect-local-servers), [Claude Help Center: local MCP servers](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop), [Cursor: MCP](https://cursor.com/docs/mcp), [Cursor help: MCP](https://cursor.com/help/customization/mcp)). They were not run inside the two apps for this page.

## 1. Download and check the files

The tools are published at https://exit-protocol.io/tools/. On 11 November 2026 the release was `2026-11-08.1`, in the archive `exit-agent-tools-20261108.zip`; [RELEASE.json](https://exit-protocol.io/tools/RELEASE.json) lists the archive's SHA-256. The tools are written for Python 3.10 or later, tested on 3.12, and need no package installation.

On macOS or Linux:

```sh
mkdir exit-agent-tools && cd exit-agent-tools
curl -O https://exit-protocol.io/tools/exit-agent-tools-20261108.zip
shasum -a 256 exit-agent-tools-20261108.zip
unzip exit-agent-tools-20261108.zip
shasum -a 256 -c SHA256SUMS
```

The archive's hash must equal its entry in RELEASE.json, and the last command must print `OK` for each of the 11 files. On Linux without `shasum`, use `sha256sum` instead: `sha256sum exit-agent-tools-20261108.zip` and `sha256sum -c SHA256SUMS`. On Windows, extract the archive and compare `Get-FileHash -Algorithm SHA256 exit_client.py, exit_mcp.py, exit_evidence.py` with the table in [the README](../README.md#verify-the-client-files).

Keep these files together. The three public log tools need `exit_evidence.py` and `tools/exit_log_verify.py`, and `exit_evidence.py` pins the SHA-256 of `tools/exit_log_verify.py` and refuses any other copy.

```text
exit-agent-tools/
  exit_mcp.py
  exit_client.py
  exit_evidence.py
  tools/exit_log_verify.py
```

## 2. Test the server in a terminal

In the `exit-agent-tools` folder, in a macOS or Linux shell:

```sh
python3 --version
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python3 -B exit_mcp.py | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["result"]["tools"]))'
```

The first command should show Python 3.10 or later. On macOS, `/usr/bin/python3` can be older than 3.10; then use a newer Python. The second command sends one `tools/list` request and prints `30`, the number of tools. These two lines were not run on Windows for this page.

Then note two absolute paths for the client settings: the Python you used (`which python3` on macOS or Linux, `where python` on Windows) and the full path of `exit_mcp.py` (`pwd` on macOS or Linux, or `cd` in the Windows Command Prompt, prints its folder).

## 3. Your access key

Research tools need an EXIT access key in `EXIT_API_KEY`. A person gets it in a browser at https://api.exit-protocol.io (**Get free access**); account actions stay in the browser. The key is private: do not share it, and never put it in a chat, a prompt, a screenshot, an issue or a file you commit or publish.

`exit_service_status` and the three public log tools need no key. Without a key, the other tools refuse a valid call with `EXIT refused or failed: 0 EXIT_API_KEY is missing or not an EXIT access key`; here status 0 means EXIT refused the call before sending your key or question. `exit_contract_controls`, `exit_research_records`, `exit_research_record`, `exit_research_record_check`, `exit_watch_list`, `exit_watch_add`, `exit_watch_check` and `exit_watch_stop` first read the public status route, so without a network they answer `EXIT refused or failed: URLError` instead. Their answer can also come from that status read, for example when the service reports the feature as not enabled.

## 4. Claude Desktop

Claude Desktop reads its local MCP servers from `claude_desktop_config.json`. Open it in a text editor, and create it if it does not exist:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

The Claude Help Center describes two settings layouts:

- Newer layout: the **Local MCP servers** section of the Extensions page (**Settings > Desktop app**, then **Manage** next to **Extensions**) shows the servers' connection status and logs.
- Older layout: the same is under **Settings > Developer** (This computer). The MCP guide shows this layout: open **Settings…** from the Claude menu in the system menu bar, not from inside the window, then **Developer → Edit Config**, which creates the file or opens it.

Add the `exit-research` entry inside `mcpServers`, next to any servers already there:

```json
{
  "mcpServers": {
    "exit-research": {
      "command": "/ABSOLUTE/PATH/TO/python3",
      "args": ["-B", "/ABSOLUTE/PATH/TO/exit-agent-tools/exit_mcp.py"],
      "env": {
        "EXIT_API_KEY": "<your EXIT key>"
      }
    }
  }
}
```

- Use absolute paths. The app may start the server in an undefined working directory, and the server receives only a limited set of environment variables, which is why the key goes in `env`.
- On Windows, write paths with double backslashes or forward slashes, for example `"C:\\ABSOLUTE\\PATH\\TO\\exit-agent-tools\\exit_mcp.py"`, and use the full path of `python.exe` as `command`.
- The key is stored in this file as plain text. Keep the file private. For the keyless tools only, leave out `env`.
- Save, then quit Claude Desktop completely and open it again; closing the window is not enough. Then open **Add files, connectors, and more → Connectors → Manage connectors** and select `exit-research` to see its tools.
- Logs: `~/Library/Logs/Claude` on macOS, `%APPDATA%\Claude\logs` on Windows, `~/.config/Claude/logs` on Linux. `mcp.log` covers connections; `mcp-server-exit-research.log` holds this server's stderr.

## 5. Cursor

Use the global file `~/.cursor/mcp.json` (the `.cursor` folder in your home directory). If you use a project file `.cursor/mcp.json` instead, never put the key in it: [Cursor's help](https://cursor.com/help/customization/mcp) suggests committing that file to git.

```json
{
  "mcpServers": {
    "exit-research": {
      "type": "stdio",
      "command": "/ABSOLUTE/PATH/TO/python3",
      "args": ["-B", "/ABSOLUTE/PATH/TO/exit-agent-tools/exit_mcp.py"],
      "env": {
        "EXIT_API_KEY": "${env:EXIT_API_KEY}"
      }
    }
  }
}
```

- `${env:EXIT_API_KEY}` keeps the key out of the file: Cursor reads it from its own environment, and Cursor's documentation says to use environment variables for secrets. The variable must be available to Cursor; restart Cursor after you set it.
- You can write the key itself as the value instead. The file then holds it as plain text: keep the file private, and never do this in a project file.
- Save the file and restart Cursor. The tools appear in the tools list at the top of the chat panel.
- Logs: open the Output panel (Cmd+Shift+U on macOS, Ctrl+Shift+U on Windows and Linux) and select **MCP Logs**.

## 6. A real exchange without a key

Recorded on 11 November 2026 at 05:40 UTC with tools release `2026-11-08.1` (`exit_mcp.py` SHA-256 `dedeac5e97e4c0265288d6348b327177f296b5640aadc39242f3ef8f688941d5`), Python 3.12.14 and no `EXIT_API_KEY`. These lines were sent to the server's stdin, one per line:

```text
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"connect-guide-check","version":"1"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"exit_history","arguments":{}}}
```

The server answered with one line for each request that has an `id`; the notification gets no reply. `…` marks where a line is cut:

```text
{"jsonrpc": "2.0", "id": 1, "result": {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}}, "serverInfo": {"name": "exit-research", "version": "1.3.1"}}}
{"jsonrpc": "2.0", "id": 2, "result": {"tools": [{"name": "exit_mint_controls", …, {"name": "exit_verify", …}]}}
{"jsonrpc": "2.0", "id": 3, "result": {"content": [{"type": "text", "text": "{\"scope\": \"published_log_consistency_only\", \"consistency_ok\": true, \"anchor_verified\": false, \"leaves\": 1051, \"roots\": […], \"anchors_listed\": […], \"log_url\": \"https://api.exit-protocol.io/v0/log/\", \"requests\": 4, \"does_not_prove\": [\"that the chain state described by the evidence is true: check the evidence at its own slot or block\", …], \"note\": \"Published roots match these leaves and consistency paths. Chain transactions were not fetched.\"}"}], "isError": false}}
```

- `initialize`: the server is `exit-research` 1.3.1 and answers protocol version `2025-06-18`.
- `tools/list` returned 30 tools: `exit_mint_controls`, `exit_contract_controls`, `exit_control_state`, `exit_control_as_of`, `exit_control_change`, `exit_research_records`, `exit_research_record`, `exit_research_record_check`, `exit_watch_list`, `exit_watch_add`, `exit_watch_check`, `exit_watch_stop`, `exit_freeze_status`, `exit_governance`, `exit_governance_proposals`, `exit_layerzero_path`, `exit_layerzero_peer`, `exit_research_graph`, `exit_compare_answers`, `exit_evidence_view`, `exit_log_binding`, `exit_watch_add_contract`, `exit_webhooks`, `exit_webhook_delete`, `exit_freshness`, `exit_usage`, `exit_service_status`, `exit_history`, `exit_cite`, `exit_verify`.
- `exit_history` checked the public log's published roots and append consistency and listed its anchors: `consistency_ok` true, 1051 leaves (tree size 1051), 16 roots, 17 listed anchors, 4 requests to `api.exit-protocol.io`. It fetched no chain transaction, so `anchor_verified` is false; `exit_verify` is the tool that fetches the Solana anchor. The reply also lists what the check does not prove, such as that the chain state described by the evidence is true, or that nothing was left out of the log.

The newest anchor in that reply, as the log lists it (decoded from the `text` field and indented here):

```json
{
  "block_time": 1794357003,
  "block_time_utc": "2026-11-11T00:30:03+00:00",
  "explorers": [
    "https://solscan.io/tx/Qo1NVAz3te7P8bwyDrVTUqTY3uCXSkorgnYapZESqfpstVQJGpJXzKWf1hUSWP4w7QiwnBTwPNCKg8V29b3dYYd",
    "https://explorer.solana.com/tx/Qo1NVAz3te7P8bwyDrVTUqTY3uCXSkorgnYapZESqfpstVQJGpJXzKWf1hUSWP4w7QiwnBTwPNCKg8V29b3dYYd"
  ],
  "memo": "EXIT-ROOT-v1 1051 1b4db8261789b4e20a1060f4f58e3da7e965d1c976e4a606360a476b3fde2503 2026-11-11 967",
  "notary": "4QuiVCiYFzBjHFNEzZnHu9WCYBAZPnUxtfHcWX9UkqJH",
  "root": "1b4db8261789b4e20a1060f4f58e3da7e965d1c976e4a606360a476b3fde2503",
  "signature": "Qo1NVAz3te7P8bwyDrVTUqTY3uCXSkorgnYapZESqfpstVQJGpJXzKWf1hUSWP4w7QiwnBTwPNCKg8V29b3dYYd",
  "size": 1051,
  "slot": 467922566
}
```

A run after the next daily job lists a newer anchor and, when records were added, a larger log: a daily job at 00:30 UTC extends and anchors the log.

## 7. A recorded answer with a key

A recorded answer from 5 November 2026 at 00:05 UTC: `GET /v0/research/solana/mint` with `mint=5vPz2s8NtkasmVRDz5ySz27V1E8UdSpzqc9xN678jups`, as the API returned it (status 200, 0 credits) during EXIT's own measurement run. The full answer is 5,703 bytes, SHA-256 `374849bb8d03e1b1a4072e81ee6eb23a037325b67d1da7012532a5505e855da3`. Through the MCP server, `exit_mint_controls` returns this body as `value`, next to `meta` with `http_status`, `research_state`, `replayed`, `request_id` (new for each research call), `research_record` and `research_intake_full`. That run called the HTTP API directly, not through MCP, and the response headers that `meta` is built from were not recorded, so `meta` is described here, not shown. The service and the chain may have changed since.

Excerpt, indented here; `…` marks cut lines:

```text
{
  …
  "controls": [
    {
      "authority_address": null,
      "designation_status": "OBSERVED_EMPTY",
      "evidence_refs": [
        {
          "acquired_at": "2026-11-05T00:05:31.303569+00:00",
          "artifact": "3",
          "content_sha256": "c350dbb1e042f47a94e40d2242cdca941102975158150638b4bb917ee53e1490",
          "method": "getMultipleAccounts",
          "observed_at_slot": 465496560
        }
      ],
      "field": "mintAuthority",
      "holder": null
    },
    {
      "authority_address": null,
      "designation_status": "OBSERVED_EMPTY",
      …
      "field": "freezeAuthority",
      "holder": null
    }
  ],
  …
  "credits_charged": 0,
  …
  "limits": [
    "One provider-reported finalized observation; not an independent consensus proof.",
    "A designation is not proof that anyone can or did exercise the authority.",
    "An empty authority field means revoked or never set; this snapshot cannot distinguish them.",
    "No person attribution, investment assessment, transaction history or manipulation finding.",
    …
  ],
  …
  "observation": {
    "block_time": "NOT_ACQUIRED",
    "discovery_slot": 465496557,
    "finalized_slot": 465496560,
    "freshness": "snapshot_at_acquisition_not_continuous_monitoring",
    "known_at": "2026-11-05T00:05:31.303569+00:00"
  },
  "outcome": "ANSWERED_WITHIN_DECLARED_SCOPE",
  "policy": "solana-finalized-mint-pair-hop/2",
  "question": "Which mint, freeze and supported extension authorities are designated now?",
  …
  "schema": "exit.solana-mint-research/2",
  …
  "subject": {
    "chain": "solana-mainnet",
    "mint": "5vPz2s8NtkasmVRDz5ySz27V1E8UdSpzqc9xN678jups",
    "token_program": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
  },
  …
}
```

The cut parts include `artifacts`: the 3 raw replies of the public Solana RPC node, each with its SHA-256, to which the `evidence_refs` point.

## 8. Limits

Free early access: no payment, no wallet and no automatic paid conversion; answers are charged 0 credits. The live limits are at https://api.exit-protocol.io/v0/early-access (no key needed; `exit_service_status` reads the same route). Since the service release of 12 November 2026 it says:

| Limit | Value | Field |
|---|---|---|
| Research attempts per account per UTC day | 150 | `limits.attempts_per_account_day` |
| Completed answers per account per UTC day | 50 | `limits.answers_per_account_day` |
| Research attempts across the service per UTC day | 1500 | `limits.attempts_global_day` |
| New keys per UTC day | 100 | `limits.enrollments_day` |
| New keys per network per UTC day | 5 | `enrollment.network_daily_limit` |
| Accounts in total; research attempts in total (never reset) | 1000; 300000 | `limits.accounts_total`, `limits.attempts_total` |

- Since the same release the route also carries `service_capacity`: service-wide counts of the attempts used and remaining today and in total, and of the keys registered and remaining. Daily limits reset at 00:00 UTC; the totals are never reset.
- On a shared network, such as an office or a conference, the network limit is shared: a further new key that day is refused with `ENROLLMENT_NETWORK_LIMIT_REACHED`. Existing keys keep working.
- Status, usage and freshness reads spend no research attempts. The HTTP transport also has a burst limit: up to 20 burst units per account, refilling at 20 units per minute; status and usage reads count toward it.
- The chain-data providers see the addresses and accounts you ask about.
- An answer is an observation with its sources, times and limits. It is not a safety verdict, a price prediction or an identification of people, and an unresolved answer stays unresolved.

## 9. If it does not work

| What you see | What to check |
|---|---|
| `exit-research` does not appear | The file is valid JSON and both paths are absolute; quit and reopen the app completely; read the logs named above. |
| `EXIT refused or failed: 0 EXIT_API_KEY is missing or not an EXIT access key` | The key is missing from `env` (in Cursor: `EXIT_API_KEY` is not available to Cursor) or incomplete. Your key and question were not sent. |
| A public log tool answers `PUBLIC_FETCH_UNAVAILABLE_NO_RETRY` | The three public log tools connect directly to `api.exit-protocol.io` (`exit_verify` also to `solana-rpc.publicnode.com`). They ignore proxy settings, so a network that allows only a proxy blocks them. They do not retry. |
| The app cannot start a session with the server | The server uses MCP's `initialize` handshake, protocol versions 2025-06-18, 2025-03-26 and 2024-11-05. The current MCP version is 2026-07-28. Its specification says that a client supporting both kinds falls back to `initialize` and works, and that a client supporting only the newer kind fails. |

More: [AGENT-TOOLS.md](../AGENT-TOOLS.md) (tools and scope), [API quick start](API.md), [tools release](https://exit-protocol.io/tools/).
