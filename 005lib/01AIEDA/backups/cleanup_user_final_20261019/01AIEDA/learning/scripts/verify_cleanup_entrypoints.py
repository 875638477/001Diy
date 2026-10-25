"""Run only preview/help for deployed BATs; verify encoding and preserved inputs."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,os,subprocess

ROOT=Path(__file__).resolve().parents[3]
STAGE=ROOT/'01AIEDA/learning/staging/cleanup_review_20261019'
manifest=json.loads((STAGE/'migration_manifest.json').read_text(encoding='utf-8'))
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
important=[p for p in (ROOT/'01env').iterdir() if p.is_file()]
important += [p for p in (ROOT/'01AIEDA/learning/examples/de_15_26_20261019/native').iterdir() if p.is_file() and p.suffix.lower() in ('.dsn','.opj','.dbk')]
important += [ROOT/'01AIEDA/learning/examples/de_15_26_20261019/BOM_baseline.csv',ROOT/'01AIEDA/learning/examples/de_15_26_20261019/BOM_eco.csv']
before={str(p):sha(p) for p in important}

def preview(entry):
    path=ROOT/entry['path'];data=path.read_bytes()
    data.decode('utf-8',errors='strict')
    assert not data.startswith(b'\xef\xbb\xbf')
    assert b'\n' not in data.replace(b'\r\n',b'')
    assert sha(path)==entry['after_sha256']
    command=f'"{os.environ["COMSPEC"]}" /d /v:off /s /c ""{path}" /preview"'
    result=subprocess.run(command,cwd=STAGE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=40)
    stdout=result.stdout.decode('utf-8',errors='strict');stderr=result.stderr.decode('utf-8',errors='strict')
    assert result.returncode==0,(entry['path'],result.returncode,stdout,stderr)
    assert f'Target (script directory): {path.parent}' in stdout,(path,stdout)
    assert 'removed=0;' in stdout and 'preview=True' in stdout
    return dict(path=entry['path'],exit_code=result.returncode,encoding='UTF-8 without BOM',newlines='CRLF',stdout=stdout,stderr=stderr)

with ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(preview,manifest['entries']))
assert all(sha(Path(path))==digest for path,digest in before.items())
special=STAGE/'entrypoint_path_tests'/'\u4e2d\u6587 ! & (test)'
special.mkdir(parents=True,exist_ok=True)
bat=special/'\u6e05\u7406 ! & (demo).bat'
bat.write_bytes((ROOT/'0000Ad_Keil_Cadence_dat_iar_txt.bat').read_bytes())
command=f'"{os.environ["COMSPEC"]}" /d /v:off /s /c ""{bat}" /help"'
result=subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=20)
assert result.returncode==0,(result.returncode,result.stdout,result.stderr)
assert b'Usage:' in result.stdout
report=dict(entrypoints=len(results),all_preview_passed=True,real_user_cleanup_executed=False,
            critical_files_unchanged=len(before),critical_file_hashes=before,
            special_CMD_path_test=dict(path=str(bat),exit_code=result.returncode),results=results)
(STAGE/'entrypoint_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('critical_file_hashes','results')},ensure_ascii=True))
