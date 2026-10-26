"""Full four-view public-module readback gate: exact planned FP inverse and FUNC_DES bijection.
Hidden GROUND/POWER rows are preserved as full source-bound empty-function records.
"""
from pathlib import Path
from collections import Counter
import argparse,copy,hashlib,importlib.util,json
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
LEDGER=None
s=importlib.util.spec_from_file_location('source_native_function_id_gate',R/'tools/verify_public_brd_function_ids.py');F=importlib.util.module_from_spec(s);s.loader.exec_module(F)
V=F.V;need=V.need
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def restore_footprints(source,candidate,plan):
 b=copy.deepcopy(candidate);xs={r['REFDES']:r for r in source['comp']['rows']};ys={r['REFDES']:r for r in b['comp']['rows']}
 need(len(xs)==len(source['comp']['rows']) and len(ys)==len(b['comp']['rows']) and set(xs)==set(ys),'Full source/candidate component bijection failed')
 rows={r['ref']:r for r in plan['changes']};need(len(rows)==len(plan['changes']),'Duplicate per-ref FP plan')
 for ref,r in rows.items():
  need(ref in xs and xs[ref]['COMP_DEVICE_TYPE']==r['device_type']==ys[ref]['COMP_DEVICE_TYPE'],'Exact per-ref source device identity changed')
  need(r['new_package'].isascii() and r['new_package']==r['new_package'].lower(),'Expected explicitly lowercase ASCII public PSM target stem')
  need(xs[ref]['COMP_PACKAGE']==r['old_package'] and ys[ref]['COMP_PACKAGE']==r['new_package'].upper(),'Exact planned original/candidate COMP_PACKAGE uppercase native serialization mismatch '+ref)
  ys[ref]['COMP_PACKAGE']=r['old_package']
 return b
def invert_functions(source,candidate,ledger):
 b=copy.deepcopy(candidate);rows={(v['ref'],v['exact_path'],v['device_type']):v for v in ledger};counts=Counter();pncounts=Counter()
 source_hidden=Counter(tuple(v[f] for f in source['pin']['fields']) for v in source['pin']['rows'] if not v['FUNC_DES'] and not v['FUNC_LOGICAL_PATH'])
 candidate_hidden=Counter(tuple(v[f] for f in b['pin']['fields']) for v in b['pin']['rows'] if not v['FUNC_DES'] and not v['FUNC_LOGICAL_PATH'])
 need(source['pin']['fields']==b['pin']['fields'] and source_hidden==candidate_hidden,'Full hidden package GROUND/POWER records changed')
 for kind in ['func','pin']:
  for row in b[kind]['rows']:
   if kind=='pin' and not row['FUNC_DES'] and not row['FUNC_LOGICAL_PATH']:continue
   k=F.key(row);need(k in rows,'Function/pin references unlisted original function identity')
   v=rows[k];need(row['FUNC_DES']==v['after'],'Pin/function designator differs from exact declared same-function mapping')
   row['FUNC_DES']=v['before']
   if kind=='func':counts[k]+=1
   else:pncounts[k]+=1
 need(set(counts)==set(rows) and all(n==1 for n in counts.values()),'Complete function identity not covered exactly once')
 need(set(pncounts)==set(rows),'Orphan function or function with no exact pin records')
 return b,sum(source_hidden.values())
def review(x,y,plan):
 restored=restore_footprints(x,y,plan);ledger=F.derive(x,restored);restored,hidden=invert_functions(x,restored,ledger)
 need(LEDGER is not None and LEDGER['schema']=='MODULE008_EXACT_POST_ECO_DRC_STATUS_METADATA_V1','Exact one-field post-ECO DRC ledger required')
 for row in LEDGER['rows']:
  k=row['kind'];a,b=x[k]['job'],restored[k]['job'];need(len(a)==len(b)==12 and a[2:]==row['complete_source_nonvolatile_job_fields'] and b[2:]==row['complete_candidate_nonvolatile_job_fields'],'Other complete source/candidate J metadata changed')
  need(row['field']=='J.BOARD_DRC_STATUS' and row['job_index']==11 and row['source']=='UP TO DATE' and row['candidate']=='OUT OF DATE' and a[-1]==row['source'] and b[-1]==row['candidate'] and a[2:-1]==b[2:-1],'Only exact post-ECO pending DRC status may inverse')
  b[-1]=a[-1]
 complete=V.compare(x,restored)
 need(complete['status'].startswith('PASS'),'Complete native feedback fields changed beyond exact FP/function-ID inverse')
 return complete,ledger,hidden
