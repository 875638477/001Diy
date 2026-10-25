procedure(deFinalCreate(lib out)
let((r name i)
axlDBChangeDesignUnits("millimeters" 3)
axlDBChangeDesignExtents(list(-30:-30 350:250))
axlSetVariable("psmpath" list(lib))
axlSetVariable("padpath" list(lib))
i=0
r=axlDBCreateSymbol(list("0603" "PACKAGE") 20:20 nil 0.0)
unless(r error("Isolated load failed 0603\n"))
i=i+1
r=axlDBCreateSymbol(list("0805" "PACKAGE") 80:20 nil 0.0)
unless(r error("Isolated load failed 0805\n"))
i=i+1
r=axlDBCreateSymbol(list("1206" "PACKAGE") 140:20 nil 0.0)
unless(r error("Isolated load failed 1206\n"))
i=i+1
r=axlDBCreateSymbol(list("sot23-6" "PACKAGE") 200:20 nil 0.0)
unless(r error("Isolated load failed sot23-6\n"))
i=i+1
r=axlDBCreateSymbol(list("sot23-5" "PACKAGE") 260:20 nil 0.0)
unless(r error("Isolated load failed sot23-5\n"))
i=i+1
r=axlDBCreateSymbol(list("sot23-3" "PACKAGE") 20:70 nil 0.0)
unless(r error("Isolated load failed sot23-3\n"))
i=i+1
r=axlDBCreateSymbol(list("so8" "PACKAGE") 80:70 nil 0.0)
unless(r error("Isolated load failed so8\n"))
i=i+1
r=axlDBCreateSymbol(list("do-214ac_sma" "PACKAGE") 140:70 nil 0.0)
unless(r error("Isolated load failed do-214ac_sma\n"))
i=i+1
r=axlDBCreateSymbol(list("do-214aa_smb" "PACKAGE") 200:70 nil 0.0)
unless(r error("Isolated load failed do-214aa_smb\n"))
i=i+1
r=axlDBCreateSymbol(list("pin02_2d54MM_1x2" "PACKAGE") 260:70 nil 0.0)
unless(r error("Isolated load failed pin02_2d54MM_1x2\n"))
i=i+1
r=axlDBCreateSymbol(list("pin03_2d54MM_1x3" "PACKAGE") 20:120 nil 0.0)
unless(r error("Isolated load failed pin03_2d54MM_1x3\n"))
i=i+1
r=axlDBCreateSymbol(list("pin04_2d54MM_1x4" "PACKAGE") 80:120 nil 0.0)
unless(r error("Isolated load failed pin04_2d54MM_1x4\n"))
i=i+1
r=axlDBCreateSymbol(list("pin06_2d54MM_1x6" "PACKAGE") 140:120 nil 0.0)
unless(r error("Isolated load failed pin06_2d54MM_1x6\n"))
i=i+1
r=axlDBCreateSymbol(list("pin08_2d54MM_1x8" "PACKAGE") 200:120 nil 0.0)
unless(r error("Isolated load failed pin08_2d54MM_1x8\n"))
i=i+1
r=axlDBCreateSymbol(list("l09_stm32f103c8_lqfp48" "PACKAGE") 260:120 nil 0.0)
unless(r error("Isolated load failed l09_stm32f103c8_lqfp48\n"))
i=i+1
r=axlDBCreateSymbol(list("l10_gct_usb4105_gf_a_12land" "PACKAGE") 20:170 nil 0.0)
unless(r error("Isolated load failed l10_gct_usb4105_gf_a_12land\n"))
i=i+1
r=axlDBCreateSymbol(list("de_abm3b_5032" "PACKAGE") 80:170 nil 0.0)
unless(r error("Isolated load failed de_abm3b_5032\n"))
i=i+1
r=axlDBCreateSymbol(list("de_capradial_6d3_p2d5" "PACKAGE") 140:170 nil 0.0)
unless(r error("Isolated load failed de_capradial_6d3_p2d5\n"))
i=i+1
r=axlDBCreateSymbol(list("de_xal6060_2land" "PACKAGE") 200:170 nil 0.0)
unless(r error("Isolated load failed de_xal6060_2land\n"))
i=i+1
unless(axlSaveDesign(?design "D:/001DIY/005lib/01AIEDA/learning/examples/de_15_26_20261019/dependencies_verified.brd" ?noMru t ?noConfirm t) error("Save failed\n"))
deDependencyRead(out)
printf("DE_FINAL_ISOLATED_CREATE_COMPLETE %d\n" i)
t))
