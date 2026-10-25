"""Official Cadence CLI only. All source, runtime and output stays in 01AIEDA."""
import pathlib,os,subprocess,json,datetime,hashlib,sys,shutil
B=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lesson10_connector_20261018")
EXE=pathlib.Path(r"C:\Program0\Cadence\SPB172\tools\bin")
mode=sys.argv[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def run(args,out,timeout=25,terminate_warning=False):
 out.mkdir(exist_ok=True,parents=True)
 assert not (out/"launch.json").exists(),"Fresh log directory required"
 env=os.environ.copy();env["ALLEGRO_PCBENV"]=str(out/"pcbenv")
 env["TEMP"]=env["TMP"]=str(B/"runtime")
 (out/"pcbenv").mkdir(exist_ok=True)
 si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (out/"stdout.txt").open("wb") as o,(out/"stderr.txt").open("wb") as e:
  p=subprocess.Popen(args,cwd=out,env=env,stdout=o,stderr=e,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW)
  try:code=p.wait(timeout=timeout);ended=True;terminated=False
  except subprocess.TimeoutExpired:
   ended=False;code=None;terminated=False
   if terminate_warning:p.terminate();code=p.wait(timeout=10);terminated=True
 record={"mode":mode,"startUTC":start,"args":list(map(str,args)),"pid":p.pid,"completed_normally":ended,"terminated_owned_warning_process":terminated,"exitCode":code}
 (out/"launch.json").write_text(json.dumps(record,indent=2),encoding="utf-8")
 print(json.dumps(record,indent=2),flush=True)
 if not ended and not terminated:raise RuntimeError("Owned process still running, inspect recorded PID and startUTC")
 return record
if mode=="pads":
 for src in sorted((B/"library").glob("*.pxml")):
  out=B/"logs"/("pad_"+src.stem)
  out.mkdir(exist_ok=True)
  local=out/src.name;shutil.copyfile(src,local)
  record=run([str(EXE/"padstack_editor.exe"),"-x",str(local)],out,25,src.stem.endswith("npth065"))
  pads=list(out.glob("*.pad"))
  assert len(pads)==1, f"Expected one imported PAD, got {pads}"
  dst=B/"library"/pads[0].name
  assert not dst.exists(),"Do not overwrite existing library PAD"
  shutil.copyfile(pads[0],dst);assert sha(dst)==sha(pads[0])
  print("PAD "+str(dst)+" "+sha(dst),flush=True)
else:
 target={"package":B/"library/l10_gct_usb4105_gf_a_12land.dra","board":B/"lesson10_connector.brd","read_package":B/"library/l10_gct_usb4105_gf_a_12land.dra","read_board":B/"lesson10_connector.brd"}[mode]
 readonly=mode.startswith("read")
 assert target.exists() if readonly else not target.exists()
 folder={"package":"create_package","board":"create_board","read_package":"reopen_package","read_board":"reopen_board"}[mode]
 script=B/"scripts"/(folder.replace("reopen","read")+".scr")
 out=B/"logs"/folder
 before=sha(target) if readonly else None
 args=[str(EXE/"allegro.exe"),"-product","Allegro_performance","-safe","-nographic"]
 if readonly:args.append("-readonly")
 if target.suffix==".dra":args+=["-symbol","package"]
 args+=["-s",str(script),"-p",str(out),str(target)]
 record=run(args,out)
 assert record["completed_normally"] and record["exitCode"]==0
 assert target.exists(),"No artifact created"
 if readonly:assert before==sha(target),"Readonly SHA changed"
 print("ARTIFACT "+str(target)+" "+sha(target),flush=True)
