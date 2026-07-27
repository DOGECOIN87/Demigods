# Demigods 777 — Modular Generative Asset System

Production specifications, category prompts, reference images, validation tools, and generation rules for a 777-piece interchangeable chibi-fantasy collection.

## Current production status

**Phase 2 uses a locked 1254 × 1254 canvas. The base-body pose family is complete, backgrounds 001–004 are registered, and hair-back 003 is the first registered character trait. There is no active blocker.**

- Live ledger: `docs/production_status.md` (the status table is generated — see below)
- Ordered asset backlog: `docs/trait-production-backlog.md`
- Intake workflow: `docs/workflows/approved_base_intake.md`
- Rig gate and coordinate guide: `docs/rig/README.md`

The approved visual design remains locked. Produce every new asset as a native 1254 × 1254 render; do not resample a rejected candidate or reconstruct the avatar from the damaged repository WebP.

## Core requirements

- Every non-background trait is a separate transparent PNG.
- Every character-compatible asset uses one locked 1254 × 1254 master canvas and shared proportionally rebased rig.
- All assets are perfectly front-facing with identical scale, anchors, proportions, and crop.
- Key light comes from the upper-left; form shadows fall toward the lower-right.
- Character names are not part of the trait system.
- Trait categories remain isolated: no baked-in unrelated layers.
- The generator creates exactly 777 unique approved outputs from the valid combination space.

## Repository structure

```text
assets/                   Canonical full-canvas production categories and source references
prompts/                  Reusable image-generation and extraction prompts
docs/                     Layer order, naming, rig, QA, workflow, and production status
images/reference_sheets/  Visual guides from the design process; never production assets
images/background_candidates/  Exact user-supplied background references awaiting native production renders
config/                   Collection and compatibility configuration
metadata/                 Token metadata schema
scripts/                  Intake, validation, configuration, generation, and output-verification tools
tests/                    Automated validator, configuration, generator, and output tests
.github/workflows/        Continuous production validation
```

## Canonical base-body paths

Production-ready neutral bodies and pose variants belong in `assets/base_bodies/`:

```text
assets/base_bodies/base_body_001_neutral_master.png
assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png
assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png
assets/base_bodies/base_pose_004_viewer_left_palm_up.png
assets/base_bodies/base_pose_005_centered_two_hand_grip.png
```

The singular `assets/base_body/` folder is a source-reference area and is excluded from production-layer discovery.

## Validation

Install dependencies and run the automated tests:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Audit the locked collection geometry and compatibility rules:

```bash
python scripts/validate_config.py \
  --collection config/collection.json \
  --compatibility config/compatibility.json \
  --assets assets \
  --json-report config_validation_report.json
```

The configuration preflight rejects changed locked anchors, malformed rules, missing trait references, duplicate relationships, impossible same-layer requirements, and requires/excludes contradictions.

Audit the current production library and preserved references:

```bash
python scripts/validate_assets.py assets \
  --manifest assets/asset_manifest.json \
  --repository-root . \
  --json-report asset_validation_report.json
```

The asset validator performs complete binary decoding and checks PNG format, dimensions, RGBA and alpha behavior, visible bounds, folder/category agreement, three-digit numbering, SHA-256 values, blocked-reference consistency, and byte-for-byte provenance for all eight background candidates.

Verify provenance for every registered production asset before treating it as usable:

```bash
python scripts/validate_manifest_consistency.py \
  --manifest assets/asset_manifest.json \
  --repository-root . \
  --json-report manifest_consistency_report.json
```

The registry currently contains ten registered assets: backgrounds 001–004, the five-member base-body pose family, and hair-back 003. The checker requires every registered file to exist at the declared production path, remain `production_ready`, match its declared SHA-256 and dimensions, and pass category-aware PNG QA.

Keep the production ledger in agreement with the manifest and the backlog:

```bash
python scripts/report_production_status.py --write   # after registering an asset
python scripts/report_production_status.py --check   # what CI enforces
```

The reporter derives per-category registered, remaining, and completion counts from `assets/asset_manifest.json` and `docs/trait-production-backlog.md`, rewrites the generated block in `docs/production_status.md`, and fails when a backlog row marked `registered` is missing from the manifest, when the manifest registers a path no backlog row claims, or when `pending_categories` names a category whose assets are all registered.

## Exact-777 generation

After the production library is complete:

```bash
python scripts/generate_777.py --preflight-only
python scripts/generate_777.py --seed <FINAL_SEED> --dry-run --output output/dry_run
python scripts/generate_777.py --seed <FINAL_SEED> --output output/final
```

The generator rejects invalid assets and stale output directories, rejects duplicate signatures, creates token IDs `0001` through `0777`, writes matching metadata, and records deterministic trait and image provenance hashes.

Audit a dry run before rendering:

```bash
python scripts/validate_output.py output/dry_run \
  --allow-dry-run \
  --json-report dry_run_validation_report.json
```

Independently verify the final render before release:

```bash
python scripts/validate_output.py output/final \
  --json-report final_output_validation_report.json
```

The output verifier requires the exact `0001`–`0777` image and metadata sets, recomputes every image hash and trait signature, validates metadata layer order and source paths, confirms final images are complete opaque RGBA PNGs, and independently recomputes both collection provenance hashes.

## Recommended workflow

Steps 1–3 are complete; the base body and its hand-pose variants are registered.

1. ~~Render and approve the Pose 001 master.~~ Done — `assets/base_bodies/base_body_001_neutral_master.png`.
2. ~~Approve hand-pose variants sequentially.~~ Done — base poses 002–005.
3. Create one isolated representative test asset from every remaining category, in canonical layer order.
4. Gate each partial trait layer with `python scripts/rig_gate_report.py --trait <file>` and confirm placement with a composite over the registered base body.
5. Composite cross-category stress-test characters.
6. Correct collisions, clipping, hidden overlaps, and layer order.
7. Produce remaining assets one item per output.
8. Validate and commit every accepted asset or small verified milestone; follow `docs/trait-production-backlog.md` and regenerate the ledger.
9. Define only necessary compatibility exclusions.
10. Dry-run, verify, render, and independently verify exactly 777 unique tokens.

## Important clarification

The trait library may contain far more than 777 mathematical combinations. The collection generator samples exactly 777 validated unique combinations rather than forcing the product of category counts to equal 777.
