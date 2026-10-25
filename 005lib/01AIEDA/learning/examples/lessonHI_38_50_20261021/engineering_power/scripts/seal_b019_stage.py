from pathlib import Path
import hashlib,json,datetime
O=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021/engineering_power');H=O.parent;dest=O/'b019_stage_manifest.json';files=[]
def item(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest().upper(),bytes=p.stat().st_size)
for p in sorted(O.rglob('*')):
 if p.is_file()and p!=dest:
  q=item(p);q['path']=str(p.relative_to(O)).replace('\\','/');files.append(q)
inputs=[]
for v in['2L','4L']:
 cp=H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING'
 for name in['normalized.json','networks.json','base_net_rules.json']:inputs.append(item(cp/name))
 network=json.loads((cp/'networks.json').read_text());assert hashlib.sha256(Path(network['board']).read_bytes()).hexdigest().upper()==network['sha256'].upper();inputs.append(item(Path(network['board'])))
inputs.append(item(H/'review/b019_native_report.json'));note=O.parents[2]/'notes/lessonHI_power_20261021.md'
body=dict(status='FROZEN_RECORD_INTEGRITY_THROUGH_B019_REVIEW_NOT_WHOLE_BOARD_OR_SI_ACCEPTANCE',created=datetime.datetime.now().astimezone().isoformat(),root=str(O),files=files,inputs=inputs,masterNote=item(note),scope='Ownnote1-41; actualb018reference/b01940checks/actualmaps, failedandunadoptedPA9RXandreturnbridgecomparisons. ParentEDA/indexnotedited.',nativeStage='Bothboards7Southjoins;65nonUSBscopedzero;465cumulativeproof/272identity/GND/HSE;USB4andwholeDRCpending',frozenHistoricalManifestsPreserved=['artifact_manifest.json','north51_stage_manifest.json','CAN07_returns02_manifest.json'],liveDocumentsMayReceiveNewStages='Futurechangesmustmakenewstageorrecordsupersession; thismanifestremainsunchanged.',excludes=['this manifest itself'])
dest.write_text(json.dumps(body,ensure_ascii=False,indent=2)+'\n',encoding='utf8');check=json.loads(dest.read_text());assert all(hashlib.sha256((O/a['path']).read_bytes()).hexdigest().upper()==a['sha256']for a in check['files']);assert all(hashlib.sha256(Path(a['path']).read_bytes()).hexdigest().upper()==a['sha256']for a in check['inputs']);print(json.dumps(dict(path=str(dest),files=len(files),inputs=len(inputs),sha256=hashlib.sha256(dest.read_bytes()).hexdigest().upper(),allSHARechecked=True)))
