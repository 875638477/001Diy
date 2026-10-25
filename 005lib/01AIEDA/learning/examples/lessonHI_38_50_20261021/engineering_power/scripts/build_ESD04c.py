from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
e=json.loads((R/'ESD_ground_routes_04b.json').read_text())
e['revision']='04c:04b40,8.95via rejected for actualDMmergey8.6 overlap;40.25,9.3 approved fullgroup screen byMCUagentv8.'
for o in e['operations']:
 if o['id']=='ESD_VBUS_U4_ESCAPE':
  o['points']=[[40.25,10.1],[40.25,9.3]];o['widths']=[.4]
 if o['id']=='V_HI_ESD_VBUS_LEFT':o['xy']=[40.25,9.3]
 if o['id']=='ESD_VBUS_BOTTOM_BRIDGE':o['points'][0]=[40.25,9.3]
e['prerequisites']=[p.replace('40,8.95','40.25,9.3') for p in e['prerequisites']]
e['status']='FULL_GROUP_GEOMETRY_SCREEN_PASSED_AWAIT_NATIVE_AND_REAL_REFERENCE_REVIEW'
e['geometryNotes'].append('Newleftvia copperannulus extends to9.6, touchingownU4VBUSlandlower9.55 by.05; drilltop9.45 remains.10 off copperland. Actualmask/tenting/assembly condition requires explicit aperture check; no falseclaim isolatedannulus or via-in-pad-approvedprocess.')
e['historyRejected']=[dict(file='ESD_ground_routes_04b.json',reason='Via40,8.95 intersects actualDMmergey8.6 horizontal. Previouslocalreview omittedthatsegment. Fullgroupreviewcaughtbeforeexecution.')]
(R/'ESD_ground_routes_04c.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
print('ESD04c saved')
