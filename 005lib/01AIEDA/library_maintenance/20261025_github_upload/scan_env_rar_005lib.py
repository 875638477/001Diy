"""List, validate, isolate, and scan the small env RAR using installed UnRAR."""
import json, re, subprocess
from pathlib import Path, PureWindowsPath
OUT=Path(r'D:\001DIY\004computer\lga1700\git_upload_005lib_20261025')
ARCHIVE=Path(r'D:\001DIY\005lib\01env\01env.rar')
UNRAR=Path(r'C:\Program0\WinRAR\UnRAR.exe')
DEST=OUT/'rar_env_isolated'
listing=subprocess.run([str(UNRAR),'lt','-c-',str(ARCHIVE)],capture_output=True,timeout=10,check=True).stdout.decode('gb18030')
members=[]
for block in listing.split('\r\n\r\n'):
    fields={m.group(1).strip():m.group(2).strip() for m in re.finditer(r'^\s*([^:\r\n]+):[ \t]*(.*)$',block,re.M)}
    if '\u540d\u79f0' in fields and '\u5927\u5c0f' in fields:
        name=fields['\u540d\u79f0']
        size=int(fields['\u5927\u5c0f'])
        attrs=fields.get('\u5c5e\u6027','')
        kind=fields.get('\u7c7b\u578b','')
        p=PureWindowsPath(name)
        if p.is_absolute() or p.drive or any(part=='..' for part in p.parts) or ':' in name or name.startswith(('/','\\')):
            raise RuntimeError('Unsafe archive member path')
        if kind not in ('\u6587\u4ef6','File') or not attrs or any(ch not in '.ARSH' for ch in attrs):
            raise RuntimeError('Unexpected member type or attributes')
        members.append({'name':name,'size':size,'attributes':attrs,'type':kind})
if not members or len(members)!=42 or sum(m['size'] for m in members)>=10*1024*1024:
    raise RuntimeError('Unexpected archive count or expanded size')
DEST.mkdir(exist_ok=False)
subprocess.run([str(UNRAR),'x','-idq','-o-','-y',str(ARCHIVE),str(DEST)+'\\'],capture_output=True,timeout=15,check=True)
extracted=list(DEST.rglob('*'))
if any(p.is_symlink() or p.stat().st_file_attributes & 0x400 for p in extracted):
    raise RuntimeError('Unexpected extracted reparse point')
files=[p for p in extracted if p.is_file()]
if len(files)!=len(members) or sum(p.stat().st_size for p in files)!=sum(m['size'] for m in members):
    raise RuntimeError('Extracted count/size mismatch')
namespace={}
source=(OUT/'scan_sensitive_005lib.py').read_text(encoding='utf-8')
exec(compile(source.split("with (OUT/'upload_inventory.csv')")[0],'<scanner-definitions>','exec'),namespace)
for path in files:
    namespace['maybe_scan']('01env/01env.rar!/'+str(path.relative_to(DEST)).replace('\\','/'),path.name,path.stat().st_size,path.read_bytes)
config_namespace={}
config_source=(OUT/'scan_unquoted_config_005lib.py').read_text(encoding='utf-8')
exec(compile(config_source.split("with (OUT/'upload_inventory.csv')")[0],'<config-scanner-definitions>','exec'),config_namespace)
unquoted=[]
for path in files:
    if path.suffix.lower() in namespace['BIN_EXT']:continue
    data=path.read_bytes()
    text=data.decode('utf-16',errors='replace') if data.startswith((b'\xff\xfe',b'\xfe\xff')) else data.decode('utf-8-sig',errors='replace')
    for match in config_namespace['PAT'].finditer(text):
        unquoted.append({'path':'01env/01env.rar!/'+str(path.relative_to(DEST)).replace('\\','/'),'line':text.count('\n',0,match.start())+1,'rule':'unquoted-config-secret-assignment','classification':'needs-review'})
report={'archive':'01env/01env.rar','status':'text-content-reviewed','tool':str(UNRAR),'listing_members':members,'expanded_bytes':sum(m['size'] for m in members),'isolated_extract_directory':str(DEST),'source_modified':False,'stats':dict(namespace['stats']),'findings':namespace['findings'],'unquoted_config_findings':unquoted,'errors':namespace['errors'],'limitations':['Binary EXE/shortcut members omitted from textual secret screening.']}
(OUT/'sensitive_env_rar_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
