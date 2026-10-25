import pathlib,subprocess,sys
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonF_stack_artwork_correction_20261019')
for key,board in [('F28_2L','F28_2L_USERFIX.brd'),('F28_4L','F28_4L_USERFIX.brd'),('F29','F29_CONSTRAINTS_v4.brd')]:
 r=subprocess.run([sys.executable,str(R/'scripts/launch_fix.py'),'--board',str(R/'current'/board),'--script',str(R/f'scripts/outline_{key}.scr'),'--log',str(R/f'logs/outline_{key}'),'--readonly'],capture_output=True,text=True)
 print(key,r.returncode,r.stdout[-200:],r.stderr,flush=True)
 assert r.returncode==0
 assert 'FCOR_OUTLINE_COMPLETE' in (R/f'logs/outline_{key}/outline_exact.tsv').read_text()
print('THREE_OUTLINES_COMPLETE')
