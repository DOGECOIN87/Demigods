# QA — DG-154 ice crystal ring, procedural route attempted and rejected

Date: 2026-07-29
Backlog row: DG-154 (`aura_rear_014_ice_crystal_ring.png`) — remains `pending`
Evidence: `docs/qa/aura_ice_ring_procedural_rejected_2026-07-29.png`

## Why it was attempted

Four ring-family auras are registered and every one of them was rendered
analytically by `build_aura_floor_ring.py`. That works because a glowing band
*is* a signed distance function — the maths and the design are the same object.

Six ring cells remain (fire, lightning, violet flame, ice crystal, smoke void,
water splash). Of those, ice looked like the one that stays honestly geometric:
the reference cell is a ring of faceted shards, and a faceted shard is a polygon.
If any textured cell could be rendered in-repo without an image generator, it was
this one — so it was built as that family's representative test.

## What was built

A supersampled polygon renderer sharing the neon family's exact seating and
ellipse radii, so the ring would keep the family footprint:

- 34→42 tapered shards placed on the ellipse from a fixed seed (a procedural
  asset that differs per run is not reproducible)
- painter-ordered far-to-near so shards overlap correctly
- perspective scaling so near-side shards read larger
- a soft base glow along the ellipse to seat them on the ground
- **v2 additionally**: per-shard vertical gradients masked by each silhouette
  (dense base, translucent tip), wider height variance, and cool facet edges

Both versions pass every automated gate: native canvas, genuine transparency,
`--floor-aura` bounds, centre X within 1 px of the locked 627.

## Why it was rejected

Passing the gates is not the bar. The gates measure geometry and alpha; they
cannot see that the result looks wrong.

Both versions read as **flat pale triangles — a picket fence or paper bunting —
not faceted ice**. The v2 gradients and variance improved it marginally and did
not change the category of the problem. Composited beside the registered
`aura_rear_001_blue_floor_ring`, the difference is not subtle: the neon ring is
polished and integrated into the scene, and the shard ring reads as clip art
dropped on top.

The underlying reason is worth recording, because it predicts the other five
cells. The neon rings succeed because a soft glow is *fully described* by
distance and falloff — there is no residual detail the maths omits. A crystal is
not: its read comes from internal refraction, facet-to-facet value shifts, and
specular breakup, none of which are functions of the outline. Rendering the
outline correctly still leaves the part that makes it look like ice unrendered.

## Consequence

DG-154 stays `pending` and stays routed to an image generator under
`prompts/19`, together with DG-151 (fire), DG-152 (lightning), DG-153 (violet
flame), DG-155 (smoke void), and DG-157 (water splash). If ice — the most
geometric of the six — does not clear the bar procedurally, turbulent smoke and a
water splash will not either.

The builder script was removed rather than kept. It produced output that passes
every automated check while being visibly below the collection's standard, and
leaving it in the repository would invite exactly that mistake. The approach and
the comparison image are retained here so the route is not retried blind.

## Note for the ledger

No asset was registered and no backlog status changed. This document records a
rejected production route, not a rejected candidate binary.
