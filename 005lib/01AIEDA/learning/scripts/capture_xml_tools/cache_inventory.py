"""Read-only Capture XML cache/reference analysis. No Dbo DLL or CAD launched."""
from pathlib import Path
import argparse, collections, copy, csv, hashlib, json, re, xml.etree.ElementTree as ET
P=argparse.ArgumentParser()
P.add_argument("--xml",type=Path,required=True);P.add_argument("--out",type=Path,required=True)
A=P.parse_args();A.out.mkdir(parents=True,exist_ok=True)
def sha_bytes(b):return hashlib.sha256(b).hexdigest().upper()
def file_sha(p):return sha_bytes(p.read_bytes())
before=file_sha(A.xml)
root=ET.parse(A.xml).getroot();cache=root.find("Cache")
assert root.tag=="Design" and cache is not None
def defn(e):return e.find("Defn").attrib if e.find("Defn") is not None else {}
def j(x):return json.dumps(x,ensure_ascii=True,separators=(",",":"))
def normlib(s):return s.replace("/","\\").upper()
def canon(e):
    text=e.text if e.text and e.text.strip() else ""
    tail=e.tail if e.tail and e.tail.strip() else ""
    return [e.tag,sorted(e.attrib.items()),text,[canon(c) for c in e],tail]
def h(e):return sha_bytes(j(canon(e)).encode())
def wrjson(n,x):(A.out/n).write_text(json.dumps(x,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
def wrcsv(n,x,cols=None):
    cols=cols or (list(x[0]) if x else ["none"])
    with (A.out/n).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore");w.writeheader();w.writerows(x)
def pkg_normalized(e,strip_defaults=False):
    q=copy.deepcopy(e);d=q.find("Defn")
    for k in ["name","sourceLibName","timestamp","timezone"]:d.attrib.pop(k,None)
    cell_names={}
    for lp in q.findall("LibPart"):
        c=lp.find("Defn")
        if c is not None and "CellName" in c.attrib:
            n=c.attrib["CellName"]
            if n not in cell_names:cell_names[n]="@CELL_%d"%len(cell_names)
            c.attrib["CellName"]=cell_names[n]
        if strip_defaults:
            for view in lp:
                if view.tag in {"NormalView","ConvertView"}:
                    for ch in list(view):
                        if ch.tag in {"SymbolUserProp","PartValue","Reference"}:view.remove(ch)
    if strip_defaults:
        for ch in list(q):
            if ch.tag=="PackageUserProp":q.remove(ch)
    return q
def symbol_normalized(e):
    q=copy.deepcopy(e);d=q.find("Defn")
    for k in ["name","sourceLibName","timestamp","timezone"]:d.attrib.pop(k,None)
    return q
def defaults(pkg):
    data={}
    for i,ch in enumerate(pkg.findall("PackageUserProp")):
        n=defn(ch).get("name","")
        data.setdefault("Package/PackageUserProp/"+n,[]).append(canon(ch))
    for i,lp in enumerate(pkg.findall("LibPart")):
        for view in lp:
            if view.tag not in {"NormalView","ConvertView"}:continue
            for ch in view:
                if ch.tag in {"SymbolUserProp","PartValue","Reference"}:
                    n=defn(ch).get("name","") if ch.tag=="SymbolUserProp" else ""
                    data.setdefault("Cell[%d]/%s/%s/%s"%(i,view.tag,ch.tag,n),[]).append(canon(ch))
    return data
def props(e,tag):
    d=collections.defaultdict(list)
    for p in e.findall(tag):
        v=defn(p);d[v.get("name","")].append(v.get("val",""))
    return dict(d)
def named_value(e,tag):
    n=e.find(tag);return defn(n).get("name","") if n is not None else None
pkgs=cache.findall("Package")
bykey={};pindex=[];pmeta={};pinrows=[];device_rows=[]
for idx,pkg in enumerate(pkgs):
    d=defn(pkg);key=(normlib(d.get("sourceLibName","")),d.get("name",""))
    assert key not in bykey,("duplicate_package_identity",key)
    bykey[key]=pkg
    cell_count=len(pkg.findall("LibPart"));phys_count=len(pkg.findall(".//PhysicalPart"))
    m={"package":d["name"],"source_lib":d.get("sourceLibName",""),"xml_index":idx,
       "identity_normalized_full_sha256":h(pkg_normalized(pkg)),
       "ordered_structure_sha256":h(pkg_normalized(pkg,True)),
       "raw_subtree_sha256":h(pkg),"cell_count":cell_count,"physical_part_count":phys_count,
       "normal_views":len(pkg.findall(".//NormalView")),"convert_views":len(pkg.findall(".//ConvertView")),
       "physical_footprint":d.get("pcbFootprint",""),"is_homogeneous":d.get("isHomogeneous",""),
       "alphabetic_numbering":d.get("alphabeticNumbering",""),"refdes_prefix":d.get("refdesPrefix","")}
    pmeta[key]=m;pindex.append(m)
    for ci,lp in enumerate(pkg.findall("LibPart")):
        for pi,phys in enumerate(lp.findall("PhysicalPart")):
            device_rows.append({"package":d["name"],"source_lib":d.get("sourceLibName",""),"cell_index":ci,
               "cell_name":defn(lp).get("CellName",""),"physical_part_index":pi,"defn_json":j(defn(phys)),
               "ordered_children_json":j(canon(phys)),"ordered_physical_sha256":h(phys)})
        for view in lp:
            if view.tag not in {"NormalView","ConvertView"}:continue
            for order,pin in enumerate(x for x in view if x.tag in {"SymbolPinScalar","SymbolPinBus"}):
                pd=defn(pin)
                pinrows.append({"package":d["name"],"source_lib":d.get("sourceLibName",""),"cell_index":ci,
                 "view":view.tag,"pin_xml_order":order,"pin_tag":pin.tag,"position":pd.get("position",""),
                 "name":pd.get("name",""),"type":pd.get("type",""),"hot_x":pd.get("hotptX",""),"hot_y":pd.get("hotptY",""),
                 "start_x":pd.get("startX",""),"start_y":pd.get("startY",""),
                 "full_ordered_pin_sha256":h(pin),"complete_pin_json":j(canon(pin))})
refrows=[];refsbykey=collections.defaultdict(list);idinst={};errors=[]
for sch in root.findall("Schematic"):
 for page in sch.findall("Page"):
  sn=defn(sch).get("name","");pn=defn(page).get("name","")
  for inst in page.findall("PartInst"):
    d=defn(inst);key=(normlib(d.get("libName","")),d.get("pkgName",""))
    if key not in bykey:errors.append({"kind":"UNRESOLVED_PACKAGE","page":pn,"id":d.get("dbId"),"lib":key[0],"pkg":key[1]})
    vals=props(inst,"PartInstUserProp")
    active=[]
    if key in bykey:
      gn=named_value(inst,"GraphicName")
      for ci,lp in enumerate(bykey[key].findall("LibPart")):
        cell=defn(lp).get("CellName","")
        for view in lp:
          if view.tag in {"NormalView","ConvertView"} and cell+defn(view).get("suffix","")==gn:active.append((ci,view.tag))
    if len(active)!=1:errors.append({"kind":"UNRESOLVED_OR_AMBIGUOUS_ACTIVE_CELL_VIEW","page":pn,"id":d.get("dbId"),"graphic":named_value(inst,"GraphicName"),"matches":active})
    row={"schematic":sn,"page":pn,"id":d.get("dbId",""),"instance_name":d.get("name",""),
         "source_lib":d.get("libName",""),"package":d.get("pkgName",""),
         "device_designator":d.get("deviceDesignator",""),"graphic_name":named_value(inst,"GraphicName"),
         "use_convert":d.get("UseConvert","0"),"active_cell_index":active[0][0] if len(active)==1 else -1,"active_view":active[0][1] if len(active)==1 else "UNRESOLVED","refdes":named_value(inst,"Reference"),"part_value":named_value(inst,"PartValue"),
         "pcb_footprint_explicit_json":j(vals.get("PCB Footprint",[])),
         "instance_user_properties_json":j(vals),"whole_instance_sha256":h(inst)}
    refrows.append(row);refsbykey[key].append((row,inst))
    if row["id"] in idinst:errors.append({"kind":"DUPLICATE_PARTINST_ID","id":row["id"]})
    idinst[row["id"]]=(row,inst)
# Preserve all occurrence paths/overrides, including pin-indexed occurrence children.
occrows=[]
def occwalk(e,path):
    if e.tag=="InstOccurrence":
        d=defn(e);ident=d.get("refInstId","")
        path=path+[ident]
        r={"path_ids":"/".join(path),"ref_inst_id":ident,"resolved_part_instance":ident in idinst,
           "refdes":idinst[ident][0]["refdes"] if ident in idinst else "",
           "occurrence_user_props_json":j(props(e,"OccUserProp")),
           "port_occurrence_count":len(e.findall("PortOccurrence")),"whole_occurrence_sha256":h(e)}
        occrows.append(r)
        if ident not in {"","-1"} and ident not in idinst:errors.append({"kind":"OCCURRENCE_NOT_A_PARTINST","id":ident,"path":r["path_ids"]})
    for c in e:
        if c.tag=="InstOccurrence":occwalk(c,path)
if root.find("Occurrences") is not None:occwalk(root.find("Occurrences"),[])
groups=[]
for mode in ("identity_normalized_full_sha256","ordered_structure_sha256"):
    buckets=collections.defaultdict(list)
    for key,m in pmeta.items():buckets[m[mode]].append(key)
    for fingerprint,keys in buckets.items():
        if len(keys)<2:continue
        keys=sorted(keys,key=lambda k:(-len(refsbykey[k]),k[1],k[0]))
        ck=keys[0]
        groups.append({"mode":"STRICT_ALIAS_ONLY" if mode.startswith("identity") else "STRUCTURE_PLUS_EXPLICIT_DEFAULTS_REQUIRED",
             "group_id":mode[:3]+"_"+fingerprint[:16],"sha256":fingerprint,
             "canonical_package":ck[1],"canonical_lib":pmeta[ck]["source_lib"],
             "package_count":len(keys),"placed_instances":sum(len(refsbykey[k]) for k in keys),
             "members":[{"package":k[1],"source_lib":pmeta[k]["source_lib"],"instances":len(refsbykey[k])} for k in keys]})
# Expose every default-property delta. Do not silently map absence to empty string.
deltas=[];plan=[];groupmemberrows=[]
for g in groups:
    if g["mode"]!="STRUCTURE_PLUS_EXPLICIT_DEFAULTS_REQUIRED":continue
    ck=(normlib(g["canonical_lib"]),g["canonical_package"]);cd=defaults(bykey[ck])
    ds=[defaults(bykey[(normlib(m["source_lib"]),m["package"])]) for m in g["members"]]
    allkeys=set().union(*(set(d) for d in ds))
    differing={k for k in allkeys if len({j(d.get(k,{"__ABSENT__":True})) for d in ds})>1}
    for m in g["members"]:
        key=(normlib(m["source_lib"]),m["package"]);od=defaults(bykey[key])
        groupmemberrows.append({"group_id":g["group_id"],"old_package":key[1],"old_lib":pmeta[key]["source_lib"],
             "canonical_package":ck[1],"canonical_lib":pmeta[ck]["source_lib"],"instance_count":len(refsbykey[key]),
             "differing_default_keys":len(differing),"structural_hash":g["sha256"],"action":"READ_ONLY_CANDIDATE_NEEDS_NATIVE_EFFECTIVE_PROPERTY_GATE"})
        for propkey in sorted(differing):
            old=od.get(propkey);canonical=cd.get(propkey)
            deltas.append({"group_id":g["group_id"],"package":key[1],"canonical_package":ck[1],"default_key":propkey,
                  "old_present":old is not None,"canonical_present":canonical is not None,
                  "old_default_json":j(old),"canonical_default_json":j(canonical)})
            tag=propkey.split("/")[0] if propkey.startswith("Package/") else propkey.split("/")[2]
            propname=propkey.split("/")[-1]
            for row,inst in refsbykey[key]:
                if not propkey.startswith("Package/"):
                    scope=propkey.split("/")
                    if scope[0]!="Cell[%s]"%row["active_cell_index"] or scope[1]!=row["active_view"]:continue
                vals=props(inst,"PartInstUserProp")
                if tag in {"PartValue","Reference"}:
                    explicit=named_value(inst,tag);present=explicit is not None
                    target=tag; values=[explicit] if present else []
                else:
                    present=propname in vals;values=vals.get(propname,[]);target="PartInstUserProp:"+propname
                # Every differing canonical default must be removed or otherwise prevented
                # from supplying a previously absent property. Native effective props decide.
                action="PRESERVE_EXISTING_EXPLICIT_AND_CONFIRM_NATIVE_EFFECTIVE" if present else "READ_NATIVE_EFFECTIVE_BEFORE_REPLACE_AND_MATERIALIZE_IF_PRESENT"
                plan.append({"group_id":g["group_id"],"old_package":key[1],"canonical_package":ck[1],"page":row["page"],
                  "instance_id":row["id"],"refdes":row["refdes"],"default_key":propkey,"target":target,
                  "xml_explicit_present":present,"xml_explicit_values_json":j(values),
                  "old_default_present":old is not None,"old_default_json":j(old),
                  "action":action,"canonical_default_policy":"REMOVE_DIFFERING_DEFAULTS_FROM_CANONICAL_OR_PROVE_NO_NEW_INHERITANCE",
                  "occurrence_policy":"KEEP_ALL_OCCURRENCE_AND_PIN_OVERRIDES_UNCHANGED; native effective values must match"})
# Net symbol references use different electrical domains. No cross-domain candidates.
sindex=[];sbykey={};srefrows=[]
for e in cache:
 if e.tag not in {"GlobalSymbol","OffPageSymbol","PortSymbol"}:continue
 d=defn(e);k=(e.tag,normlib(d.get("sourceLibName","")),d.get("name",""));sbykey[k]=e
 sindex.append({"type":e.tag,"name":d["name"],"source_lib":d.get("sourceLibName",""),
      "identity_only_full_sha256":h(symbol_normalized(e)),"full_raw_sha256":h(e),
      "pin_count":len(e.findall("SymbolPinScalar"))+len(e.findall("SymbolPinBus"))})
typemap={"Global":"GlobalSymbol","OffPageConnector":"OffPageSymbol","Port":"PortSymbol"}
for sch in root.findall("Schematic"):
 for page in sch.findall("Page"):
  for t,typ in typemap.items():
   for inst in page.findall(t):
    d=defn(inst);k=(typ,normlib(d.get("libName","")),d.get("symbolName",""))
    if k not in sbykey:errors.append({"kind":"UNRESOLVED_NET_SYMBOL","type":t,"page":defn(page).get("name",""),"id":d.get("dbId","")})
    srefrows.append({"type":t,"page":defn(page).get("name",""),"id":d.get("dbId",""),"source_lib":d.get("libName",""),
        "symbol":d.get("symbolName",""),"net_name":d.get("name",""),"loc_x":d.get("locX",""),"loc_y":d.get("locY",""),
        "rotation":d.get("rotation",""),"mirror":d.get("mirror",""),"whole_instance_sha256":h(inst)})
sg=collections.defaultdict(list)
for x in sindex:sg[(x["type"],x["identity_only_full_sha256"])].append(x)
symbol_groups=[v for v in sg.values() if len(v)>1]
assert file_sha(A.xml)==before,"Input XML changed during read-only audit"
wrcsv("package_complete_fingerprints.csv",pindex);wrcsv("package_instance_reference_graph.csv",refrows)
wrcsv("package_ordered_pin_graph.csv",pinrows);wrcsv("package_ordered_device_graph.csv",device_rows)
wrcsv("occurrence_reference_graph.csv",occrows);wrjson("reference_errors.json",errors)
wrjson("package_reuse_candidate_groups.json",groups);wrcsv("package_reuse_group_members.csv",groupmemberrows)
wrcsv("default_property_delta_ledger.csv",deltas);wrcsv("instance_explicit_property_preservation_plan.csv",plan)
wrcsv("net_symbol_complete_fingerprints.csv",sindex);wrcsv("net_symbol_instance_reference_graph.csv",srefrows)
wrjson("net_symbol_reuse_candidate_groups.json",symbol_groups)
summary={"status":"READ_ONLY_XML_AUDIT_COMPLETE_NOT_NATIVE_VALIDATED","input_xml":str(A.xml),"input_xml_sha256":before,
 "package_count":len(pkgs),"part_instance_count":len(refrows),"occurrence_count":len(occrows),
 "physical_part_rows":len(device_rows),"ordered_pin_rows":len(pinrows),
 "strict_alias_only_groups":sum(g["mode"]=="STRICT_ALIAS_ONLY" for g in groups),
 "structure_default_plan_groups":sum(g["mode"]!="STRICT_ALIAS_ONLY" for g in groups),
 "structure_candidate_packages":sum(g["package_count"] for g in groups if g["mode"]!="STRICT_ALIAS_ONLY"),
 "structure_candidate_instances":sum(g["placed_instances"] for g in groups if g["mode"]!="STRICT_ALIAS_ONLY"),
 "default_delta_rows":len(deltas),"instance_preservation_plan_rows":len(plan),
 "missing_xml_explicit_plan_rows":sum(not p["xml_explicit_present"] for p in plan),
 "net_symbol_count":len(sindex),"net_symbol_instance_count":len(srefrows),"net_symbol_reuse_groups":len(symbol_groups),
 "reference_error_count":len(errors),"policies":{
 "child_order":"Preserve every child sequence including pins, physical mappings and vectors; no recursive child sorting.",
 "normalization":"Only Package.Defn name/sourceLibName/timestamp/timezone and LibPart.Defn CellName identity alpha-renaming. Same electrical type required.",
 "structure_hash_exclusions":"Only PackageUserProp, NormalView/ConvertView SymbolUserProp, PartValue, Reference excluded to derive CONDITIONAL candidates. ALL their differences are ledgered; never silently discarded.",
 "not_excluded":"PinUserProp, SymbolDisplayProp and every font, style, visibility, unknown field; Package PCB footprint/refdesPrefix; all Device data, Normal/Convert, Contents, ordered pins and graphic data.",
 "native_required":"Effective package/instance/occurrence/pin values, full all-pin device flags, reused cache actual references, PST255 electrical/refdes/device/footprint gate, save/independent reopen.",
 "absent_vs_empty":"Preserved distinctly. Differing canonical defaults must not introduce a property absent from the original effective object."}}
wrjson("LIBRARY_REUSE_XML_AUDIT_SUMMARY.json",summary)
print(json.dumps(summary,ensure_ascii=True,indent=2))
