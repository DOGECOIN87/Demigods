# Handover: the next hand-object renders (hand and item painted together)

Written 2026-09-27 for whoever picks up the held items next, whether a person or an AI session. The block below can be pasted into a new session as its brief. The rest of the file is the detail it points to.

## Brief to paste

```text
You are continuing the Demigods held-item work in the DOGECOIN87/Demigods repository.

Goal: every hand object (hand_object_001 to 012) is one transparent 1254 x 1254 layer showing the item together with the hand that holds it, painted as one piece, so tokens need no separate hand overlay. The layer is drawn OVER the body, so the painted hand covers the body's own hand.

Read first: prompts/hand_objects_handover_2026-09-27.md (this file), then prompts/hand_objects_in_hand_pack_2026-09-26.md (the generator prompts) and docs/qa/hand_objects_in_hand_2026-09-26.md (what was accepted and rejected, and why).

Rules the owner has set:
1. The hand is painted holding the item. Pasting the body's fist over an item was rejected.
2. The hand is the body's size: the body's own hand measures 69 px wide for the pose 002 fist and 90 px for the pose 004 open palm, on the 1254 canvas (the prompts ask for about 72 and 98 px, so the painted hand covers it). The item keeps its old size. Renders with big hands were rejected, because shrinking them to fit also shrank the item.
3. No wrist. The hand stops at the base of the palm with a soft, unlined edge, and the body supplies the wrist and forearm. Painted wrists never lined up with the body's arm (sideways stumps, outlines across the wrist, hands turned the wrong way). Do not trim a painted wrist off afterwards. If a render has one, generate it again.
4. Show the owner samples before changing assets, and merge only when the owner explicitly says so.

Your job: generate or collect renders for the items still on their old art (003, 004, 005, 009, 010, 011) and fit the six candidates already in incoming/hand_objects/with_hand_candidates_2026-09-26/. That folder's README says to trim wrist stubs; that is superseded by rule 3, so the gold lantern candidate (006) needs a new render instead. Fit each render with scripts/fit_in_hand_render.py, check it against the acceptance list in the handover file, show the owner a before-and-after sheet, and register the approved ones with scripts/register_in_hand_objects.py. Then run the repository checks and open a pull request.
```

## Where things stand (2026-09-27)

The candidates README in `incoming/hand_objects/with_hand_candidates_2026-09-26/` asks for wrist stubs to be trimmed. That step was dropped at the owner's request on 2026-09-27: a render with a painted wrist is generated again. Of the six candidates, only the lantern (006) has one.

| Item | Pose | Now on main | Next step |
|---|---|---|---|
| 001 arcane staff | 002 fist | painted-in-hand render, registered (round 1) | Optional: compare with the new candidate in `incoming/` |
| 002 violet crystal orb | 004 palm | painted-in-hand render, registered (round 1) | Optional: compare with the new candidate in `incoming/` |
| 003 dark wand | 002 fist | old art, drawn behind the body's fist | Fit the new candidate. Every earlier render had a sideways wrist or a hand that was too big. |
| 004 silver sword | 002 fist | old art | Fit the new candidate. The round-3 render had the right size, but its wrist pointed sideways and a stump stuck out past the arm. |
| 005 star spellbook | 004 palm | old art | Fit the new candidate. Earlier hands were as wide as the book. |
| 006 gold lantern | 002 fist | painted-in-hand render, registered (round 2) | Its flat, outlined wrist cut is the kind of join the owner dislikes. The new candidate still has a wrist stub, so regenerate it without a wrist rather than trimming it. |
| 007 gold staff with blue gem | 002 fist | registered (round 2) | Done unless the owner asks again |
| 008 blue crescent staff | 002 fist | registered (round 2) | Done unless the owner asks again |
| 009 violet blade | 002 fist | old art | New render. Round 2 was marginal (chunky fist, blade a quarter short), and the owner chose to wait for a rerender. |
| 010 horned skull scepter | 002 fist | old art | New render. Round 3 was the right size, but a corner of the body's own fist showed above the painted hand. The fist should be taller than it is wide, with the wrist running up toward the forearm. |
| 011 round talisman | 004 palm | old art | New render. Round 3 drew a closed fist as wide as the charm. The next one needs an open palm-up hand with the ring across it, a disc about 160 px across (wider than the hand), and no blue rim light. |
| 012 brown tome | 004 palm | registered (round 2) | Done unless the owner asks again |

