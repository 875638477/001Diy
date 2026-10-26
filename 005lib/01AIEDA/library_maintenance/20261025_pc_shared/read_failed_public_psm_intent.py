"""Prepared read-only extracta intent probe for a failed compiled public variant. Only root runs it."""
from pathlib import Path
import argparse,json,hashlib,importlib.util
M=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--base-helper',type=Path,required=True);a=ap.parse_args();assert not a.output.exists();a.output.mkdir(parents=True)
 spec=importlib.util.spec_from_file_location('failed_intent_readbase',a.base_helper);b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
 source=[a.source,a.source.with_suffix('.dra')];protected={str(p):sha(p) for p in source if p.is_file()};reports=[]
 for p in source:
  if not p.is_file():continue
  for kind,view in [('pins',M/'failed_intent_symbol_pins_view.txt'),('geometry',M/'failed_intent_full_geometry_view.txt')]:
   r=a.output/(p.suffix.lstrip('.')+'_'+kind);r.mkdir();env=b.envfor(r);out=r/'extract.txt';rec=b.launch([b.CAD/'tools/bin/extracta.exe','-w','-l',r/'extract.log',p,view,out],r,env,60,'extracta');rec.update(source=str(p),source_sha256=protected[str(p)],view=str(view),view_sha256=sha(view),extract=str(out),extract_sha256=sha(out) if out.exists() else None);reports.append(rec)
 assert all(sha(p)==h for p,h in protected.items())
 (a.output/'PROBE_REPORT.json').write_text(json.dumps({'status':'READONLY_EXTRACTA_INTENT_PROBE_REQUIRES_FIELD_REVIEW','sources_unchanged':True,'protected':protected,'launches':reports},ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'source':str(a.source),'sources_unchanged':True,'reports':reports},ensure_ascii=False))
if __name__=='__main__':main()
