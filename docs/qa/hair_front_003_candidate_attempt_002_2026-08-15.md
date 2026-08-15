# QA — Hair-front 003 candidate attempt 002

**Date:** 2026-08-15
**Backlog ID:** DG-117
**Category:** `hair_front`
**Candidate:** `images/trait_candidates/hair_front/hair_front_003_silver_straight_bangs_candidate_attempt_002.png`
**Intended production path:** `assets/hair_front/hair_front_003_silver_straight_bangs.png`

## Result

**Rejected at intake. Do not crop, resize, key, extract, or register this candidate.**

This attempt used the enabled high-fidelity generation route and explicitly specified the collection’s required native canvas, transparent alpha, isolated trait scope, and locked placement. The returned file was instead an opaque RGB PNG at 2048 × 2048 pixels with a rendered checkerboard background. It therefore fails both the native-canvas and genuine-transparency requirements before any art-direction or compositing review can occur.

| Check | Required | Observed | Result |
|---|---|---|---|
| Canvas | Native 1254 × 1254 | 2048 × 2048 | Fail |
| Image mode | RGBA with genuine alpha | RGB, no alpha channel | Fail |
| Canvas background | Fully transparent outside trait | Baked checkerboard | Fail |
| SHA-256 | Recorded provenance | `453fd2ed8633207f8bb841d74684a1d57eb776431b3f1bac3ce985eb73af394b` | Recorded |
| Production status | Eligible only after all gates | Not eligible | Rejected |

This second result confirms that the enabled route does not currently provide the native 1254 × 1254 RGBA output control required for the Demigods modular-production pipeline. The output is retained only as a failed candidate record; it must not be remediated through background removal or resampling because both actions violate the locked collection policy.
