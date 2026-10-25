from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
d=json.loads((R/'engineering_power/rules_profile_2L_69nets.json').read_text())
def q(x):return json.dumps(x,ensure_ascii=True)
def mm(v):return q(str(v)+' MM')
lines=['hiRegistry=nil','unless(equal(axlSubclassRoute() list("TOP" "BOTTOM")) error("2L profile on wrong board\\n"))']
# Remove exactly the old Region-Class entries, preserving the three original region shapes.
lines += ['oldRegion=car(setof(r axlDBGetDesign()->region equal(r->name "G31_U1_ESCAPE")))','unless(oldRegion error("Original G31 region missing\\n"))',
'oldTables=axlCnsClassTableFind(\'match oldRegion)','fprintf(f "OLD_G31_TABLES_REMOVED=%L\\n" oldTables)',
'when(oldTables unless(axlCnsClassTableDelete(oldTables) error("Cannot remove old G31 region associations\\n")))']
for g in d['groups']:
 p=g['physicalCSet'];sp=g['spacingCSet']
 lines.append('unless(axlCNSCreate(\'physical '+q(p)+' nil) error("Cannot create2L physical CSet\\n"))')
 for k in ['width_min','neckwidth_min','necklength_max']:
  lines.append('f29Must(axlCNSSetPhysical('+q(p)+' nil \''+k+' '+mm(g[k+'_mm'])+') "2L specific physical value")')
 lines.append('f29Must(axlCNSSetPhysical('+q(p)+' nil \'vias '+q(':'.join(g['viaList']))+') "Approved2L via")')
 for layer in ['TOP','BOTTOM']:
  lines.append('f29Must(axlCNSSetPhysical('+q(p)+' '+q(layer)+' \'allow_etch '+('t' if layer in g['allowed_layers'] else 'nil')+') "2L layer permission")')
 lines.append('unless(axlCNSCreate(\'spacing '+q(sp)+' nil) error("Cannot create2L spacing CSet\\n"))')
 for k,v in g['spacingFields_mm'].items():lines.append('f29Must(axlCNSSetSpacing('+q(sp)+' nil \''+k+' '+mm(v)+') "2L explicit spacing value")')
 for domain,cl,cs,prop in [('physical',g['physicalClass'],p,'PHYSICAL_CONSTRAINT_SET'),('spacing',g['spacingClass'],sp,'SPACING_CONSTRAINT_SET'),('electrical',g['electricalClass'],None,None)]:
  lines.append('nc=axlNetClassCreate('+q(cl)+' \''+domain+')')
  lines.append('unless(nc error("2L netclass create failed\\n"))')
  if prop:lines.append('axlDBAddProp(list(nc) list(list('+q(prop)+' '+q(cs)+')))')
  for net in g['nets']:
   lines += ['net=axlDBFindByName(\'net '+q(net)+')','old=axlNetClassGet(net \''+domain+' t)',
    'when(old fprintf(f "CLASS_REASSIGN net=%L domain=%L old=%L new=%L\\n" '+q(net)+' \''+domain+' old->name '+q(cl)+') unless(axlNetClassRemove(old net) error("Cannot remove prior class membership\\n")))',
    'unless(axlNetClassAdd(nc net) error("Cannot bind2L netclass member\\n"))']
 # Keep the two explicit net assignments, updating their values so the new class profile is not shadowed.
 for net in g['nets']:
  if net in ['GND','V3V3']:
   lines += ['net=axlDBFindByName(\'net '+q(net)+')','axlDBAddProp(list(net) list(list("PHYSICAL_CONSTRAINT_SET" '+q(p)+') list("SPACING_CONSTRAINT_SET" '+q(sp)+')))']
for old in ['G31_POWER_P','G31_GND_P']:
 lines.append('f29Must(axlNetClassDelete('+q(old)+') "Delete old empty G31 physical class")')
for gname in ['POWER_LV','GROUND']:
 for domain,prefix,field in [('physical','P','necklength_max'),('spacing','S',None)]:
  source='HI2L_'+prefix+'_'+gname;new='HI2L_'+prefix+'_MCU_ESCAPE_'+gname;cl='HI2L_'+gname+'_'+prefix
  lines.append('f29Must(axlCNSCreate(\''+domain+' '+q(new)+' '+q(source)+') "2L G31 copy template")')
  if domain=='physical':lines.append('f29Must(axlCNSSetPhysical('+q(new)+' nil \'necklength_max "1.4 MM") "MCU local native center neck")')
  else:
   for k in ['smdpin_line','line_line']:lines.append('f29Must(axlCNSSetSpacing('+q(new)+' nil \''+k+' "0.20 MM") "MCU local escape spacing")')
  lines.append('f29Must(axlCnsClassTableCreate('+q(cl)+' nil oldRegion \''+domain+' '+q(new)+') "Rebind G31 region to new class")')
