from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rig_gate_report
import json

ROOT = Path(__file__).resolve().parent.parent
cfg = json.loads((ROOT / 'config' / 'collection.json').read_text())
canvas = cfg['canvas']
rig = cfg['master_rig']
targets = [
    ROOT / 'assets/base_bodies/base_body_001_neutral_master.png',
    ROOT / 'assets/base_bodies/base_pose_003_viewer_right_vertical_grip.png',
    ROOT / 'assets/base_bodies/base_pose_005_centered_two_hand_grip.png',
]
with TemporaryDirectory() as td:
    root = Path(td)
    for src in targets:
        print(src.name)
        with Image.open(src) as im:
            original = im.convert('RGBA')
        for shift in (-2, -1, 0, 1, 2):
            out = Image.new('RGBA', original.size, (0, 0, 0, 0))
            out.alpha_composite(original, (shift, 0))
            path = root / f'{src.stem}_{shift:+d}.png'
            out.save(path)
            report = rig_gate_report.analyze(path, rig, canvas, tolerance=1, pose_variant=True)
            center = next((c for c in report['checks'] if c[0] == 'body_center_x'), None)
            print(f'  shift_x={shift:+d}: passed={report["passed"]} body_center={center[2] if center else None} delta={center[4] if center else None}')
