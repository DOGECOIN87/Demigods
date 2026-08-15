# Demigods 777 — Collection Completion Oversight Plan

**Owner:** Collection leadership  
**Operating objective:** Deliver a fully verified, art-complete NFT release set comprising **770 deterministic generative tokens plus 7 registered legendary 1-of-1s**, for a total of **777 tokens**.

## Current Baseline

The repository is technically stable. The latest local audit passed the configuration, asset, manifest-consistency, production-ledger, and generation preflight checks, while the complete regression suite passed **192 tests**. The latest repository workflow also completed successfully, and there are no open repository issues. The collection has 32 registered trait-production assets across 16 categories, together with seven completed legendary illustrations. The live generative supply is 770 tokens; IDs 0111, 0222, 0333, 0444, 0555, 0666, and 0777 are reserved for the legendary set.

> **Release principle:** no asset, image, metadata record, or token is considered complete merely because it exists. It must satisfy the relevant art-direction, binary, rig, compatibility, provenance, and collection-level validation gates.

| Workstream | Present state | Completion standard | Accountable gate |
|---|---:|---|---|
| Base bodies and poses | 5 of 5 registered | All shared poses remain locked and compatible | Rig and asset validation |
| Backgrounds | 8 of 8 registered | Native backgrounds remain depth-treated and registered | Asset, manifest, and composite review |
| Legendary 1-of-1s | 7 of 7 registered | Seven unique opaque 1254 × 1254 illustrations on reserved IDs | Legendary validator and human art review |
| Modular trait library | 32 registered paths; 128 remaining backlog paths | Each necessary trait is approved, registered, and compatibility-safe | Intake, rig, composite, and ledger gates |
| Generative collection | Preflight passing; no final render | Exactly 770 non-reserved IDs, unique signatures, validated metadata and image provenance | Generation and output validation |
| Release operations | Not represented in this repository | Storage, contract or launchpad, metadata-hosting, and release checks are documented and completed | Separate release-readiness checklist |

## Completion Definition

The artistic and technical collection is complete only when all required trait categories have sufficient approved production assets to produce a visually coherent, rarity-balanced collection; the deterministic generator produces 770 unique modular outputs without using reserved legendary IDs; all seven legendary images are placed at their reserved IDs; every image and metadata record has passed independent verification; and the final release manifest is immutable, versioned, and ready for the selected minting route.

Marketplace publication, smart-contract deployment, token minting, storage pinning, and legal or commercial approvals are **separate external release activities**. They cannot be selected or completed responsibly until the collection owner specifies the target chain, minting model, treasury and royalty policy, marketplace or launchpad, metadata host, and release authority. Art production will proceed independently while these decisions remain open.

## Priority Roadmap

The next work must create convincing completed characters before expanding lower-impact decorative categories. The existing modular outfits are visually sound but need hair and face traits to become market-ready. The production sequence therefore prioritizes the hair-plus-face system, then silhouette and accessory variety, then effects and finishes.

| Milestone | Scope | Exit condition | Current priority |
|---|---|---|---:|
| M1 — Hair and face pilot | Hair-front 003 paired with registered hair-back 003; first eyes, eyebrows, mouth, and expression-mark representatives | At least one fully realized character passes composite review on contrasting backgrounds and with an outfit | Critical |
| M2 — Hair-family completion | Remaining seven back-hair and eight front-hair assets, with required front/back compatibility bindings | No bald or mismatched-hair output is possible; hair styles remain readable across outfits | Critical |
| M3 — Facial-system completion | 24 eye pairs, 16 eyebrow pairs, 12 mouths, and 8 expression marks | Face traits are anchored correctly, visible under the hair family, and do not produce collisions | Critical |
| M4 — Wardrobe and silhouette expansion | Five remaining outfits and eight back accessories | Pose rules and silhouette compatibility are proven with cross-category stress composites | High |
| M5 — Accessories and held objects | Eight neck, ten head, and twelve hand-object traits | Head, neck, hand, and pose interactions are explicitly rule-bound where needed | High |
| M6 — Remaining effect family | Eight outstanding rear auras and two front auras | Effects have clean alpha, correct depth order, and no character-obscuring conflicts | Medium |
| M7 — Collection lock | Full library, compatibility freeze, rarity review, dry run, final render, metadata, and verification | Exact 770-plus-7 set passes all release gates | Critical |

