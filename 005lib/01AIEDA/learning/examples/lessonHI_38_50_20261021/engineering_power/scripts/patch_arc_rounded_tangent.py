from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');f=R/'scripts/cadence_poly.py';s=f.read_text();b=R/'scripts/cadence_poly_v1_before_rounded_arcs.py'
if not b.exists():b.write_text(s,encoding='utf-8')
s=s.replace('def polygon_from_vertices', 'ROUNDED_ARC_FLATTENED = []\n\ndef polygon_from_vertices')
s=s.replace('  assert len(options)==1,(start,end,rr,options)', '''  if len(options)!=1:
   # Near a quadrant tangent the rounded endpoints can make left/right ambiguous.
   # Flatten only if the full minor-arc sagitta is <=1e-6mm, much smaller
   # than conservative_plane's 0.0001mm erosion/expansion. Preserve audit.
   sag=r-math.sqrt(max(0,r*r-d*d/4))
   if sag<=1e-6:
    ROUNDED_ARC_FLATTENED.append(dict(start=start,end=end,radius=rr,sagitta_mm=sag))
    out.append(end);continue
   raise AssertionError((start,end,rr,options,sag))''')
f.write_text(s,encoding='utf-8')