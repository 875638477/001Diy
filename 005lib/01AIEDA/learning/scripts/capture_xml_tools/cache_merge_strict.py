"""Strict Capture cache identity consolidation over official XML only.
Writes a separate XML, plan and preservation proof; never invokes Cadence."""
from pathlib import Path
import argparse,collections,copy,hashlib,json,xml.etree.ElementTree as E
def j(x):return json.dumps(x,ensure_ascii=True,separators=(",",":"))
def canon(e):return [e.tag,sorted(e.attrib.items()),e.text if e.text and e.text.strip() else "",[canon(c) for c in e],e.tail if e.tail and e.tail.strip() else ""]
def h(e):return hashlib.sha256(j(canon(e)).encode()).hexdigest().upper()
def fsha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def d(e):return e.find("Defn").attrib if e is not None and e.find("Defn") is not None else {}
def lib(s):return s.replace("/","\\").upper()
def key(e):return (lib(d(e).get("sourceLibName","")),d(e).get("name",""))
def normalized(e):
 q=copy.deepcopy(e)
 for k in ["name","sourceLibName","timestamp","timezone"]:q.find("Defn").attrib.pop(k,None)
 cells={}
 for lp in q.findall("LibPart"):
  x=lp.find("Defn")
  if x is not None and "CellName" in x.attrib:
   n=x.get("CellName")
   if n not in cells:cells[n]="@CELL_%d"%len(cells)
   x.set("CellName",cells[n])
 return q
def graphic_map(old,new):
 ol=old.findall("LibPart");nl=new.findall("LibPart");assert len(ol)==len(nl)
 m={}
 for a,b in zip(ol,nl):
  ac=d(a).get("CellName","");bc=d(b).get("CellName","")
  for tag in ["NormalView","ConvertView"]:
   av=a.find(tag);bv=b.find(tag)
   assert (av is None)==(bv is None)
   if av is not None:
    af=d(av).get("suffix","");bf=d(bv).get("suffix","")
    assert af==bf
    m[ac+af]=bc+bf
 return m
P=argparse.ArgumentParser();P.add_argument("--input",type=Path,required=True);P.add_argument("--output",type=Path,required=True);P.add_argument("--plan",type=Path,required=True)
A=P.parse_args()
assert A.input.resolve()!=A.output.resolve(),"Input may not be overwritten"
assert not A.output.exists(),"Refusing an existing output"
plan=json.loads(A.plan.read_text(encoding="utf-8-sig"))
assert plan["mode"]=="STRICT_IDENTITY_ONLY","This transformer deliberately rejects conditional/default-changing plans"
before_sha=fsha(A.input);assert before_sha==plan["input_xml_sha256"],"Input identity differs from approved read-only analysis"
before=E.parse(A.input);after=copy.deepcopy(before);br=before.getroot();ar=after.getroot();bc=br.find("Cache");ac=ar.find("Cache")
bi={key(p):p for p in bc.findall("Package")};ai={key(p):p for p in ac.findall("Package")}
changes=[];mapping={}
for m in plan["merges"]:
 old=(lib(m["old_lib"]),m["old_package"]);new=(lib(m["canonical_lib"]),m["canonical_package"])
 assert old!=new and old not in mapping
 assert old in bi and new in bi
 assert h(normalized(bi[old]))==h(normalized(bi[new]))==m["full_identity_normalized_sha256"],"Cache semantics/defaults differ"
 mapping[old]={"new":new,"target_lib":d(bi[new]).get("sourceLibName",""),"target_package":new[1],"graphic":graphic_map(bi[old],bi[new])}
assert not (set(mapping)&{x["new"] for x in mapping.values()}),"Mapping chains/cycles forbidden"
def edit_instance(inst,record=False,page=""):
 z=d(inst);k=(lib(z.get("libName","")),z.get("pkgName",""))
 if k not in mapping:return
 m=mapping[k];before_attrs=dict(z)
 inst.find("Defn").set("pkgName",m["target_package"]);inst.find("Defn").set("libName",m["target_lib"])
 gn=inst.find("GraphicName/Defn");assert gn is not None
 oldg=gn.get("name");assert oldg in m["graphic"],"Unknown placed graphic/cell/view"
 gn.set("name",m["graphic"][oldg])
 if record:changes.append({"page":page,"instance_id":z.get("dbId",""),"old_package":k[1],"new_package":m["new"][1],
    "old_lib":before_attrs.get("libName",""),"new_lib":m["target_lib"],"old_graphic":oldg,"new_graphic":gn.get("name")})
