"""Read-only backup of four frozen public BRDs; no CAD, edits, or deletion."""
from pathlib import Path
import hashlib,json,zipfile

M=Path(__file__).resolve().parent
ROOT=Path('D:/001DIY/005lib/01brdlib').resolve()
GUARD=M/'public_olb_final13_published13/PUBLIC_GUARD_AFTER_EXACT13_OLB.json'
OUT=M/'original_public_four_brd_backup13'
NAMES=('00012.brd','0010.brd','006.brd','008.brd')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()

def need(v,m):
    if not v:raise ValueError(m)

def main():
    need(not OUT.exists(),'Fresh output required')
    guard=json.loads(GUARD.read_text('utf-8-sig'))
    expected={str(Path(r['path']).resolve()).casefold():r for r in guard['files']}
    rows=[]
    for name in NAMES:
        p=ROOT/name
        need(p.resolve().parent==ROOT and not p.is_symlink(),'Path escapes exact public root')
        r=expected[str(p.resolve()).casefold()]
        need(sha(p)==r['sha256'] and p.stat().st_size==r['bytes'],'Frozen public source changed')
        rows.append({'path':str(p),'member':name,'sha256':r['sha256'],'bytes':r['bytes']})
    OUT.mkdir()
    zpath=OUT/'ORIGINAL_FOUR_PUBLIC_BRD.zip'
    with zipfile.ZipFile(zpath,'x',zipfile.ZIP_DEFLATED) as z:
        for r in rows:z.write(r['path'],r['member'])
        z.writestr('SHA256_MANIFEST.json',json.dumps(rows,indent=2))
    with zipfile.ZipFile(zpath) as z:
        need(set(z.namelist())==set(NAMES)|{'SHA256_MANIFEST.json'},'Unexpected ZIP members')
        need(json.loads(z.read('SHA256_MANIFEST.json'))==rows,'Frozen ZIP manifest differs')
        need(z.testzip() is None,'ZIP CRC failure')
        for r in rows:
            b=z.read(r['member'])
            need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest().upper()==r['sha256'],'ZIP member SHA mismatch')
            need(sha(r['path'])==r['sha256'],'Original changed during read-only backup')
    result={'status':'PASS_FOUR_ORIGINAL_PUBLIC_BRD_ZIP_FULL_SHA_ROUNDTRIP_NO_PUBLIC_MUTATION',
            'guard':str(GUARD),'guard_sha256':sha(GUARD),'archive':str(zpath),
            'archive_sha256':sha(zpath),'archive_bytes':zpath.stat().st_size,
            'members':rows,'public_files_modified':0,'public_files_removed':0,'script_sha256':sha(__file__)}
    (OUT/'BACKUP_RECEIPT.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='members'}))

if __name__=='__main__':main()
