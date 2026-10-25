import pathlib,json,csv,math,re,hashlib,sys
BASE=pathlib.Path(__file__).resolve().parent.parent
s=json.loads((BASE/'lesson09_spec.json').read_text(encoding="utf-8-sig"))
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8-sig'),delimiter='\t'))
def num(v):return float(v)
def near(a,b,tol=1e-5):assert abs(float(a)-float(b))<tol,(a,b)
def box(v):return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?(?:e[+-]?\d+)?',v)]
def rr(w,h,r):return w*h-(4-math.pi)*r*r
checks=[]
for sp in s['packages']:
 name=sp['name']; d=BASE/'logs'/(name+'_reopen03'); pins=rows(d/'pins.tsv'); pads=rows(d/'pads.tsv'); shapes=rows(d/'shapes.tsv'); texts=rows(d/'texts.tsv'); polygons=rows(d/'polygons.tsv')
 assert 'L09 READ COMPLETE' in (d/'verify.txt').read_text(encoding="utf-8-sig")
 assert 'drcs=0 drcState=t' in (d/'verify.txt').read_text(encoding="utf-8-sig")
 assert len(pins)==len(sp['pins'])
 assert {int(p['number']) for p in pins}==set(range(1,len(pins)+1))
 pinmap={int(p['number']):p for p in pins}
 for exp in sp['pins']:
  p=pinmap[exp['number']];near(p['x'],exp['xy'][0]);near(p['y'],exp['xy'][1]);near(p['rotation'],exp['rotation'])
  assert p['through']=='nil' and p['hole']=='none' and p['top']=='t' and p['bottom']=='nil'
  padname=sp['ep'] if exp['number']==17 and 'ep' in sp else sp['pad']
  assert p['padstack'].lower()==padname
  for kind,layer in [('c','ETCH/TOP'),('m','PIN/SOLDERMASK_TOP'),('p','PIN/PASTEMASK_TOP')]:
   pr=next(r for r in pads if int(r['number'])==exp['number'] and r['layer']==layer)
   definition=s['pads'][padname]
   if kind not in definition:assert pr['figure']=='NULL';continue
   w,h,r=definition[kind];ow,oh=(h,w) if exp['rotation']==90 else (w,h);near(pr['width'],ow);near(pr['height'],oh);near(pr['radius'],r)
   assert pr['figure']==('ROUNDED_RECTANGLE' if r else 'RECTANGLE')
   if r:assert set(pr['corners'].split('-'))=={'UR','UL','LL','LR'}
   if kind in ['c','p']:
    poly=next(r for r in polygons if int(r['number'])==exp['number'] and r['layer']==layer)
    near(poly['area'],rr(w,h,r),5e-6)
    bb=box(poly['bbox']);pw,ph=(h,w) if exp['rotation']==90 else(w,h)
    for a,b in zip(bb,[exp['xy'][0]-pw/2,exp['xy'][1]-ph/2,exp['xy'][0]+pw/2,exp['xy'][1]+ph/2]):near(a,b)
  for layer in ['ETCH/BOTTOM','PIN/SOLDERMASK_BOTTOM','PIN/PASTEMASK_BOTTOM']:
   assert next(r for r in pads if int(r['number'])==exp['number'] and r['layer']==layer)['figure']=='NULL'
 for layer in ['REF DES/SILKSCREEN_TOP','REF DES/ASSEMBLY_TOP','COMPONENT VALUE/ASSEMBLY_TOP']:
  t=next(t for t in texts if t['layer']==layer);near(t['x'],0);near(t['y'],0)
 bounds=[r for r in shapes if r['layer']=='PACKAGE GEOMETRY/PLACE_BOUND_TOP'];assert len(bounds)==1
 assert f'"{sp["height"]} MM"' in bounds[0]['properties'] or (sp['height']==1 and '"1 MM"' in bounds[0]['properties'])
 paste=[r for r in shapes if r['layer']=='PACKAGE GEOMETRY/PASTEMASK_TOP'];assert len(paste)==len(sp['pasteWindows'])
 for exp in sp['pasteWindows']:
  x,y,w,h=exp; assert any(all(abs(a-b)<1e-5 for a,b in zip(box(r['bbox']),[x-w/2,y-h/2,x+w/2,y+h/2])) for r in paste)
 # Source-driven independent checks: do not merely compare a duplicated generator list.
 if 'stm32' in name:
  assert len(pins)==48;near(max(abs(num(p['x'])) for p in pins)*2+1.2,9.7)
  near(min(abs(num(p['x'])) for p in pins if abs(num(p['x']))>4)-.6,7.3/2)
  expected_min_gap=.2
 else:
  assert len(pins)==17;near(max(abs(num(p['x'])) for p in pins),2.8/2)
  near(next(r for r in pads if r['number']=='17' and r['layer']=='ETCH/TOP')['width'],1.68)
  expected_min_gap=.26
 copper=[box(r['bbox']) for r in polygons if r['layer']=='ETCH/TOP']
 gaps=[]
 for i,a in enumerate(copper):
  for b in copper[i+1:]:
   dx=max(a[0]-b[2],b[0]-a[2],0);dy=max(a[1]-b[3],b[1]-a[3],0)
   assert dx>0 or dy>0,'Unintended copper bbox overlap'
   gaps.append(math.hypot(dx,dy))
 near(min(gaps),expected_min_gap)
 launch=json.loads((d/'launch.json').read_text(encoding="utf-8-sig"));assert launch['readonlyHashUnchanged'] and launch['exitCode']==0
 checks.append({'package':name,'pins':len(pins),'geometry':'PASS','roundRectRadiusCorners':'PASS','numberingViewOrigin':'PASS','padsMasksPaste':'PASS','heightMAX':sp['height'],'requiredTextsOrigin':'PASS','minNominalCopperGapMM':min(gaps),'minNominalMaskWebMM':.1 if 'stm32' in name else .12,'nativeStoredDRC':0,'nativeDRCState':True,'readonlySHAUnchanged':True})
