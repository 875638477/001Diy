import json,pathlib,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1]
for v in ['2L','4L']:
 def load(f):return json.loads(f.read_text(encoding='utf-8-sig'))
 n=load(H/f'engineering_power/N37_{v}_snapshot.json');pol=load(H/f'engineering_power/N37_{v}_policy.json')
 for a in pol['componentAnchors']:
  if a['net'] in ['GPIO_PB12','GPIO_PB13','GPIO_PB14','GPIO_PB15']:
   vv=[z for z in n['vias'] if z['net']==a['net']];assert len(vv)==1,(a,vv);a['xy']=vv[0]['xy'];a['layers']=['TOP','BOTTOM']
  if a['net'] in ['GPIO_PB1','GPIO_PB10','GPIO_PB11']:a['layers']=['TOP','BOTTOM']
 pol['bottomCost']=1.15;pol['viaCostMM']=2.;pol['topologicalSourceAccessStudy']='Use existing actual signal via as anchor, not arbitrary end of source partial. Any unused source partial must be precisely removed after final route selection.'
 (P/f'GPIO_N37_{v}_40_policy.json').write_text(json.dumps(pol,indent=2),encoding='utf8')
