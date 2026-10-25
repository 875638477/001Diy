"""Generate a fresh Capture XML that only reconnects cached Package identities
and all placed PartInst library identities to an already verified project OLB.
No CAD launch, geometry/property edit, or source/design/library mutation."""
from pathlib import Path
import argparse,collections,copy,csv,hashlib,json,ntpath,xml.etree.ElementTree as E
p=argparse.ArgumentParser()
p.add_argument("--input",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
p.add_argument("--expected-input-sha",required=True);p.add_argument("--library-xml",type=Path,required=True)
p.add_argument("--target-library",type=Path,required=True);p.add_argument("--expected-library-sha",required=True);p.add_argument("--native-source-identity",required=True)
a=p.parse_args()
assert a.input.resolve()!=a.output.resolve() and not a.output.exists(),"Fresh distinct output required"
assert a.target_library.is_absolute() and a.target_library.suffix.lower()==".olb","Explicit absolute target OLB required"
target=a.target_library.resolve(strict=True);targetName=a.native_source_identity
assert ntpath.normcase(ntpath.normpath(targetName))==ntpath.normcase(ntpath.normpath(str(target))), "Native identity path must resolve to the exact verified target OLB"
def fs(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def d(e):return e.find("Defn").attrib if e is not None and e.find("Defn") is not None else {}
def c(e):return [e.tag,sorted(e.attrib.items()),e.text if e.text and e.text.strip() else "",[c(x) for x in e],e.tail if e.tail and e.tail.strip() else ""]
def h(e):return hashlib.sha256(json.dumps(c(e),ensure_ascii=True,separators=(",",":")).encode()).hexdigest().upper()
def lib(s):return ntpath.normcase(ntpath.normpath(s.replace("/","\\")))
before_sha=fs(a.input);library_sha=fs(target);xmlsha=fs(a.library_xml)
assert before_sha==a.expected_input_sha.upper(),"Input XML hash mismatch"
assert library_sha==a.expected_library_sha.upper(),"Target OLB is not the already-verified delivery library; publish the correct independent library copy first"
br=E.parse(a.input).getroot();ar=copy.deepcopy(br);lr=E.parse(a.library_xml).getroot()
assert br.tag=="Design" and lr.tag=="Lib"
bp=br.findall("./Cache/Package");ap=ar.findall("./Cache/Package");lp=lr.findall("Package")
bi={d(x)["name"]:x for x in bp};li={d(x)["name"]:x for x in lp}
assert len(bi)==len(bp) and len(li)==len(lp) and set(bi)==set(li),"Package-name collision or external library mismatch"
def no_source(pkg):
 q=copy.deepcopy(pkg);q.find("Defn").attrib.pop("sourceLibName",None);return q
for name in bi:assert h(no_source(bi[name]))==h(no_source(li[name])),("Full external Package mismatch",name)
assert h(br.find("DefaultValues"))==h(lr.find("DefaultValues")),"Library defaults differ"
oldkeys={(lib(d(x).get("sourceLibName","")),d(x)["name"]) for x in bp};assert len(oldkeys)==len(bp)
changes=[];pkgindex={d(x)["name"]:x for x in ap}
for index,pkg in enumerate(ap):
 z=d(pkg);assert "sourceLibName" in z,"Unexpected source identity absence"
 old=z["sourceLibName"]
 z["sourceLibName"]=targetName
 changes.append({"kind":"Package","index":index,"instance_id":"","package":z["name"],"field":"sourceLibName","before":old,"after":targetName})
before_inst=br.findall(".//Page/PartInst");after_inst=ar.findall(".//Page/PartInst")
assert len(before_inst)==len(after_inst)
proof=[]
for index,(old,new) in enumerate(zip(before_inst,after_inst)):
 z=d(new);key=(lib(z.get("libName","")),z.get("pkgName",""))
 assert key in oldkeys,("Unresolved original Package identity",key)
 assert "libName" in z
 prior=z["libName"];z["libName"]=targetName
 changes.append({"kind":"PartInst","index":index,"instance_id":z.get("dbId",""),"package":z["pkgName"],"field":"libName","before":prior,"after":targetName})
 assert z["pkgName"] in pkgindex and lib(d(pkgindex[z["pkgName"]])["sourceLibName"])==lib(z["libName"])
 graphic=d(new.find("GraphicName")).get("name","")
 matches=[(ci,v.tag) for ci,cell in enumerate(pkgindex[z["pkgName"]].findall("LibPart")) for v in cell if v.tag in {"NormalView","ConvertView"} and d(cell).get("CellName","")+d(v).get("suffix","")==graphic]
 assert len(matches)==1,("Graphic identity changed or unresolved",z.get("dbId"),graphic,matches)
 expected=copy.deepcopy(old);d(expected)["libName"]=targetName
 equal=h(expected)==h(new);assert equal
 proof.append({"instance_id":z.get("dbId",""),"package":z["pkgName"],"complete_non_source_identity_subtree_equal":equal})
inverse=copy.deepcopy(ar)
for before,after in zip(bp,inverse.findall("./Cache/Package")):d(after)["sourceLibName"]=d(before)["sourceLibName"]
for before,after in zip(before_inst,inverse.findall(".//Page/PartInst")):d(after)["libName"]=d(before)["libName"]
assert h(inverse)==h(br),"Unexpected modification outside exact two source-identity fields"
unchanged={}
for path in [".//Page/NetScalar",".//Page/NetBus",".//Page/Global",".//Page/OffPageConnector",".//Page/Port","Occurrences","./Cache/GlobalSymbol","./Cache/OffPageSymbol","./Cache/PortSymbol",".//PhysicalPart","DefaultValues"]:
 unchanged[path]=[h(x) for x in br.findall(path)]==[h(x) for x in ar.findall(path)]
assert all(unchanged.values())
assert fs(a.input)==before_sha and fs(target)==library_sha and fs(a.library_xml)==xmlsha
a.output.parent.mkdir(parents=True,exist_ok=True);E.ElementTree(ar).write(a.output,encoding="utf-8",xml_declaration=True)
assert h(E.parse(a.output).getroot())==h(ar)
def csvw(name,rows):
 with (a.output.parent/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ["none"]);w.writeheader();w.writerows(rows)
csvw("source_identity_field_changes.csv",changes);csvw("all_instance_nonidentity_preservation.csv",proof)
summary={"status":"PASS_XML_ONLY_SOURCE_IDENTITY_RELINK_NATIVE_REOPEN_PST_PLACE_TEST_REQUIRED","input_xml_sha256":before_sha,"output_xml_sha256":fs(a.output),"external_library_xml_sha256":xmlsha,"target_library":targetName,"target_library_sha256":library_sha,"absolute_path_policy":"Use the exact verified final project OLB absolute path. Relative-path normalization is not assumed; it needs a separate native canary.","packages":len(bp),"instances":len(before_inst),"package_source_fields":len(bp),"instance_source_fields":len(before_inst),"total_identity_fields":len(changes),"whole_tree_inverse_allowlist_equal":True,"all_instance_nonidentity_subtrees_equal":True,"all_external_packages_complete_ordered_equal":True,"external_library_defaults_equal":True,"unchanged_domains":unchanged,"native_acceptance_required":["Official XML import into owned separate DSN; save; independent reopen/full bounded XML comparison","PST255 complete electrical/effective device/value/footprint gate","Native memory-only NewPlacedInst from the exact target OLB: Package count must not increase; returned source must resolve to target; RemoveDesign without saving; protect all input SHA"]}
a.output.with_suffix(".validation.json").write_text(json.dumps(summary,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
(a.output.parent/"source_link_plan.json").write_text(json.dumps({"input_xml_sha256":before_sha,"output_xml_sha256":fs(a.output),"target_library":targetName,"target_library_sha256":library_sha,"changes":changes},ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,ensure_ascii=True,indent=2))
