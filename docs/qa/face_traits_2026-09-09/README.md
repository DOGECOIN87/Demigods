# Facial traits — 2026-09-09

The last five pending categories are registered: 24 eye pairs, 16 eyebrow pairs,
12 mouths, 8 expression marks and the rebuilt front aura. All 16 categories are
now complete.

## Why the family is built from the master rather than the sheet

The backlog cites cells of a `FACE` reference sheet for all 60 facial traits. That
sheet exists in this repository only as
`images/reference_sheets/anime_character_creation_asset_sheet.webp`, which is
**128 × 96 px** — a browsing preview, as `images/reference_sheets/index.md` says of
all of them. A 1254 px eye pair cannot be reconstructed from a thumbnail, and
naming the output `eyes_001_sheet_r1c1_dark_neutral.png` would put a provenance
claim in the manifest that the file could not support.

The approved face was used instead, and it is the better source anyway. The base
body is not a blank mannequin: `prompts/16` specifies "large warm-brown eyes,
small nose, and gentle closed-mouth smile", and every registered base has them
painted in. That face is on-model, on-rig, in the locked style, and positioned by
the artist rather than by a placement rule. The backlog rows now carry the real
filenames, and every manifest entry records why the cell reference was dropped.

## Five defects the first build shipped

None of these failed a test. Every one was found by rendering a token at full
size and looking at it, and each measurement below was written afterwards.

1. **The cover patch was visible.** The skin behind a feature was reconstructed by
   an iterated hold-and-blur relaxation — the textbook harmonic fill. Over a band
   as long and thin as the eyebrow it had not converged, so the patch came out
   mottled, and it drifted about 4/255 down in red against the surrounding skin.
   Composited, that is a pale grey crescent on the brow line of every token whose
   eyebrow trait moved the brow off it. It is now a normalized convolution — the
   image and the known-pixel mask each blurred, and their ratio — which is smooth
   by construction and matches the surrounding skin to 0.3/255.
2. **The footprint counted only pixels darker than skin.** That is the brow's ink
   but not the pale highlight the style paints along its upper edge, so the patch
   left the highlight on the face and every mood that moved the brow left a ghost
   of it behind. The footprint is now deviation from the local skin level in
   either direction, which also brings the sclera into the eye footprint.
3. **The brow's difference field included the top of the eye**, which sits inside
   the eyebrow region. Raising the brow painted a second copy of the eyelid line
   eight pixels above the real one. Each separated feature is now confined to its
   own measured footprint.
4. **The iris recolour was clipped to the wrong disc.** It used the iris seed the
   extraction recorded — radius 28.5 at (559, 374) and (694, 374) — which is 5 to
   8 px off centre, so the recolour stopped short of the lash and left a crescent
   of the original brown. Removing the boundary was worse: recolouring everything
   inside the eye tinted the lash flat and threw coloured speckles onto the cheek.
   The disc is now fitted from the art, by least squares through the chords of the
   rows the lash does not cross: (555.0, 378.0, 25.7) and (700.5, 378.4, 25.8).
5. **The ramp desaturated and darkened every colour.** Its light stop was the base
   mixed *with* white, and its base sat at the middle of the luminance range while
   the painted iris's median is near 0.25. `gold` (214, 166, 54) rendered at a mean
   of (131, 107, 51), which reads as olive; `pink` came out dusty mauve. The light
   stop is now the base taken to full value, and the base sits at the iris's own
   median: `gold` renders at (183, 146, 61) and `pink` at (194, 130, 155).

Two more were in the drawn families. Every open mouth had a straight bar across
its top, because the lip was a stroke laid over an unclipped ellipse rather than
the edge of the opening; the opening is now the ellipse below a curved lip, both
built from the same curve. And `small_downturned` was an ellipse, which carries no
direction and read as a plain round mouth; it is a downturned line now.

## The consequence nobody had written down

