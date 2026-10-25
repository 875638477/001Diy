from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
s=(R/'scripts/precheck_CAN04_05.py').read_text()
s=s.replace("power_4L_b003c/normalized.json","mcu_4L_b006/normalized.json")
s=s.replace("files=['interface_CAN_routes_04.json','CAN_local_supply_05.json']","files=['STAR_reroute_07.json','interface_CAN_routes_04.json','CAN_local_supply_05.json','V3_peripheral_distribution_06b.json']")
s=s.replace("segments=[];vias=[];pads=[]","""deletes=plans[0]['operations'][:2]
for d in deletes:
 def match(r):
  return r['net']==d['net'] and r['layer']=='ETCH/'+d['layer'] and abs(r['width']-d['width'])<1e-6 and (r['startEnd']==d['points'] or r['startEnd']==d['points'][::-1])
 hits=[r for r in base['routes'] if match(r)]
 assert len(hits)==1,(d['id'],len(hits))
 base['routes']=[r for r in base['routes'] if not match(r)]
segments=[];vias=[];pads=[]""")
s=s.replace("if s['id'].startswith('STAR_U1_') and p['ref']=='U1':req=.2","if (s['id'].startswith('STAR_U1_') or s['id'].startswith('STAR_DIAG_GROUND_RETURN:0') or s['id'].startswith('STAR_DIAG_GROUND_RETURN:1')) and p['ref']=='U1':req=.2")
s=s.replace("if (s['id'].startswith('STAR_U1_') and t['id']=='BASE_G') or (t['id'].startswith('STAR_U1_') and s['id']=='BASE_G'):req=.2","if ((s['id'].startswith('STAR_U1_') or s['id'] in ['STAR_DIAG_GROUND_RETURN:0','STAR_DIAG_GROUND_RETURN:1']) and t['id']=='BASE_G') or ((t['id'].startswith('STAR_U1_') or t['id'] in ['STAR_DIAG_GROUND_RETURN:0','STAR_DIAG_GROUND_RETURN:1']) and s['id']=='BASE_G'):req=.2")
s=s.replace("'readouts/CAN_04_05_geometry_precheck.json'","'readouts/STAR07_V306b_CAN_geometry_precheck.json'")
s=s.replace("FrozenHI4L03c actual snapshot; no pendingplacementchanges.","FrozenMCU6 actual snapshot with2oldSTARsegments explicitlyremoved in memory; eachmatchunique. Groundescape .982843 localexistingLEFT spacing.2 considered, notglobalrelax.")
(R/'scripts/precheck_STAR07_V306b.py').write_text(s)
print('preparedscreen')
