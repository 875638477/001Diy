procedure(deInventory(lib out)
let((f p q r sym names i xy box pad poly)
axlDBChangeDesignUnits("millimeters" 3)
axlDBChangeDesignExtents(list(-30:-30 350:250))
axlSetVariable("psmpath" list(lib "D:/001DIY/005lib/01Psm_lib"))
axlSetVariable("padpath" list(lib "D:/001DIY/005lib/01Pad_lib"))
f=outfile(strcat(out "/pins.tsv"))
fprintf(f "package	pin	padstack	x	y	mechanical	layer	figure	w	h	drill	holeType	plating\n")
i=0
r=axlDBCreateSymbol(list("0603" "PACKAGE") 20:20 nil 0.0)
unless(r error("Cannot load 0603\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"0603" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("0805" "PACKAGE") 80:20 nil 0.0)
unless(r error("Cannot load 0805\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"0805" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("1206" "PACKAGE") 140:20 nil 0.0)
unless(r error("Cannot load 1206\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"1206" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("sot23-6" "PACKAGE") 200:20 nil 0.0)
unless(r error("Cannot load sot23-6\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"sot23-6" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("sot23-5" "PACKAGE") 260:20 nil 0.0)
unless(r error("Cannot load sot23-5\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"sot23-5" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("sot23-3" "PACKAGE") 20:70 nil 0.0)
unless(r error("Cannot load sot23-3\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"sot23-3" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("so8" "PACKAGE") 80:70 nil 0.0)
unless(r error("Cannot load so8\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"so8" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("do-214ac_sma" "PACKAGE") 140:70 nil 0.0)
unless(r error("Cannot load do-214ac_sma\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"do-214ac_sma" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("do-214aa_smb" "PACKAGE") 200:70 nil 0.0)
unless(r error("Cannot load do-214aa_smb\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"do-214aa_smb" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("L4018" "PACKAGE") 260:70 nil 0.0)
unless(r error("Cannot load L4018\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"L4018" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("HC-49SMD" "PACKAGE") 20:120 nil 0.0)
unless(r error("Cannot load HC-49SMD\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"HC-49SMD" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("xtal3225" "PACKAGE") 80:120 nil 0.0)
unless(r error("Cannot load xtal3225\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"xtal3225" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("pin02_2d54MM_1x2" "PACKAGE") 140:120 nil 0.0)
unless(r error("Cannot load pin02_2d54MM_1x2\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"pin02_2d54MM_1x2" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("pin03_2d54MM_1x3" "PACKAGE") 200:120 nil 0.0)
unless(r error("Cannot load pin03_2d54MM_1x3\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"pin03_2d54MM_1x3" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("pin04_2d54MM_1x4" "PACKAGE") 260:120 nil 0.0)
unless(r error("Cannot load pin04_2d54MM_1x4\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"pin04_2d54MM_1x4" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("pin06_2d54MM_1x6" "PACKAGE") 20:170 nil 0.0)
unless(r error("Cannot load pin06_2d54MM_1x6\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"pin06_2d54MM_1x6" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("pin08_2d54MM_1x8" "PACKAGE") 80:170 nil 0.0)
unless(r error("Cannot load pin08_2d54MM_1x8\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"pin08_2d54MM_1x8" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("sw_PB4_6x6" "PACKAGE") 140:170 nil 0.0)
unless(r error("Cannot load sw_PB4_6x6\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"sw_PB4_6x6" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("l09_stm32f103c8_lqfp48" "PACKAGE") 200:170 nil 0.0)
unless(r error("Cannot load l09_stm32f103c8_lqfp48\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"l09_stm32f103c8_lqfp48" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
r=axlDBCreateSymbol(list("l10_gct_usb4105_gf_a_12land" "PACKAGE") 260:170 nil 0.0)
unless(r error("Cannot load l10_gct_usb4105_gf_a_12land\n"))
sym=car(r)
foreach(p sym->pins
foreach(q list("ETCH/TOP" "ETCH/BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/PASTEMASK_TOP")
pad=axlDBGetPad(p q "REGULAR")
box=if(pad then pad->bBox else nil)
fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%s\t%L\t%L\t%L\t%L\t%L\t%L\n"
"l10_gct_usb4105_gf_a_12land" p->number p->name car(p->relxy) cadr(p->relxy) p->isMech q if(pad then pad->figureName else nil)
if(box then car(cadr(box))-car(car(box)) else nil) if(box then cadr(cadr(box))-cadr(car(box)) else nil)
p->definition->drillDiameter p->definition->holeType p->definition->plating))
i=i+1
close(f)
f=outfile(strcat(out "/summary.txt"))
fprintf(f "NATIVE_PSM_LOAD_COMPLETE packages=%d units=%L\n" i axlDBGetDesignUnits())
close(f)
unless(axlSaveDesign(?design "D:/001DIY/005lib/01AIEDA/learning/examples/de_15_26_20261019/dependencies_coupon.brd" ?noMru t ?noConfirm t) error("Save failed\n"))
t))
