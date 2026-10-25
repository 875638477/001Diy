import pathlib,hashlib,json,struct,shutil,os,datetime
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");C=pathlib.Path(r"C:\Program0\Cadence\SPB172")
files=[];notes=[]
for name in("bem2d.exe","bem2d2.exe","bem2d3.exe"):
 p=C/"tools/bin"/name;b=p.read_bytes();o=struct.unpack_from("<I",b,0x3c)[0];machine,nsect,_,_,_,optsz,_=struct.unpack_from("<HHIIIHH",b,o+4);opt=o+24;magic=struct.unpack_from("<H",b,opt)[0];dirs=opt+(112 if magic==0x20b else 96);importrva,importsize=struct.unpack_from("<II",b,dirs+8)
 sections=[]
 for i in range(nsect):
  s=opt+optsz+i*40;vsize,va,rsize,rp=struct.unpack_from("<IIII",b,s+8);sections.append((va,max(vsize,rsize),rp))
 def off(rva):
  for va,sz,rp in sections:
   if va<=rva<va+sz:return rp+rva-va
  return rva
 imports=[];ip=off(importrva)
 while importrva and any(struct.unpack_from("<IIIII",b,ip)):
  nrva=struct.unpack_from("<I",b,ip+12)[0];no=off(nrva);end=b.index(b"\0",no);dll=b[no:end].decode("ascii",errors="replace")
  candidates=[C/"tools/bin"/dll,pathlib.Path(r"C:\Windows\System32")/dll,pathlib.Path(r"C:\Windows\SysWOW64")/dll]
  imports.append({"dll":dll,"existingCandidates":[str(x) for x in candidates if x.exists()]});ip+=20
 files.append({"path":str(p),"size":len(b),"sha256":hashlib.sha256(b).hexdigest(),"PEMachine":hex(machine),"PEOptionalMagic":hex(magic),"imports":imports,"executed":False})
for rel in("cmref/analyze.html","ccoms/cchap.html","algrodesrls/chap3.html"):
 p=C/"doc"/rel;out=R/"source"/("Cadence172_"+rel.replace("/","_"));shutil.copy2(p,out);notes.append({"original":str(p),"archived":str(out),"sha256":hashlib.sha256(out.read_bytes()).hexdigest()})
report={"date":datetime.datetime.now().astimezone().isoformat(),"status":"READ_ONLY_OFFICIAL_DOC_AND_EXECUTABLE_INVENTORY_NO_CADENCE_EXECUTION","officialFindings":[{"source":"cmref/analyze.html:678-735","finding":"Length or time based constraints; pin/Zaxis inclusion options. Z-axis derives between connected signal layers."},{"source":"ccoms/cchap.html:3988","finding":"Zaxis excluded from totaletch length anddisabledbydefault."},{"source":"cmref/analyze.html:844","finding":"All differential pair checks switches phase,uncoupled,minspacing together; do not disableit to evade solver."}],"notFound":"No official documented MM-only switch that guarantees no internal bem2d while retaining all differential checks was located in searched local172docs. No invented envvariable proposed.","processPathHypothesis":{"currentReadOnlyShellWhichBem2d":shutil.which("bem2d"),"launcher":"scripts/launchHI.py inheritsenvironment and doesnot explicitlyaddtools/bin toPATH; nativeSignoise usesbarecommandbem2d. Need inspectactualchildPATH/which and controllednative rerun; this reportdoesnot assertrootcause."},"executables":files,"officialSources":notes}
(R/"review/cadence_fieldsolver_readonly_diagnostic.json").write_text(json.dumps(report,indent=2),encoding="utf-8");print(json.dumps({"which":report["processPathHypothesis"]["currentReadOnlyShellWhichBem2d"],"files":[{"name":pathlib.Path(f["path"]).name,"machine":f["PEMachine"],"importsMissingFromBinSystem32WOW64":[x["dll"] for x in f["imports"] if not x["existingCandidates"]]} for f in files]},ensure_ascii=True))
