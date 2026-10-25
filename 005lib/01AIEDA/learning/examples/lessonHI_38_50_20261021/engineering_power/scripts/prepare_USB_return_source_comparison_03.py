from pathlib import Path
import sys,json,math,hashlib
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');O=H/'engineering_power'
sys.path[:0]=[str(H/'scripts'),str(H/'tooling/packages')]
from routing_geometry import *
for v in ['2L','4L']:
 cp=H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING';n=load(cp/'normalized.json');w=load(cp/'networks.json');ops=[]
 oldxy=[40.,20.5];newxy=[39.8,20.52];rx='PA10_UART_RX';tx='PA9_UART_TX'
 matches=[a for a in n['vias']if a['net']==rx and a['xy']==oldxy];assert len(matches)==1
 ops.append(dict(type='deleteVia',id='USBRET_RX_OLD_VIA_RIP',net=rx,xy=oldxy,padstack=matches[0]['padstack']))
 def rip(net,layer,a,b,width):
  matches=[q for q in n['routes']if q['net']==net and q['layer']=='ETCH/'+layer and q['width']==width and(q['startEnd']==[a,b]or q['startEnd']==[b,a])];assert len(matches)==1,(v,net,a,b,width,len(matches))
  ops.append(dict(type='deleteSegment',id=f'USBRET_RIP_{len(ops)}',net=net,layer=layer,points=[a,b],width=width))
 rip(rx,'TOP',[40.25,22.75],[40.25,22.05],.16)
 rip(rx,'TOP',[40.205,21.285],[40,21.08],.16);rip(rx,'TOP',[40,21.08],[40,20.5],.16)
 rip(rx,'BOTTOM',[40,20.5],[40,20.3],.2);rip(rx,'BOTTOM',[40,20.3],[48.4,20.3],.2)
 rip(tx,'BOTTOM',[39.7,21.7],[40.4,21.7],.2);rip(tx,'BOTTOM',[40.4,21.7],[40.8,21.3],.2);rip(tx,'BOTTOM',[40.8,21.3],[40.8,20.85],.2);rip(tx,'BOTTOM',[40.8,20.85],[40.95,20.7],.2)
 ops.append(dict(type='via',id='USBRET_RX_NEW_VIA',net=rx,xy=newxy,padstack=matches[0]['padstack'],padDiameterMM=.52,purpose='PrivatePTHsame.26drill/.52copper, relocatedtoavoidUSBsharedreferenceprojection; allactualconductorpointapprovalmustbeadapted'))
 def route(net,layer,pts,width,purpose):ops.append(dict(type='route',id=f'USBRET_{net}_{layer}_{len(ops)}',net=net,layer=layer,points=pts,width=width,purpose=purpose))
 route(rx,'TOP',[[40.25,22.75],[40.25,22.35]],.2,'ExplicitnormalanchorinsideactualMCUpad; preserveexternalCuedges/2.4mmneckbudget')
 route(rx,'TOP',[[40.25,22.35],[40.25,22.05]],.16,'JoinexistingunmodifiedMCUsourcepartial')
 route(rx,'TOP',[[40.205,21.285],[39.8,20.88],newxy],.16,'LocalordinaryRXapproach; preserveMCUpin/USB/C14; actualneck2.0164mmestimatedafterpadnormalization')
 route(rx,'BOTTOM',[newxy,[40.02,20.3],[48.4,20.3]],.2,'KeeporiginalRXeastendpoint; shiftonlysourcepoint andshortapproach')
 route(tx,'BOTTOM',[[39.7,21.7],[40.08,21.32],[40.08,21.07],[40.45,20.7],[40.95,20.7]],.2,'MoveTXparallellegwestoftheUSBsharedcolumns; lastsharedcrossingremainsfiniteandunverified')
 out=dict(status='READ_ONLY_DERIVED_GEOMETRY_REFERENCE_COMPARISON_DO_NOT_EXECUTE',batchId=f'USB_RETURN_SOURCE_COMPARE_{v}_03',variant=v,sourceExpectedSHA256=w['sha256'],sourceCheckpoint=str(cp),operations=ops,placementChanges=[],constraintOperations=[],connectivityProofs=[{'from':'U1.30','to':'R16.1','connected':True},{'from':'U1.31','to':'R17.1','connected':True}],pending=['FullactualspacinginclallprivateviaCuLayers/pointapprovedscope','PA10existingregional2.4maxneckbudgetunchanged; normal.2insideactualpadfullycovered','Oldsourcealias40,20.5musttransparentlyretiretoactual39.78,20.37,notwaivephysicalpinproofs','Actualpostfillcommonreferencefootprint/coplanarneck/returnnetbenefitbeforeacceptance','Rootapprovalandnativefullalloldproof/HSE/refillhealthbeforeanysave'])
 p=O/f'USB_RETURN_SOURCE_COMPARE_{v}_03.json';p.write_text(json.dumps(out,indent=2)+'\n');print(v,p,len(ops))
