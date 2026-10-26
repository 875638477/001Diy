"""Canary must initialize exact same public paths as normal pc13Replace. No CAD."""
from pathlib import Path
import hashlib,json,shutil
M=Path(__file__).parent;OLD=M/'public0010_native403_bundle13_v3';OUT=M/'public0010_native403_bundle13_v4'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def need(v,m):
 if not v:raise ValueError(m)
def main():
 need(not OUT.exists(),'Freshv4 bundle required');shutil.copytree(OLD,OUT);h=OUT/'public0010_native403_v1.il';t=h.read_text('utf-8');token='pc13LoadExpected(strcat(pub403Bundle "/TARGET_LOGICAL572_EXPECTED_PINS.ilist"))';need(t.count(token)==1,'Unique canary expected-pin initialization required')
 insert='unless(axlSetVariable("psmpath" "D:/001DIY/005lib/01Psm_lib") error("PUB403 canary public PSMPATH failed\\n"))\n  unless(axlSetVariable("padpath" "D:/001DIY/005lib/01Pad_lib") error("PUB403 canary public PADPATH failed\\n"))\n  '
 h.write_text(t.replace(token,insert+token),encoding='utf-8');runner=M/'run_public0010_native403_owned_v4.py';need(not runner.exists(),'Freshv4 runner required');shutil.copyfile(M/'run_public0010_native403_owned_v3.py',runner)
 manifest=json.loads((OLD/'BUNDLE_MANIFEST.json').read_text('utf-8'));manifest.update(state='PREPARED_V4_C90_EXPLICIT_PUBLIC_PATHS_BEFORE_ALT_SAME_MIRROR_RESTORE_AS_V3',parent_bundle_manifest={'path':str(OLD/'BUNDLE_MANIFEST.json'),'sha256':sha(OLD/'BUNDLE_MANIFEST.json')});manifest['bundle_files']=[{'path':str(p),'sha256':sha(p)} for p in OUT.iterdir() if p.is_file() and p.name!='BUNDLE_MANIFEST.json'];manifest['external_proofs']+=[{'path':str(runner),'sha256':sha(runner)}];(OUT/'BUNDLE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'bundle':str(OUT),'manifest_sha256':sha(OUT/'BUNDLE_MANIFEST.json'),'runner':str(runner),'runner_sha256':sha(runner),'helper_sha256':sha(h)},indent=2))
if __name__=='__main__':main()
