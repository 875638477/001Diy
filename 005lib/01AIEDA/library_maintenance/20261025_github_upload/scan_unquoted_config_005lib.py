"""Supplementary read-only check for unquoted configuration credentials."""
import csv, json, re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
OUT=Path(r'D:\001DIY\004computer\lga1700\git_upload_005lib_20261025')
EXT={'.bat','.cmd','.ps1','.sh','.env','.ini','.cfg','.conf','.config','.json','.xml','.yaml','.yml','.toml','.properties','.txt','.md',''}
PAT=re.compile(r'(?im)^[ \t]*(?:setx?[ \t]+|export[ \t]+)?["\x27]?(?P<name>[A-Za-z0-9_]*(?:PASSWORD|PASSWD|API_KEY|API_TOKEN|ACCESS_TOKEN|CLIENT_SECRET|SECRET_KEY|GITHUB_TOKEN|GH_TOKEN|AWS_SECRET_ACCESS_KEY)[A-Za-z0-9_]*)["\x27]?[ \t]*[:=][ \t]*(?P<value>[^\r\n;#]+)')
PLACE=re.compile(r'(?i)(example|sample|dummy|placeholder|change.?me|your[_ -]|xxxx|test|password|secret|token|none|null|false|true|default|1234|abcd|^foo|^bar|^<|^\{|^\$|^%|^env[\[.(]|^os\.|^config\.|^self\.|^options\.|^settings\.|^args\.|^input\(|^get|^function|^read|^find|^string|^kwargs|^parser|^type\()')
findings=[]
files=0
with (OUT/'upload_inventory.csv').open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
def scan_row(row):
    global files
    path=Path(row['source'])
    if path.suffix.lower() not in EXT or int(row['size'])>8*1024*1024:return
    data=path.read_bytes()
    if data.startswith((b'\xff\xfe',b'\xfe\xff')): text=data.decode('utf-16',errors='replace')
    elif b'\x00' in data[:4096]:return
    else: text=data.decode('utf-8-sig',errors='replace')
    files+=1
    if not any(trigger in text.lower() for trigger in ('password','passwd','api_key','api_token','access_token','client_secret','secret_key','github_token','gh_token','aws_secret_access_key')):return
    for m in PAT.finditer(text):
        value=m.group('value').strip().strip('"\x27').strip()
        if not value: continue
        relative=row['relative']
        classification='unquoted-assignment-needs-review'
        if PLACE.search(value): classification='obvious-placeholder-or-code-expression'
        elif '/tooling/' in relative or '/tools/python_' in relative or '/tests/' in relative: classification='third-party-code-or-test-fixture'
        findings.append({'path':relative,'line':text.count('\n',0,m.start())+1,'rule':'unquoted-config-secret-assignment','classification':classification})
with ThreadPoolExecutor(max_workers=16) as pool:
    list(pool.map(scan_row,rows))
report={'files_scanned':files,'findings':findings}
(OUT/'sensitive_unquoted_config_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
