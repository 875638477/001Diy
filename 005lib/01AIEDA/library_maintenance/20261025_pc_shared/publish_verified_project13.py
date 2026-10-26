"""Publish exactly DSN/BRD/three PST files after frozen native proof review.

No CAD, no library deletion, no change to original11/12 or02pcb. Exact old
 existing files are archived and SHA round-tripped before independent atomic copies.
"""
from pathlib import Path
import argparse,hashlib,json,os,zipfile
R=Path('D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025').resolve()
M=Path(__file__).resolve().parent
ALLOWED={R/'sch/LGA1700.DSN',R/'pcb/LGA1700_RULES.brd'}|{R/'sch/netlist'/n for n in ('pstchip.dat','pstxprt.dat','pstxnet.dat')}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
current=lambda p:sha(p) if Path(p).is_file() else None

def need(v,m):
    if not v:raise ValueError(m)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--plan',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--mode',choices=('dry-run','apply'),required=True);a=ap.parse_args()
    p=jr(a.plan);need(p['schema']=='FINAL13_EXACT_FIVE_DESIGN_FILES_NATIVE_PUBLISH_PLAN_V1','Wrong frozen plan')
    need(sha(__file__)==p['publisher_sha256'],'Publisher changed')
    rows=p['files'];need(len(rows)==5 and {Path(r['target']).resolve() for r in rows}==ALLOWED,'Only exact five formal13 files accepted')
    for e in p['native_proofs']:
        need(sha(e['path'])==e['sha256'],'Native evidence changed')
        q=jr(e['path']);need(q['status']==e['required_status'] and q['status'].startswith('PASS'),'Native proof not exact PASS')
    need(p['native_proofs'],'Native proofs absent')
    for e in p['protected_originals']:need(sha(e['path'])==e['sha256'],'Protected original changed')
    for r in rows:
        s,t=Path(r['source']),Path(r['target'])
        need(s.resolve().is_relative_to(R/'w') and not s.is_symlink() and not t.is_symlink(),'Unexpected source or target path')
        need(sha(s)==r['new_sha256'] and current(t)==r['old_sha256'],'Formal/source file changed')
        need(r['old_sha256'] is not None or t.parent==R/'sch/netlist','Only three new PST targets may initially be absent')
    need(not a.out.exists() and a.out.resolve().is_relative_to(R/'verification'),'Fresh in-project verification folder required')
    a.out.mkdir(parents=True)
    base={'plan':str(a.plan),'plan_sha256':sha(a.plan),'mode':a.mode,'files_replaced':0,'CAD_started':False}
    if a.mode=='dry-run':
        (a.out/'DRY_RUN.json').write_text(json.dumps(dict(base,status='PASS_EXACT_FIVE_FILES_NATIVE_PROOFS_READONLY'),indent=2));return
    zpath=a.out/'FORMAL13_BEFORE_FINAL_PUBLISH.zip'
    with zipfile.ZipFile(zpath,'x',zipfile.ZIP_DEFLATED) as z:
        for r in rows:
            if r['old_sha256'] is not None:z.write(r['target'],str(Path(r['target']).relative_to(R)).replace('\\','/'))
    with zipfile.ZipFile(zpath) as z:
        need(len(z.namelist())==sum(r['old_sha256'] is not None for r in rows) and z.testzip() is None,'Original ZIP members/CRC failed')
        for r in rows:
            if r['old_sha256'] is None:continue
            b=z.read(str(Path(r['target']).relative_to(R)).replace('\\','/'))
            need(hashlib.sha256(b).hexdigest().upper()==r['old_sha256'],'Original ZIP roundtrip failed')
    with (a.out/'ATOMIC_FILES.jsonl').open('x',encoding='utf-8') as journal:
        for r in rows:
            s,t=Path(r['source']),Path(r['target']);tmp=t.with_name(t.name+'.publish13.tmp')
            need(not tmp.exists() and current(t)==r['old_sha256'],'Target changed just before publication')
            t.parent.mkdir(parents=True,exist_ok=True)
            with s.open('rb') as src,tmp.open('xb') as dst:
                while b:=src.read(1048576):dst.write(b)
                dst.flush();os.fsync(dst.fileno())
            need(sha(tmp)==r['new_sha256'] and current(t)==r['old_sha256'],'Staged copy/old target mismatch')
            os.replace(tmp,t);need(sha(t)==r['new_sha256'],'Published readback failed')
            journal.write(json.dumps(r)+'\n');journal.flush();os.fsync(journal.fileno())
    for e in p['protected_originals']:need(sha(e['path'])==e['sha256'],'Original changed during publication')
    for r in rows:need(sha(r['target'])==r['new_sha256'] and sha(r['source'])==r['new_sha256'],'Final5 source/formal binding failed')
    result=dict(base,status='PASS_FIVE_FORMAL13_DESIGN_FILES_NATIVE_VERIFIED_ATOMIC_COPY',files_replaced=5,
                backup=str(zpath),backup_sha256=sha(zpath),original_files_backed_up=sum(r['old_sha256'] is not None for r in rows),new_files_created=sum(r['old_sha256'] is None for r in rows),files=rows,protected_originals_unchanged=True)
    (a.out/'PUBLICATION_RECEIPT.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))

if __name__=='__main__':main()
