import pathlib
p=pathlib.Path(__file__).parent/'review_candidate_paths.py';s=p.read_text(encoding='utf8')
old="changes={}\ndeleted=[]"
new="""changes={}
deleted=[]
replacementQuiet=[]
for plan in plans:
 rework=plan.get('oscillatorReferenceRework')
 if not rework:continue
 sourceLayer=rework['source']['localLayer'][snapshot['variant']]
 matches=[p for p in snapshot['planes'] if p['net']=='GND' and p['layer']=='ETCH/'+sourceLayer and p.get('filled') and not p.get('generated')]
 assert len(matches)==1,'Source quiet static shape must be uniquely identified'
 snapshot['planes'].remove(matches[0]);deleted.append({'oldQuietShape':matches[0],'replacementFromPlan':plan.get('batchId')})
 replacementQuiet.append({'type':'shape','id':'FUTURE_HSE_QUIET_STATIC','net':'GND','layer':sourceLayer,'polygon':rework['islandPolygon'],'dynamic':False})
"""
assert old in s;s=s.replace(old,new).replace("issues=[];checked=0;opN=0", "for op in replacementQuiet:scene.add_operation(op)\nissues=[];checked=0;opN=0")
p.write_text(s,encoding='utf8')
p=pathlib.Path(__file__).parent/'plan_signal_paths.py';s=p.read_text(encoding='utf8')
needle="for op in policy.get('pendingDeleteSegments',[]):"
insert="""for rework in policy.get('pendingQuietReworks',[]):
 sourceLayer=rework['source']['localLayer'][snapshot['variant']]
 matches=[p for p in snapshot['planes'] if p['net']=='GND' and p['layer']=='ETCH/'+sourceLayer and p.get('filled') and not p.get('generated')]
 assert len(matches)==1,'Future quiet replacement must match one native source island'
 snapshot['planes'].remove(matches[0])
 policy.setdefault('pendingOperations',[]).append({'type':'shape','id':'FUTURE_QUIET_REFERENCE','net':'GND','layer':sourceLayer,'polygon':rework['islandPolygon'],'dynamic':False})
"""
assert needle in s;s=s.replace(needle,insert+needle)
p.write_text(s,encoding='utf8')