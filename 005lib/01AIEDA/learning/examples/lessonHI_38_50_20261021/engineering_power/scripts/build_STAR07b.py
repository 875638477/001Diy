from pathlib import Path
import json,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
s=json.loads((R/'STAR_reroute_07.json').read_text())
s['revision']='07b actualpad/retainedcopper screen corrected GNDbridge aroundGPIO22/VDD24tip'
for o in s['operations']:
 if o['id']=='STAR_DIAG_GROUND_RETURN':
  o['points']=[[35.75,24.75],[36.48,24.75],[37,25.27],[38,25.27]]
  o['widths']=[.25,.25,.6];o['purpose']='GNDneck .73+.735391=1.465391 aroundGPIO22andretainedVDD24tip; onlynewGNDsmallphysicalregionmax1.5, normal.6 afterpadfield. No extrabroadspacingexception.'
 if o['id']=='V_HI_STAR_GND_EAST':
  o['xy']=[38,25.27];o['purpose']='EastofnewBOTTOMstarvertical, gap.40;TOP .6normalreturn gap.42 toexistingVDD24 .6tip, .35 toGPIO22pad.'
s['prerequisites']=[x for x in s['prerequisites'] if'Noadditionalneckbudget' not in x]
s['prerequisites'].append('NewGNDneck1.465391 requires GND-only tinyTOPregionmax1.5; allglobalvalues/POWER neck budgets and allspacingfieldsunchanged. Ifnative findsotheractualDRC, stopnotblindrelax.')
s['rules']=[dict(id='HI_STAR_RETURN_GND',layer='TOP',polygon=[[35.15,24.45],[38.4,24.45],[38.4,25.7],[35.15,25.7]],
 physicalCopy='actualbaseGND.6/.25/maxneck1CSet, withallfieldsandviapermissionspreserved',
 physicalOnlyDelta={'necklength_max_mm':1.5},appliesTo='GNDonly:4LG31_GND_P,2LHI2L_GROUND_P',
 actualNeck_mm=.73+math.sqrt(.52**2+.52**2),
 spacing='No newspacingcopy. ExistingHI_U1_INNER_LEFT POWER/GROUND spacing.2 alreadycoversnearestpin22corner; outside normal.3 satisfies.')]
s['criticalLengths_mm']['newGNDNeck']=.73+math.sqrt(.52**2+.52**2)
s['rejectedPrior']=[dict(file='STAR_reroute_07.json',reason='OnlynewGNDbridge draftfailed: pin22AABB andretainedVDD24tip. Deletedpowersegments/newdiagonal/TOPtap themselves clear.')]
(R/'STAR_reroute_07b.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
c=(R/'scripts/precheck_STAR07_V306b.py').read_text().replace("'STAR_reroute_07.json'","'STAR_reroute_07b.json'").replace("'readouts/STAR07_V306b_CAN_geometry_precheck.json'","'readouts/STAR07b_V306b_CAN_geometry_precheck.json'")
(R/'scripts/precheck_STAR07b_V306b.py').write_text(c)
print('saved07bGNDneck',s['criticalLengths_mm']['newGNDNeck'])
