"""Fresh exact cache graph: explicit unique design-parent and instance ID edges."""
from pathlib import Path
import argparse,hashlib,json
from review_native_cache_id_bijection_fresh_v2 import Graph,FreshCompare,Atom
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
class CompleteFreshCompare(FreshCompare):
 def __init__(self,a,b):
  super().__init__(a,b)
  def parents(g):
   values=[str(x['parent']) for x,p in g.objects.values() if x.get('objType') in ('symdef','padstack') and str(x.get('parent')).startswith('dbid:') and str(x['parent']) not in g.objects]
   assert len(set(values))==1 and len(values)==171,'Expected unique design parent for79symdefs+92padstacks'
   return values[0]
  self.design_parent=(parents(a),parents(b));self.design_edges=0
 def value(self,x,y,path):
  if isinstance(x,Atom) and isinstance(y,Atom) and (str(x),str(y))==self.design_parent:
   assert path.endswith('/parent'),'Unclassified design-root reference'
   self.pointer(str(x),str(y),path,'typed_unique_design_parent');self.design_edges+=1;self.field_count+=1;return
  return super().value(x,y,path)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--before',type=Path,required=True);ap.add_argument('--after',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 aa=Graph(a.before);bb=Graph(a.after);c=CompleteFreshCompare(aa,bb)
 try:
  proof=c.run();assert c.design_edges==171
  report=dict(status='PASS_FRESH_COMPLETE_NATIVE_CACHE_EXACT_EXPLICIT_TYPED_ID_BIJECTION',proof=proof,external_instance_ids_bijective=len(c.instances),unique_design_parent_typed_edges=171,mapping=c.forward,external_pointer_bijection=c.ext,instance_edge_mapping=c.instances,instance_semantic_identity_requires_separate_bound_full2698_593_gate=True,design_context_requires_separate_bound_full_CFX_gate=True)
 except (ValueError,AssertionError) as e:report=dict(status='FAIL_FRESH_STRICT_FULL_NATIVE_GRAPH_BIJECTION',error=str(e),objects_matched_before_failure=len(c.forward))
 report.update(before=str(a.before),before_sha256=sha(a.before),after=str(a.after),after_sha256=sha(a.after),comparator_sha256=sha(__file__),typed_instance_comparator_sha256=sha(Path(__file__).with_name('review_native_cache_id_bijection_fresh_v2.py')),strict_core_comparator_sha256=sha(Path(__file__).with_name('review_native_cache_id_bijection_v1.py')))
 a.out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in report.items() if k not in ['mapping','external_pointer_bijection','instance_edge_mapping']},indent=2));return 0 if report['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
