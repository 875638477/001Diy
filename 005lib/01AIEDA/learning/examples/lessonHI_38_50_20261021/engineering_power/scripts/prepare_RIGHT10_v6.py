from pathlib import Path
import json,hashlib,copy
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');R=H/'engineering_power'
f=R/'RIGHT10_interface_corridors_v5.json';m=json.loads(f.read_text());(R/'RIGHT10_interface_corridors_v5_failed02.json').write_bytes(f.read_bytes())
for o in m['operations']:
 if o['id']=='RIGHT_SCL_EXPLICIT':o['points']=[[46.8,26.65],[47,26.45],[54,26.45],[55.5,27.95],[55.5,34.18],[57.7,34.18],[58.5,34.98],[58.5,35]]
m['revision']='v6 SCL left of R30 power and above BOOT_SERVICE transition without crossing R19 V3 pad';(R/'RIGHT10_interface_corridors_v6.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
p=json.loads((R/'RIGHT10_source_joint_v5.json').read_text());p['oscillatorReferenceRework']['neckProjectionException']='Finite projection of VDD48/local3V3 and VBAT source power branches across narrow quiet-stem; do not claim complete shadow free of other copper. No unrelated GPIO/I2C/SPI crosses island/guard shadow.'
(R/'RIGHT10_source_joint_v5.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
for v in ['2L','4L']:
 pol=json.loads((R/f'RIGHT10_long_policy_{v}_v5.json').read_text());ids={o['id'] for o in m['operations']};pol['pendingOperations']=[o for o in pol['pendingOperations'] if o['id'] not in ids]+m['operations']
 base=json.loads((H/f'inventory/checkpoints/USB_aux_{v}_b014/normalized.json').read_text());old=json.loads((H/f'inventory/checkpoints/SPI_external_{v}_b012/normalized.json').read_text())
 # Remove pending USBaux operations now present in actual b014; exact geometry signatures rather than assumed names.
 def present(o):
  if o['type']=='via':return any(a['net']==o['net'] and a['xy']==o['xy'] for a in base['vias'])
  if o['type']=='route':
   return all(any(r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and r['startEnd'] in [[a,z],[z,a]] and abs(r['width']-(o['widths'][j] if 'widths' in o else o['width']))<1e-5 for r in base['routes']) for j,(a,z) in enumerate(zip(o['points'],o['points'][1:])))
  return False
 pol['pendingOperations']=[o for o in pol['pendingOperations'] if not present(o)]
 # Current actual USBaux supersedes all provisional CC and USBremote operations in old policy.
 pol['pendingOperations']=[o for o in pol['pendingOperations'] if o['net'] not in ['USB_CC1','USB_CC2','VBUS_PRESENT','USB_ATTACH_N','USB_PULLUP_SRC'] and not o['id'].startswith(('CC_R3_GND','CC_R4_GND','HI_RD'))]
 base['planes']=[a for a in base['planes'] if not (a.get('filled') and not a.get('generated') and a.get('area',0)<100)]
 (R/f'source/RIGHT10_long_{v}_b014_virtual.json').write_text(json.dumps(base,indent=2),encoding='utf-8');pol['sourceCheckpoint']=f'inventory/checkpoints/USB_aux_{v}_b014';pol['sourcePlans']=[a for a in pol['sourcePlans'] if not any(x in a['path'] for x in ['SPI_external','CC_entry','aux_remote'])]
 pol['sourcePlans'] += [dict(path='engineering_power/RIGHT10_source_joint_v5.json',sha256=hashlib.sha256((R/'RIGHT10_source_joint_v5.json').read_bytes()).hexdigest()),dict(path='engineering_power/RIGHT10_interface_corridors_v6.json',sha256=hashlib.sha256((R/'RIGHT10_interface_corridors_v6.json').read_bytes()).hexdigest())]
 (R/f'RIGHT10_long_policy_{v}_v6.json').write_text(json.dumps(pol,indent=2),encoding='utf-8')
s=(R/'scripts/precheck_RIGHT10_v5_interfaces.py').read_text().replace('RIGHT10_interface_corridors_v5.json','RIGHT10_interface_corridors_v6.json').replace('SPI_external_{variant}_b012','USB_aux_{variant}_b014').replace('RIGHT10_v5_interfaces_','RIGHT10_v6_interfaces_');(R/'scripts/precheck_RIGHT10_v6_interfaces.py').write_text(s,encoding='utf-8')