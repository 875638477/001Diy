from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/prepare_readbackHI_v2.py').read_text().replace("R/'scripts/batchHI_extended.il',R/'scripts/extraReadHI.il'","R/'scripts/batchHI_extended.il',R/'scripts/batchHI_shapes_v3.il',R/'scripts/extraReadHI.il'")
s=s.replace("h+='skill errset(hiExtraRead(\"'+out+'\") t)\\n'","h+='skill errset(hiExtraRead(\"'+out+'\") t)\\n'\nh+='skill errset(hiShapeBoundaryRead(\"'+out+'\") t)\\n'")
needle=" for op in d.get('operations',[]):\n  if op['type']=='via':"
replace=""" for op in d.get('operations',[]):
  if op['type']=='shape':
   fn='hiBindExistingShape' if op.get('dynamic') else 'hiBindExistingStaticShape'
   il+='  '+fn+'(f '+json.dumps(op['id'])+' '+json.dumps(op['net'])+' '+json.dumps(op['layer'])+')\\n'
 for op in d.get('operations',[]):
  if op['type']=='via':"""
assert needle in s;s=s.replace(needle,replace)
needle=" il+='  fprintf(f \"HI_REOPEN_ALL_ENDPOINTS_COMPLETE"
start=s.index(needle)
s=s[:start]+""" for p in d.get('proofs',[]):
  il+='  hiProof(f '+json.dumps(p['from'])+' '+json.dumps(p['to'])+' '+('t' if p.get('connected',True) else 'nil')+')\\n'
 for p in d.get('postChecks',[]):
  if p['type']=='hseIsolation':
   il+='  hiHSEIsolationChallenge('+json.dumps(out)+' '+pt(p['anchorXY'])+' '+json.dumps(p['localLayer'])+' list('+' '.join(pt(x) for x in p['guardPoints'])+'))\\n'
  else:raise ValueError(p['type'])
"""+s[start:]
(R/'scripts/prepare_readbackHI_v3.py').write_text(s,encoding='ascii')
print('prepared shape/guard/isolation readback v3')
