import pathlib
h=pathlib.Path(__file__).resolve().parent
p=h/'routing_geometry.py';s=p.read_text(encoding='utf8')
s=s.replace("for layer in LAYERS:self.add(a['net'],layer,Point(a['xy']).buffer(.3,quad_segs=12),'via','native_via')", "for layer in LAYERS:\n    pads=[p for p in a.get('pads',[]) if p.get('layer','').removeprefix('ETCH/')==layer]\n    radius=max((max(abs(x) for pt in p['bbox'] for x in pt) for p in pads),default=.3)\n    self.add(a['net'],layer,Point(a['xy']).buffer(radius,quad_segs=12),'via','native_via')")
s=s.replace("for layer in LAYERS:self.add(o['net'],layer,Point(o['xy']).buffer(.3,quad_segs=12),'via',o['id'])", "for layer in LAYERS:self.add(o['net'],layer,Point(o['xy']).buffer(o.get('padDiameterMM',.6)/2,quad_segs=12),'via',o['id'])")
p.write_text(s,encoding='utf8')
p=h/'review_candidate_paths.py';s=p.read_text(encoding='utf8')
s=s.replace("  if op['type']!='deleteSegment':continue", "  if op['type']=='deleteVia':\n   matches=[v for v in snapshot.get('vias',[]) if v['net']==op['net'] and math.dist(v['xy'],op['xy'])<1e-6 and (not op.get('padstack') or v['padstack']==op['padstack'])]\n   assert len(matches)==1,('Candidate via ripup must uniquely match actual copper',op,len(matches))\n   snapshot['vias'].remove(matches[0]);deleted.append({'operation':op['id'],'actualVia':matches[0]});continue\n  if op['type']!='deleteSegment':continue")
s=s.replace("Point(op['xy']).buffer(.3,quad_segs=20)","Point(op['xy']).buffer(op.get('padDiameterMM',.6)/2,quad_segs=20)")
p.write_text(s,encoding='utf8')