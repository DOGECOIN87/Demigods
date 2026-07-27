# Rear Aura Candidates

Drop folder for `rear_auras` candidates. Intake rules: `images/trait_candidates/README.md` and `prompts/19_individual_trait_asset_co_creation.md`.

## Awaiting — DG-015 rear aura 001 blue floor ring

Generation prompt: `prompts/20_dg_015_rear_aura_001_candidate.md`

| Field | Value |
|---|---|
| Backlog ID | DG-015 |
| Expected upload | `aura_rear_001_blue_floor_ring_candidate_attempt_001.png` |
| Intended production path | `assets/rear_auras/aura_rear_001_blue_floor_ring.png` |
| Role | Rear-aura representative test — unblocks DG-016 through DG-020 |

Gate an upload before requesting approval:

```bash
python scripts/rig_gate_report.py --trait \
  images/trait_candidates/rear_auras/aura_rear_001_blue_floor_ring_candidate_attempt_001.png
```

`--trait` checks the 1254 × 1254 canvas, genuine transparency, and the locked maximum bounds `[233, 129, 1021, 1139]`. Bounds are measured from every pixel whose alpha is not exactly zero, so a soft glow that trails off at alpha 1–2 still counts. Do not use `--pose-variant`; it measures head and leg bands and only applies to full-figure base poses.

Placement is confirmed by compositing over `assets/base_bodies/base_body_001_neutral_master.png`, not by the gate.

Keep every rejected attempt under its `_attempt_###` name with the failure reason recorded. Nothing here is production-ready until binary QA, the base composite, and explicit human approval all pass.
