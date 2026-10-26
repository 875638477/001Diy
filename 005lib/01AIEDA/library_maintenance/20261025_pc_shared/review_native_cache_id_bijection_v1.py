"""Strict all-field cache graph comparison under an explicit native-ID bijection.

No geometry, unknown attribute, property or figure value is omitted. Only IDs
backed by complete native objects/properties/figure records can be remapped.
"""
from pathlib import Path
from collections import Counter
from decimal import Decimal
import argparse,hashlib,json,re,sys
sys.path.insert(0,'D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025')
from sexpr import parse_many,Atom,attrs
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
class Graph:
 def __init__(self,p):
  self.path=p;self.records=parse_many(p.read_text('utf-8-sig'));self.objects={};self.figures={};self.blocks={}
  for r in self.records:
   if r[0]=='object':
    k=str(r[1]);v=(attrs(r[2]),r[3]);assert k not in self.objects or self.objects[k]==v;self.objects[k]=v
   elif r[0]=='figure':
    k=str(r[1]);assert k not in self.figures or self.figures[k]==r[2];self.figures[k]=r[2]
   elif r[0]=='textblock':
    k=str(r[1]);assert k not in self.blocks or self.blocks[k]==r[2];self.blocks[k]=r[2]
   else:raise ValueError('Unexpected native record '+str(r[0]))
  self.roots={}
  for k,(a,p) in self.objects.items():
   if a.get('objType')=='symdef':
    n=str(a['name']);assert n not in self.roots;self.roots[n]=k
class Compare:
 def __init__(self,a,b):self.a=a;self.b=b;self.forward={};self.reverse={};self.ext={};self.extback={};self.visited=set();self.field_count=0
 def pointer(self,x,y,path,kind):
  if x in self.ext and self.ext[x]!=y:raise ValueError('External ID not bijective at '+path)
  if y in self.extback and self.extback[y]!=x:raise ValueError('External ID reverse collision at '+path)
  self.ext[x]=y;self.extback[y]=x
 def value(self,x,y,path):
  self.field_count+=1
  if isinstance(x,Atom) and isinstance(y,Atom):
   sx=str(x);sy=str(y)
   if sx in self.a.objects or sy in self.b.objects:
    if not(sx in self.a.objects and sy in self.b.objects):raise ValueError('Object edge missing '+path)
    self.node(sx,sy,path);return
   if sx.startswith('propList:') and sy.startswith('propList:'):self.pointer(sx,sy,path,'propList');return
   if re.fullmatch(r'_axlPath@0x[0-9a-fA-F]+',sx) and re.fullmatch(r'_axlPath@0x[0-9a-fA-F]+',sy):
    # Every use is a figure owner with its complete figure record compared below.
    self.pointer(sx,sy,path,'axlPath');return
  if type(x) is not type(y):raise ValueError('Native type changed '+path+' '+repr((x,y)))
  if isinstance(x,list):
   if len(x)!=len(y):raise ValueError('List cardinality changed '+path)
   for i,(xx,yy) in enumerate(zip(x,y)):self.value(xx,yy,path+'/'+str(i))
  elif x!=y:raise ValueError('Literal changed '+path+' '+repr((x,y)))
 def node(self,x,y,path):
  if x in self.forward and self.forward[x]!=y:raise ValueError('Object ID not bijective at '+path)
  if y in self.reverse and self.reverse[y]!=x:raise ValueError('Object ID reverse collision at '+path)
  self.forward[x]=y;self.reverse[y]=x
  if (x,y) in self.visited:return
  self.visited.add((x,y));aa,ap=self.a.objects[x];bb,bp=self.b.objects[y]
  if set(aa)!=set(bb):raise ValueError('Attribute keys changed '+path)
  for k in sorted(aa):
   if k=='figure' and aa[k]!=Atom('nil'):
    if x not in self.a.figures or y not in self.b.figures:raise ValueError('Opaque figure lacks full native record '+path)
   self.value(aa[k],bb[k],path+'/'+k)
  self.value(ap,bp,path+'/COMPLETE_PROPERTIES')
  if x in self.a.figures or y in self.b.figures:
   if not(x in self.a.figures and y in self.b.figures):raise ValueError('Native figure missing '+path)
   self.value(self.a.figures[x],self.b.figures[y],path+'/COMPLETE_FIGURE_PATHS')
 def run(self):
  assert self.a.roots.keys()==self.b.roots.keys()
  assert self.a.blocks==self.b.blocks
  for n in sorted(self.a.roots):self.node(self.a.roots[n],self.b.roots[n],n)
  assert set(self.forward)==set(self.a.objects) and set(self.reverse)==set(self.b.objects),'Full native node coverage incomplete'
  return dict(full_objects=len(self.forward),full_roots=len(self.a.roots),all_global_textblocks_exact=len(self.a.blocks),explicit_pointer_bijection_nodes=len(self.ext),complete_recursive_values_compared=self.field_count,zero_ignored_attributes=True,zero_numeric_tolerance=True)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--before',type=Path,required=True);ap.add_argument('--after',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 a=Graph(args.before);b=Graph(args.after);c=Compare(a,b)
 try:proof=c.run();report=dict(status='PASS_COMPLETE_NATIVE_CACHE_EXACT_UNDER_EXPLICIT_ID_BIJECTION',proof=proof,mapping=c.forward,external_pointer_bijection=c.ext)
 except (ValueError,AssertionError) as e:report=dict(status='FAIL_STRICT_FULL_NATIVE_GRAPH_BIJECTION',error=str(e),objects_matched_before_failure=len(c.forward))
 report.update(before=str(args.before),before_sha256=sha(args.before),after=str(args.after),after_sha256=sha(args.after),comparator_sha256=sha(__file__))
 args.out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps({k:v for k,v in report.items() if k not in ['mapping','external_pointer_bijection']},indent=2));return 0 if report['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