def controls(x,y,plan):
 result=[]
 def reject(name,fn,planfn=None):
  b=copy.deepcopy(y);p=copy.deepcopy(plan);fn(b)
  if planfn:planfn(p)
  try:review(x,b,p)
  except (ValueError,KeyError):result.append({'name':name,'status':'PASS_REJECTED'})
  else:raise ValueError('Negative control accepted '+name)
 reject('package_wrong_target',lambda b:b['comp']['rows'][0].__setitem__('COMP_PACKAGE','WRONG'))
 reject('value_changed',lambda b:b['comp']['rows'][0].__setitem__('COMP_VALUE','WRONG'))
 reject('device_changed',lambda b:b['comp']['rows'][0].__setitem__('COMP_DEVICE_TYPE','WRONG'))
 reject('duplicate_component',lambda b:b['comp']['rows'].append(copy.deepcopy(b['comp']['rows'][0])))
 reject('function_path_changed',lambda b:b['func']['rows'][0].__setitem__('FUNC_LOGICAL_PATH','WRONG'))
 reject('pin_function_disagrees',lambda b:b['pin']['rows'][0].__setitem__('FUNC_DES','WRONG'))
 reject('pin_net_changed',lambda b:b['pin']['rows'][0].__setitem__('NET_NAME','WRONG'))
 reject('NC_empty_to_named',lambda b:next(r for r in b['pin']['rows'] if not r['NET_NAME']).__setitem__('NET_NAME','WRONG'))
 reject('missing_pin',lambda b:b['pin']['rows'].pop())
 reject('net_constraint_changed',lambda b:b['net']['rows'][0].__setitem__('NET_VOLTAGE','WRONG'))
 reject('unplanned_comp_property',lambda b:b['comp']['rows'][0].__setitem__('COMP_REUSE_ID','WRONG'))
 if any(not r['FUNC_DES'] and not r['FUNC_LOGICAL_PATH'] for r in y['pin']['rows']):
  reject('hidden_ground_power_row_changed',lambda b:next(r for r in b['pin']['rows'] if not r['FUNC_DES'] and not r['FUNC_LOGICAL_PATH']).__setitem__('NET_NAME','WRONG'))
 return result
def main():
 global LEDGER
 ap=argparse.ArgumentParser()
 for n in ['source-model','candidate-views','candidate-board','plan','mapped-pst-review','out']:ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--candidate-sha256',required=True);ap.add_argument('--job-ledger',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'Fresh output required');a.out.mkdir(parents=True);result={'status':'FAIL_COMPLETE_PUBLIC_MODULE_NATIVE_VIEWS'}
 try:
  model=load(a.source_model);plan=load(a.plan);pst=load(a.mapped_pst_review)
  LEDGER=load(a.job_ledger);need(sha(a.source_model)==LEDGER['source_model_sha256'] and model['native_source_sha256']==LEDGER['source_board_sha256'] and a.candidate_sha256.upper()==LEDGER['candidate_board_sha256']=='63CE53B7FBEB0063B56A957DFF958352CFAC5EE3153A8988D4395BDFC3674F10','Exact008 source/candidate J ledger binding differs');need({r['kind'] for r in LEDGER['rows']}=={'comp','func','net','pin'} and len(LEDGER['rows'])==4,'Complete four-view exact one-field ledger missing')
  for row in LEDGER['rows']:need(sha(row['source_view'])==row['source_view_sha256'] and sha(row['candidate_view'])==row['candidate_view_sha256'],'Frozen native J evidence changed')
  for p,h in LEDGER['stored_actual_DRC_evidence'].items():need(sha(p)==h,'Actual stored DRC evidence changed')
  need(model['status']=='UNIQUE_DEVICE_FUNCTION_PIN_BIJECTION' and not plan['unresolved'],'Source model or per-ref category unresolved')
  need(sha(a.source_model)==plan['source_model_sha256']==pst['source_model_sha256'],'Frozen complete source model mismatch')
  need(sha(a.plan)==pst['source_plan_sha256'],'Frozen mapped-PST footprint plan mismatch')
  need(sha(a.candidate_board)==a.candidate_sha256.upper(),'Fresh candidate board SHA mismatch')
  for f in pst['files']:need(sha(f['path'])==f['sha256'],'Mapped PST files changed')
  for kind,v in model['views'].items():need(sha(v['source'])==v['sha256'],'Original complete source views changed')
  source=Path(plan['source_board']);need(sha(source)==model['native_source_sha256']==plan['source_board_sha256']==pst['source_sha256'],'Protected original source board changed')
  x=model['views'];y=V.load_views(a.candidate_views);complete,ledger,hidden=review(x,y,plan)
  result.update({'status':'PASS_COMPLETE_PUBLIC_MODULE_VIEWS_FP_FUNCTION_IDS_EXACT_PENDING_DRC_METADATA','complete_inverse_review':complete,'ref_footprint_changes':len(plan['changes']),'native_package_serialization_ledger':[{'ref':r['ref'],'original_native_package':r['old_package'],'planned_public_PSM_stem':r['new_package'],'exact_candidate_native_package':r['new_package'].upper()} for r in plan['changes']],'function_renumber_ledger':ledger,'renumbered_functions':sum(r['before']!=r['after'] for r in ledger),'hidden_empty_function_package_pin_rows':hidden,'all_pin_records_preserved':len(x['pin']['rows'])==len(y['pin']['rows']),'negative_controls':controls(x,y,plan),'exact_job_DRC_status_metadata_ledger':LEDGER,'job_metadata_ledger_path':str(a.job_ledger),'job_metadata_ledger_sha256':sha(a.job_ledger)})
 except Exception as ex:result['error']=str(ex)
 result['inputs']={str(p):sha(p) for p in [a.source_model,a.candidate_board,a.plan,a.mapped_pst_review,a.job_ledger]};result['candidate_views']={str(p):sha(p) for p in a.candidate_views.glob('*View.dat') if p.is_file()};result['script_sha256']=sha(__file__);result['scope']='Complete four native feedback views only. All original field headers/order, per-record properties and multiplicities preserved after bounded per-ref package and same-function-ID inverse; hidden package pin records remain exact. Full device CLASS/PINUSE/PINSWAP/slots, constraints, geometry, copper and typed connectivity require separate native readback gates.'
 out=a.out/'PUBLIC_MODULE_MAPPED_COMPLETE_VIEWS_REVIEW.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'status':result['status'],'error':result.get('error'),'ref_footprint_changes':result.get('ref_footprint_changes'),'renumbered_functions':result.get('renumbered_functions'),'report':str(out)}));return 0 if result['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
