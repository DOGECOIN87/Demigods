# Hand objects painted in hand - 2026-09-26

The owner asked for every held item to be drawn with the hand already gripping it, so tokens need no separate hand overlay. Copying the base's fist onto the old objects was tried first and rejected: a closed fist laid over a shaft does not read as a grip.

## What was done

- Prompts: `prompts/hand_objects_in_hand_pack_2026-09-26.md`, one per hand object, asking for the base pose's hand painted holding the item, from the wrist down.
- Seven renders arrived (1024 x 1024 RGBA); two were registered. The unedited sources are in `images/trait_candidates/hand_objects/in_hand_2026-09-26/`.
- `scripts/register_in_hand_objects.py` reduces each render so its painted hand matches the width of the base's own hand, places the painted hand's centre on the base hand's centre, and writes it over the registered asset of the same name. Every requires and excludes rule still applies. Transform details are in each manifest entry's provenance.
- Each registered render has an `in_hand` rule, so `scripts/generate_777.py` draws it over the body instead of behind it.

## Round 1

| Asset | Pose | Scale | Verdict |
|---|---|---|---|
| hand_object_001 arcane staff | 002 | 0.847 | registered |
| hand_object_002 violet orb | 004 | 0.490 | registered |
| hand_object_003 dark wand | 002 | - | rejected by the owner: the render's hand was drawn so large that fitting it shrank the wand by about a third |
| hand_object_004 silver sword | 002 | - | rejected by the owner, as above |
| hand_object_007 gold staff with blue gem | 002 | - | rejected by the owner, as above |
| hand_object_005 star spellbook | 004 | - | not registered: a cut-off wrist stump shows above the book |
| hand_object_006 gold lantern | 002 | - | not registered: the hand is so large the lantern ends up tiny |

## Round 2

The owner generated all twelve again (1920 x 1920 PNG) from the updated prompts, which give the hand's and the item's size in pixels. Each render was fitted by one reviewer, who compared a hand-matched fit, an item-size fit and a compromise on the bare body and two dressed bodies, and then re-judged by a second reviewer who tried to refute the verdict. The renders carry faint speckle and never reach full alpha, so the registration script drops alpha below 16 and specks under 0.2% of the largest piece before fitting, and sets alpha of 250 or more to 255 after fitting.

| Asset | Scale | Item vs old | Hand vs body's hand | Verdict |
|---|---|---|---|---|
| 006 gold lantern | 0.251 | 0.99 | 1.14 | registered |
| 007 gold staff with blue gem | 0.400 | 1.11 | 1.03 | registered |
| 008 blue crescent staff | 0.435 | 0.98 | 1.04 | registered |
| 012 brown tome | 0.186 | 0.84 (about the old size on screen; the old book was partly hidden behind the body) | 1.21 | registered |
| 009 violet blade | 0.33 | 0.76 | 1.31 | not registered, marginal: the fist is chunky and the blade about a quarter shorter |
| 010 horned skull scepter | 0.40 | 1.17 | 1.07 | not registered, marginal: a thin edge of the body's own knuckles shows beside the painted fist when zoomed |
| 001 arcane staff | - | - | - | round 1 version kept: the round 2 staff leans more and its foot lands on the character's foot |
| 002 violet orb | - | - | - | round 1 version kept: the round 2 orb is drawn small in a large hand |
| 003 dark wand | - | - | - | needs a new render: the painted wrist points sideways, so a cut-off wrist sticks out beside the arm |
| 004 silver sword | - | - | - | needs a new render: same sideways wrist, and the fist must be drawn 1.5x too big to cover the body's |
| 005 star spellbook | - | - | - | needs a new render: the hand is as wide as the book |
| 011 round talisman | - | - | - | needs a new render: the wrist sits off the arm and the fist is 1.5x too big |

Only the round-2 sources that were registered are kept, under `images/trait_candidates/hand_objects/in_hand_2026-09-26/round2/`.

Hand objects 003, 004, 005, 009, 010 and 011 keep their earlier art and are still drawn behind the body, where the base fist covers their grip.

Review sheet: `docs/qa/hand_objects_in_hand_2026-09-26.png` shows every registered object on the bare pose and on two dressed bodies of the same pose, with the grip enlarged underneath.

## Round 3 and after

Rerenders of the silver sword, horned skull scepter and round talisman were fitted and not registered. The sword's painted wrist pointed sideways, leaving a stump beside the arm. The scepter, fitted at the item's old size, left a corner of the body's own fist showing above the painted hand. The talisman was painted in a closed fist as wide as the charm. Their sources are not kept.

The owner then found painted wrists anatomically wrong in general and asked for renders without them. The prompt pack now stops the hand at the base of the palm. Trimming wrists off existing renders was tried and dropped at the owner's request. Six more candidates the owner generated are in `incoming/hand_objects/with_hand_candidates_2026-09-26/`, not yet fitted. The next steps are in `prompts/hand_objects_handover_2026-09-27.md`.
