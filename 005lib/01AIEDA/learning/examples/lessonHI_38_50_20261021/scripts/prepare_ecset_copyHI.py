from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/batchHI_shapes_v3.il';s=p.read_text().replace('equal(o->objType "line") && rexMatchp("^ETCH/" o->layer)','equal(o->objType "line") && o->layer && rexMatchp("^ETCH/" o->layer)');p.write_text(s,encoding='ascii')
s=(R/'scripts/compile_batchHI_v7.py').read_text()
s=s.replace(" elif typ=='netClass':",''' elif typ=='ecsetCopy':
  vals='list('+' '.join('list(\\''+k+' '+quotedValue(v)+')' for k,v in op['values'].items())+')'
  statements.append(f'hiECSetCopy(f {q(op["name"])} {q(op["copyFrom"])} {vals} {q(op["pair"])})')
 elif typ=='netClass':''')
(R/'scripts/compile_batchHI_v8.py').write_text(s,encoding='ascii')
print('ECSet copy/pair scope and null layer guard prepared')
