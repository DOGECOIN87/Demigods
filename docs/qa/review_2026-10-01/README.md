# Demigods review — 2026-10-01

Reviewed against `ae947c5416e2cd582040989b4a222bdf10818da4` on `main`, with the
subsequent mask and ledger corrections recorded in this checkpoint.

**The foreground correction batch has been rebuilt. All 134 registered modular
assets were reviewed, but the remaining garment fit defects mean this is not a
final visual approval of the collection.**

**Later update:** the scepter 010 eye overlap identified below was corrected
with a [compact in-hand replacement](../hand_object_010_compact_2026-10-01.md).
The measurements below describe the earlier snapshot.

## Corrected images

- [Corrected 50-image sheet](random_50_corrected.png) — the same 5-column,
  10-row order as the owner's marked sheet. The accidental large central circle
  is not a correction target.
- [All 72 treated variations](../../../images/variations/depth_treated_review_2026-10-01/contact_sheet.png).
- [Individual full-size exports](../../../images/variations/depth_treated_review_2026-10-01/).
- [Source / before / corrected close-ups](prop_closeups/).
- [Source roster](variations_72_sources.png) and [historical images](historical_variations.png).
- [Machine-readable review](collection_review.json).

The earlier correction scripts and overrides were committed, but their outputs
were not. This checkpoint saves the rebuilt review exports and the exact
refined masks, so the review does not depend on a previous assistant's scratch
files. Source artwork and registered production PNGs are unchanged.

The script previously blurred each local protection shape inward as well as
outward. Small props and parts near a shape's edge could therefore still get
blurred and desaturated. `refine_subject_masks.py` now retains the shape's solid
white interior and feathers its exterior. The treatment script already keeps
white-mask pixels exact.

Eight additional source images required local protection:

| Image | Detail corrected |
|---|---|
| 033 Ivory Judge | Scale beam, chains and both pans |
| 039 Rune Blacksmith | Hammer head, shaft and lower pommel |
| 041 Sand Archaeologist | Held gold tablet |
| 042 Prism Magician | Wand crystal, shaft and floating foreground prisms |
| 052 Spectral Ferryman | Staff tip, shaft and lower oar blade |
| 053 Black Opal Knight | Spiked staff head and shaft |
| 062 Cherry Blossom Guardian | Katana sheath, handle and tassels |
| 067 Bee Alchemist | Floating honey crystal and nearby light trails |

There are now 33 images with explicit local overrides, in addition to the
conservative segmentation refinement applied to all 72 masks. These are
conservative review masks; some nearby background may be protected with a prop.
The scripts do not recover details that were already soft in the source art.
Colors were preserved in the protected foreground; no blue recoloring was
applied. The earlier task and marked sheet identify unwanted foreground blur.

Treatment: background blur 7 px, saturation 0.84, brightness 0.99, contrast
0.98, exterior mask feather 1.5 px and background-only vignette 0.14, power 2.4.
Every output fully decodes at 1254 × 1254. Across all 72 outputs,
**zero pixels inside the refined mask's white region differ from their source**.
The [processing manifest](../../../images/variations/depth_treated_review_2026-10-01/processing_manifest.json)
records source, mask and output SHA-256 digests.

## The 77-image count

The variations folder contains 77 source image files, but their roles differ:

| Folder | Count | Current status |
|---|---:|---|
| `images/variations/complete_72` | 72 | Distinct current 1254 × 1254 PNG illustrations; corrected above |
| `images/variations/nature` | 4 | Historical 1024 × 1024 WebP variations, excluded from the current batch |
| `images/variations/references` | 1 | JPEG copy of legendary 005; reference, not an additional collectible |

All 77 source files were inspected. The four older WebPs were not upscaled, and
the JPEG reference was not counted as a new one-of-one. A separate historical
1254 PNG remains in `images/one_of_ones`, and seven registered legendary PNGs
remain in `assets/legendary`; these are shown in the historical and legendary
sheets. They are separate from the 72-variation correction roster.

The 72 variations still have no final token-ID assignment. `collection.json`
still describes 770 generative tokens plus seven reserved legendary IDs. A
700-generative / 77-one-of-one final roster is not yet represented by that
export configuration. Final assembly needs an explicit roster of 77 eligible
one-of-ones; the five historical/reference entries are not a substitute.

## All active trait categories

All registered files match their manifest checksums and pass canvas, PNG decode
and alpha checks. Every category was composited against the actual registered
base/pose and shared face/hair system. The sheets are generated from the current
PNG files, rather than historical previews.

| Category | Registered | Visual review |
|---|---:|---|
| Backgrounds | 8 | [All eight contexts](traits_backgrounds.png); no new file or placement defect found |
| Base bodies | 5 | [Pose family](traits_base_bodies.png); locked family preserved |
| Back accessories | 7 | [Wings and capes](traits_back_accessories.png); no new defect found |
| Rear hair | 8 | [Paired hair review](traits_hair_back.png); silver 003 needs low-alpha residue cleanup |
| Outfits | 25 | [Sheet 1](traits_outfits_01.png), [sheet 2](traits_outfits_02.png); 20 dressed bodies pass current gates, five garment-only layers retain fit defects |
| Eyes | 24 | [Eye colors](traits_eyes.png); no new placement defect found |
| Eyebrows | 16 | [Brow expressions](traits_eyebrows.png); no new placement defect found |
| Mouths | 12 | [Mouth expressions](traits_mouths.png); no new placement defect found |
| Expression marks | 8 | [Expression marks](traits_expression_marks.png); no new placement defect found |
| Front hair | 8 | [Front/back pairs](traits_hair_front.png); matching colors and compatibility maintained |
| Hand objects | 10 | [Full figures](traits_hand_objects.png); 36 legal object/outfit pairings checked; scepter 010 needs face-clearance review |
| Global finishes | 3 | [Finish comparison](traits_global_finish.png); no new defect found |

