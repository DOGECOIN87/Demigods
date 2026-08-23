# Prompts — Outfit silhouettes DG-250 to DG-259

## The problem these exist to fix

The six registered painted robes (DG-199–204) are **one garment in six
colourways**. Measured as silhouette IoU against each other:

| Pair | Overlap |
|---|---|
| black/gold vs navy/gold star | 0.920 |
| crimson/gold vs purple/black | 0.913 |
| white/gold vs black/gold | 0.910 |
| *least alike:* white/gold vs white/navy star | **0.823** |

Median 0.894. Their width profiles are near-identical row by row — every one is
217–235 px across at Y 560, 359–398 px at Y 740, and flares to a floor-length
skirt. Palette varies; shape does not.

That matters because of what survives to marketplace size.
`scripts/build_token_sheet.py --salience` measures how much swapping one category
moves a 210 px thumbnail: backgrounds 47.1, **outfits 11.8**, hair colour 4.9,
and every one of the 35 face assets under 1. Outfits are the second-strongest
signal in the collection, and right now they contribute six colours rather than
six garments.

**So these ten briefs specify silhouettes, not palettes.** Colour is left loose
on purpose.

## The gate a returned render must clear

`scripts/intake_painted_outfit.py <render> --out <candidate> --pose-report`
reports all of this. A design failing the first four is rejected.

| Check | Requirement | Why |
|---|---|---|
| Canvas | natively 1254 × 1254 | resampling to reach it is a separate waiver |
| Chin clearance | **zero** opaque pixels above Y 486 within X 470–790 | the painted jaw line is at Y 478. Seating a collar at Y 442 swallowed the chin and jaw on all six robes, and because `mouths` composites *after* `outfits`, an open mouth drew half on skin and half on the collar's dark opening |
| Shoulder cover | no bare skin in Y 535–660 | the current robes leave 541–2 804 px there and three of six read as off-shoulder gowns by accident |
| Silhouette | IoU **< 0.75** against every registered outfit | otherwise it is a recolour of something the collection already has |
| Skin contrast | ≥ 70 | the mannequin garment measures 27 and reads as nude at 210 px |
| Bounds | inside X 233–1021, Y 129–1139 | |
| Width | ≤ 1.15× the base body | capes and mantles are `back_accessories`, a separate layer |

## Shared contract

Inherit everything in `prompts/22_outfit_prompts.md` — canvas, lighting, content,
no-background-removal — then add this. Paste it above the per-design block.

```text
Create exactly one isolated Demigods outfit, rendered NATIVELY at exactly 1254 x 1254 pixels, RGBA PNG with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png + docs/rig/rig_guide_1254.png

DO NOT REMOVE A BACKGROUND. Paint onto an empty transparent canvas. Rendering on a backdrop and keying it out leaves the backdrop in the colour channels and produces a grey matte fringe.

FIT to the attached chibi body. It is a large-headed chibi, not a scaled adult: the whole body below the chin is only 606 px tall while the head is 330 px wide. Garment proportions must be rebuilt for that, not shrunk into it.
- the collar, yoke or neckline must not rise above Y 486 anywhere between X 470 and X 790. The chin and jaw sit above that line and must stay visible.
- cover the shoulders completely from Y 535 to Y 660. Bare skin there reads as a hole, not as a design.
- symmetrical about X 627 unless the design is explicitly asymmetric, perfectly front-facing, zero perspective
- clean openings where the neck and hands emerge, with hidden overlap beneath them so no seam shows
- every visible pixel inside X 233-1021 and Y 129-1139
- total width no more than about 1.15x the body width

CONTRAST: clearly separated from skin tone (253,199,163) at THUMBNAIL size, not only at full resolution. No cream, beige, tan or peach fabric as the dominant colour. Give the garment a defined outline and internal value structure so its silhouette reads at 210 px.

SILHOUETTE IS THE POINT. This design must be recognisable from its outline alone, with colour removed. Match the width profile given in the block below within about 15%.

LIGHTING: soft upper-left key at ~45 degrees, lower-right form shadows, subtle cool right rim, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish.

CONTENT: modest clothing only. Opaque fabric throughout. No nudity, lingerie, swimwear, exposed torso or hips, or emphasized anatomical contours.
```

## How to read the width profiles

