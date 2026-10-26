"""Exact module CNS gate with frozen source-origin/save metadata and bounded independent collection order."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,xml.etree.ElementTree as E
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
s=importlib.util.spec_from_file_location('strict_module_cfx_v4',R/'tools/verify_public_module_cfx_v4.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
F=C.F;need=C.need;sha=C.sha;load=C.load;local=lambda t:t.rsplit('}',1)[-1]
def canon(x):return json.loads(json.dumps(F.B.canonical_xml(x)))
def digest(x):return hashlib.sha256(repr(F.B.canonical_xml(x)).encode()).hexdigest().upper()
def unique(parent,tag,name):
 q=[e for e in parent if local(e.tag)==tag and e.get('Name')==name];need(len(q)==1,'Exact unique object/attribute missing '+tag+'/'+name);return q[0]
def origins(source,target,ledger):
 out=[]
 for row in ledger['origins']:
  a=unique(unique(C.section(source,row['section']),'object',row['object']),'attribute',row['attribute']);b=unique(unique(C.section(target,row['section']),'object',row['object']),'attribute',row['attribute'])
  need(canon(a)==row['source_full_attribute'] and canon(b)==row['candidate_full_attribute'],'Bound complete source/candidate origin metadata payload changed '+row['object']+'/'+row['attribute'])
  u=[e for e in a.iter() if local(e.tag)=='origin'];v=[e for e in b.iter() if local(e.tag)=='origin'];need(len(u)==len(v)==1 and len(u[0])==len(v[0])==1,'Origin field shape changed')
  need(u[0][0].text==row['source_origin'] and v[0][0].text==row['candidate_origin'],'Exact frozen origin pair changed');v[0][0].text=u[0][0].text;need(canon(a)==canon(b),'Additional origin attribute payload differences');out.append(row)
 return out

def attr_order(source,target,board):
 out=[]
 if board!='00012':return out
 # Frozen source cohort: only 19 explicit Nets with exactly these two width attributes,
 # and exactly their 19 BGA_BGA Region-Net overrides. References/members never reorder.
 nets=['GND','1.2V','1.8V','VCCA_ADC','DC_IN','3.3V','3.3V_SW','1.8V_SW','GND_ADC','N55694102','N55693920','GND_DAC','VCCA_PLL2','VCCA_PLL4','VCCA_PLL3','VCCA_PLL1','GND_PLL','VCCA_ADC_OUT','VCCA_DAC_OUT']
 regions={'BGA_BGA:N:NET_'+n for n in nets};targets=[]
 hasnet=[any(local(e.tag)=='xml-objects' and e.get('Name')=='Net' for e in z.iter()) for z in [source,target]]
 need(hasnet[0]==hasnet[1],'Net collection presence differs')
 if hasnet[0]:
  aa,bb=C.section(source,'Net'),C.section(target,'Net')
  for n in nets:targets.append(('Net/'+n,unique(aa,'object',n),unique(bb,'object',n)))
 aa=unique(C.section(source,'Region'),'object','BGA_BGA');bb=unique(C.section(target,'Region'),'object','BGA_BGA')
 def regionnets(x):
  q=[e for e in x if local(e.tag)=='children' and e.get('Kind')=='RegionClass'];need(len(q)==1,'Exact Region-Net container missing');return q[0]
 aa,bb=regionnets(aa),regionnets(bb)
 for n in sorted(regions):targets.append(('Region/BGA_BGA/Net/'+n,unique(aa,'object',n),unique(bb,'object',n)))
 for path,a,b in targets:
  need(a.tag==b.tag and a.attrib==b.attrib and len(a)==len(b),'Whole width-override object shape changed')
  xa=[(i,e) for i,e in enumerate(a) if local(e.tag)=='attribute'];xb=[(i,e) for i,e in enumerate(b) if local(e.tag)=='attribute']
  need([e.get('Name') for i,e in xa]==['MIN_NECK_WIDTH','MIN_LINE_WIDTH'] and [i for i,e in xa]==[0,1],'Frozen source width attribute cohort shape changed')
  need([i for i,e in xb]==[0,1] and {e.get('Name') for i,e in xb}=={'MIN_NECK_WIDTH','MIN_LINE_WIDTH'},'Candidate width attribute shape/multiplicity changed')
  names=[e.get('Name') for i,e in xb];vals={e.get('Name'):e for i,e in xb}
  need(all(canon(e)==canon(vals[e.get('Name')]) for i,e in xa),'Whole source constraint width value/origin/scope payload changed')
  need([canon(e) for e in a[2:]]==[canon(e) for e in b[2:]],'Non-attribute Region reference/member order/payload changed')
  if names!=['MIN_NECK_WIDTH','MIN_LINE_WIDTH']:
   b[:]=[vals['MIN_NECK_WIDTH'],vals['MIN_LINE_WIDTH']]+list(b)[2:];out.append({'path':path,'source_attribute_order':['MIN_NECK_WIDTH','MIN_LINE_WIDTH'],'candidate_attribute_order':names,'complete_attributes_and_other_child_relative_order_exact':True,'inverse_whole_object_sha256':digest(b)})
  need(canon(a)==canon(b),'Whole width override object differs')
 return out

def collections(source,target,model,proof):
 out=[];fns={r['before']:r for r in proof['function_renumber_ledger']};pins={k:set() for k in fns}
 for f in model['function_slot_matches']:
  k=f['function_designator'];need(k in fns and (fns[k]['ref'],fns[k]['exact_path'],fns[k]['device_type'])==(f['ref'],f['function_path'],f['device_type']),'Full source function identity changed')
  for logical,physical in f['logical_to_physical']:pins[k].add(f['ref']+'.'+physical)
 for kind in ['Gate','Part','PartDefn']:
  wrappers=[[e for e in r.iter() if local(e.tag)=='xml-objects' and e.get('Name')==kind] for r in [source,target]]
  need(len(wrappers[0])==len(wrappers[1]) and len(wrappers[0])<=1,'Collection presence changed '+kind)
  if not wrappers[0]:continue
  a,b=wrappers[0][0][0],wrappers[1][0][0];need(a.tag==b.tag and a.attrib==b.attrib,'Collection root shape changed');aa={e.get('Name'):e for e in a};bb={e.get('Name'):e for e in b}
  need(len(aa)==len(a) and len(bb)==len(b) and None not in aa and None not in bb and set(aa)==set(bb),'Collection full unique-name bijection changed '+kind)
  if kind=='Gate':
   for name,x in aa.items():
    y=bb[name]
    if canon(x)==canon(y):continue
    ux=[(i,e) for i,e in enumerate(x) if local(e.tag)=='children' and e.get('Kind')=='Pin'];uy=[(i,e) for i,e in enumerate(y) if local(e.tag)=='children' and e.get('Kind')=='Pin'];need(len(ux)==len(uy)==1 and ux[0][0]==uy[0][0],'Only exact one Gate Pin child container may reorder')
    u,v=ux[0][1],uy[0][1];need(u.tag==v.tag and u.attrib==v.attrib=={'Kind':'Pin'},'Gate Pin container fields changed')
    key=lambda e:(e.get('Name'),e.get('AltName'))
    need(all(local(e.tag)=='object' and set(e.attrib)=={'Name','AltName'} for e in list(u)+list(v)),'Whole Pin object identity shape changed')
    ak,bk=[key(e) for e in u],[key(e) for e in v];av,bv={key(e):e for e in u},{key(e):e for e in v};need(len(ak)==len(av) and len(bk)==len(bv) and set(av)==set(bv),'Whole Pin multiplicity/identity changed')
    need(name in pins and {k[0] for k in av}<=pins[name],'Whole Pin endpoints do not bind original native function slot');need(all(canon(av[k])==canon(bv[k]) for k in av),'Whole Pin subtree payload/internal order changed')
    v[:]=[bv[k] for k in ak];need(canon(x)==canon(y),'Other full Gate fields changed')
    out.append({'kind':'source_function_bound_whole_Pin_object_outer_order','Gate':name,'source_function_identity':fns[name],'candidate_order':bk,'source_order':ak,'complete_objects_including_all_attributes_children_internal_order_exact':True})
  need(all(canon(aa[k])==canon(bb[k]) for k in aa),'Complete native named-object payload differs '+kind)
  ak,bk=[e.get('Name') for e in a],[e.get('Name') for e in b]
  if ak!=bk:b[:]=[bb[k] for k in ak];out.append({'kind':'whole_independent_'+kind+'_outer_order','candidate_order':bk,'source_order':ak,'full_object_and_multiplicity_exact':True})
 return out

def revision(a,b,ledger,ext):
 rows=[r for r in ledger['revision'] if r['extension']==ext];need(len(rows)==1,'Exact save revision ledger missing');r=rows[0];x=[e for e in a.iter() if local(e.tag)=='revisionNumber'];y=[e for e in b.iter() if local(e.tag)=='revisionNumber'];need(len(x)==len(y)==1 and x[0].tag==y[0].tag==r['tag'] and x[0].attrib==r['source_attrs'] and y[0].attrib==r['candidate_attrs'],'Exact frozen native save-counter pair changed');need(int(r['candidate_attrs']['physical'])==int(r['source_attrs']['physical'])+1 and {k:v for k,v in r['source_attrs'].items() if k!='physical'}=={k:v for k,v in r['candidate_attrs'].items() if k!='physical'},'Ledger exceeds exact bookkeeping counter');y[0].set('physical',x[0].get('physical'));return r

def review(a,b,model,plan,proof,ledger,ext):
 a,b=copy.deepcopy(a),copy.deepcopy(b);parts=C.inverse_partdefn(a,b,model,plan) if ext=='dcfx' else [];origin=origins(a,b,ledger) if ext=='dcfx' else [];rev=revision(a,b,ledger,ext);attrs=attr_order(a,b,ledger['board']);order=collections(a,b,model,proof);need(canon(a)==canon(b),'Other complete ordered native CFX/TCFX rule/property/scope payload changed');return {'PartDefn':parts,'explicit_source_origin_metadata_changes':origin,'native_save_revision':rev,'exact_width_attribute_order':attrs,'whole_object_order':order}

def main():
 ap=argparse.ArgumentParser()
 for n in ['source','candidate','source-model','plan','view-proof','metadata-ledger','out']:ap.add_argument('--'+n,type=Path,required=True)
 z=ap.parse_args();need(not z.out.exists(),'Fresh output required');z.out.mkdir(parents=True);r={'status':'FAIL_MODULE_CNS_BOUND_METADATA_GATE'}
 try:
  model,plan,proof,ledger=map(load,[z.source_model,z.plan,z.view_proof,z.metadata_ledger]);need(ledger['schema']=='PUBLIC_MODULE_BOUND_SOURCE_METADATA_V1','Unknown metadata ledger');need(sha(z.source_model)==plan['source_model_sha256'],'Source model changed');need(proof['status'] in {'PASS_COMPLETE_PUBLIC_MODULE_VIEWS_ONLY_PLANNED_FP_AND_FUNCTION_IDS','PASS_COMPLETE_PUBLIC_MODULE_VIEWS_FP_FUNCTION_IDS_EXACT_PENDING_DRC_METADATA'},'Complete four-view proof not PASS');candidate_sha=load(z.candidate/'launch_report.json')['source_sha256_before'];F.bind(z.source,model['native_source_sha256'],'PUBLIC_BOARD_COMPLETE.txt');F.bind(z.candidate,candidate_sha,'PUBLIC_BOARD_COMPLETE.txt');need(ledger['source_board_sha256']==model['native_source_sha256'] and ledger['candidate_board_sha256']==candidate_sha,'Frozen origin/revision native board binding changed');need(proof['inputs'][str(z.plan)]==sha(z.plan),'Full view proof plan differs');need([v for p,v in proof['inputs'].items() if p.lower().endswith('.brd')]==[candidate_sha],'Native view proof candidate SHA differs')

  if proof['status']=='PASS_COMPLETE_PUBLIC_MODULE_VIEWS_FP_FUNCTION_IDS_EXACT_PENDING_DRC_METADATA':
   jl=load(Path(proof['job_metadata_ledger_path']));need(sha(proof['job_metadata_ledger_path'])==proof['job_metadata_ledger_sha256'] and jl==proof['exact_job_DRC_status_metadata_ledger'] and jl['schema']=='MODULE008_EXACT_POST_ECO_DRC_STATUS_METADATA_V1' and jl['candidate_board_sha256']=='63CE53B7FBEB0063B56A957DFF958352CFAC5EE3153A8988D4395BDFC3674F10','Unproved exact008 post-ECO J metadata ledger')
  expect={'00012':79,'006':20,'008':10};need(ledger['board'] in expect and len(ledger['origins'])==expect[ledger['board']],'Exact origin cohort changed');pairs={(v['section'],v['object'],v['attribute']) for v in ledger['origins']};need(len(pairs)==len(ledger['origins']),'Duplicate origin cohort')
  r['proofs']={};trees={}
  for ext in ['dcfx','tcfx']:
   row=next(v for v in ledger['revision'] if v['extension']==ext);need(sha(z.source/f'ACTUAL_SUPPLEMENT.{ext}')==row['source_cfx_sha256'] and sha(z.candidate/f'ACTUAL_SUPPLEMENT.{ext}')==row['candidate_cfx_sha256'],'Frozen complete native CFX file changed')
   a=E.parse(z.source/f'ACTUAL_SUPPLEMENT.{ext}').getroot();b=F.cfx_inverse(z.candidate/f'ACTUAL_SUPPLEMENT.{ext}',proof['function_renumber_ledger']) if ext=='dcfx' else E.parse(z.candidate/f'ACTUAL_SUPPLEMENT.{ext}').getroot();r['proofs'][ext]=review(a,b,model,plan,proof,ledger,ext);trees[ext]=(a,b)
  controls=[]
  def reject(name,fn,ext='dcfx'):
   a,b=map(copy.deepcopy,trees[ext]);fn(b)
   try:review(a,b,model,plan,proof,ledger,ext)
   except (ValueError,KeyError):controls.append({'name':name,'status':'PASS_REJECTED'})
   else:raise ValueError('Negative control accepted '+name)
  for prop in ['MIN_LINE_WIDTH','RELATIVE_PROPAGATION_DELAY_CNS','VOLTAGE','REUSE_ID','SIGNAL_MODEL']:
   nodes=[e for e in trees['dcfx'][1].iter() if local(e.tag)=='attribute' and e.get('Name')==prop]
   if nodes:
    def remove(b,prop=prop):
     e=next(e for e in b.iter() if local(e.tag)=='attribute' and e.get('Name')==prop);p=next(p for p in b.iter() if e in list(p));p.remove(e)
    reject('remove_'+prop,remove)
  reject('change_rule_value',lambda b:next(e for e in b.iter() if local(e.tag)=='value' and 'Value' in e.attrib).set('Value','WRONG'))
  reject('wrong_unapproved_origin',lambda b:next(e for e in b.iter() if local(e.tag)=='origin')[0].__setattr__('text','WRONG'))
  reject('physical_revision_other_value',lambda b:next(e for e in b.iter() if local(e.tag)=='revisionNumber').set('physical','999'))
  reject('TCFX_scope_or_value',lambda b:next(e for e in b.iter() if local(e.tag)=='value' and 'Value' in e.attrib).set('Value','WRONG'),'tcfx')
  reject('missing_named_object',lambda b:C.section(b,'Part').remove(list(C.section(b,'Part'))[0]))
  reject('duplicate_named_object',lambda b:C.section(b,'Gate').append(copy.deepcopy(list(C.section(b,'Gate'))[0])))
  r.update({'status':'PASS_FULL_SOURCE_RULES_VALUES_SCOPE_WITH_EXPLICIT_SOURCE_METADATA_LEDGER','source_board_sha256':model['native_source_sha256'],'candidate_board_sha256':candidate_sha,'exact_origin_metadata_change_count':len(ledger['origins']),'all_other_full_ordered_CFX_TCFX_fields_exact':True,'negative_controls':controls})
 except Exception as ex:r['error']=str(ex)
 r['inputs']={str(p):sha(p) for p in [z.source_model,z.plan,z.view_proof,z.metadata_ledger]+[d/n for d in [z.source,z.candidate] for n in ['launch_report.json','ACTUAL_SUPPLEMENT.dcfx','ACTUAL_SUPPLEMENT.tcfx']]};r['script_sha256']=sha(__file__);r['scope']='Every source CNS rule value, object, inheritance/reference scope and property is preserved. Only the exact frozen source-origin metadata flags and native save counter are different; complete independent objects and whole source-function-bound Pin objects may permute with all internal fields/order preserved. This explicitly does not claim byte-identical origin metadata.';out=z.out/'PUBLIC_MODULE_COMPLETE_CFX_REVIEW.json';out.write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps({'status':r['status'],'error':r.get('error'),'origin_metadata_changes':r.get('exact_origin_metadata_change_count'),'report':str(out)}));return 0 if r['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
