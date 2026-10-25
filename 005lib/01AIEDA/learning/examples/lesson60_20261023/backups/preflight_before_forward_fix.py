import argparse,json,hashlib,sys
from pathlib import Path
def main():
 ap=argparse.ArgumentParser(description="Read-only learning-root inventory; not a native/GUI/license test.")
 ap.add_argument("--root",required=True,type=Path);ap.add_argument("--cadence-root",type=Path);ap.add_argument("--out",type=Path)
 a=ap.parse_args();root=a.root.resolve()
 required=["EDA.md","\u8bfe\u7a0b\u7d22\u5f15.md","learning/notes/pcb_layer_naming.md","learning/notes/package_defaults.md"]
 files=[{"relative":r,"exists":(root/r).is_file()}for r in required]
 fixture=root/"learning/examples/lessonJK_51_59_20261022/native/4L/JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd"
 expected="471176A9B25BA8DEF9F117AEFB1E9220CBCBEBBAC5191BCBC6E228F52831F3F9"
 actual=hashlib.sha256(fixture.read_bytes()).hexdigest().upper()if fixture.is_file()else None
 native={"configured":a.cadence_root is not None,"allegroExeExists":False,"captureExeExists":False}
 if a.cadence_root:
  c=a.cadence_root.resolve();native.update({"installationRoot":str(c),"allegroExeExists":(c/"tools/bin/allegro.exe").is_file(),"captureExeExists":(c/"tools/bin/capture.exe").is_file()})
 ok=all(x["exists"]for x in files)and actual==expected
 d={"status":"LEARNING_FILES_AND_FIXED_FIXTURE_CHECKED"if ok else"LEARNING_INPUTS_MISSING_OR_DIFFERENT","root":str(root),"pythonVersion":sys.version,"requiredFiles":files,"historicalFixture":{"path":str(fixture),"expectedSHA256":expected,"actualSHA256":actual,"matched":actual==expected},"cadenceInventory":native,"nativeExecution":"NOT_TESTED_BY_PREFLIGHT","license":"NOT_TESTED_BY_PREFLIGHT","GUI":"NOT_TESTED_BY_PREFLIGHT","secondPhysicalComputer":"NOT_TESTED","readOnly":True}
 text=json.dumps(d,ensure_ascii=False,indent=2)
 if a.out:
  out=a.out.resolve()
  if not out.is_relative_to(root):ap.error("--out must remain inside the learning root")
  out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text,encoding="utf8")
 print(text)
 return 0 if ok else 2
if __name__=="__main__":raise SystemExit(main())
