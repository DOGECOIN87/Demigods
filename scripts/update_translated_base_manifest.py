from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / 'assets/asset_manifest.json'
TARGETS = {
    'base_body_001': 'assets/base_bodies/base_body_001_neutral_master.png',
    'base_pose_003': 'assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png',
    'base_pose_005': 'assets/base_bodies/base_pose_005_centered_two_hand_grip.png',
}
BACKUP = ROOT / 'incoming/base_bodies/refinement_originals_2026-08-15'
manifest = json.loads(MANIFEST.read_text())
found = set()
for entry in manifest['registered_production_assets']:
    if entry.get('id') not in TARGETS:
        continue
    rel = TARGETS[entry['id']]
    current = ROOT / rel
    backup = BACKUP / current.name
    if not backup.exists():
        raise SystemExit(f'missing immutable backup: {backup}')
    old_hash = hashlib.sha256(backup.read_bytes()).hexdigest()
    new_hash = hashlib.sha256(current.read_bytes()).hexdigest()
    if entry.get('sha256') != old_hash:
        raise SystemExit(f'{entry["id"]}: manifest hash does not match pre-translation backup')
    entry['sha256'] = new_hash
    entry.setdefault('provenance', {})['postprocessing'] = [
        'native_integer_translation_x_plus_1_px_2026-08-15'
    ]
    entry['provenance']['pre_translation_sha256'] = old_hash
    entry['provenance']['post_translation_sha256'] = new_hash
    entry['provenance']['postprocessing_script'] = 'scripts/translate_base_bodies_x.py'
    entry['qa_report'] = 'docs/qa/base_body_centering_investigation_2026-08-15.md'
    found.add(entry['id'])
missing = set(TARGETS) - found
if missing:
    raise SystemExit(f'missing manifest entries: {sorted(missing)}')
MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
print('updated', ', '.join(sorted(found)))
