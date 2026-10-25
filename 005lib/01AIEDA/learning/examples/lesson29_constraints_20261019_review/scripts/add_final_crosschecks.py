from pathlib import Path
B=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019_review')
p=B/'scripts'/'review29.py';s=p.read_text()
s=s.replace('import csv,json,re,hashlib,collections','import csv,json,re,hashlib,collections,math')
add=r'''
cp=table(A/'logs'/'read_coupon'/'route_geometry.tsv')
eq('Exactly two persistent coupon traces',len(cp),2)
for r in cp:
 numbers=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',r['startEnd'])]
 length=math.hypot(numbers[2]-numbers[0],numbers[3]-numbers[1])
 eq('Coupon '+q(r['net'])+' independent geometric length mm',length,20.0)
 eq('Coupon '+q(r['net'])+' actual width mm',float(r['width']),0.2)
rc=json.loads((A/'logs'/'read_coupon'/'launch.json').read_text())
ck('Separate coupon new-process readonly exit0',rc['completed'] and rc['exitCode']==0 and rc['beforeSHA256']==rc['afterSHA256'])
ck('Separate coupon current DRC0/t','drcs=0\ndrcState=t' in (A/'logs'/'read_coupon'/'native_summary.txt').read_text())
exp=json.loads((A/'exports'/'export_result.json').read_text())
eq('Official technology export actual SHA',sha(A/'exports'/'F29_RULES.tcf'),exp['outputSHA256'])
for r in exp['records']:
 ck('Technology '+r['step']+' exit0 and board unchanged',r['exitCode']==0 and r['boardBefore']==expectedSHA and r['boardAfter']==expectedSHA)
ct=(A/'exports'/'techfile_run'/'compare_stdout.txt').read_text(errors='replace')
ct+=(A/'exports'/'techfile_run'/'compare_techfile.log').read_text(errors='replace')
ck('Official technology compare no changes','No objects were updated' in ct)
'''
s=s.replace('# Evidence identity snapshot, not a copy of implementation validator.',add+'\n# Evidence identity snapshot, not a copy of implementation validator.')
s=s.replace("'status':'REVIEW_NATIVE_CONSTRAINTS'","'status':'PASS_INDEPENDENT_REVIEW_LESSON29'")
s=s.replace("(R/'review_core.json').write_text","(R/'review_final.json').write_text")
p.write_text(s,encoding='utf-8')
print('Independent geometry and export cross-checks added')
