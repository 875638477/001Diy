"""Fresh-process exact cache graph bijection, including typed instance edges.

Instances are external to the exported definition graph. Only the explicitly
typed instances edge can remap such DBIDs; all other fields retain v1 strictness.
Full actual symbol/pin identity is separately bound by the final2698/593 gate.
"""
from pathlib import Path
import argparse,hashlib,json,re
from review_native_cache_id_bijection_v1 import Graph,Compare,Atom
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
class FreshCompare(Compare):
 def __init__(self,a,b):super().__init__(a,b);self.instances={}
 def value(self,x,y,path):
  if isinstance(x,Atom) and isinstance(y,Atom):
   sx=str(x);sy=str(y)
   if sx not in self.a.objects and sy not in self.b.objects and re.fullmatch(r'dbid:[0-9A-Fa-f]+',sx) and re.fullmatch(r'dbid:[0-9A-Fa-f]+',sy) and re.search(r'/instances/\d+$',path):
    self.pointer(sx,sy,path,'typed_external_instance');self.instances[sx]=sy;self.field_count+=1;return
  return super().value(x,y,path)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--before',type=Path,required=True);ap.add_argument('--after',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 aa=Graph(a.before);bb=Graph(a.after);c=FreshCompare(aa,bb)
 try:proof=c.run();report=dict(status='PASS_FRESH_COMPLETE_NATIVE_CACHE_EXACT_EXPLICIT_TYPED_ID_BIJECTION',proof=proof,external_instance_edges_bijective=len(c.instances),mapping=c.forward,external_pointer_bijection=c.ext,instance_edge_mapping=c.instances,instance_semantic_identity_requires_separate_bound_full2698_593_gate=True)
 except (ValueError,AssertionError) as e:report=dict(status='FAIL_FRESH_STRICT_FULL_NATIVE_GRAPH_BIJECTION',error=str(e),objects_matched_before_failure=len(c.forward))
 report.update(before=str(a.before),before_sha256=sha(a.before),after=str(a.after),after_sha256=sha(a.after),comparator_sha256=sha(__file__),strict_core_comparator_sha256=sha(Path(__file__).with_name('review_native_cache_id_bijection_v1.py')))
 a.out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in report.items() if k not in ['mapping','external_pointer_bijection','instance_edge_mapping']},indent=2));return 0 if report['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
