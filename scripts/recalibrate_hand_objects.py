from pathlib import Path
from PIL import Image
import hashlib, json, shutil
ROOT=Path(__file__).resolve().parent.parent
TARGETS={
 'hand_object_006_gold_lantern_pose_002_left.png':(34,2),
 'hand_object_007_gold_blue_gem_staff_pose_002_left.png':(34,122),
 'hand_object_008_blue_crescent_staff_pose_002_left.png':(34,122),
 'hand_object_009_violet_blade_pose_002_left.png':(34,-143),
 'hand_object_010_horned_skull_scepter_pose_002_left.png':(34,122),
 'hand_object_011_round_talisman_pose_004_left.png':(34,120),
 'hand_object_012_brown_tome_pose_004_left.png':(35,0),
}
BACKUP=ROOT/'incoming/hand_objects/recalibration_originals_2026-08-15'
OUT=ROOT/'incoming/hand_objects/recalibration_2026-08-15'
def sha(p):
 h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def translate(im,dx,dy):
 out=Image.new('RGBA',im.size,(0,0,0,0))
 out.alpha_composite(im,(dx,dy))
 return out
def bbox(im):
 b=im.getchannel('A').getbbox(); return [b[0],b[1],b[2]-1,b[3]-1] if b else None
def main():
 BACKUP.mkdir(parents=True,exist_ok=True); OUT.mkdir(parents=True,exist_ok=True)
 rows=[]
 for name,(dx,dy) in TARGETS.items():
  src=ROOT/'assets/hand_objects'/name; backup=BACKUP/name
  if not backup.exists(): shutil.copy2(src,backup)
  im=Image.open(src).convert('RGBA'); result=translate(im,dx,dy); result.save(src)
  rows.append({'asset':str(src.relative_to(ROOT)),'source_sha256':sha(backup),'output_sha256':sha(src),'dx':dx,'dy':dy,'output_bounds':bbox(result),'method':'native_integer_translation_to_measured_hand_landmark'})
  print(name, 'dx',dx,'dy',dy,'bounds',bbox(result))
 (OUT/'provenance.json').write_text(json.dumps({'operation':'hand_object_recalibration','pose2_target':[438,772],'pose4_target':[438,748],'items':rows},indent=2)+'\n')
if __name__=='__main__': main()
