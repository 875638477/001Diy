"""Review original native outputs without CAD. Native pin/PAD proof is distinct from name hints."""
from pathlib import Path
from collections import defaultdict,Counter
from decimal import Decimal
import argparse,csv,hashlib,importlib.util,json,sys,copy
M=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('strict_native_schema',M/'review_global_suffix_native_chunks.py');N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
jr=N.jread;sha=N.sha;dump=N.dump
def collect(native,plan,out):
 out.mkdir(exist_ok=True,parents=True);p=jr(plan);frozen={r['stem'].lower():r for r in p['representatives']};results=[];errors=[]
 for d in sorted(native.glob('e[0-9][0-9][0-9][0-9][0-9]')):
  report=d/'launch_report.json'
  if not report.exists():continue
  rec=jr(report)
  if rec.get('exit_code')!=0 or not rec.get('complete') or rec.get('outputs')!=rec.get('expected'):
   errors.append({'directory':str(d),'status':'NATIVE_INCOMPLETE_PRESERVE_ASSET','launch_report_sha256':sha(report)});continue
  rows=jr(d/'manifest.json');actual=[]
  for r in rows:
   f=frozen[r['stem'].lower()];assert f['sha256']==r['source_sha256']==sha(f['path'])
   e=N.inspect(Path(r['audit_output']));e.update(stem=f['stem'],source=f['path'],source_sha256=f['sha256'],byte_identical_members=f['byte_identical_members'],family=f.get('family'),canonical_candidate=f.get('canonical_candidate'))
   actual.append(e);results.append(e)
  dump(out/(d.name+'_SCHEMA_GEOMETRY.json'),actual)
 summary={'status':'ALL_COMPLETE_NATIVE_GRAPHS_REVIEWED' if not errors and len(results)==len(frozen) else 'COMPLETE_NATIVE_GRAPHS_REVIEWED_WITH_EXPLICIT_PRESERVE_EXCEPTIONS','planned':len(frozen),'reviewed':len(results),'native_exceptions':errors,'plan':str(plan),'plan_sha256':sha(plan),'runner_report':str(native/'report.json'),'runner_report_sha256':sha(native/'report.json'),'normalization':results[0]['graph_normalization'] if results else None,'unresolved_issues':[{ 'stem':e['stem'],'issues':e['issues']} for e in results if e['issues']],'external_PAD_XML_gate':'Run bind_current_global_pad_xml.py with these e*_SCHEMA_GEOMETRY.json files and the exact public guard; no deletion approval from this report.'}
 dump(out/'NATIVE_SET_REVIEW.json',summary);return results,summary
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--plan',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();res,summary=collect(a.native,a.plan,a.out);print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
