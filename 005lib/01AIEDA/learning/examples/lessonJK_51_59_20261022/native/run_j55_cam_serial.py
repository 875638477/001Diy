import pathlib,subprocess,sys
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022')
for v in ['2L','4L']:
 for act in ['artwork','nctape','ncroute']:
  subprocess.run([sys.executable,str(R/'native/run_native56_v7.py'),'--variant',v,'--action',act,'--tag',f'J55_corrected_{v}_{act}_01','--board',str(R/'native'/v/f'JK_{v}_J55_text_height_review_NOT_RELEASED.brd'),'--outdir',str(R/'exports'/f'J55_corrected_{v}_TRAINING_NOT_FOR_FAB')],check=True)
