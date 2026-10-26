"""Prepare only; root separately launches isolated CAD. Public files are read only."""
from pathlib import Path
import csv,hashlib,importlib.util,json,shutil
M=Path(__file__).parent;OUT=M/'public0010_native403_bundle13';LEDGER=M/'public0010_full2698_expected13';R=Path('D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
def need(v,m):
 if not v:raise ValueError(m)
def main():
 need(not OUT.exists(),'Fresh bundle required');base=R/'w/pcb_migration/pc13_native_replace_v6.il';text=base.read_text('utf-8-sig');need(text.count('1066')==4,'Unexpected v6 component count substitution cohort');text=text.replace('1066','572')
 source=jr(LEDGER/'SOURCE_593_SYMBOLS_2698_TYPED_PINS.json');target=jr(LEDGER/'TARGET_593_SYMBOLS_2698_TYPED_PINS.json');planpath=M/'public_four_module_fp_plans13_v4/0010_EXACT_FOOTPRINT_PLAN.json';plan=jr(planpath);mapping={r['ref']:r for r in plan['changes']};need(len(mapping)==403,'Exact403 physical changes required')
 OUT.mkdir();(OUT/'pc13_native_replace_base572.il').write_text(text,encoding='utf-8');shutil.copyfile(M/'tools/public0010_native403_v1.il',OUT/'public0010_native403_v1.il')
 for name in ['SOURCE_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist','TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist','SOURCE_LOGICAL572_EXPECTED_PINS.ilist','TARGET_LOGICAL572_EXPECTED_PINS.ilist','NONLOGICAL21_SYMBOLS_UNCHANGED.ilist']:shutil.copyfile(LEDGER/name,OUT/name)
 approved=[];adj=[]
 for a,b in zip(source,target):
  s=a['symbol']
  if s['refdes']=='nil':continue
  ref=json.loads(s['refdes']);old=json.loads(s['definition']);new=mapping[ref]['new_package'] if ref in mapping else old
  approved.append((ref,old,new,'0'))
  if ref in mapping:
   need(old.casefold()==mapping[ref]['old_package'].casefold(),'Source/plan package mismatch')
   for p,t in zip(a['pins'],b['pins']):adj.append('('+s['refdes']+' '+p['number']+' ('+p['x']+' '+p['y']+') ('+t['x']+' '+t['y']+'))')
 need(len(approved)==572 and len(adj)==806,'Full572/806 ledger coverage required')
 for name,rows in [('ALL572_APPROVED.tsv',approved),('MIGRATE403.tsv',[r for r in approved if r[0] in mapping])]:
  (OUT/name).write_text('refdes\tfrom_package\ttarget_package\tdelta\n'+'\n'.join('\t'.join(r) for r in rows)+'\n',encoding='utf-8')
 (OUT/'CHANGED806_SOURCE_TARGET_XY.ilist').write_text('\n'.join(adj)+'\n',encoding='utf-8')
 externals=[planpath,base,M/'tools/public0010_native403_v1.il',LEDGER/'FULL2698_LEDGER_PREPARATION_REVIEW.json',LEDGER/'EXPECTED_FIELDS_SCOPE.md',M/'public0010_403_endpoint_preflight13/0010_403_806_EXPECTED_PIN_IDEAL_DELTAS.json',M/'global_canonical_targets_review13/CANONICAL40_SOURCE_FULLGRAPH_REVIEW.json']
 manifest={'schema':'PUBLIC0010_403_NATIVE_CASE_BUNDLE_V1','state':'PREPARED_NOT_NATIVE_EXECUTED_NO_PUBLIC_WRITES','source_board':plan['source_board'],'source_board_sha256':plan['source_board_sha256'],'source_units':['millimeters',4],'components':572,'symbols':593,'physical_pads':2698,'logical_pads':2688,'nonlogical_symbols':21,'nonlogical_pads':10,'changed_refs':403,'changed_pads':806,'all_rotations_delta':0,'base_v6_substitution':'Only four1066 component coverage literals ->572; core proven v6 Alt/text/props/cloak/checkpoint functions otherwise byte text unchanged. Custom wrapper adds full593symbol/2698typedpin/native-source/target806adjacency and exactmm4 gate.','bundle_files':[{'path':str(p),'sha256':sha(p)} for p in OUT.iterdir() if p.is_file()],'external_proofs':[{'path':str(p),'sha256':sha(p)} for p in externals],'expected_native_apply_marker':'PUB403_APPLY_COMPLETE.txt','scope':'Alt403 candidate only. Actual source connectivity/copper/stubs and915partitions, IfSame logical update/props/CFX restore and independent fresh fullnative review remain required. No geometry coverage inference replacesGetConnect.'}
 p=OUT/'BUNDLE_MANIFEST.json';p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'bundle':str(OUT),'manifest_sha256':sha(p),'state':manifest['state']},indent=2))
if __name__=='__main__':main()
