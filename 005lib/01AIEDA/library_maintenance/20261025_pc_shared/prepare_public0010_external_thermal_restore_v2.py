"""V2: use the proven string-keyed complete native graph/figure exporter."""
from pathlib import Path
import hashlib,json
M=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def main():
 old=M/'public0010_external_thermal_restore_bundle13_v1';b=M/'public0010_external_thermal_restore_bundle13_v2';assert not b.exists();b.mkdir()
 proven=Path('D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025/dra_audit/export.il')
 text=(old/'public0010_external_thermal_restore_v1.il').read_text('utf-8')
 start=text.index('procedure(pc25CacheVisit(o)');end=text.index('procedure(pc25CreateExternal(rows f)')
 replacement='''; Proven full-cache exporter uses sprintf DBID keys including user-type pad:.
; Preserve all native attributes, complete figures, global textblocks and props.
load("D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025/dra_audit/export.il")
procedure(pc25CacheSnapshot(path)
 let((f rows count seen line)
  seen=makeTable('pc25CacheExportSeen nil) count=0 f=outfile(path)
  foreach(d axlDBGetDesign()->symdefs draAuditVisit(d f seen) count=count+1)
  unless(count>0 error("External thermal complete cached definitions missing\\n"))
  close(f) f=infile(path) rows=nil
  while(gets(line f) rows=cons(line rows)) close(f) sort(rows 'alphalessp)))
'''
 text=text[:start]+replacement+text[end:]
 h=b/'public0010_external_thermal_restore_v2.il';h.write_text(text,'utf-8')
 man=json.loads((old/'MANIFEST.json').read_text())
 man.update(schema='PUBLIC0010_SOURCE_ONLY_EXTERNAL_THERMAL_CU_RESTORE_V2',helper=str(h),complete_cache_snapshot_method='Proven draAuditVisit full native graph including figures/textblocks/properties; stable sprintf keys for pad user objects; no weakened geometry fields')
 man['files'] += [dict(path=str(p),sha256=sha(p)) for p in [h,proven,Path(__file__),old/'MANIFEST.json']]
 (b/'MANIFEST.json').write_text(json.dumps(man,indent=2)+'\n','utf-8')
 runner=M/'run_public0010_external_thermal_restore_v2.py';runner.write_text((M/'run_public0010_external_thermal_restore_v1.py').read_text().replace('PUBLIC0010_SOURCE_ONLY_EXTERNAL_THERMAL_CU_RESTORE_V1',man['schema']),'utf-8')
 print(json.dumps(dict(bundle=str(b),manifest_sha256=sha(b/'MANIFEST.json'),helper_sha256=sha(h),runner=str(runner),runner_sha256=sha(runner)),indent=2))
if __name__=='__main__':main()
