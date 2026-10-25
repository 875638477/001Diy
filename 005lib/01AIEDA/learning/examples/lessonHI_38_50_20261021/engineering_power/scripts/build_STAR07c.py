from pathlib import Path
import json,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
s=json.loads((R/'STAR_reroute_07b.json').read_text(encoding='utf-8'))
for o in s['operations']:
 if o['id']=='STAR_DIAG_GROUND_RETURN':
  o['points']=[[35.75,24.75],[36.48,24.75],[36.952,25.222],[38,25.27]]
  o['purpose']='Newneck1.397508<=existingG31max1.4; normal.6startswithGPIO22padgap.302, viaunchanged. Avoidold1.465391neck overlappingoriginal1.4region.'
for r in s['rules']:r['physicalOnlyDelta']['necklength_max_mm']=1.4;r['actualNeck_mm']=.73+math.hypot(.472,.472)
s['revision']='07c nativeb009 proved1.4oldregionwins atoverlap; geometryshortenedtoneck1.397508, newregion1.4 matchesold, noexistingor globalrulechange.'
s['criticalLengths_mm']['newGNDNeck']=.73+math.hypot(.472,.472)
s['prerequisites']=[x.replace('1.465391','1.397508').replace('max1.5','max1.4') for x in s['prerequisites']]
s['rejectedPrior'].append(dict(file='STAR_reroute_07b.json',reason='NativeoverlappingG31max1.4 actualnewneck1.4654, 1DRC. Do not raiseoldrule;07c flares earlier by.048/.048.'))
(R/'STAR_reroute_07c.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
patch=dict(status='READONLY_GEOMETRY_PATCH_FOR_FAILED_B009_NOT_NATIVE_INSTRUCTION',operations=[
dict(type='deleteSegment',id='DELETE_07B_GND_NECK',net='GND',layer='TOP',points=[[36.48,24.75],[37,25.27]],width=.25),
dict(type='deleteSegment',id='DELETE_07B_GND_NORMAL',net='GND',layer='TOP',points=[[37,25.27],[38,25.27]],width=.6),
dict(type='route',id='STAR_DIAG_GROUND_RETURN_PATCH',net='GND',layer='TOP',points=[[36.48,24.75],[36.952,25.222],[38,25.27]],widths=[.25,.6])])
(R/'source/07c_patch_on_b009_for_geometry_only.json').write_text(json.dumps(patch,indent=2)+'\n',encoding='utf-8')
c=(R/'scripts/precheck_STAR07b_V306b.py').read_text()
c=c.replace("base=json.loads((R.parent/'inventory/checkpoints/mcu_4L_b006/normalized.json').read_text())","base=json.loads((R/'source/postcritical_b009_geometry_for_07c_review.json').read_text())")
c=c.replace("files=['STAR_reroute_07b.json','interface_CAN_routes_04.json','CAN_local_supply_05.json','V3_peripheral_distribution_06b.json']","files=['source/07c_patch_on_b009_for_geometry_only.json']")
c=c.replace("'STAR_DIAG_GROUND_RETURN:0'","'STAR_DIAG_GROUND_RETURN_PATCH:0'").replace("'STAR_DIAG_GROUND_RETURN:1'","'STAR_DIAG_GROUND_RETURN_PATCH:0'")
c=c.replace("'readouts/STAR07b_V306b_CAN_geometry_precheck.json'","'readouts/STAR07c_actual_postcritical_geometry_precheck.json'")
c=c.replace('FrozenMCU6 actual snapshot with2oldSTARsegments explicitlyremoved in memory; eachmatchunique.','Actualpostcriticalb009snapshot(1neckDRC,notacceptedboard). Only2oldGNDsegmentsremoved in memory,unique.07c newneck1.397508<=1.4. ExistingLEFTspacing.2 retained.')
(R/'scripts/precheck_STAR07c_actual.py').write_text(c)
print('saved07c neck',s['criticalLengths_mm']['newGNDNeck'])
