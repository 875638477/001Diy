import pathlib,shutil,json
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
p=R/'scripts/build29.il';s=p.read_text()
a=s.index('procedure(f29Class(');b=s.index('procedure(f29DumpDRC',a)
s=s[:a]+r'''
procedure(f29Class(name nets pset sset)
 let((nc nn pname sname ename r)
  pname=strcat(name "_P") sname=strcat(name "_S") ename=strcat(name "_E")
  foreach(test list(list(pname 'physical) list(sname 'spacing) list(ename 'electrical))
   nc=f29Must(axlNetClassCreate(car(test) cadr(test)) car(test))
   foreach(n nets
    nn=f29Must(axlDBFindByName('net n) n)
    f29Must(axlNetClassAdd(nc nn) strcat(name "/" n))
    unless(equal(axlNetClassGet(nn cadr(test) nil) nc) error("Class-domain lookup failed\n"))))
  nc=axlNetClassGet(axlDBFindByName('net car(nets)) 'physical nil)
  r=axlDBAddProp(list(nc) list(list("PHYSICAL_CONSTRAINT_SET" pset)))
  unless(equal(cadr(assoc('PHYSICAL_CONSTRAINT_SET axlDBGetProperties(nc))) pset) error("Physical class reference not applied\n"))
  nc=axlNetClassGet(axlDBFindByName('net car(nets)) 'spacing nil)
  r=axlDBAddProp(list(nc) list(list("SPACING_CONSTRAINT_SET" sset)))
  unless(equal(cadr(assoc('SPACING_CONSTRAINT_SET axlDBGetProperties(nc))) sset) error("Spacing class reference not applied\n"))
  nc))
''' + s[b:]
s=s.replace('list("NC_ANALOG_SENSITIVE" "NC_OSCILLATOR" "NC_USB_FS")','list("NC_ANALOG_SENSITIVE_S" "NC_OSCILLATOR_S" "NC_USB_FS_S")')
s=s.replace('axlCnsClassTableCreate("NC_SWITCHING" c','axlCnsClassTableCreate("NC_SWITCHING_S" c')
s=s.replace('axlCnsClassTableCreate("NC_USB_FS" "NC_DIGITAL_GENERAL"','axlCnsClassTableCreate("NC_USB_FS_S" "NC_DIGITAL_GENERAL_S"')
# Preserve original source; only this new file is authoritative for v2.
(R/'scripts/build29_v2.il').write_text(s,encoding='ascii')
src=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019\native\F28_4L.brd')
dst=R/'native/F29_CONSTRAINTS_v2.brd';assert not dst.exists();shutil.copy2(src,dst)
log=R/'logs/build02';log.mkdir(exist_ok=True)
scr='set NOCONFIRM\nskill errset(load("'+(R/'scripts/build29_v2.il').as_posix()+'") t)\nskill errset(f29Build("'+dst.as_posix()+'" "'+log.as_posix()+'") t)\nquit\nfillin "yes"\n'
(R/'scripts/build02.scr').write_text(scr,encoding='ascii')
print('v2 prepared explicit single-domain classes')
