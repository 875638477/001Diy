from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/batchHI_shapes_v3.il';s=p.read_text()
start=s.index('procedure(hiHSEIsolationChallenge(');end=s.index('\nprocedure(hiAssignNetClass',start)
g=s[start:end].replace('procedure(hiHSEIsolationChallenge(','procedure(hiHSEIsolationChallengeGraph(')
g=g.replace('  axlDRCUpdate(t) axlDBRefreshId(nil)\n','')
g=g.replace('  axlDRCUpdate(t) f29DumpDRC(f "HSE_ANCHOR_RESTORED")\n','')
g=g.replace('  unless(length(axlDBGetDesign()->drcs)==beforeCount error("Restored HSE DRC count differs\\n"))\n','')
g=g.replace('HSE_ISOLATION_NEGATIVE_TEST_COMPLETE_NO_SAVE','HSE_ISOLATION_GRAPH_NEGATIVE_TEST_COMPLETE_FULL_DRC_REQUIRED')
p.write_text(s+'\n'+g,encoding='ascii')
p=R/'scripts/compile_batchHI_v8.py';s=p.read_text()
s=s.replace('hiHSEIsolationChallenge(', 'hiHSEIsolationChallengeGraph(')
begin=s.index("code='procedure(hiBatchProgram()")
end=s.index("\nil.write_text",begin)
s=s[:begin]+"""code='procedure(hiBatchProgram()\\n let((f)\\n  f=outfile('+q((out/'hi_batch_execution.txt').as_posix())+')\\n  fprintf(f \"HI_BATCH_DRC_BEFORE=%L\\\\n\" axlDBControl(\\'drcEnable))\\n  unwindProtect(\\n   progn(\\n    axlDBControl(\\'drcEnable nil)\\n    fprintf(f \"HI_ASSEMBLY_ONLINE_DRC_TEMPORARILY_DISABLED=%L\\\\n\" axlDBControl(\\'drcEnable))\\n    '+ '\\n    '.join(statements)+'\\n    t)\\n   progn(\\n    axlDBControl(\\'drcEnable t)\\n    fprintf(f \"HI_UNWIND_DRC_RESTORED=%L\\\\n\" axlDBControl(\\'drcEnable))))\\n  unless(axlDBControl(\\'drcEnable) error(\"Final DRC must be enabled\\\\n\"))\\n  hiFinalize(f '+q(out.as_posix())+' '+q(board.as_posix())+' '+q((R/'library').as_posix())+' '+proofstr+')\\n  t))\\n'
"""+s[end:]
(R/'scripts/compile_batchHI_v9.py').write_text(s,encoding='ascii')
print('compiler9 bulk assembly has guaranteed DRC restore; graph-only HSE negative check before mandatory final full DRC')
