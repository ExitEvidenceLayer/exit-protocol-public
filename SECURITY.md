# Security reporting

Report a suspected vulnerability privately to **security@exit-protocol.io** with
subject **EXIT security report**. The same contact is published in
[security.txt](https://exit-protocol.io/.well-known/security.txt). Include the affected public surface/version,
expected and observed behavior, and a minimal reproduction that uses your own
authorized data. Never send a seed phrase, private key, bearer credential or another
person's confidential information.

Please do not place exploit steps, secrets or non-public investigations in public
issues. If the information is sensitive, begin with a non-sensitive summary and
request an appropriate confidential transfer method before sending the details.
No encrypted mailbox, response-time guarantee or paid bounty is promised here.

## Scope and safe handling

Use local reproductions and controlled inputs where possible. Do not test payment
or access behavior against other accounts, disrupt a live service or submit an
unauthorized chain transaction to demonstrate a problem.

EXIT's engineering process uses source-bound tests, negative examples, replay,
concurrency/fault checks and separate review where required. A local test suite
does not establish zero bugs or replace final operational/security acceptance.

[Delivery status](STATUS.md) · [Support](SUPPORT.md)
