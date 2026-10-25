from pathlib import Path
import shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
p=R/'scripts/finalize29.py';s=p.read_text()
shutil.copy2(p,R/'scripts/finalize29_v1_preview.py')
s=s.replace("v['physical'],'spacing_cset':v['spacing']","v.get('physical',v.get('physical_cset')),'spacing_cset':v.get('spacing',v.get('spacing_cset'))")
s=s.replace("""svg.append(f'<text x="{x}" y="{y}" class="{cl}"'+(f' fill="{fill}"' if fill else '')+'>'+html.escape(t)+'</text>')""","""size={'h':30,'s':17,'c':19}[cl]
 svg.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}"'+(' font-weight="bold"' if cl in ['h','c'] else '')+(f' fill="{fill}"' if fill else ' fill="#1c2b3d"')+'>'+html.escape(t)+'</text>')""")
p.write_text(s,encoding='ascii')