for sch in ar.findall("Schematic"):
 for page in sch.findall("Page"):
  for inst in page.findall("PartInst"):edit_instance(inst,True,d(page).get("name",""))
for old in mapping:ac.remove(ai[old])
# Independent graph pass after transform. All input instance IDs and complete
# non-reference instance subtrees remain unchanged; full Package definitions match.
after_index={key(p):p for p in ac.findall("Package")}
before_inst={d(x)["dbId"]:x for x in br.findall(".//Page/PartInst")}
after_inst={d(x)["dbId"]:x for x in ar.findall(".//Page/PartInst")}
assert set(before_inst)==set(after_inst)
electrical_rows=[];fail=[]
for ident,oldinst in before_inst.items():
 newinst=after_inst[ident]
 ok=(lib(d(oldinst).get("libName","")),d(oldinst).get("pkgName",""))
 nk=(lib(d(newinst).get("libName","")),d(newinst).get("pkgName",""))
 assert ok in bi and nk in after_index
 expected=copy.deepcopy(oldinst);edit_instance(expected)
 instance_equal=h(expected)==h(newinst)
 definition_equal=h(normalized(bi[ok]))==h(normalized(after_index[nk]))
 electrical_rows.append({"id":ident,"instance_allowed_identity_only_equal":instance_equal,"full_ordered_package_electrical_and_default_definition_equal":definition_equal})
 if not(instance_equal and definition_equal):fail.append(ident)
# Validate every design subtree outside Cache against the exact allowlisted edits.
expected=copy.deepcopy(br)
for x in expected.findall(".//Page/PartInst"):edit_instance(x)
expected.remove(expected.find("Cache"));actual=copy.deepcopy(ar);actual.remove(actual.find("Cache"))
noncache_equal=h(expected)==h(actual)
remaining_unchanged=all(h(bi[k])==h(v) for k,v in after_index.items())
symbols_before=[h(x) for x in bc if x.tag!="Package"];symbols_after=[h(x) for x in ac if x.tag!="Package"]
assert noncache_equal and remaining_unchanged and symbols_before==symbols_after and not fail
assert len(ac.findall("Package"))==len(bc.findall("Package"))-len(mapping)
assert fsha(A.input)==before_sha,"Input changed during analysis"
A.output.parent.mkdir(parents=True,exist_ok=True)
after.write(A.output,encoding="utf-8",xml_declaration=True,short_empty_elements=True)
# Independent reparsing of the actual written artifact.
written=E.parse(A.output).getroot();assert h(written)==h(ar)
proof={"status":"PASS_XML_ONLY_STRICT_IDENTITY_TRANSFORM_NOT_NATIVE_VALIDATED",
 "input_xml":str(A.input),"input_xml_sha256":before_sha,"output_xml":str(A.output),"output_xml_sha256":fsha(A.output),
 "plan_sha256":fsha(A.plan),"package_before":len(bc.findall("Package")),"package_after":len(ac.findall("Package")),
 "removed_duplicate_cache_packages":len(mapping),"changed_placed_instance_references":len(changes),"part_instance_count":len(before_inst),
 "all_instances_full_ordered_package_definitions_equal":not fail,"instance_definition_failure_ids":fail,
 "all_noncache_content_only_allowlisted_identity_edits":noncache_equal,
 "remaining_cache_package_subtrees_unchanged":remaining_unchanged,
 "net_symbols_and_cache_nonpackage_children_unchanged":symbols_before==symbols_after,
 "occurrences_raw_semantic_hash_equal":h(br.find("Occurrences"))==h(ar.find("Occurrences")),
 "native_import_save_independent_reopen_pst255_gate":"REQUIRED_NOT_EXECUTED"}
(A.output.with_suffix(".validation.json")).write_text(json.dumps(proof,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
(A.output.with_suffix(".instance_definition_proof.json")).write_text(json.dumps(electrical_rows,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
(A.output.with_suffix(".reference_changes.json")).write_text(json.dumps(changes,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
print(json.dumps(proof,ensure_ascii=True,indent=2))
