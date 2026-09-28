# Background depth treatment for complete variations

The current complete set is `images/variations/complete_72/` (72 flattened PNGs as of 2026-09-28). The old `images/one_of_ones/` roster is historical and currently contains only one PNG. The batch script works with the current 72 and additional PNGs as they arrive; use `--expected-count 77` once all 77 are present.

Because these images are flattened, the script requires an exact per-image subject mask. A guessed oval cannot reliably protect wings, held objects, hair, or poses. Make a grayscale PNG with the same filename and dimensions as each source: white (255) for everything that must remain untouched, black (0) for the background. Include character, clothing, hair, accessories, held objects, and any foreground effects you want sharp. Gray values allow partial treatment. Save masks in a separate folder, for example `images/variations/subject_masks/`. The script checks all selected masks before writing anything.

Preview the first image:

```bash
python scripts/apply_depth_treatment.py \
  --input-dir images/variations/complete_72 \
  --mask-dir images/variations/subject_masks \
  --output-dir images/variations/depth_treated_preview \
  --limit 1
```

Process the whole current roster:

```bash
python scripts/apply_depth_treatment.py \
  --input-dir images/variations/complete_72 \
  --mask-dir images/variations/subject_masks \
  --output-dir images/variations/depth_treated_review \
  --expected-count 72
```

Defaults: 10 px Gaussian background blur, saturation 0.84, brightness 0.99, contrast 0.98, a 1.5 px outward mask feather, and a subtle 0.14 background-only vignette with power 2.4. These are adjustable with `--blur-radius`, `--saturation`, `--brightness`, `--contrast`, `--feather-radius`, `--vignette`, and `--vignette-power`. Use `--overwrite` to regenerate an existing output set after review. The source images are never overwritten. Output files retain source names and dimensions; a manifest records parameters and SHA-256 digests. Review at full size before use in the collection.

A fully white mask protects every pixel; a fully black mask treats the entire image. Neither is an adequate subject mask for a flattened character illustration.

If a held object, robe, cape or sleeve is blurred, the segmentation mask is too weak in that region. Generate separate conservative review masks, then render a new review set:

```bash
python scripts/refine_subject_masks.py --expected-count 72
python scripts/apply_depth_treatment.py \
  --input-dir images/variations/complete_72 \
  --mask-dir images/variations/subject_masks_refined_review \
  --output-dir images/variations/depth_treated_refined_review \
  --expected-count 72 --blur-radius 7
```

The refinement promotes faint foreground detail near the confident subject and filters large frame-edge background fragments. It errs toward keeping more nearby pixels sharp. Inspect every full-size output and mask before approving the collection; isolated effects far from the body may still need hand correction. The original masks and source art remain intact.

After processing, the script also writes `contact_sheet.png` in the output folder. It is a labeled grid of the treated images for quick review. Set `--sheet-columns` and `--sheet-thumb` to change its layout; inspect individual PNGs at full size for mask edges.
