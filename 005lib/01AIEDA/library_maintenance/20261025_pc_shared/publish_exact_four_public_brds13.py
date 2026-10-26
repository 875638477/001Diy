"""Publish four native-verified BRD candidates; preserve unrelated public bytes.

Root supplies a frozen plan only after its independent native checks pass.
Originals are in a SHA-verified ZIP. No CAD, deletion, or in-place file edits.
"""
from pathlib import Path
import argparse,copy,importlib.util,json,os,zipfile

M=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('exact_public_guard',M/'publish_exact_public_olbs.py')
G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
sha,need=G.sha,G.need
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
ROOT=Path('D:/001DIY/005lib/01brdlib').resolve()
NAMES={'00012.brd','0010.brd','006.brd','008.brd'}
GUARD_SHA='F9D19CC95DCEA9686967EF7CF954EE7E6858225E7F9C949A203C340E6A153D88'

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--plan',required=True,type=Path)
    ap.add_argument('--mode',choices=('dry-run','apply'),required=True)
    ap.add_argument('--out',required=True,type=Path)
    a=ap.parse_args();need(not a.out.exists(),'Fresh receipt directory required')
    need(a.out.resolve().is_relative_to(M.resolve()),'Receipts outside maintenance root')
    p=jr(a.plan);need(p['schema']=='EXACT_FOUR_PUBLIC_BRD_NATIVE_PUBLISH_PLAN_V1','Wrong plan schema')
    need(p['publisher_sha256']==sha(__file__),'Publisher changed after plan freeze')
    need(sha(p['guard'])==GUARD_SHA,'Only frozen post13OLB public guard accepted')
    guard=jr(p['guard']);G.verify_guard(guard)
    rows=p['replacements'];need(len(rows)==4 and {Path(r['public']).name for r in rows}==NAMES,'Four exact public BRDs required')
    expected={G.key(r['path']):r for r in guard['files']}
    need(sha(p['backup_receipt'])==p['backup_receipt_sha256'],'Backup receipt changed after plan freeze')
    backup=jr(p['backup_receipt'])
    need(backup['status']=='PASS_FOUR_ORIGINAL_PUBLIC_BRD_ZIP_FULL_SHA_ROUNDTRIP_NO_PUBLIC_MUTATION','Original BRD backup not verified')
    need(sha(backup['archive'])==backup['archive_sha256'],'Original BRD ZIP changed')
    with zipfile.ZipFile(backup['archive']) as z:
        need(set(z.namelist())==NAMES|{'SHA256_MANIFEST.json'},'Unexpected backup members')
        need(json.loads(z.read('SHA256_MANIFEST.json'))==backup['members'],'Backup manifest changed')
        for r in backup['members']:
            b=z.read(r['member'])
            import hashlib
            need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest().upper()==r['sha256'],'Backup roundtrip mismatch')
            need(expected[G.key(r['path'])]['sha256']==r['sha256'],'Backup is not the frozen public original')
    for r in rows:
        q,c=Path(r['public']),Path(r['candidate'])
        need(q.resolve().parent==ROOT and not q.is_symlink(),'Public destination escapes exact BRD root')
        need(c.resolve().is_relative_to(M.resolve()) and not c.is_symlink(),'Candidate outside isolated maintenance root')
        old=expected[G.key(q)]
        need(old['sha256']==r['old_sha256']==sha(q),'Frozen public original changed')
        need(c.stat().st_size==r['new_bytes'] and sha(c)==r['new_sha256'],'Candidate changed')
        need(r['native_proofs'],'Independent native proof required for every board')
        for e in r['native_proofs']:
            need(sha(e['path'])==e['sha256'],'Native proof changed')
            v=jr(e['path']);need(v['status']==e['required_status'] and v['status'].startswith('PASS'),'Native proof not exact PASS')
    a.out.mkdir(parents=True)
    base={'plan':str(a.plan),'plan_sha256':sha(a.plan),'publisher_sha256':sha(__file__),
          'mode':a.mode,'original_backup_receipt':p['backup_receipt'],'public_files_replaced':0,'CAD_started':False}
    if a.mode=='dry-run':
        G.write_json(a.out/'DRY_RUN.json',dict(base,status='PASS_FOUR_PUBLIC_BRD_BACKUP_NATIVE_PROOFS_FULL_GUARD_READONLY'));return
    after=copy.deepcopy(guard);records={G.key(r['path']):r for r in after['files']}
    with (a.out/'ATOMIC_BRD_REPLACEMENTS.jsonl').open('x',encoding='utf-8') as journal:
        for r in rows:
            q,c=Path(r['public']),Path(r['candidate'])
            tmp=q.with_name(q.name+'.publish13_'+base['plan_sha256'][:12]+'.tmp')
            need(not tmp.exists() and sha(q)==r['old_sha256'],'Public BRD changed just before replacement')
            with c.open('rb') as src,tmp.open('xb') as dst:
                while chunk:=src.read(1048576):dst.write(chunk)
                dst.flush();os.fsync(dst.fileno())
            need(sha(tmp)==r['new_sha256'] and sha(q)==r['old_sha256'],'Independent copy verification failed')
            os.replace(tmp,q);need(sha(q)==r['new_sha256'],'Published BRD readback failed')
            records[G.key(q)].update(sha256=r['new_sha256'],bytes=r['new_bytes'])
            journal.write(json.dumps(r)+'\n');journal.flush();os.fsync(journal.fileno())
    G.verify_guard(after)
    after.update(status='EXPECTED_PUBLIC_BYTES_BY_EXPLICIT_FOUR_BRD_REPLACEMENT',
                 source_guard={'path':p['guard'],'sha256':GUARD_SHA},explicit_replacements=rows)
    G.write_json(a.out/'PUBLIC_GUARD_AFTER_EXACT4_BRD.json',after)
    G.write_json(a.out/'PUBLISH_RECEIPT.json',dict(base,status='PASS_FOUR_PUBLIC_BRD_ATOMIC_REPLACEMENTS_OTHER_PUBLIC_FILES_UNCHANGED',
                 public_files_replaced=4,new_guard=str(a.out/'PUBLIC_GUARD_AFTER_EXACT4_BRD.json'),
                 new_guard_sha256=sha(a.out/'PUBLIC_GUARD_AFTER_EXACT4_BRD.json')))

if __name__=='__main__':main()