Total garment width in pixels at each canvas row. The registered robes all run
roughly `230 / 265 / 310 / 370 / 340 / 285 / 390 / 215` across these rows — every
brief below departs from that shape somewhere obvious.

| Row | What it is on the body |
|---|---|
| Y 560 | shoulder line |
| Y 620 | upper arm |
| Y 740 | forearm / widest sleeve |
| Y 808 | waist |
| Y 900 | hip / upper skirt |
| Y 1000 | lower skirt |
| Y 1100 | hem, just above the foot baseline at 1139 |

---

## DG-250 — Fitted longcoat and trousers

The opposite of a robe: a straight, narrow column with no flare at all.

```text
DESIGN: a fitted double-breasted longcoat over straight trousers and low boots. The coat is cut close to the body, buttoned to a low standing collar, and falls dead straight to just below the knee with a single centre vent. Sleeves are narrow and end at the wrist with a plain turned cuff. A slim belt at the waist. Metal buttons in two rows down the chest. Trousers straight, boots flat and short.

SILHOUETTE: narrow and vertical throughout. No skirt flare, no bell sleeve, no mantle.
WIDTH PROFILE: Y560 250, Y620 255, Y740 265, Y808 250, Y900 235, Y1000 225, Y1100 215.
```

## DG-251 — Segmented plate armour

Hard edges and a hard shape. Nothing about this should drape.

```text
DESIGN: articulated plate armour. Broad angular pauldrons sitting proud of the shoulders, a fitted cuirass with a raised centre ridge, a short skirt of overlapping tassets ending mid-thigh, and separate greaves on the lower legs with the knee visible between them. Rivets, edge bevels and a cloth strip hanging at the centre front. Metal, not fabric: hard specular highlights, sharp silhouette corners, no soft folds.

SILHOUETTE: widest at the pauldrons, narrowing sharply at the waist, a short flared tasset skirt, then narrow legs. Two clear horizontal breaks.
WIDTH PROFILE: Y560 310, Y620 285, Y740 250, Y808 265, Y900 290, Y1000 210, Y1100 200.
```

## DG-252 — Layered kimono with wide rectangular sleeves

The one design that may be wider than the robes, because its sleeves are square
rather than flared.

```text
DESIGN: a layered kimono. Two visible collar layers crossing left over right, a broad stiff obi wrapped at the waist with a knot, and large RECTANGULAR hanging sleeves whose lower corners are square, not rounded or bell-shaped. The body of the garment falls as a straight column to the ankle with no flare. A narrow decorative cord across the obi.

SILHOUETTE: a straight vertical column interrupted by two large squared sleeve masses either side. The sleeve bottom edge is horizontal and ends abruptly.
WIDTH PROFILE: Y560 260, Y620 400, Y740 430, Y808 415, Y900 265, Y1000 255, Y1100 250.
```

## DG-253 — Short jacket and belted skirt

Leaves the lower leg bare, which no registered outfit does.

```text
DESIGN: a cropped fitted jacket ending at the waist, worn over a short pleated skirt that stops above the knee. The jacket has a small stand collar, an open front showing a shirt beneath, and short sleeves ending above the elbow. A wide belt with a round clasp at the waist. Knee-high boots with a folded cuff.

SILHOUETTE: the garment STOPS at about Y 950. Bare leg is visible between the skirt hem and the boot tops. Do not extend fabric below Y 970.
WIDTH PROFILE: Y560 255, Y620 270, Y740 250, Y808 270, Y900 320, Y1000 190, Y1100 185.
```

## DG-254 — Sleeveless battle dress with arm wraps

```text
DESIGN: a sleeveless high-necked dress with a broad shoulder yoke that fully covers the shoulders and collarbone, cut away at the upper arm so the arm is bare from the deltoid down. Cloth wraps bound around each forearm from wrist to elbow. A split skirt over fitted leggings, with the front panel shorter than the back. A knotted sash at the waist with hanging ends.

SILHOUETTE: bare upper arms make a clear notch either side between the yoke and the forearm wraps. The skirt splits at the centre front.
WIDTH PROFILE: Y560 265, Y620 225, Y740 300, Y808 275, Y900 305, Y1000 320, Y1100 300.
```

## DG-255 — Hooded travelling cloak over a tunic

