import sys
sys.dont_write_bytecode=True
import pathlib,json,math
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');O=R/'review/b020_engineering';sys.path.insert(0,str(R/'scripts'))
from routing_geometry import CopperScene,load,Point,LineString
summary={}
for v in ('2L','4L'):
 s=load(O/f'PB10_NW_{v}_v46_snapshot.json');d=R/'inventory/checkpoints'/f'padentry_{v}_b019_DRC_PENDING';rules=load(d/'base_net_rules.json');policy=load(R/'engineering_mcu/plans'/f'GPIO_PB1_inward_{v}_80_policy.json');sc=CopperScene(s,load(d/'networks.json'),rules,policy);cache={};rows=[];drill=[]
 for op in load(O/f'PB10_NW_{v}_v46_delta.json'):
  if op['type']=='route':
   key=op['net'],op['layer'],op['width']
   if key not in cache:cache[key]=sc.forbidden(op['net'],op['layer'],op['width'],False,0)
   forbidden,allowed=cache[key];line=LineString(op['points']);r=sc.rule(op['net'],op['layer']);rows.append({'id':op['id'],'kind':'ROUTE','net':op['net'],'layer':op['layer'],'normalWidthRuleMM':r['widthMinMM'],'candidateWidthMM':op['width'],'widthIsNormal':op['width']>=r['widthMinMM'],'actualAllowEtch':r['allowEtch'],'allPolicyRouteAndMechanicalClear':allowed.covers(line) and not forbidden.intersects(line),'scope':'Native export ROUTE_KEEPOUT, all four mounting-hole teaching zones, original HSE reservedAreas and native-derived finite spacing model'})
  elif op['type']=='via':
   per=[]
   for layer in ('TOP','BOTTOM'):
    forbidden,allowed=sc.forbidden(op['net'],layer,0,True,0);p=Point(op['xy']);r=sc.rule(op['net'],layer);per.append({'layer':layer,'nativeBaseApprovedList':r.get('approvedVias'),'stockPadstackInApprovedList':op['padstack'] in r.get('approvedVias',''),'keepoutReservedSMTAndBaseSpacingClear':allowed.covers(p) and not forbidden.intersects(p)})
   rows.append({'id':op['id'],'kind':'VIA','xy':op['xy'],'perLayer':per})
   nearest=[]
   for a in s['vias']:
    if math.dist(a['xy'],op['xy'])<1e-6:continue
    gap=math.dist(a['xy'],op['xy'])-(a['drill']+op['drillDiameterMM'])/2
    nearest.append({'net':a['net'],'xy':a['xy'],'drillToDrillGapMM':gap})
   drill.append({'id':op['id'],'appliesSameAndDifferentNet':True,'minimumDrillToDrillGapMM':min(x['drillToDrillGapMM'] for x in nearest),'conservativeRequiredHoleHoleMM':max(r['allSpacingKeys']['hole_hole'] for r in rules['rules'] if r['layer']=='TOP'),'nearestPairs':sorted(nearest,key=lambda a:a['drillToDrillGapMM'])[:3],'outerSMDHoleClearanceBasis':'Copper disk .6/finished drill .3 gives .15 radial annulus; copper clearance .2/.3 audit therefore implies drill-to-pad >= .35/.45. Existing PTH and mechanical holes are distant and additionally covered by actual native keepout/copper objects.'})
 print(v,[(x['id'],x.get('allPolicyRouteAndMechanicalClear',x.get('perLayer'))) for x in rows],flush=True)
 summary[v]={'checks':rows,'newDrillPairs':drill,'failures':[x for x in rows if x.get('allPolicyRouteAndMechanicalClear') is False or 'perLayer' in x and not all(y['stockPadstackInApprovedList'] and y['keepoutReservedSMTAndBaseSpacingClear'] for y in x['perLayer'])]}
(O/'PB10_v46_policy_and_hole_checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8')
