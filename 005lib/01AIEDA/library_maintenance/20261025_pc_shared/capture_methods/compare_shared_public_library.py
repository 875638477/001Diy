"""Strict complete named membership + ordered object/default subtree comparison; no CAD."""
import argparse,pathlib,copy,json,hashlib,xml.etree.ElementTree as E
P=argparse.ArgumentParser()
P.add_argument("--expected",type=pathlib.Path,required=True)
P.add_argument("--actual",type=pathlib.Path,required=True)
P.add_argument("--out",type=pathlib.Path,required=True)
A=P.parse_args();assert not A.out.exists();A.out.mkdir(parents=True)
def fs(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def d(e):return e.find("Defn").attrib
def canon(e):
 if e is None:return None
 return [e.tag,sorted(e.attrib.items()),e.text if e.text and e.text.strip() else "",[canon(c) for c in e],e.tail if e.tail and e.tail.strip() else ""]
def h(e):return hashlib.sha256(json.dumps(canon(e),ensure_ascii=True,separators=(",",":")).encode()).hexdigest().upper()
OBJECTS={"Package","GlobalSymbol","OffPageSymbol","PortSymbol"}
def inspect(r):
 objs=[e for e in r if e.tag in OBJECTS]
 by={(e.tag,d(e)["name"]):e for e in objs}
 assert len(by)==len(objs),"Duplicate library objects"
 rest=copy.deepcopy(r)
 for e in list(rest):
  if e.tag in OBJECTS:rest.remove(e)
 rest.find("Defn").set("name","@READONLY_INPUT_PATH")
 return by,rest
expected=E.parse(A.expected).getroot();actual=E.parse(A.actual).getroot()
assert expected.tag==actual.tag=="Lib"
def compare(a,b):
 x,xr=inspect(a);y,yr=inspect(b)
 diffs=[]
 if set(x)!=set(y):diffs.append({"field":"OBJECT_MEMBERSHIP","before":sorted(x),"after":sorted(y)})
 for key in sorted(set(x)&set(y)):
  u=copy.deepcopy(x[key]);v=copy.deepcopy(y[key])
  # External OLB must not contain phantom per-object sources; no source path normalization here.
  if h(u)!=h(v):diffs.append({"field":"COMPLETE_ORDERED_OBJECT","key":key,"expected":h(u),"actual":h(v)})
 if h(xr)!=h(yr):diffs.append({"field":"COMPLETE_NONOBJECT_LIBRARY_CONTENT","expected":h(xr),"actual":h(yr)})
 return diffs
diffs=compare(expected,actual)
tests=[]
for kind in ["PIN_TYPE","PIN_HOT","GRAPHIC","DEFAULT_FONT","DELETE_OBJECT","DUPLICATE_OBJECT"]:
 q=copy.deepcopy(actual)
 if kind=="PIN_TYPE":
  el=q.find(".//SymbolPinScalar/Defn");el.set("type",str(int(el.get("type"))+1))
 elif kind=="PIN_HOT":
  el=q.find(".//SymbolPinScalar/Defn");el.set("hotptX",str(int(el.get("hotptX"))+1))
 elif kind=="GRAPHIC":
  el=q.find(".//Line/Defn");el.set("x1",str(int(el.get("x1"))+1))
 elif kind=="DEFAULT_FONT":
  el=q.find("./DefaultValues/DefaultFont/Defn");el.set("height",str(int(el.get("height"))-1))
 elif kind=="DELETE_OBJECT":
  q.remove(next(e for e in q if e.tag in OBJECTS))
 else:q.append(copy.deepcopy(next(e for e in q if e.tag in OBJECTS)))
 try:failed=bool(compare(expected,q))
 except AssertionError:failed=True
 tests.append({"case":kind,"detected":failed})
assert all(x["detected"] for x in tests),"Negative controls failed"
result={"status":"PASS_COMPLETE_OBJECTS_AND_LIBRARY_DEFAULTS" if not diffs else "FAIL",
 "expected_xml":str(A.expected),"expected_sha256":fs(A.expected),"actual_xml":str(A.actual),"actual_sha256":fs(A.actual),
 "object_count":len(inspect(actual)[0]),"difference_count":len(diffs),"differences":diffs,"negative_controls":tests,
 "normalization":"Only external Lib/Defn/@name input path. Compare object membership by (kind,name), every ordered complete object subtree and all nonobject library content including defaults exact. No package pin/font/property omission."}
(A.out/"SHARED_PUBLIC_LIBRARY_FULL_REVIEW.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(0 if not diffs else 2)