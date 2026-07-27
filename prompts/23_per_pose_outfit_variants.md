# Prompts — Per-pose outfit variants DG-205 to DG-228

The six painted robes (DG-199 to DG-204) are each drawn with one arm position
baked into the sleeves. An outfit composites *over* the base body, so those
sleeves replace whatever the arms were doing, and the five base poses differ from
one another **only** in their arms and hands.

## What is actually broken, measured

Share of each pose's silhouette difference from the neutral master that a painted
robe covers, and — separately — whether the hands still emerge from the cuffs,
which is what makes a pose read:

| Base pose | Arm hidden | Hands visible | Needs a variant |
|---|---|---|---|
| 001 neutral master | 0.0% | yes | no — this is the art as drawn |
| 004 viewer-left palm-up | 58.6% | yes, 1284 px | optional |
| 003 viewer-right vertical grip | 63.6% | yes, 806 px | optional |
| 002 viewer-left vertical grip | 64.7% | yes, 1210 px | optional |
| 005 centered two-hand grip | 82.8% | **no** | **yes** |

The arm being hidden is not a fault — a sleeve is supposed to cover an arm. On
poses 002 to 004 the hands emerge from the bell cuffs and the fist, open hand or
upturned palm still reads. Those variants sharpen the sleeve angle; they do not
rescue anything.

Pose 005 is different. Its clasped fists sit at **X 580-705, Y 685-815** — dead
centre, in front of the torso rather than at the cuffs — so no sleeve reaches
them and every robe buries them completely. A token using pose 005 is visually
identical to the same token using pose 001.

## Why this needs new artwork

Compositing the hands back over the robe was tried and does not work. The fists
overlap the torso at the same skin tone, and the painted outlines do not enclose
them, so an edge-aware flood fill from the fist centres leaks into the torso and
shorts and returns a skin-coloured slab. There is no clean matte to recover. The
sleeves have to be painted for the pose.

## Binding a variant to its pose

`config/compatibility.json` already supports this and `generate_777.py` honours
it. Each variant requires its pose, and each base robe excludes the poses that
have variants, so the generator can never pair a sleeve with the wrong arms:

```json
{
  "trait": "outfit_003_navy_gold_star_pose005.png",
  "requires": "base_pose_005_centered_two_hand_grip.png",
  "reason": "sleeves painted for the centered two-hand grip"
}
```

Rules are added only when the matching variant is registered — a rule naming a
missing file fails `validate_config.py`.

## Shared contract

Inherit everything in `prompts/22_outfit_prompts.md` — canvas, fit, contrast,
proportion, lighting, content — with these changes. Paste this above the per-pose
block.

```text
Create exactly one isolated Demigods outfit, rendered NATIVELY at exactly 1254 x 1254 pixels, RGBA PNG with genuine transparent alpha.

ATTACH: the base pose named in the block below + the existing robe it varies + docs/rig/rig_guide_1254.png

This is a SLEEVE VARIANT. The garment's body, collar, sash, hem, trim, palette and every ornament must match the attached robe exactly. Only the sleeves change, and only enough to follow the attached pose's arms. Someone comparing the two at full resolution should see the same robe worn by a person standing differently, not a second design.

FIT — match the attached BASE POSE, not the neutral master:
- collar top at Y 442, hem at Y 1108, symmetrical about X 627
- cover the shoulder band Y 535-660 completely; bare skin there reads as a hole
- sleeves follow that pose's upper arm and forearm, with the cuff opening ending at its wrist
- the pose's hands stay OUTSIDE the garment and fully visible
- every visible pixel inside X 233-1021 and Y 129-1139

DO NOT REMOVE A BACKGROUND. Paint onto an empty transparent canvas.
```

## Priority

Generate the six pose-005 variants first. They are the only ones that recover
something currently lost. The eighteen for poses 002 to 004 are refinement and
can wait, or be dropped in favour of accepting those three poses as-is.

## DG-205 to DG-210 — pose 005, centered two-hand grip

`ATTACH: assets/base_bodies/base_pose_005_centered_two_hand_grip.png`

The arms are drawn down and angled inward, forearms converging so both fists
clasp at centre in front of the lower torso, one fist stacked above the other,
occupying roughly X 580-705 and Y 685-815.

```text
POSE: both arms angled inward and down, forearms converging toward the centre line, hands clasped together in front of the lower torso.

SLEEVES: narrower than the source robe and angled inward to follow the converging forearms. Each cuff opening ends at its wrist, at roughly X 560 and X 700, Y 690. The two cuffs frame the clasped hands from either side without touching or overlapping them.

LEAVE COMPLETELY EMPTY — transparent alpha, no fabric, no shadow, no trim — the region X 570-715 by Y 675-825. The clasped hands occupy it and must remain fully visible when this layer composites over the base pose. Fabric there is an automatic rejection.

The robe's front panel continues below Y 825 and above Y 675 exactly as in the source robe.
```

