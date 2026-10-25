from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/batchHI_shapes_v3.il';s=p.read_text().replace('localLayer guardXY)','localLayer guardPoints)')
s=s.replace('  guard=hiResolvePoint("GND" "TOP" guardXY "point")\n  fprintf(f "NEGATIVE_LOCAL_REFERENCE count=%d guardReached=%L\\n" length(quietShape) if(member(guard graph) then t else nil))\n  unless(quietShape && member(guard graph) error("Local island or quiet guard disconnected in anchor-negative test\\n"))',
'''  unless(quietShape error("Local island disconnected in anchor-negative test\\n"))
  foreach(guardXY guardPoints
   guard=hiResolvePoint("GND" "TOP" guardXY "point")
   fprintf(f "NEGATIVE_LOCAL_REFERENCE count=%d guardXY=%L guardReached=%L\\n" length(quietShape) guardXY if(member(guard graph) then t else nil))
   unless(member(guard graph) error("Quiet guard disconnected in anchor-negative test\\n")))''')
p.write_text(s,encoding='ascii')
p=R/'scripts/compile_batchHI_v3.py';s=p.read_text().replace('{pt(check["guardXY"])}','{points(check["guardPoints"])}');p.write_text(s,encoding='ascii')
