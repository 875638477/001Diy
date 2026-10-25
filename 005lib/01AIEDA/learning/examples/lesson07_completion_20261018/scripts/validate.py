from pathlib import Path
import re,json,math,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson07_completion_20261018')
def sx(s):
 t=re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+',s); i=0
 def take():
  nonlocal i
  v=t[i];i+=1
  if v=='(':
   a=[]
   while t[i]!=')': a.append(take())
   i+=1;return a
  if v.startswith('"'):return json.loads(v)
  if v=='nil':return None
  if v=='t':return True
  try:return float(v)
  except ValueError:return v
 return take()
def read(stage):
 text=(R/f'logs/{stage}/readback.txt').read_text()
 rows={}
 for line in text.splitlines():
  if '\t' in line:
   k,*cells=line.split('\t');rows.setdefault(k,[]).append([sx(v) for v in cells])
 return text,rows
checks=[]
def check(name,test,actual=None):checks.append({'name':name,'pass':bool(test),'actual':actual})
for stage,marker in [('create_flash02','L7C_FLASH COMPLETE'),('create_package07','L7C_PACKAGE COMPLETE'),('create_board03','L7C_BOARD COMPLETE'),('reopen_flash','L7C_READ COMPLETE'),('reopen_package02','L7C_READ COMPLETE'),('reopen_board02','L7C_READ COMPLETE')]:
 rec=json.loads((R/f'logs/{stage}/launch.json').read_text());log=(R/f'logs/{stage}/stdout.txt').read_text(errors='replace')
 out=R/f'logs/{stage}'/('readback.txt' if stage.startswith('reopen') else 'create.txt')
 check(stage+' process exit',rec['completed'] and rec['exitCode']==0,rec['exitCode'])
 check(stage+' semantic completion',marker in out.read_text() and 'E- *Error*' not in log)
 if stage.startswith('reopen'):check(stage+' immutable input',rec['readonlyHashUnchanged'])
package,p=read('reopen_package02');board,b=read('reopen_board02');flash,f=read('reopen_flash')
for label,rows in [('package',p),('board',b)]:
 check(label+' exactly three holes',len(rows['PIN'])==3)
 holes=[x for x in rows['PIN'] if 'npth' in x[0].lower()];check(label+' pure NPTH count',len(holes)==1)
 if holes:
  q=holes[0];check(label+' NPTH no plating',q[6]=='NON_PLATED',q);check(label+' NPTH diameter',abs(q[7]-2)<.00001,q[7]);check(label+' NPTH mechanical',q[4] is True)
  for layer in (['ETCH/TOP','ETCH/BOTTOM'] if label=='package' else ['ETCH/TOP','ETCH/L2','ETCH/L3','ETCH/BOTTOM']):
   pads=[x for x in rows['PAD'] if x[0]==q[0] and x[1]==layer and x[2]=='REGULAR']
   check(label+' NULL regular '+layer,len(pads)==1 and pads[0][3] in [None,'NULL'],pads)
 layers=[x[0] for x in rows['STACK'] if x[1]=='CONDUCTOR']
 if label=='board':
  check('board copper order',layers==['TOP','L2','L3','BOTTOM'],layers)
  negative=[x[0] for x in rows['STACK'] if x[2] is True];check('L3 negative',negative==['L3'],negative)
for layer in ['REF DES/SILKSCREEN_TOP','REF DES/ASSEMBLY_TOP','COMPONENT VALUE/ASSEMBLY_TOP']:
 t=[x for x in p.get('TEXT',[]) if x[0]==layer]
 check('package text '+layer,len(t)==1 and t[0][2]==[0,0],t)
