# Pending candidate realignment — 2026-09-07

**Categories:** head accessories (DG-123 … DG-132), hand objects (DG-133 … DG-137), plus a
correction to the registered base master's undergarment coverage.
**Scope:** all fifteen candidates are registered (see Disposition), alongside a correction to
the registered base master's undergarment coverage. No metadata, release, minting or on-chain
change has been performed.

## Why this pass exists

Both batches had already passed binary intake and the category rig gate, and both were
recorded as visual passes — `docs/qa/head_accessories_001-005_regen_review.md`,
`docs/qa/head_accessories_006-010_regen_review.md`, and
`docs/qa/hand_objects_001-005_regen_review.md`. They were nonetheless misplaced against the
rig, because the automated gates check canvas, alpha, and maximum bounds, and none of those
can see whether a layer is seated on the anatomy it belongs to.

Two distinct causes:

**Head accessories — one seat for ten designs.** Every row was normalized at 520 px wide with
its top at Y 129, the top of the locked character bounds. That is correct for a crown and
wrong for a circlet. The measured head is 329 px wide at its widest (Y 276–291) and the hair
pair spans 419–529 px, so 520 px was wider than the character's whole head, and a forehead
band seated at Y 129 floats above the skull with nothing under it. DG-129 and DG-132 read as
hovering rings; DG-124's face-on circle read as a hoop the character stands inside rather
than a halo.

A first correction pass sized each design against the skull curve but still let most bands
land on the eyebrow line at Y 308–323, which on a head this large reads as headwear slipping
down over the face. The seats here are the second pass: every band now sits on the skull dome
and clears the brow.

**Hand objects — the retired shared anchor.** All five were normalized against
`viewer_left_hand_anchor` X 404. `docs/qa/hand_object_recalibration_findings_2026-08-15.md`
established that this coordinate sits at the wrist, not through the hand, and replaced it
with measured per-pose contacts — pose 002 `(438, 772)`, pose 004 `(438, 748)` — plus a
12° outward lean so a held shaft reads as gripped rather than propped. The registered
objects DG-138 … DG-144 received that pass. These five predate it and never did.

## What was done

`scripts/align_pending_candidates.py` holds the alignment table and reproduces all fifteen
deterministically.

The ten head accessories are **re-derived from their immutable generator sources in a single
reduction**, so nothing is resampled twice; only the target width and seat Y changed. DG-124
additionally uses the new `--target-height` option on `scripts/normalize_generator_source.py`,
which foreshortens the generator's face-on ring into the ellipse a front-facing rig needs.
Both axes still reduce, so the transform stays reduction-only.

The five hand objects keep their already-normalized bytes and receive only the same integer
translation and lean the registered family received.

| ID | Asset | Change | Lowest ink | New bounds |
|---|---|---|---|---|
| DG-123 | gold pointed crown | 520 → 330 wide | Y408 → Y356 | `[462,129,791,356]` |
| DG-124 | large gold halo | 520 px circle → 400 × 115 ellipse above the crown | Y655 → Y243 | `[427,129,826,243]` |
| DG-125 | green laurel | 520 → 240 wide | Y571 → Y332 | `[507,129,746,332]` |
| DG-126 | black curved horns | 500 → 200 wide | Y580 → Y308 | `[527,129,726,308]` |
| DG-127 | silver winged circlet | 520 → 350 wide | Y407 → Y315 | `[452,129,801,315]` |
| DG-128 | silver ornate tiara | 520 → 370 wide | Y444 → Y352 | `[442,129,811,352]` |
| DG-129 | silver drop circlet | 520 → 320 wide, seat 129 → 276 | Y313 → Y388 | `[467,276,786,388]` |
| DG-130 | translucent white veil | 480 → 460 wide, seat 129 → 180 | Y511 → Y545 | `[397,180,856,545]` |
| DG-131 | pale-blue spiked tiara | 520 → 390 wide | Y339 → Y285 | `[432,129,821,285]` |
| DG-132 | gold low circlet | 520 → 320 wide, seat 129 → 240, front arc only | Y279 → Y331 | `[467,252,786,331]` |
| DG-133 | arcane staff | dx +34 to grip `(438,772)`, +12° lean | — | `[278,261,523,1101]` |
| DG-134 | violet orb | dx +34, dy −30 to palm `(438,748)` | — | `[348,518,527,737]` |
| DG-135 | dark wand | dx +34 to grip `(438,772)`, +12° lean | — | `[316,261,506,1049]` |
| DG-136 | silver sword | dx +34 to grip `(438,772)`, +12° lean | — | `[300,142,490,921]` |
| DG-137 | star spellbook | dx +34, dy −25 to palm `(438,748)` | — | `[323,587,552,747]` |

## Automated result

All fifteen pass `python scripts/rig_gate_report.py --trait` and remain inside the locked
bounds `[233,129,1021,1139]`. The head-accessory width ratios moved from 1.13–1.17× the base
body down to 0.70–0.95×, so no accessory is now wider than the character wearing it, and
every head-contact band clears the eyebrow line.

## Seat revision — three designs that still read wrong

Two further passes over the ten, composited against three hair volumes rather than one, caught
five that cleared every measurement and still looked wrong. The lesson is that no measurement
available to the automated gates distinguishes a band worn on a head from a band floating
beside one; only a composite does, and only against varied hair.

**DG-132 gold low circlet — the far side of the ring was drawn in front of the head.** The
generator drew this as a closed ellipse: two strokes in every column, the near one crossing the
forehead and the far one passing behind the skull. Head accessories composite in front of the
hair, so the far stroke was drawn over the head it should be hidden by, and the band read as a
hoop hovering around the character. `keep_front_arc()` in
`scripts/align_pending_candidates.py` keeps only the lowest stroke in each column, which leaves
the near arc and lets it disappear at the temples exactly as a worn band does. It removes
pixels and invents none.

