# Pending candidate realignment — 2026-09-07

**Categories:** head accessories (DG-123 … DG-132), hand objects (DG-133 … DG-137), plus a
correction to the registered base master's undergarment coverage.
**Scope:** the fifteen candidates remain unregistered review candidates. The one registered
change is `assets/base_bodies/base_body_001_neutral_master.png`, whose manifest entry, SHA-256
and provenance are updated in the same commit. No backlog, ledger, compatibility, metadata,
release, minting or on-chain change has been performed.

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
| DG-125 | green laurel | 520 → 310 wide | Y571 → Y392 | `[472,129,781,392]` |
| DG-126 | black curved horns | 500 → 200 wide | Y580 → Y308 | `[527,129,726,308]` |
| DG-127 | silver winged circlet | 520 → 350 wide | Y407 → Y315 | `[452,129,801,315]` |
| DG-128 | silver ornate tiara | 520 → 370 wide | Y444 → Y352 | `[442,129,811,352]` |
| DG-129 | silver drop circlet | 520 → 370 wide, seat 129 → 180 | Y313 → Y310 | `[442,180,811,310]` |
| DG-130 | translucent white veil | 480 → 420 wide | Y511 → Y462 | `[417,129,836,462]` |
| DG-131 | pale-blue spiked tiara | 520 → 390 wide | Y339 → Y285 | `[432,129,821,285]` |
| DG-132 | gold low circlet | 520 → 360 wide, seat 129 → 200 | Y279 → Y303 | `[447,200,806,303]` |
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

## Disposition

All fifteen are **automated-pass** and are presented for human approval. They remain
unregistered. Registration is a separate explicit step.
