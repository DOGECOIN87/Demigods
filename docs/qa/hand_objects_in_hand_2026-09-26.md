# Hand objects painted in hand - 2026-09-26

The owner asked for every held item to be drawn with the hand already gripping it, so tokens need no separate hand overlay. Copying the base's fist onto the old objects was tried first and rejected: a closed fist laid over a shaft does not read as a grip.

## What was done

- Prompts: `prompts/hand_objects_in_hand_pack_2026-09-26.md`, one per hand object, asking for the base pose's hand painted holding the item, from the wrist down.
- Seven renders arrived (1024 x 1024 RGBA); two were registered. The unedited sources are in `images/trait_candidates/hand_objects/in_hand_2026-09-26/`.
- `scripts/register_in_hand_objects.py` reduces each render so its painted hand matches the width of the base's own hand, places the painted hand's centre on the base hand's centre, and writes it over the registered asset of the same name. Every requires and excludes rule still applies. Transform details are in each manifest entry's provenance.
- Each registered render has an `in_hand` rule, so `scripts/generate_777.py` draws it over the body instead of behind it.

## Result

| Asset | Pose | Scale | Verdict |
|---|---|---|---|
| hand_object_001 arcane staff | 002 | 0.847 | registered |
| hand_object_002 violet orb | 004 | 0.490 | registered |
| hand_object_003 dark wand | 002 | - | rejected by the owner: the render's hand was drawn so large that fitting it shrank the wand by about a third |
| hand_object_004 silver sword | 002 | - | rejected by the owner, as above |
| hand_object_007 gold staff with blue gem | 002 | - | rejected by the owner, as above |
| hand_object_005 star spellbook | 004 | - | not registered: a cut-off wrist stump shows above the book |
| hand_object_006 gold lantern | 002 | - | not registered: the hand is so large the lantern ends up tiny |

Hand objects 003-012 keep their earlier art and are still drawn behind the body, where the base fist covers their grip.

Review sheet: `docs/qa/hand_objects_in_hand_2026-09-26.png` shows each registered object on the bare pose and on two dressed bodies of the same pose, with the grip enlarged underneath.
