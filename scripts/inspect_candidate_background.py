from pathlib import Path
from PIL import Image
from collections import Counter
root=Path('/home/ubuntu/Demigods/incoming/hand_objects/revision_2026-08-15')
for p in sorted(root.glob('*candidate.png')):
 im=Image.open(p).convert('RGB'); c=Counter(im.getdata()); print(p.name, c.most_common(12))
