# Pose-Aware Outfit Family QA

Date: 2026-07-28

Five materially distinct outfit layers were regenerated with their exact
approved pose as the placement reference. Chroma sources were converted to
genuine RGBA, contracted by one alpha pixel to remove green fringe, and
composited over the required base pose.

## Approved family

| Outfit | Required pose | Result |
|---|---|---|
| Celestial scholar | Pose 001 relaxed/open | Pass |
| Storm guardian | Pose 002 viewer-left grip | Pass |
| Verdant alchemist | Pose 003 viewer-right grip | Pass |
| Lunar oracle | Pose 004 viewer-left palm-up | Pass |
| Sun-temple ceremonial | Pose 005 centered two-hand grip | Pass — pose-bundled forearm/hand overlay |

All layers are native 1254 × 1254 RGBA. Final visible bounds begin at Y 475
and end no lower than the locked Y 1139 baseline. Composites show clean neck,
shoulder, wrist, finger, leg, and footwear alignment. The rejected two-hand
attempt containing toe pixels was not promoted. Pose 005 bundles its exact
forearms and joined hands into the outfit overlay because the crossed hands
must render above the continuous tunic and sash; its compatibility rule prevents
use with any other base pose.

Review:
`docs/qa/composites/outfits/pose_aware_outfits_001_005_production_review.png`
