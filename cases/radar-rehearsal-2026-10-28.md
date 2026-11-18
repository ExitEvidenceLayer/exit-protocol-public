# EXIT's own radar rehearsal, 28 October 2026: the record and salt of evidence-log leaves 200 and 201

EXIT Protocol · 18 November 2026 · all times UTC

This note publishes two private records of EXIT's evidence log together with their salts, so that anyone can recompute the two
leaves and check that they are in an anchored tree. Both records belong to EXIT's own test account: they come from EXIT's own
end-to-end test of the alert pilot, not from any user. Records of user accounts stay private; only their salted leaves are public
([SPEC.txt](https://exit-protocol.io/log/SPEC.txt), section 5a).

## What happened

- On 28 October 2026 at 04:56, EXIT's own end-to-end test took the alert pilot's single watch slot. The watch was on the PYUSD
  mint on Solana, `2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo`. Its alert receiver ran on EXIT's own server.
- The radar's first read of that watch made radar events. The service bound the first two to the evidence log as private records
  of kind `service_answer` and gave each record and its salt to the test account only, in the event's `log` field.
  This note covers only these two records. Later radar events of the same watch may also have been bound to the log; they
  are not covered here and are not claimed. Whether any later leaf comes from this watch is UNKNOWN by design.
- The two records entered the private intake at 04:58:03. They are leaves 200 and 201 of the log, both with known_at
  `2026-10-28T04:58:03+00:00` ([leaves.json](https://exit-protocol.io/log/leaves.json)).
- They were first anchored in the tree of size 204. The anchor is Solana transaction
  [5qWsPQ…ayWtjx](https://explorer.solana.com/tx/5qWsPQwH5En3ZbVLBZvFMaNb5XYJnb2u6eg16RRSwU5hmHdeHkwzbno1CYL5jxDoApMxzRsWZYvrqmuHJhayWtjx)
  (slot 462,679,324, block time 29 October 2026, 00:30:00), signed by the server notary key
  `4QuiVCiYFzBjHFNEzZnHu9WCYBAZPnUxtfHcWX9UkqJH`. Its memo is
  `EXIT-ROOT-v1 204 6b4caf71d4ff517887414530c3c9e853119cfe64161483982efd2aa04b61ea0a 2026-10-29 200`.
- Until this note, the log listed the proof bundles of leaves 200 and 201 as held ([proofs.json](https://exit-protocol.io/log/proofs.json)),
  because they were private. The two bundles are now in this repository.
- The test watch ended after at most seven days. On 11 November 2026 at 06:04 a read of the service's records found no receiver
  and no watch ([CHANGELOG.md](../CHANGELOG.md)).

## The two records and their salts

Leaf 200:

```json
{
 "chain": "solana-mainnet",
 "evidence": [
  "36fb032da91cd7ad99d32c8138a3eaa910400352113e28fd50b1e4b4063cbfd9"
 ],
 "kind": "service_answer",
 "known_at": "2026-10-28T04:58:03+00:00",
 "observed_at": 462349422,
 "result_sha256": "ca69b059c37ce36f352f4c3c3b63c1645d414414ce97eabb7847d88af0a244b6",
 "subject": "2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo"
}
```

Salt of leaf 200: `dbe5bd0495e1f5e00d8efcc9d012865c`

Leaf 201:

```json
{
 "chain": "solana-mainnet",
 "evidence": [
  "36fb032da91cd7ad99d32c8138a3eaa910400352113e28fd50b1e4b4063cbfd9"
 ],
 "kind": "service_answer",
 "known_at": "2026-10-28T04:58:03+00:00",
 "observed_at": 462349422,
 "result_sha256": "5fbfb805f55e685b03988728ac2692a26fc4519700e35b2f4f8bb10e75da752c",
 "subject": "2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo"
}
```

Salt of leaf 201: `5040f1ab9d4e498895b9f46b982fe304`

The fields are those of every record in the log (SPEC section 1):

- `subject` is the watched mint and `observed_at` the Solana slot the radar read.
- `known_at` is the time the service made the event. It is EXIT's own statement; the anchor bounds it from above only.
- `evidence` holds the SHA-256 digests of the raw chain-read replies the event was built from. The replies are not published.
- `result_sha256` is the SHA-256 of the complete radar event without its `log` field and the delivery-only `webhook_id`
  (SPEC section 5a). The event bodies are not published, because they carry the service's internal watch identifier. So the
  `--event` check of the verifier cannot be run by a reader; the records alone can be checked.

Proof bundles (format `exit.evidence-proof/1`, same layout as the log's `proofs/<anchored tree size>/<8-digit leaf index>.json`):

| Leaf | known_at | First anchored tree | Bundle |
|---|---|---|---|
| 200 | 2026-10-28T04:58:03+00:00 | 204 | [radar-rehearsal-2026-10-28/proofs/204/00000200.json](radar-rehearsal-2026-10-28/proofs/204/00000200.json) |
| 201 | 2026-10-28T04:58:03+00:00 | 204 | [radar-rehearsal-2026-10-28/proofs/204/00000201.json](radar-rehearsal-2026-10-28/proofs/204/00000201.json) |

## Check it yourself

You need Python 3.9 or later. Nothing else is installed.

1. Get the verifier and check its hash against the log's list:

   ```
   curl -sSO https://exit-protocol.io/log/exit_log_verify.py
   curl -sS https://exit-protocol.io/log/SHA256SUMS | grep ' exit_log_verify.py$'
   shasum -a 256 exit_log_verify.py
   ```

   The two digests must be equal. [tools/exit_log_verify.py](../tools/exit_log_verify.py) in this repository is the same file.

2. Recompute a leaf from its record and salt (SPEC section 2: SHA-256 of `EXIT-LEAF-v1`, the 16 salt bytes and the canonical JSON
   of the record):

   ```
   python3 - <<'EOF'
   import hashlib, json, urllib.request
   B = 'https://raw.githubusercontent.com/ExitEvidenceLayer/exit-protocol-public/main/cases/radar-rehearsal-2026-10-28/proofs/204/'
   leaves = json.load(urllib.request.urlopen('https://exit-protocol.io/log/leaves.json'))['leaves']
   for i in (200, 201):
       b = json.load(urllib.request.urlopen(B + '%08d.json' % i))
       body = json.dumps(b['record'], sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
       d = hashlib.sha256(b'EXIT-LEAF-v1' + bytes.fromhex(b['salt']) + body).hexdigest()
       print(i, d, d == leaves[i]['leaf'])
   EOF
   ```

   Each line must end with `True`. The published leaves are
   `59d252001e472a3366b1537c90f9c02ff46a7041c6adc329eaf7af6b8010c324` (200) and
   `383de6ca40e5a4fb3633e193ec1c8db5cb7c1240af8cf09400d62446dd493030` (201).

3. Check inclusion and the anchor with the `proof` command (any Solana provider works in place of the public endpoint below):

   ```
   python3 exit_log_verify.py proof https://raw.githubusercontent.com/ExitEvidenceLayer/exit-protocol-public/main/cases/radar-rehearsal-2026-10-28/proofs/204/00000200.json --rpc https://api.mainnet-beta.solana.com --trust github,dns,site
   python3 exit_log_verify.py proof https://raw.githubusercontent.com/ExitEvidenceLayer/exit-protocol-public/main/cases/radar-rehearsal-2026-10-28/proofs/204/00000201.json --rpc https://api.mainnet-beta.solana.com --trust github,dns,site
   ```

   Each must print `"verified": true`. Without `--rpc` the command checks inclusion in the stated root only and prints
   `"verified": false` with `"inclusion_ok": true`.

4. Check the same records against the live log with the `leaf` command. It computes the audit path from the published leaves
   itself, so it does not rely on the path in the bundle:

   ```
   curl -sSO https://raw.githubusercontent.com/ExitEvidenceLayer/exit-protocol-public/main/cases/radar-rehearsal-2026-10-28/proofs/204/00000200.json
   python3 exit_log_verify.py leaf 00000200.json --log https://exit-protocol.io/log/ --rpc https://api.mainnet-beta.solana.com
   ```

   (the same for 00000201.json).

## What this shows, and what it does not

- It shows that these two records, with these salts, are leaves 200 and 201 of EXIT's log, and that a tree containing them was
  anchored on Solana no later than 29 October 2026, 00:30:00.
- It shows that the alert pilot's binding path worked end to end once: a radar event became a private record, the record was
  admitted at the next nightly run and anchored.
- It does not show that the chain state the records describe is true (check the evidence at its own slot), that EXIT knew it
  before the anchor, or anything about who controls the PYUSD mint (SPEC section 9).
- Publishing these two salts reveals only these two records. Every record has its own random salt, so no other leaf is affected.
- It covers leaves 200 and 201 only. Later radar events of the same watch may also have been bound to the log; they are not
  covered by this note and nothing is claimed about them. Whether any later leaf comes from this watch is UNKNOWN by design.
- How EXIT checked it before publishing: both leaves were recomputed from the records and salts above, and both audit paths
  were checked against the anchored root of tree size 204. That inclusion check is computational. The anchor transaction was
  then read with exit_log_verify.py `proof --rpc` from one Solana provider only, the public endpoint
  `https://api.mainnet-beta.solana.com`; no second provider was used. Readers can repeat both checks with steps 2 to 4.

## Correction

No correction to this note so far. The list of corrections is in [CORRECTIONS.md](../CORRECTIONS.md).

## Evidence

| What | Where |
|---|---|
| Leaves 200 and 201 | [leaves.json](https://exit-protocol.io/log/leaves.json) |
| Anchor of tree size 204 | [anchors.json](https://exit-protocol.io/log/anchors.json); [Solana explorer](https://explorer.solana.com/tx/5qWsPQwH5En3ZbVLBZvFMaNb5XYJnb2u6eg16RRSwU5hmHdeHkwzbno1CYL5jxDoApMxzRsWZYvrqmuHJhayWtjx) |
| Held proof bundles before this note | [proofs.json](https://exit-protocol.io/log/proofs.json), entry 204 |
| Record and leaf rules | [SPEC.txt](https://exit-protocol.io/log/SPEC.txt), sections 1, 2 and 5a |
| Notary keys | [NOTARIES.md](../NOTARIES.md) |

EXIT does not attribute any key or account to a person or organization.
