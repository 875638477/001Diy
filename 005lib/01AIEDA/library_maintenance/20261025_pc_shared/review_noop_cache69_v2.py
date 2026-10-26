"""Read-only complete actual-cache no-op review; no library equivalence claim."""
from pathlib import Path
import sys,csv,re,json,hashlib,collections
G=Path(r'D:\001DIY\004computer\lga1700\cadence_geometry_merge_20261025');sys.path.insert(0,str(G))
import compare_native_geometry as ng
from sexpr import parse_many,Atom
M=Path(__file__).parent;A=M/'w/public_brd0010_source_allcache13';B=M/'w/public_brd0010_noop_allcache13';O=M/'w/public_brd0010_noop_cache_review13_v2'
assert not O.exists();O.mkdir()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def canon_raw(path):
 rows=parse_many(path.read_text(encoding='utf-8-sig'));handles={};counts=collections.Counter()
 # The whole-board designprops/environment are not cached-definition fields.
 # All physical cache records, full attrs, all props, figures, and text blocks
 # remain; only unstable native memory addresses are alpha-renamed in place.
 keep=[r for r in rows if r[0] in ('meta','step','selected','object','figure','textblock','complete')]
 def norm(v):
  if isinstance(v,list):return [norm(x) for x in v]
  if isinstance(v,Atom) and re.fullmatch(r'(?:dbid|pad|propList):[0-9A-Fa-f]+|_axlPath@0x[0-9A-Fa-f]+',str(v)):
   k=str(v);prefix=k.split(':')[0] if ':' in k else '_axlPath'
   if k not in handles:counts[prefix]+=1;handles[k]=prefix+':ALPHA'+str(counts[prefix])
   return ['NATIVE_HANDLE',handles[k]]
  if isinstance(v,Atom):return ['ATOM',str(v)]
  return ['SCALAR',str(v)]
 value=norm(keep);raw=json.dumps(value,sort_keys=True,separators=(',',':'));return hashlib.sha256(raw.encode()).hexdigest().upper(),value,len(keep)
def manifest(p):
 with (p/'manifest.tsv').open(encoding='utf-8-sig',newline='') as f:return {r['name']:r for r in csv.DictReader(f,delimiter='\t')}
a=manifest(A);b=manifest(B);assert a.keys()==b.keys() and len(a)==69
native={};padnames=set()
for name in a:
 for side,rows in [('source',a),('candidate',b)]:
  obj=ng.Native(rows[name]['file']);native[side,name]=obj
  padnames.update(str(attrs.get('name')) for attrs,props in obj.nodes.values() if attrs.get('objType')=='padstack')
# The primary complete raw graph gate above preserves every embedded PAD
# attribute. This secondary graph test only compares source vs candidate;
# external public PAD compatibility is deliberately outside its scope.
ng.PAD_PUBLIC={n.casefold():'SAME_EXTERNAL_REFERENCE_NOT_A_LIBRARY_COMPATIBILITY_ASSERTION' for n in padnames}
results=[];allgood=True
for name in a:
 p=Path(a[name]['file']);q=Path(b[name]['file']);s1,c1,n1=canon_raw(p);s2,c2,n2=canon_raw(q)
 x=native['source',name].signature();y=native['candidate',name].signature();raw=s1==s2;graph=x['signature']==y['signature'] and not x['issues'] and not y['issues'];allgood &= raw and graph
 if not raw:(O/(hashlib.sha256(name.encode()).hexdigest()[:10]+'.raw_alpha_diff.json')).write_text(json.dumps(dict(name=name,source=c1,candidate=c2),indent=1),encoding='utf-8')
 results.append(dict(name=name,complete_raw_all_cache_fields_exact=raw,semantic_graph_exact=graph,source_records=n1,candidate_records=n2,source_graph=x,candidate_graph=y,source_raw=str(p),source_raw_sha256=sha(p),candidate_raw=str(q),candidate_raw_sha256=sha(q),source_alpha_signature=s1,candidate_alpha_signature=s2))
report=dict(status='PASS_ALL69_ACTUAL_CACHED_DEFINITIONS_NOOP_EXACT' if allgood else 'FAIL_ACTUAL_CACHE_NOOP_CHANGED',definitions=69,complete_raw_allfields_exact=sum(r['complete_raw_all_cache_fields_exact'] for r in results),semantic_graph_exact=sum(bool(r['semantic_graph_exact']) for r in results),scope='No-op source board vs candidate actual embedded cache only. Primary exact complete raw SExpr graph preserves every cache field including PAD layers/drill/mask/figure/textBlock/full properties/LIBRARY_PATH; only native handle addresses are consistently alpha-renamed. Whole-board designprops/environment are checked by separate gates. This does not prove compatibility with disk/public library definitions.',results=results,inputs={str(p):sha(p) for p in [A/'manifest.tsv',B/'manifest.tsv',Path(__file__),G/'sexpr.py',G/'compare_native_geometry.py']})
(O/'NOOP_ALL69_ACTUAL_CACHE_REVIEW.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('results','inputs')},indent=2));print(sha(O/'NOOP_ALL69_ACTUAL_CACHE_REVIEW.json'))
