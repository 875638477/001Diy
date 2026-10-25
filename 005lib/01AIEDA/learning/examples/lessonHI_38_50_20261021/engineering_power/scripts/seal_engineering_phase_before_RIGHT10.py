from pathlib import Path
import json,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
p=R/'README.md';s=p.read_text(encoding='utf-8')
if 'VDDA_prefilter_reroute_08.json is a candidate' not in s:s += '\nVDDA_prefilter_reroute_08.json is a candidate requiring completeSPIapproval, not automatically executable. It fixes actualC8pad clearance and moves TOPpowervertical westofSCKcorridor. LatestSPI sourcev5 read-onlyscreen: readouts/SPI_source_v5_power_prefilter08_precheck.json (50629 geometry checks, no issue in declaredscope). ActualUSB8 maskzero-margin finding and nativefield-solverfailure remain manufacturing/SIopen, see note sections10-11.\n'
p.write_text(s,encoding='utf-8')
note=R.parent.parent.parent/'notes/lessonHI_power_20261021.md'
assert note.exists(),note
files=[]
for f in sorted(R.rglob('*')):
 if f.is_file() and f.name!='artifact_manifest.json':
  files.append(dict(path=str(f.relative_to(R)).replace('\\','/'),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),size=f.stat().st_size))
files.append(dict(path='../../../notes/lessonHI_power_20261021.md',sha256=hashlib.sha256(note.read_bytes()).hexdigest(),size=note.stat().st_size))
out=dict(status='ENGINEERING_PHASE_MANIFEST_NOT_FINAL_ROUTE_ACCEPTANCE',date='2026-10-22',scope='Immutablehistorical02d/03c reviews plus latestengineering07b/06b/CAN04/05/ESD04c/prefilter08 candidates, SPIv5 read-onlyscreen. Laternativeintegration requiresnewreadbackandreseal. No claimallHIcomplete.',files=files,excludes=['artifact_manifest.json'],currentCandidates=['STAR_reroute_07b.json','V3_peripheral_distribution_06b.json','interface_CAN_routes_04.json','CAN_local_supply_05.json','ESD_ground_routes_04c.json','VDDA_prefilter_reroute_08.json','routing_policy_interfaces_04.json'])
(R/'artifact_manifest.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(dict(files=len(files),manifestSHA=hashlib.sha256((R/'artifact_manifest.json').read_bytes()).hexdigest())))
