from pathlib import Path
import sys,json,math,csv,re
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
O=H/'engineering_power';n=load(H/'review/PROVISIONAL_UNSAVED_b016_2L_try11.json');w=load(O/'N49_2L_networks.json');r=load(O/'N49_2L_rules.json');p=load(O/'N49_2L_policy.json');s=CopperScene(n,w,r,p)
j=next(c for c in n['placements'] if c['ref']=='J2');print('J2',[(a['number'],a['net'],a['xy']) for a in j['pins'] if a['net']=='GND'])
candidates=[([44.32,2.6],[[44.32,6.78],[44.32,2.6]]),([46.8,2.2],[[44.32,6.78],[46.8,4.3],[46.8,2.2]]),([47.8,3.2],[[44.32,6.295],[45.8,6.295],[47.8,4.295],[47.8,3.2]]),([49.5,4.8],[[44.32,6.295],[46,6.295],[47.495,4.8],[49.5,4.8]]),([43.8,10.7764],[[44.32,6.295],[45.3,6.295],[45.3,10.7764],[43.8,10.7764]])]
report=[]
for xy,pts in candidates:
 hits=[];bridge=LineString(pts).buffer(.3)
 for a in s.obstacles:
  if a['net']=='GND':continue
  if a['layer']=='TOP':
   gap=bridge.distance(a['geometry']);need=s.space('GND',a['net'],'TOP',a['kind'])
   if gap<need-.0001:hits.append(dict(kind='TOPbridge',net=a['net'],object=a['source'],gap=gap,need=need,bbox=a['geometry'].bounds))
  g=Point(xy).buffer(.3,quad_segs=32);gap=g.distance(a['geometry']);need=s.space('GND',a['net'],a['layer'],a['kind'],True)
  if gap<need-.0001:hits.append(dict(kind='via',layer=a['layer'],net=a['net'],object=a['source'],gap=gap,need=need,bbox=a['geometry'].bounds))
 coverage=[]
 for i,a in enumerate(n['planes']):
  if a['net']=='GND' and a['layer']=='ETCH/BOTTOM':
   g=plane_from_native(dict(a,holes=a.get('holes') or []))
   if g.intersects(Point(xy).buffer(.3)):coverage.append(dict(index=i,area=g.area,missingDisk=Point(xy).buffer(.3,quad_segs=48).difference(g).area,bbox=g.bounds))
 report.append(dict(xy=xy,points=pts,pathClear=s.path_clear('GND','TOP',pts,.6),hits=hits,coverage=coverage));print(json.dumps(report[-1]))
(O/'readouts/SH2_return12_candidates.json').write_text(json.dumps(dict(source='PROVISIONAL_UNSAVED_b016_2L_try11',candidates=report),indent=2))
rows=[]
for row in csv.DictReader((Path(n['readbackDirectory'])/'hi_graph_objects.tsv').open(encoding='utf8'),delimiter='\t'):
 if row['net'].strip(chr(34))!='GND':continue
 if row['type'].strip(chr(34))=='pin' and ('xy (44.32 2.6)' in row['attributes'] or 'xy (44.32 6.78)' in row['attributes']):rows.append(dict(component=row['component'],type=row['type'],attributes=row['attributes']))
print('PINS',json.dumps(rows));(O/'readouts/SH2_actual_native_graph12.json').write_text(json.dumps(rows,indent=2))