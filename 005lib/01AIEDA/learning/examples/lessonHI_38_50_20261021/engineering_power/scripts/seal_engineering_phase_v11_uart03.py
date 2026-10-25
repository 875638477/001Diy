from pathlib import Path
import hashlib,json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power'); H=R.parent
note=H.parent.parent/'notes/lessonHI_power_20261021.md'
def item(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest().upper(),size=p.stat().st_size)
old=R/'artifact_manifest.json';history=R/'artifact_manifest_phase_v10_20261022.json'
if old.exists() and not history.exists():history.write_bytes(old.read_bytes())
selected=[]
for v in ['2L','4L']:
 for name in [f'RIGHT10_FULL_{v}_v11.json',f'UART_RX_receiver_bridge_{v}_03.json',f'readouts/UART_RX_bridge03_full_{v}.json',f'readouts/south_service_delta02_final2_{v}.json']:
  selected.append(R/name)
 selected += [H/f'inventory/checkpoints/USB_aux_{v}_b014/normalized.json',H/f'inventory/checkpoints/USB_aux_{v}_b014/networks.json',H/f'inventory/checkpoints/USB_aux_{v}_b014/base_net_rules.json']
selected.append(R/'readouts/UART_RX_receiver_bridge_03_review.json')
(R/'RIGHT11_UART03_manifest.json').write_text(json.dumps(dict(status='FROZEN_CANDIDATES_NATIVE_REBASE_AND_ACTUAL_REFERENCE_PENDING',date='2026-10-22',files=[item(f) for f in selected],scope='RIGHT11 frozenjoint source plus complete UART03 receiverdelta; native b015 has not been claimed or substituted by virtualintegration. v10 subsetmanifest preserved historical.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[item(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='artifact_manifest.json']; files.append(item(note))
out=dict(status='ENGINEERING_PHASE_MANIFEST_NOT_FINAL_ROUTE_ACCEPTANCE',date='2026-10-22',files=files,excludes=['artifact_manifest.json'],currentCandidates=['RIGHT10_FULL_2L_v11.json','RIGHT10_FULL_4L_v11.json','UART_RX_receiver_bridge_2L_03.json','UART_RX_receiver_bridge_4L_03.json'],scope='All ownengineering recordfiles. Prior power/CAN/SPI nativehistory remains stage-specific; latest complete RIGHT11 andUART03 candidates require native application/rebase/actualreference/fullreopen. Mainfeedrework paused; no claimallHIcomplete.',actualHistoricalOperations=['STAR_reroute_07c.json','V3_peripheral_distribution_06b.json','interface_CAN_routes_04.json','CAN_local_supply_05.json','ESD_ground_routes_04c.json','SPI_external_2L_engineered_v10.json','SPI_external_4L_engineered_v6.json'])
old.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Verify every newly sealed byte; nested historical manifests describe their own past scope.
assert all(item(Path(a['path']))['sha256']==a['sha256'] for a in files)
print(json.dumps(dict(fileCount=len(files),manifest=item(old),candidateManifest=item(R/'RIGHT11_UART03_manifest.json')),ensure_ascii=False))