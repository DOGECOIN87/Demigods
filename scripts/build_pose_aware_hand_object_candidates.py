from pathlib import Path
from PIL import Image
root=Path('/home/ubuntu/Demigods'); assets=root/'assets/hand_objects'; out=root/'incoming/hand_objects/revision_2026-08-15/pose_aware'; out.mkdir(parents=True,exist_ok=True)
pose2=['hand_object_006_gold_lantern_pose_002_left.png','hand_object_007_gold_blue_gem_staff_pose_002_left.png','hand_object_008_blue_crescent_staff_pose_002_left.png','hand_object_009_violet_blade_pose_002_left.png','hand_object_010_horned_skull_scepter_pose_002_left.png']
anchor=(438,772)
for name in pose2:
 im=Image.open(assets/name).convert('RGBA'); rotated=im.rotate(12, resample=Image.Resampling.BICUBIC, center=anchor, expand=False)
 rotated.save(out/name); print('angled',name,'+12deg around',anchor)
book=root/'incoming/hand_objects/revision_2026-08-15/normalized/hand_object_012_brown_tome_pose_004_left.png'; bookout=out/book.name; bookout.write_bytes(book.read_bytes()); print('replaced candidate',bookout.name)
