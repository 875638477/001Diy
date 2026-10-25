from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
tag='void_pilot_4L_01'
out=(R/'logs'/tag).as_posix()
il=r'''
procedure(hiVoidPilot()
 let((f mark shapes)
  f=outfile("@OUT@/hi_permanent_void_pilot.txt")
  hiRegistry=nil
  axlDBRefreshId(nil)
  mark=axlDBTransactionStart()
  foreach(layer list("L2" "L3")
   hiBindExistingShape(f strcat("APP_" layer) "GND" layer)
   shapes=setof(s axlDBGetShapes(strcat("ETCH/" layer)) axlGeoPointInShape(26:46 s t))
   unless(shapes error("Pilot reference point not initially copper\n"))
   hiVoid(f strcat("APP_" layer) list(25:45 27:45 27:47 25:47))
   axlShapeDynamicUpdate(nil t) axlDBRefreshId(nil)
   shapes=setof(s axlDBGetShapes(strcat("ETCH/" layer)) axlGeoPointInShape(26:46 s t))
   fprintf(f "VOID_LAYER=%L copperAtVoid=%L\n" layer shapes)
   when(shapes error("Permanent void did not clear actual generated copper\n")))
  unless(axlDBTransactionRollback(mark) error("Cannot rollback permanent-void pilot\n"))
  axlShapeDynamicUpdate(nil t) axlDBRefreshId(nil)
  foreach(layer list("L2" "L3")
   shapes=setof(s axlDBGetShapes(strcat("ETCH/" layer)) axlGeoPointInShape(26:46 s t))
   fprintf(f "RESTORED_LAYER=%L actualCopper=%L\n" layer shapes)
   unless(shapes error("Void rollback did not restore actual copper\n")))
  axlDRCUpdate(t) f29DumpDRC(f "PERMANENT_VOID_PILOT_ROLLED_BACK")
  unless(length(axlDBGetDesign()->drcs)==0 error("Restored void pilot DRC count nonzero\n"))
  fprintf(f "HI_PERMANENT_VOID_PILOT_COMPLETE_NO_SAVE\n") close(f) t))
'''.replace('@OUT@',out)
p=R/f'scripts/{tag}.il';p.write_text(il,encoding='ascii')
s=(R/'scripts/reopen_power_4L_b002d.scr').read_text()
needle='skill errset(axlDRCUpdate(t) t)'
s=s[:s.index(needle)]
for name in ['batchHI_shapes_v3.il',f'{tag}.il']:
 s+='skill errset(load('+json.dumps((R/'scripts'/name).as_posix())+') t)\n'
s+='skill errset(hiVoidPilot() t)\nquit\nfillin "yes"\n'
(R/f'scripts/{tag}.scr').write_text(s,encoding='ascii')
print(tag)
