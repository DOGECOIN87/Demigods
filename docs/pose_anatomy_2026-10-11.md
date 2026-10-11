# Pose anatomy and outfit prompt pack (2026-10-11)

All outfits were withdrawn on 2026-10-11 (`scripts/withdraw_all_outfits.py`,
`docs/qa/outfits_withdrawn_2026-10-11.md`). This document studies the 77 finished 1-of-1s
and the five locked base poses, then gives prompts for the replacement outfits.

## 1. What the 1-of-1 clothing looks like

From `images/one_of_ones/final_2026-10-10/` (e.g. 014 Lantern Keeper, 027 Frost Marshal,
039 Rune Blacksmith, 061 Oak Druid):

- **Dense, ornate, layered.** Every outfit has 3+ layers (under-tunic, coat/robe/armor,
  cape or mantle), heavy gold or silver filigree trim, belts with buckles and pouches,
  brooches, tassels, gem clasps.
- **Full coverage.** No bare torso or bare legs; arms are sleeved to the wrist, often with
  gloves or bracers. Legs end in tall detailed boots (or ornate sandals for robes).
- **Long hems that flare.** Coats, capes and robes reach the shins or floor and spread
  wider than the stance, giving a triangular silhouette.
- **Painterly semi-realistic chibi rendering**: fine fabric texture, embroidery, metallic
  highlights, warm key light from upper-left, soft rim light — not flat cel shading.
- **Themed palettes**: one dominant colour + metal accent (navy/gold, white/blue/silver,
  crimson/bronze, moss/gold, black/violet).

The old outfits failed because they were plain single-layer garments in a simpler style.

## 2. The base body (shared by every pose)

Canvas 1254 × 1254, character centred at x = 627, head top y ≈ 141, shoulder line
y ≈ 569, waist y ≈ 808, feet baseline y ≈ 1139. ~2.5-head chibi: huge round head, short
torso, short stubby arms (hands reach only to mid-thigh), short legs, feet planted
shoulder-width apart, toes forward. Undergarment: beige tank top and shorts (must be fully
covered). "Viewer-left" = the character's RIGHT hand.

| Pose | File | Character's RIGHT arm (viewer-left) | Character's LEFT arm (viewer-right) |
|---|---|---|---|
| 001 neutral | `base_body_001_neutral_master.png` | Hangs down, angled ~20° out from the body; hand open, palm facing viewer, fingers spread, beside the upper thigh (~x 404, y 772) | Mirror: open palm out, beside upper thigh (~x 850, y 772) |
| 002 viewer-left grip | `base_pose_002_viewer_left_vertical_grip.png` | Hangs ~20° out, hand a **closed fist with a vertical hole** (thumb on top) at hip height, ready to hold a staff/spear/sword vertically | Open palm, relaxed, like pose 001 |
| 003 viewer-right grip | `base_pose_003_viewer_right_vertical_grip.png` | Open palm, relaxed | **Closed vertical-grip fist** at hip height (mirror of 002) |
| 004 viewer-left palm-up | `base_pose_004_viewer_left_palm_up.png` | Forearm bent forward/outward at the elbow, **palm facing up**, hand held flat at hip height slightly further out — presenting/holding an orb, flame, potion | Open palm, relaxed |
| 005 two-hand grip | `base_pose_005_centered_two_hand_grip.png` | Both arms come **inward**, elbows near the ribs; fists **stacked one above the other** on the centre line at crotch height (~x 627, y 830–900) — gripping a planted sword hilt, staff or hammer handle | (stacked with the other fist) |

Consequences for clothing:

- **Sleeves** must end at the wrist and follow each arm's exact angle; cuffs must not cover
  the fists/palms (hand objects are drawn into those hands).
- **Poses 002/003**: the fist is a gripping hand — gloves are fine, but nothing (cuff ruffles,
  bracers) may pass through the hole in the fist.
- **Pose 004**: the bent arm shows the inner forearm and the cuff opening tilts toward the
  viewer; the palm must stay empty and visible.
- **Pose 005**: both sleeves cross the front of the torso; the front of the coat/robe is
  *behind* the forearms and fists. Front closures, belt buckles and sashes are hidden there,
  so keep the hero detail on the chest/collar and the hem.
- **Long hems/capes** may flare out to x ≈ 233–1021 (max character bounds) and down to
  y ≈ 1139; must not cover the feet entirely — boots stay visible.
- **Neck/head**: leave the neck and head untouched (hair, face, headwear are separate layers);
  collars may rise to the jaw but must not cover the chin.

## 3. Production method (keeps the rig)

Use the dressed-body workflow (`docs/workflows/dressed_body_intake.md`): give the generator
the exact base-pose PNG as the reference image and ask it to paint the clothes **onto the
body**, same canvas, same pixels for head/hands/feet. Each outfit family = 5 renders, one per
pose. Intake with `scripts/intake_dressed_bodies.py`.

### Reference images to attach (every render needs BOTH)

**Image 1: the base pose to edit** (exact file, never a different pose):

| Pose | Attach |
|---|---|
| 001 | `assets/base_bodies/base_body_001_neutral_master.png` |
| 002 | `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` |
| 003 | `assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png` |
| 004 | `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` |
| 005 | `assets/base_bodies/base_pose_005_centered_two_hand_grip.png` |

**Image 2: style reference, the closest 1-of-1** from `images/one_of_ones/final_2026-10-10/`:

