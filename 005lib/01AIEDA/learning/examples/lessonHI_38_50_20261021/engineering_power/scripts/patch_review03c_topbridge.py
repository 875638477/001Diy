from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
p=R/'scripts/review_power03c.py';s=p.read_text()
needle=" check(variant+'.VINandFBnotshorted'"
where=s.index(needle)
extra=""" for pin in ['U1.24','U1.36','U1.48','U1.1','R26.1']:
  check(variant+'.V3MainNativeComponent.'+pin,bynet.get(pin)==bynet.get('C9.1'),[bynet.get(pin),bynet.get('C9.1')])
 topG=[LineString(x['startEnd']).buffer(x['width']/2,quad_segs=32) for x in a['routes'] if x['kind']=='line' and x['net']=='GND' and x['layer']=='ETCH/TOP']
 topG+=[box(*p['padBBox'][0],*p['padBBox'][1]) for c in a['placements'] for p in c['pins'] if p['net']=='GND' and p['number'] and p['figure']!='NULL']
 topG+=[Point(v['xy']).buffer(.3,quad_segs=64) for v in a['vias'] if v['net']=='GND']
 tg=unary_union(topG);comps=list(tg.geoms) if hasattr(tg,'geoms') else[tg]
 # The bridge must exist as actualTOPcopper, not merely share a net through the global plane.
 check(variant+'.actualTOPGroundBridgeAcrossV3BottomSlit',any(q.buffer(.00001).covers(Point(32.45,25.2748)) and q.buffer(.00001).covers(Point(29.8,28.918)) for q in comps),dict(fromXY=[32.45,25.2748],toXY=[29.8,28.918],scope='OnlyexportedTOPGNDcopper/pads/viaannuli, no referenceplanes included.'))
"""
s=s[:where]+extra+s[where:];p.write_text(s)
print('patchedtopbridgeproof')