A registered item is drawn over the body because `config/compatibility.json` lists it under `in_hand`. Items without that rule are still drawn behind the body, where the body's fist covers their grip.

Open pull request #29 removes all hand objects by an earlier owner decision. It conflicts with this work, and the owner decides which way that goes.

## Generating

Use `prompts/hand_objects_in_hand_pack_2026-09-26.md`. It has one prompt per item, updated on 2026-09-26 to ask for no wrist. Each prompt takes two images, attached in this order:

1. The base pose: `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` for fist items, or `assets/base_bodies/base_pose_004_viewer_left_palm_up.png` for palm items. This is the alignment guide for the hand's place, size and skin.
2. The item's design. Use the item's asset as it was before the in-hand work (`git show 788454a:assets/hand_objects/<name>.png`), because the registered in-hand versions already include a hand.

The project's shared files hold the same prompts and images packed one folder per item, as `handheld_items/hand_objects_generator_kit_no_wrist.zip`.

What a usable render looks like:

- **Canvas:** a 1254 x 1254 transparent PNG containing only the hand and the item. No arm, sleeve, body, background or shadow.
- **Hand size and place:** the hand sits where the body's hand is, at the same size or a touch larger so it covers it. The prompts put the fist (pose 002) at the grip point (438, 772), about 72 px wide, and the open palm (pose 004) at (438, 748), about 98 px wide. The body's own hand skin measures 69 px wide, centred (447, 768), for the fist, and 90 px wide, centred (446, 739), for the palm. The body's wrist line runs roughly from (443, 722) to (487, 740) in pose 002, and from (452, 700) to (497, 718) in pose 004.
- **No wrist:** the hand stops at the base of the palm. Its edge there has no outline, no rim light and no cap. The back of the hand turns toward the elbow as in the base pose and never points sideways.
- **Item at its old size:** the size of each item before the in-hand work, in canvas px:

| Item | Old size (w x h) | Item | Old size (w x h) |
|---|---|---|---|
| 001 arcane staff | 246 x 841 | 007 gold staff | 195 x 639 |
| 002 violet orb | 180 x 220 | 008 crescent staff | 253 x 816 |
| 003 dark wand | 191 x 789 | 009 violet blade | 226 x 768 |
| 004 silver sword | 191 x 780 | 010 skull scepter | 203 x 622 |
| 005 star spellbook | 230 x 161 | 011 round talisman | 170 x 229 |
| 006 gold lantern | 174 x 398 | 012 brown tome | 310 x 133 |

- **Grip:** shafts and blades enter the top of the fist and leave the bottom in one straight line, with the fingers wrapped over them. Palm items rest on or hang from an open, palm-up hand, never from a closed fist.
- **Light:** the hand gets no rim light, so no blue or white glow runs round its outline.

Keep every raw render unedited. Commit the sources you register under `images/trait_candidates/hand_objects/<batch folder>/`. The registration script re-reads every source on each run, so they must stay committed. (`incoming/` ignores image files; the 2026-09-26 candidates there were force-added with `git add -f`.)

## Fitting

`scripts/fit_in_hand_render.py` is the tool the round-2 items (006, 007, 008 and 012) were fitted with, and it reproduces them pixel for pixel. The round-1 items (001, 002) came from an older width-matching fit inside `scripts/register_in_hand_objects.py`. The tool never writes into the repository: `fit` writes to `/tmp/in_hand_fits/ITEM`, and `overview` and `zoom` to `/tmp/in_hand_fits/<source name>`, unless `--out` is given.

