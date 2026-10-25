"""Generate a separate Capture XML with structurally identical package reuse.
Conditional mode neutralizes differing defaults and preserves each explicit
instance value; never runs CAD. The generated candidate requires native gates."""
from pathlib import Path
import argparse,collections,copy,csv,hashlib,json,xml.etree.ElementTree as E
def j(v):return json.dumps(v,ensure_ascii=True,separators=(",",":"))
def c(e):return [e.tag,sorted(e.attrib.items()),e.text if e.text and e.text.strip() else "",[c(x) for x in e],e.tail if e.tail and e.tail.strip() else ""]
def h(e):return hashlib.sha256(j(c(e)).encode()).hexdigest().upper()
def fs(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def D(e):return e.find("Defn").attrib if e is not None and e.find("Defn") is not None else {}
def L(s):return s.replace("/","\\").upper()
def K(e):return (L(D(e).get("sourceLibName","")),D(e).get("name",""))
def normal(pkg,structure=False):
 q=copy.deepcopy(pkg)
 for k in ["name","sourceLibName","timestamp","timezone"]:q.find("Defn").attrib.pop(k,None)
 cells={}
 for lp in q.findall("LibPart"):
  d=lp.find("Defn")
  if d is not None and "CellName" in d.attrib:
   old=d.get("CellName")
   if old not in cells:cells[old]="@CELL_%d"%len(cells)
   d.set("CellName",cells[old])
  if structure:
   for v in lp:
    if v.tag in {"NormalView","ConvertView"}:
     for ch in list(v):
      if ch.tag in {"SymbolUserProp","PartValue","Reference"}:v.remove(ch)
 if structure:
  for ch in list(q):
   if ch.tag=="PackageUserProp":q.remove(ch)
 return q
def default_nodes(pkg):
 out={}
 for ch in pkg.findall("PackageUserProp"):out.setdefault("Package/PackageUserProp/"+D(ch).get("name",""),[]).append(ch)
 for ci,lp in enumerate(pkg.findall("LibPart")):
  for v in lp:
   if v.tag not in {"NormalView","ConvertView"}:continue
   for ch in v:
    if ch.tag in {"SymbolUserProp","PartValue","Reference"}:
     key="Cell[%d]/%s/%s/%s"%(ci,v.tag,ch.tag,D(ch).get("name","") if ch.tag=="SymbolUserProp" else "")
     out.setdefault(key,[]).append(ch)
 return out
def default_hashes(pkg):return {k:[h(x) for x in v] for k,v in default_nodes(pkg).items()}
def active(pkg,inst):
 gn=inst.find("GraphicName/Defn");assert gn is not None
 matches=[]
 for ci,lp in enumerate(pkg.findall("LibPart")):
  for v in lp:
   if v.tag in {"NormalView","ConvertView"} and D(lp).get("CellName","")+D(v).get("suffix","")==gn.get("name"):matches.append((ci,v.tag))
 assert len(matches)==1,("Unresolved active cell/view",D(inst),gn.attrib,matches)
 return matches[0]
def props(inst):
 d=collections.defaultdict(list)
 for x in inst.findall("PartInstUserProp"):d[D(x).get("name","")].append(x)
 return dict(d)
def graph_map(old,new):
 out={}
 for x,y in zip(old.findall("LibPart"),new.findall("LibPart")):
  for v in ["NormalView","ConvertView"]:
   a=x.find(v);b=y.find(v);assert (a is None)==(b is None)
   if a is not None:
    assert D(a).get("suffix","")==D(b).get("suffix","")
    out[D(x).get("CellName","")+D(a).get("suffix","")]=D(y).get("CellName","")+D(b).get("suffix","")
 return out
def applies(key,av):return key.startswith("Package/") or key.startswith("Cell[%d]/%s/"%av)
def direct_insert_prop(inst,node):
 xs=list(inst);idx=max([i for i,x in enumerate(xs) if x.tag=="PartInstUserProp"],default=0)+1
 inst.insert(idx,node)
P=argparse.ArgumentParser();P.add_argument("--input",type=Path,required=True);P.add_argument("--output",type=Path,required=True);P.add_argument("--plan",type=Path,required=True)
A=P.parse_args();assert A.input.resolve()!=A.output.resolve() and not A.output.exists(),"Output must be a new distinct file"
plan=json.loads(A.plan.read_text(encoding="utf-8-sig"));assert plan["mode"]=="CONDITIONAL_SCOPED_DEFAULT_FLATTEN"
input_sha=fs(A.input);assert plan["input_xml_sha256"]==input_sha
br=E.parse(A.input).getroot();ar=copy.deepcopy(br);bc=br.find("Cache");ac=ar.find("Cache")
bi={K(x):x for x in bc.findall("Package")};ai={K(x):x for x in ac.findall("Package")}
mapping={};groupof={};groupdata={};removed_defaults=[]
for g in plan["groups"]:
 ck=(L(g["canonical_lib"]),g["canonical_package"]);keys=[(L(x["source_lib"]),x["package"]) for x in g["members"]]
 assert ck in keys
 dh=[default_hashes(bi[k]) for k in keys]
 names=set().union(*(set(x) for x in dh))
 diff={n for n in names if len({j(x.get(n,{"__ABSENT__":True})) for x in dh})>1}
 for k in keys:
  assert h(normal(bi[k],True))==g["sha256"],("Structural mismatch",k)
  assert k not in groupof;groupof[k]=g["group_id"]
  mapping[k]={"new":ck,"graphic":graph_map(bi[k],bi[ck]),"lib":D(bi[ck]).get("sourceLibName","")}
 groupdata[g["group_id"]]={"canonical":ck,"diff":diff,"keys":keys}
 # Remove only differing defaults from canonical at their original scope.
 q=ai[ck];dn=default_nodes(q);parents={ch:p for p in q.iter() for ch in p}
 for n in sorted(diff):
  for node in dn.get(n,[]):
   removed_defaults.append({"group_id":g["group_id"],"canonical_package":ck[1],"default_key":n,"removed_full_json":j(c(node))})
   parents[node].remove(node)
additions=[];refchanges=[];instance_proofs=[];fail=[]
binst={D(x)["dbId"]:x for x in br.findall(".//Page/PartInst")}
ainst={D(x)["dbId"]:x for x in ar.findall(".//Page/PartInst")}
assert set(binst)==set(ainst)
for ident,oldinst in binst.items():
 z=ainst[ident];k=(L(D(oldinst).get("libName","")),D(oldinst).get("pkgName",""))
 if k not in groupof:continue
 g=groupdata[groupof[k]];m=mapping[k];av=active(bi[k],oldinst);olddefs=default_nodes(bi[k]);pp=props(oldinst)
 for n in sorted(g["diff"]):
  if not applies(n,av):continue
  ps=n.split("/");tag=ps[1] if ps[0]=="Package" else ps[2];prop=ps[-1]
  nodes=olddefs.get(n,[])
  if tag in {"PartValue","Reference"}:
   assert oldinst.find(tag) is not None,("Missing explicit PartValue/Reference blocks automatic flatten",ident,n)
   continue
  if prop in pp:continue # Preserve every existing explicit value, even empty.
  if not nodes:continue # ABSENT stays ABSENT, never synthesized as empty.
  assert len(nodes)==1 and set(D(nodes[0]))=={"name","val"},("Ambiguous/unknown default property blocks flatten",ident,n)
  # Scope ambiguity must be rejected rather than guessing package/library precedence.
  applicable=[key for key,ns in olddefs.items() if applies(key,av) and key.endswith("/"+prop) and ns]
  assert len(applicable)==1,("Property has several inheritance sources",ident,prop,applicable)
  # Only names explicitly reviewed and authorized by this plan may be materialized.
  assert prop in plan["allowed_materialize_missing_property_names"],("New materialization needs explicit plan authorization",ident,prop)
  new=E.Element("PartInstUserProp");E.SubElement(new,"Defn",dict(D(nodes[0])))
  direct_insert_prop(z,new)
  additions.append({"instance_id":ident,"old_package":k[1],"canonical_package":m["new"][1],"default_key":n,"name":prop,"value":D(nodes[0])["val"],"before_scope":n,"after_scope":"PartInstUserProp"})
 if k!=m["new"]:
  old_graph=z.find("GraphicName/Defn").get("name");assert old_graph in m["graphic"]
  z.find("Defn").set("pkgName",m["new"][1]);z.find("Defn").set("libName",m["lib"]);z.find("GraphicName/Defn").set("name",m["graphic"][old_graph])
  refchanges.append({"instance_id":ident,"old_package":k[1],"canonical_package":m["new"][1],"old_graphic":old_graph,"new_graphic":m["graphic"][old_graph]})
# Remove only noncanonical complete packages.
remove_keys=[k for k,m in mapping.items() if k!=m["new"]]
assert len(remove_keys)==plan["merge_count"]
for k in remove_keys:ac.remove(ai[k])
newindex={K(x):x for x in ac.findall("Package")}
# Complete original explicit instance content is unchanged except identity fields
# and individually ledgered additions. Per-scope old default values cannot bleed.
byadded=collections.defaultdict(list)
for x in additions:byadded[x["instance_id"]].append(x)
for ident,oldinst in binst.items():
 newinst=ainst[ident];k=(L(D(oldinst).get("libName","")),D(oldinst).get("pkgName",""));nk=(L(D(newinst).get("libName","")),D(newinst).get("pkgName",""))
 expected=copy.deepcopy(oldinst)
 if k in mapping:
  m=mapping[k]
  if k!=m["new"]:
   expected.find("Defn").set("pkgName",m["new"][1]);expected.find("Defn").set("libName",m["lib"])
   gn=expected.find("GraphicName/Defn");gn.set("name",m["graphic"][gn.get("name")])
  for ad in byadded[ident]:
   x=E.Element("PartInstUserProp");E.SubElement(x,"Defn",{"name":ad["name"],"val":ad["value"]});direct_insert_prop(expected,x)
 structural=h(normal(bi[k],True))==h(normal(newindex[nk],True))
 exact_instance=h(expected)==h(newinst)
 if not(structural and exact_instance):fail.append({"instance_id":ident,"structural":structural,"allowlist_instance":exact_instance})
 instance_proofs.append({"instance_id":ident,"ordered_structure_electrical_geometry_same":structural,"explicit_instance_values_only_allowlisted_additions":exact_instance,"materialized_trace_properties":len(byadded[ident])})
 # Conditional default proof: removed default in an active scope is either
 # already explicitly on the original instance, materialized exactly once, or
 # originally ABSENT and remains without a new inherited value in that scope.
 if k in groupof:
  av=active(bi[k],oldinst);od=default_nodes(bi[k]);nd=default_nodes(newindex[nk]);op=props(oldinst);np=props(newinst);g=groupdata[groupof[k]]
  for n in g["diff"]:
   if not applies(n,av):continue
   assert n not in nd,("Differing canonical default survived neutralization",ident,n)
   ps=n.split("/");tag=ps[1] if ps[0]=="Package" else ps[2];prop=ps[-1]
   if tag in {"PartValue","Reference"}:assert h(oldinst.find(tag))==h(newinst.find(tag));continue
   if prop in op:assert [h(x) for x in op[prop]]==[h(x) for x in np[prop]]
   elif od.get(n):assert [D(x)["val"] for x in od[n]]==[D(x)["val"] for x in np.get(prop,[])]
   else:assert prop not in np or prop in {a["name"] for a in byadded[ident]} # any added value has separately unique proven source
assert not fail
# Every other design element, page geometry, occurrence, network symbol and
# property is unchanged after reproducing only the recorded instance edits.
expected=copy.deepcopy(br)
for x in expected.findall(".//Page/PartInst"):
 ident=D(x)["dbId"];y=ainst[ident]
 if h(x)!=h(y):
  parent=None
  # replace through indexed page once below
for page in expected.findall(".//Page"):
 for i,x in enumerate(list(page)):
  if x.tag=="PartInst":page.remove(x);page.insert(i,copy.deepcopy(ainst[D(x)["dbId"]]))
expected.remove(expected.find("Cache"));actual=copy.deepcopy(ar);actual.remove(actual.find("Cache"))
noncache_equal=h(expected)==h(actual)
assert noncache_equal and h(br.find("Occurrences"))==h(ar.find("Occurrences"))
assert [h(x) for x in bc if x.tag!="Package"]==[h(x) for x in ac if x.tag!="Package"]
assert fs(A.input)==input_sha
A.output.parent.mkdir(parents=True,exist_ok=True);E.ElementTree(ar).write(A.output,encoding="utf-8",xml_declaration=True)
assert h(E.parse(A.output).getroot())==h(ar)
def csvw(n,rs):
 with (A.output.parent/n).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]) if rs else ["none"]);w.writeheader();w.writerows(rs)
