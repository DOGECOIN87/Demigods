from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent.parent; mp=root/'assets/asset_manifest.json'; m=json.loads(mp.read_text())
changed={'hand_object_006_gold_lantern_pose_002_left.png','hand_object_007_gold_blue_gem_staff_pose_002_left.png','hand_object_008_blue_crescent_staff_pose_002_left.png','hand_object_009_violet_blade_pose_002_left.png','hand_object_010_horned_skull_scepter_pose_002_left.png','hand_object_012_brown_tome_pose_004_left.png'}
for e in m['registered_production_assets']:
 if Path(e.get('path','')).name not in changed: continue
 p=root/e['path']; e.setdefault('provenance',{})['pre_pose_aware_revision_sha256']=hashlib.sha256((root/'incoming/hand_objects/revision_2026-08-15/originals_before_pose_aware'/p.name).read_bytes()).hexdigest(); e['provenance']['pose_aware_revision']='12_degree_outward_hold_and_silhouette_correction_2026-08-15' if 'pose_002' in p.name else 'open_horizontal_spellbook_v2_2026-08-15'; e['provenance']['pose_aware_revision_script']='scripts/build_pose_aware_hand_object_candidates.py'; e['sha256']=hashlib.sha256(p.read_bytes()).hexdigest(); e['qa_report']='docs/qa/hand_object_recalibration_findings_2026-08-15.md'
mp.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n'); print('updated pose-aware entries:',len(changed))
