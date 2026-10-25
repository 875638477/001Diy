from pathlib import Path
r=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonF_stack_artwork_correction_20261019\review')
p=r/'independent_review.py';s=p.read_text(encoding='utf-8')
s=s.replace("comps=table(after/'components.tsv');pins=table(after/'component_pins.tsv')","eq(key+' full native constraint class/pair props and all DRC modes preserved',norm(text(after/'constraint_summary.txt')),norm(text(before/'constraint_summary.txt')))\n comps=table(after/'components.tsv');pins=table(after/'component_pins.tsv')")
s=s.replace("# Scope corrections are part", """ex=json.loads(text(C/'exports'/'export_result.json'))
eq('Final v4 TCF export SHA',sha(C/'exports'/'F29_RULES_v4.tcf'),ex['outputSHA256'])
for rec in ex['records']:
 check('Official v4 technology '+rec['step']+' exits0',rec['exitCode']==0)
 eq('Official v4 technology '+rec['step']+' input actual board',rec['boardBefore'],sha(C/'current'/'F29_CONSTRAINTS_v4.brd'))
 eq('Official v4 technology '+rec['step']+' no native mutation',rec['boardAfter'],rec['boardBefore'])
clog=text(C/'exports'/'techfile_run'/'compare_stdout.txt')+text(C/'exports'/'techfile_run'/'compare_techfile.log')
check('Official v4 technology comparison no objects updated','No objects were updated' in clog)
primary=json.loads(text(C/'validation.json'))
check('Primary native validator independently agrees',primary['status']=='PASS_NATIVE_USER_LAYER_ARTWORK_CORRECTION')
for name in ['axlFilmCreate','axlXSectionDelete','axlDBChangeDesignUnits','axlLayerCreateNonConductor','axlGetXSection']:
 sha(Path(r'C:\\Program0\\Cadence\\SPB172\\share\\pcb\\examples\\skill\\DOC\\FUNCS')/(name+'.txt'))
# Scope corrections are part""")
p.write_text(s,encoding='utf-8')
