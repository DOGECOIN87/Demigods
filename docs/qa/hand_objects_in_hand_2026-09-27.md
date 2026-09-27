# Hand objects painted in hand - 2026-09-27

Follows `docs/qa/hand_objects_in_hand_2026-09-26.md`. The six candidates in `incoming/hand_objects/with_hand_candidates_2026-09-26/` were fitted with `scripts/fit_in_hand_render.py` and checked against the acceptance list in `prompts/hand_objects_handover_2026-09-27.md`. The owner saw a before-and-after sheet of all six and approved the two recommended fits. They also asked for the registered arcane staff and violet orb to be fixed, because an edge of the body's own hand showed beside their painted hands. In the same review they approved fixing the gold staff with blue gem (007), which showed a thinner sliver.

Composite: `docs/qa/hand_objects_in_hand_2026-09-27.png`. Each row shows main before this change, the new layer on the bare body and on two dressed bodies, and the grip close up. Red marks body-hand pixels left showing.

## The 2026-09-26 candidates

| Candidate | Verdict | Why |
|---|---|---|
| 003 dark wand | registered | Scale 0.95, offset (4, 49). The painted hand is 1.20x the body's, and the wand is 0.99x its old height. The body's hand is fully covered apart from 2 edge px, and there is no painted wrist. The wand is now upright, with a silver twist and a crystal at its foot; the old wand leaned and had one crystal. |
| 005 star spellbook | registered | Scale 0.6, offset (178, 219). The painted hand is 1.24x the body's, and the book is 0.90x its old width. The layer sits 18 px lower and 6 px further left than centring would place it, so the painted fingers cover the body's fingers (2 edge px showing). The book is painted open, though the prompt asked for a closed book; the owner accepted it. |
| 004 silver sword | not registered: needs a new render | The sword is drawn about 1.25x its old length, with the hand low on the grip. At any scale where the painted fist covers the body's (0.85 and up), the blade tip runs off the top of the canvas. At 0.83 the tip is 16 px from the top and 55 core px of the body's fist show. |
| 006 gold lantern | not registered: needs a new render | The fist still carries a painted wrist stub. Its size fits (scale 0.75, body hand covered), but rule 3 of the handover says to generate the render again rather than trim it. The round-2 lantern stays. |
| 001 arcane staff | not used | A different staff from the old art (gold, with a violet crystal). Even unreduced it is 1.26x the old height, and 83 core px of the body's knuckles show. |
| 002 violet orb | not used | Unreduced, the orb is 0.44x its old height, and 360 core px of the body's palm show round the painted hand. |

## Re-fits of registered renders

Each keeps its registered render, now placed by `scripts/register_in_hand_objects.py`: batch `ROUND1_REFIT_0927` for the staff and orb, and `ROUND2_REFIT_0927` for the gold staff. Round 1 centred each painted hand on a body-hand centre 8 to 10 px higher than the measured one (see `BASE_HANDS`), so the bottom of the body's own hand showed.

| Asset | Before | After | Body hand showing |
|---|---|---|---|
| 001 arcane staff | scale 0.8471, offset (30, 218) | scale 0.93, offset (-11, 184) | 346 px (255 core) -> 2 px (0 core) |
| 002 violet orb | scale 0.49, offset (207, 378) | scale 0.49, offset (217, 384) | 396 px (266 core) -> 0 px |
| 007 gold staff with blue gem | scale 0.4, offset (85, 312) | scale 0.43, offset (58, 276) | 104 px (25 core) -> 10 px (0 core) |

The orb only moves (10 px right, 6 px down). At its old size the staff's painted fist cannot cover the body's fist wherever it is placed: the best position still showed 22 core px. So it is 9% larger, 1.06x its old height, and its foot now reaches the ankle rather than the shin. The gold staff has the same problem (21 core px at best at its old scale). It is 7.5% larger, which makes it 1.19x its old height, a little over the 1.15 guide. Its painted hand is 1.10x the body's.

The offsets were found with the new `cover` command of `scripts/fit_in_hand_render.py`. It tries every placement near a starting offset and lists those that leave the fewest body-hand pixels showing.

## Reproducing the fits

`fit --offset` pastes the reduced render at the registered offset; each command below writes a layer identical to the registered asset:

```text
python scripts/fit_in_hand_render.py fit images/trait_candidates/hand_objects/in_hand_2026-09-27/003_dark_wand.png 003 465.5 757.2 87 --scale 0.95 --offset 4 49
python scripts/fit_in_hand_render.py fit images/trait_candidates/hand_objects/in_hand_2026-09-27/005_star_spellbook.png 005 437.0 895.7 186 --scale 0.6 --offset 178 219
python scripts/fit_in_hand_render.py fit images/trait_candidates/hand_objects/in_hand_2026-09-26/001_arcane_staff_source.webp 001 491.4 634.9 88 --scale 0.93 --offset -11 184
python scripts/fit_in_hand_render.py fit images/trait_candidates/hand_objects/in_hand_2026-09-26/002_violet_crystal_orb_source.webp 002 407.0 715.8 363 --scale 0.49 --offset 217 384
python scripts/fit_in_hand_render.py fit images/trait_candidates/hand_objects/in_hand_2026-09-26/round2/007_gold_staff_with_blue_gem.png 007 906 1140 177 --scale 0.43 --offset 58 276
```

The two new sources are byte-identical copies of the candidates, renamed: `003_dark_wand.png` (SHA-256 `e7cf2041…`) and `005_star_spellbook.png` (`8d46b2eb…`), as listed in the candidates' `manifest.json`.

## Checks

Each fit was composited over the bare body and every outfit it can appear with: 007, 009, 002 and 008 for pose 002, and 007, 009, 004, 008 and 006 for pose 004. No layer touches the canvas edge, and no source was cut off at its own edge. The repository checks from `.github/workflows/production_validation.yml` pass.

## Still open

- 004 silver sword and 006 gold lantern need new renders (above).
- 009 violet blade, 010 horned skull scepter and 011 round talisman still have no usable render and keep their old art, drawn behind the body.
