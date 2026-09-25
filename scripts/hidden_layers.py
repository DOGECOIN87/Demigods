"""Which layers a selected trait keeps out of the rendered image.

An outfit painted with the body intact - a *dressed body*, see
``scripts/normalize_dressed_body.py`` - carries its own copy of the pose it was
painted in. The base body is still selected with it: the base binds the pose
(``requires``), the hand objects bind to the same base, and the metadata names
the pose through it. It is simply not drawn, because a second, bare copy of the
figure underneath would show wherever the two silhouettes differ by a pixel.

``config/compatibility.json`` records that with a ``hides`` rule:

    {"trait": "outfit_007_brown_leather_long_coat_pose_002.png",
     "hides": "base_bodies", "reason": "..."}

Everything that composites garment over base - the renderer, and the repair
scripts that measure a garment against the body under it - reads the relation
from here, so a dressed body is never measured against a body it replaces.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
COMPATIBILITY = ROOT / "config" / "compatibility.json"
BODY_LAYER = "base_bodies"


def load_rules(path: Path = COMPATIBILITY) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def hide_targets(rule: dict[str, Any]) -> list[str]:
    value = rule.get("hides", [])
    return [value] if isinstance(value, str) else list(value or [])


def hidden_categories(selected_names: Iterable[str], rules: dict[str, Any]) -> set[str]:
    """Categories that any selected trait hides."""
    names = set(selected_names)
    hidden: set[str] = set()
    for rule in rules.get("hides", []) or []:
        if isinstance(rule, dict) and rule.get("trait") in names:
            hidden.update(hide_targets(rule))
    return hidden


def dressed_outfits(rules: dict[str, Any] | None = None) -> set[str]:
    """Traits painted with the body intact: they hide the base body."""
    rules = load_rules() if rules is None else rules
    return {
        rule["trait"]
        for rule in rules.get("hides", []) or []
        if isinstance(rule, dict) and BODY_LAYER in hide_targets(rule)
    }
