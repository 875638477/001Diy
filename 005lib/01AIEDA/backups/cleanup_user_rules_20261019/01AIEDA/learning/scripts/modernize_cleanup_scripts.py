"""Back up and modernize explicitly inventoried cleanup BATs; never run them."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[3]
RECORDS=ROOT/'01AIEDA'
STAGE=RECORDS/'learning/staging/cleanup_review_20261019'
BACKUP=RECORDS/'backups/cleanup_scripts_20261019'
payload=(RECORDS/'learning/scripts/eda_cleanup_payload.ps1').read_text(encoding='utf-8-sig')
inventory=json.loads((STAGE/'family_inventory.json').read_text(encoding='utf-8-sig'))
paths=[r['path'] for r in inventory['scripts']]+['0KEIL.bat','04keil_lib/KEIL.bat']
assert len(set(paths))==21
header='''@echo off
chcp 65001 >nul
setlocal DisableDelayedExpansion
rem UTF-8 without BOM / CRLF. Clean the script directory only.
rem Options: /preview /history /build /help. Never clean 01AIEDA or 01env.
rem Default includes journals/build output and proven redundant backups/project wrappers.
set "EDA_CLEAN_SELF=%~f0"
set "EDA_CLEAN_ROOT=%~dp0"
set "EDA_CLEAN_ARG_1=%~1"
set "EDA_CLEAN_ARG_2=%~2"
set "EDA_CLEAN_ARG_3=%~3"
set "EDA_CLEAN_ARG_4=%~4"
set "EDA_CLEAN_ARG_5=%~5"
set "EDA_CLEAN_ARG_6=%~6"
set "EDA_CLEAN_ARG_7=%~7"
set "EDA_CLEAN_ARG_8=%~8"
set "EDA_CLEAN_ARG_9=%~9"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -Command "$text=[IO.File]::ReadAllText($env:EDA_CLEAN_SELF,[Text.Encoding]::UTF8);$marker='#__EDA_CLEAN_POWERSHELL__';& ([ScriptBlock]::Create($text.Substring($text.LastIndexOf($marker)+$marker.Length)))"
exit /b %errorlevel%
#__EDA_CLEAN_POWERSHELL__
'''
entries=[]
for rel in paths:
    target=(ROOT/rel).resolve()
    assert target.is_relative_to(ROOT) and target.is_file()
    original=target.read_bytes()
    saved=BACKUP/rel
    saved.parent.mkdir(parents=True,exist_ok=True)
    if saved.exists():
        legacy=saved.read_bytes()
    else:
        saved.write_bytes(original);legacy=original
    try:oldtext=legacy.decode('utf-8-sig')
    except UnicodeDecodeError:oldtext=legacy.decode('gb18030')
    templates=[name for name in ['BOM.txt','reports.txt','drill4noet.txt'] if re.search(r'^\s*copy\s+[^\r\n]*'+re.escape(name),oldtext,re.M|re.I)]
    extraction=bool(re.search(r'^(?!\s*::)[^\r\n]*WinRAR[^\r\n]*\s+x\s',oldtext,re.M|re.I))
    config='$script:CleanupTemplates=@('+','.join(repr(n) for n in templates)+')\n'
    config+='$script:CleanupHadExtraction=$'+str(extraction).lower()+'\n'
    content=header+config+payload
    data=content.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8')
    target.write_bytes(data)
    entries.append(dict(path=rel,backup=str(saved.relative_to(RECORDS)),before_sha256=hashlib.sha256(legacy).hexdigest(),after_sha256=hashlib.sha256(data).hexdigest(),encoding='UTF-8 without BOM',newlines='CRLF',copy_missing_templates=templates,old_automatic_extraction_removed=extraction))
(STAGE/'migration_manifest.json').write_text(json.dumps({'scope':str(ROOT),'count':len(entries),'cleanup_executed':False,'entries':entries},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'updated':len(entries),'cleanup_executed':False,'backup':str(BACKUP)},ensure_ascii=True))
