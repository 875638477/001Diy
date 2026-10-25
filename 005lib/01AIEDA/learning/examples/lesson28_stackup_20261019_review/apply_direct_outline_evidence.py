from pathlib import Path
O=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lesson28_stackup_20261019_review')
p=O/'review28.py';s=p.read_text();(O/'review28_before_direct_outline.py').write_text(s)
old=""" outline=[a for a in geom if a['layer']=='BOARD GEOMETRY/DESIGN_OUTLINE']
 ck(f'{n}L real outline persists',len(outline)==1 and outline[0]['bbox']==[[0,0],[80,60]])"""
new=""" md=B/'logs'/f'mech{n}_01'
 direct=table(md/'mechanical_direct.tsv')
 outline=[a for a in direct if a['layer']=='BOARD GEOMETRY/DESIGN_OUTLINE']
 expectedVertices=[[2,0],[78,0],[80,2],[80,58],[78,60],[2,60],[0,58],[0,2]]
 ck(f'{n}L real outline persists',len(outline)==1 and outline[0]['bbox']==[[0,0],[80,60]] and [a[0] for a in outline[0]['vertices']]==expectedVertices)
 roots=(md/'mechanical_roots.txt').read_text()
 ck(f'{n}L actual root outline and keepins recognized',all(t in roots for t in ['designOutline=t','keepinPlace=t','keepinRoute=t','L28_MECHANICAL_DIRECT COMPLETE']))
 ck(f'{n}L all explicit mechanical shapes match source',norm(rows(md/'mechanical_direct.tsv'))==norm(rows(B/'logs/mechbase01/mechanical_direct.tsv')))
 mr=json.loads((md/'launch.json').read_text())
 ck(f'{n}L explicit mechanical read process/hash stable',mr['completed'] and mr['exitCode']==0 and mr['readonlyHashUnchanged'] and sha(brd)==mr['afterSHA256'])
 reviewed += [md/'mechanical_direct.tsv',md/'mechanical_roots.txt',md/'launch.json']"""
assert old in s;s=s.replace(old,new)
s=s.replace("'reviewedFiles':[","'closedEvidenceGap':'Legacy fgeo map omits DESIGN_OUTLINE; explicit mechbase01/mech2_01/mech4_01 now prove actual outline/keepins and unchanged shapes.', 'stakeLengthErratum':'S=.95+/-.15mm measured from connector mounting/SMT datum, not finished board bottom. 1.6mm board assembly compatibility remains unqualified.', 'reviewedFiles':[")
p.write_text(s)
