import pathlib,json,sys,math,hashlib
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1];sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
source=H/'inventory/checkpoints/padentry_4L_b019_DRC_PENDING/normalized.json';n=load(source);d=load(P/'PB15_4L_short_L2_comparison_95.json');op=next(o for o in d['operations']if o.get('layer')=='L2');ln=LineString(op['points']);slot=ln.buffer(.4,quad_segs=20)
l3=unary_union([plane_from_native(dict(z,holes=z.get('holes')or[]))for z in n['planes']if z['layer']=='ETCH/L3'and z.get('filled')and z['net']=='GND'])
# Approximate intended new signal-PTH antipads using declared .52 copper and preserved .30 GND spacing; native dynamic fill remains authoritative.
anti=unary_union([Point(o['xy']).buffer(.56,quad_segs=20)for o in d['operations']if o['type']=='via'and o['net']=='GPIO_PB15']);projected=l3.difference(anti)
refs=[]
for name,g in [('actual_b019_L3_before_candidate',l3),('planned_L3_after_new_PTH_antipads',projected)]:
 refs.append(dict(identity=name,centerlineCoveredMM=ln.intersection(g).length,centerlineUncoveredMM=ln.difference(g).length,traceCopperAreaMM2=ln.buffer(.1).area,traceCopperCoveredAreaMM2=ln.buffer(.1).intersection(g).area,fieldBuffer04CoveredAreaMM2=slot.intersection(g).area,uncoveredBounds=(None if ln.difference(g).is_empty else list(ln.difference(g).bounds))))
cross={}
for r in n['routes']:
 if r['layer']!='ETCH/TOP'or r.get('generatedThermal'):continue
 wire=LineString(r['startEnd']);piece=wire.intersection(slot)
 if piece.length>1e-8:cross[r['net']]=cross.get(r['net'],0)+piece.length
pads=[]
for q in n['placements']:
 if q['ref']not in ['C15','C16','R17']:continue
 for a in q['pins']:
  if not a['number']:continue
  geom=box(*a['padBBox'][0],*a['padBBox'][1]);pads.append(dict(pin=q['ref']+'.'+a['number'],net=a['net'],plannedL2SlotClearanceMM=geom.distance(slot),slotOverlapAreaMM2=geom.intersection(slot).area))
out=dict(status='REFERENCE_ENGINEERING_COMPARISON_NOT_NATIVE_FILL',candidate=str(P/'PB15_4L_short_L2_comparison_95.json'),candidateSHA256=hashlib.sha256((P/'PB15_4L_short_L2_comparison_95.json').read_bytes()).hexdigest(),actualSnapshot=str(source),actualSnapshotSHA256=hashlib.sha256(source.read_bytes()).hexdigest(),L3Reference=refs,projectedTOPCenterlineCrossingPlannedL2SlotMM=cross,padProjection=pads,qualification=['Actual b019 plane geometry, not simulation or native repour of this candidate','New PTH antipad subtraction is explicit planar estimate radius.56; actual native thermal/clearance/plane readback still required','L2 slot removes local TOP reference under listed ordinary crossings, even though L3 can reference the new inner signal','Near transition reference openings are expected and need actual nearby common-GND return; no 100-percent-microstrip or SI certification claim'])
(P/'PB15_4L_L2_reference_95.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out))

