# EXIT token and service rights

## Official status

**No official EXIT mint or launch is announced in this documentation.** EXIT is the
project identity and proposed token name. A matching ticker, logo or unofficial
market listing is not verification of an official asset.

The Owner selected **Jupiter Studio / Meteora Dynamic Bonding Curve (DBC), on Solana**,
after the quota-limited free API opens. This does not require the 30-day period to end.
Free access is still being prepared. No official mint address or launch is announced;
a matching name or ticker is not verification. Final identifiers will be published
with their verified record. See [Official identity](README.md#official-identity).

The research product is designed to be useful independently of speculative token
activity. The planned token utility is a separately implemented API usage right. Free API access needs neither a token nor payment; paid redemption is not offered yet.

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

The Owner has decided that the token is created through Jupiter Studio on the Meteora
Dynamic Bonding Curve program on Solana, after the free early-access API has been opened.
The token program, decimals
and authorities of the mint are published only as read back from the chain after creation;
the earlier venue preference is withdrawn. The choice of venue does not bias EXIT's
research toward or against any platform.

Creation and wallet signing remain Owner actions. No launch date, token price,
guaranteed distribution outcome or investment return is announced here.

## What the final official record must contain

Before a launch is announced, replace pending items with verified facts:

- Network, exact mint address and token program; decimals and relevant authorities/extensions.
- Exact initial service right, conversion/quote rules, quotas, expiry and service conditions.
- Supply and actual distribution mechanics; any founder purchase, its fraction and any verifiable lock.
- Treasury custody and access policies, actual fee mechanics and operating-budget reporting.
- Final venue and release/whitepaper versions, official links and any material unresolved limitations.

These are future disclosure requirements, not executed transactions or commitments
to an unselected allocation or lock product.

[Release status](STATUS.md) · [Roadmap](ROADMAP.md) · [Transparency](TRANSPARENCY.md)

## Venue documentation and remaining facts

Jupiter’s [official Studio documentation](https://docs.jup.ag/user-docs/launch/studio/graduation-and-fees), checked 25 October 2026, describes a 1% buy/sell fee split equally between creator and Jupiter, plus a decaying launch anti-sniper fee. It describes graduation to Meteora DAMM v2 and permanent locking of the initial graduated LP. Those published mechanics are not a claim that an EXIT pool exists, all later-added liquidity is locked or a particular mint authority configuration has been verified.

The selected venue is known. The uncreated token’s exact mint, program, authorities, extensions and accepted configuration remain unverified. DBC supports different token-program configurations; do not infer one from the venue name. These technical disclosures do not transfer the Owner’s personal financial decisions to an agent.

The [reviewed DBC SPL initializer](https://github.com/MeteoraAg/dynamic-bonding-curve/blob/91e696eef6a3764157220f6c104f079b7830fc04/programs/dynamic-bonding-curve/src/instructions/initialize_pool/ix_initialize_virtual_pool_with_spl_token.rs#L227-L254) issues the initial configured supply and revokes mint authority. The [standard Token-2022 initializer path](https://github.com/MeteoraAg/dynamic-bonding-curve/blob/91e696eef6a3764157220f6c104f079b7830fc04/programs/dynamic-bonding-curve/src/instructions/initialize_pool/process_initialize_virtual_pool_with_token2022.rs#L127-L166) likewise revokes mint authority for a configuration without a retained-mint option; the non-transfer-hook entry rejects that option. This is source-level evidence for the expected mechanism, not an observation of an EXIT mint or a verified source-to-deployed-binary match. Read-back still establishes the actual asset state.
