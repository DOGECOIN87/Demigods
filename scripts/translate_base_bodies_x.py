from pathlib import Path
from PIL import Image
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [
    ROOT / 'assets/base_bodies/base_body_001_neutral_master.png',
    ROOT / 'assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png',
    ROOT / 'assets/base_bodies/base_pose_005_centered_two_hand_grip.png',
]
BACKUP = ROOT / 'incoming/base_bodies/refinement_originals_2026-08-15'
BACKUP.mkdir(parents=True, exist_ok=True)
records = []
for path in TARGETS:
    original = path.read_bytes()
    before = hashlib.sha256(original).hexdigest()
    backup = BACKUP / path.name
    backup.write_bytes(original)
    with Image.open(path) as src:
        src.load()
        if src.size != (1254, 1254) or src.mode != 'RGBA':
            raise RuntimeError(f'{path}: expected 1254x1254 RGBA, got {src.size} {src.mode}')
        shifted = Image.new('RGBA', src.size, (0, 0, 0, 0))
        shifted.alpha_composite(src.convert('RGBA'), (1, 0))
        shifted.save(path, format='PNG')
    after = hashlib.sha256(path.read_bytes()).hexdigest()
    records.append({
        'production_path': str(path.relative_to(ROOT)),
        'backup_path': str(backup.relative_to(ROOT)),
        'operation': 'native integer translation',
        'shift_x': 1,
        'shift_y': 0,
        'canvas': [1254, 1254],
        'mode': 'RGBA',
        'original_sha256': before,
        'translated_sha256': after,
    })
report = BACKUP / 'translation_provenance.json'
report.write_text(json.dumps({'created_utc': '2026-08-15', 'records': records}, indent=2) + '\n')
print(report)
for r in records:
    print(r['production_path'], r['original_sha256'], '->', r['translated_sha256'])
