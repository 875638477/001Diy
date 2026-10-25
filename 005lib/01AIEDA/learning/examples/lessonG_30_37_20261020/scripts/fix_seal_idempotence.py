from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
p=R/'scripts/seal_nativeG.py'
s=p.read_text();a=s.index("p=R/'NATIVE_WORKFLOW.md'");b=s.index('# Seal only',a)
s=s[:a]+"""p=R/'NATIVE_WORKFLOW.md'
if p.exists():
 text=p.read_text();text=text.replace('(current/','(../current/').replace('(review/','(../review/')
 (R/'native/README.md').write_text(text,encoding='utf8');p.unlink()
else: assert (R/'native/README.md').is_file()
"""+s[b:]
p.write_text(s,encoding='ascii')
