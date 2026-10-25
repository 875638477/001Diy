from pathlib import Path
P=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\scripts\render_native_copper.py')
s=P.read_text(encoding='utf8').replace('q=plane_from_native(p);','q=plane_from_native(dict(p,holes=p.get(\'holes\') or []));')
P.write_text(s,encoding='utf8')