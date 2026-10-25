"""Record the delivered native artifacts without altering CAD files."""
from pathlib import Path
import hashlib, json, re
root=Path(__file__).resolve().parents[1]
final=root/'examples/lesson14_capture/final'
files=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(final.rglob('*')) if p.is_file()]
locks=[str(p) for p in final.rglob('*') if p.is_file() and p.name.lower().endswith('lck')]
note=root/'notes/lesson14_library_propagation_20261019.md'
broken=[]
for target in re.findall(r'\]\(([^)]+)\)',note.read_text(encoding='utf-8')):
    if '://' not in target and not (note.parent/target).resolve().exists():broken.append(target)
value={'date':'2026-10-19 Asia/Shanghai','files':files,'final_lock_files':locks,'broken_record_links':broken,'native_validation':'logs/lesson14_capture_20261019/validation.json','completion_record':str(note.relative_to(root))}
dest=root/'logs/lesson14_capture_20261019/artifact_manifest.json'
dest.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'files':len(files),'final_lock_files':locks,'broken_record_links':broken},ensure_ascii=False))
if locks or broken:raise SystemExit(1)
