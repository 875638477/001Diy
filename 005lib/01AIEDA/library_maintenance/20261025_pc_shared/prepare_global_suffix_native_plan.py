"""Readonly public library scope inventory + frozen native audit inputs. Does not launch CAD."""
import argparse,pathlib,re,json,hashlib,collections
P=argparse.ArgumentParser();P.add_argument("--out",type=pathlib.Path,required=True);A=P.parse_args()
assert not A.out.exists(),"Fresh inventory directory required";A.out.mkdir(parents=True)
BASE=pathlib.Path(r"D:/001DIY/005lib")
ROOTS=[BASE/n for n in ["01Psm_lib","01brdlib","01Pad_lib","01captureLib","01script_file","01env"]]
R=pathlib.Path(r"D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025")
M=BASE/"01AIEDA/library_maintenance/20261025_pc_shared"
known=set("01005 0201 0402 0603 0805 1005 1206 1210 1806 1812 1825 2010 2012 2220 2512 2520 3030 3225 4032 5025 5650".split())
family=re.compile(r"^(r|c|l|fb)(\d{4,5})(?!\d)(.*)$",re.I)
numeric=re.compile(r"^("+"|".join(sorted(known,key=len,reverse=True))+r")(.*)$",re.I)
special={"ao3414_sot23-3":"sot23-3","sot23-3":"sot23-3","ao4468_so8":"sop-8-150mil","sop-8-150mil":"sop-8-150mil","sot23_123":"sot23-3"}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def dump(n,x):(A.out/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def classify(stem):
 s=stem.casefold()
 if s in special:return dict(family="EXPLICIT_SOT_SO",size="",suffix="",canonical_candidate=special[s],classification="USER_EXPLICIT_EQUIVALENCE_OR_NATIVE_COMPARISON",native_audit=True)
 m=family.fullmatch(stem)
 if m:
  f,z,tail=m.groups();f=f.casefold()
  classification="ORDINARY_SIZE_FAMILY_CANDIDATE_REQUIRES_NATIVE_GEOMETRY_AND_REFERENCE_REVIEW"
  canonical=f+z+"_pc"
  if z not in known or re.search(r"4p|qfn|sp|noskil|fcs",tail,re.I):
   classification="EXTENDED_OR_FUNCTIONAL_SCHEMA_VARIANT_DO_NOT_DELETE_AS_GARBAGE"
  if re.search(r"qfn|bga|sop|sot",tail,re.I):canonical=None
  return dict(family=f,size=z,suffix=tail,canonical_candidate=canonical,classification=classification,native_audit=True)
 m=numeric.fullmatch(stem)
 if m:
  return dict(family="NUMERIC_WITHOUT_COMPONENT_CATEGORY",size=m.group(1),suffix=m.group(2),canonical_candidate=None,classification="CATEGORY_AMBIGUOUS_DO_NOT_MERGE_R_C_L_FB_FROM_SIZE_ALONE",native_audit=True)
 return None
guards=[];assets=[];root_counts={}
for root in ROOTS:
 files=sorted((p for p in root.rglob("*") if p.is_file()),key=lambda p:str(p).casefold())
 root_counts[str(root)]={"files":len(files),"bytes":sum(p.stat().st_size for p in files)}
 for i,p in enumerate(files):
  h=sha(p)
  g={"path":str(p),"relative":str(p.relative_to(root)),"root":str(root),"bytes":p.stat().st_size,"sha256":h}
  guards.append(g)
  c=classify(p.stem)
  if c:assets.append(dict(g,extension=p.suffix.casefold(),stem=p.stem,**c))
 print(json.dumps({"stage":"readonly_inventory_root","root":str(root),"files":len(files)}),flush=True)
psm=[x for x in assets if pathlib.Path(x["root"]).name=="01Psm_lib" and x["extension"]==".psm"]
groups=collections.defaultdict(list)
for x in psm:groups[x["sha256"]].append(x)
representatives=[]
for h,members in sorted(groups.items(),key=lambda x:min(y["stem"].casefold() for y in x[1])):
 rep=sorted(members,key=lambda x:x["path"].casefold())[0]
 representatives.append(dict(rep,byte_identical_members=[m["path"] for m in members],representative_index=len(representatives)))
helpers=[R/"w/pcb_migration/run_pc_native_audit.py",
 pathlib.Path(r"D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025/psm_native_units.il"),
 pathlib.Path(r"D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025/psm_export.il"),
 M/"fixture4/EMPTY4.brd",
 pathlib.Path(r"D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025/symbol_probe/units_view.txt")]
plan={"schema":"GLOBAL_SUFFIX_PUBLIC_NATIVE_AUDIT_PLAN_V1","status":"PREPARED_NOT_EXECUTED_NO_DELETION_AUTHORIZATION_IN_THIS_FILE",
 "roots":[str(x) for x in ROOTS],"public_guard_manifest":str(A.out/"PUBLIC_ALL_SIX_ROOTS_SHA256.json"),
 "selected_psm_count":len(psm),"exact_byte_group_count":len(groups),"native_representative_count":len(representatives),
 "grouping_policy":"Only full byte SHA256 equality can share a native representative. No PSM header/string/name normalization or geometry omission. Representatives still require complete native geometry/PAD/attribute comparison before any deletion.",
 "canonical_policy":{"passives":"<actual component category><confirmed size>_pc; unusual materials/pin-count/schema not classified by size alone","ao3414_sot23-3":"sot23-3","ao4468_so8":"sop-8-150mil","sot23_123":"native compare with sot23-3; not assumed equivalent"},
 "psmpath":str(BASE/"01Psm_lib"),"padpath":str(BASE/"01Pad_lib"),
 "helpers":[{"path":str(p),"sha256":sha(p)} for p in helpers],"representatives":representatives}
dump("PUBLIC_ALL_SIX_ROOTS_SHA256.json",{"status":"READONLY_INPUT_SNAPSHOT","files":guards,"roots":root_counts})
dump("MATCHED_ASSETS.json",{"assets":assets})
dump("PSM_NATIVE_AUDIT_PLAN.json",plan)
summary={"status":"READONLY_INVENTORY_AND_NATIVE_PLAN_ONLY_NO_CAD_RUN","roots":root_counts,"all_guarded_files":len(guards),
 "matched_files":len(assets),"matched_by_root_extension":dict(collections.Counter(pathlib.Path(x["root"]).name+"/"+x["extension"] for x in assets)),
 "psm_candidates":len(psm),"native_representatives":len(representatives),"exact_byte_duplicates_eliminated":len(psm)-len(representatives),
 "families":dict(collections.Counter(x["family"]+x["size"] for x in psm)),
 "known_size_candidates":sum(x["family"] in {"r","c","l","fb"} and x["size"] in known for x in psm),
 "explicit_assets":{n:[x["path"] for x in psm if x["stem"].casefold()==n] for n in special},
 "user_spelling_resolution":"User sop8-150mil resolved by root to existing sop-8-150mil; no library created or renamed here.",
 "cannot_delete_by_inventory_alone":"Geometry differs or is unproven; public OLB/default/instance references, scripts/env and native board cache references must be redirected/reviewed before removal.",
 "plan":str(A.out/"PSM_NATIVE_AUDIT_PLAN.json")}
dump("INVENTORY_SUMMARY.json",summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))