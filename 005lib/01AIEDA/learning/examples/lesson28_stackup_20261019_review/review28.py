import pathlib,json,csv,re,hashlib,math
R=pathlib.Path(r'D:/001DIY/005lib/01AIEDA')
B=R/'learning/examples/lesson28_stackup_20261019'
O=R/'learning/examples/lesson28_stackup_20261019_review';O.mkdir(parents=True,exist_ok=True)
P=R/'learning/examples/lesson27_mechanical_20261019'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def rows(p):return list(csv.DictReader(p.open(encoding='utf8'),delimiter='\t',quoting=csv.QUOTE_NONE))
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
 return one() if ts else None
def table(p):return [{k:sx(v) for k,v in x.items()} for x in rows(p)]
def props(v):return dict(zip(v[::2],v[1::2]))
cs=[]
def ck(n,b,d=None):cs.append({'check':n,'pass':bool(b),'detail':d})
def norm(v):return sorted(json.dumps(x,sort_keys=True) for x in v)
def near(a,b):return abs(float(a)-b)<1e-8
reviewed=[]
spec=json.loads((B/'specification.json').read_text())
sourcepins=rows(P/'readback/component_pins.tsv')
logical=sorted((p['refdes'],p['pin'],p['net']) for p in sourcepins)
expected2=[('MASK','SOLDERMASK_TOP',.0152),('CONDUCTOR','TOP',.0356),('DIELECTRIC',None,1.524),('CONDUCTOR','BOTTOM',.0356),('MASK','SOLDERMASK_BOTTOM',.0152)]
expected4=[('MASK','SOLDERMASK_TOP',.01524),('CONDUCTOR','TOP',.035),('DIELECTRIC',None,.2104),('CONDUCTOR','L2',.0152),('DIELECTRIC',None,1.065),('CONDUCTOR','L3',.0152),('DIELECTRIC',None,.2104),('CONDUCTOR','BOTTOM',.035),('MASK','SOLDERMASK_BOTTOM',.01524)]
refComps=rows(P/'readback/components.tsv')
refC=sorted((c['refdes'],c['package'],c['deviceType'],int(c['pins'])) for c in refComps)
refPhy=[p for p in table(P/'readback/physical_pins.tsv') if p['layer']=='ETCH/TOP']
def pinKey(p):return (p['symbol'],p['pin'],p['x'],p['y'],p['padstack'],p['mechanical'],p['plating'],p['diameter'],p['drillx'],p['drilly'])
refPhy=sorted((pinKey(p) for p in refPhy),key=str)
filmSource=json.loads((B/'film_template_readonly.json').read_text())
baseGeom=rows(B/'logs/baseline01/geometry.tsv')
for n,expected in [(2,expected2),(4,expected4)]:
 d=B/'logs'/f'reopen{n}_02';m=B/'logs'/f'more{n}_01';brd=B/'native'/f'F28_{n}L.brd'
 rec=json.loads((d/'launch.json').read_text())
 ck(f'{n}L actual BRD hash matches readonly',sha(brd)==rec['afterSHA256']==rec['beforeSHA256'],sha(brd))
 ck(f'{n}L readonly exited and completed',rec['completed'] and rec['exitCode']==0 and 'L28_READ COMPLETE' in (d/'readback.txt').read_text())
 ck(f'{n}L current DRC evidence', 'drc_count=0 drc_state=t' in (d/'readback.txt').read_text())
 x=[r for r in table(d/'cross_section.tsv') if r['material']!='AIR']
 ck(f'{n}L exact native stack names/types/count',[(a['type'],a['name']) for a in x]==[(a,b) for a,b,c in expected])
 ck(f'{n}L every native thickness source match',all(near(a['thickness'],c) for a,(t,k,c) in zip(x,expected)))
 copper=[a for a in x if a['type']=='CONDUCTOR'];dielec=[a for a in x if a['type']=='DIELECTRIC'];mask=[a for a in x if a['type']=='MASK']
 ck(f'{n}L fixed conductor order',[a['name'] for a in copper]==(['TOP','BOTTOM'] if n==2 else ['TOP','L2','L3','BOTTOM']))
 ck(f'{n}L all positive copper',all(a['negative'] is None for a in copper))
 total=sum(a['thickness'] for a in x);nomask=sum(a['thickness'] for a in x if a['type']!='MASK')
 ck(f'{n}L independent mask-inclusive sum',near(total,1.6256 if n==2 else 1.61668),total)
 ck(f'{n}L independent copper+dielectric sum',near(nomask,1.5952 if n==2 else 1.5862),nomask)
 ck(f'{n}L nominal1.6 kept distinct',spec['targets'][str(n)]['nominalBoardThickness_mm']==1.6 and not near(total,1.6))
 ck(f'{n}L sourced Dk scalar values',[float(a['dk']) for a in dielec]==([4.5] if n==2 else [4.4,4.6,4.4]))
 ck(f'{n}L inherited Df default present',all(float(a['loss'])==.035 for a in dielec+mask))
 ck(f'{n}L default Df explicitly unqualified',any('loss tangent 0.035' in s for s in spec['qualificationWarnings']))
 ck(f'{n}L copper irrelevant Dk explicitly unqualified',any('Conductors have irrelevant' in s for s in spec['qualificationWarnings']))
 if n==2:
  ck('2L purple maskDk4.3 unqualified',all(float(a['dk'])==4.3 for a in mask) and any('2L mask Dk 4.3' in s for s in spec['qualificationWarnings']))
  ck('2L sourced core tolerance .1524',dielec[0]['tolPlus']==dielec[0]['tolMinus']==.1524)
 else:
  ck('4L sourced effective C2 maskDk3.8',all(float(a['dk'])==3.8 and a['thickness']==.01524 for a in mask))
 c=table(d/'components.tsv')
 ck(f'{n}L all80 logical component identities preserved',sorted((a['refdes'],a['package'],a['device_type'],int(a['pins'])) for a in c)==refC)
 pads=table(d/'pads.tsv')
 logicalNow=sorted((a['refdes'],a['number'],a['net'] or '') for a in pads if a['refdes']!='VIA_TEST' and a['layer']=='ETCH/TOP')
 ck(f'{n}L all272 logical pin-net assignments preserved',logicalNow==logical,{'count':len(logicalNow)})
 nets=table(d/'nets.tsv')
 ck(f'{n}L all69 net names preserved',sorted(a['net'] for a in nets)==sorted(a['net'] for a in table(B/'logs/baseline01/nets.tsv')))
 phy=table(m/'placed_pins.tsv')
 ck(f'{n}L all22 physical pins actually enumerated',len(phy)==22)
 now=[]
 for p in phy:now.append((p['symbol'],p['pin'],p['xy'][0],p['xy'][1],p['padstack'],p['mechanical'],p['plating'],p['drill'],p['drillX'],p['drillY']))
 ck(f'{n}L physical holes and connector coordinate identities preserved',sorted(now,key=str)==refPhy)
 bsm=[a for a in phy if a['type']=='MECHANICAL']
 ck(f'{n}L mechanical BSM4 pins not omitted',len(bsm)==4 and all(a['refdes'] is None and a['mechanical'] for a in bsm))
 pp=table(m/'placed_pads.tsv')
 npth=[a for a in pp if 'NPTH' in a['padstack']]
 ck(f'{n}L all6 NPTH every conductor NULL',len(npth)==6*n and all(a['figure']=='NULL' and a['bbox']==[[0,0],[0,0]] for a in npth),len(npth))
 ck(f'{n}L no SMD copper incorrectly copied internal/bottom',all(a['figure']=='NULL' for a in pp if 'SMD' in a['padstack'] and a['layer']!='ETCH/TOP'))
 geom=table(d/'geometry.tsv')
 ck(f'{n}L all59 mechanical geometry records unchanged',norm(rows(d/'geometry.tsv'))==norm(baseGeom),len(geom))
 md=B/'logs'/f'mech{n}_01'
 direct=table(md/'mechanical_direct.tsv')
 outline=[a for a in direct if a['layer']=='BOARD GEOMETRY/DESIGN_OUTLINE']
 expectedVertices=[[2,0],[78,0],[80,2],[80,58],[78,60],[2,60],[0,58],[0,2]]
 ck(f'{n}L real outline persists',len(outline)==1 and outline[0]['bbox']==[[0,0],[80,60]] and [a[0] for a in outline[0]['vertices']]==expectedVertices)
 roots=(md/'mechanical_roots.txt').read_text()
 ck(f'{n}L actual root outline and keepins recognized',all(t in roots for t in ['designOutline=t','keepinPlace=t','keepinRoute=t','L28_MECHANICAL_DIRECT COMPLETE']))
 ck(f'{n}L all explicit mechanical shapes match source',norm(rows(md/'mechanical_direct.tsv'))==norm(rows(B/'logs/mechbase01/mechanical_direct.tsv')))
 mr=json.loads((md/'launch.json').read_text())
 ck(f'{n}L explicit mechanical read process/hash stable',mr['completed'] and mr['exitCode']==0 and mr['readonlyHashUnchanged'] and sha(brd)==mr['afterSHA256'])
 reviewed += [md/'mechanical_direct.tsv',md/'mechanical_roots.txt',md/'launch.json']
 low=[a for a in geom if a['layer']=='PACKAGE KEEPOUT/TOP' and a['bbox']==[[10,42],[30,52]]]
 ck(f'{n}L forbidden height interval2..infinity persists',len(low)==1 and low[0]['properties']==[['PACKAGE_HEIGHT_MIN','2 MM']])
 bound=[a for a in geom if a['layer']=='PACKAGE GEOMETRY/PLACE_BOUND_TOP']
 ck(f'{n}L J2 finite maximum3.46 persists',len(bound)==1 and bound[0]['properties']==[['PACKAGE_HEIGHT_MAX','3.46 MM']])
 ck(f'{n}L no physical GND plane falsely created',not any(a['type']=='shape' and a['layer'].startswith('ETCH/') for a in geom))
 via=table(d/'vias.tsv');unique={json.dumps(a,sort_keys=True) for a in via}
 ck(f'{n}L exactly1 real via despite extractor aliases',len(unique)==1,{'rawRows':len(via),'unique':len(unique)})
 v=json.loads(next(iter(unique)))
 ck(f'{n}L through GND via coordinates/hole',v['xy']==[52,35] and v['net']=='GND' and v['plating']=='PLATED' and v['diameter']==.3 and v['usage']=='Through_via')
 films=table(d/'films.tsv')
 for name in (['TOP','BOTTOM'] if n==2 else ['TOP','L2','L3','BOTTOM']):
  f=next(a for a in films if a['name']==name);fp=props(f['properties']);orig=next(a for a in filmSource[str(n)]['films'] if a['name']==name)
  ck(f'{n}L {name} film full exact layer list',fp['groupMembers']==orig['layers'])
  ck(f'{n}L {name} preserved sequence unrelated to stack',fp['sequence']==orig['sequence'])
  ck(f'{n}L {name} suppress flags explicit false',fp['suppressUnconnectPads'] is None and fp['suppressShapeFill'] is None)
 outfilm=next(a for a in films if a['name']=='F28_DESIGN_OUTLINE')
 ck(f'{n}L actual outline independently exposed to manufacturing',props(outfilm['properties'])['groupMembers']==['BOARD GEOMETRY/DESIGN_OUTLINE'])
 ck(f'{n}L 01env script unchanged',sha(pathlib.Path(filmSource[str(n)]['path']))==filmSource[str(n)]['sha256'])
 reviewed += [brd]+list(d.glob('*.tsv'))+[d/'readback.txt',d/'launch.json']+list(m.glob('*.tsv'))+[m/'launch.json']
