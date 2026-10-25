from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/review_candidate_paths.py';s=p.read_text(encoding='utf8')
needle="changes={}\n"
insert="""changes={}
deleted=[]
for plan in plans:
 for op in plan.get('operations',[])+plan.get('commonOperations',[])+plan.get('variantOperations',{}).get(snapshot['variant'],[]):
  if op['type']!='deleteSegment':continue
  matches=[r for r in snapshot['routes'] if r['net']==op['net'] and r['layer']=='ETCH/'+op['layer'] and abs(r['width']-op['width'])<1e-6 and (r['startEnd']==op['points'] or r['startEnd']==list(reversed(op['points']))) ]
  assert len(matches)==1,('Candidate ripup must uniquely match actual copper',op,len(matches))
  snapshot['routes'].remove(matches[0]);deleted.append({'operation':op['id'],'actual':matches[0]})
"""
s=s.replace(needle,insert);s=s.replace("'placementChanges':list(changes.values()),", "'placementChanges':list(changes.values()),'deletedSegments':deleted,")
p.write_text(s,encoding='utf8')
p=R/'scripts/plan_signal_paths.py';s=p.read_text(encoding='utf8')
s=s.replace("snapshot=load(args.snapshot);networks=load(args.networks);policy=load(args.policy);scene=CopperScene(snapshot,networks,load(args.rules),policy)","""snapshot=load(args.snapshot);networks=load(args.networks);policy=load(args.policy)
for op in policy.get('pendingDeleteSegments',[]):
 matches=[r for r in snapshot['routes'] if r['net']==op['net'] and r['layer']=='ETCH/'+op['layer'] and abs(r['width']-op['width'])<1e-6 and (r['startEnd']==op['points'] or r['startEnd']==list(reversed(op['points']))) ]
 assert len(matches)==1,('Future engineered ripup must uniquely match source copper',op)
 snapshot['routes'].remove(matches[0])
scene=CopperScene(snapshot,networks,load(args.rules),policy)""")
p.write_text(s,encoding='utf8');print('Unique explicit old-segment deletion supported in geometry only; no native execution')