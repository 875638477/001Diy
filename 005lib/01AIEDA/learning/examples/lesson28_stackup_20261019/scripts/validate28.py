from pathlib import Path
import csv,json,hashlib,math,re,collections,html,sys
B=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def rows(p):
 return [dict(zip(a[0],r)) for a in [list(csv.reader(p.open(encoding='utf-8'),delimiter='\t',quoting=csv.QUOTE_NONE))] for r in a[1:]]
def q(s):return s[1:-1] if s.startswith('"') and s.endswith('"') else s
checks=[]
def ck(name,ok,detail=None):checks.append({'check':name,'pass':bool(ok),'detail':detail});assert ok,name+': '+str(detail)
def eq(name,a,b):ck(name,a==b,{'actual':a,'expected':b})
def near(name,a,b,tol=1e-8):ck(name,abs(float(a)-b)<=tol,{'actual':float(a),'expected':b,'tolerance':tol})
def norm(table):return sorted(json.dumps(r,sort_keys=True) for r in table)
base=B/'logs'/'baseline01';baseMore=B/'logs'/'morebase01'
sourcePath=Path(json.loads((B/'source'/'input_manifest.json').read_text())['source'])
eq('Original mechanical source unchanged',sha(sourcePath),'B6C84686472475F452F13F30EB7E3F99D8B9441CF0AB44B3D33917D615E5B55A')
filmSources=json.loads((B/'film_template_readonly.json').read_text())
spec={'date':'2026-10-19 Asia/Shanghai','cadence':'17.2 S045 SPB64','targets':{},'plannedFunctions4L':{'TOP':'Signal + local power; reference L2 GND','L2':'Continuous GND, not yet poured','L3':'Continuous GND, not yet poured','BOTTOM':'Signal + local power; reference L3 GND'},'physicalCopperPoursGenerated':False,'via':{'finishedHole_mm':0.3,'copperDiameter_mm':0.6,'nominalRadialRing_mm':0.15,'usage':'Through_via','xy_mm':[52,35],'net':'GND','purpose':'Teaching layer-mapping instance; no layout approval','structure':'Mechanical through hole, no blind/buried/microvia','soldermask':'No explicit aperture in PXML; tented-by-omission data, filling not guaranteed'},'qualificationWarnings':['Unknown material names inherit dielectric/loss software defaults. Only explicitly sourced Dk values are qualified as published scalar inputs, not RF guaranteed values.','All displayed loss tangent 0.035 values are inherited software defaults, not a factory-confirmed Df.','2L mask Dk 4.3 is an inherited software default, not purple soldermask source data.','Conductors have irrelevant inherited Dk 4.5, not copper permittivity for signal analysis.','No impedance solver or SI/PI simulation performed.','90-ohm USB target does not establish any width/spacing until actual impedance geometry is confirmed.']}
expected={
2:[('SOLDERMASK_TOP','MASK',0.0152,None),('TOP','CONDUCTOR',0.0356,None),(None,'DIELECTRIC',1.524,4.5),('BOTTOM','CONDUCTOR',0.0356,None),('SOLDERMASK_BOTTOM','MASK',0.0152,None)],
4:[('SOLDERMASK_TOP','MASK',0.01524,3.8),('TOP','CONDUCTOR',0.035,None),(None,'DIELECTRIC',0.2104,4.4),('L2','CONDUCTOR',0.0152,None),(None,'DIELECTRIC',1.065,4.6),('L3','CONDUCTOR',0.0152,None),(None,'DIELECTRIC',0.2104,4.4),('BOTTOM','CONDUCTOR',0.035,None),('SOLDERMASK_BOTTOM','MASK',0.01524,3.8)]}
for n in (2,4):
 tag='reopen%d_02'%n;d=B/'logs'/tag;more=B/'logs'/('more%d_01'%n)
 x=[r for r in rows(d/'cross_section.tsv') if q(r['material'])!='AIR']
 eq('%dL stack entries'%n,len(x),len(expected[n]))
 names=[q(r['name']) for r in x if r['conductor']=='t']
 eq('%dL actual physical copper order'%n,names,['TOP','BOTTOM'] if n==2 else ['TOP','L2','L3','BOTTOM'])
 for i,(r,e) in enumerate(zip(x,expected[n])):
  eq('%dL layer %d name'%(n,i),q(r['name']),e[0] or 'nil')
  eq('%dL layer %d type'%(n,i),q(r['type']),e[1])
  near('%dL layer %d thickness'%(n,i),r['thickness'],e[2])
  if e[3] is not None:near('%dL layer %d sourced scalar Dk'%(n,i),q(r['dk']),e[3])
  if r['conductor']=='t':eq('%dL layer %d positive polarity'%(n,i),r['negative'],'nil')
 total=sum(float(r['thickness']) for r in x);unmasked=sum(float(r['thickness']) for r in x if q(r['type'])!='MASK')
 near('%dL physical sum with modeled masks'%n,total,1.6256 if n==2 else 1.61668)
 near('%dL copper+dielectric sum'%n,unmasked,1.5952 if n==2 else 1.5862)
 eq('%dL all 80 component identities/placement unchanged'%n,norm(rows(d/'components.tsv')),norm(rows(base/'components.tsv')))
 eq('%dL all 69 net inventories unchanged'%n,norm(rows(d/'nets.tsv')),norm(rows(base/'nets.tsv')))
 eq('%dL all 59 mechanical geometry records unchanged'%n,norm(rows(d/'geometry.tsv')),norm(rows(base/'geometry.tsv')))
 oldpads=[r for r in rows(d/'pads.tsv') if q(r['refdes'])!='VIA_TEST' and q(r['layer']) in ['ETCH/TOP','ETCH/BOTTOM']]
 eq('%dL all 544 original outer pin-net-pad rows unchanged'%n,norm(oldpads),norm(rows(base/'pads.tsv')))
 eq('%dL 22 placed physical pin records unchanged'%n,norm(rows(more/'placed_pins.tsv')),norm(rows(baseMore/'placed_pins.tsv')))
 pp=rows(more/'placed_pads.tsv')
 outer=[r for r in pp if q(r['layer']) in ['ETCH/TOP','ETCH/BOTTOM']]
 eq('%dL 44 outer placed pin pads unchanged'%n,norm(outer),norm(rows(baseMore/'placed_pads.tsv')))
 uniqueVia={json.dumps(r,sort_keys=True) for r in rows(d/'vias.tsv')}
 eq('%dL unique native via (dedup extractor aliases)'%n,len(uniqueVia),1)
 via=json.loads(next(iter(uniqueVia)))
 eq('%dL via plating'%n,q(via['plating']),'PLATED');near('%dL via drill'%n,via['diameter'],.3)
 eq('%dL via span'%n,via['startEnd'],'("ETCH/TOP" "ETCH/BOTTOM")')
 eq('%dL via usage'%n,q(via['usage']),'Through_via')
 eq('%dL via net'%n,q(via['net']),'GND')
 eq('%dL via coordinate'%n,via['xy'],'(52.0 35.0)')
 vp={json.dumps(r,sort_keys=True) for r in rows(d/'pads.tsv') if q(r['refdes'])=='VIA_TEST'}
 eq('%dL unique via pad layers'%n,len(vp),n)
 for r in [json.loads(s) for s in vp]:
  eq('%dL via %s regular circle'%(n,r['layer']),q(r['figure']),'CIRCLE')
  eq('%dL via %s copper diameter 0.6'%(n,r['layer']),r['bbox'],'((-0.3 -0.3) (0.3 0.3))')
 for i,r in enumerate(pp):
  ps=q(r['padstack']);layer=q(r['layer']);fig=q(r['figure'])
  if 'NPTH' in ps:
   eq('%dL NPTH row %d remains NULL'%(n,i),fig,'NULL')
   eq('%dL NPTH row %d zero copper bbox'%(n,i),r['bbox'],'((0.0 0.0) (0.0 0.0))')
  elif 'SMD' in ps and layer!='ETCH/TOP':eq('%dL SMD row %d not copied into other copper'%(n,i),fig,'NULL')
  elif 'SLOT' in ps:ck('%dL PTH slot row %d regular copper mapped'%(n,i),fig=='OBLONG_X' and r['bbox']!='((0.0 0.0) (0.0 0.0))')
 for r in rows(more/'placed_pins.tsv'):
  if r['mechanical']=='t':eq('%dL mechanical pin nonplated at %s'%(n,r['xy']),q(r['plating']),'NON_PLATED')
 nativeReport=(d/'readback.txt').read_text()
 ck('%dL independent readback complete/current DRC'%n,'L28_READ COMPLETE' in nativeReport and 'drc_count=0 drc_state=t' in nativeReport)
 launch=json.loads((d/'launch.json').read_text())
 ck('%dL independent process exit0/hash unchanged'%n,launch['completed'] and launch['exitCode']==0 and launch['readonlyHashUnchanged'])
 eq('%dL current board agrees with reopened SHA'%n,sha(B/'native'/('F28_%dL.brd'%n)),launch['afterSHA256'])
 m=json.loads((more/'launch.json').read_text())
 ck('%dL second independent readback hash stable'%n,m['completed'] and m['exitCode']==0 and m['readonlyHashUnchanged'])
 challenge=(B/'logs'/('build%d_01'%n)/'build.txt').read_text()
 ck('%dL controlled +10um mismatch detected and restored'%n,'detected=t' in challenge and 'RESTORED_THICKNESS=' in challenge)
 fdata=rows(d/'films.tsv')
 namesWanted=['TOP','BOTTOM'] if n==2 else ['TOP','L2','L3','BOTTOM']
 eq('%dL copper films plus explicit board outline'%n,{q(r['name']) for r in fdata},set(namesWanted+['F28_DESIGN_OUTLINE']))
 for r in fdata:
  name=q(r['name']);p=r['properties']
  if name in namesWanted:
   orig=next(v for v in filmSources[str(n)]['films'] if v['name']==name)
   ck('%dL %s film exact mapping'%(n,name),all('"'+v+'"' in p for v in orig['layers']))
   ck('%dL %s film sequence remains PDF order'%(n,name),'sequence '+str(orig['sequence'])+' ' in p)
  for k in ['suppressUnconnectPads','drawMissingPadApertures','mirrored','negative','fullContact','useApertureRotation','suppressShapeFill','drawHolesOnly']:
   ck('%dL %s film explicit %s nil'%(n,name,k),k+' nil' in p)
  ck('%dL %s vector pads'%(n,name),'vectorBasedPad t' in p)
 eq('%dL original 01env script hash unchanged'%n,sha(Path(filmSources[str(n)]['path'])),filmSources[str(n)]['sha256'])
 spec['targets'][str(n)]={'name':'OSH Park 2 Layer Prototype' if n==2 else 'JLC04161H-7628','nominalBoardThickness_mm':1.6,'copperDielectricSum_mm':round(unmasked,8),'sumIncludingModeledMasks_mm':round(total,8),'maskGeometry':'Flat 0.0152mm per side; physical purple Dk unspecified' if n==2 else 'Uniform C2 0.01524mm per side effective above-trace model, not full C1/C2/C3 contour','nativeCrossSection':x,'board':str(B/'native'/('F28_%dL.brd'%n)),'SHA256':sha(B/'native'/('F28_%dL.brd'%n)),'readback':str(d),'placedPins':22,'logicalComponents':80,'logicalNets':69,'mechanicalGeometryRows':59,'uniqueViaCount':1}
