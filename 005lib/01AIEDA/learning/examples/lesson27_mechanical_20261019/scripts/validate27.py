import pathlib,csv,json,re,hashlib,math,sys,html
B=pathlib.Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lesson27_mechanical_20261019')
D=pathlib.Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/de_15_26_20261019')
checks=[]
def check(name,ok,actual=None):
 checks.append({'name':name,'pass':bool(ok),'actual':actual})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def readtab(p):return list(csv.DictReader(p.open(encoding='utf8'),delimiter='\t',quoting=csv.QUOTE_NONE))
def sx(s):
 ts=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',s);i=0
 def one():
  nonlocal i
  t=ts[i];i+=1
  if t=='(':
   a=[]
   while ts[i]!=')':a.append(one())
   i+=1;return a
  if t.startswith('"'):return json.loads(t)
  if t=='nil':return None
  if t=='t':return True
  try:return float(t)
  except ValueError:return t
 return one()
def table(p):return [{k:sx(v) for k,v in x.items()} for x in readtab(p)]
rb=B/'readback'
before=readtab(D/'native_flow_final/baseline_readback/components.tsv')
after=readtab(rb/'components.tsv')
check('80 logical components preserved',len(after)==80)
def cs(rows):return sorted(tuple(r[k] for k in ['refdes','package','deviceType','pins']) for r in rows)
check('logical component identity and footprint preserved',cs(before)==cs(after))
bp=readtab(D/'native_flow_final/baseline_readback/component_pins.tsv');ap=readtab(rb/'component_pins.tsv')
check('272 logical pins preserved',len(ap)==272)
def ps(rows):return sorted(tuple(r[k] for k in ['refdes','pin','net']) for r in rows)
check('all logical pin net assignments unchanged',ps(bp)==ps(ap))
check('69 net membership counts unchanged',sorted(readtab(rb/'nets.tsv'),key=lambda x:x['net'])==sorted(readtab(D/'native_flow_final/baseline_readback/nets.tsv'),key=lambda x:x['net']))
check('only J2 logical component placed',[r['refdes'] for r in after if r['placed']=='t']==['J2'])
sy=table(rb/'symbols.tsv');check('one J2 and four mechanical drill symbols',len(sy)==5)
j2=[s for s in sy if s['name']=='L10_GCT_USB4105_GF_A_12LAND'];check('J2 anchor orientation',len(j2)==1 and [j2[0][k] for k in ['x','y','rotation','mirrored','pins']]==[40,3.675,0,None,18])
mounts=[s for s in sy if s['name']=='L27_NPTH_D200_MECH']
centers=sorted((s['x'],s['y']) for s in mounts);expected=sorted([(5,5),(75,5),(75,55),(5,55)])
check('four mounting datums',centers==expected,centers)
g=table(rb/'mechanical_shapes.tsv')
by=lambda layer:[r for r in g if r['layer']==layer]
out=by('BOARD GEOMETRY/DESIGN_OUTLINE');check('one real design outline',len(out)==1)
v=[p[0] for p in out[0]['vertices']]
exp=[[2,0],[78,0],[80,2],[80,58],[78,60],[2,60],[0,58],[0,2]]
check('chamfered outline exact ordered vertices',v==exp,v)
area=abs(sum(v[i][0]*v[(i+1)%len(v)][1]-v[(i+1)%len(v)][0]*v[i][1] for i in range(len(v)))/2)
check('closed simple convex outline area 4792 mm2',area==4792,area)
check('recognized native outline and both keepins',all(re.search(k+'=dbid:',(rb/'mechanical_summary.txt').read_text()) for k in ['outline','keepinPlace','keepinRoute']))
check('route keepin inset bbox',by('ROUTE KEEPIN/ALL')[0]['box']==[[.5,.5],[79.5,59.5]])
pk=by('PACKAGE KEEPIN/ALL')[0]
check('package keepin edge exception explicitly defined',pk['box']==[[.5,-.5],[79.5,59.5]] and [34.5,-.5] in [a[0] for a in pk['vertices']])
for layer in ['ROUTE KEEPOUT/ALL','PACKAGE KEEPOUT/ALL']:
 rows=[r for r in by(layer) if abs(r['box'][1][0]-r['box'][0][0]-5)<1e-9]
 c=sorted(((r['box'][0][0]+r['box'][1][0])/2,(r['box'][0][1]+r['box'][1][1])/2) for r in rows)
 check(layer+' hardware 5mm keepouts',c==expected and all(r['filled'] for r in rows))
low=[r for r in by('PACKAGE KEEPOUT/TOP') if r['box']==[[10,42],[30,52]]]
check('effective height forbidden interval starts at 2mm',len(low)==1 and low[0]['props']==[['PACKAGE_HEIGHT_MIN','2 MM']])
for layer in ['PACKAGE KEEPOUT/TOP','PACKAGE KEEPOUT/BOTTOM']:
 check('mating effective zone '+layer,any(r['box']==[[34,-12],[46,-.5]] and r['filled'] for r in by(layer)))
