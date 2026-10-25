from pathlib import Path
import subprocess,sys
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022')
for v in ('2L','4L'):
 for action in ('nctape','ncroute'):
  args=[sys.executable,str(R/'native/run_native56_v6.py'),'--variant',v,'--action',action,'--tag',action+'_'+v+'_baseline_try01']
  print('SERIAL_NATIVE_STEP',v,action,flush=True);subprocess.run(args,check=True)
