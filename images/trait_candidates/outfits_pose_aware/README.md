# Pose-Aware Outfit Regeneration Candidates

These five native 1254 × 1254 RGB images are dressed-pose design candidates,
not production clothing layers. They intentionally remain outside `assets/`
and the production manifest.

| Candidate | Pose | Design direction | Status |
|---|---|---|---|
| `outfit_001_celestial_scholar_pose_001_candidate.png` | 001 relaxed/open | celestial tailoring | extraction required |
| `outfit_002_storm_guardian_pose_002_candidate.png` | 002 viewer-left grip | light armor | extraction required |
| `outfit_003_verdant_alchemist_pose_003_candidate.png` | 003 viewer-right grip | utility/workwear | extraction required |
| `outfit_004_lunar_oracle_pose_004_candidate.png` | 004 viewer-left palm-up | ceremonial wrap | extraction required |
| `outfit_005_sun_temple_pose_005_candidate.png` | 005 two-hand grip | woven ceremonial | extraction required |

## Known blocker

The built-in image editor rendered a visual checkerboard into RGB pixels.
These files therefore fail the repository's genuine-alpha rule. They are useful
as pose-aware design references for the next isolated extraction pass, but must
not be chroma-keyed or promoted as though the checkerboard were transparency.

Use `prompts/08_outfits.md` for extraction/regeneration. Each final outfit must
be an outfit-only RGBA layer, composited against the exact pose named in its
filename, and tied to that pose with a compatibility `requires` rule.
