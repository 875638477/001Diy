from pathlib import Path
import json,hashlib,re,sys
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent

def load(n):return json.loads((OUT/n).read_text(encoding="utf-8-sig"))
def sha(p):
 h=hashlib.sha256()
 with Path(p).open("rb") as f:
  for b in iter(lambda:f.read(1048576),b""):h.update(b)
 return h.hexdigest().upper()
(OUT/"source_validation.json").write_text(json.dumps({"status":"RUNNING","purpose":"Validation output reserved before checking note links."})+"\n",encoding="utf-8")
checks=[]
def check(name,actual,expected=True):
 checks.append({"check":name,"actual":actual,"expected":expected,"pass":actual==expected})

probe=load("pdf_read_probe.json")
recs=load("tutorial_records.json")["records"]
visual=load("visual_review.json")["records"]
check("exactly_two_scoped_pdf_pages",len(probe["records"]),2)
check("exactly_two_filled_records",len(recs),2)
check("both_full_page_views_logged",len(visual),2)
for p,r,v in zip(probe["records"],recs,visual):
 prefix=r["record_id"]+":"
 check(prefix+"source_sha_syntax",bool(re.fullmatch(r"[A-F0-9]{64}",r["source"]["sha256"])))
 check(prefix+"source_current_sha",sha(r["source"]["original_absolute_path"]),r["source"]["sha256"])
 check(prefix+"probe_and_record_source_identity",p["sha256"],r["source"]["sha256"])
 check(prefix+"physical_api_index",r["locator"]["pdf_api_index_0based"]+1,r["locator"]["pdf_physical_page_1based"])
 check(prefix+"scoped_reading_stage",r["stage"],"READ_SCOPED")
 check(prefix+"no_ocr_claim",r["reading"]["ocr"]["executed"],False)
 check(prefix+"no_native_execution_claim",r["native_execution"]["executed"],False)
 check(prefix+"no_second_pc_claim",r["migration"]["executed_on_second_computer"],False)
 check(prefix+"full_page_view",r["reading"]["full_selected_page_visually_viewed"])
 check(prefix+"image_matches_viewed_sha",sha(OUT/r["reading"]["render_path"]),r["reading"]["render_sha256"])
 check(prefix+"visual_log_sha",v["sha256"],r["reading"]["render_sha256"])
 check(prefix+"probe_view_status",p["visual_review"],"FULL_SELECTED_PAGE_VIEWED")
 check(prefix+"extracted_count",len((OUT/p["extracted_text_file"]).read_text(encoding="utf-8")),p["detected_text_characters"])
check("text_page_nonempty",probe["records"][0]["detected_text_characters"]>0)
check("real_scan_page_zero_text",probe["records"][1]["detected_text_characters"],0)
check("real_scan_page_one_image",probe["records"][1]["page_image_objects"],1)
check("real_scan_selected_printed_page","262",recs[1]["locator"]["printed_page_or_sheet"])
check("real_scan_selected_page_offset",recs[1]["locator"]["pdf_physical_page_1based"]-int(recs[1]["locator"]["printed_page_or_sheet"]),19)
video=load("video_presence_and_scope.json")
check("legacy_vs_current_video_paths",[x["exists"] for x in video["known_video_paths_checked"]],[False,True,True])
for i,v in enumerate(video["known_video_paths_checked"]):
 check("video_"+str(i)+"_no_playback",v["playback_performed_this_lesson"],False)
 check("video_"+str(i)+"_no_audio",v["audio_listened_this_lesson"],False)
 check("video_"+str(i)+"_no_frames",v["frames_viewed_this_lesson"],0)
 check("video_"+str(i)+"_no_timepoints",v["timestamps_learned_this_lesson"],[])
 if v["exists"]:
  check("video_"+str(i)+"_current_sha",sha(v["path"]),v["sha256"])
  check("video_"+str(i)+"_AVI_signature",v["riff_avi_header"])
  check("video_"+str(i)+"_duration_not_claimed",v["duration_seconds_verified_this_lesson"],None)
vt=load("video_segment_template.json")
check("video_template_start_unfilled",vt["segment"]["start_ms"],None)
check("video_template_end_unfilled",vt["segment"]["end_ms"],None)
check("video_template_completion_false",vt["completion"]["full_lecture_completed"],False)
helpj=load("selected_local_help.json")
check("installed_help_current_sha",sha(helpj["source_path"]),helpj["sha256"])
check("help_no_native_run",helpj["native_software_executed"],False)
check("no_pdf_authoring",probe["source_pdf_authoring_performed"],False)
notes=ROOT/"learning/notes/lesson60_sources_20261023.md"
nt=notes.read_text(encoding="utf-8")
check("note_utf8_no_replacement",'\ufffd' not in nt)
# Only relative Markdown links in this source-group note; skip inline code.
links=re.findall(r'\[[^\]]+\]\(([^)]+)\)',nt)
for i,link in enumerate(links):
 check("note_local_link_"+str(i), (notes.parent/link).resolve().is_file())
check("relative_prepare_script_root",'ROOT=Path(__file__).resolve().parents[4]' in (OUT/'prepare_source_examples.py').read_text(encoding='utf-8'))
result={"schema_version":1,"date_local":"2026-10-23","timezone":"Asia/Shanghai","purpose":"Source identity, scoped page-reading evidence and truthful execution/migration status; not CAD correctness or fabrication acceptance.","checks":checks,"pass_count":sum(x["pass"] for x in checks),"fail_count":sum(not x["pass"] for x in checks)}
(OUT/"source_validation.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
# Hash exact source-group outputs, excluding this manifest to avoid self-reference.
files=[p for p in OUT.iterdir() if p.is_file() and p.name!='source_group_artifact_manifest.json']+[notes]
manifest={"schema_version":1,"root_label":"01AIEDA","date_local":"2026-10-23","files":[{"root_relative_path":str(p.relative_to(ROOT)),"bytes":p.stat().st_size,"sha256":sha(p)} for p in sorted(files)],"scope":"Current sources subdirectory and its owned note only; excludes the manifest itself."}
(OUT/"source_group_artifact_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"pass":result["pass_count"],"fail":result["fail_count"],"artifact_files":len(files)},ensure_ascii=True))
if result["fail_count"]:raise SystemExit(1)
