#!/usr/bin/env python3
"""Assemble ready-to-run Grok trait-generation prompts for every layer category.

Resolves the repo's placeholder templates (prompts/00 locked spec + prompts/01
avoid block + each category template) into self-contained, copy-paste prompts
that render one isolated transparent 1254x1254 trait aligned to the registered
base body. Output: prompts/ready_to_run_trait_prompts.md
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

AVOID = ("photorealism, side or three-quarter views, camera tilt, perspective distortion, scale drift, "
         "changed rig anchors, cropped edges, extra or missing fingers, duplicated limbs, malformed hands, "
         "text, labels, captions, borders, frames, watermark, rendered checkerboard, fake transparency, "
         "gray or colored backdrop, floor shadow, multiple assets or variations, multiple characters, "
         "merged trait categories, unrelated traits, scenery, character or franchise names, blurry or "
         "low-detail rendering, inconsistent or front-right lighting")

BASE = "assets/base_bodies/base_body_001_neutral_master.png (placement/scale/lighting reference) + docs/rig/rig_guide_1254.png"


def header(title: str, attach: str) -> str:
    return f"""Create exactly one isolated Demigods {title}, rendered natively at exactly 1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.

ATTACH: {attach}

REFERENCE ROLE:
Use the attached base master ONLY as an invisible placement, scale, and lighting guide. The FINAL image must contain ONLY the requested trait on full transparency — never the body, face, or any other layer. Do not resize, rotate, crop, or change the shared proportions.