1. Find the painted hand. Run `python scripts/fit_in_hand_render.py overview SOURCE`, then `zoom SOURCE x0 y0 x1 y1` on the hand.
2. Measure it with `python scripts/fit_in_hand_render.py measure SOURCE POSE x0 y0 x1 y1` on a box round the painted hand. Keep the box tight: cream pages and parchment count as skin. The painted hand's skin centre and width are CX, CY and WIDTH, in source px. The same command prints the body hand's numbers: for pose 002, centre (447.2, 768.1) and width 69; for pose 004, centre (446.2, 738.5) and width 90.
3. Fit it with `python scripts/fit_in_hand_render.py fit SOURCE ITEM CX CY WIDTH [--scale S] [--tag T]`. Without `--scale`, the hand is matched to the body's hand width. Try a few scales and compare the review sheets and metrics. Scale is 1 or below, because renders are only ever reduced. Scale 1 is placement only, for a render already drawn at the body's size. A render drawn smaller than the body needs a new render; it cannot be enlarged.
4. The metrics that decide a fit:
   - `painted_hand_vs_body_hand_width` at most about 1.2.
   - `item_height_vs_old` roughly 0.9 to 1.15. It compares the whole layer with the item's old art (commit 788454a). For palm items the painted hand hangs below the item and is counted too, so there judge the item itself on the review sheet, whose first tile is the old art.
   - `body_hand_core_pixels_showing` near 0. Anything that shows of the body's own fingers reads as a second hand.
   - `touches_canvas_edge` and `source_touches_edge` false. The second catches a render whose item was already cut off at its own edge.

The tool treats renders the same way registration does. Alpha below 16 is dropped and specks smaller than 0.2% of the largest piece are removed before fitting. After fitting, alpha of 250 or more is set to 255. So the layer it writes is exactly what registration will write.

## Checks before asking the owner

Composite each fit over the bare body and the outfits it can appear with. The review sheet shows two outfits; check the rest by hand. For pose 002 those are outfits 007, 009, 002 and 008 (outfit 006 excludes every pose-002 item). For pose 004 they are outfits 007, 009, 004, 008 and 006. Outfits 007, 008, 009 and 006 are dressed bodies that hide the base body; outfits 002 and 004 are drawn over it.

Reject the render, and ask for a new one, if any of these show:

- a painted wrist, a stump beside the arm, or an outline or rim running across the wrist;
- a hand noticeably bigger than the body's, or an item noticeably smaller than its old art;
- the body's own knuckles or fingers peeking out beside the painted hand;
- a hand that doesn't meet the body's forearm at the same angle and width;
- the item floating beside the hand instead of passing through it, or a closed fist on a palm-up item;
- halos, speckle, glow outlines, or anything touching the canvas edge.

Then send the owner one before-and-after sheet (old art next to the new fit, bare and dressed) and wait for their choice.

## Registering an approved fit

`scripts/register_in_hand_objects.py` writes a fit over the registered asset of the same name and updates everything that depends on it. It stores the new SHA-256 and provenance in `assets/asset_manifest.json`, sets the item's `requires` reason, and adds an `in_hand` rule in `config/compatibility.json`. It can be run again safely.

To add renders, add an entry to `BATCHES` in that script. Each entry has the batch's source folder, the decision date, its QA note and composite, and an item table with the same fields as `ROUND2_ITEMS`: source file, pose, painted-hand centre and width in source px, and the chosen scale and offset (the fit tool prints the offset). Batches apply in order, so a later batch's render of an item replaces an earlier one. Then run `python scripts/register_in_hand_objects.py`. Record the batch and its verdicts in its QA note, and link that note from `docs/qa/hand_objects_in_hand_2026-09-26.md`.

Run the same checks CI runs (`.github/workflows/production_validation.yml`) before opening the pull request:

```text
python -m json.tool assets/asset_manifest.json > /dev/null
python -m json.tool config/collection.json > /dev/null
python -m json.tool config/compatibility.json > /dev/null
python -m json.tool metadata/schema.json > /dev/null
python -m compileall -q scripts tests
python -m unittest discover -s tests
python scripts/validate_config.py --collection config/collection.json --compatibility config/compatibility.json --assets assets
python scripts/validate_assets.py assets --manifest assets/asset_manifest.json --repository-root . --allow-empty
python scripts/validate_manifest_consistency.py --manifest assets/asset_manifest.json --repository-root .
python scripts/report_production_status.py --manifest assets/asset_manifest.json --backlog docs/trait-production-backlog.md --status-doc docs/production_status.md --check
```

## Mistakes already made (don't repeat them)

- Pasting the body's fist over an old item: it doesn't read as a grip.
- Hands drawn big to show the grip: they had to be shrunk, and the item shrank with them.
- Painted wrists: they pointed sideways, stuck out as stumps, or drew an outline across the forearm. Trimming them off afterwards was tried and dropped at the owner's request.
- A closed fist for palm-up items (011): the body's pose is an open palm.
- Rim light on the hand: it shows as a glowing outline against the body.
