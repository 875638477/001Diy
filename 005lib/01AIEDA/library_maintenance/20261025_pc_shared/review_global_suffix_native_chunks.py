"""Read-only, rerunnable review of COMPLETE native chunks. Never starts CAD or modifies inputs."""
from pathlib import Path
from collections import Counter,defaultdict
from decimal import Decimal,localcontext
import argparse,hashlib,json,re,sys
B=Path(r'D:\001DIY\004computer\lga1700\cadence_geometry_merge_20261025')
sys.path.insert(0,str(B))
from sexpr import parse_many,attrs,Atom
NIL=Atom('nil')
FACT={'mils':Decimal('.0254'),'millimeters':Decimal(1),'microns':Decimal('.001'),'inches':Decimal('25.4'),'centimeters':Decimal(10)}
ADMIN={'VERSION_ID','LIBRARY_PATH','LAST_SAVED_NAME','EDIT_TIME'}
NON_GEOM_HANDLES={'parent','instances','component','net','branch','parentGroups','prop','readOnly'}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def stable(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def digest(v):return hashlib.sha256(stable(v).encode()).hexdigest().upper()
def jread(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def val(v):
 if isinstance(v,list):return [val(x) for x in v]
 if isinstance(v,Atom):return {'atom':str(v)}
 if isinstance(v,Decimal):return {'number':str(v)}
 if isinstance(v,str):return {'string':v}
 return v

def number(n,f):
 with localcontext() as c:
  c.prec=80;x=n*f
  return '0' if x==0 else format(x.normalize(),'f')
def mm(v,f):
 if isinstance(v,list):return [mm(x,f) for x in v]
 if isinstance(v,Decimal):return number(v,f)
 return val(v)

def inspect(path):
 forms=parse_many(path.read_text(encoding='utf-8-sig'))
 assert forms[-1]==[Atom('complete'),Atom('t')], 'No complete native export'
 meta=next(x for x in forms if x[0]=='meta');units=str(meta[2][0]);factor=FACT[units]
 nodes={str(x[1]):(attrs(x[2]),x[3]) for x in forms if x[0]=='object'}
 assert len(nodes)==sum(x[0]=='object' for x in forms),'Duplicate native identity'
 figures={str(x[1]):x[2] for x in forms if x[0]=='figure'}
 blocks={str(x[1]):attrs(x[2]) for x in forms if x[0]=='textblock'}
 selected=next(x[1] for x in forms if x[0]=='selected')
 assert len(selected)==1,'Expected one selected definition'
 sid=str(selected[0]);s,sp=nodes[sid];assert s['objType']=='symdef'
 padrefs=set();padfiles={};issues=[];memo={};visiting=set()
 def norm(v):
  if isinstance(v,list):return [norm(x) for x in v]
  if isinstance(v,Atom) and str(v) in nodes:return node(str(v))
  if isinstance(v,Atom) and re.match(r'(dbid|pad|propList):',v):
   issues.append('UNRESOLVED_REFERENCE:'+str(v));return {'unresolved':str(v)}
  if '@0x' in str(v):issues.append('OPAQUE_NATIVE_VALUE:'+str(v))
  return val(v)
 def node(ident):
  if ident in memo:return memo[ident]
  assert ident not in visiting,'Graph cycle outside parent context'
  visiting.add(ident);a,props=nodes[ident];kind=str(a.get('objType',''));out=[]
  for key,v in sorted(a.items()):
   if key in NON_GEOM_HANDLES:continue
   if ident==sid and key=='name':continue
   if key=='figure' and ident in figures:out.append([key,norm(figures[ident])]);continue
   if key=='textBlock' and str(v) in blocks:out.append([key,[[k,norm(x)] for k,x in sorted(blocks[str(v)].items())]]);continue
   out.append([key,norm(v)])
  props2=[] if props==NIL else [[str(r[0]),norm(r[1:])] for r in props if str(r[0]) not in ADMIN]
  result={'attrs':out,'props':props2};visiting.remove(ident);memo[ident]=result;return result
 pins=[]
 for ident in s.get('pins',[]):
  a,props=nodes[str(ident)];dn=str(a.get('definition',NIL));d,dp=nodes[dn]
  assert d['objType']=='padstack','Pin does not resolve to padstack'
  padrefs.add(str(d['name']))
  dpdict={} if dp==NIL else {str(r[0]):r[1:] for r in dp}
  libpath=dpdict.get('LIBRARY_PATH',[])
  if len(libpath)==1 and isinstance(libpath[0],str):
   actualpad=Path(libpath[0]);padfiles[str(actualpad)]={'path':str(actualpad),'sha256':sha(actualpad) if actualpad.is_file() else None,'source_name':str(d['name'])}
  else:issues.append('PAD_LIBRARY_PATH_ABSENT_OR_AMBIGUOUS:'+str(d['name']))
  padlayers=[]
  for padid in d.get('pads',[]):
   pa,pp=nodes[str(padid)]
   padlayers.append({'layer':str(pa.get('layer','')),'type':str(pa.get('type','')),'figure_name':str(pa.get('figureName','')),'bbox_mm':mm(pa.get('bBox',NIL),factor),'offset_mm':mm(pa.get('offset',NIL),factor),'native_complete_attrs':{k:val(v) for k,v in pa.items() if k not in ('parent','readOnly','figure')},'native_figure':val(figures.get(str(padid),NIL))})
  pins.append({'number':str(a.get('number','')),'pad_name':str(d.get('name','')),'local_xy_mm':mm(a.get('relxy',a.get('xy',NIL)),factor),'local_rotation':val(a.get('relRotation',a.get('rotation',NIL))),'mirror_type':val(a.get('mirrorType',NIL)),'is_mechanical':a.get('isMech',NIL)!=NIL,'is_through':a.get('isThrough',NIL)!=NIL or d.get('isThrough',NIL)!=NIL,'usage':str(d.get('usage','')),'hole_type':str(d.get('holeType','')),'drill_diameter_mm':mm(d.get('drillDiameter',NIL),factor),'drill_size_mm':[mm(d.get(k,NIL),factor) for k in ('drillSizeWidth','drillSizeHeight')],'plating':val(d.get('plating',NIL)),'pad_layers':padlayers})
 pins.sort(key=lambda p:(p['number'],stable(p['local_xy_mm'])))
 core=[{k:v for k,v in p.items() if k!='pad_name'} for p in pins]
 graph={'units_and_accuracy':val(meta[2]),'selected_graph':node(sid),'step':val(next(x[1:] for x in forms if x[0]=='step'))}
 lengths={}
 if len(pins)==2:
  xy1,xy2=[p['local_xy_mm'] for p in pins]
  if all(isinstance(xy,list) and len(xy)==2 and all(isinstance(n,str) for n in xy) for xy in (xy1,xy2)):
   dx=Decimal(xy2[0])-Decimal(xy1[0]);dy=Decimal(xy2[1])-Decimal(xy1[1])
   lengths={'dx_mm':str(dx),'dy_mm':str(dy),'pitch_squared_mm2':str(dx*dx+dy*dy)}
 return {'native_path':str(path),'native_sha256':sha(path),'meta':val(meta),'package_placement_bounds':[{'layer':str(x.get('layer','')),'bbox_mm':mm(x.get('bBox',NIL),factor)} for x,_ in nodes.values() if 'PLACE_BOUND' in str(x.get('layer','')) and x.get('objType')=='shape'],'units':units,'accuracy':val(meta[2][1]),'pin_count':len(pins),'pin_numbers':[p['number'] for p in pins],'duplicate_pin_numbers':[n for n,c in Counter(p['number'] for p in pins).items() if c>1],'pins':pins,'pitch':lengths,'pad_dependencies':sorted(padrefs),'actual_loaded_pad_files':sorted(padfiles.values(),key=lambda p:p['path'].lower()),'full_ordered_graph_fingerprint':digest(graph),'physical_core_fingerprint':digest(core),'graph_normalization':'Only runtime DBIDs followed recursively; parent/instances/component/net/branch/parentGroups/prop/readOnly handles omitted; explicit user properties retained except VERSION_ID/LIBRARY_PATH/LAST_SAVED_NAME/EDIT_TIME; selected asset name omitted. All remaining fields, annotations/text/font and order retained, units preserved. Not a full external PAD XML manufacturing equivalence proof.','issues':sorted(set(issues))}

def scope(item,e):
 fam=item['family'];stem=item['stem'].lower();pins=e['pins']
 if fam=='EXPLICIT_SOT_SO':return 'USER_EXPLICIT_SOT_SO_OR_CANARY_COMPARISON'
 if fam=='NUMERIC_WITHOUT_COMPONENT_CATEGORY':return 'CATEGORY_AMBIGUOUS_KEEP_UNTIL_ALL_REFERENCE_REDIRECTION'
 if len(pins)!=2:return 'FUNCTIONAL_NON_TWO_TERMINAL_PRESERVE'
 if any(p['is_mechanical'] for p in pins):return 'MECHANICAL_PIN_SCHEMA_PRESERVE_REVIEW'
 if any(p['is_through'] or any(isinstance(v,str) and Decimal(v)>0 for v in [p['drill_diameter_mm']]+p['drill_size_mm']) for p in pins):return 'THROUGH_HOLE_SCHEMA_PRESERVE_REVIEW'
 if e['duplicate_pin_numbers'] or set(e['pin_numbers'])!={'1','2'}:return 'SPECIAL_NUMBERING_SCHEMA_PRESERVE_REVIEW'
 if re.search(r'(?i)(qfn|[34]p|p_r[+-]?d)',stem):return 'FUNCTIONAL_NAME_STRUCTURAL_VARIANT_PRESERVE'
 if fam=='c' and item['size'] not in {'0201','0402','0603','0805','1206','1210','1812'}:return 'SPECIAL_CAPACITOR_MATERIAL_OR_FORM_PRESERVE_REVIEW'
 return 'ORDINARY_TWO_TERMINAL_SMT_STANDARDIZATION_ELIGIBLE_AFTER_DEPENDENCY_AND_REFERENCE_GATES'

def pin_summary(e):
 out=[]
 for p in e['pins']:
  out.append({k:p[k] for k in ('number','pad_name','local_xy_mm','local_rotation','mirror_type','is_mechanical','is_through','usage','hole_type','drill_diameter_mm','drill_size_mm')} | {'layers':[{'layer':x['layer'],'type':x['type'],'figure':x['figure_name'],'bbox_mm':x['bbox_mm'],'offset_mm':x['offset_mm']} for x in p['pad_layers'] if x['figure_name'] not in ('NULL','nil','')]})
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--plan',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--intent-overrides',type=Path);ap.add_argument('--canonical-overrides',type=Path);a=ap.parse_args()
 a.output.mkdir(exist_ok=True,parents=True);overrides={x['stem'].lower():x for x in jread(a.intent_overrides)['overrides']} if a.intent_overrides else {};canonicals={x['stem'].lower():x for x in jread(a.canonical_overrides)['overrides']} if a.canonical_overrides else {};plan=jread(a.plan);frozen={r['stem'].lower():r for r in plan['representatives']};done=[];pending=[];errors=[];chunks=[]
 for chunk in sorted(list(a.native.glob('c[0-9][0-9][0-9]'))+list(a.native.glob('e[0-9][0-9][0-9][0-9][0-9]'))):
  report=chunk/'launch_report.json'
  if not report.exists():pending.append(str(chunk));continue
  try:rec=jread(report)
  except json.JSONDecodeError:pending.append(str(chunk));continue
  if rec.get('exit_code')!=0 or not rec.get('complete') or rec.get('outputs')!=rec.get('expected'):pending.append(str(chunk));continue
  rows=jread(chunk/'manifest.json');chunkrows=[]
  for row in rows:
   item=frozen[row['stem'].lower()];assert row['source_sha256']==item['sha256'];path=Path(row['audit_output'])
   try:
    e=inspect(path);e.update({'stem':item['stem'],'source':item['path'],'source_sha256':item['sha256'],'family':item['family'],'size':item['size'],'canonical_candidate':item['canonical_candidate'],'scope':scope(item,e)})
    if e['stem'].lower() in overrides:
     ov=overrides[e['stem'].lower()];assert ov['source_sha256']==e['source_sha256'] and ov['native_sha256']==e['native_sha256'],'Frozen intent override identity mismatch'
     e['scope_before_intent_review']=e['scope'];e['scope']=ov['classification'];e['intent_override']=ov
    if e['stem'].lower() in canonicals:
     co=canonicals[e['stem'].lower()];assert co['source_sha256']==e['source_sha256'],'Frozen canonical override identity mismatch'
     assert frozen[co['canonical'].lower()]['sha256']==co['canonical_source_sha256'],'Canonical target source mismatch'
     e['canonical_candidate']=co['canonical'];e['canonical_override']=co
    chunkrows.append(e)
   except Exception as ex:errors.append({'stem':row['stem'],'path':str(path),'error':str(ex)})
  done.extend(chunkrows);chunks.append({'path':str(chunk),'launch_report_sha256':sha(report),'manifest_sha256':sha(chunk/'manifest.json'),'complete_exports_reviewed':len(chunkrows)})
  dump(a.output/(chunk.name+'_SCHEMA_GEOMETRY.json'),chunkrows)
 indexed={e['stem'].lower():e for e in done};diffs=[]
 for e in done:
  target=e['canonical_candidate'];canonical=indexed.get(target.lower()) if target else None
  if canonical:
   diffs.append({'source':e['stem'],'target':target,'scope':e['scope'],'same_complete_ordered_graph_fingerprint':e['full_ordered_graph_fingerprint']==canonical['full_ordered_graph_fingerprint'],'same_native_four_layer_core_fingerprint':e['physical_core_fingerprint']==canonical['physical_core_fingerprint'],'source_pin_numbers':e['pin_numbers'],'target_pin_numbers':canonical['pin_numbers'],'source_pitch':e['pitch'],'target_pitch':canonical['pitch'],'source_pin_summary':pin_summary(e),'target_pin_summary':pin_summary(canonical),'source_native_path':e['native_path'],'target_native_path':canonical['native_path'],'note':'Mismatch does not make ordinary two-terminal variants undeletable after user-authorized standardization, but dimensions/mask/pin-number changes must be recorded. Functional variants remain preserved.'})
  elif target:diffs.append({'source':e['stem'],'target':target,'scope':e['scope'],'canonical_native_not_yet_available':True})
 dump(a.output/'CANONICAL_DIMENSION_DELTAS.json',diffs)
 summary={'status':'PARTIAL_READONLY_NATIVE_CHUNK_REVIEW_NO_LIBRARY_MUTATION','planned':len(frozen),'reviewed':len(done),'remaining_assets':len(frozen)-len(done),'native_chunks_reviewed':chunks,'pending_chunks':pending,'errors':errors,'scope_counts':dict(Counter(e['scope'] for e in done)),'full_native_export_sha_bound':True,'external_full_pad_xml_manufacturing_proof':'NOT_ASSERTED_BY_THIS_REPORT; actual loaded PAD paths and current SHA must additionally be bound before final standardization/removal','public_guard_final_gate':'Runner final report with all planned941 exports+13361 public files unchanged required before mutation','all_native_schemas':[{k:e[k] for k in ('stem','scope','pin_count','pin_numbers','pad_dependencies','canonical_candidate','issues')} for e in done]}
 if len(done)==len(frozen) and not errors:summary['status']='ALL_NATIVE_SCHEMAS_REVIEWED_REQUIRES_FULL_PAD_REFERENCES_AND_PUBLIC_POSTGUARD'
 dump(a.output/'NATIVE_REVIEW_SUMMARY.json',summary)
 print(json.dumps({k:v for k,v in summary.items() if k not in ('all_native_schemas','native_chunks_reviewed')},ensure_ascii=False))
if __name__=='__main__':main()
