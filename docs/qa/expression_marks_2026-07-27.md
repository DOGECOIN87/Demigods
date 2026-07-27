# QA — Expression marks DG-107 to DG-114 (2026-07-27)

Eight glyphs registered, completing the `expression_marks` category and unblocking exact-777 generation.

## Why these were built procedurally

Expression marks are flat anime emote glyphs — blush strokes, a sweat drop, an anger vein, a sparkle — not painted artwork. At this size an image generator produces blurry, inconsistent symbols; primitives drawn at 4× and downsampled give exact rig placement and clean edges. This is the right tool for the job rather than a compromise.

Provenance is `procedural_vector_render` with `scripts/build_expression_marks.py` recorded as the generator.

## Gate results

All eight pass `rig_gate_report.py --trait`: 1254 × 1254 canvas, genuine transparency, inside the locked bounds `[233,129,1021,1139]`.

| ID | Glyph | Visible bounds |
|---|---|---|
| DG-107 | Pink blush strokes, both cheeks | `[451,390,802,440]` |
| DG-108 | Yellow-green stress slashes | `[731,190,852,313]` |
| DG-109 | Dark vertical gloom lines | `[552,165,702,298]` |
| DG-110 | Gold four-point sparkle | `[396,140,575,319]` |
| DG-111 | Cyan sweat drop | `[751,196,844,350]` |
| DG-112 | Pink anger vein | `[720,168,855,303]` |
| DG-113 | Yellow-green emphasis tile | `[442,206,530,294]` |
| DG-114 | Pink curved motion mark | `[698,139,834,196]` |

Two needed their anchors lowered: the sparkle and the curved mark first rendered at Y 124 and Y 126, above the locked top bound of 129.

## Visual review and revision

First pass produced four glyphs that read correctly (blush, gloom lines, sparkle, sweat drop) and four that did not:

- **DG-112** was a plain rejection X rather than the four-lobed anime anger vein, and too large. Redrawn as four tapered lobes meeting at a central knot, at 150 px instead of 180.
- **DG-108** was a scattered radial burst that read as noise. Redrawn as three parallel slashes, the standard annoyance glyph.
- **DG-114** was a hairline arc, too thin to register. Stroke width roughly doubled.
- **DG-113** was a flat rectangle. Given a lighter inner tile so it reads as a designed shine block.

Composite: `docs/qa/composites/expression_marks_over_face_2026-07-27.png`.

DG-113 remains the weakest of the eight. The reference cell genuinely is a plain yellow-green square, so the render is faithful to source, but a square floating beside the head is a weak design. Worth revisiting if a clearer reference appears — it is faithful, not good.

## Reference limits

The `FACE` sheet is 128 × 96, so each expression-mark cell is roughly 15 × 13 px. Cells 1, 3, 4 and 5 are unambiguous. Cells 2, 6, 7 and 8 were interpreted using standard anime emote conventions, since the preview cannot resolve their detail. That interpretation is recorded here rather than presented as certainty.

## Generation unblocked

The collection space is the product of non-empty category counts, and only `backgrounds` and `base_bodies` are required — but every populated category is mandatory per token, so each one multiplies the space:

```
before: 4 backgrounds x 6 rear_auras x 1 hair_back x 5 base_bodies      = 120
after:  4 x 6 x 1 x 5 x 8 expression_marks                             = 960
```

960 clears the 777 supply, so the generator now runs:

```
python scripts/generate_777.py --preflight-only
Preflight passed. Theoretical combination space: 960.

python scripts/generate_777.py --seed 20260727 --dry-run --output <dir>
Complete: 777 unique tokens.
Trait provenance: 915fadf1da762e8e0c14d790980f3749444957bad5318ad173772a34c984e535

python scripts/validate_output.py <dir> --allow-dry-run
PASS generated collection output
Metadata: 777/777; images: 0/777; unique signatures: 777.
```

777 unique signatures with no duplicates, independently verified.

**This does not mean the collection is finished.** It means the pipeline is proven and a renderable collection now exists. Every token currently draws from 5 categories; the remaining 132 backlog assets add variety, not capability. The seed above is a dry-run seed, not the final one — choosing that is a release decision.
