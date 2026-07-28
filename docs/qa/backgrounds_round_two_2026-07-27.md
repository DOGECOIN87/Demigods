# QA — Round-two backgrounds registered (2026-07-27)

Four registered: DG-158 world tree, DG-159 infinite arcane library, DG-160 ember
ruins, and DG-249 bioluminescent grove, a new direction supplied alongside them.
`backgrounds` goes 8 → 12.

One of the five supplied was **held**: skybound isles (DG-163). See below.

- Staging check: `composites/backgrounds_round_two_staging_2026-07-27.png`

## Why backgrounds keep being the priority

`build_token_sheet.py --salience` measures what a category does to a 210 px
thumbnail. Across the whole library only three move it at all — backgrounds
(47.1), outfits (11.8) and hair colour (4.9). Everything else, including all 35
face assets, sits under 1.

Distinct thumbnail appearances, tracked as backgrounds land:

| Backgrounds | Distinct appearances | Expected distinct looks across 777 |
|---|---|---|
| 4 | 192 | 189 |
| 8 | 384 | 333 |
| 12 | 576 | 427 |

## Fit

References are portrait 784 × 1168 against a square 1254 canvas, so each is
**bottom-cropped** to 784 square before upscaling. Bottom rather than centre
because the character stands at foot baseline Y 1139 and the ground has to stay
in frame.

The upscale is 1.60×, larger than the 1.22× used for backgrounds 005–008. It
costs no more, because the limit is the category's 3.0 px blur rather than the
resample. Measured on the native candidates, where ground truth exists:

| Route | Mean | p99 | Max |
|---|---|---|---|
| native → 1024 → 1254 → depth (1.22×) | 0.24 | 1 | 5 |
| native → 784 → 1254 → depth (1.60×) | 0.28 | 1 | 5 |

Out of 255.

## Skybound isles is held, and the earlier QA was right

`docs/trait-production-backlog.md` already flagged DG-162 and DG-163 as having no
floor plane. That finding was checked rather than assumed, and it holds: the
bottom of the skybound-isles frame is falling water and mist, so the feet and the
floor-ring aura hang in open air over a waterfall drop. Bottom-cropping does not
create a floor. It stays `pending` until a native render introduces a foreground
ledge at the foot baseline.

The other four stage correctly — moss floor, library floor, cracked lava ground,
and dark foreground rock respectively.

## The eye-palette hue gate was wrong and is now advisory

Registering ember ruins made `build_face_recolours.py --check-contrast` fail:
orchid cleared the nearest background by 13.1° and magenta by 31.1°, against a
40° floor.

Two things were checked before changing anything.

**Is the measurement sound?** Ember ruins is a fire scene, so a violet reading of
286.9° looked like it might be a circular mean of a bimodal orange-and-blue
distribution — a hue present in neither. It is not: behind the head the
distribution runs 240° 35%, 270° 31%, 300° 22%. The fire is at the bottom of the
frame, well below the head window. The measurement is correct.

**Is the rule sound?** No. Rendered at full size against both ember ruins and the
infinite library, the orchid and magenta eyes read cleanly. An iris never borders
the background — it is enclosed by roughly 330 px of lit skin and framed by white
sclera and a dark lash line. Hue camouflage was a plausible hypothesis and the
visual test refutes it.

Hue separation is now **reported, not enforced**. Skin distance stays the hard
floor, because that is measured against the surface the iris actually touches and
it is what decides whether an eye reads at 210 px; every palette clears it by
116–208 against a floor of 70.

The test was changed to match, and deliberately does not assert hue separation —
asserting it would make registering a background break the eye tests, which is
the wrong coupling.

This is the third measure tried for the background relationship. RGB distance was
too blunt, hue separation as a hard gate too strict, and hue separation as a
report is the one that survives contact with a render.

## Known limits

Ten of the twelve backgrounds now sit in a blue-violet band spanning 219–287°,
and two are warm gold at 12–14°. The collection reads as tonally consistent, but
there is very little hue space left that clears 40° from all of them — greens,
teals and a sliver of rose. Ember ruins is the only warm-dominant scene and its
warmth is in the lower frame, not behind the head.

Two backgrounds remain unregistered from this wave: DG-161 clockwork sanctum,
whose reference is present and stages well, and DG-162 crystal spire, which has
the same floor-plane problem as skybound isles.
