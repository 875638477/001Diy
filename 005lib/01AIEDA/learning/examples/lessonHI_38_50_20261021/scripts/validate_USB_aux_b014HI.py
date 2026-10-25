from pathlib import Path
import json,csv,hashlib,re
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
report={'status':'PASS_NATIVE_USB_AUX_INTERMEDIATE_BUILD_AND_STORED_REOPEN_NOT_FINAL_RELEASE','variants':{},'limitations':['Final wholeboard full fresh DRC, complete69net routing, actual reference widths/topology and manufacturing assembly review remain pending.','No valid SI impedance or propagation results claimed; internal Field solution failed messages remain.','Fresh readbacks here deliberately read stored DRC and actual geometry/connectivity only, without claiming recalculation.']}
for v in ['2L','4L']:
 C=R/f'inventory/checkpoints/USB_aux_{v}_b014';D=json.loads((C/'networks.json').read_text());N=json.loads((C/'normalized.json').read_text());B=R/f'logs/USB_aux_{v}_b014';F=Path(D['readback']);old=R/f'logs/reopen_SPI_external_{v}_b012_stored_only';L=json.loads((B/'launch.json').read_text());t=(B/'hi_batch_execution.txt').read_text();h=(B/'hi_hse_isolation_challenge.txt').read_text();checks=[]
 def ck(name,value):checks.append({'name':name,'pass':bool(value)});assert value,name
 ck('build process complete exit0 sourceSHAstable',L['completed'] and L['exitCode']==0 and L['beforeSHA256']==L['afterSHA256'])
 ck('no SKILLerror plus real buildCOMPLETE0','*Error*' not in (B/'stdout.txt').read_text() and 'HI_BATCH_COMPLETED drcCount=0' in t)
 ck('numeric fullboard DRC0 enabled',bool(re.search(r'HI_FULL_DRC_REQUEST_RETURN .*result=0 online=t storedDRCs=0',t)))
 ck('actual HSEnegative/rollback complete','HSE_ISOLATION_GRAPH_NEGATIVE_TEST_COMPLETE_FULL_DRC_REQUIRED' in h)
 ck('storedfresh actual69net/266term/branch0',D['summary']['netCount']==69 and D['summary']['nettedTerminalCount']==266 and D['summary']['nativeTerminalFreeBranches']==0)
 ck('80actualplacements and6mechanicalpins',len(N['placements'])==80 and len(N['mechanicalPins'])==6)
 ck('all6actualNPTH',all(p['plating']=='NON_PLATED' for p in N['mechanicalPins']))
 ck('realJ2drill.65x2',sum(p['refdes']=='J2' and p['drillDiameter']==.65 for p in N['mechanicalPins'])==2)
 ck('4mountingdrill2',sum(p['drillDiameter']==2 for p in N['mechanicalPins'])==4)
 ck('exact layers unchanged',N['actualEtchLayers']==(['ETCH/TOP','ETCH/BOTTOM'] if v=='2L' else ['ETCH/TOP','ETCH/L2','ETCH/L3','ETCH/BOTTOM']))
 ck('fullFilm definitions options layers unchanged',(old/'films_full.tsv').read_text()==(F/'films_full.tsv').read_text())
 ck('physical CSet values unchanged',(old/'physical_csets.tsv').read_text()==(F/'physical_csets.tsv').read_text())
 ck('crosssection physical mask0 preserved',(old/'cross_section.tsv').read_text()==(F/'cross_section.tsv').read_text())
 ck('allactual routekeepouts retained',len(N['routeKeepouts'])==6)
 ck('20or17actual endpoint/returnproofs',t.count('HI_ENDPOINT_PROOF')==(20 if v=='2L' else 17))
 if v=='2L':
  cc=(B/'hi_cc_spacing_challenge.txt').read_text();ck('scopedCC strict.4actual.3restore0','CC1_REAL_030_NATIVE_DRC=' in cc and 'expected "0.4 MM" actual "0.3 MM"' in cc and bool(re.search(r'CC_RESTORED_RETURN .*result=0',cc)))
 report['variants'][v]={'board':D['board'],'sha256':D['sha256'],'summary':D['summary'],'proofCount':t.count('HI_ENDPOINT_PROOF'),'checks':checks,'checkCount':len(checks),'fullDRCRequestRecord':[x for x in t.splitlines() if x.startswith('HI_FULL_DRC_REQUEST_')],'readback':str(F),'evidenceDirectory':str(C)}
report['checkCount']=sum(d['checkCount'] for d in report['variants'].values());report['failed']=0
(R/'review/USB_aux_b014_native_validation.json').write_text(json.dumps(report,indent=2),encoding='utf8');print(report['status'],report['checkCount'])
