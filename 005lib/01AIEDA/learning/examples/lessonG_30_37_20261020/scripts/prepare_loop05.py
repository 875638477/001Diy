from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
s=(R/'scripts/local_loops04.il').read_text().replace("axlNetClassGet(net 'physical)","axlNetClassGet(net 'physical t)")
(R/'scripts/local_loops05.il').write_text(s,encoding='ascii')
for key in ['4L','2L']:
 s=(R/f'scripts/loops_{key}_04.scr').read_text().replace('local_loops04.il','local_loops05.il').replace(f'loops_{key}_04',f'loops_{key}_05').replace(f'G_{key}_LOOPS_v4',f'G_{key}_LOOPS_v5')
 (R/f'scripts/loops_{key}_05.scr').write_text(s,encoding='ascii')