```text
DESIGN: a heavy hooded cloak worn over a short tunic and trousers. The hood is DOWN, bunched in folds across the shoulders and upper back — do not draw it over the head, which belongs to a separate layer. The cloak is fastened at the throat with a round clasp and hangs open at the front, revealing the tunic and a belt. Its lower edge is uneven and weighted, widening toward the ground.

SILHOUETTE: a broad triangle widening steadily from shoulder to hem, with a visible vertical gap down the centre front where the cloak parts.
WIDTH PROFILE: Y560 300, Y620 330, Y740 380, Y808 400, Y900 430, Y1000 455, Y1100 440.
```

## DG-256 — Scholar's tabard over a shirt

```text
DESIGN: a flat rectangular tabard hanging front and back from the shoulders, open at both sides so the shirt and belt beneath are visible from the waist down. The tabard carries a bordered central emblem panel. Beneath it, a plain long-sleeved shirt with buttoned cuffs and simple trousers. A cord belt tied over the tabard at the waist.

SILHOUETTE: a narrow flat slab down the centre of the figure with the arms clearly separate from it. The open sides read as two vertical gaps.
WIDTH PROFILE: Y560 245, Y620 265, Y740 275, Y808 245, Y900 235, Y1000 240, Y1100 235.
```

## DG-257 — Tiered ceremonial gown

Wide where the robes are narrow, and narrow where they are wide.

```text
DESIGN: a fitted sleeveless bodice with a high covered neckline and a shoulder yoke, over a gown of three distinct horizontal tiers, each ruffled edge overlapping the one below. Fitted long gloves reaching above the elbow. A jewelled band at the waist marking where bodice meets skirt.

SILHOUETTE: tight from shoulder to waist, then three clear stepped widenings. The tier edges must read as separate horizontal lines, not one smooth cone.
WIDTH PROFILE: Y560 250, Y620 235, Y740 230, Y808 260, Y900 380, Y1000 460, Y1100 500.
```

## DG-258 — Asymmetric monastic wrap

The only asymmetric design in the set. Its outline should be unmistakable.

```text
DESIGN: a single length of heavy cloth wrapped over the viewer-LEFT shoulder and under the viewer-RIGHT arm, leaving the right shoulder and arm covered only by a close-fitting under-layer sleeve. A thick rope sash at the waist with a long knotted tail hanging down the left side. The wrap falls to mid-calf, its diagonal edge crossing the body from left shoulder to right hip. Simple sandals.

SILHOUETTE: DELIBERATELY ASYMMETRIC. The left side carries a heavy fabric mass and the right side is close to the body. The diagonal edge across the chest is the design's signature and must be clearly readable in outline.
WIDTH PROFILE: Y560 270, Y620 300, Y740 320, Y808 330, Y900 315, Y1000 290, Y1100 270.
```

## DG-259 — Panelled bodysuit with a segmented harness

```text
DESIGN: a close-fitting full-body suit with visible panel seams, worn under a segmented harness of straps and small hard plates across the chest and hips. A narrow standing collar. Integrated boots with a hard sole line. Thin luminous piping following the panel seams. No skirt, no cape, no loose fabric anywhere.

SILHOUETTE: the narrowest design in the set — it follows the body almost exactly. Its identity comes from internal panel lines and harness plates rather than from outline mass.
WIDTH PROFILE: Y560 240, Y620 245, Y740 250, Y808 230, Y900 215, Y1000 205, Y1100 200.
```

---

## Intake

```bash
python scripts/intake_painted_outfit.py <render> \
  --out images/trait_candidates/outfits/<name>.png --pose-report
python scripts/rig_gate_report.py --trait <candidate> --min-skin-contrast 70 --max-width-ratio 1.15
```

The intake script prints `collar over the chin` (must be 0), `bare shoulder
pixels`, and `closest registered silhouette` with a DISTINCT / TOO SIMILAR
verdict at the 0.75 threshold. It also fits the render to the rig, so a returned
image that is close but not exactly seated is still usable.

## One thing these briefs cannot fix

An outfit composites *over* the base body, so its sleeves replace whatever the
arms were doing. Each of these bakes in one arm position, which is why
`prompts/23_per_pose_outfit_variants.md` exists. Keep sleeves ending at the wrist
with the hands clearly outside the garment; a bell cuff that swallows the hand
makes the pose variants worse.
