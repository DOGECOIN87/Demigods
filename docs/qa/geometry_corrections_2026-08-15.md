# Geometry corrections — 2026-08-15

## Reported defects

The user identified three visible composition defects in dry-run output: neck bows and necklaces were oversized, held objects did not visibly read as being in the character's hands, and outfits allowed the neutral base-body undergarment to show through in places where the garment should visually cover it.

## Corrections applied

| Defect | Correction |
|---|---|
| Oversized neck accessories | Applied reduction-only refits to all 8 registered neck accessories. Small chokers and bows use a 0.45 reduction; the long navy pendant uses a 0.35 reduction. All were re-seated at the approved neck/upper-chest Y range. |
| Objects not appearing in hands | Separated metadata order from visual render order. Hand objects now render behind the base body so the gripping hand occludes the shaft, handle, or book edge at the hand anchor while the object remains visible outside the body. Updated the dry-run renderer and intake review compositor consistently. |
| Clothes not fully covering base bodies | Applied the repository-approved `hide_undergarment.py` repaint to the five locked base/outfit pairs. This removes visible neutral undergarment slivers by diffusing adjacent skin values into exposed undergarment regions; it does not upscale or redraw the clothing. |

Immutable backups were created before all production-byte changes. Manifest hashes and provenance records were updated for 13 affected assets: 5 base bodies and 8 neck accessories. No hand-object PNG bytes were changed.

## Representative visual review

Native-size examples confirm that the staff shaft passes behind the gripping hand, the lantern and tome read as held objects, the long pendant is proportionate to the torso, and the paired outfits no longer expose obvious neutral undergarment regions.

## Validation

| Check | Result |
|---|---|
| Configuration validation | Passed |
| Production asset validation | 85 checked; 0 failed |
| Manifest consistency | Passed |
| Production ledger | Passed |
| 777 preflight | Passed |
| Corrected 100-token sample | 100 unique tokens; 0 metadata/source/canvas/compatibility errors |
| Regression tests | 196 passed; 0 failures |
| Repository state | Pending final checkpoint |

The validator continues to emit the repository's known non-blocking ICC-profile and translucent-effect warnings. The corrected 100-token review sheet and native-size examples are the visual QA evidence for this pass.
