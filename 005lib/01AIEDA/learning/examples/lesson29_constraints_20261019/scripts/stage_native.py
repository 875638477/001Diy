import pathlib,shutil,json,hashlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
for n in ['prepare_native29.py','build29.il']:
 p=R/'scripts'/n;s=p.read_text();s=s.replace("axlDBFindByName('diffpair n)","axlDiffPairDBID(n)");p.write_text(s,encoding='ascii')
src=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019\native\F28_4L.brd')
sha=hashlib.sha256(src.read_bytes()).hexdigest().upper()
assert sha=='F004184D46B86A7CF56FFA05C33418A6BEEFA508A3043A3442540B69AFA558D6'
dst=R/'native/F29_CONSTRAINTS.brd';assert not dst.exists();shutil.copy2(src,dst)
(R/'input_identity.json').write_text(json.dumps({'source':str(src),'sourceSHA256':sha,'workingCopy':str(dst),'date':'2026-10-19'},indent=2),encoding='utf8')
scr='set NOCONFIRM\nskill errset(load("'+(R/'scripts/build29.il').as_posix()+'") t)\nskill errset(f29Build("'+dst.as_posix()+'" "'+(R/'logs').as_posix()+'") t)\nquit\nfillin "yes"\n'
(R/'scripts/build01.scr').write_text(scr,encoding='ascii')
print(dst)
