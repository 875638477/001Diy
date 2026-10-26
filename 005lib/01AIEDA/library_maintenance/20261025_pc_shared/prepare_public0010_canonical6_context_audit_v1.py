"""Prepare six cold package aliases in actual0010 mm4/10-layer/font context.

No CAD. Public PSM bytes copied under unique temporary names to force package
cache misses; existing PAD cache reuse is explicit and requires independent
full actual-cache PAD versus current public PAD manufacturing proof.
"""
from pathlib import Path
import csv,hashlib,json,shutil,sys
M=Path(__file__).parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
sys.path.insert(0,str(M));from build_public0010_stub_preflight_v1 import balanced
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
sk=lambda p:json.dumps(str(p).replace('\\','/'))
def main():
 D=M/'public0010_canonical6_context_bundle13_v1';assert not D.exists();D.mkdir();(D/'aliases').mkdir()
 names=['c0603_pc','c0805_pc','c1206_pc','r0603_pc','fb0805_pc','l0805_pc'];rows=[]
 for name in names:
  src=M.parents[2]/'01Psm_lib'/(name+'.psm')
  # M is01AIEDA/library_maintenance/date; library root is third parent.
  src=Path(r'D:\001DIY\005lib\01Psm_lib')/(name+'.psm');alias='p0010_cold_'+name;dst=D/'aliases'/(alias+'.psm');assert src.is_file();shutil.copyfile(src,dst);assert sha(src)==sha(dst)
  rows.append(dict(target=name,source=str(src),source_sha256=sha(src),alias=alias,alias_path=str(dst),alias_sha256=sha(dst)))
 jobs='\n'.join('('+sk(r['target'])+' '+sk(r['alias'])+')' for r in rows)
 s='load('+sk(R/'w/pcb_migration/pc13_export_board_definitions.il')+')\nload('+sk(R.parent/'cadence_geometry_merge_20261025/psm_export.il')+')\n'
 s+='''
procedure(pub0010FontContextSnapshot(path)
 let((f n rows p)
  f=outfile(path) n=axlDBGetTextBlockCount() rows=nil
  for(i 1 n p=axlGetParam(sprintf(nil "paramTextBlock:%d" i)) unless(p error("Canonical6 context has missing textblock\\n")) rows=cons(list(i p->??) rows) fprintf(f "%L\\n" list(i p->??))) close(f) reverse(rows)))
procedure(pub0010Canonical6Context(dir)
 let((jobs beforeUnits beforeFonts afterFonts name alias original fresh beforeDefs exported f d)
  sstatus(fullPrecision t) beforeUnits=axlDBGetDesignUnits()
  unless(equal(beforeUnits '("millimeters" 4)) error("Canonical6 must use actual0010 original mm4 context\\n"))
  beforeFonts=pub0010FontContextSnapshot(strcat(dir "/SOURCE_ALL_TEXTBLOCKS_BEFORE.ilist")) beforeDefs=length(axlDBGetDesign()->symdefs)
  jobs='(@JOBS@) exported=0
  axlSetVariable("psmpath" @PSMPATH@) axlSetVariable("padpath" "D:/001DIY/005lib/01Pad_lib")
  f=outfile(strcat(dir "/PACKAGE_SOURCE_AND_UNIQUE_ALIAS_MANIFEST.tsv")) fprintf(f "canonical\\talias\\tsourcecachefile\\tpublicaliasfile\\n")
  foreach(job jobs
   name=car(job) alias=cadr(job)
   original=car(setof(q axlDBGetDesign()->symdefs equal(upperCase(q->name) upperCase(name))))
   unless(original && null(setof(q axlDBGetDesign()->symdefs equal(upperCase(q->name) upperCase(alias)))) error("Canonical6 source missing or alias already cached\\n"))
   pc13ExportOneDefinition(original strcat(dir "/actual_" name ".sexp"))
   unless(psmAuditExport(alias strcat(dir "/public_" name ".sexp")) error("Canonical6 public alias package load failed\\n"))
   fresh=car(setof(q axlDBGetDesign()->symdefs equal(upperCase(q->name) upperCase(alias))))
   unless(fresh && fresh!=original error("Canonical6 package cache miss was not forced\\n"))
   fprintf(f "%s\\t%s\\t%s\\t%s\\n" name alias strcat(dir "/actual_" name ".sexp") strcat(dir "/public_" name ".sexp")) drain(f) exported=exported+1)
  close(f) afterFonts=pub0010FontContextSnapshot(strcat(dir "/SOURCE_ALL_TEXTBLOCKS_AFTER.ilist"))
  unless(equal(beforeUnits axlDBGetDesignUnits()) && equal(beforeFonts afterFonts) && exported==6 && length(axlDBGetDesign()->symdefs)==beforeDefs+6 error("Canonical6 changed source unit/font context or reused package cache\\n"))
  f=outfile(strcat(dir "/CANONICAL6_CONTEXT_COMPLETE.txt")) fprintf(f "SIX_PUBLIC_PACKAGE_BYTE_ALIASES_LOADED_FRESH_IN_ACTUAL0010_MM4_10L_SOURCE_FONTS_CONTEXT\\nNO_BOARD_SAVE_NO_PUBLIC_WRITES\\nEXISTING_PAD_CACHE_REUSE_EXPLICIT_REQUIRES_FULL_PUBLIC_PAD_MANUFACTURING_XML_PROOF\\n") close(f) t))
'''
 s=s.replace('@JOBS@',jobs).replace('@PSMPATH@',sk(str(D/'aliases').replace('\\','/')+' D:/001DIY/005lib/01Psm_lib'));balanced(s);h=D/'public0010_canonical6_context_v1.il';h.write_text(s,'utf-8')
 inputs=[h]+[Path(r['source']) for r in rows]+[Path(r['alias_path']) for r in rows]+[R/'w/pcb_migration/pc13_export_board_definitions.il',R.parent/'cadence_geometry_merge_20261025/psm_export.il',R.parent/'cadence_geometry_merge_20261025/dra_audit/export.il']
 p=D/'MANIFEST.json';p.write_text(json.dumps(dict(schema='PUBLIC0010_CANONICAL6_PACKAGE_CACHEMISS_SAME_NATIVE_CONTEXT_V1',source_board=str(M/'public0010_nil_route_stub_run13_v2_partial/PUB0010_PARTIAL_UNAPPROVED.brd'),source_sha256='1ABA0FDC27DE553535CDE454840EA245CBEBB5FDC1392A0B07E0218D11CDE26A',helper=str(h),entry='pub0010Canonical6Context',marker='CANONICAL6_CONTEXT_COMPLETE.txt',assets=rows,pad_reuse_requires_separate_full_manufacturing_proof=True,files=[dict(path=str(x),sha256=sha(x)) for x in inputs]),indent=2),'utf-8');print(json.dumps(dict(helper_sha256=sha(h),manifest_sha256=sha(p)),indent=2))
if __name__=='__main__':main()
