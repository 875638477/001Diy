from pathlib import Path
import re,json,csv,collections,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022');H=R.parent/'lessonHI_38_50_20261021'
def sx(s):
 ts=re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+',s);i=0
 def take():
  nonlocal i
  v=ts[i];i+=1
  if v=='(':
   a=[]
   while ts[i]!=')':a.append(take())
   i+=1;return a
  if v.startswith('"'):return json.loads(v)
  if v=='nil':return None
  if v=='t':return True
  try:return float(v)
  except:return v
 return take()
def data(p,manual=True):
 r=list(csv.DictReader([x for x in p.read_text(encoding='utf8').splitlines() if not x.startswith('ACTUAL_PATH_SEGMENTS_COMPLETE')],delimiter='\t',quotechar='\0'));r=[x for x in r if sx(x['isEtch']) and (not manual or not sx(x['thermal']))]
 return collections.Counter((sx(x['net']),sx(x['layer']),float(x['width']),tuple(sorted(tuple(v) for v in sx(x['startEnd'])))) for x in r)
checks=[]
for label,a,b in [('J55_2L',H/'logs/reopen_padentry_2L_b019_stored/hi_route_roles.tsv',R/'logs/native_j55_2L_reopen_01/hi_route_roles.tsv'),('J55_4L',H/'logs/reopen_padentry_4L_b019_stored/hi_route_roles.tsv',R/'logs/native_j55_4L_reopen_01/hi_route_roles.tsv'),('NEWSTACK_4L',R/'logs/native_j55_4L_reopen_01/hi_route_roles.tsv',R/'logs/native_newstack_4L_reopen_01/hi_route_roles.tsv'),('CORRECTED_NATIVE_SEGMENT_READER',R/'logs/native_newstack_4L_reopen_01/hi_route_roles.tsv',R/'logs/native_newstack_reference_segments_01/actual_path_segments.tsv')]:
 x=data(a);y=data(b);checks.append({'label':label,'before':str(a),'after':str(b),'beforeActualManualSegments':x.total(),'afterActualManualSegments':y.total(),'missing':sum((x-y).values()),'added':sum((y-x).values()),'passed':x==y and x.total()>0})
for check in checks:assert check['passed'],check
p=R/'native/manual_copper_preservation_validation.json';p.write_text(json.dumps({'status':'PASS_NONEMPTY_ACTUAL_NATIVE_MANUAL_SEGMENT_MULTISET','method':'Real native hi_route_roles records; preserve (net, layer, width, undirected segment endpoints), count duplicate records; only generated thermal excluded. Does not rely on original empty guard subset.','checks':checks},indent=2),encoding='utf8')
print(json.dumps(checks,indent=2))
