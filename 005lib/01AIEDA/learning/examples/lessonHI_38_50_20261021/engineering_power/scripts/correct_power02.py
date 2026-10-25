from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA/learning/examples/lessonHI_38_50_20261021/engineering_power')
d=json.loads((R/'power_paths_02.json').read_text())
d['supersedes']='power_paths_02.json: V5_SENSE_C5_R1 TOP path crosses VIN_C2_C3; preserve old file as rejected path history'
old=[o for o in d['operations'] if o['id']=='V5_SENSE_C5_R1'][0]
(R/'readouts/rejected_V5_sense_TOP.json').write_text(json.dumps({'operation':old,'reason':'TOP proposed y16.95 crosses VIN_C2_C3 about25.7356,16.95; discovered before native execution, no fake DRC pass.'},indent=2),encoding='utf-8')
d['operations']=[o for o in d['operations'] if o['id']!='V5_SENSE_C5_R1']
def rt(id,net,layer,points,widths,fr,to,why):return dict(type='route',id=id,net=net,layer=layer,points=points,widths=widths,**{'from':fr,'to':to},purpose=why)
def via(id,net,xy,why):return dict(type='via',id=id,net=net,xy=xy,padstack='L28_VIA030_C060',purpose=why)
d['operations'].extend([
rt('V5_SENSE_TOP_SOURCE','V5','TOP',[[14.4,23.1],[15.5,22]],[.6],'C5.1','V_HI_V5_SENSE_SOURCE','Filtered source, offpad via and no load branch'),
via('V_HI_V5_SENSE_SOURCE','V5',[15.5,22],'Sense offpad source via'),
rt('V5_SENSE_BOTTOM','V5','BOTTOM',[[15.5,22],[15.5,12],[31.8,12],[31.8,19.1]],[.6,.6,.6],'V_HI_V5_SENSE_SOURCE','V_HI_V5_SENSE_END','Go below CIN/U2 hot-return region, not between C3 ground and U2 ground; bounded reference slot must be rechecked'),
via('V_HI_V5_SENSE_END','V5',[31.8,19.1],'Sense offpad end via outside R1 pad'),
rt('V5_SENSE_TOP_END','V5','TOP',[[31.8,19.1],[30.8984,19.1]],[.6],'V_HI_V5_SENSE_END','R1.1','Low impedance V5 branch ends at divider upper node; BUCK_FB stays TOP'),
rt('V5_SENSE_2L_GND_BRIDGE','GND','TOP',[[13.8,18.3],[13.8,15.5],[16.5,15.5]],[.6,.6],'V_HI_C1','V_HI_INPUT_RETURN_BRIDGE','Restore short input GND across BOTTOM sense vertical slot; avoids forcing bulk/source return around entire cut'),
via('V_HI_INPUT_RETURN_BRIDGE','GND',[16.5,15.5],'Ground stitch on right of BOTTOM sense slot')
])
d['holdPoints'].append('Sense branch around lower power region is deliberately long but low impedance; not oscillator/FB high impedance net. Actual feedback stability/load-step hardware check remains open. Two layer GND bridge must be native connected and plane neck/detour reviewed.')
(R/'power_paths_02b.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
print('WROTE corrected02b',len(d['operations']))
