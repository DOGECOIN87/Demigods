# QA — Cross-category composite stress test (2026-07-27)

Workflow step 5. Every registered background composited with every registered rear aura, plus the registered hair-back and the base master, in canonical layer order: background → rear aura → hair back → base body.

Artifacts: `docs/qa/composites/cross_category_stress_2026-07-27.png`, `docs/qa/composites/hair_back_003_proportion_review.png`.

## Generator preflight

```
python scripts/generate_777.py --preflight-only
ERROR: theoretical combination space is only 120; at least 777 are required
```

120 = 4 backgrounds × 5 base bodies × 6 rear auras × 1 hair back. Expected at this stage and not a defect; it is the concrete distance to a renderable collection. Adding a single 8-member category multiplies the space by 8, so the gap closes quickly once outfits, eyes, and hair front land.

## Finding 1 — hair_back_003 reads as wings, not rear hair (needs review)

The registered hair-back asset is clean in isolation but disproportionate over the base body.

| Measure | Value |
|---|---|
| Hair width | 648 px |
| Body width | 443 px |
| Ratio | **1.46 ×** |
| Hair pixels outside the body silhouette | **69.7%** |
| Bald scalp above the hairline | 39 px (hair top Y 180, head top Y 141) |
| Hair bottom | Y 879 |

At 1.46 × the body width, the mass flares well outside the shoulders and arms and hangs to the waist, so in composite it reads as two detached side masses rather than hair falling behind the head. Nearly 70% of it never overlaps the body.

Two caveats before treating this as a defect:

- The **bald crown is expected** for a rear-hair layer in isolation. `hair_back` sits behind the head, so the scalp is covered by `hair_front` (DG-115–122), which is not yet produced. This part will likely resolve on its own.
- The **width will not resolve on its own.** No front layer narrows a rear silhouette.

The asset passed its `--trait` gate and its original base composite, because both check canvas, transparency, and bounds — none of which measure proportion against the body. This is a gap in the automated gate, not a missed step: silhouette proportion is a manual judgement the gate does not attempt.

**Recommendation:** hold `hair_back_003` for human review before any further hair-back colour is produced against it. It is the category's representative test, so all seven remaining colours would inherit its proportions. If the width is wrong, catching it now costs one asset; catching it after DG-029–036 costs eight.

No de-registration is proposed here — that is a maintainer decision.

## Finding 2 — aura_rear_006 gold radiance is near-invisible in composite

The soft gold glow is legible in isolation but nearly disappears once a background and the body are composited over it, on all four backgrounds including the dark arcane library. It survives best on background 004.

This is a consequence of its own design brief — peak alpha 175 with a wide falloff, deliberately soft so the body stays readable — but the current balance may be too far toward invisible to justify a distinct trait slot. Tunable without re-rendering the concept:

```bash
python scripts/build_aura_radiance.py --peak-alpha 210 --falloff 1.2
```

Flagged for maintainer judgement rather than changed unilaterally, since it is already registered.

## Finding 3 — floor rings composite cleanly on all four backgrounds

No collision, clipping, or layer-order defect. The near arc passing below the foot baseline reads correctly against all four floors, including the raised platform of background 004, where the ring sits on the platform surface rather than floating past its edge.

Background 003 carries its own painted floor circle and background 004 a gold circular motif; the registered rings overlay both without visual conflict. No compatibility exclusion is required.

## Verification

- 65 tests pass
- Manifest consistency PASS at 16 registered assets
- Ledger check PASS
