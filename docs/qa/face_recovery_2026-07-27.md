# QA — Face recovery and recolours (2026-07-27)

Follows `face_layer_conflict_2026-07-27.md`. Erasing the baked face left the
collection with no face at all, which is worse than the conflict it fixed. The
erased artwork is the approved design, so it was recovered as trait layers
rather than redrawn.

Registered: 13 eyes, 9 eyebrows, 1 mouth (DG-176 to DG-198). Combination space
38400 → 4492800.

- Recolour sheet: `composites/face_recolours_2026-07-27.png`
- Thumbnails over real backgrounds: `composites/face_tokens_thumbnail_2026-07-27.png`

## Recovery is a matte, not a cut-out

The faceless base is a measured reconstruction of the skin behind each feature,
so for every pixel the original is that feature composited over that skin.
Solving the composite recovers coverage and colour:

    alpha  = clamp(distance(original, skin) / 42)
    colour = skin + (original - skin) / max(alpha, 0.30)

Two checks say the matte is real rather than a luminance key:

| Check | Result |
|---|---|
| Round trip — three layers recomposited over the faceless base vs the original | worst channel error **5** |
| Fringe luminance vs alpha, over 3256 partial-alpha pixels | correlation **−0.22** |

The second is the one that matters. A layer keyed from black has luminance
tracking alpha near +1, which is the failure the repository's matte-contamination
check exists to catch. A negative correlation is expected here and confirms the
opposite: low-alpha pixels sit on the light eyelid highlight, high-alpha on the
dark lashes.

The `max(alpha, 0.30)` floor in the colour solve is not cosmetic. Un-premultiplying
divides by coverage, so at 4% coverage a one-level rounding difference becomes a
25-level colour swing. That was invisible while the layer stayed brown and turned
into a dashed rainbow along every eye's top edge the moment it was recoloured.
Alpha still carries the true value, so the edge is as soft as it was painted.

## Recolour holds value and alpha

Hue and saturation move; value and alpha do not, so every gradient, the pupil,
the lash weight and the upper-left key light survive. Three things are held out,
and each needed a different test:

| Held out | Test | Why not something simpler |
|---|---|---|
| Sclera, catchlights | bright and near-neutral | — |
| Eyelid highlight | close to the skin plate behind it | it is a warm tan at saturation 0.38, so a saturation threshold lets it through and a cyan variant grows a cyan eyelid |
| Socket shading | outside the eye opening | it is *also* a warm tan, and so is the lower iris highlight, so colour alone cannot separate them; the opening is found as the row-span of the definite ink |

Partial recolour is mixed in RGB, not in hue. Interpolating the hue angle from
brown toward magenta sweeps intermediate pixels through green and blue, which is
what put the rainbow on the eye edge even after the coverage floor was added.

## Contrast against the backgrounds

Measured, not judged by eye — `build_face_recolours.py --check-contrast`.

RGB distance to the backgrounds was tried first and is the wrong measure: the
iris body and the backgrounds behind the head are both mid-dark, so every
palette scored "close", including ones that obviously read. The iris never sits
against the background anyway — it sits on skin. What actually goes wrong at
thumbnail size is hue camouflage, so the gate is hue separation.

Backgrounds sampled behind the head, saturation-weighted:

| Background | Dominant hue |
|---|---|
| 001 celestial throne hall | 14° |
| 003 arcane library | 220° |
| 002 violet gothic sanctum | 243° |
| 004 crescent star dreamscape | 253° |

Requiring 40° of clearance from all four rules out blue and violet irises, not
warm ones — which is the opposite of the intuition, and the reason to measure.
What survives is the greens through teals (76–176°) and the magentas (300–332°),
plus gold at 58° and two neutrals exempt from the hue rule. Every palette clears
the skin-distance floor by a wide margin: 128–208 against a floor of 70.

Add a background in a new hue band and the check will name the palettes it
breaks.

## Known limits

These are **13 eye colours and one eye design**. The 24 `FACE` sheet eye cells,
16 eyebrow cells and 12 mouth cells are distinct paintings; DG-055 to DG-106 stay
pending and are not satisfied by this work.

`mouths` holds a single asset, so every token currently shares one mouth. It is
small enough not to read at 210 px, which is why it was not worth recolouring,
but it is the thinnest category in the collection.
