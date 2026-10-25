from pathlib import Path
import json,hashlib,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');P=R/'engineering_power';note=R.parent.parent/'notes/lessonHI_power_20261021.md'
def item(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest().upper(),size=p.stat().st_size)
can=P/'CAN_RXD_2L_engineered_07.json';q=json.loads(can.read_text());proofs=[]
for a in q['proofs']:
 b=dict(a)
 if 'targetAlias'in b:b['toAlias']=b.pop('targetAlias')
 proofs.append(b)
adapt=dict(status='DOCUMENTED_SCHEMA_ADAPTER_CANONICAL_FROZEN_UNCHANGED',canonical=item(can),proofsForNativeAdapter=proofs,operationAdaptations=['Exclude originalpendingHI_2L_VBUS_PRESENT_N_1_R1 and insert includedreplacementonce; beforeappliednative compare exactoriginal/uniqueness','If originalVBUSoperation alreadyexistsinnative, requireactualuniquesegmentripupdelta before applyingCAN07','Forremaining_returns02 automaticallyaddU1.35-GNDviaalias graphproofs; do notomit becausecandidateonlylistsengineeringreturnreview','RIGHT11 BOOToperation geometryadapt documented separatelyinBOOT_endpoint_simplification_02; originalfrozenfileunchanged'],scope='Onlyschema/integrationinstructions, noCadenceexecution or claimfinalDRC.')
(P/'CAN07_native_adapter_notes.json').write_text(json.dumps(adapt,indent=2)+'\n',encoding='utf-8')
selected=[can,P/'CAN07_native_adapter_notes.json',P/'readouts/CAN_RXD_2L_engineered_07_full.json',P/'remaining_returns_2L_v19_02.json',P/'remaining_returns_4L_v19_02.json',P/'readouts/remaining_returns_v19_02_selection.json',P/'readouts/remaining_returns_2L_v19_02_full.json',P/'readouts/remaining_returns_4L_v19_02_full.json',P/'readouts/actual_BOOT_failure07_geometry.json',P/'readouts/BOOT_endpoint_simplification_02.json',P/'readouts/PB_local_switch_corridor_02.json',R/'plans/J2_GND_entry_2L_01.json',R/'plans/J2_GND_entry_4L_01.json']
manifest=dict(status='FROZEN_SCOPED_ENGINEERING_CANDIDATES_NOT_NATIVE_ACCEPTANCE',date='2026-10-22',files=[item(x)for x in selected],scope='CAN07+low-speedsense replacement, remainingreturns02, BOOTactualdiagnosticandlocalPBstudy; all new native dynamiccopper/fullDRC/graph/negative/reopen remainsoleexecutor/root.')
(P/'CAN07_returns02_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
old=P/'artifact_manifest.json';hist=P/'artifact_manifest_phase_RIGHT11_UART03_20261022.json'
if old.exists()and not hist.exists():hist.write_bytes(old.read_bytes())
files=[item(x)for x in sorted(P.rglob('*'))if x.is_file()and x.name!='artifact_manifest.json'];files.append(item(note))
phase=dict(status='ENGINEERING_PHASE_MANIFEST_NOT_FINAL_ROUTE_ACCEPTANCE',date='2026-10-22',files=files,excludes=['artifact_manifest.json'],currentCandidates=['RIGHT10_FULL_2L_v11.json','RIGHT10_FULL_4L_v11.json','UART_RX_receiver_bridge_2L_03.json','UART_RX_receiver_bridge_4L_03.json','remaining_returns_2L_v19_02.json','remaining_returns_4L_v19_02.json','CAN_RXD_2L_engineered_07.json'],scope='Own records complete throughCAN07/return02/BOOTactualdiagnostic/PB02; oldstage/current baselinesnot substituted fornativefinal. Note includes knownactual.1935<.3 omissionandfix. NoCadenceprocessstartedbythisagent.',nativeCurrentAtSealing='FormalremainsUSBauxb014 untilsoleexecutor publishesnewcheckpoint; try08/othersource attemptsare diagnostic/workinprogress')
old.write_text(json.dumps(phase,indent=2)+'\n',encoding='utf-8');assert all(item(Path(a['path']))['sha256']==a['sha256']for a in files)
print(json.dumps(dict(files=len(files),phase=item(old),candidate=item(P/'CAN07_returns02_manifest.json'))))