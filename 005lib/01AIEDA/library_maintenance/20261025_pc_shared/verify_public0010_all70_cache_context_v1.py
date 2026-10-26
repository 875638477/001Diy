"""Full70 cache gate: six fresh public packages +64 unchanged original caches.

Zero-pad format/mechanical symbols are included. Public PAD manufacturing proof
is independent. No names/schema-only inference, unit/geometry/font tolerance.
"""
from pathlib import Path
from collections import Counter
import argparse,copy,csv,hashlib,importlib.util,json,re,sys
M=Path(__file__).parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
sys.path.insert(0,str(R.parent/'cadence_geometry_merge_20261025'));from sexpr import parse_many,attrs,Atom
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
def need(v,m):
 if not v:raise ValueError(m)
def stable(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
N=importlib.util.module_from_spec(sp:=importlib.util.spec_from_file_location('frozen_global_graph',M/'review_global_suffix_native_chunks.py'));sp.loader.exec_module(N)
def graph(path):
 forms=parse_many(path.read_text('utf-8-sig'));need(forms[-1]==[Atom('complete'),Atom('t')],'Incomplete native full graph')
 meta=next(x for x in forms if x[0]=='meta');nodes={str(x[1]):(attrs(x[2]),x[3]) for x in forms if x[0]=='object'};need(len(nodes)==sum(x[0]=='object' for x in forms),'Duplicate native graph IDs')
 figures={str(x[1]):x[2] for x in forms if x[0]=='figure'};blocks={str(x[1]):attrs(x[2]) for x in forms if x[0]=='textblock'};selected=next(x[1] for x in forms if x[0]=='selected');need(len(selected)==1,'Exactly one selected native definition required');sid=str(selected[0]);memo={};visiting=set()
 def norm(v):
  if isinstance(v,list):return [norm(x) for x in v]
  if isinstance(v,Atom) and str(v) in nodes:return node(str(v))
  need(not(isinstance(v,Atom) and re.match(r'(dbid|pad|propList):',str(v))),'Unresolved native fullgraph handle')
  need('@0x' not in str(v),'Opaque native fullgraph value')
  return N.val(v)
 def node(key):
  if key in memo:return memo[key]
  need(key not in visiting,'Unknown fullgraph cycle');visiting.add(key);a,props=nodes[key];out=[]
  for k,v in sorted(a.items()):
   if k in N.NON_GEOM_HANDLES or key==sid and k=='name':continue
   if k=='figure' and key in figures:out.append([k,norm(figures[key])]);continue
   if k=='textBlock' and str(v) in blocks:out.append([k,[[x,norm(y)] for x,y in sorted(blocks[str(v)].items())]]);continue
   out.append([k,norm(v)])
  pp=[] if props==Atom('nil') else [[str(r[0]),norm(r[1:])] for r in props if str(r[0]) not in N.ADMIN]
  result={'attrs':out,'props':pp};visiting.remove(key);memo[key]=result;return result
 result={'units_and_accuracy':N.val(meta[2]),'selected_graph':node(sid),'step':N.val(next(x[1:] for x in forms if x[0]=='step'))}
 return result,hashlib.sha256(stable(result).encode()).hexdigest().upper(),str(nodes[sid][0]['name'])
def manifest(d):
 with (d/'manifest.tsv').open(newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
 result={r['name'].casefold():Path(r['file']) for r in rows};need(len(result)==len(rows),'Duplicate case-insensitive cache names');return result
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate-native',type=Path,required=True);ap.add_argument('--candidate-sha256',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'Fresh report output required')
 context=M/'public0010_canonical6_context_run13_v2';receipt=jr(context/'RUN_RECEIPT.json');need(receipt['status']=='COMPLETE_SIX_UNIQUE_PACKAGE_ALIASES_REQUIRES_FULLGRAPH_PAD_REVIEW' and receipt['public_unchanged'],'Native six-fresh-alias job incomplete')
 bundle=jr(receipt['manifest']);need(sha(receipt['manifest'])==receipt['manifest_sha256'],'Package cachemiss frozen manifest changed')
 for e in bundle['files']:need(sha(e['path'])==e['sha256'],'Frozen public PSM/helper/alias bytes changed')
 before=context/'SOURCE_ALL_TEXTBLOCKS_BEFORE.ilist';after=context/'SOURCE_ALL_TEXTBLOCKS_AFTER.ilist';need(before.read_bytes()==after.read_bytes() and len(parse_many(before.read_text()))==64,'Actual full64-font context changed during public load')
 pads=M/'public0010_canonical4_full_padxml_gate13_v1/CANONICAL4_ACTUAL_CACHE_PUBLIC_FULL_PAD_XML_REVIEW.json';padproof=jr(pads);need(padproof['status']=='PASS_ALL_FOUR_ACTUAL_CACHED_PUBLIC_FULL_MANUFACTURING_XML_EXACT_PHYSICAL_FIELDS' and padproof['actual_board_sha256']==receipt['source_sha256_before'],'Independent complete cached/public manufacturing proof missing or different source')
 for p,h in padproof['inputs'].items():need(sha(p)==h,'Manufacturing native/XML/public PAD evidence changed')
 current=manifest(a.candidate_native);original=manifest(M/'w/public_brd0010_source_allcache13');names={r['target'] for r in bundle['assets']};legacy=set(current)-names
 need(len(current)==70 and len(original)==69 and len(legacy)==64 and legacy<=set(original),'Current70/original69/unchanged64 full cache cohort differs')
 removed=set(original)-set(current);need(removed=={'c1206','r0603','c0603','r0805','c0805'},'Unexpected removed original cache definition')
 launch=jr(a.candidate_native/'launch_report.json');need(launch['source_sha256_before']==launch['source_sha256_after']==a.candidate_sha256.upper() and launch['input_unchanged'] and launch['exit_code']==0,'Current final native board binding failed')
 rows=[]
 for asset in bundle['assets']:
  n=asset['target'];x,xh,xn=graph(context/('actual_'+n+'.sexp'));y,yh,yn=graph(context/('public_'+n+'.sexp'));z,zh,zn=graph(current[n])
  need(x==y==z,'Complete actual/public/final package graph or font/unknown field differs '+n)
  need(xn.casefold()==zn.casefold()==n and yn.casefold()==asset['alias'],'Exact selected asset identity mismatch')
  rows.append(dict(name=n,scope='FRESH_PUBLIC_SAME_MM4_10L_ALL64_FONT_CONTEXT',actual_graph=str(current[n]),actual_graph_sha256=sha(current[n]),source_context_actual=str(context/('actual_'+n+'.sexp')),source_context_actual_sha256=sha(context/('actual_'+n+'.sexp')),fresh_public_alias_graph=str(context/('public_'+n+'.sexp')),fresh_public_alias_graph_sha256=sha(context/('public_'+n+'.sexp')),full_graph_fingerprint=xh,public_PSM=asset['source'],current_public_PSM_sha256=sha(asset['source'])))
 legacyrows=[]
 for n in sorted(legacy):
  x,xh,xn=graph(original[n]);y,yh,yn=graph(current[n]);need(x==y and xn.casefold()==yn.casefold()==n,'Untouched source legacy cached graph/fonts changed '+n)
  legacyrows.append(dict(name=n,source_graph=str(original[n]),source_graph_sha256=sha(original[n]),actual_graph=str(current[n]),actual_graph_sha256=sha(current[n]),full_graph_fingerprint=xh,not_claimed_publicly_externalized=True))
 controls=[];seed=rows[0];g,_,_=graph(Path(seed['actual_graph']))
 for name,fn in [('unknown_graph_field',lambda q:q['selected_graph']['attrs'].append(['UNAPPROVED',1])),('geometry_or_font_field',lambda q:q['selected_graph']['attrs'].__setitem__(0,['WRONG',1])),('step_metadata',lambda q:q.__setitem__('step','WRONG'))]:
  bad=copy.deepcopy(g);fn(bad);need(stable(bad)!=stable(g),'Fullgraph negative control accepted');controls.append(dict(name=name,status='PASS_REJECTED'))
 report=dict(status='PASS_ALL70_CACHED_DEFINITIONS_SIX_PUBLIC_FULLGRAPH_PAD_AND64_ORIGINAL_EXACT',candidate_board_sha256=a.candidate_sha256.upper(),native_public_context_board_sha256=receipt['source_sha256_before'],actual_cache_count=70,complete_public_canonical_packages=rows,untouched_original64=legacyrows,retired_original5_cache_names=sorted(removed),all64_actual_font_context_bytes_exact=True,context_native_receipt_sha256=sha(context/'RUN_RECEIPT.json'),full_public_cached_PAD_manufacturing_proof=str(pads),full_public_cached_PAD_manufacturing_proof_sha256=sha(pads),negative_controls=controls,normalization='Same previously frozen fullgraph method: runtime DBID traversal, only parent/instance/component/net/branch/parentGroups/prop/readOnly handles omitted; version/library path/save-user/edit-time administrative props omitted; exact selected asset name bounded separately. All other complete graphics/text/font/STEP/PAD/unknown fields and ordered internal children retained. Units remain exact native mm4. Zero-pin formats included.',legacy_scope='64 original module caches preserved; four old generic public matches may predate public library differences, and60 internal module-specific caches have no current public PSM. They are not newly externalized or declared fullpublic matches.',inputs={str(before):sha(before),str(after):sha(after),str(a.candidate_native/'launch_report.json'):sha(a.candidate_native/'launch_report.json')})
 a.out.mkdir();p=a.out/'ALL70_ACTUAL_CACHE_FULLGRAPH_CONTEXT_REVIEW.json';p.write_text(json.dumps(report,indent=2),'utf-8');print(json.dumps(dict(status=report['status'],report=str(p),sha256=sha(p)),indent=2))
if __name__=='__main__':main()
