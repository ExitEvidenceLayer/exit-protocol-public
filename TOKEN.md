# EXIT token and service rights

## Official status · verified 25 October 2026

| Field | Read-back / current status |
|---|---|
| Name / symbol | EXIT Protocol / EXITP |
| Network | Solana mainnet |
| Official mint | `5vPz2s8NtkasmVRDz5ySz27V1E8UdSpzqc9xN678jups` |
| Studio page supplied by the Owner | https://studio.jup.ag/tokens/5vPz2s8NtkasmVRDz5ySz27V1E8UdSpzqc9xN678jups |
| Token program | Standard SPL Token: `TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA` |
| Decimals | 6 |
| Observed supply | 1,000,000,000 tokens; atomic supply `1000000000000000` |
| Mint authority / freeze authority | Both `null` |
| Observations | Two finalized keyless RPC reads, slots 461256701 and 461256702, 25 Oct 2026 ~12:26:04 UTC |
| Free research access | Open; no token or payment required |
| Token-to-credit / paid API Pass redemption | **NOT LIVE** |

The Owner created the token through Jupiter Studio / Meteora DBC and supplied the
identifier before the API opened at 12:38:20 UTC. The actual sequence supersedes the
earlier plan; it is not backdated. Matching names or tickers do not identify this asset.
Authority revocation is a narrow token-program fact, not a guarantee about price,
liquidity, distribution, beneficial ownership or investment safety.

The live free research service is independent of token ownership. Proposed paid
usage rights require a later implemented integration. A Studio description that says
EXITP already “redeems” for research credits or API Pass should be read as a proposed
future use, **not a current capability**. This current record states the actual boundary.

## Service rights

The proposed optional API Pass redeems an accepted token payment for a quoted
number of service credits on supported research routes. A private adapter has
undergone local tests; it is not yet offered as a public paid service.

| Question | Intended rule |
|---|---|
| What does a payment buy? | The exact service credits and scope in an accepted quote. |
| When is a research request charged? | Only when the declared primary question receives a supported delivered answer. |
| What happens to an unanswered or conflicting result? | No credit charge; bounded follow-up intake where capacity permits. |
| Does a later token transfer move redeemed credits? | Redeemed account credits do not automatically transfer with a later token sale. |
| Does merely holding the token activate unlimited access? | No. A holding balance is not a redeemed payment receipt. |
| Does payment change the evidence? | No. Research conclusions and evidence identity remain independent of payment. |
| What remains before a paid API Pass release? | Exact commercial terms, serving integration, actual payment rehearsal and final security/operating acceptance. |

The proposed token grants no automatic equity, project-income share, return, control
over findings or access to restricted investigations. This is the present utility
design, not a general ban on future business models. Any material rights change
would need a new concrete design, review, decision and disclosure.

## Venue selection

The Owner created the token through Jupiter Studio on the Meteora
Dynamic Bonding Curve program on Solana.
The token program, decimals
and authorities above were read back from the chain after creation;
the earlier venue preference is withdrawn. The choice of venue does not bias EXIT's
research toward or against any platform.

Creation and wallet signing remain Owner actions. No launch date, token price,
guaranteed distribution outcome or investment return is announced here.

## What the final official record must contain

Continue updating actual operational and financial disclosures with verified facts:

- Network, exact mint address and token program; decimals and relevant authorities/extensions.
- Exact initial service right, conversion/quote rules, quotas, expiry and service conditions.
- Supply and actual distribution mechanics; any founder purchase, its fraction and any verifiable lock.
- Treasury custody and access policies, actual fee mechanics and operating-budget reporting.
- Final venue and release/whitepaper versions, official links and any material unresolved limitations.

These are future disclosure requirements, not executed transactions or commitments
to an unselected allocation or lock product.

[Release status](STATUS.md) · [Roadmap](ROADMAP.md) · [Transparency](TRANSPARENCY.md)

## Venue documentation and remaining facts

Jupiter’s [official Studio documentation](https://docs.jup.ag/user-docs/launch/studio/graduation-and-fees), checked 25 October 2026, describes a 1% buy/sell fee split equally between creator and Jupiter, plus an additional launch anti-sniper fee described as decaying from 99% to 0% during the first 15–60 seconds, allocated to the creator. It describes graduation to Meteora DAMM v2 and permanent locking of the initial graduated LP. Those published generic mechanics do not verify the actual EXIT pool configuration, every later-added liquidity position or personal purchases. The mint fields above were verified separately.

The selected venue and created mint identity are known. Actual pool fees, liquidity positions, distribution and any personal financial actions require their own read-back and dated disclosures. DBC supports different token-program configurations; do not infer one from the venue name. These technical disclosures do not transfer the Owner’s personal financial decisions to an agent.

The [reviewed DBC SPL initializer](https://github.com/MeteoraAg/dynamic-bonding-curve/blob/91e696eef6a3764157220f6c104f079b7830fc04/programs/dynamic-bonding-curve/src/instructions/initialize_pool/ix_initialize_virtual_pool_with_spl_token.rs#L227-L254) issues the initial configured supply and revokes mint authority. The [standard Token-2022 initializer path](https://github.com/MeteoraAg/dynamic-bonding-curve/blob/91e696eef6a3764157220f6c104f079b7830fc04/programs/dynamic-bonding-curve/src/instructions/initialize_pool/process_initialize_virtual_pool_with_token2022.rs#L127-L166) likewise revokes mint authority for a configuration without a retained-mint option; the non-transfer-hook entry rejects that option. This is source-level evidence for the expected mechanism, not a source-to-deployed-binary match. The actual EXIT mint authorities were observed separately above. Read-back still establishes the actual asset state.
