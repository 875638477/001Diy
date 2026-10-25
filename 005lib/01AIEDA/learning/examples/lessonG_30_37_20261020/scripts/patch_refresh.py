from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
p=R/'scripts/placementG.il'
(R/'scripts/placementG_v01_failed.il').write_bytes(p.read_bytes())
s=p.read_text().replace('  unless(length(setof(c axlDBGetDesign()->components c->symbol))==80', '  axlDBRefreshId(nil)\n  fprintf(f "POST_REFRESH logicalPlaced=%d symbols=%d\\n" length(setof(c axlDBGetDesign()->components c->symbol)) length(axlDBGetDesign()->symbols))\n  unless(length(setof(c axlDBGetDesign()->components c->symbol))==80')
p.write_text(s,encoding='ascii')
scr=R/'scripts/place_4L_v1.scr'
(R/'scripts/place_4L_v2.scr').write_text(scr.read_text().replace('/logs/place_4L_v1','/logs/place_4L_v2'),encoding='ascii')
print('CACHE_REFRESH_PATCH_READY')
