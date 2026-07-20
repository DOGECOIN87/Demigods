# Demigods 777 — Modular Generative Asset System

Production specifications, category prompts, reference images, validation tools, and generation rules for a 777-piece interchangeable chibi-fantasy collection.

## Core requirements

- Every non-background trait is a separate transparent PNG.
- Every character-compatible asset uses one locked 2048×2048 master canvas and shared rig.
- All assets are perfectly front-facing with identical scale, anchors, proportions, and crop.
- Key light comes from the upper-left; form shadows fall toward the lower-right.
- Character names are not part of the trait system.
- Trait categories remain isolated: no baked-in unrelated layers.
- The generator creates exactly 777 unique approved outputs from the valid combination space.

## Repository structure

```text
prompts/                  Reusable image-generation and extraction prompts
docs/                     Layer order, naming, rig, and collection rules
images/reference_sheets/  Source and concept sheets from the design process
scripts/                  Validation utilities
```

## Recommended workflow

1. Approve the neutral master base.
2. Lock the rig coordinates and lighting.
3. Approve hand-pose variants.
4. Create one test asset from every category.
5. Composite a cross-theme stress-test character.
6. Correct collisions, clipping, and layer order.
7. Produce the remaining assets one item per output.
8. Validate dimensions, alpha, bounds, and file naming.
9. Define compatibility exclusions.
10. Generate token IDs `0001` through `0777`, rejecting duplicate trait signatures.

## Important clarification

The trait library may contain far more than 777 mathematical combinations. The collection generator should sample exactly 777 validated unique combinations rather than artificially forcing the product of category counts to equal 777.
