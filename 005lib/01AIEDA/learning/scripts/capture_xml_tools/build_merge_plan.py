"""Build a hash-locked proposal from a read-only cache inventory.
No CAD execution; conditional materialization remains opt-in by property name."""
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser()
p.add_argument("--audit",type=Path,required=True)
p.add_argument("--mode",choices=["strict","scoped"],required=True)
p.add_argument("--group",action="append",default=[])
p.add_argument("--materialize-property",action="append",default=[])
p.add_argument("--output",type=Path,required=True)
a=p.parse_args()
assert not a.output.exists(),"Fresh plan output required"
summary=json.loads((a.audit/"LIBRARY_REUSE_XML_AUDIT_SUMMARY.json").read_text(encoding="utf-8-sig"))
assert summary["reference_error_count"]==0,"Resolve reference graph errors before planning"
allgroups=json.loads((a.audit/"package_reuse_candidate_groups.json").read_text(encoding="utf-8-sig"))
mode="STRICT_ALIAS_ONLY" if a.mode=="strict" else "STRUCTURE_PLUS_EXPLICIT_DEFAULTS_REQUIRED"
groups=[g for g in allgroups if g["mode"]==mode and (not a.group or g["group_id"] in a.group)]
assert groups,"No selected candidate groups"
assert not set(a.group)-{g["group_id"] for g in groups},"Unknown/incompatible selected group"
if a.mode=="strict":
 merges=[]
 for g in groups:
  for m in g["members"]:
   if (m["package"],m["source_lib"])==(g["canonical_package"],g["canonical_lib"]):continue
   merges.append({"old_package":m["package"],"old_lib":m["source_lib"],"canonical_package":g["canonical_package"],"canonical_lib":g["canonical_lib"],"full_identity_normalized_sha256":g["sha256"]})
 plan={"mode":"STRICT_IDENTITY_ONLY","input_xml_sha256":summary["input_xml_sha256"],"merge_count":len(merges),"merges":merges}
else:
 plan={"mode":"CONDITIONAL_SCOPED_DEFAULT_FLATTEN","input_xml_sha256":summary["input_xml_sha256"],"merge_count":sum(len(g["members"])-1 for g in groups),"allowed_materialize_missing_property_names":sorted(set(a.materialize_property)),"groups":groups}
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_text(json.dumps(plan,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"mode":plan["mode"],"merge_count":plan["merge_count"],"output":str(a.output)},ensure_ascii=True))
