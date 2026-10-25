"""Read-only dependency probe. It never starts Cadence, a GUI or a watcher.
Writes one new JSON only below this lesson inventory; refuses overwrite.
Use the exact Python binary on the target Windows computer.
"""
from pathlib import Path
import argparse, datetime, importlib, importlib.metadata, json, platform, shutil, sys
P=Path(__file__).resolve()
ROOT=P.parents[4]
INVENTORY=P.parent
p=argparse.ArgumentParser()
p.add_argument("--cadence-root",default=r"C:\Program0\Cadence\SPB172")
p.add_argument("--output",required=True)
a=p.parse_args()
out=Path(a.output).resolve()
if not out.is_relative_to(INVENTORY) or out.exists(): raise SystemExit("Use a NEW JSON filename under this lesson inventory.")
C=Path(a.cadence_root).resolve()
package_dirs=[
 ("pymupdf","learning/tools/pymupdf_1_28_2"),
 ("hi_geometry","learning/examples/lessonHI_38_50_20261021/tooling/packages"),
 ("jk_cam","learning/examples/lessonJK_51_59_20261022/tooling/packages")]
for _,rel in package_dirs: sys.path.insert(0,str(ROOT/rel))
modules=[]
for name in ["pymupdf","numpy","shapely","gerbonara","rtree","click","yaml"]:
 try:
  m=importlib.import_module(name)
  try: version=importlib.metadata.version("PyMuPDF" if name=="pymupdf" else name)
  except importlib.metadata.PackageNotFoundError: version=str(getattr(m,"VersionBind",None))
  modules.append({"module":name,"status":"IMPORT_OK","version":version,"file":str(getattr(m,"__file__",None))})
 except Exception as e: modules.append({"module":name,"status":"IMPORT_FAILED","error":str(e)})
exes=["allegro.exe","Capture.exe","padstack_editor.exe","extracta.exe","netrev.exe","artwork.exe","nctape.exe","ncroute.exe","pstswp.exe"]
manuals=[
 "doc/algroskill/01ovrvew.html","doc/algroskill/07dbaccs.html",
 "doc/orcadtclgsg/Setting_up_the_OrCAD_TCL_Environment.html",
 "doc/orctclcap/Getting_Pin_Names_from_a_Library_Part.html",
 "doc/capinfomodel/dboimnew.html",
 "tools/capture/tclscripts/OrCAD_Capture_TclTk_Extensions.pdf",
 "tools/capture/tclscripts/capPSpiceModelApp/PWL/Digital/Gates/OR/tcl/PwlORSymbolCreate.tcl"]
source_dirs=["learning/sources","learning/examples/lessonJK_51_59_20261022/source/bench_datasheets"]
source_items=[]
for rel in source_dirs:
 for f in sorted((ROOT/rel).rglob("*")):
  if f.is_file(): source_items.append({"path":f.relative_to(ROOT).as_posix(),"bytes":f.stat().st_size,"kind":"DATASHEET" if f.suffix.lower()==".pdf" else "MANIFEST_OR_REFERENCE"})
data={
 "schemaVersion":1,"lesson":60,"observedAtUTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "clientDate":"2026-10-23","clientTimezone":"Asia/Shanghai",
 "status":"READ_ONLY_LOCAL_DEPENDENCY_OBSERVATION",
 "scope":{"noCadenceOrGuiStarted":True,"noEnvironmentDump":True,"noLicenseOrCredentialRead":True,"noOriginalFilesChanged":True,"noGlobalInstall":True,"noFullDriveSearch":True,"noHistoricalManifestRehash":True,"output":str(out)},
 "roots":{"recordRoot":str(ROOT),"cadenceRoot":str(C),"lessonRoot":str(INVENTORY.parent)},
 "machine":{"os":platform.system(),"osVersion":platform.version(),"architecture":platform.machine(),"pythonVersion":sys.version,"pythonExecutable":sys.executable},
 "pathCommands":[{"name":n,"resolved":shutil.which(n),"meaning":"PATH lookup only; null is not proof absent from whole computer."} for n in ["python","py","ffmpeg","ffprobe","tesseract","pdftotext","pdftoppm","git"]],
 "cadenceFiles":[{"path":str(C/"tools/bin"/n),"exists":(C/"tools/bin"/n).is_file(),"execution":"NOT_STARTED_BY_THIS_PROBE"} for n in exes],
 "cadenceFileVersionObservation":{"method":"PowerShell FileVersionInfo read only, earlier same lesson","allegro.exe":"17.2-2016","Capture.exe":"17.2-2016","patchLevel":"NOT_REDERIVED_FROM_FILE_METADATA; 17.2-S045 is historical native-log evidence and needs fresh native verification"},
 "captureSdk":[{"path":str(C/f),"exists":(C/f).is_file(),"execution":"NOT_LOADED_BY_THIS_PROBE"} for f in ["tools/bin/orDb_Dll_Tcl64.dll","tools/bin/orTclAutomation64.dll","tcltk/bin/tclsh.exe"]],
 "installedOfficialReferences":[{"path":str(C/f),"exists":(C/f).is_file(),"migration":"Locate from the new legal installation; retain only source locator/page references in this lesson."} for f in manuals],
 "localPackagePaths":[{"purpose":label,"path":str(ROOT/rel),"exists":(ROOT/rel).is_dir()} for label,rel in package_dirs],
 "packageImports":modules,
 "sourceInventory":source_items,
 "guiStatus":"NOT_PROBED_BY_THIS_AGENT; historical native-pipe failure is not a fresh failure or a permanent capability judgment.",
 "captureCapabilities":{"plainTcl":"Interpreter language and file operations; does not imply Dbo API available.","nativeSdk":"DLL and standalone runtime exist; earlier C11-C14 native database exercises are historical evidence, not current GUI proof.","guiCommands":"Selection, active-document menu, viewport, ERC/printing must be separately exercised in the actual app session.","databaseObjects":"Process-local DBIDs/session objects must be resolved again after reopen, not moved as persistent handles."},
 "migrationMeaning":{"records":"Local files carry procedures, evidence and limitations; available only if copied/backed up and read in the next session.","model":"No claim of model retraining or permanent mastery from these files.","cloud":"This probe neither uploads files nor proves any cloud synchronization; no automatic sync is assumed.","newComputer":"Software, compatible runtime, legal licensing and a fresh smoke-test are separate from copying records."}
}
out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"created":str(out),"modules":[{"module":x["module"],"status":x["status"],"version":x.get("version")} for x in modules],"cadenceFilesExisting":sum(x["exists"] for x in data["cadenceFiles"]),"manualsExisting":sum(x["exists"] for x in data["installedOfficialReferences"])},ensure_ascii=True))
