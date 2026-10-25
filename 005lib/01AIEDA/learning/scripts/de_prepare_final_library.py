import pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1];BASE=ROOT/'examples/de_15_26_20261019';LIB=BASE/'library'
names=['0603','0805','1206','sot23-6','sot23-5','sot23-3','so8','do-214ac_sma','do-214aa_smb','pin02_2d54MM_1x2','pin03_2d54MM_1x3','pin04_2d54MM_1x4','pin06_2d54MM_1x6','pin08_2d54MM_1x8','l09_stm32f103c8_lqfp48','l10_gct_usb4105_gf_a_12land','de_abm3b_5032','de_capradial_6d3_p2d5','de_xal6060_2land']
(BASE/'selected_footprints.json').write_text(json.dumps({'count':len(names),'footprints':names,'isolatedNativeLoad':'pending'},indent=2),encoding='utf-8')
lines=['procedure(deFinalCreate(lib out)','let((r name i)','axlDBChangeDesignUnits("millimeters" 3)','axlDBChangeDesignExtents(list(-30:-30 350:250))','axlSetVariable("psmpath" list(lib))','axlSetVariable("padpath" list(lib))','i=0']
for n,name in enumerate(names):
    x=20+(n%5)*60;y=20+(n//5)*50
    lines += [f'r=axlDBCreateSymbol(list("{name}" "PACKAGE") {x}:{y} nil 0.0)',f'unless(r error("Isolated load failed {name}\\n"))','i=i+1']
lines += [f'unless(axlSaveDesign(?design "{(BASE/"dependencies_verified.brd").as_posix()}" ?noMru t ?noConfirm t) error("Save failed\\n"))','deDependencyRead(out)','printf("DE_FINAL_ISOLATED_CREATE_COMPLETE %d\\n" i)','t))']
il=ROOT/'scripts/de_final_library_create.il';il.write_text('\n'.join(lines)+'\n',encoding='ascii')
for mode in ['create','reopen']:
    log=ROOT/'staging/de_15_26_20261019'/('dependencies_final_'+mode);log.mkdir(exist_ok=True)
    lines=['set NOCONFIRM',f'skill errset(load("{(ROOT/"scripts/de_dependency_read.il").as_posix()}") t)']
    if mode=='create':lines += [f'skill errset(load("{il.as_posix()}") t)',f'skill errset(deFinalCreate("{LIB.as_posix()}" "{log.as_posix()}") t)']
    else:lines += [f'skill errset(deDependencyRead("{log.as_posix()} ") t)'.replace(' ")','")')]
    lines+=['quit','fillin "yes"']
    (ROOT/'scripts'/('de_final_library_'+mode+'.scr')).write_text('\n'.join(lines)+'\n',encoding='ascii')
print('Prepared final isolated library:',len(names),'packages')
