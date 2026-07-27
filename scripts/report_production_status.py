#!/usr/bin/env python3
"""Derive the live Demigods production ledger from the manifest and trait backlog."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

BEGIN_MARKER = "<!-- BEGIN GENERATED PRODUCTION LEDGER -->"
END_MARKER = "<!-- END GENERATED PRODUCTION LEDGER -->"

# The README carries a shorter summary. It drifted twice while the ledger block
# stayed correct, because prose counts are not derived from anything.
README_BEGIN_MARKER = "<!-- BEGIN GENERATED REGISTRY SUMMARY -->"
README_END_MARKER = "<!-- END GENERATED REGISTRY SUMMARY -->"

REGISTERED_STATUS = "production_ready"
BACKLOG_STATUSES = ("pending", "candidate", "QA-failed", "approved", "registered")
BACKLOG_ID_PATTERN = re.compile(r"^DG-\d{3}$")
ASSET_PATH_PATTERN = re.compile(r"^assets/(?P<category>[a-z_]+)/[A-Za-z0-9_]+\.png$")

REGENERATE_COMMAND = "python scripts/report_production_status.py --write"


@dataclass
class BacklogEntry:
    id: str
    category: str
    path: str
    status: str


@dataclass
class CategoryStatus:
    category: str
    registered: int
    backlog_total: int
    remaining: int
    state: str


@dataclass
class ProductionStatus:
    total_registered: int
    backlog_total: int
    categories: list[CategoryStatus] = field(default_factory=list)
    status_counts: dict[str, int] = field(default_factory=dict)
    pending_categories: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"manifest does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON in {path} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    if not isinstance(value, dict):
        raise ValueError(f"manifest top-level value must be an object: {path}")
    return value


def strip_emphasis(cell: str) -> str:
    return cell.strip().strip("*").strip("`").strip()


def parse_backlog(path: Path) -> tuple[list[BacklogEntry], list[str]]:
    """Read every ``DG-nnn`` row out of the ordered backlog tables."""
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"backlog does not exist: {path}") from exc

    entries: list[BacklogEntry] = []
    seen_ids: set[str] = set()
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        looks_like_entry = bool(cells) and BACKLOG_ID_PATTERN.fullmatch(strip_emphasis(cells[0]))
        if len(cells) < 8:
            # Fail closed. A DG row in a table with the wrong column count used to
            # be skipped silently, so eleven added rows once went uncounted while
            # every check still reported PASS.
            if looks_like_entry:
                errors.append(
                    f"{strip_emphasis(cells[0])}: backlog row has {len(cells)} columns; "
                    f"the schema requires 8 (ID, category, description, source, dependency, "
                    f"path, prompt, status)"
                )
            continue
        entry_id = strip_emphasis(cells[0])
        if not BACKLOG_ID_PATTERN.fullmatch(entry_id):
            continue

        asset_path = strip_emphasis(cells[5])
        status = strip_emphasis(cells[7])

        if entry_id in seen_ids:
            errors.append(f"duplicate backlog id: {entry_id}")
        seen_ids.add(entry_id)

        match = ASSET_PATH_PATTERN.fullmatch(asset_path)
        if match is None:
            errors.append(
                f"{entry_id}: intended production path is not a repository asset path: {asset_path!r}"
            )
            continue
        if status not in BACKLOG_STATUSES:
            errors.append(
                f"{entry_id}: status must be one of {', '.join(BACKLOG_STATUSES)}; found {status!r}"
            )
            continue

        entries.append(
            BacklogEntry(
                id=entry_id,
                category=match.group("category"),
                path=asset_path,
                status=status,
            )
        )

    if not entries:
        errors.append(f"no backlog rows were parsed from {path}")
    return entries, errors


def registered_paths(manifest: dict[str, Any], errors: list[str]) -> dict[str, str]:
    """Map each registered production path to its manifest category."""
    registered = manifest.get("registered_production_assets")
    if not isinstance(registered, list):
        errors.append("manifest registered_production_assets must be an array")
        return {}

    paths: dict[str, str] = {}
    for entry in registered:
        if not isinstance(entry, dict):
            errors.append("registered_production_assets entries must be objects")
            continue
        if entry.get("status") != REGISTERED_STATUS:
            continue
        asset_path = entry.get("path")
        category = entry.get("category")
        if not isinstance(asset_path, str) or not isinstance(category, str):
            errors.append("registered asset entries need string path and category values")
            continue
        paths[asset_path] = category
    return paths


def build_status(
    manifest: dict[str, Any],
    entries: list[BacklogEntry],
    backlog_errors: list[str],
) -> ProductionStatus:
    errors = list(backlog_errors)
    registered = registered_paths(manifest, errors)

    directories = manifest.get("production_directories")
    if not isinstance(directories, dict) or not directories:
        errors.append("manifest production_directories must be a non-empty object")
        layer_order: list[str] = []
    else:
        layer_order = list(directories)

    backlog_paths = {entry.path for entry in entries}
    registered_backlog_paths = {entry.path for entry in entries if entry.status == "registered"}

    for path in sorted(registered_backlog_paths - set(registered)):
        errors.append(f"backlog marks {path} registered but the manifest does not register it")
    for path in sorted(set(registered) - backlog_paths):
        errors.append(f"manifest registers {path} but no backlog row claims that path")
    for path in sorted((backlog_paths & set(registered)) - registered_backlog_paths):
        errors.append(f"manifest registers {path} but its backlog row is not marked registered")

    status_counts = {status: 0 for status in BACKLOG_STATUSES}
    for entry in entries:
        status_counts[entry.status] += 1

    categories: list[CategoryStatus] = []
    derived_pending: list[str] = []
    for category in layer_order:
        category_entries = [entry for entry in entries if entry.category == category]
        registered_count = sum(
            1 for path, value in registered.items() if value == category and path in backlog_paths
        )
        backlog_total = len({entry.path for entry in category_entries})
        remaining = backlog_total - registered_count

        # A category with no backlog rows is source-gated: nothing is designed yet.
        if not category_entries:
            state = "source-gated"
        elif remaining > 0:
            state = "in progress" if registered_count else "not started"
        else:
            state = "complete"

        if state != "complete":
            derived_pending.append(category)

        categories.append(
            CategoryStatus(
                category=category,
                registered=registered_count,
                backlog_total=backlog_total,
                remaining=remaining,
                state=state,
            )
        )

    declared_pending = manifest.get("pending_categories")
    if not isinstance(declared_pending, list):
        errors.append("manifest pending_categories must be an array")
    else:
        for category in sorted(set(declared_pending) - set(derived_pending)):
            errors.append(
                f"manifest lists {category} as pending but every backlog asset for it is registered"
            )
        for category in sorted(set(derived_pending) - set(declared_pending)):
            errors.append(
                f"manifest omits {category} from pending_categories but it still has unregistered assets"
            )

    return ProductionStatus(
        total_registered=len(registered),
        backlog_total=len({entry.path for entry in entries}),
        categories=categories,
        status_counts=status_counts,
        pending_categories=derived_pending,
        errors=errors,
    )


def render_block(status: ProductionStatus) -> str:
    complete = [item.category for item in status.categories if item.state == "complete"]
    lines = [
        BEGIN_MARKER,
        "",
        f"Generated by `{REGENERATE_COMMAND}`. Do not edit this block by hand.",
        "",
        f"- Registered production assets: **{status.total_registered}**",
        f"- Distinct backlog assets: **{status.backlog_total}**",
        f"- Completed categories: **{len(complete)} of {len(status.categories)}**"
        + (f" ({', '.join(complete)})" if complete else ""),
        "",
        "| Category | Registered | Backlog assets | Remaining | State |",
        "|---|---|---|---|---|",
    ]
    for item in status.categories:
        lines.append(
            f"| `{item.category}` | {item.registered} | {item.backlog_total} "
            f"| {item.remaining} | {item.state} |"
        )
    lines.extend(
        [
            "",
            "Backlog status tally: "
            + ", ".join(
                f"{status_name} {count}" for status_name, count in status.status_counts.items()
            )
            + ".",
            "",
            END_MARKER,
        ]
    )
    return "\n".join(lines)


def render_readme_block(status: ProductionStatus) -> str:
    """Short registry summary for the README."""
    active = [item for item in status.categories if item.registered]
    parts = ", ".join(f"{item.registered} {item.category}" for item in active)
    complete = [item.category for item in status.categories if item.state == "complete"]
    return "\n".join([
        README_BEGIN_MARKER,
        "",
        f"Generated by `{REGENERATE_COMMAND}`. Do not edit this block by hand.",
        "",
        f"The registry currently contains **{status.total_registered} registered assets**"
        + (f": {parts}." if parts else "."),
        "",
        f"Backlog: **{status.backlog_total}** distinct assets across "
        f"{len(status.categories)} categories; "
        f"**{len(complete)}** complete"
        + (f" ({', '.join(complete)})." if complete else "."),
        "",
        README_END_MARKER,
    ])


def replace_block(
    document: str,
    block: str,
    *,
    begin: str = BEGIN_MARKER,
    end_marker: str = END_MARKER,
) -> str:
    start = document.find(begin)
    end = document.find(end_marker)
    if start == -1 or end == -1:
        raise ValueError(f"document is missing the {begin} / {end_marker} generated region")
    if end < start:
        raise ValueError(f"{end_marker} appears before {begin} in the document")
    return document[:start] + block + document[end + len(end_marker) :]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("assets/asset_manifest.json"))
    parser.add_argument("--backlog", type=Path, default=Path("docs/trait-production-backlog.md"))
    parser.add_argument("--status-doc", type=Path, default=Path("docs/production_status.md"))
    parser.add_argument("--readme", type=Path, default=Path("README.md"),
                        help="also maintain the registry summary block in this file")
    parser.add_argument(
        "--write",
        action="store_true",
        help="rewrite the generated ledger block in the status document",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail when the status document is stale or disagrees with the manifest",
    )
    parser.add_argument("--json-report", type=Path)
    args = parser.parse_args(argv)

    try:
        manifest = load_manifest(args.manifest)
        entries, backlog_errors = parse_backlog(args.backlog)
    except ValueError as exc:
        print(f"FAIL production status ledger\n  - ERROR: {exc}")
        return 1

    status = build_status(manifest, entries, backlog_errors)
    block = render_block(status)

    document_stale = False
    targets = [(args.status_doc, block, BEGIN_MARKER, END_MARKER, "generated ledger")]
    if args.readme:
        targets.append((args.readme, render_readme_block(status),
                        README_BEGIN_MARKER, README_END_MARKER, "registry summary"))

    if args.write or args.check:
        for target, rendered, begin, end_marker, label in targets:
            try:
                document = target.read_text(encoding="utf-8")
                updated = replace_block(document, rendered, begin=begin, end_marker=end_marker)
            except (OSError, ValueError) as exc:
                status.errors.append(str(exc))
                continue
            if args.write and updated != document:
                target.write_text(updated, encoding="utf-8")
                print(f"Updated {label} in {target}")
            elif args.check and updated != document:
                document_stale = True
                status.errors.append(
                    f"{target} {label} is stale; run `{REGENERATE_COMMAND}`"
                )

    print(f"{'PASS' if status.passed else 'FAIL'} production status ledger")
    for error in status.errors:
        print(f"  - ERROR: {error}")
    print(
        f"{status.total_registered} registered asset(s) across "
        f"{len(status.categories)} categories; {status.backlog_total} backlog asset(s)."
    )
    if not args.write and not document_stale:
        print(block)

    if args.json_report:
        args.json_report.parent.mkdir(parents=True, exist_ok=True)
        args.json_report.write_text(json.dumps(asdict(status), indent=2) + "\n", encoding="utf-8")
        print(f"Report: {args.json_report}")

    return 0 if status.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