A face trait does not sit on an empty face. It **replaces** one. A trait smaller
than the baked feature leaves the original showing beside it, and no gate in the
collection could see that: a layer that covers nothing still passes canvas, alpha,
bounds and width-ratio checks.

So every eye, eyebrow and mouth layer carries a feathered skin patch beneath its
art, shaped to the union of where the baked feature lands across **all five**
registered bases. The patch colour is the harmonic reconstruction of the skin
behind the feature, so it is continuous with the cheek and forehead rather than a
flat fill. `tests/test_face_traits.py` measures the coverage on every registered
asset: 0 uncovered pixels required, and 0 measured on all 52.

Expression marks carry no patch. They are additive overlays on skin that is
already there, and a patch on one would erase whatever it sat over — which the
tests also assert.

## How each family varies

**Eyes.** The master's eye pair, separated from the skin it is painted on by
`scripts/extract_face_features.py`, with the iris remapped through a three-stop
ramp. The lash line, sclera and the shared upper-left catchlight are the master's
own, so the pair stays on-model; only the iris body changes colour, and the ramp
keeps the pupil dark and the rim light where the painting put them.

The backlog repeats three adjectives across its rows — "dark neutral" at r1c1 and
r3c1, "charcoal" at r2c7 and r3c7, "black" at r2c8 and r3c8. Shipping two identical
eye pairs under different filenames would be two trait values a holder cannot tell
apart, so the repeats are separated by temperature, and both the palette table and
the shipped pixels are asserted distinct.

**Eyebrows.** The master's brow pair, remapped per column: how high it sits, how
far the inner end lifts or falls, how much of the painted arch is kept, and how
heavy the line is. Two things were needed to make that clean, and both are
recorded because both were failures first:

- The brow's centre line is a weighted cubic fit through the per-column centroids,
  not the centroids themselves. Reading them directly gives a line that jitters by
  a pixel wherever a column carries few faint pixels, and every transform rescales
  about it — so the jitter came out as a comb along the brow.
- The transform runs on the brow's **difference from the skin behind it**, not on
  its separated alpha and colour. Minimum-alpha separation gives a soft edge pixel
  a low alpha against an extreme colour; the pair composites back exactly, but
  resampling the two independently breaks the cancellation, and the first attempt
  hung a cream halo over every brow it moved.

The style also paints a pale warm highlight along the top of each brow. It is light
enough to pass the skin test, so holding it fixed diffused its brightness across
the whole reconstruction and the patch came out lighter than the forehead around
it — visible as a pale crescent wherever the trait's own brow no longer covered it.
Skin near a feature varies smoothly by a few units; the highlight runs 13–17 above.
`known_skin()` excludes that bright tail, which puts the highlight where it belongs:
in the feature that moves with the trait.

**Mouths.** Drawn with soft round brushes in the master's own mouth-line colour,
calibrated to the painted mouth: X 605–650, dropping 7 px from end to centre.
`mouth_001_closed_neutral` is that painted mouth itself rather than a redrawing of
it. Mouths render above the eyes layer, so none may put ink over the eyes; measured
0 on all 12.

**Expression marks.** Drawn accents on the cheeks. Two constraints fix the
placement: `hair_front` renders above expression marks, so anything on the forehead
would be hidden by most of the hair in the collection; and the face narrows fast
below the eyes — X 492–763 at Y 422, X 524–731 at Y 446 — so a mark much outside
these anchors lands on the ear or off the silhouette. The first pass put six of the
eight on the ear.

Expression marks are optional at a rate of 0.3: most faces carry none.

## Evidence

Every base body, one face trait set — the check that the shared layers land the
same way on all five, which is what the pose 005 proportion correction earlier the
same day was for:

![every base](every_base.png)

24 eye pairs:

![eyes](eyes.png)

16 eyebrow pairs:

![eyebrows](eyebrows.png)

12 mouths:

![mouths](mouths.png)

8 expression marks:

![expression marks](expression_marks.png)
