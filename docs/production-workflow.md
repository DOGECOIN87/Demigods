# Production Workflow

## Current gate

Production is blocked at the approved neutral master. Follow `docs/production_status.md` and Issue #4 before creating character-aligned assets. Never approximate the locked avatar from the damaged WebP or reference-sheet previews.

## Sequential production order

1. Restore and approve `assets/base_bodies/base_body_001_neutral_master.png`.
2. Determine whether the approved neutral master already satisfies `base_pose_001_relaxed_open.png`.
3. Register the same underlying artwork when eligible; otherwise change only the required arm and hand pixels.
4. Approve pose variants 002 through 005 in order.
5. Produce one isolated test asset from each remaining category in the locked production order.
6. Build cross-category stress-test composites to expose seams and collisions.
7. Correct anchors, hidden overlaps, layer order, and only necessary compatibility rules.
8. Produce each remaining trait individually, one file per output.
9. Freeze the approved production folders and record the final deterministic seed.
10. Run an exact-777 dry run, then the final render.
11. Confirm 777 images, 777 metadata files, 777 unique trait signatures, and provenance hashes.

## Per-asset repository loop

For every accepted asset:

1. Save it directly in its canonical `assets/<category>/` directory.
2. Update `assets/asset_manifest.json`.
3. Update `docs/production_status.md`.
4. Update `config/compatibility.json` only when a verified collision requires it.
5. Run the validator.
6. Commit with a specific asset-focused message.
7. Push and verify the exact path in the repository.
8. Continue to the next sequential asset.

Do not accumulate uncommitted batches of finished assets. Repository progress should be recorded after each accepted asset or small verified infrastructure milestone.

## Validation commands

During preproduction, while canonical production folders are empty:

```bash
python scripts/validate_assets.py assets \
  --manifest assets/asset_manifest.json \
  --repository-root . \
  --allow-empty \
  --json-report validation_report.json
```

After the first production asset exists, remove `--allow-empty`:

```bash
python scripts/validate_assets.py assets \
  --manifest assets/asset_manifest.json \
  --repository-root . \
  --json-report validation_report.json
```

The validator checks complete binary decoding, PNG format, dimensions, RGBA and alpha behavior, visible bounds, folder/category agreement, three-digit numbering, SHA-256 values, and manifest consistency.

## Generator commands

Preflight the completed library without writing outputs:

```bash
python scripts/generate_777.py --preflight-only
```

Prepare deterministic signatures and metadata without rendering images:

```bash
python scripts/generate_777.py \
  --seed <FINAL_SEED> \
  --dry-run \
  --output output/dry_run
```

Render the final collection only after the dry run passes:

```bash
python scripts/generate_777.py \
  --seed <FINAL_SEED> \
  --output output/final
```

Use `--overwrite` only when intentionally replacing an entire previous generator output directory. The generator rejects stale non-empty output directories by default.

## Asset approval gate

An asset is not production-ready until it has:

- exact 2048 × 2048 dimensions
- correct full-canvas anchor placement
- complete binary decoding with no truncation or damaged frames
- PNG format and true transparency where required
- no unrelated category pixels
- matching upper-left lighting and lower-right form shadows
- clean edges and sufficient hidden overlap
- a category-correct lowercase snake-case filename with a three-digit sequence
- successful compositing with unrelated traits
- a passing automated validation report
- manifest and production-status entries

## Binary upload rule

Use normal Git binary blob/tree/commit operations or another supported binary upload method. Never keep base64 chunks, temporary reconstruction files, workflow artifacts, or screenshots as permanent production assets.
