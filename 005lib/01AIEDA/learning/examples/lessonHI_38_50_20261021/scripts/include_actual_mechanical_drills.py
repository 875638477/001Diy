import pathlib
p=pathlib.Path(__file__).parent/'routing_geometry.py';s=p.read_text(encoding='utf8')
old="  for a in self.policy.get('componentAnchors',[]):"
new="""  # Real unnumbered mechanical drill data, independently read from native pad definitions.
  # These are NOT the zero-sized regular-copper BBOX of a NULL mechanical pad.
  mechSource=ROOT/f'inventory/mechanical_pins_{snapshot["variant"]}_b012.json'
  self.mechanicalDrillEvidence=str(mechSource)
  mech=load(mechSource)
  for hole in mech['mechanicalPins']:
   if hole['refdes']!='J2':continue # Four mounting bores already have stricter diameter5 teaching zones below.
   actual=next(p for p in snapshot['placements'] if p['ref']==hole['refdes'])
   assert any(x['mechanical'] and x['padstack']==hole['padstack'] and math.dist(x['xy'],hole['xy'])<1e-6 for x in actual['pins']),'Mechanical drill location must match source snapshot'
   assert hole['holeType']=='circle_drill' and hole['drillDiameter']>0
   for layer in LAYERS:self.add(None,layer,Point(hole['xy']).buffer(hole['drillDiameter']/2,quad_segs=24),'hole','nativeMechanical:'+hole['padstack'])
  for a in self.policy.get('componentAnchors',[]):"""
assert old in s;s=s.replace(old,new)
s=s.replace("'shape':'via_shape'", "'shape':'via_shape','hole':'hole_via'")
p.write_text(s,encoding='utf8')