# QA — Interim procedural outfits DG-164 to DG-168 (2026-07-27)

Five outfits registered, clearing the release blocker. **These are interim placeholders**, not the painted outfit set.

## What they are

One high-collar long coat in five palettes, built by `scripts/build_outfit.py` from the registered base body. The garment silhouette comes from a profile table measured against the body; the sleeves are the body's own upper-arm alpha, stopping above the hands so hands stay bare skin; the skirt extends past the body into a flared hem.

Shading is the part that makes this work. Procedural clothing usually fails because its lighting does not match the character. Here the fabric luminance is taken from the **base body's own luminance** wherever the garment overlaps it, blended 0.72 with synthesised folds, so the upper-left key light and lower-right form shadows are inherited rather than re-invented. Beyond the body the folds carry the same value structure into the skirt.

## Gate results

All five pass `--trait --max-width-ratio 1.15 --min-skin-contrast 70`:

| ID | Palette | Skin contrast | Width ratio | Bounds |
|---|---|---|---|---|
| DG-164 | navy | 240.4 | 0.87 × | `[435,495,818,1107]` |
| DG-165 | black | 270.7 | 0.87 × | identical |
| DG-166 | plum | 205.5 | 0.87 × | identical |
| DG-167 | oxblood | 221.9 | 0.87 × | identical |
| DG-168 | olive | 190.3 | 0.87 × | identical |

Against a floor of 70 and the mannequin garment's 27, all five clear the tone that caused the blocker by a wide margin. Bounds are identical because only the palette differs.

## Two rejected iterations

The first two builds left **bare shoulders** — a skin strip between the neckline and the sleeve tops, which is the same skin-exposure failure in miniature.

1. The collar profile was 74 px half-width against a body 118 px half-width at that Y, so the garment simply did not reach the shoulders.
2. Widening the collar was not enough: the garment started at Y 552 while the body's shoulder slope begins around Y 500, leaving the upper chest bare.

Fixed by moving `COLLAR_Y` to 498, shaping the profile to follow the shoulder slope, and starting the sleeve union at the collar rather than below it.

## Thumbnail verification

The test this category exists to pass. Composited at 210 px the figure reads unambiguously as clothed — see `docs/qa/composites/sheet_100_clothed_2026-07-27.png` against the earlier `sheet_100_tokens_graded_2026-07-27.png`.

## Generation

```
generate_777.py --preflight-only    Preflight passed. Combination space: 4800
generate_777.py --dry-run           777 unique tokens, provenance 4e8b91a0
validate_output.py --allow-dry-run  PASS, 777/777 metadata, 777 signatures
```

## Honest limitations

These are simpler than the base body art: flat fabric, minimal fold structure, a plain tapered skirt, a mechanical centre placket. They read as competent game-asset robes, not as painted anime costume.

They also do **not** correspond to any cell in the `OUTFIT` sheet — no hood, no split cape tail, no ragged hem, no armour. DG-037 to DG-046 remain `pending` and are not satisfied by these. Numbering starts at `outfit_011` so 001–010 stay reserved for the painted designs.

**Replace these, do not build on them.** They exist so the collection can render while the painted outfits are produced.
