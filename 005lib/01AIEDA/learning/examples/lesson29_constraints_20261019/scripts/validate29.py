from pathlib import Path
import re,json,csv,math,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
B=R/'logs/read_final02';C=R/'logs/read_coupon';L=R.parent/'lesson28_stackup_20261019'
spec=json.loads((R/'constraint_spec.json').read_text())
checks=[]
def ck(n,v,a=None):checks.append({'name':n,'pass':bool(v),'actual':a})
def sx(s):
 t=re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+',s);i=0
 def take():
  nonlocal i
  v=t[i];i+=1
  if v=='(':
   a=[]
   while t[i]!=')':a.append(take())
   i+=1;return a
  if v.startswith('"'):return json.loads(v)
  if v=='nil':return None
  if v=='t':return True
  try:return float(v)
  except ValueError:return v
 return take()
def rows(p):return list(csv.DictReader(p.open(encoding='utf8'),delimiter='\t',quotechar='\0'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def assoc(v):return {str(x[0]):x[1] for x in v or []}
for stage,marker,path in [
 ('build02_process','BUILD_COMPLETE',R/'logs/build02/build.txt'),
 ('patch03','GROUND_PATCH_COMPLETE',R/'logs/ground_patch.txt'),
 ('read_final02','READBACK_COMPLETE',B/'constraint_summary.txt'),
 ('read_geometry','L28_MECHANICAL_DIRECT COMPLETE',R/'logs/read_geometry/mechanical_roots.txt'),
 ('challenge04','CHALLENGES_COMPLETE',R/'logs/challenge04/challenges.txt'),
 ('coupon_package02','COUPON_PACKAGE_COMPLETE',R/'logs/coupon_package.txt'),
 ('coupon_board02','COUPON_BUILD_COMPLETE',R/'logs/coupon_build.txt'),
 ('read_coupon','READBACK_COMPLETE',C/'constraint_summary.txt')]:
 j=json.loads((R/f'logs/{stage}/launch.json').read_text())
 ck(stage+' actual process exit',j['completed'] and j['exitCode']==0,j['exitCode'])
 ck(stage+' semantic completion',marker in path.read_text())
 ck(stage+' no SKILL Error','E- *Error*' not in (R/f'logs/{stage}/stdout.txt').read_text(errors='replace'))
 if j.get('readonly') or stage=='challenge04':ck(stage+' hash stable',j['beforeSHA256']==j['afterSHA256'])
ck('source28 unchanged',sha(L/'native/F28_4L.brd')=='F004184D46B86A7CF56FFA05C33418A6BEEFA508A3043A3442540B69AFA558D6')
ck('final29 exact identity',sha(R/'native/F29_CONSTRAINTS_v3.brd')=='6276201EF1750D3A318D901CCF1ADFBB1CA41A4301329CD21E32A0E22B3FA607')
de=json.loads((R.parent/'de_15_26_20261019/integrated_circuit.json').read_text())
expected={(c['ref'],p):(n or '') for c in de['components'] for p,n in c['pins'].items()}
pins=rows(B/'component_pins.tsv');got={(x['refdes'],x['pin']):x['net'] for x in pins}
ck('272 exact logical pin identities/net assignments',got==expected and len(got)==272,len(got))
comps=rows(B/'components.tsv');ck('80 logical components',len(comps)==80)
for c in de['components']:
 a=next(x for x in comps if x['refdes']==c['ref'])
 ck(c['ref']+' package identity',a['package'].upper()==de['models'][c['model']]['footprint'].upper())
ck('only logical J2 placed',sorted(x['refdes'] for x in comps if x['placed']=='t')==['J2'])
summary=(B/'native_summary.txt').read_text()
ck('native5 symbols and0 currentDRC','symbols=5' in summary and 'drcs=0' in summary and 'drcState=t' in summary)
netrows=rows(B/'net_rules.tsv');ck('69 native nets classified',len(netrows)==69 and set(x['net'] for x in netrows)==set(spec['net_members']))
lookup={n:g for g,ns in spec['groups'].items() for n in ns}
usb={'USB_DP','USB_DM','PA12_SHARED','PA11_SHARED'}
for n in netrows:
 g=lookup[n['net']]
 for field,suf in [('physicalClass','P'),('spacingClass','S'),('electricalClass','E')]:
  ck(n['net']+' '+field,sx(n[field])=='NC_'+g+'_'+suf)
 props=assoc(sx(n['props']))
 ck(n['net']+' no temporary override',not any(k in props for k in ['RETAIN_NET_ON_VIAS','MIN_LINE_WIDTH','MIN_NECK_WIDTH']))
 if n['net'] in usb:
  ck(n['net']+' actual inheritedUSB limits',[sx(n[k]) for k in ['inheritedMaxVia','inheritedPhase','inheritedUncoupled']]==['2','1 MM','6 MM'])
 if n['net'] in ['GND','VDDA']:
  ck(n['net']+' direct exception',props.get('PHYSICAL_CONSTRAINT_SET')==('P_GND_PLANE' if n['net']=='GND' else 'P_VDDA_030'))
members=rows(B/'group_members.tsv')
ck('27 domain classes persisted',len({x['group'] for x in members if sx(x['groupType'])=='NETCLASS'})==27)
ck('207 class-member associations',len([x for x in members if sx(x['groupType'])=='NETCLASS'])==207)
pairmap={}
for x in members:
 if sx(x['groupType'])=='DIFF_PAIR':pairmap.setdefault(x['group'],set()).add(sx(x['member']))
ck('three true pair membership maps',pairmap=={'DP_USB_CONNECTOR':{'USB_DP','USB_DM'},'DP_USB_MCU_SIDE':{'PA12_SHARED','PA11_SHARED'},'DP_CAN_BUS':{'CAN_H','CAN_L'}})
phys={(x['cset'],x['layer']):assoc(sx(x['values'])) for x in rows(B/'physical_csets.tsv')}
ck('10 physical CSet x4layers',len(phys)==40)
widths={'DEFAULT':(.2,.15),'P_SIGNAL_020':(.2,.15),'P_POWER_060':(.6,.25),'P_SWITCH_060':(.6,.25),'P_ANALOG_020':(.2,.15),'P_OSC_020':(.2,.15),'P_USB_PROVISIONAL':(.2,.15),'P_CAN_025':(.25,.2),'P_VDDA_030':(.3,.2),'P_GND_PLANE':(.6,.25)}
for name,(w,neck) in widths.items():
 for lay in ['TOP','L2','L3','BOTTOM']:
  v=phys[name,lay]
  ck(name+' '+lay+' nominal vs neck widths',abs(v['width_min']-w)<1e-8 and abs(v['neckwidth_min']-neck)<1e-8)
  if lay in ['L2','L3']:ck(name+' '+lay+' reference layer policy',bool(v['allow_etch'])==(name=='P_GND_PLANE'))
 ck(name+' sole approved via',[x for x in phys[name,'TOP']['vias'].split(':') if x]==['L28_VIA030_C060'])
ck('USB onlyTOP',phys['P_USB_PROVISIONAL','TOP']['allow_etch'] is True and phys['P_USB_PROVISIONAL','BOTTOM']['allow_etch'] is None)
spaces={(x['cset'],x['layer']):assoc(sx(x['values'])) for x in rows(B/'spacing_csets.tsv')}
for n,g in [('DEFAULT',.2),('S_POWER_030',.3),('S_ANALOG_030',.3),('S_USB_015',.15),('S_CAN_025',.25),('S_ISOLATE_100',1.),('S_USB_OTHER_050',.5)]:
 for l in ['TOP','L2','L3','BOTTOM']:ck(n+' '+l+' line gap',abs(spaces[n,l]['line_line']-g)<1e-8)
e=rows(B/'electrical_csets.tsv')
ck('ECSet exact explicit units',len(e)==1 and assoc(sx(e[0]['values']))=={'Maximum_Via_Count':'2','Differential_Pair_Phase_Tolerance':'1 MM','Differential_Pair_Max_Uncoupled_Length':'6 MM'})
proof=(B/'specific_proof.tsv').read_text()
ck('unique physical via DBID count1','UNIQUE_VIA_COUNT\t1\n' in proof and len(re.findall(r'^UNIQUE_VIA\t',proof,re.M))==1)
cc=[]
for line in proof.splitlines():
 if line.startswith('CLASS_CLASS\t'):
  x=line.split('\t');cc.append((frozenset(x[1:3]),sx(x[3])))
  ck('classclass correct spacing domains '+x[1]+'/'+x[2],[sx(y) for y in x[4:]]==[None,True,None,None,True,None])
ck('four explicit classclass pairs',set(cc)=={(frozenset(['NC_USB_FS_S','NC_DIGITAL_GENERAL_S']),'S_USB_OTHER_050'),(frozenset(['NC_SWITCHING_S','NC_USB_FS_S']),'S_ISOLATE_100'),(frozenset(['NC_SWITCHING_S','NC_OSCILLATOR_S']),'S_ISOLATE_100'),(frozenset(['NC_SWITCHING_S','NC_ANALOG_SENSITIVE_S']),'S_ISOLATE_100')})
# Exact independent geometry readback uses same native query on source and final, not file name inference.
for a,b in [('placed_pins.tsv','more4_01'),('placed_pads.tsv','more4_01'),('padstacks.tsv','more4_01'),('mechanical_direct.tsv','mech4_01')]:
 ck(a+' unchanged from28',(R/'logs/read_geometry'/a).read_bytes()==(L/'logs'/b/a).read_bytes())
for tag,cnt in [('DEFAULT_WIDTH',1),('CLASS_POWER_WIDTH',1),('NET_OVERRIDE',0),('DEFAULT_SPACING',1),('CLASS_CLASS_ISOLATION',1),('UNAPPROVED_VIA',4),('USB_MAX_VIA',1),('L2_POWER_BLOCKED',1),('L2_GND_SHAPE_ALLOWED',0),('FINAL',0)]:
 text=(R/'logs/challenge04/challenges.txt').read_text()
 ck(tag+' native currentDRC',f'DRC_STATUS\t{tag}\t{cnt}\tt' in text)
for label in ['DEFAULT_WIDTH','NET_OVERRIDE','DEFAULT_SPACING','CLASS_CLASS_ISOLATION','UNAPPROVED_VIA','USB_MAX_VIA','L2_POWER_BLOCKED','L2_GND_SHAPE_ALLOWED']:
 ck(label+' rollback0/t',f'DRC_STATUS\t{label}_AFTER\t0\tt' in text)
ck('class power actual neck length check', 'source "P_POWER_060"' in text and 'name "Maximum Neck Length"' in text)
ck('spacing numeric actual proofs','expected "0.2 MM" actual "0.1 MM"' in text and 'expected "1 MM" actual "0.5 MM"' in text)
ck('electrical via count proof','expected "2" actual "3" name "Maximum Via Count"' in text)
phase=(R/'logs/coupon_build.txt').read_text()
ck('native phase length DRC proof','expected "1 MM" actual "7.6 MM" name "Differential Pair Phase Tolerance"' in phase)
ck('native uncoupled length DRC proof','expected "6 MM" actual "17.6 MM"' in phase)
ck('matched coupon current0DRC','DRC_STATUS\tPHASE_EQUAL\t0\tt' in phase)
route=rows(C/'route_geometry.tsv');r=[x for x in route if sx(x['net']) in ['CAL_P','CAL_N']]
ck('independent matched coupon exactly2 segments',len(r)==2)
for x in r:
 p=sx(x['startEnd']);length=math.dist(p[0],p[1]);ck('coupon '+sx(x['net'])+'20mm actual segment',abs(length-20)<1e-9 and sx(x['width'])==.2)
connection=(R/'logs/coupon_connections.tsv').read_text()
ck('coupon2 actual pins per net via official query', 'NET\tCAL_P\t2\t0\t0' in connection and 'NET\tCAL_N\t2\t0\t0' in connection)
for n in ['CAL_P','CAL_N']:
 pinxy=[]
 for line in connection.splitlines():
  if line.startswith('PIN\t'):
   z=line.split('\t')
   if sx(z[4])==n:pinxy.append(sx(z[3]))
 routepair=next(sx(x['startEnd']) for x in r if sx(x['net'])==n)
 ck(n+' actual pins coincide with full route endpoints',sorted(pinxy)==sorted(routepair))

export=json.loads((R/'exports/export_result.json').read_text())
ck('officialTCF exported+compare',[x['exitCode'] for x in export['records']]==[0,0] and (R/'exports/F29_RULES.tcf').is_file())
ck('officialTCF compare no diff','No objects were updated.' in (R/'exports/techfile_run/compare_techfile.log').read_text())
fail=[x for x in checks if not x['pass']]
result={'status':'PASS_NATIVE_CAD_CONSTRAINT_LESSON' if not fail else 'FAIL','date':'2026-10-19 Asia/Shanghai','allChecksPass':not fail,'checkCount':len(checks),'checks':checks,'failures':fail,'finalBoard':str(R/'native/F29_CONSTRAINTS_v3.brd'),'scope':'Four-layer JLC-target draft rule profile with actual native rules, independent persistence and DRC challenges. USB W/S provisional, board placement/routing/copper and manufacturing release not accepted. Pure length coupon DRC does not certify SI/impedance; automatic internal field-solver errors retained.'}
(R/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps({'status':result['status'],'checks':len(checks),'failures':fail},indent=2))
