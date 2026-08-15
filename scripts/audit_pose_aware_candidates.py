from pathlib import Path
from PIL import Image
root=Path('/home/ubuntu/Demigods'); src=root/'incoming/hand_objects/revision_2026-08-15/pose_aware'
items=sorted(src.glob('*.png'))
for p in items:
 im=Image.open(p).convert('RGBA'); a=im.getchannel('A'); b=a.getbbox();
 if 'pose_002' in p.name: x,y=438,772
 else: x,y=438,748
 vals=[a.getpixel((nx,ny)) for ny in range(y-30,y+31) for nx in range(x-30,x+31)]
 contact=sum(v>32 for v in vals); bounds=(b[0],b[1],b[2]-1,b[3]-1) if b else None
 ok=im.size==(1254,1254) and b is not None and contact>0 and bounds[0]>=250 and bounds[1]>=120 and bounds[2]<=1050 and bounds[3]<=1150
 print(f'{p.name}: size={im.size} contact_alpha_61x61={contact} bounds={bounds} PASS={ok}')
 if not ok: raise SystemExit(1)
