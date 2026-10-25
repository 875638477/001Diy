from pathlib import Path
import json,runpy,hashlib,sys,argparse
sys.dont_write_bytecode=True
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sys.path.insert(0,str(R/'tooling/packages'))
from shapely.geometry import Polygon,Point
Builder=runpy.run_path(str(R/'scripts/scoped_rule_builderHI.py'))['ScopedRuleBuilder']
p=argparse.ArgumentParser();p.add_argument('--variant',choices=['2L','4L'],required=True);p.add_argument('--right',required=True);p.add_argument('--north',required=True);p.add_argument('--south',required=True);p.add_argument('--left',required=True);p.add_argument('--output',required=True);a=p.parse_args();v=a.variant
paths=[Path(getattr(a,n)) for n in ['north','south','left','right']];assert all(t.resolve().is_relative_to(R.resolve()) for t in paths)
plans=[json.loads(t.read_text(encoding='utf-8-sig')) for t in paths];b=Builder(v);outerCoverage=[];mapping=[];regionSerial=0

def region_name(engineeringId,layer):
 global regionSerial
 regionSerial+=1;name=f'HI_JS_R{regionSerial:03d}_{v}'
 mapping.append({'engineeringId':engineeringId,'layer':layer,'nativeName':name});return name

def addphysical(engineeringId,layer,polygon,nets,changes):
 b.physical_region(region_name(engineeringId,layer),layer,polygon,nets,changes)
 approved=changes.get('vias',changes.get('viasAdd',[]))
 if 'HI_VIA026_C052_TENT' in approved:
  outerCoverage.append({'layer':layer,'polygon':Polygon(polygon),'classes':{b.rules[n,'TOP']['physicalClass'] for n in nets}})

for d in plans:
 for x in d.get('physicalExceptions',[]):
  if x['id']=='HI_LEFT07_VBUS18_P' and v=='4L':continue # Same physical class as PB1; root authorizes shared finite2.8 budget, actualVBUS <=1.4 geometric contract retained.
  if x['id']=='HI_LEFT_DIGITAL_SOURCE_P':x=dict(x,maxNeckMM=2.8) # Resolve nonnested overlap with PB1inner2.8; root authorized only this finite group.
  change={'neckwidth_min':x['neckWidthMinMM'],'necklength_max':x['maxNeckMM']}
  if x.get('approvedVias'):change['vias']=x['approvedVias']
  for layer in x.get('layers',[x['layer']]):addphysical(x['id'],layer,x['polygon'],x['nets'],change)
 for x in d.get('spacingExceptions',[]):
  netsA=x.get('netsA',x.get('nets'));netsB=x.get('netsB',x.get('nets'))
  for layer in x.get('layers',[x.get('layer')]):
   assert layer in ['TOP','BOTTOM']
   b.spacing_pairs(region_name(x['id'],layer),layer,x['polygon'],netsA,netsB,x['onlyFields'])
 for x in d.get('rules',[]):
  for layer in x['layers']:
   addphysical(x['id']+'_P',layer,x['polygon'],x['signalNets'],x['physicalOnlyDelta'])
   b.spacing_pairs(region_name(x['id']+'_S',layer),layer,x['polygon'],x['signalNets'],x['signalNets'],x['spacingOnlyDelta'])
actualLayers=['TOP','BOTTOM'] if v=='2L' else ['TOP','L2','L3','BOTTOM'];seen=set();viaScope=[]
for d in plans:
 for op in d['operations']:
  if op['type']!='via' or op.get('padstack','').upper()!='HI_VIA026_C052_TENT':continue
  ident=(op['net'],tuple(op['xy']))
  if ident in seen:continue
  seen.add(ident)
  for layer in actualLayers:
   net,xy=op['net'],op['xy'];klass=b.rules[net,'TOP']['physicalClass']
   if any(c['layer']==layer and klass in c['classes'] and c['polygon'].covers(Point(xy)) for c in outerCoverage):
    viaScope.append({'operationId':op['id'],'net':net,'xy':xy,'layer':layer,'coverage':'planned outer finite source PSet already includes privatevia; no point override to avoid tightening its local neck budget'});continue
   parent,explanation=b.existing_physical_template_at(net,layer,xy)
   name=region_name('VIA_ONLY_'+op['id'],layer);b.via_point_permission(name,net,xy,layer,parent)
   viaScope.append({'operationId':op['id'],'net':net,'xy':xy,'layer':layer,'coverage':name,'actualParentReadbackSelection':explanation,'copyTemplate':parent,'onlyDelta':'viasAdd privatevia','allOtherKeysCopied':True})
b.operations.append({'type':'existingSpacingLayerFields','name':'HI_USB_MCU_S_1_4L' if v=='4L' else 'HI_USB_MCU_S_2_2L','layerValues':{'TOP':{'via_line':'0.2 MM'},'BOTTOM':{'via_line':'0.2 MM'}},'authorization':'Root explicitly permits only original finite SWDIO-ClassPair CSet via_line TOP/BOTTOM .5->.2; original global.5 and other field/layer values must remain unchanged.'})
D={'status':'DRAFT_UNAPPLIED_NATIVE_RULE_ADAPTER_ONLY_GEOMETRY_BATCH_NOT_AUTHORIZED','variant':v,'sourceBoard':json.loads((R/f'inventory/current_{v}.json').read_text()),'engineeringSources':[{'path':str(t),'sha256':hashlib.sha256(t.read_bytes()).hexdigest().upper()} for t in paths],'constraintOperations':b.operations,'regionNameMapping':mapping,'scopeAudit':b.audit,'privateViaLayerScope':viaScope,'pending':['Root complete joint source+long routing approval and final version hashes.','Apply authorized old finite USB_MCU via_line TOP/BOTTOM .5->.2 update and prove exact field/layer diff plus scoped strict challenge.','Apply/retain actual native DRC and controlled local neck/spacing/via rule challenges, then fullboard build and fresh-state readback.','Outside old/global fields and other geometry must be compared; these JSONs are not applied constraints.']}
out=Path(a.output);assert out.resolve().is_relative_to(R.resolve());out.write_text(json.dumps(D,indent=2),encoding='utf8')
print(json.dumps({'status':D['status'],'variant':v,'constraintOperations':len(b.operations),'regions':len(b.audit),'tinyVias':len(seen),'output':str(out)},indent=2))
