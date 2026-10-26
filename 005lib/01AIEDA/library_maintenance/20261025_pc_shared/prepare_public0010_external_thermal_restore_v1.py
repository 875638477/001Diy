"""Freeze precisely the native-approved external25 thermal restoration phase."""
from pathlib import Path
import hashlib,json
M=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def main():
 b=M/'public0010_external_thermal_restore_bundle13_v1';assert not b.exists();b.mkdir()
 h=b/'public0010_external_thermal_restore_v1.il';h.write_bytes((M/'public0010_external_thermal_restore_template_v1.il').read_bytes())
 base=M/'public0010_source25_owner_probe_bundle13_v2/MANIFEST.json';man=json.loads(base.read_text('utf-8'))
 man.update(schema='PUBLIC0010_SOURCE_ONLY_EXTERNAL_THERMAL_CU_RESTORE_V1',helper=str(h),entry_source='pc25ExternalSourcePrepare',entry_target='pc25RestoreExternalThermal',source_marker='SOURCE25_EXTERNAL_RESTORE_PREPARED.txt',target_marker='SOURCE25_EXTERNAL_THERMAL_RESTORE_COMPLETE.txt',candidate_name='PUB0010_EXTERNAL_THERMAL_RESTORED.brd',no_create=False,no_save=False,source_external_fragment_keys=[1,2,4,5,7,8,9,10,11,13,14,15,16,17,18,19,20,21,23,24,25],source_only_outside_old_pad=True,do_not_restore_old_land_interior=True,post_fresh_full915_gate_required=True)
 for p in [base,h,Path(__file__),M/'public0010_external_thermal_restore_template_v1.il',M/'public0010_source25_owner_probe_run13_v2/RUN_RECEIPT.json',M/'public0010_source25_owner_probe_run13_v2/SOURCE25_TARGET_WHOLE_CU_RELATIONS.ilist',M/'public0010_source25_owner_probe_run13_v2/SOURCE25_TARGET_ACTUAL_POLYGONS.jsonl']:
  man['files'].append(dict(path=str(p),sha256=sha(p)))
 (b/'MANIFEST.json').write_text(json.dumps(man,indent=2)+'\n','utf-8')
 runner=M/'run_public0010_external_thermal_restore_v1.py'
 s=(M/'run_public0010_nil_route_stub_owned_v1.py').read_text('utf-8')
 s=s.replace('PUBLIC0010_EXACT54_NIL_SOURCE_NET_PROPAGATION_REPAIR_V1',man['schema']).replace('PASS_BOUNDED_NIL_ATTACHMENT_PHASE_ONLY','PASS_SOURCE_ONLY_EXTERNAL_THERMAL_PHASE_ONLY')
 runner.write_text(s,'utf-8')
 print(json.dumps(dict(bundle=str(b),manifest_sha256=sha(b/'MANIFEST.json'),helper_sha256=sha(h),runner=str(runner),runner_sha256=sha(runner)),indent=2))
if __name__=='__main__':main()
