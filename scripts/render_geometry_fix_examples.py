from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'docs/qa/geometry_fix_examples_2026-08-15'; OUT.mkdir(parents=True,exist_ok=True)
def rgba(p): return Image.open(ROOT/p).convert('RGBA')
def comp(parts,name):
 c=Image.new('RGBA',(1254,1254),(255,255,255,255))
 for p in parts: c.alpha_composite(rgba(p))
 c.convert('RGB').save(OUT/name)
# held objects behind the base hand, then outfit in front of torso
examples=[
 (['assets/backgrounds/background_003_arcane_library.png','assets/hand_objects/hand_object_007_gold_blue_gem_staff_pose_002_left.png','assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png','assets/outfits/outfit_002_storm_guardian_pose_002.png'],'staff_pose_002.png'),
 (['assets/backgrounds/background_006_moonlit_marble_balcony.png','assets/hand_objects/hand_object_006_gold_lantern_pose_002_left.png','assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png','assets/outfits/outfit_002_storm_guardian_pose_002.png'],'lantern_pose_002.png'),
 (['assets/backgrounds/background_001_celestial_throne_hall.png','assets/hand_objects/hand_object_012_brown_tome_pose_004_left.png','assets/base_bodies/base_pose_004_viewer_left_palm_up.png','assets/outfits/outfit_004_lunar_oracle_pose_004.png'],'tome_pose_004.png'),
 (['assets/backgrounds/background_004_crescent_star_dreamscape.png','assets/base_bodies/base_body_001_neutral_master.png','assets/outfits/outfit_010_celestial_robe_white_gold.png','assets/neck_accessories/neck_accessory_005_silver_navy_long_pendant.png'],'neck_pendant.png'),
]
for parts,name in examples: comp(parts,name); print(OUT/name)
