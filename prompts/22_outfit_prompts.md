# Prompts — Outfits DG-037 to DG-046

`outfits` is a **release blocker**, not just the next category. It is in `generate_777.REQUIRED_CATEGORIES`, so preflight fails until it is populated.

## Why this category blocks release

The base bodies wear a mannequin garment whose colour sits within ~20 RGB units of skin:

| Sample | RGB |
|---|---|
| Tank top | `(252, 218, 182)` |
| Shorts | `(247, 211, 174)` |
| Cheek skin | `(253, 199, 163)` |

At full resolution the garment reads fine. At marketplace thumbnail size the contrast disappears and the chibi figures read as unclothed — see `docs/qa/composites/sheet_100_tokens_graded_2026-07-27.png`. The background colour grade made it more obvious, because raising foreground contrast raises the contrast of bare skin too.

The mannequin is allowed this ambiguity only because an outfit always covers it. So **every outfit must clear the skin tone by a wide margin**, and the gate now measures it:

```bash
python scripts/rig_gate_report.py --trait <file> --max-width-ratio 1.15 --min-skin-contrast 70
```

`skin_contrast` is the mean RGB distance of the layer's opaque pixels from `(253,199,163)`. The mannequin garment measures **27**. A navy robe measures **274**. Anything under 70 will read as skin at small size and is rejected.

All ten designs in the `OUTFIT` sheet are floor-length robes and coats, so full coverage is inherent to the set — but a pale cream robe still needs enough value separation and outline strength to survive at 210 px.

## Shared contract

Every prompt below inherits this. Paste it above the per-outfit block.

```text
Create exactly one isolated Demigods outfit, rendered NATIVELY at exactly 1254 x 1254 pixels, RGBA PNG with genuine transparent alpha.

ATTACH: assets/base_bodies/base_body_001_neutral_master.png (fit reference) + docs/rig/rig_guide_1254.png

CANVAS — a 1024 x 1024 result is an automatic rejection:
- exactly 1254 x 1254, generated natively at that size
- never upscale, downscale, or resample to reach 1254 x 1254

DO NOT REMOVE A BACKGROUND. Paint directly onto an empty transparent canvas. Do not render on a backdrop and key it out — that leaves the backdrop in the colour channels and produces a gray matte fringe, an automatic rejection.

FIT — match the attached base body exactly:
- neck opening at the collar, shoulders at Y 569, waist centre X 627 Y 808
- hem clear of foot baseline Y 1139; bare feet and ankles may show below it
- clean openings where head, neck and hands emerge, matching the base silhouette
- hidden overlap beneath the neck and hand openings so no seam shows when those layers composite over it
- every visible pixel inside X 233-1021 and Y 129-1139
- symmetrical about X 627, perfectly front-facing, zero perspective

CONTRAST — the single most important requirement:
- the garment must be clearly distinguishable from skin tone (253,199,163) at THUMBNAIL size, not only at full resolution
- no cream, beige, tan, peach, or unsaturated flesh-adjacent fabric
- give the garment a defined outline and internal value structure so its silhouette reads at 210 px
- pale designs must carry cool shadow and a distinct trim colour, never a warm skin-adjacent midtone

PROPORTION: a garment hugs the figure. Total width must stay within about 1.15x the base body width. Capes, mantles and wings are a SEPARATE back-accessory layer.

LIGHTING: soft upper-left key at ~45 degrees, lower-right form shadows, subtle cool right rim, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish.

CONTENT: modest ceremonial clothing only. Opaque fabric throughout. No nudity, lingerie, swimwear, exposed torso or hips, or emphasized anatomical contours.

STRAY PIXELS: every pixel outside the garment must be exactly alpha 0. No alpha-1 dust anywhere on the canvas.

ISOLATION: the final asset contains ONLY the garment. No body, skin, head, face, hair, hands, held objects, aura, or scenery.

OUTPUT: one transparent 1254 x 1254 PNG. No text, no alternate versions, no contact sheet.
```

## The ten outfits

Reference: `images/reference_sheets/fantasy_character_outfits_reference_sheet.webp`. Each cell is roughly 20 × 30 px, enough to fix silhouette, palette and layering — not enough to fix trim detail. Where the preview cannot resolve ornament, invent nothing readable: use non-linguistic geometric motifs.

| ID | Cell | Design | Path stem | Contrast risk |
|---|---|---|---|---|
| DG-037 | r1c1 | White-silver celestial ceremonial robe, gold trim, deep navy inner sleeves | `outfit_001_celestial_robe_white_silver` | **high — pale** |
| DG-038 | r1c2 | Black long coat with split cape tails, cream sash, gold clasps | `outfit_002_black_split_tail_coat` | low |
| DG-039 | r1c3 | Plum-gray mage robe, pale underdress, dark hooded mantle | `outfit_003_plum_gray_mage_robe` | medium |
| DG-040 | r1c4 | Black ragged hooded cloak outfit, torn hem | `outfit_004_black_ragged_hooded_cloak` | low |
| DG-041 | r1c5 | White and blue armored ceremonial mantle, gold edging | `outfit_005_white_blue_armored_mantle` | **high — pale** |
| DG-042 | r2c1 | Black layered hooded long robe, charcoal underlayers | `outfit_006_black_layered_hooded_robe` | low |
| DG-043 | r2c2 | Oxblood-brown leather long coat, white turned cuffs | `outfit_007_brown_leather_long_coat` | low |
| DG-044 | r2c3 | Olive-green ragged cloak outfit, frayed edges | `outfit_008_olive_ragged_cloak` | medium |
| DG-045 | r2c4 | Deep-navy high-collar long coat, ragged hem | `outfit_009_navy_high_collar_coat` | low |
| DG-046 | r2c5 | Silver-white high-collar ceremonial robe, layered skirt | `outfit_010_celestial_robe_white_gold` | **high — pale** |

Substitute into the shared contract:

```text
SUBJECT: [design from the table above], worn shape only, with no body inside it.
- [two or three specific garment features: collar type, sleeve length, layering, trim placement]
- palette: [colours], with cool shadow in the folds
- ornament: non-readable geometric motifs only; no letters, runes, or pseudo-writing
```

### Order of production

**DG-045 navy high-collar coat first**, not DG-037. It is the outfit-category representative test in the backlog order, but more usefully it is the lowest-risk design in the set: deep navy against skin gives the largest possible contrast margin, so it clears the blocker on the first attempt with the least chance of a rejected round.

Then **DG-040** and **DG-042**, also dark and low-risk.

Leave the three pale designs — DG-037, DG-041, DG-046 — until after a dark one is registered and the pipeline is unblocked. They are the ones most likely to need several attempts to pass `--min-skin-contrast`, and there is no reason to have the release gated behind the hardest cases.

A collection where every token wears one robe has a monotony problem of its own, so **register three or four before rendering**, not one.

## Workflow per candidate

1. Upload to `images/trait_candidates/outfits/`.
2. Gate:
   ```bash
   python scripts/rig_gate_report.py --trait <file> --max-width-ratio 1.15 --min-skin-contrast 70
   ```
3. Composite over `assets/base_bodies/base_body_001_neutral_master.png` and confirm the head, neck and hand openings align and no mannequin garment shows through.
4. **Check it at 210 px.** Downscale the composite to thumbnail size and confirm the figure still reads as clothed. That is the test this category exists to pass.
5. Human approval, then register and run `python scripts/report_production_status.py --write`.