bound=by('PACKAGE GEOMETRY/PLACE_BOUND_TOP')
check('only real J2 place bound, no fictitious mounting component body',len(bound)==1)
check('J2 height 3.46 and courtyard at edge',bound[0]['box']==[[34.88,-.325],[45.12,8.23]] and bound[0]['props']==[['PACKAGE_HEIGHT_MAX','3.46 MM']])
pins=table(rb/'physical_pins.tsv')
check('22 placed physical pins x 2 layers',len(pins)==44)
mp=[p for p in pins if p['symbol']=='L27_NPTH_D200_MECH']
check('mount drill definition no copper on both layers',len(mp)==8 and all(p['mechanical'] and p['plating']=='NON_PLATED' and p['diameter']==2 and p['regular']=='NULL' and p['bbox']==[[0,0],[0,0]] for p in mp))
jp=[p for p in pins if p['symbol']=='L10_GCT_USB4105_GF_A_12LAND' and p['layer']=='ETCH/TOP']
slots=[p for p in jp if str(p['pin']).startswith('SH')]
check('USB 4 mechanical shell slots aligned to board edge',sorted((p['x'],p['y']) for p in slots)==sorted([(35.68,2.6),(44.32,2.6),(35.68,6.78),(44.32,6.78)]))
check('USB slot drill dimensions',all(p['hole_type']=='oval slot' and p['drillx']==.6 and p['drilly']==(1.4 if p['y']==2.6 else 1.7) for p in slots))
loc=[p for p in jp if p['mechanical']]
check('USB two true NPTH locators',len(loc)==2 and sorted((p['x'],p['y'],p['diameter']) for p in loc)==[(37.11,6.28,.65),(42.89,6.28,.65)] and all(p['regular']=='NULL' for p in loc))
smd=[p for p in jp if p['diameter']==0]
check('USB 12 lands at edge+7.355mm',len(smd)==12 and all(p['y']==7.355 for p in smd))
native=(B/'logs/create06/create.txt').read_text()
for n,count in [('BASE',0),('ROUTE',2),('HEIGHT',1),('PLACE',2),('FINAL',0)]:
 check(n+' controlled DRC count',f'{n} count={count} state=t' in native)
check('height check actual 3.46 > min2',all(t in native for t in ['source "PACKAGE_HEIGHT_MIN"','expected "2 MM" actual "3.46 MM"']))
check('route keepout named rule detected','name "Line to Route Keepout Spacing"' in native)
check('hole-to-line rule also detected','name "Mechanical Drill Hole to Line Spacing"' in native)
check('package keepin and keepout rules detected',all(t in native for t in ['name "Package to Place Keepin Spacing"','name "Package to Place Keepout Spacing"']))
check('native completion markers',all(t in (B/p).read_text() for p,t in [('logs/package03/package.txt','L27_PACKAGE COMPLETE'),('logs/create06/create.txt','L27_CREATE COMPLETE'),('readback/mechanical_summary.txt','L27_READ COMPLETE'),('readback/keepin_challenge.txt','L27_MORE COMPLETE')]))
for tag in ['create06','read01','read02']:
 rec=json.loads((B/'logs'/tag/'launch.json').read_text())
 check(tag+' actual process exit zero',rec['completed'] and rec['exitCode']==0)
 check(tag+' input hash unchanged',rec['inputBeforeSHA256']==rec['inputAfterSHA256'])
check('saved board matches readonly evidence',sha(B/'F27_MECHANICAL.brd')==json.loads((B/'logs/read01/launch.json').read_text())['inputBeforeSHA256'])
check('persisted drc0/t','drcState=t\ndrcs=0' in (rb/'mechanical_summary.txt').read_text())
if (rb/'all_texts.tsv').exists():
 texts=table(rb/'all_texts.tsv')
 target=[r for r in texts if r['layer'] in ['REF DES/SILKSCREEN_TOP','REF DES/ASSEMBLY_TOP','COMPONENT VALUE/ASSEMBLY_TOP']]
 check('J2 three package text anchors',len(target)==3 and all((r['x'],r['y'])==(40,3.675) for r in target))
 k=(rb/'keepin_challenge.txt').read_text()
 check('route keepin crossing rejected then rollback zero','name "Line to Route Keepin Spacing"' in k and 'AFTER count=0 state=t' in k)