csvw("canonical_differing_defaults_removed.csv",removed_defaults);csvw("instance_defaults_materialized.csv",additions);csvw("instance_identity_reference_changes.csv",refchanges);csvw("all_instance_structure_scope_preservation.csv",instance_proofs)
s={"status":"PASS_XML_CONDITIONAL_SCOPE_FLATTEN_ONLY_NATIVE_GATES_REQUIRED","input_xml_sha256":input_sha,"output_xml_sha256":fs(A.output),"plan_sha256":fs(A.plan),
"package_before":len(bi),"package_after":len(newindex),"duplicate_packages_removed":len(remove_keys),"all_instances":len(binst),
"identity_changed_instances":len(refchanges),"differing_canonical_default_nodes_removed":len(removed_defaults),"materialized_inherited_property_count":len(additions),
"materialized_names":dict(collections.Counter(x["name"] for x in additions)),"all_instance_structure_or_explicit_value_failures":fail,
"noncache_only_exact_allowlist":noncache_equal,"occurrence_full_subtree_unchanged":True,"all_network_symbol_cache_definitions_unchanged":True,
"all_geometry_pin_order_device_mapping_styles_hidden_global_nc_contents_footprints":"PRESERVED_BY_COMPLETE_ORDERED_STRUCTURE",
"default_scope_policy":"Keep common defaults, remove every differing default from canonical active scopes, retain all explicit values, materialize only unique-source existing trace defaults. Old ABSENT never becomes empty/default from another member.",
"native_required":"Official XML import, full cache/table audit, effective-property/value check, PST255 partition/device/refdes/footprint gate, complete independent save/reopen/layout inspection"}
A.output.with_suffix(".validation.json").write_text(json.dumps(s,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
print(json.dumps(s,ensure_ascii=True,indent=2))
