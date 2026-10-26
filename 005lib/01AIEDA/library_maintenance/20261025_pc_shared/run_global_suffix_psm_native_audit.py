"""Prepared root-only native audit. Importing this module does not run CAD."""
import argparse,collections,concurrent.futures,hashlib,importlib.util,json,pathlib,shutil,time
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest().upper()
def dump(p,x):pathlib.Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--plan",type=pathlib.Path,required=True)
 ap.add_argument("--output",type=pathlib.Path,required=True)
 ap.add_argument("--chunk-size",type=int,default=100)
 ap.add_argument("--metadata-workers",type=int,default=4)
 ap.add_argument("--timeout-per-chunk",type=int,default=1200)
 a=ap.parse_args()
 assert a.chunk_size>0 and 1<=a.metadata_workers<=4
 assert not a.output.exists(),"Fresh isolated output required"
 plan=json.loads(a.plan.read_text(encoding="utf-8-sig"))
 assert plan["schema"]=="GLOBAL_SUFFIX_PUBLIC_NATIVE_AUDIT_PLAN_V1"
 guard_path=pathlib.Path(plan["public_guard_manifest"])
 guards=json.loads(guard_path.read_text(encoding="utf-8-sig"))["files"]
 for x in plan["helpers"]:assert sha(x["path"])==x["sha256"],"Audit helper or EMPTY4 changed"
 helper=next(pathlib.Path(x["path"]) for x in plan["helpers"] if pathlib.Path(x["path"]).name=="run_pc_native_audit.py")
 spec=importlib.util.spec_from_file_location("global_suffix_base_audit",helper);b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
 empty=next(pathlib.Path(x["path"]) for x in plan["helpers"] if pathlib.Path(x["path"]).name=="EMPTY4.brd")
 native=next(pathlib.Path(x["path"]) for x in plan["helpers"] if pathlib.Path(x["path"]).name=="psm_native_units.il")
 def check_guards(label):
  bad=[x["path"] for x in guards if not pathlib.Path(x["path"]).is_file() or sha(x["path"])!=x["sha256"]]
  if bad:raise RuntimeError("Protected public file changed at "+label+": "+repr(bad[:20]))
 a.output.mkdir(parents=True);check_guards("before native execution")
 dump(a.output/"INPUT_BINDINGS.json",{"plan":str(a.plan),"plan_sha256":sha(a.plan),"guard_manifest":str(guard_path),"guard_manifest_sha256":sha(guard_path),"guarded_files":len(guards),"helpers":plan["helpers"],"runner":str(pathlib.Path(__file__)),"runner_sha256":sha(__file__)})
 rows=plan["representatives"];allrows=[];launches=[]
 print(json.dumps({"stage":"native_all_candidates_start","candidates":plan["selected_psm_count"],"representatives":len(rows),"chunks":(len(rows)+a.chunk_size-1)//a.chunk_size,"public_guard_files":len(guards),"metadata_workers":a.metadata_workers}),flush=True)
 for offset in range(0,len(rows),a.chunk_size):
  index=offset//a.chunk_size;r=a.output/f"c{index:03}";r.mkdir()
  for n in ["units","output"]:(r/n).mkdir()
  env=b.envfor(r);batch=[]
  for j,item in enumerate(rows[offset:offset+a.chunk_size]):
   assert sha(item["path"])==item["sha256"],"PSM changed since frozen plan"
   batch.append(dict(mode="public_global_suffix",source_name=item["stem"],stem=item["stem"],path=item["path"],source_path=item["path"],source_sha256=item["sha256"],alias_sha256=item["sha256"],audit_output=str(r/"output"/f"{j:04}.sexp"),byte_identical_members=item["byte_identical_members"],frozen_classification=item["classification"],canonical_candidate=item["canonical_candidate"]))
  print(json.dumps({"stage":"metadata_begin","chunk":index,"expected":len(batch),"offset":offset}),flush=True)
  completed=0
  with concurrent.futures.ThreadPoolExecutor(max_workers=a.metadata_workers) as pool:
   futures={pool.submit(b.metadata,row,r,env,i):i for i,row in enumerate(batch)}
   for future in concurrent.futures.as_completed(futures):
    future.result();completed+=1
    if completed%20==0 or completed==len(batch):print(json.dumps({"stage":"metadata_progress","chunk":index,"complete":completed,"expected":len(batch)}),flush=True)
  blank=r/"blank.brd";shutil.copyfile(empty,blank)
  jobs=[]
  for row in batch:
   box=row["original_extents"];lit="(("+" ".join(box[0])+") ("+" ".join(box[1])+"))"
   jobs.append("("+b.q(row["stem"])+" "+b.q(row["audit_output"])+" "+b.q(row["original_units"])+" "+str(row["original_accuracy"])+" "+lit+")")
  (r/"jobs.il").write_text("psmNativeBatch("+b.q(blank)+" '("+"\n".join(jobs)+") "+b.q(r/"status.tsv")+" "+b.q(plan["psmpath"])+" "+b.q(plan["padpath"])+")\n",encoding="ascii")
  (r/"run.scr").write_text("set NOCONFIRM\nskill errset(load("+b.q(native)+") t)\nskill errset(load("+b.q(r/"jobs.il")+") t)\nquit\nfillin \"yes\"\n",encoding="ascii")
  dump(r/"manifest.json",batch)
  print(json.dumps({"stage":"allegro_chunk_begin","chunk":index,"expected":len(batch),"four_layer_blank_sha256":sha(empty)}),flush=True)
  rec=b.launch([b.CAD/"tools/bin/allegro.exe","-product","Allegro_performance","-safe","-nographic","-s",r/"run.scr","-p",r,blank],r,env,a.timeout_per_chunk,"allegro")
  status=(r/"status.tsv").read_text(encoding="utf-8",errors="replace") if (r/"status.tsv").is_file() else ""
  outputs=sum(pathlib.Path(row["audit_output"]).is_file() for row in batch)
  rec.update(chunk=index,expected=len(batch),outputs=outputs,complete=status.rstrip().endswith("COMPLETE"),manifest=str(r/"manifest.json"),manifest_sha256=sha(r/"manifest.json"))
  dump(r/"launch_report.json",rec);launches.append(rec);allrows.extend(batch)
  dump(a.output/"manifest.json",allrows);dump(a.output/"CHUNK_PROGRESS.json",{"completed_chunks":len(launches),"expected_representatives":len(rows),"completed_rows":len(allrows),"launches":launches})
  check_guards("after chunk "+str(index))
  print(json.dumps({"stage":"allegro_chunk_end",**rec}),flush=True)
  if rec["exit_code"]!=0 or not rec["complete"] or outputs!=len(batch):raise RuntimeError("Incomplete native chunk; outputs retained, no geometry equivalence claimed")
 check_guards("after all native execution")
 result={"status":"RAW_COMPLETE_NATIVE_EXPORTS_REQUIRE_FULL_GEOMETRY_PAD_ATTRIBUTE_REVIEW","selected_psm_count":plan["selected_psm_count"],"native_representatives":len(rows),"outputs":sum(r["outputs"] for r in launches),"all_chunks_complete":True,"public_files_unchanged":True,"guarded_file_count":len(guards),"psmpath":plan["psmpath"],"padpath":plan["padpath"],"context":"EMPTY4 four conductor layers; per-source native units/accuracy/extents; no preloaded symdefs/padstacks; public-only library paths","launches":launches,"not_authorized_by_this_report":"No library deletion, alias rewrite, current engineering board change, or geometry equivalence is established by native export success alone"}
 dump(a.output/"report.json",result);print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=="__main__":main()