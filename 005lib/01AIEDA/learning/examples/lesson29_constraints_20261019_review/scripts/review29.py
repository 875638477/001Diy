from pathlib import Path
import csv,json,re,hashlib,collections,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019_review')
A=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
F=A/'logs'/'read_final02'
def table(p):return list(csv.DictReader(p.open(encoding='utf-8'),delimiter='\t',quoting=csv.QUOTE_NONE))
def q(s):return s[1:-1] if s.startswith('"') and s.endswith('"') else s
def attrs(s):return {m[1]:q(m[2].strip()) for m in re.finditer(r'\(([a-zA-Z_]+)\s+([^()]*)\)',s)}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
baseline=json.loads((R/'baseline_connectivity.json').read_text())
checks=[]
def ck(name,ok,detail=None):checks.append({'check':name,'pass':bool(ok),'detail':detail})
def eq(name,a,b):ck(name,a==b,{'actual':a,'expected':b})
expectedSHA='6276201EF1750D3A318D901CCF1ADFBB1CA41A4301329CD21E32A0E22B3FA607'
eq('Final native board identity',sha(A/'native'/'F29_CONSTRAINTS_v3.brd'),expectedSHA)
for tag in ['read_final02','challenge04']:
 rec=json.loads((A/'logs'/tag/'launch.json').read_text())
 ck(tag+' completed exit0',rec['completed'] and rec['exitCode']==0)
 eq(tag+' input expected SHA',rec['beforeSHA256'],expectedSHA)
 eq(tag+' no on-disk mutation',rec['afterSHA256'],expectedSHA)
comp=table(F/'components.tsv')
eq('80 logical components retained',len(comp),80)
eq('272 physical pin identities retained',sum(int(c['pins']) for c in comp),272)
bc=table(Path(baseline['source'])/'components.tsv')
eq('Component name/package/device identity unchanged',sorted((c['refdes'],c['package'],c['deviceType'],int(c['pins'])) for c in comp),sorted((q(c['refdes']),q(c['package']),q(c['device_type']),int(c['pins'])) for c in bc))
actual={}
for r in table(F/'component_pins.tsv'):actual[(r['refdes'],r['pin'])]=r['net'] or 'nil'
expect={tuple(p):(net if net not in ('','nil') else 'nil') for net,pins in baseline['nets'].items() for p in pins}
eq('272 original pin-to-net connections including six NC unchanged',actual,expect)
rules=table(F/'net_rules.tsv')
eq('Exactly 69 actual net rules',len(rules),69)
eq('Net names unchanged',sorted(r['net'] for r in rules),sorted(k for k in baseline['nets'] if k not in ('','nil')))
members=table(F/'group_members.tsv');gmap=collections.defaultdict(set);gflags={}
for r in members:
 gmap[r['group']].add(q(r['member']))
 flag=(q(r['groupType']),r['physical'],r['spacing'],r['electrical'])
 ck('Group domain stable '+r['group'],r['group'] not in gflags or gflags[r['group']]==flag)
 gflags[r['group']]=flag
groups={
'POWER_INPUT':{'VIN_RAW','VIN_FUSED','VIN_PROT'},'POWER_LV':{'V5','V3V3','VDDA','GND'},'SWITCHING':{'BUCK_SW','BUCK_BOOT'},'ANALOG_SENSITIVE':{'ADC0','ADC_IN','BUCK_FB'},'OSCILLATOR':{'OSC_IN','OSC_OUT','XTAL_OUT'},'USB_FS':{'USB_DP','USB_DM','PA11_SHARED','PA12_SHARED'},'CAN_BUS':{'CAN_H','CAN_L'},'USB_AUX':{'USB_VBUS','USB_CC1','USB_CC2'}}
groups['DIGITAL_GENERAL']=set(r['net'] for r in rules)-set().union(*groups.values())
domain={'P':('physicalClass',('NETCLASS','t','nil','nil')),'S':('spacingClass',('NETCLASS','nil','t','nil')),'E':('electricalClass',('NETCLASS','nil','nil','t'))}
for group,nets in groups.items():
 for dom,(col,flag) in domain.items():
  name='NC_'+group+'_'+dom
  eq(name+' complete actual members',gmap[name],nets)
  eq(name+' correct one-domain flags',gflags[name],flag)
  for net in nets:
   found=next(r for r in rules if r['net']==net)
   eq(net+' reverse membership '+dom,q(found[col]),name)
