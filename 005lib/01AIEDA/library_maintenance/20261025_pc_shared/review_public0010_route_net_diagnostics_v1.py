"""Independent offline review of actual2068 route /1739 via diagnostic outputs."""
from pathlib import Path
from collections import Counter
from decimal import Decimal
import csv,hashlib,json,sys
M=Path(__file__).parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
sys.path.insert(0,str(R.parent/'cadence_geometry_merge_20261025'))
from sexpr import parse_many,Atom
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
def typ(x):
 if isinstance(x,Atom):return ['ATOM',str(x)]
 if isinstance(x,str):return ['STRING',x]
 if isinstance(x,Decimal):return ['NUMBER',str(x)]
 return [typ(y) for y in x]
def main():
 D=M/'public0010_route_net_diagnostic_gate13_v1';assert not D.exists()
 N=M/'public0010_route_net_diagnostic_run13_v1';A=M/'public0010_stub_preflight_run13_v1'
 receipt=json.loads((N/'RUN_RECEIPT.json').read_text());assert receipt['status']=='COMPLETE_READONLY_ALL_BRANCH_PREFLIGHT' and receipt['public_unchanged'] and receipt['source_sha256_before']==receipt['source_sha256_after']=='008FEDC680EF5806D2C351CBF819F8A664D833D0A8D68D7A122306EE79C0A9AC'
 rows=parse_many((N/'ACTUAL2068_SOURCE_LINE_CURRENT_OBJECT_NETS.ilist').read_text());assert len(rows)==2068
 same=[];nil=[];missing=[];other=[]
 for source,actual in rows:
  if isinstance(actual,Atom):assert actual==Atom('nil');missing.append(typ(source));continue
  assert len(actual)==1
  if type(actual[0][2])==type(source[1]) and actual[0][2]==source[1]:same.append(source)
  elif isinstance(actual[0][2],Atom) and actual[0][2]==Atom('nil'):nil.append(dict(source=typ(source),actual_object=typ(actual[0])))
  else:other.append(dict(source=typ(source),actual_object=typ(actual[0])))
 assert [len(same),len(nil),len(missing),len(other)]==[1927,54,87,0]
 def rawvia(p):
  with p.open(newline='') as f:return [[parse_many(r[k])[0] for k in ['xy','padstack','net','properties']] for r in csv.DictReader(f,delimiter='\t',quoting=csv.QUOTE_NONE)]
 sv=rawvia(M/'w/public_brd0010_source_full13_v2/via_properties.tsv')
 tv=parse_many((N/'ACTUAL_ALL1739_VIAS.ilist').read_text());assert len(sv)==len(tv)==1739
 def key(r):return json.dumps(typ(r),separators=(',',':'))
 S=Counter(map(key,sv));T=Counter(map(key,tv));removed=list((S-T).elements());added=list((T-S).elements());assert len(removed)==len(added)==9
 sb={key(r[:2]):r for r in sv};tb={key(r[:2]):r for r in tv};assert len(sb)==len(tb)==1739 and sb.keys()==tb.keys()
 changed=[]
 for k,s in sb.items():
  t=tb[k];assert s[3]==t[3] and type(s[3])==type(t[3])
  if key(s)!=key(t):assert t[2]=='__NO_NET__';changed.append(dict(source=typ(s),target=typ(t)))
 assert len(changed)==9
 statuses=parse_many((A/'ALL_BRANCH_CANDIDATE_NATIVE_STATUS.ilist').read_text());counts=Counter(r[1] for r in statuses)
 assert counts=={'FIT_WHOLE_STROKE_INSIDE_TARGET_REGULAR_PAD':834,'ORIGINAL_SOURCE_STROKE_NOT_IN_CURRENT_SAME_NET_CU':144,'STROKE_OUTSIDE_TARGET_REGULAR_PAD':2}
 branches=parse_many((A/'FAILED_SOURCE_BRANCH_GROUPS.ilist').read_text());assert len(branches)==43 and len({tuple(r[0][:2]) for r in branches})==31
 inputs=[N/'RUN_RECEIPT.json',N/'SOURCE_ROUTE_AND_VIA_DIAGNOSTIC_COMPLETE.txt',N/'ACTUAL2068_SOURCE_LINE_CURRENT_OBJECT_NETS.ilist',N/'ACTUAL_ALL1739_VIAS.ilist',A/'RUN_RECEIPT.json',A/'ALL_SOURCE_BRANCH_PREFLIGHT_COMPLETE.txt',A/'ALL_BRANCH_CANDIDATE_NATIVE_STATUS.ilist',A/'FAILED_SOURCE_BRANCH_GROUPS.ilist',M/'w/public_brd0010_source_full13_v2/via_properties.tsv']
 report=dict(status='PASS_DIAGNOSTIC_CLASSIFICATION_ONLY_NOT_MIGRATION_APPROVAL',actual_candidate_sha256=receipt['source_sha256_before'],source_lines=2068,unique_same_net_source_lines=1927,source_exact_geometry_NIL_lines=54,no_exact_source_line_entity=87,wrong_non_nil_net_lines=0,all_vias=1739,via_XY_pad_properties_exact_except9_explicit_source_net_to_NO_NET=changed,source_NIL_route_lines=nil,no_exact_source_line_entities=missing,native_all_branch_preflight=dict(groups=877,fit=834,failed=43,failed_distinct_pins=31,unique_fitting_stubs=743,candidate_status_counts=counts),requires='Bounded frozen original-line NIL propagation only; 87 missing entities require full native source-own-Cu coverage, never assume missing geometry. All1739 via source net/properties and full915 exact physical partition members remain mandatory.',inputs={str(p):sha(p) for p in inputs})
 D.mkdir();p=D/'PUBLIC0010_ROUTE_AND_VIA_NET_DIAGNOSTIC_REVIEW.json';p.write_text(json.dumps(report,indent=2),'utf-8');print(json.dumps(dict(report=str(p),sha256=sha(p),status=report['status']),indent=2))
if __name__=='__main__':main()
