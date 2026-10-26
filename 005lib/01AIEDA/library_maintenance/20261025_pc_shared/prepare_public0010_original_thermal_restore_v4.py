"""Prepare finite source21 actual r_path reconstruction after cropped-shape FAIL."""
from pathlib import Path
import hashlib,json
M=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def main():
 b=M/'public0010_original_thermal_restore_bundle13_v4';assert not b.exists();b.mkdir()
 h=b/'public0010_original_thermal_restore_v4.il';h.write_bytes((M/'public0010_original_thermal_paths_template_v4.il').read_bytes())
 old=M/'public0010_external_thermal_restore_bundle13_v2/MANIFEST.json';man=json.loads(old.read_text())
 decision=M/'FINITE_SOURCE_THERMAL_PATH_RESTORE_DECISION27.json';assert sha(decision)=='9DB6EEC822612E12D76174C5098E7A362BDDCC18B69F919E1EAC4272FDF5F086'
 man.update(schema='PUBLIC0010_FINITE_ORIGINAL21_THERMAL_PATH_CU_RESTORE_V4',helper=str(h),entry_source='pc25OriginalThermalPrepare',entry_target='pc25OriginalThermalRestore',source_marker='SOURCE21_ORIGINAL_THERMAL_PATHS_PREPARED.txt',target_marker='SOURCE21_ORIGINAL_THERMAL_RESTORE_COMPLETE.txt',candidate_name='PUB0010_ORIGINAL_THERMAL_RESTORED.brd',source_only_outside_old_pad=False,restore_original_board_thermal_path_geometry_not_old_whole_land=True,do_not_restore_old_land_interior='Root finite decision allows original21 source board path Cu overlapping old land; no old land shape definition is cloned',exact_global_three_power_net_bottom_cu_union_required=True,root_finite_decision=str(decision),root_finite_decision_sha256=sha(decision))
 for p in [h,Path(__file__),M/'public0010_original_thermal_paths_template_v4.il',old,decision,M/'public0010_external_thermal_restore_run13_v3/RUN_RECEIPT.json',M/'public0010_external_thermal_restore_run13_v3/CREATE_STEP.txt',M/'public0010_external_thermal_restore_run13_v3/stdout.txt']:
  man['files'].append(dict(path=str(p),sha256=sha(p)))
 (b/'MANIFEST.json').write_text(json.dumps(man,indent=2)+'\n','utf-8')
 runner=M/'run_public0010_original_thermal_restore_v4.py'
 s=(M/'run_public0010_external_thermal_restore_v2.py').read_text().replace('PUBLIC0010_SOURCE_ONLY_EXTERNAL_THERMAL_CU_RESTORE_V2',man['schema']).replace('PASS_SOURCE_ONLY_EXTERNAL_THERMAL_PHASE_ONLY','PASS_FINITE_ORIGINAL21_THERMAL_PATH_PHASE_ONLY')
 runner.write_text(s,'utf-8')
 print(json.dumps(dict(bundle=str(b),manifest_sha256=sha(b/'MANIFEST.json'),helper_sha256=sha(h),runner=str(runner),runner_sha256=sha(runner)),indent=2))
if __name__=='__main__':main()
