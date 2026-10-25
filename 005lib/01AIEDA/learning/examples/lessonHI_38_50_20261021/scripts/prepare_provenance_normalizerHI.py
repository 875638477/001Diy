from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/normalize_HI_actual_v2.py').read_text().replace('.read_text()',".read_text(encoding='utf8')")
s=s.replace("routes=[]\nfor x in rows",'''def route_key(net,layer,ends,width):
 return (net,layer,tuple(sorted(tuple(p) for p in ends)) if ends else None,width)
role_index={}
if (B/'hi_route_roles.tsv').is_file():
 for rr in rows(B/'hi_route_roles.tsv'):
  role=ssrow(rr);k=route_key(role['net'],role['layer'],role['startEnd'],role['width'])
  role_index.setdefault(k,[]).append(role)
routes=[]
for x in rows''')
needle="vias=[];seen=set()"
s=s.replace("actualEtchLayers={'ETCH/'+sx(x['name']) for x in rows(B/'cross_section.tsv') if sx(x['layerType'])=='CONDUCTOR'}","""for route in routes:
 matches=role_index.get(route_key(route['net'],route['layer'],route['startEnd'],route['width']),[])
 route['nativeProvenance']=matches
 route['generatedThermal']=bool(matches) and all(m.get('thermal') for m in matches) if matches else None
 route['fixedManualCline']=any(m.get('isEtch') and not m.get('thermal') and m.get('parentType')=='path' for m in matches) if matches else None
actualEtchLayerSequence=['ETCH/'+sx(x['name']) for x in rows(B/'cross_section.tsv') if sx(x['layerType'])=='CONDUCTOR']
actualEtchLayers=set(actualEtchLayerSequence)""")
s=s.replace("'actualEtchLayers':sorted(actualEtchLayers)","'actualEtchLayers':actualEtchLayerSequence,'routeProvenanceSource':str(B/'hi_route_roles.tsv') if role_index else None")
(R/'scripts/normalize_HI_actual_v3.py').write_text(s,encoding='ascii')
s=(R/'scripts/extract_checkpointHI.py').read_text().replace("scripts/normalize_HI_actual.py","scripts/normalize_HI_actual_v3.py")
(R/'scripts/extract_checkpointHI_v3.py').write_text(s,encoding='ascii')
print('normalizer3: native layer sequence and line thermal provenance')
