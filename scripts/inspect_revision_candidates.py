from pathlib import Path
from PIL import Image
root=Path('/home/ubuntu/Demigods/incoming/hand_objects/revision_2026-08-15')
for p in sorted(root.glob('*candidate.png')):
 im=Image.open(p).convert('RGBA'); a=im.getchannel('A'); print(p.name, im.size, 'bbox', a.getbbox())
