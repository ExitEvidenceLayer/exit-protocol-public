# Research API · access status

**25 October 2026: restricted alpha; 30-day quota-limited free first access is prepared, not open.** No key-issuance form, public activation date or paid plan is offered here yet.

The public website searches recorded case notes and creates local drafts. It does not send arbitrary prose to a live research worker. The tested free-serving candidate accepts structured questions only on declared supported subjects. It needs no wallet, blockchain token, signature or payment.

## Available public example

```sh
curl https://exit-protocol.io/solana-pyusd.json
```

This retrieves an authored case note, not an authenticated core response or a full raw-evidence archive.

## Restricted engine

The existing alpha uses approved bearer access at `https://alpha.exit-protocol.io`; unauthenticated requests return 401. The contract declares exact supported route and parameter fields. Never place keys in URLs, browser screenshots, GitHub issues or logs.

Prepared free-service limits: 20 completed answers/account/day, 60 attempts/account/day, 300 global attempts/day, 9,000 attempts/campaign, 600 accounts maximum and 20 enrollments/day. These are candidate caps, not measured public capacity or a guaranteed allocation. Public dates, final limits and the access URL will be published only after activation. The campaign lasts 30 days from activation, not 30 days per user. No automatic paid conversion.

Incomplete answers, technical failures and unsupported requests do not spend answer allowance; attempt and abuse limits still apply. Optional cached answer copies expire after 24 hours; structured details and feedback are pruned after 7 days during maintenance. Hashed replay/counter records persist for campaign/recovery controls. These limits do not promise deletion from all backups.

No general all-wallet analysis, price prediction, guaranteed manipulation detection or beneficial-owner identification is offered. Ethereum research references and free-serving supported subjects are separate declarations; do not assume every case is a live supported route.

[Current status](../STATUS.md) · [Rights and selected venue](../TOKEN.md)

## Executed response excerpt

The following excerpt was captured from the tested service code in a local isolated run against the pinned `7ce62fe` reference runtime on 25 October 2026. The query uses the shown historical valid/known cutoffs. This is **not** a request to a public free endpoint, a claim about current chain state or a complete replay export. `controllers_excerpt` is an explicitly selected display field, not a field added to the core response schema.

```json
{
  "schema_version": "0.1.0",
  "query": {
    "known_at": "2026-08-01T23:59:59+00:00",
    "query_type": "control_state",
    "subject_id": "usdc-mint-authorities",
    "valid_at": "2026-08-01T00:00:00+00:00"
  },
  "response_content_hash": "sha256:3269a4d8f272e0346b6a88f17ddd2b73d5d533221221daa8ab5c7bcce0776985",
  "controllers_excerpt": [
    {
      "authority_class": "freeze_authority",
      "controller_status": "OBSERVED"
    },
    {
      "authority_class": "mint_authority",
      "controller_status": "OBSERVED"
    }
  ]
}
```
