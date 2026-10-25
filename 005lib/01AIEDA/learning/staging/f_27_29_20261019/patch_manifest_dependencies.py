from pathlib import Path
p=Path(r'D:\001DIY\005lib\01AIEDA\learning\staging\f_27_29_20261019\finalize_records.py')
s=p.read_text(encoding='utf-8')
a=s.index(' entries=list(m) if isinstance(m,list)')
b=s.index(' manifests.append(',a)
block=""" def hash_entries(node):
  if isinstance(node,dict):
   if 'path' in node and ('sha256' in node or 'SHA256' in node):yield node
   for value in node.values():yield from hash_entries(value)
  elif isinstance(node,list):
   for value in node:yield from hash_entries(value)
 entries=list(hash_entries(m));assert entries,(p,'empty artifact hash manifest')
 unique=set()
 for e in entries:
  q=pathlib.Path(e['path']);q=q if q.is_absolute() else p.parent/q
  q=inside(q);assert q.is_file(),q
  expected=e.get('sha256',e.get('SHA256'));assert expected and sha(q)==expected.upper(),(q,'artifact hash mismatch')
  unique.add(q)
"""
s=s[:a]+block+s[b:]
s=s.replace("'filesVerified':len(entries)","'hashEntriesVerified':len(entries),'uniqueFilesVerified':len(unique)")
p.write_text(s,encoding='utf-8')
print('Added recursive manifest identity verification')