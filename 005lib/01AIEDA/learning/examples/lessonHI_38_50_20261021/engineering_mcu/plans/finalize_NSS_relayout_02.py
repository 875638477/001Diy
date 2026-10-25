import pathlib,json,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');q=json.loads((P/'NSS_pullup_local_relayout_01.json').read_text());
for c in q['placementChanges']:
 if c['ref']=='R21':c['xy']=[33.7016,30.7]
 if c['ref']=='R23':c['xy']=[33.5,32.1]
for o in q['operations']:
 if o['id']=='NSS01_MAIN_SOURCE':o['points']=[[34.8,31.15],[33.85,32.1],[33.3984,32.1]]
 if o['id']=='NSS01_LOCAL_PULLUP_STUB':o['points']=[[33.3984,32.1],[33.3984,32.9],[32.6764,33.622],[32.6764,33.7]]
 if o['id']=='NSS01_SCK_SOURCE':o['points']=[[34.385,30.215],[33.9,30.7],[33.6,30.7]]
for v,ops in q['variantOperations'].items():
 for o in ops:
  if o['type']=='route' and o['net']=='SPI_NSS':o['points']=[[31.8236,32.1],[31.5,32.1],[30.8,32.8],[30.3 if v=='4L' else 29.94,32.8],[29.8,32.3] if v=='4L' else [29.6,32.46]]
  if o['type']=='route' and o['net']=='SPI_SCK':o['points']=[[32.0252,30.7],[31.75,30.7],[31,29.95]] if v=='4L' else [[32.0252,30.7],[31.55,30.7],[30.8,29.95]]
q['newPullupStubCenterlineMM']=.8+math.sqrt(2)*.722+.078
q['reason']+=' Exact nominal class check then found 2L MISOvia31.65,29.77 too close to R21 outputpad at y30.6. Final R21y30.7 restores .2235 pad-via gap; R23y32.1 preserves0PlaceBoundoverlap. Narrow framework gap is not actual component body/assembly clearance certification.'
(P/'NSS_pullup_local_relayout_02.json').write_text(json.dumps(q,indent=2),encoding='utf8')
s=(P/'prepare_gpio_future_13.py').read_text(encoding='utf-8-sig').replace('NSS_pullup_local_relayout_01','NSS_pullup_local_relayout_02').replace('_13_','_15_');(P/'prepare_gpio_future_15.py').write_text(s,encoding='utf8');exec(compile(s,str(P/'prepare_gpio_future_15.py'),'exec'))
s=(P/'review_NSS_relayout_classes_01.py').read_text(encoding='utf-8-sig').replace('NSS_pullup_local_relayout_01','NSS_pullup_local_relayout_02').replace('_13_','_15_').replace('class_review_{v}_01','class_review_{v}_02');(P/'review_NSS_relayout_classes_02.py').write_text(s,encoding='utf8');exec(compile(s,str(P/'review_NSS_relayout_classes_02.py'),'exec'))
