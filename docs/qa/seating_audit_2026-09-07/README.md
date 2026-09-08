# Full seating audit — 2026-09-07

Every registered trait category composited over the base body and inspected for
whether it sits on the anatomy it attaches to. Two categories were wrong. Both had
the defect the head accessories had, from the same cause and invisible to the same
gates.

## What the automated gates cannot see

Canvas size, alpha behaviour, maximum bounds and width ratio are all satisfied by
a layer sitting in completely the wrong place. A choker halfway down the chest and
a wing pair tucked behind the shoulders pass every one of them. Every asset fixed
here was `production_ready` and had passed a recorded visual review.

The sweep that found them measures each layer against the base body's measured
anatomy rather than against the canvas.

## Neck accessories — all eight seated on the chest

`scripts/refit_neck_accessories_batch.py` refit the whole category to `top_y`
545–555 at a uniform 0.45 scale. The base body's throat is Y 465–505, so every
piece sat 50–90 px below where it attaches: the chokers read as chest straps and
every pendant chain began below the collarbone with nothing holding it up.

Each is now re-derived from its immutable source with its clasp in the throat
band. `neck_accessory_005`'s long pendant keeps its longer drop.

| Asset | Top before | Top after |
|---|---:|---:|
| 001 black choker | Y555 | Y482 |
| 002 gold blue drop choker | Y550 | Y482 |
| 003 black ribbon bow | Y550 | Y482 |
| 004 silver dark round pendant | Y550 | Y482 |
| 005 silver navy long pendant | Y545 | Y478 |
| 006 silver pale circle charm | Y550 | Y482 |
| 007 gold teardrop pendant | Y550 | Y482 |
| 008 violet ribbon bow | Y550 | Y482 |

## Back accessories — six wing pairs too small and seated at the jaw

All eight were normalized at 590 px wide with `top_y` 420. On a 443 px body that
is 74 px of overhang a side, and seated at the jaw the upper half hid behind the
head and hair — so every pair read as small fins at the shoulders rather than
wings. Between 41% and 45% of each layer was occluded.

The six wing designs now span 760 px, 158 px of overhang a side, each seated so
the pair's centre sits at the upper back. The two capes are unchanged: they
already hang from the shoulder to the hem, and widening them would push the hem
past the locked foot baseline. Re-running the transform on them reproduced their
registered bytes exactly, which confirms the pipeline is faithful.

## Categories checked and found correct

- **Hair front** — the bangs cross the eye regions on most designs, which is what
  bangs do; the eyes read clearly under every one. No change.
- **Hand objects** — all twelve sit on their measured grip contact in their bound
  pose. No change.
- **Outfits** — all ten cover the base body's undergarment except the neckline
  openings recorded in `docs/qa/aligned_candidates_2026-09-07/`.
- **Rear and front auras, backgrounds, global finish** — the sweep's face-occlusion
  hits are all on layers that composite *behind* the base body, so they cannot
  occlude anything.

## Gates added

`tests/test_trait_seating.py` encodes the anatomy so a future batch cannot repeat
this silently:

- every neck accessory's topmost ink falls in the throat band Y 465–515;
- every wing pair clears the body silhouette by at least 120 px on both sides;
- both capes start at or above the shoulder line and hang to between Y 1000 and
  the foot baseline.

With `tests/test_face_occlusion.py` from the previous pass, the three categories
that shipped mis-seated are now all gated by measurement rather than by review.

## Verification

100 assets validate, manifest consistency passes, the ledger agrees, and 201 tests
pass.