check('package height','PACKAGE_HEIGHT_MAX "1 MM"' in package,p.get('HEIGHT'))
# Independent expected clearance-sector area: quarter-annulus minus the two half-spoke corridors.
h=.15;ri=.8;ro=1.0
def cap(r):return r*r*(math.pi/4-math.asin(h/r))-h*math.sqrt(r*r-h*h)+h*h
expected=cap(ro)-cap(ri)
flashpolys=[x for x in f.get('COPPER_POLY',[]) if x[0]=='ETCH/TOP' and abs(x[2]-expected)<.002]
check('native flash four clearance sectors',len(flashpolys)==4,len(flashpolys))
for i,x in enumerate(flashpolys):check('flash sector analytic area '+str(i),abs(x[2]-expected)<.002,{'actual':x[2],'expected':expected})
for layer in ['ETCH/TOP','ETCH/L2','ETCH/L3','ETCH/BOTTOM']:
 rows=[x for x in b.get('NPTH_CLEAR_PROBE',[]) if x[0]==layer]
 check('no copper within radius 1.49 '+layer,len(rows)==1 and abs(rows[0][1])<1e-8,rows)
 polys=[x for x in b.get('COPPER_POLY',[]) if x[0]==layer]
 area=sum(x[2] for x in polys)
 check('copper exists outside clearance '+layer,area>150,area)
 voids=[]
 for x in b.get('VOID',[]):
  if x[0]==layer:
   lo,hi=x[1]
   if lo[0]<20<hi[0] and lo[1]<20<hi[1]:voids.append(x)
 check('actual NPTH void '+layer,any(x[1][0][0]<=18.5 and x[1][0][1]<=18.5 and x[1][1][0]>=21.5 and x[1][1][1]>=21.5 for x in voids),voids)
check('board DRC recalculated','drc_state=t' in board,board.splitlines()[0])
check('board stored DRC zero','stored_drcs=0' in board,board.splitlines()[0])
import_log=(R/'library/eda_l07c_npth_200_null.log').read_text(errors='replace')
check('NPTH expected purpose warning retained','No default internal pads are defined' in import_log,import_log)

# Additional independently checked final-v2 data. Do not count JSON success flags alone.
centers=[x for x in f.get('COPPER_POLY',[]) if x[0]=='ETCH/TOP' and abs(x[2]-math.pi*.4**2)<1e-6]
check('flash exactly five shapes including drilled center',len(f.get('COPPER_POLY',[]))==5 and len(centers)==1)
check('center dot diameter matches drilled hole',centers[0][1]==[[-.4,-.4],[.4,.4]] if centers else False)
for label,rows,origin in [('package',p,[0,0]),('board',b,[20,20])]:
 for number,rel,angle in [('1',[-5,0],0),('2',[5,0],90)]:
  matches=[x for x in rows['PIN'] if x[1]==number]
  check(label+' electrical pin '+number+' geometry',len(matches)==1 and matches[0][2]==[origin[0]+rel[0],origin[1]+rel[1]] and matches[0][3]==angle and matches[0][6]=='PLATED' and abs(matches[0][7]-.8)<1e-9,matches)
 for pad in rows['PAD']:
  if 'pth_' in pad[0].lower() and 'npth' not in pad[0].lower():
   if pad[2]=='REGULAR':check(label+' regular diameter '+pad[1],pad[3]=='CIRCLE' and pad[4]==[[-.8,-.8],[.8,.8]],pad)
   if pad[2]=='ANTI':check(label+' anti diameter '+pad[1],pad[3]=='CIRCLE' and pad[4]==[[-1,-1],[1,1]],pad)
   if pad[2]=='THERMAL':check(label+' native FSM mapping '+pad[1],pad[3]=='FLASH' and str(pad[5]).casefold()=='eda_l07c_th4_200_160_w30_d80',pad)
  if 'npth' in pad[0].lower():check(label+' no fabricated NPTH copper '+pad[1]+' '+pad[2],pad[3] in [None,'NULL'] and (pad[4] is None or pad[4]==[[0,0],[0,0]]),pad)
 check(label+' mechanical usage',any(x[0]=='' and x[1]=='Mechanical_hole' and x[2] is None for x in rows.get('PIN_NET',[])))
 checksKO=[x for x in rows.get('SHAPE',[]) if x[0]=='ROUTE KEEPOUT/ALL']
 expectedBox=[[origin[0]-1.5,origin[1]-1.5],[origin[0]+1.5,origin[1]+1.5]]
 check(label+' independent route keepout persisted',len(checksKO)==1 and checksKO[0][1]==expectedBox,checksKO)
