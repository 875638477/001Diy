from pathlib import Path
p=Path(r'D:\001DIY\005lib\01AIEDA\learning\staging\f_27_29_20261019\finalize_records.py')
s=p.read_text()
s=s.replace("entries=m if isinstance(m,list) else m.get('files',[])","entries=list(m) if isinstance(m,list) else list(m.get('files',[]))\n if isinstance(m,dict):\n  for k in ['formalNote','note']:\n   if isinstance(m.get(k),dict) and 'path' in m[k]:entries.append(m[k])")
s=s.replace("assert sha(q)==e['sha256'].upper(),(q,'artifact hash mismatch')","expected=e.get('sha256',e.get('SHA256'));assert expected and sha(q)==expected.upper(),(q,'artifact hash mismatch')")
p.write_text(s,encoding='utf-8')
print('Manifest schemas supported')
