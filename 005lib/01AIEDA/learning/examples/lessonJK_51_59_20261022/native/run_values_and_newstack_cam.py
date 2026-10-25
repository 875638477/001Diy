from pathlib import Path
import subprocess,sys,shutil,json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022');d=json.loads((R/'audits/j55_instance_correction_delta_b019.json').read_text(encoding='utf8'));refs=[x['ref'] for x in d['variants']['2L']['instances']]
for label,v,filename in [('J55_2L','2L','JK_2L_J55_text_height_review_NOT_RELEASED.brd'),('J55_4L','4L','JK_4L_J55_text_height_review_NOT_RELEASED.brd'),('newstack_4L','4L','JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd')]:
 tag='values_'+label+'_01';L=R/'logs'/('native_'+tag);D=R/'exports'/('devicevalues_'+label+'_TRAINING');D.mkdir(exist_ok=False)
 for ref in refs:(D/ref).mkdir()
 il='procedure(jkValues()\n let((f)\n f=outfile("'+(D/'component_values_source.tsv').as_posix()+'")\n fprintf(f "refdes\\tinstanceProperties\\tdefinitionProperties\\tdefinitionAttributes\\n")\n foreach(c axlDBGetDesign()->components\n fprintf(f "%L\\t%L\\t%L\\t%L\\n" c->name axlDBGetProperties(c) axlDBGetProperties(c->compdef) c->compdef->??)\n unless(axlWriteDeviceFile(c->compdef strcat("'+D.as_posix()+'/" c->name)) error("Native definition VALUE export failed\\n")))\n fprintf(f "JK_NATIVE_80_DEVICE_VALUES_COMPLETE\\n") close(f) t))\n'
 (R/'native'/('values_'+label+'.il')).write_text(il,encoding='ascii');scr=R/'native'/('values_'+label+'.scr');scr.write_text('set NOCONFIRM\nskill errset(load("'+(R/'native'/('values_'+label+'.il')).as_posix()+'") t)\nskill errset(jkValues() t)\nskill axlKillDesign()\nquit\n',encoding='ascii')
 subprocess.run([sys.executable,str(R/'native/run_native56_v9.py'),'--variant',v,'--action','skill','--tag',tag,'--board',str(R/'native'/v/filename),'--outdir',str(D),'--script',str(scr),'--readonly'],check=True)
 assert 'JK_NATIVE_80_DEVICE_VALUES_COMPLETE' in (D/'component_values_source.tsv').read_text()
 print('VALUE_EXPORT_COMPLETE',label,flush=True)
O=R/'exports/newstack_4L_TRAINING_NOT_FOR_FAB';S=R/'exports/J55_corrected_4L_TRAINING_NOT_FOR_FAB'
for name in ['art_param.txt','nc_param.txt']:(O/name).write_text((S/name).read_text().replace(S.as_posix()+'/J55_TRAINING_NOT_FOR_FAB_4L',O.as_posix()+'/NEWSTACK_TRAINING_NOT_FOR_FAB_4L'),encoding='ascii')
(O/'TRAINING_NOT_FOR_FAB.txt').write_text('ACTUAL_NEWSTACK L2=GND L3=V3V3 POWER. Seven GPIO remain unfinished, USB4/fullDRC pending. Not manufacturing release. Do not mix with legacyL3GND exports.\n',encoding='ascii')
for action in ['artwork','nctape','ncroute']:
 subprocess.run([sys.executable,str(R/'native/run_native56_v9.py'),'--variant','4L','--action',action,'--tag','newstack_4L_'+action+'_01','--board',str(R/'native/4L/JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd'),'--outdir',str(O)],check=True)
print('ALL_VALUES_AND_NEWSTACK_CAM_COMPLETE',flush=True)