else:check('extra readonly text and route keepin challenge pending',False)
sources=[D/'native_flow_final/DE_BASELINE.brd',B/'source/DE_BASELINE.brd',B/'library/eda_l07c_npth_200_null.pad',pathlib.Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lesson10_connector_20261018/source/usb4105.pdf')]
sources+=sorted(p for p in (D/'library').iterdir() if p.suffix.lower() in ['.psm','.pad','.dra'])
(B/'source/dependency_manifest.json').write_text(json.dumps([{'path':str(p),'SHA256':sha(p)} for p in sources],indent=2),encoding='utf8')
result={'status':'PASS' if all(c['pass'] for c in checks) else 'PENDING_OR_FAIL','course':27,'board':str(B/'F27_MECHANICAL.brd'),'boardSHA256':sha(B/'F27_MECHANICAL.brd'),'checks':checks,'limitations':['Educational mechanical dimensions; not enclosure/manufacturing release.','79 logical components remain unplaced; no routing or board-level SI/PI/EMI acceptance.','2mm mounting holes and 5mm hardware clearance are engineering exercise assumptions.','Connector board thickness and slot fabrication process await lesson28 and assembly confirmation.']}
(B/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(result['status'],len(checks),'checks')
for c in checks:
 if not c['pass']:print('FAIL',c)
# Native readback preview, not a Cadence screenshot.
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1200" viewBox="-10 -80 100 100">','<rect x="-10" y="-80" width="100" height="100" fill="#111b27"/>']
parts.append('<g transform="scale(1,-1)">')
def poly(points,fill,stroke,dash=''):
 pts=' '.join(f'{x},{y}' for x,y in points)
 parts.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width=".14" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>')
poly(v,'#214a3f','#e2f3ec')
poly([a[0] for a in by('ROUTE KEEPIN/ALL')[0]['vertices']],'none','#48c8f5','.7 .4')
poly([a[0] for a in pk['vertices']],'none','#c2a4ff','.4 .4')
for x,y in centers:
 parts.append(f'<circle cx="{x}" cy="{y}" r="2.5" fill="#e5a238" fill-opacity=".24" stroke="#e5a238" stroke-width=".1"/>')
 parts.append(f'<circle cx="{x}" cy="{y}" r="1" fill="#111b27" stroke="#eee" stroke-width=".12"/>')
for row in low:poly([a[0] for a in row['vertices']],'#8d35584d','#ed80ad','.5 .3')
for row in by('PACKAGE KEEPOUT/TOP'):
 if row['box']==[[34,-12],[46,-.5]]:poly([a[0] for a in row['vertices']],'#8d35584d','#ed80ad')
poly([a[0] for a in bound[0]['vertices']],'none','#c2a4ff')
for p in jp:
 x,y=p['x'],p['y']
 if p['regular']=='NULL':parts.append(f'<circle cx="{x}" cy="{y}" r="{p["diameter"]/2}" fill="#111b27" stroke="#ccc" stroke-width=".07"/>')
 else:
  box=p['bbox'];x1,y1=box[0];x2,y2=box[1]
  parts.append(f'<rect x="{x+x1}" y="{y+y1}" width="{x2-x1}" height="{y2-y1}" rx=".12" fill="#f5ce67"/>')
  if p['diameter']>0:parts.append(f'<rect x="{x-p["drillx"]/2}" y="{y-p["drilly"]/2}" width="{p["drillx"]}" height="{p["drilly"]}" rx=".3" fill="#111b27"/>')
parts.append('<path d="M40,-11 L40,-2 M38.8,-3.8 L40,-2 L41.2,-3.8" fill="none" stroke="#79e1f2" stroke-width=".3"/>')
parts.append('<path d="M-2,0 L2,0 M0,-2 L0,2" fill="none" stroke="#fff" stroke-width=".12"/>')
parts.append('</g>')
def text(x,y,t,size=1.3,color='#dfe8f2'):parts.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="{color}">{html.escape(t)}</text>')
text(0,-76,'LESSON 27 | Native mechanical readback',2.4)
text(0,-72,'80 x 60 mm / C2 corners / 4 x NPTH D2 / TOP view',1.6)
text(0,-68,'Datums +X right, +Y up, +Z TOP; all dimensions mm',1.3)
text(12,-47,'TOP: height <= 2 mm',1.3)
text(28,15,'USB insertion +Y; opening -Y',1.4)
text(0,19,'Native data preview (not a GUI screenshot) | BRD SHA '+sha(B/'F27_MECHANICAL.brd')[:16],1.0)
text(6,-56,'H4',1.3);text(71,-56,'H3',1.3);text(6,-6,'H1',1.3);text(71,-6,'H2',1.3)
text(1,-30,'60',1.5);text(36,-61,'80',1.5)
text(48,4,'J2 courtyard edge exception',1.1,'#c2a4ff')
text(0,-64,'Gold: real copper | orange: hardware keepout | blue: route keepin | purple: package keepin',1.1)
parts.append('</svg>')
svg='\n'.join(parts);(B/'preview.svg').write_text(svg,encoding='utf8')
sys.path.insert(0,r'D:/001DIY/005lib/01AIEDA/learning/tools/pymupdf_1_28_2')
import fitz
doc=fitz.open(stream=svg.encode(),filetype='svg');doc[0].get_pixmap(matrix=fitz.Matrix(1,1)).save(B/'preview.png')
