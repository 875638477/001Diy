import sys
sys.dont_write_bytecode=True
import pathlib,json,copy,math
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sys.path.insert(0,str(R/'review/b020_engineering'))
from audit_pb10_portal_v40 import build,apply,audit,load,CopperScene,Point,LineString,OUT

def riproute(s,net,layer,points,w,id):return {'type':'deleteSegment','id':id,'net':net,'layer':layer,'points':points,'width':w}
def route(net,l,p,w,id):return {'type':'route','id':id,'net':net,'layer':l,'points':p,'width':w}
def via(net,xy,id,d=.52):return {'type':'via','id':id,'net':net,'xy':xy,'padstack':'HI_VIA026_C052_TENT' if d==.52 else 'L28_VIA030_C060','padDiameterMM':d,'drillDiameterMM':.26 if d==.52 else .3}
def clear_all(sc,s,ops):
 rows=[]
 for o in ops:
  if o['type'] not in ('route','via'):continue
  before=sc.obstacles[:]
  if o['type']=='route':
   # finite RIGHT uses real existing GPIO classpair line/via spacing .16; don't lower any GND fields.
   for la,lb in zip(o['points'],o['points'][1:]):
    g=LineString([la,lb]).buffer(o['width']/2,quad_segs=128);a=audit(sc,o['net'],o['layer'],g,False,8)
    filtered=[]
    for issue in a['baseFieldIssues']:
     # Only base -> known actual finite RIGHT .16 when BOTH entire relevant closest geometries are within rectangle.
     inright=43.5<=min(la[0],lb[0]) and max(la[0],lb[0])<=47.5 and 23.7<=min(la[1],lb[1]) and max(la[1],lb[1])<=29
     digital=issue['net'] and (issue['net'].startswith('GPIO_') or issue['net'] in ('SWO','BOOT0','SWCLK','SWDIO','I2C_SCL','I2C_SDA'))
     if inright and digital and issue['kind'] in ('line','via','smdpin') and issue['gapMM']>=.16-1e-5:issue['finiteRIGHTActualRequirementMM']=.16
     else:filtered.append(issue)
    rows.append({'id':o['id'],'layer':o['layer'],'points':[la,lb],'baseIssues':a['baseFieldIssues'],'unresolvedIssues':filtered,'nearest':a['nearest']})
  else:
   for l in ('TOP','BOTTOM'):
    a=audit(sc,o['net'],l,Point(o['xy']).buffer(o['padDiameterMM']/2,quad_segs=128),True,8)
    rows.append({'id':o['id'],'layer':l,'xy':o['xy'],'unresolvedIssues':a['baseFieldIssues'],'nearest':a['nearest']})
   if s['variant']=='4L':
    for l in ('L2','L3'):
     issues=[];nearest=[]
     for z in s['vias']:
      if z['net']==o['net']:continue
      rad=max((max(abs(x) for p in q['bbox'] for x in p) for q in z['pads'] if q['layer']=='ETCH/'+l),default=0)
      if not rad:continue
      gap=math.dist(o['xy'],z['xy'])-o['padDiameterMM']/2-rad
      req=max(sc.rule(o['net'],'TOP')['allSpacingKeys']['via_via'],sc.rule(z['net'],'TOP')['allSpacingKeys']['via_via'])
      row={'net':z['net'],'xy':z['xy'],'gapMM':gap,'requiredMM':req,'marginMM':gap-req}
      nearest.append(row)
      if gap<req-1e-5:issues.append(row)
     rows.append({'id':o['id'],'layer':l,'xy':o['xy'],'unresolvedIssues':issues,'nearest':sorted(nearest,key=lambda x:x['marginMM'])[:5]})
  sc.obstacles=before
 return rows

