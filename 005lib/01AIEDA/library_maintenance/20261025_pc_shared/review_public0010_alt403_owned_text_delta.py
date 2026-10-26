"""Independent exact logical572 text multiset delta from actualv4 native metadata."""
from pathlib import Path
from collections import Counter,defaultdict
from decimal import Decimal
import hashlib,json,sys
M=Path(__file__).parent;D=M/'public0010_alt403_run13_v4';OUT=M/'public0010_alt403_text_delta13';OUT.mkdir(exist_ok=False)
sys.path.insert(0,'D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025');from sexpr import parse_many,attrs,Atom
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def val(x):
 if isinstance(x,Decimal):return {'number':str(x.normalize())}
 if isinstance(x,Atom):return {'atom':str(x)}
 if isinstance(x,list):return [val(y) for y in x]
 return {'string':x}
key=lambda x:json.dumps(val(x),sort_keys=True,separators=(',',':'))
def main():
 before={};after=defaultdict(list)
 for line in (D/'SOURCE_ALL593_TEXT_PROPS.ilist').read_text('utf-8').splitlines():
  r=parse_many(line)[0]
  if r[0]=='symbol' and r[1][0]=='LOGICAL':before[r[1][1]]=r[2]
 for line in (D/'texts_full_after.ilist').read_text('utf-8').splitlines():
  r=parse_many(line)[0];a=attrs(r[1]);after[r[0]].append([a['text'],a['xy'],a['rotation'],a['isMirrored'],a['justify'],a['layer'],a['textBlock'],r[2]])
 assert len(before)==572 and set(after)<=set(before)
 changes=[]
 for ref,rows in before.items():
  old,new=Counter(map(key,rows)),Counter(map(key,after[ref]));removed=old-new;added=new-old
  if removed or added:changes.append({'ref':ref,'before_count':len(rows),'after_count':len(after[ref]),'removed':[{'record':json.loads(k),'count':v} for k,v in removed.items()],'added':[{'record':json.loads(k),'count':v} for k,v in added.items()]})
 layers=Counter()
 for r in changes:
  for a in r['added']:layers[str(a['record'][5])]+=a['count']
 report={'status':'EXACT_NATIVE_TEXT_DIFFERENCES_NOT_APPROVED','source_snapshot':str(D/'SOURCE_ALL593_TEXT_PROPS.ilist'),'source_snapshot_sha256':sha(D/'SOURCE_ALL593_TEXT_PROPS.ilist'),'actual_after_native_metadata':str(D/'texts_full_after.ilist'),'actual_after_native_metadata_sha256':sha(D/'texts_full_after.ilist'),'scope':'572 logical component owned texts; nativev4 after metadata excludes21nonlogical symbols so those require separate freshsnapshot. All numeric values compared exactly as numbers; no coordinate tolerance or AUTOSILK whitelist.','changed_refs':len(changes),'removed_text_records':sum(sum(x['count'] for x in r['removed']) for r in changes),'added_text_records':sum(sum(x['count'] for x in r['added']) for r in changes),'added_layers':dict(layers),'changes':changes,'public_modified':False}
 p=OUT/'EXACT_LOGICAL572_TEXT_DELTA.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='changes'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
