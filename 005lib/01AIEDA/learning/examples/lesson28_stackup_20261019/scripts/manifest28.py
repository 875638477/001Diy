from pathlib import Path
import json,hashlib
B=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019')
N=Path(r'D:\001DIY\005lib\01AIEDA\learning\notes\lesson28_stackup_20261019.md')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
readme="""# Lesson 28: native two- and four-layer stackups

Full Chinese lesson: [complete note](../../notes/lesson28_stackup_20261019.md).

- Native boards: native/F28_2L.brd and native/F28_4L.brd.
- Actual specifications and public source hashes: specification.json.
- 402 independent checks: validation.json.
- Final primary readback: logs/reopen2_02 and logs/reopen4_02.
- Placed pins / holes / slots: logs/morebase01, logs/more2_01, logs/more4_01.
- Actual recognized design outline / keepin / keepout: logs/mechbase01, logs/mech2_01, logs/mech4_01.
- Copper film template input and immutable hashes: film_template_readonly.json.
- Final explicit film parameter files: native/copper_films_2_exact.il and 4_exact.il.
- Diagram from native readback: preview.svg / preview.png. Thin layers have a minimum display height.

Scope: native CAD stackup editing, native geometry and layer mapping, current DRC, independent new-process reopen.
The 1.6mm nominal order thickness and modeled thickness sums have separate meanings.
This directory is an isolated teaching example. Manufacturing release remains false:
2L inherited USB mask web is below the selected OSH minimum; connector stake length vs 1.6mm board/process is unresolved;
4L USB 90-ohm width/spacing is not qualified; reference plane pours and remaining component placement are future work.
The 0.30mm-hole / 0.60mm-pad GND via at (52,35) is a layer-mapping teaching instance.

Historical partial film settings and helper failures are retained in logs/scripts; final canonical lesson28.il loads exact film settings.
No shared library, 01env template, shortcut, global HOME, or original engineering board was edited.
All process TMP/TEMP/PCBENV/cwd and all newly created material are within 01AIEDA.
"""
(B/'README.md').write_text(readme,encoding='utf-8')
files=[]
for p in sorted(B.rglob('*')):
 if p.is_file() and p.name!='artifact_manifest.json':
  files.append({'path':p.relative_to(B).as_posix(),'bytes':p.stat().st_size,'SHA256':sha(p)})
out={'date':'2026-10-19 Asia/Shanghai','lesson':'28','scope':'All files inside this isolated lesson directory, excluding this manifest itself','formalNote':{'path':str(N),'bytes':N.stat().st_size,'SHA256':sha(N)},'filesCount':len(files),'files':files}
(B/'artifact_manifest.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('Manifest',len(files),'files; note SHA',sha(N))
for name in ['F28_2L.brd','F28_4L.brd']:print(name,sha(B/'native'/name))
print('STATUS',json.loads((B/'validation.json').read_text())['status'])
