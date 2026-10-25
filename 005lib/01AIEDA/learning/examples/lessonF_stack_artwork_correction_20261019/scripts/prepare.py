from pathlib import Path
import shutil,json,hashlib,re
A=Path(r'D:\001DIY\005lib\01AIEDA')
R=A/'learning/examples/lessonF_stack_artwork_correction_20261019'
for x in ['backups','current','source','scripts','logs','exports']:(R/x).mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
def calls(s):
 start=None;dep=0;quoted=False;escape=False;res=[]
 for i,ch in enumerate(s):
  if quoted:
   if escape:escape=False
   elif ch=='\\':escape=True
   elif ch=='"':quoted=False
   continue
  if ch=='"':quoted=True;continue
  if ch=='(':
   if dep==0:
    j=i
    while j>0 and (s[j-1].isalnum() or s[j-1]=='_'):j-=1
    start=j
   dep+=1
  elif ch==')':
   dep-=1
   if dep==0 and start is not None:
    v=s[start:i+1]
    assert v.startswith('axlFilmCreate('),v[:100]
    res.append(v);start=None
 assert dep==0 and not quoted
 return res
records=[]
for n in [2,4]:
 src=Path(r'D:\001DIY\005lib\01env')/f'drill{n}.txt'
 dst=R/'source'/src.name
 shutil.copy2(src,dst)
 s=dst.read_text(encoding='utf8');forms=calls(s)
 data=[]
 for v in forms:
  name=re.search(r'axlFilmCreate\(\s*"([^"]+)"',v)[1]
  layers=re.search(r"\?layers\s*'\(([\s\S]*?)\)",v)[1]
  data.append({'name':name,'rawCall':v,'layers':re.findall(r'"([^"]+)"',layers)})
 assert len(data)==(15 if n==2 else 17)
 (R/f'source/drill{n}_parsed.json').write_text(json.dumps({'source':str(src),'sha256':sha(src),'filmCount':len(data),'films':data},indent=2),encoding='utf8')
 # All source calls execute, retaining original spelling, ordering and every kwarg.
 instr=[]
 for x in data:
  instr.append('r='+x['rawCall']+'\nfprintf(f "FILM_RESULT\\t%L\\t%L\\n" "'+x['name']+'" r)')
 (R/f'scripts/full_template_{n}.il').write_text('\n'.join(instr)+'\n',encoding='ascii')
 records.append({'kind':'template','source':str(src),'backup':str(dst),'sha256':sha(src),'films':len(data)})
boards=[('F28_2L',A/'learning/examples/lesson28_stackup_20261019/native/F28_2L.brd','F28_2L_USERFIX.brd',2),('F28_4L',A/'learning/examples/lesson28_stackup_20261019/native/F28_4L.brd','F28_4L_USERFIX.brd',4),('F29',A/'learning/examples/lesson29_constraints_20261019/native/F29_CONSTRAINTS_v3.brd','F29_CONSTRAINTS_v4.brd',4)]
for key,p,name,n in boards:
 b=R/'backups'/(key+'_ORIGINAL.brd')
 assert not b.exists(),b
 shutil.copy2(p,b)
 q=R/'current'/name;assert not q.exists();shutil.copy2(p,q)
 assert sha(p)==sha(b)==sha(q)
 records.append({'kind':'board','key':key,'source':str(p),'backup':str(b),'working':str(q),'sha256':sha(p),'layerCount':n})
(R/'input_manifest.json').write_text(json.dumps(records,indent=2),encoding='utf8')
shutil.copy2(A/'learning/examples/lesson29_constraints_20261019/scripts/launch29_long.py',R/'scripts/launch_fix.py')
print(json.dumps({'records':records,'root':str(R)},indent=2))
