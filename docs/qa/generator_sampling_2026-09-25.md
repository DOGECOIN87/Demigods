# Generator sampling - even poses, configured object rate, 2026-09-25

## The skew

`scripts/generate_777.py` drew every category independently and discarded any draw that broke a compatibility rule. That is unbiased only when every category is equally likely to survive, and hand objects are not: they fit Poses 002 and 004 alone. A draw holding an object survived only on those poses, so they were kept more often than the others.

A 770-token dry run on the registered library (`--seed dressed-bodies-dry-1`), before the change:

| | Pose 001 | Pose 002 | Pose 003 | Pose 004 | Pose 005 |
|---|---|---|---|---|---|
| Share of tokens | 19.1% | **28.4%** | 14.0% | **23.1%** | 15.3% |

Only 18.7% of tokens held an object, against `optional_categories.hand_objects` = 0.6. The old storm guardian, the one pose-002 outfit before the dressed bodies, was on three times as many tokens as the old sun temple.

## The fix

`choose_selection` now decides categories in layer order and draws each one only from the files the traits already chosen allow. A file's requirements on decided categories must be met. Nothing chosen may exclude it. A chosen trait that requires something in this category gets exactly that. Every current rule points back up the layer order: an outfit to its base pose, a hand object to its pose, front hair to its rear hair. So every draw is valid as it is made, and the pose - chosen before anything bound to it - is chosen evenly. An optional category's rate now applies to the tokens that can carry it. The final rule check stays, as a backstop for a rule that ever points down the order.

The same seed after the change:

| | Pose 001 | Pose 002 | Pose 003 | Pose 004 | Pose 005 |
|---|---|---|---|---|---|
| Share of tokens | 20.6% | 17.4% | 22.2% | 21.4% | 18.3% |

These are within sampling noise of 20% each: one standard deviation at 770 tokens is 1.4 points. Of the tokens whose pose and outfit can hold an object, 59.9% do. That is 21.6% of all tokens, because only two of five poses have objects and the black robe's Pose 002 excludes them. It took 770 attempts for 770 tokens: nothing is discarded.

The rule-valid combination count in the preflight is unaffected. It estimates how many valid combinations exist, which does not depend on how they are drawn.

## What changes for a fixed seed

Every seed produces different tokens than before, because the draws are made differently. No tokens have been minted, so nothing published depends on the old output.

Tests: `test_a_pose_bound_trait_does_not_skew_the_pose` and `test_requirements_and_exclusions_are_met_as_they_are_drawn` in `tests/test_generate_777.py`.
