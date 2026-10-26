"""Independent semantic cross-check only; strict full-field bijection is separate."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,sys
G=Path(r'D:\001DIY\004computer\lga1700\cadence_geometry_merge_20261025');sys.path.insert(0,str(G))
import compare_native_geometry as N
from sexpr import parse_many,attrs,Atom
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--before',type=Path,required=True);ap.add_argument('--after',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();assert not a.out.exists();a.out.mkdir(parents=True)
 rows={k:parse_many(p.read_text(encoding='utf-8-sig')) for k,p in [('before',a.before),('after',a.after)]};views={};records={};allpads=set();rootnames={};props={}
 for side,rs in rows.items():
  count=Counter(str(r[0]) for r in rs);assert set(count)<= {'object','figure','textblock'}
  nodes={str(r[1]):(attrs(r[2]),r[3]) for r in rs if r[0]=='object'};assert len(nodes)==count['object'];roots={str(v[0]['name']):key for key,v in nodes.items() if v[0]['objType']=='symdef'};assert len(roots)==79
  allpads.update(str(v[0]['name']) for v in nodes.values() if v[0]['objType']=='padstack');rootnames[side]=set(roots)
  props[side]={key:val[1] for key,val in nodes.items() if key.startswith('dbid:')}
  # The wrapper adds no geometry or props. Units, precision and LAYOUT mode
  # are the actual module context; every raw cache object/figure remains.
  h='(meta "THERMAL_CACHE_CROSSCHECK" ("millimeters" 4) "LAYOUT" "BOARD")\n(step nil nil nil)\n(designprops nil)\n(selected ('+' '.join(roots.values())+'))\n'
  p=a.out/(side+'_CACHE_WRAPPED.sexp');p.write_text(h+(a.before if side=='before' else a.after).read_text(encoding='utf-8-sig')+'\n(complete t)\n',encoding='utf-8');views[side]=N.Native(p);records[side]=dict(count)
 N.PAD_PUBLIC={s.casefold():'SAME_FULL_EMBEDDED_CACHE_COMPARISON_NOT_EXTERNAL_LIBRARY_EQUIVALENCE' for s in allpads}
 sig={side:v.signature() for side,v in views.items()};same=sig['before']['signature']==sig['after']['signature'] and not sig['before']['issues'] and not sig['after']['issues']
 common=set(props['before'])&set(props['after']);propchanges=[key for key in common if props['before'][key]!=props['after'][key]]
 report={'status':'PASS_ALL79_SEMANTIC_CACHE_CROSSCHECK_ONLY' if same and rootnames['before']==rootnames['after'] and not propchanges else 'FAIL_SEMANTIC_CACHE_CROSSCHECK','scope':'Auxiliary independent complete native semantic graph comparison. Historical comparator has documented derived/admin normalization; strict raw all-field typed handle bijection is mandatory and separate. No external public library compatibility assertion.','before':{'path':str(a.before),'sha256':sha(a.before)},'after':{'path':str(a.after),'sha256':sha(a.after)},'record_counts':records,'symdef_names_exact':rootnames['before']==rootnames['after'],'stable_DBID_object_full_property_payloads_compared':len(common),'stable_DBID_full_property_payload_differences':propchanges,'graph':sig,'parser':{'path':str(G/'sexpr.py'),'sha256':sha(G/'sexpr.py')},'comparator':{'path':str(G/'compare_native_geometry.py'),'sha256':sha(G/'compare_native_geometry.py')},'script_sha256':sha(__file__),'CAD_started':False,'public_files_written':0}
 out=a.out/'THERMAL_ALL79_CACHE_SEMANTIC_CROSSCHECK.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'status':report['status'],'report':str(out),'sha256':sha(out),'property_differences':len(propchanges),'graph':sig}))
if __name__=='__main__':main()
