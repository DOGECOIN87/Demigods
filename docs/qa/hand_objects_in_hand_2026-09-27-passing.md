# Hand-object fit review: 2026-09-27 passing set

Only items 004, 008, and 010 passed this review and were registered. The gold lantern was excluded: its generated fist shape did not cover the pose 002 base fist at an acceptable item size. It is not in the registered batch or the committed candidate-source folder.

## Checks

- Each registered layer is a 1254 x 1254 RGBA PNG with genuine transparency and no nontransparent pixels at the canvas edge.
- Each source shows the item held by a painted, wristless hand. The hand covers the base fist in the pose 002 bare-body render.
- Exact-size fit search found zero exposed core pixels of the base fist for all three selected candidates; the scepter fit has one antialiased fringe pixel outside the core.
- The full item layer remains near its previous registered height: sword 0.976x, crescent staff 1.059x, scepter 1.119x.
- Each was composited with `scripts/generate_777.py`'s production renderer on the bare pose 002 body and on all compatible pose 002 outfits (007, 008, 009). Close-ups show a clean hand/shaft contact and no duplicated base hand, wrist, or arm segment.
- Full-body and grip contact sheets: `docs/qa/hand_objects_in_hand_2026-09-27-passing-full.png` and `docs/qa/hand_objects_in_hand_2026-09-27-passing.png`.

## Registered transforms

| Item | Painted hand center (source px) | Hand width | Scale | Offset (x, y) | Layer bounds (inclusive px) |
|---|---:|---:|---:|---:|---:|
| 004 silver sword | (629.3, 958.2) | 100 px | 0.79 | (-53, 12) | (251, 122)–(501, 882) |
| 008 blue crescent staff | (906, 1012) | 165 px | 0.46 | (31, 303) | (265, 312)–(572, 1160) |
| 010 horned skull scepter | (623.6, 863.6) | 98 px | 0.76 | (-34, 116) | (340, 317)–(549, 1012) |

Transforms are reproduced by `scripts/register_in_hand_objects.py`. Source renders are preserved under `images/trait_candidates/hand_objects/in_hand_2026-09-27-pass/`.
