from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
manifest = json.loads((ROOT / 'assets/asset_manifest.json').read_text())
rig = json.loads((ROOT / 'config/collection.json').read_text())['master_rig']
base_path = ROOT / 'assets/base_bodies/base_body_001_neutral_master.png'
with Image.open(base_path) as im:
    base_box = im.convert('RGBA').getchannel('A').getbbox()
base_width = base_box[2] - base_box[0]
rows = []
for entry in manifest['registered_production_assets']:
    path = ROOT / entry['path']
    if not path.exists():
        rows.append({'id': entry['id'], 'category': entry['category'], 'path': entry['path'], 'missing': True})
        continue
    with Image.open(path) as src:
        im = src.convert('RGBA')
        alpha = im.getchannel('A')
        bbox = alpha.getbbox()
        amin, amax = alpha.getextrema()
        if bbox:
            l, t, r, b = bbox[0], bbox[1], bbox[2]-1, bbox[3]-1
            width = r-l+1
            center = round((l+r)/2, 1)
            rows.append({
                'id': entry['id'], 'category': entry['category'], 'path': entry['path'],
                'size': list(im.size), 'mode': src.mode, 'alpha_min': amin, 'alpha_max': amax,
                'bounds': [l,t,r,b], 'width': width, 'width_ratio': round(width/base_width, 3),
                'center_x': center, 'center_delta': round(center-rig['canvas_center_x'], 1),
                'touches_edge': l == 0 or t == 0 or r == im.width-1 or b == im.height-1,
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            })
        else:
            rows.append({'id': entry['id'], 'category': entry['category'], 'path': entry['path'], 'empty': True})
out = ROOT / 'docs/qa/trait_geometry_audit.json'
out.write_text(json.dumps(rows, indent=2) + '\n')
print(out)
for category in sorted({r['category'] for r in rows}):
    group = [r for r in rows if r['category'] == category and 'width_ratio' in r]
    if not group: continue
    ratios = [r['width_ratio'] for r in group]
    print(f'{category}: n={len(group)} width_ratio={min(ratios):.3f}..{max(ratios):.3f} center_delta={min(r["center_delta"] for r in group):.1f}..{max(r["center_delta"] for r in group):.1f} edge_touch={sum(r["touches_edge"] for r in group)}')