| Outfit | Attach |
|---|---|
| 1 Celestial Regent | `Demigods_032_Sapphire_Admiral.png` |
| 2 Frost Marshal | `Demigods_027_Frost_Marshal.png` |
| 3 Ember Smith | `Demigods_039_Rune_Blacksmith.png` |
| 4 Verdant Druid | `Demigods_061_Oak_Druid.png` |
| 5 Lantern Kimono | `Demigods_014_Lantern_Keeper.png` |
| 6 Void Oracle | `Demigods_050_Raven_Oracle.png` |
| 7 Dawn Paladin | `Demigods_036_Diamond_Paladin.png` |
| 8 Clockwork Artisan | `Demigods_004_Clockwork_Artisan.png` |
| 9 Tide Captain | `Demigods_015_Tide_Captain.png` |
| 10 Desert Wanderer | `Demigods_009_Desert_Hourglass.png` |
| 11 Rose Diplomat | `Demigods_028_Rose_Diplomat.png` |
| 12 Shadow Locksmith | `Demigods_056_Shadow_Locksmith.png` |

For pose 005, also attach the family's finished pose 001 render (once made) as image 3, so
colours and trims match across all five.

### Master prompt (paste per pose; fill the {} parts)

```
Two images are attached. IMAGE 1 is the base character to edit: it is the only image you
modify and the output must align pixel-for-pixel with it. IMAGE 2 is a STYLE reference
only: match its level of ornate detail, rendering, texture and lighting, but do NOT copy
its pose, hands, held items, hair, face, background or proportions.
(If a third image is attached, it is the same outfit in another pose: match its colours,
trims and details exactly.)

Edit IMAGE 1. Keep the character's body, head, face, ears, hands,
fingers, legs, proportions, position, scale and the 1254x1254 canvas EXACTLY the same —
do not move, resize or redraw any limb. Only add clothing painted onto the body.

POSE (do not change): {POSE LINE from the list below}

OUTFIT: {OUTFIT DESCRIPTION}

Style: highly detailed painterly semi-realistic chibi fantasy illustration, matching an
ornate premium NFT character collection — layered garments, fine embroidery, gold/silver
filigree trim, metallic highlights, soft fabric folds, rich texture. Key light from the
upper-left, form shadows to the lower-right, subtle cool rim light on the right.

Rules: fully cover the beige tank top and shorts; sleeves follow each arm and end at the
wrist; leave both hands fully visible and empty (no held items, no props); the hem may
flare outward but boots/feet stay visible; leave the head and neck bare (no hat, hood up,
hair, scarf over chin, or jewelry on the head). Front-facing, symmetrical stance.
Background: solid flat #00FF00 chroma green (or transparent), no shadow on the ground,
no text, no frame.
```

### Pose lines

- **001**: "Both arms hang down slightly away from the body, both hands open with palms facing the viewer beside the thighs."
- **002**: "Character's right arm (viewer's left) hangs down with the hand a closed fist gripping vertically at hip height; the other hand is open, palm out."
- **003**: "Character's left arm (viewer's right) hangs down with the hand a closed fist gripping vertically at hip height; the other hand is open, palm out."
- **004**: "Character's right forearm (viewer's left) is bent forward with the palm facing up, held open at hip height as if presenting something; the other hand hangs open, palm out."
- **005**: "Both arms come forward and inward; both fists are stacked one above the other at the centre of the body at crotch height, as if resting on a planted sword hilt. The sleeves cross in front of the torso."

### Outfit descriptions (12 families drawn from the 1-of-1 themes)

1. **Celestial Regent** — navy velvet long coat to the shins, gold star-embroidered lapels and cuffs, white high-collar shirt with jabot, wide gold-buckled belt, short navy cape with gold chain clasp, black boots with gold toe caps.
2. **Frost Marshal** — white military greatcoat with ice-blue lining and white fur collar, silver epaulettes with fringe, blue sash across the chest, snowflake embroidery on the hem, silver buttons, white gloves, black knee boots.
3. **Ember Smith** — crimson tunic, dark leather apron with bronze rivets and rune engravings, bronze shoulder guard on one side, layered leather belts with tool pouches, rolled crimson trousers, heavy riveted brown boots.
4. **Verdant Druid** — moss-green layered robe covered in overlapping oak leaves, bark-textured bracers, acorn and amber clasps, leafy mantle over the shoulders, wrapped leaf greaves and root-like boots.
5. **Lantern Kimono** — deep indigo layered kimono with red and gold inner layers, gold butterfly embroidery, wide sleeves ending at the wrists, red obi with gold cord and tassels, white tabi with lacquered sandals.
6. **Void Oracle** — black and deep-violet tattered robe with layered shredded hem, silver filigree, glowing violet runes on the trim, black high collar, amethyst brooch, black pointed boots.
7. **Dawn Paladin** — polished white-gold plate armor: breastplate with sun emblem, layered pauldrons, white tabard with gold trim, chainmail skirt, armored greaves and sabatons.
8. **Clockwork Artisan** — brown leather waistcoat with brass gears and pocket watch chain, cream shirt, copper-buttoned tailcoat, belt of small tools, striped trousers, brass-buckled boots.
9. **Tide Captain** — teal naval coat with gold braid and anchor buttons, white ruffled shirt, wide red sash, cutlass belt (empty scabbard), striped breeches, tall cuffed boots.
10. **Desert Wanderer** — sand-coloured layered wraps and long hooded cloak (hood DOWN on the shoulders), terracotta sash, bronze coin belt, leather bracers, wrapped legs, sandals.
11. **Rose Diplomat** — burgundy brocade frock coat with rose embroidery, gold lapels, lace cravat with ruby pin, cream waistcoat, white breeches, polished brown boots.
12. **Shadow Locksmith** — charcoal fitted coat with many buckled straps and silver keys hanging from the belt, dark hood down, bronze trim, fingerless gloves, dark trousers, buckled boots.

Generate each family in all five poses before intake so every pose stays usable. Keep a
family's colours, trims and details identical across its five renders.
