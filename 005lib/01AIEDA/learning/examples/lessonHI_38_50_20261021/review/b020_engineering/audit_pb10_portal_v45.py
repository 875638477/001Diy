import sys
sys.dont_write_bytecode=True
import pathlib,json,copy,math,hashlib
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sys.path.insert(0,str(R/'review/b020_engineering'))
from audit_pb10_portal_v40 import build,apply,audit,load,CopperScene,Point,LineString,OUT
from audit_pb10_portal_v41 import clear_all,route,via,riproute
from shapely.ops import unary_union
from routing_geometry import plane_from_native

def main():
 reports={}
 for v in ('2L','4L'):
  original,s,_,p80,ev=build(v)
  for o in p80:
   if o.get('id')=='PB10_RELOCATED_ORDINARY_RETURN_2L':o['xy']=[36.9,27.8]
  s,ev=apply(original,p80)
  farY=55.9 if v=="2L" else 55.95
  changes=[]
  pa1x,pa1oldY=(18.2,49.2) if v=='2L' else (18.15,49.25)
  for points in ([[32.75,33.15],[34.1,33.15]],[[15.65,50.25],[32.75,33.15]],[[15.65,farY],[15.65,50.25]]):changes.append(riproute(s,'GPIO_PA3','BOTTOM',points,.2,'PA3_RIP_'+str(len(changes))))
  changes += [route('GPIO_PA3','BOTTOM',[[34.1,33.15],[33.45,33.15],[15.65,50.95],[15.65,farY]],.2,'PA3_LONG_NORMAL_SHIFT_0666'),route('GPIO_PB10','BOTTOM',[[38,26.3],[38,27.7],[30,35.7]],.2,'PB10_NW_0657_NORMAL'),via('GPIO_PB10',[30,35.7],'PB10_NW_STOCK_PORT',.6),route('GPIO_PB10','TOP',[[30,35.7],[29.6,36.1],[28,36.1]],.2,'PB10_NW_TOP_PORTAL'),via('GND',[29.2,35.4],'PB10_NW_RETURN_STOCK',.6)]
  for net in ('GPIO_PA2','GPIO_PA1','GPIO_PC15'):
   for a in s['routes']:
    if a['net']!=net or a['layer']!='ETCH/BOTTOM' or a.get('generatedThermal'):continue
    pts=a['startEnd']
    if net=='GPIO_PA2':selected=any(q in [[33,33.6],[17.5,49.1],[17.55,49.05]] for q in pts)
    elif net=='GPIO_PA1':selected=any(q in [[33.25,34.05],[33.25,34.15],[pa1x,pa1oldY]] for q in pts)
    else:selected=any(q in [[33.55,34.5],[19.25,48.8]] for q in pts)
    if selected:changes.append(riproute(s,net,'BOTTOM',pts,.2,'RIP_NORTH_REPACK_'+str(len(changes))))
  pa2x,pa2endY=(17.55,52.55) if v=='2L' else (17.5,52.6)
  changes += [route('GPIO_PA2','BOTTOM',[[34.25,33.6],[33.6,33.6],[pa2x,67.2-pa2x],[pa2x,pa2endY]],.2,'PA2_LONG_REPACK_672'),route('GPIO_PA1','BOTTOM',[[34.4,34.05],[33.75,34.05],[pa1x,67.8-pa1x],[pa1x,55.9]],.2,'PA1_LONG_REPACK_678'),route('GPIO_PC15','BOTTOM',[[34.8,34.5],[33.9,34.5],[19.25,49.15],[19.25,55]],.2,'PC15_LONG_REPACK_684')]
  changes.append({'type':'deleteVia','id':'PC13_RIP_RECEIVER_VIA','net':'GPIO_PC13','xy':[29.45,39.55]})
  for a in s['routes']:
   if a['net']=='GPIO_PC13' and not a.get('generatedThermal') and [29.45,39.55] in a['startEnd']:
    changes.append(riproute(s,'GPIO_PC13',a['layer'].removeprefix('ETCH/'),a['startEnd'],a['width'],'PC13_RIP_END_'+str(len(changes))))
    changes.append(route('GPIO_PC13',a['layer'].removeprefix('ETCH/'),[[29.25,40.05] if q==[29.45,39.55] else q for q in a['startEnd']],a['width'],'PC13_RECONNECT_END_'+str(len(changes))))
  changes.append(via('GPIO_PC13',[29.25,40.05],'PC13_RELOCATED_STOCK_VIA',.6))
  s2,ev2=apply(s,changes)
  d=R/'inventory/checkpoints'/f'padentry_{v}_b019_DRC_PENDING';sc=CopperScene(s2,load(d/'networks.json'),load(d/'base_net_rules.json'),load(R/'engineering_mcu/plans'/f'GPIO_PB1_inward_{v}_80_policy.json'))
  idx=0
  for a in sc.obstacles:
   if a['kind']=='via':
    z=s2['vias'][idx//2];idx+=1;rad=max(abs(q) for p in z['pads'] if p['layer'].removeprefix('ETCH/')==a['layer'] for xy in p['bbox'] for q in xy);a['geometry']=Point(z['xy']).buffer(rad,quad_segs=128);a['source']=z.get('candidateId','native_via')+':'+str(z['xy'])
  checkops=[o for o in p80 if o.get('id')=='PB10_RELOCATED_ORDINARY_RETURN_2L']+[o for o in changes if o['type'] in ('route','via')]
  rows=clear_all(sc,s2,checkops)
  # Outer reference is a geometric projection of CURRENT native fill, not a hypothetical future repour.
  ref=[]
  for op in [x for x in changes if x['type']=='route' and x['net']=='GPIO_PB10']:
   reference='TOP' if v=='2L' and op['layer']=='BOTTOM' else ('BOTTOM' if v=='2L' else ('L3' if op['layer']=='BOTTOM' else 'L2'))
   copper=unary_union([plane_from_native(dict(p,holes=p.get('holes') or [])) for p in original['planes'] if p['net']=='GND' and p['filled'] and p['layer']=='ETCH/'+reference])
   line=LineString(op['points']);edge=line.buffer(.1,quad_segs=128)
   ref.append({'id':op['id'],'referenceLayer':reference,'projectedCenterlineLengthMM':line.length,'currentFillMissingCenterlineMM':line.difference(copper).length,'currentFillMissingCopperEdgeAreaMM2':edge.difference(copper).area,'scope':'Current native b019 fill only; candidate vias/changed copper require actual repour and native common/HSE checks'})
  reports[v]={'status':'READ_ONLY_LOCAL_CANDIDATE_NOT_NATIVE','scope':'PB10 source to NW local portal; J12 moved connector/full long connection not applied','actualSourceSHA256':hashlib.sha256((R/'native_candidates'/f'HI_{v}_padentry_normalized_b019_DRC_PENDING.brd').read_bytes()).hexdigest().upper(),'jointPB1_80AdaptedOperations':p80,'deltaOperations':changes,'uniqueDeleteEvidence':ev+ev2,'audit':rows,'unresolvedCount':sum(len(x['unresolvedIssues']) for x in rows),'referenceProjection':ref,'ruleChanges':[],'nativeRun':False,'remainingGates':['Rebase full South group and both moved connector variants','Native exact deletions and geometry/physical endpoint preservation','Finite source via approvals for candidate PB1 still need actual native region scope','Refill candidate plane/antipad/thermal, all common GND and HSE unique anchor negative test','Actual DRC per item and unresolved USB/full-board solver boundary']}
  print(v,'unresolved',reports[v]['unresolvedCount'],flush=True)
  for x in rows:
   if x['unresolvedIssues']:print(x['id'],x['layer'],x.get('points',x.get('xy')),x['unresolvedIssues'][:5],flush=True)
  print('reference',ref,flush=True)
 (OUT/'PB10_NW_North4_repack_v45.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()

