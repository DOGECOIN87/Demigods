# Celestial Scholar dressed-body attempts — 2026-10-01

The owner needs the active garment-only families 001, 003, 004, 005 and 010
as dressed bodies across all five poses. Storm Guardian 002 remains withdrawn;
neckwear remains omitted. No production asset or compatibility rule changed
in this checkpoint.

Two native 1254 × 1254 transparent RGBA attempts for family 001 / Pose 001
were generated from the registered base pose, an approved dressed-body format
example and the existing Celestial Scholar garment design. Neither passed
intake, so neither was added to production.

| Attempt | Normalizer scale (head / body) | Face pixels off head / on outline | Decision |
|---|---:|---:|---|
| 01 (`957eeb92…`) | 0.9302 / 0.8971 | 727 / 474 | Rejected: off-head ceiling 600 |
| 02 (`18ee90b7…`) | 1.0000 / 0.8871 | 1,352 / 824 | Rejected: both ceilings 600 |

The two runs' silhouette and face sheets showed why passing native dimensions
and visual resemblance alone are insufficient. The second edit made the shared
facial-trait fit worse. Neither render is approved or registered.
The five-family gap therefore remains 25 dressed-body renders.

For the next generation attempt, keep the *registered base's lower cheek and
chin contour* exactly. Generate each pose as a separate transparent image,
then run `scripts/intake_dressed_bodies.py` before requesting approval. The
source files must not be resized or substituted for production when the face
gate fails.

## Collection roster gate

`python scripts/audit_collection_roster.py` reports the 72 current variations,
seven separately registered legendary pieces, one historical 1254 PNG, four
historical 1024 WebPs and one JPEG reference. The 77 files in the variations
tree are not 77 current unique collectible PNGs. The current generator still
reserves seven IDs and makes 770 generative tokens.

The optional `--roster path/to/selection.json` gate validates an explicit
selection for **700 generative + 77 one-of-one**: exactly 77 unique token IDs,
distinct source PNGs, full decode and native 1254 × 1254 dimensions. Example
schema:

```json
{
  "generative_count": 700,
  "one_of_ones": [
    {"token_id": 1, "source": "images/variations/complete_72/Demigods_001_Dawnforge.png"}
  ]
}
```

The example intentionally fails until all 77 choices are made. It does not
change `config/collection.json`, assign token IDs, or treat the old WebPs and
JPEG reference as finished pieces. The 72 corrected depth exports remain
review candidates pending a final art and roster decision.
