# Production Workflow

1. Approve `base_body_001_neutral_master.png`.
2. Lock the shared rig, canvas, camera, proportions, and lighting.
3. Approve the required hand-pose variants without changing the body structure.
4. Produce one test asset from every category.
5. Build cross-theme stress-test composites to expose seams and collisions.
6. Correct category anchors, hidden overlaps, and layer order.
7. Rebuild each remaining trait individually from the reference material.
8. Run `scripts/validate_assets.py assets` and correct every failure.
9. Add only necessary exclusions and requirements to `config/compatibility.json`.
10. Freeze the approved production folders and record the final seed.
11. Run `scripts/generate_777.py --seed <FINAL_SEED>`.
12. Confirm exactly 777 image files, 777 metadata files, no duplicate signatures, and one provenance hash.

## Asset approval gate

An asset is not production-ready until it has:

- exact 2048×2048 dimensions
- correct full-canvas anchor placement
- true transparency where required
- no unrelated category pixels
- matching upper-left lighting and lower-right form shadows
- clean edges and sufficient hidden overlap
- an approved lowercase snake-case filename
- successful compositing with unrelated traits