for n in (2,4):
 mech=B/'logs'/('mech%d_01'%n);mBase=B/'logs'/'mechbase01'
 eq('%dL all explicit design-outline/keepin/keepout shapes preserved'%n,norm(rows(mech/'mechanical_direct.tsv')),norm(rows(mBase/'mechanical_direct.tsv')))
 rtext=(mech/'mechanical_roots.txt').read_text()
 for key in ['designOutline','keepinPlace','keepinRoute']:
  ck('%dL actual root %s exists'%(n,key),key+'=t' in rtext)
 outline=[r for r in rows(mech/'mechanical_direct.tsv') if q(r['layer'])=='BOARD GEOMETRY/DESIGN_OUTLINE']
 eq('%dL exactly one real design outline'%n,len(outline),1)
 eq('%dL real outline 80x60 bbox'%n,outline[0]['bbox'],'((0.0 0.0) (80.0 60.0))')
eq('2L source mask default Dk explicitly unqualified',q(rows(B/'logs'/'reopen2_02'/'cross_section.tsv')[1]['dk']),'4.300000')
for d in (B/'logs').iterdir():
 p=d/'launch.json'
 if p.is_file():
  rec=json.loads(p.read_text());ck(d.name+' real process ended normally',rec['completed'] and rec['exitCode']==0)
  if (d/'stdout.txt').exists():ck(d.name+' no SKILL exception','*Error*' not in (d/'stdout.txt').read_text(errors='replace'))
