# Corrected dry-run composition test — 2026-08-15

## Root cause

The first sample exposed a real composition-rule defect: pose-specific outfits and hand objects were being selected independently of the base pose. The asset files themselves were valid, but the generator could place a Pose 002 or Pose 004 hand object on the neutral base, or pair a pose-specific outfit with a different base pose. This produced visually incorrect armhole, grip, and object-contact relationships.

## Correction

Added explicit `requires` rules to `config/compatibility.json`:

| Trait family | Required base pose |
|---|---|
| Outfits 001, 006–010 | Neutral master / Pose 001 |
| Outfit 002 and hand objects 006–010 | Viewer-left vertical-grip Pose 002 |
| Outfit 004 and hand objects 011–012 | Viewer-left palm-up Pose 004 |
| Outfit 003 | Viewer-right vertical-grip Pose 003 |
| Outfit 005 | Centered two-hand-grip Pose 005 |

The correction changes composition compatibility only. No production PNG bytes were changed.

## Corrected sample results

| Check | Result |
|---|---|
| Unique dry-run tokens | 20 of 20 |
| Missing source files | 0 |
| Configuration validation | Passed; 25 requires rules |
| Asset validation | 85 checked, 0 failed |
| Manifest consistency | Passed |
| Production ledger | Passed |
| 777 preflight | Passed |
| Regression tests | 196 passed, 0 failures |
| Visual review | Pose-matched outfits and hand objects now align with their base poses |

The corrected sample uses a smaller but still abundant rule-valid combination space of 2,451,456 combinations. Rear auras, hair back, and global finish remain optional as configured. The corrected review sheet supersedes the earlier sample for visual QA.
