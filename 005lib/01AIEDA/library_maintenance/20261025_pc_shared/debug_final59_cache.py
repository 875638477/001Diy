from pathlib import Path
import json,sys,argparse,collections
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');G=R.parent/'cadence_geometry_merge_20261025';sys.path.insert(0,str(G));import compare_native_geometry as n
ap=argparse.ArgumentParser();ap.add_argument('--target',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();assert not a.out.exists()
r=next(x for x in json.loads((R/'w/pcb_migration/FINAL59_CACHE_FULL15_REVIEW.json').read_text())['results'] if x['name']==a.target)
lookup={};orig=n.digest
def traced(v):
 h=orig(v);lookup[h]=v;return h
n.digest=traced
class C(n.Native):
 def __init__(self,p):
  super().__init__(p)
  for attrs,props in self.nodes.values():
   if 'textBlock' in attrs:
    block=self.textblocks[str(attrs['textBlock'])];key='FULL_BLOCK_'+orig([(k,self.value(v,k)) for k,v in sorted(block.items()) if k not in ('name','userDefined')]);self.textblocks[key]=block;attrs['textBlock']=key
def expand(v):
 if isinstance(v,str) and v in lookup:return expand(lookup[v])
 if isinstance(v,list):return [expand(x) for x in v]
 if isinstance(v,dict):return {k:expand(x) for k,x in v.items()}
 return v
oa=C(r['actual_raw']);ob=C(r['public_raw']);x=oa.signature();y=ob.signature();xx=expand(x['signature']);yy=expand(y['signature']);diff=[]
def child_summary(o):
 root=o.nodes[str(o.selected[0])][0];out=[]
 for ident in root.get('children',[])+root.get('pins',[]):
  d=o.node(str(ident));attrs,props=o.nodes[str(ident)];out.append((d,attrs,props))
 return out
aa=child_summary(oa);bb=child_summary(ob);ca=collections.Counter(v[0] for v in aa);cb=collections.Counter(v[0] for v in bb)
unmatched={}
for label,items,counter in [('actual',aa,ca-cb),('public',bb,cb-ca)]:
 unmatched[label]=[]
 for h,attrs,props in items:
  if counter[h]>0:
   unmatched[label].append({'attrs':str(attrs),'props':str(props),'semantic':expand(h)});counter[h]-=1
def walk(a,b,path=''):
 if type(a)!=type(b):diff.append([path,a,b]);return
 if isinstance(a,dict):
  for k in sorted(set(a)|set(b)):walk(a.get(k),b.get(k),path+'/'+k)
 elif isinstance(a,list):
  if len(a)!=len(b):diff.append([path+'/length',len(a),len(b)])
  for i,(u,v) in enumerate(zip(a,b)):walk(u,v,path+'/'+str(i))
 elif a!=b:diff.append([path,a,b])
walk(xx,yy);a.out.write_text(json.dumps({'target':a.target,'actual':x,'public':y,'unmatched_children':unmatched,'diff':diff,'actual_expanded':xx,'public_expanded':yy},indent=2),encoding='utf-8')
print(json.dumps({'target':a.target,'diff_count':len(diff),'unmatched_children':unmatched},indent=2))
