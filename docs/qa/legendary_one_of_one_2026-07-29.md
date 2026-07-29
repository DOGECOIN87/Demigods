# QA — legendary 1-of-1 pieces (7)

Date: 2026-07-29
Assets: `assets/legendary/legendary_001…007_*.png`
Prompts: `prompts/22_legendary_one_of_one.md` → `prompts/batch_legendary.md`

## The set

| # | Title | Domain root in the collection | 1-of-1 element |
|---|---|---|---|
| 001 | Sovereign of the Solar Court | `background_005` / `outfit_005` | Solar corona behind, rays crossing in front of the shoulders |
| 002 | Oracle of the Waning Crescent | `background_006` / `outfit_004` | Crescent light held in a raised hand |
| 003 | Heir of the Celestial Throne | `background_001` / `outfit_001` | Star-mapped cape spilling across the hall floor |
| 004 | Keeper of the Arcane Index | `background_003` | Sigil rings passing behind and in front of the body |
| 005 | Warden of the Violet Void | `background_008` / `aura_rear_004` | Void singularity in one palm, hem dissolving to embers |
| 006 | Tempest Sovereign | `outfit_002` / lightning aura | Lightning branching into a raised palm |
| 007 | Verdant Archivist | `outfit_003` | Vines and drifting spores wrapping the figure |

Each is rooted in an environment or wardrobe theme the collection already
established, so a legendary reads as the apotheosis of something a holder has
already seen rather than a piece from a different world.

## Automated checks

`scripts/validate_legendary.py` — **7/7 passed**: full decode, PNG, native
1254 × 1254, fully opaque (`alpha_min=255`), RGB, and seven distinct SHA-256
digests.

The digest check is not boilerplate. "1 of 1" is the entire premise of these
pieces, and a duplicated file would destroy it silently — nothing else in the
pipeline would notice.

## Why a new validator was needed

Every existing gate assumes a modular layer and fails a legendary by design:

- `--trait` and `--floor-aura` measure a silhouette inside a transparent canvas;
  a full-bleed image has no silhouette to measure and no transparent background.
- `--global-finish` enforces a peak-alpha ceiling; these are opaque.
- `validate_assets.py` skips the folder outright, because `legendary` is not one
  of the sixteen trait categories.

So the pieces would have been registered entirely unchecked. The new validator
covers what actually matters for a flattened illustration.

## Human checks

Two things are deliberately left to a person rather than faked in code, because
neither is decidable from pixel statistics and a check that does not mean
anything is worse than no check:

- no text, signature, or watermark anywhere in frame;
- the piece's required 1-of-1 element is actually present.

Both were confirmed by eye on all seven. Every piece keeps the collection's
camera, chibi proportions, and upper-left key lighting, and each shows an
asymmetric pose, a held object, or an effect crossing the body — none of which
the modular layer system can express.

## Deliberate exclusions

**Not composed by `generate_777.py`.** It stacks approved layers; these have no
layers. `discover_assets` iterates only the sixteen entries of `LAYER_ORDER`, so
`assets/legendary/` is invisible to it and the generative run is unaffected —
verified: preflight still reports a rule-valid space of 3547 at 21.9%
saturation.

**No global finish, no background depth pass.** Both exist to make separately
produced modular parts agree with each other. A 1-of-1 is painted as a single
internally consistent image; treating it again would flatten contrast it was
composed with.

**Registered under `legendary_one_of_ones`, not `registered_production_assets`.**
A legendary is not a trait, and mixing it into the trait ledger would corrupt the
category counts that drive the production status report. The trait ledger stays
at 32 across 16 categories.

## Open decision — supply arithmetic

Still unresolved, and it must be settled before minting because it is not
reversible once the collection is public:

- **770 generative + 7 legendary = 777.** Keeps the headline number. Set
  `supply` to 770 in `config/collection.json` and reserve seven token IDs.
- **777 generative + 7 legendary = 784.** Leaves the generative run untouched
  and changes the collection size.

The saturation maths is indifferent — the rule-valid space is 3547, so dropping
to 770 changes nothing material.