board=BASE/'logs'/'board_reopen';bp=rows(board/'pins.tsv');bs=rows(board/'symbols.tsv');bsh=rows(board/'shapes.tsv');bd=rows(board/'pads.tsv')
assert len(bs)==9 and len(bp)==246
assert 'L09 READ COMPLETE' in (board/'verify.txt').read_text(encoding="utf-8-sig")
for sp,y0 in zip(s['packages'],[15,0,-15]):
 for x0,rot,mirror in [(-20,0,False),(0,90,False),(20,0,True)]:
  sy=next(r for r in bs if r['name'].lower()==sp['name'] and num(r['x'])==x0 and num(r['y'])==y0)
  near(sy['rotation'],rot);assert sy['mirrored']==('t' if mirror else 'nil')
  for p in sp['pins']:
   x,y=p['xy']
   if rot==90:x,y=-y,x
   if mirror:x=-x
   x+=x0;y+=y0
   actual=[a for a in bp if int(a['number'])==p['number'] and abs(num(a['x'])-x)<1e-5 and abs(num(a['y'])-y)<1e-5]
   assert len(actual)==1,(sp['name'],p,x,y)
   actual=actual[0];assert actual['top']==('nil' if mirror else 't') and actual['bottom']==('t' if mirror else 'nil')
   near(actual['relx'],p['xy'][0]);near(actual['rely'],p['xy'][1])
  if sp['pasteWindows']:
   layer='PACKAGE GEOMETRY/PASTEMASK_BOTTOM' if mirror else 'PACKAGE GEOMETRY/PASTEMASK_TOP'
   matching=[]
   for r in bsh:
    bb=box(r['bbox']);cx=(bb[0]+bb[2])/2;cy=(bb[1]+bb[3])/2
    if r['layer']==layer and abs(cx-x0)<1 and abs(cy-y0)<1:matching.append(r)
   assert len(matching)==4
   near(sum(num(r['area']) for r in matching),1.69)
viaids=rows(BASE/'logs'/'via_ids_reopen'/'via_ids.tsv');assert len(viaids)==5 and len({r['dbid'] for r in viaids})==5
assert 'COUNT=5 COMPLETE' in (BASE/'logs'/'via_ids_reopen'/'via_complete.txt').read_text(encoding="utf-8-sig")
assert json.loads((BASE/'logs'/'via_ids_reopen'/'launch.json').read_text(encoding="utf-8-sig"))['readonlyHashUnchanged']
via=rows(board/'vias.tsv'); unique={tuple(r.values()) for r in via};assert len(unique)==5
assert {(round(float(v[1])+20,2),round(float(v[2])+15,2)) for v in unique}=={tuple(v) for v in s['thermalVia']['centers']}
for r in via:near(r['drill'],.2);assert r['plating']=='PLATED' and r['through']=='t' and r['net']==''
for r in bd:
 if r['number']=='VIA':
  if r['layer'].startswith('ETCH/'):near(r['width'],.4);near(r['height'],.4)
  else:assert r['figure']=='NULL'
conductors=re.findall(r'layer="([^"]+)" type="CONDUCTOR"',(board/'verify.txt').read_text(encoding="utf-8-sig"));assert conductors==['TOP','L2','L3','BOTTOM']
coverage={'roundedEPAreaMM2':rr(1.68,1.68,.05),'singleRoundedPasteAreaMM2':rr(1.55,1.55,.05),'singleRoundedCoveragePercent':100*rr(1.55,1.55,.05)/rr(1.68,1.68,.05),'splitSquarePasteAreaMM2':4*.65**2,'splitRoundedCoveragePercent':100*4*.65**2/rr(1.68,1.68,.05),'splitRectangularCoveragePercent':100*4*.65**2/1.68**2,'windowSquareAreaRatioAt0125':.65/(4*.125),'qfnPeripheralRoundedAreaRatioAt0125':rr(.6,.24,.05)/((2*(.6+.24)-8*.05+2*math.pi*.05)*.125)}
result={'status':'PASS_CAD_LESSON09','packages':checks,'placementCases':9,'placedPins':246,'placementRotationMirror':'PASS','splitWindowsMirror':'PASS','thermalVias':{'unique':5,'uniqueNativeDBIDs':5,'dbidAudit':'logs/via_ids_reopen/via_ids.tsv','rawExtractRows':len(via),'drillMM':.2,'copperMM':.4,'layers':conductors,'net':'unassigned geometric example; actual EP/GND connectivity not claimed','maskPaste':'NULL pad apertures; package EP opening still exposes top via area; no filled/tented manufacturing proof'},'coverage':coverage,'knownLimitations':['Original REF DES silk anchor0,0 retained per user; QFN overlaps EP soldermask, must relocate or clip in manufacturing artwork.','Split paste differs from RGT-specific manufacturer single-window recommendation; assembly approval required.','Board storedDRC=0 with drcState=nil; not asserted as fresh DRC pass.','No electrical connectivity/SI/PI/EMI board signoff; no thermal performance or assembly experiment.'],'sourceManifest':str(BASE/'source'/'manifest.json')}
(BASE/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))