def main():
 reports={}
 for v in ('2L','4L'):
  original,s,_,p80,ev=build(v)
  # Replace PB1 candidate source via/arch and remove west L entirely, not a new route in parallel.
  for o in p80:
   if o['type']=='via' and o['net']=='GPIO_PB1' and math.dist(o['xy'],[41.9,26.79])<1e-6:o['xy']=[41.9,26.4]
   if o['type']=='route' and o['net']=='GPIO_PB1' and o['layer']=='TOP' and o['points'][0]==[37,26.75]:o['points']=[[37,26.75],[37.35,27.1],[38.3,27.1],[38.81,26.59],[41.71,26.59],[41.9,26.4]]
  p80=[o for o in p80 if not(o.get('net')=='GPIO_PB1' and (o['type']=='via' and o['xy'] in [[36.25,21.35],[34.2,20]] or o['type']=='route' and (o.get('layer')=='BOTTOM' or o['points'][0]==[36.25,21.35])))]
  s,ev=apply(original,p80)
  # Ordinary source portal rework; all actual outer and inner copper checked below.
  changes=[]
  for net,old,new in [('GPIO_PB5',[46.2,26.15],[46.2,26.25]),('GPIO_PB8',[46.2,28.15],[46.23,28.2])]:
   changes.append({'type':'deleteVia','id':'RIP_'+net+'_VIA','net':net,'xy':old});changes.append(via(net,new,'NEW_'+net+'_VIA'))
   for a in s['routes']:
    if not a.get('generatedThermal') and a['net']==net and (any(math.dist(z,old)<1e-6 for z in a['startEnd']) or a['layer']=='ETCH/BOTTOM' and any(z in [[47.2,26.55],[47.2,27.95],[46.8,26.15],[46.8,28.15]] for z in a['startEnd'])):
     changes.append(riproute(s,net,a['layer'].removeprefix('ETCH/'),a['startEnd'],a['width'],'RIP_'+net+'_'+str(len(changes))))
  changes+= [route('GPIO_PB5','TOP',[[45.1,26.15],[46.2,26.25]],.16,'PB5_TOP_NEW'),route('GPIO_PB5','BOTTOM',[[46.2,26.25],[46.8,26.25],[47.2,26.65],[56.3,26.65],[56.5,26.55]],.2,'PB5_BOTTOM_NEW'),route('GPIO_PB8','TOP',[[45.1,28.15],[46.23,28.2]],.16,'PB8_TOP_NEW'),route('GPIO_PB8','BOTTOM',[[46.23,28.2],[46.8,28.2],[47.2,28.15],[58.8,28.15],[59,27.95]],.2,'PB8_BOTTOM_NEW')]
  # SWO exact segment rework, preserve actual distant endpoint.
  for a in s['routes']:
   if not a.get('generatedThermal') and a['net']=='SWO' and a['layer']=='ETCH/BOTTOM' and any(z in [[46.8,25.15],[47.5,25.85],[50.7,25.85]] for z in a['startEnd']):changes.append(riproute(s,'SWO','BOTTOM',a['startEnd'],a['width'],'RIP_SWO_'+str(len(changes))))
  changes.append(route('SWO','BOTTOM',[[46.2,25.15],[46.8,25.15],[47.3,25.65],[50.5,25.65],[50.7,25.85]],.2,'SWO_BOTTOM_NEW'))
  changes += [route('GPIO_PB1','BOTTOM',[[41.9,26.4],[43.7,26.4],[44.4,25.7],[45.4,25.7]],.2,'PB1_EAST_NORMAL_IN'),route('GPIO_PB1','BOTTOM',[[45.4,25.7],[46.74,25.7],[47.19,26.15]],.16,'PB1_EAST_SHORT_NECK'),route('GPIO_PB1','BOTTOM',[[47.19,26.15],[49.5,26.15]],.2,'PB1_EAST_PORTAL'),route('GPIO_PB10','BOTTOM',[[38,26.3],[39,26.3],[39.3,26.6],[40.3,26.6],[40.85,27.15],[42.6,27.15],[43.125,27.675],[45.4,27.675]],.2,'PB10_EAST_NORMAL_IN'),route('GPIO_PB10','BOTTOM',[[45.4,27.675],[46.8,27.675]],.16,'PB10_EAST_SHORT_NECK'),route('GPIO_PB10','BOTTOM',[[46.8,27.675],[49.5,27.675]],.2,'PB10_EAST_PORTAL')]
  s2,ev2=apply(s,changes)
  d=R/'inventory/checkpoints'/f'padentry_{v}_b019_DRC_PENDING';sc=CopperScene(s2,load(d/'networks.json'),load(d/'base_net_rules.json'),load(R/'engineering_mcu/plans'/f'GPIO_PB1_inward_{v}_80_policy.json'))
  # Audit against full candidate including self-net exclusion; genuine pair interactions among all new routes/vias included.
  rows=clear_all(sc,s2,[o for o in p80+changes if o['type'] in ('route','via') and (o['net'] in ('GPIO_PB1','GPIO_PB10','GPIO_PB5','GPIO_PB8','SWO') or o.get('id')=='PB10_RELOCATED_ORDINARY_RETURN_2L')])
  reports[v]={'status':'READ_ONLY_LOCAL_ENGINEERING_CANDIDATE_NOT_NATIVE','p80AdaptedOperations':p80,'deltaOperations':changes,'uniqueDeleteEvidence':ev+ev2,'audit':rows,'unresolvedCount':sum(len(x['unresolvedIssues']) for x in rows)}
  print(v,'unresolved',reports[v]['unresolvedCount'],flush=True)
  for x in rows:
   if x['unresolvedIssues']:print(x['id'],x['layer'],x.get('points',x.get('xy')),x['unresolvedIssues'][:3],flush=True)
 (OUT/'PB1_PB10_RIGHT_joint_v41.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf8')
if __name__=='__main__':main()