## Immediate Production Directive

The first controlled batch should be a **face-completion pilot**, not a broad unreviewed bulk run. The pilot consists of hair-front 003, eyes 001, eyebrows 001, mouth 001, and expression mark 001, composited with registered hair-back 003 and outfit 001 over two contrasting backgrounds. This is the smallest package that can validate the complete character reading, hair/face anchors, and layer ordering. A successful pilot establishes the reusable quality bar for the entire facial system; a failed pilot prevents mass production of misaligned face traits.

After pilot approval, the next batch should complete the remaining hair-pair family before opening the full facial set. This follows the repository’s required hair pair bindings, materially increases character differentiation, and prevents the final generator from producing unfinished bald avatars. The facial system then follows in bounded review batches, rather than a single large drop, so that eye-line, mouth, and hair-overlap defects are caught early.

## Mandatory Quality Gates

| Gate | Applies to | Requirement |
|---|---|---|
| Candidate intake | Every new asset | Native 1254 × 1254 PNG, correct alpha behavior, correct canonical path, and no prohibited baked layers |
| Geometry and rig | Bodies, outfits, accessories, and traits | Correct gate mode; trait placement proved by a composite over the appropriate base pose |
| Art direction | Every candidate | Front-facing chibi-fantasy language, stable facial proportions, upper-left key light, clean transparency, and no style drift |
| Compatibility | Every cross-category interaction | Explicit rules for pose-bound outfits, paired hair, hand objects, headwear, exclusions, and requirements |
| Registration | Every accepted asset | Approved bytes copied into canonical path; manifest, backlog, and generated ledger agree |
| Batch review | Each milestone | Review sheet includes contrasting backgrounds and the relevant outfit/effect combinations |
| Collection preflight | Before final generation | Configuration, assets, manifest, ledger, capacity, rule-valid-space, and saturation checks pass |
| Final release verification | Final collection | Independently verify exact image and metadata sets, IDs, hashes, signatures, provenance, and legendary reservations |

## Oversight Cadence and Escalation

Each production checkpoint will record the work completed, validation evidence, unresolved blockers, next asset or batch, and whether a collection-level decision is required. Any asset that fails binary or rig validation is rejected without visual exception. Any asset that passes automation but conflicts with the locked visual language, obscures the face, duplicates an existing visual idea, or creates a confusing rarity pattern will be held for rework.

The following matters require owner confirmation before irreversible release work begins: the target chain and contract standard; whether the collection is minted by a smart contract, launchpad, or marketplace-native mechanism; royalty recipient and percentage; wallet and treasury controls; metadata and image hosting; launch date and pricing; allowlist, reserve, or giveaway policy; and the final legal, community, and brand approvals.

## Current Blockers

There is **no active repository blocker**. The practical constraint is production completeness: 128 distinct trait-production paths remain unregistered, and no complete modular character has yet passed the full hair-plus-face composite gate. The external release path is also undecided, but it does not prevent the next art-production milestone.

### Generator-source transformation policy

The owner authorized a formal policy revision on 2026-08-15. The repository now permits a larger isolated RGBA generator source to enter `docs/workflows/generator_source_transform.md`, which records the immutable source digest, reduction-only transform, alpha cleanup, final output digest, and locked-rig placement. The final registered asset remains strictly 1254 × 1254 RGBA with genuine alpha and must pass all existing binary, rig, composite, manifest, and human art-direction gates.

The first transformed hair-front pilot verified the new technical route: its normalized output passed source provenance, final-canvas, alpha, bounds, and width-ratio checks. It was nevertheless rejected by full-context art review because its fringe obscured the eyes, its silhouette did not blend cleanly into the registered rear-hair family, and visible green residual artifacts remained. The updated constraint is therefore **creative quality, not source normalization capability**. See `docs/qa/face_completion_pilot_hair_front_003_2026-08-15.md`.

## Sources

The plan is governed by the repository’s `config/collection.json`, `assets/asset_manifest.json`, `docs/production_status.md`, `docs/trait-production-backlog.md`, `docs/qa/legendary_one_of_one_2026-07-29.md`, approved prompts, validators, and the oversight visual review dated 2026-08-15.
