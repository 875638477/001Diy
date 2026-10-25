from pathlib import Path
import sys,json,math,hashlib
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
O=H/'engineering_power';src=H/'review/PROVISIONAL_UNSAVED_b016_2L_try09.json';n=load(src);w=load(O/'N40_2L_networks.json');r=load(O/'N40_2L_rules.json');p=load(O/'N40_2L_policy.json');s=CopperScene(n,w,r,p);xy=[35.8,20.5];bridge=[[35.8,21.95],xy];checks=[]
for layer,g,isvia in [('TOP',LineString(bridge).buffer(.3),False),('TOP',Point(xy).buffer(.3,quad_segs=32),True),('BOTTOM',Point(xy).buffer(.3,quad_segs=32),True)]:
 for a in s.obstacles:
  if a['net']=='GND' or a['layer']!=layer:continue
  gap=g.distance(a['geometry']);need=s.space('GND',a['net'],layer,a['kind'],isvia)
  if gap<need+.15:checks.append(dict(layer=layer,object=a['source'],net=a['net'],kind=a['kind'],gapMM=gap,needMM=need,passBaseField=gap>=need-1e-6))
planes=[]
for i,a in enumerate(n['planes']):
 if a['net']=='GND' and a['layer']=='ETCH/BOTTOM':
  g=plane_from_native(dict(a,holes=a.get('holes') or []));parts=[g] if g.geom_type=='Polygon' else list(g.geoms)
  for j,part in enumerate(parts):
   if part.covers(Point(xy)):
    planes.append(dict(planeIndex=i,component=j,areaMM2=part.area,fullCopperDiskUncoveredMM2=Point(xy).buffer(.3,quad_segs=48).difference(part).area,signedCenterBoundaryDistanceMM=part.boundary.distance(Point(xy)),sameComponentVSS23ViaCopperOverlapMM2=part.intersection(Point(38,25.27).buffer(.3,quad_segs=32)).area,VSS23ViaCenterMayBeDrillVoid=not part.covers(Point(38,25.27)),oldWestCenterCovered=part.covers(Point(35.8,21.95))))
ops=[dict(type='route',id='B016_WEST_COMMON_TOP_BRIDGE',net='GND',layer='TOP',points=bridge,width=.6,purpose='Actual b016 new PB12 BOTTOM slot isolated old WEST return; bridge to common BOTTOM south side without globalTOP or quiet-domain reuse'),dict(type='via',id='B016_WEST_COMMON_BOTTOM_VIA',net='GND',xy=xy,padstack='L28_VIA030_C060',purpose='Connect TOP bridge to actual common BOTTOM GND south of slot; native graph must restore old WEST to U1.23')]
out=dict(status='PASS_ACTUAL_UNSAVED_GEOMETRY_NATIVE_GRAPH_REFILL_PENDING',source=str(src),sourceSHA256=hashlib.sha256(src.read_bytes()).hexdigest(),scope='Actual unsaved try09 copper only; no derived erroneous V3 deletion analysis; new native fill and graph authoritative',operations=ops,checks=checks,failed=[a for a in checks if not a['passBaseField']],actualExistingBottomComponentsAtNewVia=planes,requiredNative=['Exact actual try09 rebuild/reapply after LIVE R27 power feed restoration','new stockvia copper through actual BOTTOM common component','old WEST via35.8,21.95 reaches U1.23; C13/C14/C15 loops and all prior GND proofs preserved','HSE singleanchor negative unchanged','PB12/PA10/class-class/ground-specific scoped DRC zero; full final whole-board DRC later'],variant='2L_ONLY_NO_4L_CHANGE')
(O/'readouts/B016_WEST_COMMON_BRIDGE_01.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
import csv
import re
rows=[]
for row in csv.DictReader((Path(n['readbackDirectory'])/'hi_graph_objects.tsv').open(encoding='utf8'),delimiter='\t'):
 if row['net'].strip(chr(34))!='GND':continue
 mt=re.search(r'\bxy \(([-+\d.]+) ([-+\d.]+)\)',row['attributes']);bb=re.search(r'\bbBox (\(\([^)]+\) \([^)]+\)\))',row['attributes']);dd={'xy':[float(z) for z in mt.groups()] if mt else None,'bBoxText':bb.group(1) if bb else None}
 if row['type'].strip(chr(34))=='shape' or (row['type'].strip(chr(34))=='via' and dd.get('xy') in [[38.,25.27],[35.8,21.95]]):rows.append(dict(component=row['component'],type=row['type'],xy=dd.get('xy'),bbox=dd.get('bBoxText'),layer=row['layer']))
out['actualNativeGraphRelevantObjects']=rows
(O/'readouts/B016_WEST_COMMON_BRIDGE_01.json').write_text(json.dumps(out,indent=2));print('NATIVEGRAPH',json.dumps(rows))