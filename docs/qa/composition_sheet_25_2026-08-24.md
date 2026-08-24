# Composition review sheet — 25 sampled tokens, 2026-08-24

Rendered with `scripts/render_composition_sheet.py` against the 85 registered
assets on `main` at `e466928`.

```bash
python scripts/render_composition_sheet.py --count 25 --seed review-2026-08-24 \
  --out docs/qa/composition_sheet_25_2026-08-24.png \
  --json-report docs/qa/composition_sheet_25_2026-08-24.json
```

- Sheet: `docs/qa/composition_sheet_25_2026-08-24.png`
- Per-cell selections: `docs/qa/composition_sheet_25_2026-08-24.json`

Cells are sampled with the generator's own `choose_selection`, `violates_rules`
and layer order, so every cell is a token the real 777 run could emit. They are
deduplicated by trait signature and the seed is recorded, so the sheet
regenerates byte-for-byte.

## Finding 1 — eight of ten outfits and three of five poses are unreachable

Across 25 cells only **two outfits** and **two base poses** appear:

| Category | Distinct in 25 cells | Registered |
|---|---:|---:|
| `outfits` | 2 | 10 |
| `base_bodies` | 2 | 5 |
| `backgrounds` | 8 | 8 |
| `hair_front` | 8 | 8 |
| `hair_back` | 8 | 8 |
| `neck_accessories` | 8 | 8 |
| `back_accessories` | 8 | 8 |
| `rear_auras` | 11 | 18 |
| `hand_objects` | 7 | 7 |

This is not sampling luck. It is forced by three rules that are individually
correct and collectively fatal:

1. Every outfit requires one specific base pose — six of them (`outfit_001`,
   `006`, `007`, `008`, `009`, `010`) require `base_body_001_neutral_master.png`.
2. Every registered hand object requires `base_pose_002` or `base_pose_004`.
   All twelve backlog hand objects are authored for those two poses; poses 001,
   003 and 005 have no hand object and none is queued.
3. `hand_objects` is **not** in `optional_categories`, so every token holds one.

Rule 3 forces the pose to 002 or 004, which forces the outfit to `outfit_002` or
`outfit_004`. Poses 001, 003, 005 and eight registered, human-approved outfits
can never appear in any of the 777 tokens.

The generator preflight does not catch this. It reports a rule-valid space of
2,451,456 and 0.0% saturation, because the space stays enormous while collapsing
onto two outfits — a count of combinations says nothing about how many distinct
*characters* a viewer can tell apart.

### The fix is a config decision, not an asset

Completing the hand-object category will not help: all twelve are pose-002/004.
Making `hand_objects` optional is the only route to the other three poses. A
sheet re-rendered at the same seed with `--optional hand_objects=0.45` reaches
**8 of 10 outfits and 5 of 5 poses**, unlocking the eight stranded outfits with no
new art.

```bash
python scripts/render_composition_sheet.py --count 25 --seed review-2026-08-24 \
  --optional hand_objects=0.45
```

This changes what the collection *is* — whether every Demigod holds an object —
so it is left as a decision rather than applied. The two candidate routes:

- add `"hand_objects": <p>` to `optional_categories` in `config/collection.json`; or
- commission hand objects for poses 001, 003 and 005 and add the backlog rows.

Note for whoever sets `p`: the generator selects independently and then rejects
rule violations, so a constrained optional category lands far below its nominal
rate. At `p = 0.45` only 2 of 25 accepted cells carried a hand object (~8%),
because a drawn hand object usually conflicts with the independently drawn
outfit and the whole composition is discarded. Set `p` against the observed rate
in a sheet, not the configured number.

## Finding 2 — every token has the same face

`eyes`, `eyebrows`, `mouths`, `expression_marks` and `head_accessories` have zero
registered assets, so those layers are absent from all 25 cells. The face in
every cell is the one baked into `base_body_001_neutral_master.png`, which
`prompts/16_native_1254_pose_001_candidate.md` line 55 specifies as "large
smooth bald head, large warm-brown eyes, small nose, and gentle closed-mouth
smile". All 777 tokens would ship with identical warm-brown eyes.

The 60 queued facial assets (24 eyes, 16 eyebrows, 12 mouths, 8 expression
marks) are layers **8–11**, above the base body at layer 5, so they must paint
over that baked face rather than onto blank skin. Measured occlusion envelope on
the registered master (alpha > 200, luminance < 140):

| Baked feature | Viewer-left | Viewer-right | Combined |
|---|---|---|---|
| Eyebrows | X 466–584, Y 309–322 | X 671–790, Y 309–322 | X 466–790, Y 309–322 |
| Eyes | X 452–585, Y 339–422 | X 669–803, Y 339–422 | X 452–803, Y 339–422 |
| Mouth | — | — | X 606–649, Y 436–441 |

The eye artwork is symmetric about X 627.5 to within half a pixel and sits on
the locked eye line Y 367; the mouth sits on the locked mouth centre Y 441. A
replacement eye layer that covers less than X 452–803 × Y 339–422 will leave the
baked lashes or iris visible around it. `rig_gate_report.py --trait` checks
canvas, transparency and maximum bounds — it does not check occlusion, so this
would pass the gate and fail on the sheet.

Before the 60-asset facial batch is generated, one of these has to be settled:

- author the facial traits to fully cover the envelope above, and gate them on it; or
- produce a face-free base master and re-register the base family against it.

The second is cleaner and matches the stated contract ("Trait categories remain
isolated: no baked-in unrelated layers", and DG-001's "neutral bald ... mannequin
master"), but it re-opens the base body that Issue #4 closed and invalidates the
registered pose family. The first is cheaper and preserves every registered
asset. This is a design call.

## What the sheet does not flag

Backgrounds, hair pairs, neck accessories and back accessories all read as eight
distinct assets and composite cleanly in canonical layer order. Front auras
appear on every cell because `front_auras` is also non-optional, but with only
two registered assets this reads as a repeated overlay rather than a defect —
worth revisiting when the category grows.
