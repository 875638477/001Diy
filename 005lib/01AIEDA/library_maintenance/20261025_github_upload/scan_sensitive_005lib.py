"""Read-only secret screening. Reports paths/rules/classification, never matched data."""
import csv
import io
import json
import re
import zipfile
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(r'D:\001DIY\005lib')
OUT = Path(r'D:\001DIY\004computer\lga1700\git_upload_005lib_20261025')
TEXT_EXT = {'.txt','.md','.rst','.log','.json','.jsonl','.csv','.tsv','.xml','.yaml','.yml','.ini','.cfg','.conf','.config','.env','.bat','.cmd','.ps1','.py','.pyw','.js','.ts','.jsx','.tsx','.html','.htm','.css','.scss','.c','.h','.cpp','.hpp','.java','.go','.rs','.sh','.bash','.zsh','.il','.ils','.scr','.reg','.sql','.toml','.properties','.lic','.dat','.tcl','.skill','.envrc','.gitignore','.gitattributes','.asc','.pem','.key','.pfx','.p12','.bak','.old'}
BIN_EXT = {'.exe','.dll','.pyd','.pyc','.png','.jpg','.jpeg','.gif','.ico','.bmp','.webp','.pdf','.docx','.xlsx','.pptx','.7z','.rar','.tar','.gz','.xz','.bz2','.zst','.dra','.psm','.pad','.bsm','.ssm','.osm','.brd','.db','.db3','.dbk','.opj','.dsn','.olb','.stp','.step','.sldprt','.sldasm','.wrl','.3ds','.dwg','.dxf','.lnk','.cat','.mp4','.avi','.wav','.zip'}
MAX_TEXT = 64 * 1024 * 1024
TOKEN_RULES = [
 ('github-token', re.compile(r'(?<![\w])gh[pousr]_[A-Za-z0-9]{36,255}(?![\w])')),
 ('github-fine-grained-token', re.compile(r'github_pat_[A-Za-z0-9_]{50,255}')),
 ('openai-style-api-token', re.compile(r'(?<![\w])sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{24,255}')),
 ('aws-access-key-id', re.compile(r'(?<![A-Z0-9])(?:AKIA|ASIA)[A-Z0-9]{16}(?![A-Z0-9])')),
 ('slack-token', re.compile(r'xox[baprs]-[A-Za-z0-9-]{20,200}')),
 ('google-api-key', re.compile(r'AIza[A-Za-z0-9_-]{35}')),
 ('private-key-block', re.compile(r'-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----')),
 ('authorization-bearer', re.compile(r'(?i)\bAuthorization\s*[=:]\s*[\"\x27]?Bearer\s+[A-Za-z0-9._~+/-]{24,}')),
 ('credential-in-url', re.compile(r'(?i)\b(?:https?|ftp|postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^\s/:@]+:[^\s/@]{4,}@')),
]
ASSIGN = re.compile(r'''(?ix)\b(?:password|passwd|pwd|api[_-]?key|api[_-]?token|access[_-]?token|secret[_-]?key|client[_-]?secret|aws[_-]?secret[_-]?access[_-]?key)\b\s*[=:]\s*["']([^\r\n"']{4,256})["']''')
FLEX = re.compile(r'(?im)^[ \t]*(?:FEATURE|INCREMENT)[ \t]+\S+[ \t]+\S+[^\r\n]*(?:SIGN[ \t]*=|SIGN2[ \t]*=|[A-Fa-f0-9]{12,})')
PLACEHOLDER = re.compile(r'(?i)(example|sample|dummy|placeholder|change.?me|your[_ -]|xxxx|yyyy|zzzz|test[_ -]|^password$|^passwd$|^secret$|^token$|^none$|^null$|^true$|^false$|^default$|^1234|^abcd|^foo|^bar|^baz|^undefined$|^\*+$|^\.+$|^<|^\{|^\$|^%|^env[\[.(]|^os\.|^config\.|^self\.|^options\.|^settings\.|^args\.|^input\()')
findings = []
errors = []
stats = Counter()

def classify(path, rule, value, line):
    lower = path.lower().replace('\\','/')
    if PLACEHOLDER.search(value) or any(x in line.lower() for x in ('this is a test','for example','example only','dummy','placeholder')):
        return 'obvious-example-or-placeholder'
    if any(x in lower for x in ('/site-packages/','/dist-info/','/tooling/packages/','/tooling/pyyaml_', '/tools/python_')):
        return 'third-party-source-or-example'
    if '/tests/' in lower or '/test/' in lower or 'cleanup_review_' in lower:
        return 'test-fixture-needs-review' if rule != 'quoted-secret-assignment' else 'test-fixture-assignment'
    if rule == 'quoted-secret-assignment':
        return 'literal-secret-assignment-needs-review'
    return 'high-confidence-pattern-needs-review'

