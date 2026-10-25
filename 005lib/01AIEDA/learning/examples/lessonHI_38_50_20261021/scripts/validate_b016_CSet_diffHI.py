from pathlib import Path
import json,csv,re
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');s=(R/'scripts/normalize_HI_actual_v5.py').read_text();ns={'json':json,'re':re};exec(s[s.index('def sx('):s.index('symbols=')],ns);sx=ns['sx'];rows=lambda p:list(csv.DictReader(p.open(encoding='utf8'),delimiter='\t',quotechar='\0'))
def cs(B,domain):return {(x['cset'],x['layer']):dict(sx(x['values'])) for x in rows(B/(domain+'_csets.tsv'))}
D={'status':'B016_BOTH_NATIVE_CSET_FIELD_DIFF_VALIDATED','variants':{}}
for v,t in [('2L','12'),('4L','05')]:
 plan=json.loads((R/f'batches/clearance_remaining_{v}_b016_DRC_PENDING_try{t}.json').read_text());B=R/f'logs/reopen_clearance_{v}_b016_DRC_PENDING_stored';old=R/f'logs/reopen_source_{v}_b015_DRC_PENDING_stored';actualChanges=[];copies=[]
 for domain in ['physical','spacing']:
  before=cs(old,domain);after=cs(B,domain)
  intended={}
  for o in plan['constraintOperations']:
   if o['type']=='existingSpacingLayerFields' and domain=='spacing':
    for l,fields in o['layerValues'].items():intended[o['name'],l]=fields
  for key,val in before.items():
   expected=dict(val);expected.update(intended.get(key,{}));assert after[key]==expected,('UnexpectedoldCSetfielddelta',domain,key,val,after[key],expected)
   for k,value in val.items():
    if after[key][k]!=value:actualChanges.append({'domain':domain,'cset':key[0],'layer':key[1],'key':k,'before':value,'after':after[key][k]})
  for o in plan['constraintOperations']:
   if o['type']!='csetCopy' or o['domain']!=domain:continue
   for (name,layer),vals in before.items():
    if name!=o['copyFrom']:continue
    av=after[o['name'],layer];expected=dict(vals);expected.update(o.get('layerValues',{}).get(layer,{}))
    for k,value in o['values'].items():
     if k=='vias':
      if k in vals:
       assert [x for x in av[k].split(':') if x]==value,(o['name'],av[k],value)
       expected[k]=av[k]
     else:expected[k]=value
    assert av==expected,('CopiedCSetunexpecteddelta',o,layer,vals,av,expected)
   copies.append({'domain':domain,'new':o['name'],'staticCopyFromActual':o['copyFrom'],'onlyValues':o['values'],'onlyLayerValues':o.get('layerValues',{}),'allOtherKeysEveryLayerExactlyEqualSource':True})
 build=(R/f'logs/clearance_remaining_{v}_b016_DRC_PENDING_try{t}/hi_batch_execution.txt').read_text();created=re.findall(r'HI_CREATED_ROUTE_NATIVE_NET id="([^"]+)" expected="([^"]+)" object=[^ ]+ actualNet="([^"]+)" layer=',build);assert created and all(a==b for _,a,b in created)
 D['variants'][v]={'sourceExistingCSetKeyDifferencesExactly':actualChanges,'copiedCSets':copies,'allExistingPhysicalCSetsUnchanged':True,'allOtherExistingSpacingKeysAllLayersUnchanged':True,'createdNativePaths':len(created),'everyCreatedPathNativeNetMatchesDeclared':True,'scopeAudit':plan['scopeAudit']}
(R/'review/b016_constraint_field_diff.json').write_text(json.dumps(D,indent=2),encoding='utf8');print(json.dumps({'status':D['status'],'oldFieldDelta':D['variants']['4L']['sourceExistingCSetKeyDifferencesExactly'],'copyCount':len(D['variants']['4L']['copiedCSets'])},indent=2))