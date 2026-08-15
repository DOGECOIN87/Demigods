from pathlib import Path
import json
from PIL import Image
try:
    from scripts.hide_undergarment import exposed_count
except ImportError:
    from hide_undergarment import exposed_count

ROOT = Path(__file__).resolve().parent.parent
manifest=json.loads((ROOT/'assets/asset_manifest.json').read_text())
def box(p):
    with Image.open(p).convert('RGBA') as im:
        b=im.getchannel('A').getbbox()
        return [b[0],b[1],b[2]-1,b[3]-1] if b else None
for category in ['neck_accessories','hand_objects','outfits']:
    print(f'[{category}]')
    for e in manifest['registered_production_assets']:
        if e['category']!=category: continue
        p=ROOT/e['path']; b=box(p)
        print(e['id'], e['path'], 'bounds=',b, 'width=',b[2]-b[0]+1 if b else None, 'height=',b[3]-b[1]+1 if b else None)
print('[outfit exposure]')
pairs=[
('base_body_001_neutral_master.png','outfit_001_celestial_scholar_pose_001.png'),
('base_pose_002_viewer_left_vertical_grip.png','outfit_002_storm_guardian_pose_002.png'),
('base_pose_003_viewer_right_vertical_grip.png','outfit_003_verdant_alchemist_pose_003.png'),
('base_pose_004_viewer_left_palm_up.png','outfit_004_lunar_oracle_pose_004.png'),
('base_pose_005_centered_two_hand_grip.png','outfit_005_sun_temple_pose_005.png'),]
for b,o in pairs:
    base=Image.open(ROOT/'assets/base_bodies'/b).convert('RGBA')
    outfit=Image.open(ROOT/'assets/outfits'/o).convert('RGBA')
    print(b,o,'exposed=',exposed_count(base,outfit))
