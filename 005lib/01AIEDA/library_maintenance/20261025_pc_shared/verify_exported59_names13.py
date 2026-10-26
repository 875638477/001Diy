"""Readonly actual dump_libraries package-name verification; no CAD or input writes."""
import argparse,pathlib,csv,json,hashlib,re,collections
P=argparse.ArgumentParser()
P.add_argument("--export-directory",type=pathlib.Path,required=True)
P.add_argument("--definition-directory",type=pathlib.Path,required=True)
P.add_argument("--out",type=pathlib.Path,required=True)
P.add_argument("--retirement-plan",type=pathlib.Path,required=True)
A=P.parse_args();assert not A.out.exists(),"Fresh verification directory required";A.out.mkdir(parents=True)
def fs(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def read(p):return json.loads(p.read_text(encoding="utf-8-sig"))
index=A.definition_directory/"ALL_PACKAGE_DEFINITIONS.tsv"
with index.open(encoding="utf-8-sig",newline="") as f:rows=list(csv.DictReader(f,delimiter="\t"))
assert rows and all(x["objType"]=="symdef" for x in rows)
names=[x["name"].casefold() for x in rows]
assert len(names)==len(set(names)),"Duplicate casefold definition names"
assert all(int(x["usedCount"])>0 for x in rows),"Unexpected unused definition in final saved inventory"
expected=set(names)
exp_launch=A.export_directory/"launch_report.json"
def_launch=A.definition_directory/"launch_report.json"
e=read(exp_launch);d=read(def_launch)
assert e["exit_code"]==d["exit_code"]==0
source=pathlib.Path(e["source"])
assert str(source).casefold()==str(d["source"]).casefold()
source_sha=fs(source)
assert source_sha==e["source_sha256_before"]==e["source_sha256_after"]==e["copy_sha256"]
assert source_sha==d["source_sha256_before"]==d["source_sha256_after"]==d["staged_sha256"]
assert fs(A.export_directory/"INPUT_COPY.brd")==fs(A.definition_directory/"INPUT_COPY.brd")==source_sha
assert e["arguments"].startswith("-ac "),"Unexpected export mode"
assert pathlib.Path(e["exe"]).name.casefold()=="dump_libraries.exe"
assert fs(pathlib.Path(e["exe"]))==e["exe_sha256"]
files=[];sets={}
for ext in [".psm",".dra"]:
 collection=sorted(p for p in A.export_directory.iterdir() if p.is_file() and p.suffix.casefold()==ext)
 stems=[p.stem.casefold() for p in collection]
 assert len(stems)==len(set(stems)),"Duplicate casefold export file names"
 sets[ext]=set(stems)
 for p in collection:files.append({"relative":p.name,"bytes":p.stat().st_size,"sha256":fs(p)})
bad=lambda n: bool(re.fullmatch(r"[cr]\d{4,5}.*",n)) and not bool(re.fullmatch(r"[cr]\d{4,5}_pc",n))
old_names=sorted(n for n in expected|sets[".psm"]|sets[".dra"] if bad(n))
diffs=[]
for ext,s in sets.items():
 if s!=expected:diffs.append({"extension":ext,"missing":sorted(expected-s),"unexpected":sorted(s-expected)})
if old_names:diffs.append({"old_generic_cr_names":old_names})
retirement=read(A.retirement_plan)
retired=set(x.casefold() for x in retirement["accepted_source_stems"])
assert len(retired)==1067 and fs(A.retirement_plan)=="77C97D6EDE67D8AA80C324DF87688661C6F93E58679E76CAB6505F17AE5E47F5"
retired_hits=sorted((expected|sets[".psm"]|sets[".dra"])&retired)
if retired_hits:diffs.append({"confirmed_retired_alias_names":retired_hits})
log=A.export_directory/"dump_libraries.log"
log_text=log.read_text(encoding="utf-8-sig",errors="replace")
errors=re.search(r"ERRORs reported:\s*(\d+)",log_text)
npkg=re.search(r"Number of package symbols dumped:\s*(\d+)",log_text)
assert errors and int(errors.group(1))==0
assert npkg and int(npkg.group(1))==len(expected)
bindings=[A.retirement_plan,index,exp_launch,def_launch,log,A.export_directory/"INPUT_COPY.brd",A.definition_directory/"INPUT_COPY.brd",source]
bound=[{"path":str(p),"sha256":fs(p),"bytes":p.stat().st_size} for p in bindings]
summary={"status":"PASS_ALL59_SAVED_DEFINITIONS_EXPORTED_NO_RETIRED_ALIASES_OR_OLD_CR_NAMES" if not diffs and len(expected)==59 else "FAIL",
 "scope":"Package export names, complete persisted definition inventory and exact source-board binding only; not a PCB copper/rules/manufacturing or final publication approval.",
 "source_board":str(source),"source_board_sha256":source_sha,
 "definition_inventory":str(index),"definition_inventory_sha256":fs(index),"definition_count":len(expected),
 "all_definition_used_counts_positive":True,"sum_definition_instances":sum(int(x["usedCount"]) for x in rows),
 "export_directory":str(A.export_directory),"native_export_exit_code":e["exit_code"],"dump_libraries_log_errors":int(errors.group(1)),
 "psm_count":len(sets[".psm"]),"dra_count":len(sets[".dra"]),
 "psm_stems_equal_all_definitions":sets[".psm"]==expected,"dra_stems_equal_all_definitions":sets[".dra"]==expected,
 "retired_alias_name_hits":retired_hits,"retirement_plan_sha256":fs(A.retirement_plan),"old_generic_cr_name_count":len(old_names),"old_generic_cr_names":old_names,
 "old_cr_rule":"case-insensitive c/r + 4/5 digit size must be exactly <category><size>_pc; catches unsuffixed names and PP/frame/line/numeric suffix variants.",
 "difference_count":len(diffs),"differences":diffs,"all_package_names":sorted(expected),
 "input_protection":"Readonly file inputs; all bound source/copy/native reports and every exported PSM/DRA hashed and rechecked after comparison."}
(A.out/"PACKAGE_EXPORT_NAME_VERIFICATION.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(A.out/"EXPORTED_PACKAGE_FILE_SHA256.json").write_text(json.dumps({"files":files,"bindings":bound},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
for b in bound:assert fs(pathlib.Path(b["path"]))==b["sha256"],"Input changed during comparison"
for f in files:assert fs(A.export_directory/f["relative"])==f["sha256"],"Export file changed during comparison"
print(json.dumps({k:v for k,v in summary.items() if k!="all_package_names"},ensure_ascii=False,indent=2))
raise SystemExit(0 if summary["status"].startswith("PASS_") else 2)