**DG-125 green laurel — the wreath framed the face instead of sitting on the head.** The design
is a U of two branches with the stems crossed at the bottom, and at 310 px the crossing landed
at the mouth with the branches flanking the eyes. At 240 px the crossing sits at the hairline
and the branches arc over the crown, which is how a laurel crown is worn.

**DG-129 silver drop circlet — the arms ended in open air.** Its side arms rise well above the
centre, so at 370 px they swept out past the hair. Narrowing to 240 px kept them inside the
head width but left them unanchored: too thin and too high to touch anything, so the band still
read as a wire floating over the hair. At 320 px seated at Y 276 the arms land on the hair at
the temples and the drop hangs centred on the forehead.

**DG-130 translucent white veil — an arch hanging from a point above the head.** The design is
an inverted U with a narrow apex and two long drapes. Seated at Y 129 the apex sat above the
crown with nothing under it, so the piece read as two curtains either side of the face rather
than a veil. At 460 px seated at Y 180 the arch rests on the crown and the drapes frame the
face.

## Undergarment coverage — the registered base master

The base bodies wear a neutral tank and shorts so the mannequin is never nude, and outfits are
meant to cover it. `scripts/hide_undergarment.py` existed for exactly this and carried a
hardcoded list of five 1:1 base/outfit pairs. Outfits 006–010 were registered later, all bound
to the neutral master, and none was in that list. Four of them left the tank showing:
outfit_007 3569 px, outfit_009 1362 px, outfit_008 749 px, outfit_010 344 px.

The pair list now comes from `config/compatibility.json`, so a newly bound outfit cannot be
missed again, and a base with several outfits is repainted against the union of the gaps they
leave — safe, because a region one outfit exposes is hidden by any outfit that covers it.

Two kinds of exposure turned out to be showing, and only one is fixable by editing pixels.

**Fit gaps — fixed.** Narrow strips where a garment fails to meet the arm or shoulder and a
tank strap shows. They touch genuine skin, so colour diffuses into them cleanly. Both of
outfit_009's shoulder slivers, outfit_010's entire exposure, and outfit_007's side strips are
gone.

**Neckline openings — left alone.** outfit_007's 82 × 77 chest V, outfit_009's 44 × 41 collar,
outfit_008's neck. These are enclosed by more tank rather than skin, so there is nothing to
diffuse from; forcing it produced a blotchy patch in the coat's V and a smear in the collar.
The tank reads there as a linen undershirt. Covering them properly means the outfit carrying
its own inner garment, which is a re-render, not an edit.

| Outfit | Exposed before | After | Outcome |
|---|---:|---:|---|
| `outfit_007_brown_leather_long_coat` | 3569 | 2858 | side strips fixed; chest V left |
| `outfit_008_olive_ragged_cloak` | 749 | 391 | upper gap fixed; enclosed neck opening left |
| `outfit_009_navy_high_collar_coat` | 1362 | 467 | both shoulder slivers fixed; collar V left |
| `outfit_010_celestial_robe_white_gold` | 344 | 0 | fully fixed |

Alpha and every rig anchor are untouched: 1967 RGB pixels changed inside x 543–698, y 500–682,
and the master still passes the full-figure rig gate at top-of-head Y 141, foot baseline
Y 1139 and centre X 627. Only the neutral master was rewritten; the four pose variants gained
nothing and were deliberately left at their existing bytes rather than taking a new SHA-256 for
no visible change.

`tests/test_hide_undergarment.py` now derives its pairs the same way and pins a per-outfit
exposure ceiling, so a new outfit with no recorded ceiling fails until someone measures it.

## Visual evidence

- `head_accessories_approval.png` — ten before/after pairs over the base master with the
  silver hair pair and an outfit.
- `hand_objects_approval.png` — five before/after pairs in the object's own approved pose,
  plus four finished tokens built from the realigned candidates.
- `undergarment_approval.png` — the four affected outfits before and after, each with a marked
  pass showing fit gaps in red and designed neckline openings in amber.

## Disposition — registered 2026-09-07

All fifteen were approved on the sheets above and are registered by
`scripts/register_aligned_candidates.py`, which copies the exact approved bytes into
`assets/`, writes a manifest entry per asset carrying the alignment provenance, flips
DG-123 … DG-137 to `registered`, binds each hand object to the pose it was fitted for, drops
both categories from `pending_categories`, and adds them to `optional_categories`
(`head_accessories` 0.55, `hand_objects` 0.60) so a token without a crown or a prop stays a
normal token.

The library goes from 85 registered assets to **100**, and `head_accessories` and
`hand_objects` are both complete at 10 and 12.

### Verification

| Gate | Result |
|---|---|
| `validate_config.py` | PASS — 100 traits, 30 requires rules |
| `validate_assets.py` | 100 files checked, 0 failed |
| `validate_manifest_consistency.py` | 100 registered assets checked |
| `report_production_status.py --check` | ledger agrees with manifest and backlog |
| `python -m unittest discover -s tests` | 196 passed |
| `generate_777.py --preflight-only` | PASS |

**Supply saturation cleared.** The rule-valid combination space goes from 800 to
**300,478,464**, and saturation from **97% to 0.0%**. Both new categories are optional, so
they multiply the space rather than constraining it. Minting 770 of 800 meant nearly every
legal character existed and rarity carried no information; that is no longer true.

Per-asset composites over the required base are in `docs/qa/composites/`, one per registered
asset, and each manifest entry points at its own.
