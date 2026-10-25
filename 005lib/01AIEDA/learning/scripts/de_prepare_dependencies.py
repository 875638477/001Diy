"""Copy unchanged learning/library candidates; native board load determines usability."""
import pathlib,shutil,json,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/'examples/de_15_26_20261019'
LIB=BASE/'library';LIB.mkdir(parents=True,exist_ok=True)
PUBLIC=ROOT.parents[1]/'01Psm_lib'
names=['0603','0805','1206','sot23-6','sot23-5','sot23-3','so8','do-214ac_sma','do-214aa_smb','L4018','HC-49SMD','xtal3225','pin02_2d54MM_1x2','pin03_2d54MM_1x3','pin04_2d54MM_1x4','pin06_2d54MM_1x6','pin08_2d54MM_1x8','sw_PB4_6x6']
entries=[]
def copy(src):
    dst=LIB/src.name
    if not dst.exists():shutil.copy2(src,dst)
    assert src.read_bytes()==dst.read_bytes()
    entries.append({'source':str(src),'destination':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
for name in names:
    for ext in ['.dra','.psm']:copy(PUBLIC/(name+ext))
for folder,name in [('lesson09_qfn_qfp_20261018','l09_stm32f103c8_lqfp48'),('lesson10_connector_20261018','l10_gct_usb4105_gf_a_12land')]:
    source=ROOT/'examples'/folder/'library'
    for ext in ['.dra','.psm']:copy(source/(name+ext))
    for src in source.glob('*.pad'):copy(src)
names+=['l09_stm32f103c8_lqfp48','l10_gct_usb4105_gf_a_12land']
(BASE/'dependency_copy_manifest.json').write_text(json.dumps({'files':entries,'native_verification':'pending'},indent=2),encoding='utf-8')
lines=['procedure(deInventory(lib out)','let((f p q r sym names i xy box pad poly)','axlDBChangeDesignUnits("millimeters" 3)','axlDBChangeDesignExtents(list(-30:-30 350:250))',f'axlSetVariable("psmpath" list(lib "{PUBLIC.as_posix()}"))',f'axlSetVariable("padpath" list(lib "{(PUBLIC.parent/"01Pad_lib").as_posix()}"))','f=outfile(strcat(out "/pins.tsv"))','fprintf(f "package\tpin\tpadstack\tx\ty\tmechanical\tlayer\tfigure\tw\th\tdrill\tholeType\tplating\\n")','i=0']
for n,name in enumerate(names):
    x=20+(n%5)*60;y=20+(n//5)*50
    lines += [f'r=axlDBCreateSymbol(list("{name}" "PACKAGE") {x}:{y} nil 0.0)',f'unless(r error("Cannot load {name}\\n"))','sym=car(r)','foreach(p sym->pins','foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")','pad=axlDBGetPad(p q "REGULAR")','box=if(pad then pad->bBox else nil)','fprintf(f "%s\\t%L\\t%L\\t%L\\t%L\\t%L\\t%s\\t%L\\t%L\\t%L\\t%L\\t%L\\t%L\\n"',f'"{name}" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)','if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)','p->definition->drillDiameter p->definition->holeType p->definition->plating)))','i=i+1']
lines+=['close(f)','f=outfile(strcat(out "/summary.txt"))','fprintf(f "NATIVE_PSM_LOAD_COMPLETE packages=%d units=%L\\n" i axlDBGetDesignUnits())','close(f)',f'unless(axlSaveDesign(?design "{(BASE/"dependencies_coupon02.brd").as_posix()}" ?noMru t ?noConfirm t) error("Save failed\\n"))','t))']
il=ROOT/'scripts/de_dependency_inventory.il';il.write_text('\n'.join(lines)+'\n',encoding='ascii')
log=ROOT/'staging/de_15_26_20261019/dependency_load02';log.mkdir(parents=True,exist_ok=True)
scr=ROOT/'scripts/de_dependency_inventory.scr';scr.write_text('set NOCONFIRM\nskill errset(load("'+il.as_posix()+'") t)\nskill errset(deInventory("'+LIB.as_posix()+'" "'+log.as_posix()+'") t)\nquit\nfillin "yes"\n',encoding='ascii')
print(json.dumps({'candidates':names,'script':str(scr),'library':str(LIB)},indent=2))