for name,nets in {'DP_USB_CONNECTOR':{'USB_DP','USB_DM'},'DP_USB_MCU_SIDE':{'PA12_SHARED','PA11_SHARED'},'DP_CAN_BUS':{'CAN_H','CAN_L'}}.items():
 eq(name+' exact pair members',gmap[name],nets)
 eq(name+' is actual DIFF_PAIR',gflags[name][0],'DIFF_PAIR')
eq('27 netclasses plus 3 differential pairs',len(gmap),30)
phys={(r['cset'],r['layer']):attrs(r['values']) for r in table(F/'physical_csets.tsv')}
physNames=sorted({p[0] for p in phys})
for name in physNames:
 for layer in ['TOP','L2','L3','BOTTOM']:
  ck(name+' has '+layer,(name,layer) in phys)
  vals=phys.get((name,layer),{})
  allow='t' if name=='P_GND_PLANE' or (layer in ['TOP','BOTTOM'] and not(name=='P_USB_PROVISIONAL' and layer=='BOTTOM')) else 'nil'
  eq(name+' '+layer+' route/plane allow',vals.get('allow_etch'),allow)
  if layer=='TOP':eq(name+' qualified via list',vals.get('vias'),'L28_VIA030_C060:')
expectedPhys={'DEFAULT':(.2,.15),'P_SIGNAL_020':(.2,.15),'P_POWER_060':(.6,.25),'P_SWITCH_060':(.6,.25),'P_ANALOG_020':(.2,.15),'P_OSC_020':(.2,.15),'P_USB_PROVISIONAL':(.2,.15),'P_CAN_025':(.25,.2),'P_VDDA_030':(.3,.2),'P_GND_PLANE':(.6,.25)}
for name,(w,nw) in expectedPhys.items():
 for layer in ['TOP','L2','L3','BOTTOM']:
  val=phys.get((name,layer),{})
  eq(name+' '+layer+' min width mm',float(val.get('width_min','nan')),w)
  eq(name+' '+layer+' min neck mm',float(val.get('neckwidth_min','nan')),nw)
  eq(name+' '+layer+' max neck length mm',float(val.get('necklength_max','nan')),1.0)
usb=phys[('P_USB_PROVISIONAL','TOP')]
for k in ['dp_min_gap','dp_neck_gap','dp_primary_gap']:eq('USB TOP '+k+' provisional mm',float(usb[k]),.15)
for net in ['USB_DP','USB_DM','PA11_SHARED','PA12_SHARED']:
 r=next(x for x in rules if x['net']==net)
 eq(net+' real inherited maxvia',q(r['inheritedMaxVia']),'2')
 eq(net+' real inherited phase length budget',q(r['inheritedPhase']),'1 MM')
 eq(net+' real inherited uncoupled budget',q(r['inheritedUncoupled']),'6 MM')
for r in rules:
 props=set(re.findall(r'\(([A-Z_]+)\s',r['props']))
 expected={'LOGICAL_PATH','PHYSICAL_CONSTRAINT_SET'} if r['net'] in ['GND','VDDA'] else {'LOGICAL_PATH'}
 eq(r['net']+' only intended permanent net props (no challenge leak)',props,expected)
 if r['net']=='GND':ck('GND direct P_GND_PLANE override','(PHYSICAL_CONSTRAINT_SET "P_GND_PLANE")' in r['props'])
 if r['net']=='VDDA':ck('VDDA direct P_VDDA_030 override','(PHYSICAL_CONSTRAINT_SET "P_VDDA_030")' in r['props'])
