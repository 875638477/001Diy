"""Publish the explicitly inventoried archive and four small navigation edits."""
import csv,hashlib,json,os,shutil,time,zipfile
from pathlib import Path,PurePosixPath

B=Path(__file__).resolve().parent
AI=Path(r'D:\001DIY\005lib\01AIEDA')
DEST=AI/'library_maintenance/20261025_pad_psm_merge'
ALLOWED_DOCS={str(AI/p).casefold() for p in ('EDA.md','AI接管cadence.md','study_records/README.md','learning/notes/record_location_rules.md')}

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def main():
    plan=json.loads((B/'publish_plan.json').read_text(encoding='utf-8'))
    files=json.loads((B/'archive_manifest.json').read_text(encoding='utf-8'))
    assert str(DEST)==plan['destination'] and not DEST.exists()
    assert len(files)==plan['file_count'] and sha(B/'archive_manifest.json')==plan['manifest_sha256']
    index=DEST.parent/'INDEX.txt'
    assert not index.exists(),'Existing library-maintenance index requires reconciliation'
    for d in plan['docs']:
        assert d['target'].casefold() in ALLOWED_DOCS
        assert sha(d['target'])==d['before_sha256'] and sha(d['after'])==d['after_sha256']
    for r in files:
        entry=PurePosixPath(r['archive_path'])
        assert not entry.is_absolute() and '..' not in entry.parts
        assert Path(r['source']).is_file() and Path(r['source']).stat().st_size==r['bytes']
    DEST.mkdir(parents=True)
    (DEST/'STATUS.txt').write_text('ARCHIVE_BUILD_IN_PROGRESS\n',encoding='ascii')
    archive=DEST/'cadence_library_maintenance_20261025_full.zip'
    start=time.monotonic()
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        for i,r in enumerate(files,1):
            # Hash the exact payload being archived; a changed source stops publication.
            content=Path(r['source']).read_bytes()
            assert len(content)==r['bytes'] and hashlib.sha256(content).hexdigest()==r['sha256'],r['source']
            info=zipfile.ZipInfo.from_file(r['source'],arcname=r['archive_path'],strict_timestamps=False)
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,content,compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
            if i%3000==0:print(json.dumps(dict(stage='ARCHIVING',files=i,total=len(files),seconds=round(time.monotonic()-start))),flush=True)
        z.write(B/'archive_manifest.json','archive_manifest.json')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();assert len(names)==len(files)+1 and len(names)==len(set(names))
        for i,r in enumerate(files,1):
            info=z.getinfo(r['archive_path'])
            assert info.file_size==r['bytes']
            with z.open(info) as f:
                h=hashlib.sha256()
                for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
            assert h.hexdigest()==r['sha256'],r['archive_path']
            if i%5000==0:print(json.dumps(dict(stage='VERIFYING_ARCHIVE',verified=i,total=len(files))),flush=True)
        assert hashlib.sha256(z.read('archive_manifest.json')).hexdigest()==plan['manifest_sha256']
    # Publish readable summaries and exact original/prepared document snapshots.
    shutil.copytree(B/'readable',DEST/'readable')
    for name in ('README.txt','archive_manifest.csv','archive_manifest.json','publish_plan.json','prepare_archive.py','publish_archive.py','refresh_prepared_docs.py'):
        shutil.copyfile(B/name,DEST/name)
    shutil.copytree(B/'docs_before',DEST/'metadata_before')
    shutil.copytree(B/'docs_after',DEST/'metadata_after')
    verification=dict(status='PASS',original_files_verified=len(files),original_bytes=sum(r['bytes'] for r in files),
        archive=str(archive),archive_bytes=archive.stat().st_size,archive_sha256=sha(archive),
        manifest_sha256=plan['manifest_sha256'],validation='Every archived member read back with byte count, CRC and SHA256',
        sources_preserved=True,source_roots=plan['sources'])
    (DEST/'archive_verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2),encoding='utf-8')
    applied=[]
    try:
        for d in plan['docs']:
            # Recheck immediately before replacement; never overwrite concurrent user edits.
            assert sha(d['target'])==d['before_sha256']
            target=Path(d['target']);pending=target.with_name(target.name+'.library_records_pending')
            assert not pending.exists()
            shutil.copyfile(d['after'],pending);assert sha(pending)==d['after_sha256']
            os.replace(pending,target);applied.append(d)
            assert sha(target)==d['after_sha256']
        shutil.copyfile(B/'INDEX.txt',index)
    except Exception:
        for d in applied:
            if sha(d['target'])==d['after_sha256']:shutil.copyfile(d['before'],d['target'])
        raise
    for source in (B/'readable').iterdir():assert sha(source)==sha(DEST/'readable'/source.name)
    for d in plan['docs']:assert sha(d['target'])==d['after_sha256']
    result=dict(status='PASS',destination=str(DEST),archived_files=len(files),
        original_bytes=verification['original_bytes'],archive_bytes=verification['archive_bytes'],
        archive_sha256=verification['archive_sha256'],updated_documents=[d['target'] for d in plan['docs']],
        seconds=round(time.monotonic()-start,1))
    (DEST/'publication_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (B/'publication_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    (DEST/'STATUS.txt').write_text('PASS_ARCHIVE_AND_INDEXES_VERIFIED\n',encoding='ascii')
    print(json.dumps(result,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
