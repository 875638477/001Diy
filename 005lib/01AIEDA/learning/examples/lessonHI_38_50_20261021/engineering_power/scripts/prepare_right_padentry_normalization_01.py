from pathlib import Path
import sys,json,hashlib,math
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');O=H/'engineering_power'
sys.path[:0]=[str(H/'scripts'),str(H/'tooling/packages')]
from routing_geometry import *
items=[('BOOT0',44,27.75,'R28.1'),('GPIO_PA15',38,24.75,'J13.4'),('GPIO_PB4',40,25.75,'J13.5'),('I2C_SCL',42,26.75,'R19.2')]
manifest=[]
for v in ['2L','4L']:
 cp=H/f'inventory/checkpoints/TOP_trial_{v}_b018_PRE_ALL69_DRC_PENDING';n=load(cp/'normalized.json');w=load(cp/'networks.json');u=next(a for a in n['placements']if a['ref']=='U1');ops=[];proofs=[];details=[]
 for net,pin,y,target in items:
  actual=next(a for a in u['pins']if a['number']==str(pin));assert actual['net']==net
  geom=box(*[z for xy in actual['padBBox']for z in xy])
  a=[44.25,y];b=[45.0,y];newa=[44.65,y];matches=[r for r in n['routes']if r['net']==net and r['layer']=='ETCH/TOP'and abs(r['width']-.16)<1e-6 and(r['startEnd']==[a,b]or r['startEnd']==[b,a])]
  assert len(matches)==1,(v,net,len(matches))
  before=geom.union(LineString([a,b]).buffer(.08,quad_segs=32));after=geom.union(LineString([newa,b]).buffer(.08,quad_segs=32)).union(LineString([a,newa]).buffer(.10,quad_segs=32));lost=before.difference(after);added=after.difference(before)
  assert lost.area<1e-12 and added.area<1e-12,(lost.area,added.area)
  assert geom.covers(Point(newa).buffer(.08));assert geom.covers(LineString([a,newa]).buffer(.1,quad_segs=32))
  ops.extend([dict(type='deleteSegment',id=f'PADENTRY_{v}_{net}_RIPUP',net=net,layer='TOP',points=[a,b],width=.16),dict(type='route',id=f'PADENTRY_{v}_{net}_NORMAL_IN_LAND',net=net,layer='TOP',points=[a,newa],width=.2,purpose='Explicitpincenteranchor normalwidthpath fullyinsideactual.30mmwidthland;Cuunionunchanged'),dict(type='route',id=f'PADENTRY_{v}_{net}_LAND_ENTRY',net=net,layer='TOP',points=[newa,b],width=.16,**{'from':f'U1.{pin}'},purpose='Normalize redundant padinternal .16path to.2normal+shorter.16object within existing solid land; actual external copper unchanged; preserve2mmneckbudget')])
  proofs.append(dict(id=f'PADENTRY_{v}_{net}_REAL_PIN',**{'from':f'U1.{pin}','to':target},connected=True))
  details.append(dict(net=net,pin=f'U1.{pin}',actualPinXY=actual['xy'],actualLandBBox=actual['padBBox'],oldPath=matches[0]['startEnd'],newPath=[newa,b],normalInsideLandPath=[a,newa],normalInsideLandWidthMM=.2,normalRoundCapFullyCoveredByLand=True,newStartInsideLandMarginToRightEdgeMM=44.85-44.65,removedCuAreaOutsideActualLandMM2=lost.area,addedCuAreaOutsideActualLandMM2=added.area,oldNativeNeck2mmBudgetActualMM=.75+math.sqrt(.02)+1.25,newPathObjectNeckExpectedMM=.35+math.sqrt(.02)+1.25,externalNarrowCopperExpectedLengthMM=.15+math.sqrt(.02)+1.25,notes='Keep explicitcenter44.25 anchor withnormal.2path tolandinternal44.65, then.16; no actual externalneck shortens, no CSet/spacing/budget changes. Native must verify freshalloldpins/aliases/health/scopedDRC.'))
 # Check proof targets against true physicalpin net rather than guessedJ13map.
 pins={f"{c['ref']}.{a['number']}":a for c in n['placements']for a in c['pins']}
 for proof in proofs:
  assert pins[proof['from']]['net']==pins[proof['to']]['net'],proof
 out=dict(status='READY_FOR_NATIVE_PAD_INTERNAL_REDUNDANT_PATH_NORMALIZATION_NOT_ROUTING_OR_SI_FIX',batchId=f'RIGHT_PADENTRY_NORMALIZE_{v}_01',variant=v,sourceExpectedSHA256=w['sha256'],sourceCheckpoint=str(cp),operations=ops,connectivityProofs=proofs,constraintOperations=[],placementChanges=[],newVias=[],geometryEvidence=details,nativeContract=['Exactfirstsegmentmustuniquelymatch; no fullnetorparentpathdelete','ActualU1lands remain intact; fournewstartpoints .16roundcaps fullyinside existinglandCu','No change to exterior copper edges, signalvias, HSEpolygons/anchor, plane boundary or permanentvoids','Retain2mmMaxNeckLength andallP/S/E values; recordbefore2.1414/afteractualnativevalue','Allcumulativephysicalpin/ground/oldendpoint proofsmuststay; no legacyalias waived','FourchangednetsscopeDRC plus freshreadback andactualfillgroundhealth; wholeboardDRC stillseparatepending'])
 p=O/f'RIGHT_PADENTRY_NORMALIZE_{v}_01.json';p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf8');manifest.append(dict(variant=v,path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),operations=len(ops),diffAreaMM2=0,proofs=proofs))
(O/'readouts/RIGHT_PADENTRY_NORMALIZE_01_manifest.json').write_text(json.dumps(dict(status='FROZEN_READY_NATIVE',files=manifest),indent=2)+'\n',encoding='utf8');print(json.dumps(manifest))
