from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/normalize_HI_actual_v3.py';s=p.read_text()
s=s.replace("role=ssrow(rr);k=route_key(role['net'],role['layer'],role['startEnd'],role['width'])","""role=ssrow(rr)
  parent_attrs=role.get('parentAttributes') or []
  parent_props=dict(zip(parent_attrs[::2],parent_attrs[1::2]))
  role['lineThermal']=bool(role.get('thermal'))
  role['parentThermal']=bool(parent_props.get('thermal'))
  role['thermal']=role['lineThermal'] or role['parentThermal']
  k=route_key(role['net'],role['layer'],role['startEnd'],role['width'])""")
s=s.replace("'routeProvenanceSource':str(B/'hi_route_roles.tsv') if role_index else None","'routeProvenanceSource':str(B/'hi_route_roles.tsv') if role_index else None,'thermalClassification':'Native line thermal OR native parent path thermal. Cadence17.2 generated reliefs return line.thermal=nil but parent.thermal=t; raw parentAttributes retained.'")
(R/'scripts/normalize_HI_actual_v4.py').write_text(s,encoding='ascii')
s=(R/'scripts/extract_checkpointHI.py').read_text().replace("scripts/normalize_HI_actual.py","scripts/normalize_HI_actual_v4.py")
(R/'scripts/extract_checkpointHI_v4.py').write_text(s,encoding='ascii')
print('normalizer4 effective native thermal=line or path; raw parent evidence retained')
