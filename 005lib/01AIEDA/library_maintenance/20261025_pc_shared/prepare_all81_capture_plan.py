"""Freeze latestcn2 only explicitFP edits for bounded all81 canonical plan; never starts CAD."""
from pathlib import Path
import copy,hashlib,json,subprocess,xml.etree.ElementTree as ET
M=Path(__file__).resolve().parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');D=M/'project81_final_canonical_plan13';O=M/'capture_all81_plan13';O.mkdir(exist_ok=True)
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
put=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
decision=D/'ALL81_PACKAGE_CANONICAL_DECISIONS.json';rules={x['source_package'].lower():x['target'] for x in jr(decision) if x['action'].startswith('STANDARDIZE_')}
xp=R/'w/sot34_xn2/native_design.xml';dsn=R/'w/sot34_cn2/LGA1700.DSN';assert sha(dsn)=='0E90B0217BCD370DEEE0CAB80C8BBF28BD5CDD00B2171F04AEE9321D3399B50C'
source=jr(M/'capture_sot34_plan_v1/SOT34_SOURCE_PLAN.json');source.update(source_design_xml=str(xp),source_design_xml_sha256=sha(xp),source_xml_sha256=sha(xp),source_DSN=str(dsn),source_DSN_sha256=sha(dsn),scope='Only latestcn2 explicit PCB Footprint attributes for frozenall81canonical decisions; all source identities are guard-only exact samevalue; no cachedefault/Value/connection/pose edits.',allowed_source_identity_mutations=0)
tree=ET.parse(xp).getroot();actual_cache_sources={e.find('Defn').get('name'):e.find('Defn').get('sourceLibName') for typ in ['Package','GlobalSymbol','OffPageSymbol'] for e in tree.findall('./Cache/'+typ)}
for r in source['object_mappings']:r['old_source']=r['new_source']=actual_cache_sources[r['name']]
for r in source['native_cache_selectors']:r['old_source']=r['new_source']=r['old_source'].upper()
sources={(r['kind'],r['id']):r for r in source['instance_source_changes']}
oldmap={str(r['dbid']):r for r in jr(R/'w/pcb_migration/FINAL_INSTANCE_MAPPING.json')};mapping=[]
for page in tree.findall('./Schematic/Page'):
 pn=page.find('Defn').get('name')
 for typ in ['PartInst','Global','OffPageConnector','Port']:
  for e in page.findall(typ):
   a=e.find('Defn').attrib;r=sources[(typ,a['dbId'])];assert r['page']==pn;r['old_source']=r['new_source']=a['libName']
   if typ!='PartInst':continue
   ref=e.find('Reference/Defn').get('name');props={u.find('Defn').get('name'):u.find('Defn').get('val') for u in e.findall('PartInstUserProp')};old=props['PCB Footprint'];target=rules.get(old.lower(),old)
   row=copy.deepcopy(oldmap[a['dbId']]);assert row['ref']==ref and row['page']==pn and row['instance']==a['name'];row.update(old_footprint=old,proposed_target=target,target=target);mapping.append(row)
assert len(mapping)==1131
sourcepath=O/'ALL81_LATEST_CN2_SOURCE_PLAN.json';mappath=O/'ALL81_LATEST_CN2_COMPLETE_INSTANCE_MAPPING.json';put(sourcepath,source);put(mappath,mapping)
compiled=O/'compiled';assert not compiled.exists(),'Fresh compiler directory required'
subprocess.run([r'C:\Users\Administrator\.local\bin\python3.15.exe',str(R/'tools/compile_capture13_native_plan.py'),'--source-plan',str(sourcepath),'--instance-map',str(mappath),'--out',str(compiled),'--new-source-identity',r'D:\001DIY\005LIB\01CAPTURELIB\COMMON_PC.OLB'],check=True)
native=M/'capture_sot34_plan_v1/apply_capture13_footprints_only.tcl';dest=O/'apply_all81_capture_footprints_only.tcl';dest.write_bytes(native.read_bytes())
plan=jr(compiled/'CAPTURE13_FROZEN_PLAN.json');assert all(r['old_source']==r['new_source'] for k in ('object_mappings','native_cache_selectors','instance_source_changes') for r in plan[k]);assert not plan['cache_default_pcb_footprint_changes']
plan['native_script']=str(dest);plan['all81_decisions_binding']={'path':str(decision),'sha256':sha(decision)};plan['allowed_source_identity_mutations']=0;put(compiled/'CAPTURE13_FROZEN_PLAN.json',plan)
syntax=O/'check_tcl_syntax_and_guard_counts.tcl';syntax.write_text('set f [open {'+str(dest).replace('\\','/')+'} r]\nset s [read $f];close $f\nif {![info complete $s]} {error {Tcl incomplete}}\nsource {'+str(compiled/'CAPTURE13_FROZEN_PLAN.tcl').replace('\\','/')+'}\nif {[dict size $footprintPlan] != '+str(len(plan['pcb_footprint_changes']))+' || [dict size $instanceGuards] != 3118 || [llength $sourceSelectors] != 231} {error {Unexpected counts}}\nforeach row $sourceSelectors {if {[dict get $row old_source] ne [dict get $row new_source]} {error {Source mutation}}}\nputs {PASS only Tcl syntax/data, noCAD}\n',encoding='utf-8')
subprocess.run([r'C:\Program0\cadence\SPB172\tcltk\bin\tclsh.exe',str(syntax)],check=True)
report={'status':'ALL81_FP_ONLY_NATIVE_PLAN_READY_NO_CAD_EXECUTED','latest_source_DSN':str(dsn),'source_DSN_sha256':sha(dsn),'latest_source_XML':str(xp),'source_XML_sha256':sha(xp),'changed_explicit_FP_instances':len(plan['pcb_footprint_changes']),'changed_unique_refs':len({r['ref'] for r in plan['pcb_footprint_changes']}),'all1131instances_guarded':True,'all231cache_and3118source_identities_unchanged':True,'new_targets_require_root_cold_native_before_apply':['mount_156a_p4567_pc','ddr4_dimm_288p_pc'],'script':str(dest),'script_sha256':sha(dest),'plan':str(compiled/'CAPTURE13_FROZEN_PLAN.json'),'plan_sha256':sha(compiled/'CAPTURE13_FROZEN_PLAN.json'),'planTcl':str(compiled/'CAPTURE13_FROZEN_PLAN.tcl'),'planTcl_sha256':sha(compiled/'CAPTURE13_FROZEN_PLAN.tcl'),'only_change_scope':'PartInstUserProp PCB Footprint val. Existing SOT34 is alreadygeneric in latestcn2 and is guardonly thispass.','native_call':'capture13NativeApply(sourceDSN, freshOutputDSN, planTcl, freshReportDir) using source thisTcl; root owns actual isolated native process.'}
put(O/'ALL81_CAPTURE_PLAN_READY.json',report);print(json.dumps(report,indent=2))
if __name__!='__main__':raise RuntimeError('Executable preparation only')
