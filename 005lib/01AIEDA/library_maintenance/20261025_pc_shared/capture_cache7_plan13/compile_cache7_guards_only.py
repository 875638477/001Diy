"""Compile fixed source and reviewed per-instance footprint mapping into guarded native Tcl."""
import argparse,pathlib,copy,json,hashlib,collections,re,xml.etree.ElementTree as E
P=argparse.ArgumentParser()
P.add_argument("--source-plan",type=pathlib.Path,required=True)
P.add_argument("--instance-map",type=pathlib.Path,required=True)
P.add_argument("--out",type=pathlib.Path,required=True)
P.add_argument("--new-source-identity",help="Exact native GetName identity for the published COMMON_PC.OLB")
A=P.parse_args();assert not A.out.exists(),"Fresh output required";A.out.mkdir(parents=True)
def fs(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def d(e):return e.find("Defn").attrib
def q(s):return '"'+str(s).replace("\\","\\\\").replace('"','\\"').replace("$","\\$").replace("[","\\[").replace("]","\\]").replace("\r","\\r").replace("\n","\\n")+'"'
def td(v):return "[dict create "+" ".join(q(k)+" "+q(x) for k,x in v.items())+"]"
plan=json.loads(A.source_plan.read_text(encoding="utf-8-sig"))
assert plan["status"]=="READY_EXPLICIT_NATIVE_SOURCE_ONLY_PLAN"
xml=pathlib.Path(plan["source_design_xml"])
assert fs(xml)==plan["source_xml_sha256"]==plan["source_design_xml_sha256"]
tree=E.parse(xml).getroot()
mapping=json.loads(A.instance_map.read_text(encoding="utf-8-sig"))
assert isinstance(mapping,list) and len(mapping)==1131,"Expected complete placed-instance mapping list"
mi={str(x["dbid"]):x for x in mapping};assert len(mi)==1131
sourceRows=plan["instance_source_changes"];assert len(sourceRows)==3118
sources={(x["kind"],x["id"]):x for x in sourceRows}
assert len(sources)==3118
if A.new_source_identity:
 assert pathlib.Path(A.new_source_identity).name.upper()=="COMMON_PC.OLB"
 assert pathlib.Path(A.new_source_identity).is_file()
 for x in plan["object_mappings"]+plan["native_cache_selectors"]+plan["instance_source_changes"]:x["new_source"]=A.new_source_identity
 plan["target_new_library"]=A.new_source_identity
guardRows=[];fpchanges=[];counts=collections.Counter()
for page in tree.findall("./Schematic/Page"):
 pn=d(page)["name"]
 for typ in ["PartInst","Global","OffPageConnector","Port"]:
  for inst in page.findall(typ):
   a=d(inst);ident=a["dbId"];key=(typ,ident)
   assert key in sources
   row=sources[key]
   assert row["page"]==pn and row["old_source"]==a["libName"]
   g={"page":pn,"old_source":a["libName"],"new_source":row["new_source"],
      "location":a["locX"]+" "+a["locY"],"rotation":a["rotation"],"mirror":a.get("mirror","0")}
   if typ=="PartInst":
    ref=d(inst.find("Reference"))["name"];val=d(inst.find("PartValue"))["name"]
    props={}
    for item in inst.findall("PartInstUserProp"):
     pd=d(item);props.setdefault(pd["name"],[]).append(pd["val"])
    assert len(props.get("PCB Footprint",[]))==1 and len(props.get("User_Value",[])) in (0,1)
    old=props["PCB Footprint"][0];m=mi[ident]
    assert m["page"]==pn and m["ref"]==ref and m["instance"]==a["name"] and m["old_footprint"]==old
    new=m["proposed_target"]
    assert new and re.fullmatch(r"[A-Za-z0-9_,.+()# -]+",new),"Unexpected footprint name characters"
    g.update(ref=ref,value=val,footprint=old)
    if "User_Value" in props:g["user_value"]=props["User_Value"][0]
    else:g["user_value_explicit_absent"]="1"
    if old!=new:fpchanges.append({"ref":ref,"page":pn,"id":ident,"old_value":old,"new_value":new,
                                  "attribute_scope":"PartInstUserProp/Defn/@val","property_name":"PCB Footprint",
                                  "instance_xml_name":a["name"],"package":a["pkgName"]})
   else:
    g["net_name"]=a["name"]
   guardRows.append((typ,ident,g));counts[typ]+=1
assert len(guardRows)==3118 and counts=={"PartInst":1131,"Global":840,"OffPageConnector":1147}
assert len(fpchanges)==0, "Cache7 must not edit instanceFP"
plan["pcb_footprint_changes"]=fpchanges
plan["source_xml_sha256"]=fs(xml)
plan["source_plan_binding"]={"path":str(A.source_plan),"sha256":fs(A.source_plan)}
plan["instance_footprint_mapping_binding"]={"path":str(A.instance_map),"sha256":fs(A.instance_map)}
plan["native_instance_counts"]=dict(counts)
plan["cache_default_pcb_footprint_changes"]=[]
plan["metadata_changes"]=[]
plan["status"]="FROZEN_NATIVE_SOURCE_AND_INSTANCE_FOOTPRINT_PLAN"
plan["native_script"]="apply_capture13_public_sources.tcl"
planPath=A.out/"CAPTURE13_FROZEN_PLAN.json"
planPath.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
lines=["# Generated frozen data only. No CAD calls.",'set sourceSelectors [list \\']
for x in plan["native_cache_selectors"]:lines.append(" "+td(x)+" \\")
lines.append("]")
lines.append("set expectedCacheCounts "+td(plan["cache_expected"]))
lines.append("set expectedInstanceCounts "+td(dict(counts)))
lines.append("set instanceGuards [dict create]")
for typ,ident,g in guardRows:
 # location must be a Tcl two-integer list; its safely quoted string is list-compatible.
 lines.append("dict set instanceGuards [list "+q(typ)+" "+q(ident)+"] "+td(g))
lines.append("set footprintPlan [dict create]")
for x in fpchanges:
 lines.append("dict set footprintPlan "+q(x["id"])+" "+td({"before":x["old_value"],"after":x["new_value"]}))
tclPath=A.out/"CAPTURE13_FROZEN_PLAN.tcl"
tclPath.write_text("\n".join(lines)+"\n",encoding="utf-8")
receipt={"status":"FROZEN_NATIVE_PLAN_COMPILED_NOT_EXECUTED","plan":str(planPath),"plan_sha256":fs(planPath),
 "tcl":str(tclPath),"tcl_sha256":fs(tclPath),"source_xml_sha256":fs(xml),"native_cache_selectors":len(plan["native_cache_selectors"]),
 "guarded_instances":dict(counts),"footprint_changes":len(fpchanges),"distinct_ref_footprint_changes":len({r["ref"] for r in fpchanges}),
 "library_identity":plan["target_new_library"],
 "scope":"Only sourceLibName/libName plus explicit instance PCB Footprint; all Package names/defaults, instance Values/NC_/metadata, electrical graph and geometry unchanged."}
(A.out/"NATIVE_PLAN_COMPILATION.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt,ensure_ascii=False,indent=2))