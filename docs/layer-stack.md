# Layer Stack

Render final tokens from back to front in this order:

1. `01_background`
2. `02_rear_aura`
3. `03_back_accessory`
4. `04_hair_back`
5. `05_base_body`
6. `06_outfit`
7. `07_neck_accessory`
8. `08_eyes`
9. `09_eyebrows`
10. `10_mouth`
11. `11_expression_marks`
12. `12_hair_front`
13. `13_head_accessory`
14. `14_hand_object`
15. `15_front_aura`
16. `16_global_finish`

Any exception must be documented in the compatibility configuration rather than handled by permanently merging traits.

Since 2026-09-25 four layers are empty by the owner's decision and render nothing: `07_neck_accessory`, `13_head_accessory`, `15_front_aura` and `16_global_finish` (`docs/qa/trait_reduction_2026-09-25.md`). They stay in the order so a category can return without renumbering.

## Hidden layers

A trait may keep a layer out of the rendered image with a `hides` rule in `config/compatibility.json`. The hidden layer is still selected and still appears in the metadata; it is only not drawn. The one use today is the dressed-body outfit - an outfit painted with the body intact - which hides `05_base_body`: the base binds the pose and the hand objects, and the dressed figure is drawn in its place. A trait that hides the base body must also `require` one. See `docs/workflows/dressed_body_intake.md`.

Hand objects are composited before the body in the render, so the hand occludes the object's grip; that order is unchanged for dressed bodies.
