import pathlib,json,hashlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
d=json.loads((R/'constraint_plan_preparation.json').read_text())
classes={
'POWER_INPUT':('P_POWER_060','S_POWER_030'),
'POWER_LV':('P_POWER_060','S_POWER_030'),
'SWITCHING':('P_SWITCH_060','S_POWER_030'),
'ANALOG_SENSITIVE':('P_ANALOG_020','S_ANALOG_030'),
'OSCILLATOR':('P_OSC_020','S_ANALOG_030'),
'USB_FS':('P_USB_PROVISIONAL','S_USB_015'),
'CAN_BUS':('P_CAN_025','S_CAN_025'),
'USB_AUX':('P_SIGNAL_020','DEFAULT'),
'DIGITAL_GENERAL':('P_SIGNAL_020','DEFAULT')}
src=r'''
; Lesson29: real Constraint Manager database using published axlCNS/NetClass interfaces.
procedure(f29Must(ret label)
 unless(ret error("F29 operation failed: %s\n" label))
 ret)
procedure(f29Setup()
 axlSetVariable("padpath" list("D:/001DIY/005lib/01AIEDA/learning/examples/lesson28_stackup_20261019/native" "D:/001DIY/005lib/01AIEDA/learning/examples/de_15_26_20261019/library"))
 axlSetVariable("psmpath" list("D:/001DIY/005lib/01AIEDA/learning/examples/de_15_26_20261019/library")))
procedure(f29Phys(name width neck necklen)
 f29Must(axlCNSCreate('physical name nil) name)
 foreach(v list(list('width_min width) list('neckwidth_min neck) list('necklength_max necklen) list('vias "L28_VIA030_C060"))
  f29Must(axlCNSSetPhysical(name nil car(v) cadr(v)) strcat(name "/physical")))
)
procedure(f29Space(name gap)
 f29Must(axlCNSCreate('spacing name nil) name)
 foreach(k list('line_line 'line_shape 'shape_shape 'smdpin_line 'thrupin_line 'via_line 'via_shape)
  f29Must(axlCNSSetSpacing(name nil k gap) strcat(name "/spacing")))
)
procedure(f29Class(name nets pset sset)
 let((nc nn)
  nc=f29Must(axlNetClassCreate(name 'all) name)
  foreach(n nets
   nn=f29Must(axlDBFindByName('net n) n)
   f29Must(axlNetClassAdd(nc nn) strcat(name "/" n)))
  f29Must(axlDBAddProp(nc list("PHYSICAL_CONSTRAINT_SET" pset "SPACING_CONSTRAINT_SET" sset)) name)
  nc))
procedure(f29DumpDRC(f label)
 axlDBRefreshId(nil)
 fprintf(f "DRC_STATUS\t%s\t%d\t%L\n" label length(axlDBGetDesign()->drcs) axlDBGetDesign()->drcState)
 foreach(x axlDBGetDesign()->drcs fprintf(f "DRC_DETAIL\t%s\t%L\n" label x->??)))
procedure(f29Build(board out)
 let((f des net pair class ctable)
  f29Setup()
  f=outfile(strcat(out "/build.txt"))
  des=axlDBGetDesign()
  fprintf(f "START units=%L layers=%L components=%d nets=%d symbols=%d\n" axlDBGetDesignUnits() axlSubclassRoute() length(des->components) length(des->nets) length(des->symbols))
  unless(equal(axlSubclassRoute() list("TOP" "L2" "L3" "BOTTOM")) error("Expected approved named4layer board\n"))
  unless(length(des->components)==80 && length(des->nets)==69 error("Unexpected source connectivity\n"))
  axlCNSMapClear()
  f29Must(axlCNSSetPhysical("" nil 'width_min "0.20 MM") "default width")
  f29Must(axlCNSSetPhysical("" nil 'neckwidth_min "0.15 MM") "default neck")
  f29Must(axlCNSSetPhysical("" nil 'necklength_max "1 MM") "default neck length")
  f29Must(axlCNSSetPhysical("" nil 'vias "L28_VIA030_C060") "default via")
  foreach(k axlCNSGetSpacing(nil nil nil)
   unless(member(k list('bbvia_gap 'hole_via 'hole_thrupin 'hole_hole 'hole_shape 'hole_line))
    f29Must(axlCNSSetSpacing("" nil k "0.20 MM") "default copper spacing")))
  f29Phys("P_SIGNAL_020" "0.20 MM" "0.15 MM" "1 MM")
  f29Phys("P_POWER_060" "0.60 MM" "0.25 MM" "1 MM")
  f29Phys("P_SWITCH_060" "0.60 MM" "0.25 MM" "1 MM")
  f29Phys("P_ANALOG_020" "0.20 MM" "0.15 MM" "1 MM")
  f29Phys("P_OSC_020" "0.20 MM" "0.15 MM" "1 MM")
  f29Phys("P_USB_PROVISIONAL" "0.20 MM" "0.15 MM" "1 MM")
  f29Phys("P_CAN_025" "0.25 MM" "0.20 MM" "1 MM")
  f29Phys("P_VDDA_030" "0.30 MM" "0.20 MM" "1 MM")
  f29Space("S_POWER_030" "0.30 MM")
  f29Space("S_ANALOG_030" "0.30 MM")
  f29Space("S_USB_015" "0.15 MM")
  f29Space("S_CAN_025" "0.25 MM")
  f29Space("S_ISOLATE_100" "1 MM")
  f29Space("S_USB_OTHER_050" "0.50 MM")
  foreach(c axlCnsList('physical)
   unless(equal(c "P_POWER_060")
    foreach(l list("L2" "L3") f29Must(axlCNSSetPhysical(c l 'allow_etch nil) "inner signal prohibition"))))
  ; USB only TOP during this prelayout course, adjacent reference is L2 GND.
  f29Must(axlCNSSetPhysical("P_USB_PROVISIONAL" "BOTTOM" 'allow_etch nil) "USB top only")
  foreach(k list('dp_primary_gap 'dp_min_gap 'dp_neck_gap)
   f29Must(axlCNSSetPhysical("P_USB_PROVISIONAL" "TOP" k "0.15 MM") "USB provisional gap"))
'''
for name,(p,s) in classes.items():
 nets=' '.join('"'+n+'"' for n in d['groups'][name])
 src+=f'  f29Class("NC_{name}" list({nets}) "{p}" "{s}")\n'
