# What you can use today

Checked live on 18 November 2026 (UTC). Each line works now and has its link. Limits and
boundaries in full: [STATUS.md](STATUS.md) and [docs/API.md](docs/API.md). Changes: [CHANGELOG.md](CHANGELOG.md).

## Without a key

- **Control Map**, https://exit-protocol.io/control-map/ : which addresses hold the control roles of 72 token deployments on
  Ethereum and Solana, each row at one finalized block or slot. The page was built once, from the nightly read of 11 November
  2026, and is not yet rebuilt every night; later changes show on the daily re-read page,
  https://exit-protocol.io/control-map/daily/ . The 27 and 28 October 2026 snapshot by holder address:
  https://exit-protocol.io/control-map/by-controller/ .
- **Case files**, https://exit-protocol.io/case-files/ : 3 case files, each with the SHA-256 of the evidence its claims rest on
  and a leaf of the evidence log. Case notes: [cases/](cases/) and the research desk, https://exit-protocol.io/#research .
- **Evidence log**, https://exit-protocol.io/log/ : EXIT's own records in an append-only Merkle log; its root is anchored on
  Solana once a day, shortly after 00:30 UTC. The same files without a key: https://api.exit-protocol.io/v0/log/SHA256SUMS .
- **Verify one record in the browser**: https://exit-protocol.io/verify/ (leaf index, proof bundle, or a record with its salt).
- **Verify from the command line** (Python 3.9 or later, standard library): download https://exit-protocol.io/log/exit_log_verify.py ,
  check its SHA-256 against the value in [README.md](README.md), then run
  `python3 exit_log_verify.py proof https://exit-protocol.io/log/proofs/1640/00000000.json --rpc <Solana RPC URL> --notaries https://exit-protocol.io/log/notaries.json`
  (another record: `proofs/<size>/<8-digit leaf>.json`; `log https://exit-protocol.io/log/ --rpc <URL>` checks the whole log).
  A pass shows that the record was committed no later than the anchor's block time, not that it is true or complete.
- **Service state and capacity**: https://api.exit-protocol.io/v0/early-access .

## Get a free key

Open https://api.exit-protocol.io/ and select **Get free access**: no email, wallet, token or payment. The browser solves a
proof of work (https://api.exit-protocol.io/early-access/challenge , 16 zero bits, valid 600 seconds); the script version
is in [docs/API.md](docs/API.md). Keep the key private. At most 100 new keys a UTC day, 5 per network;
allocation is not guaranteed. Per account (key) and UTC day: 50 completed answers and 150 attempts; across the service: 1,500 attempts a
day, and lifetime totals of 300,000 attempts and 1,000 keys, never reset. Existing keys have no fixed end date. The
[terms](https://exit-protocol.io/terms.html): "A later reduction of the offer or announced end of free access requires at least
30 days' notice. Reaching a published lifetime total is not an announced end and has no notice period." Once the attempt total
is used, requests that need a research attempt are refused and no new key is issued.

## With a key (live routes, https://api.exit-protocol.io/openapi.json )

- Mint, freeze and supported Token-2022 authorities of any Solana token mint: `GET /v0/research/solana/mint`.
- Control reads of any Ethereum contract (proxy slots, `owner()` as an observation, the multisig getOwners/getThreshold
  answer, not proof of who holds keys, and default-admin members, up to four, only when the AccessControl enumerable
  interface is declared): `GET /v0/research/ethereum/contract`.
- USDT, USDC and PYUSD issuer freeze status and balances of an Ethereum address: `GET /v0/research/ethereum/freeze`.
- Supported SPL Governance V2 accounts and their proposals: `GET /v0/research/solana/governance`, `.../governance/proposals`.
- LayerZero V2 OApp pathway and peer on Ethereum: `GET /v0/research/ethereum/layerzero`, `.../layerzero/peer`.
- Watches of a mint or contract (three per key, 300 in all, seven days), re-read when you ask, at most every six hours;
  each watch re-read spends one research attempt: `/v0/research/watch`.
- This key's research records (last 50, any state; reading spends no research attempt): `GET /v0/research/records`. Views
  over your own answers: `/v0/research/evidence`, `/v0/research/compare`, `/v0/research/graph`.
- Three recorded reference subjects, `/v0/control_state`, `/v0/control_as_of`, `/v0/control_change`: a recorded view from
  evidence read on 1 August 2026, not a current read; a holder may have changed since (the PYUSD mint authority has). For
  the current authorities of the USDC or PYUSD mint use `GET /v0/research/solana/mint`; no route of this service reads the
  Pump program's upgrade authority directly.
- Scripts and agents: `exit_client.py` and the stdio MCP server `exit_mcp.py` (30 tools; exit_history, exit_cite and
  exit_verify need no key), see [AGENT-TOOLS.md](AGENT-TOOLS.md) and [docs/CONNECT-AN-AGENT.md](docs/CONNECT-AN-AGENT.md);
  package and hashes: https://exit-protocol.io/tools/ .

## Not available today, and planned

No paid API Pass (a private prototype), no continuous monitoring (watches are re-read on request; a limited receiver pilot is in
[docs/API.md](docs/API.md)), no all-wallet tracing. Planned work and dates: [ROADMAP.md](ROADMAP.md) and
https://exit-protocol.io/ROADMAP.html . Questions: [SUPPORT.md](SUPPORT.md).
