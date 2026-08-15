from pathlib import Path
from PIL import Image
import numpy as np
root=Path('/home/ubuntu/Demigods')
src=root/'incoming/hand_objects/revision_2026-08-15'
out=root/'incoming/hand_objects/revision_2026-08-15/normalized'; out.mkdir(parents=True,exist_ok=True)
configs={
 'hand_object_009_violet_blade_pose_002_left_candidate.png':('hand_object_009_violet_blade_pose_002_left.png',(343,157,522,939)),
 'hand_object_012_brown_tome_pose_004_left_candidate.png':('hand_object_012_brown_tome_pose_004_left.png',(325,645,555,860)),
}
for name,(dest,target) in configs.items():
 im=Image.open(src/name).convert('RGBA'); arr=np.array(im)
 rgb=arr[:,:,:3].astype(int); mx=rgb.max(2); mn=rgb.min(2)
 # remove the neutral checkerboard while preserving colored artwork and dark/cream object pixels
 mask=((mx-mn)>12) | (mn<220)
 # retain only pixels connected to the central subject area; checkerboard is neutral and excluded above
 rgba=arr.copy(); rgba[:,:,3]=np.where(mask,255,0).astype('uint8')
 subject=Image.fromarray(rgba,'RGBA'); bbox=subject.getchannel('A').getbbox()
 if not bbox: raise SystemExit(f'{name}: no subject after background removal')
 crop=subject.crop(bbox)
 x0,y0,x1,y1=target; tw,th=x1-x0,y1-y0
 scale=min(tw/crop.width,th/crop.height)
 nw,nh=max(1,round(crop.width*scale)),max(1,round(crop.height*scale))
 crop=crop.resize((nw,nh),Image.Resampling.LANCZOS)
 canvas=Image.new('RGBA',(1254,1254),(0,0,0,0)); x=x0+(tw-nw)//2; y=y0+(th-nh)//2; canvas.alpha_composite(crop,(x,y))
 canvas.save(out/dest); print(dest,'source_bbox',bbox,'crop',crop.size,'placed',(x,y,x+nw,y+nh))
