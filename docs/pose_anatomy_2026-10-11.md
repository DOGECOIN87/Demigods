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

## 3. Held items repaint skin over the hand (measured)

The in-hand objects (`assets/hand_objects/`, drawn over the figure) are painted with the hand
that holds them, in bare skin:

- **Pose 002**: each object repaints the image-left fist and wrist, from about Y 720 down.
- **Pose 004**: each orb or book repaints the whole image-left forearm, from the elbow (about
  Y 665) to the fingertips.

So outfits use no gloves. The Pose 002/003 grip-side cuff ends above the wrist. In Pose 004,
the image-left sleeve is pushed up above the elbow.

## 4. Prompts

Ready-to-paste prompts, 12 outfits × 5 poses: **`prompts/outfit_prompt_pack_2026-10-11.md`**,
built by `scripts/build_outfit_prompt_pack.py`. Each prompt attaches only its base pose. It
locks the figure to the rig, asks for a bald, faceless head and bare hands, and states the
background each palette needs (transparent; flat black only for light outfits). New
families are numbered 011-022 so they never reuse a withdrawn outfit id. Intake:
`docs/workflows/dressed_body_intake.md`.

**All-in-one:** `prompts/outfit_all_in_one_prompt.md` is one paste covering every outfit and pose.
You set `OUTFIT` and `POSE`. The assistant downloads the base pose from a pinned commit,
checks its SHA-256 and that the pose is the right one, renders, self-checks against a
checklist, and returns the file name and a `sources.json` entry.
