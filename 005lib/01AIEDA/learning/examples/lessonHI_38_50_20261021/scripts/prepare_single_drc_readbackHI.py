from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/normalize_HI_actual_v4.py';s=p.read_text().replace("role['lineThermal']=bool(role.get('thermal'))","role['lineThermal']=bool(role.get('lineThermal',role.get('thermal')))");p.write_text(s,encoding='ascii')
s=(R/'scripts/prepare_readbackHI_v6.py').read_text()
start=s.index("h+='skill errset(axlDRCUpdate")
end=s.index("\nif a.plan:",start)
block=s[start:end]
s=s[:start]+"captures=''\n"+block.replace("h+=","captures+=")+s[end:]
s=s.replace("h+='quit\\nfillin", "h+=captures\nh+='quit\\nfillin")
s=s.replace("  hiRegistry=nil\\n'","  hiRegistry=nil\\n  unwindProtect(progn(\\n   axlDBControl(\\'drcEnable nil)\\n'")
s=s.replace("hiHSEIsolationChallenge(", "hiHSEIsolationChallengeGraph(")
s=s.replace(" il+='  fprintf(f \"HI_REOPEN_ALL_ENDPOINTS_COMPLETE", " il+='  t) progn(axlDBControl(\\'drcEnable t) fprintf(f \"HI_READBACK_UNWIND_DRC_RESTORED=%L\\\\n\" axlDBControl(\\'drcEnable))))\\n'\n il+='  fprintf(f \"HI_REOPEN_ALL_ENDPOINTS_COMPLETE")
(R/'scripts/prepare_readbackHI_v7.py').write_text(s,encoding='ascii')
print('readback7: graph/negative checks first with guaranteed restore, one final full DRC then snapshot')
