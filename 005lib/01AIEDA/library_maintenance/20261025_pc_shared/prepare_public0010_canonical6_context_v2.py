"""Derive no-stale-parent-return-object package cache miss audit; no CAD."""
from pathlib import Path
import hashlib,json
M=Path(__file__).parent;sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def main():
 A=M/'public0010_canonical6_context_bundle13_v1';D=M/'public0010_canonical6_context_bundle13_v2';assert not D.exists();D.mkdir();old=json.loads((A/'MANIFEST.json').read_text());s=(A/'public0010_canonical6_context_v1.il').read_text()
 s=s.replace('original fresh beforeDefs exported f d)','original fresh beforeDefs exported f d loaded freshDefs)')
 s=s.replace(') exported=0',') exported=0 freshDefs=nil')
 before='''   unless(psmAuditExport(alias strcat(dir "/public_" name ".sexp")) error("Canonical6 public alias package load failed\\n"))
   fresh=car(setof(q axlDBGetDesign()->symdefs equal(upperCase(q->name) upperCase(alias))))
   unless(fresh && fresh!=original error("Canonical6 package cache miss was not forced\\n"))'''
 after='''   loaded=axlDBCreateSymbol(list(alias "PACKAGE") '(0.0 0.0))
   unless(loaded && car(loaded) error("Canonical6 public alias package load failed\\n"))
   fresh=car(loaded)->definition
   unless(fresh && fresh!=original && !member(fresh freshDefs) && equal(upperCase(fresh->name) upperCase(alias)) error("Canonical6 returned-object package cache miss not forced\\n"))
   freshDefs=cons(fresh freshDefs)
   pc13ExportOneDefinition(fresh strcat(dir "/public_" name ".sexp"))
   axlDBRefreshId(nil)'''
 assert s.count(before)==1;s=s.replace(before,after)
 s=s.replace('length(axlDBGetDesign()->symdefs)==beforeDefs+6','length(freshDefs)==6')
 # Initial source lookup must not rely on any previous public load refreshing
 # design->symdefs. It is refreshed before each next source definition lookup.
 s=s.replace('   original=car(setof(q','   axlDBRefreshId(nil)\n   original=car(setof(q')
 from build_public0010_stub_preflight_v1 import balanced
 balanced(s);h=D/'public0010_canonical6_context_v2.il';h.write_text(s,'utf-8');j=dict(old);j.update(helper=str(h),schema='PUBLIC0010_CANONICAL6_RETURNED_FRESH_DEFINITION_SAME_CONTEXT_V2',files=[e for e in old['files'] if Path(e['path'])!=A/'public0010_canonical6_context_v1.il']);j['files'] += [dict(path=str(h),sha256=sha(h)),dict(path=str(A/'MANIFEST.json'),sha256=sha(A/'MANIFEST.json'))]
 p=D/'MANIFEST.json';p.write_text(json.dumps(j,indent=2),'utf-8')
 run=(M/'run_public0010_canonical6_context_owned_v1.py').read_text().replace('PUBLIC0010_CANONICAL6_PACKAGE_CACHEMISS_SAME_NATIVE_CONTEXT_V1','PUBLIC0010_CANONICAL6_RETURNED_FRESH_DEFINITION_SAME_CONTEXT_V2');rp=M/'run_public0010_canonical6_context_owned_v2.py';assert not rp.exists();rp.write_text(run,'utf-8')
 print(json.dumps(dict(helper_sha256=sha(h),manifest_sha256=sha(p),runner_sha256=sha(rp)),indent=2))
if __name__=='__main__':main()
