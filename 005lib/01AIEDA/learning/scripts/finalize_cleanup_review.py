"""Verify final hashes/encoding and preview the four explicitly synced copies."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime,hashlib,json,os,re,subprocess
ROOT=Path(__file__).resolve().parents[3]
RECORDS=ROOT/'01AIEDA'
STAGE=RECORDS/'learning/staging/cleanup_review_20261019'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name): return json.loads((STAGE/name).read_text(encoding='utf-8-sig'))
local=read('migration_manifest.json')
external=read('external_sync_result.json')
preview=read('entrypoint_verification.json')
FINAL=STAGE/'aggressive'
FINAL.mkdir(parents=True,exist_ok=True)
tests_path=max((FINAL/'tests').glob('run_*/results.json'),key=lambda p:p.stat().st_mtime)
tests=json.loads(tests_path.read_text(encoding='utf-8'))
payload=RECORDS/'learning/scripts/eda_cleanup_payload.ps1'
assert tests['failures']==0 and tests['production_payload_sha256'].lower()==sha(payload)
assert preview['all_preview_passed'] and preview['entrypoints']==21
for name,digest in preview['critical_file_hashes'].items(): assert sha(Path(name))==digest,name
entries=[]
for entry in local['entries']:
    path=ROOT/entry['path'];saved=RECORDS/entry['backup']
    assert sha(saved)==entry['before_sha256']
    entries.append((path,entry['after_sha256']))
for entry in external:
    assert sha(Path(entry['backup'])).upper()==entry['before_sha256']
    entries.append((Path(entry['target']),entry['after_sha256']))
for path,digest in entries:
    data=path.read_bytes();data.decode('utf-8',errors='strict')
    assert not data.startswith(b'\xef\xbb\xbf') and b'\n' not in data.replace(b'\r\n',b'')
    assert sha(path).lower()==digest.lower(),path

def external_preview(entry):
    path=Path(entry['target'])
    command=f'"{os.environ["COMSPEC"]}" /d /v:off /s /c ""{path}" /preview"'
    p=subprocess.run(command,cwd=STAGE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
    out=p.stdout.decode('utf-8',errors='strict');err=p.stderr.decode('utf-8',errors='strict')
    assert p.returncode==0 and 'removed=0;' in out and 'preview=True' in out,(path,out,err)
    return dict(path=str(path),exit_code=p.returncode,cleanup_executed=False,stdout=out,stderr=err)
with ThreadPoolExecutor(max_workers=4) as pool: external_results=list(pool.map(external_preview,external))
(FINAL/'external_preview_verification.json').write_text(json.dumps(dict(entrypoints=4,all_preview_passed=True,results=external_results),ensure_ascii=False,indent=2),encoding='utf-8')
documents=[RECORDS/'EDA.md',RECORDS/'\u8bfe\u7a0b\u7d22\u5f15.md',RECORDS/'learning/notes/cleanup_file_policy_20261019.md',RECORDS/'learning/notes/cleanup_aggressive_20261019.md']
broken=[]
for doc in documents:
    for dest in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',doc.read_text(encoding='utf-8-sig')):
        dest=dest.split('#',1)[0].strip('<>')
        if not dest or re.match(r'^[A-Za-z]+://',dest): continue
        target=(doc.parent/dest).resolve()
        if target in ((STAGE/'final_verification.json').resolve(),(FINAL/'final_verification.json').resolve()): continue
        if not target.exists(): broken.append(dict(document=str(doc),target=dest))
assert not broken,broken
report=dict(status='PASS',createdUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            entrypoints=25,workspace_entrypoints=21,external_entrypoints=4,
            all_UTF8_without_BOM=True,all_CRLF=True,all_25_CMD_previews_passed=True,
            isolated_checks=tests['checks'],isolated_failures=tests['failures'],
            isolated_report=str(tests_path),isolated_skips=tests['skips'],
            payload_sha256=sha(payload),critical_files_unchanged=preview['critical_files_unchanged'],
            broken_document_links=broken,real_user_cleanup_executed=False,
            scripts=[dict(path=str(path),sha256=sha(path)) for path,_ in entries])
(FINAL/'final_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('scripts','isolated_skips')},ensure_ascii=True))
