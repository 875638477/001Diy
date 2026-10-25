"""Retain original BOM, encoding and even mixed original newline bytes."""
import hashlib,json
from pathlib import Path
B=Path(__file__).resolve().parent
p=B/'publish_plan.json';plan=json.loads(p.read_text(encoding='utf-8'))
for d in plan['docs']:
    before=Path(d['before']).read_bytes();after=Path(d['after']).read_bytes()
    encoding=d['encoding'];codec='utf-8' if encoding=='utf-8-sig' else encoding
    old=before.decode(encoding).replace('\r\n','\n');new=after.decode(encoding).replace('\r\n','\n')
    newline='\r\n' if b'\r\n' in before else '\n'
    if d['relative']!='study_records/README.md':
        title,tail=old.split('\n',1)
        assert new.startswith(title+'\n') and new.endswith(tail)
        delta=new[len(title)+1:len(new)-len(tail)]
        split=before.index(b'\n')+1
        updated=before[:split]+delta.replace('\n',newline).encode(codec)+before[split:]
    else:
        needle='| --- | --- |';row=new.split(needle+'\n',1)[1].split('\n',1)[0]
        assert new==old.replace(needle,needle+'\n'+row,1)
        updated=before.replace(needle.encode(codec),(needle+newline+row).encode(codec),1)
    assert updated.startswith(b'\xef\xbb\xbf')==before.startswith(b'\xef\xbb\xbf')
    assert updated.decode(encoding).replace('\r\n','\n')==new
    Path(d['after']).write_bytes(updated)
    d['after_sha256']=hashlib.sha256(updated).hexdigest()
p.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'documents':len(plan['docs']),'original_bom_and_newlines_preserved':True}))
