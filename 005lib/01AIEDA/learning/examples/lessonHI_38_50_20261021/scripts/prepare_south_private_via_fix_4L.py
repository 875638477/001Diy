import pathlib,json,copy,hashlib,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021'); C=P/'inventory/checkpoints/source_4L_b015_DRC_PENDING';s=json.loads((C/'normalized.json').read_text(encoding='utf8'));ops=[]
changes=[('GPIO_PB13',[37.5,20.75],[37.5,20.725]),('GPIO_PB15',[38.5,20.7],[38.5,20.675])]
for net,old,new in changes:
 label=net.replace('GPIO_','')
 via=[v for v in s['vias'] if v['net']==net and math.dist(v['xy'],old)<1e-8];assert len(via)==1
 ops.append(dict(type='deleteVia',id=label+'_VIA_SPACING_RIP',net=net,xy=old,padstack=via[0]['padstack']))
 selected=[r for r in s['routes'] if r['net']==net and any(math.dist(x,old)<1e-8 for x in r['startEnd'])]
 if net=='GPIO_PB13':
  tail=[r for r in s['routes'] if r['net']==net and r['layer']=='ETCH/BOTTOM' and r['startEnd']==[[37.3,20.55],[37.3,19.7]]];assert len(tail)==1;selected+=tail
 for i,r in enumerate(selected):ops.append(dict(type='deleteSegment',id=label+f'_VIA_SPACING_RIP_{i}',net=net,layer=r['layer'].removeprefix('ETCH/'),points=r['startEnd'],width=r['width']))
 ops.append(dict(type='via',id=label+'_VIA_SPACING_NEW',net=net,xy=new,padstack=via[0]['padstack'],padDiameterMM=.52,drillDiameterMM=.26))
 ops.append(dict(type='route',id=label+'_VIA_SPACING_TOP',net=net,layer='TOP',points=[[new[0],21.85],new],width=.16))
 points=[new,[37.3,20.525],[37.3,19.7]] if net=='GPIO_PB13' else [new,[38.5,22.3]]
 ops.append(dict(type='route',id=label+'_VIA_SPACING_BOTTOM',net=net,layer='BOTTOM',points=points,width=.16))
result=dict(batchId='root_south_private_via_spacing_4L_01',variant='4L',status='ACTUAL_B015_EXPLICIT_GEOMETRIC_CLEARANCE_FIX_REQUIRES_NATIVE',sourceCheckpoint=str(C),sourceExpectedSHA256=hashlib.sha256((P/'native_candidates/HI_4L_source_b015_DRC_PENDING.brd').read_bytes()).hexdigest().upper(),operations=ops,privateViaNewCenters=[{'net':net,'oldXY':old,'newXY':new,'padstack':'HI_VIA026_C052_TENT','layers':['TOP','L2','L3','BOTTOM'],'scope':'Recreate via-list-only .02x.02mm local physical approval around actual new center, copy each actual parent physical CSet unchanged. No inner via spacing reduction.'} for net,old,new in changes],proofs=[{'net':'GPIO_PB13','source':'U1.26','toAlias':'PB13_VIA_SPACING_NEW'},{'net':'GPIO_PB15','source':'U1.28','toAlias':'PB15_VIA_SPACING_NEW'}],longRouteAnchorsUnchanged={'GPIO_PB13':[37.3,19.7],'GPIO_PB15':[38.5,22.3]},measurements={'adjacentViaCopperClearanceMM':math.hypot(.5,.525)-.52,'PB13TopTotalNeckMM':.65+math.hypot(.25,.25)+(21.85-20.725),'PB15TopTotalNeckMM':.65+math.hypot(.25,.25)+(21.85-20.675),'PB15BottomTotalNeckMM':22.3-20.675,'existingMaxSourceNeckMM':2.4},reason='Actual4L cache found .1871mm via-via at innerL2/L3 and BOTTOM against .2mm. Move only2 sourcevias .025mm south; preserve .2mm all-layer via spacing and frozen long endpoints, do not hide physical inner pads or lower DEFAULT.')
(P/'plans/root_south_private_via_spacing_4L_01.json').write_text(json.dumps(result,indent=2),encoding='utf8');print('ops',len(ops));print(result['measurements'])
