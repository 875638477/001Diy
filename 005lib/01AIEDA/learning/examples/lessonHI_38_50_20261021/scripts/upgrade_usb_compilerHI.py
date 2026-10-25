from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/compile_batchHI_v4.py').read_text().replace('.read_text()',".read_text(encoding='utf8')")
s=s.replace(" elif typ=='netClass':",'''  for layer,fields in op.get('layerValues',{}).items():
   for field,val in fields.items():statements.append(f'hiCSetLayerValue(f \\'{domain} {q(op["name"])} {q(layer)} \\'{field} {quotedValue(val)})')
 elif typ=='netClass':''')
s=s.replace("+q(x['cset'])+')' for x in op['assignments']", "+q(x['cset'])+' '+(q(x['otherNetClass']) if x.get('otherNetClass') else 'nil')+')' for x in op['assignments']")
s=s.replace("print(json.dumps(record,indent=2))","print(json.dumps({k:v for k,v in record.items() if k not in ['helperSnapshots','endpointDefinitions']},indent=2))")
(R/'scripts/compile_batchHI_v5.py').write_text(s,encoding='ascii')
# Keep the old readback preparers as history; new JSON plans may include UTF-8 engineering notes.
s=(R/'scripts/prepare_readbackHI_v3.py').read_text().replace('.read_text()',".read_text(encoding='utf8')")
(R/'scripts/prepare_readbackHI_v4.py').write_text(s,encoding='ascii')
print('compiler5/readback4 UTF8, CSet layer fields and Region-Class-Class')