for i,cc in enumerate(d['classClass']):
 name='HI2L_S_CLASSCLASS_'+str(i+1)
 lines.append('f29Must(axlCNSCreate(\'spacing '+q(name)+' nil) "2L class-class CSet")')
 for k in ['smdpin_line','line_line','via_line','line_shape','via_shape','shape_shape']:lines.append('f29Must(axlCNSSetSpacing('+q(name)+' nil \''+k+' '+mm(cc['spacing_mm'])+') "2L class-class copper isolation")')
 lines.append('f29Must(axlCnsClassTableCreate('+q('HI2L_'+cc['a']+'_S')+' '+q('HI2L_'+cc['b']+'_S')+' nil \'spacing '+q(name)+') "Spacing-domain class-class association")')
lines += ['f29Must(axlCNSEcsetCreate("HI2L_E_USB_BUDGET") "2L USB explicit ECSet")',
'f29Must(axlCNSEcsetValueSet("HI2L_E_USB_BUDGET" \'Maximum_Via_Count 2) "2L USB max via budget")',
'f29Must(axlCNSEcsetValueSet("HI2L_E_USB_BUDGET" \'Differential_Pair_Phase_Tolerance "1 MM") "2L USB phase teaching budget")',
'f29Must(axlCNSEcsetValueSet("HI2L_E_USB_BUDGET" \'Differential_Pair_Max_Uncoupled_Length "6 MM") "2L USB uncoupled teaching budget")']
for name,pos,neg in [('DP_USB_CONNECTOR','USB_DP','USB_DM'),('DP_USB_MCU_SIDE','PA12_SHARED','PA11_SHARED'),('DP_CAN_BUS','CAN_H','CAN_L')]:
 lines.append('pair=f29Must(axlDiffPair('+q(name)+' '+q(pos)+' '+q(neg)+') "2L native diff pair object")')
 if name.startswith('DP_USB'):lines.append('axlDBAddProp(list(pair) list(list("ELECTRICAL_CONSTRAINT_SET" "HI2L_E_USB_BUDGET")))')
lines += ['nc=car(setof(c axlDBGetDesign()->netclass equal(c->name "HI2L_USB_FS_E")))','axlDBAddProp(list(nc) list(list("ELECTRICAL_CONSTRAINT_SET" "HI2L_E_USB_BUDGET")))']
for k in ['dp_primary_gap','dp_neck_gap','dp_min_gap']:lines.append('f29Must(axlCNSSetPhysical("HI2L_P_USB_FS" nil \''+k+' "0.16 MM") "2L provisional differential geometry, not90ohm")')
lines += ['axlCNSPhysicalModeSet(\'width_min \'on)','axlCNSPhysicalModeSet(\'vias \'on)','axlCNSPhysicalModeSet(\'allow_etch \'on)','axlCNSSpacingModeSet(\'all \'on)','axlCNSEcsetModeSet(\'Maximum_Via_Count \'on)','axlCNSEcsetModeSet(\'Differential_Pair_Primary_Gap \'on)','axlCNSMapUpdate()',
'foreach(net axlDBGetDesign()->nets foreach(domain list(\'physical \'spacing \'electrical) unless(axlNetClassGet(net domain t) error("2L net fell back without class\\n"))))',
'fprintf(f "HI2L_ALL69_CLASSIFIED_IN3_DOMAINS\\n")',
'hiFinalize(f out board lib nil)','hiExtraRead(out)']
il='procedure(hi2LProfile(out board lib)\n let((f oldRegion oldTables nc old net pair)\n  f=outfile(strcat(out "/hi_2L_profile_execution.txt"))\n  '+ '\n  '.join(lines)+'\n  t))\n'
(R/'scripts/profile_2L_b001.il').write_text(il,encoding='ascii')
h=(R/'scripts/power_4L_b001.scr').read_text().split('skill errset(hiBatchProgram()')[0]
h+='skill errset(load("'+(R/'scripts/extraReadHI.il').as_posix()+'") t)\n'
h+='skill errset(load("'+(R/'scripts/profile_2L_b001.il').as_posix()+'") t)\n'
h+='skill errset(hi2LProfile("'+(R/'logs/profile_2L_b001').as_posix()+'" "'+(R/'native/HI_2L_PROFILE_b001.brd').as_posix()+'" "'+(R/'library').as_posix()+'") t)\nquit\nfillin "yes"\n'
(R/'scripts/profile_2L_b001.scr').write_text(h,encoding='ascii')
print('2L_NATIVE_PROFILE_PROGRAM_PREPARED',len(lines),'statements')
