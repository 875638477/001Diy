"""Prepare exact source2068-line / all1739-via current-net diagnostics; no CAD."""
from pathlib import Path
import collections,csv,hashlib,json,sys
M=Path(__file__).parent
sys.path.insert(0,str(M));from build_public0010_stub_preflight_v1 import balanced
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
sys.path.insert(0,str(R.parent/'cadence_geometry_merge_20261025'))
from sexpr import parse_many,Atom
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
sk=lambda p:json.dumps(str(p).replace('\\','/'))
def atom(x):
 if isinstance(x,list):return '('+' '.join(atom(v) for v in x)+')'
 if isinstance(x,Atom):return str(x)
 if isinstance(x,str):return json.dumps(x)
 return str(x)
def main():
 D=M/'public0010_route_net_diagnostic_bundle13_v1';assert not D.exists();D.mkdir()
 pre=M/'public0010_stub_preflight_bundle13_v1';P=M/'public0010_path_stubs_plan13_v1'
 source=M/'w/public_brd0010_source_full13_v2/via_properties.tsv';target=M/'w/module0010_after403_full24/via_properties.tsv'
 def rows(p):
  with p.open(newline='') as f:return list(csv.DictReader(f,delimiter='\t',quoting=csv.QUOTE_NONE))
 sr,tr=rows(source),rows(target);assert len(sr)==len(tr)==1739
 def norm(r):return tuple(r[k] for k in ['xy','padstack','net','properties'])
 A=collections.Counter(map(norm,sr));B=collections.Counter(map(norm,tr));missing=list((A-B).elements());added=list((B-A).elements());assert len(missing)==len(added)==9
 def native(r):return [parse_many(r['xy'])[0],parse_many(r['padstack'])[0],parse_many(r['net'])[0],parse_many(r['properties'])[0]]
 v=D/'SOURCE_ALL1739_VIAS.ilist';v.write_text('\n'.join(atom(native(r)) for r in sr)+'\n','utf-8')
 diff=D/'SOURCE_TO_TARGET_EXACT_NINE_VIA_NET_DELTAS.json';diff.write_text(json.dumps(dict(source=missing,target=added,only9nets_changed=True),indent=2),'utf-8')
 helper='load('+sk(pre/'public0010_stub_preflight_v1.il')+')\n'
 helper+='''
procedure(pub0010RouteGeomKey(kind layer width ends)
 let((a b)
  a=pc13StubGridPoint(car(ends)) b=pc13StubGridPoint(cadr(ends))
  unless(alphalessp(sprintf(nil "%L" a) sprintf(nil "%L" b)) a=pc13StubGridPoint(cadr(ends)) b=pc13StubGridPoint(car(ends)))
  sprintf(nil "%L" list(kind layer width a b))))
procedure(pub0010RouteObjectsWalk(o)
 let((attrs key)
  when(o && !pub0010RouteSeen[o]
   pub0010RouteSeen[o]=t
   when(equal(o->objType "line")
    key=pub0010RouteGeomKey(o->objType o->layer o->width o->startEnd)
    pub0010ActualLines[key]=cons(o pub0010ActualLines[key]))
   attrs=o->? when(member('children attrs) foreach(x o->children pub0010RouteObjectsWalk(x)))
   when(member('segments attrs) foreach(x o->segments pub0010RouteObjectsWalk(x))))))
procedure(pub0010RouteNetDiagnostic(dir)
 let((f vf rows key matches count missing changed row actual viaCount expected actualVias)
  sstatus(fullPrecision t) pub403ReadUnits()
  pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist")) pub403AllNameGate(nil)
  pub0010RouteSeen=makeTable('pub0010RouteSeen nil) pub0010ActualLines=makeTable('pub0010ActualLines nil)
  foreach(n axlDBGetDesign()->nets foreach(b n->branches pub0010RouteObjectsWalk(b)))
  foreach(b axlDBGetLonelyBranches() pub0010RouteObjectsWalk(b))
  rows=pub403Rows(@SOURCE@) unless(length(rows)==2068 error("PUB0010 frozen2068 line ledger count differs\\n"))
  f=outfile(strcat(dir "/ACTUAL2068_SOURCE_LINE_CURRENT_OBJECT_NETS.ilist")) count=0 missing=0 changed=0
  foreach(row rows
   unless(equal(car(row) "line") error("PUB0010 geometry-only exact matching restricted to actual2068 straight lines\\n"))
   key=pub0010RouteGeomKey(car(row) nth(2 row) nth(3 row) nth(4 row)) matches=pub0010ActualLines[key]
   unless(matches missing=missing+1)
   unless(length(matches)==1 && equal(car(matches)->net->name nth(1 row)) changed=changed+1)
   fprintf(f "%L\\n" list(row foreach(mapcar o matches list(o o->objType o->net->name o->layer o->width o->startEnd o->parent o->parent->net->name o->parent->??)))) drain(f) count=count+1)
  close(f) pub0010BuildCuIndex() actualVias=nil
  vf=outfile(strcat(dir "/ACTUAL_ALL1739_VIAS.ilist"))
  foreach(item pc13CuIndexRows when(equal(nth(4 item) "via")
   actual=car(item) row=list(actual->xy actual->name if(actual->net then actual->net->name else "__NO_NET__") axlDBGetProperties(actual '("user" "allegro")))
   actualVias=cons(row actualVias) fprintf(vf "%L\\n" row))) close(vf)
  unless(length(actualVias)==1739 error("PUB0010 actual via completeness differs from frozen1739\\n"))
  f=outfile(strcat(dir "/SOURCE_ROUTE_AND_VIA_DIAGNOSTIC_COMPLETE.txt"))
  fprintf(f "PUB0010_EXACT2068_SOURCE_LINE_AND_ALL1739_VIA_NET_DIAGNOSTIC_COMPLETE_NO_SAVE\\nSOURCE_LINES=%d\\nNO_EXACT_CURRENT_LINE_MATCH=%d\\nNON_UNIQUE_OR_CHANGED_CURRENT_NET=%d\\nACTUAL_VIAS=%d\\n" count missing changed length(actualVias)) close(f) t))
'''
 helper=helper.replace('@SOURCE@',sk(P/'SOURCE_FROZEN_REAL_SEGMENTS.ilist'));balanced(helper);h=D/'public0010_route_net_diagnostic_v1.il';h.write_text(helper,'utf-8')
 old=json.loads((pre/'MANIFEST.json').read_text());files=[Path(x['path']) for x in old['files']]+[pre/'MANIFEST.json',h,v,diff,source,target]
 man=dict(old);man.update(helper=str(h),entry='pub0010RouteNetDiagnostic',marker='SOURCE_ROUTE_AND_VIA_DIAGNOSTIC_COMPLETE.txt',branch_groups=2068,files=[dict(path=str(p),sha256=sha(p)) for p in dict.fromkeys(files)],phase='exact_line_and_via_net_diagnostic')
 (D/'MANIFEST.json').write_text(json.dumps(man,indent=2),'utf-8');print(json.dumps(dict(helper_sha256=sha(h),manifest_sha256=sha(D/'MANIFEST.json'),source_vias_sha256=sha(v),nine_via_deltas=str(diff)),indent=2))
if __name__=='__main__':main()
