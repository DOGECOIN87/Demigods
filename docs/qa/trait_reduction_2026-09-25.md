# Trait reduction - 2026-09-25

The owner asked for fewer traits. Withdrawn by that decision (`scripts/withdraw_trait_reductions.py`), each with its bytes retired to `incoming/trait_reduction_2026-09-25/`, its SHA-256 in `blocked_assets`, and its backlog row closed as `withdrawn`:

| Category | Before | After | Why |
|---|---|---|---|
| Head accessories | 6 (+4 already retired) | 0 | Owner decision. |
| Front auras | 2, on every token | 0 | Owner decision. They were mandatory, so every token wore flames or light pillars across the legs, over its outfit. |
| Global finish | 3, on 75% of tokens | 0 | Owner decision. A whole-image colour wash, listed in the metadata as though it were a trait. |
| Eyebrows | 16 | 6 | Most were hidden or near-duplicates (below). |

Neck accessories were withdrawn earlier the same day. The collection now registers 132 assets.

## Eyebrows

Front hair is on every token, and it covers most of the brow. Share of each brow's line hidden under each fringe, averaged over the sixteen brows:

| Fringe | Gold parted | Black side-swept | Silver straight | Violet parted | Blue pointed | Pink soft | Teal open-centre | Red short |
|---|---|---|---|---|---|---|---|---|
| Brow hidden | 60% | 79% | 86% | 40% | 49% | 92% | 100% | 86% |

The average is 74%. What does show has to read as a different expression, and ten of the sixteen did not, measured by how much of their line two brows share and confirmed side by side on one face:

- **Kept:** neutral, raised, angry, worried, flat, quizzical. Six expressions that differ in angle, not in weight.
- **Withdrawn:**
  - pleading (a copy of worried)
  - bold raised (raised)
  - furious (angry)
  - arched and fine arched (neutral's own arch, raised)
  - thin, thick, wide-set, close-set and lowered: weight and spacing variants of neutral, invisible under a fringe

## Also changed

- `scripts/despeckle_chroma_residue.py` no longer exempts the green laurel. Its exemptions must name registered assets, and the laurel left with the head accessories.
- `optional_categories` loses `head_accessories` and `global_finish`.

## Outfits withdrawn

After a sample sheet (tokens 0004, 0005, 0010 and 0025) the owner withdrew three outfits that did not render properly, with `scripts/withdraw_outfits.py`:

| Outfit | Row | What it was |
|---|---|---|
| `outfit_005_sun_temple_pose_005.png` | DG-041 | The original sun temple layer, drawn over the bare Pose 005 base |
| `outfit_010_celestial_robe_white_gold.png` | DG-046 | The original white-and-gold robe layer, drawn over the bare Pose 001 base |
| `outfit_006_black_layered_hooded_robe_pose_004.png` | DG-165 | The black robe's Pose 004 dressed render, whose palm sits 16 px inside the base's, so the round talisman and the other palm objects hung off it |

Each one's pose binding, `hides` rule and exclusions went with it. The black robe render is marked withdrawn in `images/trait_candidates/outfits_dressed/sources.json`, so intake cannot register it again. `prompts/dressed_body_pose_pack_2026-09-25.md` now carries a prompt for a new render of it. DG-041's manifest entry had no `backlog_id`, so its row was matched by path; `withdraw_outfits.py` now always matches by path.

The collection registers 129 assets. Outfits per pose: Pose 001 five, Pose 002 five, Pose 003 five, Pose 004 four, Pose 005 four.
