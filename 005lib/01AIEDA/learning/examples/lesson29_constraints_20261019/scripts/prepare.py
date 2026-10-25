import pathlib,json,hashlib,datetime
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
for n in ['scripts','source','logs','native','exports','runtime']: (R/n).mkdir(parents=True,exist_ok=True)
D=pathlib.Path(r'C:\Program0\Cadence\SPB172')
files=[
'share/pcb/examples/skill/DOC/FUNCS/axlCNSCreate.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlCNSSetPhysical.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlCNSGetPhysical.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlCNSSetSpacing.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlCNSGetSpacing.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlNetClassCreate.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlNetClassAdd.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlNetClassGet.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlCnsClassTableCreate.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlDiffPair.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlCNSEcsetCreate.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlCNSEcsetValueSet.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlCNSEcsetValueGet.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlNetEcsetValueGet.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlCnsNetFlattened.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlCNSMapUpdate.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlDRCUpdate.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlDBCreatePadStack.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlDBCreateVia.txt',
'share/pcb/examples/skill/DOC/FUNCS/axlDBCreateLine.txt',
'doc/cmug/02objects.html','doc/cmug/03constraints.html',
'doc/cmref/file.html','doc/propref/properties.html','doc/tcoms/tchap.html']
items=[]
for n in files:
 p=D/n
 items.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,kind='installed_Cadence_17_2_primary_documentation'))
(R/'source/official_local_sources.json').write_text(json.dumps(items,indent=2),encoding='utf8')
S=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\de_15_26_20261019')
d=json.loads((S/'integrated_circuit.json').read_text())
members={}
for c in d['components']:
 for pin,net in c['pins'].items():
  if net: members.setdefault(net,[]).append(c['ref']+'.'+pin)
groups={
'POWER_INPUT':['VIN_RAW','VIN_FUSED','VIN_PROT'],
'POWER_LV':['V5','V3V3','VDDA','GND'],
'SWITCHING':['BUCK_SW','BUCK_BOOT'],
'ANALOG_SENSITIVE':['ADC0','ADC_IN','BUCK_FB'],
'OSCILLATOR':['OSC_IN','OSC_OUT','XTAL_OUT'],
'USB_FS':['USB_DP','USB_DM','PA11_SHARED','PA12_SHARED'],
'CAN_BUS':['CAN_H','CAN_L'],
'USB_AUX':['USB_VBUS','USB_CC1','USB_CC2'],
'DIGITAL_GENERAL':[]}
taken={x for v in groups.values() for x in v}
groups['DIGITAL_GENERAL']=sorted(set(members)-taken)
plan={'status':'PREPARATION_ONLY_NOT_YET_APPLIED','date':'2026-10-19 Asia/Shanghai','source':str(S/'integrated_circuit.json'),'sourceSHA256':hashlib.sha256((S/'integrated_circuit.json').read_bytes()).hexdigest(),'groups':groups,'net_members':members,
'assumptions':{'default_width_mm':.20,'default_spacing_mm':.20,'power_trunk_width_mm':.60,'power_spacing_mm':.30,'local_neck_width_mm':.20,'power_neck_max_mm':2.0,'signal_via_drill_mm':.30,'signal_via_copper_mm':.60,'USB_impedance_target_ohm':90,'USB_width_gap':'pending_lesson28_manufacturer_geometry_or_explicit_provisional','length_matching':'No arbitrary global match groups for UART/I2C/SPI/ADC/oscillator; USB policy to follow verified AN4879 and stackup.','current_budget':'150mA normal total V3V3 / Ta0-40C; input fuse500mA is not unrestricted current qualification','routing_scope':'Do not route whole board; controlled challenge geometry is transient and must be removed.'}}
assert len(set(x for v in groups.values() for x in v))==len(members)
(R/'constraint_plan_preparation.json').write_text(json.dumps(plan,indent=2),encoding='utf8')
print('PREPARATION_READY',len(members),'nets',len(groups),'classes',len(items),'official sources')
