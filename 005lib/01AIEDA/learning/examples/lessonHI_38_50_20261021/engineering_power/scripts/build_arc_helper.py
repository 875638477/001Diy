from pathlib import Path
import textwrap
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
s=(R/'scripts/review_power02d.py').read_text()
start=s.index('  def cadpoly(vs):')
end=s.index("  outer=cadpoly",start)
fn=textwrap.dedent(s[start:end]).replace('def cadpoly(vs):','def polygon_from_vertices(vs, step_degrees=.5):').replace('math.radians(.5)','math.radians(step_degrees)')
header='''"""Read-only Cadence polygon conversion.
Source: installation official axlPolyFromDB.txt, copied to ../source.
Radius belongs to previous->current point. Positive arc is left of local Y-axis;
negative is right. Cadence splits arcs at quadrant boundaries.
No Cadence process/API calls. Requires caller to make Shapely available.
Half-degree chords are an approximation: use conservative_plane(.0001) for
clearance and compare area against exported native area. Not a field solver.
"""
import math
from shapely.geometry import Polygon
from shapely.ops import unary_union

'''
tail='''\ndef plane_from_native(record, step_degrees=.5):
 outer=polygon_from_vertices(record['vertices'],step_degrees)
 holes=[polygon_from_vertices(h,step_degrees) for h in record['holes']]
 return outer.difference(unary_union(holes))

def conservative_plane(record,tolerance_mm=.0001,step_degrees=.5):
 outer=polygon_from_vertices(record['vertices'],step_degrees)
 holes=[polygon_from_vertices(h,step_degrees) for h in record['holes']]
 return outer.buffer(-tolerance_mm).difference(unary_union(holes).buffer(tolerance_mm))
'''
(R/'scripts/cadence_poly.py').write_text(header+fn+tail,encoding='utf-8')
print(str(R/'scripts/cadence_poly.py'))
