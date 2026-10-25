from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');p=R/'scripts/select_SPI4L_return_v6.py';s=p.read_text()
s=s.replace('from shapely.ops import unary_union','from shapely.ops import unary_union\nfrom shapely.strtree import STRtree\nfrom shapely.prepared import prep')
s=s.replace("actualG=[", "ps={l:prep(q) for l,q in ps.items()}\ntree=STRtree([a['g'] for a in items])\nactualG=[")
s=s.replace("ps[l].buffer(1e-7).covers(g)","ps[l].covers(g)")
s=s.replace('for a in items:',"for ai in tree.query(g.buffer(.51)):\n    a=items[int(ai)]")
p.write_text(s,encoding='utf-8')