def scan_bytes(label, data):
    stats['bytes_inspected'] += len(data)
    if data.startswith((b'\xff\xfe',b'\xfe\xff')):
        text = data.decode('utf-16',errors='replace')
    elif b'\x00' in data[:8192]:
        stats['binary_skipped'] += 1
        return
    else:
        for codec in ('utf-8-sig','gb18030','cp1252'):
            try:
                text = data.decode(codec)
                break
            except UnicodeDecodeError:
                continue
        else:
            stats['undecodable_skipped'] += 1
            return
    stats['text_scanned'] += 1
    lower = text.lower()
    if not any(trigger in lower for trigger in ('ghp_','gho_','ghu_','ghs_','ghr_','github_pat_','sk-','akia','asia','xox','aiza','private key','authorization','://','password','passwd','pwd','api_key','api-key','api_token','api-token','access_token','access-token','secret_key','secret-key','client_secret','client-secret','feature','increment')):
        stats['no_sensitive_keywords'] += 1
        return
    for rule, pattern in TOKEN_RULES:
        for match in pattern.finditer(text):
            line_no = text.count('\n',0,match.start())+1
            start=text.rfind('\n',0,match.start())+1
            end=text.find('\n',match.end())
            if end<0: end=len(text)
            line=text[start:end]
            value=match.group()
            findings.append({'path':label,'line':line_no,'rule':rule,'classification':classify(label,rule,value,line)})
    for match in ASSIGN.finditer(text):
        line_no = text.count('\n',0,match.start())+1
        start=text.rfind('\n',0,match.start())+1
        end=text.find('\n',match.end())
        if end<0: end=len(text)
        line=text[start:end]
        findings.append({'path':label,'line':line_no,'rule':'quoted-secret-assignment','classification':classify(label,'quoted-secret-assignment',match.group(1),line)})
    for match in FLEX.finditer(text):
        findings.append({'path':label,'line':text.count('\n',0,match.start())+1,'rule':'flexlm-license-feature','classification':'license-content-needs-review'})

def maybe_scan(label, name, size, reader):
    suffix = Path(name).suffix.lower()
    if size > MAX_TEXT:
        stats['oversize_skipped'] += 1
        return
    if suffix in BIN_EXT:
        stats['binary_extension_skipped'] += 1
        return
    # Include known text files and unknown extensions if they pass the binary probe.
    try:
        data=reader()
        scan_bytes(label,data)
    except Exception as exc:
        errors.append({'path':label,'error_type':type(exc).__name__})

with (OUT/'upload_inventory.csv').open(encoding='utf-8-sig',newline='') as f:
    inventory=list(csv.DictReader(f))
inventory.sort(key=lambda x:(0 if x['topDirectory']=='01env' else 1 if x['topDirectory']=='01AIEDA' else 2,x['relative']))
def scan_row(row):
    path=Path(row['source'])
    label=row['relative']
    stats['files_considered']+=1
    if label.endswith('/cadence_library_maintenance_20261025_full.zip'):
        stats['user_authorized_deletion_archive_excluded']+=1
        return label
    if path.suffix.lower()=='.zip':
        stats['archives_considered']+=1
        try:
            with zipfile.ZipFile(path) as archive:
                for entry in archive.infolist():
                    if not entry.is_dir():
                        stats['archive_members_considered']+=1
                        maybe_scan(label+'!/'+entry.filename,entry.filename,entry.file_size,lambda e=entry:archive.read(e))
        except Exception as exc:
            errors.append({'path':label,'error_type':type(exc).__name__})
    else:
        maybe_scan(label,path.name,int(row['size']),path.read_bytes)
    return label

with ThreadPoolExecutor(max_workers=16) as pool:
    for completed, label in enumerate(pool.map(scan_row,inventory),1):
        if completed % 1000 == 0:
            (OUT/'sensitive_scan_progress.json').write_text(json.dumps({'stats':dict(stats),'files_completed':completed,'current_path':label,'findings':findings},ensure_ascii=False,indent=2),encoding='utf-8')

report={'generated_at_utc':datetime.now(timezone.utc).isoformat(),'source_root':str(BASE),'scope':'Nine top-level 01* directories; textual source/config/log files and first-level ZIP text members. No content excerpts stored.','stats':dict(stats),'findings':findings,'errors':errors,'classification_counts':dict(Counter(x['classification'] for x in findings)),'rule_counts':dict(Counter(x['rule'] for x in findings))}
(OUT/'sensitive_scan_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'sensitive_scan_findings.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=['path','line','rule','classification'])
    writer.writeheader()
    writer.writerows(findings)
print(json.dumps({k:v for k,v in report.items() if k!='findings'},ensure_ascii=True,indent=2))
print(json.dumps({'review_findings':[x for x in findings if x['classification'] in ('high-confidence-pattern-needs-review','literal-secret-assignment-needs-review','license-content-needs-review')]},ensure_ascii=True,indent=2))
