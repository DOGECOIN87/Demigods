from pathlib import Path
from PIL import Image
import numpy as np
root=Path('/home/ubuntu/Demigods'); p=root/'incoming/hand_objects/revision_2026-08-15/hand_object_012_brown_tome_pose_004_left_candidate_v2.png'; out=root/'incoming/hand_objects/revision_2026-08-15/normalized/hand_object_012_brown_tome_pose_004_left_v2.png'
im=Image.open(p).convert('RGBA'); arr=np.array(im); rgb=arr[:,:,:3].astype(int); mx=rgb.max(2); mn=rgb.min(2); mask=((mx-mn)>12) | (mn<220); arr[:,:,3]=np.where(mask,255,0).astype('uint8'); subject=Image.fromarray(arr,'RGBA'); bbox=subject.getchannel('A').getbbox(); crop=subject.crop(bbox)
target=(300,675,610,825); x0,y0,x1,y1=target; scale=min((x1-x0)/crop.width,(y1-y0)/crop.height); size=(max(1,round(crop.width*scale)),max(1,round(crop.height*scale))); crop=crop.resize(size,Image.Resampling.LANCZOS); canvas=Image.new('RGBA',(1254,1254),(0,0,0,0)); x=x0+((x1-x0)-size[0])//2; y=y0+((y1-y0)-size[1])//2; canvas.alpha_composite(crop,(x,y)); canvas.save(out); print('source_bbox',bbox,'crop',size,'placed',(x,y,x+size[0],y+size[1]),out)
