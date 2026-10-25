from pathlib import Path
import json,hashlib,subprocess,sys,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA');L=R/'learning/examples/lesson60_20261023';S=R/'learning/skills/cadence17-learning';p=S/'scripts/preflight.py'
old=p.read_bytes();oldsha=hashlib.sha256(old).hexdigest().upper();backup=L/'backups/preflight_before_forward_fix.py';assert not backup.exists();backup.write_bytes(old)
s=old.decode('utf8');needle='  out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text,encoding="utf8")'
replacement='  if out.suffix.lower()!=".json":ap.error("--out must name a new JSON report")\n  if out.exists():ap.error("--out already exists; refuse overwrite")\n  out.parent.mkdir(parents=True,exist_ok=True)\n  with out.open("x",encoding="utf8") as f:f.write(text)'
assert needle in s;s=s.replace(needle,replacement);p.write_text(s,encoding='utf8')
skill=S/'SKILL.md';body=skill.read_text(encoding='utf8');body+='\n可选--out只新建JSON报告并拒绝覆盖已有文件；不得把报告输出指向EDA、索引、源设计或历史证据。预检退出0只代表学习文件和固定fixture身份，不代表Cadence程序/许可/GUI就绪。\n';skill.write_text(body,encoding='utf8')
sentinel=L/'review/preflight_existing_sentinel.json';sentinel.write_text('{"sentinel":"keep unchanged"}\n',encoding='utf8');before=sentinel.read_bytes();output=L/'review/preflight_created_current.json';assert not output.exists()
cases=[('current',[str(R)],None,0),('missing',[str(L/'review/no_such_learning_root')],None,2),('refuse_existing',[str(R)],sentinel,2),('create_report',[str(R)],output,0)]
results=[]
for label,roots,out,expected in cases:
 cmd=[sys.executable,'-X','utf8',str(p),'--root',roots[0],'--cadence-root',r'C:\Program0\Cadence\SPB172']
 if out:cmd+=['--out',str(out)]
 r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8',timeout=30);d=json.loads(r.stdout)if r.stdout.strip()else None;passed=r.returncode==expected
 if label=='refuse_existing':passed=passed and sentinel.read_bytes()==before and 'refuse overwrite'in r.stderr
 if label=='create_report':passed=passed and output.exists()and json.loads(output.read_text(encoding='utf8'))==d
 results.append({'case':label,'exitCode':r.returncode,'expectedExitCode':expected,'passed':passed,'stdoutJSON':d,'stderr':r.stderr})
report={'oldSourceSHA256':oldsha,'oldByteSnapshot':str(backup),'newSourceSHA256':hashlib.sha256(p.read_bytes()).hexdigest().upper(),'fix':'Only new JSON reports using exclusive creation; any existing target is refused without writing','checks':results,'passed':all(x['passed']for x in results)}
(L/'review/preflight_forward_fix_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'oldSHA':oldsha,'newSHA':report['newSourceSHA256'],'passed':report['passed'],'cases':len(results)}))
