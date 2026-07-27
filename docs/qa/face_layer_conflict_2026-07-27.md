# QA — Face-layer architectural conflict (2026-07-27)

**Blocks 52 backlog assets: eyes (24), eyebrows (16), mouths (12).** Needs a decision before any of them is produced.

## The conflict

The registered base master has a **fully painted face**: brown eyes with lashes, outline, sclera and catchlights; brown eyebrows; a smile; blush; nose; ears.

The layer stack composites face categories *over* the base body:

```
hair_back (04) → base_bodies (05) → outfits (06) → neck (07)
→ eyes (08) → eyebrows (09) → mouths (10) → expression_marks (11)
```

So an eye layer must **fully occlude** the baked eye or the two features stack. Measured footprints of the baked ink:

| Feature | Extent | Size |
|---|---|---|
| Left eye | `(490,339)–(583,419)` | 94 × 81 px |
| Right eye | `(669,339)–(769,419)` | 101 × 81 px |
| Eyebrow pair | `(517,312)–(737,339)` | 221 × 28 px |

## Why neither option works as specified

Demonstrated in `docs/qa/composites/face_layer_conflict_2026-07-27.png`.

**Isolation-compliant layer** — the repository rule for this category is *"eye artwork only at eye line Y 367; no face, eyebrows, hair, or expression marks."* A layer obeying that rule leaves the baked lashes, eye outline and sclera visible around the new iris. The result reads as a defect, not a trait.

**Occluding layer** — covering the full 94 × 81 footprint requires skin-toned padding, which makes the layer partly *face*, contradicting the isolation rule. It also has to match the base skin exactly at every edge; the demo shows visible patch boundaries where it does not.

The same applies to eyebrows and mouths, which are thinner but equally baked in.

Note this is **not** the situation with hair. The base body is deliberately bald, so `hair_back` and `hair_front` composite cleanly. The face was not given the same treatment.

## Options

**1. Render a faceless base master.** Architecturally correct and consistent with the bald scalp: the base carries skin, nose, ears and blush but no eyes, brows or mouth, and the face categories supply them. Cost: a new master render plus all four pose variants, re-approval and re-registration of five assets, and every existing composite QA artefact regenerated. Everything downstream already fits, since the rig does not change.

**2. Accept occluding face layers.** Each of the 52 assets carries skin padding sized to its baked feature. Cheaper up front, but every layer is then coupled to the exact base skin tone and shading, so a future base re-render invalidates all 52. It also weakens the isolation rule that keeps categories independent.

**3. Drop the three face categories.** Remove 52 assets from the backlog and accept one face for the collection, with `expression_marks` carrying facial variety. Cheapest, and the combination space is already 38400 against a 777 supply — these categories are not needed for capacity, only for variety.

## Recommendation

**Option 1 if the collection is meant to have varied faces; option 3 if not.** Option 2 trades a small saving now for coupling 52 assets to a file that may well be re-rendered later.

Option 3 is defensible: the face reads at full resolution but barely at 210 px thumbnail, where silhouette, hair colour and outfit colour do the work. Option 1 is the right call only if faces matter at full-resolution viewing.

Nothing should be produced for `eyes`, `eyebrows` or `mouths` until this is decided.