LOCKED RIG (match the reference exactly; the rig guide shows these):
- 1254 x 1254, fully transparent background, no checkerboard or backdrop
- canvas center X 627; head center X 627, Y 343; eye line Y 367; mouth center X 627, Y 441
- shoulder line Y 569; waist center X 627, Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404, Y 772; viewer-right hand anchor X 850, Y 772
- keep every visible pixel within X 233-1021 and Y 129-1139; do not crop the asset
- perfectly front-facing and orthographic, zero yaw/pitch/roll/tilt/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim, soft ambient fill
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi game-art finish"""


# Uniform: (layer_no, title, attach, target, bullets, exclude, filename)
CATS = [
 (2, "rear aura / effect (behind the character)", BASE,
  "Create one rear aura or effect: [SPECIFY — e.g. blue floor halo ring / violet radial glow / lightning wisps / rising void flame / sacred light].",
  ["centered to the master rig, framing the character silhouette without covering the face zone",
   "luminous with soft transparent alpha falloff; no solid black, white, or colored fill",
   "include a floor disc ONLY if the effect is explicitly a floor circle",
   "do not clip glow or particles at the canvas edges"],
  "the character, clothing, objects, and scenery",
  "aura_[NUM]_[TYPE]_[COLOR]_rear.png"),
 (3, "back accessory (wings / cape / cloak / mantle / crest)", BASE,
  "Create one back accessory: [SPECIFY — e.g. silver feathered wings / black-violet bat wings / navy formal cape / ragged cloak].",
  ["align to the shared upper-back and shoulder-blade anchors, positioned BEHIND the body",
   "render as seen from the front while sitting behind the character",
   "wings are a balanced symmetrical pair unless deliberately asymmetric",
   "preserve a hidden central overlap behind the torso; respect the foot baseline"],
  "the mannequin, body, head, hair, outfit, hands, and background",
  "back_accessory_[NUM]_[TYPE]_[COLOR].png"),
 (4, "hair-back layer (rear hair only)", BASE,
  "Create only the REAR portion of one hairstyle: [SPECIFY — length and shape, e.g. long wavy, straight, twin braids].",
  ["back-hair layer only, positioned behind the head and shoulders",
   "align to the master scalp centered at X 627, Y 343; keep the head interior transparent",
   "exclude bangs and face-framing front strands (those are the separate front-hair layer)",
   "include hidden overlap behind the scalp to prevent seams",
   "Color: [COLOR]"],
  "bangs, front strands, face, ears, body, clothes, and accessories",
  "hair_back_[NUM]_[COLOR]_[STYLE].png"),
 (6, "outfit (clothing only)", BASE,
  "Create one isolated outfit: [SPECIFY — theme, garments, colors, e.g. royal white-gold robe / dark prince armor / celestial dress].",
  ["align to the shared neck, shoulders, torso, waist, wrists, hips, knees, and foot baseline",
   "preserve the exact approved body proportions; leave clean openings for head, neck, and hands",
   "include hidden overlap beneath hands, hair, and neck layers to prevent seams",
   "keep capes / wings / back effects as SEPARATE layers unless structurally inseparable"],
  "the body, head, face, hair, hands, held objects, aura, and scenery",
  "outfit_[NUM]_[THEME]_[COLOR].png"),
 (7, "neck accessory (necklace / choker / collar / bow / pendant)", BASE,
  "Create one isolated neck accessory: [SPECIFY — type, material, color].",
  ["align to the approved neck and upper-chest anchor",
   "preserve hidden overlap beneath hair and above the outfit"],
  "skin, outfit, head, face, and hair",
  "neck_accessory_[NUM]_[TYPE]_[COLOR].png"),
 (8, "eye set (matched pair)", BASE,
  "Create one matched eye-set trait: [SPECIFY — iris color, pupil, style, e.g. galaxy blue / soul-flame violet / silver runic].",
  ["both eyes aligned to Y 367 using the identical approved spacing and scale",
   "include eye lines, lashes, sclera, irises, pupils, internal highlights, and shading",
   "use the shared upper-left catchlight logic"],
  "eyebrows, nose, mouth, face, skin, blush, hair, and expression marks",
  "eyes_[NUM]_[COLOR]_[STYLE].png"),
 (9, "eyebrow pair", BASE,
  "Create one matched eyebrow pair expressing [SPECIFY MOOD — e.g. calm, fierce, gentle, surprised].",
  ["use the approved eyebrow anchor positions and line weight, just above the eye line (Y 367)",
   "remain compatible with all approved eye sets"],
  "eyes, face, forehead, hair, nose, mouth, and blush",
  "eyebrows_[NUM]_[MOOD].png"),
 (10, "mouth", BASE,
  "Create one isolated mouth: [SPECIFY — e.g. soft smile / confident smirk / open cheer / calm neutral / tiny pout / fang grin].",
  ["center to the mouth anchor at X 627, Y 441 using the approved scale",
   "include only the mouth (and minimal chin shading if needed)"],
  "eyes, eyebrows, nose, face, skin, blush, and hair",
  "mouth_[NUM]_[TYPE].png"),
 (11, "expression mark overlay", BASE,
  "Create one isolated expression overlay: [SPECIFY — blush / sweat drop / anger mark / sparkles / stress lines / tears].",
  ["align to the appropriate face zone (cheeks, temple, or above the head)",
   "include only the requested effect on clean transparent space; readable at small size"],
  "face features, hair, body, and any full-character aura",
  "expression_[NUM]_[TYPE].png"),
 (12, "hair-front layer (bangs / front strands only)", BASE,
  "Create only the FRONT portion of one hairstyle: [SPECIFY — bang shape and parting].",
  ["bangs and front face-framing strands only; align to the shared scalp, forehead, temple, and ear anchors",
   "preserve the approved face opening; do not change head dimensions",
   "include hidden overlap beneath the top hairline to prevent seams",
   "Color: [COLOR]  (match the paired hair-back layer)"],
  "rear hair, scalp, face, skin, eyes, eyebrows, mouth, ears, clothing, crowns, horns, halos, and jewelry",
  "hair_front_[NUM]_[COLOR]_[STYLE].png"),
 (13, "head accessory (crown / halo / horns / tiara / laurel / circlet / veil)", BASE,
  "Create one isolated head accessory: [SPECIFY — type, material, color].",
  ["center to the approved head anchor at X 627, Y 343; sit on top of or around the head",
   "preserve hidden overlap where it enters or sits behind hair",
   "use a balanced pair for horns or side ornaments; keep halos and open metalwork transparent inside"],
  "hair, scalp, face, eyes, body, clothing, neck accessory, and aura",
  "head_accessory_[NUM]_[TYPE]_[MATERIAL].png"),
 (14, "hand-held object",
  BASE + " + the matching pose file (e.g. assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png)",
  "Create one isolated hand-held object: [SPECIFY — staff / orb / book / sword / wand / lantern / relic]. Assigned hand: [VIEWER-LEFT X404,Y772 / VIEWER-RIGHT X850,Y772 / BOTH].",
  ["align the grip/contact point exactly to the assigned hand anchor, matching the chosen pose's grip angle",
   "include the object only, plus a minimal grip overlay ONLY if technically necessary",
   "contain any glow within transparent alpha falloff; keep the whole object uncropped"],
  "the body, arm, outfit, face, and background",
  "hand_object_[NUM]_[TYPE]_pose_[POSE]_[SIDE].png"),
 (15, "front aura / effect (in front of the character)", BASE,
  "Create one front aura or effect: [SPECIFY — sparkles / floating stars / embers / petals / energy motes].",
  ["centered to the master rig, sitting in FRONT of the character but never covering the eyes or mouth",
   "luminous with soft transparent alpha falloff; no solid backdrop",
   "do not clip particles at the canvas edges"],
  "the character, clothing, objects, and scenery",
  "aura_[NUM]_[TYPE]_[COLOR]_front.png"),
]


def build() -> int:
    out = ["# DEMIGODS — ready-to-run Grok trait prompts",
           "",
           "One self-contained prompt per layer category, in back-to-front stack order. Each renders a single "
           "isolated transparent 1254x1254 trait aligned to the registered base body. Fill the `[SPECIFY ...]` "
           "slot (and `[NUM]`/`[COLOR]` in the filename) per asset.",
           "",
           "**Every prompt:** attach `assets/base_bodies/base_body_001_neutral_master.png` + "
           "`docs/rig/rig_guide_1254.png` (hand objects also attach the matching pose). After generating, gate "
           "with `python scripts/rig_gate_report.py --pose-variant --tolerance 2 <file>`.",
           "", "---", ""]
    for layer, title, attach, target, bullets, exclude, fname in CATS:
        prompt = (header(title, attach) + "\n\nTARGET:\n" + target + "\n"
                  + "\n".join(f"- {b}" for b in bullets)
                  + f"\n\nISOLATION: the final asset contains ONLY the {title}; exclude {exclude}."
                  + f"\n\nOUTPUT: one transparent 1254 x 1254 PNG. filename: {fname}"
                  + f"\n\nAVOID:\n{AVOID}.\n\nReturn one transparent PNG only. No text or alternate versions.")
        out.append(f"## Layer {layer:02d} — {title}\n\n```\n{prompt}\n```\n")
    (ROOT / "prompts" / "ready_to_run_trait_prompts.md").write_text("\n".join(out))
    print(f"Wrote prompts/ready_to_run_trait_prompts.md with {len(CATS)} category prompts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
