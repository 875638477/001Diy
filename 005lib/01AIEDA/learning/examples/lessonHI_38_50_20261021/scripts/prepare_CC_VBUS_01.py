import json,pathlib
h=pathlib.Path(__file__).resolve().parents[1]
for v in ('2L','4L'):
 c=h/f'inventory/checkpoints/postcritical_{v}_b010';n=json.loads((c/'normalized.json').read_text());pins={p['ref']+'.'+str(x['number']):x for p in n['placements'] for x in p['pins']}
 ops=[];proofs=[]
 def r(id,net,points,w=.2):ops.append({'type':'route','id':id,'net':net,'layer':'TOP','points':points,'width':w,'purpose':'Explicit connector auxiliary topology candidate; combined actual-copper/native spacing/return review pending.'})
 r('CC1_ENTRY','USB_CC1',[pins['J2.A5']['xy'],[38.75,8.3],[36.9484,10.1016],pins['R3.1']['xy']])
 r('CC2_ENTRY','USB_CC2',[pins['J2.B5']['xy'],[41.75,8.4],[43.4516,10.1016],pins['R4.1']['xy']])
 for i in (3,4):
  xy=pins[f'R{i}.2']['xy'];vxy=[xy[0]+(-1.1 if i==3 else 1.1),xy[1]]
  r(f'CC_R{i}_GND','GND',[xy,vxy],.4);ops.append({'type':'via','id':f'CC_R{i}_GND_V','net':'GND','xy':vxy,'padstack':'L28_VIA030_C060'})
  proofs.append({'from':f'R{i}.2','to':'U1.23','connected':True})
 proofs+=[{'from':'J2.A5','to':'R3.1','connected':True},{'from':'J2.B5','to':'R4.1','connected':True}]
 d={'status':'ENGINEERING_CANDIDATE_ONLY','variant':v,'operations':ops,'proofs':proofs,'scope':'No widening global USB spacing; finite connector .2mm Class-Class line_line region may be required and must be explicitly proven.'}
 (h/f'plans/CC_entry_{v}_v1.json').write_text(json.dumps(d,indent=2),encoding='utf8')
 print(v,{k:pins[k]['xy'] for k in ('J2.A4_B9','J2.B4_A9','C10.1','R7.1','J2.A1_B12','J2.B1_A12')})