"""Adversarial in-memory controls for the full79 fresh cache bijection gate."""
from pathlib import Path
from copy import deepcopy
from decimal import Decimal
import argparse,hashlib,json
from review_native_cache_id_bijection_fresh_v3 import Graph,CompleteFreshCompare,Atom
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--before',type=Path,required=True);ap.add_argument('--after',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);z=ap.parse_args()
 a=Graph(z.before);b=Graph(z.after);rootname=sorted(a.roots)[0];sa=a.roots[rootname];sb=b.roots[rootname];cases=[]
 def reject(name,mutate):
  undo=mutate()
  try:
   try:CompleteFreshCompare(a,b).run()
   except (ValueError,AssertionError) as e:cases.append(dict(mutation=name,result='REJECTED',reason=str(e)))
   else:raise RuntimeError('Negative control accepted '+name)
  finally:undo()
 def attr(g,k,name,value):
  d=g.objects[k][0];present=name in d;old=d.get(name);d[name]=value
  def undo():
   if present:d[name]=old
   else:del d[name]
  return undo
 reject('new_unknown_attribute_is_not_ignored',lambda:attr(b,sb,'UNCLASSIFIED_ADDED_FIELD',Atom('t')))
 def arbitrary_external():
  ua=attr(a,sa,'UNCLASSIFIED_EXTERNAL_POINTER',Atom('dbid:00ABCDEF11111111'));ub=attr(b,sb,'UNCLASSIFIED_EXTERNAL_POINTER',Atom('dbid:00ABCDEF22222222'))
  return lambda:(ua(),ub())
 reject('unclassified_external_DBID_may_not_remap',arbitrary_external)
 def design_break():return attr(b,sb,'parent',Atom('dbid:00DEADBEEF123456'))
 reject('unique_design_parent_cannot_split_or_alias',design_break)
 def instance_alias():
  k=next(k for k,(x,p) in b.objects.items() if x.get('objType')=='symdef' and isinstance(x.get('instances'),list) and len(x['instances'])>=2)
  v=list(b.objects[k][0]['instances']);v[0]=v[1];return attr(b,k,'instances',v)
 reject('external_instance_bijection_duplicate_target_is_rejected',instance_alias)
 def instance_drop():
  k=next(k for k,(x,p) in b.objects.items() if x.get('objType')=='symdef' and isinstance(x.get('instances'),list) and len(x['instances'])>0)
  return attr(b,k,'instances',list(b.objects[k][0]['instances'])[1:])
 reject('external_instance_cardinality_is_exact',instance_drop)
 def geometry():
  k=next(k for k,(x,p) in b.objects.items() if x.get('objType')=='pad' and isinstance(x.get('bBox'),list))
  v=deepcopy(b.objects[k][0]['bBox']);v[0][0]+=Decimal('0.0001');return attr(b,k,'bBox',v)
 reject('one_mm4_pad_geometry_step_is_rejected',geometry)
 def figure():
  k=next(iter(b.figures));old=b.figures[k];v=deepcopy(old);v[0][2][0][0][0]+=Decimal('0.0001');b.figures[k]=v
  return lambda:b.figures.__setitem__(k,old)
 reject('complete_opaque_figure_coordinates_are_not_ignored',figure)
 def prop():
  old=b.objects[sb];b.objects[sb]=(old[0],[[Atom('UNCLASSIFIED_PROPERTY'),Atom('t')]])
  return lambda:b.objects.__setitem__(sb,old)
 reject('full_unknown_property_payload_is_not_ignored',prop)
 def block():
  k=next(iter(b.blocks));old=b.blocks[k];b.blocks[k]=old+[Atom('UNCLASSIFIED_FONT_FIELD'),Decimal(1)]
  return lambda:b.blocks.__setitem__(k,old)
 reject('global_textblock_all_fields_are_exact',block)
 def unused():
  name='L_VLCF5020_CU_';old=b.roots.pop(name);return lambda:b.roots.__setitem__(name,old)
 reject('unused_symbol_definition_cannot_be_omitted',unused)
 positive=CompleteFreshCompare(a,b);proof=positive.run()
 report=dict(status='PASS_ALL_FRESH79_TYPED_BIJECTION_NEGATIVE_CONTROLS_REJECTED',negative_controls=cases,positive_control_full_restored_graph=proof,before=str(z.before),before_sha256=sha(z.before),after=str(z.after),after_sha256=sha(z.after),tests_mutate_memory_only=True,files_unchanged=True,comparator_sha256=sha(Path(__file__).with_name('review_native_cache_id_bijection_fresh_v3.py')),test_sha256=sha(__file__))
 z.out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps(dict(status=report['status'],controls=len(cases),report=str(z.out),sha256=sha(z.out)),indent=2))
if __name__=='__main__':main()