Neckwear, head accessories, rear auras and front auras remain withdrawn. They
are excluded from generation and were not restored or treated as missing work.
The violet blade 009, talisman 011 and storm guardian outfit 002 also remain
withdrawn.

The old ledger still called retired gold wings 007 `QA-failed`, leaving a
phantom pending back-accessory category. Its existing 2026-09-10 retirement
record says it was dropped as a duplicate silhouette. The backlog row now
closes as withdrawn, `pending_categories` is empty and the regenerated ledger
reports all 12 active categories structurally complete. **This ledger state
does not close the visual findings below.**

## Remaining art work, in priority order

### 1. Five garment families still need dressed-body replacements

Only families 006–009 have all five registered poses. The five other active
families are garment-only layers bound to a single pose. Re-measuring the
current PNGs with `fit_outfit_torso.shortfall` reproduces their outstanding
torso/leg coverage gaps:

| Family | Existing pose | Torso/leg shortfall |
|---|---|---:|
| 001 Celestial Scholar | 001 | 2,205 px |
| 003 Verdant Alchemist | 003 | 1,190 px |
| 004 Lunar Oracle | 004 | 2,032 px |
| 005 Sun Temple | 005 | 4,514 px |
| 010 White/Gold Celestial Robe | 001 | 5,023 px |

These measurements locate coverage gaps, not a visual acceptance threshold.
Shoulder and neckline issues are also documented in the
[refit brief](../../handoff/outfit-refit-brief.md).

The required batch is **25 dressed-body renders**: five families × five poses,
replacing their five current layers and adding 20 missing pose versions. The
older 30-render prompt plan included storm guardian 002, which was subsequently
withdrawn. Keep its removal and omit neckwear. The five poses remain the shared
registered master family, with hands and held items fitted to their actual pose.

### 2. Scepter 010 overlaps the eye

The later passing batch did replace the old silver sword and horned scepter;
the earlier `hand_objects_in_hand_2026-09-27.md` “still open” list is superseded
by `hand_objects_in_hand_2026-09-27-passing.md` and the current manifest.

The current scepter covers **1,359 opaque pixels of the viewer-left eye window**
`(505,334)–(584,403)`. The other nine hand-object layers cover zero opaque pixels
in the two fixed eye windows. This is visible across its three compatible
dressed outfits in [hand sheet 2](hand_composites_02.png). Its gripping hand
fits, but the large horned head crosses the face. Review a smaller or outward
head/shaft arrangement while preserving the wristless grip; do not shrink the
whole layer until the holding hand stops covering the base fist.

The black robe's pose-002 fist remains intentionally incompatible with held
objects, because it sits inward from the shared grip. Existing exclusion rules
are preserved. [Hand sheet 1](hand_composites_01.png) and sheet 2 cover all 36
currently allowed item/outfit combinations.

### 3. Silver rear hair needs an alpha-edge cleanup

`hair_back_003` retains low-alpha strands outside the main locks, previously
recorded in the dressed-body QA. They can read as gray wisps on dark backgrounds.
Its source hash still matches the approved registered file. Clean this as a
review candidate and compare on dark and light backgrounds before replacing
the registered hair or its manifest hash.

## Validation and reproduction

- 134/134 registered modular assets pass binary and checksum checks.
- All 20 dressed-body outfits pass the crown/sole and face-clearance gates.
- Seven of seven separate legendary images pass their automated checks and
  were visually reviewed in the [legendary sheet](legendary_7.png).
- Configuration, registered-manifest consistency and production-ledger checks pass.
- [Regression suite](test_run.log): 251 tests run, 247 passed, four skipped for withdrawn categories.
- [700-token dry-run summary](generative_dry_run_700.json): 700 distinct valid
  signatures, seed `demigods-review-2026-10-01`, 55,627 selection attempts.
  The current preflight estimate is approximately 10.3 billion valid combinations.
  This dry run verifies capacity and rules, not the visual quality of every possible combination.
- PNG file checks retain the existing no-ICC warnings; no profile assumptions
  or artwork bytes were rewritten to suppress them.

```bash
python scripts/refine_subject_masks.py --expected-count 72 --overwrite
python scripts/apply_depth_treatment.py \
  --input-dir images/variations/complete_72 \
  --mask-dir images/variations/subject_masks_refined_review \
  --output-dir images/variations/depth_treated_review_2026-10-01 \
  --expected-count 72 --blur-radius 7 --overwrite
python scripts/build_collection_review.py
```

The baseline for the close-up comparisons is the prior mask code and override
configuration at `ae947c5`, reconstructed with the same treatment parameters.
The scripts write review candidates and evidence; they do not promote artwork
or assign collection token IDs.