sources=[
('https://jlcpcb.com/impedance','jlc_impedance_20261019.html','4-layer JLC04161H-7628; explicit dimensional fields / prepreg Dk / mask C1 C2 C3; frequency not given'),
('https://jlcpcb.com/capabilities/pcb-','jlc_capabilities_20261019.html','Public current capability; not a factory approval of this design'),
('https://jlcpcb.com/pcb-impedance-calculator','jlc_calculator_20261019.html','Static official calculator; no dynamic result because no connected browser was available'),
('https://docs.oshpark.com/services/two-layer/','oshpark_two_layer_20261019.html','Complete 2-layer physical build; independent service, no mixing with JLC capability'),
('https://docs.oshpark.com/resources/two-layer-substrate-Kingboard-KB6167F.pdf','Kingboard_KB6167F.pdf','Laminate typical Dk changes with frequency/RC/construction; source page1 and2'),
('https://docs.oshpark.com/resources/rigid-soldermask-taiyo-PSR-4000BN.pdf','Taiyo_PSR4000BN.pdf','Linked mask datasheet says green, not sufficient proof of purple mask RF parameters')]
sources.append(('https://www.ti.com/lit/pdf/SCAA082A','TI_SCAA082A.pdf','Rev A 2017, pages9-10 reference-return path and stackup design principles'))
sources.append(('https://gct.co/files/drawings/usb4105.pdf','GCT_USB4105_RevB4_inherited.pdf','Inherited original GCT drawing RevB4; default shell stake measured from component mounting datum; local product-page fetch blocked, web read succeeded; PCB thickness/process compatibility unverified'))
spec['manufacturingRelease']={'released':False,'twoLayer':{'usbMaskBridge_mm':0.100,'publicOshMinimumMaskWeb_mm':0.1016,'difference_mm':-0.0016,'action':'Revise mask or obtain process acceptance; no entire-board production claim'},'fourLayer':{'impedance90OhmGeometryConfirmed':False,'individualDielectricToleranceQualified':False,'stackupToleranceFieldsZeroMean':'Not supplied, not zero manufacturing tolerance'},'bothTargets':['USB4105 default shell stake S=0.95+/-0.15mm is measured from the component mounting datum, not PCB bottom. Compatibility and soldering on nominal1.6mm PCB are unverified.','Remaining 79 logical components are unplaced; reference planes not poured; no complete board manufacture release.']}
spec['explicitMechanicalReadback']='logs/mechbase01, logs/mech2_01, logs/mech4_01; root designOutline/keepinPlace/keepinRoute plus direct axlDBGetShapes geometry'
spec['sources']=[{'url':u,'file':'source/'+f,'SHA256':sha(B/'source'/f),'use':desc,'retrievedDate':'2026-10-19'} for u,f,desc in sources]
for record in spec['sources']:
 if record['file'].endswith('GCT_USB4105_RevB4_inherited.pdf'):
  record['retrievedDate']='2026-10-18 original download; reused 2026-10-19'
  record['inheritedFrom']='learning/examples/lesson10_connector_20261018/source/usb4105.pdf'
spec['webObservation']={'url':'https://gct.co/connector/usb4105','date':'2026-10-19','scope':'Web text verified shell stake lengths .60/.95/1.20mm; direct local HTML fetch received access challenge, not bypassed. Original drawing PDF is the archived source.'}
(B/'specification.json').write_text(json.dumps(spec,indent=2,ensure_ascii=False),encoding='utf-8')
result={'status':'PASS_NATIVE_CAD_LESSON28_STACKUP','allChecksPass':all(c['pass'] for c in checks),'checksCount':len(checks),'checks':checks,'scope':'2L/4L native stackup editing, detected thickness perturbation and restore, film mappings, padstack instance mapping, mechanical/net preservation, new-process reopen and current DRC; not fabrication approval or impedance certification'}
(B/'validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False,default=lambda v: sorted(v) if isinstance(v,set) else str(v)),encoding='utf-8')
print(result['status'],result['checksCount'],'checks')
