import pathlib,shutil
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
src=R/'native/F29_CONSTRAINTS_v2.brd';dst=R/'native/F29_CONSTRAINTS_v3.brd';assert not dst.exists();shutil.copy2(src,dst)
il=r'''
procedure(f29PatchGround(board out)
 let((f net c)
  f=outfile(out)
  f29Phys("P_GND_PLANE" "0.60 MM" "0.25 MM" "1 MM")
  foreach(c axlCnsList('physical)
   foreach(l list("L2" "L3")
    if(equal(c "P_GND_PLANE") then
     f29Must(axlCNSSetPhysical(c l 'allow_etch t) "GND layer copper/connection")
    else
     f29Must(axlCNSSetPhysical(c l 'allow_etch nil) "no signal or power cline in GND layers"))))
  net=axlDBFindByName('net "GND")
  axlDBAddProp(list(net) list(list("PHYSICAL_CONSTRAINT_SET" "P_GND_PLANE")))
  fprintf(f "GND_EXCEPTION=%L\n" axlDBGetProperties(net))
  unless(equal(cadr(assoc('PHYSICAL_CONSTRAINT_SET axlDBGetProperties(net))) "P_GND_PLANE") error("GND override failed\n"))
  fprintf(f "UPDATE=%L\n" axlDRCUpdate(t)) f29DumpDRC(f "FINAL_PATCHED")
  f29Must(axlSaveDesign(?design board ?noMru t ?noConfirm t) "final3save")
  fprintf(f "GROUND_PATCH_COMPLETE\n") close(f) t))
'''
(R/'scripts/ground_patch.il').write_text(il,encoding='ascii')
p=R.as_posix()
(R/'scripts/patch03.scr').write_text(f'set NOCONFIRM\nskill errset(load("{p}/scripts/build29_v2.il") t)\nskill errset(load("{p}/scripts/ground_patch.il") t)\nskill errset(f29PatchGround("{p}/native/F29_CONSTRAINTS_v3.brd" "{p}/logs/ground_patch.txt") t)\nquit\nfillin "yes"\n',encoding='ascii')
s=(R/'scripts/challenges29_v3.il').read_text().replace('30:27 "GND"','30:27 "V5"').replace('0.30 "GND"','0.30 "V5"').replace("axlDBFindByName('net \"GND\")","axlDBFindByName('net \"V5\")")
s=s.replace('  fprintf(f "FINAL_DRC=',r'''
  mark=f29ChallengeBegin(f "L2_POWER_BLOCKED")
  f29Via("L28_VIA030_C060" 30:24 "V3V3")
  f29Must(axlDBCreateLine(list(30:24 40:24) 0.60 "ETCH/L2" "V3V3" nil) "temporary inner power line")
  f29ChallengeEnd(f mark "L2_POWER_BLOCKED")
  mark=f29ChallengeBegin(f "L2_GND_SHAPE_ALLOWED")
  obj=car(f29Must(axlDBCreateRectangle(list(30:24 40:26) t "ETCH/L2" "GND" nil) "temporary GND plane"))
  f29Must(axlDBAssignNet(obj "GND" nil nil) "temporary GND plane net")
  fprintf(f "SHAPE_NET=%L LAYER=%L\n" obj->net->name obj->layer)
  f29ChallengeEnd(f mark "L2_GND_SHAPE_ALLOWED")
  fprintf(f "FINAL_DRC=''')
(R/'scripts/challenges29_v4.il').write_text(s,encoding='ascii')
(R/'scripts/challenge04.scr').write_text(f'set NOCONFIRM\nskill errset(load("{p}/scripts/build29_v2.il") t)\nskill errset(load("{p}/scripts/challenges29_v4.il") t)\nskill errset(f29Challenges("{p}/logs/challenge04") t)\nquit\nfillin "yes"\n',encoding='ascii')
# Final read scripts reuse independently loaded read helpers.
for kind,board in [('final','F29_CONSTRAINTS_v3.brd'),('coupon','F29_PHASE_COUPON.brd')]:
 scr=f'set NOCONFIRM\nskill errset(load("D:/001DIY/005lib/01AIEDA/learning/scripts/de_board_read.il") t)\nskill errset(load("{p}/scripts/build29_v2.il") t)\nskill errset(load("{p}/scripts/read29.il") t)\nskill errset(load("{p}/scripts/extra_read29.il") t)\nskill errset(f29Read("{p}/logs/read_{kind}") t)\nskill errset(f29ExtraRead("{p}/logs/read_{kind}") t)\nquit\nfillin "yes"\n'
 (R/f'scripts/read_{kind}.scr').write_text(scr,encoding='ascii')
print('GROUND_PATCH_AND_FINAL_CHECKS_PREPARED')
