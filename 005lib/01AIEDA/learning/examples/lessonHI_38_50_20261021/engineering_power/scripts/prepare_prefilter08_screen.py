from pathlib import Path
import shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
shutil.copyfile(R.parent/'plans/SPI_NSS_explicit_v3b.json',R/'source/root_SPI_NSS_explicit_v3b.json')
s=(R/'scripts/precheck_STAR07b_V306b.py').read_text()
s=s.replace("mcu_4L_b006/normalized.json","usb_esd_4L_b008/normalized.json")
s=s.replace("files=['STAR_reroute_07b.json','interface_CAN_routes_04.json','CAN_local_supply_05.json','V3_peripheral_distribution_06b.json']","files=['STAR_reroute_07b.json','interface_CAN_routes_04.json','CAN_local_supply_05.json','V3_peripheral_distribution_06b.json','VDDA_prefilter_reroute_08.json','source/root_SPI_NSS_explicit_v3b.json']")
s=s.replace("deletes=plans[0]['operations'][:2]","deletes=[o for p in plans for o in p['operations'] if o['type']=='deleteSegment']")
s=s.replace("req=clearance(v['net'],p['net'])","req=clearance(v['net'],p['net'])\n    if v['id']=='NSS_PULLUP_GND_RETURN' and p['id']=='R25.2':req=.2")
s=s.replace("'readouts/STAR07b_V306b_CAN_geometry_precheck.json'","'readouts/Prefilter08_NSS3b_power_group_precheck.json'")
s=s.replace("FrozenMCU6 actual snapshot with2oldSTARsegments explicitlyremoved in memory; eachmatchunique.","FrozenUSB8 actual snapshot with2oldSTAR+3oldprefiltersegments explicitlyremoved in memory; eachmatchunique. IncludesrootNSS3b actualcandidate;NSSGNDvia-R25pad usesnative smdpin_via.2 ratherthanincorrectgenericpower.3.")
(R/'scripts/precheck_prefilter08_NSS3b.py').write_text(s)
print('prepared08')
