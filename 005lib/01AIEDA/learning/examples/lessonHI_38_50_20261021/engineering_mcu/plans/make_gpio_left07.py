import pathlib,json,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');q=json.loads((P/'GPIO_left_joint_fanout_06.json').read_text());q['batchId']='GPIO_left_joint_fanout_07'
for o in q['operations']:
 if o['net']=='GPIO_PB1':
  if o['type']=='via':o['xy']=[38.3,27.35]
  elif o['type']=='route':o['points']=[[35.75,26.75],[37.4,26.75],[37.9,26.95],[38.3,27.35]]
q['partialEndpoints']['GPIO_PB1']['xy']=[38.3,27.35]
q['operations'] += [dict(type='route',id='LEFT07_VBUS18_SOURCE',net='VBUS_PRESENT_N',layer='TOP',points=[[35.75,27.25],[35,27.25],[34.6,26.85]],width=.16,purpose='Accessible outward source hook after PB1 moved inward. Exact peer pads/via/STAR clearance must pass combined native.'),dict(type='via',id='LEFT07_VBUS18_VIA',net='VBUS_PRESENT_N',xy=[34.6,26.85],padstack='HI_VIA026_C052_TENT',padDiameterMM=.52,drillDiameterMM=.26)]
q['partialEndpoints']['VBUS_PRESENT_N']=dict(xy=[34.6,26.85],layer='BOTTOM',connectedTo='U1.18')
q['physicalExceptions'].append(dict(id='HI_LEFT07_PB1_INNER_P',layer='TOP',polygon=[[35.4,26.4],[38.7,26.4],[38.7,27.7],[35.4,27.7]],nets=['GPIO_PB1'],neckWidthMinMM=.16,maxNeckMM=2.8,approvedVias=['L28_VIA030_C060','HI_VIA026_C052_TENT'],basis='Total source 2.7542mm. Short21.8deg segment threads measured gap between native GND37.4,27.4 and PB10source38,26.4 without via-in-pad; not arbitrary boardwide .16.'))
q['physicalExceptions'].append(dict(id='HI_LEFT07_VBUS18_P',layer='TOP',polygon=[[34.25,26.5],[36.5,26.5],[36.5,27.7],[34.25,27.7]],nets=['VBUS_PRESENT_N'],neckWidthMinMM=.16,maxNeckMM=1.4,approvedVias=['L28_VIA030_C060','HI_VIA026_C052_TENT']))
q['spacingExceptions'].append(dict(id='HI_LEFT07_PB1_GND_S',layer='TOP',polygon=[[35.4,26.4],[38.7,26.4],[38.7,27.7],[35.4,27.7]],netsA=['GPIO_PB1'],netsB=['GND'],onlyFields=dict(via_line=.2),basis='Only narrow TOP source passing native common-GND via row; outside all GND parent.3 remains. New PB1 signalvia itself commonGND37.4,27.4 edgegap.341>.3.'))
q['revision']+=' Joint pin18/PB1: remove old PB1 outside via/neck by replacing pending left06 only, PB1 inward2.7542mm TOP source, VBUS18 outward .52via34.6,26.85 has proposed Cu gap .3239 to actual STAR. No unused inner VBUS36.5,27.6 candidate is created. Requires NSS_pullup_local_relayout_01 to remove source cage before long continuation.'
q['expectedProofs']=q.get('expectedProofs',[])+[{'from':'U1.18','toAlias':'LEFT07_VBUS18_VIA','connected':True},{'from':'U1.19','toAlias':next(o['id'] for o in q['operations'] if o['type']=='via' and o['net']=='GPIO_PB1'),'connected':True}]
(P/'GPIO_left_joint_fanout_07.json').write_text(json.dumps(q,indent=2),encoding='utf8')
print('left07 source18 and PB1 complete')
