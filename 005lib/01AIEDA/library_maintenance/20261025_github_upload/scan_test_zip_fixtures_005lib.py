"""Finish raw-text checks for intentionally invalid ZIP test fixtures."""
import json
from pathlib import Path
OUT=Path(r'D:\001DIY\004computer\lga1700\git_upload_005lib_20261025')
namespace={}
source=(OUT/'scan_sensitive_005lib.py').read_text(encoding='utf-8')
exec(compile(source.split("with (OUT/'upload_inventory.csv')")[0],'<scanner-definitions>','exec'),namespace)
report=json.loads((OUT/'sensitive_scan_report.json').read_text(encoding='utf-8'))
resolved=[]
remaining=[]
for entry in report['errors']:
    path=namespace['BASE']/entry['path']
    if entry['error_type']=='BadZipFile' and '/cleanup_review_' in entry['path'] and path.stat().st_size<=1024:
        data=path.read_bytes()
        namespace['scan_bytes'](entry['path'],data)
        resolved.append({'path':entry['path'],'bytes':len(data),'classification':'tiny-nonzip-test-fixture-raw-text-scanned'})
    else:remaining.append(entry)
report['errors']=remaining
report['test_zip_fixtures_raw_text_scanned']=resolved
report['findings'].extend(namespace['findings'])
report['stats']['test_zip_fixtures_raw_text_scanned']=len(resolved)
(OUT/'sensitive_scan_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'sensitive_test_zip_report.json').write_text(json.dumps({'stats':dict(namespace['stats']),'resolved':resolved,'findings':namespace['findings']},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'resolved_test_fixtures':len(resolved),'remaining_errors':len(remaining),'new_findings':namespace['findings']},ensure_ascii=True,indent=2))
