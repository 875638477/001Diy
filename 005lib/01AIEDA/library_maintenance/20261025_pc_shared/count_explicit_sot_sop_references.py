from pathlib import Path
from collections import Counter
import json,hashlib,csv,xml.etree.ElementTree as ET
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared');R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');OUT=M/'global_canonical_publish_v1'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
names=['ao3414_sot23-3','sot23-3','ao4468_so8','sop-8-150mil','sot23_123']
xml=R/'w/xn1/native_design.xml';x=ET.parse(xml).getroot();ledger=jr(R/'w/pcb_migration/FINAL_INSTANCE_MAPPING.json');byid={r['dbid']:r for r in ledger};inst=[]
for p in x.iter('PartInst'):
 d=p.find('Defn');props={z.get('name'):z.get('val','') for z in p.findall('./PartInstUserProp/Defn')};v=props.get('PCB Footprint')
 if v and v.lower() in names:inst.append({'ref':byid[d.get('dbId')]['ref'],'page':byid[d.get('dbId')]['page'],'id':d.get('dbId'),'footprint':v,'instance':d.get('name')})
counts=Counter(r['footprint'].lower() for r in inst)
usage=jr(M/'global_suffix_reference_audit_v1/PUBLIC_BRD_REFERENCE_AUDIT.json');boards=[]
old=jr(Path(r'D:\001DIY\004computer\lga1700\cadence_library_cleanup_20261025\usage_audit\usage_counts.json'))
for s in old['sources']:
 if '\\01brdlib\\' not in s['source'].lower():continue
 assert sha(s['source'])==s['sha256'];boards.append({'source':s['source'],'sha256':s['sha256'],'placed':{n:s['counts']['psm'].get(n,0) for n in names},'declared':{n:s['counts']['declared_psm'].get(n,0) for n in names}})
olbp=R/'verification/public_olb_footprint_audit13_v4/PUBLIC_OLB_FOOTPRINT_REFERENCE_AUDIT.json';olb=jr(olbp);oc=Counter()
for n,v in olb['all_PCB_Footprint_value_counts'].items():oc[n.lower()]+=v
with (R/'w/final_alt13/symbols.tsv').open(encoding='utf-8-sig',newline='') as f:
 sy=list(csv.DictReader(f,delimiter='\t',quoting=csv.QUOTE_NONE))
def uq(v):return v[1:-1] if v.startswith('"') and v.endswith('"') else v
pc=Counter(uq(r['symbol_name']).lower() for r in sy)
l=jr(R/'w/final_alt13/launch_report.json');assert sha(l['source'])==l['source_sha256_after']
result={'status':'READONLY_EXACT_NAME_REFERENCE_COUNTS_WITH_SOURCE_BINDINGS','names':{},'project13_capture_native_xml':str(xml),'project13_capture_native_xml_sha256':sha(xml),'project13_cn1_DSN':str(R/'w/cn1/LGA1700.DSN'),'project13_cn1_DSN_sha256':sha(R/'w/cn1/LGA1700.DSN'),'project13_native_PCB_snapshot':str(R/'w/final_alt13/symbols.tsv'),'project13_native_PCB_snapshot_sha256':sha(R/'w/final_alt13/symbols.tsv'),'project13_native_PCB_source':l['source'],'project13_native_PCB_source_sha256':l['source_sha256_after'],'public_OLB_audit':str(olbp),'public_OLB_audit_sha256':sha(olbp),'public_board_counts':boards,'capture_matching_instances':inst,'limits':['Counts use exact footprint fields and actual native package names with casefold only, notValue/MPN/texttrace substring hits.','ProjectPCB is frozen49AF native snapshot before newSOT34 remap; copper-only followup does not imply different footprint names but new release must recheck.','No AO-specific active references in these audited sources means oldaliases may retire after backup; it does not authorize direct substitution in an unknown already-routed design.']}
for n in names:result['names'][n]={'project13_capture_instances':counts[n],'project13_native_PCB_placed_symbols':pc[n],'public37_OLB_PCB_Footprint_fields':oc[n],'public7_BRD_placed_symbols':sum(b['placed'][n] for b in boards),'public7_BRD_declared_packages':sum(b['declared'][n] for b in boards)}
(OUT/'EXPLICIT_SOT_SOP_ACTIVE_REFERENCE_COUNTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result['names'],indent=2))
