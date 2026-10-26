"""Prepare the exact34FP Capture-only plan from protectedcn1/fully exportedxn1. No CAD."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as E,subprocess
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared');R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');O=M/'capture_sot34_plan_v1';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper();jr=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
source=R/'w/cn1/LGA1700.DSN';xml=R/'w/xn1/native_design.xml';assert sha(source)=='0A8152BDF713C14269B0229B947CDB70A9896F87714E43DDC9E68A1A71F94C07'
base=jr(R/'w/capture_reuse_final/CAPTURE_PUBLIC_SOURCE_PLAN.json');base['source_design_xml']=str(xml);base['source_xml_sha256']=base['source_design_xml_sha256']=sha(xml)
x=E.parse(xml).getroot();actual={};native_identity={z.find('Defn').get('sourceLibName') for z in x.find('Cache') if z.tag in ('Package','GlobalSymbol','OffPageSymbol')};assert len(native_identity)==1;native_identity=next(iter(native_identity));base['target_new_library']=native_identity
for page in x.findall('./Schematic/Page'):
 pn=page.find('Defn').get('name')
 for kind in ('PartInst','Global','OffPageConnector','Port'):
  for inst in page.findall(kind):
   d=inst.find('Defn');actual[(kind,d.get('dbId'))]=(pn,d.attrib,inst)
for row in base['instance_source_changes']:
 pn,d,inst=actual[(row['kind'],row['id'])];assert pn==row['page'];row['old_source']=row['new_source']=d['libName']
for name in ('object_mappings','native_cache_selectors'):
 for row in base[name]:row['old_source']=row['new_source']=native_identity
base['pcb_footprint_changes']=[];base['status']='READY_EXPLICIT_NATIVE_SOURCE_ONLY_PLAN';base['source_DSN']=str(source);base['source_DSN_sha256']=sha(source);base['scope']='Only34explicitPartInstPCBFootprint values; every source path/name/cache definition/value/network/pose remains unchanged.'
sp=O/'SOT34_SOURCE_PLAN.json';sp.write_text(json.dumps(base,ensure_ascii=False,indent=2),encoding='utf-8')
old=jr(R/'w/pcb_migration/FINAL_INSTANCE_MAPPING.json');mapping=[];changes=[]
for row in old:
 pn,d,inst=actual[('PartInst',row['dbid'])];props={z.get('name'):z.get('val','') for z in inst.findall('./PartInstUserProp/Defn')};fp=props['PCB Footprint'];n='sot23-3' if fp.lower()=='sot23_123' else fp
 assert row['ref']==inst.find('Reference/Defn').get('name');new={**row,'old_footprint':fp,'proposed_target':n,'target':n};mapping.append(new)
 if fp!=n:changes.append({'ref':row['ref'],'page':pn,'id':row['dbid'],'before':fp,'after':n})
assert len(changes)==34 and len(mapping)==1131
mp=O/'SOT34_COMPLETE_INSTANCE_MAP.json';mp.write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf-8')
compiler=R/'tools/compile_capture13_native_plan.py';out=O/'compiled_v2'
if not out.exists():subprocess.run([__import__('sys').executable,str(compiler),'--source-plan',str(sp),'--instance-map',str(mp),'--out',str(out)],check=True)
else:assert jr(out/'CAPTURE13_FROZEN_PLAN.json')['source_xml_sha256']==sha(xml)
# Copy the proven native guards, but remove ALLsource setters. Cache/source identity is checked read-only.
srcscript=R/'tools/apply_capture13_public_sources.tcl';s=srcscript.read_text(encoding='utf-8-sig')
s=s.replace('source [file join [file dirname [info script]] native_helpers layout_native_common.tcl]','source {'+str(R/'tools/native_helpers/layout_native_common.tcl').replace('\\','/')+'}')
start=s.index('# Source setters follow installed capReplacePathInCache semantics')
end=s.index('set f [::LAY::channel $reportDir FOOTPRINT_IMMEDIATE_READBACK.tsv',start)
s=s[:start]+'''# This variant is footprint-only. The preceding full cache/source guards are read-only.
dict for {key binding} $cacheBound {
 lassign $binding libobj name old row
 if {[dict get $row old_source] ne [dict get $row new_source]} {error {Source edits forbidden in SOT34 plan}}
}
'''+s[end:]
assert 'ReplaceSourceLibName' not in s and ' SetSourceLibName ' not in s
s=s.replace('# Case13. Root owns isolated native process; only fresh target DSN is saved.','# SOT34FPonly. Exact full-instance/cache guards; no source library setters. Root owns isolated native process.')
script=O/'apply_capture13_footprints_only.tcl';script.write_text(s,encoding='utf-8')
frozen=jr(out/'CAPTURE13_FROZEN_PLAN.json');assert len(frozen['pcb_footprint_changes'])==34
frozen['native_script']=str(script);frozen['source_DSN']=str(source);frozen['source_DSN_sha256']=sha(source);frozen['allowed_source_identity_mutations']=0;frozen['status']='FROZEN_NATIVE_FOOTPRINT_ONLY_34_PLAN';frozen['SOT34_only_invariant']='Only34explicitPCBFootprint: SOT23_123 -> sot23-3; current publicCOMMON source/cache/library/Values/NC/nets/geometry unchanged.'
fp=out/'CAPTURE13_FROZEN_PLAN.json';fp.write_text(json.dumps(frozen,ensure_ascii=False,indent=2),encoding='utf-8')
receipt={'status':'PREPARED_NOT_EXECUTED_NO_CAD','source_DSN':str(source),'source_DSN_sha256':sha(source),'source_xml':str(xml),'source_xml_sha256':sha(xml),'native_script':str(script),'native_script_sha256':sha(script),'frozen_plan':str(fp),'frozen_plan_sha256':sha(fp),'frozen_tcl':str(out/'CAPTURE13_FROZEN_PLAN.tcl'),'frozen_tcl_sha256':sha(out/'CAPTURE13_FROZEN_PLAN.tcl'),'footprint_changes':changes,'mutation_scope':'Exactly34PCBFootprint instancevalues; no source setter, no cache/default/graphics/name/value/pin/net/pose mutations.','run_arguments':[str(source),str(R/'w/sot34_cn2/LGA1700.DSN'),str(out/'CAPTURE13_FROZEN_PLAN.tcl'),str(R/'w/sot34_cn2_report')],'next_gate':'Root protected native apply to freshDSN, independent reopen XML fullordered inverse34FP only plus exact administrative metadata ledger, PST255 freshsource compare oldbody inverseJEDEC_TYPE34, and native PCB34 symbol replacements fullconnection verification. No final publication here.'}
comp=jr(out/'NATIVE_PLAN_COMPILATION.json');comp.update(status='FROZEN_NATIVE_FOOTPRINT_ONLY_34_PLAN_COMPILED_NOT_EXECUTED',plan_sha256=sha(fp),native_script=str(script),native_script_sha256=sha(script),scope=receipt['mutation_scope']);(out/'NATIVE_PLAN_COMPILATION.json').write_text(json.dumps(comp,ensure_ascii=False,indent=2),encoding='utf-8')
(O/'PREPARATION_RESULT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in receipt.items() if k!='footprint_changes'},ensure_ascii=False,indent=2))