stack=table(F/'stackup_full.tsv')
sourceStack=table(Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019\logs\reopen4_02\cross_section.tsv'))
key=['position','name','type','function','material','thickness','dk','loss','conductor','negative','mfg']
eq('Full native 4-layer stackup preserved',[[r[k] for k in key] for r in stack],[[r[k] for k in key] for r in sourceStack])
geo=table(F/'direct_geometry.tsv')
sourceGeo=table(Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019\logs\mech4_01\mechanical_direct.tsv'))
# The 29 direct export covers outline/keepin and route/height keepouts, not package placebounds.
sg={(r['layer'],r['bbox'],r['vertices']) for r in sourceGeo if q(r['layer'])!='PACKAGE GEOMETRY/PLACE_BOUND_TOP'}
ag={(r['layer'],r['bbox'],r['vertices']) for r in geo}
eq('Actual design outline, all keepins/keepouts geometry preserved',ag,sg)
rs=(F/'constraint_summary.txt').read_text()
ck('Final fresh DRC0/current','DRC_STATUS\tREADBACK\t0\tt' in rs)
for val in ['(allow_etch on)','(vias on)','(width_min on)','(line_line on)','(Maximum_Via_Count on)','(Differential_Pair_Primary_Gap on)']:ck('Relevant DRC mode enabled '+val,val in rs)
challenge=(A/'logs'/'challenge04'/'challenges.txt').read_text()
for name in ['DEFAULT_WIDTH','NET_OVERRIDE','DEFAULT_SPACING','CLASS_CLASS_ISOLATION','UNAPPROVED_VIA','USB_MAX_VIA','L2_POWER_BLOCKED','L2_GND_SHAPE_ALLOWED']:
 ck(name+' actual rollback0/current','DRC_STATUS\t'+name+'_AFTER\t0\tt' in challenge)
details={
'DEFAULT_WIDTH':['source "P_SIGNAL_020"','expected "0.15 MM"','actual "0.1 MM"','name "Minimum Neck Width"'],
'CLASS_POWER_WIDTH':['source "P_POWER_060"','expected "1 MM"','actual "10 MM"','name "Maximum Neck Length"'],
'DEFAULT_SPACING':['source "DEFAULT"','expected "0.2 MM"','actual "0.1 MM"','name "Line to Line Spacing"'],
'CLASS_CLASS_ISOLATION':['source "S_ISOLATE_100"','expected "1 MM"','actual "0.5 MM"'],
'UNAPPROVED_VIA':['source "P_SIGNAL_020"','actual "F29_UNAPPROVED_VIA040_C080"','name "Via List"'],
'USB_MAX_VIA':['source "E_USB_FS_BUDGET"','expected "2"','actual "3"','name "Maximum Via Count"'],
'L2_POWER_BLOCKED':['source "P_POWER_060"','name "Allow on ETCH Subclass"']}
for label,substrings in details.items():
 lines='\n'.join(line for line in challenge.splitlines() if line.startswith('DRC_DETAIL\t'+label+'\t'))
 for txt in substrings:ck(label+' actual expected DRC field '+txt,txt in lines)
ck('GND actual inner shape allowed','SHAPE_NET="GND" LAYER="ETCH/L2"' in challenge and 'DRC_STATUS\tL2_GND_SHAPE_ALLOWED\t0\tt' in challenge)
ck('All challenges finish rollback state','CHALLENGES_COMPLETE' in challenge and 'DRC_STATUS\tFINAL\t0\tt' in challenge)
coupon=(A/'logs'/'coupon_build.txt').read_text()
for txt in ['expected "1 MM" actual "7.6 MM" name "Differential Pair Phase Tolerance"','expected "6 MM" actual "10 MM"','expected "6 MM" actual "17.6 MM"','DRC_STATUS\tPHASE_EQUAL\t0\tt','COUPON_BUILD_COMPLETE']:ck('Coupon actual length-budget evidence '+txt,txt in coupon)

sp={(r['cset'],r['layer']):attrs(r['values']) for r in table(F/'spacing_csets.tsv')}
for name,gap in {'DEFAULT':.2,'S_POWER_030':.3,'S_ANALOG_030':.3,'S_USB_015':.15,'S_CAN_025':.25,'S_USB_OTHER_050':.5,'S_ISOLATE_100':1.0}.items():
 for layer in ['TOP','L2','L3','BOTTOM']:
  ck(name+' spacing set on '+layer,(name,layer) in sp)
  eq(name+' '+layer+' line-to-line mm',float(sp.get((name,layer),{}).get('line_line','nan')),gap)
proof=[s.split('\t') for s in (F/'specific_proof.tsv').read_text().splitlines()]
cc=[r for r in proof if r[0]=='CLASS_CLASS']
expectedCC={frozenset(['NC_USB_FS_S','NC_DIGITAL_GENERAL_S']):'S_USB_OTHER_050',
 frozenset(['NC_SWITCHING_S','NC_USB_FS_S']):'S_ISOLATE_100',
 frozenset(['NC_SWITCHING_S','NC_OSCILLATOR_S']):'S_ISOLATE_100',
 frozenset(['NC_SWITCHING_S','NC_ANALOG_SENSITIVE_S']):'S_ISOLATE_100'}
eq('Four actual class-to-class tables resolved by names',len(cc),4)
for r in cc:
 pair=frozenset(r[1:3])
 ck('Class table expected pair '+str(sorted(pair)),pair in expectedCC)
 eq('Class table assigned CSet '+str(sorted(pair)),q(r[3]),expectedCC.get(pair))
 eq('Class table both ends in actual spacing domain '+str(sorted(pair)),r[4:10],['nil','t','nil','nil','t','nil'])
 ck('Class table references existing spacing CSet '+q(r[3]),(q(r[3]),'TOP') in sp)
ck('Native unique via count explicit not extractor aliases',['UNIQUE_VIA_COUNT','1'] in proof)
eq('Only one explicit via proof',len([r for r in proof if r[0]=='UNIQUE_VIA']),1)
# No routed ETCH segments have escaped the reversible teaching challenges.
routed=table(F/'route_geometry.tsv')
etch=[r for r in routed if q(r['layer']).startswith('ETCH/')]
eq('No persisted teaching challenge etch segments',len(etch),0)
solver=(A/'logs'/'coupon_board02'/'stdout.txt').read_text(errors='replace')
ck('Automatic bem2d attempt retained','bem2d' in solver)
ck('Automatic solver failure retained','failed' in solver.lower())


cp=table(A/'logs'/'read_coupon'/'route_geometry.tsv')
eq('Exactly two persistent coupon traces',len(cp),2)
for r in cp:
 numbers=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',r['startEnd'])]
 length=math.hypot(numbers[2]-numbers[0],numbers[3]-numbers[1])
 eq('Coupon '+q(r['net'])+' independent geometric length mm',length,20.0)
 eq('Coupon '+q(r['net'])+' actual width mm',float(r['width']),0.2)
rc=json.loads((A/'logs'/'read_coupon'/'launch.json').read_text())
ck('Separate coupon new-process readonly exit0',rc['completed'] and rc['exitCode']==0 and rc['beforeSHA256']==rc['afterSHA256'])
ck('Separate coupon current DRC0/t','drcs=0\ndrcState=t' in (A/'logs'/'read_coupon'/'native_summary.txt').read_text())
exp=json.loads((A/'exports'/'export_result.json').read_text())
eq('Official technology export actual SHA',sha(A/'exports'/'F29_RULES.tcf'),exp['outputSHA256'])
for r in exp['records']:
 ck('Technology '+r['step']+' exit0 and board unchanged',r['exitCode']==0 and r['boardBefore']==expectedSHA and r['boardAfter']==expectedSHA)
ct=(A/'exports'/'techfile_run'/'compare_stdout.txt').read_text(errors='replace')
ct+=(A/'exports'/'techfile_run'/'compare_techfile.log').read_text(errors='replace')
ck('Official technology compare no changes','No objects were updated' in ct)


conn=[r for r in table(A/'logs'/'coupon_connections.tsv') if r['kind'] in ['NET','PIN']]
for net in ['CAL_P','CAL_N']:
 n=next(r for r in conn if r['kind']=='NET' and r['net_or_ref']==net)
 eq('Official pinsOfNet '+net+' count',int(n['count_or_pin']),2)
 eq('Official '+net+' unconnected',int(n['unconnected_or_xy']),0)
 eq('Official '+net+' unplaced',int(n['unplaced_or_net']),0)
 pins=[r for r in conn if r['kind']=='PIN' and q(r['unplaced_or_net'])==net]
 endpoints=[]
 for r in pins:
  numbers=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',r['unconnected_or_xy'])]
  endpoints.append(tuple(numbers))
 line=next(r for r in cp if q(r['net'])==net)
 numbers=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',line['startEnd'])]
 eq('Coupon '+net+' actual endpoint pins coincide with route',sorted(endpoints),sorted([tuple(numbers[:2]),tuple(numbers[2:])]))
eq('Coupon four actual connected placed pins',len([r for r in conn if r['kind']=='PIN']),4)
eq('Coupon actual pin/net identities preserved across queries',
 sorted((r['net_or_ref'],r['count_or_pin'],q(r['unplaced_or_net'])) for r in conn if r['kind']=='PIN'),
 sorted((r['refdes'],r['pin'],r['net']) for r in table(A/'logs'/'read_coupon'/'component_pins.tsv')))

# Evidence identity snapshot, not a copy of implementation validator.
evidence=[]
for p in sorted(F.iterdir()):
 if p.is_file():evidence.append({'path':str(p),'SHA256':sha(p)})
for p in [A/'native'/'F29_CONSTRAINTS_v3.brd',A/'logs'/'challenge04'/'challenges.txt',A/'logs'/'challenge04'/'launch.json',A/'logs'/'coupon_build.txt']:
 evidence.append({'path':str(p),'SHA256':sha(p)})
for p in [A/'logs'/'coupon_connections.tsv',A/'logs'/'coupon_board02'/'stdout.txt',A/'logs'/'read_coupon'/'launch.json',A/'logs'/'read_coupon'/'native_summary.txt',A/'logs'/'read_coupon'/'component_pins.tsv',A/'logs'/'read_coupon'/'route_geometry.tsv',A/'exports'/'F29_RULES.tcf',A/'exports'/'export_result.json',A/'exports'/'techfile_run'/'compare_stdout.txt',A/'exports'/'techfile_run'/'compare_techfile.log']:
 evidence.append({'path':str(p),'SHA256':sha(p)})
(R/'evidence_manifest.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
def default(x):
 if isinstance(x,set):return sorted(x)
 if isinstance(x,dict):return {str(k):v for k,v in x.items()}
 return str(x)
result={'status':'PASS_INDEPENDENT_REVIEW_LESSON29','checksCount':len(checks),'allCoreChecksPass':all(c['pass'] for c in checks),'failedChecks':[c for c in checks if not c['pass']],'checks':checks,'physicalCsetNames':physNames,'openItems':[],'scopeLimits':['No Cadence launched by reviewer.','Default narrow-line challenge reports Minimum Neck Width, not direct Minimum Line Width. Power case reports Maximum Neck Length.','Coupon phase budget is a length check, no impedance/delay certification; automatic bem2d failure remains separate.','Original source design has 79 unplaced components, so final DRC0 is not whole-board placement/routing acceptance.']}
# Tuple dict keys in actual pin mapping are converted only for JSON evidence.
def safe(x):
 if isinstance(x,dict):return {str(k):safe(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [safe(v) for v in x]
 if isinstance(x,set):return sorted(safe(v) for v in x)
 return x
(R/'review_final.json').write_text(json.dumps(safe(result),indent=2),encoding='utf-8')
print('Core checks',len(checks),'failures',len(result['failedChecks']))
for c in result['failedChecks']:print('FAILED',c['check'],str(c['detail'])[:200])
print('Physical CSet names',physNames)