ck('L2 L3 GND only declared intent',not spec['physicalCopperPoursGenerated'] and all('not yet poured' in spec['plannedFunctions4L'][s] for s in ['L2','L3']))
for src in spec['sources']:
 fp=B/src['file']
 ck('Archived primary source SHA '+fp.name,sha(fp)==src['SHA256'])
 reviewed.append(fp)
gct=B/'source/GCT_USB4105_RevB4_inherited.pdf'
ck('Inherited official GCT drawing SHA preserved',sha(gct)=='FB331FBABEE8392ED2937ED757C1610CB0F174B84625147C0B580A18EEA8C0E5')
reviewed.append(gct)
webInputs=[{'url':'https://gct.co/connector/usb4105','reviewDate':'2026-10-19','role':'Shell Stake Length options; drawing dimension datum independently inspected'}, {'url':'https://docs.oshpark.com/services/two-layer/','reviewDate':'2026-10-19','role':'current official 2L construction, service minimum mask web'}, {'url':'https://jlcpcb.com/impedance','reviewDate':'2026-10-19','role':'current official 4L JLC04161H-7628 dimensions and scalar Dk/mask C2'}, {'url':'https://jlcpcb.com/capabilities/pcb-capabilities','reviewDate':'2026-10-19','role':'current official manufacturing tolerance/capability scope'}]
reviewed += [B/'specification.json',B/'validation.json',B/'film_template_readonly.json',P/'F27_MECHANICAL.brd']
report={'status':'PASS_NATIVE_SCOPE_WITH_FABRICATION_OPEN_ITEMS' if all(c['pass'] for c in cs) else 'FAIL','independentChecks':len(cs),'checks':cs,'sourcesVerifiedOnline':webInputs,'findings':[{'id':'R28-01','severity':'fabrication open item','issue':'Inherited USB nominal soldermask web0.100mm < OSH Park published minimum0.1016mm by0.0016mm. Need revised mask/approved process or other service before manufacturing; does not invalidate teaching stackup CAD.'},{'id':'R28-02','severity':'provenance clarification','issue':'Native per-layer tolPlus/Minus=0 in JLC model means no entered per-layer tolerance, not guaranteed zero manufacturing variation.'},{'id':'R28-03','severity':'already declared limitation','issue':'Df.035 default, 2L mask Dk4.3 default, scalar Dk frequency limits, effective uniform C2 mask and no actual reference-plane copper are explicitly unqualified, not fabrication/RF acceptance.'}], 'closedEvidenceGap':'Legacy fgeo map omits DESIGN_OUTLINE; explicit mechbase01/mech2_01/mech4_01 now prove actual outline/keepins and unchanged shapes.', 'stakeLengthErratum':'S=.95+/-.15mm measured from connector mounting/SMT datum, not finished board bottom. 1.6mm board assembly compatibility remains unqualified.', 'reviewedFiles':[{'path':str(p),'SHA256':sha(p)} for p in reviewed]}
report['findings'].extend([
 {'id':'R28-04','severity':'closed evidence gap','issue':'Legacy fgeo geometry omitted DESIGN_OUTLINE. Three explicit readonly mechanical-direct exports now prove source/2L/4L outline and keepin/out identical with unchanged board hashes.'},
 {'id':'R28-05','severity':'assembly open item and corrected documentation','issue':'GCT S0.95+/-0.15mm is Shell Stake Length from connector mounting/SMT datum, not bottom-of-finished-board protrusion. Nominal1.6mm board compatibility with selected GF-A stake and soldering process remains unqualified; lesson27 note corrected with before-copy retained.'}
])
(O/'review.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(report['status'],len(cs),'checks',sum(not a['pass'] for a in cs),'failed')
for c in cs:
 if not c['pass']:print('FAILED',c)
