from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parent.parent
rows=json.loads((ROOT/'incoming/hand_objects/recalibration_2026-08-15/provenance.json').read_text())['items']
anchors={name:(438,772) for name in [r['asset'].split('/')[-1] for r in rows if 'pose_002' in r['asset']]}
anchors.update({name:(438,748) for name in [r['asset'].split('/')[-1] for r in rows if 'pose_004' in r['asset']]})
for r in rows:
 name=Path(r['asset']).name; p=ROOT/r['asset']; im=Image.open(p).convert('RGBA'); a=im.getchannel('A'); px=a.load(); x,y=anchors[name]
 vals=[px[nx,ny] for ny in range(y-28,y+29) for nx in range(x-28,x+29)]
 contact=sum(v>32 for v in vals); b=a.getbbox(); bounds=[b[0],b[1],b[2]-1,b[3]-1]
 ok=contact>0 and bounds[0]>=233 and bounds[1]>=129 and bounds[2]<=1021 and bounds[3]<=1139
 print(f'{name}: anchor={x},{y} alpha_pixels_57x57={contact} bounds={bounds} PASS={ok}')