for layer in ['ETCH/TOP','ETCH/L2','ETCH/L3','ETCH/BOTTOM']:
 actual=[x for x in b.get('SHAPE',[]) if x[0]==layer]
 check('actual copper GND membership '+layer,len(actual)==1 and actual[0][5]=='GND',actual)
for layer in ['BOUNDARY/TOP','BOUNDARY/L2','BOUNDARY/BOTTOM']:
 actual=[x for x in b.get('BOUNDARY_NET',[]) if x[0]==layer]
 check('explicit boundary GND membership '+layer,len(actual)==1 and actual[0][2]=='GND',actual)
for layer in ['ETCH/TOP','ETCH/L2','ETCH/BOTTOM']:
 paths=[x for x in b.get('THERMAL_CLINE',[]) if x[0]=='1' and x[1]==layer]
 check('four actual GND thermal spokes '+layer,len(paths)==4,paths)
 for i,path in enumerate(paths):
  rr=[math.dist(p,[15,20]) for p in path[3]]
  check('thermal reaches actual copper '+layer+' '+str(i),min(rr)<.8 and max(rr)>.929 and path[2]==.127 and path[4]=='GND',path)
 polys=[x for x in b.get('THERMAL_COPPER_POLY',[]) if x[0]=='1' and x[1]==layer]
 check('actual thermal copper polygons '+layer,len(polys)==4 and all(x[3]>0 for x in polys),polys)
check('OTHER pin has no GND thermal',not any(x[0]=='2' for x in b.get('THERMAL_CLINE',[])))
check('pin nets independently read',sorted((x[0],x[2]) for x in b['PIN_NET'] if x[0])==[('1','GND'),('2','OTHER')],b['PIN_NET'])
challenge=(R/'logs/create_board03/create.txt').read_text()
check('controlled route keepout challenge detected','controlled_intrusion_drc=2' in challenge and 'Line to Route Keepout Spacing' in challenge)
check('controlled mechanical hole challenge detected','Mechanical Drill Hole to Line Spacing' in challenge)
check('rollback followed by full DRC','drc_update=0 state=t' in challenge)

result={'status':'PASS_CAD_LESSON07_COMPLETION' if all(c['pass'] for c in checks) else 'FAIL_CAD_LESSON07_COMPLETION','finalBoard':str(R/'library/eda_l07c_clearance_4layer_v2.brd'),'finalSpec':str(R/'spec_v2.json'),'finalReadback':str(R/'logs/reopen_board02/readback.txt'),'date':'2026-10-18','allChecksPass':all(c['pass'] for c in checks),'checks':checks,'failures':[c for c in checks if not c['pass']],'flashSectorAnalyticalArea':expected,'scope':'Native CAD pad/hole/layer/flash/actual copper clearance lesson. Not production fabrication qualification.'}
(R/'validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
manifest=[]
for path in sorted(R.rglob('*')):
 if path.is_file() and path.name not in ['artifact_manifest.json']:
  manifest.append({'path':str(path),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest().upper()})
note=R.parent.parent/'notes/lesson07_completion_20261018.md'
assert note.is_file()
manifest.append({'path':str(note),'bytes':note.stat().st_size,'sha256':hashlib.sha256(note.read_bytes()).hexdigest().upper()})
(R/'artifact_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'checks':len(checks),'allChecksPass':result['allChecksPass'],'failures':result['failures']},indent=2))
assert result['allChecksPass']
