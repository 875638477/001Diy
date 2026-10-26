"""Full2698 typed pins, including21 nonlogical symbols, from actual0010 snapshot.

No CAD. Source mm4 grid, ordinary403 targets from independently native-read pads.
Retains duplicate/nil/empty identities; does not infer electrical attachment.
"""
from pathlib import Path
from collections import Counter
from decimal import Decimal,ROUND_HALF_UP
import copy,csv,hashlib,importlib.util,json
M=Path(__file__).parent;P=M/'w/public_brd0010_source_full13_v2';OUT=M/'public0010_full2698_expected13'
def need(v,m):
 if not v:raise ValueError(m)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
tab=lambda p:list(csv.DictReader(Path(p).open(encoding='utf-8-sig'),delimiter='\t',quoting=csv.QUOTE_NONE))
spec=importlib.util.spec_from_file_location('n',M/'review_global_suffix_native_chunks.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
def native(s):
 p=N.parse_many(s);need(len(p)==1,'Expected exactly one native scalar');return p[0]
def string(s):
 p=native(s);need(isinstance(p,str) and not isinstance(p,N.Atom),'Expected native quoted string');return p
q=lambda n:format(Decimal(str(n)).quantize(Decimal('.0001'),rounding=ROUND_HALF_UP),'f')
def jtype(raw):
 v=native(raw)
 return {'type':'ATOM','value':str(v),'native':raw} if isinstance(v,N.Atom) else {'type':'STRING','value':v,'native':raw}
def pin_native(p):return '('+p['number']+' ('+p['x']+' '+p['y']+') '+p['net']+' '+p['mechanical']+' '+p['through']+' '+p['padstack']+')'
def identity_native(g):
 s=g['symbol'];return '('+' '.join(['"LOGICAL"' if s['refdes']!='nil' else '"NONLOGICAL"',s['refdes'],s['component'],s['symbol_name'],s['definition'],'('+s['x']+' '+s['y']+')',s['rotation'],s['mirrored'],str(g['same_pose_occurrence'])])+')'
def dump(name,obj):p=OUT/name;p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');return p
def write_ilist(name,groups):
 p=OUT/name;p.write_text('\n'.join('('+identity_native(g)+' ('+' '.join(pin_native(p) for p in g['pins'])+'))' for g in groups)+'\n',encoding='utf-8');return p
def logical_ilist(name,groups):
 p=OUT/name;p.write_text('\n'.join('('+g['symbol']['refdes']+' ('+' '.join(pin_native(p) for p in g['pins'])+'))' for g in groups if g['symbol']['refdes']!='nil')+'\n',encoding='utf-8');return p
def main():
 need(not OUT.exists(),'Fresh expected-ledger output required');planpath=M/'public_four_module_fp_plans13_v4/0010_EXACT_FOOTPRINT_PLAN.json';plan=jr(planpath);launch=jr(P/'launch_report.json');source=Path(plan['source_board'])
 need(plan['source_board_sha256']==sha(source)==launch['source_sha256_before']==launch['source_sha256_after']==sha(P/'INPUT_COPY.brd'),'Source board/source snapshot hash mismatch');need(launch['exit_code']==0 and launch['input_unchanged'] and not launch['write_candidate'],'Source native snapshot job incomplete or writing')
 symbols,pins=tab(P/'symbols.tsv'),tab(P/'all_symbol_pins.tsv');need(len(symbols)==593 and len(pins)==2698,'Full source593/2698 cohort required')
 rows=jr(M/'public0010_403_endpoint_preflight13/0010_403_806_EXPECTED_PIN_IDEAL_DELTAS.json');preflight=jr(M/'public0010_403_endpoint_preflight13/0010_403_ENDPOINT_STROKE_PREFLIGHT.json');mapping={x['ref']:x for x in plan['changes']};need(len(mapping)==403 and len(rows)==806,'Full403/806 target cohort required')
 need({(x['ref'],x['old_package'],x['new_package']) for x in plan['changes']}=={(x['ref'],x['old_package'],x['target_package']) for x in preflight['rows']},'Updated v4 per-ref mapping differs from native target preflight')
 changes={(x['ref'],x['pin']):x for x in rows};need(len(changes)==806,'Duplicate target ref/pin')
 groups=[];seen=Counter();index=0;logical=set()
 for ordinal,s in enumerate(symbols):
  count=int(s['pin_count']);block=pins[index:index+count];need(len(block)==count,'Source pin block truncated');index+=count
  need(all(all(p[k]==s[k] for k in ('symbol_name','refdes','component')) for p in block),'Actual pin order does not correspond to symbol traversal')
  pose=tuple(s[k] for k in ('refdes','component','symbol_name','definition','x','y','rotation','mirrored'));occ=seen[pose];seen[pose]+=1
  if s['refdes']!='nil':need(string(s['refdes']) not in logical,'Duplicate logical refdes');logical.add(string(s['refdes']))
  groups.append({'source_symbol_ordinal':ordinal,'same_pose_occurrence':occ,'symbol':copy.deepcopy(s),'pins':copy.deepcopy(block)})
 need(index==2698 and len(logical)==572 and sum(g['symbol']['refdes']=='nil' for g in groups)==21,'All source logical/nonlogical symbols must be accounted')
 target=copy.deepcopy(groups);changed=[];observed=set()
 for g in target:
  s=g['symbol']
  if s['refdes']=='nil':continue
  ref=string(s['refdes'])
  if ref not in mapping:continue
  row=mapping[ref];need(string(s['definition']).casefold()==row['old_package'].casefold() and string(s['symbol_name']).casefold()==row['old_package'].casefold(),'Actual source symbol definition does not match logical plan '+ref)
  need(len(g['pins'])==2,'Ordinary migration must preserve two source pads');targetname=json.dumps(row['new_package']);s['definition']=targetname;s['symbol_name']=targetname
  for p in g['pins']:
   k=(ref,string(p['number']));need(k in changes and k not in observed,'Unexpected/duplicate migration pin '+str(k));observed.add(k);delta=changes[k];before=copy.deepcopy(p)
   need(p['mechanical']==p['through']=='nil','Ordinary source pin is not two-terminal SMT');need(string(p['padstack']).casefold()==delta['old_pad'].casefold(),'Source pad mismatch');need(string(p['net'])==delta['net'],'Source typed net mismatch');need([q(p['x']),q(p['y'])]==[q(v) for v in delta['old_world_mm']],'Source actual worldpin mismatch')
   need(sha(delta['target_native'])==delta['target_native_sha256'],'Cold target native proof changed')
   p['x'],p['y']=[q(v) for v in delta['target_world_mm']];p['padstack']=json.dumps(delta['target_pad']);p['symbol_name']=targetname
   changed.append({'ref':ref,'pin':string(p['number']),'before':before,'after':copy.deepcopy(p),'target_package':row['new_package'],'target_native':delta['target_native'],'target_native_sha256':delta['target_native_sha256']})
 need(observed==set(changes),'Some target pad rows unused');need(sum(len(g['pins']) for g in target)==2698,'Target2698 pad count changed')
 # This comparison preserves native strings vs atoms, duplicate numbering, all nonlogical identities and all unselected fields.
 for a,b in zip(groups,target):
  if a['symbol']['refdes']=='nil' or string(a['symbol']['refdes']) not in mapping:need(a==b,'Unselected source object changed')
  for p,t in zip(a['pins'],b['pins']):need(all(p[k]==t[k] for k in ('number','net','mechanical','through','refdes','component','rotation','rel_x','rel_y')),'Unapproved typed pad fields changed')
 OUT.mkdir();paths=[dump('SOURCE_593_SYMBOLS_2698_TYPED_PINS.json',groups),dump('TARGET_593_SYMBOLS_2698_TYPED_PINS.json',target),dump('CHANGED_403_REFS_806_TYPED_PINS.json',changed),write_ilist('SOURCE_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist',groups),write_ilist('TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist',target),logical_ilist('SOURCE_LOGICAL572_EXPECTED_PINS.ilist',groups),logical_ilist('TARGET_LOGICAL572_EXPECTED_PINS.ilist',target),write_ilist('NONLOGICAL21_SYMBOLS_UNCHANGED.ilist',[g for g in groups if g['symbol']['refdes']=='nil'])]
 report={'status':'PREPARED_SOURCE2698_TARGET2698_TYPED_PADS_NATIVE_READBACK_STILL_REQUIRED','source_board':str(source),'source_board_sha256':sha(source),'source_snapshot':str(P),'source_snapshot_launch_sha256':sha(P/'launch_report.json'),'source_symbols_sha256':sha(P/'symbols.tsv'),'source_pins_sha256':sha(P/'all_symbol_pins.tsv'),'exact_v4_plan':str(planpath),'exact_v4_plan_sha256':sha(planpath),'units':'millimeters','accuracy':4,'all_symbols':593,'logical_components':572,'nonlogical_symbols':21,'all_physical_pads':2698,'logical_physical_pads':sum(len(g['pins']) for g in groups if g['symbol']['refdes']!='nil'),'nonlogical_physical_pads':sum(len(g['pins']) for g in groups if g['symbol']['refdes']=='nil'),'changed_refs':403,'mapped_target_pads':806,'native_NIL_nets':sum(p['net']=='nil' for p in pins),'native_empty_string_nets':sum(p['net']=='""' for p in pins),'pin_schema':'Each full entry: ((KIND REF COMPONENT SYMBOL_NAME DEFINITION (X Y) ROT MIRROR SAME_POSE_OCCURRENCE) ((NUMBER (WORLDX WORLDY) NET MECH THROUGH PAD) ...)); rows preserve traversal order, duplicate numbered pads, native nil versus quoted strings. Nonlogical21 are matched by full name/definition/pose+same-pose occurrence, never collapsed under nil ref. Logical-only ilists retain existing v6 ref/pins schema.','target_grid':'Independent cold-native target ideal world XY, rounded to native destination mm4. Target source same-numbered worldpose delta0; angle corrections are not introduced. Actual native candidate must exactly read back target2698 and original915 GetConnect partitions.','outputs':{str(p):sha(p) for p in paths},'CAD_started':False,'public_modified':False}
 dump('FULL2698_LEDGER_PREPARATION_REVIEW.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
