# Pending candidate realignment — 2026-09-07

**Categories:** head accessories (DG-123 … DG-132), hand objects (DG-133 … DG-137)
**Scope:** unregistered review candidates only. No manifest, backlog, ledger, compatibility,
metadata, release, minting, or on-chain change has been performed.

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

| ID | Asset | Change | New bounds |
|---|---|---|---|
| DG-123 | gold pointed crown | 520 → 400 wide, seat 129 → 132 | `[427,132,826,408]` |
| DG-124 | large gold halo | 520 px circle → 430 × 130 ellipse above the crown | `[412,132,841,261]` |
| DG-125 | green laurel | 520 → 450 wide, seat 129 → 132 | `[402,132,851,514]` |
| DG-126 | black curved horns | 500 → 440 wide | `[407,129,846,525]` |
| DG-127 | silver winged circlet | 520 → 420 wide | `[417,129,836,352]` |
| DG-128 | silver ornate tiara | 520 → 450 wide | `[402,129,851,400]` |
| DG-129 | silver drop circlet | 520 → 440 wide, seat 129 → 215 | `[407,215,846,369]` |
| DG-130 | translucent white veil | unchanged — already seated | `[387,129,866,510]` |
| DG-131 | pale-blue spiked tiara | 520 → 470 wide | `[392,129,861,318]` |
| DG-132 | gold low circlet | 520 → 430 wide, seat 129 → 240 | `[412,240,841,363]` |
| DG-133 | arcane staff | dx +34 to grip `(438,772)`, +12° lean | `[278,261,523,1101]` |
| DG-134 | violet orb | dx +34, dy −30 to palm `(438,748)` | `[348,518,527,737]` |
| DG-135 | dark wand | dx +34 to grip `(438,772)`, +12° lean | `[316,261,506,1049]` |
| DG-136 | silver sword | dx +34 to grip `(438,772)`, +12° lean | `[300,142,490,921]` |
| DG-137 | star spellbook | dx +34, dy −25 to palm `(438,748)` | `[323,587,552,747]` |

## Automated result

All fifteen pass `python scripts/rig_gate_report.py --trait` and remain inside the locked
bounds `[233,129,1021,1139]`. The head-accessory width ratios moved from 1.13–1.17× the base
body down to 0.90–1.08×, so no accessory is now wider than the character wearing it.

## Visual evidence

- `head_accessories_approval.png` — ten before/after pairs over the base master with the
  silver hair pair and an outfit.
- `hand_objects_approval.png` — five before/after pairs in the object's own approved pose,
  plus four finished tokens built from the realigned candidates.

## Disposition

All fifteen are **automated-pass** and are presented for human approval. They remain
unregistered. Registration is a separate explicit step.
