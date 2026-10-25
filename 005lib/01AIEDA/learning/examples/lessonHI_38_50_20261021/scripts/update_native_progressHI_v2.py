from pathlib import Path
import json,re,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
attempts=[]
for folder in sorted((R/'logs').iterdir()):
 if not folder.is_dir() or not (folder/'launch.json').is_file():continue
 launch=json.loads((folder/'launch.json').read_text())
 stdout=(folder/'stdout.txt').read_text(errors='replace') if (folder/'stdout.txt').is_file() else ''
 batch=(folder/'hi_batch_execution.txt').read_text(errors='replace') if (folder/'hi_batch_execution.txt').is_file() else ''
 native=(folder/'native_summary.txt').read_text(errors='replace') if (folder/'native_summary.txt').is_file() else ''
 drc=re.search(r'drcs=(\d+)',native)
 complete=re.search(r'HI_BATCH_COMPLETED drcCount=(\d+) status=(\S+) board="([^"]+)"',batch)
 x={'log':str(folder),'completed':launch.get('completed'),'processExit':launch.get('exitCode'),'sourceSHAUnchanged':launch.get('beforeSHA256')==launch.get('afterSHA256'),'stdoutErrors':[line for line in stdout.splitlines() if '*Error*' in line],'sourceBoard':launch.get('args',[])[-1],'readonly':launch.get('readonly'),'nativeDRC':int(drc[1]) if drc else None}
 if complete:
  p=Path(complete[3]);x.update({'candidateStatus':complete[2],'candidateDRC':int(complete[1]),'candidateBoard':str(p),'candidateSHA256':hashlib.sha256(p.read_bytes()).hexdigest().upper() if p.is_file() else None,'endpointProofs':len(re.findall(r'HI_ENDPOINT_PROOF',batch))})
 h=folder/'hi_hse_isolation_challenge.txt'
 if h.is_file():
  txt=h.read_text(errors='replace');x['hseIsolationChallengeComplete']=('HSE_ISOLATION_NEGATIVE_TEST_COMPLETE_NO_SAVE' in txt or 'HSE_ISOLATION_GRAPH_NEGATIVE_TEST_COMPLETE_FULL_DRC_REQUIRED' in txt);x['hseIsolationChallengeScope']='Actual single-anchor via deletion, local static plane/cap/3guard remain mutually connected, local graph loses global VSS/case; global graph retains case/VSS; rollback restores.'
 x['expectedForcedErrorPilot']=folder.name=='drc_bulk_control_pilot_4L_01'
 x['fieldSolutionFailedMessages']=stdout.count('Field solution failed')
 if (folder/'extended_completion_observed.json').is_file():x['extendedCompletionObservation']=json.loads((folder/'extended_completion_observed.json').read_text())
 attempts.append(x)
d={'status':'WORK_IN_PROGRESS_NOT_FINAL_ACCEPTANCE','current':{v:json.loads((R/f'inventory/current_{v}.json').read_text()) for v in ['4L','2L']},'nativeAttempts':attempts,'limits':['Current aliases point only to separate readonly, zero-DRC checkpoints. Failed candidates remain historical and must not replace current.','Root/engineering geometry, return-path and actual net-rule review remain required; native DRC0/connectivity alone are insufficient.','Full 69-net route is still incomplete. No GUI operation was verified.']}
(R/'review/native_progress.json').write_text(json.dumps(d,indent=2),encoding='utf8')
print(json.dumps({'attempts':len(attempts),'current':{v:d['current'][v]['summary'] for v in d['current']}},indent=2))