| ID | Varies | Base pose | Intended production path |
|---|---|---|---|
| DG-205 | DG-199 white and gold | 005 | `assets/outfits/outfit_001_white_gold_pose005.png` |
| DG-206 | DG-200 black and gold | 005 | `assets/outfits/outfit_002_black_gold_pose005.png` |
| DG-207 | DG-201 navy and gold star | 005 | `assets/outfits/outfit_003_navy_gold_star_pose005.png` |
| DG-208 | DG-202 crimson and gold | 005 | `assets/outfits/outfit_004_crimson_gold_pose005.png` |
| DG-209 | DG-203 purple and black | 005 | `assets/outfits/outfit_005_purple_black_gold_pose005.png` |
| DG-210 | DG-204 white and navy star | 005 | `assets/outfits/outfit_006_white_navy_star_pose005.png` |

## DG-211 to DG-216 — pose 002, viewer-left vertical grip

`ATTACH: assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png`

```text
POSE: viewer-left arm down with the hand closed in a vertical grip at roughly X 430, Y 790; viewer-right arm relaxed and open.

SLEEVES: the viewer-left sleeve hangs slightly outward and its cuff ends just above the closed fist, at roughly Y 745. The viewer-right sleeve matches the source robe. Both hands stay outside the garment and fully visible.
```

| ID | Varies | Base pose | Intended production path |
|---|---|---|---|
| DG-211 | DG-199 white and gold | 002 | `assets/outfits/outfit_001_white_gold_pose002.png` |
| DG-212 | DG-200 black and gold | 002 | `assets/outfits/outfit_002_black_gold_pose002.png` |
| DG-213 | DG-201 navy and gold star | 002 | `assets/outfits/outfit_003_navy_gold_star_pose002.png` |
| DG-214 | DG-202 crimson and gold | 002 | `assets/outfits/outfit_004_crimson_gold_pose002.png` |
| DG-215 | DG-203 purple and black | 002 | `assets/outfits/outfit_005_purple_black_gold_pose002.png` |
| DG-216 | DG-204 white and navy star | 002 | `assets/outfits/outfit_006_white_navy_star_pose002.png` |

## DG-217 to DG-222 — pose 003, viewer-right vertical grip

`ATTACH: assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png`

```text
POSE: viewer-right arm down with the hand closed in a vertical grip at roughly X 820, Y 790; viewer-left arm relaxed and open.

SLEEVES: the viewer-right sleeve hangs slightly outward and its cuff ends just above the closed fist, at roughly Y 745. The viewer-left sleeve matches the source robe. Both hands stay outside the garment and fully visible.
```

| ID | Varies | Base pose | Intended production path |
|---|---|---|---|
| DG-217 | DG-199 white and gold | 003 | `assets/outfits/outfit_001_white_gold_pose003.png` |
| DG-218 | DG-200 black and gold | 003 | `assets/outfits/outfit_002_black_gold_pose003.png` |
| DG-219 | DG-201 navy and gold star | 003 | `assets/outfits/outfit_003_navy_gold_star_pose003.png` |
| DG-220 | DG-202 crimson and gold | 003 | `assets/outfits/outfit_004_crimson_gold_pose003.png` |
| DG-221 | DG-203 purple and black | 003 | `assets/outfits/outfit_005_purple_black_gold_pose003.png` |
| DG-222 | DG-204 white and navy star | 003 | `assets/outfits/outfit_006_white_navy_star_pose003.png` |

## DG-223 to DG-228 — pose 004, viewer-left palm-up

`ATTACH: assets/base_bodies/base_pose_004_viewer_left_palm_up.png`

```text
POSE: viewer-left forearm raised slightly with the hand turned palm-up and open at roughly X 500, Y 775; viewer-right arm relaxed and open.

SLEEVES: the viewer-left sleeve is shortened and lifted so the cuff clears the raised forearm, ending at roughly Y 730, with the bell falling away beneath it. The viewer-right sleeve matches the source robe. The upturned palm stays outside the garment and fully visible.
```

| ID | Varies | Base pose | Intended production path |
|---|---|---|---|
| DG-223 | DG-199 white and gold | 004 | `assets/outfits/outfit_001_white_gold_pose004.png` |
| DG-224 | DG-200 black and gold | 004 | `assets/outfits/outfit_002_black_gold_pose004.png` |
| DG-225 | DG-201 navy and gold star | 004 | `assets/outfits/outfit_003_navy_gold_star_pose004.png` |
| DG-226 | DG-202 crimson and gold | 004 | `assets/outfits/outfit_004_crimson_gold_pose004.png` |
| DG-227 | DG-203 purple and black | 004 | `assets/outfits/outfit_005_purple_black_gold_pose004.png` |
| DG-228 | DG-204 white and navy star | 004 | `assets/outfits/outfit_006_white_navy_star_pose004.png` |

## Intake

Returned renders go through the same path as the base robes:

```bash
python scripts/intake_painted_outfit.py <render> \
  --out images/trait_candidates/outfits/<name>.png --pose-report
python scripts/rig_gate_report.py --trait <candidate> --min-skin-contrast 70
```

`intake_painted_outfit.py` reports `bare shoulder pixels` against the neutral
master. For a pose variant, check it against its own pose instead — the shoulder
band is the same on all five, but the arm band is not.

A pose-005 variant must additionally be checked for an empty hand window: any
opaque pixel inside X 570-715 by Y 675-825 means the hands will be buried again.
