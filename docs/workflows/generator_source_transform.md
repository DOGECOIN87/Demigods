# Generator-Source Trait Transformation Workflow

## Purpose

This workflow permits a generator-native image to serve as **source art** for a Demigods modular trait, even when the generator cannot emit the locked 1254 × 1254 RGBA production canvas directly. It does not relax the production contract: every registered asset must still be a 1254 × 1254 PNG with a genuine transparent alpha channel, valid category-specific bounds, locked-rig placement, a human-reviewed composite, and complete provenance.

> A generator output is a **source candidate**, not a production asset. It becomes eligible for registration only after the documented transformation, all automated gates, and human composite approval.

## Scope and Boundaries

The workflow applies to isolated modular traits only. It may be used for hair, outfits, accessories, facial traits, hand objects, and effects where the source depicts a single supported backlog design. It does **not** apply to the locked base-body family, registered backgrounds, or the seven flattened legendary illustrations.

The source image must be a PNG at least 1254 pixels on each side. It may be RGB or RGBA. The transform must only remove non-art presentation pixels, normalize alpha, reduce and place the isolated asset on the locked canvas, and make narrowly-scoped edge cleanup. It may not invent missing pixels, reconstruct or redraw the asset, change the represented design, crop away meaningful trait content, upscale any source detail, or alter a source after its digest has been recorded.

## Two-File Provenance Model

| File | Location | Status | Rule |
|---|---|---|---|
| Immutable generator source | `images/trait_candidates/<category>/` | Candidate evidence | Preserve exact generator bytes, dimensions, format, and SHA-256 |
| Normalized review candidate | `incoming/` or a named review directory | Transform output | Produced only by the approved transformation script; never copied into `assets/` before QA |
| Registered production asset | `assets/<category>/` | Production ready | Exact bytes of the QA-approved normalized candidate, after manifest registration |

The manifest must record `origin: generator_source_transform`, the source path and SHA-256, source dimensions and mode, the approved transform script, its parameters, and the final production SHA-256. This makes a transformed asset as auditable as the existing refit, chroma-cleanup, extraction, clipping, and repaint precedents already present in the collection ledger.

## Required Transformation Sequence

1. **Freeze the source.** Record the source path, SHA-256, dimensions, image mode, and generator route before modifying or deriving anything.
2. **Confirm source eligibility.** Reject an image with multiple variants, a visible label, a watermark, a complete character, a baked unrelated trait, non-removable framing, or insufficient detail for a reduction-only result.
3. **Recover a clean alpha field.** Preserve existing alpha where usable. Remove only presentation background pixels or negligible alpha haze using the documented threshold or approved checkerboard/matte recovery method. The process must not use generic background removal to hallucinate a hair, garment, or object edge.
4. **Isolate and reduce.** Crop only transparent margins, reduce the isolated source content with a high-quality downsampling filter, and place it on a transparent 1254 × 1254 canvas at the approved locked-rig coordinates. Upscaling is forbidden.
5. **Gate the normalized candidate.** Run binary QA and the category-specific rig gate. A normalizer output that is out of bounds, retains a matte, loses meaningful content, or requires scaling up is rejected.
6. **Composite and review.** Composite over the registered base, and for the hair-plus-face pilot also inspect a registered outfit and contrasting backgrounds. Approval remains a human art-direction decision after the automated checks pass.
7. **Register atomically.** Use the batch intake path only after review. The manifest provenance must state the transform and source digest; the backlog, ledger, compatibility rules, and asset directory must update together.

## Transformation Safety Limits

| Control | Requirement |
|---|---|
| Final canvas | Always exactly 1254 × 1254 RGBA PNG with genuine transparent alpha |
| Source scaling | Reduction only; `scale < 1.0`; no upscale or synthetic resolution recovery |
| Placement | Centered on the locked rig unless a category-specific offset is documented |
| Alpha cleanup | A documented threshold may remove negligible haze; all stronger edge recovery requires a recorded method and visual review |
| Presentation matte | Uniform green/black/white or known checkerboard may be removed only when it is demonstrably external to the trait; unresolved matte is a rejection |
| Provenance | Source and normalized SHA-256s, dimensions, mode, script, arguments, and approval record are mandatory |
| Human review | Required for every transformed candidate; automation alone cannot approve art direction or edge fidelity |

## Generator Prompt Guidance

Future prompts should still request a native transparent 1254 × 1254 PNG, because that remains the best path. When a generator cannot provide it, it may return one large, isolated source-art PNG with no text, watermark, border, collage, or duplicate. The source must have generous clean margins around the trait and must not contain a full character or checkerboard deliberately painted into the asset. The pipeline will then perform the controlled reduction-and-rigging step described here.

## Operational Rule

The final validators remain strict. This workflow changes **how source art enters intake**, not the conditions under which it can be registered. A transformed candidate that fails alpha, bounds, rig, composite, or art-direction review remains rejected.
