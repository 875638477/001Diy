"""Full original0010 CFX gate: actual403 FP/FUNC inverse and one observed MAX.

No rule/origin/date/revision waiver. One exact readOnly STRING administrative
MAX value and its whole attribute outer move are authenticated by native probes.
"""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,re,sys,xml.etree.ElementTree as E
M=Path(__file__).resolve().parents[1];R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
sys.path.insert(0,str(R.parent/'cadence_geometry_merge_20261025'));from sexpr import parse_many,Atom
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
load=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
def need(ok,msg):
 if not ok:raise ValueError(msg)
def module(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C6=module(M/'tools/verify_public_module_cfx_v6.py','strict_module_cfx_bounded_helpers');C=C6.C;F=C.F
local=lambda t:t.rsplit('}',1)[-1]
def probe(d,board,value):
 q=load(d/'launch_report.json');need(q['source_sha256_before']==q['source_sha256_after']==q['staged_sha256']==board and q['input_unchanged'] and not q['write_candidate'] and q['exit_code']==0 and '-readonly' in q['arguments'],'Native MAX readonly probe bound another board or mutable job')
 need(sha(d/'INPUT_COPY.brd')==board and sha(q['script'])==q['script_sha256'],'Native MAX probe input/helper changed')
 p=d/'MAX_PROPERTY_PROBE.ilist';lines=p.read_text('utf-8-sig').splitlines();entry=[s for s in lines if s.startswith('ENTRY_DETAILS=')];need(len(entry)==1,'MAX dictionary ambiguous')
 attrs=parse_many(entry[0].split('=',1)[1])[0];D=dict(zip(map(str,attrs[::2]),attrs[1::2]))
 need(D['dataType']=='STRING' and D['readOnly']==Atom('t') and D['name']=='MAX_FILENAME_VALUE' and D['objects']==['designs','layouts'],'MAX dictionary is not exact native readOnly STRING design/layout property')
 fields=[]
 helper=M/'tools/public0010_body_max_readonly27.il'
 need(sha(helper)=='992C285A5F62646EB918D105E3497BB99D70276C92CAA7473DFE74B182F7ACFD','Frozen exact source MAX probe helper changed')
 if Path(q['script']).name=='public0010_body_max_readonly27.il':
  need(q['script_sha256']==sha(helper),'Standalone MAX probe helper identity differs')
 else:
  need(Path(q['script']).name=='public0010_final_full_composite27.il' and q['script_sha256']=='7EEB571F143F09DDCCDCC5849F3D8933F77D299A39063D9B46C2B7FD73B9D07A','Only exact observed final0010 composite wrapper is accepted')
  need('load("D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/tools/public0010_body_max_readonly27.il")' in Path(q['script']).read_text('utf-8'),'Exact composite did not load frozen MAX helper')
  need((d/'FINAL_FULL_BODY_MAX_593_COMPOSITE_COMPLETE.txt').is_file() and (d/'MAX_PROPERTY_READONLY_COMPLETE.txt').is_file(),'Exact composite MAX completion markers missing')
 for prefix in ['BEFORE=','AFTER=']:
  rows=[s for s in lines if s.startswith(prefix)];need(len(rows)==1,'MAX full property probe missing');a=parse_many(rows[0].split('=',1)[1])[0];matches=[r for r in a if str(r[0])=='MAX_FILENAME_VALUE'];need(matches==[[Atom('MAX_FILENAME_VALUE'),value]],'MAX actual observed string differs frozen pair');fields.append(a)
 need(fields[0]==fields[1],'Readonly probe changed any full native design property')
 return dict(directory=str(d),board_sha256=board,expected_value=value,probe_sha256=sha(p),native_launch_sha256=sha(d/'launch_report.json'),full_dictionary_readonly_STRING=True,all_design_properties_unchanged=True)
def max_inverse(a,b,old,new):
 u,v=C.section(a,'Design'),C.section(b,'Design');need(len(u)==len(v)==1,'Full Design object cohort differs');u,v=u[0],v[0]
 ua=[(i,e) for i,e in enumerate(u) if local(e.tag)=='attribute' and e.get('Name')=='MAX_FILENAME_VALUE'];va=[(i,e) for i,e in enumerate(v) if local(e.tag)=='attribute' and e.get('Name')=='MAX_FILENAME_VALUE'];need(len(ua)==len(va)==1,'MAX attribute missing/duplicate')
 i,x=ua[0];j,y=va[0];xv=[e for e in x if local(e.tag)=='value'];yv=[e for e in y if local(e.tag)=='value'];need(len(xv)==len(yv)==1 and xv[0].attrib=={'Value':old} and yv[0].attrib=={'Value':new},'CFX MAX scalar shape/frozen source/candidate pair changed')
 yv[0].set('Value',old);need(F.B.canonical_xml(x)==F.B.canonical_xml(y),'Other MAX complete attribute fields changed')
 v.remove(y);v.insert(i,y);need(F.B.canonical_xml(u)==F.B.canonical_xml(v),'Other complete Design attributes/scope/relative order changed')
 return dict(section='Design',object=u.get('Name'),attribute='MAX_FILENAME_VALUE',source_value=old,candidate_value=new,source_outer_attribute_index=i,candidate_outer_attribute_index=j,complete_MAX_attribute_except_one_value_exact=True,all_other_Design_children_order_and_payload_exact=True)
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 for n in ['candidate-native','view-proof','source-max-probe','candidate-max-probe','out']:ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--candidate-sha256',required=True);ap.add_argument('--expected-source-max',required=True);ap.add_argument('--expected-candidate-max',required=True);a=ap.parse_args();need(not a.out.exists(),'Fresh output required');a.out.mkdir();report=dict(status='FAIL_COMPLETE0010_CFX')
 source=M/'w/public_brd0010_source_full13_v2';modelpath=R/'verification/public_brd_device_model13_0010_v2/DEVICE_VIEW_EXACT_MODEL.json';planpath=M/'public_four_module_fp_plans13_v4/0010_EXACT_FOOTPRINT_PLAN.json'
 try:
  model,plan,proof=map(load,[modelpath,planpath,a.view_proof]);source_sha='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898';candidate_sha=a.candidate_sha256.upper()
  need(model['native_source_sha256']==source_sha and sha(modelpath)==plan['source_model_sha256'],'Frozen source complete model/plan mismatch');need(proof['status']=='PASS_COMPLETE_PUBLIC_MODULE_VIEWS_ONLY_PLANNED_FP_AND_FUNCTION_IDS' and proof['inputs'][str(planpath)]==sha(planpath),'Full actual4views plan proof absent')
  need([v for p,v in proof['inputs'].items() if p.lower().endswith('.brd')]==[candidate_sha],'Fullviews proof another candidate SHA');F.bind(source,source_sha,'PUBLIC_BOARD_COMPLETE.txt');F.bind(a.candidate_native,candidate_sha,'PUBLIC_BOARD_COMPLETE.txt')
  need(a.expected_source_max=='20624','Original0010 frozen MAX value changed');need(a.expected_candidate_max.isdecimal(),'Candidate MAX observation must be exact numeric STRING')
  probes=[probe(a.source_max_probe,source_sha,a.expected_source_max),probe(a.candidate_max_probe,candidate_sha,a.expected_candidate_max)]
  def review(x,y,ext):
   x,y=copy.deepcopy(x),copy.deepcopy(y);parts=C.inverse_partdefn(x,y,model,plan) if ext=='dcfx' else []
   orders=C6.collections(x,y,model,proof);admin=max_inverse(x,y,a.expected_source_max,a.expected_candidate_max)
   need(F.B.canonical_xml(x)==F.B.canonical_xml(y),'Other complete ordered CFX/TCFX source rule,origin,date,revision,value or scope changed')
   return dict(PartDefn_exact_source_device_inverse=parts,whole_function_bound_objects=orders,one_exact_readonly_MAX_ledger=admin)
  trees={};checks={}
  for ext in ['dcfx','tcfx']:
   x=E.parse(source/('ACTUAL_SUPPLEMENT.'+ext)).getroot();y=F.cfx_inverse(a.candidate_native/('ACTUAL_SUPPLEMENT.'+ext),proof['function_renumber_ledger']) if ext=='dcfx' else E.parse(a.candidate_native/('ACTUAL_SUPPLEMENT.'+ext)).getroot();trees[ext]=(x,y);checks[ext]=review(x,y,ext)
  controls=[]
  def reject(name,fn,ext='dcfx'):
   x,y=map(copy.deepcopy,trees[ext]);fn(y)
   try:review(x,y,ext)
   except (ValueError,KeyError,AssertionError):controls.append(dict(name=name,status='PASS_REJECTED'))
   else:raise ValueError('Negative control accepted '+name)
  reject('MAX_unobserved_value',lambda z:next(e for e in z.iter() if local(e.tag)=='attribute' and e.get('Name')=='MAX_FILENAME_VALUE')[0].set('Value','999999'))
  reject('other_constraint_value',lambda z:next(e for e in z.iter() if local(e.tag)=='attribute' and e.get('Name')=='MECH_PIN_TO_CONDUCTOR_SPACING')[0].set('Value','999'))
  reject('origin_flag',lambda z:next(e for e in z.iter() if local(e.tag)=='origin')[0].__setattr__('text','UNAPPROVED'))
  reject('Gate_object_drop',lambda z:C.section(z,'Gate').remove(C.section(z,'Gate')[0]))
  reject('PartDefn_duplicate',lambda z:C.section(z,'PartDefn').append(copy.deepcopy(C.section(z,'PartDefn')[0])))
  reject('TCFX_extra_attribute',lambda z:next(e for e in z.iter() if local(e.tag)=='value').set('UNAPPROVED','1'),'tcfx')
  report.update(status='PASS_FULL0010_SOURCE_CFX_TCFX_EXACT_WITH_ONE_NATIVE_READONLY_MAX_LEDGER',source_board_sha256=source_sha,candidate_board_sha256=candidate_sha,native_MAX_readonly_probes=probes,proofs=checks,negative_controls=controls,no_rule_origin_date_revision_scope_exception=True)
 except Exception as ex:report['error']=repr(ex)
 paths=[modelpath,planpath,a.view_proof]+[d/n for d in [source,a.candidate_native] for n in ['launch_report.json','ACTUAL_SUPPLEMENT.dcfx','ACTUAL_SUPPLEMENT.tcfx']]+[d/n for d in [a.source_max_probe,a.candidate_max_probe] for n in ['launch_report.json','MAX_PROPERTY_PROBE.ilist']]
 report['inputs']={str(p):sha(p) for p in paths if p.is_file()};report['script_sha256']=sha(__file__);p=a.out/'PUBLIC0010_COMPLETE_CFX_REVIEW.json';p.write_text(json.dumps(report,indent=2),'utf-8');print(json.dumps(dict(status=report['status'],error=report.get('error'),report=str(p),sha256=sha(p)),indent=2));return 0 if report['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