src+=r'''
  net=f29Must(axlDBFindByName('net "VDDA") "VDDA")
  f29Must(axlDBAddProp(net list("PHYSICAL_CONSTRAINT_SET" "P_VDDA_030")) "VDDA branch exception")
  foreach(c list("NC_ANALOG_SENSITIVE" "NC_OSCILLATOR" "NC_USB_FS")
   ctable=f29Must(axlCnsClassTableCreate("NC_SWITCHING" c nil 'spacing "S_ISOLATE_100") "switch isolation class table"))
  f29Must(axlCnsClassTableCreate("NC_USB_FS" "NC_DIGITAL_GENERAL" nil 'spacing "S_USB_OTHER_050") "USB signal isolation")
  ; Pair1 is connector/ESD to R5/6, Pair2 is R5/6 to MCU plus DNP CAN branches.
  pair=f29Must(axlDiffPair("DP_USB_CONNECTOR" "USB_DP" "USB_DM") "USB connector pair")
  pair=f29Must(axlDiffPair("DP_USB_MCU_SIDE" "PA12_SHARED" "PA11_SHARED") "USB MCU side pair")
  pair=f29Must(axlDiffPair("DP_CAN_BUS" "CAN_H" "CAN_L") "CAN routing pair")
  f29Must(axlCNSEcsetCreate("E_USB_FS_BUDGET") "USB ECSet")
  f29Must(axlCNSEcsetValueSet("E_USB_FS_BUDGET" 'Maximum_Via_Count 2) "USB max2 via per net")
  ; 1mm static skew is explicit project teaching budget, not F103/USB hard limit.
  f29Must(axlCNSEcsetValueSet("E_USB_FS_BUDGET" 'Differential_Pair_Phase_Tolerance "1 MM") "USB phase budget")
  f29Must(axlCNSEcsetValueSet("E_USB_FS_BUDGET" 'Differential_Pair_Max_Uncoupled_Length "6 MM") "USB breakout budget")
  foreach(n list("DP_USB_CONNECTOR" "DP_USB_MCU_SIDE")
   pair=f29Must(axlDiffPairDBID(n) n)
   f29Must(axlDBAddProp(pair list("ELECTRICAL_CONSTRAINT_SET" "E_USB_FS_BUDGET")) "pair ECSet reference"))
  f29Must(axlCNSPhysicalModeSet('vias 'on) "enable approved-via DRC")
  f29Must(axlCNSPhysicalModeSet('width_min 'on) "enable width")
  f29Must(axlCNSPhysicalModeSet('allow_etch 'on) "enable layer")
  f29Must(axlCNSSpacingModeSet('all 'on) "enable spacing")
  f29Must(axlCNSEcsetModeSet('Maximum_Via_Count 'on) "enable maxvia")
  f29Must(axlCNSEcsetModeSet('Differential_Pair_Primary_Gap 'on) "enable DP checks")
  fprintf(f "MAP_UPDATE=%L\n" axlCNSMapUpdate())
  fprintf(f "DRC_UPDATE=%L\n" axlDRCUpdate(t))
  f29DumpDRC(f "FINAL_BASE")
  unless(axlSaveDesign(?design board ?noMru t ?noConfirm t) error("Save constraints failed\n"))
  fprintf(f "BUILD_COMPLETE\n") close(f) t))
'''
(R/'scripts/build29.il').write_text(src,encoding='ascii')
d['native_classes']={n:dict(physical=p,spacing=s,members=d['groups'][n]) for n,(p,s) in classes.items()}
d['status']='PREPARED_NATIVE_PROGRAM_NOT_YET_APPLIED'
d['exceptions']={'VDDA':{'physical_cset':'P_VDDA_030','reason':'Analog supply branch0.30mm instead of0.60mm distribution class'} }
d['USB_basis_correction']='DE22R is historical unverified engineering value, not a found DS5319/AN4879 requirement. Preserve existing schematic identity in this lesson; assess0R/jumper or measured value before final layout/release.'
d['USB_preliminary_geometry']={'width_mm':.2,'gap_mm':.15,'neck_mm':.15,'neck_length_mm':1,'status':'PROVISIONAL_NOT_90OHM_VERIFIED','reference':'TOP over continuous L2 GND; h0.2104mm,outerCu0.035,Dk4.4 selected in lesson28; manufacturer geometry pending'}
d['USB_budget']={'phase_tolerance_mm':1,'max_uncoupled_mm':6,'max_vias_per_net':2,'source':'Explicit teaching/project allocation. Not a mandatory F103/USB specification. Do not add serpentine until whole path and return are reviewed.'}
(R/'constraint_spec.json').write_text(json.dumps(d,indent=2),encoding='utf8')
print('BUILD29_PREPARED')
