from pathlib import Path
import json,hashlib,datetime,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA');L=R/'learning/examples/lesson60_20261023'
for name in ['review','backups','scripts','sources','inventory','package','native','sealed_snapshots']:(L/name).mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
jk=R/'learning/examples/lessonJK_51_59_20261022'
critical=[(jk/'artifact_manifest.json','D20CFAA4DE732D53DC980270F941B8EB582776DD294140AD10748DD48AEFC794'),(jk/'native/4L/JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd','471176A9B25BA8DEF9F117AEFB1E9220CBCBEBBAC5191BCBC6E228F52831F3F9')]
checks=[{'path':str(p),'exists':p.exists(),'expectedSHA256':h,'actualSHA256':sha(p)if p.exists()else None}for p,h in critical]
for c in checks:c['matched']=c['actualSHA256']==c['expectedSHA256']
for name in ['EDA.md','\u8bfe\u7a0b\u7d22\u5f15.md']:
 p=R/name;q=L/'backups'/name
 if not q.exists():shutil.copy2(p,q)
record={'createdUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'userReported':'abnormal shutdown; continue lesson60','observedLesson60StateBeforeRecovery':'directory absent; no lesson60 products persisted','priorJKCriticalChecks':checks,'cadenceProcessObservation':{'pid':3840,'name':'allegro','ownership':'not created by this resumed task; treat as user-owned and leave untouched'},'processQueryLimits':'CIM denied in ordinary sandbox; Get-Process read ID/start/path succeeded. No UI automation or killing attempted.','secondComputerTest':'NOT_PERFORMED','recovery':'Resume from persisted JK and create new isolated lesson60, not claim pre-crash delegates executed.'}
(L/'review/recovery_after_shutdown.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'recoveredL60Directory':str(L),'priorCriticalMatched':all(c['matched']for c in checks),'checks':checks}))
